# First-Wave Source Promotion Packet

**Prepared for:** Buddy approval  
**Prepared by:** `sjc-intel-architect`  
**Date:** 2026-06-03  
**Status:** Review packet only — no sources were promoted.

---

## 1. Executive Summary

The Deep Research report extracted 45 candidate sources plus 1 preserved
(St. Johns Citizen, already canonical). Of the 46 candidate records:

| Category | Count |
|----------|-------|
| Already promoted (St. Johns Citizen) | 1 |
| Duplicates of existing canonical sources | 6 |
| **Recommend promotion (this packet)** | **25** |
| Deferred (lower priority) | 12 |
| Sources needing manual review before decision | 2 |

This packet identifies **25 candidates ready for promotion approval**, organized
into four tiers. Official government stacks form Tier 1 — the highest-value,
lowest-risk promotions. Media and context sources are in Tier 4 and should be
reviewed with editorial rules in mind.

**Do not promote sources until Buddy explicitly approves each tier or
individual source.**

---

## 2. Current Canonical Source Count

`registry/sources.yaml` currently has **8 active/verified/populated sources**:

| source_id | Status | Relevance | Monitor Frequency |
|-----------|--------|-----------|-------------------|
| `sjc_county_news` | active | HIGH | daily |
| `sjso_news_stories` | active | HIGH | daily |
| `sjso_social_media` | verified | HIGH | realtime |
| `st_johns_citizen` | active | HIGH | daily |
| `sjc_school_district` | verified | HIGH | weekly |
| `sjc_development_tracker` | verified | HIGH | weekly |
| `nocatee_community` | verified | HIGH | weekly |
| `sjc_property_appraiser` | verified | MEDIUM | monthly |
| `sjc_tax_collector` | verified | MEDIUM | monthly |

Plus 5 commented-out placeholders (Supervisor of Elections, Clerk of Court,
SilverLeaf, RiverTown, Shearwater).

---

## 3. Candidate Source Count

Total in `registry/source_candidates.yaml`: **46** (45 from report + 1 preserved).

---

## 4. First-Wave Recommended Promotions

### Tier 1 — Core Official Stacks (Approve First)

Foundational county decision and operations stacks. Every source in this tier
is official, very-high homeowner relevance, useful for May 2026 backfill, and
aligns with established source families.

| # | Candidate | Proposed source_id | Source Family | Relevance | Cadence | Automation | Reliability | Why Promote Now |
|---|-----------|-------------------|---------------|-----------|---------|------------|-------------|----------------|
| 1 | County Commission stack | `sjc_bcc_calendar` | county_decision_stack | VERY_HIGH | weekly | moderate | official | Top decision-making body for votes, hearings, budgets, development. Pairs with Clerk records and GovTV for full stack. |
| 2 | Planning and Zoning stack | `sjc_pza_boards` | planning_development_stack | VERY_HIGH | weekly | moderate | official | Primary source for rezonings, comp-plan amendments, overlays, hearing schedules. Directly feeds `rezoning_comp_plan_dri` beat. |
| 3 | County roads, traffic, featured projects | `sjc_road_closures` | roads_transportation_stack | VERY_HIGH | daily | easy | official | Daily-life impact source for closures, projects, traffic ops. Directly feeds `transportation` beat. Easy automation (plain page). |
| 4 | Utilities, water conservation, boil water | `sjc_utility_department` | utilities_water_stack | VERY_HIGH | daily | easy | official | Top homeowner pain-index source. Boil notices, irrigation rules, reclaimed water. Directly feeds `utilities_water` beat. Easy automation. |
| 5 | Budget, OMB, transparency | `sjc_budget_transparency` | resident_cost_stack | VERY_HIGH | weekly (daily Jul-Sep) | easy | official | Budget cycle, millage, TRIM season, capital priorities. High value for FY2027 backfill and Aug-Sep 2025 second pass. |
| 6 | Emergency management and alerts | `sjc_emergency_management` | (cross-stack — county_decision / public_safety) | VERY_HIGH | daily in season; event-driven | easy | official | EOC updates, hurricane prep, emergency notices. Must route urgent items to human review. |
| 7 | Clerk online research | `sjc_clerk_online_research` | resident_cost_stack | VERY_HIGH | weekly | easy | official | Deeds, liens, board records, public records, tax-deed monitoring. Replaces stale placeholder URL in canonical registry. |
| 8 | Permit status and public permit search | `sjc_permit_status` | permit_construction_stack | VERY_HIGH | daily | moderate | official | Very high value for inspections, CO status, plan review. May need browser/API assessment for search form. |
| 9 | County transportation and infrastructure | `sjc_transportation_infrastructure` | roads_transportation_stack | VERY_HIGH | weekly | moderate | official | Project pipeline and delivery context. Companion to road-closure daily monitor. |
| 10 | SJRWMD permitting and watering restrictions | `sjrwmd_watering_restrictions` | utilities_water_stack | VERY_HIGH | daily | moderate | official | Permits, permit search, watering restrictions, drought orders. Phase III extreme water shortage signal. High May 2026 backfill relevance. |

**Tier 1 subtotal: 10 sources**

---

### Tier 2 — School, Transportation, Weather, Civic (Approve Next)

High-value official sources that extend core stacks.

| # | Candidate | Proposed source_id | Source Family | Relevance | Cadence | Automation | Reliability | Why Promote Now |
|---|-----------|-------------------|---------------|-----------|---------|------------|-------------|----------------|
| 11 | School Board BoardDocs | `sjcsd_boarddocs` | school_stack | VERY_HIGH | weekly (daily around meetings) | moderate | official | One of the most important pre-headline school sources. Agenda packets, policies, attachments, votes. Could be child of `sjc_school_district`. |
| 12 | Attendance zoning, new schools, planning | `sjcsd_zoning_planning` | school_stack | VERY_HIGH | weekly | moderate | official | Attendance zone changes, K-8 QQ (SilverLeaf), K-8 RR (Nocatee), district planning. Directly feeds `school_capacity` beat. |
| 13 | FDOT District Two and NFLRoads | `fdot_district_two_nflroads` | roads_transportation_stack | VERY_HIGH | daily | easy | official | State road projects: SR 16, CR 210 at CR 2209, First Coast Expressway, US 1. Companion: nflroads.com. |
| 14 | NWS Jacksonville | `nws_jacksonville` | (cross-stack — environment / public_safety) | VERY_HIGH | daily | easy | official | Essential for hurricanes, severe weather, fire weather, flood risk. Official hazards source, not general weather. |
| 15 | Supervisor of Elections | `sjc_supervisor_of_elections` | (civic / elections) | HIGH | weekly (daily in election season) | easy | official | Election dates, polling places, district maps, candidate reports, results. Replaces placeholder; candidate provides current URL (`votesjc.gov`). |

**Tier 2 subtotal: 5 sources**

---

### Tier 3 — CDD Governance (Approve with Per-Source Testing)

CDD sources are official special-district sites with very high homeowner relevance
(assessments, district debt, amenities, maintenance directly affect carrying
costs). Each CDD has its own document structure, so each needs individual
monitor design after promotion.

| # | Candidate | Proposed source_id | Source Family | Relevance | Cadence | Automation | Reliability | Caveat |
|---|-----------|-------------------|---------------|-----------|---------|------------|-------------|--------|
| 16 | Tolomato CDD (Nocatee) | `tolomato_cdd` | cdd_governance_stack | VERY_HIGH | weekly; monthly otherwise | moderate | official | Nocatee governance companion for assessments, schedules, district info. Each CDD needs individual structure test. |
| 17 | Trout Creek CDD (Shearwater) | `trout_creek_cdd` | cdd_governance_stack | VERY_HIGH | weekly; monthly otherwise | moderate | official | Shearwater-area governance. Packets, meetings, assessments. |
| 18 | Six Mile Creek CDD (TrailMark) | `six_mile_creek_cdd` | cdd_governance_stack | VERY_HIGH | weekly; monthly otherwise | moderate | official | TrailMark governance companion. |
| 19 | Florida Public Notices | `florida_public_notices` | cdd_governance_stack / public_notice | VERY_HIGH | daily | moderate | high (aggregator) | Strong cross-check for CDD notices, hearings, procurement that never receive news coverage. Daily aggregation. |

**Tier 3 subtotal: 4 sources**

---

### Tier 4 — Community/Developer Pages and Media (Approve with Conditions)

These sources are useful for amenities, events, community life, development
signals, and context — but governance/financial claims must resolve to official
records.

| # | Candidate | Proposed source_id | Source Family | Relevance | Cadence | Automation | Reliability | Condition for Promotion |
|---|-----------|-------------------|---------------|-----------|---------|------------|-------------|------------------------|
| 20 | SilverLeaf official | `silverleaf_community` | community_developer_stack | HIGH | weekly | easy | semi_official | Promote as amenity/event source. Governance claims cross-check against county records. |
| 21 | RiverTown official resident-facing | `rivertown_community` | community_developer_stack | HIGH | weekly | moderate | semi_official | Promote as resident operations/amenity source. Pair with rivertownflorida.com for builders. |
| 22 | Shearwater official | `shearwater_community` | community_developer_stack | HIGH | weekly | easy | semi_official | Promote as amenity/builder source. Governance to Trout Creek CDD. |
| 23 | TrailMark official | `trailmark_community` | community_developer_stack | HIGH | weekly | easy | semi_official | Promote as builder/amenity source. Governance to Six Mile Creek CDD. |
| 24 | Beachwalk amenity/district | `beachwalk_community` | community_developer_stack | HIGH | weekly | moderate | semi_official | Promote as lagoon/amenity signal source. Create separate Twin Creeks North CDD candidate if promoted. |
| 25 | Beacon Lake / Meadow View | `beacon_lake_community` | community_developer_stack | HIGH | weekly | moderate | semi_official | Promote as community facts source. Create separate Meadow View CDD candidate if promoted. |

**Tier 4 subtotal: 6 sources**

---

### Summary: 25 Recommend-Promotion Sources

| Tier | Theme | Count | Action |
|------|-------|-------|--------|
| 1 | Core official stacks | 10 | Approve as group or individually |
| 2 | School, transportation, weather, civic | 5 | Approve as group or individually |
| 3 | CDD governance | 4 | Approve; test each source structure individually |
| 4 | Community/developer pages | 6 | Approve; verify governance claims through records |

---

## 5. Sources to Defer (12)

These candidates are deferred — not rejected, but lower priority than the first
wave. They should be revisited after core stacks are monitoring.

| Candidate | Name | Defer Reason |
|-----------|------|--------------|
| CAND-SRC-0007 | Parks, trails, beaches stack | HIGH relevance but lower priority than roads/utilities/schools/development |
| CAND-SRC-0009 | Purchasing and active bids | HIGH relevance; promote after roads/development stack is working |
| CAND-SRC-0020 | Florida 511 | VERY_HIGH relevance but needs alert threshold definition before monitoring real-time events |
| CAND-SRC-0034 | eTown official | MEDIUM relevance; spillover watch outside core SJC scope |
| CAND-SRC-0035 | Seven Pines official | MEDIUM relevance; spillover watch only |
| CAND-SRC-0036 | EverRange official | MEDIUM relevance; spillover/growth-corridor watch |
| CAND-SRC-0037 | Wildlight official | MEDIUM relevance; comparator only |
| CAND-SRC-0039 | Local TV stack | HIGH relevance but media context/deferred until official stacks are live |
| CAND-SRC-0040 | Ponte Vedra Recorder | HIGH relevance but media context/deferred until official stacks are live |
| CAND-SRC-0042 | SJCC Chamber calendar | MEDIUM_HIGH; useful after official stacks |
| CAND-SRC-0043 | Florida's Historic Coast events | MEDIUM; events context only |
| CAND-SRC-0044 | City of St. Augustine meetings | HIGH but municipal; narrower than countywide first wave |
| CAND-SRC-0045 | Ponte Vedra Beach MSD | MEDIUM_HIGH; special district, narrower scope |

---

## 6. Sources That Duplicate Existing Canonical Sources (6)

These candidates are already covered by canonical sources. No action needed.

| Candidate | Candidate Name | Canonical Source | Notes |
|-----------|---------------|------------------|-------|
| CAND-SRC-0003 | Development Tracker & GIS Hub | `sjc_development_tracker` | Consider upgrading cadence from weekly to daily |
| CAND-SRC-0011 | Sheriff's Office | `sjso_news_stories` + `sjso_social_media` | Covered by existing news-stories monitor |
| CAND-SRC-0012 | Property Appraiser | `sjc_property_appraiser` | URL conflict needs resolution (see §7) |
| CAND-SRC-0013 | Tax Collector | `sjc_tax_collector` | Consider raising relevance from MEDIUM to HIGH |
| CAND-SRC-0016 | SJCSD district and School Board | `sjc_school_district` | Add BoardDocs details during school pilot |
| CAND-SRC-0025 | Nocatee official and public events | `nocatee_community` | Covered |

---

## 7. Sources Needing Manual Review (2)

| Issue | Candidate(s) | Details | Recommended Action |
|-------|-------------|---------|-------------------|
| Property Appraiser URL conflict | CAND-SRC-0012 | Report uses `sjcpa.gov`; canonical `sources.yaml` uses `sjcpa.us`. Need to verify which resolves correctly. | Check both URLs. Update canonical if needed. Do not promote candidate (already covered). |
| Clerk placeholder stale | CAND-SRC-0014 | Canonical `sources.yaml` has `sjc_clerk_of_court` placeholder with URL `https://www.sjcclerk.gov/` (no HTTP response). Candidate uses `https://stjohnsclerk.com/online-research/`. | Validate candidate URL. If valid, promote CAND-SRC-0014 and replace/remove stale placeholder. |

---

## 8. Proposed Promotion Process

After Buddy approves (per tier or individually):

1. **Add source record** to `registry/sources.yaml` using the proposed `source_id`,
   following `schemas/source.schema.yaml`.
2. **Update candidate record** in `registry/source_candidates.yaml`: set
   `promotion_decision: "promoted"`, add `canonical_source_id`, set
   `promoted_at` timestamp.
3. **Create initial monitor config** block in the new source record with
   `check_url`, `check_interval_hours`, and `extract_selector` (if known).
4. **Update `STATE.md`** — promotion count, current phase, next tasks.
5. **Design monitor spec** per source (or per stack for grouped sources).
6. **Run initial monitor test** — one manual fetch to confirm structure.
7. **Proceed to next candidate** — repeat until all approved sources are registered.

---

## 9. Recommended Next Action After Buddy Approval

1. **Approve Tier 1** (core official stacks) — 10 sources. These unlock the
   backbone of the monitoring system and immediately improve May 2026 backfill
   quality.
2. **Approve Tier 2** (school, transportation, weather, civic) — 5 sources.
   Completes the official-source picture.
3. **Approve Tier 3** (CDD governance) — 4 sources. Test each CDD structure
   individually after promotion.
4. **Approve Tier 4** (community/developer) — 6 sources. Promote with conditions
   that governance claims resolve to official records.
5. **Resolve manual review items** (Property Appraiser URL, Clerk placeholder).
6. **Begin source registration** — start with Tier 1, proceed through tiers.
7. **Draft initial monitor specs** for Tier 1 sources using
   `prompts/known_source_monitor_task.md` patterns.

---

## Appendix: Full Candidate Inventory

| # | candidate_id | Name | promotion_decision | Tier in This Packet |
|---|-------------|------|-------------------|---------------------|
| 1 | st_johns_citizen | St. Johns Citizen | already_promoted | — |
| 2 | CAND-SRC-0001 | County Commission stack | recommend_promotion | Tier 1 |
| 3 | CAND-SRC-0002 | Planning and Zoning stack | recommend_promotion | Tier 1 |
| 4 | CAND-SRC-0003 | Development Tracker & GIS Hub | duplicate_of_canonical | — |
| 5 | CAND-SRC-0004 | Permit status and public permit search | recommend_promotion | Tier 1 |
| 6 | CAND-SRC-0005 | County roads, traffic, featured projects | recommend_promotion | Tier 1 |
| 7 | CAND-SRC-0006 | Emergency management and alerts | recommend_promotion | Tier 1 |
| 8 | CAND-SRC-0007 | Parks, trails, beaches stack | deferred | — |
| 9 | CAND-SRC-0008 | Utilities, water conservation, boil water | recommend_promotion | Tier 1 |
| 10 | CAND-SRC-0009 | Purchasing and active bids | deferred | — |
| 11 | CAND-SRC-0010 | Budget, OMB, transparency | recommend_promotion | Tier 1 |
| 12 | CAND-SRC-0011 | Sheriff's Office | duplicate_of_canonical | — |
| 13 | CAND-SRC-0012 | Property Appraiser | duplicate_of_canonical (needs review) | — |
| 14 | CAND-SRC-0013 | Tax Collector | duplicate_of_canonical | — |
| 15 | CAND-SRC-0014 | Clerk online research | recommend_promotion | Tier 1 |
| 16 | CAND-SRC-0015 | Supervisor of Elections | recommend_promotion | Tier 2 |
| 17 | CAND-SRC-0016 | SJCSD district and School Board | duplicate_of_canonical | — |
| 18 | CAND-SRC-0017 | School Board BoardDocs | recommend_promotion | Tier 2 |
| 19 | CAND-SRC-0018 | Attendance zoning, new schools, planning | recommend_promotion | Tier 2 |
| 20 | CAND-SRC-0019 | FDOT District Two and NFLRoads | recommend_promotion | Tier 2 |
| 21 | CAND-SRC-0020 | Florida 511 | deferred | — |
| 22 | CAND-SRC-0021 | County transportation and infrastructure | recommend_promotion | Tier 1 |
| 23 | CAND-SRC-0022 | SJRWMD permitting and watering restrictions | recommend_promotion | Tier 1 |
| 24 | CAND-SRC-0023 | NWS Jacksonville | recommend_promotion | Tier 2 |
| 25 | CAND-SRC-0024 | SilverLeaf official | recommend_promotion | Tier 4 |
| 26 | CAND-SRC-0025 | Nocatee official and public events | duplicate_of_canonical | — |
| 27 | CAND-SRC-0026 | Tolomato CDD | recommend_promotion | Tier 3 |
| 28 | CAND-SRC-0027 | RiverTown official resident-facing | recommend_promotion | Tier 4 |
| 29 | CAND-SRC-0028 | Shearwater official | recommend_promotion | Tier 4 |
| 30 | CAND-SRC-0029 | Trout Creek CDD | recommend_promotion | Tier 3 |
| 31 | CAND-SRC-0030 | TrailMark official | recommend_promotion | Tier 4 |
| 32 | CAND-SRC-0031 | Six Mile Creek CDD | recommend_promotion | Tier 3 |
| 33 | CAND-SRC-0032 | Beachwalk amenity and district stack | recommend_promotion | Tier 4 |
| 34 | CAND-SRC-0033 | Beacon Lake and Meadow View district | recommend_promotion | Tier 4 |
| 35 | CAND-SRC-0034 | eTown official | deferred | — |
| 36 | CAND-SRC-0035 | Seven Pines official | deferred | — |
| 37 | CAND-SRC-0036 | EverRange official | deferred | — |
| 38 | CAND-SRC-0037 | Wildlight official | deferred | — |
| 39 | CAND-SRC-0038 | Jacksonville Daily Record | recommend_promotion | (waiting — see note) |
| 40 | CAND-SRC-0039 | Local TV stack | deferred | — |
| 41 | CAND-SRC-0040 | Ponte Vedra Recorder | deferred | — |
| 42 | CAND-SRC-0041 | Florida Public Notices | recommend_promotion | Tier 3 |
| 43 | CAND-SRC-0042 | SJCC Chamber calendar | deferred | — |
| 44 | CAND-SRC-0043 | Florida's Historic Coast events | deferred | — |
| 45 | CAND-SRC-0044 | City of St. Augustine meetings | deferred | — |
| 46 | CAND-SRC-0045 | Ponte Vedra Beach MSD | deferred | — |

**Note on media sources:** Jacksonville Daily Record (CAND-SRC-0038) is marked
`recommend_promotion` in the candidate registry but is not included in Tiers 1-4
above. It should be promoted separately after official stacks are live and with
explicit Buddy confirmation that media-context source rules are understood
(tip-surfacing only; verify consequential claims through official records).

---

*End of promotion packet. No sources were promoted. Awaiting Buddy approval.*
