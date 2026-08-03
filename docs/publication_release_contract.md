# Publication and SilverLeaf Release Contract

**Status:** Authoritative supporting contract for ROADMAP.md §§3A–3D.  
**Owner:** Buddy for editorial/publication decisions; implementation follows approved task packets.  
**Last reconciled:** 2026-08-03.

## 1. Authority and state separation

Review determines whether an item is factually/editorially acceptable. Publication determines whether a reviewed item belongs in a named public release. They are separate.

- `review_status` remains the corpus/review-queue state; `verified` is never a publication authorization.
- A publication record or release manifest is the authoritative file-compatible representation for public membership. It references immutable `item_id` values and does not rewrite source evidence.
- Only Buddy or an explicitly authorized human editorial reviewer may publish, withdraw, or approve a release.
- The VPS may produce candidates and operational evidence only; it never creates publication membership.

## 2. Required release semantics

A release has a stable `release_id`, `created_at`, `published_at`, `status` (`draft`, `published`, `withdrawn`, `superseded`), reviewer/approver identity, generator revision, source-corpus input identity, and a list of canonical included item IDs.

An included item must have all of:

1. a canonical, unique `item_id` selected deterministically when legacy duplicate representations exist;
2. `review_status: verified` or an explicitly approved equivalent;
3. valid title, summary, source ID, original source URL, source/discovery timestamp, topic(s), sensitivity, and required controlled references;
4. an explicit SilverLeaf relevance decision of `included` with rationale and stable matching place/entity/community IDs;
5. no unresolved high-sensitivity restriction; medium/high sensitivity needs explicit editorial publication approval;
6. a public-safe projection with no internal notes, reviewer/private fields, raw file paths, secrets, credentials, or unapproved raw excerpts.

A withdrawn item is removed from future releases and recorded with withdrawal timestamp/reason category. Existing release artifacts are retained for audit/rollback; a correction produces a new release or an explicit supersession, never silent mutation.

## 3. Canonical selection and legacy disposition

The implementation must reject ambiguous duplicate item IDs. A declared canonical selector may choose one representation only when it has deterministic precedence documented in the release manifest. Otherwise the item is `needs_review` and excluded.

Legacy/incomplete records are not repaired by the exporter. They are either:
- excluded with a machine-readable reason;
- remediated by an editorial/data task; or
- explicitly retained as non-public archival evidence.

## 4. Public projection

The release generator produces deterministic, versioned public artifacts (names may be finalized by the implementation task):

- `release.json`: public items and release metadata;
- `search-index.json`: normalized client-search fields only;
- `release-manifest.json`: input identity, generator revision, item IDs, checksums, timestamps, and prior-release reference.

Stable filter dimensions are domain, topic, entity, place/community, and source IDs. Ordering is deterministic: selected publication ordering, then source/publication timestamps, then item ID. The public allowlist is explicit; unknown fields must not export.

## 5. Validation contract

Before a release is eligible, the corpus validator must check:

- required fields, enums, IDs, timestamps, URL shape, source/registry references, source-event linkage policy, and dedupe invariants;
- canonical ID uniqueness/selection;
- publication eligibility and withdrawn/superseded semantics;
- SilverLeaf inclusion/exclusion/needs-review decision and rationale;
- stable topic/entity/place/source/release IDs;
- public allowlist and internal denylist;
- deterministic output, manifest checksums, and rollback reference.

Required implementation tests include valid release, unreviewed item, unpublished verified item, withdrawn item, incomplete legacy item, duplicate ID, missing attribution, unknown registry reference, missing relevance rationale, and internal-field leak. Proposed commands after implementation: `python3 -m pytest tests/ -v`, `python3 scripts/validate.py`, and `python3 scripts/build_public_release.py --check`.

## 6. Operator workflow and rollback

1. Validate corpus and release candidates.
2. Generate a draft release and inspect count/diff/negative-case report.
3. Human reviewer approves publication membership.
4. Generate final manifest and static artifacts; preserve the prior release.
5. Deploy only through the portfolio-site's approved workflow.
6. Roll back by restoring the prior verified release artifacts; withdraw/correct through a new explicit release decision.

A failed export, checksum mismatch, missing attribution, unavailable source link, public-field leak, or unresolved relevance/sensitivity decision stops the workflow before deployment.

