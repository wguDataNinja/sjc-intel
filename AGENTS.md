# SJC_Intel Agents

## Repo Purpose

SJC_Intel is an AI-assisted local intelligence/reporting system for St. Johns
County, Florida. It is homeowner/resident-first and uses public sources to
discover, monitor, classify, verify, and organize local information.

## Agent Locations

| Type | Location | Purpose |
|------|----------|---------|
| Interactive OpenCode agents | `.opencode/agents/{name}.md` | Agents you talk to and delegate to |
| Agent memory | `.opencode/agent_memory/{name}.memory.md` | Persistent state for each agent |
| Task prompts | `prompts/{task_name}.md` | Bounded Hermes task contracts |
| Role definitions | `agents/{name}.md` | Documentation-only role descriptions |

Interactive agents (OpenCode agents) live in `.opencode/agents/` with matching
memory files. Task prompts for Hermes delegation live in `prompts/`. Role
definitions that document what a worker does (but isn't interactive) live in
`agents/`.

## Agent Roles

| Agent | Type | File | Memory | Purpose |
|-------|------|------|--------|---------|
| `sjc-intel-architect` | Interactive | `.opencode/agents/sjc-intel-architect.md` | `.opencode/agent_memory/sjc-intel-architect.memory.md` | Top-level operator, architecture steward, workflow designer, delegation planner |
| `sjc-intel-source-watch` | Interactive | `.opencode/agents/sjc-intel-source-watch.md` | `.opencode/agent_memory/sjc-intel-source-watch.memory.md` | Source discovery, source health, gap tracking |
| `resident-interest-classifier` | Task prompt + role definition | `agents/resident-interest-classifier.md` (role) + `prompts/resident_interest_classification_task.md` (executable) | — | Adds resident-perspective layer to extracted items |
| Hermes workers | Task prompts | `prompts/known_source_monitor_task.md`, `prompts/hermes_*.md` | — | Bounded delegated task executors |

## Startup Routine

1. Read `STATE.md`.
2. Read `.opencode/agent_memory/sjc-intel-architect.memory.md`.
3. Read `BACKLOG.md` and `ROADMAP.md` when choosing work.
4. Follow `docs/operator_mode.md` if Buddy says "get to work".

## Logging Rules

- Log meaningful agent work under `logs/agents/{agent_name}/`.
- Keep narrative history in `logs/sessions/`.
- Record durable design decisions in `logs/decisions/`.
- Update `STATE.md` after durable state changes.

## Memory Rules

- Memory is for current operating state only.
- Do not store long history, secrets, private content, or raw sensitive data.
- Point to logs and source-of-truth docs instead of duplicating them.

## Safety Rules

- Public sources only.
- No private Facebook groups or login-gated resident portals.
- No fake accounts or impersonation.
- No publishing without explicit scope and review.
- Local media is context/tip-surfacing unless verified by official records.
- Human review is required for sensitive, legal, public-safety, school-safety,
  crime, or controversy items.

## Delegation Rules

- Delegate only clear, bounded tasks with specified inputs and outputs.
- Do not run live monitors or backfills without explicit instruction.
- Do not create cron, launchd, or scheduled automation.
- Verify output files before marking a task complete.

## Source Of Truth Files

- `STATE.md` — current operating state
- `ROADMAP.md` — phase plan and readiness criteria
- `BACKLOG.md` — actionable work list
- `CHECKLIST.md` — operational gates
- `docs/operator_mode.md` — behavior when told to get to work
- `docs/discovery_loops.md` — loop operating model
- `docs/taxonomy.md` — controlled vocabularies
- `registry/sources.yaml` — canonical sources
- `registry/source_candidates.yaml` — candidate sources
- `registry/beat_candidates.yaml` — candidate beats
- `registry/search_terms.yaml` — operational search terms
- `.opencode/agent_memory/sjc-intel-architect.memory.md` — concise agent memory
