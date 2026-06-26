# Deep Research Source Extraction Review

Date: 2026-06-03  
Report: `docs/deep_research/reports/2026-06-03_homeowner_public_source_monitoring_map.md`

## Summary

- Sources extracted from report tables: 45
- Existing non-report candidate preserved: 1 (`st_johns_citizen`)
- Total candidate records now in `registry/source_candidates.yaml`: 46
- Duplicates/already-covered canonical sources: 6
- Recommended promotions requiring Buddy approval: 21
- Deferred/manual-review sources: 18
- Canonical promotions made in this pass: 0

No uncertain source was promoted to `registry/sources.yaml`. St. Johns Citizen
remains promoted because that decision already existed before this pass.

## Duplicates Against Canonical Registry

| Candidate | Canonical coverage | Decision |
|-----------|--------------------|----------|
| Development Tracker and GIS Hub | `sjc_development_tracker` | duplicate_of_canonical |
| Sheriff's Office | `sjso_news_stories` plus `sjso_social_media` | duplicate_of_canonical |
| Property Appraiser | `sjc_property_appraiser` | duplicate_of_canonical; URL needs review |
| Tax Collector | `sjc_tax_collector` | duplicate_of_canonical |
| SJCSD district and School Board stack | `sjc_school_district` | duplicate_of_canonical |
| Nocatee official and public events | `nocatee_community` | duplicate_of_canonical |
| St. Johns Citizen | `st_johns_citizen` | already_promoted |

## Recommended Promotions

First-wave official/source-stack promotions to review:

- County Commission stack
- Planning and Zoning stack
- Permit status and public permit search
- County roads, traffic, and featured projects
- Emergency management and alerts
- Utilities, water conservation, and boil water stack
- Budget, OMB, and transparency stack
- Clerk online research
- Supervisor of Elections
- School Board BoardDocs
- Attendance zoning, new schools, and planning
- FDOT District Two and NFLRoads
- County transportation and infrastructure stack
- SJRWMD permitting and watering restrictions
- NWS Jacksonville
- Florida Public Notices

Community/CDD promotions to review:

- SilverLeaf official
- Tolomato CDD
- RiverTown official resident-facing site
- Shearwater official
- Trout Creek CDD
- TrailMark official
- Six Mile Creek CDD
- Beachwalk amenity and district stack
- Beacon Lake and Meadow View district stack

Media promotion to review:

- Jacksonville Daily Record

## Deferred Sources

Deferred does not mean rejected. It means lower priority or narrower scope than
the official records stack.

- Parks, trails, and beaches stack
- Purchasing and active bids
- Florida 511
- eTown official
- Seven Pines official
- EverRange official
- Wildlight official
- Local TV stack
- Ponte Vedra Recorder
- St. Johns County Chamber calendar
- Florida's Historic Coast events
- City of St. Augustine meetings and notices
- Ponte Vedra Beach MSD

## Sources Needing Manual Review

- Property Appraiser canonical URL conflict: report uses `sjcpa.gov`; canonical registry uses `sjcpa.us`.
- Clerk placeholder in canonical registry appears stale/outdated compared with report URLs.
- Permit search and GIS/map-style sources need browser/API assessment before monitor design.
- BoardDocs attachments need a packet/attachment handling rule.
- CDD sites should be tested one at a time because each district has its own document structure.
- Media sources should be treated as tip/context sources, not copied or used as sole authority for consequential claims.

## Source Families Discovered

- County decision stack: BCC, Clerk board records, GovTV, PZA, Growth Management.
- Development/permit stack: Development Tracker, GIS Hub, permit status, permit search.
- Roads/transportation stack: county road closures, traffic ops, public works, FDOT, NFLRoads, Florida 511.
- Utilities/water stack: county utility, water conservation, boil notices, SJRWMD permits/restrictions.
- School stack: SJCSD, School Board, BoardDocs, zoning, new schools, planning/government relations.
- Resident-cost stack: Property Appraiser, Tax Collector, Clerk/VAB, county budget.
- CDD governance stack: Tolomato, Trout Creek, Six Mile Creek, Twin Creeks North, Meadow View.
- Community/developer stack: official master-plan sites and amenity sites.
- Local media/context stack: St. Johns Citizen, JDR, local TV, Ponte Vedra Recorder.
- Public notice/civic stack: Florida Public Notices, Chamber, municipal meetings, tourism events.
