# Hermes weekly entry point

**Purpose:** This is the first file a weekly Hermes orchestrator reads. It
defines the bounded weekly worker run and the handoff to a human reviewer.

**Current state:** The weekly task declaration is `enabled: false`. There is no
active scheduler and no authority here to enable one. A human may authorize a
single supervised/manual weekly run; production scheduling remains gated.

## Read in this order

1. `README_INTERNAL.md` — project purpose and safety boundary.
2. `CURRENT_BRIEF.md` — current adaptive findings, health, and decisions.
3. `deploy/sjc-weekly-task.yaml` — approved monitors, limits, and activation
   state. Stop if it is not the dispatch envelope's exact task.
4. `prompts/sjc_weekly_ops_task.md` — worker instructions and forbidden paths.
5. `docs/weekly_operational_contract.md` — bundle and transfer contract.
6. `docs/human_review.md` — the human-owned decisions that follow a run.

## The weekly boundary

There are two related, deliberately separate workflows:

| Workflow | Runs where | Output | Human decision |
|---|---|---|---|
| Weekly candidate collection | Hermes/runner | An isolated, verified transfer bundle | Accept/reject/defer candidate items and source proposals |
| Adaptive discovery | Supervised local operator | Durable adaptive proposals plus `CURRENT_BRIEF.md` | Accept/reject/defer/rollback adaptive state proposals |

Neither workflow publishes, changes a canonical registry, or changes the
website. Do not merge their state stores or treat a discovery lead as an
editorially reviewed item.

## Research escalation

Before an ambiguous adaptive proposal reaches a human, the workflow runs
bounded public-source research. See `docs/live_adaptive_operations.md` and
`scripts/research_escalation.py`. Trigger categories: identity uncertainty,
geographic conflict, stale evidence, conflicting sources, and material resident
importance. The research stage is bounded (default max 8 queries, 10 results),
produces receipts, and yields a research-resolution record with a recommended
action. The strategist never evaluates its own research; the independent
evaluator does. `ACCEPT_QUALIFIED` tracks a subject with explicit uncertainty;
a confirmed tenant always requires a first-party source.

## Resident Coverage Editor

After the strategist and before the independent evaluator, the Resident
Coverage Editor assesses whether a SilverLeaf resident would reasonably expect
an update that is missing, stale, weakly tracked, or under-researched. It
creates structured gap findings and recommends bounded next actions only; it
does not search, accept, or edit state. The weekly run retains its output with
the evidence artifact, and `CURRENT_BRIEF.md` surfaces the material gaps.

## One supervised weekly run

The dispatch envelope must provide the pinned checkout SHA, a new run ID,
UTC window, and the approved monitor list. The initial supported monitors are
`sjc_nbor_public_notices` and `sjso_news_stories`.

1. Verify the pinned SHA and a clean checkout. Abort on mismatch.
2. Verify `deploy/sjc-weekly-task.yaml` still has `enabled: false` unless an
   explicit scheduler-gate authorization is included in the envelope.
3. Run only the listed approved monitors with `scripts/run_weekly.py`; write
   only to `runtime/weekly/<run-id>/`.
4. Build and verify the transfer bundle. A failed verification is a failed run,
   not a partial handoff.
5. Report the bundle path, status, candidate counts, source failures, budgets,
   and any escalation in `run.json` and `logs/run.log`.
6. Stop. Do not import into the corpus, accept a candidate, promote a source,
   alter adaptive state, publish, deploy, or enable a timer.

For a local offline simulation, use the exact command in
`docs/weekly_operator_guide.md` with the NBOR HTML and SJSO RSS fixtures. It
exercises the worker boundary without public-network activity.

## Handoff

The worker hands the verified bundle to the human operator. The operator uses
`docs/human_review.md` to decide what, if anything, enters the review queue or
adaptive state. A run with no accepted decisions is complete and valid.

## Stop conditions

Stop and record an escalation for: a non-pinned revision, an existing run ID,
an unapproved monitor, missing/invalid bundle checksums, a protected-path
write, sensitive-content ambiguity, budget/time exhaustion, source failure,
or any request to publish/promote/schedule.
