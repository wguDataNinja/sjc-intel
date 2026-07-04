#!/usr/bin/env python3
"""
ED-001 Phase 1: Build flat editorial review queue from all intel_item files.

Scans data/intel_items/**/*.yaml, collects items with review-relevant statuses,
and writes/updates data/review_queue/queue.yaml and summary.yaml.

Idempotent — safe to run multiple times. Queue entries are keyed by item_id.
"""
import os
import re
import yaml
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

INTEL_ITEMS_DIR = "data/intel_items"
QUEUE_DIR = "data/review_queue"
QUEUE_FILE = f"{QUEUE_DIR}/queue.yaml"
SUMMARY_FILE = f"{QUEUE_DIR}/summary.yaml"
FILTERS_FILE = "registry/interest_filters.yaml"
ENTITIES_FILE = "registry/tracked_entities.yaml"
SKIP_FILES = {"daily_cycle_summary.yaml", "bcc_weekly_summary.yaml", "bcc_calibration_notes.md"}
SKIP_DIRS = {".deprecated"}  # Skip deprecated files and source_event directories
SKIP_PREFIXES = {".deprecated"}  # Files ending with .deprecated

# Source_event directories are excluded from the review queue entirely.
# Source events are not intel_items — they are containers/context records.
SOURCE_EVENTS_DIR = "data/source_events"

# Canonical review statuses for internal intelligence review
CANONICAL_STATUSES = {
    "pending_review",  # New item, not yet reviewed (default)
    "in_review",       # Being reviewed
    "verified",        # Factually correct, classification confirmed
    "needs_followup",  # Requires additional information or verification
    "rejected_noise",  # Not resident-impactful; classified correctly as noise
    "duplicate",       # Duplicate of another item (not caught by dedupe)
    "escalated",       # Flagged for priority human/architect review
    "archived",        # Historical reference, no action needed
}


def load_existing_queue():
    """Load existing queue entries to preserve review state across rebuilds."""
    if not os.path.exists(QUEUE_FILE):
        return {}
    try:
        with open(QUEUE_FILE) as f:
            data = yaml.safe_load(f)
        entries = data.get("queue", [])
        return {e["item_id"]: e for e in entries}
    except Exception:
        return {}
PRIORITY_BEATS = {
    "rezoning_comp_plan_dri": "high",
    "transportation": "high",
    "utilities_water": "high",
    "taxes_exemptions_trim_vab": "high",
    "public_safety_livability": "high",
}

ACTIVE_EMERGENCY_KEYWORDS = [
    "boil water", "boil notice", "evacuation", "shelter in place",
    "hazmat", "active shooter", "amber alert", "emergency declaration",
]


def load_interest_filters():
    """Load interest filters from registry."""
    if not os.path.exists(FILTERS_FILE):
        return []
    try:
        with open(FILTERS_FILE) as f:
            data = yaml.safe_load(f)
        return data.get("interest_filters", [])
    except Exception as e:
        print(f"  WARNING: Could not load interest filters: {e}", file=__import__('sys').stderr)
        return []


INTEREST_FILTERS = load_interest_filters()


def load_tracked_entities():
    """Load tracked entities from registry."""
    if not os.path.exists(ENTITIES_FILE):
        return []
    try:
        with open(ENTITIES_FILE) as f:
            data = yaml.safe_load(f)
        return data.get("tracked_entities", [])
    except Exception as e:
        print(f"  WARNING: Could not load tracked entities: {e}", file=__import__('sys').stderr)
        return []


TRACKED_ENTITIES = load_tracked_entities()


def build_entity_match_map(entities):
    """Build a mapping from entity_id to distinctive match phrases.
    
    Uses label and aliases as match phrases. Each phrase is case-insensitive
    and checked as a substring against item title, summary, and raw_excerpt.
    """
    match_map = {}
    for ent in entities:
        eid = ent["entity_id"]
        phrases = set()
        # Label
        label = ent.get("label", "")
        if label:
            phrases.add(label.lower())
        # Aliases
        for alias in ent.get("aliases", []):
            if alias:
                phrases.add(alias.lower())
        if phrases:
            match_map[eid] = list(phrases)
    return match_map


ENTITY_MATCH_MAP = build_entity_match_map(TRACKED_ENTITIES)


def apply_entity_matching(item):
    """Match intel item against tracked entities. Returns list of entity IDs.
    
    Match rules (in order):
    1. Explicit tracked_entity_ids on the item win always.
    2. Label/alias exact substring match (case-insensitive) against
       title, summary, raw_excerpt.
    
    Precision over recall: only label and aliases are matched, not
    search_queries or description. Generic single-word matches are avoided
    by requiring aliases to be multi-word phrases chosen by the entity author.
    """
    # Rule 1: Explicit IDs on the item
    explicit = item.get("tracked_entity_ids", [])
    if explicit:
        return list(explicit)
    
    # Rule 2: Substring match against label and aliases
    text_fields = {
        "title": str(item.get("title", "")).lower(),
        "summary": str(item.get("summary", "")).lower(),
        "raw_excerpt": str(item.get("raw_excerpt", "")).lower(),
    }
    search_text = " ".join(text_fields.values())
    
    matches = []
    for eid, phrases in ENTITY_MATCH_MAP.items():
        for phrase in phrases:
            if phrase in search_text:
                matches.append(eid)
                break
    
    return matches


def get_match_basis(item, entity_id):
    """Return a short string describing why this entity matched."""
    text_fields = {
        "title": str(item.get("title", "")).lower(),
        "summary": str(item.get("summary", "")).lower(),
        "raw_excerpt": str(item.get("raw_excerpt", "")).lower(),
    }
    search_text = " ".join(text_fields.values())
    
    # Check explicit first
    if entity_id in item.get("tracked_entity_ids", []):
        return "explicit"
    
    # Check label and aliases
    for ent in TRACKED_ENTITIES:
        if ent["entity_id"] != entity_id:
            continue
        label = ent.get("label", "").lower()
        if label and label in search_text:
            return f"label: {ent['label']}"
        for alias in ent.get("aliases", []):
            if alias.lower() in search_text:
                return f"alias: {alias}"
    
    return "unknown"


def apply_interest_filters(item):
    """Check item against all interest filters. Returns list of matching filter IDs."""
    if not INTEREST_FILTERS:
        return []

    text_fields = {
        "title": str(item.get("title", "")).lower(),
        "summary": str(item.get("summary", "")).lower(),
        "raw_excerpt": str(item.get("raw_excerpt", "")).lower(),
        "description": str(item.get("description", "")).lower(),
        "communities": " ".join(str(c).lower() for c in item.get("communities", [])),
    }

    matches = []
    for flt in INTEREST_FILTERS:
        fields_to_check = flt.get("match_on", ["title", "summary"])
        text_to_search = " ".join(text_fields.get(f, "") for f in fields_to_check)
        for kw in flt.get("keywords", []):
            if kw.lower() in text_to_search:
                matches.append(flt["id"])
                break

    return matches


def compute_escalation(item):
    """Determine escalation level from urgency, sensitivity, beat, and human_review.
    
    Rules:
    - urgency=urgent OR active emergency keywords → immediate
    - human_review_required + urgency=timely → high
    - human_review_required alone → high (not immediate — routine crime reports need review but aren't emergencies)
    - priority beats → high
    - urgency=timely OR high_signal → high
    - medium_signal → normal
    - everything else → low
    """
    urg = item.get("urgency", "ongoing")
    text = (item.get("title", "") + " " + item.get("summary", "")).lower()

    # Active emergency detection
    if urg == "urgent":
        return "immediate"
    for kw in ACTIVE_EMERGENCY_KEYWORDS:
        if kw in text:
            return "immediate"

    # Human-review items are high, not immediate (unless also urgent)
    if item.get("human_review_required") or item.get("sensitivity") == "high":
        return "high"

    # Beat-based priority
    beat = item.get("beat", item.get("_beat", item.get("primary_topic", "")))
    if beat in PRIORITY_BEATS:
        return PRIORITY_BEATS[beat]

    if urg == "timely":
        return "high"
    sig = item.get("_signal", item.get("signal", "medium"))
    if sig == "high_signal":
        return "high"
    if sig == "medium_signal":
        return "normal"
    return "low"


def extract_app_id(text, title):
    """Extract application/permit IDs for cluster hints."""
    t = (text + " " + title)
    patterns = [
        r"\b(REZ\s+\d{10,})", r"\b(ZVAR\s+\d{10,})", r"\b(PVZVAR\s+\d{10,})",
        r"\b(MAJMOD\s+\d{10,})", r"\b(MINMOD\s+\d{10,})", r"\b(SUPMIN\s+\d{10,})",
        r"\b(PLNAPPL\s+\d{10,})", r"\b(CPA\(SS\)\s+\d{10,})", r"\b(PUD\s+\d{10,})",
        r"\b(CDD\s+AMD\s+\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            return m.group(1)
    return None


def collect_items():
    """Scan all intel_item YAML files and return queue entries.
    
    Preserves review state from existing queue entries (review_status,
    review_notes, reviewer, reviewed_at, escalation_override).
    """
    existing = load_existing_queue()
    preserved = 0

    entries = []
    for root, dirs, fnames in os.walk(INTEL_ITEMS_DIR):
        # Skip deprecated subdirectories
        dirs[:] = [d for d in dirs if not any(skip in d for skip in SKIP_DIRS)]

        # Skip deprecated files
        fnames = [f for f in fnames if not any(f.endswith(skip) for skip in SKIP_PREFIXES)]
        for fname in sorted(fnames):
            if not fname.endswith(".yaml") or fname in SKIP_FILES:
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath) as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                print(f"  WARNING: Could not parse {fpath}: {e}", file=__import__('sys').stderr)
                continue

            source_id = data.get("source_id", fname.replace(".yaml", ""))
            items = data.get("items", [])
            rel_path = fpath

            for item in items:
                item_id = item.get("item_id", "")
                if not item_id:
                    continue

                title = item.get("title", "")[:200]
                summary = item.get("summary", "")[:300]
                beat = item.get("_beat", item.get("primary_topic", ""))
                topics = item.get("topics", [])
                urgency = item.get("urgency", "ongoing")
                sensitivity = item.get("sensitivity", "low")
                review_status = item.get("review_status", "pending_review")
                signal = item.get("_signal", "unknown")
                source_url = item.get("source_url", "")
                dedupe_key = item.get("_dedupe_key", "")
                human_review = item.get("human_review_required", False)
                interest_tags = item.get("interest_tags", [])
                discovered_at = item.get("discovered_at", item.get("source_published_at", ""))

                escalation = compute_escalation(item)
                matched_filters = apply_interest_filters(item)
                matched_entities = apply_entity_matching(item)
                entity_match_basis = {}
                for eid in matched_entities:
                    entity_match_basis[eid] = get_match_basis(item, eid)
                app_id = extract_app_id(
                    item.get("raw_excerpt", "") + item.get("summary", ""),
                    title
                )

                # Extract meeting/agenda info
                meeting_date = item.get("_meeting_date", item.get("source_published_at", ""))
                agenda_item_num = item.get("_agenda_item_number", "")

                entry = {
                    "queue_id": f"Q-{item_id}",
                    "item_id": item_id,
                    "dedupe_key": dedupe_key,
                    "source_id": source_id,
                    "source_file": rel_path,
                    "title": title,
                    "summary": summary,
                    "beat": beat,
                    "topics": topics,
                    "signal": signal,
                    "urgency": urgency,
                    "escalation": escalation,
                    "sensitivity": sensitivity,
                    "interest_tags": interest_tags,
                    "matched_filters": matched_filters,
                    "tracked_entity_ids": item.get("tracked_entity_ids", []),
                    "matched_entities": matched_entities,
                    "entity_match_basis": entity_match_basis,
                    "review_status": review_status,
                    "human_review_required": human_review,
                    "source_url": source_url,
                    "discovered_at": str(discovered_at)[:25] if discovered_at else "",
                    "meeting_date": meeting_date if meeting_date else None,
                    "agenda_item_number": agenda_item_num if agenda_item_num else None,
                    "application_id": app_id if app_id else None,
                    "reviewer": "",
                    "review_notes": "",
                    "reviewed_at": "",
                }

                # Preserve review state from existing queue entry
                existing_entry = existing.get(item_id)
                if existing_entry:
                    for field in ["review_status", "review_notes", "reviewer", "reviewed_at"]:
                        if existing_entry.get(field):
                            entry[field] = existing_entry[field]
                            if field == "review_status" and existing_entry[field] != "pending_review":
                                preserved += 1

                entries.append(entry)

    if preserved > 0:
        print(f"   Preserved {preserved} existing review states")

    return entries


def deduplicate(entries):
    """Remove duplicate queue entries by item_id."""
    seen = set()
    unique = []
    for entry in entries:
        if entry["item_id"] not in seen:
            seen.add(entry["item_id"])
            unique.append(entry)
    return unique


def build_summary(entries):
    """Generate queue summary."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = len(entries)
    pending = sum(1 for e in entries if e["review_status"] == "pending_review")

    by_source = defaultdict(int)
    by_beat = defaultdict(int)
    by_escalation = defaultdict(int)
    by_signal = defaultdict(int)
    by_urgency = defaultdict(int)
    by_filter = defaultdict(list)
    by_entity = defaultdict(list)
    human_review = []

    for e in entries:
        by_source[e["source_id"]] += 1
        by_beat[e["beat"]] += 1
        by_escalation[e["escalation"]] += 1
        by_signal[e["signal"]] += 1
        by_urgency[e["urgency"]] += 1
        if e.get("matched_filters"):
            for fid in e["matched_filters"]:
                by_filter[fid].append(e["item_id"])
        if e.get("matched_entities"):
            for eid in e["matched_entities"]:
                by_entity[eid].append(e["item_id"])
        if e["human_review_required"]:
            human_review.append(e["item_id"])

    oldest = sorted(entries, key=lambda x: x["discovered_at"])[:5]
    urgent_items = [e for e in entries if e["escalation"] in ("immediate", "high")][:10]

    # Build prioritized items list from filter matches + entity matches
    prioritized_items = []
    for e in entries:
        if e.get("matched_filters") or e.get("matched_entities"):
            prioritized_items.append({
                "item_id": e["item_id"],
                "title": e["title"][:100],
                "matched_filters": e.get("matched_filters", []),
                "matched_entities": e.get("matched_entities", []),
                "entity_match_basis": e.get("entity_match_basis", {}),
                "escalation": e["escalation"],
                "source": e["source_id"],
                "discovered_at": e["discovered_at"],
            })

    return {
        "generated_at": now,
        "total_entries": total,
        "pending_review": pending,
        "by_source": dict(by_source),
        "by_beat": dict(by_beat),
        "by_escalation": dict(by_escalation),
        "by_signal": dict(by_signal),
        "by_urgency": dict(by_urgency),
        "interest_filter_matches": {fid: len(items) for fid, items in by_filter.items()},
        "entity_matches": {eid: len(items) for eid, items in by_entity.items()},
        "total_entity_matches": sum(len(items) for items in by_entity.values()),
        "total_prioritized_items": len(prioritized_items),
        "prioritized_items": prioritized_items,
        "human_review_count": len(human_review),
        "human_review_item_ids": human_review[:10],
        "oldest_pending": [
            {"item_id": e["item_id"], "title": e["title"][:80], "discovered_at": e["discovered_at"]}
            for e in oldest
        ],
        "top_urgent_items": [
            {"item_id": e["item_id"], "title": e["title"][:80], "escalation": e["escalation"], "source": e["source_id"]}
            for e in urgent_items
        ],
    }


def write_queue(entries, summary):
    """Write queue.yaml and summary.yaml."""
    os.makedirs(QUEUE_DIR, exist_ok=True)

    with open(QUEUE_FILE, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Editorial Review Queue\n")
        f.write("# =============================================================================\n")
        f.write("# Flat queue of all intel_items requiring or eligible for review.\n")
        f.write(f"# Generated: {summary['generated_at']}\n")
        f.write(f"# Total entries: {summary['total_entries']}\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        out = {"queue": entries}
        yaml.dump(out, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    with open(SUMMARY_FILE, "w") as f:
        yaml.dump(summary, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  Queue: {len(entries)} entries -> {QUEUE_FILE}")
    print(f"  Summary: -> {SUMMARY_FILE}")


def main():
    print("ED-001 Phase 1: Review Queue Builder")
    print("=" * 50)

    print("\n1. Scanning intel_item files...")
    entries = collect_items()
    print(f"   Collected {len(entries)} raw entries")

    print("\n2. Deduplicating by item_id...")
    entries = deduplicate(entries)
    print(f"   Unique entries: {len(entries)}")

    print("\n3. Computing escalation levels...")
    for e in entries:
        e["escalation"] = compute_escalation(e)
    print("   Done")

    print("\n4. Building summary...")
    summary = build_summary(entries)
    print(f"   Pending review: {summary['pending_review']}")
    print(f"   By escalation: {summary['by_escalation']}")

    print(f"   Entity matches: {summary.get('entity_matches', {})}")
    if summary.get('total_entity_matches', 0) > 0:
        print(f"   Total entity-matched items: {summary['total_entity_matches']}")

    print("\n5. Writing queue artifacts...")
    write_queue(entries, summary)

    print(f"\n  === Queue Summary ===")
    print(f"  Total entries: {summary['total_entries']}")
    print(f"  Pending review: {summary['pending_review']}")
    print(f"  Escalation: {summary['by_escalation']}")
    print(f"  Sources: {summary['by_source']}")
    print(f"  Beats: {summary['by_beat']}")
    if summary['human_review_count'] > 0:
        print(f"  Items requiring human review: {summary['human_review_count']}")
    print(f"\n  Top urgent items:")
    for item in summary['top_urgent_items'][:5]:
        print(f"    [{item['escalation']}] {item['title'][:70]} ({item['source']})")

    print("\nDone.")


if __name__ == "__main__":
    main()
