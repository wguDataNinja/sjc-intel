# June 2026 — St. Johns County Intelligence Wrap

**Status:** Internal baseline — exploratory, not publishable
**Generated:** 2026-08-02
**Task:** `03-monthly-cadence-closeout` (June/July closeout)
**Items found:** 99 (unique, per review queue reconciliation)
**Source families:** 8 (county decision, utilities/water, planning/development,
permits/construction, roads/transportation, public safety, emergency mgmt,
CDD governance)

> **Count correction note:** the prior `COVERAGE.md` figure of "June 115"
> double-counted the NBOR public-notice extraction (the `2026-06-08/` and
> `2026-06-26/` NBOR files are byte-identical duplicates of the same 25-item
> snapshot, both created 2026-06-26) and omitted the 9 CDD items. The
> reconciled unique count is **99**.

---

## 1. Executive Summary

- **BCC January 20, 2026 agenda retroactively extracted (44 items).** This
  was the single largest capture of the month and is the only BCC meeting
  whose agenda could be recovered — the June 2 and June 16 regular meetings
  remain blocked by broken Clerk links (GAP-001). It provides *January*
  content coverage with a *June* extraction date.
- **Phase III Extreme Water Shortage continues.** The May 11 declaration
  (Extreme Drought D3, one-day-per-week irrigation) remains in effect through
  June; the County Utility Department's own page continued to carry it as an
  active notice.
- **SR 207 Water Reclamation Facility went operational.** The $191.8M project —
  the largest capital improvement project in county history — began serving
  residents, closing the approval-to-operational arc begun in December 2025.
- **NBOR public notices remained the highest-yield daily source** (25 items),
  split across utility right-of-way permits (11), rezoning/variance hearings
  (6), site plans/construction (7), and one roadwork item.
- **First CDD coverage captured (9 items).** Six Mile Creek, Tolomato, and
  Trout Creek CDDs contributed governance items (board meetings, vacancies,
  elections, assessments) — the `cdd_governance_stack` moves from zero to
  active coverage.
- **Public safety volume was low but material.** Five SJSO items (four crime,
  one community-service rescue) plus jail-escape-plot charges; all
  human-review-required items remain `pending_review`.

---

## 2. Major Themes

### Theme 1: BCC Agenda Backlog — January 20 Meeting (Retroactive)

The Jan 20, 2026 BCC agenda was fully extracted (44 items) from the Clerk's
Board Records on 2026-06-26. It covers a 2050 Comprehensive Plan transmittal
hearing, several rezonings (Nothing Putt Fun, James-Cogo Commercial), median
openings, septic-to-sewer policy, utility easements, budget/procurement
resolutions, and appointments. The items are archived as `archival` urgency.

**Sources:** sjc_bcc_calendar (Clerk Board Records)
**Beat:** county_decision_stack
**Severity:** Low (archival reference) but high informational value

### Theme 2: Water Crisis Continuity — Phase III and Utility Infrastructure

The Phase III Extreme Water Shortage declaration stayed active all month.
Supporting utility infrastructure themes: the $191.8M SR 207 WRF becoming
operational, the CR 214 free-chlorine burnout (Jun 1–21), the $4.6M Utilities
Lab ribbon-cutting, the EPA Lead-Safe water-service-line inventory, and the
2025 Annual Report confirming residential rates ~10% below regional average.

**Sources:** sjc_utility_department, sjc_county_news
**Beat:** utilities_water
**Severity:** High (ongoing restriction)

### Theme 3: CDD Governance Enters Coverage

Three CDDs produced governance items in June: Six Mile Creek (board vacancy,
qualifying period for Seats 2/4, June 10 meeting), Tolomato (June 23 meeting,
April 28 minutes, FY2026 assessments), and Trout Creek (June 25 meeting,
July 7 workshop, July 23 meeting). This is the first CDD data in the
inventory and validates the `cdd_governance` topic promoted 2026-06-26.

**Sources:** six_mile_creek_cdd, tolomato_cdd, trout_creek_cdd
**Beat:** cdd_governance
**Severity:** Medium (assessments = direct cost impact for residents)

### Theme 4: Public Safety — Enforcement and Community Service

SJSO published five items: contraband drop (inmate charged), lifesaving
rescue / vulnerable-person programs, March DUI Wolfpack results (archival),
2023 double-murder arrest (high sensitivity, `verified` with human review),
and June jail-escape-plot charges. Emergency Management pushed hurricane
season preparedness (season opened June 1).

**Sources:** sjso_news_stories, sjc_emergency_management
**Beat:** public_safety_livability, emergency_weather_fire_flood
**Severity:** Medium–High

### Theme 5: NBOR Public-Notice Volume

The daily NBOR source yielded 25 unique notices on its June 26 snapshot:
utility ROW permits (Comcast, JEA, FPL, Beaches Energy, AT&T), three
variance hearings, a major PUD modification (Golfway Centre), two rezonings
(Surfside Ave, Old Moultrie Rd), construction site-plan approvals, and a
marine/roadwork notice (Farrell Marine).

**Sources:** sjc_nbor_public_notices
**Beat:** utilities_water, rezoning_comp_plan_dri, site_plans_permits_construction, roadwork_traffic
**Severity:** Medium

---

## 3. Community Mentions

| Community | Items | Notes |
|-----------|-------|-------|
| Countywide | ~86 | Dominant — most items are county-wide (BCC, NBOR, utility) |
| CDD areas (TrailMark, Nocatee/Shearwater) | 9 | CDD governance items |
| St. Augustine / West Augustine | 2 | Railroad crossing closure; double-murder arrest context |
| Vilano Beach / Porpoise Point | 1 | Beach access ramp resiliency |
| SilverLeaf | 0 | No SilverLeaf items in June capture (all in July) |

Notable gaps: SilverLeaf, Nocatee, RiverTown, Beachwalk, Beacon Lake, CR 210
corridor had zero June items in the captured data.

---

## 4. Construction / Development

NBOR rezoning and site-plan notices dominate (13 combined items):
- **Rezonings / variances (6):** Bargfrede Shed, Aspinwall, Tatum,
  Golfway Centre PUD (major modification), 177 Surfside Ave, 3025 Old
  Moultrie Rd.
- **Site plans / construction (7):** City of St. Augustine project, AT&T x2,
  Terracon, P&G Construction, Scott Waite, plus utility ROW permits.
- BCC rezonings also captured retroactively (Nothing Putt Fun, James-Cogo).

No development-tracker or PZA data captured (known gaps).

---

## 5. Traffic / Roads

- **Railroad crossing closure:** W. King Street and Kinlaw Road closed
  temporarily for crossing maintenance (county news, Jun 22).
- **NBOR roadwork:** Farrell Marine notice (single item).
- No FDOT, FL511, or county roads-department direct feeds captured.

---

## 6. Schools

No June school items. The school district has not been monitored since the
May backfill; BoardDocs pilot remains pending (GAP-003).

---

## 7. Public Safety

- **Contraband drop** (May 21 incident, reported June 3): inmate + civilian
  charged. Human review done, `verified`.
- **Lifesaving rescue**: autistic juvenile rescued from pond; family enrolled
  in Project Lifesaver / K9 Scent Kit / SAFE programs. Human review done.
- **March DUI Wolfpack**: 9 arrests, 173 stops (archival).
- **2023 double-murder arrest**: suspect charged in West Augustine (high
  sensitivity; `verified` with human review). Note: this is a **different
  case** from the later SilverLeaf murder-related items captured in July.
- **Jail escape plot** (Jun 22): two inmates charged. Human review done.

All crime/safety items are `human_review_required: true`; 4 remain
`pending_review` in the queue.

---

## 8. Events / Community Life

- Surplus Goods Public Auction (June 20)
- Library Summer Reading Program (runs through July 25)
- Library Card Sign-Up Month business program (deadline Aug 3)
- Porpoise Point beach access ramp resiliency completion ($524K)
- Recycling-driver feel-good feature (rejected as noise)

---

## 9. Source Gaps

See `source_gaps.md` for full detail. Key gaps:
1. **BCC June meetings (Jun 2, Jun 16) not extractable** — GAP-001, broken
   Clerk agenda links.
2. **No school district coverage** — GAP-003.
3. **Emergency management under-monitored** — only 1 June item; hurricane
   season runs Jun–Nov.
4. **No SJRWMD items** captured despite the active Phase III declaration
   (utility page carried it; SJRWMD itself not re-checked).
5. **No PZA / development-tracker / permit-status / FDOT / NWS items.**

---

## 10. Taxonomy Gaps

- No new taxonomy gaps found in June items. Existing canonical topics
  (`water_restrictions`, `budget_millage`, `cdd_governance`) were sufficient.
- NBOR items remain tagged `development`/`infrastructure` rather than the
  proposed `permit_status` / `public_records` candidates — flagged in
  `docs/taxonomy.md` as likely future proposals.

---

## 11. Resident-Interest Signal

Top interest tags across June items (queue-level, 99 items):
`utility_impact` (28), `community_trust` (23), `quality_of_life` (21),
`development_watch` (20), `cost_impact` (14).

Signal distribution: 35 `high_signal`, 7 `medium_signal`, 55 `unknown`
(review-queue population), 1 `low_signal`, 1 `routine_noise`.
Prioritized items (matched filters): 8 `major_development`, 8
`utility_disruption`, 3 `emergency_alerts`, 3 `corridor_sr16`, 2
`corridor_cr210`.

Entity matches: ENT-INFRA-SR-207-WRF (2 items), ENT-ROAD-CR-2209-CONNECTOR (1).

---

## 12. Month-over-Month vs May 2026

| Metric | May 2026 | June 2026 | Delta |
|--------|----------|-----------|-------|
| Unique items | 21 | 99 | +78 |
| Source families | 5 | 8 | +3 |
| BCC decision coverage | 0 | 44 (Jan 20 retro) | +44 |
| NBOR notices | 0 | 25 | +25 |
| CDD governance | 0 | 9 | +9 |
| School coverage | 10 | 0 | −10 |
| Emergency mgmt | 1 | 1 | 0 |
| Sheriff | 2 | 5 | +3 |
| County news | 4 | 9 | +5 |
| Utility/water | 3 | 6 | +3 |
| Local media | 0 | 0 | 0 |

June is the first month with NBOR, BCC-agenda, and CDD data — the largest
single-month capture to date. The school gap is the most significant
regression.
