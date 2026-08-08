#!/usr/bin/env python3
"""
SJC_Intel — Deterministic Publication Selector.

Produces a preview of publication-eligible items for a named release per
docs/publication_release_contract.md and ROADMAP.md §3A-G2.

  python3 scripts/select_publication_items.py --release-id <id> [--check]
  python3 scripts/select_publication_items.py --release-id <id> [--window-start ... --window-end ...]

Requirements to be SELECTED:
- policy classification AUTO_PUBLISHABLE (docs/PUBLICATION_POLICY.md);
- a valid release-window date; and
- a public-safe projection.

Default exclusions: pending, high-sensitivity, unresolved human review,
rejected noise, archived-only, duplicates, incomplete attribution, invalid
URLs, internal-only artifacts, missing SilverLeaf decision, withdrawn items.

--check mode performs no mutations and reports selected/excluded counts.
The selector never marks anything published.
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publication_common import (  # noqa: E402
    iter_intel_items,
    item_date,
    load_all_decisions,
    load_sources,
)
from publication_policy import AUTO_PUBLISHABLE, classify_item  # noqa: E402

DEFAULT_WINDOW_DAYS = 60

def selector(decision_map, items, window_start=None, window_end=None, now=None):
    """Deterministic, side-effect-free selection of release-eligible items.

    Returns dict with selected (ordered), excluded (item_id -> reason), and
    counts. Ordering: source_id, then date, then item_id.
    """
    now = now or datetime.now(timezone.utc)
    if window_end is None:
        window_end = now
    if window_start is None:
        window_start = now - timedelta(days=DEFAULT_WINDOW_DAYS)

    sources = load_sources()
    selected = []
    excluded = defaultdict(list)
    counts = Counter()
    by_source = Counter()
    by_topic = Counter()
    by_status = Counter()
    by_classification = Counter()
    classifications = {}

    seen_ids = set()

    for rel, item in sorted(items, key=lambda r: (
            r[1].get("source_id") or "",
            str(item_date(r[1]) or ""),
            r[1].get("item_id") or "")):
        item_id = item["item_id"]
        if item_id in seen_ids:
            excluded[item_id].append("duplicate_item_id")
            counts["duplicate_item_id"] += 1
            continue
        seen_ids.add(item_id)

        by_status[item.get("review_status")] += 1

        dec = decision_map.get(item_id)
        classification, policy_reasons = classify_item(item, dec, sources, as_of=window_end)
        classifications[item_id] = {"classification": classification, "reasons": policy_reasons}
        by_classification[classification] += 1

        # Release window remains a release-level concern, not a classification.
        window_reasons = []
        dt = item_date(item)
        if dt is None:
            window_reasons.append("missing_date")
        elif dt.tzinfo is None:
            window_reasons.append("naive_timestamp")
        elif not (window_start <= dt <= window_end):
            window_reasons.append(f"outside_window:{dt.date()}")

        if classification != AUTO_PUBLISHABLE:
            excluded[item_id] = policy_reasons
            counts[(policy_reasons or [classification])[0]] += 1
            continue
        if window_reasons:
            excluded[item_id] = window_reasons
            counts[window_reasons[0]] += 1
            continue

        # Passed all gates.
        selected.append(item_id)
        by_source[item.get("source_id")] += 1
        for t in item.get("topics") or []:
            by_topic[t] += 1
        counts["selected"] += 1

    return {
        "release_id": None,  # filled by caller
        "selected": selected,
        "excluded": {k: v for k, v in sorted(excluded.items())},
        "counts": dict(counts),
        "by_source": dict(by_source),
        "by_topic": dict(by_topic),
        "by_status": dict(by_status),
        "by_classification": dict(by_classification),
        "classifications": dict(sorted(classifications.items())),
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
    }


def render_human(result):
    lines = []
    lines.append(f"Publication Selection Preview — {result['release_id']}")
    lines.append("=" * 60)
    lines.append(f"Window: {result['window_start']} .. {result['window_end']}")
    lines.append(f"Selected: {len(result['selected'])}")
    lines.append(f"Excluded: {len(result['excluded'])}")
    lines.append("")
    if result["selected"]:
        lines.append("SELECTED (deterministic order):")
        for iid in result["selected"]:
            lines.append(f"  {iid}")
        lines.append("")
    lines.append("Exclusion reasons (first reason per item):")
    for reason, n in sorted(result["counts"].items()):
        lines.append(f"  {reason}: {n}")
    lines.append("")
    lines.append("By source:")
    for src, n in sorted(result["by_source"].items()):
        lines.append(f"  {src}: {n}")
    lines.append("")
    lines.append("By topic:")
    for t, n in sorted(result["by_topic"].items()):
        lines.append(f"  {t}: {n}")
    lines.append("")
    lines.append("Excluded item IDs:")
    for iid, reasons in sorted(result["excluded"].items()):
        lines.append(f"  {iid}: {reasons[0]}")
    lines.append("")
    lines.append("Classification totals:")
    for classification, n in sorted(result["by_classification"].items()):
        lines.append(f"  {classification}: {n}")
    lines.append("")
    lines.append("NOTE: This is a preview. Nothing is deployed. Policy-selected "
                 "items may be released only by an authorized release build.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Deterministic publication selector preview.")
    ap.add_argument("--release-id", required=True, help="named release id, e.g. SJC-REL-2026-08")
    ap.add_argument("--window-start", default=None, help="ISO UTC window start (default now-60d)")
    ap.add_argument("--window-end", default=None, help="ISO UTC window end (default now)")
    ap.add_argument("--check", action="store_true", help="report pass/fail for release eligibility")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    def _parse_window(val):
        if not val:
            return None
        s = val.strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    ws = _parse_window(args.window_start)
    we = _parse_window(args.window_end)

    items = list(iter_intel_items())
    decisions = load_all_decisions()
    result = selector(decisions, items, window_start=ws, window_end=we)
    result["release_id"] = args.release_id

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=False))
    else:
        print(render_human(result))

    if args.check:
        if result["selected"]:
            print("\nCHECK: policy-eligible items found; no files written.", file=sys.stderr)
            sys.exit(0)
        print("\nCHECK: no items currently eligible for this release window "
              "(awaiting policy-eligible verified resident-relevant items).", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
