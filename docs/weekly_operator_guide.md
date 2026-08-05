# SJC_Intel — Weekly Operations Operator Guide

**Status:** Concise operator reference for the candidate-to-corpus weekly path.
**Authority:** `docs/weekly_operational_contract.md` (contract), `ROADMAP.md` §3E.
**Last reconciled:** 2026-08-03 (Task 13).

All commands run from the repository root. None of them publish, promote
sources, or enable schedules.

## Lifecycle

```
weekly run workspace            scripts/run_weekly.py
    ↓
versioned transfer bundle        scripts/bundle_build.py (or run_weekly --bundle-out)
    ↓
Mac incoming staging             scripts/import_weekly_bundle.py
    ↓
validation + dedupe preview      import --preview / bundle_verify
    ↓
human decision                   scripts/accept_candidates.py (candidates)
                                 scripts/review_source_proposals.py (proposals)
    ↓
review queue                     rebuild via existing dedupe/queue tooling
```

## 1. Run a weekly local workspace (workspace-safe)

```bash
python3 scripts/run_weekly.py \
  --run-id SJC-WK-20260803-0001 \
  --monitor sjc_nbor_public_notices \
  --git-sha 1be2ade --registry-revision 1be2ade \
  --window-start 2026-08-03T10:00:00Z --window-end 2026-08-03T11:00:00Z
```

- Writes only under `runtime/weekly/{run_id}/` (run.json, source_health/,
  source_events/, intel_candidates/, source_proposals/, raw/, logs/).
- Never writes `data/intel_items/`, `data/source_events/`, `data/review_queue/`,
  `data/index/`, or `registry/`.
- Approved monitors: only `sjc_nbor_public_notices` in this foundation
  (`--monitor` repeatable; unknown monitors rejected with exit 2).
- Offline/test: add `--offline-html tests/fixtures/nbor_raw.html` (no network).
- Duplicate `--run-id` is rejected (exit ≠ 0); use `--force` only to replace a
  failed run.

## 2. Build a bundle

```bash
python3 scripts/run_weekly.py ... --bundle-out runtime/weekly/bundles
# produces runtime/weekly/bundles/{run_id}/ with manifest.json + checksums.sha256
```

Or build from any workspace:

```bash
python3 scripts/bundle_build.py --workspace <ws> --out <bundle-dir> \
  --run-id SJC-WK-... --git-sha <sha> --profile sjc-weekly-001 \
  --registry-revision <sha> --window-start <UTC> --window-end <UTC>
```

## 3. Verify a bundle

```bash
python3 scripts/bundle_verify.py --bundle <bundle-dir>
```

Exit 0 = PASS. This checks layout, manifest fields, run.json, file sizes and
sha256, unexpected files, checksums coverage, and replay identity.

## 4. Import a bundle (staging-only)

```bash
python3 scripts/import_weekly_bundle.py <bundle-dir> --git-sha 1be2ade
```

- Stages into `data/incoming/{run_id}/`; writes `data/incoming/{run_id}/receipt.json`
  and the acknowledgement mirror `data/receipts/{run_id}.receipt.json`.
- Rejects path traversal, undeclared files, malformed JSON, invalid candidates,
  checksum mismatches. Fails closed: no staging, no receipt on any failure.
- Replay of the same `run_id` is idempotent; same `run_id` with different
  content is a conflict.
- Preview without mutating: add `--preview`.
- Never writes the authoritative corpus and never promotes proposals.

## 5. Inspect candidates

```bash
python3 -c "import json; d=json.load(open('data/incoming/<run_id>/intel_candidates/<source>.json')); print(len(d['items']), 'candidates')"
```

Or review the import preview and `data/receipts/<run_id>.receipt.json` counts.

## 6. Accept one candidate (human-gated)

```bash
python3 scripts/accept_candidates.py --run-id <run_id> --candidate-id <item_id> \
  --decision accept --reviewer <name> [--notes ...] [--dry-run]
```

- `--dry-run` prints the plan (target corpus file, dedupe status) and mutates
  nothing.
- Accept writes the item to `data/intel_items/{date}/{source}.yaml` with
  `review_status: pending_review` (never verified/published), records the
  origin run/bundle, writes a decision record to
  `data/incoming/{run_id}/decisions/{item_id}.yaml`, and rebuilds dedupe +
  review queue using the existing tooling.
- Re-running is idempotent (`already_accepted`).

## 7. Reject or defer a candidate

```bash
python3 scripts/accept_candidates.py --run-id <run_id> --candidate-id <item_id> \
  --decision reject --reviewer <name> --notes "reason"
python3 scripts/accept_candidates.py --run-id <run_id> --candidate-id <item_id> \
  --decision defer --reviewer <name> --notes "pending follow-up"
```

Writes an auditable decision record under
`data/incoming/{run_id}/decisions/`; the staged candidate evidence is retained.

## 8. Review source proposals

```bash
python3 scripts/review_source_proposals.py --run-id <run_id> \
  --proposal-id <id> --decision propose_monitor_update --reviewer <name> \
  [--notes ...] [--dry-run]
```

Decisions: `propose_as_new_source`, `propose_as_alias`,
`propose_as_replacement_endpoint`, `propose_monitor_update`,
`reject_duplicate`, `defer_pending_verification`.

Records a review at `data/incoming/{run_id}/proposal_reviews/{proposal_id}.yaml`
with `promotion_performed: false`. **registry/sources.yaml is never written by
this command.** Source promotion remains the separate approved source-review
process.

## 9. Generate a receipt / acknowledge

Importing generates the receipt. The acknowledgement mirror
(`data/receipts/{run_id}.receipt.json`) is what the VPS producer observes for
prune eligibility. A bundle is never prune-eligible before this complete
receipt exists.

## 10. Replay a bundle safely

```bash
python3 scripts/import_weekly_bundle.py <bundle-dir> --git-sha <sha>
```

Same `run_id` → idempotent no-op returning the existing receipt. Identical
inputs → identical staged output (replay-safe). Never overwrites accepted
corpus records.

## 11. Recover from a failed import

- The importer fails closed: nothing is staged and no receipt is written.
- Fix the cause (missing file, checksum drift, malformed JSON, unsafe path,
  invalid candidate) at the producer, rebuild the bundle, re-import.
- A half-written staging dir (rare) can be removed manually
  (`rm -rf data/incoming/<run_id>`) and re-imported; it never touched corpus
  or review state.

## Safety rules

- No command here publishes, promotes, deploys, enables timers, or touches
  PostgreSQL/Ivy state.
- Rejected/deferred candidates and proposals are never deleted.
- `verify` ≠ `published`; `pending_review` is the acceptance ceiling for the
  candidate-to-corpus path.
