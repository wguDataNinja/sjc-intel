# Codex Roadmap Prompt — SJC_Intel + VPS Migration

> **Intended use:** Paste this prompt into a Codex high-reasoning planning session.
> **Mission:** Write or overwrite `ROADMAP.md` for SJC_Intel, aligned with the ivy-control shared VPS migration.
> **Constraint:** Planning only. Do not implement. Do not modify scripts, schemas, registries, data, or deployment files.
> **Constraint:** Do not enable production timers or cutover without explicit approval gates.
> **Constraint:** Public publishing remains deferred.
> **Prepared:** 2026-07-04

---

## 0. Shared Conventions Reference

Before reading other context, read `/Users/buddy/projects/ivy-control/vps/shared-conventions.md`. It defines cross-repo defaults for: database isolation (database-per-project), role naming (`{project}_writer`, `{project}_reader`, `{project}_monitor`, `{project}_migrator`), migration file layout (`db/migrations/YYYYMMDD_NNN_description.sql`), environment variable naming, VPS filesystem layout, systemd naming (`{project}-{role}-{action}`), health contract format, backup destination (`~/projects/backups/postgres/{project}/`), branch/PR ownership, Hermes conventions, and gate terminology.

Align every decision with these conventions. Justify any deviation explicitly.

## 1. Your Task

Read all required context files from both SJC_Intel and ivy-control/VPS planning. Then produce a single file: `ROADMAP.md` at the repo root of `/Users/buddy/projects/sjc_intel`. The roadmap must be an implementation-ready plan for weaker Worker agents, with explicit HITL checkpoints, Git Steward commit boundaries, and VPS deployment/cutover gates.

**Evidence hierarchy:** Treat the discovery brief and input packets as derived evidence, not proven fact. Inspect the actual repo files to confirm every claim. Clearly distinguish: (a) verified facts from repo inspection, (b) inferred conclusions, (c) open decisions requiring Buddy input.

## 2. Ecosystem Direction

Key facts you must align with:

- `ivy-control/vps/` (at `/Users/buddy/projects/ivy-control/vps/`) is the active VPS planning area. `vps/README.md` is the VPS master plan.
- `ivy-vps/` is superseded reference material — do not rely on it.
- Recurring ingestion workloads are moving toward one shared VPS (Hetzner CX23, 46.224.146.164).
- One PostgreSQL instance will be shared, logically separated by project (database-per-project per shared-conventions §2). SJC Intel uses database `sjc_intel`, not a shared `ivy_control` schema.
- GitHub is the code/review boundary — SJC_Intel currently has NO GitHub remote.
- Deterministic health checks must work without Hermes (Python script + JSON output).
- Hermes may later inspect health, summarize incidents, and create branches/PRs under narrow permissions — but never modify production directly.
- A sanitized public dashboard will show health and freshness across multiple real pipelines.
- Public publishing for SJC_Intel remains deferred (PUB-001/PUB-002 in BACKLOG.md).
- Manual review, evidence controls, and approval gates must remain intact.

## 3. Required Context Files

### SJC_Intel (Primary)

Read every file in this list:

```
README.md
README_INTERNAL.md
AGENTS.md
SESSION.md
LOG.md
BACKLOG.md
ROADMAP.md
docs/data_model.md
docs/cadence.md
docs/monitoring_workflow.md
docs/discovery_loops.md
docs/operator_mode.md
docs/taxonomy.md
docs/design/tracked_entities_design.md
docs/reviews/sjc_vps_codex_discovery_brief.md         ← Primary discovery artifact
docs/reviews/codex_roadmap_preflight.md
docs/reviews/codex_review_output.md
docs/editorial/ed001_review_queue_requirements.md
docs/editorial/batch_review_rules.md
docs/data_inventory/COVERAGE.md
docs/data_inventory/GAPS.md
registry/sources.yaml
registry/source_candidates.yaml
registry/communities.yaml
registry/interest_filters.yaml
registry/tracked_entities.yaml
schemas/source.schema.yaml
schemas/source_event.schema.yaml
schemas/intel_item.schema.yaml
schemas/tracked_entity.schema.yaml
scripts/extract_nbor.py
scripts/extract_bcc_agenda.py
scripts/build_review_queue.py
scripts/rebuild_dedupe_index.py
data/review_queue/summary.yaml
.opencode/agent_memory/sjc-intel-architect.memory.md
```

Run:
```
cd /Users/buddy/projects/sjc_intel
git log --oneline -10
git status --short
```

### ivy-control / VPS (Context)

Read these files:

```
/Users/buddy/projects/ivy-control/vps/README.md
/Users/buddy/projects/ivy-control/vps/vps-host.md
/Users/buddy/projects/ivy-control/vps/shared-conventions.md
/Users/buddy/projects/ivy-control/vps/VPS_MIGRATION_STATUS.md
/Users/buddy/projects/ivy-control/vps/logs/session/gpt1.md
/Users/buddy/projects/ivy-control/docs/project-context/ecosystem-cross-repo-review-2026-07-04.md
/Users/buddy/projects/ivy-control/repo-operating-standard.md
/Users/buddy/projects/ivy-control/github-readiness-checklist.md
```

Note: `ivy-control` has NOT been pushed to GitHub. Both repos are local-only.

---

### Full eventual VPS role

Classify every meaningful workflow from SJC Intel (NBOR extraction, utility check, county news, sheriff news, BCC agenda, CDD monitoring, FDOT, SJRWMD, development tracker, permit portal, St. Johns Citizen monitoring, backfills, tracked-entity discovery, source candidate review, dedupe index rebuild, review queue rebuild, review status updates, monthly closeout, health monitoring, LAST_RUN tracking) into exactly one category from shared-conventions §1 (1=VPS-ready now, 2=shadow/parity, 3=HITL gate, 4=hardening, 5=local long-term, 6=deferred, 7=unclear).

Consider more than ingestion: acquisition, normalization, parsing, deterministic enrichment, validation, regeneration, exports, notifications, static builds, branch/PR creation, health checks, backups, restore verification, retries, recovery, bounded LLM work.

### Database role naming

Use shared-conventions §3: `{project}_writer`, `{project}_reader`, `{project}_monitor`, `{project}_migrator`, `{project}_backup`. Example: `sjc_intel_writer`, `sjc_intel_monitor`.

### Migration layout

Use shared-conventions §4: `db/migrations/YYYYMMDD_NNN_description.sql` with `rollback/` and `validation/` directories.

## 4. Decisions You Must Make Explicitly

Before writing the roadmap, decide and document each of these:

1. **SilverLeaf-first vs county-wide scope** — Is Phase 1 SilverLeaf/Nocatee only, or full-county?
2. **Stakeholder-readable outputs** — What's the first human-readable output (community digest, entity dashboard, weekly brief)?
3. **Knowledgebase definition** — Is it the set of verified queue items, or a separate curated layer?
4. **Community/neighborhood schema expansion** — Enrich `registry/communities.yaml` first, or accept manual config churn?
5. **Browser/news-search architecture** — Defer to post-VPS, or design contracts now?
6. **Evidence hierarchy** — How to preserve official > news > lead in the database model?
7. **PostgreSQL isolation model** — Database-per-project per shared-conventions §2. Use database `sjc_intel`.
8. **File-to-database migration** — Which YAML data migrates to PG, what stays file-based, dual-write period?
9. **Ingestion contracts** — Common collector contract design for all VPS-schedulable workflows.
10. **Raw artifact storage** — Filesystem layout, naming, checksums, retention, compression.
11. **Backup/retention/restore** — Policies for PG, raw artifacts, config, logs.
12. **Deterministic health checks** — What metrics, output format, schedule.
13. **Shared dashboard metrics** — Which are public-safe, internal-only, or sensitive.
14. **Hermes permissions** — Read-only health inspector now, or defer to P6?
15. **GitHub readiness** — Blocking items to fix before push.
16. **Publishing deferral** — Confirm deferred; schema must support future eligibility + history.
17. **VPS deployment and rollback** — Exact cutover sequence and rollback procedure.

---

## 5. What the Roadmap Must Contain

### A. Roadmap Overview

```
- Target end state (one paragraph)
- Guiding principles (bullet list)
- Assumptions (what must be true)
- Explicitly deferred work (out of scope)
- Critical path diagram
```

### B. Phases

Each phase must contain ALL of:

| Field | Required |
|-------|----------|
| Purpose (1-2 sentences) | ✅ |
| Stakeholder value (what a resident gains) | ✅ |
| Dependencies (blocks or is blocked by) | ✅ |
| Exact likely files/directories affected | ✅ |
| Schema/model changes (if any) | ✅ |
| Worker-sized tasks (3-5 per phase) | ✅ |
| Required context files | ✅ |
| Validation commands (exact shell commands) | ✅ |
| Pass/fail criteria | ✅ |
| Rollback procedure | ✅ |
| HITL approval gate | ✅ |
| Git Steward commit boundary (exact paths to stage) | ✅ |
| GitHub push gate (where applicable) | ✅ |
| VPS deployment/cutover gate (where applicable) | ✅ |

### C. PostgreSQL Implementation Detail

Require:

- Recommended isolation model (schema vs database) with rationale
- Schema and migration layout: `db/migrations/` per shared-conventions §4
- Migration naming convention: `YYYYMMDD_NNN_description.sql` per shared-conventions §4
- Database roles: `sjc_intel_app` (read/write), `sjc_intel_readonly` (dashboard), `hermes_reader` (health only)
- Permissions: schema-level GRANTs, not table-level
- Full table inventory (at minimum):

| Table | Grain | PK | FKs | Important Timestamps | Append-Only or Mutable | Retention |
|-------|-------|----|-----|----------------------|------------------------|-----------|
| `sources` | One source | `source_id` | — | `created_at`, `updated_at` | Mutable | Permanent |
| `source_families` | One family | `family_id` | — | `created_at` | Mutable | Permanent |
| `topics` | One topic | `topic_id` | — | `created_at` | Mutable | Permanent |
| `beat_groups` | One beat | `beat_id` | — | `created_at` | Mutable | Permanent |
| `communities` | One community | `community_id` | — | `created_at`, `updated_at` | Mutable | Permanent |
| `tracked_entities` | One entity | `entity_id` | — | `created_at`, `last_checked_at` | Mutable | Permanent |
| `entity_aliases` | One alias | `(entity_id, alias)` | `entity_id` | — | Mutable | Permanent |
| `source_entity_links` | Link | `(source_id, entity_id)` | `source_id`, `entity_id` | `created_at` | Append | Permanent |
| `collection_runs` | One run | `run_id` (bigserial) | `source_id` | `started_at`, `completed_at` | Append | 90 days |
| `fetched_documents` | One fetch/meeting | `document_id` | `source_id`, `run_id` | `fetched_at`, `event_date` | Append | 90 days |
| `raw_artifact_metadata` | One artifact | `artifact_id` (bigserial) | `document_id` | `created_at` | Append | 90 days |
| `source_events` | One event | `event_id` | `source_id` | `event_date`, `discovered_at` | Mutable | Permanent |
| `intel_items` | One item | `item_id` | `source_id`, `event_id` | `discovered_at`, `created_at` | Mutable | Permanent |
| `item_entity_links` | Link | `(item_id, entity_id)` | `item_id`, `entity_id` | `created_at` | Append | Permanent |
| `item_topic_links` | Link | `(item_id, topic_id)` | `item_id`, `topic_id` | `created_at` | Append | Permanent |
| `deduplication_keys` | One fingerprint | `dedupe_key` | `item_id` | `created_at` | Append | Permanent |
| `provenance` | Provenance event | `provenance_id` | `item_id`, `event_id` | `created_at` | Append | Permanent |
| `extraction_results` | Extraction output | `extraction_id` | `document_id` | `created_at` | Append | 90 days |
| `enrichment_results` | Classification | `enrichment_id` | `item_id` | `created_at` | Append | 30 days |
| `review_status_history` | Status change | `review_id` | `item_id` | `changed_at` | Append | Permanent |
| `publishing_status_history` | Pub event | `publish_id` | `item_id` | `published_at` | Append | Permanent |
| `pipeline_errors` | Error record | `error_id` | `run_id`, `source_id` | `occurred_at` | Append | 90 days |
| `pipeline_health` | Run health | `run_id` | `run_id` | `checked_at` | Append | 30 days |
| `health_snapshots` | Periodic health | `snapshot_id` | — | `snapped_at` | Append | 30 days |
| `scheduler_executions` | Timer run | `execution_id` | `run_id` | `started_at` | Append | 90 days |
| `schema_versions` | Migration | `version_id` | — | `applied_at` | Append | Permanent |

- Indexes and uniqueness constraints for each table
- Provenance model (who discovered what, when, from which source)
- Review and publishing history (append-only, immutable)
- Schema versioning via `schema_versions` table
- Migration rollback policy (each migration must have a `DOWN` SQL file)
- File compatibility period (how long YAML and PG both exist)
- Project-level restore strategy (`pg_restore -n sjc_intel`)

### D. Ingestion Contracts

Define a common collector contract that produces, for every run:

```yaml
run:
  source_id: str
  run_id: uuid
  started_at: timestamp
  completed_at: timestamp
  status: success | partial | failed
  fetch:
    url: str
    http_status: int
    duration_ms: int
  artifact:
    path: str (relative to artifact_root)
    checksum_sha256: str
    size_bytes: int
  extraction:
    source_event_ids: [str]
    extracted_item_ids: [str]
    duplicate_count: int
    new_item_count: int
  errors:
    - message: str
      severity: warn | error | fatal
      context: str
  retry_count: int
  health:
    source_reachable: bool
    consecutive_failures: int
```

Idempotency behavior: re-running the same source_id+date must not create duplicate intel_items.
Exit codes: 0 = success, 1 = partial (some items extracted, some errors), 2 = fatal (no items).

### E. Workflow Classification Matrix

Classify EVERY workflow as one of:

- **VPS-ready** — has an extraction script, deterministic, no JS/form input
- **Harden before scheduling** — needs extraction script, error handling, or env support
- **Supervised/manual** — requires human judgment or Buddy approval
- **Prohibited from automation** — by policy (e.g., private sources, publishing)

Workflows to classify:

| Workflow | Current Status |
|----------|----------------|
| NBOR public notices | Has `scripts/extract_nbor.py` |
| BCC agenda (Clerk) | Has `scripts/extract_bcc_agenda.py` — broken links |
| County news (WordPress) | Manual HTTP GET |
| Utility department | Manual HTTP GET |
| Emergency management | Manual, seasonal |
| Sheriff news (WordPress) | Manual HTTP GET |
| CDD sources (3 active) | WordPress, some with RSS |
| School stack (BoardDocs) | Not built, Cloudflare/JS unknown |
| FDOT District Two / NFLRoads | Not started |
| SJRWMD watering restrictions | Not started |
| Development tracker (GIS) | JS map — needs browser automation |
| Permit portal (forms) | Form interaction — needs browser automation |
| St. Johns Citizen (media) | Tip/context only — manual |
| Backfill passes | Fully manual, Hermes prompts |
| Tracked-entity discovery | Manual search, Hermes prompts |
| Source candidate review | Architecture judgment — manual |
| Dedupe index rebuild | `rebuild_dedupe_index.py` — idempotent |
| Review queue rebuild | `build_review_queue.py` — idempotent |
| Monthly closeout | Synthesis, judgment — manual |

### F. Deployment Artifacts

Require exact likely paths:

```
deploy/
  env/
    env.example
    production.env          (gitignored)
  sql/
    001_create_schema_sjc_intel.sql
    002_create_sources.sql
    003_create_intel_items.sql
    004_create_review_status.sql
    005_create_health.sql
    ...                      (one file per migration)
  systemd/
    sjc-extract-nbor.service
    sjc-extract-nbor.timer
    sjc-daily-cycle.service
    sjc-health-check.service
    sjc-health-check.timer
    sjc-dashboard-export.service
    sjc-dashboard-export.timer
    sjc-backup-pg.service
    sjc-backup-pg.timer
    sjc-retention-cleanup.service
    sjc-retention-cleanup.timer
  health/
    health_check.sh
    check_sjc_health.py
    dashboard_export.py
  backup/
    pg_dump_sjc_intel.sh
    pg_restore_sjc_intel.sh
    artifact_cleanup.py
  restore/
    disaster_recovery.md
    restore_from_backup.md
scripts/
  collectors/
    collect_nbor.py
    collect_bcc_agenda.py
    collect_county_news.py
    collect_utility.py
    collect_sheriff.py
    collect_emergency.py
    collect_cdd.py
  health/
    check_source_health.py
  migrations/
    migrate_yaml_to_pg.py
migrations/
  (all numbered SQL migration files)
docs/
  runbooks/
    deploy.md
    rollback.md
    cutover.md
    incident_response.md
```

### G. Services/Timers

Propose likely systemd units for:
- Daily NBOR ingestion (`sjc-extract-nbor.service` + `sjc-extract-nbor.timer`)
- Weekly BCC ingestion (`sjc-extract-bcc.service` + `sjc-extract-bcc.timer`)
- Seasonal emergency ingestion (Jun-Nov, `sjc-extract-emergency.service`)
- Source health checks (`sjc-health-check.service` + `sjc-health-check.timer`)
- Review queue/health-refresh refresh (`sjc-dashboard-export.service`)
- Dedupe maintenance (`sjc-dedupe-rebuild.service`)
- Dashboard JSON export (`sjc-dashboard-export.service`)
- PostgreSQL backup (`sjc-backup-pg.service` + `sjc-backup-pg.timer`)
- Artifact retention cleanup (`sjc-retention-cleanup.service`)

Do NOT finalize schedules without checking `docs/cadence.md`. Note dependencies between services.

### H. Environment and Secrets

Define all likely environment variables:

```
SJC_DB_HOST=localhost                          # Safe config
SJC_DB_PORT=5432                               # Safe config
SJC_DB_NAME=ivy_control                        # Safe config (shared instance)
SJC_DB_SCHEMA=sjc_intel                        # Safe config
SJC_DB_USER=sjc_intel_app                      # Safe config
SJC_DB_PASSWORD=<generated>                    # SECRET — .env only
SJC_ARTIFACT_ROOT=/var/opt/sjc_intel/artifacts # Host-local
SJC_LOG_ROOT=/var/opt/sjc_intel/logs           # Host-local
SJC_HEALTH_OUTPUT=/var/www/health/status.json  # Host-local
SJC_DASHBOARD_EXPORT=/var/www/health/dashboard.json # Host-local
SJC_HERMES_DB_USER=hermes_reader               # Safe config
SJC_HERMES_DB_PASSWORD=<generated>             # SECRET — .env only
SJC_HTTP_USER_AGENT=SJC_Intel/1.0              # Safe config
SJC_HTTP_TIMEOUT_SECONDS=30                    # Safe config
SJC_HTTP_RETRY_MAX=3                           # Safe config
SJC_ALERT_WEBHOOK_URL=<optional>               # SECRET — optional
```

Distinguish: safe config (committed in `.env.example`), secrets (`.env` gitignored), host-local (per-environment).

### I. Raw Artifact Policy

Define:
- Filesystem layout: `{artifact_root}/{source_id}/{YYYY}/{MM}/{DD}/{event_id}.{ext}`
- Naming convention: `{event_id}_{sequence}.{ext}` with `sha256sum` recorded in PG
- Compression: gzip raw HTML, PDFs, and text extracts
- Retention: 7 days for raw HTML/PDF/screenshots, 30 days for extracts, logrotate for logs
- Backup: NOT backed up — re-fetchable from source. PG `raw_artifact_metadata` is the canonical pointer.
- Deletion policy: scheduled purge via `sjc-retention-cleanup.service`
- Database pointers: `raw_artifact_metadata` table with path, checksum, size, content_type
- Safe fixtures in Git: small representative files (<100KB) in `tests/fixtures/`
- Prohibited in Git: no mutable production data, no full-size snapshots, no raw HTML dumps

### J. Health/Dashboard Model

Define deterministic health JSON output (works without Hermes):

```json
{
  "project": "sjc_intel",
  "checked_at": "2026-07-04T12:00:00Z",
  "sources": [
    {
      "source_id": "sjc_nbor_public_notices",
      "last_successful_run": "2026-07-04T06:00:00Z",
      "expected_cadence_hours": 24,
      "freshness_lag_hours": 6,
      "reachable": true,
      "last_run_duration_seconds": 45,
      "document_count": 1,
      "extracted_item_count": 25,
      "duplicate_count": 0,
      "error_count": 0,
      "consecutive_failures": 0,
      "status": "healthy"
    }
  ],
  "pipeline": {
    "scheduler_active": true,
    "last_full_cycle": "2026-07-04T07:00:00Z",
    "backup_freshness_hours": 8,
    "schema_version": "001",
    "disk_usage_percent": 45,
    "total_items": 132,
    "pending_review": 43,
    "verified_items": 83
  }
}
```

Metrics classification:

| Metric | Public-safe | Internal-only | Potentially sensitive |
|--------|-------------|---------------|----------------------|
| Last successful run | ✅ | | |
| Expected cadence | ✅ | | |
| Freshness lag | ✅ | | |
| Source reachable | ✅ | | |
| Run duration | ✅ | | |
| Document count | ✅ | | |
| Extracted item count | ✅ | | |
| Duplicate rate | ✅ | | |
| Error count | ✅ | | |
| Consecutive failures | ✅ | | |
| Scheduler active | ✅ | | |
| Backup freshness | | ✅ | |
| Schema version | ✅ | | |
| Pending review count | | ✅ | |
| Verified item count | | ✅ | |
| Disk usage | | ✅ | |
| Specific item IDs | | | ✅ |
| Source-specific errors | | | ✅ |

### K. Hermes Role

Define:
- DB role: `hermes_reader` — `SELECT` only on `pipeline_health`, `health_snapshots`, `scheduler_executions`, `pipeline_errors`
- Actions: read health, compute freshness, summarize incidents, open branches, propose fixes, create PRs
- Prohibited: write to intel_items, source_events, review_status, registries; merge its own PRs; hold broad secrets; bypass human review; modify deploy/scripts/schemas without PR
- Audit trail: all Hermes actions logged in `pipeline_errors` or a `hermes_actions` table

### L. GitHub Readiness

Identify blockers:

| Blocking Issue | Fix |
|---------------|-----|
| `/Users/buddy/` hardcoded paths | Parameterize with `$HOME` or env vars |
| No `.env.example` | Create from §H |
| No `LICENSE` | Add MIT or note private |
| `.gitignore` incomplete | Add `logs/`, `runtime/`, `.env`, `*.key`, `__pycache__/`, `.venv/` |
| `data/` mutable YAML files | Gitignore runtime data; commit curated state only |
| No CI | Add YAML validation + schema lint workflow |
| No migration SQL directory | Create `migrations/` |
| No branch naming convention | Document in `AGENTS.md` |
| No GitHub remote | `gh repo create buddyowens/sjc_intel --private --source=. --push` |

Gate: Buddy must approve the first push.

### M. Publishing

Confirm: public publishing remains deferred (PUB-001/PUB-002 deferred in BACKLOG.md).

The schema must preserve:
- `review_status` on `intel_items` (pending_review → verified)
- `publishing_eligible` computed: `verified AND NOT human_review_required`
- `publishing_status_history` table for future publication events
- `publishing_approved_by`, `published_at`, `publishing_channel` fields
- Redaction/safety: `sensitivity` field, `human_review_required` flag, `reviewer_notes`

No publishing channel implementation in scope.

### N. Roadmap Quality Rules

The roadmap must:

1. ✅ Be practical for weaker (intern-level) Worker agents. Every task must specify exact input files, output files, commands, and validation.
2. ✅ Avoid vague tasks like "productionize" — decompose into concrete steps.
3. ✅ Avoid giant multi-week phases without decomposition. Max session size: one bounded Worker session.
4. ✅ Specify exact approval points between each phase.
5. ✅ Distinguish architecture decisions (requires high-reasoning GPT) from implementation tasks (Worker-suitable).
6. ✅ Identify critical-path tasks (must complete before dependent phases start).
7. ✅ Mark parallelizable work (GitHub prep ∥ schema design ∥ script writing).
8. ✅ Identify tasks that require Buddy or high-reasoning GPT.
9. ✅ Stop before enabling production timers or cutover without explicit approval.
10. ✅ Include a rollback section for every phase that modifies data or infrastructure.

---

## 6. Additional Required Deliverables Within ROADMAP.md

### 6.1 Decision Table

Include a concise table:

```
| Decision | Recommendation | Rationale | Approval Needed? |
|----------|---------------|-----------|------------------|
| PG isolation | Dedicated schema | ... | ✅ Buddy |
| Raw artifacts | Filesystem | ... | ❌ |
| ... | ... | ... | ... |
```

### 6.2 Phase Dependency Graph

Use ASCII or mermaid:

```
GitHub Readiness → Schema Design → Migration → Scripts → Health → VPS → Backup → Dashboard → Hermes → Cutover
    │                  │              │
    └── Parallel ──────┴── Parallel ──┘
```

### 6.3 Worker-Sized Session Table

| Session | Goal | Inputs | Files | Validation | HITL Gate | Commit |
|---------|------|--------|-------|------------|-----------|--------|

### 6.4 First Worker Task Prompt Outline

A concrete prompt outline for the very first Worker session after the roadmap is approved. This should be a small, safe, bounded task (e.g., GitHub prep: create `.env.example`, add `LICENSE`, harden `.gitignore`).

### 6.5 Unresolved Questions

List questions that must be answered before any implementation begins, e.g.:
- Is `sjc_intel` schema in `ivy_control` DB approved, or dedicated database?
- What is the raw artifact root path on the VPS?
- What is the migration period where YAML + PG both live?

### 6.6 Roadmap Completion Definition

Define when the roadmap itself is complete:
- All phases specified with Worker-sized tasks
- All approval gates identified
- All unresolved questions documented
- First Worker task prompt outline accepted
- Codex planning session can conclude; implementation can begin

When should a new Codex planning session be scheduled: after every 3-4 phases are complete, after any architectural decision reversal, or when a phase reveals unanticipated complexity that changes the dependency graph.

---

## 7. Output Format

Write `ROADMAP.md` at the SJC_Intel repo root. The file may be long (aim for 200-500 lines). Use markdown with tables, code blocks, and mermaid diagrams as needed. The file should be:

- Self-contained enough that a new Worker agent can read it and know what to do
- Specific enough that Buddy can approve/reject individual phases
- Structured enough that Codex or another GPT can review it for completeness
- Practical enough that a weaker Worker can execute phase tasks without architect intervention

Do NOT:
- Implement anything
- Edit scripts, schemas, registries, data, or deployment files
- Enable timers or cutover
- Commit the ROADMAP.md yourself — Buddy or Git Steward will commit it after review

If you have ambiguity questions, document them in the Unresolved Questions section rather than guessing. Do not ask the human during this session.
