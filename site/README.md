# SilverLeaf Brief — Standalone Site (MVP) Guide

Concise build/preview/deployment guide for the standalone static SilverLeaf
Brief site. This is an **SJC_Intel-owned MVP** — it is not hosted inside any
portfolio site. Full product/UI authority: `docs/public_ui_v0_spec.md`. Static
data contract: `docs/static_release_data_contract.md`.

## What this directory is

`site/` is the standalone, deployment-neutral static v0 application, generated
by repository tooling. It is plain HTML/CSS/JSON/JS — no backend, no API, no
database, no framework, no Hugo, no Ivy/VPS dependency. It can be previewed
locally and later deployed to any simple static host.

The **default build is the latest real release** (`site/data/releases/…`).
The demo fixture (`site/fixtures/demo/`) is for development/preview only.

## Commands (run from the repo root)

| Task | Command |
|------|---------|
| Resolve a publication exception | `python3 scripts/publication_decision.py approve --item-id <id> --reviewer <name> --silverleaf included --relevance <label> [--public-summary-override "..."]` |
| Build a real release (policy-selected items) | `python3 scripts/build_static_release.py --release-id <id> --reviewer "<name>" --prior-release-id <prior-id> --window-start ... --window-end ...` |
| Build the demo release | `python3 scripts/build_static_release.py --release-id SJC-REL-DEMO-20260804 --demo` |
| Check a release without writing | `python3 scripts/build_static_release.py --release-id <id> --check` |
| Generate the site (real release default) | `python3 scripts/build_static_site.py` |
| Generate from a specific release | `python3 scripts/build_static_site.py --source site/data/releases/<release-id>` |
| Generate the demo site | `python3 scripts/build_static_site.py --source site/data/demo` |
| List generated routes | `python3 scripts/build_static_site.py --list-routes` |
| Preview locally | `cd site && python3 -m http.server 8000` |

## First release (recorded)

`SJC-REL-2026-08-002` — 7 local policy-selected items, generated 2026-08-07
with `SJC-REL-2026-08-001` retained as its rollback predecessor. It has not
been deployed by this task. Regenerate with:
`--window-start 2025-01-01 --window-end 2026-08-07T23:59:59Z`.

## Release input

- **Real releases** come from `AUTO_PUBLISHABLE` items under
  [`docs/PUBLICATION_POLICY.md`](../docs/PUBLICATION_POLICY.md), plus approved
  human exceptions (`data/publication_decisions/`). The exporter validates the
  full corpus, runs the deterministic selector, validates content quality, and emits `release.json`,
  `search-index.json`, and `release-manifest.json` under
  `site/data/releases/{release-id}/`.
- **Demo mode** reads the explicit fixture `site/fixtures/demo/release.yaml`
  and emits to `site/data/demo/` with `environment: demo`. Demo data is
  isolated, labeled, and the site renders a visible "Demo preview" banner.
  Demo data is never a real public release.

## Output

- Release artifacts: `site/data/releases/{id}/` (real) or `site/data/demo/`
  (demo).
- Generated site: `site/` (Latest, Browse, About, Data & Sources, item,
  topic, place, entity routes, 404).
- `site/build.json` records which release produced the current build.

## Validation

- Export: `python3 scripts/build_static_release.py --release-id <id> --check`
  (no writes). Checksums in the release manifest are verified against bytes
  before the site generator will build (rollback safety).
- Site: `python3 scripts/build_static_site.py --list-routes` (no writes);
  the generator refuses to build if manifest checksums do not match.
- Suite: `python3 -m pytest tests/ -v`, `python3 scripts/validate.py`
  (includes §9 SilverLeaf site check + §10 scope registry checks).

## Deployment (simple static host)

The generated `site/` directory is the deployable artifact. To deploy:

1. Build the release + site (see Commands) so `site/` contains the real
   release output.
2. Copy the **entire `site/` directory** to the host (do not copy only the
   HTML — the app needs `assets/`, `data/`, and the route directories).
3. Serve the directory as static files. All URLs are relative, so it works at
   the domain root or any subpath.

Host-neutral examples (no automatic deployment):

- **Any static host / nginx / S3 / CDN / Netlify / Cloudflare Pages / GitHub
  Pages:** upload `site/` as the publish directory (build output). No build
  step on the host is required — it is already static output.
- **GitHub Pages:** push this repository, then serve `site/` (e.g., a Pages
  action with `publish_dir: site` or a `.nojekyll` file in `site/`). A
  `404.html` at the site root is honored by Pages for SPA-style fallback.
- **Local check:** `python3 -m http.server 8000` from inside `site/`.

Do **not** deploy automatically; a deployment target must be explicitly
selected first.

## Portability

- All URLs are relative; the site works at any path depth.
- Semantic HTML + CSS + minimal JS; core content is readable with JavaScript
  disabled (Browse degrades to the full release list; collection routes are
  server-rendered).
- Fonts use local/system fallbacks; no external font loading; no font
  binaries committed.
- No Hugo, Ivy, VPS, database, or backend dependency.
