# Adaptive discovery and historical replay

`data/backtests/<id>/` is an isolated simulation root. It never writes the
production registries, review queue, corpus, release, or cadence markers.

The weekly loop is: historically visible state → frozen week evidence →
deterministic findings → Resident Coverage Strategist proposals → independent
evaluator → accepted changes visible next week. The Resident Editor is the
coverage-lane proposal behavior in the same bounded strategy stage; neither
role can approve its proposals.

Availability is conservative: explicit `available_on` wins; otherwise a
record is unavailable. Accepted transitions use `week_start + 7 days`.
`evaluator_baseline` is accessed only by final metrics, never by the generator
or evaluator. Frozen replay evidence is date-filtered before the generator.

## Historical breadth and health metrics

The replay feed (`replay_evidence.yaml`) now carries `milestone_due` dates and
additional construction/growth subjects. The final evaluation reports, in
addition to recall/precision:

* **overdue / met milestones** — a milestone is overdue when its due date has
  passed without a realizing event for its subject; met when a realizing event
  is visible. Milestones without a due date are never claimed overdue.
* **stale subjects** — tracked entities/profiles with no finding within the
  stale window (default 60 days).
* **search-profile yield** — accepted profiles that produced findings in later
  weeks, plus query-attempt counts.
* **source freshness** — first/last evidence date per source.
* **lane coverage health** — per-lane weeks covered over total replayed weeks.
* **false positives** — rejected proposals across the replay.

A consolidated `final/coverage_health.yaml` artifact is written after every
replay. Metrics are intentionally not tuned for a perfect score; honest misses
are reported.

## Commands

```bash
python3 scripts/build_historical_state.py --backtest-id task22_replay --as-of 2025-05-05
python3 scripts/init_historical_backtest.py --backtest-id task22_replay --reset
python3 scripts/run_historical_week.py --backtest-id task22_replay --week-start 2025-05-05 --week-end 2025-05-11
python3 scripts/run_historical_backtest.py --backtest-id task22_replay --start 2025-05-05 --end 2026-08-03
python3 scripts/evaluate_historical_backtest.py --backtest-id task22_replay
python3 scripts/report_coverage_health.py --state-root data/backtests/task22_replay
```

To cleanly restart one simulation, run `init_historical_backtest.py --reset`;
it replaces only that named simulation root from immutable fixtures. In
production, use the same proposal/evaluator contract. Durable governance state
lives under `data/adaptive_discovery/`; transient live runs and receipts live
under `runtime/adaptive_discovery/`; a human must apply reviewed transitions.
Stop the loop on repeated evaluator failure, missing dated evidence, a search
budget breach, or any sensitive/publication decision.
