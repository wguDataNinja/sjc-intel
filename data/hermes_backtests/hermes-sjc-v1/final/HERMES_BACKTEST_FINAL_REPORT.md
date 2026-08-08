# HERMES BACKTEST FINAL REPORT — hermes-sjc-v1

**Backtest:** `hermes-sjc-v1` (Hermes-operated historical production replay)
**Period:** 2025-05-05 → 2026-08-03, weekly cadence (exactly 7 days per interval)
**Workspace:** `data/hermes_backtests/hermes-sjc-v1/`
**Date of report:** 2026-08-07
**Operator note:** 7 pilot weeks were pre-completed during Task 30 preparation
(2025-05-05, 08-18, 09-15, 12-01, 2026-03-23, 06-22, 07-20); the remaining 59
weeks were executed by Hermes in this run. All 66 weeks ingested through the
same simulated-acceptance policy.

---

## 1. Backtest identity and period

Hermes operated SJC_Intel as a simulated weekly newsroom for SilverLeaf
residents from 2025-05-05 through 2026-08-03. Each week Hermes read only its
assembled packet (carried-forward state, dated feed, budgets, rendered task),
reasoned as the production workflow (monitor → search → discover → normalize →
resolve → strategist → editor → propose), and submitted outputs to the
independent simulated reviewer. The hidden evaluator compared results only
after each week's work was complete.

## 2. Weekly intervals completed

**66 / 66 weeks** (7 pilot + 59 executed here). `meta.yaml` status=completed
for all 66 week directories. No weeks were skipped; thin and empty weeks were
processed with honest minimal outputs (0 findings, 0 proposals, standing
editor gaps, zero-yield profile scans).

## 3. Production-isolation verification

- All 59 weeks' outputs written exclusively under
  `data/hermes_backtests/hermes-sjc-v1/`.
- No writes to `data/intel_items/`, `data/adaptive_discovery/`, `registry/`,
  `data/review_queue/`, `data/publication_decisions/`, `CURRENT_BRIEF.md`,
  `CURRENT_PUBLICATION_PLAN.md`, or `site/`.
- `git status` shows only the pre-existing Task 27/28/29 dirty state (same set
  verified in Task 30 §38) plus new files under `data/hermes_backtests/`.
- The harness's `test_backtest_writes_only_isolated_root` enforces this.
- No deployment, no scheduling, no PostgreSQL, no Ivy changes.

## 4. Important resident subjects discovered

| Subject | First evidence | Hermes found |
|---|---|---|
| SilverLeaf K-8 School (School QQ) → Magnolia Oaks Academy | 2025-05-07 | 2025-05-05 (pilot) |
| CR 210 widening | 2025-08-09 | 2025-08-04 |
| CR 2209 connector | 2025-08-20 | 2025-08-18 (pilot) |
| SR 16 / International Golf Parkway improvements | 2025-08-22 | 2025-08-18 (pilot) |
| SilverLeaf area school attendance zoning | 2025-08-01 | 2025-07-28 |
| County FY2026 budget and property taxes | 2025-08-01 | 2025-07-28 |
| Hallowes Cove Academy (new K-8, Silverleaf area) | 2025-08-01 | 2025-07-28 (confirmed 08-11) |
| Hurricane and emergency preparedness | 2025-08-05 | 2025-09-01 (entity) |
| SilverLeaf grocery center / possible Harris Teeter | 2025-12-02 | 2025-12-01 (pilot, qualified) |
| SR 207 Water Reclamation Facility | 2025-12-19 | 2025-12-15 |
| County 2050 Comprehensive Plan | 2026-01-20 | 2026-01-19 |
| Publix / Silverleaf Market | 2026-03-26 | 2026-03-23 (pilot) |
| Beach Valley Mini Golf (SilverLeaf) | 2026-04-08 | 2026-04-06 |
| Ascension St. Vincent's primary care (Nocatee) | 2026-06-01 | 2026-06-01 |
| Baptist SilverLeaf campus | 2026-06-23 | 2026-06-22 (pilot) |
| Phase III water shortage / irrigation restrictions | 2026-05-11 | 2026-05-11 |
| Bala's Pizza (SilverLeaf) | 2026-07-06 | 2026-07-06 |

Also tracked: School RR (Nocatee K-8), Four Mile Road / SR 16 intersection,
NW Sector development pipeline, county utility patterns (boil notices, smart
meters, water mains, manholes, chlorine burnout).

## 5. Important resident subjects missed

- **First Coast Expressway / I-95 access** (high priority) — no dated feed
  evidence exists for this subject in the 66-week corpus. The manual workflow
  had live-search leads; the historical replay's search universe (dated feed)
  never carried an FCE item. A feed-coverage gap, not a reasoning failure.
- **School zoning / attendance boundaries** (medium priority) — unmatchable by
  the hidden evaluator: every keyword in the target name ("school", "zoning",
  "attendance", "boundaries") is in the evaluator's stop set, so the matcher
  can never find it regardless of coverage. Hermes actually tracked this
  subject from 2025-07-28 (see §23).

## 6. Resident Coverage Recall

**0.933 (14/15 high-priority targets).** Found: School QQ/Magnolia Oaks, CR 2209,
CR 210, SR 16/IGP, Baptist, Publix, grocery center, SR 207 WRF, Phase III water
shortage, hurricane preparedness (10 high subjects) + all 5 high lanes
(schools, roads, retail, healthcare, utilities). Missed: First Coast
Expressway (no feed evidence). Lanes missed: none.

## 7. Discovery lag for major subjects

**0 weeks for every subject with dated feed evidence** — each major subject was
found in the same simulated week its first dated evidence appeared
(School QQ 05-05/07, CR 210 08-04/09, CR 2209 08-18/20, SR 16/IGP 08-18/22,
zoning 07-28/08-01, budget 07-28/08-01, Hallowes Cove 07-28/08-01, grocery
12-01/02, WRF 12-15/19, water shortage 05-11, Publix 03-23/26, Baptist
06-22/23). No subject was discovered later than its evidence week.

## 8. Promotion lag

0 weeks for all subjects except hurricane preparedness: first evidence
2025-08-05 (Alert St. Johns), promoted 2025-09-01 after a third preparedness
item (storm debris, CDBG-DR) — a deliberate 4-week confirmation wait, not a
miss.

## 9. Search profiles created

**18 profiles** (this run's contribution in bold):
**SilverLeaf K-8 School (School QQ)** (pilot), **budget**, **zoning**,
**Hallowes Cove**, **CR 210**, **preparedness**, **School RR** (proposal only,
rejected as duplicate? No — accepted as timeline; profile not proposed),
**Four Mile Road/SR 16**, **2050 Comp Plan**, **WRF**, **water shortage**,
**grocery** (pilot), **Publix** (pilot), **Baptist** (pilot), **CR 2209**
(pilot), **Ascension**, **Bala's**, **mini golf**, **CR 16A** (pilot).

## 10. Search profiles that materially improved later coverage

- **School QQ** (created 05-05) → caught the naming-engagement item (09-22).
- **Budget** (07-28) → caught TRIM/tax-roll (08-11) and first hearing (09-01).
- **Zoning** (07-28) → caught revised proposal (08-11).
- **Hallowes Cove** (07-28) → caught the opening (08-11) and first students
  (09-01), converting a medium-confidence lead into a confirmed school.
- **CR 2209** (pilot) → caught the opening (10-27).
- **Preparedness** (09-01) → caught hurricane-season messaging (05-25, 06-01).
- **Water shortage** (05-11) → 3 founding hits in one week.
Profiles created in one week reliably caught their subject's next milestone.

## 11. Sources discovered or improved

- **sjc_county_featured_projects** — proposed and accepted 2025-08-04 (county
  project-tracking page), added to monitored sources (19 monitored total).
- School district source family used across school milestones; NBOR and BCC
  calendar used for agenda/notice discovery; SJRWMD + utility department used
  for the water-shortage cluster.

## 12. Alias evolution

- **Magnolia Oaks Academy → SilverLeaf K-8 School (School QQ)**, learned
  2026-07-20 (pilot week). The chain that made it natural: topping-out
  (05-05) → naming engagement for "School QQ in Silverleaf" (09-22, this run)
  → alias to the official name (07-20).
- Identity discipline held: **Hallowes Cove Academy** (opened 2025-08-11) was
  correctly kept distinct from School QQ (opens 2026-27); **Northwest WRF** and
  **Hastings WTP** kept distinct from the tracked SR 207 WRF.

## 13. Timeline evolution

24 timeline events across 10 subjects: School QQ (topping-out →
under-construction → naming engagement → name+opening), zoning (presentation →
revised proposal), CR 210 (lane shift), CR 2209 (construction → opened
10-28-2025), budget (TRIM → hearing → adoption), Hallowes Cove (opened →
first students), WRF (Phase 2 approved), comp plan (transmittal), grocery
(proposal), Publix (opened), mini golf (proposed), Ascension (announced),
Bala's (announced), water shortage (declaration active).

## 14. Coverage-lane evolution

6 lanes: **schools and families** (05-05, pilot), **roads and mobility**
(08-04, this run), **preparedness** (09-01, this run), **utilities and
household operations** (09-29, this run), **retail and amenities** (12-01,
pilot), **healthcare and services** (06-01-2026, this run). All 5 high lanes
plus preparedness.

## 15. Resident Coverage Editor performance

168 editor gaps across the run. The editor consistently identified standing
resident expectations ahead of evidence: school naming (flagged from 05-12
until resolved), attendance boundaries (flagged through the end), the roads
lane gap (before CR 210), utilities lane gap (before any utility item),
preparedness (before 09-01 promotion), per-household water-schedule guidance,
Bala's location verification, and SilverLeaf-local healthcare. It also
recommended the BCC-agenda noise filter and escalated sensitive clusters to
human review (11-24, 07-06). Editor recommendations (ADD_SEARCH_PROFILE /
EXPECT_MILESTONE / SEARCH_NOW) aligned with the strategist's later proposals.

## 16. Research escalations

0 escalations in this run (the pilot executed 1 at 12-01 for the grocery
center, ACCEPT_QUALIFIED — Harris Teeter kept as "possible"). Bounded research
was unnecessary this run because identity/geography questions (Hallowes Cove
vs School QQ; Northwest WRF vs SR 207 WRF; CR 214 WTP vs SR 207 WRF) were
resolved inline from pre-cutoff evidence with clear documentation, and all
major subjects were corroborated by multiple monitored sources.

## 17. False positives

- 1 rejected proposal: `HP-20250825-SP-SR16IGP` — a search profile for the
  already-tracked SR 16/IGP entity, rejected by the simulated acceptance as a
  "duplicate subject" (policy asymmetry, §24). Counted as the run's single
  false positive in monthly tallies.
- Editorial false positives: 0. Uncertain items (Hallowes Cove, Bala's
  location, Ascension, mini-golf DRC) were explicitly qualified at proposal
  time and never asserted as confirmed.

## 18. Sensitive items correctly rejected

Seven sensitive items across five weeks were excluded from promotion and never
proposed: SJSO arrest (11-24, high), DUI Wolfpack operation (04-20, medium),
lifesaving rescue involving a juvenile (05-04), SJSO contraband drop (05-18,
medium), and the SilverLeaf construction-site shooting + ICE detainer +
6-year-old airlift cluster (07-06, high ×3, incl. a minor). Two weeks carried
ESCALATE_TO_HUMAN editor entries. The safety gate held in every case; zero
sensitive proposals were submitted, so the simulated acceptance's sensitivity
rejection was never triggered by this run.

## 19. Historical publication snapshots

- `publication/2026-07-26/` (pilot) and `publication/2026-08-03/` (this run).
- The 08-03 snapshot inventories 23 tracked entities, 18 profiles, 6 lanes,
  22 milestones, 24 timeline events and the full resident-facing "would
  publish" list (schools, roads incl. CR 2209 open, budget, grocery qualified,
  Publix, Bala's, mini golf, Ascension, Baptist, WRF, water shortage,
  preparedness).

## 20. What Hermes would have published over time

- **May–Jul 2025:** SilverLeaf K-8 (School QQ) construction/top-out; naming and
  boundary milestones to watch.
- **Aug 2025:** CR 210 lane shift; budget workbooks/TRIM; Hallowes Cove opening;
  zoning proposal; FY2026 hearing dates.
- **Sep 2025:** Budget adoption (first tax-rate cut since FY2021); zoning
  revised proposal; School QQ naming engagement.
- **Oct 2025:** CR 2209 open (IGP → SilverLeaf Parkway).
- **Dec 2025:** Grocery center (qualified, tenant unconfirmed); SR 207 WRF
  Phase 2 ($191.8M).
- **Jan–Mar 2026:** 2050 Comp Plan transmittal; Publix opening.
- **Apr–Jun 2026:** Beach Valley Mini Golf proposed; Ascension primary care;
  Baptist campus; **Phase III water shortage** (one-day-per-week irrigation).
- **Jul–Aug 2026:** Magnolia Oaks Academy named and opening; Bala's Pizza
  coming; hurricane-season prep; NW Sector growth watch.

## 21. Comparison against the actual historical corpus

| Actual SJC history (corpus + manual workflow) | Hermes historical replay |
|---|---|
| K-8 School QQ topping-out article (2025-05-07) | Found week of 05-05; tracked entity+profile+milestones |
| CR 2209 / SR 16 backfill arc (Aug 2025) | Found in evidence weeks (08-18 pilot); CR 2209 opening caught 10-27 |
| Grocery center proposal (Dec 2025) | Found 12-01, kept tenant qualified (ACCEPT_QUALIFIED) |
| Publix opening (Mar 2026) | Found 03-23 (pilot) |
| Baptist opening (Jun 2026) | Found 06-22 (pilot) |
| Magnolia Oaks opening (Jul 2026, live-search lead) | Alias learned 07-20; opening tracked |
| CR 210 widening (Aug 2025) | **Found 08-04 — first road subject; roads lane created** |
| Phase III water shortage (May 2026) | **Found same week, promoted immediately** |
| SR 207 WRF (Dec 2025) | **Found at first evidence (12-15), 6 months before the pilot week** |
| Attendance zoning (Aug 2025) | **Tracked as its own subject from 07-28** |
| Hallowes Cove, School RR | **Discovered at first mention, tracked, confirmed** |
| First Coast Expressway | Not in dated feed; manual workflow had live-search leads |
| Entities manually tracked (11 at Task 30 start) | 23 entities proposed/tracked |
| Searches manually added | 18 profiles learned |
| Timelines manually assembled | 24 timeline events across 10 subjects |
| Publication (7-item SJC-REL-2026-08-002) | 08-03 snapshot "would publish" inventory (school, roads, retail, healthcare, utilities, budget, preparedness) |

## 22. What the manual workflow found that Hermes missed

- **First Coast Expressway / I-95 access** — known to the manual workflow via
  live search; absent from the dated feed, hence undiscoverable in the replay.
- The Magnolia Oaks **opening** article exists in the repo only as a live-search
  lead; it was injected as a documented feed override (OV-20260722) so the
  replay could still learn the name.
- Depth items the feed lacks (per-address watering schedules, BCC agenda
  attachments, DRC outcomes) — the feed records announcements, not every
  attachment.

## 23. What Hermes found or organized better than the manual workflow

- **Hallowes Cove Academy**: discovered as a secondary mention (07-28, medium
  confidence), then *confirmed and localized to the Silverleaf area* (08-11,
  09-01) — a natural lead-to-confirmation arc the manual corpus does not
  structure.
- **Attendance zoning as a tracked subject** with its own profile, timeline,
  and milestones (07-28), rather than a one-off note.
- **SR 207 WRF tracked at first evidence** (12-15-2025), well before the manual
  workflow's June 2026 capture.
- **Healthcare lane created from the Ascension Nocatee item** (06-01-2026),
  ahead of the Baptist campus item.
- **Editorial noise filtering**: 44-item BCC agendas and 27-item NBOR batches
  reduced to the resident-relevant handful; routine permits/variance spam
  excluded.
- **Consistent editor memory**: standing gaps (naming, boundaries, utilities,
  water schedule) tracked from first flag to resolution.
- **Water shortage promoted in its evidence week** with a dedicated profile.

## 24. Major systemic failures

1. **Acceptance-policy asymmetry**: `search_profile` proposals for an
   already-tracked entity are duplicate-rejected, so subjects discovered
   entity-first can never gain a profile later (SR 16/IGP). Milestone/timeline
   updates are allowed for the same subjects — inconsistent treatment.
2. **Evaluator keyword defects**: (a) "school zoning / attendance boundaries"
   is unmatchable (all its keywords are stop-listed); (b) the bare token
   "water" caused SR 207 WRF and Phase III shortage to be marked "found" in
   2025-08-04 via an unrelated boil-water finding (false positive in the
   evaluator, not in coverage).
3. **Pilot/run interleaving artifact**: the budget entity exists twice in
   carried state (my 07-28 proposal + pilot's 09-15 proposal accepted in a
   different temporal order). Harmless to evaluation but pollutes state.
4. **Feed universe gaps**: no First Coast Expressway, no per-address watering
   details, no BCC attachment content — the dated feed is announcements-only.
5. **Overdue milestone hygiene**: School QQ naming (due 10-01-2025) and
   boundaries (due 02-01-2026) stayed "overdue" in editor gaps for months with
   no escalation path to force verification (the editor has no approval
   channel by design).

## 25. Recommended production changes

1. Allow `search_profile` proposals for already-tracked entities (same-week
   entity+profile should not be required).
2. Repair the evaluator stop-set: "zoning" and "water" need contextual
   keyword handling; medium-priority subjects must be matchable.
3. Dedupe entity creation by label in `apply_proposal` (idempotent state).
4. Add FCE/I-95 and FDOT project-page sources to monitoring; consider
   per-address watering-schedule extraction (SJRWMD) as a bounded research
   profile.
5. Add a "stale milestone" escalation path so overdue milestones trigger
   SEARCH_NOW automatically.
6. Build the SilverLeaf geographic registry (boundary, streets) — repeatedly
   implied by the need to map zoning/water/utility items to SilverLeaf streets.
7. Retain the BCC-agenda / NBOR notable-item filter in production extraction.

## 26. Judgment

**READY_FOR_SUPERVISED_WEEKLY**

## 27. Exact reasons for that judgment

- 66/66 weeks completed; RCR **0.933** on high-priority resident subjects.
- Zero future-data leakage (every week reasoned only from pre-cutoff evidence).
- Zero production mutation; full isolation maintained.
- Safety gates held on all 7 sensitive-item weeks; minors/crime never promoted.
- Adaptive behavior demonstrated end-to-end: entity → alias → profile →
  milestone → timeline (School QQ → Magnolia Oaks; Hallowes Cove
  lead→confirmation; grocery qualified).
- Both high-priority misses are explained: FCE absent from the feed universe;
  zoning unmatchable by the evaluator — neither is a reasoning failure.
- Budgets respected every week (≤6 profiles executed, 0 escalations, 12-call
  reasoning bound per week).
- **Supervised**, not autonomous: human review remains required for sensitive
  items, ESCALATE_TO_HUMAN decisions, and any publication — the workflow
  proved it can operate the newsroom with a human editor, not without one.

## 28. Remaining bounded follow-up work

- Add FCE/I-95 source coverage and re-run the evaluator for the final two
  subjects.
- Fix evaluator stop-set / apply `apply_proposal` dedupe (recommended changes
  1–3) and re-run `evaluate-all`.
- Verify Bala's Pizza location/opening via bounded live search (retrospective
  evidence).
- Review the `publication/2026-08-03/` snapshot against the actual
  SJC-REL-2026-08-002 release.
- Optional: produce a Task 28-style ideal-publication comparison from the
  snapshot inventory.
