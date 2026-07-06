# SJC_Intel Session — 2026-07-04 (Doc Consolidation)

## Task
Consolidate project docs, define Git policy, and formalize logging practice.

## Summary
Reduced root-level doc count from 11 to 7 by folding STATE.md, ROADMAP.md,
CHECKLIST.md content into README_INTERNAL.md and AGENTS.md. Made
README_INTERNAL.md the primary development entrypoint. Added git policy,
three-tier logging, and worker context-gathering requirement to AGENTS.md.
Archived two stale discovery docs (ST_JOHNS_COUNTY_INTELLIGENCE.md,
discovery_test.md) to docs/archive/. Created logs/conversations/ for
Buddy's GPT research thread storage.

## PostgreSQL Foundation Complete (2026-07-06)

All 9 schema migrations applied, validated, backed up, and restore-drilled PASS.
Pilot loader at `scripts/pilot_loader.py` — dry-run/plan/apply/rollback/parity, 11 tests.
No real data ingested. No VPS deployment.

See `docs/VPS_CONTINUITY.md` for continuity details.
See ivy-control `vps/worker-control/reports/STRONG_AGENTIC_EXECUTION_REPORT.md` for full execution evidence.

## VPS PostgreSQL Capacity Gate Failed (2026-07-06)

The current `ih-market-vps` was inspected for SJC Intel PostgreSQL 16 hosting and failed the capacity Gate. PostgreSQL was not installed on the VPS and no SJC database was provisioned there.

Key blockers: root filesystem 89% used with ~4.3 GB free, 2.0 GiB swap in use, active Chrome/collector/WGU/private-search workloads, 13 GB private chat archive, no passwordless sudo path for provisioning/firewall verification, and pending reboot.

Current authority: Mac PostgreSQL 16 remains the active verified foundation, fallback, and migration source. SJC is pre-pilot-ready locally, but the current VPS is not approved as PostgreSQL primary.

Evidence: `ivy-control/vps/worker-control/reports/VPS_POSTGRES_CAPACITY_GATE_20260706.md`.

## Changes Made

### Rewritten
- `README_INTERNAL.md` — now primary dev entrypoint (was 286 lines, now 183)
  - Removed long session narrative (moved to logs)
  - Added review pipeline status (115 dedupe, 132 queue, interest filters)
  - Added Current Phase, Core Docs, Open Loops, Logging Tiers sections
  - Kept architecture tables, durable decisions, agent cautions, memory export

- `AGENTS.md` — added:
  - Git policy (commit boundaries, staging rules, conventional prefixes)
  - Three-tier logging practice (agent/runs/conversations)
  - Worker context-gathering requirement
  - Session checklists (start, end, Hermes delegation)
  - Updated startup routine (README_INTERNAL.md replaces STATE.md)

### Deprecated (short stubs remain pointing to new homes)
- `STATE.md` — content folded into README_INTERNAL.md
- `ROADMAP.md` — phase table folded into README_INTERNAL.md
- `CHECKLIST.md` — checklists folded into AGENTS.md
- `README.md` — shortened to dev pointer to README_INTERNAL.md

### Archive
- `ST_JOHNS_COUNTY_INTELLIGENCE.md` → `docs/archive/`
- `discovery_test.md` → `docs/archive/`

### New
- `logs/conversations/README.md` — third logging tier definition
- `logs/runs/daily/2026-07-04_interest_filters_and_silverleaf.md` — prior session log

### Updated references
- `docs/cadence.md` — STATE.md references → README_INTERNAL.md
- `docs/operator_mode.md` — STATE.md/ROADMAP.md → README_INTERNAL.md

### Not modified (intentional)
- No extraction scripts touched
- No data artifacts modified (beyond existing dirty state)
- No source monitors added
- No source_event migration performed

## Validation
- All YAML files parse correctly
- No stale STATE.md/ROADMAP.md/CHECKLIST.md references remain in core docs
- Data artifacts untouched
- Git shows expected dirty files (doc changes only)

## Residual Stale References (archival docs only, not updated)
- `docs/hermes_task_contract.md` — references STATE.md/ROADMAP.md (historical Hermes spec)
- `docs/reviews/codex_review_output.md` — review artifact, not active
- `docs/repo_audit.md` — historical audit, not active
- `docs/source_promotion/first_wave_source_promotion_packet.md` — historical

---

# SJC_Intel Session — 2026-07-04 (Tracked Entities Design)

## Task
Design the tracked_entities workflow using the new data model.

## Summary
Inspected all context files and produced `docs/design/tracked_entities_design.md`.
The design resolves tracked_entity ↔ intel_item, interest_filter, community,
and source relationships. Defines schema, entity types, lifecycle statuses,
ID convention, and clear ENT-001 implementation boundaries. Does not create
the registry file yet — design only per constraints.

## Key Design Decisions
- Entity IDs are descriptive slugs (`ENT-RETAIL-PUBLIX-SILVERLEAF`), not
  date-based. Entities are durable across sessions.
- Interest filters and tracked entities are separate concerns: filters are
  lightweight keyword rules; entities are authoritative records.
- Future: build_review_queue.py should load both registries and auto-tag.
- ENT-001 scope: create registry + schema + seed ~8 entities. ENT-002..004
  deferred (auto-tagging, Hermes prompt, stakeholder workflow doc).

## Files Created
- `docs/design/tracked_entities_design.md` — full design, schema, types,
  lifecycle, ID convention, seed list, implementation boundaries

## Files Updated
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Not Modified
- No registry, scripts, data artifacts, or core docs changed.
- No commits.

---

# SJC_Intel Session — 2026-07-04 (ENT-001 Implementation)

## Task
Implement ENT-001 tracked entities registry and schema.

## Summary
Created `registry/tracked_entities.yaml` with 10 seed entities (8 from design
doc + 2 non-retail: SR 207 WRF, SilverLeaf community). Created
`schemas/tracked_entity.schema.yaml`. Updated `docs/data_model.md` to mark
tracked_entities as implemented. Updated `README_INTERNAL.md` pipeline table
and open loops. Marked ENT-001 done in BACKLOG.md.

## Files Created
- `registry/tracked_entities.yaml` — 11 entities seeded
- `schemas/tracked_entity.schema.yaml` — field-level spec

## Files Updated
- `docs/data_model.md` — tracked_entities marked implemented, ID convention
  updated, lifecycle status documented, placeholder section rewritten
- `README_INTERNAL.md` — added tracked entities row to Review Pipeline table,
  updated open loop #4
- `BACKLOG.md` — ENT-001: todo → done
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Entities Seeded
1. SilverLeaf Mega Publix (retail_development, completed)
2. Harris Teeter — SilverLeaf (retail_development, proposed)
3. SilverLeaf K-8 School (education_facility, under_construction)
4. Beach Valley Mini Golf (recreational_attraction, proposed)
5. CR 2209 Connector (road_project, completed)
6. Ascension St. Vincent's — Nocatee (healthcare_facility, proposed)
7. Fairfield Inn & Suites — CR 210 (hospitality, proposed)
8. Nocatee Crosswater Retail Center (mixed_use_development, under_construction)
9. SR 207 Water Reclamation Facility Phase 2 (infrastructure_project, approved)
10. SilverLeaf Master-Planned Community (community, tracked)

## Not Modified
- No scripts, data artifacts, or registries (other than tracked_entities) changed.
- No commits.

---

# SJC_Intel Session — 2026-07-04 (ENT-002 Implementation)

## Task
Implement ENT-002 tracked-entity matching and queue integration.

## Summary
Updated intel_item.schema.yaml with optional `tracked_entity_ids` field.
Updated scripts/build_review_queue.py to load registry/tracked_entities.yaml
and match entity labels/aliases against intel item text fields (title,
summary, raw_excerpt). Matching is conservative exact-phrase substring,
prioritizing precision over recall. Queue entries gain `matched_entities`,
`entity_match_basis`, and `tracked_entity_ids` fields. Summary gains
`entity_matches` and `total_entity_matches`.

## Files Changed
- `schemas/intel_item.schema.yaml` — added tracked_entity_ids field
- `scripts/build_review_queue.py` — added entity loading, matching, and
  queue field integration
- `data/review_queue/queue.yaml` — rebuilt with entity matches
- `data/review_queue/summary.yaml` — rebuilt with entity match counts
- `docs/data_model.md` — marked ENT-002 as implemented, updated relationship
  map and entity linkage section
- `README_INTERNAL.md` — updated open loop #4
- `BACKLOG.md` — ENT-002: todo → done
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Match Results
- 11 entity matches across 8 unique items
- Matched entities: ENT-COMM-SILVERLEAF(5), ENT-INFRA-SR-207-WRF(2),
  ENT-ROAD-CR-2209-CONNECTOR(2), ENT-EDU-SILVERLEAF-K8(1),
  ENT-REC-BEACH-VALLEY-MINI-GOLF(1)
- False positives: 0
- False negatives: expected (Publix, Harris Teeter, Ascension, Fairfield Inn,
  Nocatee Crosswater) — acceptable due to conservative exact-phrase matching
- Review states preserved: 114 unchanged
- Idempotent: confirmed across 3 runs

## Matching Algorithm
1. Explicit `tracked_entity_ids` on item win (future use)
2. Entity label + aliases matched as exact case-insensitive substrings
   against title, summary, raw_excerpt
3. Match basis recorded (label/alias, which phrase matched)

## Scope Notes
- Hermes entity-search prompt deferred (not in ENT-002 scope as revised)
- Interest filters NOT modified or auto-generated
- No new entities added
- No lifecycle statuses changed

---

# SJC_Intel Session — 2026-07-04 (Codex Roadmap Preflight)

## Task
Prepare a Codex roadmap-planning preflight packet before Buddy's next
high-reasoning planning session.

## Summary
Inspected all context files, analyzed stakeholder value, data coverage,
search/discovery capabilities, neighborhood expansion model, knowledgebase
workflow, and documentation quality. Produced `docs/reviews/codex_roadmap_preflight.md`
with 17 sections including a full recommended Codex prompt.

## Key Findings
- System has strong infrastructure but no resident-facing output
- 132 items in queue but no human-readable digest or report
- Coverage heavily concentrated on SilverLeaf/Jun 2026
- 20+ communities in registry with zero items
- Community schema lacks aliases, search keywords, related sources
- Knowledgebase is undefined (verified queue items vs curated layer?)
- No search/browser automation execution exists (contracts drafted but untested)
- Next roadmap faces fundamental decision: deepen, expand, or build automation

## Files Created
- `docs/reviews/codex_roadmap_preflight.md` — preflight packet with analysis,
  gaps, decisions Codex must make, and recommended Codex prompt

## Files Updated
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Not Modified
- No scripts, schemas, registries, or data changed.
- No commits.

---

# SJC_Intel Session — 2026-07-04 (Cross-Repo VPS Discovery Brief)

## Task
Cross-repo discovery pass for SJC_Intel and ivy-control VPS migration. Produce a compact implementation-planning brief for Codex to write/overwrite ROADMAP.md.

## Summary
Inspected all SJC_Intel context files (README.md, README_INTERNAL.md, AGENTS.md, BACKLOG.md, ROADMAP.md, all docs/, all registries, all schemas, scripts, git history) and all ivy-control/VPS planning files (vps/README.md, vps-host.md, session log, ecosystem review, repo-operating-standard, github-readiness-checklist).

Produced `docs/reviews/sjc_vps_codex_discovery_brief.md` — a 22-section brief covering: architecture, ingestion mode classification, automation constraints, data inventory, PG isolation recommendation, table inventory (28 tables), raw artifact policy, backup/restore, dashboard metrics, Hermes role, GitHub blockers, required VPS services/timers, environment model, publishing deferral, critical path, decision table, unresolved decisions, and Codex prompt recommendations.

## Key Findings
- SJC_Intel is VPS-ready after: GitHub cleanup, PostgreSQL schema design, data migration, and ingestion script hardening
- Recommended isolation: dedicated `sjc_intel` schema in shared `ivy_control` DB
- 7 workflows are immediately VPS-schedulable; ~10 need script hardening; ~4 remain manual
- 28 PostgreSQL tables proposed with grain, PK, FK, retention, mutability
- Hermes role: read-only health inspector, never modify production, never bypass human review
- Publishing remains deferred; schema must preserve eligibility fields
- Critical path: GitHub → Schema → Migration → Scripts → Health → VPS → Backup → Dashboard → Hermes → Cutover

## Files Created
- `docs/reviews/sjc_vps_codex_discovery_brief.md` — 22-section discovery brief (~500 lines)

## Files Updated
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Not Modified
- No scripts, schemas, registries, data, or deployment files changed.
- No commits.

---

# SJC_Intel Session — 2026-07-04 (Git Steward + Codex Roadmap Prompt)

## Task
- Commit the VPS-aligned discovery brief.
- Draft the self-contained Codex prompt for ROADMAP.md planning.

## Summary
Inspected git status, confirmed only LOG.md + SESSION.md modified + `docs/reviews/sjc_vps_codex_discovery_brief.md` untracked. No scripts, schemas, registries, data, or deployment files changed. No secrets present. Staged and committed 3 files with message `docs: add VPS-aligned Codex roadmap discovery brief` (commit `ab0faed`).

Then read all required SJC_Intel and ivy-control context files and produced `docs/reviews/sjc_vps_codex_roadmap_prompt.md` — a self-contained prompt Buddy can paste into Codex. The prompt requires Codex to produce ROADMAP.md with: roadmap overview, detailed phases, PostgreSQL implementation detail, ingestion contracts, workflow classification matrix, deployment artifacts, services/timers, environment/secrets model, raw artifact policy, health/dashboard model, Hermes role, GitHub readiness, publishing deferral, roadmap quality rules, decision table, phase dependency graph, Worker-sized session table, first Worker task outline, unresolved questions, and completion definition.

## Files Created
- `docs/reviews/sjc_vps_codex_roadmap_prompt.md` — Codex planning prompt for ROADMAP.md generation

## Files Updated
- `SESSION.md` — appended this session record
- `LOG.md` — appended this session record

## Commit
- `ab0faed` — `docs: add VPS-aligned Codex roadmap discovery brief`
- 3 files: `docs/reviews/sjc_vps_codex_discovery_brief.md`, `LOG.md`, `SESSION.md`

## Not Modified
- No scripts, schemas, registries, data, or deployment files changed.
- ROADMAP.md not overwritten.
- Codex not run.

## Current Dirty State
- `docs/reviews/codex_roadmap_preflight.md` untracked (from prior session, not part of this work)
- `docs/reviews/sjc_vps_codex_roadmap_prompt.md` untracked (created this session; not committed per constraint)

---

# SJC_Intel Session — 2026-07-05 (SJC-010 PRE_GITHUB Remediation)

## Task
SJC-010: PRE_GITHUB minimum remediation for sjc_intel. Add/improve `.gitignore`, `.env.example`, validation command, pytest test harness, and documentation. LICENSE deferred (portfolio decision not finalized).

## Assignment Authority
- `vps/worker-control/reports/first-wave/SHARED-009.md` — batch plan defining SJC-010 scope
- `vps/worker-control/reports/first-wave/SHARED-010.md` — durable closeout standard (capability-based, not filename-based)
- `vps/PORTFOLIO_REPO_STANDARD.md` — PRE_GITHUB_MINIMUM criteria
- `vps/audits/maturity/sjc-intel.md` — maturity audit: testing CRITICAL, GitHub blockers
- SJC-010 assignment instructions (session prompt)

## Files Changed

### Modified
- `.gitignore` — added `.venv/`, `venv/`, `*.key`, `*.pem`
- `README.md` — added Setup and Validation sections
- `SESSION.md` — appended this session record

### Created
- `.env.example` — documented current (no env vars) and future env vars
- `pytest.ini` — pytest configuration
- `scripts/validate.py` — deterministic offline validation script
- `tests/conftest.py` — pytest fixtures (fixture_dir, schema_dir, nbor_html, bcc_agenda_text, etc.)
- `tests/test_schemas.py` — YAML schema validation tests (4 schemas)
- `tests/test_bcc_parser.py` — BCC agenda parser tests (12 tests)
- `tests/test_nbor_parser.py` — NBOR parser tests (7 tests)
- `tests/test_scripts_compile.py` — all script compilation tests (1 test across 8 scripts)

### Not Modified (intentional)
- LICENSE not added — portfolio license choice not finalized per SHARED-009 finding
- No extraction scripts touched
- No data artifacts modified
- No source monitors added
- No VPS, PostgreSQL, scheduler, service, or remote access

## Validation Results
- `python3 scripts/validate.py` — ALL PASSED (schema parse, script compile, fixture presence)
- `python3 -m pytest tests/ -v` — 25/25 passed
- `rg -n '/Users/buddy/'` — hardcoded paths exist in `README_INTERNAL.md:10` (informational metadata field) and `docs/reviews/` (planning artifacts, not functional source). No functional hardcoded paths in scripts, configs, or schemas.
- `git status --short` — shows only expected modified/untracked files
- No secrets in any diff

## Current Git State
```
 M .gitignore
?? .env.example
?? pytest.ini
?? scripts/validate.py
?? tests/conftest.py
?? tests/test_bcc_parser.py
?? tests/test_nbor_parser.py
?? tests/test_schemas.py
?? tests/test_scripts_compile.py
```

## Stop/Escalation Conditions
- **LICENSE deferred**: Portfolio license choice not finalized per SHARED-009. Requires Buddy decision before adding MIT or other license file.
- No secrets or private data discovered.
- No VPS/remote access required or performed.
- No tests require live services, production data, or network.

## Next Steps
1. Buddy to decide portfolio LICENSE default for publishable repos
2. SJC-010 report at `vps/worker-control/reports/first-wave/SJC-010.md`
3. Future VPS work depends on license decision and SJC-010 acceptance

---

# SJC_Intel Session — 2026-07-05 (SJC-006 Adapter and Shadow-Parity Package)

## Task
Implement storage adapter interface, file/PG backends, shadow-parity comparison, and comprehensive tests. Part of Batch 1 VPS migration.

## Summary
Built the adapter boundary layer specified in Codex Session 1 §10 (SJC migration and parity plan). File adapter is the DEFAULT and AUTHORITATIVE backend — reads/writes existing YAML files in `data/intel_items/`, `registry/`, `data/source_events/`, `data/review_queue/`. PG adapter implements the same interface but is disabled by default (`SJC_INTEL_PG_ADAPTER_ENABLED=false`), every method guards with `if not self._enabled: raise RuntimeError(...)`. Parity report compares file vs PG and produces deterministic JSON. All 93 tests pass (34 new + 59 existing).

## Architecture Decisions
- **Generic entity_type routing**: `list_items(filter)` supports `entity_type` filter to route to sources, tracked_entities, queue_entries, source_events, or default intel items
- **Date-prefix lookup**: `read_item` extracts date from item_id (`SJC-{prefix}-{YYYYMMDD}-{NNNN}`) for efficient directory targeting
- **Upsert semantics**: `write_item` uses item_id as stable key — updates existing or appends new item in target date directory
- **StorageFacade primary/fallback**: when PG is primary and fails (or is disabled), automatically falls back to file adapter with warning logging
- **No psycopg2 dependency**: PG adapter raises NotImplementedError for actual DB methods — concrete implementation deferred to SJC-004

## Files Created
- `scripts/adapter_base.py`
- `scripts/file_adapter.py`
- `scripts/pg_adapter.py`
- `scripts/storage_adapter.py`
- `scripts/parity_report.py`
- `tests/test_adapter.py` (22 tests)
- `tests/test_parity.py` (10 tests)
- `tests/fixtures/test_intel_items.yaml`
- `tests/fixtures/test_sources.yaml`
- `tests/fixtures/test_tracked_entities.yaml`

## Files Modified
- `.env.example` — added adapter PG configuration variables

## Validation
- `python3 -m pytest tests/ -v` — 93/93 passed (34 new + 59 existing)
- All adapter tests pass: FileAdapter reads/writes/idempotency, PgAdapter disabled raises, PgAdapter enabled falls back, StorageFacade primary/fallback
- Parity report produces valid JSON, detects disabled PG, compares counts/fields/dedupe keys
- No data artifacts modified
- No live DB connection or production ingestion
- File remains authoritative backend

## Gates Preserved
- File is primary: no change to production data authority
- PG disabled by default: explicit env var required
- No production ingestion, scraping, or network calls
- YAML fallback intact: PG failure falls back to file adapter
- All 59 existing tests pass

## Report
- `ivy-control/vps/worker-control/reports/implementation-batch-1/SJC-006.md`

---

# SJC_Intel Session — 2026-07-06 (Pilot Readiness Dry-Run)

## Summary
SJC Intel was evaluated for a bounded real-data PostgreSQL pilot. No live ingest was executed.

## Decision
Pilot remains blocked until a real PostgreSQL adapter or loader is implemented. Current `scripts/pg_adapter.py` is intentionally disabled by default and its real query/upsert/connection methods raise `NotImplementedError`.

## New Artifact
- `scripts/pilot_readiness_report.py` — non-mutating dry-run report for deterministic pilot subset selection, required-field checks, duplicate `item_id` checks, duplicate dedupe-key checks, rollback model, and delete-and-reimport model.

## Current Candidate
- Command: `python3 scripts/pilot_readiness_report.py --eligible-only --json`
- Source: `sjc_nbor_public_notices`
- Count: 10
- Digest: `6c0008d2855daf6c07fc4c0f2dda5478856cae775927bcc54cdda790571254b4`
- Status: `BLOCKED` because PG adapter is not live.

## Validation
- `python3 -m pytest tests/test_adapter.py tests/test_parity.py` — 34/34 passed.

## Next Action
Implement a real writer-safe PostgreSQL loader/adapter with dry-run/plan/apply, reject reporting, rollback by selected `item_id`, delete-and-reimport proof, and parity before any Gate-approved load.
