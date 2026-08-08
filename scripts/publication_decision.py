#!/usr/bin/env python3
"""
SJC_Intel — Publication Decision Operator Tool.

Records explicit, human-controlled publication decisions for individual items
per docs/publication_release_contract.md and ROADMAP.md §3A-G2.

Commands:
  python3 scripts/publication_decision.py approve --item-id SJC-... [options]
  python3 scripts/publication_decision.py reject  --item-id SJC-... [options]
  python3 scripts/publication_decision.py defer   --item-id SJC-... [options]
  python3 scripts/publication_decision.py withdraw --item-id SJC-... [options]
  python3 scripts/publication_decision.py show    --item-id SJC-...

Guarantees:
- requires explicit item ID, reviewer identity, and rationale;
- shows current review/sensitivity/source/SilverLeaf state;
- dry-run diff before mutation (--dry-run);
- validates before mutation and rejects invalid state transitions;
- preserves prior decisions (audit history appended, never rewritten);
- prevents accidental bulk approval (one item per invocation);
- idempotent (repeat of same decision is a no-op);
- NEVER marks anything published and never creates a release.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publication_common import (  # noqa: E402
    DECISION_SCHEMA_VERSION,
    DECISIONS_DIR,
    EDITORIAL_ROLES,
    ITEM_ID_RE,
    PUBLICATION_STATUSES,
    SILVERLEAF_DECISIONS,
    VALID_SENSITIVITIES,
    decision_path,
    is_valid_url,
    load_decision,
    load_legacy_exceptions,
    load_sources,
    now_iso,
    public_projection,
)

VALID_TRANSITIONS = {
    # from_state -> allowed new states (None = no decision yet)
    None: {"approved", "rejected", "deferred", "withdrawn"},
    "approved": {"rejected", "deferred", "withdrawn"},
    "rejected": {"deferred", "approved"},
    "deferred": {"approved", "rejected", "withdrawn"},
    "withdrawn": {"approved"},
}

# Operator command -> recorded publication_status.
COMMAND_TO_STATUS = {
    "approve": "approved",
    "reject": "rejected",
    "defer": "deferred",
    "withdraw": "withdrawn",
}


class PublicationDecisionError(Exception):
    pass


def find_item(item_id):
    """Locate an item record across the corpus (intel_items + backfill)."""
    import glob
    import yaml
    from publication_common import iter_intel_items
    for rel, item in iter_intel_items():
        if item.get("item_id") == item_id:
            return rel, item
    return None, None


def current_state(item):
    """Human-oriented summary of the current review/sensitivity state."""
    sources = load_sources()
    src = sources.get(item.get("source_id")) or {}
    sl = item.get("communities") or []
    entities = item.get("tracked_entity_ids") or []
    return {
        "item_id": item["item_id"],
        "title": item.get("title"),
        "review_status": item.get("review_status"),
        "verification_status": item.get("verification_status"),
        "sensitivity": item.get("sensitivity"),
        "human_review_required": item.get("human_review_required"),
        "source_id": item.get("source_id"),
        "source_name": src.get("name"),
        "source_url": item.get("source_url"),
        "communities": sl,
        "tracked_entity_ids": entities,
        "silverleaf_relevance": item.get("silverleaf_relevance"),
    }


def build_decision(action, item, reviewer, rationale, args):
    """Return the decision record that would be written (no side effects)."""
    status = COMMAND_TO_STATUS[action]
    item_id = item["item_id"]
    prior = load_decision(item_id) or {}
    prior_status = prior.get("publication_status")
    if prior_status == status:
        raise PublicationDecisionError(f"idempotent: {item_id} is already {status}")

    if status not in VALID_TRANSITIONS.get(prior_status, set()):
        raise PublicationDecisionError(
            f"invalid transition: {item_id} {prior_status or 'no-decision'} -> {status} "
            f"(allowed: {sorted(VALID_TRANSITIONS.get(prior_status, set()))})")

    record = dict(prior)
    record.update({
        "schema_version": DECISION_SCHEMA_VERSION,
        "item_id": item_id,
        "publication_status": status,
        "reviewer": reviewer,
        "decision_timestamp": now_iso(),
        "rationale": rationale,
        "origin_review_status": item.get("review_status"),
    })

    # Sensitive items require explicit editorial approval, never auto-pass.
    if item.get("sensitivity") == "high" and status == "approved":
        raise PublicationDecisionError(
            f"cannot approve high-sensitivity item {item_id} without explicit "
            "editorial publication approval (see contract §2 item 5)")

    if args.silverleaf:
        record["silverleaf_relevance"] = {
            "decision": args.silverleaf,
            "rationale": args.silverleaf_rationale or rationale,
            "place_ids": args.place_ids or item.get("communities") or [],
            "entity_ids": args.entity_ids or item.get("tracked_entity_ids") or [],
        }

    if status == "approved":
        record["release_eligible"] = True
        record["source_attribution_confirmed"] = True
        record.setdefault("withdrawn", False)
        record.setdefault("withdrawal_reason", None)
        record.setdefault("superseded_by", None)
        if args.relevance:
            record["relevance"] = args.relevance
        role = getattr(args, "role", None)
        if role:
            record["role"] = role
        if getattr(args, "qualified", False):
            record["qualified"] = True
            if getattr(args, "qualified_label", None):
                record["qualified_label"] = args.qualified_label
        corr = getattr(args, "corroboration", None)
        if corr:
            parsed = []
            for entry in corr:
                if isinstance(entry, dict):
                    parsed.append(entry)
                    continue
                parts = str(entry).split("|")
                if len(parts) == 3:
                    parsed.append({"source": parts[0].strip(),
                                   "url": parts[1].strip(),
                                   "kind": parts[2].strip()})
                else:
                    parsed.append({"source": str(entry).strip()})
            record["corroboration"] = parsed
        if args.public_summary_override:
            if len(args.public_summary_override.strip()) < 10:
                raise PublicationDecisionError(
                    "public_summary_override must be a real public-facing summary "
                    "(>=10 chars); do not truncate source facts")
            record["public_summary_override"] = args.public_summary_override.strip()
        if args.public_title_override:
            record["public_title_override"] = args.public_title_override.strip()
        if args.why_override:
            if len(args.why_override.strip()) < 10:
                raise PublicationDecisionError(
                    "why_override must be a real resident-facing sentence (>=10 chars)")
            record["public_why_override"] = args.why_override.strip()
        if args.display_topic:
            record["display_topic"] = args.display_topic
        if args.event_date:
            record["event_date"] = args.event_date
        if args.event_date_label:
            record["event_date_label"] = args.event_date_label
        if args.lifecycle:
            record["lifecycle"] = args.lifecycle
        if args.lifecycle_label:
            record["lifecycle_label"] = args.lifecycle_label
    elif status == "withdrawn":
        record["withdrawn"] = True
        record["withdrawal_reason"] = args.reason or rationale
        record["release_eligible"] = False
    elif status in ("rejected", "deferred"):
        record["release_eligible"] = False
        record.setdefault("withdrawn", False)

    # Append-safe audit history (never mutates prior entries).
    history = list(prior.get("history", []))
    history.append({
        "status": status,
        "reviewer": reviewer,
        "timestamp": now_iso(),
        "rationale": rationale,
    })
    record["history"] = history
    return record


def write_decision(record):
    import yaml
    os.makedirs(DECISIONS_DIR, exist_ok=True)
    path = decision_path(record["item_id"])
    with open(path, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Publication Decision\n")
        f.write("# =============================================================================\n")
        f.write("# Explicit human decision per docs/publication_release_contract.md.\n")
        f.write("# Never marks an item published; release membership is a separate act.\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        yaml.safe_dump(record, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return path


def cmd_show(item):
    fpath, item = find_item(item["item_id"]) if isinstance(item, str) else (None, item)
    state = current_state(item)
    print(json.dumps(state, indent=2, sort_keys=False))
    dec = load_decision(item["item_id"])
    if dec:
        print("\nExisting decision:")
        print(json.dumps(dec, indent=2, sort_keys=False))


def main():
    ap = argparse.ArgumentParser(description="SJC publication decision operator tool.")
    sub = ap.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--item-id", required=True, help="exact item_id (one item only)")
        p.add_argument("--reviewer", default=os.environ.get("SJC_PUB_REVIEWER"), help="reviewer identity")
        p.add_argument("--rationale", default="", help="decision rationale (required)")
        p.add_argument("--silverleaf", choices=sorted(SILVERLEAF_DECISIONS),
                       help="SilverLeaf relevance decision")
        p.add_argument("--silverleaf-rationale", default="", help="relevance rationale")
        p.add_argument("--relevance", choices=("in_silverleaf", "near_silverleaf", "countywide_impact"),
                       help="explicit public relevance label override (editorial)")
        p.add_argument("--role", choices=sorted(EDITORIAL_ROLES),
                       help="editorial product role: latest/browse/context/timeline")
        p.add_argument("--qualified", action="store_true",
                       help="publish as qualified (confirmed subject, unresolved detail)")
        p.add_argument("--qualified-label", default="",
                       help="public label for the qualified posture, e.g. 'Tenant unconfirmed'")
        p.add_argument("--corroboration", nargs="*", default=[],
                       help="corroboration evidence entries, each 'source|url|kind' "
                            "(kind: official|first_party|local_media)")
        p.add_argument("--place-ids", nargs="*", default=[], help="matching community/place IDs")
        p.add_argument("--entity-ids", nargs="*", default=[], help="matching entity IDs")
        p.add_argument("--reason", default="", help="withdrawal reason (withdraw)")
        p.add_argument("--public-summary-override", default="",
                       help="approved public-facing summary override (copy-edit; "
                            "never alters the source intelligence record)")
        p.add_argument("--public-title-override", default="",
                       help="approved public-facing title override (copy-edit)")
        p.add_argument("--why-override", default="",
                       help="approved public-facing why-it-matters override (copy-edit)")
        p.add_argument("--display-topic", choices=("roads_traffic", "utilities_water",
                                                   "emergency_preparedness",
                                                   "schools_community", "local_business"),
                       help="resident-facing v0 topic category (never a raw taxonomy id)")
        p.add_argument("--event-date", default="", help="explicit event/hearing date (ISO) for display")
        p.add_argument("--event-date-label", default="", help="label for --event-date, e.g. 'Hearing date'")
        p.add_argument("--lifecycle", default="", help="explicit lifecycle id when supported")
        p.add_argument("--lifecycle-label", default="", help="label for --lifecycle")
        p.add_argument("--dry-run", action="store_true", help="print plan without writing")
        p.add_argument("--json", action="store_true", help="machine-readable output")

    for cmd in ("approve", "reject", "defer", "withdraw", "show"):
        add_common(sub.add_parser(cmd, help=f"{cmd} publication decision"))

    args = ap.parse_args()

    if args.command == "show":
        fpath, item = find_item(args.item_id)
        if not item:
            print(f"ERROR: item {args.item_id} not found in corpus", file=sys.stderr)
            sys.exit(2)
        cmd_show(item)
        return

    if not args.reviewer:
        print("ERROR: --reviewer is required (or set SJC_PUB_REVIEWER)", file=sys.stderr)
        sys.exit(2)
    if not args.rationale and args.command != "defer":
        print("ERROR: --rationale is required for a durable decision", file=sys.stderr)
        sys.exit(2)

    fpath, item = find_item(args.item_id)
    if not item:
        print(f"ERROR: item {args.item_id} not found in corpus", file=sys.stderr)
        sys.exit(2)

    try:
        record = build_decision(args.command, item, args.reviewer, args.rationale, args)
    except PublicationDecisionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    # Always print the state + plan for review.
    print(f"Item:          {item['item_id']}")
    print(f"Title:         {item.get('title','')[:70]}")
    print(f"Review status: {item.get('review_status')}")
    print(f"Sensitivity:   {item.get('sensitivity')}")
    print(f"Source URL:    {item.get('source_url')}")
    sl = item.get("communities") or []
    print(f"Communities:   {sl}")
    print(f"SilverLeaf relevance: {args.silverleaf or 'unchanged'}")
    print(f"Decision:      {args.command} by {args.reviewer}")
    print(f"Rationale:     {args.rationale}")

    if args.json:
        print(json.dumps({"plan": record}, indent=2, sort_keys=False))
    else:
        print("\n--- would write ---")
        print(f"  path: {decision_path(item['item_id'])}")
        print(f"  publication_status: {record['publication_status']}")
        print(f"  release_eligible:   {record.get('release_eligible')}")
        print(f"  history entries:    {len(record.get('history', []))}")
        print("--- end plan ---")

    if args.dry_run:
        print("\nDry-run: no file written.")
        return

    path = write_decision(record)
    print(f"\nWrote decision: {path}")


if __name__ == "__main__":
    main()
