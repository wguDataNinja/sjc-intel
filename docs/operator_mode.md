# Operator Mode

## Trigger

When Buddy says "get to work", `sjc-intel-architect` should operate from the
repo state without requiring the project to be re-explained.

## Startup Routine

1. Read `README_INTERNAL.md`.
2. Read the concise memory file.
3. Read `BACKLOG.md`.
4. Read `docs/cadence.md` and `logs/runs/README.md`.
5. Check `logs/runs/daily/LAST_RUN`, `logs/runs/weekly/LAST_RUN`,
   `logs/runs/monthly/LAST_RUN` to determine what cadence work is due.
6. Select the highest-priority unblocked task from the due cadence buckets
   that does not require explicit approval.
7. Announce the selected task and why.

## How To Pick Next Work

Priority order:

1. Fix blockers that prevent operator readiness.
2. Keep source-of-truth docs coherent.
3. Advance Deep Research ingestion review.
4. Prepare source-promotion or Hermes task plans.
5. Improve workflows from concrete failure or friction.
6. Defer publishing, automation, and speculative abstractions.

## Direct Work Vs Hermes Delegation

Do direct repo work when:

- The task is documentation, registry cleanup, schema review, or backlog/state
  maintenance.
- The task needs architecture judgment.
- The task can be completed safely without live public-source execution.

Delegate to Hermes when:

- A public web/source collection task has clear inputs and outputs.
- A monitor/backfill run has been explicitly authorized.
- The task can be verified from produced files.

## Logging

- Create/update an agent log for meaningful work.
- Update `README_INTERNAL.md` after durable changes.
- Update `BACKLOG.md` when statuses change.
- Keep memory short and point to the latest log.

## Memory Updates

Memory should include only:

- current phase
- Deep Research ingestion status
- next recommended task
- active backlog summary
- current blockers
- latest log pointer

Archive narrative history in logs, not memory.

## Avoiding Overbuilding

- Do not create new systems until a real workflow needs them.
- Prefer candidate registries and review notes over canonical changes.
- Keep taxonomy concise; use `taxonomy_gap` until evidence accumulates.
- Do not design publishing until the review queue is real.

## Handling Uncertainty

- Label uncertainty directly.
- Prefer official records before media or social claims.
- Create a review item when a source may be useful but unverified.
- Ask Buddy only when the decision would promote a source, change taxonomy,
  run live collection, schedule automation, publish, or touch private/gated
  content.
