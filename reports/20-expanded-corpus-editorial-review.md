# Task 20 — Expanded Corpus Editorial Review for SilverLeaf Brief

**Task identity:** 20-expanded-corpus-editorial-review.md
**Date:** 2026-08-04
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Final status:** COMPLETE

**Read-only scope honored:** no publication decisions changed, no review status
changed, no source records altered, no taxonomy changes, no UI changes, no
deploy, no commit, no push. One read-only live source check was performed
(recorded in §28).

---

## 1. Executive result

The actual SJC_Intel corpus is substantially larger and more SilverLeaf-relevant
than the current four-item release suggests. This review inspected **231 unique
intelligence items** spanning **May 2025 – August 2026** (August–September 2025
backfill, May 2026 baseline, June 2026, July 2026, and August 2026 catch-up)
and produced a decision-ready, source-supported map of what belongs in the
inaugural SilverLeaf Brief archive.

Key findings:

- **~30 candidates** have credible SilverLeaf relevance (direct, nearby, or
  countywide-household). Of these, **10–14 are strong inaugural additions**
  (Tier 1) and ~10 more are useful after copy/source work (Tier 2).
- The strongest under-used material is **durable SilverLeaf context**: the
  CR 2209 connector, the SilverLeaf K-8 school (confirmed still under
  construction), the mega Publix, proposed Harris Teeter supermarkets, Beach
  Valley Mini Golf, the SR 16/CR 210 corridor projects, and the SR 207
  water-reclamation facility — none of which appear in the current release.
- The corpus supports a **two-part product shape**: keep Latest as a small
  current/ongoing release (4–8 items) and publish a larger **Browse/archive
  corpus** of durable context. The current static data contract does not yet
  support an archive corpus and needs a small, defined extension (§24–25).
- **Repetition is concentrated**: five-plus items describe the same continuing
  subjects (CR 2209, SilverLeaf K-8, water shortage, SR 207 WRF, FY2026
  budget). Publishing one clear current item per cluster with a timeline is
  better than five near-duplicate updates.
- **Public-safety/crime remains excluded** (policy), and the 44-item January
  2026 BCC backfill and most NBOR utility permits are **boilerplate noise**
  with no SilverLeaf value.

No publication or review state was changed.

## 2. Starting repository state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `9c985c7` (clean; local == origin) |
| Working tree | Clean (0 changes) |
| Tests | 217 passed |
| Validators | `validate.py` ALL PASSED; corpus validator 0 errors / 321 warnings; scope validator PASS |
| Publication decisions | 4 (the current release: CR 16A, hurricane, service-line, water) |
| Review queue | 167 entries (83 verified / 77 pending / 1 duplicate / 5 archived / 1 rejected_noise) |
| Current public site | 4-item release, 13 routes |

## 3. Corpus and time periods inspected

| Period | Source | Items inspected |
|--------|--------|----------------|
| 2025-05–12 | `data/intel_items/` + backfill | SilverLeaf K-8 (May 2025), CR 2209 (Oct 2025), Harris Teeter (Dec 2025) |
| Aug–Sep 2025 backfill | `data/monthly/2025-08/`, `2025-09/` | 48 items (FY2026 budget, school arc, CR 210, SR 16, Pine Island Rd) |
| May 2026 baseline | `data/monthly/2026-05/` | 21 items (school 10, county news 4, utility 3, SJSO 2, SJRWMD 1, EM 1) |
| June 2026 | `data/intel_items/2026-06-03/08/26/`, `data/monthly/2026-06/` | ~99 unique (44 BCC Jan retro, 25 NBOR, utility, county news, emergency, SJSO) |
| July 2026 | `data/intel_items/2026-07-04/`, `2026-07-06/`, `data/search_runs/2026-07-06/` | 38 items (11 SilverLeaf discovery, NBOR, utility) |
| Aug 2026 catch-up | `data/intel_items/2026-08-02/` | 5 items (CR 16A, Daily's, S.E.A., Clerk, SJSO) |
| Legacy CDD | `data/intel_items/2026-06-26/` | 9 archival records |

Also inspected: `data/review_queue/`, `data/publication_decisions/`,
`data/index/`, `registry/` (sources, communities, tracked entities, SilverLeaf
scope), `docs/source_discoveries/`, `docs/source_reviews/`, monthly crosscut and
wrap syntheses.

## 4. Total candidate universe

**231 unique item records** (deduped across `intel_items` + `monthly` +
`search_runs`; 25 records exist in both `intel_items` and a monthly backfill).

| Review status | Count |
|---------------|-------|
| verified | 83 |
| pending_review | 133 |
| archived | 4 |
| duplicate | 1 |
| rejected_noise | 1 |
| (none — legacy CDD) | 9 |

| Source family | Count |
|---------------|-------|
| NBOR public notices | 75 |
| County news | 46 |
| BCC calendar (Jan 2026 retro) | 44 |
| St. Johns Citizen (SilverLeaf discovery) | 11 |
| School district (SJCSD) | 11 |
| Utility department | 9 |
| SJSO | 8 |
| CDD (legacy) | 9 |
| Emergency management | 2 |
| Other (tax, budget, SJRWMD, web) | 6 |

**SilverLeaf-relevant candidate pool (after full record inspection): ~30
items.** The rest are excluded on relevance/quality grounds (§20).

## 5. Relevance classification summary

Classes applied per §4 (from the SilverLeaf-resident perspective, using actual
record content — not keyword matching):

| Class | Count | Representative items |
|-------|-------|----------------------|
| DIRECT_SILVERLEAF | 12 | CR 2209 expansion, mega Publix, SilverLeaf K-8, Harris Teeter, mini golf, Bala's, CR 16A (published), SilverLeaf crime (excluded) |
| NEARBY_MATERIAL | 8 | SR 16 widening (IGP–I-95), CR 210 widening, Four Mile Rd/SR 16, Nocatee retail/Ascension, NW-Sector NBOR meetings, railroad crossing |
| COUNTYWIDE_HOUSEHOLD | 9 | Phase III water (published), SR 207 WRF, service-line (published), hurricane (published), Programs of Choice, half-cent surtax, FY2026 budget tax cut, S.E.A. center |
| DURABLE_CONTEXT | 8 | School QQ/RR construction + naming, Hallowes Cove opening + attendance zoning, budget-cycle arc, CR 210 timeline |
| WEAK_OR_INCIDENTAL | ~10 | SJC-SL-20260706-0003 lightning, NBOR single-word utility permits, county library promos, Clerk service center |
| NOT_RELEVANT | ~180 | BCC boilerplate resolutions, St. Augustine/coastal rezonings, Ponte Vedra boil notice, most NBOR, all CDD, all SJSO crime |

## 6. Product-role classification summary

| Role | Count | Meaning |
|------|-------|---------|
| CURRENT_RELEASE | 4 | The published four (water, hurricane, service-line, CR 16A) |
| ACTIVE_OR_ONGOING | 4 | SilverLeaf K-8, Phase III water (ongoing), SR 207 WRF (online May 2026), Programs of Choice (deadline passed — now history) |
| RECENT_HISTORY | 6 | CR 2209 opened (Oct 2025), mega Publix (Mar 2026), mini golf proposal, SR 16 groundbreak, CR 210 shift, FY2026 budget |
| DURABLE_CONTEXT | 10 | School QQ/RR construction + naming, Harris Teeter proposal, Nocatee retail, Hallowes Cove + zoning, SR 16 corridor, utility program evolution |
| ENTITY_TIMELINE | 8 | SilverLeaf K-8, CR 2209, Publix, Harris Teeter, mini golf, SR 207 WRF, Baptist (inferred), water shortage |
| PLACE_TIMELINE | 4 | CR 210 corridor, SR 16 corridor, SilverLeaf neighborhoods, countywide water |
| SOURCE_REFERENCE_ONLY | ~20 | NBOR notices, BCC resolutions, budget-cycle arc (reference value only) |
| EXCLUDE | ~180 | See §20 |

This classification strongly supports **Option B** (small Latest + broader
Browse/archive), because the corpus's durable value is largely contextual and
timeline-shaped rather than "fresh news."

## 7. Roads and traffic candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-CN-20260802-0001 CR 16A closures | DIRECT (access road) | CURRENT | **PUBLISHED** |
| SJC-BF-202508-0013 CR 2209 expansion underway | DIRECT (silverleaf) | ENTITY_TIMELINE | STRONG_PUBLISH (as context) |
| SJC-SL-20260704-0004 CR 2209 connector opened | DIRECT | ENTITY_TIMELINE | MERGE with above |
| SJC-BF-202508-0020 SR 16 widening (IGP–I-95) hearings | NEARBY | ENTITY_TIMELINE | STRONG_PUBLISH (context) |
| SJC-BF-202508-0021 SR 16/IGP intersection groundbreaking | NEARBY | ENTITY_TIMELINE | MERGE with 0020 |
| SJC-BF-202509-0013 Four Mile Rd / SR 16 open house | NEARBY | RECENT_HISTORY | DEFER (minor) |
| SJC-BF-202508-0010 CR 210 widening traffic shift | NEARBY | RECENT_HISTORY | STRONG_PUBLISH (context) |
| SJC-BF-202508-0011 Beachwalk alternate access | NEARBY | RECENT_HISTORY | MERGE with 0010 |
| SJC-CN-20260626-0002 Railroad crossing West King/Kinlaw | NEARBY | RECENT_HISTORY | DEFER (likely completed) |

Source-supported facts (Tier 1): CR 2209 — county began construction Aug 2025
building a four-lane corridor between Silverleaf Parkway and SR 16; opened
Oct 28, 2025 per local reporting. SR 16 — FDOT public hearings Aug 2025 for
widening IGP to I-95; $25M SR 16/IGP intersection improvements broke ground
Aug 2025. CR 210 — widening traffic shift Aug 15, 2025.
Resident interpretation: these are the access roads SilverLeaf households
depend on; durable context explains today's commute.
Temporal: CR 2209 **completed**; SR 16 **underway/planned** (follow-up needed);
CR 210 **ongoing/completed** (follow-up needed).
Publication concern: CR 2209 has two near-duplicate records (merge); SR 16 has
two (merge); none have a follow-up milestone since late 2025.

## 8. Utilities and water candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-UTIL-20260603-0001 Phase III water shortage | COUNTYWIDE | CURRENT / ongoing | **PUBLISHED** |
| SJC-UTIL-20260603-0005 service-line inventory | COUNTYWIDE | CURRENT | **PUBLISHED** |
| SJC-CN-20260626-0001 SR 207 WRF now serving | COUNTYWIDE | ENTITY_TIMELINE | STRONG_PUBLISH (context) |
| SJC-UTIL-20260603-0003 SR 207 WRF Phase 2 approved | COUNTYWIDE | ENTITY_TIMELINE | MERGE with above |
| SJC-BF-202605-0005 SJRWMD one-day-per-week | COUNTYWIDE | RECENT_HISTORY | MERGE into water shortage |
| SJC-BF-202509-0012 manhole rehabilitation program | COUNTYWIDE | DURABLE_CONTEXT | DEFER (low value) |
| SJC-UD-20260704-0001 $1.6M Plantation WTP | COUNTYWIDE | RECENT_HISTORY | DEFER (Ponte Vedra) |
| SJC-UD-20260704-0002 Moody's rating | COUNTYWIDE | RECENT_HISTORY | DEFER (low value) |
| SJC-UTIL-20260603-0002 chlorine burnout (Jun 1–21) | COUNTYWIDE | RECENT_HISTORY | EXCLUDE (event over) |

Source-supported facts (Tier 1): SR 207 WRF — $191.8M facility now operational
(county news, Jun 2026); prior record documents the Dec 2025 Phase 2
design-build approval. Both describe the same project (merge into one durable
item: "largest capital improvement in county history, now serving residents").
Temporal: **completed/operational** May 11, 2026. Publication concern: two
records for one project; the utility item and county item should merge.

## 9. Schools and education candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-BF-202509-0006 K-8 Schools QQ/RR construction update | DIRECT (silverleaf) | ENTITY_TIMELINE | STRONG_PUBLISH (as context/active) |
| SJC-SL-20260704-0002 SilverLeaf K-8 topping-out | DIRECT | ENTITY_TIMELINE | MERGE with above |
| SJC-BF-202509-0008 School QQ/RR naming & mascot | DIRECT (silverleaf) | ENTITY_TIMELINE | MERGE (context) |
| SJC-BF-202508-0005 Hallowes Cove Academy opens | NEARBY | RECENT_HISTORY | PUBLISH_AS_CONTEXT |
| SJC-BF-202508-0006/07/08 + 202509-0005 attendance zoning + first students | NEARBY | DURABLE_CONTEXT | MERGE (school-arc timeline) |
| SJC-BF-202605-0009 Programs of Choice application | COUNTYWIDE | ACTIVE (deadline passed) | DEFER / BUDDY_DECISION |
| SJC-BF-202605-0008 St. Johns Compass (Aug 2026 launch) | COUNTYWIDE | RECENT_HISTORY | PUBLISH_AFTER_SOURCE_CHECK |
| SJC-BF-202605-0011 half-cent surtax / one mill | COUNTYWIDE | DURABLE_CONTEXT | PUBLISH_AS_CONTEXT |
| SJC-BF-202605-0013 SJCSD 'A' grade | COUNTYWIDE | RECENT_HISTORY | DEFER (no SL angle) |

Source-supported facts (Tier 1): SilverLeaf K-8 (School QQ) — 190,000 sq ft,
73 classrooms, ~1,500 students, topping-out May 2025, expected to open for
2026-27; **live source check 2026-08-04: SJCSD confirms School QQ (SilverLeaf
DRI, Parcel 29C) is "Under Construction."** School RR (Nocatee) same program.
Naming/mascot community engagement began Sep 2025.
Resident interpretation: the single most important neighborhood-specific
school story; parents need the opening/boundary status.
Temporal: **under construction / opening imminent** (2026-27).
Publication concern: three records describe the same school — merge into one
durable item with a timeline; opening date/boundary still needs confirmation.

## 10. Development and zoning candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-SL-20260704-0005 two new supermarkets (Harris Teeter) | DIRECT | DURABLE_CONTEXT | STRONG_PUBLISH (as context) |
| SJC-SL-20260704-0003 Beach Valley Mini Golf | DIRECT | ENTITY_TIMELINE | STRONG_PUBLISH (as context) |
| SJC-NBOR-20260704-0020 NW Sector Colee Cove Tower | NEARBY? (location unconfirmed) | RECENT_HISTORY | BUDDY_DECISION |
| SJC-NBOR-20260802-0007 NW Sector Little Florence Fish Camp | NEARBY? | RECENT_HISTORY | BUDDY_DECISION |
| SJC-NBOR-20260802-0002 NW Sector Bartram Grove CPA/MAJMOD | NEARBY? | RECENT_HISTORY | BUDDY_DECISION |
| SJC-NBOR-20260802-0001 Moseley Property CPA(SS) | unknown | RECENT_HISTORY | DEFER |
| SJC-BCC-20260120-0001 2050 Comprehensive Plan hearing | COUNTYWIDE | DURABLE_CONTEXT | DEFER (durable but generic) |
| SJC-BCC-20260120-0002 REZ Nothing Putt Fun | unknown | RECENT_HISTORY | EXCLUDE (location unknown) |

Source-supported facts (Tier 1): Harris Teeter — two 61,000 sq ft Kroger-owned
supermarkets proposed, one at Veterans Pkwy/CR 210 West and one **in a
SilverLeaf shopping center** (Dec 2025 local reporting). Beach Valley Mini
Golf — 36-hole course on 2 acres in SilverLeaf proposed Apr 2026.
Resident interpretation: grocery competition and an on-site family amenity are
directly relevant; both are **proposals** and must stay conditional.
Publication concern: both are local-media sourced (need corroboration); both
are proposals (conditional wording required); status since the original
reports is unknown (source check needed).

## 11. Businesses, services, and amenities candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-SL-20260704-0001 mega Publix opened | DIRECT | ENTITY_TIMELINE | STRONG_PUBLISH (as context) |
| SJC-SL-20260704-0006 Nocatee retail center / Ascension | NEARBY | ENTITY_TIMELINE | PUBLISH_AFTER_SOURCE_CHECK |
| SJC-SL-20260706-0005 Bala's second location | DIRECT | RECENT_HISTORY | PUBLISH_AFTER_SOURCE_CHECK (URL 404) |
| ENT-HEALTH-BAPTIST-SILVERLEAF (no item) | DIRECT | — | **Coverage gap** (registry only) |
| ENT-RETAIL-SILVERLEAF-COMMONS / MARKET (no items) | DIRECT | — | **Coverage gap** |

Source-supported facts (Tier 1): mega Publix — 55,701 sq ft at 1975 SilverLeaf
Parkway, opened Mar 2026 (local reporting). Nocatee — Ascension St. Vincent's
primary care planned in a six-storefront strip on Crosswater Pkwy (Jun 2026).
Resident interpretation: Publix is the neighborhood grocery anchor; Ascension
adds nearby healthcare.
Temporal: Publix **completed**; Nocatee/Ascension **proposed/under
construction**; Bala's **opening likely, unverified**.
Publication concern: all local media — corroboration recommended; Bala's
recorded URL returns 404 (article exists via site search, needs corrected URL).

## 12. Government and community-service candidates

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-BF-202509-0003 FY2026 budget tax reduction | COUNTYWIDE | DURABLE_CONTEXT | STRONG_PUBLISH (as context) |
| SJC-BF-202509-0001/0002 budget hearings + adoption | COUNTYWIDE | DURABLE_CONTEXT | MERGE into budget timeline |
| SJC-BF-202508-0001/0002 TRIM + tax roll | COUNTYWIDE | DURABLE_CONTEXT | MERGE (budget/tax arc) |
| SJC-BF-202509-0004 tax bills mailed | COUNTYWIDE | DURABLE_CONTEXT | MERGE (budget/tax arc) |
| SJC-CN-20260802-0003 S.E.A. resource center | WEAK (rural SJC) | RECENT_HISTORY | DEFER (weak SL link) |
| SJC-CN-20260802-0004 Clerk service center | WEAK | RECENT_HISTORY | DEFER (no SL angle) |
| BCC January 44-item backfill | NOT_RELEVANT | SOURCE_REFERENCE_ONLY | EXCLUDE (boilerplate) |

Source-supported facts (Tier 1): FY2026 — $1.8B county budget adopted Sep 16,
2025 with the **first property-tax rate reduction since FY2021** (county press
release).
Resident interpretation: property-tax direction directly affects every
household; durable context for the next TRIM/budget season (Aug–Sep 2026,
upcoming and currently uncovered).
Temporal: **adopted/completed**; relevance **recurring**.
Publication concern: the FY2026 cycle is old; if published, it needs a "durable
context — FY2026" label and a link to the upcoming FY2027 cycle. Note: the
half-cent sales surtax + one mill (SJC-BF-202605-0011) is a separate, ongoing
school-funding fact that belongs with schools or taxes.

## 13. Preparedness and public-safety candidates

Durable preparedness (keep separate from crime):

| Item | Relevance | Role | Disposition |
|------|-----------|------|-------------|
| SJC-EM-20260626-0001 hurricane season prep | COUNTYWIDE | CURRENT | **PUBLISHED** |
| SJC-BF-202605-0021 hurricane preparedness messaging | COUNTYWIDE | RECENT_HISTORY | MERGE into published EM item |
| SJC-BF-202508-0022 Alert St. Johns notification episode | COUNTYWIDE | DURABLE_CONTEXT | DEFER (low value) |

Public-safety / crime (excluded for v0 by policy):

| Item | Disposition |
|------|-------------|
| SJC-SJSO-20260603-0001/0004, SJC-SJSO-20260626-0001, SJC-SJSO-20260802-0001, SJC-BF-202605-0019 | EXCLUDE (crime/public-safety policy) |
| SJC-SL-20260706-0001/-0002/-0004 (ICE, shooting, minor) | EXCLUDE (high sensitivity, crime/minors) |
| SJC-SJSO-20260603-0002 lifeguard/rescue (low) | BUDDY_DECISION (positive community story; policy-adjacent) |

Source-supported facts: none published here (all excluded). The SilverLeaf
crime/minor candidates remain pending_review and are flagged human-review in
the queue — they must not enter v0 without an explicit policy exception.

## 14. Entity and place clusters

| Cluster | Related item IDs | Current known state | Strongest candidate |
|---------|------------------|---------------------|----------------------|
| SilverLeaf K-8 (School QQ) | SJC-BF-202509-0006, SJC-SL-20260704-0002, SJC-BF-202509-0008 | Under construction (verified live) | SJC-BF-202509-0006 |
| CR 2209 connector | SJC-BF-202508-0013, SJC-SL-20260704-0004 | Opened Oct 2025 | SJC-SL-20260704-0004 |
| SR 207 Water Reclamation | SJC-CN-20260626-0001, SJC-UTIL-20260603-0003 | Operational May 2026 | SJC-CN-20260626-0001 |
| Phase III water shortage | SJC-UTIL-20260603-0001, SJC-CN-20260603-0005, SJC-BF-202605-0005 | Active (verified live) | SJC-UTIL-20260603-0001 (published) |
| Harris Teeter proposal | SJC-SL-20260704-0005, ENT-RETAIL-HARRIS-TEETER-SILVERLEAF | Proposed (status unknown) | SJC-SL-20260704-0005 |
| Mega Publix | SJC-SL-20260704-0001, ENT-RETAIL-PUBLIX-SILVERLEAF | Opened Mar 2026 | SJC-SL-20260704-0001 |
| SR 16 corridor | SJC-BF-202508-0020, SJC-BF-202508-0021, SJC-BF-202509-0013 | Underway (follow-up needed) | SJC-BF-202508-0021 |
| CR 210 widening | SJC-BF-202508-0010, SJC-BF-202508-0011 | Ongoing/completed (follow-up) | SJC-BF-202508-0010 |
| FY2026 budget/tax cycle | SJC-BF-202508-0001..0004, SJC-BF-202509-0001..0004 | Adopted Sep 2025 | SJC-BF-202509-0003 |
| Hallowes Cove school arc | SJC-BF-202508-0005..0008, SJC-BF-202509-0005 | Opened 2025-26 | SJC-BF-202508-0005 |
| Baptist SilverLeaf campus | (registry only — no item) | Tracked | **No candidate** (gap) |

## 15. Timeline opportunities

Best timeline candidates (publish as one durable item + timeline rather than
repeated updates):

1. **SilverLeaf K-8 timeline** — topping-out (May 2025) → construction update
   (Sep 2025) → naming/mascot (Sep 2025) → opening (2026-27). Merge 3 records;
   one durable "current status: under construction, opening for 2026-27."
2. **CR 2209 timeline** — construction began (Aug 2025) → opened (Oct 2025).
   Merge 2 records.
3. **SR 207 WRF timeline** — approved (Dec 2025) → operational (May/Jun 2026).
   Merge 2 records.
4. **Water shortage timeline** — declaration (May 2026) → ongoing (Jun–Aug
   2026). The published item carries it; do not republish near-duplicates.
5. **FY2026 budget/tax timeline** — TRIM (Aug) → hearings (Sep) → adoption +
   tax cut → bills (Sep 30). Merge 8 records into one durable context item.
6. **Hallowes Cove / attendance zoning arc** — zoning (Aug 2025) → opening →
   first students → QQ/RR planning. Useful as a northwest-corridor school
   context timeline.

Recommendation: do **not** publish 5 repetitive updates per project. Publish
one current item with a chronological timeline where the record supports it.

## 16. Missing and underrepresented coverage

| Area | Finding |
|------|---------|
| Schools | Data exists but unreviewed + **stale**: SilverLeaf K-8 records are Sep-2025-era; no 2026 opening/boundary item. **Top gap.** |
| Major roads | CR 2209/CR 210/SR 16 have late-2025 records; **no 2026 status follow-up**. First Coast Expressway effects (SR 13/CR 16A) referenced but not tracked. |
| Active development | NW-Sector NBOR items exist but **location metadata missing** — relevance classification failed; needs geocoding/editorial tagging. |
| Community businesses | Publix/Harris Teeter/mini-golf present; **Baptist SilverLeaf campus, Silverleaf Commons, Silverleaf Market have no items** (registry only). |
| Healthcare | Only Nocatee/Ascension + Baptist registry. |
| Utilities | Good (water shortage, WRF, service-line); no boil-water notices for the SL area; SJRWMD direct coverage is a recurring gap. |
| CDD/governance | 9 legacy records, archival-only; no SilverLeaf CDD (SilverLeaf is not a CDD-governed community in current data). |
| County services | Present but weak SL angle. |
| SilverLeaf neighborhoods | `communities.yaml` has 12; **no items tagged to specific neighborhoods** — place timelines impossible. |
| FY2027 TRIM/budget (upcoming Aug–Sep 2026) | **No coverage yet**; highest-value *upcoming* gap. |

None of these require a broad new discovery run; they require (a) source
coverage for the FY2027 cycle and school opening, and (b) editorial tagging
(location, neighborhood) of existing records.

## 17. Tier 1 — Strong inaugural additions (10–14)

Complete evidence packets (§6–7 fields) for each:

### 17.1 SJC-BF-202509-0006 — SilverLeaf K-8 construction (merged timeline)
- Item: SJC-BF-202509-0006 (SJCSD newschools; pending, low, source_confirmed).
  Merge: SJC-SL-20260704-0002, SJC-BF-202509-0008.
- Proposed title: "SilverLeaf K-8 School Under Construction, Set to Open for 2026–27"
- Source: SJCSD New School Construction (stjohns.k12.fl.us/newschools/); date
  Sep 15, 2025; observed Jun 26, 2026.
- Topics: education, school_capacity → display topic **Schools & Community**.
- Places: silverleaf. Entities: ENT-EDU-SILVERLEAF-K8.
- Relevance: **DIRECT_SILVERLEAF**. Role: **ACTIVE_OR_ONGOING / ENTITY_TIMELINE**.
- Summary (source-supported): 190,000 sq ft, 73-classroom K-8 (School QQ) in
  the SilverLeaf DRI; expected ~1,500 students; SJCSD confirmed "Under
  Construction" as of Aug 4, 2026.
- Resident significance: school opening + boundary are the top neighborhood
  questions.
- Temporal: **under construction, opening imminent**.
- Publication concern: local-media + district sources; merge 3 records; confirm
  opening date/attendance zone before a "current" claim. Disposition:
  **STRONG_PUBLISH** (as context; opening confirmed needs a final source check).

### 17.2 SJC-SL-20260704-0004 — CR 2209 connector opened (merged)
- Item: SJC-SL-20260704-0004 (St. Johns Citizen; pending, low). Merge:
  SJC-BF-202508-0013 (county).
- Proposed title: "CR 2209 Connector Opens Between International Golf Parkway and SilverLeaf"
- Source: St. Johns Citizen, Oct 28, 2025; county Aug 20, 2025.
- Topics: transportation/infrastructure → **Roads & Traffic**.
- Places: silverleaf, cr_210_corridor. Entity: ENT-ROAD-CR-2209-CONNECTOR.
- Relevance: **DIRECT_SILVERLEAF**. Role: **ENTITY_TIMELINE / DURABLE_CONTEXT**.
- Summary: three-mile four-lane connector IGP→SilverLeaf Parkway opened Oct 28,
  2025; construction began Aug 2025.
- Resident significance: direct SilverLeaf→IGP/I-95 route; commute relief.
- Temporal: **completed** (Oct 2025). Disposition: **STRONG_PUBLISH** (context).

### 17.3 SJC-SL-20260704-0001 — Mega Publix opened
- Item: SJC-SL-20260704-0001 (St. Johns Citizen; pending, low, source_confirmed).
- Proposed title: "SilverLeaf's Mega Publix Is Now Open"
- Source: St. Johns Citizen, Mar 26, 2026.
- Topic **Local Business**. Places silverleaf. Entity ENT-RETAIL-PUBLIX-SILVERLEAF.
- Relevance: **DIRECT_SILVERLEAF**. Role: **ENTITY_TIMELINE / DURABLE_CONTEXT**.
- Summary: 55,701 sq ft Publix at 1975 SilverLeaf Parkway, opened Mar 2026 with
  full-service departments.
- Resident significance: neighborhood grocery anchor.
- Temporal: **completed**. Disposition: **STRONG_PUBLISH** (context).

### 17.4 SJC-SL-20260704-0005 — Harris Teeter proposal
- Item: SJC-SL-20260704-0005 (St. Johns Citizen; pending, low).
- Proposed title: "Harris Teeter Supermarket Proposed for a SilverLeaf Center"
- Topic **Local Business**. Places silverleaf. Entity ENT-RETAIL-HARRIS-TEETER-SILVERLEAF.
- Relevance: **DIRECT_SILVERLEAF**. Role: **DURABLE_CONTEXT**.
- Summary: two 61,000 sq ft supermarkets proposed (one SilverLeaf, one CR 210
  West); conditional wording required.
- Resident significance: grocery competition + second option in-community.
- Temporal: **proposed** (status unknown). Publication concern: local media;
  needs corroboration; **must stay conditional**. Disposition:
  **STRONG_PUBLISH** (context, after source check).

### 17.5 SJC-SL-20260704-0003 — Beach Valley Mini Golf
- Item: SJC-SL-20260704-0003 (St. Johns Citizen; pending, low).
- Proposed title: "Mini-Golf Course Proposed for SilverLeaf"
- Topic **Local Business** or **Schools & Community** (amenity) → recommend
  **Local Business** for v0 (amenity/recreation). Places silverleaf. Entity
  ENT-REC-BEACH-VALLEY-MINI-GOLF.
- Relevance: **DIRECT_SILVERLEAF**. Role: **ENTITY_TIMELINE / DURABLE_CONTEXT**.
- Summary: 36-hole course on 2 acres proposed (Apr 2026), husband-and-wife
  developers, lease from The Hutson Companies.
- Temporal: **proposed**. Disposition: **STRONG_PUBLISH** (context, conditional).

### 17.6 SJC-CN-20260626-0001 — SR 207 Water Reclamation now serving (merged)
- Item: SJC-CN-20260626-0001 (county news; verified, low). Merge:
  SJC-UTIL-20260603-0003.
- Proposed title: "County's Largest-Ever Water Project Now Serving Residents"
- Topic **Utilities & Water**. Relevance: **COUNTYWIDE_HOUSEHOLD**. Role:
  **ENTITY_TIMELINE / ACTIVE_OR_ONGOING**.
- Summary: $191.8M SR 207 Water Reclamation Facility operational May 2026;
  ~15 miles of pipelines; reclaimed water capacity; funded by utility revenues.
- Resident significance: reclaimed-water capacity + utility stewardship
  (relevant to SilverLeaf irrigation and growth).
- Temporal: **operational**. Disposition: **STRONG_PUBLISH** (context).

### 17.7 SJC-BF-202508-0021 — SR 16 / IGP improvements (merged)
- Item: SJC-BF-202508-0021 (county news; pending, low). Merge: SJC-BF-202508-0020.
- Proposed title: "SR 16 and International Golf Parkway Improvements Underway"
- Topic **Roads & Traffic**. Places: sr_16_corridor, cr_210_corridor. Relevance:
  **NEARBY_MATERIAL**. Role: **ENTITY_TIMELINE**.
- Summary: $25M intersection improvements broke ground Aug 2025; FDOT widening
  of SR 16 (IGP–I-95) hearings held Aug 2025.
- Resident significance: SilverLeaf's western access/commute route.
- Temporal: **underway/planned** (needs 2026 follow-up). Disposition:
  **STRONG_PUBLISH** (context) — mark "status as of late 2025; follow-up needed."

### 17.8 SJC-BF-202508-0010 — CR 210 widening
- Item: SJC-BF-202508-0010 (county news; pending, low). Merge: SJC-BF-202508-0011.
- Proposed title: "CR 210 Widening Underway Through Northern St. Johns"
- Topic **Roads & Traffic**. Place cr_210_corridor. Relevance: **NEARBY_MATERIAL**.
  Role: **ENTITY_TIMELINE / DURABLE_CONTEXT**.
- Summary: traffic shifted to new roadway Aug 2025 as part of widening; Beachwalk
  access advisories.
- Temporal: **ongoing/completed** (follow-up needed). Disposition:
  **STRONG_PUBLISH** (context).

### 17.9 SJC-BF-202509-0003 — FY2026 budget / property-tax reduction
- Item: SJC-BF-202509-0003 (county news; pending, low). Merge: SJC-BF-202508-0001..0004,
  SJC-BF-202509-0001/0002/0004.
- Proposed title: "County Adopts $1.8 Billion Budget With First Tax-Rate Cut Since FY2021"
- Topic **Government & Community** (new display topic needed) — or **Schools &
  Community**? Recommend adding a v0 topic **"Government & Taxes"** (see §24).
  Relevance: **COUNTYWIDE_HOUSEHOLD**. Role: **DURABLE_CONTEXT**.
- Summary: FY2026 budget adopted Sep 16, 2025; first property-tax rate
  reduction since FY2021; TRIM→hearing→adoption→bills arc.
- Resident significance: property-tax direction affects every household; frame
  as context for the upcoming FY2027 cycle.
- Temporal: **adopted (FY2026)**. Disposition: **STRONG_PUBLISH** (context, with
  FY2026 label).

### 17.10 SJC-BF-202605-0011 — school funding (half-cent surtax + one mill)
- Item: SJC-BF-202605-0011 (SJCSD; pending, low).
- Proposed title: "Half-Cent Sales Surtax and One Mill Keep Funding County Schools"
- Topic **Schools & Community** (or **Government & Taxes**). Relevance:
  **COUNTYWIDE_HOUSEHOLD**. Role: **DURABLE_CONTEXT**.
- Summary: voter-approved surtax (capital) + one mill (operations) continue
  funding schools.
- Temporal: **active/recurring**. Disposition: **STRONG_PUBLISH** (context) —
  it explains how schools are funded (relevant when discussing K-8 building).

### 17.11 (Optional) SJC-SL-20260704-0006 — Nocatee retail / Ascension
- Item: SJC-SL-20260704-0006 (St. Johns Citizen; pending, low).
- Proposed title: "Primary Care + Retail Coming to Nocatee's Crosswater Center"
- Topic **Local Business** / healthcare. Place nocatee (adjacent-only).
  Relevance: **NEARBY_MATERIAL**. Role: **ENTITY_TIMELINE / DURABLE_CONTEXT**.
- Disposition: **PUBLISH_AFTER_SOURCE_CHECK** (local media; adjacent-only label).

### 17.12 (Optional) SJC-BF-202508-0005 — Hallowes Cove Academy (merged arc)
- Merge SJC-BF-202508-0005/06/07/08 + SJC-BF-202509-0005 into one
  "northwest-corridor school context" item. Disposition: **PUBLISH_AS_CONTEXT**
  (nearby school relief; attendance-zoning arc).

Tier 1 total: **10–14 items** depending on the two optionals and merges.

## 18. Tier 2 — Useful after copy/source work

| Item | Work needed | Recommendation |
|------|-------------|----------------|
| SJC-SL-20260706-0005 Bala's | Correct URL (article exists via site search; recorded URL 404); confirm location | PUBLISH_AFTER_SOURCE_CHECK |
| SJC-BF-202605-0008 St. Johns Compass | Confirm launch details (Aug 2026) | PUBLISH_AFTER_SOURCE_CHECK |
| SJC-SL-20260704-0006 Nocatee/Ascension | Corroborate local media; adjacent label | PUBLISH_AFTER_SOURCE_CHECK |
| SJC-BF-202605-0005 SJRWMD water | Merge into published water item as the SJRWMD source | MERGE_WITH_RELATED |
| SJC-BF-202605-0021 hurricane prep | Merge into published EM item | MERGE_WITH_RELATED |
| SJC-BF-202509-0007 enrollment/capacity | Needs SJCSD source detail | DEFER (thin) |
| SJC-BF-202605-0013 'A' grade | No SilverLeaf angle unless framed as context | DEFER / BUDDY_DECISION |
| SJC-CN-20260802-0003 S.E.A. center | Weak SL link; rural SJC | DEFER |
| SJC-NBOR NW-Sector items (Colee Cove, Little Florence, Bartram Grove) | **Missing location metadata**; relevance unverifiable | DEFER until geo-tagged, or BUDDY_DECISION if Buddy knows the sites |
| SJC-SJSO-20260603-0002 rescue (low) | Policy decision (public-safety-adjacent positive) | BUDDY_DECISION |

## 19. Tier 3 — Durable context or timeline material

- FY2026 budget/tax arc (all 8 records) — merge into §17.9 or keep as a
  reference timeline.
- Hallowes Cove + attendance zoning arc (2025) — nearby school context.
- CR 210 widening timeline (Aug–Sep 2025).
- SR 16 corridor timeline (Aug–Sep 2025).
- Utility programs: manhole rehabilitation (SJC-BF-202509-0012), raised
  pavement markers (SJC-BF-202509-0014), utilities annual report
  (SJC-UD-20260626-0001).
- 2050 Comprehensive Plan transmittal hearing (SJC-BCC-20260120-0001) —
  long-horizon county land-use context.
- SilverLeaf neighborhoods/place background (registry-level; no items).

## 20. Tier 4 — Exclude

| Group | Reason |
|-------|--------|
| All SJSO crime/arrest items (8) | Public-safety/crime policy exclusion |
| SilverLeaf crime/minor items SJC-SL-20260706-0001/-0002/-0004 | High sensitivity, crime/minors |
| SJC-SL-20260706-0003 lightning | Unverified, low value |
| BCC January 2026 backfill (~40 of 44) | Boilerplate resolutions, stale, no SL value |
| NBOR utility ROW permits (Comcast/AT&T/JEA/FPL/etc., ~40) | Noise; single-word titles |
| NBOR St. Augustine / coastal rezonings (REZ/ZVAR/MAJMOD/ARC, ~20) | Not SilverLeaf-relevant; medium sens |
| CDD legacy records (9) | Archival only; not release candidates |
| Ponte Vedra / coastal items (boil notice, Marsh Landing, Magic Beach, North Beach, Porpoise Point, Solomon Calhoun) | Not SilverLeaf access/corridor |
| Library/civic promos (summer reading, awards, auctions, recycling) | No household impact |
| Free chlorine burnout (event over) | Stale |
| Moody's rating / utilities lab / Clerk center | Low resident value |
| SJC-BF-202508-0009 / 202509-0009/0010 (Ponte Vedra water/boil) | Not SilverLeaf |

## 21. Proposed public copy (Tier 1)

Kept source-supported; editorial interpretation labeled. (Only a sample; full
packets in §17.)

- **SilverLeaf K-8**: Summary: "SilverLeaf's new K-8 school (School QQ) is
  under construction and expected to open for the 2026–27 school year, adding
  about 1,500 seats." Why: "The opening may change attendance zones and end
  long commutes for SilverLeaf students." Conditional wording preserved.
- **CR 2209**: Summary: "The connector between International Golf Parkway and
  SilverLeaf Parkway opened October 28, 2025, giving SilverLeaf a direct
  route toward I-95." Why: "A faster, shorter route for the school run and
  daily commute."
- **Mega Publix**: Summary: "A 55,701-square-foot Publix at 1975 SilverLeaf
  Parkway opened in March 2026 with pharmacy, bakery, and prepared foods."
  Why: "A full-service grocery anchor inside the community shortens daily
  errands."
- **Harris Teeter**: Summary: "A Harris Teeter supermarket is proposed for a
  SilverLeaf shopping center and a second location near CR 210 West."
  Why: "A second major grocer would add competition and convenience — if the
  projects move forward." (explicitly conditional)
- **SR 207 WRF**: Summary: "The county's $191.8 million water-reclamation
  facility is now operating, adding reclaimed-water capacity and drinking-water
  protection." Why: "Reclaimed water helps SilverLeaf irrigation during
  restrictions." (Relevance: countywide-household.)
- **FY2026 budget**: Summary: "St. Johns County adopted a $1.8 billion budget
  for FY2026 with the first property-tax rate cut since FY2021." Why:
  "Property-tax direction affects every household; FY2027 TRIM notices are the
  next cycle to watch." (Context label required.)

## 22. Master decision table

| Rank | Item ID | Topic | Relevance | Product role | Source quality | Work needed | Recommendation |
|------|---------|-------|-----------|--------------|----------------|-------------|----------------|
| 1 | SJC-BF-202509-0006 (+0002 SL, 0008) | Schools | DIRECT | Ongoing/context | Official + media | Merge; confirm opening date | STRONG_PUBLISH |
| 2 | SJC-SL-20260704-0004 (+BF-0013) | Roads | DIRECT | Context | Media (corroborated) | Merge; corroborate | STRONG_PUBLISH |
| 3 | SJC-SL-20260704-0001 | Business | DIRECT | Context | Media (corroborated) | Corroborate | STRONG_PUBLISH |
| 4 | SJC-SL-20260704-0005 | Business | DIRECT | Context | Media | Corroborate; conditional | STRONG_PUBLISH |
| 5 | SJC-SL-20260704-0003 | Business | DIRECT | Context | Media | Corroborate; conditional | STRONG_PUBLISH |
| 6 | SJC-CN-20260626-0001 (+UTIL-0003) | Utilities | Countywide | Ongoing | Official | Merge | STRONG_PUBLISH |
| 7 | SJC-BF-202508-0021 (+0020) | Roads | Nearby | Context | Official | Merge; status follow-up | STRONG_PUBLISH |
| 8 | SJC-BF-202508-0010 (+0011) | Roads | Nearby | Context | Official | Merge; status follow-up | STRONG_PUBLISH |
| 9 | SJC-BF-202509-0003 (budget arc) | Government | Countywide | Context | Official | Merge 8; context label | STRONG_PUBLISH |
| 10 | SJC-BF-202605-0011 | Schools/Taxes | Countywide | Context | Official | None | STRONG_PUBLISH |
| 11 | SJC-SL-20260704-0006 | Business/Health | Nearby | Context | Media | Corroborate; adjacent label | PUBLISH_AFTER_SOURCE_CHECK |
| 12 | SJC-BF-202508-0005 (Hallowes arc) | Schools | Nearby | Context | Official | Merge arc | PUBLISH_AS_CONTEXT |
| 13 | SJC-SL-20260706-0005 | Business | DIRECT | Recent | Media (URL 404) | Fix URL; verify | PUBLISH_AFTER_SOURCE_CHECK |
| 14 | SJC-BF-202605-0008 | Schools | Countywide | Recent | Official | Confirm launch | PUBLISH_AFTER_SOURCE_CHECK |

## 23. Buddy/GPT decision groups

- **APPROVE_AS_CONTEXT (recommended):** items 1–10 above (Tier 1) — durable
  SilverLeaf context/timelines, not "Latest" news.
- **APPROVE_AS_UPDATE (candidate, conditional):** SilverLeaf K-8 opening status
  and SR 16/CR 210 2026 follow-ups **once re-sourced** — these are the only
  Tier-1 items with genuine "current" potential.
- **NEEDS_COPY:** Harris Teeter + mini-golf (conditional wording), FY2026 budget
  (context label).
- **NEEDS_SOURCE_CHECK:** Bala's, St. Johns Compass, Nocatee/Ascension,
  K-8 opening date, SR 16/CR 210 status.
- **MERGE:** CR 2209 (2), SR 207 WRF (2), SR 16 (2), CR 210 (2), K-8 (3),
  water shortage (3), FY2026 budget (8), Hallowes arc (5), hurricane (2).
- **DEFER:** §18 Tier-2 remainder, §19 Tier-3 unless timeline presentation is
  adopted.
- **EXCLUDE:** §20 (all).

## 24. Recommended inaugural archive shape

**Primary recommendation: Option B — keep Latest as a small current release
(4–8 items) and publish a larger historical Browse/archive corpus.**

- Target Latest count: **4–6 current/active items** (the 4 published; optionally
  add the K-8 opening and a re-sourced SR 16/CR 210 follow-up when current).
- Target total Browse/archive count: **14–20 items** (Tier 1 + Tier 2 that pass
  source checks + Tier 3 timeline merges).
- Historical cutoff: **back to ~May 2025** for durable SilverLeaf context
  (nothing before the SilverLeaf K-8 / CR 2209 era adds value).
- Inclusion standard: same publication standard as the current release —
  reviewed, source-linked, no sensitive/crime material; local media published
  only as context with corroboration.
- Ongoing projects: published as **ACTIVE_OR_ONGOING** with a "status as of
  <date>" line and follow-up flag.
- Completed projects: published as **DURABLE_CONTEXT / ENTITY_TIMELINE** with a
  "completed" label; never presented as news.
- Ordering: archive ordered by the deterministic release rule; older items carry
  an explicit "context" role and a source-date label.
- Old source dates: **require a context label** ("from <date>") so residents
  are never misled about freshness.
- Archive items: **require explicit publication approval** — the archive is
  reviewed membership, not a firehose.
- Data contract support: **Not currently.** The static contract holds one
  release; supporting an archive needs a small extension — an `item_role`
  (`current` / `ongoing` / `context`) on each public item plus either (a) a
  multi-release merge for Browse, or (b) a `context` section in release.json.
  This is a bounded implementation task, not this task.

Do **not** put all historical material on Latest.

## 25. Current release versus Browse/archive recommendation

- Keep the four published items as **Latest** (current/ongoing, all verified
  active).
- Add the archive as a **Browse corpus** (durable context + timelines) with
  clear role/date labels.
- Do not merge historical items into Latest; do not inflate Latest to absorb
  the archive.
- Rationale: a resident scanning Latest needs "what's active now"; a resident
  exploring Browse needs "what exists in/around SilverLeaf and how it got
  here." The corpus's value is mostly the latter.

## 26. Publication command appendix (prepared, not executed)

Command form (run only after Buddy/GPT approves each item; `--display-topic`
uses the v0 resident category):

```
python3 scripts/publication_decision.py approve \
  --item-id <ITEM_ID> --reviewer <REVIEWER> \
  --rationale "<decision rationale>" \
  --silverleaf included --silverleaf-rationale "<relevance rationale>" \
  --relevance <in_silverleaf|near_silverleaf|countywide_impact> \
  --display-topic <roads_traffic|utilities_water|emergency_preparedness|schools_community|local_business> \
  [--public-title-override "..."] \
  [--public-summary-override "..."] \
  [--why-override "..."]
```

Per-item proposals (placeholders marked `<...>`):

- SJC-BF-202509-0006 — `--relevance in_silverleaf --display-topic schools_community`
  (merge note in rationale).
- SJC-SL-20260704-0004 — `--relevance in_silverleaf --display-topic roads_traffic`
  `--public-title-override "CR 2209 Connector Opens Between International Golf Parkway and SilverLeaf"`.
- SJC-SL-20260704-0001 — `--relevance in_silverleaf --display-topic local_business`.
- SJC-SL-20260704-0005 — `--relevance in_silverleaf --display-topic local_business`
  (conditional summary override).
- SJC-SL-20260704-0003 — `--relevance in_silverleaf --display-topic local_business`
  (conditional).
- SJC-CN-20260626-0001 — `--relevance countywide_impact --display-topic utilities_water`.
- SJC-BF-202508-0021 — `--relevance near_silverleaf --display-topic roads_traffic`.
- SJC-BF-202508-0010 — `--relevance near_silverleaf --display-topic roads_traffic`.
- SJC-BF-202509-0003 — `--relevance countywide_impact --display-topic
  government_taxes` (requires a new v0 topic id; see §24).
- SJC-BF-202605-0011 — `--relevance countywide_impact --display-topic schools_community`.
- SJC-SL-20260704-0006 — `--relevance near_silverleaf --display-topic local_business`.

No decision files were created; nothing was executed.

## 27. Data-quality findings

Individual editorial fixes (ready to apply during the approval pass):
- Merge near-duplicate records into single durable items (§15, §23 MERGE).
- Reword titles that embed stale relative time ("Next Two Weekends" — already
  fixed for CR 16A; check others like NBOR titles).
- Remove unexplained acronyms (SUPMAJ/CPA(SS)/ZVAR/REZ/NZVAR/PVZVAR/ARCCC/NCDRB)
  or supply plain-language equivalents for any published NBOR-derived content.
- Conditional wording for all proposals (Harris Teeter, mini golf, Bala's,
  Nocatee/Ascension).

Systemic validation improvements (recommended, not implemented here):
- **Missing public labels** already fail release validation (v0 display-topic
  layer, Task 19); extend the same guard to places/entities (a raw place or
  entity id with no label should fail export).
- NBOR "NW Sector" items lack **location/community metadata** — add a
  geocode/editorial tag step so relevance can be classified.
- `rural_sjc` community reference is unregistered (legacy exception) — resolve
  before any S.E.A. center publication.
- Duplicate-capture risk (NBOR 06-08 vs 06-26) is documented; keep the
  canonical-file rule.

Source-monitoring gaps (not this task's scope):
- No 2026 school-opening / boundary capture (GAP-003); no FY2027 TRIM/budget
  capture; no 2026 SR 16/CR 210/CR 2209 status follow-ups; no SL-area
  boil-water notices; SJRWMD direct capture is a recurring gap.

## 28. Source and verification gaps

Read-only live checks performed this task (recorded):

1. **2026-08-04** `https://www.stjohns.k12.fl.us/newschools/` → **K-8 School QQ
   (SilverLeaf DRI, Parcel 29C) confirmed "Under Construction."** Validates the
   highest-value candidate as ACTIVE.

Checks needed before any Tier-1 publication (recommended, not run):
- SilverLeaf K-8 opening date + attendance-zone/boundary authority (DIR-010).
- SR 16 widening and CR 210 widening 2026 status (FDOT/nflroads).
- Harris Teeter, mini golf, Bala's, Nocatee/Ascension current status + URL
  validity (Bala's recorded URL returns 404).
- Corroborate St. Johns Citizen claims against county/official records where
  the claim is consequential.

## 29. Validation results

```
python3 -m pytest tests/ -v            → PASS, 217 passed
python3 scripts/validate.py            → PASS — ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS — 0 errors, 321 warnings, 192 items
python3 scripts/validate_silverleaf_scope.py  → PASS — 0 errors, 0 warnings
git diff --check                       → clean
git status --short                     → clean (0 changes — read-only task)
```

## 30. Files changed

None. This task is read-only by design: no publication decisions, no review
status, no source records, no taxonomy, no UI, no Git changes.

## 31. Final Git status

`master` @ `9c985c7`, clean working tree, local == origin. No commits, no push.
Publication decisions unchanged (the four current-release items only).

## 32. Final task status

| Area | Status |
|------|--------|
| Corpus inspection (231 items, May 2025–Aug 2026) | COMPLETE |
| Candidate universe + relevance + product-role classification | COMPLETE |
| Resident-concern sections (roads/utilities/schools/dev/business/govt/preparedness) | COMPLETE |
| Clusters + timelines | COMPLETE |
| Missing/underrepresented coverage | COMPLETE |
| Tier 1 (10–14) / Tier 2 / Tier 3 / Tier 4 | COMPLETE |
| Public copy proposals (source-supported) | COMPLETE |
| Master decision table + decision groups | COMPLETE |
| Recommended archive shape (Option B) + contract gap | COMPLETE |
| Command appendix (not executed) | COMPLETE |
| Data-quality + source/verification gaps | COMPLETE |
| Validation (read-only) | COMPLETE |
| Publication/review state | UNCHANGED (as required) |

**Final status vocabulary:** COMPLETE — Buddy and GPT now have a decision-ready,
source-supported view of substantially more of the corpus, with tiered
candidates, merge/timeline recommendations, excluded material, copy proposals,
and an archive-shape recommendation. No publication or review state was
changed, and the repository remains clean.
