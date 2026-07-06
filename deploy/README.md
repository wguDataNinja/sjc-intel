# SJC Intel — Deployment

## Overview

This directory contains inert systemd service and timer templates for SJC Intel
workflows. These units are designed to run on the VPS
(`ih-market-vps`, `46.224.146.164`, user `scraper`).

**All units are inert. DO NOT INSTALL OR ENABLE WITHOUT SCHEDULER GATE.**

## Env File

The VPS environment file lives at `/home/scraper/config/sjc_intel.env`.
A safe template with variable names (no secrets) is at `deploy/env.example`.

Required variables:

| Variable | Purpose |
|----------|---------|
| `SJC_INTEL_PG_ADAPTER_ENABLED` | `false` (file mode) or `true` (PG mode) |
| `SJC_INTEL_PG_URL` | PostgreSQL connection URL (secret) |
| `SJC_INTEL_BACKUP_ROOT` | Backup dump directory |
| `SJC_INTEL_HEALTH_OUTPUT` | Health JSON output path |
| `SJC_INTEL_DATA_ROOT` | Data directory root |
| `SJC_INTEL_EXPORT_ROOT` | Export directory |
| `SJC_INTEL_MIGRATION_VERSION` | Current DB schema version |

## Manual Invocation

All services are `Type=oneshot` and can be run manually:

```bash
# Run NBOR ingestion (skips if lock held)
sudo -u scraper /home/scraper/apps/sjc-intel/scripts/extract_nbor.py

# Run BCC agenda ingestion
sudo -u scraper /home/scraper/apps/sjc-intel/scripts/extract_bcc_agenda.py

# Rebuild dedupe index
sudo -u scraper /home/scraper/apps/sjc-intel/scripts/rebuild_dedupe_index.py

# Build review queue
sudo -u scraper /home/scraper/apps/sjc-intel/scripts/build_review_queue.py

# Run health export
sudo -u scraper /home/scraper/apps/sjc-intel/scripts/health_export.py

# Run backup (PG only)
sudo -u scraper pg_dump --dbname="${SJC_INTEL_PG_URL}" --format=custom --compress=9
```

Or via systemd (after install):

```bash
sudo systemctl start sjc-intel-ingest-nbor.service
sudo systemctl status sjc-intel-ingest-nbor.service
```

## Lock / Concurrency

Each workflow has a dedicated lock file under
`/home/scraper/data/sjc-intel/.locks/{action}.lock`.

- Services use `flock -n` (non-blocking). If a lock is held, the service exits
  immediately with code 0 (skip — another instance is running).
- Locks prevent concurrent ingestion and process runs. Health checks and
  backups have independent locks and can run concurrently with ingestion.
- Lock files are automatically released when the service process exits.

## Service Inventory

| Unit | Timer | Workflow | Script |
|------|-------|----------|--------|
| `sjc-intel-ingest-nbor.service` | `.timer` (daily) | NBOR public notices | `scripts/extract_nbor.py` |
| `sjc-intel-ingest-bcc-agenda.service` | `.timer` (weekly) | BCC agenda items | `scripts/extract_bcc_agenda.py` |
| `sjc-intel-process-dedupe.service` | `.timer` (6-hourly) | Dedupe index rebuild | `scripts/rebuild_dedupe_index.py` |
| `sjc-intel-process-review-queue.service` | `.timer` (daily) | Review queue build | `scripts/build_review_queue.py` |
| `sjc-intel-check-health.service` | `.timer` (2-hourly) | Health export | `scripts/health_export.py` |
| `sjc-intel-backup-postgres.service` | `.timer` (daily @ 04:00) | PostgreSQL backup | inline `pg_dump` |

## PG Adapter / File Fallback

All services check `SJC_INTEL_PG_ADAPTER_ENABLED`:

- **`false` (default)** — File adapter is authoritative. Data is read from and
  written to YAML files under `data/`. No database dependency.
- **`true`** — PG adapter is enabled. Data goes to the `sjc_intel` database.
  Requires `SJC_INTEL_PG_URL` and Database Authority Gate approval.

During shadow mode, PG adapter can be enabled for dual-write while file
adapter remains authoritative. Cutover requires PostgreSQL Cutover Gate.

## Health Exports

After each run, the service should update the health JSON at
`${SJC_INTEL_HEALTH_OUTPUT}` (defined in the env file). The health format
follows SHARED-003 sanitized contract: no IPs, no paths, no credentials.

## Gates

| Gate | Required For |
|------|--------------|
| Scheduler Gate | Installing or enabling any `.timer` unit |
| Database Authority Gate | Setting `SJC_INTEL_PG_ADAPTER_ENABLED=true` |
| Backup/Restore Gate | Enabling `sjc-intel-backup-postgres.timer` |
| PostgreSQL Cutover Gate | Switching file → PG authority |
