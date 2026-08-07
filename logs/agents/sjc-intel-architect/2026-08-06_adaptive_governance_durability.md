# Adaptive governance durability and readiness status

- Migrated the existing adaptive governance authority from ignored runtime
  files into tracked `data/adaptive_discovery/`:
  `accepted_state.yaml`, `pending_proposals.yaml`, `decisions.yaml`,
  `coverage_health.yaml`, and derived `health.yaml`.
- Kept raw run artifacts, receipts, and publication-candidate preparation in
  ignored `runtime/adaptive_discovery/`.
- Updated live adaptive commands and brief generation to use durable authority
  while retaining a separate transient artifact root.
- Added explicit pipeline health, operator status, and overall status to the
  brief. Pending proposals now make operator and overall status `NEEDS_REVIEW`
  without changing a healthy pipeline assessment.
- Added the repeatable `scripts/migrate_adaptive_governance.py` bootstrap
  command and regression tests for the status distinction.
- Verification: `pytest -q`, `python3 scripts/build_current_brief.py --check`,
  `python3 -m compileall -q scripts`, and `git diff --check` passed. No live
  monitor, source promotion, publication, or canonical-registry mutation ran.
