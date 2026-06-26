# Tier 1 + Tier 2 Promotion Review

**Reviewer:** `hermes-promotion-reviewer`  
**Date:** 2026-06-03  
**Status:** PASS — all checks passed

---

## Check Results

| # | Check | Expected | Actual | Result |
|---|-------|----------|--------|--------|
| 1 | Total sources promoted | 15 | 15 | PASS |
| 2 | Tier 1 promoted | 10 | 10 | PASS |
| 3 | Tier 2 promoted | 5 | 5 | PASS |
| 4 | No Tier 3/4 promoted | 0 | 0 | PASS |
| 5 | No media sources promoted | 0 | 0 | PASS |
| 6 | St. Johns Citizen canonical | Present | Present | PASS |
| 7 | Candidate records updated | 15 | 15 | PASS |
| 8 | YAML valid (sources.yaml) | valid | valid | PASS |
| 9 | YAML valid (candidates.yaml) | valid | valid | PASS |
| 10 | No duplicate source_ids | 0 | 0 | PASS |

## Promoted Source IDs

### Tier 1 — Core Official Stacks (10)

| source_id | CAND ID | Name |
|-----------|---------|------|
| `sjc_bcc_calendar` | CAND-SRC-0001 | County Commission stack |
| `sjc_pza_boards` | CAND-SRC-0002 | Planning and Zoning stack |
| `sjc_road_closures` | CAND-SRC-0005 | County roads, traffic, featured projects |
| `sjc_utility_department` | CAND-SRC-0008 | Utilities, water conservation, boil water |
| `sjc_budget_transparency` | CAND-SRC-0010 | Budget, OMB, transparency |
| `sjc_emergency_management` | CAND-SRC-0006 | Emergency management and alerts |
| `sjc_clerk_online_research` | CAND-SRC-0014 | Clerk online research |
| `sjc_permit_status` | CAND-SRC-0004 | Permit status and public permit search |
| `sjc_transportation_infrastructure` | CAND-SRC-0021 | County transportation and infrastructure |
| `sjrwmd_watering_restrictions` | CAND-SRC-0022 | SJRWMD permitting and watering restrictions |

### Tier 2 — School/Transportation/Weather/Civic (5)

| source_id | CAND ID | Name |
|-----------|---------|------|
| `sjcsd_boarddocs` | CAND-SRC-0017 | School Board BoardDocs |
| `sjcsd_zoning_planning` | CAND-SRC-0018 | Attendance zoning, new schools, planning |
| `fdot_district_two_nflroads` | CAND-SRC-0019 | FDOT District Two and NFLRoads |
| `nws_jacksonville` | CAND-SRC-0023 | NWS Jacksonville |
| `sjc_supervisor_of_elections` | CAND-SRC-0015 | Supervisor of Elections |

## Should NOT Have Been Promoted (Confirmed Empty)

| Candidate | Name | Correct Status |
|-----------|------|----------------|
| CAND-SRC-0024 to CAND-SRC-0033 | Tier 4 community/developer sources (10) | still recommend_promotion (awaiting Buddy) |
| CAND-SRC-0026, 0029, 0031 | Tier 3 CDD sources | still recommend_promotion (awaiting Buddy) |
| CAND-SRC-0038 | Jacksonville Daily Record | still recommend_promotion (media — awaiting Buddy) |
| CAND-SRC-0041 | Florida Public Notices | still recommend_promotion (Tier 3 — awaiting Buddy) |

## Remaining `recommend_promotion` Candidates (11)

These are all Tier 3 (CDD), Tier 4 (community/developer), or media — correct to
leave unpromoted per Buddy's instructions. They remain in the candidate registry
for future promotion waves.

1. CAND-SRC-0024 — SilverLeaf official
2. CAND-SRC-0026 — Tolomato CDD
3. CAND-SRC-0027 — RiverTown official resident-facing
4. CAND-SRC-0028 — Shearwater official
5. CAND-SRC-0029 — Trout Creek CDD
6. CAND-SRC-0030 — TrailMark official
7. CAND-SRC-0031 — Six Mile Creek CDD
8. CAND-SRC-0032 — Beachwalk amenity/district
9. CAND-SRC-0033 — Beacon Lake / Meadow View
10. CAND-SRC-0038 — Jacksonville Daily Record
11. CAND-SRC-0041 — Florida Public Notices

## Manual Review Items (Unchanged)

- Property Appraiser URL conflict (`sjcpa.gov` vs `sjcpa.us`) — not resolved
  (SRC-002)
- Stale Clerk placeholder in canonical registry (`sjcclerk.gov`) — addressed by
  promoting CAND-SRC-0014 as `sjc_clerk_online_research`

## Verdict

**PASS.** All 15 approved sources were promoted correctly. No out-of-scope
sources were promoted. YAML validates. Candidate records are updated. The
canonical registry is intact.
