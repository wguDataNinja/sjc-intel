#!/usr/bin/env python3
"""Report coverage health from a backtest state root or the live runtime.

Backtest:
  python3 scripts/report_coverage_health.py --state-root data/backtests/task22_replay

Live:
  python3 scripts/report_coverage_health.py --live
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def backtest_health(state_root: Path) -> int:
    r = state_root
    state = yaml.safe_load((r / "state.json").read_text())
    print(yaml.safe_dump({
        "entities": len(state.get("entities", [])),
        "search_profiles": len(state.get("search_profiles", [])),
        "lanes": state.get("lanes", []),
        "milestones": len(state.get("milestones", [])),
        "gaps": state.get("gaps", []),
        "last_week": state.get("last_week"),
    }, sort_keys=False))
    return 0


def live_health() -> int:
    from live_adaptive import initialize, read, coverage_path
    r = initialize()
    coverage = read(coverage_path(r), {})
    print(yaml.safe_dump({
        "run_id": coverage.get("run_id"),
        "generated_at": coverage.get("generated_at"),
        "fresh": coverage.get("fresh", []),
        "stale": coverage.get("stale", []),
        "no_yield_queries": coverage.get("no_yield_queries", []),
        "source_gaps": coverage.get("source_gaps", []),
        "missed_milestones": coverage.get("missed_milestones", []),
        "lanes_covered": coverage.get("lanes_covered", []),
    }, sort_keys=False))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state-root", default=None, help="backtest state root directory")
    p.add_argument("--live", action="store_true", help="report from the live runtime")
    a = p.parse_args()
    if a.live:
        return live_health()
    if a.state_root:
        return backtest_health(Path(a.state_root))
    p.error("provide --state-root or --live")


if __name__ == "__main__":
    raise SystemExit(main())
