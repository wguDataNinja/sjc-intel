# Task 32 — Post-Launch Operations and Forward Plan

**Task identity:** 32-post-launch-operations-and-forward-plan.md
**Date:** 2026-08-08
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Mode:** supervised
**Final status:** COMPLETE — analysis and forward plan; no production changes

**Starting premise (per Buddy):** Release `SJC-REL-2026-08-003` is **live,
deployed, and verified** at https://wgudataninja.github.io/sjc-intel/ (Pages
run `31254375733`, SHA `87a09597`, 34 items). v1 / Model B is an operating
product. This task does not re-litigate deployment; it answers seven forward
questions.

---

## 1. Executive result

SilverLeaf Brief is now a **live, useful, but young** product. It genuinely
answers "what is changing around SilverLeaf" for schools, roads, retail,
healthcare, utilities, and preparedness, and it does so with honest source
links, dates, and qualified uncertainty. It is not yet a *complete* resident
newsroom: the 66-week Hermes backtest proved the workflow is capable, but also
exposed four concrete defects that should be fixed before normal weekly
operation, and the live product has real coverage gaps (First Coast Expressway,
school-zone finality, FY2027 TRIM season, live road incidents, maps).

Recommended posture: keep v1 live; run the next phase as **supervised weekly
operation on the file-first SJC side**, fix the backtest-revealed defects, and
resolve the publication-exceptions backlog (PUB-004) to deepen the corpus — all
before enabling any Ivy timer. Do **not** activate autonomous VPS scheduling
yet. SJC v1.1 = a reliable weekly rhythm + deeper, current, resident-local
coverage + the geographic registry completed with real geometry.

---

## 2. Starting Git and operating state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `87a09597d53ef6b993a60efa5ab52ba85bf6d036` |
| Origin | synchronized (0 ahead / 0 behind), working tree clean |
| Public product | Live Release `SJC-REL-2026-08-003` (34 items, 59 routes) |
| Deployment | GitHub Pages run `31254375733` success; verified end-to-end + isolation |
| Weekly cadence | LAST_RUN 2026-07-04T10:00:00Z — **no live weekly run since launch** |
| Weekly task | `deploy/sjc-weekly-task.yaml` → `enabled: false`, two-source pilot (NBOR + SJSO) |
| Backtest | Full 66-week Hermes replay completed; RCR 0.933; provenance manifest committed |

---

## 3. Q1 — Is the live 34-item product actually useful to a SilverLeaf resident?

**Yes, with clear limits.**

**What works (verified against the live site):**
- **Answers the top resident questions.** Schools (Magnolia Oaks opening,
  Hallowes Cove, zoning arc, funding), roads (CR 16A closure, CR 210
  completion, CR 2209, SR 16/IGP), retail (Publix, Silverleaf Market, possible
  Harris Teeter qualified), healthcare (Baptist campus), utilities (Phase III
  water active, SR 207 WRF, service-line inventory), preparedness (hurricane,
  Alert St. Johns). A resident arriving today learns the school is opening,
  the grocery question is "unconfirmed," the water rule is active, and a road
  is closed this weekend.
- **Trust mechanics are right:** every item links to a public source (12/12
  spot checks HTTP 200), dates are explicit, "Reviewed" is defined honestly,
  and the possible-Harris-Teeter item carries a visible "Tenant unconfirmed"
  label. No crime/minor material leaked.
- **Browse + timelines give durable value** the four-item site never had: the
  Magnolia Oaks construction→naming→opening arc, CR 2209, the water-shortage
  subject, Publix history.
- **Category browsing is non-empty everywhere** (Schools 10, Roads 9, Local
  Business 6, Utilities 6, Emergency 3).

**What is not yet useful / weak:**
- **Currentness decay risk.** Latest includes items from May–June (water
  shortage, hurricane, service-line, SR 207). They are active/seasonal and
  labeled, but a site with no *new* weekly content will age badly; the product
  needs a supervised weekly cycle soon, not later.
- **Thin categories.** Emergency Preparedness (3) and Local Business (6) are
  minimal; Healthcare is two items. "Useful" today, "sad" if not grown.
- **No live-incident lane.** Road closures are static notices, not live
  conditions; the product deliberately avoids real-time claims (correct for
  v1, a v1.1 opportunity).
- **Missing high-value subjects.** First Coast Expressway is absent from the
  live corpus (backtest proved it is a feed gap, not a reasoning gap); the
  FY2027 TRIM season is not yet covered; school-zone finality (DIR-010) is
  pending; Bala's second location is still a source-check item.
- **No maps, no search by timeline, no corrections page** (ED-002 deferred).

**Judgment:** the product is **genuinely useful for "what changed and what to
keep watching"** — a real neighborhood briefing — and is materially better than
any local alternative for SilverLeaf specifically. Its usefulness will depend on
(1) weekly freshness and (2) closing the enumerated coverage gaps. It is not a
complete county-news product, and it does not claim to be.

---

## 4. Q2 — What did the completed 66-week Hermes backtest really prove or expose?

Evidence: `data/hermes_backtests/hermes-sjc-v1/final/HERMES_BACKTEST_FINAL_REPORT.md`,
`final/comparison.yaml`, `final/backtest_provenance.yaml` (committed, SHA-anchored).

**What it proved (strong):**
- **The workflow can operate the newsroom.** 66/66 weeks completed on
  historical-visible state with **zero future-data leakage**, zero production
  mutation, budgets respected every week.
- **Resident Coverage Recall 0.933** (14/15 high-priority subjects+lanes).
  Found: School QQ→Magnolia Oaks, CR 2209, CR 210, SR 16/IGP, Baptist, Publix,
  grocery center (qualified), SR 207 WRF, Phase III water, hurricane, all 5
  high lanes + preparedness.
- **Zero discovery lag** for every subject with dated feed evidence; the
  School QQ→Magnolia alias and Hallowes Cove lead→confirmation arcs formed
  naturally.
- **Safety gates held** on all 7 sensitive-item weeks (crime, minors, DUI,
  rescue) — zero sensitive proposals submitted.
- **Adaptive learning works:** 18 search profiles; profiles created one week
  reliably caught the subject's next milestone (School QQ→naming, Hallowes
  Cove→opening, CR 2209→opened, budget→TRIM/hearing).
- **The evaluator beat the manual workflow on structure:** attendance zoning as
  a tracked subject, SR 207 WRF tracked at first evidence (Dec 2025 vs the
  manual workflow's Jun 2026), the healthcare lane raised from the Ascension
  item, and BCC/NBOR noise filtering.

**What it exposed (the honest defects):**
1. **Acceptance-policy asymmetry** — a `search_profile` proposal for an
   already-tracked entity is duplicate-rejected, so an entity-first subject can
   never gain a profile later (SR 16/IGP). Milestone/timeline updates for the
   same subject are allowed. Inconsistent.
2. **Hidden-evaluator keyword defects** — "school zoning / attendance
   boundaries" is unmatchable (all its tokens are stop-listed) and bare "water"
   caused false "found" marks. The **RCR 0.933 understates the true misses**
   (zoning was tracked, FCE genuinely absent) but the matcher itself needs
   repair.
3. **State dedupe gap** — the budget entity exists twice in carried state
   (pilot + full-run proposals in different temporal order); `apply_proposal`
   needs idempotent label dedupe.
4. **Feed-universe gaps** — no First Coast Expressway, no per-address watering
   detail, no BCC attachments. The replay could only discover what the dated
   feed contained; the manual workflow's live-search FCE leads were invisible.
5. **Milestone hygiene** — overdue milestones (School QQ naming/boundaries) had
   no escalation path to force verification.

**Bottom line:** the backtest is strong evidence that **Hermes can run a
supervised resident newsroom** and that the two high-priority "misses" are
explainable (feed gap + matcher defect). It is not evidence that Hermes can run
it *autonomously*, nor that today's live product is complete — those are the
next two questions.

---

## 5. Q3 — Generalized defects to fix before normal weekly operation

Ranked, each with fix + owner:

| # | Defect | Fix | Owner |
|---|--------|-----|-------|
| 1 | Acceptance asymmetry (search profile for tracked entity rejected) | Allow `search_profile` proposals for already-tracked entities; require entity OR profile, not both, for promotion | SJC (hermes_backtest + production acceptance policy) |
| 2 | Evaluator keyword defects (zoning unmatchable; "water" false positives) | Contextual token handling + non-stop medium-priority matching | SJC |
| 3 | `apply_proposal` non-idempotent entity creation | Dedupe entity creation by normalized label | SJC |
| 4 | FCE / FDOT project-page coverage missing | Add FDOT District Two project pages to monitored sources + recurring profile; re-run evaluator | SJC source-watch |
| 5 | No stale-milestone escalation path | Add a "stale milestone → SEARCH_NOW" editor action | SJC |
| 6 | Production weekly prompt predates Model B | Align `prompts/sjc_weekly_ops_task.md` and the weekly bundle contract with `role`/`qualified`/corroboration fields | SJC |
| 7 | Weekly cadence has not run since 2026-07-04 | Run a bounded **supervised** weekly cycle locally (not Ivy), import findings, review, and refresh the release | SJC operator |
| 8 | PUB-004 exceptions backlog (69 research + 51 human-review) | Resolve in bounded policy-driven groups (Model B policy + corroboration), no bulk promotion | SJC |
| 9 | Bala's location/opening unresolved (404 URL) | Bounded live-search verification (retrospective evidence) | SJC |
| 10 | Site freshness + corrections path | A "Report an issue"/corrections policy (ED-002) and a clear weekly-freshness signal | SJC + Buddy |

**Gate before normal weekly operation:** fix #1–#6, run one supervised weekly
cycle (#7), and only then consider an Ivy timer. #8–#10 are product-depth, not
blocking gates.

---

## 6. Q4 — Is the real production Hermes weekly workflow ready to run?

**Ready to run supervised, on the SJC side; not ready to run autonomously from
Ivy.**

- **What is ready:** the file-first weekly loop (known-source capture →
  bounded discovery → research escalation → strategist/editor → independent
  evaluation → human review → release) is implemented and validated (Tasks
  23–26, 29). The publication pipeline is live. The backtest proved the agent
  workflow under supervision. The Pages deploy lane is automated and proven.
- **What is not ready:**
  - No weekly run has executed against the **live** product since launch (the
    backtest ran a simulation, not production state).
  - The production weekly contract (`prompts/sjc_weekly_ops_task.md`) predates
    the Model B role/qualified/corroboration fields; a run would need the
    reconciliation in Q3-#6.
  - `deploy/sjc-weekly-task.yaml` is `enabled: false`; the two-source pilot
    (NBOR + SJSO) lacks a scripted county-news capture; Ivy timer activation is
    a separate privileged gate (correctly).
  - The defects in Q3-#1–#6 are unapplied to production tooling.
- **Recommended:** proceed as **supervised weekly operation on the Mac/SJC
  side** (bounded, receipt-backed, human-reviewed), not autonomous. Keep Ivy
  activation deferred until at least two consecutive clean supervised cycles
  complete and the defects are fixed. The judgment from the backtest final
  report — **READY_FOR_SUPERVISED_WEEKLY** — is accurate and is the posture to
  adopt.

---

## 7. Q5 — What should SJC v1.1 become?

**v1.1 = a reliable weekly rhythm plus a deeper, current, resident-local
product.** Specifics:

1. **Weekly operations as the center of gravity.** A supervised weekly cycle
   (monitor → discover → research → review → release) that keeps Latest fresh.
   This is the single highest-leverage change for usefulness.
2. **Close the coverage gaps that matter to residents:**
   - Confirm the Magnolia Oaks opening date + attendance zone (DIR-010).
   - First Coast Expressway status/timeline (add FDOT source).
   - FY2027 TRIM/budget season (Aug–Sep 2026) — the next real news cycle.
   - Baptist campus services/expansion; Silverleaf Market tenant timing.
   - Bala's, mini-golf DRC outcome.
3. **Complete the geographic registry with real, reviewed geometry** (DIR-001),
   then add maps / "is this relevant to me" filtering (DIR-007) — the most
   differentiating v1.1 feature after freshness.
4. **Product mechanics:** corrections/report-issue path (ED-002), a dedicated
   timeline presentation (timelines exist as a role but not a first-class
   view), category depth for Emergency Preparedness and Local Business, and an
   explicit "last updated" freshness signal on the homepage.
5. **Live-incident lane (stretch):** road closures as live conditions (CR 16A,
   I-95/SR 16) via an approved incident source (DIR-003/004/005) — carefully,
   keeping the "not an alert service" boundary.
6. **Backtest-informed hygiene:** fix the acceptance/evaluator/state defects so
   the backtest→production loop is trusted.

**Non-goals for v1.1:** no accounts, no subscriptions, no real-time alerts, no
full county-news coverage, no autonomous publication.

---

## 8. Q6 — What belongs in Ivy/VPS rather than SJC?

The **authority boundary stays**: SJC owns the file-first corpus, review,
publication, and release; Ivy/VPS owns only bounded execution transport.

| Lane | SJC (Mac, file-first) | Ivy/VPS |
|------|----------------------|---------|
| Weekly run | Import + review bundles, accept/reject, build releases, CURRENT_BRIEF/PLAN | Run `scripts/run_weekly.py` on the timer, fetch approved sources, produce the versioned transfer bundle, retry/log, 14-day retention |
| Deployment | Commit + push (Pages auto-deploys site/) — already the lane | Nothing; Pages is GitHub-hosted |
| PostgreSQL | Dormant-future-ready; file authority preserved | If adopted later, host + migrate; not now |
| Scheduler | No cron/launchd | Ivy systemd timer for `sjc-weekly-001` — **only after** supervised cycles pass and activation gates clear |
| Secrets/credentials | None stored | Deploy-side only, via Ivy's privileged packet |

**Concrete Ivy handoff (from reports 26/30):** deploy the exact pushed SHA
(`87a09597`) to `/home/scraper/apps/sjc-intel`, retain `deploy/sjc-weekly-task.yaml`
with `enabled: false`, invoke `python3 scripts/run_weekly.py` in the declared
Wed 01:30–03:00 UTC window with the 120-min/120-fetch/2-retry/public-HTTP
bounds. **Do not enable the timer yet.**

---

## 9. Q7 — What exactly should the next three tasks be?

Recommended sequence (each bounded, each producing a task/report pair):

**Task 33 — Fix the production weekly workflow and backtest defects**
`fix: align production weekly workflow with Model B and repair backtest defects`
- Apply Q3-#1–#6: acceptance-policy asymmetry, evaluator keyword repair,
  `apply_proposal` label dedupe, FDOT/FCE source + profile, stale-milestone
  escalation, and reconcile `prompts/sjc_weekly_ops_task.md` + the weekly
  bundle contract with role/qualified/corroboration.
- Re-run the backtest evaluator and confirm RCR is computed correctly with the
  repaired matcher; record the corrected FCE/zoning outcome.
- Output: `tasks/33-…`, `reports/33-…`.

**Task 34 — Resolve the publication-exceptions backlog (PUB-004) and deepen the corpus**
- In bounded, policy-driven groups, resolve the 69 research exceptions and 51
  human-review exceptions surfaced by the Model B classifier: verify, add
  corroboration, or qualify; no bulk promotion. Target a deepened Browse/Latest
  (~40–44 items) covering FCE, school-zone finality, FY2027 TRIM, Baptist
  services, and Silverleaf Market tenants.
- Output: a decision-ready review packet and a proposed Release 004.

**Task 35 — Run the first supervised weekly cycle and publish Release 004**
- Execute one real, bounded weekly run against the live product (known sources
  + accepted profiles), import/review findings, resolve Bala's + current-status
  source checks, refresh CURRENT_BRIEF/PLAN, and build + push **Release 004**
  through the now-proven Pages lane.
- This is the first "normal weekly operation" proof after launch and the gate
  for any future Ivy activation.
- Output: `reports/35-…`, run logs, Release 004 deployed.

(These three follow Task 32. If a corrections policy — ED-002 — is wanted
before public issue-reporting, fold a minimal version into Task 34.)

---

## 10. Validation

```
python3 -m pytest tests/ -q            → PASS, 325
python3 scripts/validate.py            → ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS (0 errors)
python3 scripts/validate_silverleaf_scope.py   → PASS (0/0)
python3 scripts/validate_silverleaf_mobility.py → PASS (0 errors)
python3 scripts/build_current_brief.py --check → PASS
python3 scripts/build_publication_plan.py --check → PASS
git diff --check                       → clean
git status --short                     → clean (this task made no changes)
```

No files were changed by this task (analysis only).

---

## 11. Final Git status

`master` @ `87a09597d53ef6b993a60efa5ab52ba85bf6d036`, synchronized with
`origin/master`, working tree clean. Release 003 live. No commit or push.

---

## 12. Final task status

| Question | Answer |
|----------|--------|
| 1. Live product useful? | Yes, genuinely, with enumerated limits (freshness, category depth, FCE/zone/TRIM gaps) |
| 2. What did the backtest prove/expose? | Proved supervised capability + RCR 0.933 + zero leakage; exposed 5 defects (acceptance asymmetry, evaluator matcher, state dedupe, feed gaps, milestone hygiene) |
| 3. Defects before weekly operation | 10 ranked items; #1–#6 are the operational gate |
| 4. Production weekly ready? | Ready supervised on SJC side; not autonomous/Ivy |
| 5. SJC v1.1 | Weekly rhythm + deeper/current/local coverage + completed geography + corrections/timeline/freshness mechanics |
| 6. Ivy vs SJC | SJC owns authority; Ivy owns bounded bundle execution + timer (deferred); Pages owns deployment |
| 7. Next three tasks | Task 33 (fix workflow+backtest defects), Task 34 (PUB-004 backlog → Release 004 candidate), Task 35 (first supervised weekly run → deploy Release 004) |

**Final status vocabulary:** COMPLETE. v1 / Model B is live and verified. The
path forward is supervised weekly operation on the file-first SJC side, the
backtest-informed defect fixes, and a deepened, fresh corpus — before any
autonomous Ivy scheduling.
