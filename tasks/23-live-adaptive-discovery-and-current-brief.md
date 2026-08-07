# Task 23 — Live Adaptive Discovery, Human Review, and Current Operational Brief

**Session:** Strong Codex, new session, working from `/Users/buddy/projects/sjc_intel`.
**Mode:** supervised-live-pilot. Broad implementation, integration, validation,
and polish session. Authorized to inspect/modify the repository broadly, run
stateful local commands, use approved public network sources, revise agents and
prompts, add schemas and scripts, consolidate documentation, execute supervised
discovery pilots, evaluate results, and improve the repository toward reliable
publication. Do not stop at assessment; implement all safe work and write one
authoritative final report to `reports/23-live-adaptive-discovery-and-current-brief.md`.

## Human-facing outputs

* `CURRENT_BRIEF.md` at the repository root — the canonical current operational
  brief, regenerated from durable state after every meaningful run.
* One dated immutable snapshot per regeneration under `reports/briefs/YYYY-MM-DDTHHMMSSZ.md`.
* Task report: `reports/23-live-adaptive-discovery-and-current-brief.md`.
* `CURRENT_BRIEF.md` and the report must not duplicate each other.

## 1. Mission

Move the adaptive-discovery system from a deterministic historical harness into
a trustworthy supervised live-pilot workflow capable of: known-source
monitoring; bounded live public-web discovery; full query/result/cost/source/
timestamp/disposition recording; resident-subject detection; entity/alias/
project/source/search/milestone/timeline/coverage-lane proposals; independent
evaluation; one concise Markdown brief for all pending human decisions; explicit
accept/reject/defer/rollback; application of accepted proposals to isolated
production adaptive state carried into the next weekly run; pipeline/coverage
health, failure, gap, and upcoming-work reporting; history preserved in versioned
artifacts; file-first and PostgreSQL-dormant; restartable/rerunnable/auditable;
and publication-readiness via prepared (not auto-applied) SilverLeaf candidates.

Governing objective: after each run, Buddy reads one obvious, current,
versioned Markdown document with everything needed on health, findings, gaps,
proposed state changes, publication opportunities, and required decisions.

## 2. Required source material

Read the repository authority hierarchy and inspect the current implementation:
`README.md`, `README_INTERNAL.md`, `AGENTS.md`, `ROADMAP.md`, `BACKLOG.md`,
`docs/ARCHITECTURE.md`, `docs/discovery_loops.md`, `docs/cadence.md`,
`docs/operator_mode.md`, `docs/adaptive_discovery_backtest.md`,
`docs/weekly_operational_contract.md`, `docs/weekly_operator_guide.md`,
`docs/publication_release_contract.md`, `docs/public_ui_v0_spec.md`,
`reports/20-expanded-corpus-editorial-review.md`,
`reports/21-resident-coverage-backtest-assessment.md`,
`reports/22-adaptive-discovery-backtest-implementation.md`, `tasks/README.md`,
`reports/README.md`, and the harness reference at
`/Users/buddy/projects/alori/learn-harness-engineering/notes.md`.

Apply harness-engineering principles (repository as system of record; bounded
task state; initialization and restartability; generator/evaluator separation;
observable loops; explicit evidence; full-pipeline verification; failure
containment; current-state handoff; clean completion criteria) without
mechanically reproducing the course structure.

## 3. Locked decisions

1. **File-first authority.** PostgreSQL remains DORMANT_FUTURE_READY. Do not activate it.
2. **Human proposal control.** Agents may propose but never silently canonize
   or apply sources, entities, aliases, projects, places, search profiles,
   milestones, timelines, or coverage lanes. Explicit human acceptance is
   required for production adaptive state.
3. **Simulation vs production isolation.** Keep historical backtest state,
   supervised live-pilot state, accepted production adaptive state,
   publication decisions, review queue, and public releases isolated. Every
   artifact identifies its mode.
4. **Publication boundary.** Do not automatically verify intelligence items,
   approve publication, publish, change the current release, or modify the
   public UI from unreviewed findings. Preparation of candidates and
   recommended copy is allowed.
5. **Source policy.** Public sources only. No login-gated groups, private
   social feeds, private portals, or credentials not already authorized.
   Official sources remain primary authority for consequential claims; local
   media may surface leads and context.
6. **Scope.** The central purpose is the live adaptive-discovery workflow and
   `CURRENT_BRIEF.md`. Documentation and publication-readiness improvements are
   secondary and bounded.

## 4. CURRENT_BRIEF.md

See the brief generator contract below. It must be the first operational
document a human reads, prominently linked from `README_INTERNAL.md` and any
operator entrypoint that currently forces inspection of multiple status files.

### Properties
Markdown; concise (3–7 minute read); readable without opening YAML;
regenerated from durable run state; safe to commit; free of secrets and
private infrastructure details; explicit about uncertainty; explicit about
simulation vs live mode; source-backed; version-linked; deterministic in
section ordering; limited to currently relevant material.

### Required header
`# SJC_Intel Current Brief`, then `**Generated:**`, `**Mode:**`,
`**Run ID:**`, `**Repository SHA:**`, `**Data cutoff:**`,
`**Overall health:**`, `**Publication status:**`, plus links to the latest
dated brief snapshot, latest weekly run artifact, pending-proposal registry,
latest coverage-health report, relevant task report, and the public SilverLeaf
Brief if available. Use relative repository links.

### Required sections (stable order)
1. Executive summary (3–8 bullets)
2. Pipeline health (compact component table with evidence and action)
3. What changed since the previous brief
4. Important resident findings (grouped by resident concern)
5. Coverage health
6. Decisions needed (proposal queue grouped HIGH_PRIORITY / ROUTINE /
   DEFERRED / BLOCKED, with acceptance command per decision)
7. Publication opportunities
8. Risks and failures
9. Next run plan
10. Commands for Buddy
11. Provenance

### Versioning
Every regeneration writes `reports/briefs/YYYY-MM-DDTHHMMSSZ.md`; the current
brief identifies that snapshot. No manually numbered briefs. Git history is the
long-term history.

### Generator
`python3 scripts/build_current_brief.py` must derive content from durable state
and run artifacts; fail when required health evidence is missing; warn about
stale inputs; produce stable ordering; avoid unsupported conclusions; create the
dated snapshot; atomically replace `CURRENT_BRIEF.md`; support `--check`; support
a supplied run ID; support production/pilot/simulation modes; and validate output
structure. Add tests.

## 5. Live bounded discovery

A provider-neutral search interface (`scripts/search_adapter.py`) supporting
query, allowed/excluded domains, result limit, date window, budget, timeout,
retry limit, user agent, receipts, raw-result preservation, normalized records,
deduplication, source-type labeling, and no-match records. Do not hardwire to one
provider. Provide at least one practical live mode in the current environment
(credential-free Google News RSS) plus a deterministic stub for simulation and
tests, or document a precise provider blocker. Do not scrape search engines in
violation of their rules.

Every query records a receipt: run ID, query ID, exact query, source profile,
domains, simulated/real time, started/completed timestamps, result count,
accepted count, duplicate count, failure, cost estimate, budget remaining,
result URLs, and hashes. Receipts are stored separately from human reports.

Budgets are supported per run, coverage lane, search profile, subject, and
source domain, and must prevent uncontrolled agent-generated query expansion.
Budget status appears in `CURRENT_BRIEF.md`.

## 6. Proposal review and rollback

`python3 scripts/review_adaptive_proposal.py` with `show`, `accept`, `reject`,
`defer`, and `rollback` subcommands. Must: show evidence before mutation; show
the exact proposed state change; show affected future searches; validate IDs;
preserve append-safe decision history; prohibit accidental bulk acceptance;
reject invalid state transitions; apply accepted changes atomically; support
`--dry-run`; support rollback; preserve rejected proposals; regenerate the
current brief after a successful decision; and never change publication state.
Add tests.

## 7. Supervised live-pilot state

Isolated runtime state at `runtime/adaptive_discovery/` containing accepted
entities/aliases/projects/places/sources/search profiles/coverage lanes/
milestone plans, timelines, unresolved gaps, last-run state, pending proposals,
decision history, and health state. Do not duplicate canonical registries
without a clear promotion boundary. Document which records are proposals vs
canonical. State must be inspectable, snapshottable, restorable, rollback-able,
initializable safely, and independently validatable.

## 8. Supervised live pilot

Run at least one bounded supervised live-pilot cycle using approved public
sources and searches seeded from existing canonical sources and approved search
profiles. Do not seed hidden evaluation subjects into discovery prompts. Stages:
known-source monitoring → bounded live discovery → evidence normalization →
identity reconciliation → strategist proposals → coverage-lane analysis →
evaluator review → pending-proposal persistence → coverage-health generation →
current-brief generation. Do not auto-accept proposals. Inspect quality/false
positives/missing sources/weak queries/duplicate proposals/unsupported claims/
budgets/health/report usefulness; revise where evidence supports it; rerun the
bounded pilot after material revisions; compare results.

Evaluator interests (not instructions to fabricate findings): Magnolia Oaks
Academy, CR 2209, First Coast Expressway access, Baptist SilverLeaf campus,
Publix center, Harris Teeter center, active shopping-center tenants, nearby
commercial construction, utilities, major roads, and other resident concerns.

## 9. Broader historical evidence and milestone scoring

Expand the historical replay evidence enough to test realistic breadth without
rewriting the full corpus (School QQ/Magnolia, CR 2209, FCE, Publix, Harris
Teeter, Baptist, water shortage, hurricane preparedness, major roads and
utilities, plus Task 20 construction/growth subjects). Add missed-milestone
detection, overdue-milestone state, stale-subject detection, search-profile
yield tracking, false-positive tracking, source freshness, and lane coverage
health. Do not tune scoring for perfect results; report misses honestly.

## 10. Pipeline-health model

Machine-readable `runtime/adaptive_discovery/health.yaml` plus human summary in
`CURRENT_BRIEF.md`, covering source_health, known_source_capture, live_search,
normalization, dedupe, identity_reconciliation, strategist, editor, evaluator,
proposal_storage, proposal_review, timeline_state, milestones, coverage_health,
publication_candidate_handoff, report_generation, state_persistence. Each
component: status (HEALTHY/DEGRADED/BLOCKED/STALE/NOT_CONFIGURED), last
success, last failure, evidence artifact, freshness threshold, failure count,
warning count, action required. Overall health derives from components using
documented rules; never hand-written.

## 11. Publication-readiness support

Use live and historical findings to identify publication opportunities.
Prepare, but do not execute, candidate source checks, suggested titles,
suggested summaries, why-it-matters copy, relevance labels, timeline/context
proposals, Browse/archive additions, and Latest candidates. Identify whether
the current four-item site is missing high-value subjects. Do not change
publication decisions or the release. Bounded UI/doc defect fixes are allowed
but this task is not a UI redesign.

## 12. Documentation consolidation and discoverability

Ensure a fresh operator can start from `README_INTERNAL.md` → `CURRENT_BRIEF.md`
→ relevant operator guide → durable architecture. Correct stale current-state
claims, duplicated operational status, competing "latest" documents, obsolete
run instructions, old agent responsibilities, and conflicting adaptive-discovery
descriptions. Do not delete useful historical reports. Do not copy task history
into permanent architecture docs. End with clear authority for architecture,
discovery loops, adaptive discovery, weekly operation, proposal review, health,
publication, backtesting, and current status.

## 13. Creative authority

Implement additional improvements that materially increase trust, correctness,
observability, restartability, operator clarity, publication readiness,
resident relevance, source quality, failure visibility, or report usefulness
(e.g., proposal summary renderer, coverage-health scoring, stale-subject
detector, subject timeline summary, source-yield report, query-budget dashboard
in Markdown, safer atomic state updates, additional tests, clearer operator
commands, pruning redundant status docs, stronger validation). Do not expand
into databases, account systems, subscriptions, live incidents, maps, public
APIs, autonomous publication, VPS deployment, or Ivy changes.

## 14. Required tests

Current brief (required sections, stable ordering, snapshot link, mode
labeling, health evidence, stale-input warning, atomic replacement, check mode,
secret/private-path exclusion, deterministic generation); search adapter
(budgets, receipts, normalized results, duplicate handling, no-match handling,
failure/retry, date/domain constraints, provider isolation); proposal review
(show, accept, reject, defer, rollback, dry-run, invalid transitions, atomicity,
decision history, brief regeneration); health (component status, stale
detection, degraded/blocked overall, evidence links, freshness thresholds); live
pilot (full stage execution, proposal persistence, evaluator separation, no
publication mutation, bounded budget, restart/resume, report generation);
historical improvements (milestone overdue, stale subject, search-profile
yield, broader fixture, honest missed-target scoring).

## 15. Required validation

Run: `python3 -m pytest tests/ -v`, `python3 scripts/validate.py`,
`python3 scripts/validate_publication_corpus.py`,
`python3 scripts/validate_silverleaf_scope.py`,
`python3 scripts/portability_check.py`, `git diff --check`, `git status --short`.
Also run the Task 22 backtest regression, expanded historical replay,
search-adapter tests, live supervised pilot, pilot rerun after revisions,
proposal-review dry runs, one isolated acceptance and rollback proof on
nonproduction fixture state, pipeline-health generation, current-brief
generation, current-brief check, restart/resume proof, secret/private-path scan
of generated Markdown, and the full pipeline from search result to pending
proposal and brief. Record exact commands and results.

## 16. Git and versioning

Do not commit or push unless explicitly authorized. Prepare a clean commit plan.
Versionable: `CURRENT_BRIEF.md`, dated brief snapshots, proposal schemas,
operator tooling, health logic, durable configuration, accepted production
decisions when explicitly made, tests, authority docs. Avoid committing raw
volatile caches, secrets, browser state, unbounded raw search responses where
policy says transient, and redundant generated artifacts. Document retention
for search receipts and raw results.

## 17. Prohibited actions

No PostgreSQL activation; no review-status modification; no publication
decision modification; no publishing; no public-release change; no Ivy
modification; no VPS deployment; no timers; no private sources; no secret
exposure; no automatic acceptance of all proposals; no strategist self-
evaluation; no production-readiness claims from fixture-only success; no hiding
failed searches or missed subjects; no force-push; no overwriting unrelated
user changes.

## 18. Stop conditions

Stop only for a genuine human or credential blocker: no lawful/approved
live-search path; a required source is private; unexplained conflicting repo
state; a decision would alter publication policy; a destructive action would be
necessary; live credentials or paid-provider approval required. Do not stop for
failing tests, weak search results, false positives, missing schemas, stale
docs, prompt revisions, reruns, or report complexity.

## 19. Required final report

One comprehensive report at `reports/23-live-adaptive-discovery-and-current-brief.md`
with the following sections: 1 Executive result, 2 Starting repository and Git
state, 3 Authorities inspected, 4 Decisions made, 5 Creative improvements made,
6 Final architecture, 7 CURRENT_BRIEF.md design, 8 Brief generator, 9 Brief
versioning and snapshots, 10 Pipeline-health model, 11 Health evidence and
derivation, 12 Live-search adapter, 13 Search providers and limitations,
14 Query budgets, 15 Search receipts, 16 Human proposal-review workflow,
17 Acceptance implementation, 18 Rejection and deferral, 19 Rollback,
20 Production adaptive state, 21 State initialization and restore,
22 Coverage-health implementation, 23 Stale-subject detection,
24 Milestone-overdue detection, 25 Search-yield tracking,
26 Expanded historical evidence, 27 Backtest regression,
28 Supervised live-pilot configuration, 29 First live-pilot results, 30 Findings,
31 Important subjects discovered, 32 Important subjects missed, 33 False
positives, 34 Proposals generated, 35 Evaluator outcomes,
36 Revisions after pilot, 37 Pilot rerun results, 38 Current brief generated,
39 Human decisions surfaced, 40 Publication opportunities,
41 Documentation consolidated, 42 Authority hierarchy, 43 Files created,
44 Files changed, 45 Tests added, 46 Validation results, 47 Runtime and cost,
48 Network activity, 49 Privacy and secret audit, 50 Known limitations,
51 Production-readiness assessment, 52 Remaining human decisions,
53 Recommended next weekly run, 54 Commit plan, 55 Ivy handoff if any,
56 Final Git status, 57 Final task status.

The report must let Buddy and GPT judge whether live discovery is trustworthy,
the human proposal process is safe, the current brief is complete and useful,
pipeline health is visible, the repository can run supervised weekly
operations, and what still blocks publication breadth or production activation.

## 20. Success criteria

`CURRENT_BRIEF.md` exists at the root, linked prominently from the operator
entrypoint, generated from durable state, with a dated immutable snapshot;
pipeline health reported with evidence; recent findings, coverage gaps, pending
human decisions, publication opportunities, risks/failures, and next-run plan
reported; live bounded search can run or a precise provider blocker is proven;
every search has a receipt; budgets enforced; review commands exist and
accept/reject/defer/rollback work; no proposal silently canonized; supervised
state isolated and restartable; pipeline-health artifact exists; stale subjects
and overdue milestones visible; search-profile yield measured; broader
historical evidence tested; Task 22 leakage protections intact; a supervised
live pilot runs, is independently evaluated, and is revised after real evidence;
a pilot rerun demonstrates the resulting behavior; publication opportunities are
prepared without publication mutation; operational docs easier to navigate; one
authoritative final report produced; remaining work bounded and explicit; Buddy
can understand repository state by reading one concise Markdown file.

## Launch instruction

New Strong Codex session. Work from `/Users/buddy/projects/sjc_intel`. Read and
execute this task. Implement the supervised live adaptive-discovery workflow,
bounded search with receipts and budgets, human proposal
acceptance/rejection/deferral/rollback, pipeline-health reporting, broader
evidence and milestone scoring, and one canonical versioned operational
document: `CURRENT_BRIEF.md`. Generate a dated immutable snapshot under
`reports/briefs/` whenever it changes. Make safe improvements that increase
trust, observability, restartability, resident relevance, operator clarity, and
publication readiness. Do not stop at assessment. Implement, run, evaluate,
revise, and polish. Write one authoritative engineering report to
`reports/23-live-adaptive-discovery-and-current-brief.md`. Do not activate
PostgreSQL, modify review/publication state, modify Ivy, deploy, enable timers,
use private sources, expose secrets, commit, or push unless separately
authorized.
