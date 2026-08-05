Task 14 — Publish Readiness and VPS Onboarding

Session

This is a new OpenCode agent session.

Work primarily from:

/Users/buddy/projects/sjc_intel

Inspect ivy-control-vps as a second repository:

/Users/buddy/projects/ivy-control-vps

This task is broader than a single implementation patch. It is a publish-readiness, repository-cleanup, backup-policy, Hermes-scheduling, and Ivy-onboarding preparation task.

Do not perform privileged VPS changes unless the applicable Ivy authority explicitly permits them for this agent. Where privileged work is required, produce an exact execution packet.

Required report

Write:

reports/14-publish-readiness-and-vps-onboarding.md

Follow reports/README.md.

Mission

Move SJC_Intel materially closer to being portfolio-ready and operationally onboarded to Ivy.

This task must:

1. determine exactly what remains before the repository is publish-ready;
2. consolidate remaining medium-sized implementation work into practical work packages;
3. perform a full repository-cleanup preflight with clear explanations;
4. define the external-backup policy for SJC_Intel;
5. identify where generic backup requirements belong in Ivy onboarding;
6. inspect all relevant Ivy onboarding, backup, restore, retention, scheduling, Hermes, and control-plane documentation;
7. determine the current intended SJC PostgreSQL position and remove ambiguity;
8. determine how project repositories should submit recurring Hermes tasks to the VPS;
9. prepare a testable weekly Hermes schedule that can be set minutes into the future for initial automation proof;
10. update SJC and Ivy documentation where safely authorized and appropriate;
11. leave exact remaining builder and privileged tasks;
12. avoid further broad architectural rediscovery.

The governing objective is:

Make SJC_Intel publish-ready quickly, while using it to improve Ivy’s reusable onboarding, backup, scheduling, and Hermes-task model for future repositories.

⸻

1. Required source material

1.1 SJC_Intel

Read at minimum:

README_INTERNAL.md
AGENTS.md
ROADMAP.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md
docs/publication_release_contract.md
docs/weekly_operational_contract.md
docs/weekly_operator_guide.md
docs/backup-restore.md
docs/retention.md
docs/postgresql_adapter.md
tasks/README.md
reports/README.md
reports/10-ivy-operational-admission.md
reports/11-operational-admission-continuation.md
reports/12-weekly-operations-implementation-prep.md
reports/13-candidate-to-corpus-import.md

Inspect actual implementation in:

scripts/
schemas/
registry/
data/
tests/
runtime/
prompts/
reports/
tasks/
logs/
db/

1.2 Ivy Control VPS

Begin from its entrypoint and authority documents.

Inspect at minimum, where present:

README.md
docs/VPS_INVENTORY.md
docs/DATABASE.md
docs/VPS_ADMISSION_CHECKLIST.md
docs/PORTFOLIO_CONVENTIONS.md
docs/HEALTH_CONTRACT.md
agents/VPS_ORCHESTRATION.md
_internal/vps-inventory-and-runbook.md
_internal/
templates/
tools/
deploy/
systemd/

Also inspect the best prior onboarding examples.

1.3 GitHub and remote state

Repository remote:

https://github.com/wguDataNinja/sjc-intel

Inspect:

* local branch and HEAD;
* remote branches;
* whether local changes are committed;
* whether origin/master matches;
* whether repository presentation is public-ready;
* whether README, license, topics, and description are adequate;
* whether sensitive/private operational material is excluded.

Do not expose secrets or private Ivy material.

⸻

2. Publish-readiness assessment

Define what remains before SJC_Intel can be considered publish-ready.

Separate:

Required before public launch

Likely areas include:

* publication contract implementation;
* complete corpus validation;
* SilverLeaf scope registry;
* reviewed-only static release export;
* stable search/filter data;
* portfolio-site integration;
* public methodology and limitations;
* architecture/case-study explanation;
* release rollback;
* repository cleanup;
* license;
* public-safe README;
* screenshots or demo material.

Valuable but non-blocking

Examples:

* weekly VPS automation;
* SJSO RSS monitor;
* BCC workspace mode;
* subscriptions;
* second-domain portability proof;
* operational PostgreSQL metadata.

Deferred

Examples:

* live incidents;
* PostGIS;
* semantic search;
* public API;
* full multi-domain platform;
* autonomous publication;
* real-time alerts;
* user accounts.

Produce a short, prioritized publish-ready sequence.

Do not inflate the launch gate.

⸻

3. Repository-cleanup preflight

Perform a full cleanup preflight.

Do not silently delete or rewrite artifacts.

Classify every relevant tracked, modified, and untracked artifact as:

* authoritative;
* current implementation;
* generated but durable;
* generated and reproducible;
* historical;
* private;
* stale;
* superseded;
* duplicate;
* test fixture;
* runtime-only;
* backup-required;
* safe to ignore;
* candidate for deletion;
* candidate for compression;
* candidate for archive.

Inspect:

* root files;
* data/;
* runtime/;
* logs/;
* tasks/;
* reports/;
* .opencode/;
* db/;
* fixtures;
* generated bundles;
* incoming staging;
* receipts;
* monthly wraps;
* source events;
* raw captures;
* review queue;
* dedupe index;
* candidate/proposal records.

For each cleanup recommendation, explain:

* what the artifact is;
* why it exists;
* whether it is authoritative;
* whether it can be regenerated;
* whether it should be committed;
* whether it should be backed up;
* whether it should be compressed;
* whether it should be deleted;
* whether action is safe now;
* what verification is required first.

The Task 14 report must contain a concise cleanup table Buddy can review before any destructive action.

Do not delete durable or unexplained artifacts.

⸻

4. External-backup policy for SJC_Intel

Define exactly what must be externally backed up.

The initial bias is:

Back up everything that is durable, difficult to reproduce, editorially significant, or operationally necessary.

Evaluate whether “everything” is practical.

4.1 Classify data by backup priority

At minimum classify:

Must back up

Likely includes:

* source registry;
* source candidates;
* tracked entities;
* communities/geography;
* intelligence items;
* source events;
* review decisions;
* publication decisions;
* release manifests;
* release artifacts;
* dedupe state where useful;
* incoming accepted bundles;
* receipts and acknowledgments;
* source proposals;
* task reports;
* critical run logs;
* schema and migration history;
* configuration;
* operator documentation;
* deployment manifests;
* secret-name contracts, but never secret values in normal backups.

Reconstructable but worth backing up

Likely includes:

* generated indexes;
* summary files;
* search indexes;
* release projections;
* metrics snapshots;
* derived reports.

Optional or excluded

Likely includes:

* virtual environments;
* caches;
* temporary workspace;
* transient raw downloads;
* duplicate bundle copies;
* test outputs;
* logs beyond retention;
* local secrets.

4.2 Size and compression

Measure current storage by category.

Report:

* file counts;
* uncompressed size;
* compressibility;
* expected growth;
* backup frequency;
* estimated archive size;
* whether full or incremental backup is appropriate;
* whether raw HTML/XML should be compressed;
* whether old bundles should be tarred and compressed;
* whether content-addressed dedupe is useful;
* retention period.

Use real measurements where safe.

4.3 Restore objective

Define what must be restorable.

At minimum:

* recover the corpus;
* recover review state;
* recover release history;
* recover source registry;
* recover incoming bundles;
* reproduce a public release;
* resume weekly operations;
* validate integrity;
* restore to a clean Mac checkout.

Define restore-order dependencies.

4.4 Backup destination and ownership

Inspect existing Ivy and portfolio backup conventions.

Determine:

* what “external backup” means in this ecosystem;
* whether the destination is another machine, cloud storage, object storage, encrypted archive, or existing backup service;
* who initiates backup;
* who verifies it;
* encryption expectations;
* retention;
* checksum and manifest requirements;
* restore-test cadence;
* failure alerting.

Do not invent credentials or providers.

If the destination is undecided, prepare the provider-neutral contract.

4.5 Required SJC backup document

Recommend and, if appropriate, create or update the authoritative SJC backup policy.

Prefer extending an existing authority such as:

docs/backup-restore.md

Do not create a duplicate policy if the current file can be made authoritative.

The document should define:

* backup scope;
* exclusions;
* archive layout;
* compression;
* frequency;
* manifest;
* checksums;
* encryption boundary;
* retention;
* restore procedure;
* restore verification;
* responsibility;
* failure handling.

⸻

5. Surface backup as a generic Ivy onboarding requirement

SJC_Intel is a good test case because it is moving from:

local-only repository
→ VPS workload

The Ivy onboarding process must require every new repository to answer:

* what data is durable;
* what data is ephemeral;
* what remains on VPS;
* what transfers elsewhere;
* what must be backed up externally;
* backup frequency;
* retention;
* compression;
* encryption;
* restore procedure;
* restore-test evidence;
* ownership;
* failure alerting;
* prune gate;
* whether deployment may begin before backup is configured.

Inspect existing Ivy backup and onboarding docs.

Recommend the correct authority location.

Possible locations may include:

* docs/VPS_ADMISSION_CHECKLIST.md;
* docs/DATABASE.md;
* a generic backup contract;
* a workload-manifest template;
* a portfolio conventions document.

Choose the smallest coherent authority structure.

Do not create several overlapping backup documents.

Where this agent is permitted to edit Ivy docs, make the minimal reusable improvement.

Otherwise include an exact proposed patch in the report.

The generic Ivy onboarding gate should require:

backup scope defined
→ first backup completed
→ checksum verified
→ restore path documented
→ restore test scheduled or completed

No repo should become a production VPS workload without an explicit backup disposition.

⸻

6. Clarify PostgreSQL policy for SJC

Determine and document the current accepted decision.

The working direction has been:

* no durable SJC corpus in VPS PostgreSQL;
* Mac file corpus remains authoritative;
* PostgreSQL is optional;
* PostgreSQL may later hold narrow operational metadata;
* SQL readiness is preserved;
* database work must not block launch.

Verify this against:

* ROADMAP.md;
* VPS_ROADMAP.md;
* docs/VPS_CONTINUITY.md;
* docs/postgresql_adapter.md;
* docs/DATABASE.md in Ivy;
* Task 08–13 reports.

Resolve contradictions.

Classify the current SJC PostgreSQL mode as one of:

* NOT_USED;
* DORMANT_FUTURE_READY;
* OPERATIONAL_METADATA_ONLY;
* BOUNDED_STAGING;
* CORPUS_AUTHORITY.

The expected answer is likely:

DORMANT_FUTURE_READY

or:

OPERATIONAL_METADATA_ONLY

Do not activate PostgreSQL merely to make use of existing migrations.

Document:

* what is intentionally unused;
* what remains future-ready;
* what would trigger activation;
* what must never become an accidental second authority.

⸻

7. Hermes task-submission and scheduling model

Determine how a project repository should submit recurring Hermes tasks to the VPS.

Buddy can configure tasks manually, but the preferred model is:

Each onboarded repository can declare bounded Hermes tasks through a documented, reviewable workflow.

Inspect actual Ivy and Hermes state.

Determine:

* where Hermes is installed;
* current version;
* provider/auth status;
* how tasks are invoked;
* whether task files are read from the deployed repository;
* whether Ivy has a central registry;
* whether systemd invokes Hermes directly or through wrappers;
* how task identity is represented;
* how a repository declares cadence;
* how tasks are reviewed;
* how approved SHA is enforced;
* how credentials are referenced;
* where outputs go;
* where logs go;
* how costs and timeouts are bounded;
* how duplicate runs are prevented;
* how tasks are disabled;
* how a one-time near-future test schedule is created;
* how a recurring weekly schedule is activated afterward.

7.1 Desired reusable workflow

Evaluate a model such as:

project repo
  declares task specification
        ↓
Ivy admission/review
        ↓
Ivy deploy manifest references task
        ↓
systemd service invokes Hermes
        ↓
systemd timer controls schedule
        ↓
project output contract governs bundles

Do not assume this exact implementation if current Ivy conventions differ.

7.2 Repository-side task declaration

Determine whether SJC should declare:

* task ID;
* prompt path;
* profile;
* approved sources;
* discovery budget;
* output path;
* timeout;
* retry count;
* environment requirements;
* secret names;
* schedule recommendation;
* health output;
* bundle contract version;
* enabled/disabled state.

Recommend the authoritative file and schema.

Prefer extending existing manifests or prompt/task contracts rather than adding another parallel registry.

7.3 Ivy-side scheduling

Determine whether Ivy should own:

* service unit;
* timer unit;
* enablement;
* exact schedule;
* randomized delay;
* environment;
* resource limits;
* deployment SHA;
* health;
* rollback.

The likely answer is yes.

Document the responsibility split.

7.4 Test schedule minutes from now

Prepare a safe test procedure that can schedule the SJC weekly task for a few minutes in the future.

The purpose is to prove:

* timer activation;
* service invocation;
* Hermes execution;
* output creation;
* logging;
* health;
* bundle generation;
* transfer readiness.

The test must:

* use an explicitly bounded task;
* use a temporary test timer or transient override;
* avoid waiting a week;
* preserve the eventual weekly schedule;
* be easy to disable;
* avoid duplicate runs;
* record exact start time;
* record exact expected completion window;
* record rollback.

Do not enable or modify production scheduling unless this task is explicitly authorized under Ivy policy.

If not authorized, produce the exact commands and packet for the privileged operator.

After the proof, recommend an ideal recurring weekly window based on current VPS workload overlap.

⸻

8. SJC weekly task contents

The scheduled Hermes workflow should include two distinct stages.

Stage A — canonical-source monitoring

Run approved deterministic monitors and produce:

* source health;
* source events;
* intelligence candidates;
* evidence;
* duplicate/no-match/partial/failure statuses;
* bundle artifacts.

Stage B — bounded discovery

Search for:

* new relevant sources;
* moved endpoints;
* source-health failures;
* SilverLeaf coverage gaps;
* missing coverage for roads, schools, utilities, government, communities, and development.

Produce source proposals only.

Hermes must not:

* promote sources;
* change taxonomy;
* publish;
* edit reviewed corpus;
* bypass human review;
* widen permanent scope without a reviewed task change.

Ensure the existing SJSO RSS monitor-update proposal can be incorporated through the approved source-review path.

Determine whether SJSO RSS and BCC workspace support should be implemented in this task or left as exact next builder tasks.

Prefer combining small safe implementation work where it materially improves publish or shadow-run readiness.

⸻

9. Publish-ready implementation work

This task may implement medium-sized, clearly bounded work that materially shortens the launch path.

Evaluate whether to complete any of the following now:

* SJSO RSS workspace monitor;
* BCC workspace mode;
* corpus validator;
* publication selector;
* SilverLeaf scope registry;
* static public release builder;
* search index;
* public-safe architecture document;
* README/public presentation cleanup;
* license;
* release artifact examples.

Do not attempt all work indiscriminately.

Choose work based on:

* launch impact;
* dependency order;
* current context;
* safe scope;
* testability;
* whether another repo is required.

The report must state what was completed versus deferred.

⸻

10. Public architecture and portfolio artifact

Assess whether the repository has a polished public architecture document.

A portfolio-quality artifact should explain:

* problem;
* product;
* architecture;
* source discovery;
* deterministic monitoring;
* agentic discovery;
* evidence model;
* review model;
* weekly operations;
* VPS/Mac split;
* publication;
* portability;
* limitations;
* future domains.

Recommend the authoritative location.

Potentially:

docs/ARCHITECTURE.md

or a public section in README.md.

Do not duplicate README_INTERNAL.md.

The public artifact must not expose private host details, secrets, internal paths, or operational vulnerabilities.

Prepare recommendations for diagrams and screenshots.

Implementation may be included if safely bounded.

⸻

11. Ivy onboarding completeness review

Because SJC was not previously in the Ivy control plane, inspect whether onboarding covers:

* repository identity;
* remote;
* approved SHA;
* deployment path;
* service account;
* permissions;
* environment;
* secrets;
* Python/runtime dependencies;
* Hermes task declarations;
* schedule;
* output contract;
* transfer;
* acknowledgments;
* pruning;
* backup;
* restore;
* health;
* alerting;
* logs;
* retention;
* resource budget;
* network policy;
* PostgreSQL disposition;
* rollback;
* removal/offboarding;
* ownership;
* documentation;
* proof run;
* natural-run verification.

Identify missing generic controls.

SJC should become a reference onboarding case for future repositories.

⸻

12. Roadmap and documentation updates

Update ROADMAP.md only where verified implementation or decisions materially change task status, dependencies, or sequencing.

Update SJC and Ivy docs only where authorized and necessary.

Do not create duplicate roadmaps.

Ensure durable documentation retains:

* backup policy;
* PostgreSQL disposition;
* Hermes task-submission model;
* scheduling test procedure;
* external-backup onboarding requirement;
* SJC onboarding status;
* publish-ready sequence;
* remaining human decisions.

⸻

13. Validation

Run at minimum for SJC:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
python3 scripts/retention.py --json
python3 scripts/metrics_snapshot.py --backend file --json
git diff --check
git status --short
git branch --show-current
git remote -v

Run targeted tests for any new implementation.

For backup analysis, record safe size commands and results.

For Ivy, use repository-defined validation commands.

Do not:

* expose secrets;
* delete data;
* prune backups;
* modify production VPS state without authority;
* activate timers without authority;
* run destructive migrations;
* force-push;
* overwrite unrelated changes;
* commit or push without explicit instruction.

⸻

14. Required report structure

Write reports/14-publish-readiness-and-vps-onboarding.md with:

1. Executive result
2. Starting SJC Git state
3. Starting Ivy state
4. Publish-readiness assessment
5. Required launch work
6. Non-blocking work
7. Deferred work
8. Repository-cleanup preflight
9. Backup scope classification
10. Backup size and compression findings
11. SJC external-backup policy
12. Ivy generic backup-onboarding requirement
13. Restore requirements
14. SJC PostgreSQL disposition
15. Hermes runtime reality
16. Repository-to-Hermes task-submission model
17. Systemd scheduling model
18. Near-future test schedule packet
19. Recommended recurring weekly schedule
20. SJC weekly task scope
21. Ivy onboarding completeness review
22. Implementation completed
23. Files changed
24. Validation results
25. Remaining Buddy actions
26. Remaining medium-agent tasks
27. Remaining privileged Ivy actions
28. Risks and unresolved issues
29. Final Git status
30. Final task status

Use the established final-status vocabulary.

⸻

15. Success criteria

This task is complete when:

1. the remaining path to portfolio publication is short and explicit;
2. repository cleanup is fully classified and explained;
3. SJC’s external-backup scope is defined;
4. backup size/compression/retention are evidence-based;
5. restore requirements are documented;
6. Ivy onboarding requires an explicit external-backup disposition for every repo;
7. SJC’s PostgreSQL status is unambiguous;
8. the repository-to-Hermes task-submission model is understood or proposed precisely;
9. the scheduling authority split is clear;
10. a minutes-from-now automation test packet exists;
11. an ideal recurring weekly schedule is recommended;
12. small launch-critical implementation work is completed where practical;
13. SJC is a stronger reference case for onboarding future repositories;
14. remaining medium and privileged tasks require no broad rediscovery;
15. Buddy can focus mainly on UI, editorial approval, credentials, and final publication.