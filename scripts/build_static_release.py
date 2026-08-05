#!/usr/bin/env python3
"""
SJC_Intel — Static Release Exporter (SilverLeaf Brief v0).

Completes ROADMAP.md §3B-G2: produces deterministic public release artifacts
for the v0 static site per docs/static_release_data_contract.md:

  site/data/releases/{release-id}/release.json
  site/data/releases/{release-id}/search-index.json
  site/data/releases/{release-id}/release-manifest.json

Modes:
  real  python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001
        Runs the full corpus validator, the deterministic publication selector,
        projects approved+reviewed+SilverLeaf-included items, and validates
        content quality. May validly produce zero selected items (no
        publication decisions yet).
  demo  python3 scripts/build_static_release.py --release-id SJC-REL-DEMO-20260804 --demo
        Builds a clearly nonproduction demo release from explicit fixtures
        under site/fixtures/demo/ into site/data/demo/. Demo output is labeled
        environment=demo and is isolated from production releases.

--check performs no writes and reports whether the build would succeed.
The exporter NEVER marks items published and NEVER creates a publication
decision; release membership is a separate human act.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publication_common import (  # noqa: E402
    is_valid_url,
    iter_intel_items,
    item_date,
    load_all_decisions,
    load_sources,
    public_projection,
)
from static_release_common import (  # noqa: E402
    ENVIRONMENTS,
    GENERATOR_REVISION,
    INTERNAL_DENYLIST,
    PUBLIC_ITEM_FIELDS,
    RELEASE_SCHEMA_VERSION,
    RELEVANCE_LABELS,
    V0_TOPICS,
    build_release_dict,
    build_search_index,
    compute_related_item_ids,
    derive_relevance,
    deterministic_json,
    order_items,
    sha256_bytes,
    validate_public_item,
    write_artifacts,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DEMO_OUT = os.path.join(REPO_ROOT, "site", "data", "demo")
DEFAULT_REAL_OUT = os.path.join(REPO_ROOT, "site", "data", "releases")
DEFAULT_DEMO_FIXTURE = os.path.join(REPO_ROOT, "site", "fixtures", "demo", "release.yaml")

# Friendly topic labels for resident-facing filter chips and cards.
TOPIC_LABELS = {
    "county_government": "County government",
    "public_safety": "Public safety",
    "crime": "Crime",
    "education": "Schools & education",
    "development": "Development",
    "infrastructure": "Infrastructure",
    "environment": "Environment",
    "transportation": "Transportation & roads",
    "community_events": "Community events",
    "public_notices": "Public notices",
    "emergency_alerts": "Emergency alerts",
    "economic_development": "Local business",
    "parks_recreation": "Parks & recreation",
    "library": "Library",
    "coastal_projects": "Coastal projects",
    "organizational_excellence": "Awards & recognition",
    "community_trust": "Community trust",
    "health_wellness": "Health & wellness",
    "water_restrictions": "Water restrictions",
    "budget_millage": "Budget & millage",
    "housing": "Housing",
    "taxes": "Taxes",
    "elections": "Elections",
    "cdd_governance": "CDD governance",
    "general_government": "General government",
}

VERIFICATION_DISPLAY = {
    "source_confirmed": "Confirmed from source",
    "cross_referenced": "Cross-referenced with another source",
    "fact_checked": "Fact-checked against source",
    "unverified": "Source not yet independently verified",
}

SOURCE_TYPE_LABELS = {
    "wordpress_blog": "Government / agency website",
    "official_records": "Official records",
    "local_media": "Local news",
    "social_media": "Social media",
    "government_meeting": "Government meeting records",
    "rss": "Official news feed",
}

# Standardized resident-facing source names (never expose internal registry
# labels such as "SJC County News" or "Emergency Management and Alerts").
PUBLIC_SOURCE_NAMES = {
    "sjc_county_news": "St. Johns County",
    "sjc_utility_department": "St. Johns County Utility Department",
    "sjc_emergency_management": "St. Johns County Emergency Management",
    "sjc_nbor_public_notices": "St. Johns County Neighborhood Board of Review",
    "sjc_school_district": "St. Johns County School District",
    "st_johns_citizen": "St. Johns Citizen",
}

# Per-source kind label shown with the source name in the Data & Sources table.
PUBLIC_SOURCE_KINDS = {
    "sjc_county_news": "County news release",
    "sjc_utility_department": "Utility notice",
    "sjc_emergency_management": "Emergency-management guidance",
    "sjc_nbor_public_notices": "Public notice",
    "sjc_school_district": "School district update",
    "st_johns_citizen": "Local news",
}


def _public_source_name(source_id, fallback):
    return PUBLIC_SOURCE_NAMES.get(source_id, fallback)


# Deterministic fallback: primary taxonomy topic -> v0 resident category.
V0_FROM_TOPIC = {
    "transportation": "roads_traffic",
    "roadwork_traffic": "roads_traffic",
    "infrastructure": "utilities_water",
    "water_restrictions": "utilities_water",
    "environment": "utilities_water",
    "health_wellness": "utilities_water",
    "emergency_alerts": "emergency_preparedness",
    "public_safety": "emergency_preparedness",
    "education": "schools_community",
    "development": "local_business",
    "economic_development": "local_business",
}


def _derive_display_topic(item):
    primary = item.get("primary_topic") or (item.get("topics") or [None])[0]
    return V0_FROM_TOPIC.get(primary, "utilities_water")


def build_display_topics(items):
    """Return the v0 resident-topic dimension entries present in a release."""
    present = {}
    for it in items:
        dt = it.get("display_topic")
        if dt and dt in V0_TOPICS:
            present[dt] = dict(V0_TOPICS[dt])
    return present


# --------------------------------------------------------------------------- #
# Real-mode projection
# --------------------------------------------------------------------------- #

def _source_date(item):
    for key in ("source_published_at", "discovered_at", "created_at"):
        val = item.get(key)
        if val:
            return str(val)[:10]
    return None


def _verification_display(item):
    vs = item.get("verification_status")
    if vs in VERIFICATION_DISPLAY:
        return VERIFICATION_DISPLAY[vs]
    if vs:
        return "Reviewed from source"
    return "Reviewed from source"


def project_item(item, decision, release_id):
    """Map a selected corpus item + decision to a public release item (§2A)."""
    proj = public_projection(item, decision)
    date_val = _source_date(item)
    lifecycle = decision.get("lifecycle") if decision else None
    lifecycle_label = decision.get("lifecycle_label") if decision else None
    event_date = decision.get("event_date") if decision else None
    event_date_label = decision.get("event_date_label") if decision else None

    # Editorial overrides (never alter the source intelligence record).
    title = (decision or {}).get("public_title_override") or proj["title"]
    why = ((decision or {}).get("public_why_override")
           or (item.get("resident_relevance") or {}).get("why_it_matters")
           or proj["summary"])
    source_name = _public_source_name(item.get("source_id"), proj["source_name"])
    display_topic = (decision or {}).get("display_topic")
    if display_topic not in V0_TOPICS:
        display_topic = _derive_display_topic(item)

    record = {
        "public_item_id": proj["item_id"],
        "title": title,
        "summary": proj["summary"],
        "why_it_matters": why,
        "source_name": source_name,
        "source_date": date_val,
        "published_date": str((decision or {}).get("decision_timestamp") or "")[:10],
        "relevance": (decision or {}).get("relevance") or derive_relevance(item, decision),
        "display_topic": display_topic,
        "topic_ids": list(proj["topics"] or []),
        "entity_ids": list(proj["entity_ids"] or []),
        "place_ids": list(proj["place_ids"] or []),
        "sensitivity_display": "reviewed_sensitive"
        if proj.get("sensitivity") in ("medium", "high") else "none",
        "verification_display": _verification_display(item),
        "release_id": release_id,
    }
    if is_valid_url(proj.get("source_url")):
        record["source_url"] = proj["source_url"]
    else:
        record["source_unavailable"] = True
    if lifecycle:
        record["lifecycle"] = lifecycle
        if lifecycle_label:
            record["lifecycle_label"] = lifecycle_label
    if event_date:
        record["event_date"] = event_date
        if event_date_label:
            record["event_date_label"] = event_date_label
    return record


# --------------------------------------------------------------------------- #
# Dimensions
# --------------------------------------------------------------------------- #

def _dimensions(original_items, projected_items):
    """Build the self-describing dimensions block from registry + items.

    `original_items` carry source_id/topics (registry lookups); `projected_items`
    carry display_topic. The public interface exposes only the v0 display
    topics; granular taxonomy ids never appear without a label.
    """
    sources = load_sources()
    relevance = {rid: {"label": label}
                 for rid, label in sorted(RELEVANCE_LABELS.items())}

    display_topics = build_display_topics(projected_items)

    # Granular topic ids must ALL have a resident label (raw-id leak guard).
    for it in original_items:
        for t in it.get("topics") or []:
            if t not in TOPIC_LABELS:
                raise ReleaseExportError(
                    f"topic '{t}' on {it['item_id']} has no resident-facing label; "
                    "raw taxonomy ids must never reach the public interface")

    places = {}
    try:
        import yaml
        with open(os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "registry", "communities.yaml")) as f:
            comm = yaml.safe_load(f)
        comm_map = {c["id"]: c for c in comm.get("communities", [])}
    except Exception:
        comm_map = {}
    for it in original_items:
        for p in it.get("communities") or []:
            rec = comm_map.get(p)
            places[p] = {"label": (rec or {}).get("name", p)}
            if rec and rec.get("type"):
                places[p]["type"] = rec["type"]

    entities = {}
    try:
        import yaml
        with open(os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "registry", "tracked_entities.yaml")) as f:
            ent = yaml.safe_load(f)
        ent_map = {e["entity_id"]: e for e in ent.get("tracked_entities", [])}
    except Exception:
        ent_map = {}
    for it in original_items:
        for e in it.get("tracked_entity_ids") or []:
            rec = ent_map.get(e)
            entry = {"label": (rec or {}).get("label", e)}
            if rec and rec.get("lifecycle_status"):
                entry["lifecycle"] = rec["lifecycle_status"]
                entry["lifecycle_label"] = _lifecycle_label(rec["lifecycle_status"])
            if rec and rec.get("description"):
                entry["description"] = str(rec["description"]).strip()
            entities[e] = entry

    src_entries = {}
    for it in original_items:
        sid = it.get("source_id")
        if not sid:
            continue
        rec = sources.get(sid) or {}
        entry = {
            "name": _public_source_name(sid, rec.get("name") or sid),
            "source_kind": PUBLIC_SOURCE_KINDS.get(sid, rec.get("source_type") or ""),
        }
        if rec.get("url"):
            entry["url"] = rec["url"]
        if rec.get("source_type"):
            entry["source_type"] = SOURCE_TYPE_LABELS.get(
                rec["source_type"], rec["source_type"])
        src_entries[sid] = entry

    return {
        "relevance": relevance,
        "display_topics": display_topics,
        "places": places,
        "entities": entities,
        "sources": src_entries,
    }


def _lifecycle_label(status):
    return {
        "proposed": "Proposed",
        "under_construction": "Under construction",
        "completed": "Completed",
        "approved": "Approved",
        "tracked": "Tracked",
        "provisional": "Provisional",
    }.get(status, str(status).replace("_", " ").title())


# --------------------------------------------------------------------------- #
# Demo mode
# --------------------------------------------------------------------------- #

def _load_fixture(path):
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)


def build_demo_release(fixture_path, release_id, published_at, created_at,
                       reviewer, generator_revision):
    """Assemble a demo release dict from an explicit fixture."""
    data = _load_fixture(fixture_path)
    meta = data.get("release_metadata") or {}
    dimensions = dict(data.get("dimensions") or {})
    items = list(data.get("items") or [])

    env_release_id = release_id or meta.get("release_id")
    pub = published_at or meta.get("published_at")
    cre = created_at or meta.get("created_at")
    rev = reviewer or meta.get("reviewer")
    prior = meta.get("prior_release_id")

    # Validate content quality first; errors block the build.
    validation = [validate_public_item(it) for it in items]
    errors = [r for r in validation if not r.ok]
    warnings = [w for r in validation for w in r.warnings]
    if errors:
        raise ReleaseExportError(
            "demo fixture content-quality errors:\n" +
            "\n".join(f"  {r.item_id}: {err}" for r in errors for err in r.errors))

    # The public topic dimension is always the v0 display-topics layer.
    dimensions["display_topics"] = build_display_topics(items)

    related = compute_related_item_ids(items)
    for it in items:
        it["related_item_ids"] = [
            rel["public_item_id"] for rel in related[it["public_item_id"]]
        ]

    identity = sha256_bytes(
        "\n".join(sorted(it["public_item_id"] for it in items)).encode("utf-8"))

    release = build_release_dict(
        env_release_id, "demo", items, dimensions,
        published_at=pub, created_at=cre,
        generator_revision=generator_revision,
        source_identity=identity,
        prior_release_id=prior,
    )
    return release, rev, warnings


class ReleaseExportError(Exception):
    pass


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="SJC static release exporter (§3B-G2).")
    ap.add_argument("--release-id", required=True, help="release id, e.g. SJC-REL-2026-08-001")
    ap.add_argument("--demo", action="store_true",
                    help="build a nonproduction demo release from site/fixtures/demo")
    ap.add_argument("--fixture", default=DEFAULT_DEMO_FIXTURE,
                    help="demo fixture path (default site/fixtures/demo/release.yaml)")
    ap.add_argument("--out-dir", default=None,
                    help="override output directory (default site/data/demo or site/data/releases/<id>)")
    ap.add_argument("--check", action="store_true",
                    help="validate + report only; write nothing")
    ap.add_argument("--published-at", default=None, help="ISO-8601 published_at override")
    ap.add_argument("--now", default=None, help="ISO-8601 created_at override (byte-stable builds)")
    ap.add_argument("--reviewer", default=None, help="manifest reviewer identity (real releases)")
    ap.add_argument("--generator-revision", default=GENERATOR_REVISION)
    ap.add_argument("--window-start", default=None, help="release window start (real mode)")
    ap.add_argument("--window-end", default=None, help="release window end (real mode)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if args.demo:
        out_dir = args.out_dir or DEFAULT_DEMO_OUT
    else:
        out_dir = args.out_dir or os.path.join(DEFAULT_REAL_OUT, args.release_id)

    try:
        if args.demo:
            release, reviewer, warnings = build_demo_release(
                args.fixture, args.release_id, args.published_at, args.now,
                args.reviewer, args.generator_revision)
        else:
            release, reviewer, warnings = build_real_release(
                args.release_id, args.generator_revision, args)
    except ReleaseExportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    search_index = build_search_index(release, release["dimensions"])
    count = len(release["items"])

    result = {
        "mode": "demo" if args.demo else "real",
        "release_id": release["release_id"],
        "environment": release["environment"],
        "item_count": count,
        "out_dir": out_dir,
        "warnings": warnings,
        "checksums_would_write": {k: sha256_bytes(deterministic_json(v).encode("utf-8"))
                                  for k, v in (("release.json", release),
                                               ("search-index.json", search_index))},
    }

    if args.check:
        print(json.dumps(result, indent=2, sort_keys=True))
        if warnings:
            print("Warnings (editorial):", file=sys.stderr)
            for w in warnings:
                print(f"  - {w}", file=sys.stderr)
        print(f"CHECK: {'READY' if not warnings else 'READY_WITH_WARNINGS'} — "
              f"{count} item(s) for {release['release_id']}; no files written.",
              file=sys.stderr)
        sys.exit(0)

    paths, checksums, manifest = write_artifacts(
        out_dir, release, search_index, reviewer=reviewer)
    result["written"] = paths
    result["checksums"] = checksums

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Built {release['environment']} release: {release['release_id']}")
        print(f"  items:      {count}")
        print(f"  output:     {out_dir}")
        print(f"  release.json:        {paths['release.json']}")
        print(f"  search-index.json:   {paths['search-index.json']}")
        print(f"  release-manifest.json: {paths['release-manifest.json']}")
        if warnings:
            print("  warnings (editorial revision):")
            for w in warnings:
                print(f"    - {w}")
        if release["environment"] == "demo":
            print("  NOTE: demo release — nonproduction fixture data.")


def build_real_release(release_id, generator_revision, args):
    """Full real-release pipeline: validate corpus -> select -> project -> validate."""
    from datetime import datetime, timezone
    from select_publication_items import selector
    from validate_publication_corpus import CorpusValidator

    v = CorpusValidator()
    summary = v.run()
    if summary["errors"]:
        raise ReleaseExportError(
            f"corpus validation failed ({summary['errors']} blocking errors); "
            "release export blocked. See validate_publication_corpus.py --json")

    def _parse_window(val):
        if not val:
            return None
        s = str(val).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    decisions = load_all_decisions()
    items = list(iter_intel_items())
    sel = selector(decisions, items,
                   window_start=_parse_window(args.window_start),
                   window_end=_parse_window(args.window_end))
    selected_ids = sel["selected"]

    # Locate items + decisions for selected ids.
    by_id = {}
    for rel, item in items:
        by_id.setdefault(item["item_id"], item)

    public_items = []
    for pid in selected_ids:
        item = by_id.get(pid)
        if not item:
            raise ReleaseExportError(f"selected item {pid} not found in corpus")
        decision = decisions.get(pid)
        public_items.append(project_item(item, decision, release_id))

    related = compute_related_item_ids(public_items)
    for it in public_items:
        it["related_item_ids"] = [
            rel["public_item_id"] for rel in related[it["public_item_id"]]
        ]

    # Content-quality validation: errors block the build.
    validation = [validate_public_item(it) for it in public_items]
    errors = [r for r in validation if not r.ok]
    warnings = [w for r in validation for w in r.warnings]
    if errors:
        raise ReleaseExportError(
            "content-quality errors in selected items:\n" +
            "\n".join(f"  {r.item_id}: {err}" for r in errors for err in r.errors))

    dimensions = _dimensions(
        [by_id[pid] for pid in selected_ids], public_items)

    now = args.now
    if not now:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    published = args.published_at or now
    identity = sha256_bytes(
        "\n".join(sorted(pid for pid in selected_ids)).encode("utf-8"))

    release = build_release_dict(
        release_id, "real", public_items, dimensions,
        published_at=published, created_at=now,
        generator_revision=generator_revision,
        source_identity=identity,
    )
    if not args.reviewer:
        raise ReleaseExportError(
            "real release export requires an explicit --reviewer identity "
            "(recorded on the release manifest only)")
    return release, args.reviewer, warnings


if __name__ == "__main__":
    main()
