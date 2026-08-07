# Task 22 adaptive discovery backtest

- Read repository authority, Task 21 assessment, dated corpus evidence, and
  harness-engineering reference.
- Implemented a file-backed isolated weekly replay harness under
  `data/backtests/task22_replay`, with date-gated evidence, next-week accepted
  transitions, evaluator separation, alias/timeline/milestone/lane proposals,
  reports, reset, and metrics.
- Ran pilot weeks, corrected a lane/subject precision denominator, and ran the
  contiguous 66-week replay (2025-05-05 through 2026-08-03).
- Result: 9/9 subject targets, 1/1 lane target, 47 accepted proposals, zero
  detected leakage violations. This is a frozen-fixture result, not a claim of
  historical search-engine replay.
- Did not change production registries, review/publication state, PostgreSQL,
  Ivy, scheduling, or deploy state. No commit made.
- Validation: 220 pytest tests passed; repository validator, corpus validator
  (0 errors/321 existing warnings), scope validator, portability check, and
  diff check passed.
