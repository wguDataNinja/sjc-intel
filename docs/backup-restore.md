# SJC Intel — Backup and Restore Policy

**Status:** Authoritative SJC backup policy (external backup of the durable
file corpus). The PostgreSQL runbook below remains **dormant future-ready
scope** and is not the active backup path — the Mac file corpus is the
authoritative store.
**Last reconciled:** 2026-08-03 (Tasks 14–15).
**Ivy context:** Backup manifests per Ivy `docs/BACKUP_MANIFEST_STANDARD.md`;
data-class semantics per Ivy `docs/DATA_LIFECYCLE_STANDARD.md`.
**Deferral:** External-backup **implementation** (destination, automation,
provider) is deliberately deferred so the portfolio can address repositories
together under a shared Ivy policy. This document preserves the required scope,
restore objectives, and verification expectations; it does not select a
provider or implement automation.

---

## 0. Active file-corpus external-backup policy

### 0.1 Scope (what is backed up)

Back up everything durable, editorially significant, or operationally
necessary. The SJC repository is small (~5 MB tracked), so backing up the
durable corpus wholesale is practical and preferred.

| Class | Contents | Backup treatment |
|-------|----------|------------------|
| Must back up | `registry/` (sources, candidates, communities, tracked entities, search profiles), `data/intel_items/`, `data/source_events/`, `data/review_queue/` (incl. decisions), `data/index/` (dedupe state), `data/incoming/` (accepted staged bundles + receipts), `data/receipts/`, `data/monthly/`, `schemas/`, `db/` (migrations + validation), `deploy/` (incl. task manifest), docs (methodology, contracts, operator guides), `prompts/` | Every backup, encrypted |
| Reconstructable but worth backing up | `data/search_runs/`, `data/monthly/*/topic_clusters.yaml`, metric snapshots, generated summaries, derived reports, public release projections (once they exist) | Every backup; small |
| Optional / excluded | `.venv/`, `__pycache__/`, `node_modules/`, `.opencode/node_modules/`, `runtime/` (workspace + workers, regenerable), `.git` (re-clonable), local secrets (`.env*`, `*.key`, `*.pem` — never), transient raw downloads, duplicate bundle copies | Excluded or pruned |
| Historical / audit | Prior intel-item date trees, review decisions, task/report history | Backed up (small) |

Secret **values** are never backed up in normal backups; only secret **name
contracts** (e.g. `deploy/env.example`) are included.

### 0.2 Archive layout, compression, manifest

- Archive target follows Ivy convention: a cold-archive volume with a dated
  tree `archives/<date>/repos/sjc-intel/` and a manifest on the volume root
  (see Ivy `BACKUP_MANIFEST_STANDARD.md`). The destination decision is a Buddy
  choice; this policy is provider-neutral.
- Archive the **Git-exported working tree** (tracked files + small curated
  `data/` additions) as a tarball: `sjc-intel_<date>.tar.gz`.
- Text corpus is highly compressible (measured ~7×: `data/` ≈ 1.2 MB → ~175 KB
  gzip-9). Use `gzip -9`; consider a content-addressed or incremental scheme
  only if growth makes full archives impractical.
- One **manifest** per backup run (Ivy schema): source path, include/exclude
  groups, file counts, uncompressed and archive byte sizes, checksums, restore
  steps, verification result.
- **Checksums:** SHA-256 sidecar per archive; verify before transport.

### 0.3 Frequency and retention

- **Frequency:** full archive immediately after each meaningful session that
  produces durable state; a weekly full archive is the minimum cadence.
- **Retention:** keep the 4 most recent weekly archives plus one
  month-end archive; the latest verified archive is the restore baseline.
  Pre-launch/cutover snapshots are immutable until explicitly retired.
- **Growth expectation:** ~1–2 MB/session of corpus; weekly bundles add
  KB-scale per run. Full weekly archives remain tiny for the foreseeable
  future, so full (not incremental) backup is appropriate.

### 0.4 Restore objective and order

Restorable, in dependency order:

1. `registry/` (sources/candidates/entities) — identity of the system;
2. `schemas/` + `db/migrations/` — contracts and migration history;
3. `data/intel_items/` + `data/source_events/` — the corpus and provenance;
4. `data/review_queue/` + `data/index/` — review state and dedupe;
5. `data/receipts/` + `data/incoming/` — acknowledgement and staged-bundle state;
6. `docs/`, `prompts/`, `deploy/`, `scripts/` — configuration and tooling.

After restore: run `python3 scripts/validate.py`, `python3 -m pytest tests/`,
and rebuild `data/index/prior_items.yaml` + `data/review_queue/queue.yaml`
(idempotent). Restore to a clean checkout is a supported target.

### 0.5 Responsibility and failure handling

- **Initiator:** SJC operator (or delegated agent) on the Mac.
- **Verifier:** checksum verification after archive; monthly restore-sample
  verification from the archive; recorded in the manifest.
- **Failure:** failed archive or checksum mismatch → re-run; failed restore
  sample → investigate divergence and re-archive. Missed two+ backups →
  surface as a known gap.
- **Encryption:** the archive volume is encrypted; archive encryption verified
  in the manifest (encryption boundary is the volume/target, not the
  repository).

---

## 1. Backup Scope (dormant PostgreSQL — NOT the active path)

> DORMANT: The PostgreSQL corpus authority was intentionally not adopted. The
> Mac file corpus is authoritative (see `docs/postgresql_adapter.md`,
> `VPS_ROADMAP.md`). This runbook is retained future-ready and must NOT be
> treated as the active backup procedure.

| Artifact | Method | Target |
|----------|--------|--------|
| `sjc_intel` database | pg_dump `--format=custom --compress=9` | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.dump` |
| Checksum | SHA-256 | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.dump.sha256` |
| Manifest | JSON | `${SJC_INTEL_BACKUP_ROOT}/sjc_intel_YYYYMMDDTHHMMSSZ.manifest.json` |
| Code (Git) | throwable — re-clone | n/a |
| YAML artifacts (shadow mode) | Git-tracked / export | `data/`, `registry/` |

## 2. Dump Format

> Dormant scope (see §1). Retained for future SQL-readiness; not an active backup procedure.

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
