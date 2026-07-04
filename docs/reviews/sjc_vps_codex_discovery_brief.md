# SJC_Intel — VPS Codex Discovery Brief

> **Purpose:** Compact implementation-planning brief for Codex to write/overwrite SJC_Intel's ROADMAP.md, aligned with the ivy-control VPS migration.
> **Generated:** 2026-07-04
> **Inspected:** SJC_Intel (local) + ivy-control/vps/ (VPS master plan)
> **Constraint:** Do not implement, do not write ROADMAP.md, do not commit.

---

## 1. Executive Summary

SJC_Intel is ready for VPS migration planning. It has 24 canonical sources, 3 interactive agents, 11 Hermes task prompts, 132 review queue items, a functioning cadence system, and a well-documented data model — all 100% local, file-based, and manual-trigger only. The ivy-control VPS transition (P1-P6) provides the infrastructure path: a shared Hetzner CX23 PostgreSQL instance, systemd timers, health monitoring, and a git-enforced PR loop.

The critical decisions Codex must make are: (a) PostgreSQL schema design for SJC_Intel's YAML-structured data, (b) which ingestion workflows are VPS-schedulable, (c) how raw artifacts are stored and retained, (d) the isolation model on a shared PostgreSQL instance, and (e) whether the Hermes read-only health monitoring role is implemented now or deferred. GitHub readiness blockers (secrets, local paths, missing CI) must be resolved before VPS deployment.

---

## 2. Stakeholder and Product Purpose

- **Primary user:** St. Johns County residents (SilverLeaf, Nocatee, countywide)
- **Product:** Structured intel items for editorial review — not published news
- **Status:** Supervised operator mode — no cron/launchd/scheduled automation
- **Current consumer:** Buddy + sjc-intel-architect agent
- **Future consumer:** Hermes agent (read-only health monitoring), public portfolio dashboard (sanitized metrics)
- **Non-goal:** Publishing, newsletter, or resident-facing output (deferred PUB-001/PUB-002)

---

## 3. Current SJC_Intel Architecture

### Pipeline Stages (Discovery Loops)

| Loop | Purpose | Status | Automation |
|------|---------|--------|-----------|
| A — Known-source monitoring | Poll 24 registered sources for new items | Designed, 2 pilots county_news + sheriff | 2 scripts (NBOR, BCC), rest manual |
| B — Search discovery | Find unregistered sources/items via web search | Design only | None |
| C — Historical backfill | Backfill by month (May 2026 done; Aug-Sep 2025 done) | Executed 2 backfills | Fully manual via Hermes prompts |
| D — Cross-section/beat | Detect recurring themes across sources | Design only | None |
| E — Taxonomy improvement | Collect/approve taxonomy gaps | Design only | None |
| F — Review/editorial | Gate items before publication | Phase 1+2 implemented (queue + status update) | `build_review_queue.py`, `update_review_status.py` |

### Implemented vs Planned

| Component | Status |
|-----------|--------|
| Source registry (24 canonical, 46 candidates) | ✅ Implemented |
| Source_event model | ✅ Implemented (partial — NBOR, BCC have events; county news, sheriff, utility lack events) |
| Intel_item extraction | ✅ 7 scripts, ~132 items across 6+ sources |
| Dedupe index (115 keys) | ✅ `rebuild_dedupe_index.py` |
| Review queue (132 entries, 43 pending, 83 verified) | ✅ `build_review_queue.py`, `update_review_status.py` |
| Interest filters (9 groups) | ✅ Active |
| Tracked entities (11) | ✅ ENT-001/002 complete |
| Community registry (18 communities) | ✅ Active |
| Cadence system with LAST_RUN markers | ✅ Active |
| Automated daily monitoring | ❌ No Hermes runtime, no cron |
| Utility extractor script | ❌ Manual only |
| School BoardDocs extraction | ❌ Pilot pending |
| Development tracker (GIS) | ❌ Browser automation needed |
| Permit portal extraction | ❌ Form interaction needed |
| Search discovery execution | ❌ Contracts drafted, untested |
| Human-readable reports | ❌ YAML-only output |
| Monthly closeout | ⏳ Last Jun 8 — overdue |
| BCC June 2026 agenda links | ❌ Broken (GAP-001) |

### Manual, Supervised, Scheduled, or Ad Hoc

| Mode | What |
|------|------|
| Manual trigger | All extraction runs (Buddy says "get to work") |
| Script-idempotent | Dedupe rebuild, queue rebuild, NBOR extraction, BCC extraction |
| Supervised/Hermes | Backfill passes, known-source monitor runs (prompt → execute → review) |
| Scheduled | None — intentionally no cron/launchd |
| Ad hoc | Source discovery, gap investigation, taxonomy changes |

---

## 4. Current Data Model and Formats

| Object | Format | Location | Records |
|--------|--------|----------|---------|
| source | YAML | `registry/sources.yaml` | 24 canonical |
| source_candidate | YAML | `registry/source_candidates.yaml` | 46 candidates |
| community | YAML | `registry/communities.yaml` | 18 communities |
| interest_filter | YAML | `registry/interest_filters.yaml` | 9 groups |
| tracked_entity | YAML | `registry/tracked_entities.yaml` | 11 entities |
| source_event | YAML | `data/source_events/{date}/{source_id}.yaml` | ~12+ events |
| intel_item | YAML | `data/intel_items/{date}/{source_id}.yaml` | ~132 items |
| review_queue_entry | YAML | `data/review_queue/queue.yaml` | 132 entries (43 pending, 83 verified, rest archived/rejected) |
| dedupe_entry | YAML | `data/index/prior_items.yaml` | 115 keys |
| monthly wrap | Markdown | `data/monthly/{YYYY-MM}/` | 2 months (May 2026, Aug-Sep 2025) |
| run logs | Markdown | `logs/runs/{daily,weekly,monthly}/` | ~10+ logs |
| agent logs | Markdown | `logs/agents/{name}/` | ~15+ logs |
| LAST_RUN state | Text (ISO 8601) | `logs/runs/*/LAST_RUN` | 3 files |
| session logs | Markdown | `logs/sessions/` | 1 master session doc |
| test fixtures | HTML/PDF/text | `tests/fixtures/` | ~5 files |
| backfill artifacts | YAML/MD | `data/monthly/`, `data/intel_items/` backfill-dated | 64 backfill items |
| taxonomies, beats, search terms | YAML | `registry/` | Various |

**All data is file-based YAML/MD/JSON.** No database. No SQL. No API. `pypdf` is the only extraction dependency.

---

## 5. Current Ingestion Modes

| Source | Current Mode | Extraction | Frequency | Script |
|--------|-------------|------------|-----------|--------|
| sjc_nbor_public_notices | Script + manual | Python (plain HTML, ASP.NET) | Daily | `extract_nbor.py` |
| sjc_bcc_calendar | Script + manual | Python (pypdf, PDF parsing) | Weekly | `extract_bcc_agenda.py` |
| sjc_county_news | Manual HTTP GET + parse | WordPress blog | Daily | None |
| sjso_news_stories | Manual HTTP GET + parse | WordPress blog | Daily | None |
| sjc_utility_department | Manual HTTP GET + parse | Government portal | Daily | None |
| sjc_emergency_management | Manual HTTP GET + parse | Government portal | Seasonal daily | None |
| sjc_school_district | Manual (pilot done) | WordPress/BoardDocs | Weekly | None |
| sjc_pza_boards | Not started | Government portal | Weekly | None |
| sjc_development_tracker | Not started | GIS map (JS) | Weekly | None |
| sjc_permit_status | Not started | Form search | Daily | None |
| fdot_district_two | Not started | Government portal | Daily | None |
| sjrwmd_watering | Not started | Government portal | Daily | None |
| CDDs (3) | Not started | WordPress/RSS | Weekly | None |
| st_johns_citizen | Not started (manual tip) | Local media | Daily | None |
| nocatee_community | Not started | CMS | Weekly | None |
| 8 other canonical | Not monitored | Various | Various | None |
| Backfills (May 2026, Aug-Sep 2025) | Manual Hermes prompts | Web search | One-off | Hermes prompt |
| SilverLeaf discovery | Manual Hermes prompt | Web search | One-off | Hermes prompt |

---

## 6. Workflow-by-Workflow VPS Suitability Matrix

### Key
- **Manual** = remain human-triggered on Mac
- **Supervised** = Mac-triggered, human reviews output
- **VPS-schedulable** = can run on VPS via systemd timer, deterministic
- **VPS-after-hardening** = needs extraction script, error handling, health check, or env support first
- **Unsuited** = requires human judgment, architecture decisions, or sensitive review

| Workflow | Suitability | Rationale |
|----------|-------------|-----------|
| **NBOR daily extraction** | VPS-schedulable | Plain HTML, script exists, deterministic, high yield (~25 items) |
| **Utility department daily check** | VPS-after-hardening | No extraction script yet — needs `extract_utility.py` |
| **County news daily** | VPS-after-hardening | WordPress blog — needs extraction script |
| **SJSO news daily** | VPS-after-hardening | Same WordPress pattern as county news |
| **Emergency management (seasonal daily)** | VPS-after-hardening | Needs extraction script + seasonal activation logic |
| **BCC weekly agenda** | VPS-after-hardening | Script exists but PDF link patterns change; needs error handling for broken links |
| **School district (weekly)** | VPS-after-hardening | BoardDocs extraction not built; Cloudflare/JS unknown |
| **CDD monitoring (weekly)** | VPS-after-hardening | WordPress/RSS feeds exist for 2/3 CDDs; needs extraction |
| **Nocatee community (weekly)** | VPS-after-hardening | CMS scrapeable; needs extraction script |
| **FDOT / roads** | VPS-after-hardening | Needs extraction script |
| **SJRWMD watering restrictions** | VPS-after-hardening | Needs extraction script |
| **Development tracker (GIS)** | VPS-after-hardening | Needs browser automation or API discovery |
| **Permit portal** | VPS-after-hardening | Needs form interaction script |
| **St. Johns Citizen monitoring** | Manual/Supervised | Media = tip/context; needs human judgment to not copy content |
| **Backfills** | Supervised/manual | Requires Hermes prompt writing, search strategy, architecture judgment |
| **Tracked-entity discovery** | Supervised/manual | Requires source gap analysis, taxonomy decisions |
| **Source candidate review/promotion** | Manual | Architecture judgment, Buddy approval required |
| **Dedupe index rebuild** | VPS-schedulable | Idempotent script, pure YAML scan |
| **Review queue rebuild** | VPS-schedulable, but gated | Idempotent, but queue state changes should be reviewed |
| **Review status updates** | Manual | Human editorial judgment |
| **Interest filter/taxonomy changes** | Manual | Architecture decisions, Buddy approval |
| **Monthly wrap/closeout** | Manual | Synthesis, judgment, gap analysis |
| **Health monitoring / LAST_RUN tracking** | VPS-schedulable | Deterministic after cadence rules are codified |

---

## 7. Automation and Approval Constraints

These are **non-negotiable** — the VPS architecture must enforce them:

| Constraint | Source | How to preserve |
|------------|--------|-----------------|
| Human review for sensitive items | AGENTS.md, Safety Rules | `pending_review` default; `human_review_required` flag; no auto-publish |
| Publishing deferred | README_INTERNAL.md, BACKLOG.md | Publishing status field reserved; never auto-publish |
| Official records first authority | discovery_loops.md, Durable Decisions | Evidence hierarchy in schema: `verification_status` field |
| Public sources only | AGENTS.md Safety Rules | No private groups, no login-gated portals |
| No fake accounts/impersonation | AGENTS.md Safety Rules | VPS extraction uses public HTTP only |
| Local media is tip/context only | AGENTS.md Safety Rules | `verification_status` not set to `source_confirmed` for non-official |
| No cron/launchd (explicitly deferred) | BACKLOG.md MON-004, cadence.md | WAIT — must be approved. Systemd timers are a NEW approval gate |
| Git policy: explicit paths only | AGENTS.md Git Policy | VPS scripts must stage by explicit path, no `git add .` |
| Agents never commit without instruction | AGENTS.md | VPS Hermes opens PRs only, never pushes to main |
| No browser automation without approval | Agent Cautions | Any Playwright/Camoufox extraction requires explicit approval |
| Evidence hierarchy (official > news > lead) | preflight codex doc | Must be preserved in all extracted item classifications |
| `human_review_required` for crime/emergency | ED-001 requirements | Must be set by extraction script or classifier |

---

## 8. PostgreSQL Isolation Recommendation

**Recommendation: Dedicated schema in a shared database (`ivy_control` → schema `sjc_intel`)**

| Criterion | Dedicated DB | Dedicated Schema | Same schema, table-prefixed |
|-----------|-------------|------------------|----------------------------|
| Migration simplicity | Moderate (separate `CREATE DATABASE`) | **Easy** (one `CREATE SCHEMA`) | Easy but risky |
| Backup/restore boundaries | **Best** (pg_dump per DB) | Good (pg_dump -n sjc_intel) | Poor (table filters) |
| Permissions | **Best** (DB-level GRANT) | Good (schema-level GRANT) | Poor (table-level) |
| Dashboard access | Good (separate connection) | **Good** (same connection, schema search_path) | Moderate |
| Future multi-project operations | Good (new DB per project) | **Good** (new schema per project) | Poor (name collisions) |
| Cross-project coupling risk | **Lowest** | Low (shared instance, schema boundary) | High |

**Decision:** Dedicated schema in a shared `ivy_control` database.

Rationale: SJC_Intel is one of many workloads (WGU-Reddit, ih_market_companion, idlehacking_kb chat) that will share the VPS PostgreSQL instance. A dedicated schema provides clean logical isolation, straightforward backup (`pg_dump -n sjc_intel`), per-schema permissions, and the same connection/dashboard access pattern as a dedicated DB — without the connection overhead. The dedicated-DB pattern can be adopted later if SJC_Intel outgrows the schema boundary.

---

## 9. PostgreSQL Table Inventory

### Naming: `sjc_intel.{table_name}`

| Table | Grain | PK | Important FKs | Important Timestamps | Retention | Mutable/Append |
|-------|-------|----|---------------|---------------------|-----------|----------------|
| `sources` | One source | `source_id` (text) | — | `created_at`, `updated_at` | Permanent | Mutable |
| `source_families` | One family | `family_id` (text) | — | `created_at` | Permanent | Mutable |
| `topics` | One topic | `topic_id` (text) | — | `created_at` | Permanent | Mutable |
| `beat_groups` | One beat | `beat_id` (text) | — | `created_at` | Permanent | Mutable |
| `communities` | One community | `community_id` (text) | — | `created_at`, `updated_at` | Permanent | Mutable |
| `tracked_entities` | One entity | `entity_id` (text) | — | `created_at`, `last_checked_at` | Permanent | Mutable |
| `entity_aliases` | One alias | `(entity_id, alias)` | `entity_id` | — | Permanent | Mutable |
| `source_entity_links` | Link | `(source_id, entity_id)` | `source_id`, `entity_id` | `created_at` | Permanent | Append |
| `collection_runs` | One run | `run_id` (bigserial) | `source_id` | `started_at`, `completed_at` | 90 days | Append |
| `fetched_documents` | One fetch/meeting | `document_id` (text, e.g. EVT-*) | `source_id`, `run_id` | `fetched_at`, `event_date` | 90 days | Append |
| `raw_artifact_metadata` | One raw artifact | `artifact_id` (bigserial) | `document_id` | `created_at` | 90 days (pointer only) | Append |
| `source_events` | Same as YAML source_event | `event_id` (text) | `source_id` | `event_date`, `discovered_at` | Permanent | Mutable |
| `intel_items` | One intel item | `item_id` (text) | `source_id`, `event_id` | `discovered_at`, `created_at` | Permanent | Mutable |
| `item_entity_links` | Link | `(item_id, entity_id)` | `item_id`, `entity_id` | `created_at` | Permanent | Append |
| `item_topic_links` | Link | `(item_id, topic_id)` | `item_id`, `topic_id` | `created_at` | Permanent | Append |
| `deduplication_keys` | One fingerprint | `dedupe_key` (char(16)) | `item_id` (optional) | `created_at` | Permanent | Append |
| `provenance` | Provenance event | `provenance_id` (bigserial) | `item_id`, `event_id` | `created_at` | Permanent | Append |
| `extraction_results` | Extraction output | `extraction_id` (bigserial) | `document_id` | `created_at` | 90 days | Append |
| `enrichment_results` | RI classification | `enrichment_id` (bigserial) | `item_id` | `created_at` | 30 days | Append |
| `review_status_history` | Status change | `review_id` (bigserial) | `item_id` | `changed_at` | Permanent | Append |
| `publishing_status_history` | Pub event | `publish_id` (bigserial) | `item_id` | `published_at` | Permanent | Append |
| `pipeline_errors` | Error record | `error_id` (bigserial) | `run_id`, `source_id` | `occurred_at` | 90 days | Append |
| `pipeline_health` | Run health | `run_id` | `run_id` | `checked_at` | 30 days | Append |
| `health_snapshots` | Periodic health | `snapshot_id` (bigserial) | — | `snapped_at` | 30 days | Append |
| `scheduler_executions` | Timer run | `execution_id` (bigserial) | `run_id` | `started_at` | 90 days | Append |
| `schema_versions` | Migration record | `version_id` (text) | — | `applied_at` | Permanent | Append |

**Note:** Raw HTML/PDF/text content stays outside PostgreSQL (see §10). The `raw_artifact_metadata` table holds the pointer (path, checksum, size).

---

## 10. File/Raw-Artifact Retention Model

### Out-of-Database (filesystem)

| Artifact | Storage Path Pattern | Retention | Policy |
|----------|---------------------|-----------|--------|
| Raw HTML | `{artifact_root}/raw_html/{source_id}/{YYYY}/{MM}/{DD}/{event_id}.html` | 7 days | Compressed (gzip), auto-purge |
| PDFs | `{artifact_root}/pdfs/{source_id}/{YYYY}/{MM}/{DD}/{filename}.pdf` | 7 days | Compressed, auto-purge |
| Images | `{artifact_root}/images/{source_id}/{YYYY}/{MM}/{DD}/{filename}` | 7 days | Compressed, auto-purge |
| Screenshots | `{artifact_root}/screenshots/{source_id}/{YYYY}/{MM}/{DD}/{event_id}.png` | 7 days | Auto-purge |
| Browser traces | `{artifact_root}/traces/{source_id}/{YYYY}/{MM}/{DD}/{event_id}.zip` | 7 days | Auto-purge |
| Large text extracts | `{artifact_root}/extracts/{source_id}/{YYYY}/{MM}/{DD}/{item_id}.txt` | 30 days | Compressed, auto-purge |
| Test fixtures | `tests/fixtures/` (Git) | Permanent (Git) | Manual curation |
| Logs | `{log_root}/` | 14 days | logrotate, auto-rotate |

### Naming Convention
```
{source_id}/{event_type}/{YYYY}/{MM}/{DD}/{event_id}_{sequence}.{ext}
```

### Checksums
- Every file artifact gets a `sha256sum` recorded in `raw_artifact_metadata.content_hash`
- The database pointer is authoritative; the file can be re-fetched if checksum matches

### Git Fixture Subset
- Small (<100KB), representative HTML/PDF/text fixtures committed in `tests/fixtures/`
- No full-size snapshots committed
- Fixtures are examples, not backups

---

## 11. Backup and Restore Requirements

| Requirement | Detail |
|-------------|--------|
| PostgreSQL backups | Daily `pg_dump -n sjc_intel` via systemd timer |
| WAL strategy | Archive WAL to `{artifact_root}/wal_archive/`; 7-day retention |
| Logical backup | Weekly full schema-level dump to Mac via scp/rsync |
| Raw artifact backup | NOT backed up individually — re-fetchable from source |
| Config/schema backup | Git is the backup — `registry/`, `schemas/`, `scripts/` |
| Retention — DB | 7 daily dumps, 4 weekly, 3 monthly |
| Retention — WAL | 7 days |
| Retention — artifacts | As defined in §10 |
| Restore testing | Monthly restore-to-timestamp test (first Sunday) |
| Project-level restore | `pg_restore -n sjc_intel` from daily dump |
| Full shared-instance restore | `pg_restore` from full db dump (weekly) |
| DR documentation | `deploy/disaster_recovery.md` |

---

## 12. Shared Dashboard Metrics

### Public-Safe (can appear on sanitized portfolio dashboard)

| Metric | Source | Public? |
|--------|--------|---------|
| Last successful run timestamp | `pipeline_health.last_successful_run` | ✅ Yes |
| Expected cadence | `sources.monitor_frequency` | ✅ Yes |
| Freshness lag (hours since last run) | Computed | ✅ Yes |
| Source health (reachable/unreachable) | `pipeline_health.source_reachable` | ✅ Yes |
| Run duration (last run, seconds) | `collection_runs.duration` | ✅ Yes |
| Fetched document count (last run) | `extraction_results.document_count` | ✅ Yes |
| Extracted item count (last run) | `extraction_results.item_count` | ✅ Yes |
| Duplicate rate | `extraction_results.duplicate_count / item_count` | ✅ Yes |
| Error count (last run) | `pipeline_errors.count` | ✅ Yes |
| Consecutive failures per source | `pipeline_health.consecutive_failures` | ✅ Yes |
| Scheduler status (active/inactive) | `scheduler_executions` latest | ✅ Yes |
| Schema migration status | `schema_versions` latest | ✅ Yes |

### Internal-Only

| Metric | Reason |
|--------|--------|
| Pending review count | Unreviewed items are internal editorial state |
| Verified item count | Internal quality metric |
| Stale source count | Operational — could reveal gaps |
| Backup freshness | Operational — internal reliability metric |

### Potentially Sensitive

| Metric | Sensitivity |
|--------|-------------|
| Specific item IDs or URLs | Could reveal ongoing monitoring patterns |
| Source-specific error details | Could reveal source parsing weaknesses |
| Run output volumes per source | Could reveal monitoring cadence |

---

## 13. Hermes Role and Permission Boundaries

### May Do (read-only health)
- Read `pipeline_health`, `health_snapshots`, `scheduler_executions` tables
- Read `pipeline_errors` table (read-only, last 24h)
- Compare last_run time vs expected cadence
- Compute freshness lag
- Summarize incidents from `pipeline_errors`
- Open GitHub branches with proposed health fixes
- Create PRs with health-related changes (e.g., update `check_interval_hours`)
- Email/WhatsApp alert if consecutive failures > threshold

### Must Never Do
- Write to `intel_items`, `source_events`, `review_status_history`
- Modify `sources`, `communities`, `tracked_entities` registries
- Bypass human review (`pending_review` must remain)
- Hold broad secrets (database credentials = in env file only, not in Hermes memory)
- Merge its own PRs (Buddy or Git Steward merges)
- Modify `deploy/`, `scripts/`, or `schemas/` without PR
- Access `raw_artifact_metadata` pointer paths directly (file system access out of scope)

### Narrow Permissions Model
```
GRANT SELECT ON sjc_intel.pipeline_health, sjc_intel.health_snapshots,
              sjc_intel.scheduler_executions, sjc_intel.pipeline_errors
TO hermes_reader;
```

---

## 14. GitHub Readiness Blockers

These must be resolved before VPS deployment:

### Must Fix

| Blocking Issue | Location | Fix |
|---------------|----------|-----|
| `/Users/buddy/` hardcoded paths | Possibly in scripts/schemas | Parameterize or use `$HOME` |
| No `.env` or `.env.example` | Root | Create `.env.example` with all env vars |
| No `LICENSE` file | Root | Add MIT or note private |
| No `.gitignore` for `logs/runs/` (currently tracked) | Root | Add to `.gitignore` if not wanted; or document as intentional |
| `data/` directory with mutable YAML files | `data/` | Gitignore runtime data OR commit curated state only |
| `tests/fixtures/` — ensure no oversize | `tests/fixtures/` | Verify all fixtures < 1MB |

### Should Fix

| Issue | Location | Fix |
|-------|----------|-----|
| No CI workflow | Root | Add YAML validation + schema lint workflow |
| No dependency installation script | Root | Add `requirements.txt` (pypdf) + install instructions |
| ROADMAP.md is a stub | Root | Codex will overwrite it |
| `docs/data-model.md` path doesn't exist (only `docs/data_model.md`) | Docs | Document the naming convention |
| Memory file stale since June 3 | `.opencode/agent_memory/` | Update after this session |
| No branch naming convention documented | AGENTS.md | Add conventional branch prefix policy |
| No migration SQL directory | `deploy/` | Not yet needed — schema design first |

### Acceptable As-Is (private repo)

| Item | Rationale |
|------|-----------|
| `session.md` tracked for active dev | Acceptable in private repo |
| `LOG.md` tracked | Required append-only history |
| `data/review_queue/queue.yaml` tracked with 132 entries | Curated project state — per git policy |
| `data/index/prior_items.yaml` tracked | Curated project state |
| `data/source_events/` and `data/intel_items/` | Data artifacts — per git policy, may be committed when curated |

---

## 15. Required VPS Services/Timers

### Services (systemd units)

| Service | Purpose | Dependencies |
|---------|---------|-------------|
| `sjc-extract-nbor.service` | Run NBOR extraction script | Database must be up |
| `sjc-extract-utility.service` | Run utility department check | Extraction script must exist |
| `sjc-extract-county-news.service` | Run county news check | Extraction script must exist |
| `sjc-extract-sheriff.service` | Run SJSO news check | Extraction script must exist |
| `sjc-health-check.service` | Run source health checks | Python env with requests |
| `sjc-dedupe-rebuild.service` | Rebuild dedupe index | Extraction must complete |
| `sjc-queue-rebuild.service` | Rebuild review queue | Dedupe must complete |
| `sjc-dashboard-export.service` | Export health JSON | Health check must complete |
| `sjc-backup-pg.service` | PostgreSQL dump | pg_dump available |
| `sjc-retention-cleanup.service` | Purge old artifacts | None |

### Timers (systemd timer units)

| Timer | Cadence | Service | Dependencies |
|-------|---------|---------|-------------|
| `sjc-daily-ingestion.timer` | Daily at 06:00 ET | `sjc-extract-nbor.service` | None (NBOR first) |
| `sjc-utility.timer` | Daily at 06:15 ET | `sjc-extract-utility.service` | After NBOR |
| `sjc-county-news.timer` | Daily at 06:30 ET | `sjc-extract-county-news.service` | After utility |
| `sjc-sheriff.timer` | Daily at 06:45 ET | `sjc-extract-sheriff.service` | After county news |
| `sjc-bcc-weekly.timer` | Weekly Wed 07:00 ET | BCC extraction | Meeting-schedule aware |
| `sjc-health.timer` | Daily at 07:00 ET | `sjc-health-check.service` | After all extractions |
| `sjc-dedupe.timer` | Daily at 07:15 ET | `sjc-dedupe-rebuild.service` | After health |
| `sjc-queue.timer` | Daily at 07:20 ET | `sjc-queue-rebuild.service` | After dedupe |
| `sjc-dashboard.timer` | Daily at 07:25 ET | `sjc-dashboard-export.service` | After queue |
| `sjc-backup.timer` | Daily at 04:00 ET | `sjc-backup-pg.service` | None |
| `sjc-retention.timer` | Daily at 03:00 ET | `sjc-retention-cleanup.service` | None |
| `sjc-emergency-seasonal.timer` | Daily Jun-Nov at 06:10 ET | Emergency extraction | Seasonal logic |

**Note:** All timers require Buddy approval per MON-004.

---

## 16. Environment and Secrets Model

### Environment Variables

```
# --- Database ---
SJC_DB_HOST=localhost                          # Safe config
SJC_DB_PORT=5432                               # Safe config
SJC_DB_NAME=ivy_control                        # Safe config (shared instance)
SJC_DB_SCHEMA=sjc_intel                        # Safe config
SJC_DB_USER=sjc_intel_app                      # Safe config
SJC_DB_PASSWORD=<secret>                       # SECRET — .env only

# --- Storage ---
SJC_ARTIFACT_ROOT=/var/opt/sjc_intel/artifacts # Host-local
SJC_LOG_ROOT=/var/opt/sjc_intel/logs           # Host-local
SJC_HEALTH_OUTPUT=/var/www/health/status.json  # Host-local
SJC_DASHBOARD_EXPORT=/var/www/health/dashboard.json  # Host-local

# --- Hermes ---
SJC_HERMES_DB_USER=hermes_reader               # Safe config
SJC_HERMES_DB_PASSWORD=<secret>                # SECRET — .env only

# --- HTTP ---
SJC_HTTP_USER_AGENT=SJC_Intel/1.0              # Safe config
SJC_HTTP_TIMEOUT_SECONDS=30                    # Safe config
SJC_HTTP_RETRY_MAX=3                           # Safe config

# --- Optional ---
SJC_ALERT_WEBHOOK_URL=<secret>                 # SECRET — optional
```

### Classification

| Type | Examples | Where stored |
|------|----------|-------------|
| Safe config | All non-password, non-secret env vars | `.env.example` + `deploy/env/` templates |
| Secrets | DB passwords, webhook URLs | `.env` (gitignored), Vault (future) |
| Host-local | Artifact root, log root, health output path | `deploy/env/production.env` (gitignored) |
| Git-managed examples | `deploy/env/env.example` | Committed |

---

## 17. Publishing Deferral and Future Support

**Confirmed: Publishing remains deferred.** PUB-001/PUB-002 are explicitly deferred in BACKLOG.md. The architecture must preserve:

| Capability | How to preserve |
|------------|----------------|
| Review status | `review_status` on `intel_items` table — `pending_review`, `verified`, etc. |
| Publishing eligibility | `publishing_eligible` computed field: `verified AND NOT human_review_required` |
| Publishing status/history | `publishing_status_history` table — append-only log of publication events |
| Approval gates | `human_review_required` column blocks auto-publishing; `verified` status gates eligibility |
| Redaction/safety checks | `sensitivity` field + `reviewer_notes` on `intel_items` |
| Future export capability | `publishing_status_history` stores target channel, timestamp, export format |

No publishing channel implementation needed now. The schema supports it for future use.

---

## 18. Dependencies and Critical Path

```
GitHub Readiness
    │
    ▼
PostgreSQL Schema Design ←───────┐
    │                            │
    ▼                            │
PostgreSQL Migration (SQL DDL) ──┤
    │                            │
    ▼                            │
Data Migration (YAML → PG) ─────┤
    │                            │
    ▼                            │
Ingestion Scripts (extract_*) ──┤
    │                            │
    ▼                            │
Deterministic Health Checks ────┤
    │                            │
    ▼                            │
VPS Deployment: services/timers─┤
    │                            │
    ▼                            │
Backup/Restore Setup ───────────┤
    │                            │
    ▼                            │
Dashboard Integration ──────────┤
    │                            │
    ▼                            │
Hermes Read-Only Access ────────┤
    │                            │
    ▼                            │
Cutover (Mac manual → VPS timer)┘
```

### Parallelizable Tracks

| Track | Can run in parallel with |
|-------|------------------------|
| GitHub readiness | Schema design |
| Ingestion script writing | Schema design, migration |
| Health check design | Schema design |
| Dashboard frontend | Migration, ingestion scripts |

### Gating Decisions

| Gate | Blocks | Needs |
|------|--------|-------|
| Architecture approval | Schema design | Buddy + Codex |
| Database isolation approval | Migration | Buddy |
| Schema approval | Migration/bulk loading | Buddy |
| GitHub push approval | VPS deployment | Buddy |
| VPS deployment approval | Timer enablement | Buddy |
| Timer enablement approval | Production cutover | Buddy (per MON-004) |
| Production cutover approval | Live VPS operation | Buddy |
| Dashboard public approval | Dashboard | Buddy |
| Hermes permission approval | Hermes access | Buddy |

---

## 19. Unresolved Decisions

| Decision | Options | Impact | Needs |
|----------|---------|--------|-------|
| Schema `sjc_intel` vs dedicated DB `sjc_intel` | Schema (recommended) vs DB | Migration complexity, isolation | Buddy approval |
| Raw artifact storage root | `/var/opt/sjc_intel/artifacts` vs `/home/scraper/data/sjc_intel/` | VPS filesystem layout | Architecture decision |
| Post-migration: keep YAML files? | Yes (source of truth until migration validated) vs No (PG is canonical) | Rollback safety | Migration review |
| Hermes read-only access now or P6 defer | Now (dashboard + alerting) vs After cutover | Timelines | Buddy |
| Ingestion script priority order | NBOR→Utility→County→Sheriff→BCC→Emergency vs reverse | Which gets automated first | Codex roadmap |
| Dashboard tech stack | Static JSON file vs lightweight web server | Complexity | Architecture decision |

---

## 20. Decision Table

| Decision | Recommendation | Confidence | Needs Buddy Approval? |
|----------|---------------|------------|----------------------|
| PostgreSQL isolation | Dedicated `sjc_intel` schema in shared `ivy_control` DB | High | ✅ Yes |
| Raw artifact storage | Filesystem, not PG | High | ❌ (architectural, brief-level) |
| Dedupe (post-migration) | PG `deduplication_keys` table as canonical | High | ❌ |
| Review queue (post-migration) | PG `review_status_history` as canonical | High | ❌ |
| Hermes DB role | `hermes_reader` — SELECT-only on health tables | High | ✅ Yes |
| Publishing activation | Remain deferred | High | Already deferred per BACKLOG |
| Data migration strategy | YAML → PG bulk load, both live during cutover | Medium | ✅ Yes |
| Dashboard access pattern | Static JSON file export, no web server | Medium | ❌ |
| Timer activation | Gate behind explicit Buddy approval | High | ✅ Yes (per MON-004) |
| Ingestion script creation | Build extract_*.py for each VPS-schedulable workflow | Medium | Architecture-level |
| BCC broken links fix | Before schema migration (data completeness) | Medium | Architecture-level |

---

## 21. Recommendations for the Codex Roadmap Prompt

The Codex prompt should instruct the planner to:

1. **Accept this brief** (`docs/reviews/sjc_vps_codex_discovery_brief.md`) as the primary input for scoping.
2. **Read these files** (see §22) before writing ROADMAP.md.
3. **Design the PostgreSQL schema** first — this gates everything else.
4. **Produce a phased roadmap** with explicit HITL checkpoints:
   - Phase 0: GitHub readiness + env setup
   - Phase 1: PostgreSQL schema DDL + migration bootstrap
   - Phase 2: data migration (YAML → PG, dual-write validated)
   - Phase 3: ingestion scripts for VPS-schedulable workflows
   - Phase 4: health checks + dashboard export
   - Phase 5: VPS services/timers + backup
   - Phase 6: Hermes read-only access (optional, gated)
   - Phase 7: cutover and manual-to-timer transition
5. **Identify all approval gates** between phases.
6. **Flag the constraint** that publishing remains deferred.
7. **Keep the roadmapped changes bounded** — no new features outside migration scope unless explicitly requested.

---

## 22. Exact Files Codex Should Inspect

### SJC_Intel (Primary Context)

| Priority | File | Why |
|----------|------|-----|
| 1 | `README_INTERNAL.md` | Current phase, architecture tables, open loops |
| 2 | `AGENTS.md` | Git policy, safety rules, delegation rules, session checklists |
| 3 | `docs/data_model.md` | Entity-relationship model, ID conventions, lifecycle statuses |
| 4 | `docs/taxonomy.md` | Controlled vocabularies, source families, beat groups |
| 5 | `docs/cadence.md` | Daily/weekly/monthly rhythms, LAST_RUN rules |
| 6 | `BACKLOG.md` | All open/in-progress tasks with dependencies |
| 7 | `registry/sources.yaml` | 24 canonical sources with monitor_config blocks |
| 8 | `registry/source_candidates.yaml` | 46 candidates awaiting review |
| 9 | `registry/interest_filters.yaml` | 9 keyword-based priority rule groups |
| 10 | `registry/tracked_entities.yaml` | 11 entities with lifecycle statuses |
| 11 | `registry/communities.yaml` | 18 geographic communities |
| 12 | `schemas/intel_item.schema.yaml` | Intel item field-level spec (v2.0) |
| 13 | `schemas/source_event.schema.yaml` | Source event field-level spec |
| 14 | `schemas/tracked_entity.schema.yaml` | Tracked entity field-level spec |
| 15 | `schemas/source.schema.yaml` | Source registry field-level spec |
| 16 | `docs/editorial/ed001_review_queue_requirements.md` | Review queue design, escalation logic |
| 17 | `docs/editorial/batch_review_rules.md` | Batch review rules |
| 18 | `docs/discovery_loops.md` | All 6 loop definitions, agent roles |
| 19 | `docs/monitoring_workflow.md` | 10-step monitoring workflow |
| 20 | `docs/operator_mode.md` | Startup routine, task selection |
| 21 | `docs/design/tracked_entities_design.md` | Entity relationship design |
| 22 | `docs/data_inventory/COVERAGE.md` | Data coverage map |
| 23 | `docs/data_inventory/GAPS.md` | Data gaps analysis |
| 24 | `docs/reviews/codex_review_output.md` | Prior Codex review findings |
| 25 | `docs/reviews/codex_review_packet_2026-06-26.md` | Prior review packet |
| 26 | `docs/reviews/codex_roadmap_preflight.md` | Prior preflight analysis |
| 27 | `docs/reviews/sjc_vps_codex_discovery_brief.md` | THIS FILE |
| 28 | `scripts/extract_nbor.py` | NBOR extraction pattern |
| 29 | `scripts/extract_bcc_agenda.py` | BCC agenda extraction pattern |
| 30 | `scripts/build_review_queue.py` | Queue builder (entity matching) |
| 31 | `scripts/rebuild_dedupe_index.py` | Dedupe index rebuild |
| 32 | `.opencode/agent_memory/sjc-intel-architect.memory.md` | Latest architect memory |

### ivy-control / VPS (Context)

| Priority | File | Why |
|----------|------|-----|
| 1 | `/Users/buddy/projects/ivy-control/vps/README.md` | VPS master plan (P1-P6, git-enforced loop) |
| 2 | `/Users/buddy/projects/ivy-control/vps/vps-host.md` | Hetzner CX23 identity, workloads, Hermes feasibility |
| 3 | `/Users/buddy/projects/ivy-control/vps/logs/session/gpt1.md` | VPS transition session log — GitHub readiness, repo standard |
| 4 | `/Users/buddy/projects/ivy-control/docs/project-context/ecosystem-cross-repo-review-2026-07-04.md` | Cross-repo review — SJC_Intel profile at lines 45-116 |
| 5 | `/Users/buddy/projects/ivy-control/ivy-vps/repo-operating-standard.md` | Repo doc/process standard for downstream repos |
| 6 | `/Users/buddy/projects/ivy-control/ivy-vps/github-readiness-checklist.md` | 5-section GitHub gate |

### Files That Do NOT Exist

| Expected Path | Status |
|--------------|--------|
| `docs/data-model.md` | ❌ Does not exist (only `docs/data_model.md` exists) |
| `TODO.md` | ❌ Does not exist |
| `docs/monitor_specs/sjc_utility_department.md` | ✅ Exists |
| `docs/safety/` or `docs/privacy/` | ❌ Not present in the repo |
| `docs/agent-contracts/` | ❌ Not present (agents in `.opencode/agents/`) |

---

## Appendix: Git Commands for Inspection

```bash
# SJC_Intel
cd /Users/buddy/projects/sjc_intel
git log --oneline -20
git status --short
git diff --stat

# ivy-control VPS
cd /Users/buddy/projects/ivy-control
git log --oneline -5 vps/
```

**Both repos are local.** No GitHub remotes are active for SJC_Intel. ivy-control is private-ready with warnings but not pushed.
