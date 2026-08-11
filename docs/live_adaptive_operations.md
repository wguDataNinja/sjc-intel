# Supervised live adaptive discovery

**Authority:** this document defines the live-pilot layer. `CURRENT_BRIEF.md`
is the current human status; `docs/adaptive_discovery_backtest.md` remains the
historical-simulation contract.

Durable governance authority is isolated at `data/adaptive_discovery/`; volatile
execution artifacts are isolated at `runtime/adaptive_discovery/`. Live runs may
create pending proposals but never change production registries, review queue,
publication decisions, or the public release. Google News RSS is a
credential-free discovery lead provider; its results require primary-source
verification for consequential claims. The search provider boundary is
`scripts/search_adapter.py`; it is provider-neutral and enforces budgets,
receipts, domain/date constraints, and deduplication.

## Workflow

Known-source monitoring → active targeted search profiles → bounded discovery
→ evidence normalization → identity/entity reconciliation → ambiguity/conflict
detection → **bounded research escalation** → Resident Coverage Strategist →
**Resident Coverage Editor** → independent evaluation → pending human
proposals → publication opportunities → coverage/pipeline health →
`CURRENT_BRIEF.md`.

Before a human sees an ambiguous proposal, `scripts/research_escalation.py`
runs bounded follow-up research. Trigger categories: identity uncertainty,
geographic conflict, stale evidence, conflicting sources, and material resident
importance. Every escalation has a budget (default max 8 queries, 10 results
per query, official sources first, local reporting second), receipts, and a
stop condition. The strategist never evaluates its own research; the
independent evaluator applies the recommended action (`ACCEPT`,
`ACCEPT_QUALIFIED`, `DEFER`, `REJECT`, `RESEARCH_AGAIN`). An `ACCEPT_QUALIFIED`
result tracks the subject with explicit uncertainty (e.g., "SilverLeaf grocery
center — possible Harris Teeter"); a confirmed tenant always requires a
first-party source.

## Commands

```bash
# Bounded supervised live-pilot cycle (receipts + proposals + health)
python3 scripts/run_live_adaptive_pilot.py --run-id SJC-LIVE-YYYYMMDD-0001 \
  --query '"Magnolia Oaks Academy" SilverLeaf' \
  --query '{"query": "\"CR 2209\" St. Johns", "lane": "roads and mobility"}' \
  --budget 3

# Run the reviewed recurring search profiles (one bounded supervised cycle).
python3 scripts/run_live_adaptive_pilot.py --run-id SJC-LIVE-YYYYMMDD-0002 \
  --accepted-profiles --budget 28

# Research escalation for ambiguous proposals
python3 scripts/research_adaptive_proposal.py check --proposal-id <ID>
python3 scripts/research_adaptive_proposal.py classify --proposal-id <ID>
python3 scripts/research_adaptive_proposal.py resolve --proposal-id <ID> \
  --query '"SilverLeaf" "Harris Teeter"' --budget 8 --persist

# Regenerate the canonical brief + immutable snapshot
python3 scripts/build_current_brief.py
python3 scripts/build_current_brief.py --check

# Human proposal review (one proposal per invocation)
python3 scripts/review_adaptive_proposal.py show --proposal-id <ID>
python3 scripts/review_adaptive_proposal.py accept --proposal-id <ID> --reviewer Buddy --rationale "evidence reviewed"
python3 scripts/review_adaptive_proposal.py reject --proposal-id <ID> --reviewer Buddy --rationale "reason"
python3 scripts/review_adaptive_proposal.py defer --proposal-id <ID> --reviewer Buddy --rationale "follow up later"
python3 scripts/review_adaptive_proposal.py rollback --proposal-id <ID> --decision-id <DEC> --reviewer Buddy --rationale "undo"

# Coverage health (live or backtest)
python3 scripts/report_coverage_health.py --live
python3 scripts/report_coverage_health.py --state-root data/backtests/task22_replay

# Publication-readiness candidates (preparation only; never publishes)
python3 scripts/prepare_publication_candidates.py
```

## State layout

`data/adaptive_discovery/` is the versioned authority required to recover human
governance after a fresh checkout:

| Artifact | Purpose |
|----------|---------|
| `accepted_state.yaml` | Accepted isolated adaptive state (entities, aliases, search profiles, lanes, milestones, timelines) |
| `pending_proposals.yaml` | Pending human-review proposals |
| `decisions.yaml` | Append-only decision history (accept/reject/defer/rollback) |
| `health.yaml` | Derived pipeline-health model with evidence and freshness |
| `coverage_health.yaml` | Coverage health: fresh/stale subjects, no-yield queries, source gaps |

`runtime/adaptive_discovery/` is intentionally ignored and contains only
reproducible/transient execution artifacts:

| Artifact | Purpose |
|----------|---------|
| `runs/<run_id>/run.yaml` | Full run artifact (findings, proposals, evaluator outcome, budgets) |
| `runs/<run_id>/receipts.yaml` | Per-query search receipts |
| `publication_candidates.md` | Prepared publication opportunities (never approved) |

## Rules

- Human review accepts, rejects, defers, or rolls back exactly one proposal at
  a time; acceptance updates only durable isolated adaptive state and regenerates
  `CURRENT_BRIEF.md`.
- Every query produces a receipt with query ID, timestamps, result counts,
  duplicates, failure, budget before/after, result URLs, hashes, and raw SHA.
- Budgets are enforced per run and may be limited per lane, search profile,
  subject, and source domain. `run_pilot` refuses to exceed the run budget.
- Search receipts and raw hashes are retained under the run as versioned
  operational evidence; no browser profiles or credentials are used.
- The evaluator stage is separate from the strategist: it validates evidence,
  rejects duplicates, and never approves itself.
- The Resident Coverage Editor runs after the strategist and before evaluation.
  It does not search or approve recommendations. Its structured gap findings
  live at `runtime/adaptive_discovery/runs/<run_id>/resident_coverage_editor.yaml`
  and return through the normal research/evaluator/human-review path.
  It includes **stale-milestone escalation** (Task 33): an accepted subject
  whose expected milestone has passed without fresh coverage triggers a
  `SEARCH_NOW` finding so important subjects are not quietly left stale.
- Stop on budget breach, provider/source failure, sensitive material, or lack
  of source evidence.

## Health model

`health.yaml` reports each pipeline component (known-source capture,
live search, normalization, dedupe, identity reconciliation, strategist,
editor, evaluator, proposal storage, proposal review, timeline state,
milestones, coverage health, publication-candidate handoff, report
generation, state persistence) with status, last success/failure, evidence
artifact, freshness threshold, and failure/warning counts. Pipeline health is
derived: BLOCKED if the run was blocked, DEGRADED if any component is
DEGRADED/BLOCKED/STALE, otherwise HEALTHY. Statuses are never hand-written.
`CURRENT_BRIEF.md` separately reports operator status: any pending proposal
sets it to `NEEDS_REVIEW`, and the overall status is `NEEDS_REVIEW` even when
the pipeline itself is healthy. Publication readiness remains separate.
