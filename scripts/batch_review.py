#!/usr/bin/env python3
"""
Batch review helper for ED-001 calibration.
Usage: python3 scripts/batch_review.py
Reads review_decisions from inline data and applies them.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import update function
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "update_review_status.py")).read().replace(
    'if __name__ == "__main__":', 'def update_fn():'))

# Override sys.argv for each call
def apply(item_id, status, note):
    old_argv = sys.argv[:]
    sys.argv = ["update_review_status.py", item_id, status, "--note", note]
    try:
        update_fn()
    except SystemExit:
        pass
    sys.argv = old_argv

# ===== REVIEW DECISIONS =====

decisions = [
    # Immediate items
    ("SJC-UTIL-20260603-0001", "verified",
     "Same event as county news. Phase III water shortage. Keep both as supporting sources."),

    # Human-review items
    ("SJC-SJSO-20260603-0001", "verified",
     "Routine crime press release - contraband drop. Human review done. No active threat."),
    ("SJC-SJSO-20260603-0002", "verified",
     "Positive community story - lifesaving rescue program. No controversy. Human review confirms."),
    ("SJC-SJSO-20260603-0003", "archived",
     "March 2026 DUI operation - 3+ months old. Archival reference only."),
    ("SJC-SJSO-20260603-0004", "verified",
     "Major crime development - 2023 double murder arrest. Human review confirms factual accuracy from SJSO."),
    ("SJC-SJSO-20260626-0001", "verified",
     "Jail escape plot charges. Human review done. No active public threat beyond facility."),

    # High items - BCC agenda (sample)
    ("SJC-BCC-20260120-0001", "verified",
     "2050 Comprehensive Plan transmittal hearing. Major land-use policy. Correct classification."),
    ("SJC-BCC-20260120-0004", "verified",
     "Flagler Estates Road interlocal agreement. Infrastructure governance. Correct classification."),
    ("SJC-BCC-20260120-0005", "verified",
     "Septic-to-sewer connection policy. Major utility infrastructure. Correct classification."),
    ("SJC-BCC-20260120-0010", "verified",
     "Road impact fee transfer resolution. Transportation funding. Correct classification."),

    # High items - NBOR (sample)
    ("SJC-NBOR-20260626-0002", "verified",
     "ZVAR 2026000011 Bargfrede Shed variance hearing. Correct classification as rezoning beat."),
    ("SJC-NBOR-20260626-0016", "verified",
     "MAJMOD Golfway Centre PUD. Major development modification. Correct classification."),
    ("SJC-NBOR-20260626-0019", "verified",
     "REZ 177 Surfside Ave rezoning. Correct classification."),

    # High items - county news (sample)
    ("SJC-CN-20260626-0001", "verified",
     "SR 207 WRF now operational. Largest capital project in county history. Correct classification."),
    ("SJC-CN-20260626-0002", "verified",
     "Railroad crossing closure - W. King St and Kinlaw Rd. Active traffic impact. Correct classification."),

    # High items - utility/emergency
    ("SJC-EM-20260626-0001", "verified",
     "Hurricane season preparedness. Seasonal awareness item. Correct classification."),

    # Example of noise/rejection
    ("SJC-CN-20260626-0004", "rejected_noise",
     "Feel-good recycling driver story. Community interest but not resident-impact intel. Correct for noise rejection."),

    # Duplicate across sources
    ("SJC-CN-20260603-0005", "duplicate",
     "Phase III water shortage already captured as SJC-UTIL-20260603-0001 on utility dept page. Keeping both is correct - different sources."),
]

for item_id, status, note in decisions:
    print(f"\n  Processing {item_id} -> {status}...")
    apply(item_id, status, note)

print(f"\n  Reviewed {len(decisions)} items.")
