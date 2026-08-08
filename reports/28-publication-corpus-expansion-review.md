# Task 28 — Publication Corpus Expansion Review

**Task identity:** 28-publication-corpus-expansion-review.md
**Date:** 2026-08-07
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Mode:** supervised
**Final status:** COMPLETE — read-only editorial assessment

**Scope honored:** no publication policy, publication decisions, review status,
source records, taxonomy, site output, deployment state, scheduler state, Git
history, Ivy, or PostgreSQL state was changed. No commit or push. Bounded live
source checks were performed and are recorded separately in §34.

---

## 1. Executive result

The current seven-item SilverLeaf Brief is sparse **not because the corpus is
empty, but because most resident-relevant material never reaches the public
classifier, and most of what does reach it is blocked by un-reviewed data state
rather than by weak evidence.**

Three distinct causes, in order of magnitude:

1. **Pipeline invisibility (dominant cause).** The entire August–September 2025
   and May 2026 backfill corpus (`SJC-BF-*`, including the county's own CR 2209
   construction, SR 16 widening, CR 210 widening, K-8 school construction,
   school naming, attendance zoning, FY2026 budget, and hurricane-preparedness
   records) lives under `data/monthly/`, which the publication classifier's
   item iterator never reads. **Zero** `SJC-BF-*` items appear in the 167-item
   classifier input. They are not "blocked by policy" — they are invisible to it.
2. **Un-reviewed data state.** All 11 SilverLeaf-discovery records
   (`SJC-SL-*`, the mega Publix, Harris Teeter, mini golf, CR 2209 opening,
   K-8 school, Bala's) are `pending_review`, so the classifier returns
   `NEEDS_MORE_RESEARCH (review_status:pending_review)` before any substantive
   policy judgment. Baptist SilverLeaf and Magnolia Oaks have **no corpus item
   at all** — they exist only as accepted adaptive-state subjects and live RSS
   leads.
3. **A real but secondary policy restriction.** The `local_media` source-type
   rule and the stale-timely (30-day) rule would suppress the local-media
   records even after verification, and the classifier cannot express a
   "qualified context" category for a project like the possible-Harris-Teeter
   center.

The evidence quality is largely **good**. Live source checks confirmed: Magnolia
Oaks Academy (School QQ → SilverLeaf K-8 → Magnolia Oaks) opened/opening for
2026-27; Baptist SilverLeaf outpatient campus opened June 23, 2026; the Publix
at Silverleaf Market opened March 26, 2026 (multi-source corroborated); the
SilverLeaf grocery center is under county review with Harris Teeter
**unconfirmed**; First Coast Expressway final phase is in St. Johns County
hearings with full completion targeted 2030; CR 210 widening opened ahead of
the 2026 school year.

Under a reasonably permissive but still credible resident-publication model
(**Model B**), the corpus supports approximately **38–44 published items**
(Latest + Browse/context + timelines) across every category the site exposes —
enough that category browsing becomes genuinely useful. The current policy
produces 7. The gap is therefore mostly pipeline + review-state debt, not a
"weak evidence" problem.

---

## 2. Starting Git and repository state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` |
| HEAD commit | `fix: isolate research escalation test state` (2026-08-07 02:40 -0400) |
| Working tree | Not clean — Task 27 artifacts uncommitted (docs/PUBLICATION_POLICY.md, scripts/publication_policy.py, reports/27, site/data/releases/SJC-REL-2026-08-002/, briefs, modified docs/site/scripts/tests) |
| Publication decisions | 4 approved (`SJC-CN-20260802-0001`, `SJC-EM-20260626-0001`, `SJC-UTIL-20260603-0001`, `SJC-UTIL-20260603-0005`) + `legacy_exceptions.yaml` |
| Current public release | `SJC-REL-2026-08-002` (7 items, 16 routes), local-only; deployed site is `SJC-REL-2026-08-001` (4 items) at https://wgudataninja.github.io/sjc-intel/ |
| Adaptive state | 6 accepted entities, 4 lanes, 6 search profiles, 2 timelines, 0 pending proposals |

No changes were made to any of this by Task 28.

---

## 3. Corpus inspected

| Area | Location | What was reviewed |
|------|----------|-------------------|
| Intel items | `data/intel_items/2026-06-03`, `06-08`, `06-26`, `07-04`, `07-06`, `08-02` | county news, utility, NBOR, SJSO, emergency mgmt, BCC, CDD, silverleaf discovery, agentic search |
| Review queue | `data/review_queue/queue.yaml`, `summary.yaml` | 167 entries, 77 pending / 83 verified, prioritization, entity matches |
| Publication decisions | `data/publication_decisions/` | 4 approved + legacy exceptions |
| Monthly backfill | `data/monthly/2025-08/`, `2025-09/`, `2026-05/`, `2026-06/`, `2026-07/` | 48 + 21 + 21 backfill records and wraps — **not readable by the classifier** |
| Search runs | `data/search_runs/2026-07-06/` | SilverLeaf discovery run |
| Source events | `data/source_events/` | fetch/meeting containers |
| Adaptive discovery | `data/adaptive_discovery/` | accepted_state, coverage_health, research_resolutions |
| Registry | `registry/` | sources, tracked_entities, silverleaf_scope, communities, interest filters |
| Site | `site/data/releases/SJC-REL-2026-08-001|002/`, `site/build.json` | current published membership and routes |

**Count of records the classifier actually sees:** `iter_intel_items` yields
**192** records; after canonical-ID dedupe the selector classifies **167**
(`AUTO_PUBLISHABLE 7`, `NEEDS_HUMAN_REVIEW 51`, `NEEDS_MORE_RESEARCH 69`,
`EXCLUDE 40`). **The ~70-item monthly backfill corpus is entirely outside this
set** (verified programmatically: `0` of the `SJC-BF-*` IDs appear in
`iter_intel_items`).

---

## 4. Total resident-relevant universe

Starting from the actual corpus (not the classifier), asking "would a SilverLeaf
resident reasonably want to know this?", the plausible publication universe is
**~62 records across ~14 subjects**, of which ~40 are credible publishable
candidates under a less conservative standard:

| Category | Candidate items | Strong publishable | Subject strength |
|---|---|---:|---:|
| Schools & Families | 13 | 9 | Very strong |
| Roads & Mobility | 12 | 9 | Very strong |
| Growth & Construction (cross-cut) | 8 | 6 | Strong |
| Retail & Amenities | 6 | 6 | Strong |
| Healthcare & Services | 2 | 2 | Strong (under-covered) |
| Utilities & Water | 12 | 6 | Strong |
| Development & Zoning | 6 | 3 | Moderate |
| Government / community services | 9 | 1 | Weak |
| Preparedness | 3 | 2 | Moderate |

The excluded remainder is: crime/public-safety (sensitivity), NBOR ROW utility
permits and non-SilverLeaf rezonings (boilerplate/no local scope), coastal /
St. Augustine / Ponte Vedra items (not SilverLeaf access/corridor), CDD agenda
items, BCC boilerplate resolutions, library/awards/auction promos, and stale
event-only notices.

---

## 5. Current publication-policy inventory

Authoritative policy is `docs/PUBLICATION_POLICY.md`; deterministic classifier
`scripts/publication_policy.py`; selector `scripts/select_publication_items.py`.

| Classification | Count | Meaning |
|---|---|---:|
| `AUTO_PUBLISHABLE` | 7 | verified official resident-relevant low-sensitivity |
| `NEEDS_HUMAN_REVIEW` | 51 | sensitive, media-only, stale-timely, agenda needs concrete scope, missing resident scope |
| `NEEDS_MORE_RESEARCH` | 69 | `pending_review`, unknown source, missing URL, weak verification |
| `EXCLUDE` | 40 | rejected/duplicate/archived/legacy/crime |

Key rules that shape the outcome (from `publication_policy.py`):
- `review_status != verified` → `NEEDS_MORE_RESEARCH`.
- `source_type` not in `{wordpress_blog, official_records, government_meeting,
  rss, government_website, government_portal}` → `NEEDS_HUMAN_REVIEW`
  (this excludes `local_media`).
- `urgency == timely` and item date > 30 days old → `NEEDS_HUMAN_REVIEW`
  (`timely_item_stale_needs_context_review`).
- Sensitivity keywords / medium-high sensitivity / human-review flag →
  `NEEDS_HUMAN_REVIEW`.
- Missing resident scope (no silverleaf/corridor/countywide place, no tracked
  entity, no structured countywide-household explanation) →
  `NEEDS_HUMAN_REVIEW (missing_resident_scope)`.
- NBOR/BCC agenda items need a concrete local scope →
  `agenda_or_notice_needs_concrete_local_scope`.
- 60-day default release window filters older items at release build time even
  when classified.

---

## 6. Why the current site is sparse

The seven published items are all county utilities + one road closure + one
hurricane notice. The site's category layout is therefore 5× Utilities & Water,
1× Roads & Traffic, 1× Emergency Preparedness — **Schools & Community and
Local Business are empty**. Causes:

1. **Backfill corpus is outside the classifier input** (verified: `SJC-BF-*` →
   0 records in `iter_intel_items`). The county's own CR 2209, SR 16, CR 210,
   K-8 school, naming, zoning, budget, and preparedness items are the strongest
   resident material and never even get classified.
2. **SilverLeaf-discovery records are all `pending_review`** → `NEEDS_MORE_RESEARCH`
   before any source-type/sensitivity judgment. None have been reviewed since
   July 2026.
3. **Baptist SilverLeaf and Magnolia Oaks have no intel items** — they are
   adaptive-state subjects with RSS leads only. The most important 2026
   SilverLeaf health/school stories are absent from the corpus.
4. **Local-media rule would still block** the Publix/Harris-Teeter/mini-golf/
   CR-2209-opening records even after review, because `st_johns_citizen` is
   `local_media`.
5. **Stale-timely rule** would block the older school/road county items
   (Sep–Oct 2025) as "context needs review" even if they reached the classifier
   and were verified.

The report's core conclusion: the sparsity is caused by **pipeline and
review-state debt (approximately 70%)** plus **a policy posture tuned for
"fresh official news" (approximately 30%)** — not by weak source evidence.

---

## 7. Schools and Families

Resident question: *Which school do my kids attend, when does the new school
open, and does it relieve the commute?*

| Item | Date | Source | Status | Evidence | Recommended treatment |
|------|------|--------|--------|----------|------------------------|
| SJC-SL-20260704-0002 SilverLeaf K-8 topping-out | 2025-05-07 | St. Johns Citizen | pending | strong | MERGE into Magnolia Oaks timeline |
| SJC-BF-202509-0006 K-8 QQ/RR construction update | 2025-09-15 | SJCSD | pending (invisible) | strong | MERGE; VERIFY_THEN_PUBLISH |
| SJC-BF-202509-0008 naming/mascot engagement | 2025-09-25 | SJCSD | pending (invisible) | strong | MERGE timeline |
| SJC-BF-202509-0007 enrollment/capacity | 2025-09-15 | SJCSD | pending (invisible) | medium | DEFER / context |
| SJC-BF-202508-0005 Hallowes Cove opens | 2025-08-11 | SJCSD | pending (invisible) | strong | PUBLISH_AS_CONTEXT |
| SJC-BF-202508-0006/0007/0008 attendance zoning arc | 2025-08 | SJCSD | pending (invisible) | strong | PUBLISH_AS_TIMELINE (merge 3) |
| SJC-BF-202509-0005 Hallowes first students | 2025-09-01 | SJCSD | pending (invisible) | strong | PUBLISH_AS_CONTEXT |
| SJC-BF-202605-0008 St. Johns Compass (Aug 2026) | 2026-05-26 | SJCSD | pending (invisible) | strong | VERIFY_THEN_PUBLISH |
| SJC-BF-202605-0009 Programs of Choice | 2026-05-27 | SJCSD | pending (invisible) | medium | DEFER (deadline passed) |
| SJC-BF-202605-0011 half-cent surtax + one mill | 2026-05-18 | SJCSD | pending (invisible) | strong | PUBLISH_AS_CONTEXT |
| SJC-BF-202605-0013 'A' grade | 2026-05-21 | SJCSD | pending (invisible) | weak | DEFER |
| Live: Magnolia Oaks opens for 2026-27 | 2026-07-22 | News4JAX/ActionJax | lead | strong | VERIFY_THEN_PUBLISH (Latest) |
| Live: "Before the Roar" K-8 reveal | 2026-07-24 | St. Johns Citizen | lead | strong | source-check then Latest |
| Live: zoning changes 2026-27 | 2025-12-02 | St. Johns Citizen | lead | strong | VERIFY_THEN_PUBLISH |

**Why a resident cares:** the SilverLeaf K-8 / Magnolia Oaks opening and the
2026-27 attendance zoning directly determine daily school commutes and
enrollment; it is the single most neighborhood-specific story in the corpus.

---

## 8. Roads and Mobility

Resident question: *What are the access routes, what's closed, what's being
widened, and when does the commute improve?*

| Item | Date | Source | Status | Evidence | Recommended treatment |
|------|------|--------|--------|----------|------------------------|
| SJC-CN-20260802-0001 CR 16A closures | 2026-07-20 | County | verified | strong | **Already published** |
| SJC-BF-202508-0013 CR 2209 expansion underway | 2025-08-20 | County | pending (invisible) | strong | MERGE with CR 2209 opening |
| SJC-SL-20260704-0004 CR 2209 connector opened | 2025-10-28 | St. Johns Citizen | pending | strong | PUBLISH_AS_CONTEXT (merge) |
| SJC-BF-202508-0020 SR 16 widening hearings | 2025-08-22 | County/FDOT | pending (invisible) | strong | MERGE timeline |
| SJC-BF-202508-0021 SR 16/IGP groundbreaking | 2025-08-29 | County | pending (invisible) | strong | MERGE timeline |
| SJC-BF-202508-0010 CR 210 widening traffic shift | 2025-08-09 | County | pending (invisible) | strong | MERGE timeline |
| SJC-BF-202508-0011 Beachwalk alternate access | 2025-08-08 | County | pending (invisible) | medium | MERGE |
| SJC-BF-202509-0013 Four Mile Rd / SR 16 open house | 2025-09-26 | County | pending (invisible) | medium | DEFER |
| SJC-CN-20260626-0002 Railroad crossing (W King/Kinlaw) | 2026-06-22 | County | verified | weak-SL | EXCLUDE (St. Augustine) |
| Live: CR 210 widening open before school year | 2026-08 | News4JAX | lead | strong | VERIFY_THEN_PUBLISH (Latest) |
| Live: CR 210/CR 2209 intersection meetings | 2026-03-31 | Action News Jax | lead | strong | VERIFY_THEN_PUBLISH |
| Live: FCE final phase open house (St. Johns) | 2026-01-27 | JDR | lead | strong | VERIFY_THEN_PUBLISH (Browse) |
| Live: St. Johns Parkway detour for FCE work | current | Action News Jax | lead | medium | VERIFY_THEN_PUBLISH |
| Live: FCE full open targeted 2030 | current | Action News Jax | lead | strong | PUBLISH_AS_CONTEXT |

**Why a resident cares:** CR 2209, SR 16/IGP, CR 210, CR 16A, and the FCE/I-95
access are the household's commuting reality; CR 210 just opened ahead of the
school year and is currently unpublished.

---

## 9. Growth and Construction

Cross-cutting active-construction subjects (school, hospital, grocery, roads,
town center, expressway). Explicit subjects and status:

| Subject | Corpus items | Live-verified status | Treatment |
|---------|--------------|----------------------|-----------|
| Magnolia Oaks Academy (school) | 0 (leads only) | opening for 2026-27 | VERIFY_THEN_PUBLISH |
| Baptist SilverLeaf campus | 0 (leads only) | opened 2026-06-23 | VERIFY_THEN_PUBLISH (Latest) |
| Publix at Silverleaf Market | 1 (SJC-SL-20260704-0001) | opened 2026-03-26 | PUBLISH_AS_CONTEXT |
| SilverLeaf grocery center (HT?) | 1 (SJC-SL-20260704-0005) | under county review; tenant unconfirmed | PUBLISH_AS_CONTEXT (qualified) |
| 165-acre SilverLeaf town center | 0 (lead) | Publix is cornerstone (2025) | VERIFY_THEN_PUBLISH (context) |
| SilverLeaf Market outparcels | 0 (lead) | planning buildings (2026-08-06) | VERIFY_THEN_PUBLISH |
| First Coast Expressway | 0 (leads) | final phase hearings; 2030 target | VERIFY_THEN_PUBLISH |
| SR 207 Water Reclamation Facility | 2 (published) | operational | Already published |
| CR 2209 / SR 16 / CR 210 | 7 corpus | mixed | MERGE timelines |

The town-center, outparcel, FCE, Baptist, and Magnolia records are **pipeline
coverage failures** (see §37).

---

## 10. Retail and Amenities

| Item | Date | Source | Status | Treatment |
|------|------|--------|--------|-----------|
| SJC-SL-20260704-0001 mega Publix opened | 2026-03-26 | St. Johns Citizen | pending | PUBLISH_AS_CONTEXT |
| SJC-SL-20260704-0005 two new supermarkets (HT) | 2025-12-02 | St. Johns Citizen | pending | PUBLISH_AS_CONTEXT (qualified) |
| SJC-SL-20260704-0003 Beach Valley Mini Golf | 2026-04-08 | St. Johns Citizen | pending | PUBLISH_AS_CONTEXT (conditional) |
| SJC-SL-20260706-0005 Bala's second location | 2026-07 (URL 404) | St. Johns Citizen | pending | VERIFY_THEN_PUBLISH (fix URL) |
| SJC-SL-20260704-0006 Nocatee retail / Ascension | 2026-06-01 | St. Johns Citizen | pending | PUBLISH_AS_CONTEXT (adjacent) |
| Live: Fifth Third Bank at Publix center | 2025-10 / 2026-04 | JDR | lead | VERIFY_THEN_PUBLISH |
| Live: M Shack + Natural Greens join lineup | 2026-07-20 | Business Journals | lead | VERIFY_THEN_PUBLISH (Latest) |
| Live: New Dunkin' in SilverLeaf | 2026-03-06 | WhatNow | lead | VERIFY_THEN_PUBLISH |

**Why a resident cares:** grocery competition (Harris Teeter), the Publix
anchor, and new tenants are daily-life change. All must use conditional language
for unconfirmed tenants.

---

## 11. Healthcare and Services

| Item | Date | Source | Status | Treatment |
|------|------|--------|--------|-----------|
| Live: Baptist Health SilverLeaf outpatient campus opened | 2026-06-23 | News4JAX / Business Journals / JaxToday / JDR | lead | VERIFY_THEN_PUBLISH (Latest) |
| Live: Helipad addition approved | 2026-04-10 | JDR | lead | MERGE timeline |
| Live: $16.8M permit / construction | 2025-01 | Business Journals / JDR | lead | MERGE timeline |
| SJC-SL-20260704-0006 Ascension St. Vincent's Nocatee | 2026-06-01 | St. Johns Citizen | pending | PUBLISH_AS_CONTEXT (adjacent) |

**Why a resident cares:** Baptist is the first hospital-grade medical presence
in SilverLeaf; its emergency/outpatient opening is a top household question.
**Coverage gap:** the campus has no corpus item despite opening six weeks ago
(see §19).

---

## 12. Utilities and Water

| Item | Date | Source | Status | Treatment |
|------|------|--------|--------|-----------|
| SJC-UTIL-20260603-0001 Phase III water shortage | 2026-05-11 | County | verified | **Already published** |
| SJC-UTIL-20260603-0005 service-line inventory | — | County | verified | **Already published** |
| SJC-UTIL-20260603-0003 SR 207 WRF Phase 2 | 2025-12-19 | County | verified | **Already published** (merge with below) |
| SJC-UTIL-20260603-0004 utilities lab | — | County | verified | **Already published** |
| SJC-CN-20260626-0001 SR 207 WRF serving | 2026-06-23 | County | verified | **Already published** |
| SJC-UTIL-20260603-0002 chlorine burnout (Jun 1–21) | 2026-05-26 | County | verified | EXCLUDE (event over) |
| SJC-BF-202605-0005 SJRWMD one-day-per-week | 2026-05-11 | SJRWMD | pending (invisible) | MERGE into water shortage |
| SJC-BF-202605-0006 June chlorine burnout | 2026-05-26 | County | pending (invisible) | EXCLUDE (stale) |
| SJC-BF-202509-0012 manhole rehab | 2025-09-29 | County | pending (invisible) | DEFER |
| SJC-BF-202509-0014 raised pavement markers | 2025-09-29 | County | pending (invisible) | DEFER |
| SJC-UD-20260626-0001 2025 annual report | 2026-06-26 | County | pending | DEFER (low value) |
| Ponte Vedra / coastal / North Beach utility items | 2025 | County | pending | EXCLUDE (not SilverLeaf) |

**Why a resident cares:** irrigation restrictions and reclaimed water directly
control household landscaping; SR 207 WRF capacity underpins growth. Already
well published — this is the one category the current site does not underserve.

---

## 13. Development and Zoning

| Item | Date | Source | Treatment |
|------|------|--------|-----------|
| SJC-BF-202509-0015 impact fee updates | 2025-09-17 | County (invisible) | PUBLISH_AS_CONTEXT |
| SJC-BCC-20260120-0001 2050 Comp Plan transmittal | 2026-01-20 | BCC | DEFER (durable, generic) |
| SJC-NBOR-20260802-0002 Bartram Grove community meeting | 2026-07 | NBOR | DEFER (location is Racetrack Rd — not SilverLeaf) |
| SJC-NBOR-20260802-0007 Little Florence Fish Camp | 2026-07 | NBOR | DEFER (location unconfirmed) |
| SJC-NBOR-20260802-0013 Colee Cove Tower | 2026-08 | NBOR | DEFER (location unconfirmed) |
| SJC-NBOR-20260802-0001 Moseley Property CPA | 2026-08 | NBOR | DEFER (location unconfirmed) |
| SJC-NBOR-20260802-0003 Daily's Place CPA (withdrawn) | 2026-07 | NBOR/County | EXCLUDE (withdrawn) |

Only the impact-fee and 2050 Comp Plan items carry countywide-household value;
the NW-Sector NBOR items lack SilverLeaf-specific location evidence and remain
location-unconfirmed. No SilverLeaf zoning/PUD change is currently in the corpus
(see §22 for the town center / grocery center, which are the real zoning stories).

---

## 14. Government / community services

| Item | Date | Treatment |
|------|------|-----------|
| SJC-BF-202508-0001..0004 TRIM / tax roll / budget workbooks / calendar | 2025-08 | MERGE into FY2026 budget timeline |
| SJC-BF-202509-0001/0002/0003/0004 hearings / adoption / bills | 2025-09 | MERGE; PUBLISH_AS_CONTEXT (FY2026 label) |
| SJC-CN-20260802-0003 S.E.A. resource center | 2026-07 | DEFER (weak SilverLeaf link) |
| SJC-CN-20260802-0004 Clerk service center | 2026-07 | DEFER |
| SJC-BF-202509-0016 Hastings center/library | 2025-09 | DEFER |
| BCC January 2026 backfill (44 items) | 2026-01 | EXCLUDE (boilerplate) |

Only the FY2026 property-tax-reduction arc is publishable as durable context
(and it doubles as the FY2027 TRIM-season explainer). Everything else is
boilerplate or weak.

---

## 15. Preparedness

| Item | Date | Source | Treatment |
|------|------|--------|-----------|
| SJC-EM-20260626-0001 hurricane season prep | 2026-06-01 | County | **Already published** |
| SJC-BF-202605-0021 hurricane preparedness messaging | 2026-05-26 | County (invisible) | MERGE into published EM item |
| SJC-BF-202508-0022 Alert St. Johns | 2025-08-05 | County (invisible) | PUBLISH_AS_CONTEXT |

Durable preparedness is thin (two merges to one item) but adequate as context;
no live storm activity is current. This category should stay small and
publishable by default (already is).

---

## 16. Magnolia Oaks Academy — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| SJC-BF-202509-0006 K-8 QQ/RR construction update | 2025-09-15 | SJCSD | timeline |
| SJC-SL-20260704-0002 topping-out sneak peek | 2025-05-07 | St. Johns Citizen | timeline |
| SJC-BF-202509-0008 naming/mascot engagement | 2025-09-25 | SJCSD | timeline |
| Live: Magnolia Oaks Academy set to open in SilverLeaf 2026-27 | 2026-07-22 | News4JAX | Latest |
| Live: Action News Jax "prepares for first day" | 2026-07-22 | Action News Jax | Latest (dup) |
| Live: "Before the Roar" K-8 reveal | 2026-07-24 | St. Johns Citizen | Latest |
| Live: school site (stjohns.k12.fl.us) | current | SJCSD | authoritative |
| Live: 2026-27 zoning changes announced | 2025-12-02 | St. Johns Citizen | Latest/Browse |
| Adaptive state: identity chain School QQ → SilverLeaf K-8 → Magnolia Oaks | 2026-08 | accepted timeline | canonical |

- **Chronology:** School QQ planning/construction (2025) → topping-out (May
  2025) → naming/mascot engagement (Sep 2025) → district announces name
  "Magnolia Oaks Academy" (2026) → opening for 2026-27 (Aug 2026).
- **Strongest sources:** SJCSD official pages + News4JAX + Action News Jax
  (2026-07-22) + St. Johns Citizen (2026-07-24).
- **Current known state:** opening for 2026-27; attendance zone per 2026-27
  zoning announcement; ~1,500 students, 73 classrooms (K-8).
- **What could publish now:** a merged Magnolia Oaks item (opening + zoning)
  as Latest; timeline School QQ → SilverLeaf K-8 → Magnolia Oaks.
- **What should be merged:** SJC-SL-20260704-0002, SJC-BF-202509-0006,
  SJC-BF-202509-0008, plus the three live leads.
- **Requires one source check:** confirm opening date and final attendance-zone
  boundary from SJCSD (DIR-010 remains open).
- **Coverage gap:** no intel item captures the Magnolia Oaks name/opening
  (2026) — the accepted adaptive timeline exists but the corpus does not.

---

## 17. CR 2209 — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| SJC-BF-202508-0013 construction underway (Silverleaf Pkwy → SR 16) | 2025-08-20 | County | timeline |
| SJC-SL-20260704-0004 opened Oct 28, 2025 | 2025-10-28 | St. Johns Citizen | timeline |
| Live: CR 210/CR 2209 intersection meetings | 2026-03-31 | Action News Jax | follow-up |
| Live: "roadway project improves connectivity in SilverLeaf" | 2026-08-05 | Business Journals | follow-up |

- **Chronology:** construction began (Aug 2025) → opened (Oct 2025) → 2026
  intersection-meeting / connectivity follow-ups.
- **Current known state:** completed connector (IGP → SilverLeaf Parkway);
  county is still working adjacent intersections.
- **What could publish now:** merged "CR 2209 connector now open" context item.
- **Merge:** SJC-BF-202508-0013 + SJC-SL-20260704-0004.
- **Source check:** county public-works verification of opening date (registry
  notes it as unverified).
- **Coverage gap:** the two corpus records are the only ones; the 2026
  intersection work is lead-only.

---

## 18. First Coast Expressway / I-95 access — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| (none in corpus) | — | — | **pipeline gap** |
| Live: FDOT open house in St. Johns for final phase | 2026-01-27 | Jacksonville Daily Record | Latest/Browse |
| Live: St. Johns Parkway detour during FCE construction | current | Action News Jax | Latest |
| Live: "new toll road through north St. Johns County expected to spur development" | current | Business Journals | context |
| Live: FCE still on track to fully open 2030 | current | Action News Jax | context |

- **Chronology:** construction through Clay/St. Johns → St. Johns final phase
  public meetings (2026) → target full opening 2030.
- **Current known state:** final phase in St. Johns County; full completion
  targeted 2030; the expressway will provide SilverLeaf's I-95 alternative
  access.
- **What could publish now:** one qualified FCE item ("final phase; targeted
  2030") as Browse/context, with the St. Johns Parkway detour as the current
  detail.
- **Source check:** FDOT / nflroads for segment status and completion date.
- **Coverage gap:** **zero** corpus items — this is a top pipeline failure given
  it is an accepted search profile (`LIVE-55b639933dba`) and a deferred timeline.

---

## 19. Baptist SilverLeaf campus — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| (none in corpus) | — | — | **pipeline gap** |
| Live: plans under review | 2024-07-26 | JDR / JaxToday | timeline |
| Live: $16.8M permit issued | 2025-01-16 | Business Journals / JDR | timeline |
| Live: more permits | 2025-01-24 | JDR | timeline |
| Live: helipad addition approved | 2026-04-10 | JDR | timeline |
| Live: first phase opened June 23, 2026 | 2026-06-22 | News4JAX / Business Journals / JaxToday / JDR | **Latest** |

- **Chronology:** under review (Jul 2024) → permitted ($16.8M, Jan 2025) →
  construction → helipad approved (Apr 2026) → **opened Jun 23, 2026**.
- **Current known state:** outpatient medical campus open; helipad approved.
- **What could publish now:** "Baptist SilverLeaf outpatient campus is open"
  (Latest) with a construction timeline.
- **Merge:** all four leads into one campus timeline.
- **Source check:** baptistjax.com facility page for services list.
- **Coverage gap:** **zero** corpus items despite opening six weeks ago — a
  clear pipeline failure (accepted entity `LIVE-476ade9e84c0`, no intel item).

---

## 20. Publix / Silverleaf Market — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| SJC-SL-20260704-0001 "mega Publix" first look | 2026-03-26 | St. Johns Citizen | context |
| Live: Publix corporate "opens new store in St. Augustine" | 2026-03-26 | Publix | corroboration |
| Live: "Florida's largest Publix" / "largest in NE FL" | 2026-03-26 | Business Journals / JDR | corroboration |
| Live: News4JAX wine bar / deli details | 2026-03-20 | News4JAX | corroboration |
| Live: permitted (Mar 2025), green light (Apr 2025), under construction (Feb 2026) | 2025–2026 | JDR / News4JAX | timeline |
| Live: SilverLeaf Market planning outparcel buildings | 2026-08-06 | JDR | Latest/Browse |
| Live: Fifth Third Bank planned at Publix-anchored center | 2025-10 / 2026-04 | JDR | Latest/Browse |
| Live: M Shack + Natural Greens join lineup | 2026-07-20 | Business Journals | Latest |
| Live: New Dunkin' | 2026-03-06 | WhatNow | Latest |

- **Chronology:** grocery-anchored center planned (2024) → Publix permitted
  (Mar 2025) → under construction (Feb 2026) → **opened Mar 26, 2026** →
  tenants (2026).
- **Current known state:** open; "Silverleaf Market" is the Publix-anchored
  center; outparcels and additional tenants (M Shack, Natural Greens, Fifth
  Third, Dunkin') in planning/opening.
- **What could publish now:** merged Publix context item + a "Silverleaf Market
  grows" Browse item; tenant news can be Latest.
- **Source check:** Publix corporate + JDR corroborate the single media item
  (resolves the "media-only" concern).
- **Coverage gap:** all tenant/outparcel detail is lead-only (none in corpus).

---

## 21. SilverLeaf grocery center — possible Harris Teeter — complete item set

| Item / lead | Date | Source | Role |
|-------------|------|--------|------|
| SJC-SL-20260704-0005 two 61k sq ft supermarkets proposed | 2025-12-02 | St. Johns Citizen | context |
| Live: "Another Harris Teeter-size grocery store proposed" | 2026-05-15 | Jacksonville Daily Record | corroboration |
| Adaptive: ACCEPT_QUALIFIED resolution (confidence 0.6) | 2026-08-07 | research escalation | identity ruling |
| Adaptive: accepted timeline (uncertainty-preserving) | 2026-08-07 | — | canonical |

- **Chronology:** Dec 2025 proposal → 2026 county review → May 2026 "another
  Harris-Teeter-size store" report.
- **Current known state:** grocery-anchored center at CR 16A / SilverLeaf
  Parkway under county review; footprint matches a Harris Teeter prototype;
  **tenant NOT confirmed** by any first-party source.
- **What could publish now:** a qualified context item with the uncertainty
  language from the accepted adaptive timeline. Never state "Harris Teeter
  confirmed."
- **Merge:** SJC-SL-20260704-0005 + the two JDR leads + tracked entity
  `ENT-RETAIL-CR16A-SL-PKWY-GROCERY`.
- **Source check:** continuing (next search cycle); harristeeter.com remains
  non-confirmatory.
- **Coverage gap:** no 2026 intel item captures the May 2026 JDR reaffirmation.

---

## 22. Other major construction subjects

| Subject | Corpus items | Live leads | Assessment |
|---------|--------------|------------|------------|
| 165-acre SilverLeaf "town center" | 0 | Business Journals (Mar 2025) | coverage failure |
| SilverLeaf Market outparcels | 0 | JDR (Aug 2026) | coverage failure |
| Fifth Third Bank / M Shack / Natural Greens / Dunkin' | 0 | JDR / Business Journals / WhatNow | coverage failure |
| CR 210 widening completion | 2 (2025 shift) | News4JAX (Aug 2026 opening) | coverage failure (no completion item) |
| SR 16 / IGP widening | 2 (2025) | — | coverage failure (no 2026 follow-up) |
| SR 207 WRF | 2 | — | **well covered (published)** |
| Phase III water shortage | 2 + SJRWMD | — | **well covered (published)** |

The county's FY2026-budget and school-arc subjects are well covered in the
backfill but invisible to the pipeline. The outstanding gap is **active
commercial construction and completed-road milestones during 2026**.

---

## 23. Current-policy blockers

For every high-value record currently `NEEDS_HUMAN_REVIEW` or
`NEEDS_MORE_RESEARCH`, with the concrete blocker classified:

| Item | Current classification | Exact reason | Blocker class |
|------|------------------------|--------------|---------------|
| SJC-SL-20260704-0001 (Publix) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_SIMPLE_SOURCE_CHECK |
| SJC-SL-20260704-0002 (K-8) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_ENTITY_CANONICALIZATION |
| SJC-SL-20260704-0003 (mini golf) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_SIMPLE_SOURCE_CHECK |
| SJC-SL-20260704-0004 (CR 2209) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_TIMELINE_MERGE |
| SJC-SL-20260704-0005 (HT) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_COPY_QUALIFICATION |
| SJC-SL-20260704-0006 (Nocatee) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_LOCATION_CONFIRMATION |
| SJC-SL-20260706-0005 (Bala's) | NEEDS_MORE_RESEARCH | `review_status:pending_review` | NEEDS_SIMPLE_SOURCE_CHECK |
| SJC-SL-20260706-0001/-0002/-0004 | NEEDS_MORE_RESEARCH | pending + sensitivity | LEGITIMATE_SAFETY_GATE |
| SJC-BF-202508-0013 (CR 2209) | not classified | never reaches classifier | PIPELINE (invisible) |
| SJC-BF-202509-0006 (K-8) | not classified | never reaches classifier | PIPELINE (invisible) |
| SJC-BF-202508-0020/-0021 (SR 16) | not classified | never reaches classifier | PIPELINE (invisible) |
| SJC-BF-202508-0010/-0011 (CR 210) | not classified | never reaches classifier | PIPELINE (invisible) |
| SJC-BF-202509-0003 (budget) | not classified | never reaches classifier | PIPELINE (invisible) |
| SJC-BF-202605-0005/-0021 etc. | not classified | never reaches classifier | PIPELINE (invisible) |

(Blocker classes beyond the enumerated vocabulary: "PIPELINE (invisible)" is
used to record that these items do not enter the classifier at all.)

**Central output:** the sparse site is caused by **pipeline + review-state
debt**, not by weak evidence. Only the SJC-SL-20260706 crime/minor items are
blocked by a legitimate safety gate.

---

## 24. Policy false negatives

Strong items the current policy/pipeline blocks but that should reasonably
appear publicly:

| Item | Current classification | Why blocked | Why it should publish | Minimum fix |
|------|------------------------|-------------|------------------------|-------------|
| SJC-SL-20260704-0001 (Publix) | NEEDS_MORE_RESEARCH | pending + media-only | corroborated by Publix corporate + 4 outlets | SOURCE_CHECK + COPY |
| SJC-SL-20260704-0005 (HT center) | NEEDS_MORE_RESEARCH | pending + media + unconfirmed | confirmed project, tenant unconfirmed — publishable qualified | ENTITY_CANONICALIZATION + COPY_QUALIFICATION |
| SJC-SL-20260704-0003 (mini golf) | NEEDS_MORE_RESEARCH | pending + media | real DRC proposal on 2 acres | SOURCE_CHECK |
| SJC-SL-20260704-0004 (CR 2209) | NEEDS_MORE_RESEARCH | pending + media | completed route; county item corroborates | SOURCE_CHECK + TIMELINE_MERGE |
| SJC-SL-20260704-0002 (K-8) | NEEDS_MORE_RESEARCH | pending + media | identity of Magnolia Oaks | ENTITY_CANONICALIZATION + TIMELINE_MERGE |
| SJC-BF-202509-0006 (K-8 build) | invisible | backfill path | SJCSD official; top SL school story | PIPELINE (import) + SOURCE_CHECK |
| SJC-BF-202508-0013 (CR 2209) | invisible | backfill path | county official | PIPELINE (import) |
| SJC-BF-202508-0020/-0021 (SR 16) | invisible | backfill path | FDOT/county official | PIPELINE (import) |
| SJC-BF-202508-0010/-0011 (CR 210) | invisible | backfill path | county official | PIPELINE (import) |
| SJC-BF-202509-0003 (FY2026 budget) | invisible | backfill path | first tax-rate cut since FY2021 | PIPELINE (import) + HISTORICAL_CONTEXT_LABEL |
| SJC-BF-202605-0011 (surtax/one mill) | invisible | backfill path | explains school funding | PIPELINE (import) |
| Baptist campus (opened 6/23) | no item | never captured | hospital-grade care opened | SOURCE_CHECK (create item) |
| Magnolia Oaks opening | no item | never captured | top school story | SOURCE_CHECK (create item) |

**Answer to the governing question:** the block is ~70% pipeline/review-state
debt and ~30% policy posture. A small set of source checks + review actions
plus one data-import path unlocks most of Model B.

---

## 25. Genuine safety / exclusion cases

| Item | Reason excluded | Safety/editorial rationale |
|------|-----------------|----------------------------|
| SJC-SL-20260706-0001 ICE detainer | crime/legal, named individuals | LEGITIMATE_SAFETY_GATE |
| SJC-SL-20260706-0002 construction-site shooting | crime, fatality | LEGITIMATE_SAFETY_GATE |
| SJC-SL-20260706-0004 airlifted minor | minors | LEGITIMATE_SAFETY_GATE |
| SJC-SL-20260706-0003 lightning strike | unverified, low value | DEFER (not a safety gate — low value) |
| SJC-SJSO-* (6) + SJC-BF-202605-0019 | crime/arrest | LEGITIMATE_SAFETY_GATE |
| NBOR ROW utility permits (~40) | boilerplate, no local scope | NOT resident-relevant |
| NBOR non-SilverLeaf rezonings (St. Aug/coastal) | no SilverLeaf signal | NOT resident-relevant |
| BCC Jan 2026 backfill (~40/44) | boilerplate | NOT resident-relevant |
| CDD agenda/minutes (9) | not SilverLeaf-governed | NOT resident-relevant |
| Ponte Vedra/coastal utilities, boil notices | outside access/corridor | NOT resident-relevant |
| Chlorine burnout (event over) | expired | stale |
| Daily's CPA (withdrawn) | withdrawn | superseded |

No sensitive incident is recommended for auto-publication. This boundary is
preserved in every model.

---

## 26. Model A — current policy

| Category | Latest | Browse/context | Timeline/merged | Total |
|----------|-------:|---------------:|----------------:|------:|
| Schools & Families | 0 | 0 | 0 | 0 |
| Roads & Mobility | 1 (CR 16A) | 0 | 0 | 1 |
| Growth & Construction | 0 | 0 | 0 | 0 |
| Retail & Amenities | 0 | 0 | 0 | 0 |
| Healthcare & Services | 0 | 0 | 0 | 0 |
| Utilities & Water | 5 | 0 | 0 | 5 |
| Development & Zoning | 0 | 0 | 0 | 0 |
| Government/community | 0 | 0 | 0 | 0 |
| Preparedness | 1 (hurricane) | 0 | 0 | 1 |
| **Total** | **7** | **0** | **0** | **7** |

Site shape: 7 items / 16 routes; topic pages exist for Roads & Traffic,
Utilities & Water, Emergency Preparedness; **Schools & Community and Local
Business render empty**.

---

## 27. Model B — reasonably permissive resident publication

Standard: real public event/project/service/facility/business/school/road or
household condition; identifiable source; central facts reasonably supported;
material to a SilverLeaf resident; uncertainty representable; no meaningful
privacy/safety/defamation problem. Excludes crime, allegations, private material,
unsupported rumor, duplicates, and generic boilerplate.

| Category | Latest | Browse/context | Timeline/merged | Total |
|----------|-------:|---------------:|----------------:|------:|
| Schools & Families | 3 | 4 | 1 | 8 |
| Roads & Mobility | 2 | 4 | 2 | 8 |
| Growth & Construction | 2 | 4 | 2 | 8 |
| Retail & Amenities | 1 | 5 | 1 | 7 |
| Healthcare & Services | 1 | 2 | 1 | 4 |
| Utilities & Water | 3 | 3 | 1 | 7 |
| Development & Zoning | 0 | 2 | 0 | 2 |
| Government/community | 0 | 1 | 1 | 2 |
| Preparedness | 1 | 1 | 0 | 2 |
| **Total** | **13** | **26** | **9** | **48** |

(Across-category dedupe, e.g. Baptist counted once in Healthcare and once as
construction context, yields ~42 unique published items.)

---

## 28. Model C — broad archive

Adds nearly all source-backed SilverLeaf-relevant historical material even if
only Browse/context/timeline-worthy (whole FY2026 budget arc, full school
backfill, additional SJCSD programming, county capital projects, both CR 210 /
SR 16 timelines in full):

| Category | Latest | Browse/context | Timeline/merged | Total |
|----------|-------:|---------------:|----------------:|------:|
| Schools & Families | 3 | 6 | 2 | 11 |
| Roads & Mobility | 2 | 6 | 3 | 11 |
| Growth & Construction | 2 | 6 | 3 | 11 |
| Retail & Amenities | 1 | 6 | 1 | 8 |
| Healthcare & Services | 1 | 2 | 1 | 4 |
| Utilities & Water | 3 | 5 | 2 | 10 |
| Development & Zoning | 0 | 3 | 1 | 4 |
| Government/community | 0 | 4 | 2 | 6 |
| Preparedness | 1 | 2 | 0 | 3 |
| **Total** | **13** | **40** | **15** | **68** |

Model C is the "everything useful" ceiling; Model B is the recommended product
(§29–31).

---

## 29. Recommended Latest (Model B) — 13 items

Recommended 8–15 current/recent/still-active items. Not forced; 13 is supported.

| Title | Category | Date | Current state | Why it matters | Work needed |
|-------|----------|------|---------------|----------------|-------------|
| Magnolia Oaks Academy opens for 2026-27 (merged K-8 story) | Schools & Families | 2026-07-22 | opening imminent | top neighborhood school story | SOURCE_CHECK (opening date) + MERGE |
| St. Johns County announces 2026-27 school zoning changes | Schools & Families | 2025-12-02 | final | who goes where next year | SOURCE_CHECK + MERGE |
| St. Johns Compass launches for families (Aug 2026) | Schools & Families | 2026-05-26 | launching | new family resource | SOURCE_CHECK |
| County Road 16A weekend closures (existing) | Roads & Mobility | 2026-07-20 | active | SilverLeaf access road | none (published) |
| CR 210 widening opens ahead of school year | Roads & Mobility | 2026-08 | just completed | commute change | SOURCE_CHECK (county) |
| Baptist SilverLeaf outpatient campus is open | Healthcare & Services | 2026-06-23 | open | first hospital-grade care in community | SOURCE_CHECK (baptistjax) |
| Phase III water shortage still in effect (existing) | Utilities & Water | 2026-05-11 | active | irrigation law | none (published) |
| SR 207 Water Reclamation now serving (existing) | Utilities & Water | 2026-06-23 | operational | capacity + growth | none (published) |
| Water service-line material inventory (existing) | Utilities & Water | ongoing | active | EPA lead-safety program | none (published) |
| SilverLeaf Market grows: new tenants + outparcels | Retail & Amenities | 2026-08-06 | active | daily-life retail change | SOURCE_CHECK |
| M Shack and Natural Greens join SilverLeaf lineup | Retail & Amenities | 2026-07-20 | opening | restaurant options | SOURCE_CHECK |
| Hurricane season preparedness (existing) | Preparedness | 2026-06-01 | active | seasonal | none (published) |
| Utilities lab ribbon-cutting (existing) | Utilities & Water | 2026-06 | completed | water testing capability | none (published) |

(Removing the low-value utilities-lab and merging SR 207 WRF duplicate yields
a tight 11–13; the exact membership is editorial.)

---

## 30. Recommended Browse corpus (Model B) — grouped by category

**Schools & Families (4–5)**
- Magnolia Oaks construction timeline (School QQ → SilverLeaf K-8 → Magnolia Oaks → opening)
- Hallowes Cove Academy opened + first students (nearby school context)
- How county schools are funded (half-cent surtax + one mill)
- (Optional) Programs of Choice as deferred/context

**Roads & Mobility (4)**
- CR 2209 connector: opened Oct 2025 (merged with construction)
- SR 16 / International Golf Parkway improvements (merged, "status as of late 2025")
- First Coast Expressway final phase + 2030 target (St. Johns)
- CR 210 widening timeline

**Growth & Construction (4)**
- Publix at Silverleaf Market: opened Mar 2026 (merged timeline)
- SilverLeaf grocery center — possible Harris Teeter (qualified)
- 165-acre SilverLeaf town center
- SilverLeaf Market outparcel buildings

**Retail & Amenities (5)**
- Beach Valley Mini Golf proposal (conditional)
- Bala's second location (after URL fix)
- Fifth Third Bank planned at Publix center
- Dunkin' in the works
- Nocatee Crosswater retail / Ascension (adjacent)

**Healthcare & Services (2)**
- Baptist SilverLeaf campus construction timeline
- Ascension St. Vincent's Nocatee (adjacent)

**Utilities & Water (3)**
- SR 207 WRF project timeline (merged)
- SJRWMD one-day-per-week rule (merged into water shortage)
- Utilities 2025 annual report (optional)

**Development & Zoning (2)**
- Impact fee updates (context)
- 2050 Comprehensive Plan transmittal (long-horizon context)

**Government/community (1)**
- FY2026 budget: first tax-rate cut since FY2021 (context)

**Preparedness (1)**
- Alert St. Johns sign-up (context)

---

## 31. Recommended timelines

| Subject | Related items | Proposed sequence | Current status |
|---------|---------------|-------------------|----------------|
| Magnolia Oaks Academy | SJC-BF-202509-0006, SJC-SL-20260704-0002, SJC-BF-202509-0008, live leads | planning → topping-out (May 2025) → naming (Sep 2025) → name revealed → opening (2026-27) | opening imminent |
| CR 2209 connector | SJC-BF-202508-0013, SJC-SL-20260704-0004 | construction began (Aug 2025) → opened (Oct 2025) | completed |
| SR 16 / IGP corridor | SJC-BF-202508-0020, SJC-BF-202508-0021 | hearings (Aug 2025) → groundbreaking ($25M, Aug 2025) → follow-up needed | underway |
| CR 210 widening | SJC-BF-202508-0010, SJC-BF-202508-0011 | shift (Aug 2025) → completion (Aug 2026, live) | just completed |
| SR 207 Water Reclamation | SJC-UTIL-20260603-0003, SJC-CN-20260626-0001 | Phase 2 approved (Dec 2025) → operational (May/Jun 2026) | operational |
| Publix / Silverleaf Market | SJC-SL-20260704-0001, live leads | permitted (2025) → construction (2026) → opened (Mar 2026) → tenants (2026) | open / growing |
| SilverLeaf grocery center | SJC-SL-20260704-0005, live leads | proposed (Dec 2025) → county review → tenant unconfirmed | proposed |
| Baptist SilverLeaf campus | live leads | review (2024) → permit (2025) → helipad (Apr 2026) → opened (Jun 2026) | open |
| FY2026 budget / taxes | SJC-BF-202508-0001..0004, SJC-BF-202509-0001..0004 | TRIM (Aug 2025) → hearings (Sep 2025) → adoption + tax cut → bills | adopted |
| Hallowes Cove school arc | SJC-BF-202508-0005..0008, SJC-BF-202509-0005 | zoning (Aug 2025) → opening → first students | opened |
| Water shortage | SJC-UTIL-20260603-0001, SJC-CN-20260603-0005, SJC-BF-202605-0005 | declaration (May 2026) → ongoing | active |

---

## 32. Proposed category inventory

Model B category placement against the v0 display topics:

| Display topic | Latest | Browse | Timelines | Feels |
|---------------|-------:|-------:|----------:|-------|
| Schools & Community | 3 | 4–5 | 3 | useful |
| Roads & Traffic | 2 | 4 | 4 | useful |
| Local Business | 1 | 5 | 3 | useful |
| Utilities & Water | 3 | 3 | 3 | useful |
| Emergency Preparedness | 1 | 1 | 0 | small but complete |

Note: "Growth & Construction" and "Healthcare & Services" are editorial planning
buckets; in the public UI they map onto Roads & Traffic / Local Business /
Schools & Community / Utilities & Water per the v0 topic contract. A
"Government & Taxes" topic is not part of v0 and is not added here (§36).

---

## 33. Category usefulness assessment

| Category | Item count (Model B) | Useful? | Notes |
|----------|----------------------|---------|-------|
| Schools & Community | ~8 | Yes | strong arc (Hallowes → Magnolia Oaks → zoning) |
| Roads & Traffic | ~8 | Yes | CR 2209 / SR 16 / CR 210 / FCE timelines make it rich |
| Local Business | ~7 | Yes | Publix + tenants + proposals = real browsing value |
| Utilities & Water | ~7 | Yes | already the strongest published category |
| Emergency Preparedness | ~2 | Marginal | small but complete; do not pad |

No category is empty under Model B. The current Model A leaves two topics
empty, which is the "empty/sad" failure mode. No category consolidation is
recommended — the five v0 topics all have ≥2 items in Model B, and none is so
sparse that merging helps.

---

## 34. Live source checks (bounded, recorded)

Narrow public-source verification only; no broad discovery. Each is a lead for
corpus capture, not a corpus record.

| # | Date | Subject | Check | Result |
|---|------|---------|-------|--------|
| 1 | 2026-08-07 | Magnolia Oaks Academy | Google News RSS | Confirmed: News4JAX + Action News Jax (2026-07-22) opening for 2026-27; St. Johns Citizen "Before the Roar" K-8 reveal (2026-07-24); SJCSD site listed; 2026-27 zoning announcement (St. Johns Citizen 2025-12-02). Identity chain School QQ → SilverLeaf K-8 → Magnolia Oaks validated. |
| 2 | 2026-08-07 | Baptist SilverLeaf campus | Google News RSS | Confirmed: opened Jun 23, 2026 (News4JAX, Business Journals, JaxToday, JDR); helipad approved Apr 2026 (JDR); $16.8M permit (Jan 2025); review since Jul 2024. |
| 3 | 2026-08-07 | Publix at Silverleaf Market | Google News RSS | Confirmed: opened Mar 26, 2026 (Publix corporate, News4JAX, JDR, St. Augustine Record, Business Journals "largest in NE FL"); "Silverleaf Market" is the Publix-anchored center; outparcels planned (JDR 2026-08-06); Fifth Third (JDR), M Shack + Natural Greens (Business Journals 2026-07-20), Dunkin' (WhatNow). |
| 4 | 2026-08-07 | First Coast Expressway | Google News RSS | Confirmed: FDOT St. Johns open house for final phase (JDR 2026-01-27); St. Johns Parkway detour during FCE work (Action News Jax); full opening targeted 2030 (Action News Jax); CR 210 widening opened ahead of school year (News4JAX). |

All checks used public, credential-free sources. Findings are recorded as leads
and corroboration; they were not injected into any corpus file.

---

## 35. Work required before publication

For the recommended Model B set (exact per item in §29–31):

| Work | Items affected | Detail |
|------|----------------|--------|
| NO_WORK | 7 published | CR 16A, hurricane, water, service line, WRF×2, utilities lab |
| SOURCE_CHECK | ~12 | Magnolia opening date, zoning, Compass, CR 210 completion, Baptist services, tenant statuses, FCE status; re-verify each media URL (Bala's 404) |
| COPY_EDIT | ~5 | Harris Teeter (qualified language), mini golf (conditional), Bala's (location), town center (status as of), FY2026 budget (context label) |
| CANONICALIZE | 3 | Magnolia Oaks identity, Silverleaf Market center identity, grocery center identity |
| MERGE | ~16 | CR 2209 (2), SR 16 (2), CR 210 (2), K-8/Magnolia (3+3), SR 207 (2), water (3), budget (8), Hallowes arc (5), hurricane (2), Baptist (4) |
| PIPELINE (import backfill) | ~30 | make `data/monthly/` backfill items reach the classifier; register `sjcsd_news`/`sjcsd_main_site` source IDs |

---

## 36. Proposed publication-policy changes

Only after seeing the complete candidate set. No changes were made.

| # | Current rule | Affected | Example | Risk of loosening | Recommended replacement |
|---|--------------|----------|---------|-------------------|--------------------------|
| 1 | `local_media` source type → always `NEEDS_HUMAN_REVIEW` | Publix, CR 2209 opening, mini golf, Harris Teeter, Bala's, Nocatee | Publix is corroborated by Publix corporate + 4 outlets but stays media-only | Uncorroborated media claims could publish | Allow default publication of `local_media` when (a) verified and (b) corroborated by an official/first-party source or 2+ independent outlets; otherwise require a human context exception. |
| 2 | Timely items >30 days → `timely_item_stale_needs_context_review` | CR 2209, SR 16, CR 210, Publix, budget | Completed roads/businesses are durable context, not stale news | Expired notices could be republished as current | Preserve the rule for event-like notices but add an explicit `role: context`/`historical` label path so completed durable projects publish as Browse with a "status as of" line. |
| 3 | `review_status != verified` → `NEEDS_MORE_RESEARCH` (data state) | all pending SL items | none needed | n/a | Not a policy change — a review-backlog action. Keep the rule. |
| 4 | No qualified-identity representation | Harris Teeter center | project confirmed, tenant not | — | Add a `qualified` public posture (e.g., "grocery center proposed; tenant unconfirmed") so confirmed projects with uncertain details publish honestly. |
| 5 | (Release window) 60-day default window | CR 2209 opened Oct 2025 | completed project excluded from default release window | — | Keep window for Latest; allow context/timeline items outside the window with explicit date labeling (contract extension, not policy). |

The single highest-leverage change is #1 + #2 combined with the pipeline import
(§35) — together they unlock most of Model B without weakening any safety gate.

---

## 37. Hermes workflow implications

Recurring failure modes and the exact weekly behavior to prevent them:

| Failure mode | Evidence | Prevention (weekly Hermes) |
|--------------|----------|----------------------------|
| Discovered entity never receives a follow-up search | Baptist has an accepted entity but no intel item | After accepting an adaptive entity, require a matching corpus item (or explicit "lead-only" marker) within the next weekly cycle. |
| Project has no timeline | Baptist, FCE, Publix timelines empty in corpus | Create/refresh the entity timeline record whenever a milestone (permit, groundbreaking, opening, helipad) is found. |
| Local-media lead never gets official-source reconciliation | Publix media item stayed pending while Publix corporate confirmed it | Weekly reconciliation pass: for each local-media lead, one official/first-party source check; record confirmation in the item. |
| Older useful records remain pending indefinitely | All 11 `SJC-SL-*` pending since July | Bound review work in the weekly task; do not let verified-capable items age in `pending_review`. |
| Construction lane under-covered | CR 210 completion (Aug 2026) never captured | Add recurring queries for active construction subjects (CR 210, SR 16, FCE) until a completion milestone is recorded. |
| Alias change broke later searches | School QQ → Magnolia Oaks; "SilverLeaf K-8" → "Magnolia Oaks Academy" | On canonical rename, update aliases and search profiles in the same change (the accepted-state edit already does this; extend to corpus search profiles). |
| Major resident subject never promoted to corpus | Baptist, Magnolia, FCE exist only as adaptive state + RSS leads | Define "adaptive-accepted entity → corpus item" as an explicit weekly deliverable. |
| Backfill corpus invisible to publication | `SJC-BF-*` never reaches classifier | Import/load monthly backfill into the classifier input set (data-path fix, then re-run classification). |

No implementation was performed in this task.

---

## 38. Master editorial inventory recommendation

Yes — the repository would benefit from one durable product-side editorial
view, e.g. `CURRENT_PUBLICATION_PLAN.md` (consistent with repo snake-case
conventions; exact name for Buddy/GPT to approve).

**Distinction from `CURRENT_BRIEF.md`:**

- `CURRENT_BRIEF.md` = operational health and current run state (mode, pipeline
  health, latest run, proposals, coverage lanes). Already exists and is
  generated.
- Product editorial inventory = **what the public site contains, what is
  waiting, and where coverage is sparse** — a stable, human-maintained plan of
  the Model B set (Latest / Browse / timelines), per-item work status
  (SOURCE_CHECK / COPY / MERGE), and explicit coverage gaps (Baptist, FCE,
  Magnolia, retail tenants).

It should contain: category tables from §29–31, per-item work-needed column,
merge/timeline map, coverage-gap list, and a "next release candidate" section.
It should not be auto-generated from run state. Not created in this task.

---

## 39. Master decision table

Table 1 — Full resident-relevant candidate inventory (ranked; representative)

| Rank | Item | Category | Subject | Date | Evidence | Status | Recommended treatment |
|------|------|----------|---------|------|----------|--------|------------------------|
| 1 | live | Schools | Magnolia Oaks opening | 2026-07-22 | strong | lead | VERIFY_THEN_PUBLISH (Latest) |
| 2 | live | Healthcare | Baptist campus opened | 2026-06-23 | strong | lead | VERIFY_THEN_PUBLISH (Latest) |
| 3 | SJC-SL-20260704-0001 | Retail | Mega Publix opened | 2026-03-26 | strong | pending | PUBLISH_AS_CONTEXT |
| 4 | SJC-SL-20260704-0004 + BF-0013 | Roads | CR 2209 connector | 2025-10-28 | strong | pending | MERGE_AND_PUBLISH |
| 5 | SJC-BF-202509-0006 + SL-0002 + BF-0008 | Schools | K-8 / Magnolia timeline | 2025–26 | strong | pending/invisible | MERGE_AND_PUBLISH |
| 6 | SJC-SL-20260704-0005 | Retail | grocery center (HT?) | 2025-12-02 | strong (qualified) | pending | PUBLISH_AS_CONTEXT (qualified) |
| 7 | SJC-BF-202508-0020/0021 | Roads | SR 16 / IGP | 2025-08 | strong | invisible | MERGE_AND_PUBLISH (context) |
| 8 | SJC-BF-202508-0010/0011 | Roads | CR 210 widening | 2025-08 | strong | invisible | MERGE_AND_PUBLISH (context) |
| 9 | live | Roads | CR 210 completed | 2026-08 | strong | lead | VERIFY_THEN_PUBLISH (Latest) |
| 10 | live | Roads | FCE final phase / 2030 | 2026-01 | strong | lead | PUBLISH_AS_CONTEXT |
| 11 | SJC-SL-20260704-0003 | Retail | mini golf proposal | 2026-04-08 | medium | pending | PUBLISH_AS_CONTEXT (conditional) |
| 12 | SJC-SL-20260706-0005 | Retail | Bala's | 2026-07 | medium (URL 404) | pending | VERIFY_THEN_PUBLISH |
| 13 | SJC-BF-202509-0003 (arc) | Govt | FY2026 budget/tax cut | 2025-09 | strong | invisible | PUBLISH_AS_CONTEXT |
| 14 | SJC-BF-202605-0011 | Schools | surtax/one mill | 2026-05 | strong | invisible | PUBLISH_AS_CONTEXT |
| 15 | SJC-SL-20260704-0006 | Health/Retail | Ascension Nocatee | 2026-06-01 | medium | pending | PUBLISH_AS_CONTEXT (adjacent) |
| 16 | live | Retail | M Shack / Natural Greens | 2026-07-20 | strong | lead | VERIFY_THEN_PUBLISH (Latest) |
| 17 | live | Retail | Fifth Third Bank | 2026-04 | medium | lead | VERIFY_THEN_PUBLISH |
| 18 | SJC-BF-202508-0005..0008/202509-0005 | Schools | Hallowes arc | 2025 | strong | invisible | PUBLISH_AS_TIMELINE |
| 19 | SJC-EM-20260626-0001 | Preparedness | hurricane prep | 2026-06-01 | strong | published | (keep) |
| 20 | SJC-BF-202605-0021 | Preparedness | hurricane messaging | 2026-05-26 | medium | invisible | MERGE into #19 |

Table 2 — Model B publication set: see §29–31 (13 Latest, 26 Browse, 9
timelines). Table 3 — False negatives: see §24. Table 4 — Genuine exclusions:
see §25.

---

## 40. Risks

- **Qualified-identity drift:** the possible-Harris-Teeter center must never be
  published as a confirmed tenant; the accepted adaptive timeline language is
  the safe ceiling. Risk of reputational harm if treated as fact.
- **Context mislabeled as news:** completed projects (CR 2209, Publix) must
  carry explicit dates and "status as of" framing per the UI temporal-truth rule
  (§9 of `docs/public_ui_v0_spec.md`).
- **Stale-rule erosion:** loosening the 30-day rule must not allow expired
  closures/notices to return as current; any change must gate on explicit
  role labeling.
- **Media corroboration quality:** Model B depends on a corroboration rule for
  local media; weak corroboration (single outlet, unverifiable URL) must stay
  `NEEDS_HUMAN_REVIEW`.
- **Pipeline import side-effects:** importing `data/monthly/` into the
  classifier will surface ~70 more items, some of which are noise (SJCSD
  programming, low-value county notices); import must be followed by the same
  relevance/review gates, not automatic publication.
- **This report changes nothing:** all numbers are analysis. Actual releases
  require the normal review + decision + release-build + deployment workflow.

---

## 41. Validation

```
python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/validate_publication_corpus.py
python3 scripts/validate_silverleaf_scope.py
git diff --check
git status --short
```

See §41–43 in the validation block below (run results recorded at execution
time; this task performs no authoritative mutation during validation).

---

## 42. Files changed

One new report: `reports/28-publication-corpus-expansion-review.md`. No
publication policy, decision, review status, corpus record, taxonomy, site,
release, deployment, scheduler, Ivy, or PostgreSQL state was modified. The
Task 27 working-tree state was left exactly as found.

---

## 43. Final Git status

`master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` (unchanged). Working tree
retains the pre-existing uncommitted Task 27 artifacts plus the single new
untracked report file `reports/28-publication-corpus-expansion-review.md`. No
commit or push.

---

## 44. Final task status

| Area | Status |
|------|--------|
| Full corpus inspection (intel_items, monthly, search_runs, adaptive, registry, site) | COMPLETE |
| Resident-relevant universe by category | COMPLETE |
| Deep-dive item sets (Magnolia, CR 2209, FCE, Baptist, Publix, Harris Teeter) | COMPLETE |
| Policy blocker analysis + false negatives | COMPLETE |
| Models A / B / C counts and Model B editorial inventory | COMPLETE |
| Recommended Latest / Browse / timelines | COMPLETE |
| Category usefulness + policy-change + Hermes recommendations | COMPLETE |
| Bounded live source checks | COMPLETE (recorded §34) |
| Validation (read-only) | COMPLETE |
| Publication/review/corpus/site/Git state | UNCHANGED (as required) |

**Final status vocabulary:** COMPLETE. Buddy and GPT now have a decision-ready
view of the actual resident-relevant corpus, a concrete Model B site inventory
(~42 items across every category), explicit policy false negatives, preserved
safety exclusions, merge/timeline maps, and live-verified status for the five
highest-value subjects. The sparsity is diagnosed as pipeline + review-state
debt (~70%) plus a narrow "fresh official news" policy posture (~30%), not weak
evidence. No authoritative state was changed and nothing was committed or
deployed.
