#!/usr/bin/env python3
"""
SJC_Intel — human-gated source proposal review record.

Records a human disposition for a staged bundle source proposal WITHOUT ever
writing registry/sources.yaml. Source promotion remains the separate,
explicitly approved source-review process.

    python3 scripts/review_source_proposals.py \
        --run-id <run_id> --proposal-id <id> \
        --decision propose_as_new_source|propose_as_alias|propose_as_replacement_endpoint|propose_monitor_update|reject_duplicate|defer_pending_verification \
        --reviewer <name> [--notes <text>] [--dry-run]

Review records: data/incoming/{run_id}/proposal_reviews/{proposal_id}.yaml
"""
import argparse
import datetime
import os
import sys
import yaml

try:
    from scripts.bundle_common import manifest_path, read_json
except ImportError:
    from bundle_common import manifest_path, read_json

DEFAULT_INCOMING_ROOT = "data/incoming"

VALID_DECISIONS = {
    "propose_as_new_source",
    "propose_as_alias",
    "propose_as_replacement_endpoint",
    "propose_monitor_update",
    "reject_duplicate",
    "defer_pending_verification",
}


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_proposals(incoming_root, run_id):
    """Return {proposal_id: proposal} from a staged run."""
    path = os.path.join(incoming_root, run_id, "source_proposals", "proposals.json")
    if not os.path.isfile(path):
        return {}
    try:
        data = read_json(path)
    except Exception:
        return {}
    return {p.get("proposal_id"): p for p in data.get("source_proposals", [])}


def write_review(incoming_root, run_id, proposal, decision, reviewer, notes):
    rev_dir = os.path.join(incoming_root, run_id, "proposal_reviews")
    os.makedirs(rev_dir, exist_ok=True)
    path = os.path.join(rev_dir, f"{proposal['proposal_id']}.yaml")
    record = {
        "review_id": f"REV-{run_id}-{proposal['proposal_id']}",
        "proposal_id": proposal["proposal_id"],
        "run_id": run_id,
        "source_name": proposal.get("source_name"),
        "url": proposal.get("url"),
        "feed_type": proposal.get("feed_type"),
        "current_source_relationship": proposal.get("current_source_relationship"),
        "decision": decision,
        "reviewer": reviewer,
        "decided_at": utc_now_iso(),
        "notes": notes or "",
        "promotion_performed": False,
        "registry_untouched": "registry/sources.yaml unchanged by this command",
    }
    with open(path, "w") as f:
        yaml.dump(record, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return path


def main():
    parser = argparse.ArgumentParser(description="Record a human source-proposal decision.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--decision", required=True, choices=sorted(VALID_DECISIONS))
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--incoming-root", default=DEFAULT_INCOMING_ROOT)
    args = parser.parse_args()

    proposals = load_proposals(args.incoming_root, args.run_id)
    if args.proposal_id not in proposals:
        print(f"ERROR: proposal {args.proposal_id} not found in "
              f"{args.incoming_root}/{args.run_id}/source_proposals/proposals.json",
              file=sys.stderr)
        sys.exit(1)

    proposal = proposals[args.proposal_id]

    if args.dry_run:
        print(f"DRY RUN: would record decision {args.decision} for proposal "
              f"{args.proposal_id} (registry/sources.yaml stays untouched).")
        return

    path = write_review(args.incoming_root, args.run_id, proposal,
                        args.decision, args.reviewer, args.notes)
    print(f"Proposal review recorded -> {path}")
    print("registry/sources.yaml untouched; no promotion performed.")


if __name__ == "__main__":
    main()
