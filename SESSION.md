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
