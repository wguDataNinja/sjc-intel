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

1. Read `README_INTERNAL.md` — primary dev entrypoint with current state and architecture.
2. Read `.opencode/agent_memory/sjc-intel-architect.memory.md` — concise current memory.
3. Read `BACKLOG.md` — for highest-priority open item.
4. Read `docs/operator_mode.md` if Buddy says "get to work".
5. Read `docs/cadence.md` and check `logs/runs/{daily,weekly,monthly}/LAST_RUN` for due work.
6. Confirm task does not require live monitoring, backfill execution, source promotion,
   or publishing without explicit approval.

## Worker Context-Gathering Requirement

Before starting any task, workers must read:
1. `README_INTERNAL.md` — project state and architecture
2. `AGENTS.md` — rules, git policy, logging expectations
3. `BACKLOG.md` — task context if applicable
4. Relevant monitor spec or task prompt — extraction/classification rules

## Git Policy

- Agents do NOT commit unless explicitly instructed by Buddy.
- Commit after meaningful completed sessions that produce durable output.
- Git Steward is the preferred commit agent.
- Stage explicit paths only — never use broad `git add .` without Git Steward review.
- Inspect `git diff` and `git status` before staging anything.
- Conventional commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `data:`.
- Never commit: secrets, `.env`, credentials, private exports, raw GPT transcripts,
  `node_modules/`, caches, or large generated dumps.
- Generated data under `data/` may be committed when it represents curated project state
  (intel items, dedupe index, review queue).
- Validate YAML/JSON before commit when touching structured data.
- If unsure about a file, leave it unstaged and ask.

## Logging Rules

Three logging tiers:

| Tier | Content | Location | Cadence |
|------|---------|----------|---------|
| Agent logs | What agents did, decisions, friction, rationale | `logs/agents/{agent_name}/{YYYY-MM-DD}_{task}.md` | Per session |
| Run logs | Pipeline execution, extractions, cadence work | `logs/runs/{daily,weekly,monthly}/{YYYY-MM-DD}_{task}.md` | Per cadence run |
| Conversation logs | Buddy's GPT/research outputs (curated summaries) | `logs/conversations/{YYYY-MM-DD}_{topic}.md` | Per research thread |

Rules:
- Agent logs record technical decisions, files read/changed, friction encountered.
- Run logs record what cadence was evaluated, what was selected, what was produced.
- Conversation logs are curated summaries, not raw transcripts by default.
- Log meaningful work; do not log trivial no-op sessions.
- Update LAST_RUN markers after completing cadence work.
- Full session narrative: `logs/sessions/` for major buildout sessions.

## Memory Rules

- Memory is for current operating state only.
- Do not store long history, secrets, private content, or raw sensitive data.
- Point to logs and source-of-truth docs instead of duplicating them.
- Architect memory must stay under ~100 lines. Archive to logs when it grows.

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

## Session Checklists

### Start Of Session
- Read `README_INTERNAL.md` and `AGENTS.md`.
- Read `.opencode/agent_memory/sjc-intel-architect.memory.md`.
- Check `BACKLOG.md` for the highest-priority open item.
- Check `docs/operator_mode.md` if Buddy says "get to work".
- Check `docs/cadence.md` and evaluate due work from LAST_RUN markers.
- Confirm the task does not require live monitoring, backfill execution,
  source promotion, or publishing without explicit approval.

### Before Hermes Delegation
- Define the exact input files and output files.
- State whether web access is needed.
- Confirm public-source-only boundaries.
- Include dedupe and sensitivity rules.
- Specify what should be logged.
- Make the task small enough to verify.

### After Hermes Completion
- Inspect output files for schema shape and obvious overreach.
- Check source URLs and public accessibility assumptions.
- Confirm sensitive items are `pending_review` and human-review-required.
- Update `BACKLOG.md` and agent memory if durable state changed.
- Add or update an agent log.

### End Of Session
- Update changed docs (`README_INTERNAL.md`, `BACKLOG.md`, etc.).
- Write meta-run log to `logs/runs/{cadence}/{YYYY-MM-DD}_{task}.md`.
- Update `logs/runs/{cadence}/LAST_RUN` timestamp.
- Write agent log to `logs/agents/{agent_name}/{YYYY-MM-DD}_{task}.md`.
- Keep agent memory concise (< 100 lines).
- Do not leave unreported blockers.
