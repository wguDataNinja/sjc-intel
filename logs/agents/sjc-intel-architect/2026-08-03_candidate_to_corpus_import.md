# Agent Log — 2026-08-03 candidate-to-corpus-import (Task 13)

## Session

`sjc-intel-architect` executed `tasks/13-candidate-to-corpus-import.md` in a
fresh OpenCode session. Local and non-privileged: no VPS, PostgreSQL, Ivy
state, systemd, timers, publish, promotion, commit, or push.

## Files read (authority)

README_INTERNAL.md, AGENTS.md, ROADMAP.md, VPS_ROADMAP.md,
docs/VPS_CONTINUITY.md, docs/publication_release_contract.md,
docs/weekly_operational_contract.md, tasks/README.md, reports/README.md,
reports/10, 11, 12, logs/runs/daily/2026-08-02_daily_cadence_catchup_2.md,
reports/06-daily-cadence-catchup-2.md, registry/source_candidates.yaml,
registry/sources.yaml, scripts/{rebuild_dedupe_index,update_dedupe_index,
build_review_queue,extract_nbor,bundle_build,bundle_verify,bundle_common,
bundle_import}.py, schemas/intel_item.schema.yaml, tests/conftest.py.

## Key findings

- Git: master @ 1be2ade == origin/master (0/0). Task 12 outputs present
  (untracked). No data/incoming, data/receipts, or runtime/weekly existed.
- Sheriff's Office discovery identified: `https://www.sjso.org/feed/` — valid
  RSS 2.0 feed, first used 2026-08-02 (run log `2026-08-02_daily_cadence_catchup_2.md`
  + report 06 §4.4; source_event EVT-SJSO-20260802-0001 type rss_snapshot).
  Bounded re-verification 2026-08-03T23:19:48Z: HTTP 200,
  application/rss+xml, 65799 bytes, sha256 42d340c9…, valid RSS 2.0 XML,
  no SSL error. Buddy's "SSL" shorthand not confirmed; it is an RSS discovery.
- Disposition: propose_monitor_update / replacement endpoint for canonical
  `sjso_news_stories` (NOT a new source; CAND-SRC-0011 already marked
  duplicate_of_canonical).
- Task 12 foundation classification: bundle build/verify/import + manifest +
  checksums + receipt + sample fixture + tests = implemented and tested;
  workspace-safe runner = missing; extractor workspace mode = missing;
  candidate acceptance = missing; proposal review = missing.

## Work performed

- Schemas: `schemas/intel_candidate.schema.yaml`, `schemas/source_proposal.schema.yaml`.
- `scripts/extract_nbor.py`: added `--workspace <dir>` mode + `candidate_items()`
  + `write_workspace_output()` (no corpus writes, no fixture overwrite).
- `scripts/run_weekly.py`: bounded local weekly runner (workspace-safe,
  runtime/weekly/{run_id}/, NBOR monitor, offline fixture mode, duplicate-run
  prevention, meaningful exit codes, optional --bundle-out).
- `scripts/import_weekly_bundle.py`: staging-only importer (full verification,
  path-traversal/malformed-JSON/candidate-schema checks, idempotent replay,
  conflict detection, --preview, receipt at data/incoming/{run_id}/receipt.json
  + ack mirror data/receipts/).
- `scripts/accept_candidates.py`: human-gated accept/reject/defer with dry-run,
  dedupe preview, corpus append (review_status pending_review), origin
  provenance, decision records, idempotent, reuses existing dedupe/queue
  rebuild tooling.
- `scripts/review_source_proposals.py`: human proposal-review records,
  never writes registry/sources.yaml.
- Tests: test_run_weekly.py (5), test_import_weekly.py (7), test_accept_candidates.py (6).
  Updated fixture candidate to the new schema; regenerated sample_bundle.
- Proof: SJSO RSS proposal through the real chain — workspace → bundle → verify
  (PASS) → import into data/incoming/SJC-WK-20260803-0001 → receipt → replay
  idempotent → human review `propose_monitor_update` →
  registry/sources.yaml sha unchanged.
- Docs: docs/weekly_operator_guide.md; ROADMAP §3E-G3 + §8 updated;
  weekly contract header links operator guide + schemas.

## Design decisions / friction

- Reconciled proposal identity field: Task 12 contract said `candidate_id`;
  Task 13 uses `proposal_id`. Made `proposal_id` canonical (schema, fixture,
  contract §4.1 updated).
- Candidate schema required fields caused the Task 12 fixture candidate to be
  invalid; updated fixture (added summary/discovered_at) and regenerated bundle.
- accept_candidates drops `status`/`outcome` from accepted corpus records so
  accepted items read as corpus items (review_status pending_review).
- Task 12 receipt path (data/receipts) vs Task 13 suggested colocated receipt:
  wrote both (colocated per-bundle + canonical ack mirror).
- raw/ captures stay workspace-local per bundle contract §7.1 (bundle has no
  raw/ class); smoke test confirmed.
- build_review_queue schema vs intel_item.schema review_status enum differ
  (pre-existing); accepted items use pending_review which both accept.

## Validation

pytest 138 passed (120 pre-existing + 18 new). validate.py ALL PASSED;
portability_check PASS; git diff --check clean. Proof: bundle_verify PASS,
import PASS + idempotent replay, review recorded, registry sha unchanged.

## Files changed (this session)

Added: schemas/{intel_candidate,source_proposal}.schema.yaml,
scripts/{run_weekly,import_weekly_bundle,accept_candidates,review_source_proposals}.py,
tests/{test_run_weekly,test_import_weekly,test_accept_candidates}.py,
docs/weekly_operator_guide.md, data/incoming/SJC-WK-20260803-0001 (proof),
data/receipts/SJC-WK-20260803-0001.receipt.json.
Modified: scripts/extract_nbor.py, ROADMAP.md, docs/weekly_operational_contract.md,
tests/fixtures/bundle_workspace/*, tests/fixtures/sample_bundle/*.
Nothing committed/pushed. Pre-existing dirty data files untouched.
