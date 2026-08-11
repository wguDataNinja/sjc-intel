# Agent log — Task 33 production hardening and corpus deepening

**Date:** 2026-08-09
**Agent:** sjc-intel-architect
**Mode:** supervised
**Task:** `tasks/33-production-hardening-and-corpus-deepening.md`

## Work performed

### Phase A — production workflow hardening (code + tests)
1. **Acceptance asymmetry (defect #1):** `scripts/hermes_backtest.py` now
   duplicate-rejects only `entity` proposals for an already-tracked subject;
   `search_profile`/milestone/timeline updates for an existing entity are
   accepted. Production `scripts/live_adaptive.py` `evaluate_proposals` is
   type-aware (BUCKET_TO_TYPE map) so an entity-first subject can later gain a
   profile. Regression tests added.
2. **Evaluator matcher (defect #2):** replaced the over-aggressive stop list in
   `_subject_keywords` with a majority-token matcher (`_token_hit`, ceil 2/3)
   plus precise alias phrases. "school zoning / attendance boundaries" is now
   matchable; bare "water" no longer produces a false found. Rerun of
   `evaluate-all` now finds zoning; only FCE remains missed (genuine feed gap).
3. **Entity/proposal dedupe (defect #3):** `apply_proposal` dedupes entity and
   search-profile creation by normalized label; milestone acceptance added to
   production `review()` bucket map.
4. **FDOT/FCE coverage (defect #4):** verified the FDOT final-segment project
   page (`nflroads.com/ProjectDetails?p=5639`, $205M Mastec contract, early
   2026 start, late 2030/early 2031 completion); added it to the mobility
   registry, the FDOT source notes, and a new `sl_fce_fdot` recurring search
   profile.
5. **Stale-milestone escalation (defect #5):** `resident_coverage_editor` now
   emits SEARCH_NOW findings for accepted subjects whose expected milestone is
   overdue with no fresh coverage.
6. **Production/backtest alignment (defect #6):** documented the authoritative
   13-step production sequence in `docs/hermes_weekly_entrypoint.md`; aligned
   `prompts/sjc_weekly_ops_task.md` with Model B fields, stale-milestone
   escalation, and FDOT project-page monitoring; added a Task 33 note to
   `docs/live_adaptive_operations.md`.

### Phase B — PUB-004 backlog triage + bounded research
- Triaged the 106 NEEDS_MORE_RESEARCH + 56 NEEDS_HUMAN_REVIEW records by reason
  and grouped them (SOURCE_CHECK / IDENTITY / LOCATION / CORROBORATION /
  TIMELINE_MERGE / NOT_RELEVANT / SENSITIVE_HUMAN_REVIEW / etc.).
- Bounded public-source research on high-priority subjects:
  - **Magnolia Oaks:** SJCSD first-party confirmation (opened, K-7 first year,
    1,300 students, first day Aug 10; K-8 QQ Plan C-Modified approved 11/18/25;
    live 2026-27 zone locator).
  - **Baptist SilverLeaf:** first-party Baptist Health page confirms Orthopedics
    opening Aug 2026 and Emergency Center opening Sep 2026.
  - **FCE:** official FDOT/NFLRoads project page (contract, cost, schedule).
  - **FY2027 budget/TRIM:** county OMB page (recommended budget 7/21/26, TRIM
    mid-Aug, first hearing Sep 3).
  - **Courtney Vista Drive:** county completion record (CR 2209–Silverleaf
    Parkway link).
  - **SR 16 RCUT:** county traffic-pattern change (mid-late Sep).
  - **Bala's:** located the working article URL (404 resolved) and verified.
- Created 6 new verified corpus items (`data/intel_items/2026-08-09/`), 16 new
  publication decisions, reconciled 32 low-risk official records to verified
  (`data/editorial/task33_reconciliation.yaml`).

### Release 004 candidate + state docs
- Built `SJC-REL-2026-08-004` locally: 48 items (12 latest, 24 browse, 11
  timeline, 1 context), 75 routes, zero warnings. Not deployed.
- Regenerated `CURRENT_PUBLICATION_PLAN.md` and `CURRENT_BRIEF.md`.
- Updated `registry/search_profiles.yaml`, `registry/silverleaf_mobility.yaml`,
  `registry/sources.yaml`, `BACKLOG.md`, `docs/`.

## Friction / decisions
- The publication-policy classifier rose NEEDS_HUMAN_REVIEW when reconciled
  items gained verified status but still need editorial role/scope decisions —
  this is correct triage (research debt became decidable classification), not
  regression. Two medium-sensitivity NBOR items were accidentally reconciled
  and reverted.
- FY2027 budget item verified in corpus but held out of Release 004 by the
  standing "Government & Taxes topic decision" gate (recorded as `defer`).

## Files changed
See `reports/33-production-hardening-and-corpus-deepening.md` §Files changed.

## Validation
All 332 tests pass; `validate.py` ALL PASSED; `validate_publication_corpus.py`
0 errors; scope/mobility validators PASS; CURRENT_BRIEF/PLAN `--check` PASS;
`git diff --check` clean; Release 004 `--check` PASS (0 warnings); bundle
verify PASS.
