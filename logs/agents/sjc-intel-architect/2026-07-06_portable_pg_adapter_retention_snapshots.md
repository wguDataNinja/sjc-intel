# 2026-07-06 — Portable PostgreSQL Adapter, Retention, Snapshots

## Task

Move SJC Intel from bounded pilot tooling toward a complete, portable
PostgreSQL-backed application architecture while preserving file authority and
pilot Gates.

## Files Read

- `AGENTS.md`
- `README.md`
- `README_INTERNAL.md`
- `SESSION.md`
- `LOG.md`
- `docs/VPS_CONTINUITY.md`
- Ivy-Control VPS authority docs and reports listed in the session prompt
- Current database, migration, adapter, pilot, retention, backup, deployment,
  and validation files

## Work Completed

- Implemented real PostgreSQL adapter operations in `scripts/pg_adapter.py`.
- Kept backend selection explicit and file fallback available in
  `scripts/storage_adapter.py`.
- Added migrations 10 and 11 for retention/pipeline metadata and compact metric
  snapshots.
- Added non-destructive retention dry-run and prune-selector tooling.
- Added deterministic metric snapshot generation.
- Added non-mutating Mac-to-VPS portability checks.
- Fixed pilot `--plan` mode to report `mode=plan` and preserve the established
  eligible NBOR 10-record digest.
- Corrected pilot-loader direct PostgreSQL apply statements to match the current
  schema while leaving apply backup-gated and unexecuted.
- Applied migrations 10 and 11 on the Mac development database after a
  pre-migration backup.
- Verified post-migration backup and restore into an isolated temporary
  database, then removed the restore database.

## Validation

- `python3 -m pytest tests/ -v` — 109 passed.
- `python3 scripts/validate.py` — all checks passed.
- `bash scripts/migration_readiness_check.sh` — 8 passed, 0 failed.
- `python3 scripts/portability_check.py` — PASS.
- `db/validation/999_full_validation.sql` — PASS on Mac development database
  and temporary restore database.
- `python3 scripts/retention.py --json` — 28 source policies, no destructive
  actions.
- `python3 scripts/metrics_snapshot.py --backend file --json` — 49 snapshots,
  0 written.
- Pilot dry-run and plan both preserve digest
  `6c0008d2855daf6c07fc4c0f2dda5478856cae775927bcc54cdda790571254b4`.

## Boundaries Preserved

- No VPS PostgreSQL installation.
- No real-data pilot apply.
- No production service or timer activation.
- No destructive pruning.
- No secrets committed or copied into docs.
- File-backed authority remains active.
