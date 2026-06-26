# sjc-intel-architect Memory

Last updated: 2026-06-03

## Current State

- Phase: source promotion (Tier 1 + Tier 2 complete). Transitioning to monitor
  design and Hermes task contracts.
- 15 new official sources promoted into `registry/sources.yaml` (10 Tier 1, 5
  Tier 2). Total canonical sources: 24.
- Tier 3 (CDD governance, 4 candidates) and Tier 4 (community/developer, 6
  candidates) remain in candidate registry awaiting future promotion.
- St. Johns Citizen remains canonical and active.
- Repo is approaching autonomous readiness for supervised operator mode.

## Source Of Truth

- State: `STATE.md`
- Roadmap: `ROADMAP.md`
- Backlog: `BACKLOG.md`
- Checklists: `CHECKLIST.md`
- Operator mode: `docs/operator_mode.md`
- Self-improvement: `docs/self_improvement.md`
- Discovery loops: `docs/discovery_loops.md`
- Taxonomy: `docs/taxonomy.md`
- Source candidates: `registry/source_candidates.yaml`
- Canonical sources: `registry/sources.yaml`
- Beat candidates: `registry/beat_candidates.yaml`
- Search terms: `registry/search_terms.yaml`
- May plan: `docs/backfill/may_2026_backfill_plan.md`
- Promotion packet: `docs/source_promotion/first_wave_source_promotion_packet.md`
- Promotion review: `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md`

## Promotion Status

- **Tier 1 (core official):** 10 promoted
- **Tier 2 (school/transport/weather/civic):** 5 promoted
- **Tier 3 (CDD governance):** pending future promotion
- **Tier 4 (community/developer):** pending future promotion
- **Deferred:** 13 sources
- **Duplicates:** 6
- **Manual review needed:** Property Appraiser URL (SRC-002)

## Next Recommended Task

Evaluate cadence via LAST_RUN markers at session start. Daily sources due:
`sjc_utility_department`, `sjc_county_news`, `sjso_news_stories`. Weekly
sources due: `sjc_school_stack`, BCC calendar, backlog review. Monthly tasks
due: source gaps, taxonomy review, cleanup.

## Active Backlog Summary

- Operator docs/checklists/backlog: complete.
- Cadence system: created (`docs/cadence.md`, `logs/runs/`).
- Source promotion: Tier 1 + 2 done (SRC-001 complete).
- Hermes task contracts: HERMES-001 and HERMES-002 done; HERMES-003 remaining.
- May 2026 backfill: executed (BF-002 complete). 21 items.
- Monitor specs: 5 created.
- **`sjc_utility_department` pilot: done** — first daily-ready source.
- SJC School District pilot: spec ready; awaiting execution.
- Property Appraiser URL conflict: open (SRC-002).
- Taxonomy gaps evidence ready: `water_restrictions` (TAX-003), `budget_millage` (TAX-004).
- Editorial/review queue: future.

## Blockers And Gates

- Property Appraiser URL conflict (SRC-002) needs manual verification.
- No Hermes runtime exists for automated monitoring.
- Buddy approval required for: Tier 3/4 promotion, taxonomy/schema changes,
  live monitor execution without supervision, backfill execution, scheduled
  automation, and publishing.
- Public sources only. No private Facebook groups, login-gated resident portals,
  or private screenshots.

## Session Closeout

Full closeout appended to `logs/sessions/2026-06-03_initial_sjc_intel_buildout.md`.
Repo is now in supervised operator mode. Next session begins with "get to work".

## Latest Agent Log

- `logs/agents/sjc-intel-architect/2026-06-03_codex_strong_repo_advancement.md`
- `logs/agents/sjc-intel-architect/2026-06-03_hermes_001_monitor_template.md`
- `logs/agents/sjc-intel-architect/2026-06-03_src_001_source_promotion_packet.md`
- `logs/agents/sjc-intel-architect/2026-06-03_tier_1_2_promotion_review.md`
- `logs/agents/sjc-intel-architect/2026-06-03_hermes_002_may_backfill_template.md`
- `logs/agents/sjc-intel-architect/2026-06-03_may_2026_backfill_review.md`
- `logs/agents/sjc-intel-architect/2026-06-03_backfill_informed_monitor_specs.md`
- `logs/agents/sjc-intel-architect/2026-06-03_sjc_utility_department_monitor_review.md`
- `logs/agents/sjc-intel-architect/2026-06-03_cadence_system.md`
- `logs/agents/sjc-intel-architect/2026-06-03_session_closeout.md`

## Durable Decisions

- Use discovery loops rather than a single pipeline.
- Official records are authoritative for consequential claims; local media is
  context/tip-surfacing unless cross-verified.
- CDD governance, utilities/water, and transportation/roadwork are first-class
  homeowner operating areas.
- May 2026 is the first backfill baseline.
- Hermes delegation model: bounded worker tasks with architect review.
- Memory stays concise; narrative history belongs in logs.
