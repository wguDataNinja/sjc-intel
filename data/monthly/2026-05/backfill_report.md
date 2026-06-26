# Backfill Report — May 2026

**Task:** `historical-backfill-2026-05`  
**Executed:** 2026-06-03  
**Worker:** `historical-backfill-worker`  
**Status:** completed (with warnings)

---

## Source-Check Log

| Source ID | Checked? | May Items Found? | Notes |
|-----------|----------|-----------------|-------|
| `sjc_county_news` | Yes | Yes (4) | WordPress blog with date-filtered archive. Featured items visible on main page. |
| `sjc_bcc_calendar` | Yes | No | Calendar shows upcoming meetings only; past meetings link to external agenda PDFs. No inline archive. |
| `sjc_pza_boards` | Yes | No | Page is a boards listing. Meeting archive not directly scrapable from main page. |
| `sjc_road_closures` (now `sjc_nbor_public_notices`) | Yes (backfill) / ✅ (post-backfill) | No (backfill) / 25 records found (post-backfill) | Landing page was dead end. NBOR app found 2026-06-08 — plain HTML, daily-ready. |
| `sjc_utility_department` | Yes | Yes (3) | Utility department page includes Announcements section with dated entries. Phase III notice, chlorine burnout, and past projects. |
| `sjc_emergency_management` | Yes | Yes (1) | Hurricane preparedness page. Seasonal messaging; no specific May emergency events. |
| `sjc_budget_transparency` | Yes | No | Budget page for FY2026. May 2026 is outside budget cycle (peak is Jul-Sep). |
| `sjc_clerk_online_research` | No | — | Not checked in this pass. Portal-based search requires form interaction. |
| `sjc_permit_status` | No | — | Not checked in this pass. Permit search requires form interaction. |
| `sjc_transportation_infrastructure` | Yes | No | Division landing page; no dated items. |
| `sjrwmd_watering_restrictions` | Yes | Yes (1) | SJRWMD site references Phase III declaration. General permitting page; specific drought orders may be on separate page. |
| `sjc_school_district` | Yes | Yes (10) | WordPress portal with news feed, video archive, and events. Multiple May items found. |
| `sjcsd_boarddocs` | Yes | Yes (1) | BoardDocs public portal confirms May 12 meeting. |
| `sjcsd_zoning_planning` | Yes | No | Zoning page is static; no dated announcements. |
| `fdot_district_two_nflroads` | Yes | No | FDOT District Two landing page; no specific SJC project updates found. |
| `nws_jacksonville` | No | — | Not checked in this pass. NWS site is real-time; historical May 2026 data would need archive search. |
| `sjc_supervisor_of_elections` | No | — | Not checked in this pass. Off-election-cycle month. |
| `sjso_news_stories` | Yes | Yes (2) | WordPress blog with date-filtered stories. Two May 2026 items found. |
| `sjc_development_tracker` | No | — | GIS map page; not easily searchable historically. |

## Search Term Effectiveness

| Category | Terms Used | Effective? | Notes |
|----------|------------|------------|-------|
| Utilities/water | ST-0601–ST-0604 | Yes | Found Phase III declaration and related utility content |
| School | ST-0201–ST-0205 | Yes | Multiple SJCSD items found |
| Community | ST-0001–ST-0013 | Partial | Community terms returned limited results in official-source-only pass |
| Transportation | ST-0101–ST-0106 | No | No road closure or traffic items found |
| Permits/development | ST-0301–ST-0302 | No | No permit or development items found |
| Corridor | ST-0101–ST-0106 | No | Corridor-specific terms returned nothing |

## Items Summary

| Metric | Value |
|--------|-------|
| Total items extracted | 21 |
| By source: `sjc_school_district` | 10 |
| By source: `sjc_county_news` | 4 |
| By source: `sjc_utility_department` | 3 |
| By source: `sjso_news_stories` | 2 |
| By source: `sjrwmd_watering_restrictions` | 1 |
| By source: `sjc_emergency_management` | 1 |
| By topic: education | 12 |
| By topic: environment/water | 3 |
| By topic: public safety | 3 |
| By topic: infrastructure | 2 |
| By topic: county government | 1 |
| Items with `human_review_required: true` | 1 (SJC-BF-202605-0019) |
| Taxonomy gaps proposed | 2 (`water_restrictions`, `budget_millage`) |

## Issues Encountered

| Issue | Severity | Workaround |
|-------|----------|------------|
| BCC calendar does not archive past agendas inline | Warning | Manual PDF inspection needed for past meetings |
| Road closures page links to external app | Warning | SJC Road Closures app may need API or browser automation |
| PZA meeting archive not directly accessible | Warning | May need direct page inspection of minutes |
| Permit search requires form interaction | Info | Deferred from first pass |
| Clerk portal requires form interaction | Info | Deferred from first pass |
| FDOT District Two page lacks per-project updates | Warning | NFLRoads or site-specific searches needed |
| Some SJCSD items lack full article text (video-only) | Info | Video descriptions provide context, not full articles |

## Recommendations for Next Pass

1. **Immediate follow-up:** Inspect BCC meeting agendas and minutes for May 5
   and May 19 meetings. These likely contain development approvals, budget
   decisions, and policy votes.
2. **Road closures data source:** Investigate the SJC Neighborhood Bill of
   Rights application as a potential data source for road closure history.
3. **PZA agenda archive:** Directly check PZA meeting minutes page for May
   2026 hearings.
4. **Taxonomy proposals:** Consider promoting `water_restrictions` and
   `budget_millage` to canonical topic tags given real item evidence.
5. **Second-pass scope:** Include community/CDD sources (SilverLeaf, Nocatee)
   and St. Johns Citizen for media context.
6. **Monitor spec design:** The most productive sources from this backfill
   (county news, school district, sheriff) already have monitor specs.
   Next priorities: `sjc_utility_department` and `sjc_nbor_public_notices` (NBOR, closed gap).

## Completion Checklist

- [x] All official source stacks attempted (results recorded)
- [x] `discovered_items.yaml` created (21 items)
- [x] `topic_clusters.yaml` created (4 clusters, 6 unclustered)
- [x] `source_gaps.md` created (7 gaps identified)
- [x] `monthly_wrap.md` created (11 sections)
- [x] `backfill_report.md` created (this file)
- [x] All items have required schema fields
- [x] Sensitive items flagged `human_review_required: true`
- [x] No unsanctioned taxonomy values used
- [x] No publishing, scheduling, or monitor execution occurred
