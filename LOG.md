# SJC_Intel Session Log

## 2026-07-04 (Doc Consolidation) — Reduce doc sprawl, add git/logging policy

**Task:** Consolidate project docs, define Git policy, formalize logging practice.

**Work done:**
- Rewrote README_INTERNAL.md as primary dev entrypoint (183 lines, was 286)
- Rewrote AGENTS.md with git policy, 3-tier logging, session checklists
- Deprecated STATE.md, ROADMAP.md, CHECKLIST.md (short stubs remain)
- Shortened README.md to dev pointer
- Archived ST_JOHNS_COUNTY_INTELLIGENCE.md and discovery_test.md to docs/archive/
- Created logs/conversations/README.md for third logging tier
- Updated stale references in docs/cadence.md and docs/operator_mode.md

**Validation:** All YAML valid. No data artifacts modified. No stale refs in core docs.

## 2026-07-04 (Tracked Entities Design) — Design ENT workflow

**Task:** Design tracked_entities workflow.

**Work done:**
- Inspected all context files (data_model, taxonomy, cadence, registry, etc.)
- Created `docs/design/tracked_entities_design.md` with full schema, entity
  types, lifecycle statuses, ID convention, seed list, implementation boundaries
- Resolved entity ↔ intel_item, interest_filter, community, source relationships
- Defined ENT-001 scope (registry + schema + seed) vs deferred (ENT-002..004)
- Appended SESSION.md and LOG.md

**Design-only session.** No files modified outside docs/design/ and session logs.

## 2026-07-04 (ENT-001 Implementation) — Create tracked entities registry

**Task:** Implement ENT-001 tracked entities registry.

**Work done:**
- Created `registry/tracked_entities.yaml` with 10 seed entities
- Created `schemas/tracked_entity.schema.yaml`
- Updated `docs/data_model.md` (marked tracked_entities as implemented)
- Updated `README_INTERNAL.md` (pipeline table, open loops)
- Marked ENT-001 done in BACKLOG.md

**Validation:** All YAML valid. Communities cross-referenced. No scripts or data changed.

## 2026-07-04 (ENT-002 Implementation) — Tracked entity matching and queue integration

**Task:** Integrate tracked entities into intel_item schema and review queue builder.

**Work done:**
- Updated `schemas/intel_item.schema.yaml` with optional `tracked_entity_ids`
- Updated `scripts/build_review_queue.py` with entity loading, matching, and queue fields
- Rebuilt review queue: 11 entity matches across 8 items, 0 false positives
- Updated `docs/data_model.md`, `README_INTERNAL.md`, `BACKLOG.md`
- Marked ENT-002 done

**Matching:** Exact label/alias substring match. Precision over recall.
**Validation:** 114 review states preserved. Idempotent. 0 source_events leaked.

## 2026-07-04 (Codex Roadmap Preflight) — Prep next planning session

**Task:** Prepare Codex roadmap-planning preflight packet.

**Work done:**
- Read all context files — architecture, data, registries, docs, logs
- Analyzed stakeholder value, data coverage, search/discovery, neighborhood
  model, knowledgebase workflow, documentation quality
- Created `docs/reviews/codex_roadmap_preflight.md` with 17 sections including
  full recommended Codex prompt
- Updated SESSION.md and LOG.md

**Key finding:** System is solid infrastructure but produces no resident-
facing output. Next roadmap must decide: deepen, expand, or automate.
**Design-only session.** No scripts, schemas, registries, or data changed.

## 2026-07-04 (Cross-Repo VPS Discovery Brief) — VPS migration planning

**Task:** Cross-repo discovery pass for SJC_Intel and ivy-control VPS migration.

**Work done:**
- Inspected all SJC_Intel context (docs, registries, schemas, scripts, git)
- Inspected all ivy-control/vps planning files (vps/README, vps-host.md, session log, ecosystem review, standards)
- Produced `docs/reviews/sjc_vps_codex_discovery_brief.md` — 22 sections, 28 PG tables, 7 workflow classifications, decision table, critical path, unresolved decisions, Codex prompt recommendations

**Key findings:**
- Recommended isolation: dedicated `sjc_intel` schema in shared `ivy_control` DB
- 7 VPS-schedulable workflows; ~10 need hardening; 4 remain manual
- 28 PostgreSQL tables proposed with retention/mutability
- Hermes role: read-only health inspector only
- Publishing remains deferred; schema preserves eligibility fields
- GitHub blockers: local paths, missing env example, no CI, missing license
- Critical path: GitHub → Schema → Migration → Scripts → Health → VPS → Backup → Dashboard → Hermes → Cutover

**Design-only session.** No scripts, schemas, registries, data, or deployment files changed.

## 2026-07-04 (Git Steward + Codex Roadmap Prompt) — Commit brief, draft Codex prompt

**Task:** Commit VPS-aligned discovery brief. Draft self-contained Codex prompt for ROADMAP.md planning.

**Work done:**
- Inspected git status, diffs — confirmed only LOG.md + SESSION.md modified, no scripts/schemas/registries/data changed
- No secrets found in any diff
- Staged explicit paths: `docs/reviews/sjc_vps_codex_discovery_brief.md`, `LOG.md`, `SESSION.md`
- Committed: `ab0faed` — `docs: add VPS-aligned Codex roadmap discovery brief`
- Read all required context (SJC_Intel + ivy-control VPS)
- Produced `docs/reviews/sjc_vps_codex_roadmap_prompt.md` — self-contained Codex prompt requiring ROADMAP.md with 15+ sections, worker session tables, decision tables, phase dependency graphs

**Validation:** Post-commit status clean. Only `docs/reviews/codex_roadmap_preflight.md` (prior session) and `docs/reviews/sjc_vps_codex_roadmap_prompt.md` (this session, not committed per constraint) remain untracked. Codex not run. ROADMAP.md not overwritten.
