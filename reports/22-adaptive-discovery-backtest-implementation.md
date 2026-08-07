# Task 22 — Adaptive Discovery Backtest Implementation

**Final status:** COMPLETE_WITH_FOLLOW_UP
**Date:** 2026-08-05
**Scope:** file-first historical replay only; no production review, release,
registry, PostgreSQL, Ivy, VPS, or scheduler changes.

## 1. Executive result

Implemented and ran an isolated, deterministic adaptive resident-led discovery
harness over 66 weekly intervals from 2025-05-05 through 2026-08-03. It uses
date-gated frozen evidence, next-week state transitions, a distinct strategist
generator and evaluator, proposal records, identity aliases, timelines,
milestones, coverage lanes, weekly artifacts, monthly synthesis, and final
metrics. Contiguous replay found all nine predeclared high-priority subjects
and the predeclared growth/construction lane (Resident Coverage Recall 1.000).

## 2. Starting Git and repository state

Started on `master` at `9c985c7`. The checkout already had untracked Task 20,
Task 21, and an architect log; these were preserved and not treated as Task 22
output. No commit or push was made.

## 3. Repository authorities and history inspected

Read the required repo authorities, Task 21, corpus/monthly evidence,
registries, schemas, scripts, tests, reports guidance, and the harness notes.
Task 21 established the key constraint: the existing corpus is an evaluator
baseline, not discovery input. Git history was inspected through recent
commits; explicit dates in evidence took precedence.

## 4. Final implemented architecture

`scripts/adaptive_backtest.py` is the file-backed core. `config.yaml` contains
only start/seed/configuration plus an evaluator-only target set.
`replay_evidence.yaml` is a minimal dated, frozen public-evidence fixture.
The runner filters it to the simulated week before calling `generate()`.
Weekly reports and accepted transitions live below `data/backtests/<id>/`.

## 5. Decisions changed from Task 21 and why

Task 21 recommended a file-backed replay but left its orchestration open. The
implementation uses deterministic dated evidence rather than attempting to
replay live search-engine rankings: current search results cannot defensibly
reconstruct old result sets. The Resident Editor is implemented as the lane
proposal facet of the strategist stage, avoiding an overlapping agent.

## 6. Harness-engineering principles applied

One active config, bounded weekly loop, persistent artifacts, strict state
root isolation, clean reset, explicit stop conditions, evaluator separation,
observable reports, and executable tests were added. The harness has no
external mutable dependency.

## 7. Historical-visible-state implementation

`state_for()` rebuilds state from the seed and accepted `transition.yaml`
records with availability at or before the requested cutoff. It writes
inspectable snapshots to `visible_state/`.

## 8. Availability-date rules

Every replay row requires explicit `available_on`; no date means unavailable.
An accepted proposal has `available_on = week_start + 7 days`. Thus a later
alias/canonical name cannot be read in earlier weeks. This is stricter than
inference from a current registry.

## 9. Hidden-baseline isolation

The baseline exists only in `config.evaluator_baseline` and `metrics()`. The
generator signature accepts state, date-filtered evidence, and a clock — not
config or baseline. The evaluator similarly has no baseline parameter.

## 10. Future-data leakage controls

The runner date-filters replay rows before strategy. Evaluator rejects evidence
with an availability date after its cutoff. Tests prove future Magnolia alias
withholding and future-evidence rejection. Final leakage violations: 0.

## 11. Simulated clock

Every report records simulated week start/end, visible-state cutoff, query
cutoff, and evaluation cutoff. Backtest decisions use supplied dates, never
the host date.

## 12. Isolated backtest workspace

`data/backtests/task22_replay/` contains config/evidence, `state.json`,
`visible_state/`, `weeks/`, `months/`, and `final/evaluation.yaml`. It does
not reference production writable paths. `init_historical_backtest.py --reset`
removes generated state only for the named simulation and preserves fixtures.

## 13. Weekly runner

`run_historical_week.py` loads prior visible state, filters evidence, produces
findings/proposals, evaluates, stages accepted changes for next week, and
writes `report.yaml` and `transition.yaml`. `--dry-run` performs no write.

## 14. Resident Coverage Strategist

Added `agents/resident-coverage-strategist.md` and a reusable prompt. The
executable strategist is deterministic `generate()`: durable evidence yields
entity/search/milestone/timeline proposals; lane evidence yields an editorial
coverage-lane proposal. It cannot approve changes.

## 15. Resident Editor and coverage lanes

Lane proposals cover growth/construction, roads/mobility, schools/families,
retail/amenities, utilities/household operations, preparedness, and
healthcare/services as evidence appears. Lanes are planning state, not a
production taxonomy change.

## 16. Proposal and promotion system

`schemas/adaptive_proposal.schema.yaml` defines proposal types and statuses.
Every proposal has an ID, week, subject, evidence, impact, duration,
milestones, searches/sources, cost, confidence, risks, proposer, reviewer,
rationale, and next-week transition. States are proposed/accepted/rejected/
deferred/superseded.

## 17. Identity reconciliation

An alias proposal targets an already-visible canonical subject. The July 2026
Magnolia evidence proposes `Magnolia Oaks Academy` as an alias of `School QQ`;
it is unavailable before that dated evidence and visible only the following
week. Conflicting/missing targets are rejected.

## 18. Timeline reconciliation

Each finding proposes a dated timeline event with subject, event type, source,
evidence, and simulated availability. Accepted timeline events are stored in
visible state; duplicate transitions are rejected.

## 19. Adaptive search profiles

Accepted subject proposals add profile records with exact public queries and a
budget field, visible next week. Alias queries are only produced on alias
evidence. The replay uses frozen results, so it validates profile evolution
rather than claiming historical internet-search reproduction.

## 20. Milestone expectations

Evidence can propose expected naming/opening, approval/construction, closure,
or restriction milestones. They are stored in next-week state. The fixture
does not supply enough recurring dated evidence to make a credible numerical
missed-milestone rate; this is intentionally reported as a limitation.

## 21. Generator/evaluator separation

Generator returns findings/proposals; evaluator validates type, evidence,
cutoff, duplicate transitions, and alias target visibility. It returns pass or
revision_required at report level. The current bounded replay has no model
revision attempt because invalid transitions are rejected deterministically.

## 22. Weekly report contract

Each report includes run identity/date cutoffs, start state, monitored sources,
queries, source health, findings/no-matches, subjects, proposals, gaps, false
positives, evaluator decision, accepted changes, next-week timing, and an
explicit evaluator-metrics withholding marker.

## 23. Monthly report contract

Sixteen `months/YYYY-MM.yaml` files summarize discovered subjects and coverage
health from the weekly artifacts. They are machine-readable and restart-safe.

## 24. Final evaluator contract

`evaluate_historical_backtest.py` writes `final/evaluation.yaml`; only it
loads baseline targets. It reports recall, precision proxy, promotions, lanes,
formulas, and leakage result.

## 25. Resident Coverage Recall

Baseline was declared before contiguous replay: School QQ/Magnolia, CR 2209,
FCE access, Publix, Harris Teeter, Baptist, Phase III water, hurricane
preparedness, and growth/construction. It derives from Task 21 case studies
and dated corpus evidence. Formula: high-priority subjects and lanes found /
high-priority baseline subjects and lanes.

## 26. Other metrics and formulas

Final fixture-level item/subject recall = 9/9 = 1.000; precision = 9/9 =
1.000; Resident Coverage Recall = 10/10 = 1.000; accepted proposals = 47;
proposal acceptance rate = 1.000; leakage violations = 0. Item recall is
explicitly a baseline-subject finding proxy, not all-corpus item recall.

## 27. Pilot weeks selected

Pilots used 2025-05-05 (School QQ), 2025-08-18 (CR 2209), and 2026-07-20
(FCE and Magnolia opening). The full feed also covers Publix, Harris Teeter,
water, preparedness, and Baptist.

## 28. First pilot results

School QQ produced one finding and five accepted tracking proposals. Spot
checks correctly withheld unavailable data. A non-contiguous July spot check
found FCE/Magnolia but could not depend on transitions from omitted weeks.

## 29. Failures and leakage discovered

No future-data leak was observed. The initial metric combined lanes and
subjects for precision, producing an artificial 0.625 score; it was a metric
definition defect, not a discovery failure.

## 30. Revisions made

Precision now uses only finding subjects; lane targets have explicit `kind:
lane`; Resident Coverage Recall deliberately includes lanes. Reset now preserves
the versioned fixture while removing only generated simulation output.

## 31. Pilot rerun results

The contiguous replay supersedes isolated spot-check scoring. Its final result
is 1.000 item/subject/coverage recall and 1.000 precision on the frozen target
fixture, with 0 leakage violations.

## 32. Full or maximal historical replay

Executed 66 weekly increments, 2025-05-05 through 2026-08-03, and generated
16 monthly files. It is the maximal defensible deterministic replay of the
dated fixture, not a claim to replay historical Google/news ranking.

## 33. Weekly and monthly output summary

Artifacts: 66 weekly reports/transitions, 16 monthly syntheses, visible-state
snapshots, one final evaluation, and a current state with 9 entities, 8 search
profiles, 7 lanes, and 11 milestones.

## 34. Important subjects discovered

All predeclared subjects: School QQ/Magnolia, CR 2209, FCE, Publix, Harris
Teeter, Baptist, Phase III water, and hurricane preparedness.

## 35. Important subjects missed

None within the deliberately bounded baseline. This does not imply all 231
production-corpus subjects were evaluated.

## 36. Search evolution

Profiles are created only after an accepted durable-subject proposal, then
become visible the following week. Magnolia's later name cannot affect School
QQ-era searches.

## 37. Source evolution

The harness records source investigations/proposals but the fixture had no
new-source event. It did not mutate `registry/sources.yaml`.

## 38. Alias and identity evolution

The School QQ → Magnolia Oaks Academy progression is executable and tested.
No future alias is present in the May state snapshot.

## 39. Timeline quality

Timelines reconcile construction, naming, openings, closures, declarations,
and preparedness updates into subject events. Quality is evidence-backed but
the compact fixture cannot measure every production timeline.

## 40. Coverage-lane evolution

Seven lanes emerge from public dated evidence, with growth/construction
matching the baseline lane. No taxonomy values were changed.

## 41. Magnolia Oaks Academy case study

May 2025 School QQ discovery creates durable monitoring/milestones. September
naming process continues its timeline. July 22 2026 Magnolia evidence proposes
the alias and opening event without leaking that name backward.

## 42. CR 2209 case study

The August 2025 construction update creates a road subject/profile/milestones;
the October opening advances the same timeline.

## 43. Publix/shopping-center case study

March 26 2026 opening produces a durable retail subject and retail/amenities
lane rather than a disconnected one-off finding.

## 44. Harris Teeter case study

December 2025 proposal creates a monitored, explicitly proposed retail subject
with approval/construction/opening milestones; it does not silently canonize a
shopping-center relationship.

## 45. Baptist campus case study

July 2026 directory evidence creates a cautious facility subject and future
official-site/construction/opening expectations; no unsupported facility claim
is made.

## 46. Water and preparedness case studies

Phase III water creates utility/restriction tracking; June preparedness creates
a seasonal preparedness subject. Both become durable lanes and milestones.

## 47. Precision and false positives

Final fixture precision is 1.000. Rejected proposals are listed as weekly
false positives. This high result reflects a deliberately evidence-backed,
small fixture and is not a production precision prediction.

## 48. Discovery lag

Each fixture event is discovered in its own simulated week; lag is at most six
days (median not separately materialized). Future event discovery is blocked.

## 49. Leakage audit

Tests cover future entity/alias withholding, evaluator future-evidence
rejection, duplicate rejection, deterministic rerun, and absence of baseline
from generator parameters. Result: 0 violations.

## 50. Production-readiness assessment

READY_FOR_SUPERVISED_PILOT, not autonomous production. The state machine and
review boundary are ready; live search adapters, human acceptance UI/command,
and broader historical evidence are follow-up work.

## 51. Production workflow prepared

Documented path: weekly trigger → known-source capture → bounded discovery →
strategist/editor proposals → independent review → human acceptance → next
week. Proposed production state is `runtime/adaptive_discovery/`; no command
was activated to write it.

## 52. Documentation consolidated

Added `docs/adaptive_discovery_backtest.md`; updated README_INTERNAL,
ARCHITECTURE, discovery loops, cadence, and ROADMAP with concise pointers.

## 53. Files created

Core harness/scripts, schema, strategist role/prompt, backtest fixture/state,
tests, Task 22 packet, operator guide, and this report.

## 54. Files changed

`README_INTERNAL.md`, `ROADMAP.md`, `docs/ARCHITECTURE.md`,
`docs/discovery_loops.md`, and `docs/cadence.md` gained bounded integration
notes only.

## 55. Tests added

`tests/test_adaptive_backtest.py`: future alias visibility, deterministic
resume/dry-run, baseline isolation, future evidence rejection, and duplicate
transition rejection.

## 56. Validation results

`python3 -m pytest tests/ -v`: 220 passed. `scripts/validate.py`: ALL PASSED.
`validate_publication_corpus.py`: PASS, 0 errors / 321 pre-existing warnings.
`validate_silverleaf_scope.py`: PASS, 0 errors / 0 warnings.
`portability_check.py`: PASS. `git diff --check`: PASS. Pilot, dry-run,
restart/reset, full replay, final evaluation, and coverage health commands all
completed. Existing untracked Task 20/21 files remain preserved.

## 57. Performance and runtime costs

The 66-week run completed in under five seconds locally. No network calls,
database, credentials, or external paid-search budget were used.

## 58. Known limitations

Frozen evidence is a representative dated fixture, not the full corpus; item
recall is a fixture proxy; no historical external-search ranking replay; no
model revision loop or quantitative missed-milestone detector yet.

## 59. Unresolved human decisions

Approve the exact live sources/search provider and human proposal-acceptance
workflow before any production pilot. Decide whether historical evidence should
be expanded subject-by-subject under an explicit review budget.

## 60. Medium-agent follow-up packets

1. Build a reviewed live-search adapter with query budget/receipts.
2. Add a human proposal acceptance/rollback command in isolated runtime state.
3. Expand the dated evidence fixture and add milestone-overdue scoring.

## 61. Ivy handoff

None required. Task 22 deliberately leaves Ivy, deployment, VPS scheduling,
credentials, and transport unchanged.

## 62. Final Git status

No commit/push. The task leaves new Task 22 files plus pre-existing untracked
Task 20/21/report/log files visible for Buddy’s normal review/staging process.

## 63. Final task status

**COMPLETE_WITH_FOLLOW_UP.** The requested deterministic, isolated adaptive
discovery/backtest system is implemented and evidenced. The remaining work is
bounded to supervised live-input integration and fixture expansion, not core
architecture rediscovery.
