# Deep Research Intake Note

**Report file:** `docs/deep_research/reports/2026-06-03_homeowner_public_source_monitoring_map.md`
**Report title:** Public Source Monitoring Map for SJC_Intel in St. Johns County
**Report date:** 2026-06-03
**Intake date:** 2026-06-03
**Intake status:** Pending extraction

---

## Summary

A ChatGPT Deep Research report on homeowner-focused public source
discovery for St. Johns County. The report maps the county's decision
and operations stack (Commission, Planning & Zoning, Development
Tracker, permits, roads, utilities, schools, emergency management),
community and developer pages (SilverLeaf, Nocatee, RiverTown,
Shearwater, TrailMark, Beachwalk, Beacon Lake, eTown, Seven Pines,
EverRange, Wildlight), local media and civic sources (Jacksonville
Daily Record, local TV, Ponte Vedra Recorder, St. Johns Citizen,
Florida Public Notices, Chamber, tourism, St. Augustine city, PVB
MSD), and identifies 13 candidate homeowner beats, search term banks
across 6 categories, gap/blind-spot analysis, and backfill
recommendations.

---

## Major Source Categories Identified

1. **Government / official stack** — County Commission, Planning &
   Zoning, Development Tracker & GIS Hub, permit status, road
   closures, emergency management, parks, utilities, purchasing,
   budget/transparency, Sheriff, Property Appraiser, Tax Collector,
   Clerk, Supervisor of Elections, School District, BoardDocs,
   attendance zoning, FDOT, NFLRoads, Florida 511, SJRWMD, NWS
   Jacksonville
2. **Community / developer pages** — SilverLeaf, Nocatee, Tolomato
   CDD, RiverTown, Shearwater, Trout Creek CDD, TrailMark, Six Mile
   Creek CDD, Beachwalk, Twin Creeks North CDD, Beacon Lake, Meadow
   View CDD, eTown, Seven Pines, EverRange, Wildlight
3. **Media / civic / municipal** — Jacksonville Daily Record, local
   TV (WJXT, Action News Jax, First Coast News), Ponte Vedra
   Recorder, St. Johns Citizen, Florida Public Notices, Chamber,
   tourism, St. Augustine city, Ponte Vedra Beach MSD

## Major Homeowner Beats Identified

1. Rezoning, comp-plan, and DRI changes
2. Site plans, permits, and vertical construction
3. Roadwork and traffic impacts
4. School capacity, rezoning, and new-school delivery
5. Utilities, irrigation, reclaimed water, and boil notices
6. CDD governance, assessments, and amenity operations
7. Property taxes, exemptions, TRIM, and VAB
8. Public safety and neighborhood livability
9. Retail, grocery, restaurant, and service openings
10. Parks, libraries, trails, and amenity expansion
11. Local government, budgets, and procurement
12. Elections and district politics
13. Emergency, weather, fire, flood, and beach conditions
14. Property values and market liquidity

## Recommended First Backfill Window

The report recommends **May 2026** as the first backfill month (most
recent complete month, captures a countywide water story and FY2027
budget workshop cycle), then **August–September 2025** as a second pass
(school rezoning, TRIM/budget season, late-summer hearing cycles).

## Key Pipeline Implications

- **17 government/official sources** are new candidates for the
  canonical source registry, many of which (Commission stack, PZA,
  permit search, FDOT, SJRWMD, NWS) have very high homeowner relevance.
- **Community/CDD pages** for 11 master-planned communities are now
  identified with URLs — source candidates for community-specific
  monitoring.
- **The beat candidates** align closely with SJC_Intel's existing
  taxonomy but add specificity (e.g., "CDD governance" as a distinct
  beat, "TRIM/VAB" as a tax-season sub-beat).
- **Search term bank** provides 40+ seed strings across 6 categories
  that can feed the Search Discovery and Historical Backfill loops.
- **Gap analysis** identifies ArcGIS trackers, meeting packets, CDD
  sprawl, and resident portals as known blind spots — useful for
  managing extraction scope.

## Next Extraction Tasks

1. Extract candidate sources (government/official, community/developer,
   media/civic) → `registry/source_candidates.yaml`
2. Extract candidate beats → `registry/beat_candidates.yaml`
3. Extract search terms → `registry/search_terms.yaml`
4. Deduplicate against canonical registries
5. Recommend promotions for review
6. Route for approval

---

*Intake note created: 2026-06-03*
*Raw report: 223 lines, 13 sections*
*Candidate sources identified: ~35 across 3 categories*
*Candidate beats identified: 14*
*Search terms provided: 40+ across 6 categories*
