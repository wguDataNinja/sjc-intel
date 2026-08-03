# SJC-2026-08-02-04 — Daily Cadence Catch-Up Runs

- **Task ID:** `04-daily-cadence-catchup`
- **Session:** `session-2026-08-02` (resume)
- **Repository:** `/Users/buddy/projects/sjc_intel`
- **Branch:** `master` (post-closeout state)
- **Agent role:** OpenCode (implementation) — bounded cadence execution
- **Result report:** `reports/04-daily-cadence-catchup.md` (singular report)

## Objective

Execute the overdue daily cadence catch-up (LAST_RUN 2026-07-04, ~29 days
overdue). Per `docs/cadence.md` and `reports/01-resume-roadmap-assessment.md`,
run the daily sources (2 sources per session) that have been idle, capturing
new intel items for the gap period 2026-07-05 → 2026-08-02.

## Current accepted state (verified 2026-08-02)

- Daily cadence LAST_RUN: `2026-07-04T10:00:00Z` — **~29 days overdue**
- 6 daily sources ready: `sjc_utility_department` (extractor exists),
  `sjc_county_news`, `sjso_news_stories`, `sjc_emergency_management`
  (seasonal Jun-Nov), `sjc_nbor_public_notices` (extractor `scripts/extract_nbor.py`),
  `st_johns_citizen` (context scan)
- Live-monitor gate: **explicitly authorized by Buddy 2026-08-02** for this
  cadence catch-up
- Post-T1: dedupe index 120 entries, review queue 137 entries (48 pending)

## Roadmap authority

- `docs/cadence.md` — daily cadence rules + live-monitor gate + run patterns
- `reports/01-resume-roadmap-assessment.md` — cadence overdue findings;
  "run 2 sources/session until caught up"
- `reports/02-july-artifact-disposition.md` — prior state

## Scope — what to do

1. **Run 2 daily sources this session** (select by importance + extractor
   readiness; suggest: `sjc_nbor_public_notices` + `sjc_utility_department`
   first — both have extractors). Use each source's documented monitor spec
   and run pattern (`docs/monitor_specs/`).
2. **Capture new items** into `data/intel_items/<YYYY-MM-DD>/` per repo
   convention, with correct schema (canonical intel_item schema).
3. **Absorb into dedupe index + review queue** using the repo's rebuild
   scripts (`scripts/rebuild_dedupe_index.py`, `scripts/build_review_queue.py`).
4. **Update cadence markers**: `logs/runs/daily/LAST_RUN` + run log
   (this task IS authorized to update daily cadence state).
5. **Update data inventory** if the repo convention requires
   (`docs/data_inventory/`).
6. **Write the result report** to `reports/04-daily-cadence-catchup.md`.

## Exclusions (do not)

- Do NOT run more than 2 sources this session (cadence rule; remaining 4 in a
  follow-up task).
- Do NOT touch monthly/weekly cadence markers (separate cadences).
- Do NOT promote any review-queue item; new items land `pending_review`
  (or the repo's default intake status).
- Do NOT auto-verify article content beyond what the extractor captures.
- Do NOT modify ROADMAP.md, source registry, schemas, or taxonomy.
- Do NOT `git add .` — explicit paths only; commit curated data per repo
  convention (or leave uncommitted + report, per convention).
- Do NOT run `st_johns_citizen` if its monitor spec marks it context-scan
  only and requires special handling — note and defer if so.

## Files to inspect

- `docs/cadence.md` (daily rules, gate, patterns), `docs/monitor_specs/`
  (both source specs)
- `scripts/extract_nbor.py`, utility extractor if present,
  `scripts/rebuild_dedupe_index.py`, `scripts/build_review_queue.py`
- `registry/sources.yaml` (both sources), `data/intel_items/` (convention),
  `logs/runs/daily/LAST_RUN` + last run log
- `data/index/prior_items.yaml`, `data/review_queue/`
- `reports/01-resume-roadmap-assessment.md`, `reports/02-july-artifact-disposition.md`

## Validation

- `python3 -m pytest tests/ -q` + `python3 scripts/validate.py` — must stay
  green
- Captured items parse + dedupe correctly (no dupes vs existing 120)
- LAST_RUN updated to this session's timestamp
- Report: per-source items captured, dedupe/queue deltas, marker update,
  remaining sources for next session

## Stop conditions

- A source's fetch fails entirely (network/403) → stop that source, report,
  continue the other.
- Extractor produces malformed items → stop, report, do not force-commit.
- Any captured item looks like private/sensitive data beyond public records →
  stop, report, keep pending_review.
- Dedupe/queue rebuild breaks existing entries → stop, report.

## Execution exception (§3.5f) — recorded 2026-08-02

- **Designated executor unavailable:** OpenCode CLI (`opencode run --agent build`,
  variants medium ×2 + tiny ×1) wedged on this task three consecutive times —
  zero agent output, zero disk changes, no network activity after start. CLI
  smoke test likewise produced no model response. Executor is demonstrably
  unavailable for this task in the current environment.
- **Exception granted:** Hermes executes this bounded mechanical task directly
  per HERMES_AGENT_CONTRACT §3.5f exception policy: no suitable separate
  executor is available; additional review control = every command + exact
  output recorded in this packet's result report; no commits (SJC policy:
  leave uncommitted + report, per repo convention); no publication or approval
  gate bypassed — Buddy reviews the report.
- **Scope unchanged:** exactly what this packet specifies. No novel code;
  existing scripts only.

## Tooling constraints (non-negotiable)

- The NBOR capture for 2026-08-02 ALREADY EXISTS on disk
  (`data/intel_items/2026-08-02/sjc_nbor_public_notices.yaml`, 25 items,
  validated). DO NOT re-fetch NBOR — absorb the existing capture into the
  dedupe index and review queue.
- Utility fetch: use `curl --max-time 30` (or equivalent bounded timeout).
  The monitor-spec URL is `https://www.sjcfl.us/departments/utility-department/`
  (verified HTTP 200 2026-08-02). If the fetch fails or times out, record the
  failure in the report and CONTINUE — do not retry indefinitely.
- One simple command per terminal call. No compound commands spanning
  multiple external paths. No `/tmp` or external scratch — write any scratch
  inside the repository worktree.
- No servers, daemons, or background processes.
- If any probe is blocked, record the block in the report and continue.
- The result report MUST be written to `reports/04-daily-cadence-catchup.md`
  regardless of what failed.

## Result-report requirements

One report at `reports/04-daily-cadence-catchup.md`: task identity; starting
Git state; sources run + items captured (with IDs); dedupe/queue deltas;
LAST_RUN + run-log update; validation results; files changed; commit SHA (if
any); remaining sources for the next session; unresolved issues; final status.

## Candidate next tasks (propose, don't create)

1. Remaining 4 daily sources (next catch-up session).
2. Weekly cadence catch-up (also 29d overdue).
3. Evidence required before either begins.
