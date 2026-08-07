# SJC_Intel — On-Demand Cadence System

> When Buddy says "get to work", `sjc-intel-architect` evaluates what cadence
> work is due, selects a task, delegates to Hermes if appropriate, and logs
> the run. No cron, no launchd, no scheduled automation.

---

## 1. How Cadence Works

SJC_Intel operates on daily, weekly, and monthly rhythms. SJC has no local
scheduler; an Ivy-owned VPS timer remains a separate privileged activation
step. Supervised/manual weekly operation is ready.
When the agent runs, it checks `logs/runs/` to determine what work is overdue,
then picks the highest-priority unblocked task that fits the cadence.

Adaptive discovery remains supervised: a weekly run may generate proposals,
but a separate review accepts state transitions for the following week. The
historical/restartable harness is `docs/adaptive_discovery_backtest.md`.

**Missed days are acceptable.** Missed full weeks should be avoided. Monthly
tasks can slip by a few days.

When Buddy says "get to work":

1. Read `docs/cadence.md` (this file).
2. Read `README_INTERNAL.md` and `BACKLOG.md`.
3. Read `docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md` if
   product-direction context is needed for task selection.
4. Read `logs/runs/README.md` for the run-log format.
4. Check `logs/runs/daily/LAST_RUN` for the last daily run timestamp.
5. Check `logs/runs/weekly/LAST_RUN` for the last weekly run timestamp.
6. Check `logs/runs/monthly/LAST_RUN` for the last monthly run timestamp.
7. Determine which cadence buckets are due.
8. Pick the smallest safe unblocked task from the due buckets.
9. Execute or delegate.
10. Write a meta-run log to `logs/runs/{cadence}/{YYYY-MM-DD}_{task}.md`.
11. Update LAST_RUN markers.
12. Update `README_INTERNAL.md`, `BACKLOG.md`, memory, and agent log if state changed.

---

## 2. Daily Cadence

**Tolerance:** Missing a day is fine. If more than 2 consecutive days pass,
prioritize the daily bucket before starting weekly work.

### Daily Sources

| Priority | Source ID | Type | Spec | Status |
|----------|-----------|------|------|--------|
| 1 | `sjc_utility_department` | Utility/water announcements | `docs/monitor_specs/sjc_utility_department.md` | Pilot passed; Hermes-ready |
| 2 | `sjc_county_news` | County press releases | `docs/monitoring_workflow.md` (pilot) | Active |
| 3 | `sjso_news_stories` | Sheriff news stories | `docs/monitoring_workflow.md` (pilot) | Active |
| 4 | `sjc_emergency_management` | Emergency alerts/preparedness (hurricane season) | `docs/monitor_specs/backfill_lessons_may_2026.md` | Seasonal daily: June-November. Activated 2026-06-26. |
| 5 | `sjc_nbor_public_notices` | NBOR public notices (road closures, hearings, permits) | `docs/monitor_specs/sjc_nbor_public_notices.md` | Extractor built, daily-ready, 25 records |
| 6 | `st_johns_citizen` | Local media context scan | `registry/sources.yaml` | Tip/context only; not full extraction |

### Daily Task Selection

Pick **one** daily source per agent run. Do not try to run all daily sources
in one session — that leads to long runs. The goal is steady progress. The
first integrated daily cycle (2026-06-26) proved all 4 sources can run in
one session, but this should be reserved for catch-up.

If more than 2 consecutive daily runs were missed, run 2 daily sources in
the current session to catch up, but no more than 2.

### Daily Source Run Order (Recommended)

| Priority | Source | Method | Notes |
|----------|--------|--------|-------|
| 1 | `sjc_nbor_public_notices` | `python3 scripts/extract_nbor.py` | Highest yield (25 items). Auto-generates YAML. |
| 2 | `sjc_utility_department` | Manual (HTTP GET + parse Announcements) | Slow-updating. Check for new alerts. |
| 3 | `sjc_county_news` | Manual (HTTP GET + parse Featured News) | WordPress blog. |
| 4 | `sjso_news_stories` | Manual (HTTP GET + parse blog) | WordPress blog. |
| 5 | `sjc_emergency_management` | Manual (HTTP GET + check for alerts) | Seasonal: daily June-November (hurricane season). |

### Daily Output

Each daily monitor run produces:
- `data/source_events/{YYYY-MM-DD}/{source_id}.yaml` — source event record (container for the fetch)
- `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml` — extracted items with `source_event_id` linking to parent event
- `data/intel_items/{YYYY-MM-DD}/daily_cycle_summary.yaml` — cross-source summary (optional, for full cycles)
- Prior items index update via `python3 scripts/rebuild_dedupe_index.py`
- Review queue update via `python3 scripts/build_review_queue.py` (optional after individual runs; recommended after full cycles)
- Hermes worker log (if delegated)

### Daily Dedupe Step

After extracting items, update the dedupe index:

```
python3 scripts/rebuild_dedupe_index.py
```

This scans all intel_item YAML files, generates deterministic keys, and
writes unique entries to `data/index/prior_items.yaml`. Safe to run
multiple times — skips duplicate keys on subsequent runs.

---

## 3. Weekly Cadence

**Tolerance:** Missing a week should be avoided. If the last weekly run is
more than 10 days old, prioritize weekly work before starting new daily
items. If more than 14 days have passed, run a catch-up weekly session
covering all weekly sources.

### Weekly Sources

| Priority | Source ID | Type | Spec | Status |
|----------|-----------|------|------|--------|
| 1 | `sjc_bcc_calendar` | County Commission meetings | `docs/monitor_specs/sjc_bcc_calendar.md` | Spec ready; pre/post meeting design |
| 2 | `sjcsd_boarddocs` | School Board agenda system | `docs/monitor_specs/sjc_school_stack.md` | Spec ready; BoardDocs extraction pending |
| 3 | `sjc_school_district` | District news (filtered) | `docs/monitor_specs/sjc_school_stack.md` | Spec ready; signal/noise filtering |
| 4 | `sjc_pza_boards` | Planning & Zoning meetings | `docs/monitor_specs/backfill_lessons_may_2026.md` | Investigation needed |
| 5 | `sjc_development_tracker` | Development GIS map | `registry/sources.yaml` | Browser automation likely needed |
| 6 | `sjc_permit_status` | Permit search portal | `registry/sources.yaml` | Form interaction needed |
| 7 | `fdot_district_two_nflroads` | State road projects | `registry/sources.yaml` | Per-project pages needed |
| 8 | Source candidate review | Candidate registry | `registry/source_candidates.yaml` | Direct repo work |
| 9 | Backlog review | All backlog items | `BACKLOG.md` | Direct repo work |

### Weekly Task Selection

Pick **one or two** weekly items per session. Prioritize sources that have
monitor specs and are ready to pilot (BCC, school stack) over those still
needing investigation (PZA, permits).

### Weekly Output

Each weekly source check produces:
- Intel items (if applicable)
- Candidate status updates (if reviewing candidates)
- Backlog updates (if reviewing backlog)

---

## 4. Monthly Cadence

**Tolerance:** Monthly tasks can slip by a few days. If more than 40 days
have passed since the last monthly run, prioritize it before weekly work.

### Monthly Tasks

| Priority | Task | Owner | Artifact |
|----------|------|-------|----------|
| 1 | Monthly wrap | architect/reviewer | `data/monthly/{YYYY-MM}/monthly_wrap.md` |
| 2 | Topic clusters from monthly items | architect | `data/monthly/{YYYY-MM}/topic_clusters.yaml` |
| 3 | Source gaps review | architect | `data/monthly/{YYYY-MM}/source_gaps.md` |
| 4 | Taxonomy gap review | architect | Proposals to `docs/taxonomy.md` |
| 5 | Source performance review | architect | `logs/runs/monthly/` report |
| 6 | Memory/log cleanup | architect | Trim memory; archive old logs |
| 7 | Self-improvement review | architect | Review friction; propose changes |

### Monthly Task Selection

Monthly work is a full-session commitment. When monthly work is due, dedicate
at least one entire agent session to it. Do not mix daily or weekly work into
a monthly session unless the monthly tasks are complete.

### Monthly Output

Each monthly cycle produces:
- `data/monthly/{YYYY-MM}/monthly_wrap.md`
- `data/monthly/{YYYY-MM}/topic_clusters.yaml` (if new items exist)
- `data/monthly/{YYYY-MM}/source_gaps.md`
- Updated taxonomy proposals (if gaps found)
- Memory/log cleanup

---

## 5. When to Use Hermes

Delegate to Hermes when:

| Condition | Example |
|-----------|---------|
| Source collection with clear inputs/outputs | Fetch → extract → classify a daily source |
| Monitor/backfill run authorized | Daily monitor cycles, backfill passes |
| Task verifiable from produced files | YAML output can be checked after run |
| Task is bounded and repeatable | Same extraction approach each time |

Do **not** delegate to Hermes when:

| Condition | Example |
|-----------|---------|
| Task needs architecture judgment | Taxonomy decisions, promotion review |
| Task edits source-of-truth docs | Schema updates, registry changes |
| Task requires human judgment | Sensitivity review, controversy assessment |
| Extraction method is unproven | First investigation of a new source |

---

## 6. When to Do Direct Repo Work

Do direct (architect) work when:

| Condition | Example |
|-----------|---------|
| Documentation | Cadence docs, monitor specs, READMEs |
| Registry cleanup | Candidate updates, dedupe, notes |
| Schema review | Taxonomy, intel_item, source schemas |
| Backlog/state hygiene | Updating README_INTERNAL.md, BACKLOG.md, memory |
| Investigation | Determining whether a source is monitorable |
| Architecture judgment | Deciding what to build next |

---

## 7. Choosing the Smallest Safe Task

When multiple tasks are due, pick the one that:

1. Is **safe** — does not require approval, does not touch private content,
   does not publish.
2. Is **small** — can be completed in a single agent session.
3. Is **unblocked** — no dependencies on Buddy approval, Hermes runtime, or
   unresolved investigations.
4. Is **highest priority** within its cadence bucket.

If the highest-priority task is blocked, pick the next highest. Do not skip
an entire cadence bucket because one task is blocked.

---

## 8. How Cadence Interacts with README_INTERNAL.md, BACKLOG.md, Memory, and Logs

### README_INTERNAL.md

Updated after every session that produces durable output:
- Update "Current Phase" and architecture counts
- Add completed work to open loops / backlog
- Update "Open Loops" if status changes

### BACKLOG.md

Updated when task statuses change:
- Mark items `done` when complete
- Update `in_progress` items with latest next action
- Add new items when gaps are discovered
- Do not remove deferred items — keep them visible

### Memory (`.opencode/agent_memory/sjc-intel-architect.memory.md`)

Keep short:
- Current phase (1 line)
- Promotion status (1-2 lines)
- Next recommended task (1-2 lines)
- Active backlog summary (5-8 lines)
- Blockers (2-3 lines)
- Latest agent log pointer (1 line)

### Run Logs (`logs/runs/`)

Every agent session writes a meta-run log. See `logs/runs/README.md` for
the format. The run log records what cadence was evaluated, what was due,
what was selected, and what was produced.

### Agent Logs (`logs/agents/`)

Detailed technical log of what the agent did, what files it read, what files
it changed, and what decisions it made. Written after every session.

---

## 9. LAST_RUN Markers

Each cadence directory contains a `LAST_RUN` file with the ISO 8601 timestamp
of the last completed run for that cadence. The agent reads these to determine
what is overdue.

**Format:**
```
2026-06-03T23:30:00Z
```

**Files:**
- `logs/runs/daily/LAST_RUN`
- `logs/runs/weekly/LAST_RUN`
- `logs/runs/monthly/LAST_RUN`

If a `LAST_RUN` file does not exist, treat all sources in that cadence as due.

### Run Types and LAST_RUN Rules

| Run Type | Definition | Advance LAST_RUN? |
|----------|------------|-------------------|
| **Source-health pilot** | First investigation of a source — metadata discovery, accessibility check, no intel_items | Yes, to document the investigation happened |
| **Successful extraction run** | Monitor produced normalized intel_items, dedupe updated, YAML valid | Yes |
| **Manual-review-only run** | Items extracted but require human review before output | Yes, with note |
| **Failed run** | Source unreachable, parser broken, no useful output | No — document failure, do not advance |
| **Catch-up run (multiple sources)** | Running 2+ daily sources in one session | Advance once for the session |

---

## 10. Catch-Up Rules

| Condition | Action |
|-----------|--------|
| 1-2 days missed (daily) | Run 1 daily source per session until caught up |
| 3+ days missed (daily) | Run 2 daily sources per session until caught up |
| 7-10 days since last weekly | Run weekly work before starting new daily items |
| 11+ days since last weekly | Run a dedicated weekly catch-up session |
| 30-40 days since last monthly | Schedule monthly session; defer daily/weekly |
| 41+ days since last monthly | Prioritize monthly before anything else |
| Both daily and weekly overdue | Run daily catch-up first (2 sources), then weekly |
