# SJC_Intel — Architecture

**Status:** Public portfolio architecture overview. This document is
publication-safe: it contains no secrets, private host paths, credentials, or
operational vulnerabilities. Internal operating detail lives in the
repository's internal documentation and is not part of this presentation.

## 1. Problem

St. Johns County, Florida residents — especially in master-planned communities
— face a fragmented information landscape: county press releases, road and
permitting notices, school district feeds, sheriff updates, utility
announcements, and community-specific news arrive across dozens of separate
public websites with no common structure. Important local change (road
closures, rezoning hearings, water advisories, school boundary adjustments)
is easy to miss.

## 2. Product

SJC_Intel is an evidence-first, agent-assisted local intelligence system. It
discovers, monitors, classifies, verifies, and organizes public information
about St. Johns County, producing structured intelligence items for editorial
review. It is **periodic neighborhood intelligence**, not a live alert service.

The first public product lens is **SilverLeaf neighborhood intelligence**:
a reviewed, source-linked, searchable set of intelligence items for the
SilverLeaf community and its surrounding corridor.

## 3. Design principles

- **Official records are the first authority** for consequential claims; local
  media is context and tip-surfacing unless verified against official records.
- **Deterministic capture first** — reproducible scripts and bounded HTTP
  fetches form the core; agentic search enriches but never replaces them.
- **Public sources only** — no private groups, login-gated portals, fake
  accounts, or scraping of paywalled content.
- **Candidate ≠ reviewed ≠ published** — machines propose, humans decide,
  publication is a separate explicit act.
- **The corpus lives in files** — the Mac file-backed repository is the durable
  authority for items, review state, and release history.

## 4. Architecture

```
discovery (source candidates, search profiles)
      ↓
source registry ──→ monitored sources
      │                    │
      ▼                    ▼
   intel candidates ◄── source events (fetches/meetings)
      │                    │
      ▼                    ▼
   dedupe index ◄── corpus items ──→ review queue
                                          │
                                          ▼
                              publication decision
                                          │
                                          ▼
                            static release export (reviewed-only)
```

### Core objects

| Object | Role |
|--------|------|
| **Source** | A registered public source (registry). |
| **Source event** | One occurrence — a fetch, meeting, or snapshot container. |
| **Intel item** | One discrete resident-impact finding (the atomic unit). |
| **Candidate** | A machine-produced finding awaiting a human decision. |
| **Dedupe index** | Deterministic fingerprints preventing duplicate items. |
| **Review queue** | Editorial review state and decisions for every item. |
| **Release** | An explicit, reviewed-only publication decision. |

## 5. Source discovery

Discovery runs in bounded loops over public sources and search profiles. It
may propose new sources, moved endpoints, coverage gaps, and monitor
improvements — but proposals are never promoted into the canonical source
registry automatically. Promotion requires an approved source-review process.

## 6. Deterministic monitoring

Approved sources are monitored by deterministic, reproducible runners
(fetch → parse → normalize → candidate). Each run is isolated in a run
workspace, captures source health and source events, and produces candidates
classified with a resident-interest perspective. Runs never write directly to
the authoritative corpus.

## 7. Agentic discovery

Bounded agentic search enriches discovery by finding new public sources and
gaps, always subject to the same human-review boundary. It does not replace
deterministic capture and never operates outside an explicit budget.

### Adaptive coverage loop

The Resident Coverage Strategist can propose durable subjects, aliases, search
profiles, milestones, timeline links, and coverage lanes. The Resident Coverage
Editor then independently asks what a SilverLeaf resident would expect to know
that remains missing, stale, weakly tracked, or under-researched; it can only
recommend bounded follow-up. A separate evaluator checks evidence and
historical availability; accepted changes become usable only in the next weekly
run. The file-backed replay contract is documented in
`docs/adaptive_discovery_backtest.md`.

## 8. Evidence and review model

Every item retains:

- original source URL;
- observed/discovered timestamp;
- bounded verbatim excerpt (never wholesale content copying);
- source attribution;
- classification (topic, geography, urgency, sensitivity);
- provenance to its source event and run.

Editorial review is a human decision recorded in the review queue. Items with
public-safety, legal, crime, or minors involvement require mandatory human
review. `verified` never means `published`.

## 9. Weekly operations and the VPS/Mac split

A bounded weekly operational run executes approved deterministic monitors and
bounded discovery on a low-cost VPS. It produces a versioned transfer bundle
(manifest + checksums + candidates + proposals). The Mac pulls the bundle,
verifies it, stages it in an incoming area, and records a receipt. Imported
candidates stay distinct from accepted corpus items until an explicit human
decision. The VPS never publishes, never promotes sources, never changes
taxonomy, and never writes the Mac corpus.

Transfer semantics (idempotent replay, checksum verification, receipts,
acknowledgements, and delayed pruning only after a verified receipt) are
defined in the weekly operational contract.

## 10. Publication

Publication is a separate explicit act. A reviewed item becomes part of a
named release only through a human publication decision. The release export is
deterministic and versioned; prior releases are retained for rollback. No
autonomous publication exists.

## 11. Portability

The pipeline is organized so that generic intelligence behavior (source/event
semantics, evidence, dedupe, review/publication separation, validation, bundle
transfer) is distinct from St. Johns County configuration (registries,
extractors, taxonomy, geography) and from SilverLeaf publication policy. This
layout is a reference implementation for a future second domain; it does not
claim to be a turnkey multi-domain platform.

## 12. Limitations

- Periodic intelligence, not real-time alerts or emergency notification.
- County-wide collection but product focus on SilverLeaf for the first release.
- Manual geographic relevance rules (no GIS/PostGIS in the launch scope).
- Human editorial review is required for sensitive items; it is a throughput
  and quality constraint by design.
- No user accounts, subscriptions, or public API in the launch scope.

## 13. Future domains

Live incident awareness, broader county coverage, additional master-planned
communities, and other geographies are natural extensions once the reference
pipeline and publication workflow are proven and a portability demonstration
passes.

## Diagrams and screenshots

Recommended portfolio artifacts (not yet produced): a pipeline diagram, a
review-flow diagram, and a public release screenshot once the first release
exists.
