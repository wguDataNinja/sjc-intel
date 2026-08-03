# Tasks (inbox)

Bounded task packets for agent execution, per the GPT-Orchestrated Workflow
(`ivy-control-vps/_internal/GPT_ORCHESTRATED_WORKFLOW.md`).

- One task = one stable ID = one result report in `../reports/`.
- Task IDs: `NN-<slug>.md` (NN = sequence within session).
- Each task names: objective, roadmap authority, scope, exclusions, files to
  inspect, work to execute, validation, required evidence, Git boundaries,
  stop conditions, result-report requirements.

Current session: **session-2026-08-02 (resume)** — see `tasks/01-resume-roadmap-assessment.md`.

## History note

`prompts/` holds **reusable task templates** (the prompt library), not
dispatched task instances. Dispatched bounded tasks live here in `tasks/`.
The former `_outbox/` was folded into `reports/` on 2026-08-02.
