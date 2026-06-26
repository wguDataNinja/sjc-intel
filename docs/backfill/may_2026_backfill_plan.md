# May 2026 Historical Backfill Plan

Status: planned only  
Do not run without explicit instruction from Buddy.

## Window

- Start date: 2026-05-01
- End date: 2026-05-31
- Output month key: `2026-05`

## Why May 2026 First

Deep Research recommends May 2026 because it is the most recent full month
before the 2026-06-03 report date. It is close enough to current operations to
produce useful source-discovery and taxonomy feedback, and it likely includes a
countywide water/restriction story plus FY2027 budget-workshop context.

This supersedes the earlier January 2026 first-backfill idea unless Buddy gives
a specific reason to start with January.

## Expected Outputs

- `data/monthly/2026-05/discovered_items.yaml`
- `data/monthly/2026-05/topic_clusters.yaml`
- `data/monthly/2026-05/source_gaps.md`
- `data/monthly/2026-05/monthly_wrap.md`

## Source Stacks To Check

Official first:

- County Commission / Clerk / GovTV stack
- Planning and Zoning / Growth Management stack
- Development Tracker and GIS Hub
- Permit status and public permit search
- County roads / traffic / featured projects
- FDOT District Two / NFLRoads / Florida 511
- County utility / water conservation / boil notices
- SJRWMD permitting and watering restrictions
- SJCSD / BoardDocs / zoning / new schools
- Sheriff / Emergency Management / NWS Jacksonville
- Property Appraiser / Tax Collector / budget / transparency
- Florida Public Notices

Context and tip-surfacing:

- St. Johns Citizen
- Jacksonville Daily Record
- Ponte Vedra Recorder
- Local TV stack
- Chamber calendar
- Community/developer pages and public CDD sites

## Search Terms To Use First

Use `registry/search_terms.yaml`, prioritizing:

- `utilities_water`: `ST-0601` through `ST-0604`
- `transportation`/corridor: `ST-0101` through `ST-0106`, `ST-0303`
- `school`: `ST-0201` through `ST-0205`
- `permits_development`: `ST-0301`, `ST-0302`
- `cdd_governance`: `ST-0403`, `ST-0404`, plus community-specific CDD terms
- community terms for SilverLeaf, Nocatee, RiverTown, Shearwater, TrailMark,
  Beachwalk, and Beacon Lake

## Classification Requirements

Every discovered item must include:

- source URL and source type
- title or concise label
- date observed and event/publication date when available
- topics from `docs/taxonomy.md`
- communities from `registry/communities.yaml`
- geographic scope
- urgency
- sensitivity
- verification status
- review status
- taxonomy_gap when existing vocabulary is insufficient

## Resident-Interest Requirements

Use the resident-interest classifier rules for:

- primary topic
- interest tags
- affected audiences
- resident relevance level
- plain-language why-it-matters note
- human_review_required

Treat public-safety, crime, legal, school-safety, and controversy items as
human-review-required.

## Dedupe And Index Handling

- Do not update `data/index/prior_items.yaml` during exploratory backfill unless
  Buddy explicitly wants backfill items to affect live monitor dedupe.
- Within `data/monthly/2026-05/discovered_items.yaml`, dedupe by normalized URL
  first, then by source/date/title.
- Keep cross-source duplicates as one canonical item with `supporting_sources`
  when the same fact appears in multiple places.
- Store source IDs when canonical; use `web_discovery` or `source_candidate`
  when not yet canonical.

## Sensitivity Rules

- Official records can be `source_confirmed`, but publication still requires
  review.
- Local media can surface tips/context; consequential claims need official
  confirmation.
- Private Facebook groups, private forums, login-gated HOA/resident portals,
  private screenshots, and forwarded texts are out of scope.
- Store minimal personal information. Prefer parcel IDs, agenda item numbers,
  permit numbers, CDD names, and official document URLs.

## Publishable Vs Exploratory

Publishable requires:

- public source URL
- factual claim traceable to source
- no unresolved sensitive-claim ambiguity
- human review for sensitive or consequential items
- clear resident relevance

Exploratory includes:

- source-discovery leads
- search results needing confirmation
- local-media-only claims not confirmed by official records
- taxonomy/source gaps
- monthly clustering observations

Do not publish the May wrap. It is an internal baseline until editorial review
and corrections workflow exist.

## Hermes Task Outline

Task: `historical-backfill-2026-05`

Inputs:

- target month: `2026-05`
- search terms: selected IDs from `registry/search_terms.yaml`
- canonical sources: `registry/sources.yaml`
- candidate sources: `registry/source_candidates.yaml`
- taxonomy: `docs/taxonomy.md`
- RI rules: `docs/resident_interest_classification.md`

Steps:

1. Create `data/monthly/2026-05/`.
2. Search official stacks first, then media/context sources.
3. Extract candidate items with source URL, date, title, and summary.
4. Dedupe within month.
5. Classify factual fields and resident-interest fields.
6. Write `discovered_items.yaml`.
7. Cluster by beat/community/corridor into `topic_clusters.yaml`.
8. Write `source_gaps.md`.
9. Write internal-only `monthly_wrap.md`.
10. Update search-term effectiveness notes in a review artifact, not by
    silently rewriting the registry during the run.

Completion criteria:

- At least the top five beats were searched.
- Official-source attempts are recorded even when no items were found.
- All gaps and uncertain claims are labeled.
- No publishing, scheduling, or live monitor run occurs.
