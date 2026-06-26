# SJC_Intel — Logging Policy

> Defines how SJC_Intel preserves narrative history, agent activity, and
> durable decisions outside of operational agent memory.

---

## Core Principle

**Memory is for operating state. Session logs are for narrative history.
Agent logs are for task accountability. Decision logs are for durable
commitments.**

Agent memory (`.opencode/agent_memory/sjc-intel-architect.memory.md`)
must stay compact and operational. Narrative history belongs in
`logs/sessions/`. Agent actions belong in `logs/agents/`. Durable
decisions belong in `logs/decisions/`.

---

## Log Types

| Type | Directory | Purpose | Length |
|------|-----------|---------|--------|
| **Session log** | `logs/sessions/` | Human-readable story of a work session | Medium/long |
| **Agent log** | `logs/agents/{agent_name}/` | What an agent did during a run | Short/structured |
| **Decision log** | `logs/decisions/` | Durable decisions only | Short |

---

## 1. Session Logs

**File pattern:** `logs/sessions/{YYYY-MM-DD}_{short_description}.md`

**Purpose:** Preserve the narrative arc of a work session — what was
attempted, what was completed, what was decided, what is next. These are
written for humans and future agents to understand project history.

**Required sections:**
- **Date** — ISO date of the session
- **Project** — Always "SJC_Intel"
- **Participants/Agents** — Who or what participated
- **Summary** — 2-5 paragraph overview
- **Work completed** — Bullet list of durable output
- **Decisions made** — Key decisions with rationale
- **Files created/updated** — Full paths
- **Open questions** — Any unresolved questions
- **Next actions** — Recommended next steps

**Cadence:** One session log per major human-agent interaction session.
Multiple agent runs within one human session share one session log.

---

## 2. Agent Logs

**File pattern:** `logs/agents/{agent_name}/{YYYY-MM-DD}.md`

**Purpose:** Record what an agent did during a specific run — inputs
consumed, actions taken, outputs produced. Useful for debugging,
auditing, and accountability.

**Required sections:**
- **Date/Time** — When the run occurred
- **Agent name** — Which agent executed
- **Trigger/Request** — What initiated the run
- **Inputs read** — Files consumed
- **Actions taken** — What the agent did
- **Files changed** — Files created or modified
- **Outputs produced** — Results returned
- **Blockers** — Any issues encountered
- **Next recommended action** — What the agent suggests next

**Cadence:** One agent log per discrete agent run. If a Hermes worker
runs 3 tasks in one cycle, each task gets a separate entry within the
same day's file.

---

## 3. Decision Logs

**File pattern:** `logs/decisions/{YYYY-MM-DD}_{short_description}.md`

**Purpose:** Preserve durable design decisions with context, rationale,
and consequences. These are the canonical record of why the system is
designed the way it is.

**Required sections:**
- **Decision date** — When the decision was made
- **Decision title** — Short name
- **Context** — What prompted the decision
- **Decision** — What was decided
- **Rationale** — Why this choice
- **Consequences** — What this enables or forecloses
- **Status** — active, superseded, reconsidering

**Cadence:** When a decision affects architecture, schemas, workflows,
or project direction that future agents or humans need to understand.
Not for minor operational choices.

---

## Memory Policy

| What | Where | Length |
|------|-------|--------|
| Current state | `.opencode/agent_memory/sjc-intel-architect.memory.md` | ~5 lines |
| Next actions | `.opencode/agent_memory/sjc-intel-architect.memory.md` | ~5 lines |
| Durable decisions | `.opencode/agent_memory/sjc-intel-architect.memory.md` (summary) + `logs/decisions/` (full) | Summary in memory |
| Active backlog | `.opencode/agent_memory/sjc-intel-architect.memory.md` | As needed |
| Last 2-3 session summaries | `.opencode/agent_memory/sjc-intel-architect.memory.md` | Short paragraphs |
| Full narrative history | `logs/sessions/` | Unlimited |
| Agent task records | `logs/agents/` | Unlimited |
| Full decision records | `logs/decisions/` | Unlimited |

**Rules:**
1. Memory must not carry full narrative history. That belongs in
   `logs/sessions/`.
2. Memory must not duplicate full agent logs. That belongs in
   `logs/agents/`.
3. Decision summaries in memory may reference decision log files for
   full context.
4. When memory grows past ~400 lines, archive old activity log entries
   into `logs/sessions/` and trim.

---

## Agent Self-Logging Rule

1. When an agent completes meaningful work, it should append or create
   an agent log (`logs/agents/{agent_name}/{YYYY-MM-DD}.md`).
2. If the task changes project direction or makes a durable design
   decision, also create or update a decision log
   (`logs/decisions/{YYYY-MM-DD}_{description}.md`).
3. If the task is part of a larger human work session, summarize it
   in the session log or note that a session log update is needed.
4. If an agent detects a pattern or gap worth preserving for future
   sessions, add it to a session log or decision log rather than
   cluttering memory.
