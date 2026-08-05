# Task 19 — Standalone SilverLeaf Brief MVP Publication

**Task identity:** 19-standalone-mvp-publication.md
**Date:** 2026-08-04
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Final status:** COMPLETE

---

## 1. Executive result

The first real SilverLeaf Brief release is **approved, generated, and published
as a standalone MVP owned by SJC_Intel**, and the repository is **committed and
pushed**. The earlier portfolio-integration direction was discarded per Buddy's
correction: `buddyowens-site` is not archived, but SilverLeaf Brief is **not**
published inside any portfolio site.

Delivered:

- **First release approved and recorded** — 4 publication decisions
  (SJC-UTIL-20260603-0001 water shortage, SJC-EM-20260626-0001 hurricane
  preparedness, SJC-UTIL-20260603-0005 service-line inventory,
  SJC-CN-20260802-0001 CR 16A closures) with copy edits and relevance labels.
- **Real release generated** — `site/data/releases/SJC-REL-2026-08-001/`
  (release.json, search-index.json, release-manifest.json; 4 items;
  checksums verified).
- **Standalone MVP built** — `site/` generated from the real release (17
  routes), deployment-neutral, no Hugo/Ivy/VPS/backend dependency.
- **Validated** — full suite (217 tests), desktop/mobile, accessibility,
  search, filters, source links, no horizontal overflow.
- **Committed and pushed** — 7 logical commits to `origin/master`.
- **Deployment instructions** — static-host-neutral guide in `site/README.md`.

## 2. Corrections adopted

- `buddyowens-site` is **not archived** (Task 18 inspection wrongly flagged it);
  corrected and not relied upon.
- SilverLeaf Brief is a **standalone MVP owned by SJC_Intel** under `site/`,
  not published inside the portfolio.
- No modification of `buddyowens-site`; no files copied into the portfolio; no
  portfolio case-study page; no Hugo, Ivy, or VPS dependency; no automatic
  deployment.

## 3. First-release verification and approvals

Source verification performed before approval:

- **SJC-UTIL-20260603-0001 (water)** — verified still active on the utility
  page Aug 4, 2026 (Phase III, Extreme Drought D3, one-day-per-week irrigation,
  reclaimed water exempt).
- **SJC-EM-20260626-0001 (hurricane)** — county emergency management page
  (2026 season, began June 1).
- **SJC-UTIL-20260603-0005 (service line)** — utility page (EPA Community
  Lead-Safe Hub inventory).
- **SJC-CN-20260802-0001 (CR 16A)** — county page (updated July 27; weekend
  closures Jul 31–Aug 3 and Aug 7–10, detour SR 16 / SR 13). Review status
  flipped to `verified`.
- **SJC-CN-20260802-0002 (Daily's)** — resolved to **exclude**: the property is
  at 600 SR 13 North, Fruit Cove (not a SilverLeaf access route).
- **SJC-SL-20260706-0005 (Bala's)** — deferred: article exists on St. Johns
  Citizen but the recorded URL returns 404 (needs a corrected URL before a
  future release).

Approvals recorded via `scripts/publication_decision.py` (reviewer Buddy) with
relevance labels and approved `public_summary_override` copy edits. Medium
sensitivity (water) received explicit editorial approval.

## 4. Real release generated

`python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001
--reviewer Buddy --published-at 2026-08-04T12:00:00Z --now
2026-08-04T12:00:00Z --window-start 2026-05-01 --window-end 2026-08-04` →

- 4 items, deterministic order (CR 16A → service line → hurricane → water).
- Copy edits and `near_silverleaf` override for CR 16A honored.
- Manifest checksums verify; no internal fields exported.

## 5. Standalone MVP site

`site/` generated from the real release: Latest, Browse (search + filters),
About, Data & Sources, item detail (4), topic collections, place collections,
404 — 17 routes. The generator now **cleans stale routes on rebuild** (a prior
demo build had left leftover demo pages in the output) and **defaults to the
latest real release** (demo remains available via `--source site/data/demo`).

## 6. Deployment-neutrality

- All URLs relative; works at any path depth / any static host.
- Semantic HTML + CSS + minimal JS; no external fonts, no font binaries.
- No backend, API, database, Hugo, Ivy, or VPS dependency.
- Demo fixtures isolated under `site/fixtures/demo/`; generated demo output
  git-ignored (`site/data/demo/`).
- Deployable by copying `site/` to any simple static host; no automatic
  deployment configured.

## 7. Validation results

```
python3 -m pytest tests/ -v            → PASS, 217 passed (order-independent; conftest now
                                         sets the publication fixture env before import)
python3 scripts/validate.py            → PASS — ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS — 0 errors, 321 warnings, 192 items, 4 decisions
python3 scripts/validate_silverleaf_scope.py  → PASS — 0 errors, 0 warnings
python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001 --check --reviewer Buddy
                                         → READY, 1 item (CR 16A) under the default 60-day window;
                                           the full 4-item release requires the approved 90-day
                                           window (--window-start 2026-05-01), per §10 policy
python3 scripts/build_static_site.py --list-routes → 17 routes (4 items, env=real)
python3 scripts/portability_check.py   → PASS
node --check site/assets/js/browse.js  → syntax OK
git diff --check                       → clean
```

Browser validation (headless Chrome): no horizontal overflow at 390 px
(`scrollWidth == clientWidth`); Browse filter `?topic=transportation` hides the
3 non-matching cards; search `q=water` finds the water item; every page has a
skip link + single H1; item source links open the correct public URLs.

## 8. Deployment instructions

Written to `site/README.md`: build the release + site, then copy the entire
`site/` directory to any simple static host (GitHub Pages with
`publish_dir: site`, Netlify, Cloudflare Pages, S3/CDN, nginx, or local
`python3 -m http.server`). A `404.html` is provided for static hosts that honor
it. No automatic deployment is configured.

## 9. Git: committed and pushed

Seven commits pushed to `origin/master` (explicit paths, no secrets):

1. `feat:` weekly operational bundle/import foundation (Tasks 12-13)
2. `feat:` file-backed publication decisions and corpus validation (Task 16)
3. `data:` SilverLeaf scope registry (Task 18)
4. `feat:` SilverLeaf Brief static export and standalone site (Tasks 17-19)
5. `docs:` publication/UI authority, roadmap, reports, and logs (Tasks 11-19)
6. `data:` approve first SilverLeaf release and refresh curated corpus state
7. `docs:` Task 19 report (this commit)

Working tree is clean. Nothing unrelated was committed; `data/incoming/` and
`site/data/demo/` are git-ignored (transient/generated).

## 10. Remaining work

- **Deployment** only when a target is explicitly selected (copy `site/` to the
  chosen static host).
- **Portfolio integration** is a later, separate case-study/link task (explicitly
  out of scope here).
- Future releases: editorial review of the remaining backlog, then repeat the
  approve → generate → build → deploy cycle.

## 11. Final task status

| Area | Status |
|------|--------|
| Verify + approve first-release items | COMPLETE |
| Generate real release | COMPLETE |
| Standalone MVP site | COMPLETE |
| Deployment-neutral | COMPLETE |
| Validation (desktop/mobile/a11y/search/filters/links) | COMPLETE |
| Commit + push | COMPLETE |
| Deployment instructions | COMPLETE |
| Portfolio integration (later, separate) | DEFERRED |

**Final status vocabulary:** COMPLETE — the standalone SilverLeaf Brief MVP is
approved, generated, validated, committed, and pushed; only an explicitly
selected deployment target remains.
