# sjc-intel-architect Memory

Last updated: 2026-08-09

## Current state

- SJC_Intel is supervised and file-first. Canonical corpus/review authority is
  local; no scheduler or autonomous publication exists.
- Task 33 (production hardening + corpus deepening) completed: the six
  backtest-exposed workflow defects are fixed with tests, the PUB-004 backlog
  is materially reduced, and local Release `SJC-REL-2026-08-004` (48 items,
  75 routes) is built and validated but NOT deployed.

## Publication

- `docs/PUBLICATION_POLICY.md` is the authority; `scripts/publication_policy.py`
  derives AUTO_PUBLISHABLE / NEEDS_HUMAN_REVIEW / NEEDS_MORE_RESEARCH / EXCLUDE.
- Publication counts (2026-08-09): 48 auto-publishable; 79 human-review; 75
  research; 65 excluded. The 79/75 are genuine editorial gates and
  non-SilverLeaf items, not routine research debt.
- Local Release 003 remains the last DEPLOYED release. Release 004 is a local
  candidate awaiting Task 34 review and an explicit deployment authorization.
- FY2027 budget/TRIM is verified in corpus but held out of Release 004 by the
  standing "Government & Taxes topic decision" gate.

## Operations

- Production weekly sequence is documented in `docs/hermes_weekly_entrypoint.md`
  (authoritative 13-step sequence, stale-milestone escalation, Model B fields).
- Weekly runner remains declared but disabled in `deploy/sjc-weekly-task.yaml`.
- FCE now has official project-page coverage (`nflroads.com` p=5639) + a
  recurring search profile; mobility registry updated.

## Latest evidence

- `reports/33-production-hardening-and-corpus-deepening.md`
- `logs/agents/sjc-intel-architect/2026-08-09_task33-hardening-corpus-deepening.md`
- `logs/runs/weekly/2026-08-09_task33-hardening-and-corpus-deepening.md`
