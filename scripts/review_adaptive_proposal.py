#!/usr/bin/env python3
"""Human proposal review and rollback for supervised adaptive discovery.

Acts on exactly one proposal per invocation (no bulk acceptance). Shows
evidence and the exact proposed state transition before any mutation. Every
decision is appended to ``data/adaptive_discovery/decisions.yaml``. On
success the current brief is regenerated. Publication state is never touched.

Examples:
  python3 scripts/review_adaptive_proposal.py show --proposal-id <ID>
  python3 scripts/review_adaptive_proposal.py accept --proposal-id <ID> --reviewer Buddy --rationale "evidence reviewed" [--dry-run]
  python3 scripts/review_adaptive_proposal.py reject --proposal-id <ID> --reviewer Buddy --rationale "reason"
  python3 scripts/review_adaptive_proposal.py defer --proposal-id <ID> --reviewer Buddy --rationale "follow up later"
  python3 scripts/review_adaptive_proposal.py rollback --proposal-id <ID> --decision-id <DEC> --reviewer Buddy --rationale "undo"
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import yaml

from live_adaptive import read, review, edit_proposal, initialize, ROOT

ACTIONS = ("accept", "reject", "defer", "rollback", "edit")
TYPE_BUCKETS = {"entity": "entities", "search_profile": "search_profiles",
                "coverage_lane": "lanes", "timeline_reconciliation": "timelines",
                "milestone": "milestones", "alias": "aliases"}


def parse_list(value):
    return [v.strip() for v in value.split(",") if v.strip()] if value else None


def show_proposal(proposal_id: str) -> int:
    r = initialize()
    pending = read(r / "pending_proposals.yaml", {"proposals": []})["proposals"]
    decisions = read(r / "decisions.yaml", {"decisions": []})["decisions"]
    p = next((x for x in pending if x["proposal_id"] == proposal_id), None)
    if not p:
        print(f"proposal {proposal_id!r} not found in pending proposals", file=sys.stderr)
        return 1
    history = [d for d in decisions if d.get("proposal_id") == proposal_id]
    print(yaml.safe_dump({"proposal": p}, sort_keys=False))
    bucket = TYPE_BUCKETS.get(p["type"])
    print(f"Exact proposed state change: accepted[{bucket or '?'}] += {p['subject']!r} "
          f"(isolated adaptive state only)")
    affected = [f"'{s}'" for s in (p.get("evidence") or [])]
    print(f"Affected future searches: profiles keyed on {p['subject']!r} (none added beyond proposal)")
    print(f"Decision history for this proposal: {len(history)} entries")
    if history:
        print(yaml.safe_dump(history, sort_keys=False))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["show", *ACTIONS])
    p.add_argument("--proposal-id", required=True)
    p.add_argument("--reviewer")
    p.add_argument("--rationale")
    p.add_argument("--decision-id", help="acceptance decision to reverse (rollback)")
    p.add_argument("--dry-run", action="store_true",
                   help="validate and print the result without writing state")
    p.add_argument("--subject", help="edit: new canonical subject")
    p.add_argument("--canonical-name", dest="canonical", help="edit: recommended canonical name")
    p.add_argument("--aliases", help="edit: comma-separated aliases")
    p.add_argument("--location", help="edit: subject location")
    p.add_argument("--queries", help="edit: comma-separated recurring search queries")
    p.add_argument("--timeline-state", dest="timeline_state", help="edit: timeline state language")
    a = p.parse_args()

    if a.action == "show":
        return show_proposal(a.proposal_id)

    if a.action == "rollback":
        if not a.decision_id:
            p.error("--decision-id is required for rollback")
    if a.action == "edit":
        if not any((a.subject, a.canonical, a.aliases, a.location, a.queries, a.timeline_state)):
            p.error("edit requires at least one of --subject/--canonical-name/--aliases/--location/--queries/--timeline-state")
    if not a.reviewer:
        p.error("--reviewer is required")
    if not a.rationale:
        p.error("--rationale is required")

    if a.action == "edit":
        try:
            result = edit_proposal(a.proposal_id, a.reviewer, a.rationale, dry_run=a.dry_run,
                                   subject=a.subject, aliases=parse_list(a.aliases),
                                   location=a.location, queries=parse_list(a.queries),
                                   recommended_canonical_name=a.canonical,
                                   timeline_state=a.timeline_state)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(yaml.safe_dump(result, sort_keys=False))
        return 0

    try:
        result = review(a.proposal_id, a.action, a.reviewer, a.rationale,
                        dry_run=a.dry_run, decision_id=a.decision_id)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(yaml.safe_dump(result, sort_keys=False))
    if not a.dry_run:
        gen = subprocess.run([sys.executable, "scripts/build_current_brief.py"],
                             cwd=ROOT, capture_output=True, text=True)
        if gen.returncode != 0:
            print(f"brief regeneration failed: {gen.stderr.strip()}", file=sys.stderr)
            return 1
        print(gen.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
