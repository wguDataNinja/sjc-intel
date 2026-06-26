# Session Log — Initial SJC_Intel Buildout

**Date:** 2026-06-03
**Project:** SJC_Intel
**Session type:** Initial concept, architecture, agent setup, source discovery, pilot testing
**Primary participants:** Buddy, ChatGPT, OpenCode sjc-intel-architect, Hermes workers

---

## Summary

This session established the foundation for SJC_Intel, an AI-assisted local intelligence/reporting system for St. Johns County, Florida. The project began from the idea of monitoring and reporting on master-planned communities such as SilverLeaf, Nocatee, RiverTown, Shearwater, TrailMark, Beacon Lake, Beachwalk, eTown, Seven Pines, EverRange, and nearby corridors.

The core thesis evolved from "local social media/news accounts" into a structured homeowner/resident intelligence system: public sources, social signals, government records, community pages, local media, and resident tips can be discovered, classified, verified, and routed into useful community updates.

By the end of the session, the repo had working schemas, registries, source candidates, agent definitions, pilot data, discovery-loop documentation, Deep Research intake structure, and a validated Hermes workflow for public web discovery and extraction.

---

## Product Direction Established

The project was framed around a public-facing opportunity: existing neighborhood Facebook groups serve individual neighborhoods, but there is limited organized reporting across the broader St. Johns County master-planned community landscape.

The intended public model is:
- social media for discovery
- website/newsletter as the owned hub
- community-specific and topic-specific segmentation
- homeowner-centered relevance
- transparent sourcing
- human review before publication

The project name SJC_Intel was accepted as an internal system/repo name. Public-facing names may differ later.

---

## Key Strategic Concepts

### Homeowner/Resident View

The system should root analysis in the homeowner/resident perspective. Items should be classified by why residents care, not only by source category.

Examples of resident-interest beats:
- construction
- roadwork and traffic
- school capacity and zoning
- development
- public safety
- new retail and restaurants
- utilities and water restrictions
- CDD/HOA governance
- taxes and assessments
- parks and amenities
- quality of life
- property values

### Cross-Source Beats

A key insight was that resident interests cut across sources. "Construction" may include houses, roads, schools, utilities, commercial development, parks, and medical facilities. Therefore topics must not be tied to one source type.

This led to the need for:
- primary_topic
- topics
- interest_tags
- optional facets
- resident_relevance
- taxonomy_gap

### Discovery Loops

The project was reframed from a fixed pipeline into multiple discovery loops:
1. Known-source monitoring loop
2. Search discovery loop
3. Historical backfill loop
4. Cross-section / beat clustering loop
5. Taxonomy improvement loop
6. Review / editorial loop

This reframing allows the system to discover new sources, new beats, and missing categories over time.

---

## Agent System Established

### OpenCode Agent

A project-local OpenCode agent was created:
- **sjc-intel-architect**

Role:
- main repo operator
- architecture and schema steward
- source registry maintainer
- workflow designer
- memory maintainer
- Hermes delegation planner
- editorial/safety guardrail keeper

The agent has a persistent memory file: `.opencode/agent_memory/sjc-intel-architect.memory.md`

### Resident-Interest Classifier

A repo-level specialist role was created:
- `agents/resident-interest-classifier.md`
- `prompts/resident_interest_classification_task.md`
- `docs/resident_interest_classification.md`

Role: read extracted intel items from a resident perspective, classify why people care, assign interest tags, identify affected audiences, flag taxonomy gaps, separate source-supported facts from reasonable inference, flag human review requirements.

### Hermes

Hermes was validated as the automated task/control-plane layer.

A feasibility test confirmed Hermes workers can:
- access public web sources
- extract structured data
- write files into the repo
- update artifacts
- complete through Hermes protocol

---

## Hermes Feasibility Test

A Hermes worker ran a public-source discovery test for SJC_Intel.

Validated targets included:
- St. Johns County main site
- St. Johns County Development Tracker
- St. Johns County Sheriff's Office
- St. Johns County School District
- Nocatee

Result: Hermes was deemed sufficient for the minimum public-source discovery and extraction workflow. Browser-backed access worked where simple HTTP/curl was limited. No private sources, logins, or non-public content were accessed.

Artifact: `discovery_test.md`

---

## Initial Repo Foundation Created

Core project files were created or updated:
- `README.md`
- `STATE.md`
- `docs/repo_audit.md`
- `docs/discovery_loops.md`
- `docs/monitoring_workflow.md`
- `docs/source_registry.md`
- `docs/taxonomy.md`
- `docs/resident_interest_classification.md`
- `docs/deep_research_ingestion.md`
- `schemas/source.schema.yaml`
- `schemas/intel_item.schema.yaml`
- `registry/sources.yaml`
- `registry/communities.yaml`
- `registry/source_candidates.yaml`
- `registry/beat_candidates.yaml`
- `registry/search_terms.yaml`

---

## Source Registry Work

A canonical source registry was created at `registry/sources.yaml`.

Initial monitored or verified sources included:
- sjc_county_news
- sjso_news_stories
- sjso_social_media
- sjc_school_district
- sjc_development_tracker
- nocatee_community
- sjc_property_appraiser
- sjc_tax_collector

Later in the session, St. Johns Citizen was promoted into the canonical registry after source review.

---

## Pilot Runs

### SJC County News Pilot

A Hermes-style monitor pilot was run against `sjc_county_news`.

Output: `data/intel_items/2026-06-03/sjc_county_news.yaml`, `data/intel_items/2026-06-03/sjc_county_news_report.md`, `data/index/prior_items.yaml`

Result: 5 county news items extracted. Source suitable for daily monitoring. Pilot revealed schema issues, later reconciled.

### SJSO News Stories Pilot

The sheriff/public-safety pilot ran before the resident-interest layer was fully created, then was reconciled afterward.

Output: `data/intel_items/2026-06-03/sjso_news_stories.yaml`, `data/intel_items/2026-06-03/sjso_news_stories_report.md`

Result: 4 sheriff items extracted. Resident-interest fields were backfilled. Public-safety sensitivity defaults were validated. Human review became mandatory for crime, arrest, victim, minor, emergency, or unresolved allegation items.

---

## Schema Evolution

The intel item schema evolved to v2.0.

Important fields added or clarified:
- primary_topic
- topics
- interest_tags
- resident_relevance
- resident_relevance.summary
- resident_relevance.affected_audiences
- resident_relevance.why_it_matters
- resident_relevance.confidence
- resident_relevance.inference_notes
- taxonomy_gap
- human_review_required
- recommended_channels
- review_status

Canonical review_status became: `pending_review`

Important recommended channels added: `website_review_queue`, `weekly_brief_candidate`

---

## Taxonomy and Communities

A controlled taxonomy was created at `docs/taxonomy.md`.

A community registry was created at `registry/communities.yaml`.

Initial communities/corridors included:
- countywide, st_johns_county
- silverleaf, nocatee, rivertown, shearwater, trailmark, beacon_lake, beachwalk, etown, seven_pines, everrange, wildlight
- cr_210_corridor, sr_16_corridor, us_1_corridor
- ponte_vedra, st_augustine

---

## Deep Research Intake

The project prepared for ChatGPT Deep Research output.

Created:
- `docs/deep_research/README.md`
- `docs/deep_research_ingestion.md`
- `registry/source_candidates.yaml`
- `registry/beat_candidates.yaml`
- `registry/search_terms.yaml`

Policy: Deep Research output is candidate material. It does not directly modify canonical registries. Candidate sources and beats require review. Canonical promotion requires approval.

Deep Research is expected to help discover: government sources, local media, school sources, transportation sources, CDD/HOA-style public sources, homeowner-relevant beats, search terms, blind spots.

---

## St. Johns Citizen Discovery

Buddy discovered St. Johns Citizen by searching Facebook: https://sjcitizen.com/ | https://www.facebook.com/stjohnscitizen

This led to a major pipeline insight: if Buddy found St. Johns Citizen by accident, SJC_Intel needs an intentional loop for discovering similar local reporting and social-news organizations.

Artifacts created: `docs/source_discoveries/st_johns_citizen.md`, `docs/source_reviews/st_johns_citizen_review.md`

St. Johns Citizen was assessed as: legitimate local media, professional reporting organization, multiple named contributors, daily publishing cadence, newsletter and advertising infrastructure, strong mission overlap with SJC_Intel, useful comparable model, high-value source candidate.

After review, Buddy approved canonical promotion. Canonical source ID: `st_johns_citizen`

---

## Local Media Discovery Loop

The St. Johns Citizen discovery led to a new local-media discovery sub-loop. Search terms were added to `registry/search_terms.yaml`.

The loop should search for: local media websites, Facebook pages, Instagram accounts, newsletters, Substacks, community news projects, journalist-led local outlets, St. Johns County reporting organizations.

Quality signals for local media candidates were added, including: original reporting, multiple contributors, regular cadence, public website hub, social distribution, newsletter/owned audience capture, advertising/sponsorship infrastructure, clear geographic focus, homeowner-relevant beats.

---

## Repo Audit

A repo-wide audit was performed. Created: `docs/repo_audit.md`, `STATE.md`.

Audit conclusion: Foundation is strong. Repo is partially ready for operator mode. Memory is too long and needs trimming. Hermes automation is proven but not deployed. No self-improvement framework exists yet. README is stale relative to recent progress. County pilot remains v1.1 while sheriff pilot is v2.0.

Top gaps identified:
1. No deployed Hermes tasks
2. No self-improvement framework
3. Memory file too long
4. README stale
5. v1.1/v2.0 pilot compatibility gap

---

## Current Tracks

By the end of the session, the repo had multiple possible next tracks:
1. sjc_school_district monitor pilot
2. January 2026 historical backfill experiment
3. Deep Research ingestion
4. St. Johns Citizen/local media discovery expansion
5. Source/beat/search-term candidate review
6. Future Codex Strong organization pass

---

## Strategic Plan Going Forward

The working plan became:
1. Ingest Deep Research when available.
2. Use Deep Research to seed candidates, beats, and search terms.
3. Perform initial hunting and 2026 month-by-month historical backfill.
4. Build real artifacts from multiple months.
5. After enough evidence exists, run Codex Strong for organization and streamlining.

Codex Strong should not be used too early. It should optimize based on observed data, not abstract theory.

Readiness criteria for Codex Strong:
- Deep Research ingested
- at least 2–3 monthly backfills complete
- source candidates reviewed
- beat candidates reviewed
- taxonomy gaps collected
- known-source pilots documented
- memory/backlog issues visible

---

## Important Decisions

- SJC_Intel is the internal repo/system name. Public brand may differ later.
- The project is homeowner/resident-centered.
- Social media is discovery; website/newsletter is the owned hub.
- Private groups are not scrapeable sources.
- Resident chatter is a lead, not verified fact.
- Sensitive items require human review.
- Deep Research output is candidate material, not canonical.
- St. Johns Citizen is a canonical source and comparable model.
- Agents should be organized around discovery loops, not a rigid hierarchy.
- Session logs should preserve narrative history outside agent memory.

---

## Recommended Next Actions

1. Create a formal repo session logging structure.
2. Trim and restructure sjc-intel-architect memory.
3. Update README to reflect current state.
4. Ingest Deep Research when available.
5. Run January 2026 historical backfill.
6. Run sjc_school_district monitor pilot when ready.
7. Define agent self-improvement framework.
8. Later, run Codex Strong after real historical artifacts accumulate.

---

## Files and Artifacts Mentioned

**Core:** README.md, STATE.md, docs/repo_audit.md, docs/discovery_loops.md, docs/monitoring_workflow.md, docs/taxonomy.md, docs/source_registry.md, schemas/source.schema.yaml, schemas/intel_item.schema.yaml, registry/sources.yaml, registry/communities.yaml, registry/source_candidates.yaml, registry/beat_candidates.yaml, registry/search_terms.yaml

**Agents:** .opencode/agents/sjc-intel-architect.md, .opencode/agent_memory/sjc-intel-architect.memory.md, agents/resident-interest-classifier.md, prompts/resident_interest_classification_task.md, docs/resident_interest_classification.md

**Pilot data:** data/intel_items/2026-06-03/sjc_county_news.yaml, data/intel_items/2026-06-03/sjc_county_news_report.md, data/intel_items/2026-06-03/sjso_news_stories.yaml, data/intel_items/2026-06-03/sjso_news_stories_report.md, data/index/prior_items.yaml

**Deep Research:** docs/deep_research/README.md, docs/deep_research_ingestion.md

**St. Johns Citizen:** docs/source_discoveries/st_johns_citizen.md, docs/source_reviews/st_johns_citizen_review.md

---

## Closing State

SJC_Intel has moved from concept to structured repo foundation. The repo now has: validated public-web agent workflow, canonical source registry, source candidate intake, beat candidate intake, search-term registry, community registry, taxonomy, resident-interest classification, discovery loops, pilot outputs, St. Johns Citizen as a canonical local-media source, Deep Research intake structure.

The next durable improvement is to formalize session/agent logging and then continue discovery/backfill work.

---

## Final Closeout — Supervised Operator Mode Established

Late-session work after the initial buildout transformed the repo from
foundation to operating system.

### Deep Research Ingestion and Extraction

The Deep Research homeowner public-source monitoring map report was archived,
extracted, and converted into:

- `registry/source_candidates.yaml` — 45 sources extracted from the report,
  plus preserved St. Johns Citizen candidate
- `registry/beat_candidates.yaml` — 14 homeowner beats extracted, top five
  marked for first focus
- `registry/search_terms.yaml` — 52 operational terms across 6 categories
- `docs/deep_research/` — Three extraction review artifacts

Deep Research conclusion: official records are first authority for consequential
claims. Local media is tip-surfacing/context. CDD governance, utilities/water,
and transportation/roadwork are first-class homeowner operating areas.

### Codex Strong Repo Advancement

A repo-wide advancement pass converted the Deep Research findings into
operating docs:

- `ROADMAP.md` — Phase roadmap with readiness criteria
- `CHECKLIST.md` — Operating gates for start/end of session, before Hermes
  delegation, before canonical promotion, before taxonomy change, before
  publishing
- `BACKLOG.md` — Grouped actionable backlog by operating area
- `docs/operator_mode.md` — How architect operates when told to work
- `docs/self_improvement.md` — How agents improve workflows safely
- `AGENTS.md` — Agent roles and operating rules
- Agent memory trimmed to concise operational state
- Architect prompt updated with operator-mode behavior

The repo moved from intake prep to operating baseline.

### Tier 1 + Tier 2 Canonical Source Promotions (Hermes Delegated)

Buddy approved Tier 1 and Tier 2 from the promotion packet. A three-task
Hermes delegation model was used:

1. **Task A** (hermes-source-promoter): Promoted 10 Tier 1 sources into
   `registry/sources.yaml`
2. **Task B** (hermes-source-promoter): Promoted 5 Tier 2 sources into
   `registry/sources.yaml` (merge-safe with Tier 1)
3. **Task C** (hermes-promotion-reviewer): Validated all 15 promotions,
   checked scope compliance, verified YAML, wrote review artifact

Results:
- 15 sources promoted (10 Tier 1 + 5 Tier 2)
- Total canonical sources: 24
- No scope violations — Tier 3/4/media not promoted
- YAML validated
- All 10 review checks passed
- Tier 3 (CDD governance) and Tier 4 (community/developer) remain in
  candidate registry

Hermes delegation pattern proven:
- Architect creates bounded task contracts
- Hermes workers perform mechanical edits
- Hermes reviewer validates
- Architect updates state/backlog/memory

### May 2026 Historical Backfill

Hermes task contract `prompts/hermes_may_2026_backfill_task.md` was created,
then executed across three bounded phases:

- **Task A:** Official-source discovery and extraction — 21 items found
- **Task B:** Topic clustering and resident-interest normalization — 4 clusters
- **Task C:** Review, validation, gaps, wrap, backfill report — all 6 pass
  criteria met

Results:
- 21 items extracted across 5 source families
- 4 topic clusters (Phase III water, SJCSD programs, SJCSD awards, public safety)
- 7 source gaps identified (BCC, PZA, roads, FDOT, SR 207, community/CDD, media)
- 2 taxonomy gaps with real evidence: `water_restrictions`, `budget_millage`
- YAML validated
- No private-source contamination
- 5 output files produced

### Backfill-Informed Monitor Specifications

Based on backfill evidence, 6 monitor spec documents created:

- `docs/monitor_specs/README.md` — Prioritization and reference
- `docs/monitor_specs/sjc_utility_department.md` — Daily, Hermes-ready
- `docs/monitor_specs/sjc_school_stack.md` — Weekly, with signal/noise filtering
- `docs/monitor_specs/sjc_bcc_calendar.md` — Pre/post meeting, PDF investigation
- `docs/monitor_specs/sjc_road_closures.md` — Investigation-first (app data source)
- `docs/monitor_specs/backfill_lessons_may_2026.md` — Cross-cutting lessons

### `sjc_utility_department` Monitor Pilot

First backfill-informed live monitor run:
- 5 items extracted (Phase III water, chlorine burnout, SR 207 WRF, utilities
  lab, lead service line inventory)
- YAML validated
- Prior index updated
- 0 duplicates, 0 human-review items
- **First daily-ready source** — Hermes-ready confirmed
- Spec updated with sidebar extraction scope and pilot lessons

### On-Demand Cadence System

Created operating rhythms without cron/launchd automation:

- `docs/cadence.md` — Daily, weekly, monthly cadences with catch-up rules,
  Hermes/delegation guidance, LAST_RUN marker system
- `logs/runs/README.md` — Meta-run log format
- `logs/runs/{daily,weekly,monthly}/LAST_RUN` — Initialized timestamps
- `docs/operator_mode.md` — Updated startup to evaluate cadence
- `CHECKLIST.md` — Updated start/end session checklists

### Summary of Hermes Task Contracts Created

| Contract | File | Purpose |
|----------|------|---------|
| HERMES-001 | `prompts/known_source_monitor_task.md` | Generic known-source monitor |
| HERMES-002 | `prompts/hermes_may_2026_backfill_task.md` | May 2026 historical backfill |
| Task A | `prompts/hermes_tier_1_promotion_task.md` | Tier 1 source promotion |
| Task B | `prompts/hermes_tier_2_promotion_task.md` | Tier 2 source promotion |
| Task C | `prompts/hermes_promotion_review_task.md` | Promotion validation |

Still remaining: HERMES-003 (search discovery template).

---

## Current Closeout State

### Phase

**Supervised operator mode established.** Repo has moved from foundation to
operating baseline. Cadence system ready for daily/weekly/monthly rhythms.

### What Works

- HERMES delegation model: task contracts → bounded execution → review →
  state update
- May 2026 backfill: 21 items, 4 clusters, 7 source gaps, 2 taxonomy gaps
- `sjc_utility_department`: first daily-ready source with validated monitor
- `sjc_county_news` and `sjso_news_stories`: validated monitor pilots
- Tier 1 + Tier 2 source promotions: 24 canonical sources
- Cadence system: LAST_RUN markers for on-demand operation

### What Remains Supervised

- No launchd/cron/scheduled automation exists
- No publishing or newsletter workflow
- No editorial review queue (ED-001)
- Private sources remain out of scope
- Tier 3 (CDD) and Tier 4 (community/developer) not promoted
- Property Appraiser URL conflict unresolved (SRC-002)
- Hermes runtime does not exist for fully automated monitoring
- All monitor execution requires active session

### Best Next Tasks

Priority order for the next "get to work" session:

1. **Run daily cadence task** — `sjc_utility_department` or `sjc_county_news`
   from daily bucket
2. **Run `sjc_school_stack` monitor pilot** — weekly bucket, spec ready
3. **Investigate `sjc_road_closures` app** — determine if data source is
   accessible
4. **Evaluate/promote `water_restrictions` taxonomy gap** — evidence ready
   from backfill + live monitor (TAX-003)
5. **Draft HERMES-003** — search discovery task template (last remaining
   Hermes contract)

---

## Key Files

### Source-of-Truth Docs

| File | Purpose |
|------|---------|
| `STATE.md` | Current phase, next task, blockers |
| `ROADMAP.md` | Phase plan and readiness criteria |
| `CHECKLIST.md` | Operating gates |
| `BACKLOG.md` | Grouped actionable backlog |
| `docs/operator_mode.md` | How architect operates |
| `docs/cadence.md` | On-demand cadence system |
| `docs/self_improvement.md` | Agent improvement framework |
| `docs/discovery_loops.md` | Loop operating model |
| `docs/taxonomy.md` | Controlled vocabularies |

### Registries

| File | Contents |
|------|----------|
| `registry/sources.yaml` | 24 canonical sources |
| `registry/source_candidates.yaml` | 46 candidate records |
| `registry/beat_candidates.yaml` | 14 homeowner beats |
| `registry/search_terms.yaml` | 52 operational terms |
| `registry/communities.yaml` | Registered communities |

### Monitor Specs

| File | Source | Cadence |
|------|--------|---------|
| `docs/monitor_specs/sjc_utility_department.md` | `sjc_utility_department` | Daily |
| `docs/monitor_specs/sjc_school_stack.md` | School district + BoardDocs | Weekly |
| `docs/monitor_specs/sjc_bcc_calendar.md` | BCC calendar | Weekly (pre/post) |
| `docs/monitor_specs/sjc_road_closures.md` | Road closures | Daily (pending) |

### Prompts / Task Contracts

| File | Purpose |
|------|---------|
| `prompts/known_source_monitor_task.md` | Known-source monitor (HERMES-001) |
| `prompts/hermes_may_2026_backfill_task.md` | May 2026 backfill (HERMES-002) |
| `prompts/hermes_tier_1_promotion_task.md` | Tier 1 promotion (Task A) |
| `prompts/hermes_tier_2_promotion_task.md` | Tier 2 promotion (Task B) |
| `prompts/hermes_promotion_review_task.md` | Promotion validation (Task C) |
| `prompts/resident_interest_classification_task.md` | RI classifier |

### Backfill Data

| File | Contents |
|------|----------|
| `data/monthly/2026-05/discovered_items.yaml` | 21 items |
| `data/monthly/2026-05/topic_clusters.yaml` | 4 clusters |
| `data/monthly/2026-05/source_gaps.md` | 7 source gaps |
| `data/monthly/2026-05/monthly_wrap.md` | Monthly narrative |
| `data/monthly/2026-05/backfill_report.md` | Operational report |

### Agent Logs (sjc-intel-architect)

| Log | Session |
|-----|---------|
| `logs/agents/sjc-intel-architect/2026-06-03_codex_strong_repo_advancement.md` | Codex Strong pass |
| `logs/agents/sjc-intel-architect/2026-06-03_deep_research_archive.md` | Deep Research archive |
| `logs/agents/sjc-intel-architect/2026-06-03_hermes_001_monitor_template.md` | HERMES-001 |
| `logs/agents/sjc-intel-architect/2026-06-03_src_001_source_promotion_packet.md` | SRC-001 packet |
| `logs/agents/sjc-intel-architect/2026-06-03_tier_1_2_promotion_review.md` | Tier 1+2 promotion |
| `logs/agents/sjc-intel-architect/2026-06-03_hermes_002_may_backfill_template.md` | HERMES-002 |
| `logs/agents/sjc-intel-architect/2026-06-03_may_2026_backfill_review.md` | Backfill review |
| `logs/agents/sjc-intel-architect/2026-06-03_backfill_informed_monitor_specs.md` | Monitor specs |
| `logs/agents/sjc-intel-architect/2026-06-03_sjc_utility_department_monitor_review.md` | Utility pilot |
| `logs/agents/sjc-intel-architect/2026-06-03_utility_monitor_lessons_applied.md` | Pilot lessons |
| `logs/agents/sjc-intel-architect/2026-06-03_cadence_system.md` | Cadence system |
| `logs/agents/sjc-intel-architect/2026-06-03_session_closeout.md` | Session closeout |

---

*End of session log. SJC_Intel is now in supervised operator mode.
Next session should begin with "get to work".*
