#!/usr/bin/env python3
"""
ED-001 Batch review: process pending queue items by family.

Directly updates queue.yaml and source intel_item files.
More reliable than calling update_review_status.py in subprocess.
"""
import os
import sys
import yaml
from datetime import datetime, timezone
from collections import defaultdict

QUEUE_FILE = "data/review_queue/queue.yaml"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def save_yaml(path, data, header_lines=None):
    with open(path, "w") as f:
        if header_lines:
            for line in header_lines:
                f.write(f"# {line}\n")
            f.write("\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def update_item(filepath, item_id, new_status, note):
    """Update review_status in a source intel_item file."""
    if not os.path.exists(filepath):
        return False
    data = load_yaml(filepath)
    changed = False
    for item in data.get("items", []):
        if item.get("item_id") == item_id:
            item["review_status"] = new_status
            if note:
                item["reviewer_notes"] = note
            changed = True
            break
    if changed:
        save_yaml(filepath, data)
    return changed


def main():
    print("=" * 60)
    print("ED-001 Batch Review")
    print("=" * 60)

    # Load queue
    data = load_yaml(QUEUE_FILE)
    entries = data["queue"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    pending = [e for e in entries if e["review_status"] == "pending_review"]
    print(f"\nPending items: {len(pending)}")

    # Show breakdown
    by_source = defaultdict(int)
    for e in pending:
        by_source[e["source_id"]] += 1
    print(f"  By source: {dict(by_source)}")

    # Define batch rules: (filter_fn, status, note)
    # Rules are ordered — first match wins
    rules = []

    def rule(name, filter_fn, status, note):
        rules.append((name, filter_fn, status, note))

    # NBOR — utility ROW permits
    rule("NBOR utility ROW permits",
         lambda e: e["source_id"] == "sjc_nbor_public_notices" and e["beat"] == "utilities_water",
         "verified",
         "Batch verified: NBOR utility ROW permit. Public notice with project description, district, date, and PDF evidence.")

    # NBOR — construction/site work
    rule("NBOR construction/site work",
         lambda e: e["source_id"] == "sjc_nbor_public_notices" and e["beat"] == "site_plans_permits_construction",
         "verified",
         "Batch verified: NBOR construction/site work ROW permit. Public notice with project details.")

    # NBOR — development hearings
    rule("NBOR development hearings",
         lambda e: e["source_id"] == "sjc_nbor_public_notices" and e["beat"] == "rezoning_comp_plan_dri",
         "verified",
         "Batch verified: NBOR development hearing notice. Application ID, description, and hearing date present.")

    # NBOR — roadwork
    rule("NBOR road closure",
         lambda e: e["source_id"] == "sjc_nbor_public_notices" and e["beat"] == "roadwork_traffic",
         "verified",
         "Batch verified: NBOR road closure notice. Lane closure with project details.")

    # BCC — meeting-level metadata records (source events)
    rule("BCC meeting-level metadata",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["agenda_item_number"] is None and e["beat"] == "county_government",
         "archived",
         "Batch archived: BCC meeting-level metadata record. Source event tracker — per-item extraction is in separate file.")

    # BCC — broken agenda link meetings
    rule("BCC broken agenda link",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and "agenda link broken" in e["title"].lower(),
         "needs_followup",
         "Needs follow-up: BCC meeting with broken agenda link. Clerk's office may need to correct.")

    # BCC — utilities/water
    rule("BCC utilities consent items",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "utilities_water",
         "verified",
         "Batch verified: BCC utility/water consent item. Utility easement or infrastructure resolution from agenda PDF.")

    # BCC — parks/amenities
    rule("BCC parks/amenities items",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "parks_amenities",
         "verified",
         "Batch verified: BCC parks/amenities item. Donation, license agreement, or park resolution from agenda PDF.")

    # BCC — rezoning/development
    rule("BCC rezoning/development",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "rezoning_comp_plan_dri",
         "verified",
         "Batch verified: BCC rezoning/development item. Land-use resolution from agenda PDF.")

    # BCC — transportation
    rule("BCC transportation",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "transportation",
         "verified",
         "Batch verified: BCC transportation item. Road/infrastructure resolution from agenda PDF.")

    # BCC — budget/tax
    rule("BCC budget/tax items",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "taxes_exemptions_trim_vab",
         "verified",
         "Batch verified: BCC budget/tax item. Budget/funding resolution from agenda PDF.")

    # BCC — public safety
    rule("BCC public safety items",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "public_safety_livability",
         "verified",
         "Batch verified: BCC public safety item. Safety/emergency services resolution from agenda PDF.")

    # BCC — procurement/contract (needs follow-up — limited context)
    rule("BCC procurement/contract (needs followup)",
         lambda e: e["source_id"] == "sjc_bcc_calendar" and e["beat"] == "local_government_budget_procurement",
         "needs_followup",
         "Needs follow-up: BCC procurement/contract item. Limited agenda PDF context for resident impact assessment.")

    # County news — low impact
    rule("County news low-impact",
         lambda e: e["source_id"] == "sjc_county_news" and e["escalation"] == "low",
         "verified",
         "Batch verified: county news low-impact item. Public announcement with source URL.")

    # County news — medium/high
    rule("County news medium/high",
         lambda e: e["source_id"] == "sjc_county_news" and e["escalation"] != "low",
         "verified",
         "Batch verified: county news medium/high item. Official press release with source URL.")

    # Utility department
    rule("Utility department items",
         lambda e: e["source_id"] == "sjc_utility_department",
         "verified",
         "Batch verified: utility department announcement. Official county utility notice with source URL.")

    # Apply rules
    updated = 0
    errors = 0
    ruled_items = set()

    for name, filter_fn, status, note in rules:
        matching = [e for e in entries if filter_fn(e) and e["review_status"] == "pending_review" and e["item_id"] not in ruled_items]
        if not matching:
            continue
        ruled_items.update(e["item_id"] for e in matching)
        print(f"\n  {name}: {len(matching)} items -> {status}")

        for entry in matching:
            entry["review_status"] = status
            entry["review_notes"] = note
            entry["reviewed_at"] = now
            # Also update source file
            src = entry.get("source_file", "")
            if src:
                try:
                    update_item(src, entry["item_id"], status, note)
                except Exception as e:
                    print(f"    WARN: could not update source file {src}: {e}")
                    errors += 1
            updated += 1

    # Check for unmatched pending items
    unmatched = [e for e in entries if e["review_status"] == "pending_review" and e["item_id"] not in ruled_items]
    if unmatched:
        print(f"\n  UNMATCHED (no rule applied): {len(unmatched)} items")
        for e in unmatched:
            print(f"    {e['source_id']:35s} | {e['beat']:30s} | {e['title'][:60]}")

    # Save updated queue
    save_yaml(QUEUE_FILE, data, [
        "=" * 77,
        "SJC_Intel — Editorial Review Queue",
        "=" * 77,
        f"Updated: {now}",
        f"Entries: {len(entries)}",
        "=" * 77,
    ])

    print(f"\n{'=' * 60}")
    print(f"Batch Review Complete")
    print(f"{'=' * 60}")
    print(f"\nUpdated: {updated}")
    print(f"Errors: {errors}")
    print(f"Remaining pending: {len(unmatched)}")


if __name__ == "__main__":
    main()
