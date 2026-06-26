# Hermes Task: Tier 2 Source Promotion

**Worker:** `hermes-source-promoter`  
**Task:** `tier-2-promotion-2026-06-03`  
**Approval:** Buddy approved Tier 2 (school/transportation/weather/civic) via SRC-001 packet
**Dependency:** Must merge with `sources.yaml` after Tier 1 promotion

## Scope

Promote only Tier 2 sources. Do NOT touch Tier 1, 3, 4, or media sources.

## Approved Tier 2 Sources (5)

| Candidate ID | Name | Proposed source_id |
|-------------|------|-------------------|
| CAND-SRC-0017 | School Board BoardDocs | `sjcsd_boarddocs` |
| CAND-SRC-0018 | Attendance zoning, new schools, planning | `sjcsd_zoning_planning` |
| CAND-SRC-0019 | FDOT District Two and NFLRoads | `fdot_district_two_nflroads` |
| CAND-SRC-0023 | NWS Jacksonville | `nws_jacksonville` |
| CAND-SRC-0015 | Supervisor of Elections | `sjc_supervisor_of_elections` |

## Inputs

- `docs/source_promotion/first_wave_source_promotion_packet.md`
- `registry/source_candidates.yaml`
- `registry/sources.yaml` (post-Tier-1)
- `schemas/source.schema.yaml`

## Steps

1. Read current `sources.yaml` (must include Tier 1 promotions).
2. For each Tier 2 source:
   a. Read candidate record.
   b. Add new source record to `sources.yaml`.
   c. Update candidate record: `promotion_decision: "promoted"`,
      `canonical_source_id`, `promoted_at`.
3. Validate YAML.
4. Do not promote Tier 1, 3, 4, or media sources.
5. Write report to `logs/agents/hermes/2026-06-03_tier_2_promotion.md`.

## Completion Criteria

- 5 new source records appended to `sources.yaml` (coexisting with Tier 1).
- 5 candidate records updated.
- YAML validates.
- No non-Tier-2 sources promoted.
- Report written.
