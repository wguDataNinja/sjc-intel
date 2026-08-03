# SJC-2026-08-02-03 — Monthly Cadence Closeout (June/July)

- **Task ID:** `03-monthly-cadence-closeout`
- **Session:** `session-2026-08-02` (resume)
- **Repository:** `/Users/buddy/projects/sjc_intel`
- **Branch:** `master` (post-disposition state)
- **Agent role:** OpenCode (implementation) — bounded cadence work
- **Result report:** `reports/03-monthly-cadence-closeout.md` (singular report)

## Objective

Execute the overdue monthly cadence closeout (LAST_RUN 2026-06-08, ~55 days
overdue per `reports/01-resume-roadmap-assessment.md`). Produce the monthly
wrap for June and July 2026: item counts, topic clusters, source-gap review,
and resident-interest themes — following the repo's existing monthly patterns.

## Current accepted state (verified 2026-08-02)

- Monthly cadence LAST_RUN: `2026-06-08T04:31:15Z` — **~55 days overdue**
- `data/monthly/` holds 2026-05, 2025-08, 2025-09 backfills; **no 2026-06/07**
- Monthly pattern precedent: `data/monthly/*`, `data/monthly/*_crosscut.md`,
  `docs/data_inventory/COVERAGE.md` + `GAPS.md` (updated after each
  backfill/monitor cycle per BACKLOG DATA-003)
- Existing intel items through 2026-07-06 (post-T1 disposition if completed)

## Roadmap authority

- `docs/cadence.md` — monthly cadence rules (tolerance: may slip a few days;
  55 days is a major overrun)
- `BACKLOG.md` DATA-003 (data inventory update after each cycle),
  DATA-001/002 (coverage + homeowner perspective docs)
- `reports/01-resume-roadmap-assessment.md` — monthly closeout is the
  recommended alternative task

## Scope — what to do

1. **Inventory June+July items**: gather all intel items, source events, and
   review-queue rows dated 2026-06-01 through 2026-07-31 from
   `data/intel_items/`, `data/source_events/`, `data/review_queue/`.
2. **Produce monthly wrap**: counts by source, by taxonomy topic, by
   resident-interest classification; month-over-month comparison with
   `data/monthly/2026-05*`.
3. **Topic clustering**: group items into clusters (precedent:
   `data/monthly/*_crosscut.md` pattern).
4. **Source-gap review**: identify sources with no captured items in June/July
   vs their monitor expectations (e.g., sources whose cadence should have
   produced items). Write findings to the wrap.
5. **Update data inventory**: refresh `docs/data_inventory/COVERAGE.md` +
   `GAPS.md` per DATA-003.
6. **Write monthly artifacts** to `data/monthly/2026-06.md` (or the repo's
   established monthly naming) and the result report.

## Exclusions (do not)

- Do NOT run live monitors, backfills, or any network fetch — this task works
  from ALREADY-CAPTURED data only.
- Do NOT touch `logs/runs/` LAST_RUN markers (cadence markers are updated by
  the operator/architect, not this task) — unless the repo convention
  explicitly requires the monthly marker update; if so, note it in the report
  and update it.
- Do NOT modify ROADMAP.md, source registry, schemas, or taxonomy.
- Do NOT promote review-queue items.
- Do NOT `git add .` — explicit paths only; commit curated artifacts if the
  repo convention requires, otherwise leave uncommitted and report.

## Files to inspect

- `docs/cadence.md` (monthly rules), `BACKLOG.md` (DATA section)
- `data/intel_items/2026-06-*`, `data/intel_items/2026-07-*`
- `data/source_events/2026-06-*`, `data/source_events/2026-07-*`
- `data/review_queue/queue.yaml`, `data/review_queue/summary.yaml`
- `data/monthly/2026-05*` (precedent), `docs/data_inventory/COVERAGE.md`,
  `docs/data_inventory/GAPS.md`
- `docs/taxonomy.md`, `registry/interest_filters.yaml`
- `reports/01-resume-roadmap-assessment.md` (cadence findings)

## Validation

- Wrap counts reconcile against `data/intel_items/` + `data/review_queue/`
  (counts must be traceable, not invented)
- `python3 scripts/validate.py` + `python3 -m pytest tests/ -q` — must stay
  green if run
- Report: item counts, clusters, source gaps, coverage update summary

## Stop conditions

- Data inconsistencies that cannot be resolved from captured data → report,
  do not invent counts.
- Need for network/monitor access → stop (out of scope).
- Cadence marker update requirement conflicts with repo convention → report.

## Result-report requirements

One report at `reports/03-monthly-cadence-closeout.md`: task identity;
starting Git state; June+July item counts by source/topic/RI-class;
month-over-month comparison; topic clusters; source-gap findings; data
inventory updates; files changed; validation results; unresolved issues;
final status (COMPLETE / PARTIAL / BLOCKED / HUMAN_DECISION_REQUIRED).

## Candidate next tasks (propose, don't create)

1. Recommended next (e.g., daily catch-up runs — 29d overdue).
2. Alternative if blocked.
3. Evidence required before either can begin.
