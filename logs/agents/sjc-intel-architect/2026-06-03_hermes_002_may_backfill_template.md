# sjc-intel-architect Agent Log — HERMES-002: May 2026 Backfill Template

**Date/time:** 2026-06-03  
**Agent:** `sjc-intel-architect`  
**Task:** HERMES-002 — Draft May 2026 historical backfill Hermes task template

## Inputs Read

- `STATE.md`
- `BACKLOG.md`
- `CHECKLIST.md`
- `docs/operator_mode.md`
- `docs/backfill/may_2026_backfill_plan.md`
- `docs/discovery_loops.md`
- `docs/taxonomy.md`
- `docs/resident_interest_classification.md`
- `docs/monitoring_workflow.md`
- `registry/sources.yaml`
- `registry/search_terms.yaml`
- `schemas/intel_item.schema.yaml`
- `prompts/known_source_monitor_task.md`
- `.opencode/agent_memory/sjc-intel-architect.memory.md`

## Deliverable

Created `prompts/hermes_may_2026_backfill_task.md` — a bounded Hermes task
template for executing the May 2026 historical backfill. Contains all 15
required sections:

1. Purpose — exploratory baseline, not definitive journalism
2. Source scope — official/high-authority sources only (Tier 1 + 2); media/CDD/Tier 4 excluded
3. Date scope — 2026-05-01 through 2026-05-31
4. Search/source-check instructions — direct source checks + web search, with term priorities
5. Deduping rules — URL, source+title+date, cross-source merge
6. Factual extraction rules — per intel_item schema v2.0
7. Resident-interest classification rules — with mandatory human-review triggers
8. Sensitivity/privacy rules — public sources only, no publishing, minimal PII
9. Topic/beat clustering rules — min 2 items per cluster, beat_candidate labels
10. Source gap rules — identify missing sources, gaps in coverage
11. Output schema expectations — 5 output files with YAML/MD formats
12. Completion/block protocol — checklist, block conditions, partial completion
13. Explicit "do not publish" rule
14. Explicit "public sources only" rule
15. Exploratory, not definitive journalism — labeling uncertainty

## Key Design Decisions

- **First pass limited to official sources only** — media and community sources
  deferred to reduce scope and focus on authoritative records.
- **5 output files** instead of the plan's 4 — added `backfill_report.md` for
  operational logging (source check log, term effectiveness, issues).
- **No dedupe with live index** — within-month dedupe only; does not touch
  `data/index/prior_items.yaml`.
- **Item ID format `SJC-BF-202605-{NNNN}`** — distinguishes backfill items
  from live monitor items.
- **Term priority list** — utilities/water and transportation first, matching
  Deep Research's recommended beat focus.

## Readiness Assessment

HERMES-002 is **ready to run** — but **requires explicit instruction from Buddy**
before execution. The template is complete, bounded, and verifiable.

## Blockers Before Running

1. No Hermes runtime exists for automated execution.
2. Requires explicit Buddy instruction to begin.
3. Manual source checks may need human judgment for ambiguous dates or page
   structures.
4. Property Appraiser URL conflict (SRC-002) may affect backfill coverage of
   resident-cost stack — unresolved.

## Recommended Execution Strategy

When ready to run:

1. **Execute as a single bounded Hermes task** — the worker follows the 5-step
   output pipeline: search → extract → dedupe/classify → cluster → report.
2. **Start with utilities/water and transportation** (highest resident-impact
   beats for May 2026).
3. **Produce all 5 output files in sequence.**
4. **Architect reviews outputs** — checks schema shape, scope compliance,
   sensitivity flags, and gap analysis.
5. **Iterate** — refine search terms, add sources, adjust taxonomy based on
   what the backfill reveals.

## Files Changed

| File | Change |
|------|--------|
| `prompts/hermes_may_2026_backfill_task.md` | Created (HERMES-002 deliverable, 280+ lines) |
| `logs/agents/sjc-intel-architect/2026-06-03_hermes_002_may_backfill_template.md` | Created (this log) |

## Next Recommended Action

- Update `BACKLOG.md` (mark HERMES-002 done).
- Update `STATE.md`.
- Update memory.
- Next task: HERMES-003 (search discovery template) or monitor spec design
  for `sjc_road_closures` and `sjc_utility_department`.
