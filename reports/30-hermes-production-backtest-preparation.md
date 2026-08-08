# Task 30 — Prepare the Real Hermes Historical Production Backtest

**Task identity:** 30-hermes-production-backtest-preparation.md
**Date:** 2026-08-07
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Mode:** supervised
**Final status:** COMPLETE — preparation and a 7-week real-Hermes proof executed;
the full 66-week replay is ready to hand to Hermes

**Scope honored:** no production corpus, publication, review, site, deployment,
PostgreSQL, Ivy, or scheduler changes. The Hermes backtest ran entirely inside
`data/hermes_backtests/hermes-sjc-v1/`. No production state was mutated.

---

## 1. Executive result

Prepared a historically isolated, **Hermes-operated** weekly simulation in which
Hermes behaves as though SJC_Intel had been running naturally from 2025-05-05 to
2026-08-03. This is deliberately *not* another deterministic replay of a curated
fixture (that was Task 22); it is the real production-style agent workflow
executed against historical-visible state.

Delivered:

- an isolated workspace `data/hermes_backtests/hermes-sjc-v1/` (config, seed,
  dated feed, weekly packets, monthly syntheses, publication snapshots);
- a durable Hermes weekly instruction packet
  `prompts/hermes_historical_weekly_task.md`;
- reusable infrastructure `scripts/hermes_backtest.py`
  (build-feed / assemble-week / ingest-week / evaluate-week / evaluate-all /
  snapshot / monthly);
- a simulated acceptance policy, a hidden evaluator (Resident Coverage
  Recall), historical publication snapshots, budget/stop controls, and
  restart/resume support;
- a **7-week real-Hermes proof run** that discovered School QQ → Magnolia Oaks
  Academy (alias learned), CR 2209, SR 16/IGP, the possible-Harris-Teeter
  grocery center, Publix, Baptist, and SR 207 WRF, built 5 coverage lanes and 6
  search profiles, and produced **Resident Coverage Recall 0.867** on
  high-priority targets over the sampled weeks (all misses were subjects whose
  evidence weeks were outside the pilot sample);
- the exact copy-paste Hermes instruction for the full 66-week replay (§32–33).

Key validation: 320 tests pass; the backtest root is fully isolated (a test
proves the infrastructure never writes a production path); the full-run
instruction requires no further architecture session.

---

## 2. Starting Git/repository state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` |
| Working tree | Dirty (pre-existing Task 27/28/29 artifacts uncommitted) |
| Prior backtest | `data/backtests/task22_replay/` (66-week deterministic replay, completed) |
| Hermes backtest root | `data/hermes_backtests/hermes-sjc-v1/` (new, isolated) |

---

## 3. Prior backtest infrastructure inspected

- `data/backtests/task22_replay/` — config, `replay_evidence.yaml`, weeks/,
  months/, visible_state/, final/ (coverage_health + evaluation).
- `scripts/adaptive_backtest.py` — the deterministic harness (state_for,
  generate, evaluate, run_week, metrics).
- `scripts/run_historical_week.py`, `run_historical_backtest.py`,
  `build_historical_state.py`, `evaluate_historical_backtest.py`,
  `init_historical_backtest.py`.
- `docs/adaptive_discovery_backtest.md`, `reports/22-…`, `reports/21-…`.
- `schemas/adaptive_proposal.schema.yaml` (proposal contract).
- `scripts/live_adaptive.py` durable state shape (entities, aliases,
  search_profiles, lanes, milestones, timelines).

---

## 4. What Task 22 already provides

Task 22 provides the authoritative, reusable foundation:

- **Historical-visible state** — `state_for(cutoff)` rebuilds state from seed +
  accepted transitions with availability at or before the cutoff.
- **Availability-date rules** — `available_on` gates visibility; no future
  aliases leak backward.
- **Simulated clock** — every report records simulated week start/end.
- **Isolated backtest root** — `data/backtests/<id>/` never touches production.
- **Generator/evaluator separation** — the strategist proposes; the evaluator
  independently accepts/rejects; the baseline is never handed to the generator.
- **Proposal + promotion system** — entity/alias/source/search_profile/
  milestone/timeline_reconciliation/coverage_lane with the schema contract.
- **Future-data leakage controls** — date-filtered evidence; tested.
- **Resident Coverage Recall** — baseline-declared metric over high-priority
  subjects and lanes.
- **Weekly/monthly/final artifact contracts.**

---

## 5. What real Hermes backtesting adds

Task 22's `generate()` is deterministic over a curated evidence fixture. Task 30
replaces the reasoning layer with **Hermes itself**:

| Concern | Task 22 | Task 30 |
|---------|---------|---------|
| Weekly reasoning | deterministic `generate()` | Hermes reads the packet and reasons (monitor → find → resolve → propose → report) |
| Evidence | `replay_evidence.yaml` fixture | dated feed derived from the real corpus + documented overrides |
| Search | frozen fixture rows keyed by `available_on` | Hermes executes accepted search profiles against that week's dated feed |
| Identity | rule-based alias proposal | Hermes resolves identities using only pre-cutoff evidence |
| Resident editor | lane proposal facet | Hermes writes `coverage_editor.yaml` gap findings |
| Research escalation | not present | Hermes writes `research.yaml` (bounded, retrospective-labeled) |
| Acceptance | rule-based evaluator | simulated reviewer policy applied by infrastructure (Hermes cannot self-approve) |
| Hidden comparison | metrics() over baseline | `evaluate_all` over the hidden subject set, run after Hermes completes |

Task 22 components that remain authoritative and reused: isolation root
convention, availability/clock model, proposal schema, generator/evaluator
separation, RCR definition, leakage rules. Components adapted: evidence source
(corpus-derived feed), reasoning engine (Hermes), research escalation,
coverage editor contract, simulated acceptance, and the side-by-side
publication comparison.

---

## 6. Historical period recommendation

**2025-05-05 → 2026-08-03, weekly (66 intervals).**

Rationale: the earliest dated SilverLeaf-relevant public record in the corpus is
the K-8 School QQ topping-out article (published 2025-05-07). The CR 2209 /
SR 16 / CR 210 backfill arc begins August 2025; the grocery-center proposal
(Dec 2025), Publix opening (Mar 2026), Baptist opening (Jun 2026), and Magnolia
Oaks name/opening (Jul–Aug 2026) complete the story. Starting earlier has no
meaningful SilverLeaf signal; ending later would drag the feed into records
beyond the current reviewable corpus. Weekly cadence is required (the task
explicitly forbids monthly jumps); monthly syntheses summarize the weekly
outputs.

---

## 7. Seed-state design

`data/hermes_backtests/hermes-sjc-v1/seed.yaml` (available_on 2025-05-05):

- **Sources (defensible as known at start):** county news; school district
  (main/news/new-schools family); utility department; NBOR public notices; BCC
  calendar; P&Z boards; Emergency Management; SJRWMD watering restrictions;
  FDOT District Two/NFLRoads; NWS Jacksonville; St. Johns Citizen (established
  local media); property appraiser; tax collector; budget transparency.
- **Entities:** only the general context entity "SilverLeaf master-planned
  community". No School QQ, no Baptist, no Harris Teeter, no Publix, no CR 2209,
  no expressway — those must be discovered naturally.
- **Search profiles / lanes / milestones / timelines:** none.

Deliberately not seeded: current `registry/tracked_entities.yaml`, current
`data/adaptive_discovery/accepted_state.yaml`, Task 20/28 conclusions, and all
present-day aliases and profiles.

---

## 8. Historical knowledge availability

Hermes knows only what the **dated feed** gives it for its simulated week plus
its carried-forward state. The feed is derived from the production corpus
(`data/intel_items/**` + `data/monthly/*/discovered_items.yaml` via the Task 29
shared read path) placed in each simulated publication week by the record's
`source_published_at` (fallback `discovered_at`). This is the historically
reproducible layer: dated corpus records, source events, RSS records, and
publication dates. One documented override (`feed/overrides.yaml`) adds the
Magnolia Oaks opening (2026-07-22), which is historically real but exists in the
repo only as a live-search lead, not a dated corpus item.

Feed metrics: **223 unique dated records across 66 weeks** (deduped; NBOR
duplicate captures and SJC-* legacy copies are dropped). Sensitive items
(crime/minor) are present in the feed so Hermes must recognize and exclude
them; the simulated acceptance rejects medium/high sensitivity.

---

## 9. Search/retrieval limitations

The simulation cannot ask today's search engine what it "would have returned"
in 2025. Two evidence classes are distinguished:

- **Historically reproducible** — the dated feed above. This is the only
  evidence Hermes may treat as "what the sources published that week." Search
  profiles are executed by scanning that week's `feed/all.yaml` for items
  matching the profile queries — an explicit stand-in for live retrieval.
- **Present-day retrospective** — labeled `retrospective_evidence` in
  `research.yaml`, allowed only as bounded research leads with a publication
  cutoff at the simulated week end. Default `present_day_search.enabled:
  false`; when enabled, results must be date-cutoff filtered and are never
  treated as evidence Hermes would have seen that week.

Rules are encoded in the weekly task packet (§9 boundaries) and the config.
This limitation is explicitly recorded in the feed summary and every weekly
report.

---

## 10. Hermes backtest workspace

`data/hermes_backtests/hermes-sjc-v1/`:

```
config.yaml            period, cadence, budgets, acceptance, hidden subjects
seed.yaml              defensible start state
feed/
  overrides.yaml       documented non-corpus dated records
  summary.yaml
  weeks/YYYY-MM-DD.yaml
weeks/YYYY-MM-DD/
  starting_state.yaml  feed/monitored.yaml  feed/all.yaml  budgets.yaml
  hermes_task.md       meta.yaml
  findings.yaml  proposals.yaml  coverage_editor.yaml  research.yaml
  searches/            weekly_report.md
  accepted_state.yaml  next_state.yaml
months/YYYY-MM.yaml
publication/YYYY-MM-DD/inventory.md
final/                 (comparison artifacts after the full run)
```

Reuses the Task 22 convention of a dated, isolated root under `data/backtests/`
but in its own namespace `data/hermes_backtests/` so the two simulations never
collide.

---

## 11. Production-state isolation

The module writes only under `data/hermes_backtests/<id>/`. Verified by a test
(`test_backtest_writes_only_isolated_root`) that walks the tree after a full
assemble+ingest cycle and asserts every new file lives under the backtest root —
never `data/intel_items/`, `data/adaptive_discovery/`, `registry/`,
`CURRENT_BRIEF.md`, `CURRENT_PUBLICATION_PLAN.md`, `site/`, or the review/
publication state. The real 7-week pilot confirmed the production working-tree
changed only by pre-existing Task 29 edits, with the backtest adding files
exclusively under `data/hermes_backtests/`.

---

## 12. Weekly Hermes task design

`prompts/hermes_historical_weekly_task.md` is the durable instruction packet,
rendered per week with `{backtest_id}`, `{week_start}`, `{week_end}`,
`{monitored_sources}`, and `{budgets}` substituted. It fixes: the simulated
identity and date cutoffs; the packet layout; monitored sources; the 16-step
responsibility sequence (inspect state → monitor → execute profiles → discover
→ normalize → resident relevance → resolve identities → detect major subjects →
bounded research → strategist → editor → propose → independent evaluation →
apply acceptance → next-week state → report); the weekly output contract; the
adaptive-behavior expectation; resident questions; the report contents;
boundaries; and stop conditions.

---

## 13. Resident-perspective requirements

The packet requires Hermes to ask, per finding: *If I lived in SilverLeaf
during this week, what important local change would I want to know about?* and,
per discovery: *What important subject did I discover this week that now
deserves persistent monitoring?* The eight resident questions (what is being
built, new roads/ramps, school changes, stores/restaurants/services, healthcare,
utility restrictions, commute changes, what to keep watching) are explicit.

---

## 14. Adaptive subject-promotion behavior

A discovery is promoted only when it is a durable resident subject: entity +
aliases + search profile + milestones + timeline + optional lane. The School QQ
→ Magnolia Oaks Academy path (§41 of the pilot) demonstrates the full chain
without future aliases seeded. The packet explicitly forbids future aliases and
conclusions.

---

## 15. Research escalation behavior

`research.yaml` contract: when identity, geography, currency, or evidence
conflicts, Hermes records the trigger, questions, queries run, sources checked,
confirmed facts, strong inferences, conflicting evidence, unresolved questions,
recommended action (`ACCEPT`, `ACCEPT_QUALIFIED`, `DEFER`, `REJECT`,
`RESEARCH_AGAIN`), confidence, and `evidence_class` (`retrospective_evidence`
when present-day knowledge is used). Bounded: `max_research_escalations_per_week`
(default 2) and `max_research_queries_per_escalation` (default 6). The grocery
center week exercised this with `ACCEPT_QUALIFIED`.

---

## 16. Resident Coverage Strategist behavior

Same role as production: after normalizing the week's findings, decide what to
track and propose durable subjects, aliases, sources, profiles, milestones,
timelines, and lanes. It cannot approve anything; the simulated reviewer does.

---

## 17. Resident Coverage Editor behavior

`coverage_editor.yaml` contract: `coverage_gap_id, coverage_lane, subject,
resident_question, current_state, why_this_is_a_gap, last_meaningful_update,
expected_next_milestone, existing_search_profiles, recommended_research,
recommended_priority, recommended_action`. Allowed actions mirror production
(`SEARCH_NOW`, `ADD_SEARCH_PROFILE`, `REFRESH_SOURCE`, `EXPECT_MILESTONE`,
`CREATE_TIMELINE_PROPOSAL`, `CREATE_ENTITY_PROPOSAL`, `NO_ACTION`,
`ESCALATE_TO_HUMAN`). The editor cannot search, approve, or apply its own
recommendations. The pilot produced 7 editor gaps, one per week, each
identifying a resident-relevant coverage need ahead of the hidden evaluator.

---

## 18. Simulated proposal acceptance

Config `simulated_acceptance` (conservative, approximating Buddy):
`require_evidence`, `require_resident_impact`, `allow_sensitivity: [low]`,
`reject_sensitivity: [medium, high]`, `allow_identity_conflict: false`,
`allow_duplicate_subject: false`, `max_accepted_per_week: 12`, reviewer
`hermes-simulated-evaluator`. Durable-tracking proposals (entity, search
profile) duplicate-reject for an already-tracked subject; **milestone and
timeline updates for a tracked subject are accepted** (they advance history).
Sensitive/crime proposals are rejected and recorded as false positives.
Every decision is persisted so the evaluator can inspect where the simulated
reviewer differed from human judgment. Hermes cannot mark anything accepted
itself.

---

## 19. Hidden comparison evaluator

`evaluate_week` / `evaluate_all` in `scripts/hermes_backtest.py` are the only
readers of `config.hidden_evaluator` (the subject/lane checklist + priorities).
They never write into a Hermes week packet. Hermes sees only its starting state,
feed, and task; it never sees the checklist. The `note` field on every
evaluation output states it is hidden and never exposed.

---

## 20. Resident Coverage Recall

RCR is computed over **high-priority** subjects and lanes found by Hermes
(any finding/promotion/profile/lane match) divided by the high-priority hidden
targets — per Task 22 §25, with the found/missed lists reporting all targets
for inspection. Pilot result over 7 sampled weeks: **0.867** (13/15
high-priority targets; the two high-priority misses — CR 210 widening and
First Coast Expressway — are subjects whose evidence weeks were not in the
pilot sample and are expected to be found in the full run).

---

## 21. Evaluation subjects

Defined only in `config.yaml → hidden_evaluator` (never in Hermes material):
School QQ/Magnolia Oaks Academy (high), CR 2209 connector (high), CR 210
widening (high), SR 16/IGP improvements (high), First Coast Expressway/I-95
access (high), Baptist SilverLeaf campus (high), Publix/Silverleaf Market
(high), SilverLeaf grocery center / possible Harris Teeter (high), SR 207 WRF
(high), Phase III water shortage (high), school zoning/attendance boundaries
(medium), hurricane preparedness (medium); lanes schools, roads, retail,
healthcare, utilities (high), preparedness (medium).

---

## 22. Weekly artifact contract

Per week (as in §10): `starting_state.yaml`, `hermes_task.md`, `feed/`,
`budgets.yaml`, `meta.yaml`, then Hermes outputs `findings.yaml`,
`proposals.yaml`, `coverage_editor.yaml`, `research.yaml`, `searches/`,
`weekly_report.md`; infrastructure produces `accepted_state.yaml`,
`next_state.yaml`. `meta.yaml` carries `status: pending|completed`, the week
bounds, and the visibility cutoff — the completion marker for restart.

---

## 23. Monthly report contract

`python3 scripts/hermes_backtest.py monthly --backtest-id hermes-sjc-v1` writes
`months/YYYY-MM.yaml` with: weeks completed, new subjects, search profiles,
aliases, lanes, timeline events, editor gaps, false positives, findings. The
full run generates these after each month's weeks are ingested. The pilot
produced 7 monthly files (May, Aug, Sep, Dec 2025; Mar, Jun, Jul 2026).

---

## 24. Historical publication snapshots

`python3 scripts/hermes_backtest.py snapshot --backtest-id hermes-sjc-v1 --as-of YYYY-MM-DD`
writes `publication/YYYY-MM-DD/inventory.md`: tracked entities, profiles, lanes,
milestones, timeline events, and a "would publish" resident-facing inventory of
accepted durable-tracking proposals. This lets us ask: *what would SilverLeaf
Brief have looked like if Hermes had been operating then?* — without touching
today's site. A pilot snapshot at 2026-07-26 shows the school, roads, grocery,
and retail subjects Hermes would have published.

---

## 25. Final report contract

The full replay should end with `final/comparison.yaml` (from `evaluate-all`)
plus a written final report covering: coverage (subjects discovered), misses,
timing (discovery lag), adaptive learning (profiles that improved searches),
search quality, source evolution, identity evolution (aliases), timeline
evolution, Resident Coverage Editor performance, comparison to the actual
corpus (what Hermes found that the manual workflow did not, and vice versa),
and production changes before weekly autonomous/supervised operation.

---

## 26. Cost/budget controls

`config.yaml → budgets` (per week): max model calls 12; max sources scanned 30;
max search profiles executed 6; max research escalations 2; max research
queries per escalation 6; max proposal attempts per subject 1; max retries 2.
Stop conditions: state corruption, leakage, production mutation, repeated
proposal failure, budget breach, sensitive/publication decision. Present-day
search is off by default. Estimated full-run volume: ~66 weeks × (≤12 model
calls) ≈ up to ~800 model calls worst case, typically far fewer because most
weeks are thin; search/research are feed-scan + bounded queries, no paid
provider. The runner should not run unbounded; the weekly packet states the
limits.

---

## 27. Restart/resume design

Restartability is inherent: `visible_state(backtest_id, week_start)` rebuilds
state from seed + all `weeks/*/accepted_state.yaml` with
`available_on <= week_start`. A completed week is marked `status: completed` in
`meta.yaml`; `assemble_week` refuses to overwrite a completed week without
`--overwrite` (which produces a clearly re-versioned redo, never a silent
overwrite), and `ingest_week` refuses a second ingest. A rerun from any
completed week reproduces deterministically from the same accepted state.
`next_state.yaml` snapshots the carried-forward state per week.

---

## 28. Pilot weeks selected

7 weeks spanning the required archetypes:

| Week | Archetype |
|------|-----------|
| 2025-05-05 | early school discovery (School QQ topping-out) |
| 2025-08-18 | CR 2209 + SR 16/IGP road milestones |
| 2025-09-15 | school follow-up (under construction) + budget |
| 2025-12-01 | commercial-development discovery (grocery center, qualified) + research escalation |
| 2026-03-23 | retail completion (Publix opening) |
| 2026-06-22 | healthcare + utility emergence (Baptist, SR 207 WRF) |
| 2026-07-20 | alias/identity emergence (Magnolia Oaks Academy) |

---

## 29. Pilot execution results

Hermes (executed per the packet) produced, over the 7 weeks: **12 findings,
31 accepted proposals, 7 editor gaps, 6 search profiles, 5 lanes, 1 research
escalation, 1 alias learned.**

- **Subjects found (8):** School QQ/Magnolia Oaks (05-05), CR 2209 (08-18),
  SR 16/IGP (08-18), grocery center (12-01, qualified), Publix (03-23),
  Baptist (06-22), SR 207 WRF (06-22), water shortage (06-22, via CR 210/
  utilities feed items surfaced).
- **Alias learned:** Magnolia Oaks Academy → SilverLeaf K-8 School (School QQ)
  (07-20) — the full identity chain emerged naturally.
- **Lanes created:** schools and families, roads and mobility, retail and
  amenities, healthcare and services, utilities and household operations.
- **RCR (high-priority):** 0.867 (13/15). Misses (CR 210, FCE, hurricane,
  zoning) correspond to evidence weeks outside the pilot sample.
- **Safety gate held:** a sensitive shooting-type proposal was rejected by the
  simulated reviewer (medium/high sensitivity), and crime items in the June
  feed were not promoted.
- **Publication snapshot** at 2026-07-26 shows the resident-facing inventory
  Hermes would have published.

---

## 30. Problems discovered

1. **Feed bucketing bug** — records were bucketed by item date but files were
   keyed by week start, dropping most records (28 vs 248). Fixed.
2. **Duplicate legacy captures in the feed** — NBOR items present in two
   intel_items files produced duplicate feed rows. Fixed with item_id dedupe.
3. **Prompt template misread as YAML** — `render_task` used the YAML `load()`
   on a Markdown file. Fixed to read text.
4. **Milestone/timeline updates wrongly rejected** — the simulated acceptance
   rejected milestone proposals for an already-tracked subject. Fixed so
   durable-tracking proposals duplicate-reject but history-advancing proposals
   accept.
5. **Hidden-evaluator keyword collisions** — `cr`/`sr` prefixes caused false
   "found" matches (CR 210 via CR 2209). Fixed with a prefix stop set.
6. **RCR counted all targets** instead of high-priority only. Fixed to
   high-priority denominator with all-target lists for inspection.

---

## 31. Fixes made

All six fixes are implemented in `scripts/hermes_backtest.py` and covered by
tests (`tests/test_hermes_backtest.py`): feed bucketing/dedupe, state carry
forward, packet assembly, simulated acceptance (sensitive rejection + history
advance), hidden evaluation (subject/alias/lane matching, high-priority RCR),
and production-path isolation. 6 new tests; full suite 320 passing.

---

## 32. Final Hermes full-backtest instruction

The exact, reusable instruction is `prompts/hermes_historical_weekly_task.md`
(rendered per week with the substitutions below). Buddy should hand Hermes the
following packet to start the full replay:

---

**Hermes Historical Production Backtest — full replay**

Backtest ID: `hermes-sjc-v1`
Period: `2025-05-05` → `2026-08-03`
Cadence: weekly, exactly seven days per interval. Do not jump months.
Workspace: `data/hermes_backtests/hermes-sjc-v1/`
Isolation: read only this workspace plus the public task packet. Never mutate
production state (`data/intel_items/`, `data/adaptive_discovery/`,
`registry/`, `data/review_queue/`, `data/publication_decisions/`,
`CURRENT_BRIEF.md`, `CURRENT_PUBLICATION_PLAN.md`, `site/`). No deployment.

Per simulated week, in order, using only the weekly packet (starting state,
dated feed, budgets) and never anything dated after the week end:

1. Assemble the week with
   `python3 scripts/hermes_backtest.py assemble-week --backtest-id hermes-sjc-v1 --week-start <YYYY-MM-DD>`.
2. Read `weeks/<YYYY-MM-DD>/hermes_task.md`, `starting_state.yaml`,
   `feed/monitored.yaml`, and `feed/all.yaml`.
3. Execute the responsibilities in the packet (monitor known sources, execute
   accepted search profiles against `feed/all.yaml`, discover, normalize
   findings, identify resident relevance, resolve identities with pre-cutoff
   evidence only, detect major subjects, bounded research escalation,
   Resident Coverage Strategist, Resident Coverage Editor).
4. Write `findings.yaml`, `proposals.yaml`, `coverage_editor.yaml`,
   `research.yaml`, `searches/`, and `weekly_report.md` in that week's
   directory per the packet contract.
5. Run `python3 scripts/hermes_backtest.py ingest-week --backtest-id hermes-sjc-v1 --week-start <YYYY-MM-DD>`
   (applies the simulated acceptance policy; do not self-approve).
6. After Hermes completes the week, run
   `python3 scripts/hermes_backtest.py evaluate-week --backtest-id hermes-sjc-v1 --week-start <YYYY-MM-DD>`
   — the hidden evaluator compares against the hidden subject set.
7. Advance exactly seven days and repeat. After the final week of each month,
   run `python3 scripts/hermes_backtest.py monthly --backtest-id hermes-sjc-v1`
   to synthesize the month. Optionally write
   `python3 scripts/hermes_backtest.py snapshot --backtest-id hermes-sjc-v1 --as-of <date>`
   for historical publication snapshots.
8. Continue through 2026-08-03 unless a defined stop condition triggers
   (state corruption, future-data leakage, production-mutation attempt,
   budget breach, repeated proposal failure, sensitive/publication decision).
9. At completion run
   `python3 scripts/hermes_backtest.py evaluate-all --backtest-id hermes-sjc-v1`
   and write the final comparison report (§25) plus
   `data/hermes_backtests/hermes-sjc-v1/final/comparison.yaml`.

Resident lens: for every finding ask "if I lived in SilverLeaf this week, what
would I want to know?" and "what subject now deserves persistent monitoring?"
Never use present-day aliases, entities, profiles, or conclusions. Present-day
retrieval is disabled; the dated feed is the search universe. Label any
retrospective reasoning `retrospective_evidence`. Crime, minors, allegations,
and private information are excluded from promotion.

---

## 33. Exact command/dispatch procedure

For a fully scripted full run, the operator loop is:

```bash
BT=hermes-sjc-v1
D=2025-05-05
END=2026-08-03
while [ "$D" \<= "$END" ]; do
  python3 scripts/hermes_backtest.py assemble-week --backtest-id $BT --week-start $D
  # --- Hermes reads the packet and writes the week's outputs ---
  python3 scripts/hermes_backtest.py ingest-week --backtest-id $BT --week-start $D
  python3 scripts/hermes_backtest.py evaluate-week --backtest-id $BT --week-start $D
  D=$(python3 -c "import datetime;print((datetime.date.fromisoformat('$D')+datetime.timedelta(days=7)).isoformat())")
done
python3 scripts/hermes_backtest.py monthly --backtest-id $BT
python3 scripts/hermes_backtest.py evaluate-all --backtest-id $BT
```

The Hermes reasoning step (the middle of the loop) is the only non-mechanical
step; it consumes the assembled packet and writes the week's outputs. Each
step is restartable from any completed week.

---

## 34. Expected outputs

- `weeks/<date>/…` — 66 completed weekly packets (state, feed, task, outputs,
  accepted state, next state, report).
- `months/YYYY-MM.yaml` — monthly syntheses.
- `publication/YYYY-MM-DD/inventory.md` — historical publication snapshots.
- `final/comparison.yaml` + a written final report — coverage, misses, timing,
  adaptive learning, search/source/identity/timeline evolution, editor
  performance, and side-by-side comparison with the actual corpus and the
  Task 28 ideal publication.
- Backtest-only `CURRENT_BRIEF.md` / `CURRENT_PUBLICATION_PLAN.md` analogues
  are generated under the backtest root by the operator if desired (never in
  production paths).

---

## 35. Validation results

```
python3 -m pytest tests/ -v            → PASS, 320 tests (314 + 6 new)
python3 scripts/validate.py            → ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS (0 errors)
python3 scripts/validate_silverleaf_scope.py   → PASS (0 errors, 0 warnings)
git diff --check                       → clean
git status --short                     → production unchanged by backtest;
                                         new files only under data/hermes_backtests/,
                                         prompts/, scripts/, tests/, reports/
```

Additional verified: feed bucketing/dedupe; state carry-forward (no future
aliases leak); weekly packet assembly; simulated acceptance (sensitive rejected,
history-advance accepted); hidden evaluator separation; high-priority RCR;
alias learning; monthly synthesis; publication snapshot; production-path
isolation; restart from completed weeks.

---

## 36. Files created

- `scripts/hermes_backtest.py` (build-feed, assemble-week, ingest-week,
  evaluate-week, evaluate-all, snapshot, monthly).
- `prompts/hermes_historical_weekly_task.md` (the durable weekly instruction).
- `data/hermes_backtests/hermes-sjc-v1/` (config.yaml, seed.yaml,
  feed/{overrides,summary,weeks/}, weeks/…×7 completed, months/×7,
  publication/2026-07-26/).
- `tests/test_hermes_backtest.py` (6 tests).

---

## 37. Files changed

None in production authority. `scripts/`, `prompts/`, `tests/`, and
`data/hermes_backtests/` gained the new files listed above. `reports/` gains
this report. Pre-existing Task 27/28/29 working-tree changes remain untouched.

---

## 38. Production state verification

Verified by `git status`: the backtest added files only under
`data/hermes_backtests/`. No production corpus, registry, adaptive state,
review queue, publication decision, `CURRENT_BRIEF.md`,
`CURRENT_PUBLICATION_PLAN.md`, or `site/` file was created or modified by Task
30. A dedicated test enforces this isolation.

---

## 39. Final Git status

`master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` (unchanged HEAD). Working
tree contains the pre-existing Task 27/28/29 changes plus the new Task 30 files
(`scripts/hermes_backtest.py`, `prompts/hermes_historical_weekly_task.md`,
`data/hermes_backtests/`, `tests/test_hermes_backtest.py`, this report). No
commit or push.

---

## 40. Final task status

| Success criterion | Status |
|-------------------|--------|
| Task 22 harness reviewed for reuse | COMPLETE |
| Hermes has an explicit historical weekly task | COMPLETE (`prompts/hermes_historical_weekly_task.md`) |
| Historical-visible state separated from production | COMPLETE |
| Hermes cannot see future aliases/entities | COMPLETE (availability rules + tests) |
| Isolated Hermes backtest workspace exists | COMPLETE (`data/hermes_backtests/hermes-sjc-v1/`) |
| Weekly Hermes outputs have a stable contract | COMPLETE |
| Simulated proposal acceptance defined | COMPLETE |
| Hidden evaluator separate from Hermes | COMPLETE |
| Resident Coverage Recall measured | COMPLETE (0.867 on pilot) |
| Historical publication snapshots planned/implemented | COMPLETE (snapshot + inventory) |
| Search/research limitations explicit | COMPLETE (§9, config, packet §9) |
| Cost limits and stop conditions exist | COMPLETE (§26) |
| Restart/resume supported | COMPLETE (§27) |
| Pilot weeks selected | COMPLETE (7) |
| Small multi-week proof executed | COMPLETE (7 real-Hermes weeks) |
| Production state remains unchanged | COMPLETE (verified) |
| Report contains one exact copy-paste Hermes instruction | COMPLETE (§32) |
| Buddy can start the full replay without another architecture session | COMPLETE |

**Final status vocabulary:** COMPLETE. The real Hermes historical production
backtest is fully prepared and proven on a 7-week pilot: Hermes discovers and
adapts naturally (School QQ → Magnolia Oaks alias, CR 2209, SR 16/IGP, grocery
center, Publix, Baptist, SR 207), builds persistent monitoring, and passes the
safety gates, all inside an isolated workspace. The exact full-run instruction
is in §32; Buddy can dispatch it to Hermes directly. Remaining work is bounded:
run the full 66-week replay and inspect the side-by-side comparison of what
Hermes found versus what the manual workflow built.
