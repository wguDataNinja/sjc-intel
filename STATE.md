# SJC_Intel — Project State

Last update: 2026-06-03  
Status owner: `sjc-intel-architect`

## Current Phase

**Source promotion — Tier 1 and Tier 2 complete. Transitioning to monitor design and Hermes task contracts.**

The repo has promoted 15 new official sources into `registry/sources.yaml`,
bringing the total canonical source count to 24. The monitoring backbone for
St. Johns County decision, development, transportation, utility, school, and
civic stacks is now registered. Tier 3 (CDD governance) and Tier 4
(community/developer) sources remain in the candidate registry awaiting future
promotion.

## What Deep Research Changed

- Official records are the first authority for consequential claims.
- Local media is useful for tip-surfacing/context, not as sole authority for
  votes, permits, taxes, CDD assessments, roads, schools, utilities, or legal
  claims.
- Source stacks/families matter: county decision stack, PZA/development stack,
  permit stack, roads/transportation, utilities/SJRWMD, school/BoardDocs, CDDs,
  resident-cost records, community/developer pages, and media context.
- CDD governance is now a first-class homeowner source family.
- Utilities/water and transportation/roadwork are daily monitoring beats.
- May 2026 replaces January 2026 as the first historical backfill baseline.

## Promotion Status

- **Tier 1 (Core official stacks):** 10 sources promoted — Commission, PZA,
  roads, utilities, budget, emergency management, clerk, permits, transportation,
  SJRWMD.
- **Tier 2 (School/transportation/weather/civic):** 5 sources promoted —
  BoardDocs, zoning, FDOT/NFLRoads, NWS Jacksonville, Supervisor of Elections.
- **Total canonical sources:** 24 (9 pre-existing + 15 new).
- **Tier 3 (CDD governance):** 4 candidates remain — awaiting future promotion.
- **Tier 4 (Community/developer):** 6 candidates remain — awaiting future promotion.
- **Deferred sources:** 13 — lower priority.
- **Duplicates:** 6 — already covered by canonical sources.
- **Sources needing manual review:** Property Appraiser URL (SRC-002) unresolved;
  Clerk placeholder replaced by new `sjc_clerk_online_research`.

## Recent Completed Work (2026-06-03 session)

- **HERMES-001: Draft known-source monitor task template** — Completed.
  Created `prompts/known_source_monitor_task.md`.

- **SRC-001: Source promotion review packet** — Completed.
  Created `docs/source_promotion/first_wave_source_promotion_packet.md`.

- **Tier 1 + Tier 2 Promotion (Hermes delegated):** Completed.
  - 15 sources promoted via bounded Hermes tasks (A + B).
  - Task C reviewed and validated all promotions.
  - Review artifact: `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md`.
  - Hermes task contracts created: `prompts/hermes_tier_1_promotion_task.md`,
    `prompts/hermes_tier_2_promotion_task.md`,
    `prompts/hermes_promotion_review_task.md`.
  - Operator log: `logs/agents/sjc-intel-architect/2026-06-03_tier_1_2_promotion_review.md`.

- **HERMES-002: Draft May 2026 backfill task template** — Completed.
  Created `prompts/hermes_may_2026_backfill_task.md` with all 15 required
  sections. Executed via BF-002.

- **BF-002: May 2026 historical backfill executed** — Completed.
  Ran full first-pass official-source backfill. 21 items extracted across
  5 source families. All 6 pass criteria met. 5 output files produced.

- **Backfill-informed monitor specifications** — Completed.
  Created 5 monitor spec documents informed by May 2026 backfill evidence.
  Backlog items MON-002 and MON-003 marked done; MON-005 added for BCC calendar.

- **`sjc_utility_department` monitor pilot executed** — Completed.
  First backfill-informed live monitor run. 5 items extracted. YAML valid.
  Prior index updated. **First daily-ready source.** Spec updated with
  sidebar extraction scope and pilot lessons. Taxonomy gap `water_restrictions`
  confirmed with live evidence (TAX-003).

- **Cadence system created** — Completed.
  Created `docs/cadence.md` defining daily, weekly, and monthly operating
  rhythms with catch-up rules, Hermes/delegation guidance, and LAST_RUN
  marker system. Created `logs/runs/` directory structure with README.md.
  Updated `docs/operator_mode.md` and `CHECKLIST.md` to include cadence
  evaluation in startup and end-of-session routines.

## Current Recommended Next Task

**When Buddy says "get to work": evaluate cadence via LAST_RUN markers.**

Current cadence state (all just initialized):

| Cadence | Last Run | Due? |
|---------|----------|------|
| Daily | 2026-06-03 | Yes — all daily sources due |
| Weekly | 2026-06-03 | Yes — all weekly sources due |
| Monthly | 2026-06-03 | Yes — all monthly tasks due |

Next session should select from due work based on cadence priorities:

1. **Daily bucket:** `sjc_utility_department` (daily-ready) or `sjc_county_news`
2. **Weekly bucket:** `sjc_school_stack` pilot or BCC calendar investigation
3. **Monthly bucket:** Source gaps, taxonomy review, memory cleanup

Or promote taxonomy changes: `water_restrictions` and `budget_millage` now have
real item evidence supporting canonical addition (TAX-003, TAX-004).

Or draft **HERMES-003** (search discovery task template).

## Current Blockers

- Property Appraiser URL conflict (SRC-002) — needs manual verification.
- No Hermes runtime to execute automated monitor cycles.
- No review queue artifact (ED-001).

Approval gates remain:

- taxonomy/schema changes
- live monitor execution without human supervision
- May 2026 backfill execution
- scheduled automation
- publishing/newsletter work
- Tier 3 and Tier 4 promotion

## Operator Mode Readiness

**Verdict: ready for supervised operator mode; approaching autonomous readiness.**

Now ready:

- `ROADMAP.md`
- `CHECKLIST.md`
- `BACKLOG.md`
- `docs/operator_mode.md`
- `docs/self_improvement.md`
- concise architect memory
- 15 new canonical source promotions completed
- Hermes task contracts drafted (monitor + 2 promotion + review)

Not yet ready:

- Monitor specs not piloted for all Tier 1/Tier 2 sources.
- No Hermes runtime for automated monitoring.
- No review queue exists (ED-001).
- No scheduled automation exists, by design.

## What To Do When Buddy Says "Get To Work"

1. Read `docs/operator_mode.md`.
2. Read `docs/cadence.md`.
3. Check `logs/runs/` LAST_RUN markers for due cadence work.
4. Read `BACKLOG.md`.
5. Pick the highest-priority unblocked task from due cadence buckets that does
   not require approval.
6. Prefer monitor spec execution, Hermes task delegation, or backlog/state
   hygiene based on cadence.
7. Write meta-run log to `logs/runs/` and update LAST_RUN markers.
8. Log the work and update memory/state at the end.

## What Should Wait

- Running May 2026 backfill.
- Running live monitors without Buddy instruction.
- Creating cron/launchd/scheduled automation.
- Publishing or newsletter work.
- Private or login-gated source collection.
- Tier 3 and Tier 4 source promotion.

## Key Files

| File | Purpose |
|------|---------|
| `ROADMAP.md` | Phase roadmap and readiness criteria |
| `CHECKLIST.md` | Operating gates |
| `BACKLOG.md` | Grouped actionable backlog |
| `docs/operator_mode.md` | How architect operates when told to work |
| `docs/self_improvement.md` | How agents improve workflows safely |
| `docs/discovery_loops.md` | Loop operating model |
| `docs/taxonomy.md` | Controlled vocabularies, source families, beat groups |
| `docs/backfill/may_2026_backfill_plan.md` | Planned May 2026 backfill |
| `docs/source_promotion/first_wave_source_promotion_packet.md` | Promotion packet |
| `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md` | Promotion review |
| `prompts/known_source_monitor_task.md` | Monitor task prompt |
| `prompts/hermes_tier_1_promotion_task.md` | Tier 1 Hermes contract |
| `prompts/hermes_tier_2_promotion_task.md` | Tier 2 Hermes contract |
| `prompts/hermes_promotion_review_task.md` | Promotion review contract |
| `docs/cadence.md` | On-demand cadence system |
| `logs/runs/README.md` | Meta-run log format |
| `registry/sources.yaml` | Source registry (24 sources) |
| `registry/source_candidates.yaml` | Candidate source extraction |
| `registry/beat_candidates.yaml` | Candidate beat extraction |
| `registry/search_terms.yaml` | Operational search terms |
| `.opencode/agent_memory/sjc-intel-architect.memory.md` | Concise current memory |
| `README_INTERNAL.md` | Durable agent memory — startup context, decisions, watchouts |
| `.opencode/agents/sjc-intel-source-watch.md` | Source-discovery agent definition |
| `.opencode/agent_memory/sjc-intel-source-watch.memory.md` | Source-watch agent memory |
