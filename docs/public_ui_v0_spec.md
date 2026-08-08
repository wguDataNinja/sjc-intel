# SilverLeaf Brief — v0 Public UI Specification

**Status:** Accepted for v0 implementation
**Product:** SilverLeaf Brief
**Authority:** `ROADMAP.md` §3C; `docs/publication_release_contract.md` (public
projection, release artifacts); `docs/static_release_data_contract.md`
(data/export semantics — this document links it, it does not re-define it).
**Owner:** Buddy for editorial/publication decisions; implementation follows an
approved task packet (§3C-G1/§3C-G2).
**Last reconciled:** 2026-08-04 (Task 17).

This document is the **single authoritative product/UI specification** for
SilverLeaf Brief v0. It preserves the accepted, synthesized resident-facing
design. It intentionally rejects several earlier recommendations (§10). The
static data contract lives in `docs/static_release_data_contract.md` and is
authoritative for `release.json`, `search-index.json`, and
`release-manifest.json` semantics.

---

## 1. Product identity

| Element | Value |
|---------|-------|
| Name | **SilverLeaf Brief** |
| Tagline | *What changed around SilverLeaf—and why it matters.* |
| Public value proposition | SilverLeaf Brief turns reviewed local records and reporting into clear, source-linked updates for SilverLeaf residents. |

### 1.1 Product character

The product is:

* a finite reviewed neighborhood briefing;
* source-forward;
* calm;
* editorial;
* resident-centered;
* static;
* mobile-first;
* accessible.

It is **not**:

* a breaking-news service;
* an emergency alert service;
* a government portal;
* a dashboard;
* a social network;
* an analytics tool;
* a real-time feed;
* an autonomous AI publication.

## 2. Target user and resident questions

The primary user is a **SilverLeaf resident** (owner or renter in or adjacent
to the SilverLeaf master-planned community in northwestern St. Johns County,
Florida) who wants a fast, understandable way to see local change that may
affect their household, commute, utilities, schools, development, neighborhood
services, and community.

Secondary users: prospective residents evaluating the area, and local
business/community observers. v0 is deliberately single-audience to stay small.

### 2.1 Primary resident questions (in order)

The UI must answer, in order:

1. **What changed?**
2. **Why might it matter to me?**
3. **Does it apply directly to SilverLeaf, nearby, or countywide?**
4. **Where can I read the original source?**

## 3. Design constraints

- **Static-only:** all data comes from a deterministic static release
  (`release.json`, `search-index.json`, `release-manifest.json`); no API, no
  server, no VPS dependency. Works offline on the static host.
- **Published-only:** only policy-classified `AUTO_PUBLISHABLE` items or
  approved human exceptions with release membership appear. Nothing else.
- **Source-linked:** every item links to the original public source. The source
  remains authoritative; summaries are editorial context.
- **Honest scope:** explicitly not an alert system, not complete county
  coverage, not real-time.
- **Small by design:** no accounts, subscriptions, admin UI, live maps,
  real-time alerts, editing, or personalization in v0.
- **Accessible and mobile-first:** readable on a phone without pinching.

## 4. Navigation and routes

### 4.1 Navigation

Primary navigation (header and mobile bottom navigation):

* Latest
* Browse
* About

Secondary (footer):

* Data & Sources
* Coverage & limitations
* Report an issue
* Current release

### 4.2 Routes

| Route | Purpose |
|-------|---------|
| `/` | Latest release |
| `/browse` | Search and filters |
| `/topic/{topic-id}` | Collection template filtered by topic |
| `/place/{place-id}` | Collection template filtered by place |
| `/entity/{entity-id}` | Collection template filtered by entity |
| `/item/{public-item-id}` | Item detail |
| `/about` | Product, methodology, review meaning, limitations |
| `/sources` | Release provenance and source directory |

Topic, place, and entity routes **must reuse one collection-page
implementation**. No bespoke layouts.

## 5. Home / Latest

Home must contain, in order:

1. product name;
2. tagline;
3. release date;
4. real item count;
5. trust statement;
6. populated topic shortcuts;
7. ordered item list;
8. coverage statement;
9. footer.

Trust statement (exact copy):

> Reviewed summaries with direct links to public sources.

Footer disclaimer (exact copy):

> Not an official government or emergency-alert service.

**Ordering:** render items in the deterministic order supplied by the release
artifact. Do **not** silently reorder by source date, topic, relevance,
inferred importance, or lifecycle state.

**Do not** group Home by topic or relevance. **Do not** add a featured item
unless the release contract explicitly provides one. **Do not** promise a
weekly cadence.

## 6. Card content (item anatomy)

Every item card must show:

* one relevance label;
* one topic;
* title;
* summary;
* why it matters;
* source name;
* absolute source date;
* Reviewed indicator;
* Read update action (item detail);
* Original source action.

Limit visible metadata. Do **not** display every topic, entity, or place.

### 6.1 v0 resident topic categories

The public interface exposes only a small set of resident-facing topic
categories — never raw taxonomy ids, slugs, or underscore-separated strings.
The `display_topic` field on each release item is one of:

| id | Label |
|----|-------|
| `roads_traffic` | Roads & Traffic |
| `utilities_water` | Utilities & Water |
| `emergency_preparedness` | Emergency Preparedness |
| `schools_community` | Schools & Community |
| `local_business` | Local Business |

A release shows only the categories present in its items. Any taxonomy value
without a resident-facing label is a release-validation failure, not a display
concern.

## 7. Search and filters (Browse)

Search is **always visible on Browse**. Home may contain a compact search
action but not a dominant search hero.

### 7.1 Search fields

* title;
* summary;
* why it matters;
* topic labels;
* place labels;
* entity labels;
* source name.

### 7.2 Filters

Visible desktop filters: **topic**, **relevance**. Secondary filters:
**place**, **entity**. Mobile filters use a **bottom sheet**. No user-facing
sort control in v0.

### 7.3 Query parameters

`q`, `topic`, `place`, `entity`, `scope`.

### 7.4 Behavior

* OR within a filter dimension;
* AND across filter dimensions;
* URL state is shareable;
* browser Back restores state;
* opening and returning from detail preserves Browse state.

Search:

* begins after two characters;
* lexical only;
* deterministic;
* release order breaks ties;
* no semantic search;
* no sort menu.

## 8. Trust language

Public label: **Reviewed** (a link to the About definition on every card)

Detail explanation (exact copy):

> Each summary is reviewed against the linked source for clarity, relevance,
> and attribution before publication.

Do **not** say: *independently verified*, *verified truth*, *AI verified*,
*official*, *guaranteed accurate*.

Relevance and review state are **separate** and must not be merged.

## 9. Temporal truth

Use absolute, labeled dates. Potential labels:

* Source published.
* Hearing date.
* Effective date.
* Published in SilverLeaf Brief.

Do **not** infer lifecycle from age. Do **not** automatically label items
stale after a fixed number of days. Render lifecycle **only when explicitly
present** in the public release. Otherwise temporal status must appear in
editorial wording. Do not substitute one date for another.

## 10. Relevance labels

Use exactly:

* **In SilverLeaf.**
* **Near SilverLeaf.**
* **Countywide impact.**

Stable IDs: `in_silverleaf`, `near_silverleaf`, `countywide_impact`. Do not
merge relevance and review state.

## 11. Low volume

The first release may contain 5–15 items. Do not add filler. Do not include
old items merely to make the site look populated. Show: release date; actual
item count; coverage statement; curated spacing. No historical filler.

## 12. Item detail

Required:

* back link;
* relevance label;
* topic;
* title;
* source date;
* Reviewed indicator;
* summary;
* why-it-matters block;
* event/effective date when explicitly available;
* source panel;
* places;
* entities;
* publication date;
* related items when present;
* methodology link.

The source panel must support:

1. a working source URL;
2. a missing/unavailable source URL.

Unavailable state (exact copy):

> The original source link is currently unavailable.

Do **not** remove the published item solely because a link later fails.

## 13. About

Include:

* what the product is;
* selection method;
* definition of Reviewed;
* coverage;
* noncoverage;
* release approach;
* corrections;
* link to Data & Sources.

## 14. Data & Sources

Include:

* current release metadata;
* source directory for the release;
* source types;
* how source links are handled;
* public data fields;
* excluded internal data;
* coverage limitations;
* correction/source-problem link.

**Never expose:** agent reasoning, candidate records, internal review notes,
sensitivity rationale, dedupe metadata, logs, unpublished source proposals.

## 15. Mobile behavior

Below the mobile breakpoint:

* sticky three-item bottom navigation;
* full-width cards;
* Browse search at top;
* one Filters button;
* accessible bottom sheet;
* full why-it-matters content;
* large source/detail targets;
* no horizontal filter scroller;
* safe-area handling;
* content cannot be covered by bottom navigation.

Filter-sheet requirements: focus moves inside on open; focus is trapped;
Escape closes; focus returns to trigger; selected count visible; Clear all;
Show results action; screen-reader labeling.

## 16. Accessibility acceptance criteria (WCAG 2.2 AA)

Test:

* semantic landmarks;
* one H1 per page;
* sequential headings;
* skip link;
* visible focus;
* keyboard search and filtering;
* filter-sheet focus management;
* 200% zoom;
* 320px reflow;
* no horizontal page scrolling;
* color-independent badges;
* touch targets near 44px;
* accessible external-link names;
* no hover-only content;
* polite result-count announcements;
* reduced motion;
* readable no-JavaScript baseline.

## 17. Failure and empty states

Required:

* zero search results;
* zero filtered results;
* empty release;
* valid empty collection;
* missing related items;
* unavailable source link;
* missing optional date;
* missing entity;
* 404;
* JavaScript enhancement failure.

Do not leave blank sections. Do not substitute one date for another. Do not
invent missing values.

## 18. Static data contract

The UI consumes three static JSON files generated on the Mac by the export
step (`ROADMAP.md` §3B-G2). Full field contract:
`docs/static_release_data_contract.md`. The release artifacts are
self-describing: `release.json` includes a `dimensions` block with stable
topic/place/entity/source/relevance identifiers and their public labels, so
the site is portable and needs no registry access at runtime.

- `release.json` — release metadata + public items (public projection only).
- `search-index.json` — normalized client-search fields (lowercased tokens).
- `release-manifest.json` — input identity, generator revision, item IDs,
  checksums, timestamps, prior-release reference (rollback identity).

## 19. Design system

Typography: Source Serif 4 for headings; Source Sans 3 for body/UI — with
approved local/system fallbacks. No external font loading; no font binaries
committed.

Colors:

| Token | Value |
|-------|-------|
| Page background | `#F7F6F2` |
| Surface | `#FFFFFF` |
| Primary text | `#1F2522` |
| Secondary text | `#5B6560` |
| Evergreen | `#235B43` |
| Link | `#005F73` |
| Border | `#D9DED9` |
| Why-it-matters background | `#EDF5F0` |
| Neutral badge | `#EEF1EF` |
| Focus ring | `#005F73` |
| Error | `#A12828` |

Test actual contrast; do not assume compliance from the values alone.

Layout: editorial single-column cards; maximum content width ~1120px; reading
column ~760px; mobile gutters 16px; no default shadows; no equal-height
dashboard grid; no horizontal page scrolling.

Motion: 120–180 ms; minimal; respect reduced motion; no scroll-triggered
animation.

## 20. Content rules and public claims

* Every item must be verifiable against its linked source.
* Never claim: "all county news", "real-time", "automated alerts",
  "complete coverage", "official partner".
* Crime/public-safety items appear only under explicit editorial approval
  (default excluded).
* Editorial summaries may be written in plain language but must not invent
  facts absent from the source.
* Publication timestamps must distinguish source date vs review vs publish.

## 21. Explicit non-goals (v0)

Do not implement: accounts; subscriptions; admin; live maps; alerts; semantic
search; API; chat; comments; trending; confidence scores; infinite scroll;
dark mode; onboarding modal; historical filler; source-type trust scores.

## 22. Rejected recommendations (accepted synthesis)

The following earlier recommendations were intentionally **rejected** for v0
and must not be re-introduced without a new product decision:

| Rejected recommendation | Reason |
|-------------------------|--------|
| Dashboard-style home | Contradicts the calm, editorial, briefing character. |
| User-facing sort control | Release order is deterministic and editorial; residents read the briefing. |
| "Active Now" without explicit data | No real-time data source is in scope. |
| Fixed weekly buckets | No weekly-cadence promise; releases happen when reviewed. |
| Inferred stale state | Temporal truth must be explicit, not inferred from age. |
| Dark mode | Out of scope for v0. |
| New backend fields required solely for UI | The data contract supplies everything the UI needs. |
| Historical filler | Low-volume, no-filler principle. |

## 23. Acceptance criteria

The v0 UI passes when, using a reviewed release:

1. Home lists only published items, in release order, with source links.
2. Search finds items by title/summary/topic/entity/place and shows snippets.
3. Topic, relevance, place, and entity filters work independently and combined.
4. Item detail shows title, summary, why-it-matters, place, topic, entity,
   source name/URL, source date, publication date, Reviewed indicator.
5. About page states scope, periodicity, non-alert nature, source authority.
6. No internal/reviewer/dedupe fields appear anywhere.
7. Empty and error states render without JS dependency.
8. Pages are usable at 320px wide and keyboard-only.
9. Every item's source URL opens the original public record (or shows the
   unavailable state).
10. Data loads from static JSON only (no VPS/API dependency).
