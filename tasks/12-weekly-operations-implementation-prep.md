Task 12 — Weekly Operations Implementation Preparation

Session

This is a new OpenCode agent session.

Work from:

/Users/buddy/projects/sjc_intel

Read repository authority before acting:

README_INTERNAL.md
AGENTS.md
ROADMAP.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md
docs/publication_release_contract.md
tasks/README.md
reports/README.md
reports/10-ivy-operational-admission.md
reports/11-operational-admission-continuation.md

Also inspect relevant Ivy documentation read-only at:

/Users/buddy/projects/ivy-control-vps

Begin with its repository entrypoint and follow its authority hierarchy. Do not assume permission for privileged VPS operations.

Required report

Write:

reports/12-weekly-operations-implementation-prep.md

Follow reports/README.md.

Mission

Prepare SJC_Intel for a bounded weekly VPS/Hermes workflow and remove every local implementation blocker that a medium-strength agent can safely resolve.

The target workflow is:

weekly scheduled run on VPS
→ monitor approved canonical sources
→ run bounded discovery for potential new sources
→ produce intelligence candidates and source proposals
→ create a manifested transfer bundle
→ Mac pulls and verifies the bundle
→ Mac imports it without damaging review state
→ receipt and acknowledgement are recorded
→ VPS payload becomes eligible for delayed pruning

The weekly workflow must never publish, promote sources automatically, change taxonomy automatically, or bypass human review.

This task is not authorized to deploy to the VPS, modify PostgreSQL, install systemd units, configure secrets, or perform privileged Ivy operations.

It should implement everything safely possible in the SJC repository and produce a precise privileged follow-up packet for the remaining Ivy work.

⸻

1. Verify current repository and remote state

Inspect and report:

* current branch;
* current HEAD;
* clean or dirty working tree;
* configured remotes;
* whether origin/master now exists;
* whether SHA 1be2ade is present remotely;
* whether GitHub main contains unrelated or initialized content;
* whether local master can be pushed safely without overwriting main.

Do not force-push.

Do not rewrite history.

If authentication remains blocked, report the exact minimal Buddy action. Continue all other work.

⸻

2. Understand the existing monitoring system

Inspect actual code, prompts, registries, monitor specifications, cadence documents, data artifacts, and prior run reports.

Document:

* which canonical sources are currently monitored;
* which monitors are deterministic scripts;
* which are manual;
* which are prompt-led;
* which have passed pilots;
* which two sources are safest for an initial VPS shadow run;
* what outputs each monitor currently creates;
* where dedupe and review-queue rebuilding occur;
* what assumptions currently require local execution.

Do not select two pilot sources silently. Recommend them with evidence.

⸻

3. Define the weekly operational contract

Create a durable supporting document at the repository location most consistent with existing conventions.

Suggested name:

docs/weekly_operational_contract.md

Use a different location only when repository authority clearly indicates a better one.

The contract must define:

Inputs

* approved canonical sources;
* source registry revision;
* tracked entities;
* search profiles;
* taxonomy/configuration revision;
* run time window;
* prior dedupe state;
* explicit runtime budget.

Stage A — canonical-source monitoring

The run should produce:

* source-health result;
* source events;
* normalized intelligence candidates;
* source URLs;
* evidence excerpts;
* duplicate, no-match, partial, and failed outcomes;
* bounded raw captures only where required.

Stage B — bounded source discovery

The run should search for:

* newly relevant public sources;
* missing source coverage;
* moved or replaced sources;
* SilverLeaf-specific sources;
* gaps involving schools, roads, utilities, development, government, communities, and tracked entities.

Discovery may produce proposals only.

Each source proposal should include:

* candidate ID;
* source name;
* URL;
* source family;
* authority level;
* discovered through;
* evidence;
* relevance rationale;
* geographic relevance;
* coverage gap addressed;
* recommended disposition;
* confidence;
* review status.

The run must not:

* promote candidates into registry/sources.yaml;
* remove canonical sources;
* change taxonomy;
* change permanent scope;
* publish intelligence;
* treat social media as sole consequential evidence.

Outputs

Define exact artifact classes and proposed paths for:

* run record;
* source-health results;
* source events;
* intelligence candidates;
* source proposals;
* bounded logs;
* manifest;
* checksums;
* failure summary.

Runtime controls

Define:

* one run ID;
* one writer;
* duplicate-run prevention;
* maximum runtime;
* retry ceiling;
* query/fetch ceiling;
* token or cost ceiling for agentic work;
* partial-run behavior;
* failure behavior;
* no-match behavior;
* restart/replay behavior;
* stop conditions.

Review boundary

State explicitly:

candidate intelligence ≠ verified intelligence
verified intelligence ≠ published intelligence
source proposal ≠ canonical source

⸻

4. Specify the transfer-bundle contract

Define a stable, versioned bundle format suitable for transfer from VPS to Mac.

The bundle should contain only required artifacts.

At minimum consider:

bundle/
  manifest.json
  checksums.sha256
  run.json
  source_health/
  source_events/
  intel_candidates/
  source_proposals/
  logs/

The manifest should include:

* bundle schema version;
* run ID;
* producing Git SHA;
* producing task/profile;
* source-registry revision;
* start/end timestamps;
* run status;
* included files;
* file sizes;
* checksums;
* candidate counts;
* failure counts;
* replay identity.

Define:

* deterministic file layout;
* checksum algorithm;
* duplicate bundle semantics;
* partial transfer handling;
* safe replay;
* import failure behavior;
* Mac-offline retention behavior;
* acknowledgement format;
* delayed-prune eligibility;
* prohibition on pruning before verified acknowledgement.

⸻

5. Implement bounded local tooling where appropriate

Inspect the repository before choosing implementation.

Implement the smallest coherent local foundation that medium agents can safely complete now.

Likely candidates include:

* bundle builder;
* bundle validator;
* manifest generator;
* checksum generator;
* incoming-bundle validator;
* idempotent Mac-side staging/import command;
* receipt generator;
* sample bundle fixture;
* tests.

Do not invent a second storage system.

Preserve the file-backed corpus as authority.

Do not overwrite reviewed corpus or review state during test imports.

A safe first implementation may import into an explicit incoming/staging area rather than directly merging into authoritative data.

Use repository conventions and update the roadmap if implementation details materially clarify an existing goal.

⸻

6. Prepare the Hermes execution specification

Inspect existing Hermes prompts and task contracts.

Create or update a reusable SJC weekly task specification that tells VPS Hermes exactly:

* what repository revision to run;
* what sources to monitor;
* what discovery profile to use;
* what data it may read;
* what files it may write;
* what commands it may run;
* what network access is permitted;
* what it must never change;
* runtime, cost, retry, and scope limits;
* expected bundle outputs;
* report/run-log requirements;
* stop and escalation conditions.

Do not claim a Hermes runtime capability that is not verified.

Separate:

* repository-side task contract;
* Ivy-side provider credentials;
* Ivy-side systemd scheduling;
* privileged deployment.

⸻

7. Review Ivy onboarding requirements

Read the current Ivy onboarding, VPS, database, health, orchestration, transfer, and admission documentation.

Report whether the proposed SJC weekly contract fits the generic Ivy process.

Identify:

* reusable Ivy components already available;
* project-specific work required;
* missing Ivy helpers or templates;
* contradictions or stale documentation;
* exact privileged changes still required;
* whether PostgreSQL provides any concrete value for this first workflow.

Prefer no SJC PostgreSQL unless locks, run state, health, or acknowledgements clearly benefit from it.

Do not modify protected or private Ivy files in this task.

Instead, prepare a detailed proposed privileged packet.

⸻

8. Prepare the privileged Ivy/VPS packet

The report must include a complete packet suitable for a later authorized Ivy operator or Strong Codex execution.

It should specify:

* deployable remote and exact SHA;
* VPS checkout path;
* service account;
* directories;
* permissions;
* Python environment;
* dependency command;
* environment variables and secret names, without values;
* Hermes provider requirement;
* manual invocation command;
* systemd service design;
* weekly timer design;
* lock method;
* timeout;
* resource limits;
* logs;
* health output;
* bundle output path;
* Mac pull command or contract;
* receipt/acknowledgement path;
* retention period;
* delayed-prune command;
* rollback;
* shadow-run sequence;
* activation gates.

Use exact proposed paths and commands where repository/Ivy conventions support them.

Label anything uncertain as requiring live verification.

⸻

9. Roadmap elaboration

Update ROADMAP.md only where necessary to make subsequent medium-agent work executable.

Do not rewrite its architecture.

Add or refine:

* exact weekly-contract references;
* exact bundle/import dependencies;
* builder task boundaries;
* validation commands;
* high-reasoning/privileged gates;
* required preceding report evidence;
* stop conditions.

Ensure GPT can use the roadmap and Task 12 report to dispatch the next bounded tasks without rediscovery.

⸻

10. Validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
git diff --check
git status --short
git branch --show-current
git remote -v

Run tests for any new tooling.

Do not:

* fetch live production sources unless an existing test explicitly requires it;
* modify VPS state;
* modify PostgreSQL;
* install services;
* configure provider credentials;
* enable timers;
* commit;
* push;
* discard unrelated changes.

⸻

11. Required report structure

Write reports/12-weekly-operations-implementation-prep.md with:

1. Executive result
2. Starting Git and remote state
3. Sources and current monitor capabilities
4. Recommended initial two-source pilot
5. Weekly operational contract
6. Bounded source-discovery contract
7. Bundle and manifest contract
8. Local tooling implemented
9. Hermes weekly task specification
10. Ivy compatibility assessment
11. Exact privileged VPS packet
12. PostgreSQL recommendation
13. Validation results
14. Files changed
15. Remaining Buddy actions
16. Remaining privileged actions
17. Next medium-agent tasks
18. Risks and unresolved issues
19. Final status

Use the established final-status vocabulary.

Success criteria

This task is complete when:

* the weekly workflow is precisely documented;
* canonical monitoring and source discovery are clearly separated;
* source proposals cannot be promoted automatically;
* transfer and acknowledgement semantics are explicit;
* local bundle/import foundations are implemented or decomposed into exact tasks;
* Hermes has a bounded repository-side execution specification;
* Ivy’s remaining privileged work is expressed as an executable packet;
* the roadmap contains sufficient detail for later agents;
* no further broad architectural discovery is required.