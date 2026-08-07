#!/usr/bin/env python3
"""Run one bounded supervised live-pilot cycle with receipts and budgets.

Example:
  python3 scripts/run_live_adaptive_pilot.py --run-id SJC-LIVE-YYYYMMDD-0001 \
    --query '"Magnolia Oaks Academy" SilverLeaf' \
    --query '{"query": "\"CR 2209\" St. Johns", "lane": "roads and mobility"}' \
    --budget 3
"""
from __future__ import annotations

import argparse
import json
from live_adaptive import run_pilot, active_search_queries

P = argparse.ArgumentParser(description=__doc__)
P.add_argument("--run-id", required=True)
P.add_argument("--query", action="append",
               help="plain query string or JSON dict (query/lane/subject/date_after/date_before/result_limit)")
P.add_argument("--accepted-profiles", action="store_true",
               help="run all reviewed active search profiles from durable accepted state")
P.add_argument("--budget", type=int, default=3)
P.add_argument("--timeout", type=int, default=15)
P.add_argument("--provider", default="google_news_rss", choices=["google_news_rss", "stub"])
P.add_argument("--allowed-domain", action="append", default=[])
P.add_argument("--excluded-domain", action="append", default=[])
P.add_argument("--date-after", default=None)
P.add_argument("--date-before", default=None)


def main() -> int:
    a = P.parse_args()
    queries = []
    for q in a.query or []:
        try:
            queries.append(json.loads(q))
        except json.JSONDecodeError:
            queries.append(q)
    if a.accepted_profiles:
        queries.extend(active_search_queries())
    if not queries:
        P.error("provide --query or --accepted-profiles")
    run = run_pilot(a.run_id, queries, budget=a.budget, timeout=a.timeout,
                    provider=a.provider, allowed_domains=tuple(a.allowed_domain),
                    excluded_domains=tuple(a.excluded_domain),
                    date_after=a.date_after, date_before=a.date_before)
    print(f"{run['run_id']}: {len(run['normalized_findings'])} findings, "
          f"{len(run['proposals'])} new pending proposals, "
          f"{len(run['evaluator_rejected'])} evaluator-rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
