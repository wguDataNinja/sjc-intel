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
