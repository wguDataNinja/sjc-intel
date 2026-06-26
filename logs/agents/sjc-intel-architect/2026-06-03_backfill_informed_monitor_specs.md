# sjc-intel-architect Operator Log — Backfill-Informed Monitor Specs

**Date/time:** 2026-06-03  
**Agent:** `sjc-intel-architect`  
**Task:** Create monitor specification documents for 4 source families based on May 2026 backfill evidence

## Inputs Read

- `data/monthly/2026-05/discovered_items.yaml` (21 items)
- `data/monthly/2026-05/topic_clusters.yaml` (4 clusters)
- `data/monthly/2026-05/source_gaps.md` (7 gaps)
- `data/monthly/2026-05/backfill_report.md` (source-check log)
- `docs/monitoring_workflow.md`
- `prompts/known_source_monitor_task.md`
- `registry/sources.yaml` (24 sources)
- `docs/taxonomy.md`
- `STATE.md`
- `BACKLOG.md`
- `.opencode/agent_memory/sjc-intel-architect.memory.md`

## Deliverables Created (6 files)

### Monitor Specs

| File | Source | Cadence | Hermes Ready? | Key Insight from Backfill |
|------|--------|---------|---------------|---------------------------|
| `docs/monitor_specs/sjc_utility_department.md` | `sjc_utility_department` | Daily | YES | 3 items in May; Phase III water shortage was highest-impact event |
| `docs/monitor_specs/sjc_school_stack.md` | `sjc_school_district` + `sjcsd_boarddocs` | Weekly | PARTIAL (homepage yes, BoardDocs needs browser) | 10 items but ~30% noise — signal filtering rules added |
| `docs/monitor_specs/sjc_bcc_calendar.md` | `sjc_bcc_calendar` | Weekly (pre/post meeting) | NOT YET (PDF-gated) | Zero items — biggest gap confirmed. Agenda PDFs need extraction strategy |
| `docs/monitor_specs/sjc_road_closures.md` | `sjc_road_closures` | Daily | NOT YET (app-first) | Zero items — landing page links to external app. Investigation phase designed |
| `docs/monitor_specs/backfill_lessons_may_2026.md` | Cross-source | Reference | — | Source-family patterns, taxonomy gaps, next pilots |
| `docs/monitor_specs/README.md` | Overview | Index | — | Prioritization and reference |

### Key Design Decisions

1. **Signal/noise filtering for school stack:** 40% high-signal, 30% medium,
   30% noise. Added explicit filtering rules and classification tables so the
   monitor can tag signal level and editorial queue can dismiss noise.

2. **BCC pre/post meeting pattern:** Instead of daily polling (which yields
   nothing between meetings), designed a 2-phase weekly pattern: pre-meeting
   (agenda check) and post-meeting (minutes/votes check). PDF extraction added
   as phase 2.

3. **Road closures investigation-first:** Explicitly designed the spec to
   start with an app investigation phase before any scraper build. Documented
   the fallback chain (FDOT map → Florida 511 → local media).

4. **Utility department first pilot:** This is the highest-leverage first
   monitor because it's Hermes-ready, backfill-proven, and covers the
   highest-impact May story (water shortage).

## State File Changes

| File | Change |
|------|--------|
| `BACKLOG.md` | MON-002 → done; MON-003 → done; MON-005 added for BCC |
| `STATE.md` | Added monitor specs to completed work; updated next task |
| `.opencode/agent_memory/sjc-intel-architect.memory.md` | Updated backlog, next task, log pointer |
| This log | Created |

## Next Recommended Action

1. **Run `sjc_utility_department` monitor pilot** — highest-leverage, Hermes-ready.
2. **Investigate SJC Road Closures app URL** — determine extraction feasibility.
3. **Manually inspect 1-2 BCC agenda PDFs** — validate the PDF-gated pattern.
4. **Promote taxonomy gaps** — `water_restrictions` and `budget_millage` have
   real evidence.
