# Task 10 — Ivy Operational Admission


Task 10 — Ivy Operational Admission

Task type

Final Strong Codex architecture, implementation, privileged operations, and builder-handoff task.

This is the third and final planned Strong Codex pass for SJC_Intel.

Reuse the context and conclusions from Tasks 08 and 09. Do not repeat broad discovery unless live verification is necessary to execute safely.

Primary repositories

/Users/buddy/projects/sjc_intel
/Users/buddy/projects/ivy-control-vps

Also inspect the portfolio-site repository if its location is discoverable from existing project authority documents. Do not assume its framework or deployment model.

Required report

Write:

/Users/buddy/projects/sjc_intel/reports/10-ivy-operational-admission.md

Follow reports/README.md.

The report must include:

* task identity;
* starting Git state for every repository touched;
* live VPS starting state;
* files inspected;
* files changed;
* infrastructure changes;
* database changes;
* service/timer changes;
* validation commands and results;
* proof-run evidence;
* rollback evidence;
* remaining risks;
* unresolved blockers;
* detailed builder-agent handoff;
* final Git and VPS state;
* final status.

Use one of:

* COMPLETE
* COMPLETE_WITH_FOLLOW_UP
* PARTIAL
* BLOCKED
* HUMAN_DECISION_REQUIRED

⸻

1. Mission

Complete the remaining high-reasoning and operational work necessary to put SJC_Intel on a credible path to publication and bounded weekly operation.

This task must:

1. finalize the publication, validation, release, runtime, transfer, retention, and database contracts;
2. execute the risky cross-repository and VPS work that should not be delegated to medium-strength agents;
3. improve Ivy’s reusable repository-onboarding process for future projects;
4. operationally admit SJC_Intel to the Ivy VPS where safe and feasible;
5. prepare bounded weekly Hermes execution;
6. implement or finalize VPS-to-Mac transfer, acknowledgment, and pruning;
7. add enough detail to ROADMAP.md that medium-strength OpenCode agents can finish the remaining work without architectural improvisation;
8. leave high-reasoning gates clearly identified and prepared through durable task/report requirements;
9. leave GPT able to issue, review, and steer subsequent medium-agent tasks from the roadmap and reports;
10. avoid requiring another planned Strong Codex architecture pass.

The governing objective is:

Finish the risky architecture and operations now, then leave a precise, evidence-backed roadmap that medium-strength agents and Hermes can execute.

⸻

2. Explicit authorization

Buddy explicitly authorizes Strong Codex to perform the necessary work across SJC_Intel, Ivy Control VPS, the live VPS, PostgreSQL, systemd, transfer tooling, and relevant authority documents.

This authorization includes, where justified by the accepted architecture:

* inspecting the live VPS;
* editing SJC_Intel and Ivy Control VPS files;
* correcting or replacing stale operational documentation;
* improving generic Ivy onboarding contracts;
* creating or modifying deployment manifests;
* cloning or updating SJC_Intel on the VPS;
* creating users, directories, permissions, and virtual environments;
* configuring environment files through approved secret-handling paths;
* creating or modifying PostgreSQL databases, roles, schemas, tables, functions, migrations, grants, retention, and operational metadata;
* creating or modifying systemd services and timers;
* configuring Hermes or the smallest viable bounded agent runtime;
* configuring locks, retries, timeouts, health, logs, transfer state, and failure handling;
* implementing VPS-to-Mac run bundles;
* implementing manifest, checksum, receipt, acknowledgment, replay, and prune behavior;
* performing proof runs;
* performing rollback and recovery tests;
* updating SJC and Ivy authority documents;
* updating the SJC roadmap with implementation-level detail;
* leaving bounded follow-up task recommendations.

Do not stop merely because an existing Ivy document says another approval is normally required. Buddy’s direct authorization in this task supersedes stale or unnecessarily restrictive process wording.

Where Ivy governance is outdated, contradictory, or prevents a safe and reusable operating model, update the proper authority document.

Hard safety boundaries

Do not:

1. expose PostgreSQL publicly;
2. print, commit, or copy secrets into reports or tracked files;
3. delete durable project data without verified Mac receipt and acknowledgment;
4. disrupt unrelated VPS workloads;
5. make destructive shared-system changes without rollback capture;
6. replace narrow reversible changes with broad platform rewrites;
7. enable autonomous public publishing;
8. enable live-incident or emergency-alert behavior;
9. make the VPS the durable SJC corpus authority;
10. commit or push unless Buddy’s repository policy explicitly authorizes it within this task.

Stop only when:

* required credentials are unavailable;
* an irreversible ambiguity cannot be resolved from authority documents or live state;
* execution would materially endanger unrelated workloads;
* a public/editorial decision genuinely requires Buddy;
* the target portfolio repository is unavailable and its implementation cannot be safely inferred.

Complete all unblocked work before reporting a blocker.

⸻

3. Accepted architecture

Use ROADMAP.md as the authoritative product and execution plan.

Use VPS_ROADMAP.md and docs/VPS_CONTINUITY.md as supporting operational boundaries.

3.1 Product

The first public product is a reviewed, static SilverLeaf Intelligence experience.

It includes:

* reviewed SilverLeaf-relevant intelligence;
* original-source attribution;
* keyword search;
* topic, entity, and place filters;
* release timestamp;
* methodology;
* limitations;
* architecture and portfolio explanation.

The public site must remain useful when the VPS is unavailable.

3.2 Publication authority

Human review remains mandatory.

verified is not equivalent to published.

The VPS never publishes.

The Mac remains responsible for:

* editorial review;
* publication decisions;
* durable release artifacts;
* historical corpus;
* rollback;
* publication preparation.

3.3 VPS role

The VPS is intentionally small and inexpensive.

It exists to provide:

* uptime;
* bounded fetching;
* bounded Hermes execution;
* scheduling;
* operational health;
* temporary run artifacts;
* transfer preparation;
* small operational state.

The VPS is not the durable corpus archive.

3.4 Mac role

The Mac remains authoritative for:

* source events;
* intelligence items;
* review state;
* durable evidence;
* historical memory;
* release generation;
* public release artifacts;
* archive;
* restore.

3.5 Expected operating flow

Weekly Ivy timer
    ↓
bounded Hermes task on VPS
    ↓
deterministic source checks and bounded discovery
    ↓
temporary run bundle
    ↓
manifest + checksums + run metadata
    ↓
Mac pulls bundle
    ↓
Mac verifies and imports idempotently
    ↓
Mac writes receipt acknowledgement
    ↓
VPS observes acknowledgement
    ↓
VPS prunes acknowledged payload after retention delay

The VPS may retain only bounded operational state after transfer.

3.6 PostgreSQL

Do not make PostgreSQL the durable corpus authority.

The expected ceiling for initial SJC operations is Option B:

* run state;
* locks;
* source health;
* transfer manifests;
* acknowledgments;
* retry/error state;
* compact operational metrics;
* small bounded queues where useful.

Use no PostgreSQL if it adds no concrete operational value.

Use temporary staging only if required to make weekly execution safer or more reliable.

3.7 Hermes

Assume the target is one automatic weekly Hermes run on the VPS.

Verify what Hermes actually is.

Do not build a universal agent platform unless required to execute one safe bounded weekly task.

A project-specific, well-controlled runtime is acceptable.

3.8 Reusability

Preserve:

generic Ivy operational platform
        ↓
generic intelligence-system patterns
        ↓
SJC domain implementation
        ↓
SilverLeaf publication lens

Recurring operational patterns discovered during SJC admission belong in ivy-control-vps, not duplicated inside SJC_Intel.

Examples include:

* admission manifests;
* deployment contracts;
* systemd conventions;
* health registration;
* bundle formats;
* transfer acknowledgment;
* retention;
* database operational metadata;
* rollback;
* proof-run requirements;
* onboarding checklists.

⸻

4. Required source material

4.1 SJC_Intel

Read at minimum:

README_INTERNAL.md
AGENTS.md
ROADMAP.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md
BACKLOG.md
reports/08-codex-redesign-1.md
reports/09-codex-redesign-2.md
tasks/README.md
reports/README.md

Inspect relevant:

scripts/
schemas/
registry/
data/
db/
prompts/
runtime/
.opencode/
tests/
docs/

Verify actual implementation state rather than trusting summary documents.

4.2 Ivy Control VPS

Read at minimum:

README.md
docs/VPS_INVENTORY.md
docs/DATABASE.md
docs/PORTFOLIO_CONVENTIONS.md
docs/HEALTH_CONTRACT.md
agents/VPS_ORCHESTRATION.md
_internal/vps-inventory-and-runbook.md

Inspect relevant:

templates/
tools/
deploy/
systemd/
_internal/

Inspect existing onboarded projects and identify the strongest working precedents.

4.3 Harness guidance

Use:

/Users/buddy/projects/alori/learn-harness-engineering/notes.md

Apply its principles selectively:

* repository authority;
* bounded tasks;
* durable state;
* timer loops;
* verification;
* independent evaluation;
* retries;
* stop conditions;
* evidence bundles;
* restartability.

Do not create redundant workflow artifacts.

4.4 Live infrastructure

Use the approved Ivy orchestration modes to inspect and modify the VPS.

Verify current:

* disk;
* memory;
* load;
* services;
* timers;
* PostgreSQL;
* database roles;
* project directories;
* logs;
* health producers;
* backup/restore systems;
* transfer/archive systems;
* existing Hermes or model runtime;
* workload windows;
* scheduler ownership.

⸻

5. Workstream A — publication and release contracts

Finalize the remaining high-reasoning design required by ROADMAP.md §3A-G1.

5.1 Publication contract

Define and document:

* review state;
* publication decision;
* published state;
* withdrawn state;
* release membership;
* release ID;
* release timestamp;
* reviewer attribution;
* publication authority;
* sensitivity eligibility;
* source-attribution requirements;
* canonical item selection;
* duplicate handling;
* supersession;
* legacy and incomplete records;
* rollback;
* public field allowlist;
* private/internal field denylist;
* negative cases.

Choose the authoritative file-compatible representation.

Avoid unnecessary schema redesign.

5.2 Corpus-validation contract

Define:

* required fields;
* enum enforcement;
* ID validation;
* uniqueness and canonical selection;
* source references;
* entity/topic/place references;
* source-event linkage;
* timestamp rules;
* URL validation;
* dedupe invariants;
* publication eligibility;
* SilverLeaf relevance;
* public-export safety;
* legacy-record disposition.

Specify exact tests and commands medium agents must implement.

5.3 SilverLeaf release contract

Finalize:

* minimum geographic and entity registry;
* inclusion and exclusion rules;
* relevance rationale;
* needs_review;
* stable IDs;
* public filter dimensions;
* release projection;
* search-index requirements;
* release-manifest requirements;
* deterministic ordering;
* rollback retention.

5.4 Required implementation detail

Add enough detail to ROADMAP.md under §3A and §3B that medium OpenCode agents can implement the contracts without making architecture decisions.

Where appropriate, create or update one dedicated supporting contract document and link it from the roadmap.

Do not create a competing roadmap.

⸻

6. Workstream B — reusable Ivy repository admission

Treat Ivy as an operational product, not merely a set of private server notes.

6.1 Evaluate existing onboarding

Determine whether Ivy currently provides a coherent reusable contract for onboarding a new repository.

Inspect:

* admission decision;
* deployment manifest;
* reviewed SHA;
* repository location;
* service account;
* permissions;
* virtual environment;
* dependency installation;
* secrets;
* environment files;
* systemd service;
* systemd timer;
* health producer;
* logs;
* backup;
* transfer;
* retention;
* rollback;
* evidence;
* ownership;
* natural-run proof.

6.2 Improve Ivy

Where gaps or inconsistencies exist, implement the smallest reusable improvement.

Possible outputs include:

* generic onboarding checklist;
* workload manifest schema or template;
* systemd templates;
* environment-file contract;
* health registration contract;
* transfer-bundle contract;
* retention contract;
* rollback checklist;
* proof-run checklist;
* operational status template;
* helper improvements;
* corrected authority hierarchy.

Do not over-generalize beyond demonstrated needs.

6.3 Governance cleanup

Correct stale or conflicting Ivy documentation.

Private host-specific details may remain private.

Public or reusable docs must not expose secrets.

Leave a clear distinction:

* Ivy owns generic operational onboarding and production controls;
* project repositories own workload behavior and domain data;
* Buddy owns admission and product decisions;
* Strong Codex executes privileged cross-cutting work when authorized;
* medium agents implement bounded project tasks.

⸻

7. Workstream C — SJC operational admission

Operationally admit SJC_Intel to the Ivy VPS if safe after live verification.

7.1 Deployment

Prepare and, where safe, execute:

* clean approved revision selection;
* VPS repository clone or deployment checkout;
* service account and permissions;
* deployment directory;
* virtual environment;
* dependency installation;
* environment configuration;
* secret routing;
* log directory;
* run directory;
* transfer directory;
* health registration;
* rollback capture.

Preserve unrelated local and VPS changes.

Do not deploy from a dirty unreviewed working tree.

If the local SJC tree prevents a safe reviewed-SHA deployment, prepare the exact repository-cleanup and commit packet required, complete all other infrastructure work, and mark only deployment activation as blocked.

7.2 Two-source pilot

Choose two deterministic sources using explicit criteria:

* current health;
* stable extraction;
* useful SilverLeaf or county relevance;
* bounded volume;
* repeatability;
* low operational risk.

Do not automatically schedule agentic discovery before deterministic monitoring is proven.

7.3 Run bundle

Implement a stable run bundle containing only what the Mac needs.

Consider:

* run metadata;
* source events;
* normalized intelligence candidates;
* agent discovery candidates;
* raw excerpts or bounded raw captures;
* source-health records;
* logs;
* manifest;
* checksums;
* schema/version;
* producing revision;
* task/profile identity;
* time window;
* retry state.

Avoid transferring unnecessary caches, environments, or secrets.

7.4 Mac import

Implement or finalize a Mac-side pull/import workflow that is:

* pull-based unless an existing safer standard exists;
* authenticated;
* idempotent;
* checksum verified;
* resumable;
* duplicate safe;
* capable of partial-transfer recovery;
* capable of delayed collection if the Mac is offline;
* capable of replay;
* explicit about import authority;
* non-destructive to review state.

The Mac should import into the existing file-backed corpus or a clearly defined incoming staging area.

7.5 Acknowledgment and pruning

Implement:

bundle produced
→ bundle pulled
→ checksums verified
→ Mac import succeeds
→ receipt written
→ receipt transferred or observed
→ retention delay
→ VPS payload pruned

Pruning must never occur from transfer initiation alone.

Define behavior when:

* Mac is offline;
* transfer is partial;
* receipt is lost;
* bundle is duplicated;
* import fails;
* acknowledgment is delayed;
* disk pressure rises;
* a bundle must be replayed.

⸻

8. Workstream D — Hermes weekly runtime

8.1 Verify reality

Determine:

* installed runtime;
* invocation mechanism;
* model provider;
* credentials;
* cost;
* profiles;
* prompts;
* state;
* output;
* retries;
* timeouts;
* locks;
* concurrency;
* duplicate prevention;
* logs;
* health;
* failure semantics.

Do not infer runtime capability from prompt filenames.

8.2 Implement the smallest viable weekly runtime

The target is one bounded weekly run.

It must have:

* one scheduler authority;
* one writer authority;
* stable task/profile identity;
* explicit source and query scope;
* maximum runtime;
* maximum retries;
* duplicate lock;
* failure status;
* no-match status;
* partial status;
* bounded output size;
* explicit token/cost ceiling where applicable;
* structured output;
* evidence;
* health;
* no publication authority.

Hermes may:

* fetch approved sources;
* run bounded discovery;
* produce source events;
* produce intelligence candidates;
* classify candidates;
* produce run evidence.

Hermes may not:

* publish;
* promote sources automatically;
* change taxonomy without approval;
* bypass review;
* delete durable Mac data;
* expand scope without a task/profile change.

8.3 Scheduling

Configure or prepare:

* systemd service;
* weekly timer;
* randomized delay if appropriate;
* persistent behavior after downtime;
* timeout;
* kill behavior;
* lock;
* resource limits;
* log rotation;
* health;
* manual proof-run command;
* disabled/shadow mode;
* activation mode.

Use a schedule that does not conflict with existing workloads.

8.4 Proof sequence

Where possible within this task:

1. manual dry run;
2. manual real bounded run;
3. bundle creation;
4. Mac pull;
5. checksum validation;
6. import;
7. receipt;
8. prune simulation or safe proof;
9. rollback;
10. health verification.

Do not claim natural weekly-run evidence that cannot exist yet.

Leave the timer disabled if activation would occur before required proof gates.

If all roadmap and Ivy gates are satisfied and enabling the timer is safe, Buddy’s authorization in this task permits activation.

Record the exact decision.

⸻

9. Workstream E — PostgreSQL finalization

9.1 Decide the narrow role

Choose the narrowest useful SJC PostgreSQL role.

Expected candidate responsibilities:

* advisory locks;
* run records;
* source health;
* transfer manifests;
* receipt acknowledgments;
* retry/error state;
* compact metrics;
* small operational queues.

Do not store the durable corpus merely because migrations exist.

9.2 Reconcile existing database work

Inspect SJC migrations, adapters, retention tooling, metrics, and backup/restore design.

Classify existing work as:

* useful now;
* useful later;
* incompatible with Mac corpus authority;
* redundant;
* historical;
* should remain dormant.

Do not delete sound future-ready work merely because it is not activated.

9.3 Execute database work

Where PostgreSQL provides concrete value, Codex is authorized to:

* create database;
* create roles;
* create schemas;
* run approved migrations;
* add operational tables;
* add constraints;
* add indexes;
* add retention;
* configure grants;
* configure local-only access;
* configure backup/restore;
* verify rollback;
* register health.

Prefer project isolation.

Do not place generic Ivy operational state in an SJC-specific schema if multiple projects should reuse it.

Conversely, do not make an Ivy-global schema own project-specific data.

9.4 Documentation

Update docs/DATABASE.md and project DB docs so they accurately describe:

* actual live topology;
* ownership;
* retention;
* authority;
* backup;
* restore;
* operational versus durable data;
* onboarding for future repositories.

⸻

10. Workstream F — roadmap elaboration and builder handoff

The final purpose of this task is not only to perform risky work. It must make the remaining work executable by medium-strength agents.

10.1 Update roadmap detail

Update ROADMAP.md to reflect:

* final publication contract;
* final validation contract;
* final SilverLeaf release contract;
* actual Ivy admission status;
* actual Hermes/runtime status;
* actual PostgreSQL role;
* actual transfer contract;
* actual proof completed;
* remaining activation gates;
* exact builder tasks;
* dependencies;
* validation;
* stop conditions;
* ownership.

Preserve its role as the authoritative execution roadmap.

Do not add narrative session history.

10.2 Medium-agent task readiness

Every remaining implementation goal must include enough detail for a medium OpenCode agent:

* stable roadmap reference;
* outcome;
* exact input files;
* expected output files;
* in scope;
* out of scope;
* dependencies;
* acceptance criteria;
* exact validation;
* expected report;
* stop conditions;
* escalation conditions;
* Git policy;
* whether network access is permitted;
* whether another repository is involved;
* whether privileged execution is involved.

10.3 High-reasoning gates

Identify any remaining high-reasoning gates.

Do not automatically require another Strong Codex pass.

For each gate, state:

* what decision is required;
* why medium agents must not decide it;
* what evidence a preceding medium-agent report must collect;
* what exact question GPT should ask;
* what artifact should be produced;
* whether Buddy alone can decide;
* whether a small Strong Codex review is only contingently useful.

Examples may include:

* editorial publication-policy edge cases;
* portfolio repository deployment design;
* unexpected VPS capacity conflict;
* source authority dispute;
* privacy/provider decision for subscriptions;
* portability architecture after launch.

10.4 GPT coordination model

Document the expected workflow:

ROADMAP.md
    ↓
GPT prepares bounded tasks
    ↓
medium OpenCode or Hermes executes
    ↓
reports/NN-*.md records evidence
    ↓
GPT reviews report and keeps work aligned
    ↓
next bounded task

GPT will help Buddy:

* prepare detailed task packets;
* interpret reports;
* identify drift;
* prepare high-reasoning gates;
* keep medium agents aligned;
* decide when escalation is warranted;
* prevent repeated rediscovery.

Do not create a new task ledger.

Use:

* tasks/ for dispatched tasks;
* reports/ for task reports;
* prompts/ for reusable prompts;
* logs/runs/ for cadence runs;
* logs/agents/ for operational agent logs;
* ROADMAP.md for sequencing and gates.

10.5 Candidate task queue

In the report, propose the next bounded tasks in order.

Use exact filenames where practical.

The likely remaining builder sequence includes:

1. publication/corpus implementation;
2. SilverLeaf registry;
3. deterministic static export;
4. portfolio-site context;
5. static UI;
6. first reviewed release;
7. shadow-run evidence;
8. weekly activation verification;
9. subscriptions;
10. portability proof.

Revise this based on actual completed work.

⸻

11. Validation and proof

Run all safe relevant checks.

SJC baseline

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
python3 scripts/retention.py --json
python3 scripts/metrics_snapshot.py --backend file --json
git diff --check
git status --short

Use task-specific checks where implemented.

Ivy

Use repository-defined checks.

Validate:

* docs;
* templates;
* manifests;
* systemd units;
* shell scripts;
* permissions;
* health output;
* backup/restore;
* database manifest;
* rollback;
* live service state.

VPS

Capture:

* pre-change state;
* post-change state;
* changed services;
* changed timers;
* changed DB objects;
* resource usage;
* proof-run logs;
* bundle evidence;
* receipt evidence;
* pruning evidence;
* rollback evidence.

Redact secrets.

Git

Do not overwrite unrelated changes.

Record exact starting and final status for both repositories.

Do not claim changes are committed unless they are actually committed under repository policy.

⸻

12. Required report structure

Write reports/10-ivy-operational-admission.md with:

1. Executive outcome

State:

* what was finalized;
* what was executed;
* what is live;
* what remains disabled;
* whether weekly operation is ready;
* whether publication work is ready for medium agents.

2. Authorization used

List privileged actions performed under this task.

3. Starting state

Cover both repositories, VPS, PostgreSQL, services, timers, and resource condition.

4. Architecture decisions finalized

Include:

* publication;
* validation;
* SilverLeaf release;
* Hermes;
* VPS/Mac authority;
* transfer;
* PostgreSQL;
* reusable Ivy onboarding.

5. Ivy changes

Explain generic onboarding improvements.

6. SJC repository changes

Explain contract, roadmap, runtime, transfer, and documentation changes.

7. VPS changes

List exact deployed paths, users, permissions, services, timers, environment routes, and health registrations without exposing secrets.

8. PostgreSQL changes

List databases, roles, schemas, migrations, operational tables, grants, retention, backup, and rollback.

9. Hermes/runtime changes

Describe actual invocation, provider, scope, cost controls, locking, retry, timeout, output, and schedule.

10. Transfer proof

Document bundle, manifest, checksum, pull, import, receipt, acknowledgment, prune, replay, and failure behavior.

11. Validation

Record exact commands and results.

12. Rollback and recovery

State how to disable, revert, restore, replay, and recover.

13. Roadmap elaboration

Explain what detail was added so medium agents can execute.

14. High-reasoning gates

List any remaining gates and the reports/evidence needed before them.

15. Medium-agent work plan

Provide ordered bounded tasks with exact suggested filenames.

16. Hermes work plan

State which future cadence tasks Hermes may perform automatically and under what controls.

17. GPT coordination notes

State what GPT should inspect in each future report to keep work aligned.

18. Risks and unresolved items

Be explicit.

19. Final system status

Classify each:

* publication foundation;
* corpus validation;
* SilverLeaf registry;
* static export;
* portfolio UI;
* Ivy admission;
* VPS deployment;
* PostgreSQL;
* Hermes;
* transfer;
* weekly scheduling;
* portability.

Use:

* COMPLETE
* READY_FOR_MEDIUM_AGENT
* READY_BUT_DISABLED
* PARTIAL
* BLOCKED
* DEFERRED

20. Final task status

Use the established report status vocabulary.

⸻

13. Success criteria

Task 10 succeeds when:

1. the remaining high-risk architecture is resolved;
2. publication and release contracts are durable;
3. Ivy has a clearer reusable onboarding process;
4. SJC has been operationally admitted or every remaining deployment blocker is exact and minimal;
5. the weekly Hermes path is implemented or concretely prepared;
6. VPS-to-Mac transfer and acknowledgment are real, not aspirational;
7. pruning cannot occur before verified receipt;
8. PostgreSQL has a narrow justified role or is deliberately unused;
9. unrelated workloads remain safe;
10. rollback and recovery are demonstrated;
11. roadmap status matches reality;
12. medium agents can perform remaining work from detailed roadmap goals;
13. high-reasoning gates are prepared by explicit report requirements;
14. GPT can keep future agents aligned through the task/report flow;
15. no further broad Strong Codex planning pass is required.

⸻

14. Governing instruction

Use this final Strong Codex pass to push SJC_Intel through the risky architecture, Ivy onboarding, VPS, PostgreSQL, Hermes, transfer, and operational work. Improve Ivy for future repositories, preserve Mac corpus authority, and leave ROADMAP.md detailed enough that medium OpenCode agents and Hermes can finish the product under GPT-guided task/report control.