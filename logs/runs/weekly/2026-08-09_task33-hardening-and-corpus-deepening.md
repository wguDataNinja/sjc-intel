# Run log — Task 33 production hardening and corpus deepening

**Date:** 2026-08-09
**Cadence type:** Task 33 (workflow hardening + corpus deepening; not a cadence run)
**Agent:** sjc-intel-architect

## Summary
- Hardened the production Hermes workflow against the six generalized defects
  exposed by the 66-week backtest (acceptance asymmetry, evaluator matcher,
  entity/proposal dedupe, FDOT/FCE coverage, stale-milestone escalation,
  production/backtest prompt alignment).
- Triaged and materially reduced the PUB-004 publication/research exception
  backlog through bounded public-source research and reconciliation.
- Prepared and validated the local `SJC-REL-2026-08-004` candidate (48 items,
  75 routes); did NOT deploy.

## Publication-state before → after
| Metric | Before | After |
|---|---|---|
| AUTO_PUBLISHABLE | 34 | 48 |
| NEEDS_HUMAN_REVIEW | 56 | 79 |
| NEEDS_MORE_RESEARCH | 106 | 75 |
| EXCLUDE | 65 | 65 |
| Release items | 34 (003) | 48 (004 candidate) |
| Latest | 10 | 12 |
| Browse/context | 15 | 25 |
| Timelines | 9 | 11 |

## Cadence markers
No cadence run performed. `logs/runs/{daily,weekly,monthly}/LAST_RUN` markers
unchanged (weekly still 2026-07-04). This task did not execute a live weekly
cycle; it prepared the workflow and Release 004 candidate for one.

## Key evidence
- Backtest evaluator rerun: RCR 0.933, zoning now found, FCE only miss (feed gap).
- Production dry run (offline fixtures): NBOR 25 candidates, SJSO 2, bundle PASS.
- Full suite: 332 tests pass; all validators PASS.
