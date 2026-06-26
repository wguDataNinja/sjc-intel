#!/usr/bin/env python3
"""
ED-001 Phase 2: Update review status for queue entries.

Usage:
    python3 scripts/update_review_status.py <item_id> <new_status> [--note "reason"]

Examples:
    python3 scripts/update_review_status.py SJC-CN-20260626-0001 verified
    python3 scripts/update_review_status.py SJC-BCC-20260120-0005 duplicate --note "Also in NBOR as hearing notice"

Supported statuses:
    pending_review  — New item, not yet reviewed (default)
    in_review       — Being reviewed
    verified        — Factually correct, classification confirmed
    needs_followup  — Requires additional information or verification
    rejected_noise  — Not resident-impactful; classified correctly as noise
    duplicate       — Duplicate of another item (not caught by dedupe)
    escalated       — Flagged for priority human/architect review
    archived        — Historical reference, no action needed
"""
import os
import sys
import yaml
from datetime import datetime, timezone

QUEUE_FILE = "data/review_queue/queue.yaml"
VALID_STATUSES = {"pending_review", "in_review", "verified", "needs_followup", "rejected_noise", "duplicate", "escalated", "archived"}


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/update_review_status.py <item_id> <new_status> [--note 'reason']")
        print(f"Valid statuses: {', '.join(sorted(VALID_STATUSES))}")
        sys.exit(1)

    item_id = sys.argv[1]
    new_status = sys.argv[2].lower()
    note = ""
    if "--note" in sys.argv:
        idx = sys.argv.index("--note")
        if idx + 1 < len(sys.argv):
            note = sys.argv[idx + 1]

    if new_status not in VALID_STATUSES:
        print(f"ERROR: Invalid status '{new_status}'. Valid: {', '.join(sorted(VALID_STATUSES))}")
        sys.exit(1)

    if not os.path.exists(QUEUE_FILE):
        print(f"ERROR: Queue file not found at {QUEUE_FILE}. Run build_review_queue.py first.")
        sys.exit(1)

    # Load queue
    with open(QUEUE_FILE) as f:
        data = yaml.safe_load(f)
    entries = data.get("queue", [])

    # Find and update the entry
    found = False
    changed = False
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for entry in entries:
        if entry["item_id"] == item_id:
            old_status = entry["review_status"]
            entry["review_status"] = new_status
            entry["reviewed_at"] = now
            if note:
                entry["review_notes"] = (entry.get("review_notes", "") + "; " + note).strip("; ")
            found = True
            changed = (old_status != new_status)
            print(f"  {item_id}: {old_status} -> {new_status}")
            if note:
                print(f"  Note: {note}")
            break

    if not found:
        print(f"ERROR: Item '{item_id}' not found in queue.")
        sys.exit(1)

    if not changed:
        print(f"  Status unchanged (already {new_status}).")
        sys.exit(0)

    # Write updated queue
    with open(QUEUE_FILE, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Editorial Review Queue\n")
        f.write("# =============================================================================\n")
        f.write(f"# Last updated: {now}\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        yaml.dump({"queue": entries}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  Queue updated.")

    # Also update the source intel_item file if possible
    source_file = entry.get("source_file", "")
    if source_file and os.path.exists(source_file):
        try:
            with open(source_file) as f:
                item_data = yaml.safe_load(f)
            for item in item_data.get("items", []):
                if item.get("item_id") == item_id:
                    item["review_status"] = new_status
                    if note:
                        item["reviewer_notes"] = note
                    break
            with open(source_file, "w") as f:
                yaml.dump(item_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"  Source file also updated: {source_file}")
        except Exception as e:
            print(f"  WARNING: Could not update source file: {e}")

    print("\nDone. Run rebuild_dedupe_index.py only if needed.")


if __name__ == "__main__":
    main()
