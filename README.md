# SJC_Intel

AI-assisted local intelligence and reporting for St. Johns County, Florida.

SJC_Intel is an evidence-first, agent-assisted system that discovers, monitors,
classifies, verifies, and organizes public information about St. Johns County —
focused on master-planned communities, county government, utilities, schools,
roads, and development. It produces structured intelligence items for editorial
review, not published news or automated alerts.

The first public product lens is **SilverLeaf neighborhood intelligence**:
reviewed, source-linked periodic intelligence for the SilverLeaf area.

## What it is

- **Public sources only.** Official records, government portals, school and
  utility feeds, and local media — no private or login-gated content.
- **Evidence-first.** Every item carries its original source URL, an observed
  timestamp, and a bounded verbatim excerpt.
- **Human-reviewed.** Machine-produced candidates become corpus items only
  through explicit human decisions; nothing is published automatically.
- **Mac-authoritative.** The durable corpus, review state, and release history
  live in the file-backed repository. A bounded VPS worker may prepare
  transfer bundles; it never writes the corpus or publishes.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a public overview of the
domain, source discovery, deterministic monitoring, evidence/review model,
weekly operations, and the VPS/Mac split.

## Repository layout

| Path | Purpose |
|------|---------|
| `registry/` | Sources, candidates, communities, tracked entities, search profiles |
| `data/intel_items/` | Normalized intelligence items (corpus) |
| `data/source_events/` | Fetch/meeting container records |
| `data/review_queue/` | Editorial review queue and decisions |
| `data/index/` | Dedupe fingerprint index |
| `site/` | SilverLeaf Brief — the portable static v0 site (generated) |
| `scripts/` | Deterministic extraction, validation, and operational tooling |
| `schemas/` | Field-level data contracts |
| `docs/` | Methodology, contracts, and operating references |

## SilverLeaf Brief

**SilverLeaf Brief** is the first public product: a reviewed, static,
mobile-first neighborhood briefing for SilverLeaf and the surrounding
corridor — clear, source-linked updates that answer "what changed, and why it
matters." Design authority: `docs/public_ui_v0_spec.md`; static data contract:
`docs/static_release_data_contract.md`.

It is a **standalone, deployment-neutral MVP owned by this repository** (under
`site/`) — not hosted inside any portfolio site. Everything is generated from
public reviewed items; no backend, no API, no database, no framework, no
Ivy/VPS dependency.

### Build and preview

```bash
# 1. Build the real release (from approved publication decisions)
python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001 \
  --reviewer "<reviewer>" --window-start 2026-05-01 --window-end <approval date>

# 2. Generate the standalone site (defaults to the latest real release)
python3 scripts/build_static_site.py

# 3. Preview locally
cd site && python3 -m http.server 8000
# open http://localhost:8000/
```

To preview the nonproduction demo instead:

```bash
python3 scripts/build_static_release.py --release-id SJC-REL-DEMO-20260804 --demo
python3 scripts/build_static_site.py --source site/data/demo
```

The site is deployable by copying `site/` to any simple static host (see
`site/README.md` for deployment instructions). No automatic deployment is
configured; a target must be explicitly selected.

## Setup

```bash
pip install -r requirements.txt
```

## Validation

Run offline (no network, no VPS, no credentials):

```bash
python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
```

## Status

Development. This repository is being prepared for public portfolio
publication; it is not yet a published product. Internal operating material is
maintained separately and is not part of the public presentation.

## License

MIT License. Copyright (c) 2026 wguDataNinja. See [LICENSE](LICENSE).
