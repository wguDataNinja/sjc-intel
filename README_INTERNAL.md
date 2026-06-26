# README_INTERNAL

```yaml
agent_context:
  repo:
    name: sjc_intel
    purpose: AI-assisted local intelligence/reporting for St. Johns County, Florida
    status: supervised operator mode
    ecosystem: ivy
    home: /Users/buddy/projects/sjc_intel
  entrypoint: README.md / AGENTS.md / .opencode/agents/sjc-intel-architect.md
  memory_source: README_INTERNAL.md
  architect_memory: .opencode/agent_memory/sjc-intel-architect.memory.md
  source_watch_memory: .opencode/agent_memory/sjc-intel-source-watch.memory.md
  cadence_system: docs/cadence.md
  run_logs: logs/runs/{daily,weekly,monthly}/LAST_RUN
  monitor_specs: docs/monitor_specs/
```

## What This Repo Is

SJC_Intel discovers, monitors, classifies, and organizes public information
about St. Johns County, Florida — focused on master-planned communities,
government decisions, utilities, schools, roads, and development. It produces
structured intelligence items for editorial review, not published news.

It operates in **supervised operator mode**: no cron, no launchd, no
scheduled automation. Buddy says "get to work", the agent evaluates what
cadence work is due from LAST_RUN markers, picks the smallest safe task,
executes or delegates to Hermes, and writes a meta-run log.

## Recent Work — 2026-06-03 Session

This session built the entire system from concept through operating baseline.

### Deep Research Ingestion

- ChatGPT Deep Research report archived, extracted, and converted into
  candidate sources (45), beat candidates (14), and search terms (52).
- Official records established as first authority for consequential claims.
- CDD governance, utilities/water, transportation/roadwork defined as
  first-class homeowner operating areas.

### Codex Strong Repo Advancement

- Created ROADMAP.md, CHECKLIST.md, BACKLOG.md, AGENTS.md, docs/operator_mode.md,
  docs/self_improvement.md. Trimmed architect memory to concise state.

### Tier 1 + Tier 2 Source Promotions (Hermes Delegated)

- 15 sources promoted across 3 Hermes tasks (A: promote, B: promote, C: review).
- Total canonical sources: 24.
- Tier 3 (CDD) and Tier 4 (community/developer) remain in candidate registry.
- Hermes delegation pattern proven: contract → execute → validate → state update.

### May 2026 Historical Backfill

- 21 items extracted across 5 source families.
- 4 topic clusters, 7 source gaps, 2 taxonomy gaps with real evidence.
- Phase III Extreme Water Shortage was the dominant story.
- All 6 pass criteria met. YAML validated.

### Backfill-Informed Monitor Specs

- 6 spec documents created for sjc_utility_department, sjc_school_stack,
  sjc_bcc_calendar, sjc_nbor_public_notices, plus backfill_lessons and README.

### sjc_utility_department Monitor Pilot

- First daily-ready source. 5 items extracted. Hermes-ready confirmed.
- Pilot lessons applied: sidebar extraction scope added, spec updated.

### Cadence System

- docs/cadence.md created with daily/weekly/monthly rhythms and LAST_RUN markers.
- logs/runs/ structure created with README.md and initialized timestamps.

### Additional Track Work

- `water_restrictions` promoted to canonical taxonomy.
- `sjc_school_stack` pilot run (2 new June items, signal/noise filtering validated).
- `HERMES-003` (search discovery template) drafted.
- Road closures app investigated — data confirmed behind NBOR application;
  exact URL needs browser inspection.
- Data inventory and homeowner perspective docs created.
- `sjc-intel-source-watch` agent defined with memory file.
- AGENTS.md updated with agent location guidance.
- Session closeout appended to session log.

## Current Architecture

### Sources

| Status | Count | Details |
|--------|-------|---------|
| Canonical | 24 | Tier 1 (10 official stacks) + Tier 2 (5 school/transport/weather/civic) + 9 pre-existing |
| Candidates (recommend_promotion) | 11 | Tier 3 CDD (4) + Tier 4 community (6) + media (1) |
| Deferred | 13 | Lower priority |
| Duplicates | 6 | Already covered by canonical |

### Monitors

| Source | Cadence | Status | Spec |
|--------|---------|--------|------|
| sjc_utility_department | Daily | ✅ Pilot passed, daily-ready | `docs/monitor_specs/sjc_utility_department.md` |
| sjc_county_news | Daily | ✅ Pilot passed | `docs/monitoring_workflow.md` |
| sjso_news_stories | Daily | ✅ Pilot passed | `docs/monitoring_workflow.md` |
| sjc_school_stack | Weekly | ✅ Pilot run (filtering validated) | `docs/monitor_specs/sjc_school_stack.md` |
| sjc_bcc_calendar | Weekly | ⬜ Spec ready, not piloted | `docs/monitor_specs/sjc_bcc_calendar.md` |
| sjc_nbor_public_notices | Daily | ✅ Extractor ready — 25 records, plain HTML | `docs/monitor_specs/sjc_nbor_public_notices.md` |
| sjc_emergency_management | Daily/seasonal | ⬜ Spec designed | From backfill lessons |

### Agents

| Agent | Location | Memory | Role |
|-------|----------|--------|------|
| `sjc-intel-architect` | `.opencode/agents/` | `.opencode/agent_memory/` | Top-level operator, delegation planner, state steward |
| `sjc-intel-source-watch` | `.opencode/agents/` | `.opencode/agent_memory/` | Source discovery, source health, gap tracking |
| `resident-interest-classifier` | `agents/` (role) + `prompts/` (task) | None (task prompt) | Adds resident-perspective layer to items |

### Hermes Task Contracts

| Contract | File | Status |
|----------|------|--------|
| HERMES-001 — Known-source monitor | `prompts/known_source_monitor_task.md` | ✅ Active |
| HERMES-002 — May 2026 backfill | `prompts/hermes_may_2026_backfill_task.md` | ✅ Active |
| HERMES-003 — Search discovery | `prompts/hermes_search_discovery_task.md` | ✅ Drafted |
| Tier 1 promotion (Task A) | `prompts/hermes_tier_1_promotion_task.md` | ✅ Executed |
| Tier 2 promotion (Task B) | `prompts/hermes_tier_2_promotion_task.md` | ✅ Executed |
| Promotion review (Task C) | `prompts/hermes_promotion_review_task.md` | ✅ Executed |
| RI classification | `prompts/resident_interest_classification_task.md` | ✅ Active |

### Backlog Status

Current priorities:
- **SW-002** — Run first source-discovery cycle (high)
- **MON-001** — Run SJC School District monitor pilot (high) *[partially done]*
- **MON-005** — BCC calendar weekly monitor pilot (high)
- **MON-007** — Investigate NBOR app URL for road closures (high)
- **TAX-004** — Evaluate budget_millage taxonomy gap (medium, evidence ready)
- **BF-005** — Plan Aug-Sep 2025 backfill (medium)
- **HERMES-003** — Search discovery template (done)

## Open Loops / To-Do

### High Priority

1. **NBOR app URL extraction** — Road closures data is confirmed behind the
   Neighborhood Bill of Rights app. Need a human to open the road closures
   page in a browser, inspect the SJC Road Closures button element, and grab
   the URL. Added as MON-007.

2. **Budget_millage taxonomy promotion** — Evidence ready from backfill (1 item).
   Needs Buddy approval to promote to canonical topic. TAX-004.

3. **BCC calendar weekly monitor pilot** — Agenda PDF pattern needs validation.
   Manually inspect 1-2 agenda PDFs to confirm extraction approach. MON-005.

### Medium Priority

4. **Aug-Sep 2025 backfill** — Next historical window for TRIM/budget season
   and school rezoning. BF-005 planning needed.

5. **Source-watch first discovery cycle** — Run search terms, check source
   health, report findings. SW-002.

6. **Editorial review queue design** — Needed before any publishing pipeline.
   ED-001.

## Completed This Session

- ✓ Deep Research ingestion (sources, beats, search terms)
- ✓ Codex Strong repo advancement (operator docs, checklists, backlog)
- ✓ Tier 1 + Tier 2 source promotions (15 via Hermes)
- ✓ May 2026 backfill (21 items, 4 clusters, 7 gaps)
- ✓ Monitor specs (6 docs)
- ✓ Utility department pilot (5 items, daily-ready)
- ✓ Cadence system (docs/cadence.md, logs/runs/)
- ✓ Taxonomy promotion (water_restrictions)
- ✓ School stack pilot (2 items, filtering validated)
- ✓ HERMES-003 draft (search discovery)
- ✓ Road closures investigation (confirmed NBOR gap)
- ✓ Data inventory and homeowner perspective docs
- ✓ Source-watch agent definition with memory
- ✓ AGENTS.md agent location guidance
- ✓ README_INTERNAL.md (this file)

## Durable Decisions

- Discovery loops > single linear pipeline. Each loop has its own trigger,
  inputs, outputs, and owner.
- Official records are first authority for consequential claims. Local media
  is tip-surfacing/context.
- CDD governance, utilities/water, and transportation/roadwork are first-class
  homeowner operating areas.
- May 2026 is the first backfill baseline. Aug-Sep 2025 is next.
- Hermes delegation model: architect creates bounded task contracts, workers
  perform mechanical work, reviewer validates, architect updates state.
- Cadence system uses LAST_RUN markers. No cron/launchd.
- Taxonomy gaps require real item evidence before promotion.
- Memory stays concise; narrative history belongs in logs.
- Public sources only. No private groups, login-gated portals, or scraping
  that violates terms of service.
- Source candidates must be reviewed and approved before canonical promotion.

## Directory Overview

- `.opencode/agents/` — Interactive OpenCode agent definitions
- `.opencode/agent_memory/` — Persistent agent memory files
- `agents/` — Role definitions (non-interactive)
- `prompts/` — Hermes task contracts and classification prompts
- `docs/` — Architecture, taxonomy, cadence, monitor specs, deep research
- `registry/` — Sources, candidates, beats, search terms, communities
- `schemas/` — Intel item and source schemas
- `data/` — Intel items, backfill artifacts, dedupe index
- `logs/` — Agent logs, session logs, Hermes worker logs, run logs

## Important Files

| File | Purpose |
|------|---------|
| `STATE.md` | Current phase, next task, blockers |
| `BACKLOG.md` | Grouped actionable backlog |
| `docs/cadence.md` | On-demand cadence system |
| `docs/taxonomy.md` | Controlled vocabularies |
| `docs/discovery_loops.md` | Loop operating model |
| `docs/operator_mode.md` | How architect operates |
| `docs/monitor_specs/` | Per-source monitor specifications |
| `registry/sources.yaml` | 24 canonical sources |
| `registry/source_candidates.yaml` | 46 candidates |
| `prompts/known_source_monitor_task.md` | Generic monitor task (HERMES-001) |

## Watchouts & Cautions

- Missed days in the cadence are acceptable. Missed weeks should be avoided.
- Monthly tasks can slip a few days. Prioritize at 40+ days overdue.
- Do NOT promote sources without Buddy approval.
- Do NOT make taxonomy changes without Buddy approval.
- Do NOT run backfill without explicit instruction.
- Do NOT publish anything — no newsletter, social, or web output.
- Do NOT access private Facebook groups, login-gated portals, or members-only content.
- Store minimal personal information. Prefer parcel IDs, permit numbers, document URLs.
- Local media is context, not authority for consequential claims.
- All monitor/backfill execution is supervised — no cron, no launchd, no automation.

## Resume Notes

- Start every session by reading `docs/operator_mode.md` and `docs/cadence.md`.
- Check `logs/runs/{daily,weekly,monthly}/LAST_RUN` for cadence state.
- Read `STATE.md` and `BACKLOG.md` for current phase and priorities.
- Pick the smallest safe unblocked task from due cadence buckets.
- Write meta-run log to `logs/runs/{cadence}/` and update LAST_RUN after work.
- Full narrative history in `logs/sessions/2026-06-03_initial_sjc_intel_buildout.md`.
- 12 architect agent logs in `logs/agents/sjc-intel-architect/`.

## Agent Cautions

- Do not store secrets, tokens, credentials, private URLs, or raw sensitive data.
- Do not read .env or credential files.
- Do not git commit without Git Steward pattern (explicit paths only).
- Do not assign tasks to non-existent Hermes profiles.
- Keep claims source-backed or explicitly labeled proposals.
- Do not treat generated artifacts as canonical — rebuild when needed.
- Architect memory must stay under ~100 lines. Archive to logs when it grows.

## Memory Export

```yaml
memories:
  - id: repo-purpose
    content: "SJC_Intel is an AI-assisted local intelligence/reporting system for St. Johns County, Florida. It discovers, monitors, classifies, and organizes public information about master-planned communities, government, utilities, schools, roads, and development."
  - id: operating-mode
    content: "Supervised operator mode. No cron/launchd. Buddy says 'get to work', agent evaluates cadence via LAST_RUN markers, picks smallest safe task, executes or delegates to Hermes, writes run log."
  - id: canonical-sources
    content: "24 canonical sources in registry/sources.yaml. 15 promoted from Deep Research candidates (10 Tier 1 + 5 Tier 2), 9 pre-existing. 46 candidates remain in source_candidates.yaml."
  - id: backfill-may-2026
    content: "May 2026 backfill complete: 21 items, 4 topic clusters, 7 source gaps, 2 taxonomy gaps. Phase III Extreme Water Shortage was dominant story. School district most productive source (10 items)."
  - id: daily-ready-monitor
    content: "sjc_utility_department is the first daily-ready Hermes monitor. 5 items extracted in pilot. Spec at docs/monitor_specs/sjc_utility_department.md."
  - id: cadence-system
    content: "Daily, weekly, monthly rhythms with LAST_RUN markers at logs/runs/{daily,weekly,monthly}/LAST_RUN. Cadence doc at docs/cadence.md. Missed days OK; missed weeks avoid."
  - id: hermes-delegation
    content: "6 Hermes task contracts exist: monitor, backfill, search discovery, Tier 1 promotion, Tier 2 promotion, promotion review. RI classification prompt also exists."
  - id: taxonomy-water-restrictions
    content: "water_restrictions promoted to canonical topic. Added to docs/taxonomy.md with definition and usage guidance. Evidence from backfill (2 items) + live monitor (1 item). TAX-003 closed."
```
