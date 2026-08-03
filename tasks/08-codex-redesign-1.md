# Task 08 — Codex Redesign 1

Task type

Architecture, publishability, deployment, and completion assessment.

This is a new Strong Codex session. Do not assume prior conversational context beyond the repository artifacts and references named in this task.

Required output

Write the final report to:

reports/08-codex-redesign-1.md

Follow the report contract in reports/README.md, including:

* task identity;
* starting Git state;
* files and repositories inspected;
* work performed;
* validation commands and results;
* evidence provenance;
* final Git status;
* unresolved issues;
* risks;
* candidate next tasks;
* final status.

Use one of the established final statuses:

* COMPLETE
* COMPLETE_WITH_FOLLOW_UP
* PARTIAL
* BLOCKED
* HUMAN_DECISION_REQUIRED

Do not modify

This is an assessment and planning task.

Do not:

* edit the roadmap;
* edit code;
* change data;
* change schemas;
* modify the VPS;
* modify PostgreSQL;
* install services;
* create timers;
* run migrations;
* commit;
* push;
* prune or delete anything.

Read-only inspection and safe validation are permitted.

The intended next step, after Buddy reviews the report, is a separate Strong Codex task to rewrite the authoritative roadmap.

⸻

1. Mission

Determine the shortest credible path to make SJC_Intel:

1. publishable;
2. portfolio-worthy;
3. operationally reliable;
4. maintainable by medium-strength OpenCode builder agents;
5. deliberately reusable for future intelligence domains;
6. deployable using the existing low-cost Ivy VPS operating model.

Push back on any assumption that is weak, unnecessary, internally inconsistent, or likely to delay publication.

Do not optimize for an ideal theoretical platform.

Optimize for:

Publish soon, preserve correctness, use the VPS intelligently, and leave deliberate seams for future reuse.

⸻

2. Repository and system context

Two repositories are relevant.

2.1 SJC_Intel

Local repository:

/Users/buddy/projects/sjc_intel

SJC_Intel is the domain application.

Current framing:

SJC_Intel is an agent-led domain intelligence system that discovers sources, monitors them, extracts evidence, maintains structured memory, and produces reviewable intelligence for a defined domain.

St. Johns County is the first implementation.

SilverLeaf is the first public product lens.

The existing system is primarily:

* registry-driven;
* file-backed;
* prompt-assisted;
* human-operated;
* evidence-oriented;
* review-gated.

Its strongest current spine appears to be:

source
→ source_event
→ intel_item
→ dedupe
→ review_queue_entry
→ reviewed corpus

Do not accept that description without inspecting the implementation.

2.2 Ivy Control VPS

Local repository:

/Users/buddy/projects/ivy-control-vps

ivy-control-vps is the portfolio operations repository.

It owns or documents:

* production topology;
* VPS deployment;
* scheduler authority;
* service health;
* PostgreSQL operations;
* backup and restore;
* retention;
* archive flow;
* bounded privileged execution;
* operational evidence.

The VPS is intentionally inexpensive and resource-constrained.

The portfolio objective is to demonstrate that several useful always-on projects can operate reliably on a roughly $5/month VPS through disciplined scheduling, bounded storage, transfer, retention, and archive practices.

The VPS is not automatically the permanent home for all project data.

⸻

3. Locked provisional decisions

Treat these as current decisions.

You are explicitly authorized to challenge them, but only with concrete evidence and a better alternative.

3.1 Product framing

SJC_Intel is not merely a local-news scraper or newsletter generator.

It is a reference implementation of a reusable agent-led domain intelligence architecture.

The reusable concepts include:

* source discovery;
* source qualification;
* deterministic monitoring;
* evidence extraction;
* structured intelligence items;
* deduplication;
* review;
* entity tracking;
* cadence;
* agent task contracts;
* publication views.

3.2 First public product

The first public product is a SilverLeaf-focused intelligence experience.

The first useful release should include:

* a simple interface on Buddy’s portfolio website;
* reviewed SilverLeaf-relevant intelligence;
* clear source attribution;
* search;
* filtering by topic, entity, place, or other stable classification;
* a clear explanation of the project and architecture;
* automatic periodic updates.

Email subscriptions are desired, but may follow the first UI release if they materially increase launch complexity.

3.3 Human review

Automated discovery, monitoring, extraction, classification, and drafting are acceptable.

Initial public publication should remain human-reviewed.

Do not recommend fully autonomous publication unless the alternative is tightly bounded, evidence-backed, and clearly safer or simpler.

3.4 No live-incident launch product

The initial release is:

Periodic, reviewed, evidence-backed neighborhood intelligence.

It is not intended to be a real-time emergency, crash, outage, or public-safety alert service.

Live incidents may remain a future architectural lane.

They should not block the first release.

3.5 File compatibility

The current file-backed workflow remains valid.

Do not force PostgreSQL authority merely because PostgreSQL infrastructure exists.

File artifacts may remain:

* durable corpus;
* review artifacts;
* archive format;
* interchange format;
* publication input;
* rollback path.

3.6 SQL readiness

Even if PostgreSQL is deferred or used only narrowly, new work should remain SQL-ready where practical.

Preserve:

* stable schemas;
* clear IDs;
* explicit relationships;
* deterministic normalization;
* storage boundaries;
* migration compatibility;
* idempotent operations.

Do not turn SQL readiness into a database rewrite.

3.7 Reusable architecture

Reusability should become an explicit roadmap concern.

The intended separation is:

Generic intelligence architecture
        ↓
SJC domain implementation
        ↓
SilverLeaf public product

Do not require complete multi-domain generalization before launch.

Identify the minimum boundaries worth making explicit now.

3.8 VPS role

The likely operating model is:

VPS
- always-on scheduling
- bounded fetching
- bounded agent execution
- temporary operational state
- health and run records
- transfer/export preparation
        ↓ verified transfer and acknowledgment
Mac
- durable corpus authority
- archive
- review
- development
- publication preparation
- historical memory
- restore authority

PostgreSQL on the VPS may still be useful for:

* run state;
* health state;
* locks;
* transfer acknowledgments;
* small operational queues;
* bounded staging;
* source status;
* short-lived publication support.

Do not assume the main SJC corpus should remain on the VPS.

3.9 Resource constraints are intentional

The VPS is weak and inexpensive by design.

The system should use:

* bounded execution;
* bounded retention;
* prompt transfer to the Mac;
* archive acknowledgment;
* pruning only after verification;
* one scheduler and writer authority;
* staggered workloads;
* explicit timeouts;
* resource-aware operation.

A solution that requires a substantially larger VPS should be treated as suspect unless unavoidable.

⸻

4. Required source material

Begin with the repository-defined entrypoints and workflow documents.

Do not rely only on the files listed below if the repositories identify additional authorities.

4.1 SJC_Intel core

Inspect at minimum:

README_INTERNAL.md
AGENTS.md
BACKLOG.md
VPS_ROADMAP.md
ROADMAP.md
VPS_CONTINUITY.md
README.md

Inspect the planning, schema, workflow, source, cadence, data, task, report, and agent-memory artifacts relevant to completion.

Particularly relevant uploaded or repository documents include:

docs/data_model.md
docs/postgresql_adapter.md
docs/retention.md
docs/snapshots_and_metrics.md
docs/news_ingestion_readiness.md
docs/deep_research_ingestion.md
docs/backup-restore.md
docs/taxonomy.md
docs/discovery_test.md
docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md
docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md

Also inspect:

tasks/README.md
reports/README.md
tasks/
reports/
prompts/
logs/
runtime/
.opencode/
registry/
schemas/
scripts/
data/
db/migrations/
tests/

Inspect actual code and data, not merely architectural descriptions.

4.2 Harness-engineering notes

Use:

/Users/buddy/projects/alori/learn-harness-engineering/notes.md

Treat this as a proposed operating standard, not automatically as repository authority.

Evaluate how its principles apply to:

* agent task design;
* repository authority;
* durable task state;
* bounded execution;
* timer loops;
* verification;
* evaluator separation;
* retry and stop conditions;
* evidence bundles;
* session handoff;
* clean restartability.

Do not copy its artifact structure blindly.

Identify overlap and conflicts with existing SJC and Ivy conventions.

4.3 Ivy Control VPS

Inspect at minimum:

README.md
docs/VPS_INVENTORY.md
docs/DATABASE.md
docs/PORTFOLIO_CONVENTIONS.md
docs/HEALTH_CONTRACT.md
agents/VPS_ORCHESTRATION.md

Inspect relevant:

templates/
tools/
deploy/
_internal/

Private material may be used for operational evidence but should remain private.

Do not copy credentials, private host data, secret-adjacent content, or unnecessary private chronology into the public-facing report.

4.4 Existing architectural assessment

Review the existing architectural assessment that characterized:

* the evidence-and-review spine as strong;
* PostgreSQL as largely unwired;
* machine-enforced contracts as missing;
* extractor scripts as fragile;
* search and UI as absent;
* orchestration as fragmented;
* domain leakage as unresolved;
* source adapters and PostgreSQL authority as proposed future directions.

Treat it as prior analysis, not final authority.

Its earlier recommendation that PostgreSQL become authoritative is explicitly not locked.

⸻

5. Inspect actual current state

Do not build the report from documentation alone.

Inspect:

* current Git branch;
* working-tree state;
* tracked and untracked task/report artifacts;
* current data volume;
* actual item and queue counts;
* current tests;
* validation behavior;
* current storage write paths;
* current extractor behavior;
* current agentic-discovery artifacts;
* actual roadmap authority;
* current task and report workflow;
* actual VPS onboarding process;
* actual Hermes/runtime status;
* current transfer and archive precedent;
* current scheduler and workload constraints.

Distinguish every material finding using these labels where useful:

* VERIFIED
* INFERRED
* DOCUMENTED BUT NOT VERIFIED
* MISSING
* CONFLICT
* RECOMMENDATION

Do not silently reconcile contradictions.

⸻

6. Required analysis

6.1 Define the publishable finish line

State a precise recommended first-release definition.

At minimum assess:

* public UI;
* SilverLeaf scope;
* publication eligibility;
* source attribution;
* search;
* topic/entity/place filtering;
* update cadence;
* automation;
* human review;
* subscription timing;
* public case-study presentation;
* operational evidence;
* repository cleanliness;
* maintenance workflow.

Separate:

* required for launch;
* valuable but non-blocking;
* post-launch;
* intentionally deferred.

6.2 Evaluate the three-layer architecture

Assess the boundary between:

Generic intelligence infrastructure

Examples:

* source registry pattern;
* source qualification;
* monitor contracts;
* evidence model;
* dedupe;
* review;
* task contracts;
* cadence;
* storage abstraction;
* publication export.

SJC domain implementation

Examples:

* county sources;
* taxonomy;
* resident-interest rules;
* communities;
* tracked entities;
* geographic rules;
* county extractors.

SilverLeaf product

Examples:

* geographic scope;
* public filters;
* presentation;
* publication criteria;
* search experience;
* subscriptions.

Identify:

* useful existing separation;
* harmful coupling;
* coupling acceptable until after launch;
* minimum changes needed now;
* changes that would be premature.

6.3 Data quality and presentation readiness

The dataset must be efficient, coherent, and portfolio-worthy even if it remains file-backed.

Assess:

* schema consistency;
* actual corpus validation;
* stable IDs;
* deterministic dedupe;
* source provenance;
* verification status;
* classification ownership;
* entity references;
* geographic references;
* review state;
* publication state;
* stale or malformed records;
* redundant fields;
* extractor-specific leakage;
* efficient loading for search and UI;
* exportability.

Determine the minimum machine-enforced contract required before scheduled automation and publication.

Do not presume a complete schema redesign is required.

6.4 Search and public data export

Determine the simplest credible search architecture for the first release.

Consider:

* generated static JSON;
* generated compact search index;
* client-side search;
* static-site build-time indexing;
* Mac-generated reviewed export;
* serverless API;
* read-only VPS endpoint;
* PostgreSQL-backed endpoint;
* direct database access.

Favor a site that remains useful if the VPS is temporarily unavailable.

Address:

* search fields;
* filters;
* stable topic/entity IDs;
* reviewed-only guarantees;
* source links;
* update process;
* artifact size;
* privacy;
* caching;
* failure behavior.

6.5 Subscriptions

Assess whether subscriptions should be:

* launch-blocking;
* immediate follow-up;
* later enhancement.

Determine what must be designed now so subscriptions are not blocked later:

* stable topic/entity/place identifiers;
* publication-event semantics;
* subscriber data location;
* matching logic;
* delivery service;
* unsubscribe handling;
* privacy;
* reviewed-only trigger.

Do not build a full subscription platform unless necessary.

6.6 Geographic scope

The first public product is SilverLeaf-focused.

Determine the minimum geographic registry required for a credible launch.

Assess whether launch requires:

* full polygons;
* PostGIS;
* point-in-polygon;
* street-level geography;
* manually curated inclusion rules;
* community and neighborhood aliases;
* roads, schools, utilities, and nearby entities;
* explicit exclusion rules.

Recommend the smallest defensible implementation.

Do not assume full GIS infrastructure is required.

6.7 Source monitoring architecture

Assess the current monitoring approach.

Determine:

* which sources are genuinely automated;
* which are manual;
* which are prompt-driven;
* which are pilot-only;
* which are needed for launch;
* whether source health is operational;
* whether extractors are too fragile for unattended use;
* whether a SourceAdapter framework is required now.

The SourceAdapter/plugin framework is currently a proposal.

Approve, defer, narrow, or reject it based on launch needs.

Prefer incremental refactoring if only a few sources are required.

6.8 Agentic discovery and Hermes reality

Determine what Hermes actually is in the current environment.

Do not infer runtime capability from prompt filenames.

Report:

* installed runtime, if any;
* invocation mechanism;
* model/provider;
* credentials;
* cost;
* task contracts;
* state;
* logging;
* retries;
* timeouts;
* concurrency;
* duplicate-run prevention;
* stop conditions;
* output paths;
* existing scheduled use;
* Mac versus VPS execution.

Classify it as one of:

* production-ready reusable runtime;
* working but project-specific runtime;
* partial harness;
* prompt convention only;
* absent.

If Hermes is not ready, recommend the smallest honest agent-led alternative.

A systemd timer invoking a bounded script plus explicit model call may be acceptable if that is the real available capability.

6.9 VPS onboarding

Determine the exact current process for adding SJC_Intel as a VPS workload.

Assess:

* repository deployment;
* reviewed revision;
* user and permissions;
* Python environment;
* dependency installation;
* environment files;
* secrets;
* systemd service;
* systemd timer;
* helper limitations;
* logging;
* health registration;
* backup or export registration;
* rollback;
* natural-run proof;
* evidence bundle;
* Mac archive integration.

Separate:

* productized;
* documented but manual;
* proven only through prior sessions;
* missing.

Identify what medium agents can prepare and what requires Strong Codex or Buddy authorization.

6.10 VPS-to-Mac flow

Determine the best SJC transfer unit and authority model.

Possible artifacts include:

* raw fetched pages;
* source events;
* normalized intelligence items;
* discovery candidates;
* review queue candidates;
* run logs;
* health records;
* compact run bundles;
* PostgreSQL exports.

Assess existing portfolio transfer patterns for:

* push versus pull;
* transport;
* authentication;
* manifests;
* checksums;
* idempotency;
* partial transfer;
* retries;
* acknowledgment;
* prune gate;
* restore.

Recommend a bounded transfer contract.

The VPS should not retain durable SJC data longer than operationally necessary.

6.11 PostgreSQL options

Evaluate PostgreSQL only against concrete SJC needs.

Compare:

Option A — no SJC PostgreSQL

The VPS runs bounded fetch and agent tasks, produces transfer bundles, and the Mac file store remains authoritative.

Option B — operational metadata only

PostgreSQL stores:

* run state;
* health;
* locks;
* transfer acknowledgments;
* source status;
* perhaps small operational queues.

The main corpus transfers to the Mac.

Option C — bounded staging

PostgreSQL temporarily stores normalized findings or candidates until transfer and acknowledgment, followed by retention.

Option D — active operational corpus

PostgreSQL holds an active corpus while the Mac receives durable archive copies.

For each assess:

* actual launch value;
* complexity;
* resource use;
* failure modes;
* two-truth risk;
* search value;
* subscription value;
* rollback;
* time to publish;
* portfolio value.

Do not select PostgreSQL merely because migrations already exist.

Do not reject it merely because the VPS is small.

Recommend the narrowest option that produces concrete value.

6.12 Scheduler and resource model

The low-cost VPS constraint is intentional.

Assess:

* current disk pressure;
* current memory;
* current load;
* workload overlap;
* current scheduling windows;
* persistent timers;
* randomized delays;
* locks;
* maximum runtimes;
* timeout behavior;
* retries;
* journal growth;
* temp-file behavior;
* repository and virtualenv footprint;
* backup footprint;
* transfer footprint.

Evaluate at least:

Scenario A

Weekly deterministic source fetches.

Scenario B

Weekly deterministic fetches plus bounded agentic discovery.

Scenario C

Daily known-source monitoring plus weekly agentic discovery.

Use ranges.

Identify what is safe now and what would require prerequisite cleanup or scheduling changes.

6.13 Orchestration consolidation

SJC currently appears to have multiple overlapping conventions:

* .opencode/agents/;
* prompts/;
* runtime/workers/;
* WORKER_CONTEXT.md;
* tasks/;
* reports/;
* agent memory;
* cadence logs;
* run logs.

Determine which should be authoritative for:

* dispatched tasks;
* reusable prompts;
* agent definitions;
* execution state;
* cadence state;
* run evidence;
* task reports;
* long-term memory;
* roadmap authority.

Do not create another parallel convention.

Use the harness-engineering notes to recommend the minimum coherent operating harness.

6.14 Roadmap and authority documents

Inventory the current planning and authority documents.

For each classify:

* authoritative;
* supporting;
* historical;
* stale;
* conflicting;
* private;
* should be consolidated;
* should be superseded;
* should remain unchanged.

Determine exactly which roadmap should be rewritten during Task 09.

Also identify which other documents Task 09 should update, link, deprecate, or leave alone.

6.15 Builder-agent readiness

Most implementation after the roadmap rewrite will be done by medium-strength OpenCode agents.

Assess whether the repo gives them enough:

* context;
* task boundaries;
* acceptance criteria;
* validation;
* safe commands;
* Git policy;
* escalation;
* evidence expectations;
* architecture references;
* continuity.

Identify tasks that are too broad for medium agents.

Recommend where Strong Codex is materially justified.

⸻

7. Required pushback

Do not merely validate Buddy’s current preferences.

Explicitly challenge:

* launch scope that is too broad;
* launch scope that is too weak to be portfolio-worthy;
* unnecessary database work;
* premature framework refactoring;
* insufficient data validation;
* fragile unattended extractors;
* unclear publication state;
* weak transfer semantics;
* unsafe VPS assumptions;
* confusing roadmap authority;
* unrealistic use of Hermes;
* overreliance on prompts without runtime controls;
* underdeveloped geographic boundaries;
* subscription work that should be deferred;
* reuse work that should be accelerated;
* reuse work that should be postponed.

For each pushback item, provide:

* the assumption;
* the evidence;
* the risk;
* the recommended correction.

⸻

8. Required report structure

Write reports/08-codex-redesign-1.md with these sections.

1. Executive recommendation

State:

* recommended first-release product;
* recommended architecture;
* recommended VPS/Mac authority model;
* recommended runtime;
* recommended PostgreSQL role;
* recommended publication path;
* estimated major workstreams;
* principal reasons.

2. Verified current state

Include:

* Git state;
* working-tree state;
* tests;
* data counts;
* storage paths;
* actual automated capabilities;
* actual agentic capabilities;
* actual deployment capabilities;
* stale or conflicting documentation.

3. Publishable finish line

Define:

* launch requirements;
* non-blocking improvements;
* post-launch work;
* deferred work;
* explicit non-goals.

4. Recommended system topology

Include a clear diagram showing:

* source collection;
* deterministic extraction;
* agentic work;
* VPS responsibilities;
* Mac responsibilities;
* transfer;
* review;
* publication export;
* portfolio UI;
* subscriptions, if later.

5. Data and contract readiness

Cover:

* schema enforcement;
* IDs;
* dedupe;
* classification;
* provenance;
* review state;
* publication state;
* export format;
* SQL readiness.

6. VPS operating model

Cover:

* deployment;
* scheduler;
* resource constraints;
* health;
* transfer;
* retention;
* rollback;
* evidence.

7. Hermes and agent-runtime recommendation

State what exists and what should actually be used.

8. PostgreSQL recommendation

Choose and justify one of Options A–D, or a clearly defined hybrid.

9. Public UI and search recommendation

Recommend the simplest portfolio-worthy implementation.

10. Subscription recommendation

State what belongs before launch, immediately after launch, and later.

11. Reusability boundary

State:

* what should become generic now;
* what should remain SJC-specific;
* what should remain SilverLeaf-specific;
* what should be proposed but deferred.

12. Harness and orchestration recommendation

Define one coherent authority model for:

* tasks;
* reports;
* prompts;
* agents;
* cadence;
* logs;
* memory;
* roadmap.

13. Roadmap authority recommendation

Identify the exact Task 09 rewrite target and supporting-document changes.

14. Prioritized blockers

For every blocker include:

* reason;
* dependency;
* acceptance condition;
* suggested agent strength;
* privileged-operation requirement.

15. False blockers and deferrals

Identify work that may sound important but should not delay launch.

16. Recommended completion sequence

Provide a phased sequence from current state to publication.

Use stable section identifiers suitable for conversion into the Task 09 roadmap.

For each phase include:

* outcome;
* dependencies;
* work packages;
* verification;
* stop conditions;
* agent strength.

17. Strong Codex versus medium-agent allocation

Separate:

* Strong Codex tasks;
* medium OpenCode tasks;
* Buddy decisions;
* privileged VPS packets.

18. Risks and unresolved decisions

Do not hide uncertainty.

19. Proposed Task 09 instructions

Provide a concise recommended specification for the second Strong Codex pass that will rewrite the roadmap.

20. Candidate next tasks

List bounded follow-up tasks in priority order.

⸻

9. Validation expectations

Run safe, relevant validations where practical.

At minimum consider:

python3 -m pytest tests/ -v
python3 scripts/validate.py
git status --short
git branch --show-current

Use repository-defined validation commands where they differ.

Do not run networked, mutating, backfill, migration, deployment, or privileged commands without explicit authority.

Read-only VPS inspection is permitted only if allowed by the applicable Ivy orchestration rules.

Record exact commands and results in the report.

⸻

10. Success criteria

This task is complete when the report gives Buddy enough evidence to decide:

1. what the first public release is;
2. what runs on the VPS;
3. what stays on the Mac;
4. how data moves between them;
5. whether PostgreSQL is used and how narrowly;
6. what Hermes or another runtime actually does;
7. what must be fixed before unattended runs;
8. what public UI/search path to use;
9. what subscriptions require;
10. what reusable boundaries to establish now;
11. what to defer;
12. which roadmap is authoritative;
13. how Task 09 should rewrite it;
14. how medium OpenCode agents can finish the work safely.

The report must make a recommendation, not merely inventory possibilities.

Where uncertainty remains, identify the smallest next verification needed.

⸻

11. Governing instruction

Design the shortest credible path to a publishable, portfolio-worthy SJC_Intel deployment. Preserve correctness, bounded VPS operation, Mac archive authority, human-reviewed publication, and deliberate seams for future reuse. Push back on weak assumptions, but do not turn launch into a speculative platform rewrite.