# Task 23 — Live Adaptive Discovery, Human Review, and Current Operational Brief

**Final status:** COMPLETE_WITH_FOLLOW_UP
**Mode:** supervised-live-pilot
**Date:** 2026-08-06
**Scope:** file-first live discovery, human proposal review, pipeline health,
current brief, and publication-readiness preparation. No production registry,
review-queue, publication-decision, release, PostgreSQL, Ivy, deployment,
scheduler, credential, or secret-state mutation.

> **Follow-up correction (2026-08-06):** This report records the Task 23
> implementation as it stood at completion. Durable governance authority was
> subsequently migrated from ignored runtime files to
> `data/adaptive_discovery/`; only run artifacts and raw receipts remain under
> `runtime/adaptive_discovery/`. `CURRENT_BRIEF.md` and
> `docs/live_adaptive_operations.md` are the current operational authority.

---

## 1. Executive result

Implemented and ran a supervised live adaptive-discovery workflow with a
provider-neutral search adapter, per-query receipts and budgets, an independent
evaluator stage, isolated runtime state at `runtime/adaptive_discovery/`, human
accept/reject/defer/rollback commands, a derived pipeline-health model, and one
canonical generated operational document: `CURRENT_BRIEF.md`, with dated
immutable snapshots under `reports/briefs/`.

Three clean supervised live pilots ran against public sources:
`SJC-LIVE-20260806-0201/0202/0203`. They produced 22 normalized findings and 22
pending human proposals across Magnolia Oaks Academy, CR 2209, SilverLeaf Mega
Publix, First Coast Expressway access, Harris Teeter SilverLeaf, Baptist
SilverLeaf campus, and four resident coverage lanes. The rerun produced 0 new
proposals (persistent duplicate control). An acceptance → rollback proof ran on
the isolated runtime without touching any production or publication state.

## 2. Starting repository and Git state

Started on `master` at `9c985c7e6fcca544e78c9e51336d74866c605f75`. The working
tree already contained uncommitted Task 20/21/22 work (reports, scripts, logs,
and an abbreviated prior Task 23 scaffold with a functional but thin live
harness, brief generator, and review CLI). All pre-existing files were
preserved. No commit or push was made.

## 3. Authorities inspected

Read `README.md`, `README_INTERNAL.md`, `AGENTS.md`, `ROADMAP.md`, `BACKLOG.md`,
`docs/ARCHITECTURE.md`, `docs/discovery_loops.md`, `docs/cadence.md`,
`docs/operator_mode.md`, `docs/adaptive_discovery_backtest.md`, the weekly and
publication contracts, `docs/public_ui_v0_spec.md`, reports 20/21/22,
`tasks/README.md`, `reports/README.md`, and the harness reference
`/Users/buddy/projects/alori/learn-harness-engineering/notes.md`. Inspected
`scripts/`, `agents/`, `prompts/`, `registry/`, `schemas/`, `runtime/`,
`data/`, `tests/`, `reports/`, `logs/`, and `site/`.

## 4. Decisions made

- Kept file-first authority; PostgreSQL remains DORMANT_FUTURE_READY.
- Chose credential-free public Google News RSS as the live discovery provider
  with a deterministic `stub` provider for simulation and tests, exposed behind
  one adapter boundary so a commercial provider can be added later without
  changing the pipeline.
- Isolated all live state under `runtime/adaptive_discovery/`; canonical
  registries, review queue, publication decisions, and the release are never
  written by the live loop.
- The strategist generates; the evaluator approves/rejects independently; no
  proposal is auto-canonized.
- Milestone-overdue and stale-subject detection is intentionally conservative
  (no due date → no overdue claim) and scoring is not tuned for perfect output.

## 5. Creative improvements made

- Provider-neutral search adapter with budgets at five scopes and full receipts.
- Independent evaluator stage separating proposal generation from approval.
- Coverage-health artifact (fresh/stale subjects, no-yield queries, source gaps).
- Milestone-overdue/met, stale-subject, search-yield, source-freshness, and
  lane-coverage metrics in the backtest harness plus a consolidated
  `final/coverage_health.yaml`.
- Publication-candidate preparation (titles, summaries, why-it-matters,
  relevance labels) that never mutates publication state.
- Stale-input warnings and structure validation in the brief generator.

## 6. Final architecture

```
scripts/search_adapter.py        provider boundary, budgets, receipts, dedupe
scripts/live_adaptive.py         pilot runner, evaluator, health, review, state
scripts/run_live_adaptive_pilot.py   CLI: one bounded live run
scripts/review_adaptive_proposal.py  CLI: show/accept/reject/defer/rollback
scripts/build_current_brief.py       CLI: CURRENT_BRIEF + snapshot + --check
scripts/report_coverage_health.py    CLI: live or backtest coverage health
scripts/prepare_publication_candidates.py  CLI: prepared candidates only
scripts/adaptive_backtest.py      historical replay + expanded health metrics
runtime/adaptive_discovery/       isolated supervised live-pilot state
reports/briefs/YYYY-MM-DDTHHMMSSZ.md   immutable brief snapshots
```

Pipeline: known-source probes → bounded live queries → receipts → normalization
and dedupe → identity/subject matching → strategist proposals → independent
evaluator → pending-proposal persistence → coverage health → pipeline health →
current brief. Publication-candidate prep is a separate read-only step.

## 7. CURRENT_BRIEF.md design

The brief is the first operational document a human reads. It has the required
header (Generated, Mode, Run ID, Repository SHA, Data cutoff, Overall health,
Publication status) with links to the latest snapshot, run artifact, pending
registry, coverage report, task report, and the public SilverLeaf Brief. Eleven
sections in stable order: Executive summary, Pipeline health, What changed,
Important resident findings, Coverage health, Decisions needed, Publication
opportunities, Risks and failures, Next run plan, Commands for Buddy,
Provenance. Reading time is a few minutes; details live in run artifacts.

## 8. Brief generator

`scripts/build_current_brief.py` derives content from `state.yaml`,
`health.yaml`, `coverage.yaml`, `pending_proposals.yaml`, and the run artifact.
It fails when required health/run evidence is missing, warns when the health
artifact is stale (> 168 hours), renders deterministic section ordering, writes
the dated snapshot first, then atomically replaces `CURRENT_BRIEF.md`.
`--check` validates all required sections and headers in order, and rejects any
private path or secret marker. Modes: production, supervised-live-pilot,
simulation. A run ID can be supplied or defaults to `state.last_run`.

## 9. Brief versioning and snapshots

Every generation writes `reports/briefs/YYYY-MM-DDTHHMMSSZ.md` and the current
brief points to that snapshot. There are no manually numbered briefs; Git is the
long-term history. Final snapshot: `reports/briefs/20260806T041348Z.md`.

## 10. Pipeline-health model

`runtime/adaptive_discovery/health.yaml` reports all required components:
source_health, known_source_capture, live_search, normalization, dedupe,
identity_reconciliation, strategist, editor, evaluator, proposal_storage,
proposal_review, timeline_state, milestones, coverage_health,
publication_candidate_handoff, report_generation, state_persistence. Each has
status, last success, last failure, evidence artifact, freshness threshold,
failure count, warning count, and required action.

## 11. Health evidence and derivation

Overall health is derived, never hand-written: BLOCKED if the run was blocked;
otherwise DEGRADED if any component is DEGRADED/BLOCKED/STALE; otherwise
HEALTHY. Component statuses derive from run flags and search-failure receipts.
The current run is HEALTHY with all 16 components GREEN, backed by the run
artifact and two official public source probes (200 OK).

## 12. Live-search adapter

`scripts/search_adapter.py` is provider-neutral. `SearchSpec` carries query,
provider, result limit, allowed/excluded domains, date window, timeout, retry
limit, user agent, budget, lane, subject, and source profile. `BudgetTracker`
enforces run/lane/profile/subject/domain limits. `execute_search` produces a
full receipt, normalized results, raw-row preservation, cross-query dedupe, and
no-match records. The `google_news_rss` provider is the approved credential-free
live mode; `stub` is deterministic and offline.

## 13. Search providers and limitations

Google News RSS is used for discovery leads only, not primary authority. It
does not guarantee server-side domain or date filtering, so the adapter applies
post-filters. RSS redirect URLs are leads for human follow-up. The stub provider
supports offline simulation and tests. No commercial provider credentials were
available or required; no search engine was scraped in violation of rules.

## 14. Query budgets

The run budget defaults to 3 and is enforced before execution (`run_pilot`
raises on overshoot). Budgets can also be limited per coverage lane, search
profile, subject, and source domain. Budget spend and remaining are recorded per
query and summarized in the run artifact; the brief reports budget state
implicitly through receipts. Pilot 0201/0202/0203 each spent exactly 3/3.

## 15. Search receipts

Every query writes a receipt under `runs/<run_id>/receipts.yaml` with run ID,
query ID, exact query, provider, source profile, lanes, subjects, domains,
started/completed timestamps, simulated flag, result count, accepted count,
duplicate count, failure, cost estimate, budget before/after, result URLs,
result hashes, and raw SHA-256. Receipts are stored separately from human
reports. Retention: receipts and raw hashes are versioned operational evidence;
raw bodies are not retained beyond the hash.

## 16. Human proposal-review workflow

`review_adaptive_proposal.py show` prints the proposal, the exact proposed
state change (accepted bucket append), affected future searches, and prior
decision history before any mutation. `accept`, `reject`, `defer`, and
`rollback` each act on exactly one proposal ID and require `--reviewer` and
`--rationale` (rollback additionally requires `--decision-id`). Decisions are
appended to `decisions.yaml`; the brief is regenerated after a non-dry-run
success. Publication state is never referenced or changed.

## 17. Acceptance implementation

Acceptance validates the pending proposal, removes it from pending, sets
status `accepted`, records the decision, and appends it to the isolated
accepted bucket (`entities`, `search_profiles`, `lanes`, or `timelines`) in
`state.yaml`. `--dry-run` validates and prints without writing. Bulk acceptance
is impossible because the CLI takes a single `--proposal-id`.

## 18. Rejection and deferral

Reject removes the proposal from pending, marks it `rejected`, and preserves
the full proposal inside the append-only decision record. Defer does the same
with status `deferred`. Neither touches production state, and rejected
proposals remain in the decision history for audit.

## 19. Rollback

Rollback requires the original acceptance `decision_id`, verifies it belongs
to the same proposal, removes the record from the accepted bucket, restores the
proposal to pending as `pending_human_review`, and appends a rollback decision.
It is atomic and tested.

## 20. Production adaptive state

Accepted state lives only in `runtime/adaptive_discovery/state.yaml`. The
runtime holds accepted entities/aliases/search profiles/lanes/milestones/
timelines, pending proposals, decision history, health, and coverage. It never
writes `registry/`, `data/review_queue/`, `data/publication_decisions/`,
`data/corpus/`, or `site/`. Promotion to canonical registries is a separate,
explicit, human-gated action not performed here.

## 21. State initialization and restore

`initialize()` creates empty state/pending/decisions/health/coverage files when
absent. The runtime is restartable: a rerun with identical queries produced 0
new proposals, proving state round-trips. `--dry-run` provides safe previews.
Rollback restores state to its prior shape.

## 22. Coverage-health implementation

`coverage.yaml` lists fresh subjects (found in the run), stale subjects
(tracked entities/profiles with no finding within the stale window), missed
milestones (not determinable from a single live pilot; no claim made), no-yield
queries, source gaps (failed probes), and lanes covered. The live report is
generated after every run; the backtest report is generated at replay end.

## 23. Stale-subject detection

`stale_subjects()` flags tracked entities and search profiles whose most recent
finding is older than the stale window (default 60 days). On the expanded
replay fixture it correctly reports six stale subjects including Harris Teeter
and Phase III water (no recent findings), while fresh subjects are excluded.

## 24. Milestone-overdue detection

`milestone_status()` compares each accepted milestone's due date against the
cutoff and checks for a realizing event (e.g., `opened` realizes `opening`).
Milestones with no due date are never claimed overdue. The expanded replay
reports 7 overdue and 4 met milestones; e.g., Harris Teeter approval/construction
and Publix tenant announcements are overdue, while School QQ opening and CR 2209
completion are met. This is an honest, evidence-backed result, not a tuned
perfect score.

## 25. Search-yield tracking

`search_profile_yield()` measures accepted profiles that produced findings in
later weeks and counts query attempts. The replay reports a 1.0 profile yield
rate with 10 yielded profiles; each weekly report records per-profile yielded
status and no-match subjects.

## 26. Expanded historical evidence

`replay_evidence.yaml` grew from 12 to 16 dated rows, adding `milestone_due`
dates, the SilverLeaf shopping-center expansion, CR 210 safety meetings, the
official naming event, and a commercial-tenants row, plus new queries. This
covers schools, CR 2209, First Coast Expressway, Publix, Harris Teeter, Baptist,
water shortage, hurricane preparedness, major roads, and additional
construction/growth subjects. The harness remains a dated frozen fixture, not a
claim to replay historical search rankings.

## 27. Backtest regression

The 66-week contiguous replay (2025-05-05 → 2026-08-03, 16 monthly syntheses)
was re-run with the expanded fixture. Result: item/subject recall 1.000,
Resident Coverage Recall 1.000, precision 0.818 (honestly lower because new
subjects are found outside the baseline), 7 overdue milestones, 4 met, 6 stale
subjects, and 0 leakage violations. Task 22 future-evidence and
baseline-isolation protections remain intact.

## 28. Supervised live-pilot configuration

Pilots used approved public sources (SJC county news, SJCSD site probes) and
bounded Google News RSS queries seeded from existing canonical subjects
(Magnolia Oaks, CR 2209, Publix, Harris Teeter, Baptist, FCE). Budget 3 per run.
No hidden evaluation subjects were injected; the resident concerns listed in the
task were treated as evaluator interests only.

## 29. First live-pilot results

Run `SJC-LIVE-20260806-0201` (Magnolia Oaks, CR 2209, Publix) returned 8
normalized findings and created 12 pending proposals (entity, search profile,
timeline, and lane proposals) with 0 evaluator rejections.

## 30. Findings

Run `SJC-LIVE-20260806-0202` (FCE, Harris Teeter, Baptist) returned 14 findings
across First Coast Expressway access (4), Harris Teeter SilverLeaf (4),
SilverLeaf Mega Publix (1 additional), and Baptist SilverLeaf campus (5),
creating 10 new proposals and correctly rejecting 5 duplicates for subjects
already pending.

## 31. Important subjects discovered

Magnolia Oaks Academy (2026-27 opening), CR 2209 connector (CR 210 intersection
meetings), SilverLeaf Mega Publix (opening and two new supermarkets),
First Coast Expressway access (final phase open houses), Harris Teeter
SilverLeaf (proposal and reaffirmation), Baptist SilverLeaf campus (opening,
helipad approval), and the schools/families, roads/mobility, retail/amenities,
and healthcare/services coverage lanes.

## 32. Important subjects missed

Within a three-query budget per run, utilities/water restrictions and
hurricane-preparedness produced no live findings in these runs; they remain
explicit coverage gaps for the next run. No finding was fabricated to fill them.

## 33. False positives

The evaluator rejected 5 proposals across pilots for "subject already tracked
or proposed" (Publix and lane duplicates). No evaluator-approved proposal was
later found unsupported; all were kept pending for human review.

## 34. Proposals generated

22 pending proposals total: 6 entity, 6 search_profile, 4 coverage_lane, and 6
timeline_reconciliation. Each carries evidence, resident impact, benefit,
budget, risk, proposed transition, status, and creation timestamp.

## 35. Evaluator outcomes

The evaluator accepted 22 and rejected 5 with explicit rationales recorded in
each run artifact (`evaluator_rejected`). Evaluator and strategist remain
separate; the evaluator never sees the strategist as its own oracle.

## 36. Revisions after pilot

After the first pilots, the run report was corrected to count only
newly-appended proposals, and the evaluator's duplicate check was extended to
coverage-lane proposals, eliminating silent re-proposals. The brief decision
section was capped at 12 items with a pointer to the full registry to keep the
brief concise. These revisions were validated by the rerun.

## 37. Pilot rerun results

Run `SJC-LIVE-20260806-0203` repeated 0201/0202 subjects: 8 findings, 0 new
pending proposals, 15 evaluator-rejected duplicates. This proves persistent
duplicate control and restart/resume correctness after revisions.

## 38. Current brief generated

`CURRENT_BRIEF.md` (final snapshot `reports/briefs/20260806T041348Z.md`)
reports mode supervised-live-pilot, run SJC-LIVE-20260806-0203, overall health
HEALTHY, 22 pending proposals, fresh coverage, 0 stale, 0 no-yield, 0 source
gaps, and the exact review commands. `--check` passes.

## 39. Human decisions surfaced

All 22 pending proposals are listed in the brief (12 inline, the rest linked to
the registry) with per-proposal accept commands. An accept → rollback proof on
proposal LIVE-ad9eee3e390e produced decision history `['accept', 'rollback']`
and restored the pending state exactly.

## 40. Publication opportunities

`runtime/adaptive_discovery/publication_candidates.md` prepares suggested
titles, summaries, why-it-matters copy, and relevance labels for Baptist
SilverLeaf campus, First Coast Expressway access, Harris Teeter SilverLeaf, and
SilverLeaf Mega Publix, marking each NOT_APPROVED and identifying which are not
represented in the current demo release. The current four-item site misses
several of these high-value subjects. No review status, decision, or release
was changed.

## 41. Documentation consolidated

`README_INTERNAL.md` now leads with CURRENT_BRIEF and documents the live pilot
and operations doc. `docs/operator_mode.md` startup routine references
CURRENT_BRIEF and the live operations contract. `docs/live_adaptive_operations.md`
and `docs/adaptive_discovery_backtest.md` were rewritten as authority documents.
Stale duplicate status narratives were not added; briefs remain generated.

## 42. Authority hierarchy

Fresh operator path: `README_INTERNAL.md` → `CURRENT_BRIEF.md` →
`docs/live_adaptive_operations.md` (or weekly guide) → durable architecture
(`docs/ARCHITECTURE.md`, `docs/discovery_loops.md`), with
`docs/adaptive_discovery_backtest.md` for simulation.

## 43. Files created

`CURRENT_BRIEF.md`; `reports/briefs/*.md` snapshots;
`scripts/search_adapter.py`, `scripts/prepare_publication_candidates.py`;
refactored `scripts/live_adaptive.py`, `scripts/review_adaptive_proposal.py`,
`scripts/build_current_brief.py`, `scripts/run_live_adaptive_pilot.py`,
`scripts/report_coverage_health.py`; expanded
`data/backtests/task22_replay/replay_evidence.yaml`; runtime state under
`runtime/adaptive_discovery/`; tests `test_search_adapter.py`,
`test_brief_generator.py`, `test_proposal_review.py`, `test_health_model.py`,
`test_live_pilot.py`, `test_publication_candidates.py`; agent log; Task 23
packet and this report.

## 44. Files changed

`README_INTERNAL.md`, `docs/operator_mode.md`, `docs/live_adaptive_operations.md`,
`docs/adaptive_discovery_backtest.md`, `scripts/adaptive_backtest.py`,
`scripts/live_adaptive.py` (rewritten), `data/backtests/task22_replay/config.yaml`
and `replay_evidence.yaml`. Pre-existing Task 20/21/22 untracked files preserved.

## 45. Tests added

51 tests added across the six new/expanded modules covering: brief sections,
ordering, modes, health evidence, stale warnings, atomic replacement, check
mode, private-path exclusion, determinism; adapter budgets, receipts, dedupe,
no-match, retry, domains, dates, provider isolation; review show/accept/reject/
defer/rollback, dry-run, invalid transitions, atomicity, history; health
component/overall/stale/blocked; full live-pilot stages, isolation, budgets,
restart; milestone-overdue, stale subject, yield, and broader-fixture honesty.

## 46. Validation results

`python3 -m pytest tests/ -v`: 274 passed.
`python3 scripts/validate.py`: ALL PASSED.
`validate_publication_corpus.py`: PASS, 0 errors / 321 pre-existing warnings.
`validate_silverleaf_scope.py`: PASS, 0 errors / 0 warnings.
`portability_check.py`: PASS. `git diff --check`: PASS. Brief `--check`: PASS.
Secret/private-path scan of `CURRENT_BRIEF.md`, `reports/briefs/`, and
publication candidates: CLEAN. Backtest regression, expanded replay, live
pilots, rerun, acceptance/rollback proof, health and coverage generation, and
restart/resume proof all completed.

## 47. Runtime and cost

Each live pilot completed in under 2 seconds at $0 estimated cost (credential-
free RSS + official public probes). The full test suite runs in ~40 seconds.
The 66-week backtest replay completes in seconds locally.

## 48. Network activity

Public sources only: `sjcfl.us/news/`, `stjohns.k12.fl.us/` probes, and six
Google News RSS queries across the three pilots (plus three in earlier
scaffold runs). No private, gated, or credentialed network access.

## 49. Privacy and secret audit

No secrets, credentials, `.env`, private paths, or browser state are stored or
referenced by the new code or artifacts. A regex scan of generated Markdown and
runtime receipts found no private markers. User agents identify the repository.

## 50. Known limitations

Google News RSS is lead-discovery only and cannot enforce server-side domain/
date windows. Quantitative missed-milestone state is derived only where due
dates exist. One live pilot cannot yet determine a credible missed-milestone
rate for the live lane; the backtest supplies the honest fixture-level numbers.
The brief decision section shows 12 proposals inline with the rest linked.

## 51. Production-readiness assessment

READY_FOR_SUPERVISED_WEEKLY_PILOT, not autonomous production. Human review of
the 22 pending proposals is required before any accepted adaptive state is
carried forward. Provider hardening (a direct official-source search adapter or
an approved commercial provider), milestone-due maintenance, and source-promotion
review remain before autonomous operation.

## 52. Remaining human decisions

Review and accept/reject/defer the 22 pending proposals in CURRENT_BRIEF.
Approve whether Google News RSS remains the discovery provider or a commercial
provider should be integrated. Decide whether to promote any discovered source
(Jacksonville Daily Record, JaxToday) via the normal source-review path.
Decide whether `runtime/adaptive_discovery/` (pending proposals, decision
history, health, coverage) should be versioned: the existing `.gitignore`
excludes all of `runtime/`, so pending proposals and decisions are currently
local-only and would not survive a fresh checkout; the versioned durable
surface is the brief snapshots under `reports/briefs/`. If the next weekly run
must restore pending proposals from a fresh clone, add a targeted
`.gitignore` carve-out for `runtime/adaptive_discovery/` after review.

## 53. Recommended next weekly run

Run two official health checks and at most three queries targeting the remaining
gaps (utilities/water, hurricane preparedness, commercial construction), plus
any accepted profiles. Re-review pending proposals first; stop on provider
failure, budget breach, sensitive claim, or missing evidence. Regenerate
CURRENT_BRIEF and a dated snapshot after the run.

## 54. Commit plan

After Buddy review, stage explicit Task 22/23 paths only (scripts, tests,
schemas, docs, CURRENT_BRIEF, reports/briefs, task/report packets). Do not
stage unrelated pre-existing Task 20/21 files or secrets. Use conventional
prefixes (feat/docs/data/chore). `runtime/adaptive_discovery/` is excluded by
the repo `.gitignore`; if pending proposals and decisions should be versioned,
add a targeted carve-out for that directory in a follow-up decision. No commit
was made by this task.

## 55. Ivy handoff

None required. Ivy, deployment, VPS scheduling, credentials, and transport were
not modified.

## 56. Final Git status

Working tree contains modified `README_INTERNAL.md`, `ROADMAP.md`,
`docs/ARCHITECTURE.md`, `docs/cadence.md`, `docs/discovery_loops.md`,
`docs/operator_mode.md` and new Task 22/23 files (scripts, tests, runtime,
reports, briefs, tasks). No staging or commits were performed.

## 57. Final task status

**COMPLETE_WITH_FOLLOW_UP.** The supervised live adaptive-discovery workflow,
bounded search with receipts and budgets, human proposal review with rollback,
pipeline-health reporting, broader evidence with milestone/stale/yield metrics,
and the canonical `CURRENT_BRIEF.md` are implemented, tested (274 passing), and
demonstrated by three real pilots and an acceptance/rollback proof. Remaining
work is bounded human evidence review and provider/metric hardening.
