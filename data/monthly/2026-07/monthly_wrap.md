# July 2026 — St. Johns County Intelligence Wrap

**Status:** Internal baseline — exploratory, not publishable
**Generated:** 2026-08-02
**Task:** `03-monthly-cadence-closeout` (June/July closeout)
**Items found:** 38 (unique, per review queue reconciliation)
**Source families:** 4 (planning/development, permits/construction,
utilities/water, local-media/SilverLeaf discovery)

> **Context:** July capture is much thinner than June because daily monitoring
> ran only once (2026-07-04) and the SilverLeaf search-discovery profiles
> (active since 07-04) are the only new-content source. 25 of 38 items are
> from the single NBOR snapshot on 07-04; 11 are SilverLeaf discovery items;
> 2 are utility-department items. No county news, sheriff, emergency, BCC,
> CDD, or school items were captured in July.

---

## 1. Executive Summary

- **SilverLeaf is now the dominant resident-interest story.** The
  `silverleaf_discovery` profile produced 11 items — grocery anchor (mega
  Publix, 55k sq ft), SilverLeaf K-8 school milestone, Beach Valley Mini Golf
  proposal, CR 2209 connector highway, Harris Teeter supermarket proposals,
  Bala's second location, and a Nocatee retail/healthcare center. This is the
  first SilverLeaf-specific coverage in the inventory and directly supports
  the SilverLeaf product direction.
- **High-sensitivity public-safety items captured as unverified candidates.**
  Three of the 07-06 agentic-search candidates involve crime/incidents at or
  near SilverLeaf (ICE-detainer follow-up to the 2023 murder case, a
  construction-site shooting with a fatality, and a minor airlifted from the
  amenities center). All are `pending_review`, `unverified`, URLs unresolved,
  and human-review-required. None are promoted.
- **NBOR snapshot (07-04) mirrors June volume (25 items)** — utility ROW
  permits, rezonings/variance hearings, site plans, and one roadwork notice.
- **Utility department: two modest items** — $1.6M Plantation WTP capital
  project completion and a high Moody's rating for the utility department.
- **Every July item is `pending_review`.** Unlike June (83 verified / 10
  pending / 5 archived / 1 rejected), no July items have been reviewed.

---

## 2. Major Themes

### Theme 1: SilverLeaf Development and Commercial Growth

The strongest resident-interest theme of July is SilverLeaf commercial and
civic development:
- 55,701 sq ft mega Publix opened at 1975 SilverLeaf Parkway (first look).
- Two 61,000 sq ft Harris Teeter supermarkets proposed — one at Veterans
  Parkway/CR 210 West and one in a SilverLeaf shopping center (first major
  non-Publix grocery competition).
- Bala's (St. Johns Pizza favorite) close to opening a second location in
  SilverLeaf.
- Beach Valley Mini Golf — 36-hole, 2-acre recreation proposal (Hutson land
  lease, pending DRC approval).
- Nocatee: Ascension St. Vincent's primary care center planned for a
  Crosswater Parkway retail strip.

**Sources:** st_johns_citizen via silverleaf_discovery profile
**Beat:** development, retail_openings
**Severity:** Medium–High resident interest

### Theme 2: SilverLeaf Infrastructure and Schools

- **SilverLeaf K-8 school** reached its structural milestone (topping-out);
  190,000 sq ft, 73 classrooms, ~1,500 students, opening for the 2026–27
  school year — part of the district's anti-overcrowding push.
- **CR 2209 connector** (International Golf Parkway ↔ SilverLeaf Parkway)
  opened Oct 2025, relieving congestion around Tocoi Creek High School;
  matched to ENT-ROAD-CR-2209-CONNECTOR.

**Sources:** st_johns_citizen via silverleaf_discovery
**Beat:** school_capacity, transportation
**Severity:** Medium

### Theme 3: SilverLeaf Public-Safety Incidents (Unverified Candidates)

Five 07-06 agentic-search results, three of which are high-sensitivity:
- Man charged in connection with SilverLeaf murder case faces ICE detainer
  (appears to be a follow-up to SJC-SJSO-20260603-0004, the 2023 double-murder
  arrest — ICE angle is new).
- Man charged with shooting three at a SilverLeaf construction site, killing
  one.
- 6-year-old airlifted from SilverLeaf amenities center.
- Lower-sensitivity: suspected lightning strike on a SilverLeaf home;
  Bala's restaurant opening (development).

All are from St. Johns Citizen with **unresolved direct-fetch URLs** (timeout)
and `verification_status: unverified`. HUMAN DECISION REQUIRED before any
promotion — see `data/review_queue/queue.yaml` (SJC-SL-20260706-*).

**Sources:** st_johns_citizen via silverleaf_discovery
**Beat:** crime, public_safety
**Severity:** High (human review mandatory)

### Theme 4: NBOR Public Notices (July 4 Snapshot)

25 notices: utility ROW (Comcast x6, FPL, Beaches Energy — 8 items),
rezonings/variance hearings (7 items: St. Thomas Island Parkway cell tower,
St. Augustine Airport East, Coddington Driveway, Herlth SFR, Porter Road
extension, Canopy Shores MAJMOD, Daily's Place, Bushrangers Brewery), site
plans (10 items incl. TECO, North Beach Camp Resort, Marsh Landing, Upperline
Health), and one roadwork item (E. Peyton Pkwy traffic light activation).

**Sources:** sjc_nbor_public_notices
**Beat:** utilities_water, rezoning_comp_plan_dri, site_plans_permits_construction, roadwork_traffic
**Severity:** Medium

### Theme 5: Utility Department Announcements

- $1.6M capital improvement at Plantation Water Treatment Plant completed.
- Utility Department earned a high Moody's rating for strong financial
  management.

**Sources:** sjc_utility_department
**Beat:** utilities_water
**Severity:** Low

---

## 3. Community Mentions

| Community | Items | Notes |
|-----------|-------|-------|
| SilverLeaf | 11 | Development, school, road, retail, incidents |
| Countywide | 27 | NBOR + utility items |
| Nocatee | 1 | Retail/healthcare center (in silverleaf_discovery) |
| St. Augustine area | 2 | NBOR airport/St. Thomas Island notices |

This is the first month with meaningful SilverLeaf coverage — the first public
product's neighborhood is now appearing in the intel stream.

---

## 4. Construction / Development

NBOR site plans + rezoning dominate (17 items), plus SilverLeaf development
items (Publix, Harris Teeter, Bala's, mini golf). Highest-impact new signals:
- St. Augustine Airport East rezoning (REZ 2026000012)
- St. Thomas Island Parkway cell tower (SUPMAJ)
- Canopy Shores major PUD modification
- Bushrangers Brewery (variance + site plan)
- SilverLeaf mega Publix + Harris Teeter proposals

---

## 5. Traffic / Roads

- **E. Peyton Pkwy traffic light activation** (NBOR, single item).
- **CR 2209 connector** (SilverLeaf discovery — background/context, opened
  Oct 2025).

No county/FDOT closure items captured in July.

---

## 6. Schools

- **SilverLeaf K-8 school topping-out** (discovery, positive signal). No
  school-district direct monitoring (GAP-003 persists).

---

## 7. Public Safety

Three unverified high-sensitivity candidates (ICE detainer, construction-site
shooting, airlifted minor) plus a lightning-strike item. All are
`pending_review` and `unverified`; no SJSO/county official records confirm
them in captured data. Human review mandatory; 3 of 5 are on the
human-review list.

---

## 8. Events / Community Life

No dedicated community-event items captured in July.

---

## 9. Source Gaps

See `source_gaps.md` for full detail. Key gaps:
1. **Daily sources mostly not run in July** — only NBOR + utility (07-04).
   County news, sheriff, emergency mgmt, st_johns_citizen direct checks: 0.
2. **BCC, CDD, school, PZA, development tracker: no July items.**
3. **SilverLeaf incident candidates unverified** — URLs unresolved.

---

## 10. Taxonomy Gaps

- No new taxonomy gaps identified. `shopping` and `healthcare` interest tags
  appear on SilverLeaf items (non-canonical but informational); the existing
  `retail_openings` and `parks_amenities` beat groups cover them.

---

## 11. Resident-Interest Signal

Top interest tags across July items (queue-level, 38 items):
`development_watch` (24), `quality_of_life` (14), `utility_impact` (8),
`safety_concern` (4), `emergency_awareness` (3), `property_values` (3).

Prioritized items (matched filters): 11 `silverleaf_northwest_dev`, 10
`neighborhood_silverleaf`, 5 `major_development`, 3 `corridor_cr210`,
1 `emergency_alerts`, 1 `school_zoning_changes`, 1 `neighborhood_nocatee`.

Entity matches: ENT-COMM-SILVERLEAF (10), ENT-EDU-SILVERLEAF-K8,
ENT-REC-BEACH-VALLEY-MINI-GOLF, ENT-RETAIL-SILVERLEAF-COMMONS,
ENT-ROAD-CR-2209-CONNECTOR.

Signal distribution: all 38 `unknown` (not yet reviewed).

---

## 12. Month-over-Month vs June 2026

| Metric | June 2026 | July 2026 | Delta |
|--------|-----------|-----------|-------|
| Unique items | 99 | 38 | −61 |
| Source families | 8 | 4 | −4 |
| SilverLeaf coverage | 0 | 11 | +11 |
| NBOR notices | 25 | 25 | 0 |
| County news | 9 | 0 | −9 |
| Sheriff | 5 | 0 | −5 |
| Utility/water | 6 | 2 | −4 |
| BCC | 44 (Jan retro) | 0 | −44 |
| CDD | 9 | 0 | −9 |
| Emergency mgmt | 1 | 0 | −1 |
| School | 0 | 0 | 0 |
| Reviewed (non-pending) | 89 | 0 | −89 |

July's drop is a monitoring-cadence artifact (fewer runs), not a true decline
in county activity. The single most important structural change is the start
of SilverLeaf discovery coverage.
