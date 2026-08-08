#!/usr/bin/env python3
"""SJC_Intel — Apply a Model B editorial manifest (Task 29).

Writes durable publication decisions (data/publication_decisions/<id>.yaml) for
the explicitly listed Model B items, using the same validated decision logic as
scripts/publication_decision.py. Every entry requires a rationale; roles,
display topics, corroboration, and qualified posture are recorded for the
release classifier and projection.

Usage:
  python3 scripts/apply_editorial_manifest.py --manifest data/editorial/model_b_manifest.yaml [--dry-run]

Manifest entry shape (see data/editorial/model_b_manifest.yaml):
  - item_id: SJC-SL-20260704-0001
    role: timeline
    display_topic: local_business
    relevance: in_silverleaf
    lifecycle: completed
    lifecycle_label: Completed
    silverleaf: included
    qualified: true
    qualified_label: Tenant unconfirmed
    corroboration:
      - source: Publix
        url: https://corporate.publix.com/
        kind: first_party
    rationale: "..."
"""
import argparse
import os
import sys
from argparse import Namespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml

import publication_decision as pd  # noqa: E402


def build_ns(entry):
    """Build the argparse Namespace publication_decision.build_decision expects."""
    corr = []
    for c in entry.get("corroboration") or []:
        corr.append(f"{c.get('source')}|{c.get('url')}|{c.get('kind')}")
    return Namespace(
        silverleaf=entry.get("silverleaf", "included"),
        silverleaf_rationale=entry.get("silverleaf_rationale", entry.get("rationale", "")),
        place_ids=entry.get("place_ids") or [],
        entity_ids=entry.get("entity_ids") or [],
        relevance=entry.get("relevance"),
        role=entry.get("role"),
        qualified=bool(entry.get("qualified")),
        qualified_label=entry.get("qualified_label"),
        corroboration=corr,
        public_summary_override=entry.get("public_summary_override", ""),
        public_title_override=entry.get("public_title_override", ""),
        why_override=entry.get("why_override", ""),
        display_topic=entry.get("display_topic"),
        event_date=entry.get("event_date", ""),
        event_date_label=entry.get("event_date_label", ""),
        lifecycle=entry.get("lifecycle", ""),
        lifecycle_label=entry.get("lifecycle_label", ""),
        reason="",
    )


def main():
    ap = argparse.ArgumentParser(description="Apply a Model B editorial manifest.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--reviewer", default="Buddy",
                    help="reviewer identity recorded on decisions (default Buddy)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = yaml.safe_load(open(args.manifest)) or {}
    entries = manifest.get("decisions", [])
    if not entries:
        print("No decisions listed in manifest.")
        return

    for entry in entries:
        item_id = entry["item_id"]
        rationale = entry.get("rationale", "").strip()
        if not rationale:
            raise SystemExit(f"ERROR: {item_id} requires a rationale")
        rel_path, item = pd.find_item(item_id)
        if not item:
            raise SystemExit(f"ERROR: {item_id} not found in corpus")
        ns = build_ns(entry)
        try:
            record = pd.build_decision("approve", item, args.reviewer, rationale, ns)
        except pd.PublicationDecisionError as e:
            raise SystemExit(f"ERROR: {item_id}: {e}")
        print(f"  {item_id}: approved | role={record.get('role')} | "
              f"topic={record.get('display_topic')} | "
              f"qualified={record.get('qualified', False)} | corr={len(record.get('corroboration') or [])}")
        if not args.dry_run:
            pd.write_decision(record)

    print(f"\n{'Dry-run: would write' if args.dry_run else 'Wrote'} "
          f"{len(entries)} publication decision(s).")


if __name__ == "__main__":
    main()
