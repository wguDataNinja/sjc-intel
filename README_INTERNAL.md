# README_INTERNAL

```yaml
agent_context:
  repo:
    name: sjc_intel
    purpose: AI-assisted local intelligence/reporting for St. Johns County, Florida
    status: supervised operator mode
    ecosystem: ivy
    home: /Users/buddy/projects/sjc_intel
    git:
      branch: master
      policy: Commit after meaningful sessions. Stage explicit paths only.
        Conventional commits: feat, fix, docs, chore, data.
        Never commit secrets, .env, raw transcripts.
        Agent never commits without explicit instruction.
  entrypoint: README_INTERNAL.md / AGENTS.md / .opencode/agents/sjc-intel-architect.md
  architect_memory: .opencode/agent_memory/sjc-intel-architect.memory.md
  source_watch_memory: .opencode/agent_memory/sjc-intel-source-watch.memory.md
  cadence_system: docs/cadence.md
  run_logs: logs/runs/{daily,weekly,monthly}/LAST_RUN
  monitor_specs: docs/monitor_specs/
```

## What This Repo Is

> **Start here for current operations:** [CURRENT_BRIEF.md](CURRENT_BRIEF.md)
> is the canonical, generated human status. It identifies mode, health, latest
> run, pending decisions, risks, and the next supervised action.

SJC_Intel discovers, monitors, classifies, and organizes public information
about St. Johns County, Florida — focused on master-planned communities,
government decisions, utilities, schools, roads, and development. It produces
structured intelligence items for editorial review, not published news.

**Product direction:** First public product is SilverLeaf neighborhood
intelligence. Internal collection remains countywide and regional. See
`docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md`.

Operates in **supervised operator mode**: no cron, no launchd, no scheduled
automation. Buddy says "get to work", the agent evaluates cadence via
LAST_RUN markers, picks the smallest safe task, executes or delegates,
and writes a meta-run log.

Official records are the first authority for consequential claims. Local media
is tip-surfacing/context unless verified by official records.

## Public website

The deployable, static **SilverLeaf Brief** is in [site/](site/): it contains a
reviewed four-item release across 13 generated routes and is published through
GitHub Pages at <https://wgudataninja.github.io/sjc-intel/>. Build, preview,
validation, and deployment instructions are in [`site/README.md`](site/README.md).

## Current Architecture

### Sources
| Status | Count | Details |
|--------|-------|---------|
| Canonical | 28 | Registry sources in `registry/sources.yaml`, including official records, school/transport/weather/civic, local media, and aliases |
| Candidates | 46 | Awaiting review/promotion |
| Deferred | 13 | Lower priority |
| Duplicates | 6 | Already covered by canonical |

### Monitors
| Source | Cadence | Status | Spec |
|--------|---------|--------|------|
| `sjc_utility_department` | Daily | ✅ Daily-ready | `docs/monitor_specs/sjc_utility_department.md` |
| `sjc_county_news` | Daily | ✅ Pilot passed | `docs/monitoring_workflow.md` |
| `sjso_news_stories` | Daily | ✅ Pilot passed | `docs/monitoring_workflow.md` |
| `sjc_nbor_public_notices` | Daily | ✅ Extractor ready | `docs/monitor_specs/sjc_nbor_public_notices.md` |
| `sjc_emergency_management` | Daily/seasonal | ⬜ Designed | Backfill lessons |
| `sjc_school_stack` | Weekly | ✅ Pilot run | `docs/monitor_specs/sjc_school_stack.md` |
| `sjc_bcc_calendar` | Weekly | ⬜ Spec ready | `docs/monitor_specs/sjc_bcc_calendar.md` |

### Review Pipeline
| Artifact | Location | Contents |
|----------|----------|----------|
| Intel items | `data/intel_items/{date}/{source}.yaml` | Structured discovery records |
| Source events | `data/source_events/{date}/{source}.yaml` | Fetch/meeting container records |
| Dedupe index | `data/index/prior_items.yaml` | 115 unique fingerprints |
| Review queue | `data/review_queue/queue.yaml` | 132 entries (43 pending, 83 verified) |
| Interest filters | `registry/interest_filters.yaml` | Keyword rules for flagging priority items |
| Tracked entities | `registry/tracked_entities.yaml` | 11 durable things watched over time |

### Agents
| Agent | Type | File | Purpose |
|-------|------|------|---------|
| `sjc-intel-architect` | Interactive | `.opencode/agents/sjc-intel-architect.md` | Top-level operator, delegation planner, state steward |
| `sjc-intel-source-watch` | Interactive | `.opencode/agents/sjc-intel-source-watch.md` | Source discovery, source health, gap tracking |
| `resident-interest-classifier` | Role + prompt | `agents/` + `prompts/` | Adds resident-perspective layer to items |

### Hermes Task Contracts
| Contract | File | Status |
|----------|------|--------|
| HERMES-001 — Known-source monitor | `prompts/known_source_monitor_task.md` | ✅ Active |
| HERMES-002 — May 2026 backfill | `prompts/hermes_may_2026_backfill_task.md` | ✅ Executed |
| HERMES-003 — Search discovery | `prompts/hermes_search_discovery_task.md` | ✅ Drafted |
| Silverleaf search discovery | `prompts/silverleaf_search_discovery_task.md` | ✅ Drafted |
| Tier 1 promotion | `prompts/hermes_tier_1_promotion_task.md` | ✅ Executed |
| Tier 2 promotion | `prompts/hermes_tier_2_promotion_task.md` | ✅ Executed |
| Promotion review | `prompts/hermes_promotion_review_task.md` | ✅ Executed |
| RI classification | `prompts/resident_interest_classification_task.md` | ✅ Active |
| Aug-Sep 2025 backfill | `prompts/hermes_aug_sep_2025_backfill_task.md` | ✅ Executed |

## Current Phase

**Product direction and sourcing strategy established.** See
`docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md` for the full
authority summary, accepted decisions, and roadmap implications.

**Adaptive discovery replay implemented (Task 22).** The file-backed,
historically isolated weekly harness, evaluator, proposal state, and operator
commands are documented in `docs/adaptive_discovery_backtest.md`. It is a
simulation/verification tool only; production remains supervised and does not
auto-promote any registry or review state.

**Supervised live adaptive-discovery pilot (Task 23).** `CURRENT_BRIEF.md`
is the canonical generated operational brief (mode, health, findings,
coverage, pending decisions, next run). Bounded live discovery runs with
per-query receipts and budgets through a provider-neutral adapter; every
proposal is reviewed by a human via `review_adaptive_proposal.py`. Live
governance authority is versioned under `data/adaptive_discovery/`; volatile
run artifacts remain under `runtime/adaptive_discovery/`. See
`docs/live_adaptive_operations.md`.

**Research escalation + proposal resolution (Task 25).** Ambiguous proposals
(identity uncertainty, geographic conflict, stale evidence, conflicting
sources, or material resident importance) trigger bounded follow-up research
via `scripts/research_adaptive_proposal.py` before human review; the result is
a research-resolution record with a recommended action. Proposals can be
edited (canonical name, aliases, location, queries, timeline language) with a
preserved original and history, then accepted as the corrected record.
Current accepted adaptive subjects and active recurring searches are listed in
`CURRENT_BRIEF.md`.

**v1 finish pass (Task 26).** The first supervised weekly adaptive cycle ran
against all accepted profiles with receipts, bounded research escalation,
independent evaluation, and the Resident Coverage Editor. It generated no new
pending proposals after canonical-alias reconciliation; the editor identified
utilities, preparedness, and government-decision coverage as next profile
gaps. See `CURRENT_BRIEF.md` and `reports/26-codex-v1-finish-and-publish.md`.

Strategic priorities (not implementation orders):

1. **SilverLeaf geographic registry** — foundational dependency for all
   public-facing work. Boundary, neighborhoods, streets, schools, roads,
   aliases, and exclusion rules.
2. **Three-lane architecture** — durable knowledge (existing pipeline),
   live incident (new), agentic investigation (new).
3. **Geographic and coordinate-based filtering** — point-in-polygon,
   corridor proximity, PostGIS readiness.
4. **Live incident sourcing** — FHP, FL511, county notices, emergency
   management (source feasibility investigation open).
5. **Agentic sourcing framework** — targeted news/social searches,
   evidence extraction, reconciliation, proposed updates.
6. **School sourcing expansion** — athletics, activities, recognition,
   community achievements beyond BoardDocs.

PostgreSQL foundation work (file authority preserved):

- general application-facing PostgreSQL adapter (`scripts/pg_adapter.py`);
- backend selection and file fallback (`scripts/storage_adapter.py`);
- retention/pipeline metadata migrations (`20260706_010...`);
- compact metric snapshot migration and generator (`20260706_011...`,
  `scripts/metrics_snapshot.py`);
- non-destructive retention dry-run tooling (`scripts/retention.py`);
- portability check (`scripts/portability_check.py`);
- future news-ingestion boundaries (`docs/news_ingestion_readiness.md`).

## Core Docs

| File | Why |
|------|-----|
| `README_INTERNAL.md` | This file — primary dev entrypoint |
| `AGENTS.md` | Agent roles, git policy, logging rules |
| `BACKLOG.md` | All actionable tasks with status |
| `docs/cadence.md` | Daily/weekly/monthly rhythms with LAST_RUN markers |
| `docs/live_adaptive_operations.md` | Supervised live discovery, research escalation, receipts, budgets, proposal review, health |
| `docs/hermes_weekly_entrypoint.md` | Hermes weekly-run entry point, scope boundary, and handoff |
| `docs/human_review.md` | Human decisions across adaptive proposals, bundles, and publication |
| `site/README.md` | Static SilverLeaf Brief build, validation, preview, and deployment guide |
| `docs/taxonomy.md` | Controlled vocabularies, beats, source families |
| `docs/discovery_loops.md` | How the six discovery loops work |
| `docs/operator_mode.md` | Session startup routine and task selection |
| `docs/postgresql_adapter.md` | PostgreSQL adapter and backend-selection contract |
| `docs/retention.md` | Source-by-source retention and pruning dry-run behavior |
| `docs/snapshots_and_metrics.md` | Compact metric snapshot behavior |
| `docs/news_ingestion_readiness.md` | Later relevant-news extension boundaries |
| `docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md` | Product direction and sourcing strategy |
| `docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md` | Prompt-led discovery standards and architecture |

## Open Loops

1. **BCC June 2026 agenda links broken** — Two regular meetings (Jun 2, Jun 16)
   not extractable. Need Clerk's office verification. (GAP-001)
2. **No Hermes runtime** for automated daily monitoring. (ongoing)
3. **No `scripts/extract_utility.py`** — utility monitoring is manual.
4. **Tracked entity → intel_item linkage wired** — ENT-002 complete. Queue builder matches entity labels/aliases. No Hermes entity-search prompt yet (ENT-002 scope reduced).
5. **School district has no June coverage** — BoardDocs pilot pending.
6. **Tier 3 (CDD) and Tier 4 (community) sources** not promoted.
7. **Monthly closeout** — last monthly run was 2026-06-08 (26+ days ago).
8. **SilverLeaf geographic registry** — foundational but not started. Needs
   boundary, neighborhoods, streets, schools, roads, and aliases.
   (see `docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md`)
9. **Live incident lane** — FHP source adapter and normalized incident schema
   not started. (see planning doc)
10. **Agentic investigation framework** — search infrastructure, LLM
    integration, and review gates not designed. (see planning doc)

## Durable Decisions

- Discovery loops > single linear pipeline.
- Official records are first authority for consequential claims.
- CDD governance, utilities/water, and transportation/roadwork are first-class
  homeowner operating areas.
- May 2026 is the first backfill baseline. Aug-Sep 2025 is the next target.
- Cadence system uses LAST_RUN markers. No cron/launchd.
- Memory stays concise; narrative history belongs in logs.
- Public sources only. No private groups or login-gated portals.
- Source candidates reviewed before canonical promotion.
- **First public product: SilverLeaf neighborhood intelligence.** (per
  `docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md`)
- **Three-lane architecture:** durable knowledge, live incident, agentic
  investigation.
- **Deterministic official capture first** — agentic search enriches but
  does not replace.
- **Geographic registry is foundational** — SilverLeaf boundary and
  coordinate-based filtering before public launch.
- **Social media is corroboration only** — not sole primary detection.

## Safe Commands

```bash
python3 scripts/rebuild_dedupe_index.py        # Idempotent dedupe rebuild
python3 scripts/build_review_queue.py           # Rebuild review queue
python3 scripts/extract_nbor.py                 # Fetch and parse NBOR page
python3 scripts/extract_bcc_agenda.py           # Fetch BCC agenda items
python3 scripts/batch_review.py                 # Batch review operations
python3 scripts/retention.py --json             # Non-destructive retention policy dry run
python3 scripts/metrics_snapshot.py --backend file --json
python3 scripts/portability_check.py            # Non-mutating migration/env portability checks
```

## Agent Cautions

- Do NOT promote sources or change taxonomy without Buddy approval.
- Do NOT run backfill without explicit instruction.
- Do NOT publish anything — no newsletter, social, or web output.
- Do NOT access private Facebook groups or login-gated content.
- Do NOT store secrets, tokens, credentials, or raw sensitive data.
- Do NOT commit without Git Steward pattern (explicit paths only).
- Do NOT assign tasks to non-existent Hermes profiles.
- Keep claims source-backed or explicitly labeled proposals.

## Logging Tiers

| Tier | Content | Location | Exists? |
|------|---------|----------|---------|
| Agent logs | What agents did, decisions, friction | `logs/agents/{name}/{date}_{task}.md` | ✅ |
| Run logs | Pipeline runs, extractions, cadence work | `logs/runs/{daily,weekly,monthly}/{date}_{task}.md` | ✅ |
| Conversation logs | Buddy's GPT outputs, research threads (curated) | `logs/conversations/{YYYY-MM-DD}_{topic}.md` | ❌ New |

Full narrative session history: `logs/sessions/2026-06-03_initial_sjc_intel_buildout.md`

## Memory Export

```yaml
memories:
  - id: repo-purpose
    content: "SJC_Intel discovers, monitors, classifies, and organizes public information about St. Johns County, Florida — focused on master-planned communities, government, utilities, schools, roads, and development."
  - id: operating-mode
    content: "Supervised operator mode. No cron/launchd. Buddy says 'get to work', agent evaluates cadence via LAST_RUN markers, picks smallest safe task, executes or delegates, writes run log."
  - id: review-pipeline
    content: "132 items in review queue (43 pending). 115 unique dedupe entries. Interest filters at registry/interest_filters.yaml. Source events at data/source_events/."
  - id: open-loops
    content: "BCC June agenda links broken. No Hermes runtime. No tracked_entities.yaml (ENT backlog). No school data since May. Monthly closeout overdue."
```
