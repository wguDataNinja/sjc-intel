# SJC Intel — Database Migrations

## Directory Purpose

Holds forward-only PostgreSQL migration SQL for the `sjc_intel` database.

## Layout

```
db/
  migrations/
    YYYYMMDD_NNN_description.sql       # Forward migration
    rollback/
      YYYYMMDD_NNN_description_down.sql # Rollback SQL
    validation/
      YYYYMMDD_NNN_description_check.sql # Validation query
  fixtures/                             # Seed data YAML samples
  seeds/                                # Import scripts (future)
```

## Migration Convention

Every migration MUST provide:
1. Forward SQL — idempotent DDL where practical
2. Rollback SQL — reverses non-destructive changes (or documents irreversibility)
3. Validation query — row-count, constraint, or invariant check
4. Version record — INSERT into `app.sjc_intel_migrations`

## Architecture Reference

Full architecture: `ivy-control/vps/worker-control/reports/CODEX_SESSION_1_ARCHITECTURE.md`

Key sources:
- §9 SJC schema architecture
- §10 SJC migration and parity plan
- `ivy-control/vps/shared-conventions.md` §4 Migration File Layout

## Database Authority Gate

No migration may be applied against a live `sjc_intel` database without:
1. Schema and migration files reviewed and accepted
2. Fixture rehearsal passing locally
3. Database Authority Gate explicitly granted by Buddy
4. Pre-migration snapshot taken before any forward migration

## Rollback Boundary

- Rollback SQL is provided for non-destructive structural changes.
- Destructive changes (DROP TABLE, DROP COLUMN with data loss) require:
  - Pre-change backup and restore evidence
  - Immutable snapshot manifest
  - Explicit Destructive Operation Gate
  - Documented forward recovery path
- Data-destructive rollbacks are gated and snapshot-backed, not casually reversible.

## Database

| Property | Value |
|----------|-------|
| Database | `sjc_intel` |
| Server | PostgreSQL 16, localhost only |
| Ownership | `sjc_intel_owner` |
| Writer | `sjc_intel_writer` |
| Reader | `sjc_intel_reader` |
| Monitor | `sjc_intel_monitor` |
| Migrator | `sjc_intel_migrator` |
| Backup | `sjc_intel_backup` |
