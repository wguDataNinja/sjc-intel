# Task 23 hardening: live adapter, review workflow, health, brief, evidence

- Built `scripts/search_adapter.py`: provider-neutral search boundary
  (Google News RSS live + deterministic stub), per-run/lane/profile/subject/
  domain budgets, per-query receipts with hashes, domain/date constraints,
  retry, dedupe, no-match records.
- Refactored `scripts/live_adaptive.py` to use the adapter, added an
  independent evaluator stage, coverage-health artifact (`coverage.yaml`),
  stale-subject detection, and no-yield/source-gap reporting.
- Hardened `scripts/review_adaptive_proposal.py` (show with state-change and
  affected-searches, accept/reject/defer/rollback, dry-run, append-only
  decision history, brief regeneration) and `scripts/build_current_brief.py`
  (fail on missing evidence, stale-input warnings, `--check`, mode labeling,
  atomic snapshot + replacement, secret/private-path exclusion).
- Expanded `replay_evidence.yaml` with milestone due dates and additional
  subjects; added milestone-overdue/met, stale-subject, search-yield,
  source-freshness, and lane-coverage metrics plus a consolidated
  `final/coverage_health.yaml` artifact to the backtest harness.
- Added `scripts/prepare_publication_candidates.py` (preparation only).
- Ran clean supervised pilots SJC-LIVE-20260806-0201/0202/0203: 22 findings,
  22 pending proposals, 5 evaluator-rejected, 0 duplicates on rerun.
- Ran acceptance/rollback proof on isolated runtime; decision history
  clean. Regenerated CURRENT_BRIEF and dated snapshots under reports/briefs/.
- Full suite 274 passed; validate.py, corpus, scope, portability, and
  `git diff --check` all pass. No publication/review/PostgreSQL/Ivy changes;
  no commit made.
