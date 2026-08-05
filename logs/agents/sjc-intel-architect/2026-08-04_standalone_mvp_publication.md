# Agent Log — 2026-08-04 Standalone SilverLeaf Brief MVP Publication

**Agent:** sjc-intel-architect (OpenCode session)
**Task:** 19-standalone-mvp-publication.md
**Report:** reports/19-standalone-mvp-publication.md
**Status:** COMPLETE

## What was done

Executed the standalone MVP publication (per Buddy's correction: buddyowens-site
is not archived; the site is NOT published inside the portfolio):

1. **Approved the first release** — verified sources (water still active; CR 16A
   closures; Daily's at SR 13/Fruit Cove excluded; Bala's URL 404 deferred),
   recorded 4 publication decisions (reviewer Buddy) with copy edits +
   relevance overrides.
2. **Generated the real release** SJC-REL-2026-08-001 (4 items, 90-day window).
3. **Built the standalone MVP** — generator now defaults to the latest real
   release and cleans stale routes on rebuild (fixed leftover demo pages).
4. **Deployment-neutral** — relative URLs, no external deps; deployment
   instructions in site/README.md; demo output git-ignored.
5. **Validated** — 217 tests (made order-independent via conftest env), browser
   checks (mobile no-overflow, JS filters, search, accessibility structure,
   source links).
6. **Committed + pushed** — 7 logical commits to origin/master, clean tree.
7. **Deployment instructions** for a simple static host.

## Key decisions

- Water item = SJC-UTIL-20260603-0001 (authoritative, medium, editorial
  approval granted); Daily's excluded (SR 13/Fruit Cove not SilverLeaf); Bala's
  deferred (URL 404).
- 90-day release window required (default 60-day drops ongoing countywide
  items).
- Generated real site output IS committed (the standalone MVP deliverable);
  demo output + data/incoming git-ignored.
- test_static_release TestRealMode made hermetic via sandbox + publication_common
  constant monkeypatch; conftest now sets the publication fixture env before
  import so the suite is order-independent.

## Friction / notes

- Legacy-exception constant (LEGACY_EXCEPTIONS_FILE) is import-time; had to
  monkeypatch it too for the sandbox tests.
- build_static_site.py previously left stale routes from prior builds; added
  clean_generated (DryRun overrides it to keep --list-routes non-mutating).
- class-body `reviewer = reviewer` NameError under pytest; used type("Args",…).

## Files changed

- Approvals: data/publication_decisions/SJC-*.yaml (4), CR16A review status.
- New: tasks/19-standalone-mvp-publication.md, reports/19-standalone-mvp-publication.md.
- Modified: scripts/build_static_site.py (clean + default-release), .gitignore,
  tests/conftest.py, tests/test_static_release.py, site/README.md, README.md.
- Committed in 7 groups (Tasks 12-19) and pushed to origin/master.

## Next steps

Deploy only when a target is explicitly selected; portfolio integration is a
later, separate task.
