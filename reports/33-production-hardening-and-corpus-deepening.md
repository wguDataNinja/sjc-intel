# Task 33 — Production Workflow Hardening and Corpus Deepening

**Task identity:** 33-production-hardening-and-corpus-deepening.md
**Date:** 2026-08-09
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Mode:** supervised
**Final status:** COMPLETE_WITH_FOLLOW_UP — workflow hardened, corpus deepened,
Release 004 candidate built and validated locally; deployment not performed and
a real supervised weekly run remains for Task 34.

**Scope honored:** no deployment, no scheduler activation, no source promotion,
no taxonomy change, no publication of Release 004, no PostgreSQL, no Ivy
changes. Release 004 exists only as a local candidate under `site/`.

---

## 1. Executive result

SJC_Intel's production Hermes workflow is hardened against the generalized
defects the 66-week backtest exposed, and the publication/research exception
backlog is materially reduced through bounded evidence work.

- **Six generalized defects addressed** (acceptance asymmetry, evaluator
  matcher, entity/proposal dedupe, FDOT/FCE coverage, stale-milestone
  escalation, production/backtest prompt alignment) — each with code changes
  and regression tests. The backtest evaluator now correctly finds
  "school zoning / attendance boundaries" (was unmatchable); only First Coast
  Expressway remains a miss, and that is a genuine feed-coverage gap now
  addressed by official FDOT project-page monitoring.
- **Backlog materially reduced:** AUTO_PUBLISHABLE 34 → 48;
  NEEDS_MORE_RESEARCH 106 → 75. Thirty-two low-risk official records were
  reconciled to `verified`; six strong new verified corpus items were created
  from first-party/official research (Magnolia Oaks opening, Baptist expansion,
  FCE construction, Courtney Vista Drive, SR 16 RCUT, FY2027 TRIM). The
  remaining human-review (79) and research (75) records are genuine editorial
  gates or non-SilverLeaf items, not routine research debt.
- **Release `SJC-REL-2026-08-004` candidate** built and fully validated
  locally: 48 items (12 latest, 24 browse, 11 timeline, 1 context), 75 routes,
  zero warnings, zero safety leaks. It is a candidate, not a deployment.
- **Readiness judgment: READY_FOR_FIRST_SUPERVISED_WEEKLY_RUN.**

---

## 2. Starting Git state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `87a09597d53ef6b993a60efa5ab52ba85bf6d036` |
| Origin | synchronized (0 ahead / 0 behind) |
| Working tree | One pre-existing untracked file (`reports/32-post-launch-operations-and-forward-plan.md`) |
| Public product | Live Release `SJC-REL-2026-08-003` (34 items) |
| Scheduler | `deploy/sjc-weekly-task.yaml` `enabled: false` |

## 3. Starting publication state

| Metric | Before Task 33 |
|--------|---------------:|
| Public items (Release 003) | 34 |
| Latest | 10 |
| Browse/context | 15 |
| Timelines | 9 |
| Category counts | Schools 10, Roads 9, Local Business 6, Utilities 6, Emergency 3 |

## 4. Starting exception counts (live classifier, 2026-08-09)

| Classification | Count |
|----------------|------:|
| AUTO_PUBLISHABLE | 34 |
| NEEDS_HUMAN_REVIEW | 56 |
| NEEDS_MORE_RESEARCH | 106 |
| EXCLUDE | 65 |

(Note: `CURRENT_BRIEF.md` generated 2026-08-07 reported 7/51/69/65 from a
stale snapshot; the live classifier at task start reported the counts above.)

## 5. Task 32 defects reviewed

| Defect | Status | Where fixed |
|--------|--------|-------------|
| Acceptance asymmetry | Fixed | `scripts/hermes_backtest.py` ingest; `scripts/live_adaptive.py` `evaluate_proposals` |
| Evaluator keyword defects | Fixed | `scripts/hermes_backtest.py` `_subject_keywords` / `_token_hit` / `_alias_terms` |
| `apply_proposal` non-idempotent entity creation | Fixed | `apply_proposal` label dedupe |
| FDOT/FCE feed-universe gap | Addressed | registry sources + mobility scope + `sl_fce_fdot` search profile |
| No stale-milestone escalation | Fixed | `resident_coverage_editor` SEARCH_NOW escalation |
| Production weekly prompt predates Model B | Fixed | `docs/hermes_weekly_entrypoint.md` + `prompts/sjc_weekly_ops_task.md` |

## 6. Acceptance asymmetry

**Evidence:** the backtest rejected a `search_profile` proposal for an
already-tracked entity as a "duplicate subject," while milestone/timeline
updates for the same subject were accepted — inconsistent. The same flaw
existed in production `evaluate_proposals`, which rejected any proposal whose
subject was already accepted.

**Fix:** entity recreation for a tracked subject is still rejected as a
duplicate; a `search_profile`, `milestone`, `timeline_reconciliation`, or
`coverage_lane` for an existing entity is accepted when that exact pair is not
already present. Production now uses an explicit bucket→type map.

**Regression tests:** `test_acceptance_allows_search_profile_for_tracked_entity`,
`test_acceptance_rejects_duplicate_entity` (backtest); `test_evaluate_allows_search_profile_for_tracked_entity`,
`test_evaluate_rejects_duplicate_entity` (production).

## 7. Evaluator matcher

**Evidence:** the old stop set stripped every generic token, making "school
zoning / attendance boundaries" unmatchable, while the bare token "water"
produced false "found" marks for unrelated boil-water items.

**Fix:** the matcher now (a) uses precise alias phrases first, and (b) requires
a majority (ceil 2/3) of distinctive tokens via `_token_hit`, so bare single
tokens never satisfy a subject. Medium-priority subjects whose tokens all
survive remain matchable.

**Rerun result (`evaluate-all` on the completed 66 weeks):**
- RCR: 0.933 (high-priority denominator unchanged).
- Now found: `school zoning / attendance boundaries` (was missed).
- Still missed: `First Coast Expressway / I-95 access` — genuine feed gap;
  addressed operationally by the new FDOT project-page monitoring.

## 8. Entity/proposal dedupe

**Evidence:** `apply_proposal` appended entities without checking labels; the
budget entity existed twice in carried backtest state.

**Fix:** entity and search-profile creation are now idempotent by normalized
label; a re-proposal updates nothing rather than creating a second record.
**Regression test:** `test_apply_proposal_dedupes_entity_by_label`.

## 9. Transportation / FDOT coverage

**Finding (verified 2026-08-09):** FDOT's final St. Johns County segment —
First Coast Expressway from I-95 to east of CR 2209 — is under construction,
with a $205M contract (Mastec Civil LLC), early-2026 start, and late
2030/early 2031 expected completion, per the official project page
`https://nflroads.com/ProjectDetails?p=5639`.

**Changes:**
- `registry/silverleaf_mobility.yaml`: new authority source
  `FDOT-FCE-I95-CR2209-2026` and a new `nearby_commute_corridor` segment
  `sl_fce_final_segment_context` with explicit "never imply a direct SilverLeaf
  interchange" exclusion.
- `registry/sources.yaml`: `fdot_district_two_nflroads` notes now anchor both
  the FCE (p=5639) and SR 16 IGP-to-I-95 PD&E (p=5615) project pages.
- `registry/search_profiles.yaml`: new `sl_fce_fdot` weekly profile.
- `docs/silverleaf_mobility_scope.md`: FCE project record documented.

## 10. Stale-subject escalation

`resident_coverage_editor` now checks accepted `milestones` for a
`milestone_due` date that has passed without a fresh finding and emits a
`SEARCH_NOW` finding ("expected milestone due X passed without confirmed
coverage"). Expected milestones were added to accepted state for Magnolia Oaks
(2026-08-10), Baptist Emergency Center (2026-09-01), and FCE completion
(2030-12-31). **Regression test:** `test_editor_escalates_overdue_milestone`.

## 11. Production/backtest workflow alignment

The authoritative 13-step production sequence is now documented once, in
`docs/hermes_weekly_entrypoint.md`: known-source capture → targeted searches →
bounded discovery → normalize/relevance → identity/alias reconciliation →
ambiguity → research escalation → strategist → Resident Coverage Editor →
independent evaluation → human review → Model B classification →
adaptive-state-to-corpus → regenerate plan/brief. The simulation-only mechanics
(simulated acceptance, hidden evaluator) are explicitly NOT copied into
production. `prompts/sjc_weekly_ops_task.md` was aligned with Model B fields
(roles, qualified posture, corroboration), stale-milestone escalation, and the
FDOT project-page anchors.

## 12. Production Hermes workflow after changes

Known-source capture (NBOR + SJSO pilot; county news when scripted) → active
search profiles (incl. FCE) → bounded discovery → normalize + resident
relevance → identity reconciliation (entity → alias → timeline) → research
escalation → strategist → editor (incl. stale-milestone escalation) →
independent evaluation → human review → Model B classification (roles,
qualified, corroboration) → adaptive-state-to-corpus → regenerate
CURRENT_PUBLICATION_PLAN.md and CURRENT_BRIEF.md. Scheduler stays disabled.

## 13. PUB-004 backlog triage

For every unresolved resident-relevant candidate, the reason was classified.
Groups used: SOURCE_CHECK, IDENTITY_RECONCILIATION, LOCATION_CONFIRMATION,
COPY_QUALIFICATION, CORROBORATION, TIMELINE_MERGE, STALE_FOLLOW_UP,
PUBLICATION_POLICY_EXCEPTION, SENSITIVE_HUMAN_REVIEW, NOT_RELEVANT,
INSUFFICIENT_EVIDENCE.

## 14. Initial backlog counts by reason

| Reason | Before |
|--------|-------:|
| NEEDS_MORE_RESEARCH — pending_review | 106 |
| NEEDS_HUMAN_REVIEW — agenda/notice needs concrete local scope | 38 |
| NEEDS_HUMAN_REVIEW — timely-stale needs context review | 11 |
| NEEDS_HUMAN_REVIEW — sensitivity/personal-harm | 4 |
| NEEDS_HUMAN_REVIEW — missing resident scope | 2 |
| NEEDS_HUMAN_REVIEW — local-media source check | 1 |
| EXCLUDE (legacy/dup/archived) | 65 |

## 15. Research performed (bounded, official-first)

| Subject | Official evidence | Result |
|---------|-------------------|--------|
| Magnolia Oaks | SJCSD news + zoning page | Opening confirmed (Aug 10, 1,300 students, K-7; K-8 QQ Plan C-Modified 11/18/25; live locator) |
| Baptist SilverLeaf | Baptist Health campus page | Orthopedics Aug 2026; Emergency Center Sep 2026 |
| First Coast Expressway | FDOT/NFLRoads p=5639 | $205M contract, early 2026 start, late 2030/31 completion |
| FY2027 budget/TRIM | County OMB FY27 page | Recommended budget 7/21/26; TRIM mid-Aug; hearing Sep 3 |
| Courtney Vista Drive | County news | CR 2209–Silverleaf Parkway link complete (9 months) |
| SR 16 RCUT | County news | Traffic-pattern change mid-late Sep at Stratton/Industry Center |
| Bala's | St. Johns Citizen (working URL) | 404 resolved; second location at 60 Silver Forest Dr |
| CR 2209 / CR 210 | County records (existing) | Verified current via mobility registry + Courtney Vista link |

## 16. Source checks resolved

- **Bala's (`SJC-SL-20260706-0005`):** recorded URL returned 404; located and
  verified the working St. Johns Citizen article URL; item verified.
- **Magnolia Oaks opening date + grade span:** resolved from first-party SJCSD
  (removed from Needs-source-check).
- **First Coast Expressway timing:** resolved from FDOT project page (moved
  from "lead-only" to a corpus item with official schedule).
- **SR 16 current 2026 status:** partial (RCUT milestone captured; PD&E
  completion still TBD on nflroads).
- **Silverleaf Market tenant opening dates:** remain reporting-only.

## 17. Identity issues resolved

- School QQ → SilverLeaf K-8 → Magnolia Oaks Academy identity chain retained
  and now anchored to the district's first-party opening announcement.
- FCE tracked as a project subject, explicitly NOT presented as a
  SilverLeaf-owned road or a direct-interchange claim.

## 18. Location issues resolved

- Bala's location confirmed at 60 Silver Forest Dr, Suite 111.
- Baptist campus address confirmed at 8595 St. Johns Parkway.
- FCE segment endpoints documented (I-95 → east of CR 2209).

## 19. Qualified-publication cases

- **Bala's second location:** presented as reported (owner quote in article),
  not operator-confirmed; "reported near-opening" framing retained.
- **Possible-Harris-Teeter grocery center:** unchanged, still tenant-unconfirmed.

## 20. Genuine human-review cases (preserved)

- SJSO crime/arrest items and SilverLeaf shooting/ICE-detainer/airlifted-child
  items remain `pending_review` + human-gated.
- NBOR non-SilverLeaf permits and BCC boilerplate remain out of scope.
- FY2027 budget/tax content awaits the standing "Government & Taxes topic
  decision" (recorded as `defer`).
- Timely-stale items awaiting context-role decisions (25).

## 21. Remaining research cases

75 items remain NEEDS_MORE_RESEARCH: ~45 NBOR non-SilverLeaf permits/noise, 7
sensitive crime/incident items, and ~23 non-SilverLeaf county/school records.
These are genuinely not routine SilverLeaf-resident evidence debt and were left
pending rather than bulk-promoted.

## 22. Magnolia Oaks

`SJC-SL-20260809-0001` (Latest, Schools & Community): SJCSD first-party
confirmation of the Aug 10 opening, 1,300 students, K-7 first-year span;
K-8 QQ Plan C-Modified (approved 11/18/25) and the live 2026-27 attendance-zone
locator retained as the address-level authority (DIR-010). Replaces the earlier
"opening date to confirm" source check.

## 23. First Coast Expressway

`SJC-SL-20260809-0003` (Timeline anchor, Roads & Traffic): official project
record — I-95 to east of CR 2209, $205M Mastec contract, early-2026 start,
late 2030/early 2031 completion, Feb 2026 construction open house. FCE moves
from "public-hearing-stage context" to a tracked under-construction project
subject with a recurring `sl_fce_fdot` search profile.

## 24. CR 2209

Courtney Vista Drive completion (`SJC-SL-20260809-0005`, Latest) records the
new direct CR 2209–Silverleaf Parkway link and feeds the CR 2209 timeline. The
opened Silverleaf Parkway–IGP segment and the 7.7-mile central project remain
in the mobility registry as direct-access context.

## 25. CR 210

The completed widening milestone (Release 003) remains current for the 2026-27
school year. No new 2026 CR 210 construction milestone beyond the completed
record was found; it stays as completed-project context.

## 26. SR 16 / IGP

`SJC-SL-20260809-0006` (Browse, Roads & Traffic): RCUT traffic-pattern change
at Stratton Boulevard / Industry Center Road (mid-late Sep). The SR 16–IGP
intersection improvements ($25M) and the IGP-to-I-95 PD&E study remain in the
mobility registry with their project pages.

## 27. Baptist SilverLeaf

`SJC-SL-20260809-0002` (Timeline anchor, Local Business): first-party Baptist
Health expansion — Orthopedics Aug 2026, Emergency Center Sep 2026 — extends
the Baptist timeline beyond the first-phase opening (Release 003 latest).

## 28. Publix / Silverleaf Market

Unchanged core corpus (`SJC-SL-20260807-0005`): outparcels + tenants (Fifth
Third, M Shack, Natural Greens) remain reporting-only for opening dates. No
new tenant opening was confirmed in this pass.

## 29. SilverLeaf grocery center / Harris Teeter

Unchanged qualified subject: project under county review; tenant NOT confirmed.
No new first-party evidence confirming or weakening Harris Teeter was found;
the qualified posture is retained.

## 30. FY2027 budget / TRIM

`SJC-SL-20260809-0004` verified in corpus (county OMB source): recommended
budget 7/21/26, proposed millage ceilings, first public hearing Sep 3, TRIM
mid-August. Held out of Release 004 by a `defer` decision pending Buddy's
public "Government & Taxes" topic decision (standing plan gate).

## 31. Major construction coverage

New resident-visible construction items: Magnolia Oaks opening (school),
Baptist Orthopedics/ER (healthcare), Courtney Vista Drive (road), SR 16 RCUT
(road), FCE final segment (expressway). These close the editor's
"what major thing is being built that the publication doesn't explain" gap for
the current cycle.

## 32. Adaptive subjects vs corpus coverage

| Accepted adaptive subject | Corpus item now? |
|---------------------------|------------------|
| Magnolia Oaks Academy | Yes (latest + timeline) |
| CR 2209 connector | Yes (timeline + Courtney Vista latest) |
| CR 210 widening | Yes (release 003 + browse) |
| SR 16 / IGP | Yes (browse + timelines) |
| First Coast Expressway access | Yes (timeline + browse) |
| Baptist SilverLeaf campus | Yes (timeline + latest) |
| Publix at Silverleaf Market | Yes (timeline + latest) |
| SilverLeaf grocery center / possible Harris Teeter | Yes (browse, qualified) |
| SR 207 WRF | Yes (timeline) |
| Phase III water shortage | Yes (latest) |

No accepted high-priority subject is lead-only (the plan's
adaptive-state-to-corpus check reports zero gaps).

## 33. Timeline improvements

Release 004 timelines: 11 (was 9). New anchors: FCE project subject, Baptist
SilverLeaf expansion. The new milestone items (Magnolia opening, Courtney
Vista, SR 16 RCUT) auto-link into the CR 2209 / SR 16 / Publix / WRF timelines
via shared topic/entity relations, deepening the existing subject arcs.

## 34. Release 004 candidate

`SJC-REL-2026-08-004` built locally at `site/data/releases/SJC-REL-2026-08-004/`
(48 items, 75 routes). `--check` passes with zero warnings. The site is rebuilt
to this candidate locally. **Not deployed.**

## 35. Latest inventory (12)

Magnolia Oaks opening; CR 210 completion; Silverleaf Market outparcels;
Courtney Vista Drive; Magnolia Oaks Aug 10 opening; CR 16A weekend closure;
SJC largest capital project; Baptist outpatient campus; water service-line
inventory; hurricane-season prep; St. Johns Compass; Phase III water shortage.

## 36. Browse/context inventory (25)

Durable resident knowledge across Schools (attendance-zoning arc, Hallowes
Cove, surtax/one mill, STAR awards, A-grade, board records), Roads (FCE, SR 16
RCUT, Four Mile/SR 16, signals/markers), Local Business (grocery center
qualified, mini golf, Nocatee/Ascension), Utilities (annual report, Moody's,
capital project, SR 207 WRF context), Emergency (Alert St. Johns, storm
debris), and countywide services (S.E.A. center, Clerk's office).

## 37. Timeline inventory (11)

Publix/Silverleaf Market, SR 207 WRF, CR 2209, School QQ/RR naming, K-8
construction, SR 16/IGP groundbreaking, SR 16 widening hearings, CR 210
widening, Magnolia Oaks, FCE, Baptist SilverLeaf.

## 38. Category counts

| Category | Release 003 | Release 004 candidate |
|----------|------------:|----------------------:|
| Schools & Community | 10 | 14 |
| Roads & Traffic | 9 | 13 |
| Local Business | 6 | 7 |
| Utilities & Water | 6 | 11 |
| Emergency Preparedness | 3 | 3 |

## 39. Category usefulness

| Category | Release 003 | Release 004 candidate | Assessment |
|----------|------------:|----------------------:|------------|
| Schools & Community | 10 | 14 | STRONG — Magnolia Oaks arc now complete (construction → naming → opening) |
| Roads & Traffic | 9 | 13 | STRONG — FCE construction, Courtney Vista, SR 16 RCUT add current value |
| Local Business | 6 | 7 | GOOD — Baptist expansion adds healthcare-service depth |
| Utilities & Water | 6 | 11 | GOOD — annual report, Moody's, capital project add durable context |
| Emergency Preparedness | 3 | 3 | THIN but complete — no real storm threat exists to add |

Internal lenses: **Growth & Construction** and **Healthcare & Services** now
carry substantial resident value (FCE, Courtney Vista, Magnolia Oaks, Baptist
expansion). If those lenses continue to grow, they are reasonable future public
category candidates — but this task made no taxonomy change (per its boundary).

## 40. Before/after exception counts

| Metric | Before | After |
|--------|-------:|------:|
| Public items | 34 | 48 (004 candidate) |
| Latest | 10 | 12 |
| Timelines | 9 | 11 |
| NEEDS_MORE_RESEARCH | 106 | 75 |
| NEEDS_HUMAN_REVIEW | 56 | 79 |
| AUTO_PUBLISHABLE | 34 | 48 |
| EXCLUDE | 65 | 65 |
| High-priority tracked subjects without corpus item | 0 | 0 |
| Stale high-priority subjects (milestone escalation) | unmeasured | 3 tracked |
| Active search profiles (registry+adaptive) | 6 adaptive + 7 registry | +1 (FCE) |
| Research escalations resolved | 1 (Harris Teeter) | +7 subjects researched |
| Human-sensitive exceptions | 4 | 4 (preserved) |

Note: NEEDS_HUMAN_REVIEW rose because 32 reconciled items moved from
"research debt" into a decidable classification state (they need role/scope
decisions). That is triage, not regression — the 79 are genuine gates.

## 41. CURRENT_PUBLICATION_PLAN changes

Regenerated from Release 004 + updated `data/editorial/plan_inputs.yaml`:
reflects the 48-item candidate, resolved Magnolia/FCE/Bala's source checks,
the FY2027 TRIM capture (deferred for topic decision), reduced ready-next list,
and updated category gaps. `--check` PASS.

## 42. CURRENT_BRIEF changes

Regenerated from accepted adaptive state + current classifier: publication
counts now 48/79/75/65; milestone escalation state added; still reports the
last live run (`SJC-LIVE-20260807-2604`) as the data-cutoff reference.
`--check` PASS.

## 43. Targeted backtest reruns

`python3 scripts/hermes_backtest.py evaluate-all --backtest-id hermes-sjc-v1`
was rerun with the repaired matcher on the existing 66 completed weeks (no
weeks rewritten, no production mutation):
- RCR 0.933 (high-priority denominator unchanged).
- `school zoning / attendance boundaries` now found (was unmatchable).
- FCE remains the single miss — a feed-universe gap, not a reasoning failure.
- The acceptance/dedupe fixes were validated by new unit tests rather than a
  full replay, because they change state progression and the completed week
  history must not be rewritten to improve scores.

## 44. Production dry run

`python3 scripts/run_weekly.py` ran the two-source pilot in offline-fixture mode
(NBOR HTML + SJSO RSS fixtures, pinned SHA, no network):
- NBOR: health=accessible, 25 candidates, 0 errors.
- SJSO: health=accessible, 2 candidates, 0 errors.
- `bundle_verify.py` PASS; run status `completed`. Transient artifacts removed.

## 45. Safety validation

Programmatic check on Release 004: zero `SJC-SJSO-*` or sensitive
SilverLeaf-incident IDs; zero sensitive-title hits (arrest/shooting/murder/
minor/detainer/inmate/alleged). Crime/minor items remain `pending_review`.
Human-sensitive exception count unchanged (4).

## 46. Remaining human decisions

- **Deploy Release 004?** Not authorized in this task. Buddy decides after
  Task 34's review.
- **Public "Government & Taxes" topic decision** for FY2027 TRIM/budget content
  (verified corpus is ready).
- Review of the 79 NEEDS_HUMAN_REVIEW records (role/scope/context decisions)
  and the 75 remaining research records (mostly non-SilverLeaf NBOR/sensitive).
- Whether Growth & Construction / Healthcare & Services become public
  categories (future).

## 47. Readiness judgment

**READY_FOR_FIRST_SUPERVISED_WEEKLY_RUN.**

Supporting evidence: all six generalized backtest defects are fixed or
consciously addressed with regression tests; the production workflow matches
the documented authoritative sequence; routine research debt is materially
reduced (106 → 75); all accepted high-priority subjects have functioning
searches and corpus items; publication classification is stable (48
auto-publishable); Release 004 validates with zero warnings and no safety
leak; the production dry run succeeds; the scheduler remains disabled and a
real supervised weekly run is the correct next step under Task 34.

## 48. Recommended Task 34

**First real supervised weekly Hermes production run → finalize and deploy
Release 004.**

1. Execute one bounded real weekly cycle (approved sources + accepted profiles)
   on the SJC side using the hardened workflow.
2. Import/review the findings; resolve the genuine exceptions (79 human-review
   + 75 research) in bounded groups; confirm Bala's current status and any new
   tenant openings.
3. Finalize Release 004 with the week's fresh findings, refresh
   CURRENT_PUBLICATION_PLAN/BRIEF, and deploy only on explicit authorization.
4. Decide the Government & Taxes topic for FY2027 content.
5. Keep Ivy timer activation deferred until at least two clean supervised
   cycles complete.

## 49. SJC v1.1 recommendations

- Construction tracking with richer per-project milestone states.
- Stronger school-service presentation (address-level zone authority, DIR-010).
- Better retail-opening tracking (tenant confirmations before "opened" claims).
- Release archive + corrections workflow (ED-002).
- Continued FDOT project-page monitoring for FCE and SR 16.
- Category depth for Emergency Preparedness and Local Business as real
  developments justify it.

## 50. Ivy/VPS handoff

Infrastructure-owned work only, unchanged from Task 32: timer activation for
`sjc-weekly-001` remains gated behind two clean supervised cycles; runtime
credentials, resource limits, temporary storage, transfer/prune, backups,
logs, and monitoring remain Ivy-owned. No Ivy change performed.

## 51. Deferred v2 ideas

Live incident lane (DIR-003/004/005), PostGIS/geometric filtering (DIR-007),
generic SourceAdapter framework, universal Hermes runtime, full subscription
platform — all deferred per ROADMAP §5.

## 52. Files changed

**Code:** `scripts/hermes_backtest.py`, `scripts/live_adaptive.py`,
`scripts/static_release_common.py`.
**Registries:** `registry/sources.yaml`, `registry/search_profiles.yaml`,
`registry/silverleaf_mobility.yaml`.
**Docs:** `docs/hermes_weekly_entrypoint.md`, `docs/live_adaptive_operations.md`,
`docs/silverleaf_mobility_scope.md`, `prompts/sjc_weekly_ops_task.md`,
`BACKLOG.md`, `CURRENT_PUBLICATION_PLAN.md`, `CURRENT_BRIEF.md`.
**Data:** `data/intel_items/2026-08-09/task33_corpus.yaml` (new, 6 items),
`data/intel_items/2026-07-06/agentic_search_results.yaml` (Bala's fix),
reconciliation in 9 corpus files via `data/editorial/task33_reconciliation.yaml`
(new), 16 new `data/publication_decisions/*.yaml`,
`data/adaptive_discovery/accepted_state.yaml` (milestones),
`data/editorial/plan_inputs.yaml`.
**Tests:** `tests/test_hermes_backtest.py` (4 new), `tests/test_live_adaptive.py`
(3 new).
**Release/site:** `site/data/releases/SJC-REL-2026-08-004/`, rebuilt `site/`.
**Logs/reports:** `logs/agents/.../2026-08-09_task33-...md`,
`logs/runs/weekly/2026-08-09_task33-...md`, `reports/briefs/20260809T044234Z.md`,
this report. (Reports 32 pre-existing untracked.)

## 53. Tests changed/added

+7 tests (4 backtest, 3 production). Total suite: 332 passing (was 325).

## 54. Validation results

```
python3 -m pytest tests/ -q          → PASS, 332
python3 scripts/validate.py          → ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS (0 errors)
python3 scripts/validate_silverleaf_scope.py   → PASS (0/0)
python3 scripts/validate_silverleaf_mobility.py → PASS (0 errors)
python3 scripts/build_current_brief.py --check → PASS
python3 scripts/build_publication_plan.py --check → PASS
python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-004 --check → PASS (0 warnings)
python3 scripts/build_static_site.py --list-routes → 75 routes
python3 scripts/bundle_verify.py --bundle <dry-run bundle> → PASS
git diff --check                    → clean
git status --short                  → 88 M, 38 ?? (all Task 33 + pre-existing Task 32 report)
```

## 55. Proposed commit grouping

1. `fix: harden Hermes workflow (acceptance asymmetry, evaluator matcher, entity dedupe, stale-milestone escalation)` — `scripts/hermes_backtest.py`, `scripts/live_adaptive.py`, `tests/`, `data/adaptive_discovery/accepted_state.yaml`.
2. `feat: add FDOT/FCE project coverage and recurring search profile` — `registry/sources.yaml`, `registry/search_profiles.yaml`, `registry/silverleaf_mobility.yaml`, `docs/silverleaf_mobility_scope.md`.
3. `docs: align weekly workflow with backtest-proven sequence` — `docs/hermes_weekly_entrypoint.md`, `docs/live_adaptive_operations.md`, `prompts/sjc_weekly_ops_task.md`.
4. `data: resolve PUB-004 backlog and deepen corpus (Task 33)` — `data/intel_items/2026-08-09/`, `data/editorial/task33_reconciliation.yaml`, reconciled corpus files, `data/publication_decisions/`, `data/editorial/plan_inputs.yaml`.
5. `data: build Release 004 candidate (48 items)` — `site/data/releases/SJC-REL-2026-08-004/`, rebuilt `site/`, `CURRENT_PUBLICATION_PLAN.md`, `CURRENT_BRIEF.md`.
6. `docs: record Task 33 and update backlog` — `BACKLOG.md`, `logs/`, this report.

## 56. Final Git status

`master` @ `87a09597d53ef6b993a60efa5ab52ba85bf6d036` (unchanged HEAD). Working
tree contains all Task 33 changes plus the pre-existing Task 32 report. Nothing
committed, pushed, deployed, or scheduled. `git diff --check` clean.

## 57. Final task status

| Success criterion | Status |
|-------------------|--------|
| Task 32 generalized defects addressed | COMPLETE (6 defects, regression tests) |
| Evaluator matching materially safer | COMPLETE (zoning now found; bare-water FP removed) |
| Duplicate adaptive proposals reduced | COMPLETE (idempotent apply_proposal) |
| Official transportation coverage improved | COMPLETE (FCE p=5639 + profile) |
| Stale high-priority subjects trigger follow-up | COMPLETE (milestone escalation) |
| Production incorporates backtest-proven behavior | COMPLETE (13-step authoritative sequence) |
| Unresolved publication backlog materially reduced | COMPLETE (106 → 75 research; 34 → 48 auto-publishable) |
| Routine evidence work no longer waits on Buddy | COMPLETE (32 reconciled + 6 created) |
| Genuine human gates intact | COMPLETE (crime/minor/topic-gate preserved) |
| Magnolia Oaks coverage current | COMPLETE (Aug 10, 1,300 students, K-7) |
| FCE/I-95 coverage materially improved | COMPLETE (official construction record + timeline) |
| CR 2209/CR 210/SR16 current enough for resident use | COMPLETE (Courtney Vista + RCUT + completion records) |
| Baptist coverage reflects current services | COMPLETE (Ortho Aug, ER Sep) |
| Silverleaf Market coverage deeper | PARTIAL (tenant dates still reporting-only) |
| Harris Teeter uncertainty remains honest | COMPLETE (qualified retained) |
| Adaptive high-priority subjects have corpus representation | COMPLETE (0 lead-only) |
| Timelines improve | COMPLETE (9 → 11 anchors; milestones deepen arcs) |
| Release 004 candidate exists | COMPLETE (48 items) |
| Release 004 validates | COMPLETE (0 warnings, safety-clean) |
| CURRENT_PUBLICATION_PLAN accurate | COMPLETE |
| CURRENT_BRIEF reflects operational state | COMPLETE |
| Targeted backtest regression passes | COMPLETE (RCR 0.933; zoning found) |
| Production dry run passes | COMPLETE (bundle PASS) |
| Safety boundaries intact | COMPLETE (no sensitive items in 004) |
| READY_FOR_FIRST_SUPERVISED_WEEKLY_RUN | COMPLETE |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP. The production Hermes
workflow is hardened, the publication backlog is materially reduced, and the
Release 004 candidate is built, validated, and safety-clean locally. The next
step is the first real supervised weekly production run (Task 34), human review
of the genuine exceptions, Release 004 finalization, and an explicit deployment
decision — none of which occurred here.
