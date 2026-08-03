# Reports (outbox)

Singular result reports for dispatched tasks, per the GPT-Orchestrated
Workflow. One report per task, keyed by task ID in `../tasks/`.

- Report IDs mirror task IDs: `NN-<slug>.md`.
- Each report includes: task identity, starting Git state, files
  inspected/changed, work performed, validation commands + results, evidence
  provenance, Git status, unresolved issues, risks, candidate next tasks,
  final status (COMPLETE / COMPLETE_WITH_FOLLOW_UP / PARTIAL / BLOCKED /
  HUMAN_DECISION_REQUIRED).

Existing report moved from former `_outbox/` on 2026-08-02:
- `silverleaf-discovery-pilot-results-2026-07-06.md`

Run logs for cadence work remain in `logs/runs/` — those are operational
logs, not task result reports.
