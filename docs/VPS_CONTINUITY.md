# SJC Intel — VPS Continuity Document

**Date:** 2026-07-06
**Purpose:** Provide a durable record of the repository's PostgreSQL foundation, pilot readiness, and VPS deployment path. Future agents should read this first before making VPS-related changes.

## Read First

A future worker should begin in this order:

1. Repo-local `AGENTS.md` — routing and safety rules
2. Repo-local `SESSION.md` — current session state
3. Repo-local `LOG.md` — durable activity log
4. **This document** (`docs/VPS_CONTINUITY.md`) — project-specific VPS status
5. `ivy-control/vps/worker-control/reports/STRONG_AGENTIC_EXECUTION_REPORT.md` — most recent execution report
6. `ivy-control/vps/worker-control/reports/VPS_POSTGRES_CAPACITY_GATE_20260706.md` — current VPS PostgreSQL capacity decision
7. `ivy-control/vps/worker-control/reports/REAL_DATA_PILOT_GATE_ASSESSMENT_20260706.md` — current Gate status
8. `ivy-control/vps/worker-control/reports/POST_FOUNDATION_TO_VPS_ROADMAP.md` — forward roadmap

### Where Recent Work Was Logged

| What | Path |
|------|------|
| Repo-local activity log | `LOG.md` (this repo) |
| Repo-local session state | `SESSION.md` (this repo) |
| Migration/validation evidence | `db/migrations/`, `db/validation/999_full_validation.sql` |
| Clean backup manifest | `/Users/buddy/projects/backups/postgres/sjc_intel/manifest_clean_20260706T064146Z.yaml` |
| Restore evidence | Same manifest (restore_status: PASS, validation_status: PASS) |
| Pilot loader | `scripts/pilot_loader.py` |
| Pilot loader tests | `tests/test_pilot_loader.py` (11 tests PASS) |
| VPS continuity | This file |
| GitHub-readiness report | `ivy-control/vps/worker-control/reports/SJC_TRADERIE_GITHUB_AND_DOCS_READINESS.md` |
| VPS capacity Gate | `ivy-control/vps/worker-control/reports/VPS_POSTGRES_CAPACITY_GATE_20260706.md` |

### Authority Rule

This document summarizes project state. Ivy-Control (`/Users/buddy/projects/ivy-control/vps/`) controls shared infrastructure, Gates, deployment workflow, and cross-project sequencing. Always check the Ivy-Control reports before making cross-project or VPS-level changes.

---

## Current Completed Work

| Work Item | Status | Evidence |
|-----------|--------|----------|
| PostgreSQL database (`sjc_intel`) | ✅ Provisioned, Wave 1 | `ivy-control/vps/worker-control/reports/DATABASE_AUTHORITY_GATE_EXECUTION_REPORT.md` |
| 6 project roles | ✅ Provisioned | Same |
| 3 base schemas (app/archive/health) | ✅ Provisioned | Same |
| 9 schema migrations | ✅ Applied | `db/migrations/` — validated and backed up |
| `db/validation/999_full_validation.sql` | ✅ PASS | Post-migration restore drill evidence in backup manifest |
| Clean baseline backup + restore drill | ✅ PASS | Manifest at `/Users/buddy/projects/backups/postgres/sjc_intel/` |
| Pilot loader (`scripts/pilot_loader.py`) | ✅ Implemented, tested (11 tests) | dry-run/plan/apply/rollback/parity modes, writer-role-only |
| File authority (YAML/JSON) | ✅ Current source of truth | `data/` directory — not yet loaded to PG |
| Real-data ingestion | ❌ Not started | Blocked on pilot Gate approval |
| VPS PostgreSQL primary | ❌ Not approved | Current VPS failed capacity Gate on 2026-07-06 |
| VPS deployment | ❌ Not started | No services, no timers, no checkout |

## VPS Capacity Gate — 2026-07-06

The current `ih-market-vps` failed the PostgreSQL 16 capacity Gate for SJC Intel. PostgreSQL was not installed on the VPS, no SJC database was provisioned there, and no real-data pilot was executed.

Blocking evidence from the Gate:

- root filesystem 89% used with ~4.3 GB free;
- 2.0 GiB swap in use;
- active Chrome/browser, Idle Hacking collector, WGU, and private-search workloads;
- `/home/scraper/data/private/chat` at 13 GB;
- no passwordless sudo path for non-interactive provisioning/firewall verification;
- pending reboot before service-start behavior can be trusted.

Current authority after the failed Gate:

- Mac PostgreSQL 16 remains the active verified foundation, fallback, and migration source.
- SJC is not approved to use the current VPS as PostgreSQL primary.
- Preferred next option is a dedicated PostgreSQL VPS, minimum 2 vCPU / 4 GB RAM / 80 GB disk, or a resized current host of at least 4 vCPU / 8 GB RAM / 80 GB disk after cleanup, reboot verification, root/sudo maintenance access, and root filesystem below 70%.

---

## Relevant Ivy-Control Documents

| Document | Path | Purpose |
|----------|------|---------|
| Database Authority Gate execution report | `ivy-control/vps/worker-control/reports/DATABASE_AUTHORITY_GATE_EXECUTION_REPORT.md` | Live PostgreSQL state, roles, schemas, privileges |
| Deployment workflow | `ivy-control/vps/DEPLOYMENT_WORKFLOW.md` | Canonical Mac→GitHub→VPS deployment model |
| VPS capacity Gate | `ivy-control/vps/worker-control/reports/VPS_POSTGRES_CAPACITY_GATE_20260706.md` | Current VPS failed PostgreSQL capacity Gate |
| Post-foundation roadmap | `ivy-control/vps/worker-control/reports/POST_FOUNDATION_TO_VPS_ROADMAP.md` | Current forward roadmap with SJC pilot sequence |
| Real-data pilot Gate assessment | `ivy-control/vps/worker-control/reports/REAL_DATA_PILOT_GATE_ASSESSMENT_20260706.md` | SJC Gate status and pilot candidate definition |
| SJC/Traderie readiness report | `ivy-control/vps/worker-control/reports/SJC_TRADERIE_GITHUB_AND_DOCS_READINESS.md` | Pilot loader, GitHub readiness, docs inventory |
| Backup/restore Gate package | `ivy-control/vps/worker-control/reports/BACKUP_RESTORE_GATE_PACKAGE.md` | Template for backup/restore drills |
| Implementation program | `ivy-control/vps/IMPLEMENTATION_PROGRAM.md` | Layered implementation ledger with reconciliation sections |

---

## Historical Context

The following pre-foundation documents contain useful repository state facts that may still be relevant:

| Document | Useful Facts | Superseded Facts | Still-Open Work |
|----------|-------------|------------------|-----------------|
| Codex Session 1 Architecture | SJC schema design decisions, adapter boundary, health model | PG host assumption (was VPS, now Mac) | Service/timer template activation |
| Codex Session 1 Implementation Queue | Task breakdown for SJC-003 through SJC-009 | Task statuses (many now DONE or superseded by later reconciliations) | SJC-008 (VPS shadow run) remains gated |
| Evidence Wave 1 (SJC-001) | Original repo structure audit, test counts, source inventory | Specific file paths may have changed | None — audit findings addressed |
| Portfolio maturity audit | SJC maturity scores (Organization STRONG, Testing CRITICAL) | Test status (33 → 93+ tests now) | Testing gaps for pilot loader (11 new tests added) |

---

## Authority Boundaries

| Material | Travel Path | Notes |
|----------|-------------|-------|
| Code and migrations | GitHub → reviewed PR → approved SHA → VPS checkout | Exact SHAs, not branches |
| Secret values | Outside Git entirely | Stored in `~/.local/secure/ivy-control/postgres/` |
| Live PostgreSQL state | pg_dump/restore or deterministic importer | Not through normal Git history |
| YAML/JSON source authority | Not committed for deployment convenience | Source stays in repo `data/` for development |
| Real data | Does not belong in normal Git history | Use importer or controlled dump/restore |
| Services/timers | Activatable only after Scheduler Gate | No activation without Gate approval |

---

## Next Repository-Local Steps

1. Dry-run and plan verification: `python3 scripts/pilot_loader.py --dry-run --json`
2. Select dedicated DB VPS or resize/clean current VPS and rerun capacity Gate
3. Pilot Gate approval (Buddy)
4. Fresh pre-load backup: `pg_dump -Fc -Z 9 ...` + manifest
5. Bounded pilot: `python3 scripts/pilot_loader.py --apply --limit 10 --eligible-only`
6. Parity: `python3 scripts/pilot_loader.py --parity`
7. Rollback proof: `python3 scripts/pilot_loader.py --rollback`
8. Delete-and-reimport proof: apply → delete → re-apply → compare digest
9. Reviewed commits + GitHub push
10. Exact-SHA VPS deployment preparation
11. Shadow operation (VPS health-only timers)
12. Later cutover after evidence

---

## Pilot Loader Quick Reference

```bash
# Dry run (no mutation)
python3 scripts/pilot_loader.py --dry-run --json

# Plan (expanded evidence, no mutation)
python3 scripts/pilot_loader.py --plan --json

# Apply (requires Gate approval + recent backup)
python3 scripts/pilot_loader.py --apply --limit 10 --eligible-only

# Rollback (delete pilot rows by item_id set)
python3 scripts/pilot_loader.py --rollback

# Parity (compare file counts vs PG counts)
python3 scripts/pilot_loader.py --parity
```

## CI / GitHub Readiness

Current gaps:
- GitHub Actions workflow exists and passed locally via `python3 -m pytest tests/ -v`
- `deploy/` directory exists with inert service/timer templates
- Pilot-readiness documentation exists, but current VPS failed the PostgreSQL capacity Gate
- AGENTS.md references obsolete agents

See `ivy-control/vps/worker-control/reports/SJC_TRADERIE_GITHUB_AND_DOCS_READINESS.md` for full readiness status.
