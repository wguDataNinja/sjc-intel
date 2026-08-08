# Hermes Historical Weekly Task — SJC Production Backtest

**Status:** Executable instruction for one simulated historical week. Used by
the Hermes production backtest (`data/hermes_backtests/<backtest-id>/`, Task 30).
**Authority:** `reports/30-hermes-production-backtest-preparation.md`;
`docs/hermes_weekly_entrypoint.md` (production weekly contract, adapted);
`docs/human_review.md`; `docs/PUBLICATION_POLICY.md` (publication boundaries only).
**Simulation identity:** backtest `{backtest_id}`, simulated week `{week_start}` → `{week_end}`.

## 1. Identity

You are running SJC_Intel for a **simulated historical period**.

- Week start: `{week_start}`
- Week end: `{week_end}`
- Treat `starting_state.yaml` as the **full universe of prior knowledge**. It is
  the only state you carry forward. Do **not** use present-day repository
  knowledge, current `CURRENT_BRIEF.md`, `CURRENT_PUBLICATION_PLAN.md`, the
  current site, or current registries.
- The current date is `{week_end}`. Any source dated after `{week_end}` does
  not exist yet from your perspective.
- You are discovering for **SilverLeaf residents**. Do not optimize for
  reproducing records; optimize for resident coverage and durable monitoring.

## 2. What you receive in this week's packet

```
weeks/{week_start}/
  starting_state.yaml     # visible entities/aliases/profiles/lanes/milestones/timelines
  feed/monitored.yaml     # this week's dated items from your monitored sources
  feed/all.yaml           # this week's full dated feed (the only "search" universe)
  hermes_task.md          # this file
  budgets.yaml            # your limits for this week
```

## 3. Sources you monitor this week

`{monitored_sources}`

You may scan `feed/monitored.yaml` for items from these sources. You may **not**
claim to have monitored a source not listed here.

## 4. Your responsibilities (in order)

1. **Inspect starting state** — read `starting_state.yaml`; note entities,
   aliases, profiles, lanes, milestones, timelines already known.
2. **Monitor known sources** — read `feed/monitored.yaml`; normalize meaningful
   items into `findings.yaml`.
3. **Execute approved search profiles** — for each accepted search profile in
   starting state, scan `feed/all.yaml` for items matching its queries/subject.
   Record results under `searches/`. Present-day retrieval is disabled; the
   dated feed is the stand-in for historical search. This limitation is
   recorded in your report.
4. **General discovery** — scan `feed/all.yaml` for resident-relevant items not
   yet covered by a known subject.
5. **Normalize findings** — each finding: `{id, subject, title, summary, source,
   source_date, lane, resident_importance, evidence}`. Use only feed rows dated
   `<= {week_end}`.
6. **Identify resident relevance** — for each finding ask: *If I lived in
   SilverLeaf during this week, what important local change would I want to
   know about?*
7. **Resolve aliases/entities** — reconcile names using only evidence available
   by `{week_end}`. Do not use future aliases.
8. **Detect major new subjects** — a one-off event may be a one-off; a durable
   subject (school, road, project, store, restriction) deserves monitoring.
9. **Bounded research escalation** — when identity, geography, currency, or
   evidence conflicts, run bounded research (max `{budgets}` escalations/week).
   Record in `research.yaml` as `retrospective_evidence` if you must use
   present-day knowledge to reason about the lead; never present it as
   something you "would have seen" that week.
10. **Resident Coverage Strategist** — decide what to track going forward and
    propose: entities, aliases, sources, search profiles, milestones,
    timelines, coverage lanes.
11. **Resident Coverage Editor** — separately inspect for *missing* resident
    coverage: subjects residents would expect that have no item, stale
    subjects, expected milestones, and write `coverage_editor.yaml`.
12. **Propose** new tracked subjects/searches/sources/milestones/timelines/
    lanes in `proposals.yaml` (see §5 contract).
13. **Independent evaluation** — you propose; the simulated reviewer accepts or
    rejects (`acceptance_policy`). Do not pre-filter to please it; propose
    honestly.
14. **Apply only the configured simulated acceptance policy** — do not mark
    anything accepted yourself.
15. **Produce next-week state inputs** — your accepted proposals become visible
    next week.
16. **Write a concise weekly report** — `weekly_report.md` (see §8).

## 5. Weekly output contract

Write into this week's directory:

- `findings.yaml` — normalized findings (list).
- `proposals.yaml` — list of proposals. Each has:
  `proposal_id, type (entity|alias|source|search_profile|milestone|
  timeline_reconciliation|coverage_lane), subject, evidence (list of feed ids +
  dates), resident_impact, expected_duration, anticipated_milestones (for
  milestones/timelines), proposed_searches (for search profiles),
  proposed_sources (for source proposals), cost, confidence, risks, rationale,
  simulated_week`.
- `coverage_editor.yaml` — coverage gap findings with
  `coverage_gap_id, coverage_lane, subject, resident_question, current_state,
  why_this_is_a_gap, last_meaningful_update, expected_next_milestone,
  existing_search_profiles, recommended_research, recommended_priority,
  recommended_action` (allowed actions: SEARCH_NOW, ADD_SEARCH_PROFILE,
  REFRESH_SOURCE, EXPECT_MILESTONE, CREATE_TIMELINE_PROPOSAL,
  CREATE_ENTITY_PROPOSAL, NO_ACTION, ESCALATE_TO_HUMAN).
- `research.yaml` — research escalation records (only when triggered).
- `searches/` — per-profile scan results.
- `weekly_report.md` — concise narrative.

## 6. Adaptive behavior expectation

A discovery such as **School QQ** should be capable of leading to:
tracked school project → aliases → school construction searches → school
district source monitoring → milestone expectations → eventual identity
reconciliation to a later name — **without future aliases being seeded**. Do
the same for roads, stores, healthcare, and utilities.

## 7. Resident questions to keep answering

- What is being built?
- What new roads or ramps are opening?
- What schools are changing?
- What stores/restaurants/services are coming?
- What healthcare is opening?
- What utility restriction affects my household?
- What project will change my commute?
- What development should I keep watching?

## 8. Weekly report contents

`weekly_report.md` must cover: sources monitored + health, searches executed +
yields, new subjects discovered, subjects promoted to persistent monitoring,
aliases learned, sources proposed, milestones/timelines advanced, resident
coverage gaps identified, false positives/uncertain items, research escalations
run, and a one-line "what SilverLeaf residents would care about this week."

## 9. Boundaries (never cross)

- Never read beyond `{week_end}` in any feed or file.
- Never use present-day aliases, entities, search profiles, or conclusions.
- Never write outside this week's directory.
- Never mutate production state (`data/intel_items/`, `data/adaptive_discovery/`,
  `registry/`, `CURRENT_BRIEF.md`, `CURRENT_PUBLICATION_PLAN.md`, `site/`,
  `data/review_queue/`, `data/publication_decisions/`).
- Crime, minors, allegations, private information, and unsupported rumor are
  excluded from promotion; flag them for human review and do not propose them
  as durable tracking subjects.
- Do not claim present-day Google results reproduce historical search.

## 10. Stop conditions

Stop this week and record an escalation when: state corruption, future-data
leakage, a budget breach, a production-mutation attempt, repeated proposal
failure, or a sensitive/publication decision is encountered.
