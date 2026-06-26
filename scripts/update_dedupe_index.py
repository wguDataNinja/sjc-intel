#!/usr/bin/env python3
"""
Update the prior_items.yaml dedupe index with new items from intel_item files.

Usage:
    python3 scripts/update_dedupe_index.py data/intel_items/2026-06-26/sjc_nbor_public_notices.yaml

Or scan a whole directory:
    python3 scripts/update_dedupe_index.py data/intel_items/2026-06-26/

Generates dedupe keys for items that don't have them, checks against existing
index, and appends new entries.
"""
import os
import sys
import yaml
import hashlib
from datetime import datetime, timezone

INDEX_FILE = "data/index/prior_items.yaml"


def load_index():
    """Load existing prior_items.yaml. Returns list of entries."""
    if not os.path.exists(INDEX_FILE):
        print(f"  Index file not found at {INDEX_FILE}, creating new.")
        return []
    with open(INDEX_FILE) as f:
        data = yaml.safe_load(f)
    return data.get("prior_items", []) if data else []


def save_index(entries, new_count):
    """Write prior_items.yaml with updated entries."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(INDEX_FILE, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Prior Items Dedupe Index\n")
        f.write("# =============================================================================\n")
        f.write("# Tracks item fingerprints for deduplication across monitor cycles.\n")
        f.write("#\n")
        f.write("# Schema version: 1.1\n")
        f.write(f"# Last updated: {now[:10]}\n")
        f.write("# Updated by: update_dedupe_index.py\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        f.write("prior_items:\n")
        for entry in entries:
            sid = entry.get("source_id", "unknown")
            beat = entry.get("beat", "unknown")
            disc = entry.get("discovered_at", now)
            stat = entry.get("status", "pending_review")
            f.write(f"\n  - key: {yaml.dump(entry['key'], default_flow_style=False).strip()}\n")
            f.write(f"    item_id: {entry['item_id']}\n")
            f.write(f"    title: {yaml.dump(entry['title'], default_flow_style=False).strip()}\n")
            f.write(f"    source_id: {sid}\n")
            f.write(f"    beat: {beat}\n")
            f.write(f"    discovered_at: {disc}\n")
            f.write(f"    status: {stat}\n")
    print(f"  Wrote {len(entries)} entries to {INDEX_FILE}")


def generate_key(item, source_id):
    """Generate a deterministic dedupe key for an item."""
    # If item already has _dedupe_key, use it
    if item.get("_dedupe_key"):
        return item["_dedupe_key"]

    # For URL-based sources (county news, sheriff), use source_id + URL
    source_url = item.get("source_url", "")
    if source_url:
        raw = f"{source_id}||{source_url}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    # Fallback: source_id + title + date
    title = item.get("title", "")
    date = item.get("source_published_at", item.get("discovered_at", ""))
    raw = f"{source_id}||{title}||{date}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def process_file(filepath):
    """Process a single intel_item YAML file, returning (added, skipped_existing, skipped_no_items)."""
    with open(filepath) as f:
        data = yaml.safe_load(f)

    source_id = data.get("source_id", os.path.basename(filepath).replace(".yaml", ""))
    items = data.get("items", [])

    if not items:
        return 0, 0, 1

    # Generate keys for all items
    new_entries = []
    for item in items:
        item_id = item.get("item_id", "unknown")
        title = item.get("title", "")
        key = generate_key(item, source_id)
        beat = item.get("_beat", item.get("primary_topic", "unknown"))
        disc_at = item.get("discovered_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

        new_entries.append({
            "key": key,
            "item_id": item_id,
            "title": title,
            "source_id": source_id,
            "beat": beat,
            "discovered_at": disc_at,
        })

    return new_entries, source_id


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/update_dedupe_index.py <file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]

    # Collect files to process
    if os.path.isdir(path):
        files = sorted([
            os.path.join(path, f) for f in os.listdir(path)
            if f.endswith(".yaml") and f != "daily_cycle_summary.yaml"
        ])
    else:
        files = [path]

    if not files:
        print(f"No intel_item files found at {path}")
        sys.exit(0)

    print(f"Scanning {len(files)} file(s)...")

    # Load existing index and add source_id for backward compat
    existing_entries = load_index()
    for entry in existing_entries:
        if "source_id" not in entry:
            # Infer from key pattern: source_id||...
            key_parts = entry["key"].split("||")
            entry["source_id"] = key_parts[0] if len(key_parts) > 0 else "unknown"
    existing_keys = {e["key"] for e in existing_entries}
    print(f"  Existing index: {len(existing_entries)} entries")

    total_added = 0
    total_skipped_existing = 0
    total_skipped_no_items = 0

    for filepath in files:
        print(f"\n  Processing: {filepath}")
        new_entries, source_id = process_file(filepath)

        if isinstance(new_entries, tuple):
            # File had no items
            total_skipped_no_items += new_entries[2]
            print(f"    No items found")
            continue

        added = 0
        skipped = 0
        for entry in new_entries:
            if entry["key"] in existing_keys:
                skipped += 1
            else:
                existing_entries.append(entry)
                existing_keys.add(entry["key"])
                added += 1

        print(f"    Source: {source_id}")
        print(f"    Items in file: {len(new_entries)}")
        print(f"    Added to index: {added}")
        print(f"    Already indexed: {skipped}")

        total_added += added
        total_skipped_existing += skipped

    # Save
    save_index(existing_entries, total_added)

    print(f"\n  === Summary ===")
    print(f"  Files scanned: {len(files)}")
    print(f"  New keys added: {total_added}")
    print(f"  Keys already present: {total_skipped_existing}")
    print(f"  Total index size: {len(existing_entries)}")


if __name__ == "__main__":
    main()
