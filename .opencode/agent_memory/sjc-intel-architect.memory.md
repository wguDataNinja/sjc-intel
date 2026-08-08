# sjc-intel-architect Memory

Last updated: 2026-08-07

## Current state

- SJC_Intel is supervised and file-first. Canonical corpus/review authority is
  local; no scheduler or autonomous publication exists.
- `CURRENT_BRIEF.md` is generated from durable adaptive state and now also
  summarizes the publication-policy exception counts.
- Task 26 completed the supervised weekly adaptive cycle. Its final run is
  `SJC-LIVE-20260807-2604`; current adaptive proposals are resolved there.

## Publication

- `docs/PUBLICATION_POLICY.md` is the authority for default publication.
  `scripts/publication_policy.py` derives `AUTO_PUBLISHABLE`,
  `NEEDS_HUMAN_REVIEW`, `NEEDS_MORE_RESEARCH`, or `EXCLUDE`; it never mutates
  evidence, review state, or decisions.
- Individual files in `data/publication_decisions/` are human exceptions,
  corrections, and withdrawals rather than a per-item default gate.
- Local `SJC-REL-2026-08-002` contains seven policy-selected items and records
  `SJC-REL-2026-08-001` as rollback predecessor. It was generated locally;
  no commit, push, or GitHub Pages deployment occurred in Task 27.
- The next corpus-expansion work is not bulk publication: resolve the policy
  exceptions by adding concrete relevance/canonical/source evidence for the
  high-value historical candidates from Task 20.

## Operations

- Weekly runner remains declared but disabled in `deploy/sjc-weekly-task.yaml`.
  Ivy scheduler activation remains a separate privileged gate.
- Keep live runs, source promotion, review-state changes, and deployment under
  explicit scope. Never turn `pending_review` into `verified` by policy.

## Latest evidence

- `reports/26-codex-v1-finish-and-publish.md`
- `reports/27-publication-policy-defaults.md`
- `logs/agents/sjc-intel-architect/2026-08-07_publication-policy-defaults.md`
