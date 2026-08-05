# Task 19 — Standalone SilverLeaf Brief MVP Publication

**Status:** Approved bounded task (Buddy direction, supersedes the earlier
portfolio-integration Task 19 packet, which is discarded).

## Objective

Publish a standalone SilverLeaf Brief v0 as a deployment-neutral static MVP
owned by SJC_Intel, suitable for local preview and later independent
deployment. **Portfolio integration is explicitly out of scope** and deferred to
a later, separate case-study/link task.

## Corrections adopted

- `buddyowens-site` is **not archived** (Task 18 inspection wrongly flagged it).
- SilverLeaf Brief must **not** be published inside the portfolio site.

## Scope (in)

1. Verify and approve the first-release items.
2. Generate the real release (`SJC-REL-2026-08-001`).
3. Build the standalone SilverLeaf Brief MVP.
4. Make the site deployment-neutral.
5. Validate desktop, mobile, accessibility, search, filters, and source links.
6. Commit and push the SJC repository.
7. Prepare deployment instructions for a simple static host.
8. Leave portfolio integration as a later, separate case-study/link task.

## Scope (out / never)

- Modify `buddyowens-site`; copy files into the portfolio; create a portfolio
  case-study page.
- Depend on Hugo, Ivy, or the VPS.
- Deploy automatically unless a deployment target is explicitly selected.
- Approve items beyond the verified first-release set (no high-sensitivity or
  unverified items).

## Site location

`/Users/buddy/projects/sjc_intel/site/` (or an equivalent generated output
directory defined by the repo).

## Outputs

- First-release publication decisions (recorded in
  `data/publication_decisions/`).
- `site/data/releases/SJC-REL-2026-08-001/` (real release artifacts).
- Standalone MVP site built from the real release under `site/`.
- Deployment instructions (static-host-neutral).
- `reports/19-standalone-mvp-publication.md`.

## Validation

`python3 -m pytest tests/ -v`; `python3 scripts/validate.py`;
`python3 scripts/validate_publication_corpus.py`;
`python3 scripts/validate_silverleaf_scope.py`;
`python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001 --check`;
`python3 scripts/build_static_site.py --list-routes`; `git diff --check`;
browser checks (desktop/mobile/accessibility/search/filters/source links).

## Git policy

Explicitly authorized by Buddy: commit the repository in logical groups and
push to `origin/master`. Stage explicit paths only; no secrets; validate
structured data before commit.
