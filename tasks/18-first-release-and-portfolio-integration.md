Proceed with a new OpenCode session for the final pre-publication pass.

Use:

* tasks/18-first-release-and-portfolio-integration.md
* reports/18-first-release-and-portfolio-integration.md

Task 18 — First Real Release Preparation and Portfolio Integration

Session

This is a new OpenCode agent session.

Work primarily from:

/Users/buddy/projects/sjc_intel

Locate and inspect the portfolio website repository using existing SJC, Ivy, Git, shell-history-safe project indexes, or /Users/buddy/projects/ structure.

Do not guess its location or framework.

Inspect Ivy Control VPS read-only only where necessary to understand deployment ownership:

/Users/buddy/projects/ivy-control-vps

Required report

Write:

reports/18-first-release-and-portfolio-integration.md

Follow reports/README.md.

Mission

Move SilverLeaf Brief from a working demo into a decision-ready real v0 release and determine the exact portfolio integration path.

This task must:

1. visually and functionally review the Task 17 UI;
2. inspect the actual corpus and publication queue;
3. finalize the file-backed SilverLeaf scope registry needed for publication;
4. prepare a small, coherent first real release candidate set;
5. identify every editorial decision still requiring Buddy;
6. prepare publication-decision commands without executing final approvals;
7. prove the real release exporter against the selected candidates in check/dry-run form;
8. locate and inspect the portfolio repository;
9. determine whether SilverLeaf Brief should be embedded, linked, copied as static output, or independently deployed;
10. prepare the exact integration implementation plan;
11. resolve minor v0 UI defects that do not require product-owner judgment;
12. leave Buddy and GPT with one short approval packet;
13. leave the project one bounded implementation/deployment task from publication.

The governing objective is:

Replace demo assumptions with real SJC evidence, prepare the first reviewed SilverLeaf release, and define the exact path for presenting it through Buddy’s portfolio.

⸻

1. Required source material

Read:

README.md
README_INTERNAL.md
AGENTS.md
ROADMAP.md
docs/public_ui_v0_spec.md
docs/static_release_data_contract.md
docs/publication_release_contract.md
docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md
reports/15-publication-readiness-review.md
reports/16-publication-foundation-and-ui-discovery.md
reports/17-silverleaf-brief-v0.md
tasks/README.md
reports/README.md

Inspect:

registry/
schemas/
data/intel_items/
data/source_events/
data/review_queue/
data/publication_decisions/
data/index/
scripts/
site/
tests/

Run the Task 17 preview and inspect the rendered site.

⸻

2. Verify current state

Report:

* branch and HEAD;
* remote synchronization;
* dirty, staged, and untracked files;
* Task 12–17 artifacts still uncommitted;
* test count;
* publication-validator state;
* current publication decisions;
* review queue counts;
* SilverLeaf relevance counts;
* current generated demo;
* real release eligibility count;
* portfolio repository discovery status.

Do not discard, commit, or push.

⸻

3. Visual and functional review of SilverLeaf Brief

Build and preview the Task 17 demo site.

Inspect at minimum:

* Latest desktop;
* Latest mobile;
* Browse desktop;
* Browse mobile;
* filtered Browse;
* search results;
* zero-results state;
* item detail desktop;
* item detail mobile;
* topic collection;
* place collection;
* entity collection;
* About;
* Data & Sources;
* empty release;
* 404.

Use real browser inspection where repository tooling supports it.

Evaluate:

* resident comprehension in the first ten seconds;
* card density;
* visual hierarchy;
* mobile navigation;
* filter usability;
* source prominence;
* date clarity;
* Reviewed meaning;
* relevance labels;
* typography;
* spacing;
* source table;
* footer;
* demo labeling;
* accessibility;
* broken layouts;
* text overflow;
* external-link behavior.

Implement minor objective fixes where justified.

Do not redesign the accepted product.

Report all visual changes with before/after reasoning.

⸻

4. Finalize the SilverLeaf scope registry

Use the existing scope decision packet, registries, tracked entities, interest filters, intelligence items, and source evidence.

Implement the minimum launch-ready SilverLeaf scope representation.

It should support:

* canonical SilverLeaf identity;
* aliases;
* parent geography;
* neighborhoods where verified;
* directly serving roads and corridors;
* materially adjacent corridors;
* schools;
* utilities;
* tracked developments;
* community businesses and services;
* inclusion rules;
* exclusion rules;
* direct / nearby / countywide-material relevance;
* needs_review;
* evidence source;
* verification status.

Do not invent precise boundaries or GIS facts.

Do not require PostGIS.

Distinguish:

verified
inferred
editorial-policy
needs-review

Use stable IDs.

Add machine validation and tests.

Update relevant documentation without creating another competing scope document.

⸻

5. Inspect actual publication candidates

Inspect the real review queue and intelligence corpus.

Identify a bounded first-release candidate set, preferably around 5–15 items.

Assess each candidate for:

* SilverLeaf relevance;
* resident usefulness;
* freshness;
* verification;
* source authority;
* source URL;
* source date;
* title clarity;
* summary clarity;
* why-it-matters quality;
* sensitivity;
* duplication;
* lifecycle wording;
* unresolved acronyms;
* publication-contract compliance.

Prioritize a coherent mix such as:

* utilities/water;
* roads/traffic;
* schools;
* development/zoning;
* community/services.

Do not include categories merely for balance if the records are weak.

Do not automatically include public-safety material.

⸻

6. Prepare the first-release editorial packet

For every proposed first-release item include:

* item ID;
* title;
* source;
* source URL;
* source date;
* observed date;
* topic;
* places;
* entities;
* proposed relevance label;
* review status;
* sensitivity;
* publication-contract status;
* resident value;
* unresolved issue;
* exact recommended action.

Classify each:

READY_TO_APPROVE
READY_AFTER_COPY_EDIT
READY_AFTER_SOURCE_CHECK
DEFER
EXCLUDE
BUDDY_DECISION

Provide the proposed release order.

Explain why that order serves a resident.

Do not approve the items.

⸻

7. Prepare copy edits

For candidates classified READY_AFTER_COPY_EDIT, propose exact public-facing:

* title;
* summary;
* why-it-matters;
* temporal wording;
* relevance label;
* lifecycle label only when supported.

Do not alter authoritative source facts.

Remove unexplained acronyms.

Keep proposals conditional.

Do not make claims broader than the source supports.

Preserve both original and proposed copy in the report.

Repository mutation is allowed only if the existing publication-decision model explicitly supports a separate public-summary override without altering the source intelligence record.

Otherwise provide proposed copy in the report only.

⸻

8. Prepare publication decisions

Prepare exact dry-run commands for each candidate.

Example:

python3 scripts/publication_decision.py approve \
  --item-id <ITEM_ID> \
  --reviewer Buddy \
  --rationale "<RATIONALE>"

Use the actual command interface.

Do not execute final approvals.

For rejected or deferred candidates, prepare the corresponding commands.

Group commands into:

* proposed approvals;
* proposed deferrals;
* proposed exclusions;
* source-check blockers.

Buddy should be able to approve the release by reviewing a short table and then authorizing one bounded command packet.

⸻

9. Prove the real release path

Without making approvals, prove:

1. current real release selection;
2. expected exclusions;
3. candidate eligibility after proposed decisions, using fixtures, simulation, or nonmutating preview;
4. static export check mode;
5. site generation from an empty or simulated real release;
6. rollback identity;
7. release-manifest validation;
8. search-index validation;
9. no internal data leakage.

Do not fake a production release.

Clearly separate:

* current real state;
* simulated post-approval state;
* demo state.

⸻

10. Determine first-release parameters

Recommend one specific v0 policy for Buddy and GPT to approve.

Include:

* release ID;
* publication date handling;
* item count;
* release window;
* countywide-material-impact rule;
* treatment of old but ongoing items;
* treatment of proposals;
* treatment of sensitive items;
* public-safety inclusion or exclusion;
* ordering rule;
* withdrawal procedure;
* correction procedure;
* cadence language.

Do not promise weekly publication unless operationally guaranteed.

⸻

11. Locate and inspect the portfolio repository

Find the repository that owns Buddy’s public portfolio website.

Inspect read-only:

* exact path;
* remote;
* framework;
* branch;
* working tree;
* route structure;
* project/case-study conventions;
* static asset handling;
* static JSON handling;
* deployment target;
* build commands;
* styling system;
* navigation;
* project metadata;
* existing public projects;
* whether subdirectory hosting works;
* whether an independent static site can be linked;
* whether route rewrites are available.

Do not modify the portfolio repository.

If multiple candidate repos exist, compare them and identify the authority.

⸻

12. Decide the integration architecture

Recommend exactly one v0 integration approach.

Evaluate:

A. Embed SilverLeaf Brief inside the portfolio site

B. Deploy SilverLeaf Brief independently and link from the portfolio

C. Copy generated static output into a portfolio-controlled public directory

D. Use another established portfolio convention

Assess:

* speed to publication;
* deployment complexity;
* portability;
* search and routes;
* static asset paths;
* maintenance;
* release updates;
* repository boundaries;
* portfolio presentation;
* failure isolation;
* future reuse.

Choose one.

Do not hedge.

The preference should be the smallest credible route to public v0.

⸻

13. Prepare the portfolio case-study specification

Define what the portfolio page should communicate.

Required story:

Agent-led intelligence architecture
→ St. Johns County implementation
→ SilverLeaf resident product
→ reviewed static release
→ bounded VPS automation later

Specify:

* project title;
* one-sentence description;
* short overview;
* problem;
* solution;
* architecture;
* resident UI;
* evidence and review;
* reusable patterns;
* Mac/VPS split;
* limitations;
* repository link;
* live demo link;
* screenshots;
* technology;
* validation proof;
* lessons learned.

Do not overclaim:

* multi-domain platform;
* live automation;
* real-time alerts;
* autonomous publication;
* production PostgreSQL;
* completed VPS deployment.

⸻

14. Prepare screenshots and demo evidence

Identify the minimum portfolio evidence:

* Latest desktop;
* Latest mobile;
* Browse/filter view;
* item detail;
* architecture diagram;
* optional workflow diagram.

Where possible, generate current screenshots to a temporary directory.

Do not commit them unless repository conventions and the selected integration architecture support doing so.

Specify:

* dimensions;
* crop;
* page state;
* demo versus production labeling;
* alt text;
* captions.

⸻

15. Commit-readiness preflight

The repository contains substantial uncommitted work.

Prepare a commit plan, but do not commit.

Classify all current changes into logical groups such as:

1. weekly operations and bundle/import;
2. publication foundation;
3. SilverLeaf scope;
4. static export and site;
5. tests;
6. docs and reports;
7. generated demo output;
8. durable data updates;
9. artifacts that should remain ignored or uncommitted.

For each group provide:

* exact paths;
* purpose;
* validation;
* commit type and proposed message;
* whether it belongs in Git;
* whether generated output should be tracked;
* dependency order.

Identify:

* stale artifacts;
* duplicate outputs;
* accidental generated files;
* private material;
* large files;
* line-ending issues;
* permission issues;
* missing .gitignore coverage.

Do not delete anything.

⸻

16. Ivy handoff note

SJC static publication does not require VPS deployment.

Confirm the separation:

Public v0
- static release
- portfolio deployment
- no VPS dependency
Operational follow-up
- Ivy admission
- VPS deployment
- scheduled collection
- bundle transfer
- Mac review

Prepare a concise handoff for Strong Codex/Ivy stating:

* public release status;
* exact reviewed Git SHA requirement;
* deployment-independent static architecture;
* minimum SJC VPS workload;
* no corpus PostgreSQL;
* no UI backend;
* temporary ingest data;
* expected bundle lifecycle;
* remaining capacity and scheduling proof.

Do not perform Ivy work.

⸻

17. Approved modifications

This task may modify SJC files needed to:

* finalize the SilverLeaf scope registry;
* validate the registry;
* fix objective UI defects;
* improve static exporter validation;
* add tests;
* clarify public documentation;
* update roadmap status;
* improve portfolio-neutral deployment instructions.

Do not:

* approve publication decisions;
* mark items published;
* execute real release publication;
* modify the portfolio repository;
* deploy;
* modify Ivy;
* commit;
* push;
* activate VPS services;
* add a database;
* add analytics.

⸻

18. Required validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/validate_publication_corpus.py
python3 scripts/portability_check.py
python3 scripts/build_static_release.py \
  --release-id SJC-REL-2026-08-001 \
  --check \
  --reviewer Buddy
python3 scripts/build_static_release.py \
  --release-id SJC-REL-DEMO-20260804 \
  --demo
python3 scripts/build_static_site.py --list-routes
git diff --check
git status --short

Run browser-based visual checks if available.

Record:

* test count;
* route count;
* current eligible count;
* proposed candidate count;
* output sizes;
* screenshot locations;
* portfolio repository facts.

⸻

19. Required report structure

Write reports/18-first-release-and-portfolio-integration.md with:

1. Executive result
2. Starting SJC state
3. Task 17 visual review
4. UI fixes implemented
5. SilverLeaf scope registry
6. Registry validation
7. Review queue and corpus summary
8. First-release candidate set
9. Proposed release order
10. Candidate copy edits
11. Exclusions and deferrals
12. Buddy/GPT decision table
13. Proposed publication commands
14. Real-release dry-run evidence
15. Simulated post-approval evidence
16. Recommended v0 release policy
17. Portfolio repository identified
18. Portfolio architecture and deployment
19. Recommended integration approach
20. Portfolio case-study specification
21. Screenshot plan and evidence
22. Commit-readiness preflight
23. Proposed commit groups
24. Ivy handoff
25. Files changed
26. Validation results
27. Remaining Buddy actions
28. Remaining medium-agent work
29. Remaining deployment work
30. Risks and unresolved issues
31. Final Git status
32. Final task status

Use the established status vocabulary.

⸻

20. Success criteria

This task is complete when:

1. Buddy can inspect a polished v0;
2. the SilverLeaf scope registry exists and validates;
3. a small real first-release candidate set is proposed;
4. every candidate has a clear recommendation;
5. exact publication commands are prepared but not executed;
6. the post-approval release path is proven nonmutatingly;
7. the portfolio repository is identified;
8. one integration architecture is selected;
9. the portfolio case-study content is specified;
10. screenshot requirements are clear;
11. the dirty repository has a safe commit plan;
12. static publication is explicitly independent of VPS work;
13. remaining work is limited to Buddy approval, bounded release generation, integration implementation, deployment, and commit/push.

Use this session instruction:

New OpenCode session.
Work primarily from:
/Users/buddy/projects/sjc_intel
Read and execute:
tasks/18-first-release-and-portfolio-integration.md
Visually review the working SilverLeaf Brief v0, finalize the launch-ready SilverLeaf scope registry, inspect the real corpus, prepare a small first-release editorial packet and exact nonexecuted publication commands, locate the portfolio repository, select the integration architecture, and prepare the commit/deployment path.
Write the report to:
reports/18-first-release-and-portfolio-integration.md
Do not approve or publish items, modify the portfolio repository, modify Ivy, deploy, commit, push, or activate VPS services.
