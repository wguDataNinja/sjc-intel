# SJC-2026-08-02-02 — Validate + Disposition July 2026 Artifacts

- **Task ID:** `02-july-artifact-disposition`
- **Session:** `session-2026-08-02` (resume)
- **Repository:** `/Users/buddy/projects/sjc_intel`
- **Branch:** `master` @ `f0d9b25` (clean tracked tree)
- **Agent role:** OpenCode (implementation) — **bounded execution, curated state**
- **Result report:** `reports/02-july-artifact-disposition.md` (singular report)

## Objective

Validate and disposition the uncommitted July 2026 SilverLeaf/search-discovery
artifacts (ROADMAP milestone 1), absorbing them into the repo's dedupe and
review infrastructure as curated state. This is the recommended next task from
`reports/01-resume-roadmap-assessment.md`.

## Current accepted state (verified 2026-08-02)

- Untracked: `data/intel_items/2026-07-06/agentic_search_results.yaml` (5
  candidates, all `review_status: pending_review`),
  `data/search_runs/2026-07-06/SRCH-20260706-0001.yaml`,
  `logs/agents/sjc-intel-architect/2026-07-06_agentic_search.md`
- `data/index/prior_items.yaml` rebuilt 2026-07-04 — does NOT include 07-06
- `data/review_queue/` rebuilt 2026-07-04 — 131 rows, no 07-06 candidates
- 109 tests + `scripts/validate.py` ALL PASSED on current state

## Roadmap authority

- `ROADMAP.md` (2026-07-28) — milestone 1: "validate and either commit or
  disposition the July 2026 SilverLeaf/search discovery artifacts"
- `reports/01-resume-roadmap-assessment.md` — findings + recommendation
- `BACKLOG.md` ENT-003/ENT-004 (tracked entities closeout)

## Scope — what to do

1. **Validate** the 07-06 artifact files: YAML parses, schema-consistent,
   cross-registry ID consistency (`python3 scripts/validate.py` + pytest).
2. **Absorb into infrastructure**: rebuild dedupe index and review queue so the
   5 candidates enter `data/review_queue/` with correct statuses.
3. **Sensitivity handling (MANDATORY):** the 3 high-sensitivity candidates
   (ICE-detainer/crime item, construction-site shooting with fatality, minor
   airlifted from amenities center) MUST remain `pending_review` — do NOT
   promote, do NOT mark verified, do NOT auto-resolve their failed fetch URLs.
4. **Record the search run**: ensure `data/search_runs/2026-07-06/SRCH-20260706-0001.yaml`
   is linked/indexed per repo convention.
5. **Commit** the curated state: the 3 data paths + any regenerated index/queue
   files, as ONE commit with explicit paths only (no `git add .`). Include the
   agent log if the repo convention tracks it.
6. **Update BACKLOG.md**: mark ENT-003 done (tracked_entities.yaml already
   holds the SilverLeaf set); note ENT-004 as the remaining doc task.
7. **Write the singular result report** to `reports/02-july-artifact-disposition.md`.

## Exclusions (do not)

- Do NOT promote any `pending_review` candidate to verified/canonical.
- Do NOT verify the 3 high-sensitivity URLs (they timed out in the source run;
  human verification required).
- Do NOT run live monitors, backfills, or any network fetch.
- Do NOT modify ROADMAP.md, source registry, schemas, or taxonomy.
- Do NOT touch `logs/runs/` or cadence LAST_RUN markers.
- Do NOT push (no remote configured).
- Do NOT `git add .` — explicit paths only.

## Files to inspect

- `data/intel_items/2026-07-06/agentic_search_results.yaml`
- `data/search_runs/2026-07-06/SRCH-20260706-0001.yaml`
- `logs/agents/sjc-intel-architect/2026-07-06_agentic_search.md`
- `scripts/rebuild_dedupe_index.py`, `scripts/build_review_queue.py`,
  `scripts/update_review_status.py`, `scripts/validate.py`
- `data/index/prior_items.yaml`, `data/review_queue/queue.yaml`,
  `data/review_queue/summary.yaml`
- `registry/tracked_entities.yaml` (for ENT-003 closeout)
- `BACKLOG.md` (ENT section)
- `reports/01-resume-roadmap-assessment.md` (prior findings)

## Validation

- `python3 -m pytest tests/ -q` — must stay green
- `python3 scripts/validate.py` — must report ALL PASSED after absorption
- `git status --short --branch` — only the intended files staged/committed
- Report: review queue now contains the 5 candidates with correct statuses;
  the 3 high-sensitivity items remain `pending_review`

## Stop conditions

- Any candidate cannot be parsed/validated → stop, report, do not force.
- Dedupe/queue rebuild breaks existing 07-04 items → stop, report.
- A high-sensitivity candidate would need promotion to proceed → stop.
- Secrets or private data discovered in the artifacts → stop, report.

## Result-report requirements

One report at `reports/02-july-artifact-disposition.md`: task identity;
starting Git state; validation results (before/after); how each of the 5
candidates was dispositioned (incl. explicit `pending_review` for the 3
high-sensitivity ones); files changed; commit SHA; BACKLOG update summary;
unresolved issues (failed URLs, Baptist Health entity unconfirmed); final
status (COMPLETE / PARTIAL / BLOCKED / HUMAN_DECISION_REQUIRED).

## Candidate next tasks (propose, don't create)

1. Recommended next (e.g., monthly cadence closeout — 55d overdue).
2. Alternative if blocked.
3. Evidence required before either can begin.
