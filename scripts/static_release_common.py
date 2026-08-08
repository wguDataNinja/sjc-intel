#!/usr/bin/env python3
"""
SJC_Intel — Static Release Export Shared Helpers (SilverLeaf Brief v0).

Implements the public projection, content-quality validation, search-index
building, and deterministic release artifacts described in
docs/static_release_data_contract.md and consumed by
scripts/build_static_release.py and scripts/build_static_site.py.

Guarantees:
- public-only output: only the §2A field set is written; unknown fields and
  internal-only fields are rejected;
- deterministic ordering (release order = source date desc, then item id asc);
- content-quality validation with required-copy errors and editorial warnings;
- byte-stable JSON output for identical inputs;
- demo data is never confused with real data (environment tag + isolation).
"""
import hashlib
import json
import re

# --------------------------------------------------------------------------- #
# Stable constants
# --------------------------------------------------------------------------- #

# Generator identity for release-manifest.json. Kept stable (not a git SHA) so
# repeated generation of identical inputs is byte-identical. Overridable by
# the exporter --generator-revision flag for deployment traceability.
GENERATOR_REVISION = "silverleaf-brief-export-1.0"

# Editorial product roles (see publication_common.EDITORIAL_ROLES). Validated
# on public release items so a role typo cannot leak into the public interface.
EDITORIAL_ROLES = ("latest", "browse", "context", "timeline")

RELEASE_SCHEMA_VERSION = "1.0"
SEARCH_INDEX_SCHEMA_VERSION = "1.0"
MANIFEST_VERSION = "1.0"

ENVIRONMENTS = ("real", "demo")

RELEVANCE_IDS = ("in_silverleaf", "near_silverleaf", "countywide_impact")
RELEVANCE_LABELS = {
    "in_silverleaf": "In SilverLeaf",
    "near_silverleaf": "Near SilverLeaf",
    "countywide_impact": "Countywide impact",
}

# v0 resident-facing topic categories. The public interface shows ONLY these
# (never raw taxonomy ids). One display_topic per item; filters and collection
# routes are keyed on it.
V0_TOPICS = {
    "roads_traffic": {
        "label": "Roads & Traffic",
        "description": "Road closures, construction, detours, and commute impacts.",
    },
    "utilities_water": {
        "label": "Utilities & Water",
        "description": "Drinking water, sewer, reclaimed water, and utility notices.",
    },
    "emergency_preparedness": {
        "label": "Emergency Preparedness",
        "description": "Hurricane season, alerts, and household readiness guidance.",
    },
    "schools_community": {
        "label": "Schools & Community",
        "description": "Schools, community facilities, and neighborhood life.",
    },
    "local_business": {
        "label": "Local Business",
        "description": "Retail, dining, and services opening or changing in the area.",
    },
}

# SilverLeaf community IDs and adjacency corridors (from registry/communities).
_SILVERLEAF_PLACES = {"silverleaf"}
_SILVERLEAF_NEIGHBORHOOD_PREFIX = "sl_"
_ADJACENCY_CORRIDORS = {"cr_210_corridor", "sr_16_corridor", "us_1_corridor"}

# The exact public item field allowlist (docs/static_release_data_contract.md
# §2A). Unknown keys are rejected at export time.
PUBLIC_ITEM_FIELDS = {
    "public_item_id",
    "title",
    "summary",
    "why_it_matters",
    "source_name",
    "source_url",
    "source_unavailable",
    "source_date",
    "event_date",
    "event_date_label",
    "published_date",
    "relevance",
    "display_topic",
    "role",
    "qualified",
    "qualified_label",
    "lifecycle",
    "lifecycle_label",
    "topic_ids",
    "entity_ids",
    "place_ids",
    "sensitivity_display",
    "verification_display",
    "related_item_ids",
    "release_id",
}

# Internal-only prose/identity keys that must never appear in public output.
# Mirrors scripts/publication_common.py::INTERNAL_ONLY_FIELDS for the release
# projection (the exporter enforces its own allowlist regardless).
INTERNAL_DENYLIST = {
    "_dedupe_key", "_signal", "_beat", "_category", "_app_id",
    "_raw_text", "_pdf_urls", "_map_url", "_district", "_meeting_date",
    "_agenda_item_number", "_action_type", "_origin_run_id",
    "_origin_bundle_id", "_imported_at", "_reviewer",
    "reviewer", "reviewer_notes", "reviewed_at", "review_notes",
    "matched_filters", "matched_entities", "entity_match_basis",
    "escalation", "signal", "queue_id", "source_file",
    "internal_notes", "private_notes",
    "candidate_id", "run_id", "review_status", "publication_status",
    "raw_excerpt", "evidence", "citation", "notes",
}

# Internal patterns that should not appear unexplained in resident-facing copy.
_INTERNAL_CODE_RE = re.compile(
    r"\bSJC-[A-Z0-9]+-\d{8}-\d{4}\b"      # corpus item IDs
    r"|\bCAND-[0-9]{8}-[0-9]{4}\b"        # candidate IDs
    r"|\b(SRCH|PROP|ENT-[A-Z0-9-]+)\b"    # run/proposal/entity internal ids
)
# Planning acronyms that are confusing without a plain-language explanation.
_PLANNING_ACRONYM_RE = re.compile(
    r"\b(SUPMAJ|MAJMOD|CPA\(SS\)|PVZVAR|NZVAR|ZVAR|REZ(?!\d))\b"
)
# Internal field/status tokens that must never surface in copy.
_INTERNAL_TOKEN_RE = re.compile(
    r"\b(_dedupe_key|_signal|_beat|review_status|publication_status|"
    r"candidate_id|run_id|entity_match_basis)\b"
)

# Top-level release.json key set (no reviewer; reviewer lives on the manifest).
RELEASE_TOP_FIELDS = {
    "release_id", "schema_version", "environment", "status", "created_at",
    "published_at", "generator_revision", "source_corpus_input_identity",
    "prior_release_id", "dimensions", "items",
}


# --------------------------------------------------------------------------- #
# Small utilities
# --------------------------------------------------------------------------- #

def normalize_text(text):
    """Lowercase, strip punctuation, collapse whitespace (search index)."""
    if text is None:
        return ""
    out = re.sub(r"[^0-9A-Za-z]+", " ", str(text))
    return re.sub(r"\s+", " ", out).strip().lower()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def deterministic_json(data) -> str:
    """Byte-stable JSON serialization (sorted keys, no trailing spaces)."""
    return json.dumps(data, indent=2, sort_keys=True,
                      ensure_ascii=False, default=str) + "\n"


def is_valid_url(url):
    if not url:
        return False
    s = str(url).strip()
    return s.startswith("http://") or s.startswith("https://")


def _now_iso(now):
    if now:
        return now
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# Relevance derivation
# --------------------------------------------------------------------------- #

def derive_relevance(item, decision=None):
    """Derive a stable relevance id for a corpus item.

    Rule (docs/public_ui_v0_spec.md §10):
    - in_silverleaf: place_ids include silverleaf or an sl_* neighborhood;
    - countywide_impact: countywide scope/place;
    - near_silverleaf: adjacency corridor (CR 210 / SR 16 / US 1) fallback.
    """
    place_ids = [p for p in (item.get("communities") or []) if p]
    if any(p == "silverleaf" or p.startswith(_SILVERLEAF_NEIGHBORHOOD_PREFIX)
           for p in place_ids):
        return "in_silverleaf"
    if item.get("geographic_scope") == "county_wide" or "countywide" in place_ids:
        return "countywide_impact"
    if any(p in _ADJACENCY_CORRIDORS for p in place_ids):
        return "near_silverleaf"
    sl = (decision or {}).get("silverleaf_relevance") or {}
    if sl.get("decision") == "included":
        return "near_silverleaf"
    return "countywide_impact"


# --------------------------------------------------------------------------- #
# Content-quality validation (docs/public_ui_v0_spec.md §6 / data contract §7.4)
# --------------------------------------------------------------------------- #

class ValidationResult:
    def __init__(self, item_id):
        self.item_id = item_id
        self.errors = []    # required content missing / contract violation
        self.warnings = []  # needs editorial revision, not exclusion

    @property
    def ok(self):
        return not self.errors


def _blank(value):
    return value is None or str(value).strip() == ""


def _check_unexplained_acronyms(text, result):
    """Flag internal codes or unexplained planning acronyms in copy."""
    if not text:
        return
    if _INTERNAL_CODE_RE.search(text):
        result.warnings.append("internal code/ID appears in resident-facing copy")
    if _PLANNING_ACRONYM_RE.search(text):
        result.warnings.append(
            "planning acronym (SUPMAJ/REZ/ZVAR/...) appears without plain-language "
            "explanation; needs editorial wording")
    if _INTERNAL_TOKEN_RE.search(text):
        result.warnings.append("internal field/status token appears in copy")


def _check_conditional_wording(record, result):
    """Proposals and under-construction items must use conditional framing."""
    lifecycle = str(record.get("lifecycle") or "").lower()
    if lifecycle not in ("proposed", "under_construction", "provisional", "planned"):
        return
    copy = " ".join([record.get("title") or "",
                     record.get("summary") or "",
                     record.get("why_it_matters") or ""])
    conditional = ("proposed", "planned", "expected", "may", "would", "could",
                   "scheduled", "intends", "seeking", "under review", "targeting",
                   "pending", "subject to", "close to", "in the works")
    if not any(word in copy.lower() for word in conditional):
        result.warnings.append(
            f"lifecycle is '{record.get('lifecycle')}' but copy lacks conditional "
            "wording (proposed/planned/expected/...) for a non-completed state")


def validate_public_item(record):
    """Validate one public release item. Returns ValidationResult.

    Errors (exclude/fail): missing required copy, missing source name/date,
    missing relevance, no topic, missing source URL and unavailable flag both,
    invalid URL, unknown keys, leaked internal fields.
    Warnings (editorial): internal codes/acronyms, missing conditional wording.
    """
    result = ValidationResult(record.get("public_item_id") or "?")

    # Allowlist: unknown public fields must not export.
    unknown = [k for k in record.keys() if k not in PUBLIC_ITEM_FIELDS]
    if unknown:
        result.errors.append(f"unknown/forbidden field(s): {', '.join(sorted(unknown))}")
    leaked = [k for k in record.keys() if k in INTERNAL_DENYLIST]
    if leaked:
        result.errors.append(f"internal-only field(s) present: {', '.join(sorted(leaked))}")
    for k in record.keys():
        if k.startswith("_"):
            result.errors.append(f"underscore-prefixed field present: {k}")

    # Required resident-facing copy.
    for field in ("public_item_id", "title", "summary", "why_it_matters",
                  "source_name", "source_date", "published_date", "relevance",
                  "display_topic"):
        if _blank(record.get(field)):
            result.errors.append(f"missing required field: {field}")

    # Display topic must be a resident-facing v0 category (never a raw id).
    if record.get("display_topic") not in V0_TOPICS:
        result.errors.append(
            f"display_topic '{record.get('display_topic')}' not in "
            f"{sorted(V0_TOPICS)}")

    # Editorial role must be a known product role (latest/browse/context/timeline).
    if record.get("role") is not None and record.get("role") not in EDITORIAL_ROLES:
        result.errors.append(
            f"role '{record.get('role')}' not in {sorted(EDITORIAL_ROLES)}")

    # Qualified items must carry a public-safe label (or the default is used).
    if record.get("qualified") is not None and not isinstance(record.get("qualified"), bool):
        result.errors.append("qualified must be a boolean")

    # Stable public ID shape.
    if not _blank(record.get("public_item_id")):
        pid = str(record["public_item_id"])
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", pid):
            result.errors.append("public_item_id contains unsafe characters")

    # Relevance must be a valid stable id.
    if record.get("relevance") not in RELEVANCE_IDS:
        result.errors.append(
            f"relevance '{record.get('relevance')}' not in {sorted(RELEVANCE_IDS)}")

    # Source URL XOR source_unavailable.
    has_url = is_valid_url(record.get("source_url"))
    unavail = bool(record.get("source_unavailable"))
    if record.get("source_url") and not has_url:
        result.errors.append("source_url is present but not a valid http(s) URL")
    if not has_url and not unavail:
        result.errors.append(
            "no working source_url and source_unavailable is not set")

    # Topics: at least one, non-empty, stable ids.
    topics = record.get("topic_ids") or []
    if not isinstance(topics, list) or not topics:
        result.errors.append("topic_ids must be a non-empty list")
    elif any(_blank(t) for t in topics):
        result.errors.append("topic_ids contains an empty id")

    # At least one relevance/place relationship (relevance id satisfies this).
    # Arrays must be lists.
    for field in ("topic_ids", "entity_ids", "place_ids", "related_item_ids"):
        if field in record and not isinstance(record[field], list):
            result.errors.append(f"{field} must be a list")

    # Editorial wording checks.
    for field in ("title", "summary", "why_it_matters"):
        _check_unexplained_acronyms(record.get(field), result)
    _check_conditional_wording(record, result)

    return result


# --------------------------------------------------------------------------- #
# Search index
# --------------------------------------------------------------------------- #

def build_search_index(release, dimensions):
    """Normalized client-search fields for search-index.json.

    The searchable topic dimension is the v0 display_topic (resident-facing);
    raw taxonomy ids are never exposed to client search.
    """
    entries = []
    for item in release.get("items", []):
        pid = item["public_item_id"]
        display_topic = item.get("display_topic")
        topic_labels = (dimensions.get("display_topics", {})
                        .get(display_topic, {}) or {}).get("label", display_topic or "")
        place_labels = " ".join(
            (dimensions.get("places", {}).get(p, {}) or {}).get("label", p)
            for p in (item.get("place_ids") or []))
        entity_labels = " ".join(
            (dimensions.get("entities", {}).get(e, {}) or {}).get("label", e)
            for e in (item.get("entity_ids") or []))
        tokens = " ".join([
            item.get("title") or "",
            item.get("summary") or "",
            item.get("why_it_matters") or "",
            topic_labels,
            place_labels,
            entity_labels,
            item.get("source_name") or "",
        ])
        entries.append({
            "id": pid,
            "tokens": normalize_text(tokens),
            "title": normalize_text(item.get("title")),
            "summary": normalize_text(item.get("summary")),
            "why_it_matters": normalize_text(item.get("why_it_matters")),
            "topics": [display_topic] if display_topic else [],
            "places": list(item.get("place_ids") or []),
            "entities": list(item.get("entity_ids") or []),
            "source": normalize_text(item.get("source_name")),
            "source_date": item.get("source_date"),
        })
    return {
        "release_id": release.get("release_id"),
        "schema_version": SEARCH_INDEX_SCHEMA_VERSION,
        "environment": release.get("environment"),
        "items": entries,
    }


# --------------------------------------------------------------------------- #
# Release assembly
# --------------------------------------------------------------------------- #

def order_items(items):
    """Deterministic release order: source date descending, then item id asc.

    Items without a source_date sort after dated items (still deterministic,
    ordered by id). Stable sorts keep the id-ascending tie-break within equal
    source dates (docs/static_release_data_contract.md §6).
    """
    dated = [it for it in items if it.get("source_date")]
    undated = [it for it in items if not it.get("source_date")]
    dated.sort(key=lambda it: str(it["public_item_id"]))        # id asc tie-break
    dated.sort(key=lambda it: str(it["source_date"]), reverse=True)  # date desc
    undated.sort(key=lambda it: str(it["public_item_id"]))
    return dated + undated


def compute_related_item_ids(release_items):
    """Map each item to sibling public_item_ids sharing a topic or entity.

    Deterministic: for each item, siblings are those sharing >=1 topic_id or
    entity_id, in release order, excluding the item itself.
    """
    by_topic = {}
    by_entity = {}
    for it in release_items:
        pid = it["public_item_id"]
        for t in it.get("topic_ids") or []:
            by_topic.setdefault(t, []).append(pid)
        for e in it.get("entity_ids") or []:
            by_entity.setdefault(e, []).append(pid)

    related = {}
    for it in release_items:
        pid = it["public_item_id"]
        siblings = set()
        for t in it.get("topic_ids") or []:
            siblings.update(by_topic.get(t, []))
        for e in it.get("entity_ids") or []:
            siblings.update(by_entity.get(e, []))
        siblings.discard(pid)
        related[pid] = [s for s in release_items
                        if s["public_item_id"] in siblings]
    return related


# --------------------------------------------------------------------------- #
# Artifact writing
# --------------------------------------------------------------------------- #

def write_artifacts(out_dir, release, search_index, reviewer=None):
    """Write release.json + search-index.json and return (paths, checksums).

    Writes release.json and search-index.json, then computes checksums, then
    writes release-manifest.json containing those checksums. Returns
    (artifact_paths, checksums, manifest).

    `reviewer` is recorded on the manifest only (data contract §8 denylist:
    reviewer identity is never part of the public release.json).
    """
    import os

    os.makedirs(out_dir, exist_ok=True)

    release_path = os.path.join(out_dir, "release.json")
    search_path = os.path.join(out_dir, "search-index.json")
    manifest_path = os.path.join(out_dir, "release-manifest.json")

    release_bytes = deterministic_json(release).encode("utf-8")
    search_bytes = deterministic_json(search_index).encode("utf-8")

    with open(release_path, "w", encoding="utf-8") as f:
        f.write(release_bytes.decode("utf-8"))
    with open(search_path, "w", encoding="utf-8") as f:
        f.write(search_bytes.decode("utf-8"))

    checksums = {
        "release.json": sha256_bytes(release_bytes),
        "search-index.json": sha256_bytes(search_bytes),
    }

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "release_id": release["release_id"],
        "environment": release["environment"],
        "release_status": release.get("status"),
        "created_at": release["created_at"],
        "published_at": release.get("published_at"),
        "generator_revision": release.get("generator_revision"),
        "source_corpus_input_identity": release.get("source_corpus_input_identity"),
        "reviewer": reviewer,
        "item_ids": [it["public_item_id"] for it in release.get("items", [])],
        "checksums": checksums,
        "prior_release_id": release.get("prior_release_id"),
        "rollback_reference": release.get("prior_release_id"),
    }
    manifest = {k: v for k, v in manifest.items() if v is not None}

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(deterministic_json(manifest))

    return {"release.json": release_path, "search-index.json": search_path,
            "release-manifest.json": manifest_path}, checksums, manifest


def build_release_dict(release_id, environment, items, dimensions, *,
                       published_at, created_at, generator_revision,
                       source_identity, prior_release_id=None,
                       status="published"):
    """Assemble the top-level release.json dict (no reviewer on this artifact)."""
    ordered = order_items(items)
    return {
        "release_id": release_id,
        "schema_version": RELEASE_SCHEMA_VERSION,
        "environment": environment,
        "status": status,
        "created_at": created_at,
        "published_at": published_at,
        "generator_revision": generator_revision,
        "source_corpus_input_identity": source_identity,
        "prior_release_id": prior_release_id,
        "dimensions": dimensions,
        "items": ordered,
    }
