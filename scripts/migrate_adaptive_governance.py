#!/usr/bin/env python3
"""Migrate adaptive-discovery governance authority from legacy runtime state.

Copies only versioned human-governance artifacts into ``data/adaptive_discovery``:
pending proposals, decision/rollback history, accepted adaptive state, coverage
health, and derived pipeline health. Run receipts and run artifacts remain
transient under ``runtime/adaptive_discovery``.
"""
from __future__ import annotations

import argparse
import sys

from live_adaptive import DURABLE, RUNTIME, read, write

ARTIFACTS = {
    "state.yaml": "accepted_state.yaml",
    "pending_proposals.yaml": "pending_proposals.yaml",
    "decisions.yaml": "decisions.yaml",
    "coverage.yaml": "coverage_health.yaml",
    "health.yaml": "health.yaml",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace", action="store_true",
                        help="replace an existing durable artifact")
    args = parser.parse_args()
    migrated = []
    for legacy, durable in ARTIFACTS.items():
        source = RUNTIME / legacy
        target = DURABLE / durable
        if not source.exists():
            print(f"missing legacy artifact: {source}", file=sys.stderr)
            return 1
        if target.exists() and not args.replace:
            print(f"refusing to overwrite {target}; rerun with --replace", file=sys.stderr)
            return 1
        write(target, read(source, {}))
        migrated.append(target)
    for path in migrated:
        print(path.relative_to(DURABLE.parents[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
