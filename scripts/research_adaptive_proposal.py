#!/usr/bin/env python3
"""Run bounded follow-up research on an ambiguous adaptive proposal.

Usage:
  python3 scripts/research_adaptive_proposal.py resolve --proposal-id <ID> \
      --query '"SilverLeaf" "Harris Teeter"' --budget 8 --persist
  python3 scripts/research_adaptive_proposal.py check --proposal-id <ID>
  python3 scripts/research_adaptive_proposal.py classify --proposal-id <ID>
"""
from __future__ import annotations

import argparse
import json
import sys

import yaml

from live_adaptive import read, initialize, DURABLE
from research_escalation import (
    detect_ambiguity,
    needs_research,
    research_resolution,
    run_research,
    validate_resolution,
    classify_findings,
    ResearchBudget,
)


def _proposal(proposal_id: str) -> dict:
    r = initialize()
    pending = read(r / "pending_proposals.yaml", {"proposals": []})["proposals"]
    p = next((x for x in pending if x["proposal_id"] == proposal_id), None)
    if not p:
        raise SystemExit(f"proposal {proposal_id!r} not found")
    return p


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    resolve = sub.add_parser("resolve")
    resolve.add_argument("--proposal-id", required=True)
    resolve.add_argument("--query", action="append", required=True)
    resolve.add_argument("--budget", type=int, default=8)
    resolve.add_argument("--result-limit", type=int, default=10)
    resolve.add_argument("--persist", action="store_true",
                         help="append the resolution to research_resolutions.yaml")
    resolve.add_argument("--dry-run", action="store_true",
                         help="detect triggers and show queries without running them")

    check = sub.add_parser("check")
    check.add_argument("--proposal-id", required=True)

    classify = sub.add_parser("classify")
    classify.add_argument("--proposal-id", required=True)

    a = parser.parse_args()

    if a.command == "check":
        p = _proposal(a.proposal_id)
        triggers = detect_ambiguity(p)
        needs = needs_research(p)
        print(yaml.safe_dump({"proposal_id": a.proposal_id, "needs_research": needs,
                              "triggers": {k: v for k, v in triggers.items() if v}}, sort_keys=False))
        return 0 if needs else 0

    if a.command == "classify":
        p = _proposal(a.proposal_id)
        triggers = detect_ambiguity(p)
        print(yaml.safe_dump(triggers, sort_keys=False))
        return 0

    p = _proposal(a.proposal_id)
    triggers = detect_ambiguity(p)
    if not needs_research(p):
        print("proposal has no research triggers; resolve directly", file=sys.stderr)
        return 1
    if a.dry_run:
        print(yaml.safe_dump({"proposal_id": a.proposal_id, "queries": a.query,
                              "budget": a.budget, "triggers": triggers}, sort_keys=False))
        return 0
    budget = ResearchBudget(max_queries=a.budget, max_results_per_query=a.result_limit)
    record = research_resolution(p, a.query, budget=budget, persist=a.persist)
    problems = validate_resolution(record)
    if problems:
        print("research-resolution validation failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(yaml.safe_dump(record, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
