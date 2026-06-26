# SJC_Intel — Monitor Specifications

Each monitor spec defines how a specific source or source family should be
monitored: what to fetch, how to extract, how to classify, and how to handle
errors. Specs are informed by the May 2026 historical backfill evidence.

## Specification Format

Every monitor spec includes:

1. **source_id** or source family reference
2. **Homeowner relevance** — why this matters to residents
3. **Proven signal** — items actually found in the May 2026 backfill
4. **Source URLs** — pages to fetch
5. **Monitor cadence** — daily, weekly, event-driven
6. **Extraction approach** — how to parse the page
7. **Dedupe strategy** — how to avoid duplicates
8. **Classification defaults** — topic, community, urgency defaults
9. **Resident-interest defaults** — RI rules specific to this source
10. **Sensitivity/privacy rules** — special handling needed
11. **Expected failure modes** — what can go wrong
12. **Hermes readiness** — can this run now?
13. **Browser/PDF/manual requirements** — extra steps needed
14. **First pilot recommendation** — how to start

## Source Prioritization (from Backfill Evidence)

| Priority | Source | Cadence | Backfill Signal | Spec |
|----------|--------|---------|-----------------|------|
| 1 | `sjc_utility_department` | Daily | 3 items incl. Phase III water shortage | `sjc_utility_department.md` |
| 2 | `sjc_school_district` + `sjcsd_boarddocs` | Weekly | 10 items — high signal but noisy | `sjc_school_stack.md` |
| 3 | `sjc_bcc_calendar` | Weekly (pre/post meeting) | No items — known gap; agenda PDFs needed | `sjc_bcc_calendar.md` |
| 4 | `sjc_nbor_public_notices` | Daily | 25 records — NBOR app, plain HTML, rich source | `sjc_nbor_public_notices.md` |

## Sources Already With Monitor Specs (from earlier pilot)

| Source | Spec | Status |
|--------|------|--------|
| `sjc_county_news` | `docs/monitoring_workflow.md` (pilot) | Active |
| `sjso_news_stories` | `docs/monitoring_workflow.md` (pilot) | Active |
| `prompts/known_source_monitor_task.md` | Generic monitor task prompt | Available |

## Backfill Lessons

See `backfill_lessons_may_2026.md` for source-by-source performance, taxonomy
gap proposals, and recommended next pilots.
