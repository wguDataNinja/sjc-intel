Task 16 — Publication Foundation, Resident UI Discovery, and Ivy Codex Preparation

Session

This is a new OpenCode agent session.

Work primarily from:

/Users/buddy/projects/sjc_intel

Inspect Ivy Control VPS read-only at:

/Users/buddy/projects/ivy-control-vps

Inspect the portfolio-site repository only if its location is discoverable from current repository or Ivy authority documents. Do not modify another repository during this task.

Required report

Write:

reports/16-publication-foundation-and-ui-discovery.md

Follow reports/README.md.

Task character

This is a substantial medium-strength implementation and discovery task.

It has four connected purposes:

1. implement the publication foundation that no longer requires Buddy’s architectural input;
2. inspect the actual SJC corpus from a SilverLeaf resident’s perspective;
3. determine the minimum useful v0 UI and the exact data contract it requires;
4. prepare a detailed Strong Codex packet for Ivy Control VPS consolidation, VPS optimization, reusable onboarding, and rapid application to the Reckless Ben repository.

Do not make final editorial publication decisions on Buddy’s behalf.

Do not deploy, publish, modify Ivy, alter VPS state, configure credentials, enable timers, or mark items published.

⸻

1. Mission

Move SJC_Intel from publication planning into publication-capable implementation.

This task must:

1. implement the file-backed publication contract;
2. add complete corpus validation for publication-relevant records;
3. add explicit human-controlled publication decisions;
4. implement a deterministic publication selector;
5. preserve review, sensitivity, provenance, and duplicate protections;
6. inspect the real intelligence corpus and review queue as though the agent were a SilverLeaf resident trying to understand what matters locally;
7. identify what residents would reasonably want to browse, search, filter, and understand;
8. define the smallest credible v0 interface;
9. define the exact static release/export contract that UI agents will consume;
10. identify the SilverLeaf scope and editorial facts still requiring Buddy and GPT;
11. inspect the portfolio repository context needed for later UI implementation;
12. reconstruct the SJC-to-Ivy onboarding lessons already identified;
13. prepare a high-quality Strong Codex task specification for consolidating Ivy documentation and operational workflows;
14. ensure that Strong Codex can use SJC as the completed reference case and prepare Ivy for rapid onboarding of Reckless Ben;
15. leave one clear next sequence from current state to public v0.

The governing objective is:

Complete the publication foundation now, define the resident-facing product from the actual data, and prepare Strong Codex to simplify Ivy into a reusable operations platform before the next repository is onboarded.

⸻

2. Accepted decisions

2.1 Product

SJC_Intel is an agent-led local intelligence system.

St. Johns County is the first domain.

SilverLeaf is the first public product lens.

2.2 Launch

The initial public release should be:

* static or statically generated;
* human-reviewed;
* source-attributed;
* SilverLeaf-focused;
* searchable;
* filterable;
* understandable to a resident;
* useful even when the VPS is unavailable.

2.3 Publication authority

candidate
≠ verified
≠ publication-approved
≠ published

Human publication approval is required.

The VPS never publishes.

The Mac remains authoritative for:

* corpus;
* review state;
* publication decisions;
* release generation;
* full history;
* restore.

2.4 VPS and PostgreSQL

SJC PostgreSQL remains:

DORMANT_FUTURE_READY

Do not activate PostgreSQL.

Do not make the VPS a corpus authority.

The future VPS role is bounded execution, temporary bundles, health, scheduling, and possibly minimal public UI-serving state if later justified.

2.5 Backup

Backup implementation is deferred to a later portfolio-wide Ivy effort.

Do not implement backup automation.

Preserve the documented backup requirements and identify any dependency that Strong Codex must carry into Ivy.

2.6 Deferred launch work

Do not make these launch dependencies:

* live incidents;
* PostGIS;
* semantic search;
* subscriptions;
* public API;
* user accounts;
* autonomous publication;
* corpus PostgreSQL;
* universal Hermes runtime;
* full multi-domain generalization.

⸻

3. Required source material

3.1 SJC authority

Read at minimum:

README.md
README_INTERNAL.md
AGENTS.md
ROADMAP.md
BACKLOG.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md
docs/ARCHITECTURE.md
docs/publication_release_contract.md
docs/weekly_operational_contract.md
docs/weekly_operator_guide.md
docs/weekly_scheduling.md
docs/backup-restore.md
docs/retention.md
docs/postgresql_adapter.md
docs/data_model.md
docs/taxonomy.md
tasks/README.md
reports/README.md

Read recent reports:

reports/08-codex-redesign-1.md
reports/09-codex-redesign-2.md
reports/10-ivy-operational-admission.md
reports/11-operational-admission-continuation.md
reports/12-weekly-operations-implementation-prep.md
reports/13-candidate-to-corpus-import.md
reports/14-publish-readiness-and-vps-onboarding.md
reports/15-publication-readiness-review.md

Inspect actual implementation and data in:

schemas/
registry/
scripts/
data/
tests/
runtime/
deploy/
prompts/
logs/
tasks/
reports/
db/

3.2 Ivy Control VPS

Inspect read-only:

README.md
PORTFOLIO_WORKING_MEMORY.md
docs/REPOSITORY_CONTROL_MODEL.md
docs/VPS_ADMISSION_CHECKLIST.md
docs/VPS_INVENTORY.md
docs/DATABASE.md
docs/PORTFOLIO_CONVENTIONS.md
docs/HEALTH_CONTRACT.md
docs/DATA_LIFECYCLE_STANDARD.md
docs/BACKUP_MANIFEST_STANDARD.md
agents/VPS_ORCHESTRATION.md
repos/sjc-intel/CONTROL.md

Also inspect SJC-specific Ivy evidence:

repos/sjc-intel/
_internal/outbox/
_internal/logs/
_internal/generated/

Search Ivy for:

sjc
sjc-intel
SilverLeaf
publication
admission
release gate
weekly
bundle
receipt
acknowledgement
retention
storage
backup
Hermes
Reckless Ben
reckless-ben

3.3 Portfolio repository

If discoverable, inspect read-only:

* framework;
* routes;
* data-loading pattern;
* deployment method;
* static asset conventions;
* search implementation;
* design system;
* current project/case-study pages;
* expected build artifacts.

If not discoverable, report the exact missing context without inventing it.

⸻

4. Verify current state

Report:

* branch;
* HEAD;
* remote status;
* ahead/behind;
* working-tree state;
* staged state;
* current tests;
* current review queue counts;
* publication-decision artifacts;
* release artifacts;
* SilverLeaf registry state;
* current public README/architecture/license;
* Task 15 changes;
* any conflict between current files and report 15;
* whether prior task outputs are committed;
* whether the repository is safe for a medium implementation session.

Do not discard unrelated work.

Do not commit or push.

⸻

5. Implement the publication-decision model

Use docs/publication_release_contract.md as the authority.

Implement the smallest durable file-backed representation for explicit publication decisions.

The model must support:

* item ID;
* publication status;
* reviewer;
* decision timestamp;
* decision rationale;
* release eligibility;
* sensitivity review;
* public summary override, if approved by the contract;
* withdrawn status;
* withdrawal reason;
* superseded item;
* source attribution confirmation;
* SilverLeaf relevance decision;
* origin review status;
* audit history or append-safe decision record.

Required publication statuses should follow the contract and existing vocabulary.

Do not silently invent conflicting terminology.

The implementation must ensure:

verified

does not automatically become:

publication_approved

Prefer a separate publication-decision registry or release-selection artifact over rewriting all legacy intelligence items unless the contract clearly requires item-level fields.

Add machine validation and tests.

⸻

6. Implement complete corpus validation

Extend the existing validator or add a clearly named publication/corpus validator.

It must validate actual records, not only schema files.

At minimum validate:

* item ID format;
* item ID uniqueness;
* source ID existence;
* source-event linkage policy;
* source URL presence and format;
* observed/source timestamps;
* required evidence;
* dedupe fingerprint presence;
* enum values;
* sensitivity;
* review status;
* publication-decision references;
* entity references;
* community/place references;
* topic references;
* public-field safety;
* internal-only field exclusion;
* canonical/superseded relationships;
* duplicate or repeated IDs;
* release eligibility;
* SilverLeaf relevance state;
* legacy exceptions.

The validator must produce:

* deterministic output;
* machine-readable summary;
* human-readable summary;
* failure counts;
* warning counts;
* exact item IDs;
* nonzero exit status for blocking errors;
* a documented treatment for legacy records.

Do not require immediate normalization of all historical records when an explicit legacy exception or exclusion is safer.

Add tests using real-shaped fixtures.

⸻

7. Implement the publication selector

Implement a deterministic selector that produces a preview of publication-eligible items.

Suggested command:

python3 scripts/select_publication_items.py --release-id <id> --check

Use repository conventions if another command shape is better.

The selector must require:

* verified review status;
* explicit publication approval;
* allowed sensitivity;
* valid source attribution;
* non-withdrawn state;
* non-superseded canonical record;
* valid SilverLeaf relevance decision;
* public-safe projection;
* inclusion within the configured release window;
* explicit handling of medium-sensitivity items.

It must exclude by default:

* pending items;
* high-sensitivity items;
* human-review-required unresolved items;
* rejected noise;
* archived-only items;
* duplicates;
* incomplete attribution;
* invalid URLs;
* internal-only artifacts;
* missing SilverLeaf decision;
* withdrawn items.

The selector should produce:

* selected item IDs;
* excluded item IDs;
* exclusion reasons;
* counts by source/topic/status;
* deterministic ordering;
* no mutations in --check mode.

Do not mark anything published.

⸻

8. Implement publication-decision operator tooling

Add the smallest safe human decision command.

Suggested operations:

python3 scripts/publication_decision.py approve --item-id <id>
python3 scripts/publication_decision.py reject --item-id <id>
python3 scripts/publication_decision.py defer --item-id <id>
python3 scripts/publication_decision.py withdraw --item-id <id>

The exact interface may differ.

The tool must:

* require explicit item ID;
* show current review and sensitivity state;
* show source URL;
* show SilverLeaf relevance;
* show dry-run diff;
* require reviewer identity;
* require rationale;
* validate before mutation;
* preserve prior decisions;
* prevent accidental bulk approval;
* reject invalid state transitions;
* remain idempotent;
* preserve an audit trail;
* never publish or create a release directly.

Add tests.

⸻

9. Inspect the actual data as a SilverLeaf resident

This is not a generic UX brainstorm.

Read the actual intelligence items, review queue, source events, tracked entities, communities, taxonomy, and publication candidates.

Adopt this working perspective:

I live in or near SilverLeaf. I want a fast, understandable way to see what may affect my household, commute, utilities, schools, development, neighborhood services, and local community.

Evaluate the real corpus for resident value.

Determine:

* what information is genuinely useful;
* what is too countywide;
* what is too bureaucratic;
* what is stale;
* what needs context;
* what topics residents would browse;
* what entities residents would follow;
* what places/corridors matter;
* what date context matters;
* which source types need explanation;
* what should be summarized;
* what should link directly to source records;
* what should remain excluded.

Inspect at least:

* verified items;
* pending SilverLeaf items;
* utility items;
* road/transportation items;
* development/zoning items;
* school items;
* government decisions;
* SJSO/public-safety items;
* community/business items;
* source proposals.

Do not make final publication decisions.

Prepare evidence-backed UI recommendations from the actual records.

⸻

10. Define the resident-facing information architecture

Recommend the minimum useful v0.

At minimum evaluate:

Home/latest view

Should answer:

* What changed recently?
* Why might it matter?
* When did it happen?
* Is it verified?
* What is the source?

Browse by topic

Likely categories may include:

* roads and traffic;
* utilities and water;
* development and zoning;
* schools;
* local government;
* community and amenities;
* public safety, if approved.

Use actual taxonomy and corpus evidence rather than inventing categories.

Browse by place

Possible dimensions:

* SilverLeaf;
* neighborhoods;
* CR 210 corridor;
* schools;
* roads;
* nearby developments.

Use actual registry evidence.

Browse by entity

Possible entities:

* utility providers;
* schools;
* county departments;
* developers;
* roads/corridors;
* community businesses.

Search

Define:

* searchable fields;
* ranking expectations;
* result snippets;
* filter interaction;
* empty states;
* source/date display.

Item detail

Define:

* title;
* plain-language summary;
* why it matters;
* affected place;
* topic;
* entity;
* source;
* source date;
* review date;
* publication date;
* verification level;
* limitations;
* related items.

Methodology/limitations

Explain:

* public sources;
* human review;
* periodic updates;
* not emergency alerts;
* not complete county coverage;
* source links remain authoritative.

⸻

11. Produce a v0 UI specification

Create a durable UI/product specification in the location most consistent with repository conventions.

Suggested:

docs/public_ui_v0_spec.md

Do not create it if an existing public-product spec should be extended instead.

The specification should include:

* target user;
* primary resident questions;
* page list;
* page hierarchy;
* navigation;
* search;
* filters;
* sort behavior;
* item cards;
* item detail;
* methodology;
* empty/error states;
* mobile behavior;
* accessibility;
* data fields;
* content rules;
* public claims;
* explicit non-goals;
* examples based on actual items;
* acceptance criteria.

Keep the v0 intentionally small.

Do not design:

* accounts;
* subscriptions;
* admin UI;
* live maps;
* real-time alerts;
* editing;
* personalization.

⸻

12. Define the static UI data contract

Based on the actual resident-facing specification, define the release data needed by the UI.

At minimum specify:

release-manifest.json
release.json
search-index.json

Or equivalent names consistent with current contracts.

Define exact public fields.

Potential release item fields:

* public item ID;
* title;
* summary;
* why-it-matters;
* source name;
* source URL;
* source date;
* published date;
* topic IDs;
* entity IDs;
* place IDs;
* sensitivity display rule;
* verification display;
* related item IDs;
* release ID.

Define:

* stable filter IDs;
* deterministic ordering;
* search normalization;
* public allowlist;
* internal denylist;
* release version;
* rollback identity;
* validation;
* file-size expectations;
* client-side caching;
* no-results behavior.

This contract should be implementable in the next static-export task without architectural decisions.

Do not build the final exporter unless the publication foundation makes it safe and the remaining scope is small enough to complete coherently.

⸻

13. SilverLeaf scope decision packet

Task 15 identified the scope registry as a blocker.

Prepare the decision-ready input for Buddy and GPT.

Include:

* known neighborhoods;
* aliases;
* likely access roads;
* likely serving schools;
* utilities;
* nearby entities;
* tracked businesses/services;
* inclusion rules;
* exclusion rules;
* adjacency rules;
* countywide-material-impact rule;
* needs_review cases;
* source provenance for each proposed scope element.

Distinguish:

* repository-verified facts;
* inferred items;
* missing authoritative sources;
* editorial choices.

Do not silently treat inferred geography as verified.

The report should allow Buddy and GPT to make the remaining scope decisions without reading the entire corpus.

⸻

14. Editorial packet update

Using Task 15 as the baseline, update the discussion packet only where deeper implementation/data inspection provides new evidence.

Include:

* candidate first-release items;
* stronger exclusion reasons;
* possible replacements for weak candidates;
* freshness options;
* countywide relevance rule;
* crime/public-safety recommendation;
* source-date versus publish-date display;
* likely first-release size;
* gaps that still block a credible release.

Do not approve or publish items.

⸻

15. Portfolio-site context discovery

If the portfolio repository is discoverable, inspect it read-only and report:

* path;
* framework;
* deployment;
* project page structure;
* data-loading pattern;
* static JSON support;
* client-side search options;
* build/deploy commands;
* design conventions;
* responsive layout;
* likely integration path;
* whether SJC UI belongs inside the portfolio repo or as a separately deployed static app.

If it is not discoverable, prepare the exact context-gathering packet for the next agent.

Do not modify the portfolio repository.

⸻

16. Ivy retrospective consolidation

Use Task 15’s findings as the starting point.

Do not redo the entire retrospective.

Extract the durable notes that Strong Codex needs.

The Strong Codex packet must explain:

What happened with SJC

* SJC matured substantially before Ivy gate tracking caught up;
* GitHub publication and operational design happened partly outside formal Ivy updates;
* CONTROL.md became stale;
* RELEASE_GATES.md was missing;
* SJC tasks/reports accumulated implementation history that Ivy should not duplicate;
* Ivy owned the right conceptual concerns but did not consistently receive state transitions;
* bundle/import/receipt/prune patterns emerged in SJC and should become Ivy standards;
* backup disposition, task declarations, and offboarding need stronger generic treatment;
* documentation sprawl made authority harder to follow.

Ownership model

Strong Codex should preserve:

Project repositories own products and implementation.
Ivy owns admission and operations.

Project repositories own:

* roadmap;
* tasks;
* reports;
* domain code;
* schemas;
* tests;
* editorial workflow;
* release artifacts.

Ivy owns:

* portfolio admission;
* control records;
* release gates;
* deployment;
* exact-SHA authority;
* scheduling;
* Hermes runtime;
* systemd;
* secrets;
* VPS capacity;
* PostgreSQL standards;
* backup disposition;
* health;
* rollback;
* operational evidence;
* activation;
* offboarding.

Documentation-sprawl problem

Strong Codex must inspect and consolidate overlapping Ivy authorities.

Potential overlap includes:

* working memory;
* repository-control model;
* VPS admission checklist;
* portfolio conventions;
* database docs;
* lifecycle docs;
* backup manifest docs;
* per-repo control files;
* per-repo release gates;
* private runbook;
* onboarding evidence.

The goal is not fewer documents at any cost.

The goal is:

* one authority per concern;
* clear entrypoint;
* clear per-repo record;
* clear gate evidence;
* no duplicated task tracking;
* no stale next-task state spread across many files;
* no project implementation history copied into Ivy.

⸻

17. Prepare the Strong Codex task specification

The Task 16 report must include a full proposed Strong Codex task specification suitable for a later task file.

The task should cover:

Ivy documentation consolidation

* inventory all active authorities;
* identify conflicts and duplicates;
* define one authority hierarchy;
* consolidate or deprecate documents;
* preserve private/public boundaries;
* reduce stale state;
* define what belongs in per-repo control records;
* define what belongs in shared standards;
* avoid tracking project tasks/reports in Ivy.

SJC reconciliation

* update SJC CONTROL.md;
* create or reconcile RELEASE_GATES.md;
* record actual remote and approved SHA;
* record backup deferral;
* record PostgreSQL disposition;
* record static launch independence from VPS;
* record current operational blockers;
* preserve SJC project authority.

Live VPS storage audit

* verify disk use;
* identify large consumers;
* distinguish durable, temporary, cache, logs, backups, browser state, PostgreSQL, releases, checkouts, virtual environments;
* propose safe cleanup;
* define per-repo storage budgets;
* define reserve thresholds;
* define temporary-data retention;
* define minimal UI-serving state;
* verify reboot status;
* avoid disrupting unrelated workloads.

Reusable onboarding

* turn SJC lessons into templates;
* define gate-update requests;
* define exact-SHA workflow;
* define data-authority declaration;
* define VPS-storage declaration;
* define database disposition;
* define backup disposition;
* define task declaration;
* define near-future timer proof;
* define natural-run proof;
* define transfer/receipt/prune proof;
* define offboarding.

Reckless Ben preparation

* inspect the existing Reckless Ben control record;
* identify missing intake data;
* create a bounded onboarding packet;
* reuse SJC patterns without copying domain-specific artifacts;
* sequence work so onboarding can begin immediately after Ivy consolidation.

Privileged SJC operational work

Where safe and authorized:

* deploy approved SHA;
* install service/timer disabled;
* run minutes-from-now proof;
* verify deterministic Stage A;
* verify bundle creation;
* verify Mac pull/import/receipt;
* test prune eligibility;
* register health;
* verify rollback;
* leave activation gated.

The Codex task must not become another abstract assessment.

It should consolidate, correct, execute safe operational work, and leave exact follow-ups.

⸻

18. Recommend documentation consolidation targets

In the report, identify:

* documents to retain;
* documents to merge;
* documents to supersede;
* documents to mark historical;
* documents to keep private;
* documents to link from the primary entrypoint;
* per-repo fields that should replace prose;
* helper scripts that could detect stale control records;
* checks that could detect missing release-gate evidence.

Do not modify Ivy.

⸻

19. Approved SJC repository changes

This task may modify SJC code and documentation needed for:

* publication decision model;
* corpus validation;
* publication selector;
* operator tooling;
* UI v0 specification;
* public data contract;
* tests;
* roadmap status;
* task/report references.

Do not:

* modify review decisions;
* approve items;
* mark items published;
* generate a public release;
* build the final UI;
* modify Ivy;
* deploy;
* configure credentials;
* activate timers;
* commit;
* push.

⸻

20. Required validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
git diff --check
git status --short
git branch --show-current
git remote -v

Run targeted tests for:

* publication-decision validation;
* invalid transitions;
* corpus errors;
* legacy warnings;
* selector exclusions;
* sensitivity exclusions;
* missing source links;
* missing SilverLeaf relevance;
* withdrawn items;
* superseded items;
* deterministic ordering;
* audit preservation;
* dry-run safety.

For Ivy read-only inspection:

git -C /Users/buddy/projects/ivy-control-vps status --short
git -C /Users/buddy/projects/ivy-control-vps branch --show-current
git -C /Users/buddy/projects/ivy-control-vps log -n 10 --oneline
git -C /Users/buddy/projects/ivy-control-vps diff --check

Do not perform privileged or mutating Ivy operations.

⸻

21. Required report structure

Write reports/16-publication-foundation-and-ui-discovery.md with:

1. Executive result
2. Starting SJC state
3. Starting Ivy state
4. Publication foundation implemented
5. Publication-decision model
6. Corpus validator
7. Publication selector
8. Operator decision workflow
9. Tests and negative cases
10. Actual corpus viewed as a SilverLeaf resident
11. Resident information needs
12. Useful topics, entities, and places
13. Low-value or confusing data
14. Recommended v0 information architecture
15. Recommended v0 pages
16. Search and filter behavior
17. Item-detail requirements
18. Static UI data contract
19. SilverLeaf scope decision packet
20. Updated editorial packet
21. Candidate first-release items
22. Portfolio-site context
23. Remaining UI unknowns
24. SJC files changed
25. Validation results
26. Ivy lessons carried forward
27. Documentation-sprawl findings
28. Recommended Ivy authority hierarchy
29. Strong Codex task specification
30. SJC reconciliation requirements
31. VPS storage-audit requirements
32. Reusable onboarding requirements
33. Reckless Ben preparation
34. Remaining medium-agent tasks
35. Remaining Buddy/GPT decisions
36. Remaining Strong Codex/privileged work
37. Risks and unresolved issues
38. Final Git status
39. Final task status

Use the established final-status vocabulary.

⸻

22. Success criteria

This task is complete when:

1. publication decisions have a durable file-backed model;
2. actual corpus records receive publication-relevant validation;
3. publication eligibility can be previewed deterministically;
4. publication approval remains explicit and human-controlled;
5. no item is marked published;
6. the actual corpus has been reviewed from a resident perspective;
7. the v0 UI is defined from real user needs and real data;
8. the static UI data contract is implementation-ready;
9. Buddy and GPT have a concise SilverLeaf scope packet;
10. the editorial packet is updated;
11. portfolio integration context is known or precisely requested;
12. the Strong Codex task is ready without broad rediscovery;
13. Ivy documentation consolidation goals are explicit;
14. SJC reconciliation requirements are explicit;
15. live VPS storage-audit requirements are explicit;
16. reusable onboarding and Reckless Ben preparation are explicit;
17. the next work is limited to static export, UI implementation, editorial approval, Codex/Ivy consolidation, and publication;
18. no further broad SJC product or architecture discovery is required.