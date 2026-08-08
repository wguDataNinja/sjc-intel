"""Deterministic, side-effect-free publication policy classifier.

The policy authority is docs/PUBLICATION_POLICY.md.  Classification is derived
from canonical corpus fields and any existing human publication decision; it
does not rewrite evidence, review status, or decision records.
"""
from publication_common import (
    is_valid_url,
    item_date,
    legacy_treatment_for_item,
    validate_public_safe,
    public_projection,
)

AUTO_PUBLISHABLE = "AUTO_PUBLISHABLE"
NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
EXCLUDE = "EXCLUDE"
NEEDS_MORE_RESEARCH = "NEEDS_MORE_RESEARCH"

CLASSIFICATIONS = (
    AUTO_PUBLISHABLE, NEEDS_HUMAN_REVIEW, EXCLUDE, NEEDS_MORE_RESEARCH,
)

# These feeds carry either high-volume boilerplate or agenda-level material.
# Their records need a concrete SilverLeaf/corridor/entity signal before a
# default policy can call them resident-relevant.
CONTEXT_REQUIRED_SOURCES = {"sjc_nbor_public_notices", "sjc_bcc_calendar"}

OFFICIAL_SOURCE_TYPES = {
    "wordpress_blog", "official_records", "government_meeting", "rss",
    "government_website", "government_portal", "wordpress_portal",
}

# Editorial product roles that represent durable, non-current content.
# ``browse``/``context``/``timeline`` items are not "fresh event notices" and
# are exempt from the stale-timely rule so completed projects and historical
# milestones can live in Browse/context without repeated human exceptions.
DURABLE_ROLES = {"browse", "context", "timeline"}

# Corroboration evidence kinds recorded on an approved publication decision
# (data/publication_decisions/<id>.yaml -> corroboration[].kind).
OFFICIAL_CORROBORATION_KINDS = {"official", "first_party"}
LOCAL_MEDIA_CORROBORATION_KIND = "local_media"

RESIDENT_TOPICS = {
    "county_government", "development", "infrastructure", "transportation",
    "education", "economic_development", "health_wellness",
    "water_restrictions", "emergency_alerts", "parks_recreation", "library",
    "public_notices", "community_services", "public_services", "taxes",
    "budget_millage", "housing", "environment", "coastal_projects",
}

SENSITIVE_TOPICS = {"crime", "public_safety", "elections"}
SENSITIVE_WORDS = {
    "arrest", "arrested", "charged", "alleged", "allegation", "inmate",
    "minor", "murder", "shooting", "victim", "incident", "injury",
}

BLOCKING_LEGACY_TREATMENTS = {
    "non_canonical_duplicate_capture", "retained_as_archival_evidence",
    "legacy_incomplete_record", "needs_registry_fix",
}


def _decision_status(decision):
    return (decision or {}).get("publication_status")


def _resident_scope(item, decision):
    """Return (is_established, reason) without relying on keyword guesswork."""
    decision_scope = ((decision or {}).get("silverleaf_relevance") or {}).get("decision")
    if decision_scope == "included":
        return True, "human_relevance_override"
    if decision_scope in {"excluded", "needs_review", "not_assessed"}:
        return False, f"human_relevance:{decision_scope}"

    places = set(item.get("communities") or [])
    if places & {"silverleaf", "cr_210_corridor", "sr_16_corridor", "countywide"}:
        return True, "registered_resident_scope"
    if item.get("tracked_entity_ids"):
        return True, "tracked_entity_scope"

    # A low-sensitivity official countywide household item can be useful by
    # default, but only when its structured topic and resident explanation are
    # both present.  This deliberately rejects generic notices without a
    # product-relevance signal.
    topic = item.get("primary_topic") or next(iter(item.get("topics") or []), None)
    relevance = item.get("resident_relevance") or {}
    why = str(relevance.get("why_it_matters") or "").strip()
    audiences = set(relevance.get("affected_audiences") or [])
    if (item.get("geographic_scope") == "county_wide" and topic in RESIDENT_TOPICS
            and len(why) >= 24 and audiences & {"residents", "homeowners", "commuters"}):
        return True, "structured_countywide_household_scope"
    return False, "missing_resident_scope"


def _corroboration_satisfied(decision):
    """Return True when an approved decision carries adequate corroboration.

    A local-media item may publish when a human recorded corroboration of its
    central fact: at least one official/first-party source, or two or more
    credible independent outlets (docs/PUBLICATION_POLICY.md Model B).
    """
    corr = (decision or {}).get("corroboration") or []
    official = [c for c in corr if c.get("kind") in OFFICIAL_CORROBORATION_KINDS]
    if official:
        return True
    local = [c for c in corr if c.get("kind") == LOCAL_MEDIA_CORROBORATION_KIND]
    return len(local) >= 2


def classify_item(item, decision, sources, as_of=None):
    """Classify one canonical item with ordered, explainable reasons."""
    reasons = []
    status = _decision_status(decision)
    item_id = item.get("item_id")

    if status in {"withdrawn", "rejected"} or (decision or {}).get("withdrawn"):
        return EXCLUDE, ["human_publication_exclusion"]
    if item.get("review_status") in {"rejected_noise", "duplicate", "archived"}:
        return EXCLUDE, [f"review_status:{item.get('review_status')}"]
    if item.get("superseded_by"):
        return EXCLUDE, ["superseded"]
    if legacy_treatment_for_item(item_id) in BLOCKING_LEGACY_TREATMENTS:
        return EXCLUDE, [f"legacy_exception:{legacy_treatment_for_item(item_id)}"]

    if item.get("review_status") != "verified":
        return NEEDS_MORE_RESEARCH, [f"review_status:{item.get('review_status') or 'none'}"]
    if not item.get("source_id") or item.get("source_id") not in sources:
        return NEEDS_MORE_RESEARCH, ["unknown_or_missing_source"]
    if not is_valid_url(item.get("source_url")):
        return NEEDS_MORE_RESEARCH, ["missing_public_source_url"]
    if item.get("verification_status") not in {"source_confirmed", "cross_referenced", "fact_checked"}:
        return NEEDS_MORE_RESEARCH, ["verification_evidence_incomplete"]

    # Timely notices are not silently converted into historical context after
    # their action window. A human can preserve a durable lesson explicitly,
    # either through an approved decision or an explicit durable editorial role
    # (browse/context/timeline). Items marked as durable context are not
    # "expired notices" and do not require repeated human exceptions.
    if item.get("urgency") == "timely" and status != "approved" and as_of is not None:
        dated = item_date(item)
        if dated is not None and (as_of - dated).days > 30:
            role = (decision or {}).get("role")
            if role not in DURABLE_ROLES:
                return NEEDS_HUMAN_REVIEW, ["timely_item_stale_needs_context_review"]

    source = sources[item["source_id"]]
    source_type = source.get("source_type")
    if source_type not in OFFICIAL_SOURCE_TYPES:
        # Local-media / non-official items may publish when a human approved
        # them with corroboration (official/first-party source, or 2+ outlets),
        # or when approved as a qualified subject with explicit attribution.
        if status == "approved" and (_corroboration_satisfied(decision)
                                     or (decision or {}).get("qualified")):
            pass
        else:
            return NEEDS_HUMAN_REVIEW, [f"source_type_requires_review:{source_type or 'none'}"]

    title_text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
    if (item.get("human_review_required") or item.get("sensitivity") in {"medium", "high"}
            or set(item.get("topics") or []) & SENSITIVE_TOPICS
            or any(word in title_text for word in SENSITIVE_WORDS)):
        if status == "approved":
            return AUTO_PUBLISHABLE, ["human_approved_sensitive_exception"]
        return NEEDS_HUMAN_REVIEW, ["sensitivity_or_personal_harm_exception"]

    if status == "deferred":
        return NEEDS_HUMAN_REVIEW, ["human_deferred"]

    scope_ok, scope_reason = _resident_scope(item, decision)
    if not scope_ok:
        return NEEDS_HUMAN_REVIEW, [scope_reason]
    if item.get("source_id") in CONTEXT_REQUIRED_SOURCES and scope_reason == "structured_countywide_household_scope":
        return NEEDS_HUMAN_REVIEW, ["agenda_or_notice_needs_concrete_local_scope"]

    leaked = validate_public_safe(public_projection(item, decision))
    if leaked:
        return NEEDS_HUMAN_REVIEW, ["public_projection_leak:" + ",".join(sorted(leaked))]
    if status == "approved":
        return AUTO_PUBLISHABLE, ["human_approved_exception"]
    return AUTO_PUBLISHABLE, ["verified_official_resident_relevant"]
