# Task 13 — Candidate-to-Corpus Import and First Source-Proposal Proof

**Task identity:** 13-candidate-to-corpus-import.md
**Date:** 2026-08-03
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Final status:** COMPLETE

## 1. Executive result

The first safe candidate-to-corpus path for weekly VPS/Hermes outputs is fully
implemented and validated, and the Sheriff's Office RSS feed discovery has
passed through the new source-proposal workflow end-to-end without any
automatic promotion.

Delivered:

- **Workspace-safe weekly execution:** `scripts/run_weekly.py` (bounded local
  weekly runner into `runtime/weekly/{run_id}/`) plus a `--workspace <dir>`
  mode in `scripts/extract_nbor.py`. Weekly runs never write the authoritative
  corpus by default — proven by tests.
- **Bundle ingestion:** `scripts/import_weekly_bundle.py` — validates manifest,
  checksums, completeness, producing revision metadata; rejects path traversal,
  undeclared files, malformed JSON, and invalid candidates; stages idempotently
  into `data/incoming/{run_id}/`; writes a durable receipt
  (`data/incoming/{run_id}/receipt.json` + acknowledgement mirror
  `data/receipts/{run_id}.receipt.json`); never writes corpus or promotes
  proposals.
- **Human-gated acceptance:** `scripts/accept_candidates.py` — explicit
  accept/reject/defer with dry-run plan, dedupe preview, corpus append as
  `review_status: pending_review` (never verified/published), origin-run
  provenance, auditable decision records, idempotent and replay-safe, reusing
  the existing dedupe-index and review-queue rebuild tooling.
- **Source-proposal proof:** `scripts/review_source_proposals.py` plus the real
  SJSO RSS discovery passed through workspace → bundle → verify → import →
  human review → no promotion (registry/sources.yaml sha unchanged).
- **Protections + docs:** candidate and proposal schemas, 18 new tests, an
  operator guide, and ROADMAP §3E-G3 updated so the next tasks need no
  rediscovery.

No source was promoted; no publication, deployment, PostgreSQL, systemd,
timer, Ivy, commit, or push occurred.

## 2. Starting Git and repository state

| Item | Observed |
|------|----------|
| Branch | `master` |
| HEAD | `1be2ade` (docs: define SilverLeaf publication and execution roadmap) |
| Working tree | Dirty (pre-existing, not from this task): `data/intel_items/2026-07-06/agentic_search_results.yaml`, `data/review_queue/queue.yaml`, `data/review_queue/summary.yaml`; plus untracked Task 12 outputs |
| Remotes | `origin https://github.com/wguDataNinja/sjc-intel.git` |
| origin/master | Exists, == local master (0 ahead / 0 behind) |
| Task 12 outputs | Present (untracked): bundle tooling, weekly contract, `prompts/sjc_weekly_ops_task.md` |
| Incoming/bundle/candidate dirs | `data/incoming/`, `data/receipts/`, `runtime/weekly/` did not exist; `runtime/` is gitignored |
| Tests before | 120 passed |
| Unfinished/conflicting prior implementation | None found; Task 12 tooling was coherent |

No unrelated changes were discarded and no history was rewritten. The GitHub
push is complete (no remaining Buddy action for the remote).

## 3. Task 12 foundation inspected

| Concern | Status |
|---------|--------|
| Weekly workspace layout | Documented only (`docs/weekly_operational_contract.md` §6); no executable runner |
| Bundle construction | Implemented and tested (`scripts/bundle_build.py`) |
| Manifest / checksums | Implemented and tested (`bundle_build.py`, `schemas/bundle_manifest.schema.yaml`) |
| Bundle validation | Implemented and tested (`scripts/bundle_verify.py`) |
| Incoming staging | Partial (`scripts/bundle_import.py` stages + writes Task-12 receipt) |
| Receipt generation / acknowledgment | Implemented (Task-12 path `data/receipts/`) — extended by Task 13 to add a colocated per-bundle receipt |
| Delayed-prune eligibility | Documented only (contract §7.7) — depends on a complete receipt (now produced) |
| Hermes task specification | Documented only (`prompts/sjc_weekly_ops_task.md`) |
| Source-proposal schema/examples | Missing — created `schemas/source_proposal.schema.yaml` |

Extensions were added on top of the Task 12 design rather than duplicated.
`bundle_import.py` remains available for the contract path; `import_weekly_bundle.py`
is the fuller Task 13 importer.

## 4. Sheriff's Office discovery identified

- **Source:** `sjso_news_stories` — St. Johns County Sheriff's Office.
- **URL:** `https://www.sjso.org/feed/`.
- **Feed type:** RSS 2.0.
- **Discovery artifact:** `logs/runs/daily/2026-08-02_daily_cadence_catchup_2.md`
  (meta-run log, task 06, 2026-08-02T14:55Z) and `reports/06-daily-cadence-catchup-2.md`
  §4.4; operationalized in `data/source_events/2026-08-02/sjso_news_stories.yaml`
  (`event_type: rss_snapshot`, `source_url: https://www.sjso.org/feed/`).
- **Prior evidence:** RSS used for the first time on 2026-08-02; parsed 7
  items; 1 new (SJC-SJSO-20260802-0001, 2026-06-22 jail-escape story); 6
  already captured. Prior captures were HTML listing scrapes.
- **Technical issue:** No SSL/TLS issue. Buddy's shorthand ("RSS, SSL, or
  feed-related") resolves to an RSS discovery; the verified fact is a valid
  RSS 2.0 feed with no SSL error. (The county, by contrast, has no RSS:
  `/feed/` and `/news/feed/` both 301 to homepage.)

## 5. Verified source/feed facts

Bounded read-only re-verification performed 2026-08-03T23:19:48Z (allowed by
task §3; no credentials; single GET; recorded with timestamp and provenance):

| Fact | Value |
|------|-------|
| URL | `https://www.sjso.org/feed/` |
| HTTP status | 200 |
| Content-Type | `application/rss+xml; charset=UTF-8` |
| Bytes | 65799 |
| sha256 | `42d340c905c1a19b739e726b34774cb24719399e4d826bbd559354d1fdb97b54` |
| Feed validity | RSS 2.0 XML (rss2 marker present) |
| SSL/TLS | No error observed |
| Duplicates existing SJSO source? | No — same canonical source (`sjso_news_stories`) |
| New endpoint for existing canonical? | Yes — `/feed/` is a new/alternate fetch endpoint; current `monitor_config.check_url` is the HTML listing `https://www.sjso.org/news-stories/` |

## 6. Recommended source disposition

**`propose_monitor_update` (replacement endpoint) for canonical
`sjso_news_stories`** — not a new source, not an alias, not a promotion.

- **Type:** new endpoint / monitor improvement for an existing canonical source.
- **Coverage gap:** single-fetch daily SJSO captures instead of HTML scrapes.
- **Authority level:** official. **Cadence:** daily. **Produces:** discrete
  intelligence items (RSS entries → intel candidates), not just health.
- **Next step:** in an approved source-review task, register `/feed/` as
  `monitor_config.check_url` with `check_type: rss`, and confirm feed items
  parse as discrete candidates for 4 consecutive weeks before any registry
  change.

## 7. Workspace-safe weekly execution implemented

- `scripts/extract_nbor.py --workspace <dir>` writes candidates/events/health/
  raw only into the workspace (no corpus writes, no fixture overwrite); default
  operator behavior is unchanged.
- `scripts/run_weekly.py` — the bounded local weekly runner:
  - stable `--run-id` or auto-generation (`SJC-WK-{YYYYMMDD}-{NNNN}`);
  - isolated workspace `runtime/weekly/{run_id}/` (run.json, source_health/,
    source_events/, intel_candidates/, source_proposals/, raw/, logs/);
  - explicit `--workspace-root`; never writes corpus paths by default;
  - runs only explicitly approved monitors (currently
    `sjc_nbor_public_notices`; unknown monitors exit 2);
  - captures source-health, source events, candidates, no-match/partial/
    failed/success outcomes;
  - records producing Git SHA, registry/config revisions, window, counts,
    failure summary, replay identity;
  - bounded logs; fail-safe; replayable; duplicate-run prevention (existing
    run_id rejected unless `--force`); meaningful exit codes (0/1/2/3);
  - optional `--bundle-out` assembles the versioned bundle via the Task 12
    builder.

Tests (`tests/test_run_weekly.py`) prove weekly execution does not mutate
`data/intel_items/`, `data/source_events/`, `data/review_queue/`,
`data/index/`, or `registry/sources.yaml`.

## 8. Bundle-import path implemented

`scripts/import_weekly_bundle.py <bundle-path>` (see operator guide §4):

- verifies manifest schema, all checksums, bundle completeness, and producing
  revision metadata (reuses `bundle_verify.run_checks`);
- rejects path traversal, undeclared files, malformed JSON, and invalid
  candidate/proposal records (fail-closed: no staging, no receipt);
- detects duplicate bundle IDs and replayed run IDs (idempotent replay returns
  the existing receipt; same run_id + different content is a conflict);
- stages idempotently into `data/incoming/{run_id}/`;
- never overwrites authoritative corpus files, never alters review status,
  never promotes source proposals;
- produces an import preview (`--preview`, no mutation);
- writes a durable receipt only after successful staging:
  `data/incoming/{run_id}/receipt.json` (colocated) + mirror
  `data/receipts/{run_id}.receipt.json` (acknowledgement path).
- Receipt includes bundle ID, run ID, checksum-set identity, import timestamp,
  importer Git SHA, files accepted, candidate/proposal/duplicate/rejected
  counts, validation result, staging location, acknowledgment eligibility.
- Prune eligibility: never marked until the complete receipt exists.

## 9. Candidate decision path implemented

`scripts/accept_candidates.py` (operator guide §6–7):

- requires explicit `--candidate-id` selection and explicit `--decision`
  (accept/reject/defer) + `--reviewer`;
- `--dry-run` prints a full plan (target corpus file, dedupe status) before any
  mutation;
- validates the candidate again and checks dedupe against the authoritative
  index;
- accept: writes the record to `data/intel_items/{date}/{source}.yaml` with
  `review_status: pending_review` (never verified/published), assigns stable
  item IDs per repository conventions (reusing the candidate id when unique),
  preserves evidence and source URL, records `_origin_run_id`,
  `_origin_bundle_id`, `_reviewer`, `_imported_at`; rebuilds the dedupe index
  and review queue using the existing tooling (which preserves prior decisions);
- reject/defer: writes an auditable decision record, preserves all evidence,
  writes nothing to the corpus;
- idempotent and replay-safe; already-accepted candidates are reported cleanly;
  never accepts all by default; source proposals are never promoted by this
  command.

## 10. Source-proposal proof

The verified Sheriff's Office discovery passed through the new workflow
(proposal `PROP-public_safety-0001`):

1. **Repository evidence** — run log + report 06 (2026-08-02) + bounded
   re-verification (2026-08-03T23:19:48Z) recorded in the proposal.
2. **Proposal created** — `runtime/weekly/SJC-WK-20260803-0001/source_proposals/proposals.json`
   with the full field set (proposal_id, run_id, discovered_at, source_name,
   URL, feed_type RSS 2.0, current_source_relationship, source_family, authority
   official, geographic relevance, coverage gap, evidence, technical_issue,
   discovered_through, relevance_rationale, recommended_disposition
   `monitor_update`, confidence high, review_status candidate, human_review_status
   pending_review, next_verification_step).
3. **Bundle / incoming staging** — `bundle_build.py` → `bundle_verify.py` PASS →
   `import_weekly_bundle.py` staged into `data/incoming/SJC-WK-20260803-0001/`,
   receipt + ack mirror written; replay idempotent.
4. **Validation** — full import validation PASS (candidates 0, proposals 1).
5. **Human review record** — `review_source_proposals.py` recorded
   `decision: propose_monitor_update`, `reviewer: buddy`,
   `promotion_performed: false` at
   `data/incoming/SJC-WK-20260803-0001/proposal_reviews/PROP-public_safety-0001.yaml`.
6. **No automatic promotion** — `registry/sources.yaml` sha256 verified
   unchanged before/after.

The workflow reached a clear, reviewable, non-“new source” disposition without
touching the canonical registry.

## 11. Dedupe and review-state protections

Tests (`tests/test_accept_candidates.py`, `tests/test_import_weekly.py`) prove:

- duplicate candidate imports do not create duplicate staged records
  (idempotent replay);
- replaying the same bundle is safe (identical staged output, existing receipt);
- accepting one candidate does not reset unrelated review states;
- rebuilding the review queue preserves prior decisions (a pre-existing
  `verified` entry with reviewer stays `verified` while the new accepted item
  is `pending_review`);
- rejected candidates remain auditable (decision record + evidence retained);
- deferred source proposals remain auditable (review record, no deletion);
- accepted candidates retain origin run, bundle, evidence, and source URL;
- source proposals cannot enter the canonical registry through the importer or
  reviewer (test module asserts `registry/sources.yaml` is byte-identical
  before/after; importer stages only under `data/incoming/`);
- public release eligibility remains false: accepted records are
  `review_status: pending_review` — `verified` and publication are separate
  gates per the publication contract.

## 12. Files changed

Added:

- `schemas/intel_candidate.schema.yaml`, `schemas/source_proposal.schema.yaml`
- `scripts/run_weekly.py`, `scripts/import_weekly_bundle.py`,
  `scripts/accept_candidates.py`, `scripts/review_source_proposals.py`
- `tests/test_run_weekly.py`, `tests/test_import_weekly.py`,
  `tests/test_accept_candidates.py`
- `docs/weekly_operator_guide.md`
- Proof artifacts (staged + receipts): `data/incoming/SJC-WK-20260803-0001/`,
  `data/receipts/SJC-WK-20260803-0001.receipt.json`
- Proof workspace/bundle (gitignored `runtime/`):
  `runtime/weekly/SJC-WK-20260803-0001/`, `runtime/weekly/bundles/SJC-WK-20260803-0001/`

Modified:

- `scripts/extract_nbor.py` (workspace mode)
- `ROADMAP.md` (§3E-G3, §8)
- `docs/weekly_operational_contract.md` (header links; §4.1 proposal_id)
- `tests/fixtures/bundle_workspace/*`, `tests/fixtures/sample_bundle/*`
  (candidate schema-complete; regenerated)

Pre-existing dirty/untracked files (data + Task 12 outputs) preserved
untouched. Nothing committed or pushed.

## 13. Validation commands and results

```
python3 -m pytest tests/ -v        → PASS, 138 passed (120 pre-existing + 18 new)
python3 scripts/validate.py        → PASS — ALL PASSED
python3 scripts/portability_check.py → PASS
git diff --check                   → clean
git status --short                 → only intended new files + pre-existing dirty files
git branch --show-current          → master
git remote -v                      → origin https://github.com/wguDataNinja/sjc-intel.git
```

Targeted checks (all covered by the suite or the proof): workspace-safe
execution; bundle validation; checksum failure; duplicate bundle import; path
traversal rejection; candidate staging; dry-run acceptance; accepted candidate
dedupe; review-state preservation; source-proposal non-promotion; and the
Sheriff's Office proposal proof. No network was required for the test suite
(the one bounded feed GET was the proof verification, recorded in §5).

## 14. Operator workflow

`docs/weekly_operator_guide.md` documents: running a weekly local workspace;
building a bundle; importing a bundle; inspecting candidates; accepting,
rejecting, or deferring a candidate; reviewing source proposals; generating a
receipt; replaying a bundle; and recovering from a failed import. It is linked
from the weekly operational contract and the roadmap. No second roadmap was
created.

## 15. Remaining privileged VPS work

- Execute the privileged packet from report 12 §11 / this report: exact-SHA
  deployment (`1be2ade` refreshed at admission), directories/permissions, venv +
  deps, disabled weekly timer, lock, capacity evidence, transfer route + ack
  observation (`data/receipts/` mirror), delayed-prune procedure, rollback.
- Add the SJSO `/feed/` monitor to `run_weekly.py`'s monitor registry (medium
  task, not privileged) before or during the shadow run, per the approved
  proposal disposition.
- Refresh Ivy CONTROL.md (privileged cross-repo).

## 16. Remaining Buddy decisions

- Approve the source-proposal disposition (`propose_monitor_update` for
  `sjso_news_stories` /feed/) or the alternative decision.
- Approve the §3E-G1 VPS admission packet when ready.
- Editorial/publication gates remain separate and unaffected.

## 17. Candidate next tasks

- **extract-bcc-workspace-mode.md** (medium, non-privileged): add the
  workspace-output mode to `scripts/extract_bcc_agenda.py`.
- **14-vps-admission-packet.md** (§3E-G1, privileged).
- **15-shadow-run-proof.md** (§3E-G2, privileged).
- Optional **16-weekly-contract-docs-check.md**.

## 18. Risks and unresolved issues

- **`extract_bcc_agenda.py` still writes corpus paths** — flagged as a medium
  follow-up before BCC becomes a VPS-capable monitor.
- **SJSO feed parse implementation** is not yet in `run_weekly.py`; the proposal
  recommends a 4-week parse proof in an approved source-review task before the
  registry `monitor_config.check_url` change.
- **Pre-existing schema enum divergence** (intel_item.schema vs
  build_review_queue CANONICAL_STATUSES) is unchanged; accepted items use
  `pending_review`, which both accept.
- **Task 12 vs Task 13 receipt location** reconciled by writing both the
  colocated bundle receipt and the canonical ack mirror; documented in the
  operator guide.
- **`runtime/` is gitignored** — proof workspace/bundle artifacts there are
  local; the durable proof record lives in `data/incoming/` + `data/receipts/`
  (tracked).
- No SSL issue with the SJSO feed; Buddy's "SSL" shorthand is explicitly
  documented as not confirmed.

## 19. Final Git status

Branch `master`, HEAD `1be2ade`, origin/master == master. Working tree contains
only intended Task 13 files plus the pre-existing dirty data files and Task 12
outputs. Nothing was staged, committed, or pushed.

## 20. Final task status

| Area | Status |
|------|--------|
| Workspace-safe weekly execution | COMPLETE |
| Extractor workspace mode (NBOR) | COMPLETE |
| Bundle import (staging-only) | COMPLETE |
| Human-gated candidate acceptance | COMPLETE |
| Source-proposal review record | COMPLETE |
| SJSO proposal proof | COMPLETE (no promotion) |
| Dedupe/review-state protections | COMPLETE |
| Schemas (candidate + proposal) | COMPLETE |
| Operator docs + roadmap | COMPLETE |
| BCC workspace mode | READY_FOR_MEDIUM_AGENT |
| VPS admission / shadow run | BLOCKED (privileged) |

**Final status vocabulary:** COMPLETE — the local candidate-to-corpus path and
the source-proposal proof are fully implemented and validated; the repository
is ready for the privileged Ivy/VPS admission packet without further
candidate-flow architecture work.
