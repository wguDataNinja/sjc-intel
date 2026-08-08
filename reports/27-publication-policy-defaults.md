# Task 27 — Publication Policy Defaults and Exception-Based Release Selection

**Date:** 2026-08-07
**Status:** COMPLETE — local artifacts generated; no deployment, commit, or push

## Outcome

SJC_Intel no longer requires a bespoke publication-decision record for every
ordinary item. `docs/PUBLICATION_POLICY.md` is now the authoritative policy,
and `scripts/publication_policy.py` deterministically classifies each canonical
record as `AUTO_PUBLISHABLE`, `NEEDS_HUMAN_REVIEW`, `NEEDS_MORE_RESEARCH`, or
`EXCLUDE`.

The local SilverLeaf Brief was regenerated as `SJC-REL-2026-08-002`: **7
items**, up from the four-item baseline. Its manifest records
`SJC-REL-2026-08-001` as the rollback predecessor. The public GitHub Pages
deployment remains unchanged because no commit, push, or deployment was
authorized or performed.

## Decisions made

1. **Policy, not a bulk status rewrite.** Classification is derived at release
   time from immutable evidence, registered source metadata, existing human
   decisions, and public-projection validation. No record was promoted from
   `pending_review` to `verified`.
2. **Default eligibility requires more than verification.** A record must be
   verified, public-source linked, official-source attributable, low
   sensitivity, public-safe, and have a concrete SilverLeaf/corridor/entity or
   structured countywide-household relevance signal. This stops a generic
   county notice feed from becoming the public product.
3. **Exceptions remain human-controlled.** Crime, public-safety incidents,
   minors, arrests, allegations, person-harm language, medium/high sensitivity,
   weak/conflicting/stale evidence, media-only claims, and vague local scope
   require human review. Reject/withdraw/defer records override the default.
4. **Time-bound notices expire from default eligibility.** Timely records over
   30 days old require an explicit context decision, preventing expired notices
   from silently becoming historical content.
5. **Historical context is supported, but not invented.** A durable official
   record can publish by default. The 10–14 strong historical candidates in
   Task 20 are not yet mass-added because most remain `pending_review` or need
   canonical merge/source confirmation. This is the correct evidence boundary,
   not a return to the old manual release gate.

## Current classification inventory

At the frozen 2026-08-07 release window:

| Classification | Count | Meaning |
|---|---:|---|
| `AUTO_PUBLISHABLE` | 7 | Included in the local policy release |
| `NEEDS_HUMAN_REVIEW` | 51 | Sensitive, stale, insufficiently localized, or otherwise exception cases |
| `NEEDS_MORE_RESEARCH` | 69 | Not yet `verified` or lacks required evidence |
| `EXCLUDE` | 40 | Withdrawn/rejected/duplicate/archival/legacy-disposition material |

The main exception groups are 38 high-volume agenda/notice records without a
concrete local scope, 7 stale timely records, and 69 pending-review records.
No sensitive incident was auto-published.

## Local release membership

`SJC-REL-2026-08-002` contains:

- `SJC-CN-20260626-0001` — county water-reclamation facility now serving.
- `SJC-CN-20260802-0001` — CR 16A closure (existing approved human decision).
- `SJC-EM-20260626-0001` — hurricane preparedness (existing approved human exception).
- `SJC-UTIL-20260603-0001` — active Phase III water shortage (existing approved exception).
- `SJC-UTIL-20260603-0003` — SR 207 water-reclamation facility approval.
- `SJC-UTIL-20260603-0004` — county water-testing laboratory improvement.
- `SJC-UTIL-20260603-0005` — water service-line material inventory (existing approved decision).

The release has 16 generated static routes. The older four-item release remains
in `site/data/releases/SJC-REL-2026-08-001/` for rollback.

## Implementation

- Added `docs/PUBLICATION_POLICY.md` and reconciled the release contract,
  human-review guide, static data contract, UI spec, README, backlog, and
  operator memory.
- Added `scripts/publication_policy.py` and changed the selector to report
  classification reasons rather than demand a decision file for every item.
- Kept `scripts/publication_decision.py` unchanged as the durable human
  exception/withdrawal mechanism.
- Added a release-builder `--prior-release-id` option so new manifests retain
  explicit rollback identity.
- Updated `CURRENT_BRIEF.md` to show only policy totals and exception queues.
- Regenerated local release/site artifacts and added regression coverage.

## Validation

- `python3 -m pytest tests/ -q` — **PASS, 300 tests**.
- `python3 scripts/validate.py` — **ALL PASSED**.
- `python3 scripts/validate_publication_corpus.py` — **PASS, 0 blocking
  errors** (321 pre-existing data-quality warnings remain visible).
- `python3 scripts/build_current_brief.py --check` — **PASS**.
- `python3 scripts/build_static_site.py --list-routes` — **PASS, 16 routes / 7
  items**.
- `git diff --check` — **PASS**.

## Next action

Use `PUB-004` to resolve the high-value Task 20 candidates in bounded groups:
first canonicalize and verify SilverLeaf K-8, CR 2209, SR 16/CR 210, and the
qualified retail/development context; then let the same policy classify the
result. Before public deployment, inspect the local seven-item diff and use the
normal explicit Git workflow/Pages deployment authorization.
