#!/usr/bin/env python3
"""
SJC_Intel — Publication-decision shared helpers.

Supports the file-backed publication-decision model, corpus validation, and
the deterministic publication selector (docs/publication_release_contract.md,
ROADMAP.md §3A-G2).

Semantics:
- ``review_status: verified`` is never a publication authorization.
- A publication decision file under ``data/publication_decisions/`` is the
  authoritative file-backed record of an explicit human decision.
- ``published`` is a release-level state owned by the release manifest, never
  set by decision/selector tooling.
"""
import os
import re
import sys
import glob
import yaml
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Allow tests and alternate environments to point the file-backed corpus
# elsewhere without touching the authoritative data/ tree.
_DATA_ROOT = os.environ.get("SJC_INTEL_DATA_ROOT", os.path.join(REPO_ROOT, "data"))
_REG_ROOT = os.environ.get("SJC_INTEL_REGISTRY_ROOT", os.path.join(REPO_ROOT, "registry"))

INTEL_ITEMS_DIR = os.path.join(_DATA_ROOT, "intel_items")
SOURCE_EVENTS_DIR = os.path.join(_DATA_ROOT, "source_events")
DECISIONS_DIR = os.path.join(_DATA_ROOT, "publication_decisions")
LEGACY_EXCEPTIONS_FILE = os.path.join(DECISIONS_DIR, "legacy_exceptions.yaml")
SOURCES_FILE = os.path.join(_REG_ROOT, "sources.yaml")
COMMUNITIES_FILE = os.path.join(_REG_ROOT, "communities.yaml")
ENTITIES_FILE = os.path.join(_REG_ROOT, "tracked_entities.yaml")

DECISION_SCHEMA_VERSION = "1.0"

# Item-level publication decision statuses. ``published`` is reserved for
# release-level membership and is intentionally absent here.
PUBLICATION_STATUSES = ("approved", "rejected", "deferred", "withdrawn")

SILVERLEAF_DECISIONS = ("included", "excluded", "needs_review", "not_assessed")

VALID_SENSITIVITIES = ("low", "medium", "high")

CANONICAL_REVIEW_STATUSES = {
    "pending_review", "in_review", "verified", "needs_followup",
    "rejected_noise", "duplicate", "escalated", "archived",
}

# Item ID format for the SJC corpus (publication-relevant records).
# Legacy records (e.g. CDD items) predate this format and are documented in
# legacy_exceptions.yaml.
ITEM_ID_RE = re.compile(r"^SJC-[A-Z0-9]+-\d{8}-\d{4}$")

# Fields that must never appear in a public projection, regardless of source.
INTERNAL_ONLY_FIELDS = {
    "_dedupe_key", "_signal", "_beat", "_category", "_app_id",
    "_raw_text", "_pdf_urls", "_map_url", "_district", "_meeting_date",
    "_agenda_item_number", "_action_type", "_origin_run_id",
    "_origin_bundle_id", "_imported_at", "_reviewer",
    "reviewer", "reviewer_notes", "reviewed_at", "review_notes",
    "matched_filters", "matched_entities", "entity_match_basis",
    "escalation", "signal", "queue_id", "source_file",
    "internal_notes", "private_notes",
}

# Public fields explicitly allowed in a release item projection.
PUBLIC_FIELD_ALLOWLIST = {
    "item_id", "title", "summary", "why_it_matters", "source_name",
    "source_url", "source_published_at", "published_at", "topics",
    "primary_topic", "entity_ids", "place_ids", "sensitivity",
    "sensitivity_display", "verification_display", "related_item_ids",
    "release_id", "verification_status", "residents_affected",
    "citation_source_name", "communities",
}

TOPIC_VOCABULARY = {
    "county_government", "public_safety", "crime", "education",
    "development", "infrastructure", "environment", "transportation",
    "community_events", "public_notices", "emergency_alerts",
    "economic_development", "parks_recreation", "library",
    "coastal_projects", "organizational_excellence", "community_trust",
    "health_wellness", "water_restrictions", "budget_millage", "housing",
    "taxes", "elections", "cdd_governance", "general_government",
}


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_legacy_exceptions():
    """Return the documented legacy-exception record, or None."""
    if not os.path.exists(LEGACY_EXCEPTIONS_FILE):
        return None
    try:
        return load_yaml(LEGACY_EXCEPTIONS_FILE)
    except Exception:
        return None


def legacy_suppressed_for(exception_id):
    """Return the set of check codes suppressed by a legacy exception."""
    ex = load_legacy_exceptions()
    if not ex:
        return set()
    for entry in ex.get("legacy_exceptions", []):
        if entry.get("id") == exception_id:
            return set(entry.get("suppress", []))
    return set()


def legacy_exception_for_item(item_id):
    """Return the exception id covering an item, or None."""
    ex = load_legacy_exceptions()
    if not ex:
        return None
    for entry in ex.get("legacy_exceptions", []):
        if item_id in entry.get("item_ids", []):
            return entry.get("id")
    return None


def legacy_treatment_for_item(item_id):
    """Return the treatment of the legacy exception covering an item, or None.

    Treatment is the machine-readable reason recorded in
    legacy_exceptions.yaml (e.g. warning_timestamp_default). Release blocking
    is decided by the selector using these treatments.
    """
    ex = load_legacy_exceptions()
    if not ex:
        return None
    for entry in ex.get("legacy_exceptions", []):
        if item_id in entry.get("item_ids", []):
            return entry.get("treatment")
    return None


def iter_intel_items():
    """Yield (rel_path, item) for every intel item record in the corpus."""
    for fpath in sorted(glob.glob(os.path.join(INTEL_ITEMS_DIR, "*", "*.yaml"))):
        if fpath.endswith(".deprecated") or ".deprecated" in fpath:
            continue
        try:
            data = load_yaml(fpath)
        except Exception:
            continue
        recs = data.get("items") if isinstance(data, dict) else data
        if not isinstance(recs, list):
            continue
        rel = os.path.relpath(fpath, REPO_ROOT)
        for item in recs:
            if isinstance(item, dict) and item.get("item_id"):
                yield rel, item


def load_sources():
    if not os.path.exists(SOURCES_FILE):
        return {}
    data = load_yaml(SOURCES_FILE)
    return {s["source_id"]: s for s in data.get("sources", []) if s.get("source_id")}


def load_communities():
    if not os.path.exists(COMMUNITIES_FILE):
        return set()
    data = load_yaml(COMMUNITIES_FILE)
    return {c["id"] for c in data.get("communities", []) if c.get("id")}


def load_entities():
    if not os.path.exists(ENTITIES_FILE):
        return set()
    data = load_yaml(ENTITIES_FILE)
    return {e["entity_id"] for e in data.get("tracked_entities", []) if e.get("entity_id")}


def load_source_events():
    """Return set of known event_ids."""
    events = set()
    for fpath in sorted(glob.glob(os.path.join(SOURCE_EVENTS_DIR, "*", "*.yaml"))):
        try:
            data = load_yaml(fpath)
        except Exception:
            continue
        recs = data.get("events") or data.get("items") or []
        for r in recs:
            if isinstance(r, dict) and r.get("event_id"):
                events.add(r["event_id"])
    return events


def decision_path(item_id):
    return os.path.join(DECISIONS_DIR, f"{item_id}.yaml")


def load_decision(item_id):
    path = decision_path(item_id)
    if not os.path.exists(path):
        return None
    try:
        return load_yaml(path)
    except Exception:
        return None


def load_all_decisions():
    """Return dict item_id -> decision record."""
    decisions = {}
    for fpath in sorted(glob.glob(os.path.join(DECISIONS_DIR, "*.yaml"))):
        base = os.path.basename(fpath)
        if base == "legacy_exceptions.yaml":
            continue
        try:
            data = load_yaml(fpath)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("item_id"):
            decisions[data["item_id"]] = data
    return decisions


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(ts):
    if not ts:
        return None
    s = str(ts).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def item_date(item):
    """Deterministic date used for release-window evaluation."""
    for key in ("source_published_at", "discovered_at", "created_at"):
        dt = parse_iso(item.get(key))
        if dt:
            return dt
    return None


def is_valid_url(url):
    if not url:
        return False
    s = str(url).strip()
    return s.startswith("http://") or s.startswith("https://")


def public_projection(item, decision=None):
    """Build the public-safe projection of an item for a release.

    Never mutates input. Excludes internal-only fields and derives display
    fields from reviewed state.
    """
    out = {}
    title = item.get("title")
    summary = item.get("summary")
    if decision and decision.get("public_summary_override"):
        summary = decision["public_summary_override"]
    out["item_id"] = item.get("item_id")
    out["title"] = title
    out["summary"] = summary
    rr = item.get("resident_relevance") or {}
    out["why_it_matters"] = rr.get("why_it_matters") or summary
    sources = load_sources()
    src = sources.get(item.get("source_id")) or {}
    out["source_name"] = src.get("name") or item.get("citation", {}).get("source_name")
    out["source_url"] = item.get("source_url")
    out["source_published_at"] = item.get("source_published_at")
    out["published_at"] = (decision or {}).get("decision_timestamp")
    out["topics"] = item.get("topics", [])
    out["primary_topic"] = item.get("primary_topic")
    out["entity_ids"] = item.get("tracked_entity_ids", [])
    out["place_ids"] = item.get("communities", [])
    out["communities"] = item.get("communities", [])
    out["sensitivity"] = item.get("sensitivity")
    out["verification_status"] = item.get("verification_status")
    return out


def validate_public_safe(projection):
    """Return list of internal-only field names leaked in a projection."""
    leaked = []
    for k in projection:
        if k in INTERNAL_ONLY_FIELDS:
            leaked.append(k)
    return leaked
