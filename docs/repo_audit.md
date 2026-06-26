# SJC_Intel — Repo Audit

> Audit date: 2026-06-03
> Auditor: sjc-intel-architect
> Scope: Complete repo state, schema compatibility, backlog health,
>   agent readiness, memory structure, self-improvement framework

---

## 1. Current Project Phase

**Phase: Foundation + Pilot Testing**

The project has moved through:
1. **Initial setup** — Agent, memory, repo structure, schemas ✓
2. **Feasibility test** — HTTP 200 for all 5 priority targets ✓
3. **Schema definition** — source.schema v1.0, intel_item.schema v1.0→v2.0 ✓
4. **Source registry** — 8 active sources, 20 communities ✓
5. **Pilot 1 (county)** — Extraction baseline, 5 items, v1.1 schema ✓
6. **Schema reconciliation** — Taxonomy, community registry, channel cleanup ✓
7. **Pilot 2 (sheriff)** — Sensitivity baseline, 4 items, v2.0 schema ✓
8. **Resident-interest classifier** — Agent, prompt, docs, schema v2.0 ✓

Still ahead:
9. Pilot 3 (school district)
10. Hermes cronjob automation
11. Editorial review workflow
12. Publishing pipeline

---

## 2. Files Present

| Category | File | Purpose | Status |
|----------|------|---------|--------|
| Root | `README.md` | Project overview, milestones | Current but stale (sheriff pilot not reflected) |
| Root | `discovery_test.md` | Feasibility test results | Complete |
| Root | `ST_JOHNS_COUNTY_INTELLIGENCE.md` | Comprehensive source map | Complete |
| Schemas | `schemas/source.schema.yaml` v1.0 | Source record schema | Stable |
| Schemas | `schemas/intel_item.schema.yaml` v2.0 | Intel item schema (includes RI fields) | Stable |
| Registry | `registry/sources.yaml` | 8 active + 4 placeholder sources | Current |
| Registry | `registry/communities.yaml` | 20+ community entries | Current |
| Docs | `docs/source_registry.md` | Source registry documentation | Needs cross-ref to communities.yaml |
| Docs | `docs/monitoring_workflow.md` | 10-step Hermes workflow | Current with RI and sensitivity steps |
| Docs | `docs/taxonomy.md` | Controlled vocabularies for all fields | Current |
| Docs | `docs/resident_interest_classification.md` | RI classification docs + 6 examples | Complete |
| Agents | `agents/resident-interest-classifier.md` | RI classifier agent definition | Complete |
| Prompts | `prompts/resident_interest_classification_task.md` | RI task template for Hermes | Complete |
| Data | `data/intel_items/2026-06-03/sjc_county_news.yaml` | 5 county items (v1.1) | Needs v2.0 migration |
| Data | `data/intel_items/2026-06-03/sjc_county_news_report.md` | County pilot report | Current |
| Data | `data/intel_items/2026-06-03/sjso_news_stories.yaml` | 4 sheriff items (v2.0) | Current |
| Data | `data/intel_items/2026-06-03/sjso_news_stories_report.md` | Sheriff pilot report | Current |
| Data | `data/index/prior_items.yaml` | 9-item dedup index | Current |
| Config | `.opencode/opencode.json` | Agent registration | Current |
| Config | `.opencode/agents/sjc-intel-architect.md` | Agent prompt (211 lines) | Current |
| Memory | `.opencode/agent_memory/sjc-intel-architect.memory.md` | Full session memory (664 lines) | Current, but long |

---

## 3. What Is Complete

- Hermes feasibility test (proved concept)
- Source registry with 8 active sources
- Community registry with 20+ entries
- Intel item schema through v2.0 (with RI fields)
- Taxonomy with all classification field vocabularies
- Monitoring workflow documented as 10-step pipeline
- Resident-interest classifier agent, prompt, and docs
- County pilot (5 items, extraction baseline)
- Sheriff pilot (4 items, sensitivity + RI baseline)
- Dedupe index with 9 entries
- Agent prompt with memory management rules

---

## 4. What Is Partially Complete

- **README.md** — Milestone checkboxes don't reflect sheriff pilot completion or RI classifier creation
- **docs/source_registry.md** — Doesn't cross-reference communities.yaml or taxonomy.md
- **sjc_county_news data** — Schema-compliant with v1.1 but missing v2.0 RI fields
- **Memory file** — Current state is up to date but activity log makes the file very long

---

## 5. What Is Missing

| Item | Priority | Notes |
|------|----------|-------|
| `ROADMAP.md` | Medium | Would help agents orient on future milestones |
| `AGENTS.md` (repo root) | Low | Planned but deferred |
| `ORCHESTRATOR.md` (repo root) | Low | Planned but deferred |
| `docs/editorial.md` | Low | 8 editorial rules exist in agent prompt; not yet extracted to standalone doc |
| `workflows/` directory | Low | Empty; workflow definitions in docs/ instead |
| Hermes worker task definitions | High | No actual Hermes task YAML files exist |
| Hermes cronjobs | High | No cron-based scheduling set up |
| Editorial review workflow | Medium | How humans will review/reject/approve items |
| Publishing workflow | Low | Newsletter/website/social output pipeline |
| Self-improvement framework | Medium | Agents can't detect/report friction autonomously |
| Community URLs for placeholders | Medium | SilverLeaf, RiverTown, Shearwater need source discovery |

---

## 6. Schema Status & v1.1/v2.0 Compatibility

### Current State

| Schema | Version | Status |
|--------|---------|--------|
| `source.schema.yaml` | 1.0 | Stable — no changes needed |
| `intel_item.schema.yaml` | 2.0 | Stable — RI fields added |
| `registry/communities.yaml` | 1.0 (inline) | Stable |

### v1.1-v2.0 Gap

The **county pilot** (`sjc_county_news.yaml`) was created under v1.1 and is
**missing** these v2.0 fields:
- `primary_topic`
- `interest_tags`
- `resident_relevance` (entire block)
- `taxonomy_gap`
- `human_review_required`

The **sheriff pilot** (`sjso_news_stories.yaml`) was created under v2.0 and
has all fields.

### Migration Recommendation

**Do NOT migrate the county pilot.** The county data file is an archival
record of the first monitor run. Adding RI fields retroactively would
introduce inference that was not made at the time of extraction. Instead:

1. All future pilots (school district, others) should use v2.0.
2. If the county source is re-monitored (in a real Hermes cycle), the new
   output will use v2.0 automatically.
3. Document this decision in the relevant reports.

### Inconsistency Risk

Low. The two data files are independent artifacts. No downstream process
reads both files simultaneously. The dedupe index is source-specific and
doesn't depend on schema version.

---

## 7. Source Registry Status

| Source ID | Status | Piloted |
|-----------|--------|---------|
| sjc_county_news | active | Yes |
| sjso_news_stories | active | Yes |
| sjso_social_media | verified | No |
| sjc_school_district | verified | No |
| sjc_development_tracker | verified | No |
| nocatee_community | verified | No |
| sjc_property_appraiser | verified | No |
| sjc_tax_collector | verified | No |
| (4 placeholders) | observed | No |

**2 active, 6 verified, 4 observed.** Next to activate: sjc_school_district.

---

## 8. Community Registry Status

**20 entries across 6 types.** Complete for known master-planned communities
and major corridors. Needs expansion when community-specific sources are
discovered (e.g., SilverLeaf HOA page, RiverTown community group).

---

## 9. Taxonomy Status

**Complete.** 22 topics, 10 interest tags, 12 audience types, 5 geographic
scopes, 4 urgency levels, 3 sensitivity levels, 5 verification levels,
6 review statuses, 7 recommended channels. All documented with examples
and classification rules.

---

## 10. Monitor Pilot Status

| Pilot | Items | Schema | Baseline For | Issues |
|-------|-------|--------|-------------|--------|
| sjc_county_news | 5 | v1.1 | Extraction | Missing v2.0 RI fields |
| sjso_news_stories | 4 | v2.0 | Sensitivity + RI | Unicode URL issue on one listing item |
| sjc_school_district | — | — | Complexity | Not yet run |

---

## 11. Resident-Interest Classifier Status

**Complete.** Three files created:
- `agents/resident-interest-classifier.md` — 10 rules, clear inputs/outputs
- `prompts/resident_interest_classification_task.md` — Hermes task template
- `docs/resident_interest_classification.md` — 6 worked examples

One gap: The classifier has no way to be invoked autonomously — it's
documented as a pipeline step but there's no Hermes task definition or
agent configuration that would make it run.

---

## 12. Hermes Readiness Status

| Capability | Ready? | Notes |
|-----------|--------|-------|
| Public source access | Yes | Proven by 2 pilots |
| Item extraction | Yes | Manual webfetch works |
| Deduplication | Yes | Flat-file index exists |
| Classification | Partially | Manual only; no automated Hermes tasks |
| RI classification | Partially | Agent/prompt exist but no execution framework |
| Sensitivity review | Partially | Rules documented; no automation |
| Kanban task creation | No | Not yet set up |
| Cronjob scheduling | No | Not yet set up |
| Output writing | Yes | Manual only |

**Verdict:** Hermes feasibility is proven, but **no Hermes tasks are
defined or deployed**. All pilots run interactively.

---

## 13. OpenCode Agent Readiness

| Agent | Purpose | Self-Improve? | Gaps |
|-------|---------|--------------|------|
| `sjc-intel-architect` | Architecture, schemas, workflows, docs | Limited | No friction-detection framework; no autonomous proposal mechanism |
| `resident-interest-classifier` | RI classification | No | Can't self-invoke; designed as sub-agent but no Hermes task wiring |

### Self-Improvement Gaps

- No mechanism for agents to detect when a schema or taxonomy gap is
  recurring and propose a fix.
- No escalation path for repeated failures or anomalies.
- No process for agents to create or update backlog items.
- Memory updates are manual (agent writes them after sessions).

---

## 14. Editorial/Safety Status

**8 rules defined** in agent prompt. Key gaps:
- No standalone `docs/editorial.md` — rules live only in the agent prompt
- No corrections policy (noted as future work)
- No escalation path for contentious items
- No privacy review checklist

---

## 15. Data/Output Status

| Artifact | Schema | Validated | Notes |
|----------|--------|-----------|-------|
| sjc_county_news.yaml | v1.1 | Yes | Missing v2.0 fields; archival |
| sjso_news_stories.yaml | v2.0 | Yes | Current |
| prior_items.yaml | 1.0 | Yes | 9 entries |
| Both reports | N/A | N/A | Markdown, no schema |

---

## 16. Known Inconsistencies

1. **README.md milestones** — Don't reflect sheriff pilot or RI classifier
2. **Memory "next action"** — Says "run sjc_school_district pilot" but audit
   may change that priority
3. **Workflow registry in memory** — Says "8-step" but actual workflow is
   now 10-step
4. **docs/source_registry.md** — Doesn't reference communities.yaml
5. **County data file** — v1.1 in a v2.0 world (intentional, but a gap)
6. **ROADMAP.md** — Doesn't exist; project trajectory is undocumented
7. **No `.gitignore` adjustments** — `node_modules/` is committed (in .opencode/)

---

## 17. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Schema drift (data files on different versions) | Low | Low | Documented; no cross-file processing |
| Hermes task never built | Medium | High | Must prioritize after pilot 3 |
| Memory bloat (664 lines, growing) | Medium | Medium | Prune activity log to last 3 sessions |
| Backlog item rot (stale planned items) | Medium | Low | Consolidate during next cleanup |
| No self-improvement framework | Medium | Medium | Design after pilot 3 |
| Unicode URL issue on SJSO | Low | Low | Handle in extraction logic |

---

## 18. Memory File Audit

### Structure
- 664 lines — well-organized but **long**
- Clear sections: Current State → Open Items → Decisions → Schema Registry
  → Source Registry → Workflow Registry → Repo Doc Status → Key References
  → Activity Log
- Activity log dominates (5 entries, ~400 lines)

### Strengths
- Current State is concise and actionable
- Open Items table is well-maintained with clear status labels
- Decisions table is a durable record of design choices
- Schema/Source/Workflow registries are accurate snapshots
- Activity log has consistent format (Summary, Decisions, Open Questions, Next Action, Tracker Updates)

### Weaknesses
- **Activity log is too long** — Each entry contains detailed summaries that
  repeat information already in the living sections
- **Stale open questions** in activity log entries — Session 1 questions
  like "Should the monitoring workflow write to artifacts/ or data/?" have
  been resolved but remain in the log text
- **Workflow Registry says "8-step"** but workflow is now 10-step
- **Repo Documentation Status says "Updated with session 2 results"** for
  agent memory — stale description
- **No guidance on self-improvement** — Memory defines how to update but not
  when or why to propose structural changes

### Recommendations
1. **Trim activity log** — Keep only last 2-3 sessions; archive older entries
   to a separate file if needed
2. **Fix stale descriptions** — Update the Repo Documentation Status entry
   for agent memory
3. **Add self-improvement section** — Brief guidelines on proposing changes
4. **Keep living sections** — Current State, Open Items, Decisions are the
   right size and format

---

## 19. Backlog Audit

### All Open Items (from memory, SJC-001 through SJC-036)

See `.opencode/agent_memory/sjc-intel-architect.memory.md` Open Items table.
Of 36 items:
- **22 resolved/verified** — Done
- **5 planned** — Backlog items that may never be needed
- **3 pending** — Active items needing work
- **2 in_progress** — Partially complete
- **4 not yet tracked** — Items identified in this audit

### Thematic Grouping

| Theme | Open Items | Notes |
|-------|-----------|-------|
| **Schemas/Taxonomy** | SJC-005 (workflow schema), SJC-020 (done), SJC-025 (done), SJC-026 (done), SJC-027 (done), SJC-031 (pending), SJC-034 (done) | Mostly resolved |
| **Sources/Monitoring** | SJC-021 (done), SJC-022 (done), SJC-023 (pending), SJC-032 (done), SJC-036 (pending) | Active — pilots 1 and 2 done, pilot 3 pending |
| **RI Classification** | SJC-033 (done), SJC-035 (done) | Complete |
| **Hermes Workflows** | SJC-006 (planned), SJC-007 (done), SJC-008 (planned), SJC-009 (planned), SJC-010 (planned), SJC-019 (planned) | Mostly deferred |
| **Editorial/Review** | SJC-011 (planned), SJC-018 (planned) | Not started |
| **Data/Indexing/Dedup** | SJC-024 (done) | Complete |
| **Repo Operating System** | SJC-001 (done), SJC-002 (done), SJC-014 (planned), SJC-015 (planned), SJC-016 (done), SJC-017 (in_progress) | AGENTS.md and ORCHESTRATOR.md deferred |
| **Future Publishing** | SJC-012 (planned), SJC-013 (planned) | Not started |

### Issues

- **Duplicates/Near-duplicates:** SJC-006 (source discovery) and SJC-008
  (item extraction) are subsumed by the monitoring workflow
- **Stale:** SJC-005 (workflow schema) — monitoring workflow is documented
  inline without a formal schema; may never need this
- **Dependency order:** SJC-023 (school district pilot) depends on:
  - SJC-036 (run the pilot — the actual task)
  - Schema v2.0 (done)
  - RI classification layer (done)
  - No further dependencies remain

### Recommended Cleanup

| Action | Items |
|--------|-------|
| Resolve (mark deferred) | SJC-005, SJC-006, SJC-008, SJC-009, SJC-019 |
| Keep pending | SJC-023 (actually SJC-036), SJC-031 |
| Keep planned (future) | SJC-010, SJC-011, SJC-012, SJC-013, SJC-014, SJC-015, SJC-018 |
| Add new | School district pilot readiness, Hermes task creation, editorial guidelines doc |

---

## 20. Agent Definition Audit

### sjc-intel-architect
- **Purpose:** Architecture, schemas, workflows, docs, editorial systems
- **Status:** Configured and active
- **Context:** 211-line prompt with memory management, project identity,
  editorial rules, design conventions, boundaries
- **Inputs/Outputs:** Well-defined — reads/writes repo files, updates memory
- **Self-improve:** No autonomous improvement framework — agent proposes
  changes via user conversation
- **Gaps:** No Hermes integration, no task delegation ability, no
  self-triggering

### resident-interest-classifier
- **Purpose:** Add resident-perspective layer to intel items
- **Status:** Defined but not executable (no Hermes task wiring)
- **Context:** 81-line agent definition with 10 rules, clear inputs/outputs
- **Inputs/Outputs:** Explicit — structured intel item in, RI fields out
- **Self-improve:** No — proposes new tags via `taxonomy_gap` field
- **Gaps:** No way to invoke autonomously; designed as sub-agent but no
  execution framework

### Hermes Prompt Templates
- `prompts/resident_interest_classification_task.md` — Clear task definition
  with output format. Only RI prompt exists. Missing prompts for:
  - Factual extraction
  - Deduplication
  - Sensitivity review
  - Editorial review
  - Drafting

---

## 21. Self-Improvement Framework (Recommended)

### How Agents Should Detect Friction

1. **Schema gaps:** When a data field is needed but not defined, note via
   `taxonomy_gap` or propose a schema change.
2. **Extraction failures:** When a source returns non-200 or unparseable
   content, log to source registry `last_error` and set status to `failing`.
3. **Recurring patterns:** When the same edge case appears in 3+ monitor
   cycles, open a backlog item to address it.
4. **Memory staleness:** When the activity log exceeds 5 entries, older
   entries should be archived.
5. **Permission friction:** When an agent action is blocked by permissions
   but would clearly benefit the project, open a permission-change ticket.

### How Agents Should Propose Changes

1. **Minor changes** (typo fixes, documentation updates, schema additions
   within existing patterns) — Agent can make directly after confirming
   with memory write.
2. **Medium changes** (new schema fields, new workflows, new source
   registrations) — Agent proposes via conversation with Buddy; Buddy
   approves or redirects.
3. **Major changes** (architectural shifts, public name changes, Hermes
   automation, publishing pipeline) — Agent drafts a proposal; Buddy
   reviews and decides.

### What Agents Can Change Directly

- Memory file (always allowed)
- Documentation files (`.md`)
- Schema and registry files (`.yaml`)
- Data output files (under `data/`)
- Dedupe index
- Taxonomy additions (with `taxonomy_gap` tracking)

### What Requires Buddy Approval

- `.opencode/opencode.json` configuration changes
- `.opencode/agents/` — agent prompt changes
- New file types or directories at repo root
- Any change involving Hermes task creation or cron scheduling
- Publishing or external distribution
- Privacy/editorial rule changes
- Source removals from registry

### How Changes Should Be Recorded

1. **Memory activity log** — Every session that makes durable changes
2. **Decisions table** — Every design decision with rationale
3. **Open Items table** — Every task created or resolved
4. **Repo doc updates** — Every documentation change

### How Memory/Backlog/Docs Should Stay Aligned

1. **After any session:** Update activity log first, then Current State,
   Open Items, Decisions, and any registry/doc tables
2. **Weekly:** Review open items for staleness; close or defer
3. **After each pilot:** Update README milestones, source registry status,
   data output listing
4. **After schema version bump:** Update all affected docs, note in
   schema changelog header

---

## 22. Recommended Next Actions

| # | Action | Priority | Theme |
|---|--------|----------|-------|
| 1 | **Run sjc_school_district monitor pilot** | High | Sources/Monitoring |
| 2 | **Update README.md** to reflect current state (sheriff pilot, RI classifier) | Medium | Repo OS |
| 3 | **Fix docs/source_registry.md** to reference communities.yaml | Low | Repo OS |
| 4 | **Trim memory activity log** — archive sessions 1-3, keep sessions 4-5 | Medium | Repo OS |
| 5 | **Create ROADMAP.md** with upcoming milestones | Medium | Repo OS |
| 6 | **Define Hermes task YAML** for the first monitor workflow | High | Hermes |
| 7 | **Create editorial guidelines doc** (docs/editorial.md) | Medium | Editorial |
| 8 | **Archive county pilot as v1.1** (document that it won't be migrated) | Low | Data |
| 9 | **Add self-improvement section to agent prompt** | Medium | Repo OS |
| 10 | **Audit .gitignore** — node_modules/ is inside .opencode/ | Low | Repo OS |
