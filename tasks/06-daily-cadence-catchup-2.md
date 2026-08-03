# SJC-2026-08-02-06 — Daily Cadence Catch-Up Session 2 (County News + SJSO)

- **Task ID:** `06-daily-cadence-catchup-2`
- **Session:** `session-2026-08-02` (resume)
- **Repository:** `/Users/buddy/projects/sjc_intel`
- **Branch:** `master`
- **Agent role:** OpenCode (implementation) — bounded cadence execution
- **Result report:** `reports/06-daily-cadence-catchup-2.md`

## Objective

Continue the daily cadence catch-up (task 04 ran NBOR + utility; this is the
next 2-source session per `reports/01-resume-roadmap-assessment.md` — "run 2
sources/session until caught up"). Run `sjc_county_news` +
`sjso_news_stories`, capture new items for gap period 2026-07-05 →
2026-08-02, absorb into dedupe/queue, update markers.

## Current accepted state (verified 2026-08-02)

- Daily LAST_RUN: `2026-08-02T14:28:10Z` (updated by task 04)
- Monthly LAST_RUN: `2026-06-08T04:31:15Z` — **stale; T2 monthly closeout
  completed 09:00Z but marker never updated** (task 04 was scoped daily-only).
- Dedupe index: 139 entries; review queue: 162 entries.
- Prior captures of these sources (format reference):
  `data/intel_items/2026-06-03/sjc_county_news.yaml` (5 items),
  `data/intel_items/2026-06-03/sjso_news_stories.yaml` (4 items).

## Roadmap authority

- `docs/cadence.md` — daily cadence rules + live-monitor gate + run patterns
- `reports/01-resume-roadmap-assessment.md` — "run 2 sources/session until
  caught up"
- `reports/04-daily-cadence-catchup.md` — prior session result

## Scope — what to do

1. **Run 2 daily sources this session:**
   - `sjc_county_news` — `https://www.sjcfl.us/news/` (WordPress; NO RSS —
     both `/feed/` and `/news/feed/` 301-redirect to homepage; verified
     2026-08-02). The news page currently lists exactly 4 articles:
     1. `county-road-16a-closures-detours-three-july-august-weekends`
     2. `dailys-withdraws-comp-plan-amendment-application-august-4-bcc-agenda`
     3. `sea-community-help-resource-center-opens-to-rural-sjc`
     4. `clerks-office-new-service-center-2026`
     Fetch each article page (or the listing page) and capture per the
     prior format template at
     `data/intel_items/2026-06-03/sjc_county_news.yaml` (monitor_cycle
     wrapper). Registry `check_url` + `item_url_pattern` at
     `registry/sources.yaml` lines ~22-59.
   - `sjso_news_stories` — **USE THE RSS FEED**: `https://www.sjso.org/feed/`
     (verified HTTP 200, valid RSS 2.0 XML, 2026-08-02). One fetch + XML
     parse (item titles, links, pubDates) — do NOT scrape the HTML listing.
     Capture items newer than the last capture (2026-06-03, 4 items) per
     the prior format template at
     `data/intel_items/2026-06-03/sjso_news_stories.yaml`.
   - Neither has an extractor script — manual fetch + parse per the prior
     capture format (monitor_cycle wrapper: source_id, checked_at,
     http_status, items_extracted, new_items, duplicates_skipped, items[]).
2. **Capture new items** into `data/intel_items/<YYYY-MM-DD>/` per the
   prior format. Use item_id prefixes `SJC-CN-YYYYMMDD-NNNN` (county news)
   and `SJC-SJSO-YYYYMMDD-NNNN` (sjso).
3. **Absorb into dedupe index + review queue** using
   `scripts/rebuild_dedupe_index.py` + `scripts/build_review_queue.py`.
4. **Update cadence markers** (authorized for BOTH in this task):
   - `logs/runs/daily/LAST_RUN` → this session's timestamp
   - `logs/runs/monthly/LAST_RUN` → `2026-08-02T09:00:00Z` (T2 monthly
     closeout completion — this is the explicit authorization to fix the
     stale marker, previously excluded from task 04)
   - Write one run log: `logs/runs/daily/2026-08-02_daily_cadence_catchup_2.md`
5. **Write the result report** to `reports/06-daily-cadence-catchup-2.md`.

## Do Not

- Do NOT run more than these 2 sources this session.
- Do NOT run `st_johns_citizen` (context-scan-only local media source —
  special handling required; note and defer per task 04 convention).
- Do NOT touch `logs/runs/weekly/LAST_RUN` (weekly cadence is a separate
  task).
- Do NOT promote any review-queue item; new items land `pending_review`.
- Do NOT auto-verify article content beyond what the fetch captures.
- Do NOT modify ROADMAP.md, source registry, schemas, or taxonomy.
- Do NOT `git add .` — explicit paths only; leave uncommitted + report per
  repo convention (SJC policy: no commit unless Buddy/Git Steward instructs).
- Do NOT copy article content wholesale from `sjcitizen.com` or any source —
  summaries/excerpts only (public-record fair use per repo convention).

## Files to inspect

- `registry/sources.yaml` (both sources, lines ~22-97)
- `data/intel_items/2026-06-03/sjc_county_news.yaml` + `sjso_news_stories.yaml`
  (format templates)
- `data/index/prior_items.yaml`, `data/review_queue/queue.yaml`
- `logs/runs/daily/LAST_RUN`, `logs/runs/monthly/LAST_RUN`
- `reports/01-resume-roadmap-assessment.md`, `reports/04-daily-cadence-catchup.md`

## Tooling constraints (non-negotiable)

- Use `curl --max-time 30` for each fetch. If a fetch fails or times out,
  record the failure in the report and CONTINUE — do not retry indefinitely.
- One simple command per terminal call. No compound commands spanning
  multiple external paths. No `/tmp` or external scratch — write any scratch
  inside the repository worktree.
- No servers, daemons, or background processes.
- If any probe is blocked, record the block in the report and continue.
- The result report MUST be written to `reports/06-daily-cadence-catchup-2.md`
  regardless of what failed.

## Validation

- `python3 -m pytest tests/ -q` + `python3 scripts/validate.py` — must stay
  green (baseline: 109 passed / ALL PASSED).
- Captured items parse + dedupe correctly (no dupes vs existing 139).
- LAST_RUN markers updated (daily → now, monthly → 2026-08-02T09:00:00Z).
- Report: per-source items captured, dedupe/queue deltas, marker updates,
  remaining sources for next session.

## Stop conditions

- A source's fetch fails entirely (network/403) → stop that source, report,
  continue the other.
- Extractor produces malformed items → stop, report, do not force-commit.
- Any captured item looks like private/sensitive data beyond public records →
  stop, report, keep pending_review.
- Dedupe/queue rebuild breaks existing entries → stop, report.

## Result-report requirements

One report at `reports/06-daily-cadence-catchup-2.md`: task identity;
starting Git state; sources run + items captured (with IDs); dedupe/queue
deltas; LAST_RUN updates (daily + monthly); run-log path; validation
results; files changed; remaining sources for the next session; unresolved
issues; final status.

## Candidate next tasks (propose, don't create)

1. `sjc_emergency_management` (seasonal Jun-Nov, do-not-auto-publish) +
   `st_johns_citizen` (context-scan, needs special handling) — next session.
2. Weekly cadence catch-up (29d overdue) — separate task.
3. SilverLeaf DIR-001 registry + DIR-002 three-lane architecture — STOP GATE
   (high-reasoning, Buddy/Codex).
