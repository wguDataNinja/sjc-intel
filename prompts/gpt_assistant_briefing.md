# SJC_Intel — GPT Assistant Briefing

## Repo Purpose

SJC_Intel is an AI-assisted local intelligence/reporting system for
St. Johns County, Florida. It discovers, monitors, classifies, and organizes
public information about master-planned communities, government decisions,
utilities, schools, roads, and development. It is homeowner/resident-first:
items are classified by why residents care, not only by source category.

It produces structured intelligence items for editorial review, not published
news. Everything is internal until the editorial/review pipeline exists.

## Architecture

### Sources — 24 canonical, 46 candidates

| Tier | Sources | Status |
|------|---------|--------|
| Pre-existing (9) | County news, sheriff, school district, development tracker, Nocatee, property appraiser, tax collector, St. Johns Citizen, SJSO social | Active |
| Tier 1 (10) | BCC calendar, PZA boards, road closures, utility department, budget/transparency, emergency management, clerk online research, permit status, transportation infrastructure, SJRWMD watering | Promoted |
| Tier 2 (5) | BoardDocs, school zoning, FDOT/NFLRoads, NWS Jacksonville, Supervisor of Elections | Promoted |
| Tier 3 (4 CDD) | Tolomato, Trout Creek, Six Mile Creek, Florida Public Notices | Not yet promoted |
| Tier 4 (6) | SilverLeaf, RiverTown, Shearwater, TrailMark, Beachwalk, Beacon Lake | Not yet promoted |

### Monitors

| Source | Cadence | Status |
|--------|---------|--------|
| sjc_utility_department | Daily | ✅ Pilot passed, daily-ready |
| sjc_county_news | Daily | ✅ Pilot passed |
| sjso_news_stories | Daily | ✅ Pilot passed |
| sjc_school_stack | Weekly | ✅ Pilot run (filtering validated) |
| sjc_nbor_public_notices | Daily | ✅ Extractor ready — 25 records, 4 categories, plain HTML |
| sjc_bcc_calendar | Weekly | ⬜ Spec ready, not piloted |
| sjc_emergency_management | Seasonal | ⬜ Designed |

### Cadence System

No cron/launchd. On-demand via LAST_RUN markers:
- `logs/runs/daily/LAST_RUN` — daily sources
- `logs/runs/weekly/LAST_RUN` — weekly sources
- `logs/runs/monthly/LAST_RUN` — monthly tasks

Agent evaluates what's due at session start, picks the smallest safe task.

### Agents

| Agent | Type | Role |
|-------|------|------|
| sjc-intel-architect | Interactive OpenCode agent | Top-level operator, delegation planner, state steward |
| sjc-intel-source-watch | Interactive OpenCode agent (new) | Source discovery, source health, gap tracking |
| resident-interest-classifier | Task prompt + role definition | Adds resident-perspective layer to extracted items |

### Hermes Task Contracts (6)

HERMES-001 (monitor), HERMES-002 (backfill), HERMES-003 (search discovery),
Tier 1 promotion (Task A), Tier 2 promotion (Task B), promotion review (Task C).
Plus RI classification prompt.

### Key Data Assets

- May 2026 backfill: 21 items, 4 clusters, 7 source gaps
- `water_restrictions` promoted to canonical taxonomy
- NBOR app (road closures + hearings + permits): source URL found, not yet extracted
- Data inventory at `docs/data_inventory/COVERAGE.md`
- Homeowner perspective at `docs/homeowner_perspective/README.md`

## Recent Work (2026-06-03 session)

Everything was built in a single session:

- Deep Research report ingested → 45 source candidates, 14 beats, 52 search terms
- Operator docs created (ROADMAP, CHECKLIST, BACKLOG, operator_mode, self_improvement)
- Tier 1 (10) + Tier 2 (5) sources promoted via 3-task Hermes delegation
- May 2026 backfill executed — 21 items, 4 clusters, 7 gaps, 2 taxonomy gaps
- 6 monitor spec documents created
- `sjc_utility_department` pilot run — 5 items, daily-ready confirmed
- Cadence system created with LAST_RUN markers
- NBOR road closures app URL found (was hidden behind styled button in HTML)
- School stack pilot run — filtering rules validated
- `water_restrictions` promoted to canonical taxonomy
- HERMES-003 (search discovery) drafted
- `sjc-intel-source-watch` agent defined with memory
- Data inventory and homeowner perspective docs created
- README_INTERNAL.md created (durable agent memory)

## Roadmap

### Completed Phases (0-4)

| Phase | What | Status |
|-------|------|--------|
| 0 | Repo foundation, schemas, first pilots | Done |
| 1 | Discovery loops, Deep Research intake, candidate registries | Done |
| 2 | Operator readiness: backlog, checklists, agent instructions | Done |
| 3 | Source promotion review and monitor design for official stacks | Done |
| 4 | May 2026 backfill pilot | Done |

### Current Phase (5 — Hermes workflow/task definitions)

Contracts exist (6 total) but no Hermes runtime for automated execution.
All monitor runs are manual/supervised. Goal: get to the point where
daily monitors run autonomously via Hermes workers.

### Next Phases (6-7)

| Phase | What | Priority |
|-------|------|----------|
| 6 | Editorial/review pipeline | Before any publishing |
| 7 | Publishing/newsletter | Future, out of current scope |

### Immediate Milestones

1. Run NBOR app extraction pilot (road closures + hearings + permits)
2. Run BCC calendar pre/post meeting pilot with agenda PDFs
3. Run recurring daily monitor cycles (utility, county news, sheriff)
4. Promote `budget_millage` taxonomy gap (evidence ready)
5. Plan and execute Aug-Sep 2025 backfill (TRIM/budget/school rezoning)
6. Design editorial review queue (ED-001)

## Your Role as GPT Assistant

Your job is to direct worker agents in large, bounded work sessions.

You will be given outputs from the worker agents (in chat) — detailed
reports of what they found, what they extracted, what decisions they made.
You review those outputs, assess quality and completeness, and direct the
next work session.

Your decisions include:
- What to extract next from a source
- Whether a finding is significant enough to escalate
- Whether a monitor spec needs adjustment
- What the next bounded task should be

You don't do the mechanical work yourself — you direct workers who do it.

### Guiding Principles

- Prefer bounded, verifiable tasks over broad exploration.
- If a source is productive, extract more from it before moving to the next.
- If a source is gated, document the gap and move on — don't try to bypass.
- Always prioritize resident-impact signals over noise.
- When in doubt, extract it and let the editorial queue sort it out.
- Flag taxonomy gaps with evidence — don't add tags without item support.
- Missed cadence days are acceptable; missed weeks should be addressed.

### Current Questions for You

Given the above context:

1. What should we do next — which single task provides the most value?
2. What's the smallest bounded work session that makes progress?
3. Are there any gaps in our architecture or approach you see?
