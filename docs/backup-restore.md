# SJC Intel — Backup and Restore Runbook

**Reference:** SHARED-002 Backup Standard (shared-conventions.md §9, evidence-wave-1/SHARED-002.md)
**Scope:** `sjc_intel` PostgreSQL database + documentation artifacts
**Gate:** Backup/Restore Gate — do NOT prune, cut over, or execute destructive cleanup before verified restore evidence exists.

---

## 1. Backup Scope

| Artifact | Method | Target |
|----------|--------|--------|
| `sjc_intel` database | pg_dump `--format=custom --compress=9` | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.dump` |
| Checksum | SHA-256 | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.dump.sha256` |
| Manifest | JSON | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.manifest.json` |
| Code (Git) | throwable — re-clone | n/a |
| YAML artifacts (shadow mode) | Git-tracked / export | `data/`, `registry/` |

## 2. Dump Format

```bash
pg_dump \
  --dbname="${SJC_INTEL_PG_BACKUP_URL:-${SJC_INTEL_PG_READER_URL}}" \
  --format=custom \
  --compress=9 \
  --file="${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.dump"
```

## 3. Checksum

```bash
sha256sum "${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.dump" \
  > "${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.dump.sha256"
```

## 4. Manifest

Manifest fields per Codex Session 1 §7:

| Field | Value |
|-------|-------|
| project | `sjc_intel` |
| database | `sjc_intel` |
| dump_file | `sjc_intel_YYYYMMDDTHHMMSSZ.dump` |
| checksum_sha256 | `<sha256 hex>` |
| created_at | ISO 8601 |
| created_by_role | `sjc_intel_backup` |
| postgres_version | `16` |
| schema_version | `<health contract schema version>` |
| migration_version | `<latest migration filename stem; currently 20260706_011 after new migrations apply>` |
| source_host_label | `macbook-development` or `ih-market-vps` |
| source_cluster_label | `sjc_intel` |
| file_size_bytes | `<bytes>` |
| tables_included | `<table list>` |
| off_host_copy_status | `pending ∣ copied ∣ verified` |
| restore_drill_status | `pending ∣ passed ∣ failed` |
| retention_class | `daily ∣ weekly ∣ migration_snapshot ∣ cutover` |
| notes_redacted | `true` |

## 5. Retention

| Location | Retention |
|----------|-----------|
| VPS (`/home/scraper/backups/postgres/sjc_intel/`) | 7 daily + 4 weekly (Sunday) |
| Mac (`/Users/buddy/projects/backups/postgres/sjc_intel/`) | 14 daily during active cutover, then 7 daily + 4 weekly |
| Migration/cutover snapshots | Immutable until explicitly retired by Buddy |

## 6. Off-Host Copy

```bash
scp "${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.dump" \
  buddy@mac:/Users/buddy/projects/backups/postgres/sjc_intel/
scp "${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.dump.sha256" \
  buddy@mac:/Users/buddy/projects/backups/postgres/sjc_intel/
scp "${BACKUP_DIR}/sjc_intel_${TIMESTAMP}.manifest.json" \
  buddy@mac:/Users/buddy/projects/backups/postgres/sjc_intel/
```

Verify checksum on Mac:
```bash
cd /Users/buddy/projects/backups/postgres/sjc_intel/
sha256sum -c "sjc_intel_${TIMESTAMP}.dump.sha256"
```

## 7. Restore Drill Procedure

**Cadence:** Monthly, on Mac
**Target:** Temporary PostgreSQL database (never production)

```bash
# Create temp database
createdb -U buddy sjc_intel_restore_drill

# Restore from dump
pg_restore \
  --dbname="postgresql:///sjc_intel_restore_drill" \
  --format=custom \
  --jobs=4 \
  "${DUMP_PATH}/sjc_intel_${TIMESTAMP}.dump"

# Run validation queries
psql -d sjc_intel_restore_drill -f db/validation/999_full_validation.sql
psql -d sjc_intel_restore_drill -c "SELECT count(*) FROM app.sources;"
psql -d sjc_intel_restore_drill -c "SELECT count(*) FROM app.intel_items;"
psql -d sjc_intel_restore_drill -c "SELECT count(*) FROM app.metric_snapshots;"
psql -d sjc_intel_restore_drill -c "SELECT max(discovered_at) FROM app.intel_items;"
psql -d sjc_intel_restore_drill -c "SELECT version, applied_at FROM app.sjc_intel_migrations ORDER BY applied_at;"

# Drop temp database when done
dropdb sjc_intel_restore_drill
```

## 8. Evidence Checklist

Before passing Backup/Restore Gate:

- [ ] Source inventory matches current schema
- [ ] Dump paths exist and are writable
- [ ] Checksum generated and verified
- [ ] Off-host copy completed and verified
- [ ] Restore command documented and tested
- [ ] Validation queries produce expected row counts
- [ ] Migration version recorded in manifest
- [ ] Manifest stored alongside dump
- [ ] Retention class assigned
- [ ] No secrets in manifest or logs

## 9. Failure Handling

| Condition | Action |
|-----------|--------|
| Dump fails | Set `backup_state=fail`, log error, retry at next window |
| Checksum mismatch | Discard dump, re-run, investigate transport |
| Off-host copy fails | Retry, escalate if persistent |
| Restore drill fails | Block cutover, investigate divergence |
| Missed 2+ routine backups | Set health `status=warn` |

## 10. Restore Drill Log Template

```
# Restore Drill — YYYY-MM-DD
Source dump: sjc_intel_YYYYMMDDTHHMMSSZ.dump
Checksum:     <sha256> → verified
Target DB:    sjc_intel_restore_drill (temp)
Restore command: pg_restore --dbname=... --format=custom --jobs=4
Validation:
  - app.sources:              <count> rows
  - app.intel_items:          <count> rows
  - app.sjc_intel_migrations: <version list>
  - max(discovered_at):       <timestamp>
Status: PASS / FAIL
```

---

## Inert Scripts Reference

These inert templates exist in `scripts/` but have no live execution capability:

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/backup_postgres.sh` | Inert backup wrapper | DEFINED ONLY — no execution |
| `scripts/restore_drill.sh` | Inert restore drill wrapper | DEFINED ONLY — no execution |
