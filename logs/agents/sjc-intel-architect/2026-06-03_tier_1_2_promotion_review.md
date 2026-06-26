# sjc-intel-architect Operator Log — Tier 1 + Tier 2 Promotion Review

**Date/time:** 2026-06-03  
**Agent:** `sjc-intel-architect` (operator/reviewer)  
**Delegated workers:** `hermes-source-promoter` (Task A, Task B), `hermes-promotion-reviewer` (Task C)

## Summary

Buddy approved Tier 1 and Tier 2 sources from the SRC-001 promotion packet.
I created three bounded Hermes task contracts, executed them as separate workers,
then reviewed all outputs as architect.

## Hermes Task Contracts Created

| Contract | File | Purpose |
|----------|------|---------|
| Task A | `prompts/hermes_tier_1_promotion_task.md` | Promote 10 Tier 1 sources |
| Task B | `prompts/hermes_tier_2_promotion_task.md` | Promote 5 Tier 2 sources (merge-safe with Tier 1) |
| Task C | `prompts/hermes_promotion_review_task.md` | Validate and review both promotions |

## Worker Reports

- `logs/agents/hermes/2026-06-03_tier_1_promotion.md` — Tier 1: 10 sources, PASS
- `logs/agents/hermes/2026-06-03_tier_2_promotion.md` — Tier 2: 5 sources, PASS
- `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md` — Review: all 10 checks PASS

## Sources Promoted (15)

### Tier 1 — Core Official Stacks

| source_id | Name | Family |
|-----------|------|--------|
| `sjc_bcc_calendar` | County Commission Calendar | county_decision_stack |
| `sjc_pza_boards` | Planning and Zoning Boards | planning_development_stack |
| `sjc_road_closures` | County Roads and Traffic | roads_transportation_stack |
| `sjc_utility_department` | Utility Department — Water/Boil | utilities_water_stack |
| `sjc_budget_transparency` | Budget, OMB, Transparency | resident_cost_stack |
| `sjc_emergency_management` | Emergency Management | (cross-stack) |
| `sjc_clerk_online_research` | Clerk Online Research Portal | resident_cost_stack |
| `sjc_permit_status` | Permit Status and Search | permit_construction_stack |
| `sjc_transportation_infrastructure` | County Transportation | roads_transportation_stack |
| `sjrwmd_watering_restrictions` | SJRWMD Permitting/Restrictions | utilities_water_stack |

### Tier 2 — School/Transportation/Weather/Civic

| source_id | Name | Family |
|-----------|------|--------|
| `sjcsd_boarddocs` | School Board BoardDocs | school_stack |
| `sjcsd_zoning_planning` | School Attendance Zoning | school_stack |
| `fdot_district_two_nflroads` | FDOT District Two / NFLRoads | roads_transportation_stack |
| `nws_jacksonville` | NWS Jacksonville | (cross-stack) |
| `sjc_supervisor_of_elections` | Supervisor of Elections | (civic) |

## Scope Compliance

- Only Tier 1 and Tier 2 promoted ✓
- No Tier 3 (CDD), Tier 4 (community/developer), or media sources promoted ✓
- St. Johns Citizen remains canonical and unmodified ✓
- All 15 promoted candidates updated with `promotion_decision: promoted` ✓
- 11 `recommend_promotion` candidates remain (Tier 3/4/media — correct) ✓
- YAML validated for both `sources.yaml` and `source_candidates.yaml` ✓

## Unresolved Items

- Property Appraiser URL conflict (`sjcpa.gov` vs `sjcpa.us`) — SRC-002 still open
- Stale `sjc_supervisor_of_elections` placeholder removed (replaced by promoted source)
- Stale `sjc_clerk_of_court` placeholder remains commented-out (replaced by `sjc_clerk_online_research`)
- No Hermes runtime for automated monitoring yet

## Files Changed in This Session

| File | Change |
|------|--------|
| `registry/sources.yaml` | +15 new source records (24 total) |
| `registry/source_candidates.yaml` | 15 records updated to promoted; 11 remain recommend_promotion |
| `STATE.md` | Full state update for new phase |
| `BACKLOG.md` | SRC-001 marked done |
| `.opencode/agent_memory/sjc-intel-architect.memory.md` | Full state update |
| `prompts/hermes_tier_1_promotion_task.md` | Created |
| `prompts/hermes_tier_2_promotion_task.md` | Created |
| `prompts/hermes_promotion_review_task.md` | Created |
| `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md` | Created |
| `logs/agents/hermes/2026-06-03_tier_1_promotion.md` | Created |
| `logs/agents/hermes/2026-06-03_tier_2_promotion.md` | Created |
| `logs/agents/sjc-intel-architect/2026-06-03_tier_1_2_promotion_review.md` | Created (this log) |

## Next Recommended Action

Design monitor specs for the new sources, starting with high-cadence
easy-automation sources:
- `sjc_road_closures` (daily, easy) — first monitor spec
- `sjc_utility_department` (daily, easy)
- `sjc_emergency_management` (daily, easy)
- `sjc_bcc_calendar` (weekly, moderate)

Or draft HERMES-002 (May 2026 backfill task template).
