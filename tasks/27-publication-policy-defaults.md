# Task 27 — Publication Policy Defaults and Exception-Based Release Selection

**Authority:** Direct Buddy instruction, 2026-08-07.

## Objective

Replace the item-by-item publication-membership default with a documented,
deterministic policy classifier. Verified, public-source, resident-relevant,
low-sensitivity items should become eligible by default; sensitive, weak,
ambiguous, or non-resident-relevant items must remain exceptions.

## Scope

- Add the public publication-policy authority and reconcile the existing
  release/review contracts.
- Implement a side-effect-free classifier used by the release selector.
- Preserve existing individual publication decisions as human overrides and
  withdrawal controls.
- Produce a local policy-classification inventory and regenerate only the
  local static artifacts that pass the new policy.
- Add regression tests and an operator-facing current-brief exception summary.

## Boundaries

- No source collection, monitor run, registry promotion, review-queue
  promotion, deployment, push, commit, or external publishing.
- Do not turn `pending_review` into `verified` merely because a previous
  narrative report found it interesting.
- Do not auto-publish crime, public-safety incidents, allegations, minors,
  personally sensitive material, weak/stale/conflicting evidence, or raw
  operational metadata.

## Validation

- Focused publication and static-release tests, full test suite, corpus and
  general validators, deterministic selector check, static-site check, and
  `git diff --check`.
