# SJC_Intel

AI-assisted local intelligence/reporting system for St. Johns County, Florida.

SJC_Intel is homeowner/resident-first. It discovers, monitors, classifies,
verifies, and organizes public information that affects daily life, property,
schools, roads, utilities, public safety, taxes, construction, development,
amenities, and community governance.

## Operating Model

SJC_Intel is organized around discovery loops:

1. Known-source monitoring
2. Search discovery
3. Historical backfill
4. Cross-section / beat clustering
5. Taxonomy improvement
6. Review / editorial
7. Local-media/social-news discovery

Official records are the first authority for consequential claims. Local media
is useful for surfacing tips and context, but claims about votes, permits,
taxes, roads, utilities, schools, CDD assessments, public safety, and legal
notices should resolve back to public records or attributable reporting.

## Current Status

Current phase: **operator-readiness foundation after Deep Research ingestion**.

Completed:

- Source and intel item schemas
- Community registry
- Two monitor pilots: county news and SJSO news stories
- Resident-interest classifier docs/prompt
- Discovery loops
- Deep Research archive and intake note
- Deep Research extraction into:
  - `registry/source_candidates.yaml`
  - `registry/beat_candidates.yaml`
  - `registry/search_terms.yaml`
- May 2026 backfill plan
- Operator docs, roadmap, backlog, and checklists

Not yet done:

- No May 2026 backfill has been run.
- No live monitors were run as part of the Deep Research extraction pass.
- No new source candidates were promoted to canonical sources.
- No scheduled automation, cron, or launchd jobs exist.
- No public publishing/newsletter pipeline exists.

## Deep Research

Archived report:

- `docs/deep_research/reports/2026-06-03_homeowner_public_source_monitoring_map.md`

Extraction reviews:

- `docs/deep_research/2026-06-03_source_extraction_review.md`
- `docs/deep_research/2026-06-03_beat_extraction_review.md`
- `docs/deep_research/2026-06-03_search_term_extraction_review.md`

Deep Research changed the first backfill baseline from January 2026 to May
2026. The plan is in `docs/backfill/may_2026_backfill_plan.md`. Do not run it
without explicit instruction.

## Key Files

| File | Purpose |
|------|---------|
| `STATE.md` | Current operating state and next action |
| `ROADMAP.md` | Phase roadmap and readiness criteria |
| `BACKLOG.md` | Grouped actionable backlog |
| `CHECKLIST.md` | Operating gates |
| `AGENTS.md` | Agent roles and repo rules |
| `docs/operator_mode.md` | How `sjc-intel-architect` operates when told to work |
| `docs/self_improvement.md` | Agent improvement rules |
| `docs/discovery_loops.md` | Loop model |
| `docs/taxonomy.md` | Controlled vocabularies and beat/source-family notes |
| `docs/monitoring_workflow.md` | Known-source monitoring workflow |
| `docs/resident_interest_classification.md` | Resident-interest classification rules |
| `registry/sources.yaml` | Canonical source registry |
| `registry/source_candidates.yaml` | Candidate source registry |
| `registry/beat_candidates.yaml` | Candidate beat registry |
| `registry/search_terms.yaml` | Operational search terms |

## Safety Rules

- Public sources only.
- No private Facebook groups.
- No login-gated or members-only scraping.
- No fake accounts or impersonation.
- No publishing private screenshots.
- No treating resident chatter as verified fact.
- Human review before publishing sensitive items.
- No publishing yet.

## Project Agent

This repo includes the OpenCode agent `sjc-intel-architect`. It should use
`STATE.md`, `BACKLOG.md`, `ROADMAP.md`, `CHECKLIST.md`, and
`docs/operator_mode.md` to resume work without the project being re-explained.
