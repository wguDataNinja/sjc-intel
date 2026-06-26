#!/usr/bin/env python3
"""
Rebuild the prior_items.yaml dedupe index from all existing intel_item files.
Scans data/intel_items/*/*.yaml (excluding daily_cycle_summary.yaml).

Safe to run multiple times — skips duplicate keys.
"""
import os
import yaml
import hashlib
from datetime import datetime, timezone

INDEX_FILE = "data/index/prior_items.yaml"
INTEL_ITEMS_DIR = "data/intel_items"
SKIP_FILES = {"daily_cycle_summary.yaml"}
SKIP_PREFIXES = {".deprecated"}  # Skip deprecated files

# Note: source_event files in data/source_events/ are excluded because
# the dedupe index only tracks intel_items, not source events.


def generate_key(item, source_id):
    """Generate deterministic dedupe key."""
    if item.get("_dedupe_key"):
        return item["_dedupe_key"]
    source_url = item.get("source_url", "")
    if source_url:
        raw = f"{source_id}||{source_url}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    title = item.get("title", "")
    date = item.get("source_published_at", item.get("discovered_at", ""))
    raw = f"{source_id}||{title}||{date}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def collect_all_items():
    """Walk data/intel_items/ and collect all item entries."""
    all_items = []
    for date_dir in sorted(os.listdir(INTEL_ITEMS_DIR)):
        dirpath = os.path.join(INTEL_ITEMS_DIR, date_dir)
        if not os.path.isdir(dirpath):
            continue
        for fname in sorted(os.listdir(dirpath)):
            if not fname.endswith(".yaml") or fname in SKIP_FILES:
                continue
            if any(fname.endswith(skip) for skip in SKIP_PREFIXES):
                continue
            fpath = os.path.join(dirpath, fname)
            with open(fpath) as f:
                data = yaml.safe_load(f)
            source_id = data.get("source_id", fname.replace(".yaml", ""))
            items = data.get("items", [])
            for item in items:
                all_items.append({
                    "key": generate_key(item, source_id),
                    "item_id": item.get("item_id", "unknown"),
                    "title": item.get("title", ""),
                    "source_id": source_id,
                    "beat": item.get("_beat", item.get("primary_topic", "unknown")),
                    "discovered_at": item.get("discovered_at",
                        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "status": "pending_review",
                })
    return all_items


def deduplicate(entries):
    """Remove duplicate keys, keeping first occurrence."""
    seen = set()
    unique = []
    for entry in entries:
        if entry["key"] not in seen:
            seen.add(entry["key"])
            unique.append(entry)
    return unique


def main():
    print("Rebuilding dedupe index from all intel_item files...")
    items = collect_all_items()
    print(f"  Collected {len(items)} raw entries")
    items = deduplicate(items)
    print(f"  After dedupe: {len(items)} unique keys")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    output = {"prior_items": items}

    with open(INDEX_FILE, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Prior Items Dedupe Index\n")
        f.write("# =============================================================================\n")
        f.write("# Tracks item fingerprints for deduplication across monitor cycles.\n")
        f.write("#\n")
        f.write("# Schema version: 1.1\n")
        f.write(f"# Last updated: {now[:10]}\n")
        f.write("# Updated by: rebuild_dedupe_index.py\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  Wrote {len(items)} entries to {INDEX_FILE}")
    print("Done.")


if __name__ == "__main__":
    main()
