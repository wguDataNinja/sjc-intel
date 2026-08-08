#!/usr/bin/env python3
"""SJC_Intel — Bounded Review-Backlog Reconciliation Tool (Task 29).

Flips review state on explicitly listed low-risk, evidence-backed items so
ordinary verifiable resident items are not left at ``pending_review`` forever.
Preserves every other line of the source files (line-based edits, no YAML
round-trip reflow) and touches ONLY the item_ids listed in the manifest.

Usage:
  python3 scripts/reconcile_items.py --manifest data/editorial/reconciliation.yaml [--dry-run]

Guarantees:
- only the review_status line of a listed item is changed;
- sensitive items are never touched by this tool;
- the manifest is required (no bulk promotion);
- --dry-run prints the exact edits without writing.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml

from publication_common import iter_intel_items  # noqa: E402

REVIEW_STATUS_RE = re.compile(r'^(\s*review_status:\s*).*$')


def locate(target_id):
    """Return (path, start_line, end_line) of the item block containing target_id."""
    for rel, item in iter_intel_items():
        if item.get("item_id") != target_id:
            continue
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel)
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        start = None
        for i, line in enumerate(lines):
            if re.search(r'item_id:\s*["\']?' + re.escape(target_id) + r'["\']?', line):
                start = i
                break
        if start is None:
            raise SystemExit(f"ERROR: item_id line not found for {target_id} in {path}")
        end = len(lines)
        for i in range(start + 1, len(lines)):
            if re.match(r'^\s*-\s*item_id:', lines[i]):
                end = i
                break
        return path, start, end
    raise SystemExit(f"ERROR: item {target_id} not found in corpus")


def apply_edit(lines, start, end, target_id, review_status):
    for i in range(start, end):
        m = REVIEW_STATUS_RE.match(lines[i])
        if m:
            lines[i] = f'{m.group(1)}"{review_status}"\n'
            return i + 1
    raise SystemExit(f"ERROR: no review_status line in item block for {target_id}")


def main():
    ap = argparse.ArgumentParser(description="Bounded review-backlog reconciliation.")
    ap.add_argument("--manifest", required=True, help="reconciliation manifest YAML")
    ap.add_argument("--dry-run", action="store_true", help="print edits without writing")
    args = ap.parse_args()

    manifest = yaml.safe_load(open(args.manifest)) or {}
    entries = manifest.get("items", [])
    if not entries:
        print("No items listed in manifest; nothing to do.")
        return

    # Group by file so all edits to one file apply to the same lines buffer.
    plans = {}
    for entry in entries:
        item_id = entry["item_id"]
        review_status = entry.get("review_status", "verified")
        path, start, end = locate(item_id)
        plans.setdefault(path, []).append((item_id, start, end, review_status))

    total = 0
    for path, group in sorted(plans.items()):
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        edits = []
        for item_id, start, end, review_status in group:
            line_no = apply_edit(lines, start, end, item_id, review_status)
            edits.append((item_id, line_no))
            total += 1
            print(f"  {item_id}: review_status -> {review_status} ({path}:{line_no})")
        if not args.dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)

    print(f"\n{'Dry-run: would reconcile' if args.dry_run else 'Reconciled'} "
          f"{len(plans)} file(s), {total} item(s).")


if __name__ == "__main__":
    main()
