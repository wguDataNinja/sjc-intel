Task 15 — Publication Readiness Review and Ivy Onboarding Retrospective

Session

This is a new OpenCode agent session.

Work primarily from:

/Users/buddy/projects/sjc_intel

Inspect Ivy Control VPS read-only at:

/Users/buddy/projects/ivy-control-vps

This task is a combined:

* publication-readiness review;
* editorial decision-preparation packet;
* repository presentation audit;
* complete SJC work-history reconstruction;
* Ivy onboarding retrospective;
* repository-versus-control-plane ownership assessment;
* VPS storage and operational-model assessment;
* next-repository readiness review.

It is primarily an evidence-gathering, synthesis, and decision-preparation task.

Do not make final editorial publication decisions on Buddy’s behalf.

Do not modify:

* the VPS;
* PostgreSQL;
* systemd;
* Hermes credentials;
* production timers;
* protected Ivy state;
* review decisions;
* publication decisions.

Limited SJC documentation edits are allowed only where explicitly authorized in this task.

Required report

Write:

reports/15-publication-readiness-review.md

Follow reports/README.md.

The report must be detailed enough for Buddy and GPT to review together and make the remaining:

* publication;
* editorial;
* UI;
* repository-cleanup;
* VPS;
* Ivy onboarding;
* storage;
* scheduling;
* high-reasoning;

decisions without broad rediscovery.

⸻

1. Mission

Prepare the final decision packet needed to move SJC_Intel from technically mature to publish-ready.

At the same time, reconstruct and evaluate the full SJC onboarding experience so Ivy Control VPS can improve its reusable process before the next repository, expected to include Reckless Ben.

This task must:

1. review everything SJC_Intel says about what should be public;
2. identify exactly what can be published now;
3. identify what must remain internal;
4. prepare a complete editorial-review packet for Buddy and GPT;
5. inspect the current review queue and propose a bounded first-release set;
6. identify the exact remaining implementation work that blocks publication;
7. reconstruct the full SJC work history from tasks, reports, logs, commits, planning documents, and Ivy records;
8. determine which onboarding stages were completed inside SJC without being recorded in Ivy;
9. determine whether Ivy documentation accurately reflects the real SJC onboarding state;
10. test the hypothesis that ownership between Ivy and project repositories has been inconsistent;
11. define a clean responsibility boundary between Ivy and target repositories;
12. evaluate how well the documented Ivy admission gates worked in practice;
13. identify reusable onboarding improvements before applying the process to another repository;
14. inspect Ivy’s portfolio goals and operating principles;
15. assess the VPS as a low-cost, temporary execution and bounded-serving platform;
16. define what SJC data should remain on the VPS, if any;
17. define what should transfer promptly to the Mac;
18. prepare a Strong Codex assessment packet for remaining privileged VPS and optimization work;
19. retain backup requirements while deferring portfolio-wide backup implementation;
20. preserve the accepted PostgreSQL decision;
21. leave a short, ordered completion plan separated by medium-agent, Buddy, GPT, Strong Codex, and privileged Ivy responsibilities.

The governing objective is:

Finish SJC_Intel for publication while converting its real onboarding history into a simpler, reusable Ivy process for the next repository.

⸻

2. Working hypotheses to test

Do not assume these are correct. Test them against repository evidence.

2.1 Documentation-location hypothesis

We may not have been sufficiently disciplined about deciding when work belonged in:

* sjc_intel; versus
* ivy-control-vps.

Determine where ownership was unclear or inconsistent.

2.2 Ivy ownership hypothesis

The expected boundary is:

Ivy Control VPS should own

* portfolio admission;
* release gates;
* repository control records;
* public-repository readiness checklist;
* GitHub publication gate;
* VPS admission checklist;
* deployment standards;
* exact-SHA deployment;
* service-user standards;
* systemd standards;
* task scheduling standards;
* Hermes runtime standards;
* task-declaration contract;
* VPS capacity checks;
* resource budgets;
* network policy;
* secrets handling;
* PostgreSQL operational standards;
* backup disposition requirements;
* transfer/receipt/acknowledgment standards;
* prune gates;
* health standards;
* rollback standards;
* production activation;
* natural-run proof;
* offboarding;
* reusable templates and helper tooling.

Target repositories should own

* their roadmap;
* their implementation tasks;
* their task reports;
* their domain architecture;
* their source registries;
* their schemas;
* their extractors;
* their runtime behavior;
* their task declaration;
* their output bundle contents;
* their tests;
* their public product;
* their editorial workflow;
* their release artifacts;
* their project-specific operator documentation.

Ivy should not normally own

* project implementation tasks;
* project implementation reports;
* detailed product backlog;
* domain-specific editorial work;
* source-specific extraction logic;
* project-local development history.

Test whether the current SJC/Ivy structure follows this boundary.

2.3 Missed-stage hypothesis

SJC work may have progressed outside Ivy’s formal gate tracking.

Determine whether:

* stages were completed but not recorded;
* approvals occurred informally;
* artifacts existed before the corresponding Ivy gate;
* control records became stale;
* release-gate records lagged reality;
* Ivy only learned about project state after work was already complete.

2.4 Process-efficiency hypothesis

The current Ivy process may be complete but too fragmented, repetitive, or documentation-heavy for the next repository.

Determine where:

* the same facts are recorded multiple times;
* agents repeatedly rediscover state;
* checklists and authority documents overlap;
* gate ownership is unclear;
* a template or helper could remove manual work;
* project agents need to understand too much Ivy internals.

⸻

3. Locked decisions

Treat these as accepted unless repository evidence shows a direct contradiction.

3.1 Product

SJC_Intel is:

An agent-led domain intelligence system that discovers sources, monitors them, extracts evidence, maintains structured memory, and produces reviewable intelligence for a defined domain.

St. Johns County is the first domain.

SilverLeaf is the first public product lens.

3.2 First release

The first public release should be:

* static or statically generated;
* reviewed;
* SilverLeaf-focused;
* source-attributed;
* searchable;
* filterable by stable topics, entities, and places;
* understandable as a portfolio case study;
* useful even when the VPS is unavailable.

3.3 Publication authority

Human review remains required.

candidate
≠ verified
≠ published

The VPS never publishes.

The Mac remains the publication and durable-corpus authority.

3.4 Deferred launch scope

Do not make these launch blockers:

* live incidents;
* emergency alerts;
* subscriptions;
* PostGIS;
* semantic search;
* public API;
* user accounts;
* autonomous publication;
* full multi-domain generalization;
* corpus PostgreSQL.

3.5 PostgreSQL

SJC PostgreSQL mode is currently:

DORMANT_FUTURE_READY

Preserve:

* migrations;
* adapters;
* SQL readiness;
* future narrow operational use.

Do not activate PostgreSQL merely because it exists.

Do not treat PostgreSQL as the corpus authority.

3.6 Backup

External backup implementation is intentionally deferred so the portfolio can address repositories together under a shared Ivy policy.

This task should:

* preserve the documented SJC backup requirements;
* identify what Ivy must standardize;
* identify dependencies and risks;
* avoid implementing backup automation;
* avoid selecting a provider.

3.7 License

Buddy has selected:

MIT License

Adding the MIT license is approved repository work, subject to normal validation and Git policy.

3.8 VPS philosophy

The VPS is intended to be:

* inexpensive;
* always on;
* resource constrained;
* operationally reliable;
* temporary for ingest payloads;
* bounded in retained data;
* capable of serving only the minimal current or historical data required by each public UI.

The Mac remains the durable archive and full historical authority.

The VPS should not become an uncontrolled data warehouse.

⸻

4. Required source material

4.1 SJC_Intel authority and planning

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
docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md
docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md
tasks/README.md
reports/README.md

4.2 Full SJC task/report history

Inspect all relevant files in:

tasks/
reports/
logs/agents/
logs/runs/
logs/sessions/
logs/conversations/

Do not limit the review to Tasks 08–14.

Reconstruct earlier work where it materially affected:

* architecture;
* product direction;
* source discovery;
* VPS plans;
* PostgreSQL;
* publication;
* Hermes;
* onboarding;
* backup;
* review workflow;
* GitHub publication.

Read Task 01 onward where present.

At minimum read recent reports:

reports/08-codex-redesign-1.md
reports/09-codex-redesign-2.md
reports/10-ivy-operational-admission.md
reports/11-operational-admission-continuation.md
reports/12-weekly-operations-implementation-prep.md
reports/13-candidate-to-corpus-import.md
reports/14-publish-readiness-and-vps-onboarding.md

4.3 SJC implementation and data

Inspect actual state in:

registry/
schemas/
scripts/
data/
runtime/
deploy/
prompts/
tests/
tasks/
reports/
logs/
db/
.opencode/

Inspect Git history where useful:

git log --oneline --decorate --graph --all
git show --stat <relevant-sha>

Do not assume task numbers fully capture the project history.

4.4 Ivy Control VPS authority

Begin with Ivy’s entrypoint and follow its authority hierarchy.

Inspect at minimum, where present:

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
_internal/vps-inventory-and-runbook.md

Inspect all SJC-specific Ivy material:

repos/sjc-intel/
_internal/outbox/
_internal/logs/
_internal/generated/

Search Ivy for:

sjc
sjc-intel
SJC_Intel
SilverLeaf
operational admission
Task 10
weekly operations
bundle
receipt
acknowledgement
publication

Inspect prior onboarding examples where they clarify conventions.

4.5 Portfolio goals

Read durable Ivy notes concerning:

* purpose of the portfolio;
* low-cost VPS constraint;
* reusable operations platform;
* how project repos demonstrate capabilities;
* repository publication;
* Mac/VPS authority;
* data lifecycle;
* databases;
* current and historical UI data;
* recurring workloads;
* evidence and operational proof.

The report should explain how these goals affect SJC publication and deployment.

Do not expose private host details or secrets.

⸻

5. Verify current state

5.1 SJC

Inspect and report:

* branch;
* HEAD;
* remote;
* ahead/behind;
* working-tree state;
* staged state;
* untracked state;
* task/report outputs;
* current test count;
* validation state;
* review queue count;
* pending-review count;
* human-review-required count;
* publication state;
* SilverLeaf classifications;
* release artifacts;
* README state;
* architecture-document state;
* license state;
* ignored/runtime footprint.

5.2 Ivy

Read-only inspect:

* branch;
* HEAD;
* working-tree state;
* ahead/behind;
* SJC control record;
* SJC release-gate record;
* approved SHA;
* current gate;
* documented blockers;
* documented capacity state;
* Hermes state;
* scheduling state;
* backup-disposition state;
* storage-lifecycle standards;
* SJC-specific outbox evidence;
* stale or conflicting records.

Use labels:

* VERIFIED
* DOCUMENTED BUT NOT VERIFIED
* INFERRED
* CONFLICT
* MISSING
* RECOMMENDATION

Do not silently reconcile contradictions.

⸻

6. Reconstruct the complete SJC work history

Produce a concise but complete chronology of material work.

Do not reproduce every minor edit.

For each major phase include:

* date or sequence;
* work performed;
* repository where it occurred;
* task/report/log evidence;
* resulting architecture or decision;
* whether Ivy was updated;
* whether a formal Ivy gate was passed;
* whether a gate should have been updated but was not;
* current status.

Expected phases may include:

* initial local buildout;
* source registry and discovery loops;
* review pipeline;
* PostgreSQL foundation;
* product-direction pivot;
* SilverLeaf scope;
* agentic sourcing;
* roadmap redesign;
* publication contract;
* GitHub remote;
* weekly operations;
* bundle/import workflow;
* Ivy admission preparation;
* backup and scheduling decisions;
* publication-readiness work.

Identify work that occurred:

* entirely in SJC;
* entirely in Ivy;
* across both;
* outside any formal tracked process.

⸻

7. Gate-by-gate Ivy assessment

The documented active model contains five sequential gates:

1. Portfolio Admission
2. Public Repository Readiness
3. GitHub Publication
4. Deployment Readiness
5. VPS Deployment

For each gate:

* quote or accurately summarize the documented requirement;
* identify the required evidence;
* determine the actual SJC evidence;
* determine the true current status;
* compare that status with CONTROL.md and RELEASE_GATES.md;
* identify missing records;
* identify work completed out of order;
* identify ambiguous approval;
* identify duplicated evidence;
* recommend correction.

Classify each gate:

* PASSED_AND_RECORDED
* PASSED_NOT_RECORDED
* PARTIAL
* BLOCKED
* NOT_STARTED
* DOCUMENTATION_CONFLICT

Explicitly assess:

* whether Gate 2 and Gate 3 are distinct enough;
* whether Gate 4 contains too many unrelated subgates;
* whether canonical ingestion admission belongs inside Gate 4;
* whether static public launch should depend on Gate 5;
* whether project agents know when to request a gate update.

⸻

8. Checklist effectiveness review

Evaluate the Ivy VPS admission checklist against the actual SJC experience.

For every checklist item:

1. identity and fit;
2. GitHub authority;
3. hygiene;
4. data lifecycle;
5. PostgreSQL;
6. capacity;
7. placement/deployment;
8. runtime authority;
9. secrets and recovery;
10. acceptance and cleanup;
11. proposed external-backup disposition;

report:

* what SJC supplied;
* where the evidence lives;
* whether evidence is project-owned or Ivy-owned;
* whether the requirement was clear;
* whether it was checked at the right time;
* whether it needs a template;
* whether it needs automation;
* whether it should be a gate rather than checklist evidence;
* whether it created repeated work.

⸻

9. Repository-versus-Ivy ownership audit

Produce a responsibility matrix.

For every major artifact or concern, recommend one owner:

* Ivy;
* project repository;
* shared contract with Ivy authority;
* private Ivy evidence;
* public project documentation.

Cover:

* roadmap;
* backlog;
* tasks;
* reports;
* agent logs;
* cadence logs;
* repository control record;
* release gates;
* admission checklist;
* deployment manifest;
* weekly task declaration;
* Hermes prompt;
* systemd units;
* source registry;
* schemas;
* bundle schema;
* bundle contents;
* receipt schema;
* acknowledgment state;
* prune state;
* health contract;
* health output;
* PostgreSQL manifest;
* data lifecycle;
* backup requirements;
* restore instructions;
* runtime secrets;
* UI data declaration;
* resource budget;
* offboarding;
* live operational evidence.

Test the specific hypothesis:

Ivy should own admission, shared VPS/database/runtime standards, gates, and operational evidence—but should not track project implementation tasks and reports.

Identify current violations or confusing overlaps.

⸻

10. Review all publication plans and ideas

Inspect every durable artifact discussing:

* product direction;
* public release;
* SilverLeaf;
* publication eligibility;
* reviewed-only output;
* portfolio presentation;
* public/private boundaries;
* source attribution;
* methodology;
* limitations;
* screenshots;
* architecture diagrams;
* demo content;
* public UI;
* search;
* filters;
* subscriptions;
* public API;
* reusable-platform claims.

For every material proposal classify:

* accepted;
* implemented;
* partially implemented;
* proposed;
* deferred;
* contradicted;
* superseded;
* unclear.

Explicitly identify:

* ideas only in task reports;
* ideas only in older planning docs;
* ideas incorporated into the roadmap;
* ideas implemented in code;
* ideas that should not appear publicly;
* claims that would overstate capabilities.

⸻

11. Define what is publishable

Prepare a publication-readiness matrix.

11.1 Repository publication

Assess:

* GitHub repository;
* README;
* architecture document;
* MIT license;
* setup instructions;
* validation instructions;
* examples;
* screenshots;
* diagrams;
* limitations;
* security/privacy notes;
* internal-document exposure;
* public-safe roadmap references.

Classify:

* ready;
* ready with minor edits;
* blocked;
* private;
* unnecessary.

11.2 Product-data publication

Assess:

* eligible items;
* verified items;
* provenance;
* SilverLeaf relevance;
* sensitivity;
* duplicates;
* obsolescence;
* editorial review;
* public exclusions.

Do not mark items published.

11.3 UI publication

Identify the minimum launch pages and data:

* homepage;
* SilverLeaf overview;
* latest intelligence;
* topic filters;
* entity filters;
* place filters;
* search;
* item detail;
* source attribution;
* methodology;
* limitations;
* architecture/case study.

Classify:

* launch-critical;
* optional;
* post-launch.

11.4 Portfolio publication

Using Ivy portfolio goals, determine what the public presentation should emphasize:

* technical problem;
* agent-led discovery;
* deterministic monitoring;
* evidence model;
* human review;
* bounded automation;
* low-cost infrastructure;
* Mac/VPS split;
* portability;
* lessons learned.

Assign content to:

* SJC README;
* SJC architecture document;
* portfolio-site copy;
* Ivy documentation;
* screenshots;
* demo video.

⸻

12. Editorial-review packet

Prepare a structured discussion packet for Buddy and GPT.

12.1 Queue summary

Include:

* total entries;
* status counts;
* pending;
* human-review-required;
* likely SilverLeaf-relevant;
* likely release-eligible;
* likely noise;
* likely duplicates;
* sensitive or unsuitable.

12.2 Candidate first-release set

Propose a small, coherent first-release set.

For each item include:

* item ID;
* title;
* source;
* date;
* topic;
* entities;
* SilverLeaf relevance;
* verification;
* publication eligibility;
* sensitivity;
* source URL;
* rationale;
* unresolved issue;
* recommended editorial action.

Do not choose a large release merely because data exists.

12.3 Exclusion categories

Summarize exclusions:

* not SilverLeaf-relevant;
* unverified;
* duplicate;
* stale;
* incomplete;
* sensitive;
* low-value;
* weak attribution;
* internal-only;
* contract failure.

12.4 Buddy/GPT decisions

Prepare explicit questions:

* release size;
* freshness window;
* countywide relevance;
* school and road adjacency;
* crime/public-safety content;
* summary editing;
* publication timestamps;
* withdrawal;
* methodology visibility;
* source screenshots;
* unresolved GAP-009 items;
* sensitivity threshold.

⸻

13. SilverLeaf readiness

Assess:

* aliases;
* neighborhoods;
* roads;
* schools;
* utilities;
* entities;
* interest filters;
* inclusion rules;
* exclusions;
* relevance fields;
* needs_review.

Determine:

* existing;
* missing;
* required for launch;
* safely deferred;
* inputs for the SilverLeaf-registry task.

Do not require PostGIS.

⸻

14. Publication implementation gaps

Assess:

* corpus validator;
* publication selector;
* publication decision storage;
* reviewed-only export;
* release builder;
* search index;
* release manifest;
* rollback;
* allowlist;
* denylist;
* deterministic ordering;
* tests.

Classify:

* complete;
* partial;
* documented only;
* missing.

Recommend the smallest coherent task grouping.

Avoid unnecessary tiny tasks.

⸻

15. Ivy Control VPS — SJC Onboarding Retrospective and Next-Repository Readiness

This must be a standalone major report section that can be handed directly to an Ivy-focused agent.

15.1 Actual SJC onboarding story

Reconstruct:

local-only repository
→ architecture/product stabilization
→ Ivy portfolio admission
→ GitHub readiness
→ GitHub remote and reviewed SHA
→ operational contracts
→ weekly task declaration
→ transfer/import/receipt model
→ VPS admission preparation
→ scheduling model
→ deployment/shadow-run readiness

State where each step was documented.

15.2 Missing Ivy updates

Identify:

* work completed in SJC but absent from Ivy;
* gate records not updated;
* stale control records;
* admission evidence stored only in SJC reports;
* operational standards discovered in SJC but not promoted into Ivy;
* decisions that should have triggered Ivy documentation earlier.

15.3 Recommended Ivy authority model

Recommend the exact distinction between:

Ivy authority

* admission;
* gate state;
* control records;
* VPS standards;
* DB standards;
* runtime standards;
* task scheduling;
* backup disposition;
* resource/capacity;
* secrets;
* health;
* rollback;
* operational evidence;
* activation/offboarding.

Project authority

* implementation tasks;
* implementation reports;
* product roadmap;
* domain behavior;
* workload code;
* output contents;
* tests;
* editorial review;
* publication.

15.4 Reusable onboarding sequence

Recommend a concise generic sequence for the next repository.

At minimum consider:

1. portfolio-fit decision;
2. repository-control record;
3. public-readiness preflight;
4. GitHub publication;
5. data-authority declaration;
6. VPS storage declaration;
7. PostgreSQL disposition;
8. backup disposition;
9. task declaration;
10. deployment manifest;
11. exact-SHA deployment;
12. shadow run;
13. near-future timer proof;
14. transfer/import/receipt/prune proof;
15. natural run;
16. activation;
17. health and review;
18. offboarding.

15.5 Reckless Ben preparation

Prepare a concise pre-onboarding checklist for the Reckless Ben repository.

Include what should be known before work begins:

* repo location;
* purpose;
* public/private target;
* Git status;
* remote;
* data classes;
* durable authority;
* runtime;
* network needs;
* secrets;
* database role;
* VPS role;
* UI-serving needs;
* backup disposition;
* scheduling;
* health;
* rollback;
* publication target.

Identify what can be reused directly from SJC and what must remain project-specific.

15.6 Exact Ivy agent handoff

Produce a proposed task packet outline for an Ivy agent.

Include:

* files to inspect;
* files to update;
* control records to reconcile;
* gate records to reconcile;
* checklist changes;
* templates to create;
* helpers to consider;
* duplicated docs to consolidate;
* validation;
* live verification;
* Buddy decisions;
* Strong Codex gates.

Do not modify Ivy.

⸻

16. VPS storage and retention assessment

16.1 Governing model

Evaluate:

VPS
- ingestion
- bounded processing
- temporary bundles
- health
- scheduler state
- minimal public UI-serving data
Mac
- full corpus
- review state
- history
- release generation
- archive
- restore authority

16.2 Artifact classification

For each SJC artifact recommend:

* temporary VPS;
* UI-retained VPS;
* immediate Mac transfer;
* bounded VPS retention;
* never VPS;
* compression;
* prune after receipt;
* regenerate.

Cover:

* raw captures;
* source events;
* candidates;
* proposals;
* logs;
* manifests;
* checksums;
* receipts;
* health;
* review queue;
* corpus;
* release files;
* search index;
* current summaries;
* historical published items;
* metrics;
* database state.

16.3 UI-serving state

Compare:

* no SJC UI data on VPS;
* latest static release only;
* bounded release history;
* compact public database;
* corpus access.

Recommend the minimum.

16.4 Strong Codex storage-audit packet

Prepare a bounded task outline for:

* live disk audit;
* workload footprints;
* safe cleanup;
* retention;
* repo budgets;
* UI data declarations;
* capacity thresholds;
* journals;
* browser/cache;
* PostgreSQL;
* old releases;
* deployment;
* rollback.

Do not execute it.

⸻

17. Hermes and scheduling readiness

Assess:

* Hermes resident-assistant status;
* deterministic scheduled execution;
* agentic discovery;
* project task declaration;
* Ivy scheduler authority;
* systemd readiness;
* provider authentication;
* near-future test;
* weekly activation.

Use precise terminology.

Do not call deterministic scripts “Hermes” unless Hermes executes them.

⸻

18. Backup deferral

Verify:

* SJC requirements are documented;
* external destination is deferred;
* automation is deferred;
* Ivy generic requirement remains pending;
* static publication is not blocked;
* VPS production activation may still require an explicit backup exception or disposition.

Recommend where Ivy records the deferral.

⸻

19. Approved SJC repository changes

Allowed:

* add MIT license;
* correct public-safe documentation;
* clarify roadmap status;
* fix stale task/report references;
* link architecture/methodology docs;
* clarify backup deferral;
* clarify PostgreSQL status;
* clarify Ivy handoff ownership.

Do not:

* implement the publication pipeline;
* alter review decisions;
* mark items published;
* build UI;
* modify Ivy;
* deploy;
* configure credentials;
* enable timers;
* commit;
* push.

Report every change.

⸻

20. Remaining completion plan

Produce one ordered plan.

Separate:

Medium OpenCode

* publication validator/selector;
* SilverLeaf registry;
* static release;
* BCC workspace support;
* portfolio integration;
* UI implementation;
* public presentation polish.

Buddy and GPT

* editorial review;
* release-set approval;
* UI decisions;
* sensitive-item decisions;
* launch approval.

Strong Codex

Only for:

* live VPS storage audit;
* capacity-sensitive cleanup;
* privileged deployment;
* systemd activation;
* cross-repository changes;
* provider authentication;
* rollback-sensitive work.

Ivy agent

* reconcile SJC gate/control records;
* update reusable onboarding docs;
* create templates/checklists;
* prepare Reckless Ben onboarding;
* implement backup-disposition gate;
* define offboarding.

Privileged Ivy operator

* deploy approved SHA;
* install service/timer;
* run near-future proof;
* verify transfer;
* activate after gates.

Every task should state:

* dependency;
* outcome;
* publication blocker;
* required report;
* agent strength.

⸻

21. Required validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
git diff --check
git status --short
git branch --show-current
git remote -v

For Ivy read-only assessment:

git -C /Users/buddy/projects/ivy-control-vps status --short
git -C /Users/buddy/projects/ivy-control-vps branch --show-current
git -C /Users/buddy/projects/ivy-control-vps log -n 10 --oneline
git -C /Users/buddy/projects/ivy-control-vps diff --check

Do not run privileged or mutating operations.

⸻

22. Required report structure

Write reports/15-publication-readiness-review.md with:

1. Executive result
2. Starting SJC state
3. Starting Ivy state
4. SJC work-history reconstruction
5. Material work outside formal Ivy gates
6. Gate-by-gate SJC status
7. Admission-checklist effectiveness
8. Repository-versus-Ivy ownership findings
9. Documentation-location conflicts
10. Publication-plan synthesis
11. Repository publication readiness
12. Product-data publication readiness
13. UI and portfolio requirements
14. Editorial queue summary
15. Candidate first-release set
16. Exclusion categories
17. Buddy/GPT editorial questions
18. SilverLeaf readiness
19. Publication implementation gaps
20. Ivy Control VPS — SJC Onboarding Retrospective and Next-Repository Readiness
21. Reusable Ivy onboarding sequence
22. Reckless Ben pre-onboarding checklist
23. Exact Ivy-agent handoff
24. VPS storage and retention assessment
25. Minimum SJC UI-serving state
26. Strong Codex storage-audit packet
27. Hermes and scheduling readiness
28. Backup deferral status
29. SJC files changed
30. Validation results
31. Remaining medium-agent tasks
32. Remaining Buddy/GPT decisions
33. Remaining Ivy tasks
34. Remaining privileged actions
35. Risks and unresolved issues
36. Final Git status
37. Final task status

Use the established final-status vocabulary.

⸻

23. Success criteria

This task is complete when:

1. Buddy and GPT have a decision-ready publication packet;
2. the first-release candidate set is visible;
3. publication blockers are exact;
4. the complete SJC onboarding history is reconstructed;
5. missed or stale Ivy gate records are identified;
6. repository-versus-Ivy ownership is clarified;
7. Ivy’s gate/checklist process is evaluated against reality;
8. reusable onboarding improvements are specified;
9. an Ivy-focused agent can act from the report;
10. Reckless Ben has a pre-onboarding checklist;
11. the VPS storage philosophy is translated into artifact-level rules;
12. a Strong Codex live-storage packet is prepared;
13. backup remains deliberately deferred but documented;
14. PostgreSQL remains DORMANT_FUTURE_READY;
15. the remaining path to publication is short and executable;
16. no further broad SJC architectural discovery is required.