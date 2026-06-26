# sjc-intel-architect Agent Log — HERMES-001: Known-Source Monitor Task Template

**Date/time:** 2026-06-03  
**Agent:** `sjc-intel-architect`  
**Trigger:** Buddy said "get to work in supervised operator mode"  
**Task:** HERMES-001 — Draft known-source monitor task template (high priority)

## Inputs Read

- `STATE.md`
- `ROADMAP.md`
- `CHECKLIST.md`
- `BACKLOG.md`
- `docs/operator_mode.md`
- `docs/discovery_loops.md`
- `docs/taxonomy.md`
- `docs/monitoring_workflow.md`
- `docs/backfill/may_2026_backfill_plan.md`
- `registry/sources.yaml`
- `registry/source_candidates.yaml` (partial)
- `schemas/intel_item.schema.yaml`
- `schemas/source.schema.yaml`
- `prompts/resident_interest_classification_task.md`
- `.opencode/agent_memory/sjc-intel-architect.memory.md`
- `logs/agents/sjc-intel-architect/2026-06-03_codex_strong_repo_advancement.md`
- `logs/sessions/2026-06-03_initial_sjc_intel_buildout.md`

## Decision Rationale

**Selected HERMES-001 over alternatives because:**

1. **Highest-priority unblocked task** — HERMES-001 is `high` priority and has
   no hard dependencies on Buddy approval or source promotion.
2. **Gap analysis** — `docs/monitoring_workflow.md` exists as a design/architecture
   document with a YAML workflow stub, but no concise executable task prompt exists
   in the `prompts/` directory. The `resident_interest_classification_task.md`
   prompt demonstrated that the prompt format works for Hermes delegation.
3. **Forward-leveraging** — Once sources are promoted, the monitor template must
   be ready. Drafting it now reduces the gap between promotion and execution.
4. **Roadmap alignment** — Advances Phase 5 (Hermes workflow/task definitions)
   while Phase 3 source promotion review is pending Buddy approval.

**Alternative tasks considered but deprioritized:**
- *DR-005 (extraction quality review)* — medium priority, less impact
- *SRC-002/003 (URL resolution)* — medium priority, concrete but narrow
- *HERMES-002 (backfill template)* — equally high priority; selected HERMES-001
  first because monitor templates apply to ongoing operations vs. one-time backfill

## Deliverable

Created `prompts/known_source_monitor_task.md` — a standalone Hermes task prompt
for executing a known-source monitoring cycle. Includes:

1. Worker role definition and inputs (source record + prior items index)
2. Step-by-step procedure (fetch → extract → dedupe → classify → RI → structure
   → sensitivity → output)
3. Controlled vocabulary references (taxonomy.md, communities.yaml)
4. RI classification delegation to existing prompt
5. Intel item schema compliance
6. Classification defaults for official government sources
7. Sensitivity and safety rules (public sources only, no impersonation, no
   publishing, crime/safety flags)
8. Comprehensive error handling table
9. Output format specification
10. Completion return format

## Files Changed

| File | Change |
|------|--------|
| `prompts/known_source_monitor_task.md` | Created (HERMES-001 deliverable) |
| `BACKLOG.md` | Marked HERMES-001 as done |
| `STATE.md` | Added recent completed work section; updated next recommended task |
| `.opencode/agent_memory/sjc-intel-architect.memory.md` | Updated backlog summary, added log pointer |
| This log | Created |

## Blockers / Approval Needed

- Source promotion approvals still need Buddy (SRC-001, SRC-004).
- No Hermes runtime exists to execute this prompt — that's expected; it's a
  design artifact awaiting the Hermes execution layer.
- No live monitors, backfill, or automation was started.

## Next Recommended Action

Continue drafting Hermes task contracts:

1. **HERMES-002** — May 2026 backfill task template (high priority, plan exists
   at `docs/backfill/may_2026_backfill_plan.md`)
2. **HERMES-003** — Search discovery task template (medium priority, search terms
   exist in `registry/search_terms.yaml`)

Or, if Buddy is available, review and approve first-wave source promotions
(SRC-001) so the monitor template can be exercised against real sources.
