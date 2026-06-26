# sjc-intel-architect Agent Log — Utility Monitor Lessons Applied

**Date/time:** 2026-06-03  
**Agent:** `sjc-intel-architect`  
**Trigger:** Apply pilot findings from `sjc_utility_department` monitor

## Changes Made

### 1. Monitor Spec Updated

`docs/monitor_specs/sjc_utility_department.md`:

- Added pilot status banner: **PASSED** — 5 items, YAML valid, Hermes-ready
- **§6 Extraction Approach:** Added step 6 for "Featured Department News"
  sidebar extraction. Documented the 2025 Annual Report as a missed item from
  the first cycle.
- **§14:** Replaced "First Pilot Recommendation" with "Pilot Results and Next
  Steps." Documented concrete findings (page structure stable, boil alert
  fallback works), confirmed taxonomy gap `water_restrictions`, and laid out
  daily automation steps including sidebar scope.

### 2. Backlog Updated

- **MON-006** added: "Run recurring daily utility monitor" — todo, high.
  Executes daily at 8:00 AM using `prompts/known_source_monitor_task.md`.
- **TAX-003** updated: `water_restrictions` evidence is ready from backfill
  (2 items) + live monitor (1 item). Priority raised to high.
- **TAX-004** added: `budget_millage` evidence ready from backfill (1 item).

### 3. State & Memory Updated

- STATE.md notes `sjc_utility_department` as "first daily-ready source."
- Memory updated with MON-006 and taxonomy backlog refinements.

## Key Decision

Taxonomy gaps `water_restrictions` and `budget_millage` now have sufficient
evidence for promotion. TAX-003 and TAX-004 are ready for Buddy approval or
architect execution.

## Files Changed

| File | Change |
|------|--------|
| `docs/monitor_specs/sjc_utility_department.md` | Pilot banner, sidebar extraction (§6), pilot results (§14) |
| `BACKLOG.md` | MON-006 added; TAX-003 updated; TAX-004 added |
| `STATE.md` | Noted first daily-ready source |
| `.opencode/agent_memory/sjc-intel-architect.memory.md` | Updated backlog, next task |
| This log | Created |
