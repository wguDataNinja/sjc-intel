Decisions:

* Product name: SilverLeaf Brief
* Static, framework-light v0.
* Primary navigation: Latest · Browse · About
* Secondary route: Data & Sources
* One reusable collection template for topic, place, and entity pages.
* Home respects deterministic release order.
* No user-facing sort.
* Search is prominent on Browse, compact from Home.
* “Why it matters” stays visible on cards.
* Trust label: Reviewed, defined precisely as reviewed against the linked source for clarity, relevance, and attribution.
* Relevance and trust remain separate.
* Lifecycle labels appear only when explicitly exported.
* No weekly-cadence promise.
* No historical filler.
* No dark mode, dashboard, map, account, alerting, or backend API.
* Implement as a portable static site in SJC_Intel first. Portfolio integration can wrap or relocate it later.

Use:

* tasks/17-silverleaf-brief-v0.md
* reports/17-silverleaf-brief-v0.md

Task 17 — Adopt and Build SilverLeaf Brief v0

Session

This is a new OpenCode agent session.

Work from:

/Users/buddy/projects/sjc_intel

This task adopts the final synthesized resident-facing design and begins implementation immediately.

Do not perform another broad UI study.

Do not reopen settled design choices unless repository evidence proves a technical incompatibility.

Required report

Write:

reports/17-silverleaf-brief-v0.md

Follow reports/README.md.

Mission

Turn the accepted SilverLeaf Brief design into durable repository authority and a functioning static v0 implementation.

This task must:

1. preserve the final UI design in one authoritative repository document;
2. reconcile it with existing UI and static-release documents;
3. avoid creating competing UI specifications;
4. implement or complete the static public release exporter required by the UI;
5. build the first working SilverLeaf Brief interface;
6. use realistic public-safe fixtures or generated release data;
7. preserve progressive enhancement and no-JavaScript readability;
8. implement resident-facing search and filtering;
9. implement the primary routes and components;
10. meet the stated accessibility and mobile requirements;
11. produce screenshots or locally inspectable proof where repository tooling supports it;
12. leave only editorial approval, real release generation, final polish, and deployment work.

The governing objective is:

Produce a credible, static, mobile-friendly SilverLeaf Brief v0 that a resident can browse and that Buddy can visually review before publication.

⸻

1. Required source material

Read at minimum:

README.md
README_INTERNAL.md
AGENTS.md
ROADMAP.md
docs/ARCHITECTURE.md
docs/publication_release_contract.md
docs/public_ui_v0_spec.md
docs/static_release_data_contract.md
docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md
reports/15-publication-readiness-review.md
reports/16-publication-foundation-and-ui-discovery.md
tasks/README.md
reports/README.md

Inspect:

scripts/
schemas/
registry/
data/
tests/
runtime/
deploy/

Inspect the actual publication implementation:

scripts/publication_common.py
scripts/publication_decision.py
scripts/select_publication_items.py
scripts/validate_publication_corpus.py
schemas/publication_decision.schema.yaml
data/publication_decisions/

Inspect Git and working-tree state before making changes.

Do not overwrite unrelated Task 12–16 work.

⸻

2. Accepted product decisions

These are locked for v0.

2.1 Product identity

Name:

SilverLeaf Brief

Tagline:

What changed around SilverLeaf—and why it matters.

Public value proposition:

SilverLeaf Brief turns reviewed local records and reporting into clear, source-linked updates for SilverLeaf residents.

2.2 Product character

The product is:

* a finite reviewed neighborhood briefing;
* source-forward;
* calm;
* editorial;
* resident-centered;
* static;
* mobile-first;
* accessible.

It is not:

* a breaking-news service;
* an emergency alert service;
* a government portal;
* a dashboard;
* a social network;
* an analytics tool;
* a real-time feed;
* an autonomous AI publication.

2.3 Primary resident questions

The UI must answer, in order:

1. What changed?
2. Why might it matter to me?
3. Does it apply directly to SilverLeaf, nearby, or countywide?
4. Where can I read the original source?

2.4 Navigation

Primary:

Latest
Browse
About

Secondary:

Data & Sources
Coverage & limitations
Report an issue

2.5 Routes

Required route model:

/
  Latest release
/browse
  Search and filters
/topic/{topic-id}
  Collection template filtered by topic
/place/{place-id}
  Collection template filtered by place
/entity/{entity-id}
  Collection template filtered by entity
/item/{public-item-id}
  Item detail
/about
  Product, methodology, review meaning, limitations
/sources
  Release provenance and source directory

Topic, place, and entity routes must reuse one collection-page implementation.

2.6 Home ordering

Render items in the deterministic order supplied by the release artifact.

Do not silently reorder by:

* source date;
* topic;
* relevance;
* inferred importance;
* lifecycle state.

2.7 Search and filters

Search is always visible on Browse.

Home may contain a compact search action but not a dominant search hero.

Search fields:

* title;
* summary;
* why it matters;
* topic labels;
* place labels;
* entity labels;
* source name.

Visible desktop filters:

* topic;
* relevance.

Secondary filters:

* place;
* entity.

Mobile filters use a bottom sheet.

No user-facing sort control in v0.

2.8 Card content

Every item card must show:

* one relevance label;
* one topic;
* title;
* summary;
* why it matters;
* source name;
* absolute source date;
* Reviewed indicator;
* Read update action;
* Original source action.

Limit visible metadata.

Do not display every topic, entity, or place.

2.9 Trust language

Public label:

Reviewed

Detail explanation:

A human reviewed this summary against the linked source for clarity, relevance, and attribution before publication.

Do not say:

* independently verified;
* verified truth;
* AI verified;
* official;
* guaranteed accurate.

2.10 Temporal truth

Use absolute, labeled dates.

Potential labels:

* Source published.
* Hearing date.
* Effective date.
* Published in SilverLeaf Brief.

Do not infer lifecycle from age.

Do not automatically label items stale after a fixed number of days.

Render lifecycle only when explicitly present in the public release.

Otherwise temporal status must appear in editorial wording.

2.11 Relevance labels

Use:

* In SilverLeaf.
* Near SilverLeaf.
* Countywide impact.

Do not merge relevance and review state.

2.12 Low volume

The first release may contain 5–15 items.

Do not add filler.

Do not include old items merely to make the site look populated.

Show:

* release date;
* actual item count;
* coverage statement;
* curated spacing.

2.13 Explicit non-goals

Do not implement:

* accounts;
* subscriptions;
* admin;
* live maps;
* alerts;
* semantic search;
* API;
* chat;
* comments;
* trending;
* confidence scores;
* infinite scroll;
* dark mode;
* onboarding modal;
* historical filler;
* source-type trust scores.

⸻

3. Consolidate the UI documentation

The repository currently contains:

docs/public_ui_v0_spec.md
docs/static_release_data_contract.md

Create one clear design authority or revise the existing UI specification so the accepted synthesis becomes authoritative.

Preferred approach:

docs/public_ui_v0_spec.md

remains the primary product/UI authority.

Update it to include the accepted decisions in this task.

Do not create a second competing full UI specification unless the current document cannot reasonably hold both product and implementation requirements.

docs/static_release_data_contract.md should remain authoritative for data/export semantics.

The UI document must link to the data contract.

Add a short status header:

Status: Accepted for v0 implementation
Product: SilverLeaf Brief

Document which earlier recommendations were intentionally rejected:

* dashboard;
* sort control;
* Active Now without explicit data;
* fixed weekly buckets;
* inferred stale state;
* dark mode;
* new backend fields required solely for UI;
* historical filler.

Update ROADMAP.md only to mark the design as accepted and implementation underway.

⸻

4. Resolve implementation location

Inspect the repository for existing frontend conventions.

The portfolio-site repository remains undiscovered.

Therefore, implement SilverLeaf Brief as a portable static application inside SJC_Intel.

Preferred location:

site/

A reasonable structure is:

site/
  index.html
  browse/
  about/
  sources/
  assets/
    css/
    js/
  data/

Dynamic item and collection rendering may use static route generation or a portable static fallback according to the existing project tooling.

Do not introduce a large framework without strong repository evidence.

Default preference:

* semantic HTML;
* CSS;
* minimal JavaScript;
* generated static pages;
* static JSON;
* no backend.

If a lightweight generator materially simplifies route generation, justify it in the report before adopting it.

Do not require Node unless it provides clear value and is documented.

The resulting site must be relocatable into a future portfolio repository or deployed independently as static assets.

⸻

5. Implement the static release exporter

Complete the §3B-G2 static exporter using:

docs/static_release_data_contract.md

Suggested command:

python3 scripts/build_static_release.py --release-id <release-id>

Support a dry-run or check mode.

Required outputs:

release.json
search-index.json
release-manifest.json

Required behavior:

* select only explicitly publication-approved items;
* use the publication selector;
* validate the complete corpus first;
* validate publication decisions;
* apply the public allowlist;
* exclude internal fields;
* preserve deterministic release order;
* include stable topic/place/entity/source identifiers;
* include source name and URL;
* include absolute date values;
* include explicit lifecycle only when present;
* produce release counts;
* produce source directory information;
* produce file checksums;
* produce schema/version identity;
* fail on incomplete required public fields;
* preserve rollback identity;
* never mark items published by itself.

Because no real items are approved yet, support:

1. real release mode, which may validly produce zero selected items;
2. fixture/demo mode using test fixtures or explicitly nonproduction sample data.

Demo data must never be confused with real published data.

Clearly label its output path and environment.

Suggested:

site/data/demo/
site/data/releases/{release-id}/

Add tests.

⸻

6. Content-quality validation

Add publication-time checks for every exported item.

Require:

* understandable title;
* summary;
* why-it-matters text;
* source name;
* source URL or explicit unavailable state;
* source date or explicit unavailable marker;
* at least one relevance/place relationship;
* no unexplained internal acronym in resident-facing fields;
* conditional wording for proposals;
* no internal fields;
* stable public ID.

The exporter should fail or exclude items lacking required resident-facing content.

Do not silently manufacture missing content.

Warnings may identify content needing editorial revision.

⸻

7. Build the static site shell

Implement:

* skip link;
* semantic header;
* desktop navigation;
* mobile bottom navigation;
* main landmark;
* footer;
* route-safe links;
* 404 page;
* accessibility metadata;
* responsive viewport configuration.

Primary navigation:

Latest
Browse
About

Footer:

Data & Sources
Coverage & limitations
Report an issue
Current release

Use no private local paths in public output.

⸻

8. Implement the design system

Typography

Use:

* Source Serif 4 for headings;
* Source Sans 3 for body/UI;

or approved local/system fallbacks when external font loading would harm privacy, portability, or offline behavior.

Do not commit font binaries.

Use a resilient fallback stack.

Colors

Use:

Page background: #F7F6F2
Surface: #FFFFFF
Primary text: #1F2522
Secondary text: #5B6560
Evergreen: #235B43
Link: #005F73
Border: #D9DED9
Why-it-matters background: #EDF5F0
Neutral badge: #EEF1EF
Focus ring: #005F73
Error: #A12828

Test actual contrast.

Do not assume compliance from the color values alone.

Layout

* Editorial single-column cards.
* Maximum content width approximately 1120px.
* Reading column approximately 760px.
* Mobile gutters 16px.
* No default shadows.
* No equal-height dashboard grid.
* No horizontal page scrolling.

Motion

* 120–180 ms.
* Minimal.
* Respect reduced motion.
* No scroll-triggered animation.

⸻

9. Implement Latest

Latest must contain:

1. product name;
2. tagline;
3. release date;
4. real item count;
5. trust statement;
6. populated topic shortcuts;
7. ordered item list;
8. coverage statement;
9. footer.

Trust statement:

Human-reviewed summaries with links to original sources. Not an official county or emergency-alert service.

Cards must contain the accepted anatomy.

Do not group Home by topic or relevance.

Do not add a featured item unless the release contract explicitly provides one.

Do not promise a weekly cadence.

⸻

10. Implement Browse

Browse must include:

* search;
* topic controls;
* relevance controls;
* place filter;
* entity filter;
* active filter chips;
* clear-all;
* result count;
* zero-results state;
* same item cards as Latest.

Query parameters:

q
topic
place
entity
scope

Behavior:

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

Base HTML must remain readable when JavaScript fails.

Use progressive enhancement.

⸻

11. Implement collection routes

Implement one reusable collection-page template for:

* topics;
* places;
* entities.

Do not create bespoke layouts.

Pages should show:

* label;
* result count;
* applicable related filters;
* item cards;
* empty state.

Do not invent:

* entity biographies;
* unsupported place descriptions;
* inferred timelines;
* taxonomy content not present in public data.

Valid empty routes may show a clear empty collection state.

Ordinary filter controls should hide zero-count options.

⸻

12. Implement item detail

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

1. working source URL;
2. missing/unavailable source URL.

Unavailable state:

The original source link is currently unavailable.

Do not remove the published item solely because a link later fails.

⸻

13. Implement About and Data & Sources

About

Include:

* what the product is;
* selection method;
* definition of Reviewed;
* coverage;
* noncoverage;
* release approach;
* corrections;
* link to Data & Sources.

Data & Sources

Include:

* current release metadata;
* source directory for the release;
* source types;
* how source links are handled;
* public data fields;
* excluded internal data;
* coverage limitations;
* correction/source-problem link.

Never expose:

* agent reasoning;
* candidate records;
* internal review notes;
* sensitivity rationale;
* dedupe metadata;
* logs;
* unpublished source proposals.

⸻

14. Implement mobile behavior

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

Filter sheet requirements:

* focus moves inside on open;
* focus is trapped;
* Escape closes;
* focus returns to trigger;
* selected count visible;
* Clear all;
* Show results action;
* screen-reader labeling.

⸻

15. Accessibility acceptance criteria

Meet WCAG 2.2 AA.

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

Where tooling supports it, run automated accessibility checks.

Document manual checks still required.

⸻

16. Implement failure and empty states

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

Do not leave blank sections.

Do not substitute one date for another.

Do not invent missing values.

⸻

17. Demo data and visual proof

Because production publication decisions are not yet recorded, create a clearly nonproduction demo release using realistic examples.

Use examples based on existing corpus categories:

* water shortage;
* school construction;
* CR 2209 connector;
* development hearing;
* local service or retail opening.

Demo items must be labeled and isolated as fixtures.

Do not present them as a real public release.

Provide a clear local preview command.

Examples:

python3 -m http.server

or a repository-appropriate equivalent.

Where feasible, produce visual screenshots or documented local routes for Buddy’s review.

Do not add screenshot binaries to Git unless repository convention supports them and they are clearly useful.

⸻

18. Testing

Add automated tests for:

Export

* deterministic output;
* public field allowlist;
* internal denylist;
* no unapproved items;
* no high-sensitivity items;
* checksums;
* release identity;
* missing required copy;
* broken source handling;
* demo isolation.

UI behavior

Use the lightest reasonable test strategy.

Test:

* route generation;
* card rendering;
* filter logic;
* query parsing;
* OR/AND semantics;
* search ranking;
* release-order tie breaking;
* zero-result behavior;
* unavailable source state;
* collection routes;
* no-JavaScript content presence.

Accessibility

Automate what the chosen stack supports.

At minimum validate HTML structure and key accessible labels.

⸻

19. Documentation

Update:

README.md

with a brief SilverLeaf Brief section and local preview instructions.

Update:

ROADMAP.md

with actual implementation status.

Update or create a concise UI operator/build guide only if needed.

Do not duplicate the full design specification.

Document:

* build command;
* preview command;
* release input;
* demo mode;
* output directory;
* validation;
* portability;
* deployment-neutral static nature.

⸻

20. Scope restrictions

Do not:

* approve publication decisions;
* mark items published;
* modify the review queue;
* silently change SilverLeaf scope;
* add a database;
* add backend APIs;
* deploy;
* modify Ivy;
* configure VPS;
* add analytics;
* add cookies;
* add external behavioral tracking;
* add third-party embeds;
* add font binaries;
* commit;
* push.

Do not block implementation merely because the portfolio-site repository remains undiscovered.

Build the portable static v0 in SJC_Intel.

⸻

21. Required validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/validate_publication_corpus.py
python3 scripts/portability_check.py
git diff --check
git status --short

Run all UI/export-specific tests and build commands.

Record:

* output size;
* JavaScript size where applicable;
* search-index size;
* route count;
* demo item count;
* accessibility test results;
* manual review URLs.

⸻

22. Required report structure

Write reports/17-silverleaf-brief-v0.md with:

1. Executive result
2. Starting Git state
3. Design decisions adopted
4. UI documentation consolidation
5. Implementation location and stack
6. Static exporter
7. Content-quality validation
8. Demo-release strategy
9. Generated routes
10. Latest page
11. Browse/search/filter behavior
12. Collection routes
13. Item detail
14. About
15. Data & Sources
16. Mobile behavior
17. Accessibility
18. Empty and failure states
19. Design-system implementation
20. Files changed
21. Test coverage
22. Validation commands and results
23. Output sizes
24. Local preview instructions
25. Visual-review notes
26. Remaining editorial dependencies
27. Remaining deployment dependencies
28. Remaining UI polish
29. Risks and unresolved issues
30. Final Git status
31. Final task status

Use the established final-status vocabulary.

⸻

23. Success criteria

This task is complete when:

1. the synthesized design is preserved as repository authority;
2. old UI recommendations no longer compete with the accepted design;
3. a static release exporter exists;
4. public output is validated and deterministic;
5. a portable SilverLeaf Brief site exists;
6. Latest works;
7. Browse works;
8. search works;
9. topic/place/entity filters work;
10. item detail works;
11. About works;
12. Data & Sources works;
13. mobile behavior is implemented;
14. accessibility requirements are materially implemented;
15. no-JavaScript content remains readable;
16. demo data is isolated from production;
17. Buddy can preview a coherent v0;
18. no item is approved or published;
19. remaining work is limited to editorial approval, real release generation, polish, deployment, and optional later enhancements.

Use this new-session instruction:

New OpenCode session.
Work from:
/Users/buddy/projects/sjc_intel
Read and execute:
tasks/17-silverleaf-brief-v0.md
Adopt the finalized SilverLeaf Brief design, consolidate it into the repository’s UI authority, implement the static release exporter, and build a portable static v0 site with Latest, Browse, collection routes, item detail, About, and Data & Sources.
Write the report to:
reports/17-silverleaf-brief-v0.md
Do not approve or publish items, modify review decisions, modify Ivy, deploy, add a database or backend API, configure VPS services, commit, or push.