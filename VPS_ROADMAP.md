# SJC Intel VPS Roadmap

**Date:** 2026-07-04  
**Status:** Planning artifact only. No implementation authorized.  
**Scope:** `/Users/buddy/projects/sjc_intel`, shared VPS/PostgreSQL conventions, future `sjc_intel` PostgreSQL database, health output, backups, systemd timers, and GitHub readiness.

## Architecture Assessment

Verified facts:
- SJC Intel is currently local, file-based, and supervised. Actual files include YAML registries, YAML/Markdown data outputs, extraction scripts for NBOR and BCC agenda, review-queue scripts, source registries, schemas, and monitoring/operator docs.
- The prompt correctly points Codex to the shared VPS conventions and requires full workflow classification, but it still contains old examples such as `sjc_intel_app`, `sjc_intel_readonly`, `hermes_reader`, `sjc-health-check.service`, and schema-in-`ivy_control`.
- The discovery brief's schema-per-project recommendation is superseded by the accepted shared convention: one PostgreSQL instance, database-per-project.

Resolved decisions:

| Decision | Resolution | Rationale | Gate |
|---|---|---|---|
| Roadmap artifact | `VPS_ROADMAP.md` companion file | User naming override; preserves product docs | None |
| Database | `sjc_intel` | Shared convention; simpler backup/restore isolation | Database Authority Gate |
| Roles | `sjc_intel_writer`, `sjc_intel_reader`, `sjc_intel_monitor`, `sjc_intel_migrator`, `sjc_intel_backup` | Shared convention replaces old prompt examples | Database Authority Gate |
| Service slug | `sjc-intel-*` | Hyphenated service slug, snake_case DB/env slug | Scheduler Gate |
| Health storage | Project-private health tables plus sanitized JSON export; optional future aggregate copy in ivy-control | Keeps Hermes/dashboard independent and avoids premature shared DB coupling | Ecosystem ratification |
| Raw artifacts | Filesystem with checksums and PG pointers, not raw blobs in PG | Re-fetchable source evidence, large binary/text artifacts | Backup/Restore Gate before cleanup |
| Publication | Deferred/manual | SJC Intel contains resident-interest/editorial judgment | Publication Gate |
| Hermes | Read-only via `sjc_intel_monitor` | Hermes is observer, not runtime dependency | Hermes Read-Only Gate |

Recommended default where evidence remains incomplete:

| Uncertainty | Default | Alternatives | Evidence still needed | Latest decision point |
|---|---|---|---|---|
| VPS artifact root | `/home/scraper/data/sjc_intel/artifacts` | `/var/opt/sjc_intel/artifacts` | VPS filesystem capacity and service user policy | Before deploy wrapper |
| Backup retention | 7 daily, 4 weekly local VPS dumps; 14 daily during cutover on Mac | Longer retention if disk permits | Capacity check and restore drill | Before PostgreSQL Cutover Gate |
| Browser/form sources | Defer to hardening phase | Playwright/Camoufox proof | Source-by-source probe | Before adding those sources to timers |

## Target End State

SJC Intel runs deterministic source checks on the VPS, stores structured source events, intel items, scheduler executions, health snapshots, and artifact metadata in `sjc_intel`, and exports sanitized health JSON for ivy-control. Manual review, source promotion, monthly closeout, publication, deep research, and resident-interest judgment remain human-gated.

## Workflow Classification

| Workflow | Category | Notes |
|---|---:|---|
| NBOR daily extraction | 2 VPS-ready after shadow/parity | Script exists; needs wrapper, idempotency, health output |
| Utility department check | 4 hardening | Existing data and fixtures; needs durable extraction wrapper |
| County news | 4 hardening | WordPress/news extraction script needed |
| Sheriff news | 4 hardening | Same as county news |
| Emergency management | 4 hardening | Add seasonal activation logic |
| BCC agenda | 4 hardening | Script exists; PDF-link error handling required |
| CDD monitoring | 4 hardening | Needs source-specific extractor |
| Nocatee/community sources | 4 hardening | Needs extractor and source contract |
| FDOT/SJRWMD/roads | 4 hardening | Needs extractor and cadence design |
| Development tracker/permit portal | 6 deferred | Browser/form/API discovery required |
| Dedupe index rebuild | 2 shadow/parity | Deterministic YAML scan |
| Review queue rebuild | 3 HITL gate design | State-changing review queue must be gated |
| Review status updates | 5 local/manual long term | Editorial state |
| Tracked entity discovery | 5 local/manual long term | Human judgment |
| Backfills | 5 local/manual long term | Large, contextual, review-heavy |
| Monthly closeout | 5 local/manual long term | Editorial summary |
| Health checks/LAST_RUN tracking | 1 VPS-ready now after script | Deterministic once codified |
| Backup/restore verification | 4 hardening | Needs scripts and restore drill artifact |
| Branch/PR creation | 3 HITL gate design | Requires GitHub Push Gate and PR model |

## PostgreSQL Design

Use `db/migrations/YYYYMMDD_NNN_description.sql`, rollback files under `db/migrations/rollback/`, validation queries under `db/migrations/validation/`, and a schema-level migration table.

Design-level tables:
- `sources`, `source_events`, `intel_items`, `tracked_entities`, `item_entity_links`
- `raw_artifact_metadata` with filesystem path, size, content type, checksum, retention class
- `ingestion_runs`, `scheduler_executions`, `pipeline_errors`
- `review_queue_items`, read/write gated until review semantics are settled
- `pipeline_health`, `health_snapshots`

No migration may contain credentials, production dumps, mutable data, or environment-specific absolute secrets.

## Health and Backup Contract

Private health records live in `sjc_intel` and include run status, source freshness, error counts, backup age, disk usage, and schema version. Sanitized JSON omits raw paths, source-specific sensitive leads, resident-interest classifications, and review details.

Restore evidence must be a Markdown restore-drill record with: dump filename, dump checksum, restore target, row counts, validation query results, start/end timestamps, operator, and rollback notes.

## Worker Assignments

| ID | Class | Title | Objective | Rationale | Prerequisites | Working directory | Allowed files/systems | Explicit exclusions | Expected changes/artifacts | Commands or inspections expected | Validation/tests | Completion criteria | Rollback/recovery | Gates | Required worker report | Stop-and-escalate | Unlocks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SJC-VPS-001 | inspection or documentation only | Current-state verification | Verify prompt claims against repo files and produce a gap note | Avoid building on stale discovery | Roadmap accepted | `/Users/buddy/projects/sjc_intel` | Docs, registries, scripts, tests; read-only | No source edits, no git writes, no network mutation | `docs/reviews/vps_current_state_gap_note.md` if authorized later | `rg --files`, inspect listed scripts/docs, optional `python -m py_compile` read-only target list | No code tests required; command outputs summarized | Verified/contradicted list complete | Delete the note if wrong before commit | None | Files read, contradictions, no mutations | Missing required files or sensitive data needed | SJC-VPS-002 |
| SJC-VPS-002 | local code change with no runtime mutation | GitHub readiness docs | Add or update safe repo hygiene artifacts for future GitHub push | GitHub Push Gate blocks PR automation | SJC-VPS-001 accepted | same | `.gitignore`, `.env.example`, README pointers, CI draft docs | No secrets, no production data, no push | Safe hygiene/docs patch | `rg` for local paths; inspect ignored paths | `git status --short`; no secret output | Buddy can review first GitHub-readiness patch | Revert patch by explicit paths before commit | GitHub Push Gate before remote push | Paths changed, secret-scan summary, risks | Secret exposure or unclear generated data policy | SJC-VPS-003 |
| SJC-VPS-003 | database preparation | Schema design package | Author migration skeleton and schema README for empty DB | All later data work depends on stable schema | SJC-VPS-001, SJC-VPS-002 | same | `db/`, docs only | No live DB connection, no production data | Migration SQL, rollback, validation files, `db/README.md` | Inspect YAML schemas and scripts | SQL lint if available; validation queries reviewed | Migrations are idempotent for empty `sjc_intel` | Drop empty DB only if applied in dev; otherwise revert files | Database Authority Gate before apply | Schema files, assumptions, unresolved fields | Need live data sample not in repo | SJC-VPS-004 |
| SJC-VPS-004 | local code change with no runtime mutation | Collector contract wrappers | Add planned wrapper interfaces for deterministic extractions | Normalizes script output before VPS timers | SJC-VPS-003 | same | `scripts/`, `tests/fixtures`, docs | No scheduler, no DB write, no network fetch beyond existing tests | Wrapper scripts or interface docs | `python -m py_compile`, targeted fixture tests | Existing fixture-based tests pass | Wrappers produce deterministic manifests locally | Revert wrapper files | None | Commands run, fixture counts, manifest sample | Live source required to proceed | SJC-VPS-005 |
| SJC-VPS-005 | shadow or parity validation | Local parity rehearsal | Compare wrapper output to existing YAML outputs without authority change | Proves data contract before DB writes | SJC-VPS-004 | same | Local generated scratch under ignored runtime/logs | No production DB, no scheduler | Parity report artifact | Run local wrapper against fixtures or existing files | Row/item counts, checksum comparison | Parity report shows known diffs only | Remove scratch artifacts | None | Counts, diffs, limitations | Unexpected semantic drift | SJC-VPS-006 |
| SJC-VPS-006 | infrastructure preparation | Service/timer definitions | Draft systemd units and env templates for later VPS deployment | Enables review without installing | SJC-VPS-004 | same | `deploy/` or `vps/` service templates, docs | Do not copy to VPS or enable timers | Service/timer templates for `sjc-intel-*` | Inspect shared conventions; no `systemctl` | Static review; shellcheck if shell wrappers exist | Units are reviewable and disabled by default | Delete templates | Scheduler Gate before install | Unit names, env vars, schedule | Service would need secrets or live path unknown | SJC-VPS-007 |
| SJC-VPS-007 | infrastructure preparation | Backup and restore plan | Create backup scripts/templates and restore-drill procedure | Required before DB authority | SJC-VPS-003 | same | `backup/`, `docs/ops/`, templates | No live `pg_dump`, no production data transfer | Restore drill template and backup wrapper draft | Static inspect | Shellcheck if present | Restore evidence format complete | Revert docs/templates | Backup/Restore Gate before live drill | Retention, paths, restore test plan | Capacity unknown blocks retention | SJC-VPS-008 |
| SJC-VPS-008 | scheduler or service change | VPS shadow deployment | Install and run disabled/manual VPS shadow services | Prove deterministic VPS execution | SJC-VPS-006, SJC-VPS-007 | VPS clone path later | VPS user service files, env, logs | No timer enable without Gate, no production authority | Manual service run evidence | `systemctl --user status`, journal excerpts, health JSON | One manual run exit 0 | Shadow output reviewed; no authority transfer | Disable/remove units by explicit names | Scheduler Gate | Service status, logs, artifacts | Any service writes unexpected locations | SJC-VPS-009 |
| SJC-VPS-009 | production cutover | Enable approved timers | Make VPS primary for approved deterministic checks only | Completes first SJC automation lane | SJC-VPS-008 accepted | VPS clone path later | Approved `sjc-intel-*` timers | Manual/HITL workflows, publication | Enabled timers and health records | `systemctl --user enable --now`, status checks | 7-day healthy window | Timers enabled, health green | Disable timers; resume local manual run | Scheduler Gate, PostgreSQL Cutover Gate | Timer state, run history, health | Missed runs or data divergence | SJC-VPS-010 |
| SJC-VPS-010 | production cutover | Dashboard and Hermes read-only | Expose sanitized health to ivy-control and Hermes monitor role | Makes SJC observable without write access | SJC-VPS-009 stable | repo + ivy-control later | Health JSON/export docs, monitor grants | No Hermes writes, no PR automation without Gate | Health lane integrated | Check JSON schema, dashboard render | Dashboard shows sanitized SJC lane | Remove lane config | Hermes Read-Only Gate, Publication Gate for public view | Fields exposed, redaction decisions | Sensitive field exposure | Ecosystem implementation |

## First Worker Guidance

Start with `SJC-VPS-001`. The first worker must not modify runtime state. It should read the roadmap, prompt, discovery brief, shared conventions, and actual repo files; then report verified facts, contradictions, and whether `SJC-VPS-002` is safe to dispatch.

## Implementation Stop Conditions

Stop before implementation if a worker needs live VPS inspection, secrets, production database access, scheduler changes, destructive cleanup, GitHub push, publication, or unreviewed raw sensitive data. These require explicit Buddy Gate approval.
