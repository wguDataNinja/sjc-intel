# Agent Self-Improvement

## Purpose

Agents should improve SJC_Intel by detecting repeated friction, proposing small
changes, and keeping logs, memory, backlog, and state aligned. This is an
operating discipline, not permission to overbuild.

## How Agents Detect Friction

Flag friction when:

- The same manual step repeats across sessions.
- A source cannot be monitored because a workflow is unclear.
- A schema field is ambiguous or repeatedly misused.
- Search terms return low-quality or private/login-gated results.
- Taxonomy choices force broad catch-all labels.
- Hermes tasks fail because inputs/outputs are underspecified.
- Memory or state becomes too long to orient quickly.

## How Agents Propose Improvements

- Add a backlog item with owner, priority, dependency, and next action.
- Add a `taxonomy_gap` only when tied to real source/item evidence.
- Add a short note in an agent log when the friction affected a run.
- Update docs directly only when the change is low-risk and consistent with
  existing rules.

## Autonomous Changes Allowed

- Search-term additions/refinements in `registry/search_terms.yaml`.
- Candidate-source or candidate-beat notes.
- Backlog/status/log updates.
- Clarifying docs that do not change policy.
- Non-canonical planning artifacts.

## Changes Requiring Buddy Approval

- Canonical source promotion to `registry/sources.yaml`.
- Taxonomy additions or schema changes.
- Publishing, newsletter, or public-facing claims.
- Live monitor execution or scheduled automation.
- Use of any source that might be private, login-gated, or sensitive.

## Keeping Logs, Memory, Backlog, And State Aligned

- `STATE.md` answers current phase, next task, readiness, and blockers.
- `BACKLOG.md` carries actionable work by area.
- Memory carries compact operational state and pointers to logs.
- `logs/agents/` records what an agent did.
- `logs/sessions/` carries narrative history when needed.

Do not duplicate long narrative in memory.

## Taxonomy Gap Flow

1. Worker records `taxonomy_gap` on an item or review artifact.
2. Architect groups similar gaps.
3. Architect checks existing taxonomy coverage.
4. If real, draft a proposed definition and examples.
5. Buddy approves before canonical taxonomy/schema change.

## Source Candidate Promotion Flow

1. Add candidate to `registry/source_candidates.yaml`.
2. Dedupe against `registry/sources.yaml`.
3. Assess public access, reliability, cadence, owner, and source family.
4. Recommend promotion or deferral.
5. Buddy approves.
6. Architect adds canonical source and updates candidate status.

## Failed Monitor Run Improvement Flow

1. Log failure with source, URL, command/task, and failure mode.
2. Decide whether the issue is source structure, prompt/task ambiguity, schema
   gap, dedupe issue, or transient access failure.
3. Add one backlog item or patch one workflow.
4. Do not mark the monitor reliable until a rerun verifies it.
