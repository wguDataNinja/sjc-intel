# Hermes Task: Tier 1 Source Promotion

**Worker:** `hermes-source-promoter`  
**Task:** `tier-1-promotion-2026-06-03`  
**Approval:** Buddy approved Tier 1 (core official stacks) via SRC-001 packet

## Scope

Promote only Tier 1 sources from `registry/source_candidates.yaml` into
`registry/sources.yaml`. Update candidate records. Do NOT touch Tier 2, 3, 4,
or media sources.

## Approved Tier 1 Sources (10)

| Candidate ID | Name | Proposed source_id |
|-------------|------|-------------------|
| CAND-SRC-0001 | County Commission stack | `sjc_bcc_calendar` |
| CAND-SRC-0002 | Planning and Zoning stack | `sjc_pza_boards` |
| CAND-SRC-0005 | County roads, traffic, featured projects | `sjc_nbor_public_notices` (formerly `sjc_road_closures`) |
| CAND-SRC-0008 | Utilities, water conservation, boil water | `sjc_utility_department` |
| CAND-SRC-0010 | Budget, OMB, transparency | `sjc_budget_transparency` |
| CAND-SRC-0006 | Emergency management and alerts | `sjc_emergency_management` |
| CAND-SRC-0014 | Clerk online research | `sjc_clerk_online_research` |
| CAND-SRC-0004 | Permit status and public permit search | `sjc_permit_status` |
| CAND-SRC-0021 | County transportation and infrastructure | `sjc_transportation_infrastructure` |
| CAND-SRC-0022 | SJRWMD permitting and watering restrictions | `sjrwmd_watering_restrictions` |

## Inputs

- `docs/source_promotion/first_wave_source_promotion_packet.md`
- `registry/source_candidates.yaml`
- `registry/sources.yaml`
- `schemas/source.schema.yaml`

## Steps

1. For each Tier 1 source:
   a. Read candidate record from `source_candidates.yaml`.
   b. Add new source record to `sources.yaml` following the schema, with
      proposed `source_id`, URL, source_type, relevance, monitor_frequency,
      automatable, status: `verified`, topics, communities, notes.
   c. Update candidate record: set `promotion_decision: "promoted"`,
      `canonical_source_id: "<source_id>"`, `promoted_at` timestamp.
2. Validate YAML after all edits.
3. Do not promote Tier 2, 3, 4, or media sources.
4. Do not resolve manual-review items (Property Appraiser URL, Clerk placeholder).
5. Write report to `logs/agents/hermes/2026-06-03_tier_1_promotion.md`.

## Completion Criteria

- 10 new source records in `sources.yaml`.
- 10 candidate records updated with `promotion_decision: promoted`.
- YAML validates without errors.
- No Tier 2/3/4/media sources promoted.
- Report written.
