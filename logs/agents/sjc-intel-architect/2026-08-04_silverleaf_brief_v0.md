# Agent Log — 2026-08-04 SilverLeaf Brief v0

**Agent:** sjc-intel-architect (OpenCode session)
**Task:** 17-silverleaf-brief-v0.md
**Report:** reports/17-silverleaf-brief-v0.md
**Status:** COMPLETE_WITH_FOLLOW_UP

## What was done

Adopted the accepted SilverLeaf Brief design and built a portable static v0:

1. **Docs consolidation** — rewrote `docs/public_ui_v0_spec.md` as the single
   authoritative SilverLeaf Brief v0 spec (accepted decisions + rejected
   recommendations); updated `docs/static_release_data_contract.md` with v0
   fields (relevance, source_unavailable, event dates, lifecycle, dimensions,
   environment); updated `ROADMAP.md` (§3B-G2 implemented, §3C-G2 underway).
2. **Exporter** — `scripts/build_static_release.py` + `static_release_common.py`:
   real/demo modes, `--check`, deterministic byte-stable output, content-quality
   validation, checksums, rollback identity, demo isolation.
3. **Site** — `scripts/build_static_site.py` + `site_templates.py` + `site_search.py`;
   `site/` with design-system CSS, progressive browse.js, 30 generated routes,
   8-item demo fixture under `site/fixtures/demo/`.
4. **Tests** — 42 new (exporter + site/search + accessibility structure);
   203 total pass.
5. **Validation** — full suite passes (pytest, validate.py incl. new §9,
   corpus validator, selector, portability, git diff --check).

## Key decisions

- Python generator (not Node) for route generation — matches repo tooling,
  documented in report §5.
- Embedded JSON data on Browse for progressive enhancement; server-rendered
  cards = no-JS baseline; JS only hides/reorders.
- Reviewer identity on manifest only (data contract §8 denylist); release.json
  never carries reviewer.
- Demo IDs use `DEMO-` prefix + `environment: demo` + visible site banner.
- Search semantics: 2-char threshold, lexical AND across tokens, OR within
  filter dimensions, release-order tie-break, no sort menu.

## Friction / notes

- Initial vision-review of screenshots flagged mobile "clipping"; disproved via
  headless-Chrome layout metrics (scrollWidth == clientWidth at 390px) and
  re-capture with `--force-device-scale-factor=1`. Screenshot tooling races on
  rapid sequential invocations; used separate runs.
- Real mode requires an explicit `--reviewer`; zero-item real release is valid
  and verified.
- No item approved/published; nothing committed.

## Files changed

- New: scripts/build_static_release.py, scripts/build_static_site.py,
  scripts/static_release_common.py, scripts/site_search.py,
  scripts/site_templates.py, tests/test_static_release.py,
  tests/test_site_build.py, site/**, reports/17-silverleaf-brief-v0.md.
- Modified: docs/public_ui_v0_spec.md, docs/static_release_data_contract.md,
  ROADMAP.md, scripts/validate.py, README.md.

## Next steps (Buddy/editorial)

- Editorial review of 78 pending items; SilverLeaf scope approval; per-item
  publication decisions; real release generation; §3C-G1 portfolio-site packet.
