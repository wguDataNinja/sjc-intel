#!/usr/bin/env python3
"""
SJC_Intel — Deterministic Publication Selector.

Produces a preview of publication-eligible items for a named release per
docs/publication_release_contract.md and ROADMAP.md §3A-G2.

  python3 scripts/select_publication_items.py --release-id <id> [--check]
  python3 scripts/select_publication_items.py --release-id <id> [--window-start ... --window-end ...]

Requirements to be SELECTED:
- review_status == verified (or an explicitly approved equivalent);
- an explicit publication decision with publication_status == approved;
- allowed sensitivity (low; medium only with explicit editorial approval
  recorded on the decision; high excluded);
- valid source URL and source attribution;
- not withdrawn;
- not superseded (canonical record);
- SilverLeaf relevance decision == included;
- public-safe projection (no internal-only fields);
- within the configured release window (source_published_at / discovered_at).

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
    is_valid_url,
    iter_intel_items,
    item_date,
    legacy_exception_for_item,
    legacy_treatment_for_item,
    load_all_decisions,
    load_sources,
    public_projection,
    validate_public_safe,
)

DEFAULT_WINDOW_DAYS = 60

# Legacy treatments that exclude an item from release (non-canonical captures,
# archival-only records, and items needing a registry fix). Pure timestamp
# warnings (warning_timestamp_default) do NOT block release.
BLOCKING_LEGACY_TREATMENTS = {
    "non_canonical_duplicate_capture",
    "retained_as_archival_evidence",
    "legacy_incomplete_record",
    "needs_registry_fix",
}


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

        reasons = []

        # 1. Review status must be verified.
        if item.get("review_status") != "verified":
            reasons.append(f"review_status:{item.get('review_status') or 'none'}")

        # 2. Explicit publication decision required.
        dec = decision_map.get(item_id)
        if not dec:
            reasons.append("no_publication_decision")
        elif dec.get("withdrawn") or dec.get("publication_status") == "withdrawn":
            reasons.append("withdrawn")
        elif dec.get("publication_status") != "approved":
            reasons.append(f"publication_status:{dec.get('publication_status')}")

        # 3. Sensitivity policy.
        sens = item.get("sensitivity")
        if sens == "high":
            reasons.append("high_sensitivity")
        elif sens == "medium":
            # Medium requires explicit editorial approval recorded on decision.
            if not dec or dec.get("publication_status") != "approved" \
                    or not dec.get("release_eligible"):
                reasons.append("medium_sensitivity_needs_approval")

        # 4. Source attribution.
        if not item.get("source_id"):
            reasons.append("missing_source_id")
        elif item.get("source_id") not in sources:
            reasons.append(f"unknown_source:{item.get('source_id')}")
        if not is_valid_url(item.get("source_url")):
            reasons.append("invalid_source_url")

        # 5. Non-superseded canonical record.
        if item.get("superseded_by"):
            reasons.append("superseded")

        # 6. SilverLeaf relevance decision.
        sl = (dec or {}).get("silverleaf_relevance") or {}
        if sl.get("decision") != "included":
            if not sl.get("decision"):
                reasons.append("missing_silverleaf_decision")
            else:
                reasons.append(f"silverleaf:{sl.get('decision')}")

        # 7. Public-safe projection.
        proj = public_projection(item, dec)
        leaked = validate_public_safe(proj)
        if leaked:
            reasons.append(f"public_projection_leak:{','.join(sorted(leaked))}")

        # 8. Release window.
        dt = item_date(item)
        if dt is None:
            reasons.append("missing_date")
        elif dt.tzinfo is None:
            reasons.append("naive_timestamp")
        elif not (window_start <= dt <= window_end):
            reasons.append(f"outside_window:{dt.date()}")

        # 9. Legacy exception (only blocking treatments exclude from release;
        #    pure timestamp warnings do not).
        treatment = legacy_treatment_for_item(item_id)
        if treatment in BLOCKING_LEGACY_TREATMENTS:
            reasons.append(f"legacy_exception:{treatment}")

        if reasons:
            excluded[item_id] = reasons
            counts[reasons[0]] += 1
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
    lines.append("NOTE: This is a preview. Nothing is published. Release "
                 "membership is a separate human act.")
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
            print("\nCHECK: eligible items found; release still requires human approval.", file=sys.stderr)
            sys.exit(0)
        print("\nCHECK: no items currently eligible for this release window "
              "(awaiting verified+approved+SilverLeaf-included items).", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
