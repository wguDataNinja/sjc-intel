# SJC Intel — Prompt-Led Discovery Standards and Architecture

**Date:** 2026-07-06
**Purpose:** Reconcile SJC Intel execution conventions with ivy-control LLM
standards, then design a prompt-led agentic discovery architecture that follows
both.

---

## Part 1 — ivy-control Standards Found

Archaeology of `/Users/buddy/projects/ivy-control` found these active,
authoritative conventions relevant to SJC agentic search:

| Standard | File | Key Content |
|----------|------|-------------|
| LLM Tenets | `policy/llm-tenets.md` | Narrow scope per stage, deterministic narrowing first, structured contracts (input/output/failure), test/fixture/evaluation, audit trail, failure taxonomy, output authority levels, human review boundaries |
| Bounded LLM Policy | `docs/bounded-llm-policy.md` | Non-agentic first, design for weaker models, minimum necessary context, trust earned per task, hard human-approval boundary, expose blast radius, structured interfaces, provider-agnostic |
| Agent Task Template | `templates/hermes/backlog_prep_packet.md` | Identity/objective/context/acceptance/safety/implementation/escalation/git/metadata — YAML schema with file source_type taxonomy, retry policy, git path classification |
| Worker Log Template | `templates/worker_log_template.md` | Structured YAML front matter + per-entry fields: time, run_slug, runtime_agent, status, files_changed, validation, next_action. Chat output convention with BLOCKED: format |
| Tool Permissions | `hermes/ivy_tools.md`, `hermes/ivy_permissions.md` | Three safety lanes (read-only → IVY writes → external writes), agent + orchestrator role split, compact packets only (≤4K/8K chars) |
| Browser Search | `portable/browser_search/SKILL.md` | Three tiers: SearXNG → Camofox → CloakBrowser. Automatic escalation. Read-only. No social media browsing. |
| Git Policy | `AGENTS.md`, `skills/git_steward_agent.md` | Explicit paths, never `git add .`, path classification taxonomy for risk, safe auto-execute rules |
| Session Continuity | `portable/ivy_handoff/` | Point A → Point B pattern, recipient capability × execution mode matrix, handoff packet structure |
| Hermes Governance | `vps/worker-control/reports/HERMES_GOVERNANCE_ARCHITECTURE.md` | Fail-closed conditions, PR body template, scan schedule, audit log format |
| VPS Conventions | `vps/shared-conventions.md` | Run metadata, health contract, backup/restore, shadow/parity/authority transfer |
| Path Classification | `schemas/git_steward_review.schema.json` | safe_docs, safe_context, safe_logs, safe_tooling_review, generated_review, public_approval, sensitive_never, unknown_escalate |

---

## Part 2 — SJC Execution Standards Found

Archaeology of `/Users/buddy/projects/sjc_intel` found these conventions:

| Standard | Files | Key Content |
|----------|-------|-------------|
| Session Startup | AGENTS.md, operator_mode.md, cadence.md | 6-7 step startup, required reads, LAST_RUN evaluation, smallest-safe-task selection |
| Git Policy | AGENTS.md | Explicit paths, conventional prefixes (feat/docs/chore/test/ci), never `git add .`, validate YAML/JSON before commit |
| Logging (3 tiers) | AGENTS.md | Agent logs, run logs, conversation logs with specific path patterns and cadence |
| Worker Context | AGENTS.md | Required reads before any task: README_INTERNAL.md, AGENTS.md, BACKLOG.md, relevant prompt |
| Tool Permissions | `.opencode/opencode.json`, `.opencode/agents/*.md` | Read: wide allow. Edit: ask default. Bash: deny with allowlist. Webfetch/websearch: ask. Task: allow. |
| Prompt Format | `prompts/known_source_monitor_task.md` (and 10 others) | Worker identity + purpose + inputs + step-by-step procedure + output files + reference paths + sensitivity rules + error handling + completion criteria |
| Run Log Format | `logs/runs/daily/*.md` | Run date/time, operator, trigger, cadence status table, work selected, outputs, skipped work, blockers, next action, LAST_RUN updated |
| Agent Log Format | `logs/agents/sjc-intel-architect/*.md` | Task, files read, work completed, validation, boundaries preserved |
| Naming Patterns | Multiple prompts and scripts | `SJC-{prefix}-{YYYYMMDD}-{NNNN}`, `data/intel_items/{date}/`, `logs/runs/{cadence}/{date}_{task}.md`, conventional commit prefixes |
| Failure Handling | known_source_monitor_task.md, cadence.md | HTTP error → block, parse failure → retry once, dedupe missing → warn, partial success → write successful items, monitor failure → do not advance LAST_RUN |
| Safety Rules | AGENTS.md, architect agent definition | Public sources only, no private groups, no auto-publish, human review for sensitive items, attribute sources |

---

## Part 3 — Reconciliation Table

| Concern | SJC Current Practice | ivy-control Standard | Recommended SJC Rule |
|---------|---------------------|---------------------|---------------------|
| **Prompt ownership** | Ad-hoc per task, stored in `prompts/` | Backlog prep packet with structured YAML | Keep SJC's simpler format; adopt ivy's required sections (purpose, inputs, steps, safety, completion) |
| **Prompt versioning** | None — `last_updated` in file comments | Prompt version with SHA-256 hash tracking | Add version comment header to prompts, but keep it lightweight |
| **Session startup** | 6-7 step checklist with required reads | Agent context loading order + START HERE sections | Keep SJC's AGENTS.md startup — it's well-established and specific to SJC |
| **Required context reads** | README_INTERNAL, AGENTS.md, BACKLOG.md, relevant prompt | docs/README → AGENTS → SESSION → TODO → LOG → README | Keep SJC's — it's tighter and more appropriate for the smaller project |
| **Search-tool use** | `websearch: ask`, `webfetch: ask` (in opencode.json) | SearXNG + Camofox + CloakBrowser (three-tier) | Keep OpenCode tools for pilot. Camofox only if a specific source proves JS-dependent |
| **Browser-tool use** | Not configured (bash deny blocks it) | Three-tier: SearXNG → Camofox → CloakBrowser | Add only when needed. No Camofox for SJC pilot. |
| **Evidence capture** | `raw_excerpt` + `citation` on intel items | Audit trail: prompt version, model, input digest, raw/parsed output, validation result | Adopt ivy's audit trail for all search-run records — add run_metadata from idlehacking_kb pattern |
| **Structured output** | YAML intel items with implicit schema | JSON Schema with input/output/failure contracts | Keep SJC's YAML for intel items; add JSON Schema for search-run records |
| **No-result handling** | Not specified for search | `no_match` is a valid outcome, logged but not discarded | Adopt the 5-level match classification (exact/probable/related/unverified/no_match) from the pilot report |
| **Duplicate detection** | Dedupe index (SHA-256 of source+title+date) | Path-based deduplication in search context | Keep SJC's dedupe for intel items; add URL dedup for search candidates |
| **Human review** | review_status: pending_review → verified | Trust earned per stage; classification authority granted per stage, not per model | Keep SJC's review_status for intel items. Add `review_status` to search candidates |
| **Logging** | 3 tiers (agent/run/conversation) + session narratives | LOG.md (append-only) + SESSION.md (living) + logs/workers/ (gitignored) | Keep SJC's 3 tiers. Add structured run records for search (see Part 6) |
| **Continuity updates** | SESSION.md append-only, LOG.md append-only, agent memory | Point A → Point B with handoff packets | Keep SJC's append-only logs. Adopt Point A → Point B for session planning |
| **Validation** | validate.py + pytest + YAML parse checks | Preflight checklist, acceptance criteria, JSON Schema validation | Keep SJC's pattern. Add search-run record validation when implemented. |
| **Git commits** | Explicit paths, conventional prefixes, after meaningful sessions | Same core pattern + path classification taxonomy | Adopt ivy's path classification for commit planning: safe_docs vs sensitive_never vs generated_review |
| **Final reporting** | Not formally specified | Structured chat output with run_slug, status, files, next action | Adopt the ivy worker log chat output pattern |
| **Failure states** | Per-prompt error handling | Per-failure-type retry taxonomy (timeout/malformed/refusal/validation/transient/persistent) | Adopt ivy's retry taxonomy for search runs |
| **Partial completion** | "Write successful items; report per-item status" | Produce failure record, stop stage. No degraded output. | Keep SJC's pattern for search — partial results are useful |
| **Prompt evolution** | Create new prompt file, update last_updated | Version with SHA-256 hash, document exceptions | Add version comments to prompts. Don't add SHA hashing yet. |

---

## Part 4 — Prompt-Led Discovery Architecture

### Architecture Principle

The agentic search follows SJC's existing `known_source_monitor_task.md` prompt
pattern (worker identity + step-by-step + error handling + completion), extended
with ivy-control's structured contracts (input template, output template, failure
handling) and audit trail requirements.

### Workflow: Recurring SilverLeaf Discovery

```
Buddy starts agent session
  → Agent reads: AGENTS.md, README_INTERNAL.md, the discovery prompt
  → Agent reads enabled search profiles from registry (future)
  → Agent reads entity names/aliases from tracked_entities.yaml
  → Agent reads neighborhood names from communities.yaml
  → For each profile:
       Generate query from profile + entity registry
       websearch (with ask confirmation in pilot)
       webfetch promising results
       Classify match (exact/probable/related/unverified/no_match)
       Check duplicates against prior search run records
       Write candidate record
  → Log run outcome
  → Report summary in chat
  → Do NOT write intel_items directly — candidates require review
```

### Workflow: Evidence-Triggered Investigation

```
Deterministic source produces item with unresolved entity/claim
  → Architect creates investigation trigger record
  → Agent reads: AGENTS.md, README_INTERNAL.md, investigation prompt
  → Agent reads trigger record (field: item_id, entity_name, claim, dates)
  → Agent inspects what is already known (grep intel_items, entities)
  → Agent generates bounded queries (max 3 searches, max 5 URLs)
  → websearch + webfetch as above
  → Classify results
  → Propose update or record no-match
  → Do NOT modify canonical registries or intel items directly
```

---

## Part 5 — Minimum Prompt Artifact Set

**Two prompts, not more.** One for recurring discovery, one for triggered
investigation. No separate source-path or candidate-review prompts —
those are architect tasks, not search-specific.

### Prompt 1: Recurring Discovery

| Field | Value |
|-------|-------|
| Path | `prompts/agentic_silverleaf_discovery.md` |
| Purpose | Bounded weekly/monthly search for SilverLeaf entity updates |
| Inputs | `registry/search_profiles.yaml` (future), `registry/tracked_entities.yaml`, `registry/communities.yaml` |
| Reads | `AGENTS.md` (git/logging rules), `README_INTERNAL.md` (product direction), `docs/taxonomy.md` (vocabularies) |
| Allowed tools | Read, Glob, Bash (on allowlist only), **Webfetch (ask)**, **Websearch (ask)** |
| Forbidden | Edit registries, modify intel_items, commit, run backfill, publish |
| Output path | `data/intel_items/{date}/agentic_search_results.yaml` |
| Output schema | See Part 6.2 |
| Log path | `logs/agents/sjc-intel-architect/{date}_agentic_search.md` |
| Stop conditions | 15 minutes elapsed OR 5 URLs fetched OR 3 profiles searched |
| Validation | `python3 -c "import yaml; yaml.safe_load(open('path'))"` |
| Final report | Chat: run_slug, profiles searched, results by match class, files written |

### Prompt 2: Triggered Investigation

| Field | Value |
|-------|-------|
| Path | `prompts/agentic_investigation.md` |
| Purpose | Targeted search triggered by deterministic source change |
| Inputs | Trigger record (item_id, entity_name, claim, dates) + same registry reads as above |
| Reads | Same as discovery + the triggering intel_item |
| Allowed tools | Same as discovery |
| Forbidden | Same as discovery |
| Output path | `data/intel_items/{date}/agentic_investigation_results.yaml` |
| Output schema | Same as discovery results (see Part 6.2) |
| Log path | Same pattern |
| Stop conditions | 10 minutes OR 3 queries OR 5 URLs |
| Validation | Same |
| Final report | Same format |

### What NOT to Create

- No source-path discovery prompt (architect does this interactively)
- No candidate-review prompt (architect reviews manually)
- No Hermes runtime (pilot uses interactive OpenCode)
- No separate prompt for SilverLeaf specifically (the discovery prompt reads
  search profiles from data, so it works for any entity set)

---

## Part 6 — Logging and Run Records

### 6.1 Run Record (Structured YAML)

Written to `data/search_runs/{YYYY-MM-DD}/{run_id}.yaml`:

```yaml
run_id: "SRCH-{YYYYMMDD}-{NNNN}"
prompt_version: "agentic_silverleaf_discovery.v1"
agent: "sjc-intel-architect"
model: "opencode-go/qwen3.5-plus"
mode: scheduled  # or event_triggered
trigger: null    # or trigger record ID

profile_ids:
  - "sl_retail_publix"
  - "sl_education_k8"

started_at: "2026-07-06T14:00:00Z"
completed_at: "2026-07-06T14:15:00Z"

queries_issued:
  - query: '"SilverLeaf Publix" site:sjcitizen.com'
    result_count: 3
    urls_considered:
      - url: "https://sjcitizen.com/..."
        fetch_status: fetched
        match_class: exact

  - query: '"SilverLeaf K-8" site:sjcitizen.com'
    result_count: 1
    urls_considered: []

urls_fetched: 2
errors: []

summary:
  profiles_searched: 2
  total_results: 2
  by_match_class:
    exact: 1
    probable: 0
    related: 0
    unverified: 1
    no_match: 0

files_written:
  - "data/intel_items/2026-07-06/agentic_search_results.yaml"

validation: "yaml parse OK"
```

### 6.2 Search Candidate Record (Structured YAML within results file)

```yaml
candidates:
  - candidate_id: "CAND-{YYYYMMDD}-{NNNN}"
    run_id: "SRCH-{YYYYMMDD}-{NNNN}"
    profile_id: "sl_retail_publix"
    entity_id: "ENT-RETAIL-PUBLIX-SILVERLEAF"
    url: "https://sjcitizen.com/..."
    title: "Article title"
    snippet: "First 200 chars or key excerpt"
    published_at: "2026-07-01"
    retrieved_at: "2026-07-06T14:05:00Z"
    match_class: exact  # exact | probable | related | unverified | no_match
    evidence:
      - field: "title"
        value: "SilverLeaf"
      - field: "body"
        excerpt: "...Publix at SilverLeaf Parkway..."
    duplicate_of: null        # or candidate_id if known duplicate
    review_status: pending_review
    notes: ""
```

### 6.3 What Goes Where

| Content | Location | Retention | Purpose |
|---------|----------|-----------|---------|
| Run record | `data/search_runs/{date}/{run_id}.yaml` | 30 days | Structured audit trail, query-by-query |
| Candidate records | `data/intel_items/{date}/agentic_search_results.yaml` | Until reviewed | Input to review queue |
| Human-readable log | `logs/agents/sjc-intel-architect/{date}_agentic_search.md` | Indefinite | Session continuity, lessons learned |
| Chat output | LLM chat history | Ephemeral | Real-time status |
| Git commit | Git history | Permanent | Only for prompt/registry/schema changes, not search results |

---

## Part 7 — Git and Repository Workflow

| Action | When | Example |
|--------|------|---------|
| **Do NOT commit** | Search run results, transient candidates, rejected material | `data/search_runs/`, `agentic_search_results.yaml` |
| **Commit** | Prompt changes | `prompts/agentic_silverleaf_discovery.md` |
| **Commit** | Registry or schema changes | `registry/search_profiles.yaml` |
| **Commit** | Planning doc updates | `docs/planning/*.md` |
| **Commit** | Search profile additions | `registry/search_profiles.yaml` |
| **Leave uncommitted** | Search run output files, agent logs | `data/search_runs/*`, `logs/agents/*` |

**Rule:** Search results are generated data, not curated project state. They
follow the same convention as `data/intel_items/` — committed only when they
represent curated project state. During pilot, they are reviewed and either
promoted to intel_items (committed) or discarded (not committed).

---

## Part 8 — Staged Implementation Sequence

| Phase | What | Depends On |
|-------|------|-----------|
| 1 | Draft `prompts/agentic_silverleaf_discovery.md` | This design doc approved |
| 2 | Create `registry/search_profiles.yaml` with 3 profiles | Phase 1 |
| 3 | Manual pilot: run discovery prompt with Buddy | Phase 2 |
| 4 | Draft `prompts/agentic_investigation.md` | Lessons from Phase 3 |
| 5 | Manual pilot: run investigation prompt | Phase 4 |
| 6 | Create `data/search_runs/` directory + validation script | Phase 5 |
| 7 | Refine based on real results | Phases 3-6 complete |
| 8 | Design automation (future — not in scope) | All above stable |

---

## Part 9 — Next Implementation Prompt

```
Create prompts/agentic_silverleaf_discovery.md following the prompt
structure in docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md.

The prompt must:
- Define the agent as a "silverleaf-discovery-worker"
- Require reads: AGENTS.md, README_INTERNAL.md, docs/taxonomy.md,
  registry/tracked_entities.yaml, registry/communities.yaml
- Reference search profiles from the future registry/search_profiles.yaml
  (description only — file does not exist yet)
- Allow: Read, Glob, Bash (allowlist), Webfetch (ask), Websearch (ask)
- Forbid: editing registries, modifying intel_items, committing,
  running backfill, publishing
- Define the 5-level match classification
- Specify output path as data/intel_items/{date}/agentic_search_results.yaml
- Include the run record schema from Part 6.1
- Include error handling for: HTTP errors, empty results, websearch
  unavailability, timeout, rate limiting
- Set stop conditions: 15 minutes OR 5 URLs fetched OR 3 profiles searched
- Require validation: yaml parse check on output file
- End with the ivy worker log chat output format

Do NOT create registry/search_profiles.yaml yet.
Do NOT run the prompt yet.
```

---

## Summary

- **ivy-control standards found:** LLM tenets, bounded LLM policy, agent task
  template, worker log template, three safety lanes, browser search tiers,
  git path classification, handoff patterns, fail-closed conditions

- **Recommended for adoption:** Audit trail for LLM calls, structured input/
  output/failure contracts, worker log chat output format, run record with
  metadata, match classification with no-match as valid outcome, path
  classification for git planning

- **Rejected:** Full backlog_prep_packet YAML (too heavy for SJC's scale),
  Camofox browser automation (not needed for pilot), SHA-256 prompt versioning
  (premature), Hermes runtime (pilot uses interactive agents)

- **Prompt files that should exist:** `prompts/agentic_silverleaf_discovery.md`,
  `prompts/agentic_investigation.md`

- **Logs and run records:** Structured YAML run records at
  `data/search_runs/{date}/{run_id}.yaml`, candidates at
  `data/intel_items/{date}/agentic_search_results.yaml`, agent log at
  `logs/agents/sjc-intel-architect/{date}_agentic_search.md`

- **Git handling:** Prompt/registry/schema changes committed. Search run
  results NOT committed. Generated data committed only when curated.

- **Next implementation session:** Create `prompts/agentic_silverleaf_discovery.md`
  (the prompt file only, no search runtime, no search profiles file yet)
