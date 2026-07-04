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
