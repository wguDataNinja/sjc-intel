# Task 09 — Codex Redesign 2

Task 09 — Codex Redesign 2

Task type

Authoritative roadmap rewrite and completion-plan consolidation.

This is a follow-up Strong Codex session to Task 08. Reuse the architectural and repository context already gathered. Do not repeat broad discovery unless a specific fact must be rechecked before changing an authority document.

Required output

Write the task report to:

reports/09-codex-redesign-2.md

Follow reports/README.md, including:

* task identity;
* starting Git state;
* files inspected and changed;
* work performed;
* validation commands and results;
* evidence provenance;
* final Git status;
* unresolved issues;
* risks;
* candidate next tasks;
* final status.

Use one of:

* COMPLETE
* COMPLETE_WITH_FOLLOW_UP
* PARTIAL
* BLOCKED
* HUMAN_DECISION_REQUIRED

⸻

1. Mission

Rewrite ROADMAP.md as the single authoritative execution roadmap for taking SJC_Intel from its current state to a publishable, portfolio-worthy SilverLeaf intelligence product.

The rewritten roadmap must:

1. incorporate the accepted findings from Task 08;
2. sequence the shortest credible route to publication;
3. preserve the Mac as the durable file-corpus authority;
4. keep VPS work bounded and explicitly gated;
5. keep PostgreSQL optional and narrow;
6. preserve deliberate seams for future reuse;
7. make work executable by medium-strength OpenCode agents;
8. distinguish launch requirements from post-launch improvements;
9. remove or resolve roadmap conflicts;
10. remain concise enough to function as an operating document.

Do not turn the roadmap into an architectural essay or duplicate all supporting documentation.

The governing objective is:

Publish soon, preserve correctness, use the low-cost VPS intelligently, and leave deliberate seams for future reuse.

⸻

2. Primary authority

Use the Task 08 report as the principal planning input:

reports/08-codex-redesign-1.md

Also read:

README_INTERNAL.md
AGENTS.md
BACKLOG.md
ROADMAP.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md
tasks/README.md
reports/README.md

Consult supporting planning, schema, workflow, product-direction, data-model, and Ivy VPS documents only where needed to ensure the rewrite is accurate.

Do not re-open decisions already resolved in Task 08 unless:

* repository state has materially changed;
* the report contains a factual error;
* two accepted recommendations conflict;
* implementation sequencing exposes a genuine dependency problem.

Record any such correction in the Task 09 report.

⸻

3. Accepted direction

Treat the following as accepted roadmap direction.

3.1 Product

The first public product is a reviewed, static SilverLeaf Intelligence experience on Buddy’s portfolio website.

It should provide:

* reviewed SilverLeaf-relevant intelligence;
* source attribution and original-source links;
* keyword search;
* topic, entity, and place filtering;
* release/update timestamp;
* methodology and limitations;
* a clear architecture and portfolio explanation.

The site must remain usable when the VPS is unavailable.

3.2 Publication

Automation may discover, fetch, extract, classify, and prepare candidates.

Human review remains required before public publication.

verified must not automatically mean published.

The roadmap must require an explicit publication decision and deterministic reviewed-only export.

3.3 Scope

The launch product is periodic, reviewed neighborhood intelligence.

Explicitly exclude from the launch critical path:

* live incidents;
* emergency alerting;
* real-time traffic or outage service;
* complete county coverage;
* autonomous publication;
* broad subscription infrastructure;
* full GIS/PostGIS;
* a public API;
* a generic multi-domain product.

3.4 Data authority

The Mac file corpus remains authoritative for:

* durable intelligence items;
* source events;
* review state;
* historical memory;
* publication preparation;
* archives;
* restore.

Do not require PostgreSQL corpus authority.

Preserve file compatibility and SQL readiness.

3.5 VPS

The VPS is a low-cost, always-on operational node used for:

* bounded deterministic fetching;
* later bounded agentic work;
* scheduler uptime;
* temporary run artifacts;
* health state;
* transfer preparation;
* small operational metadata where justified.

The VPS should transfer durable outputs to the Mac promptly.

Deployment, services, timers, secrets, PostgreSQL changes, and production scheduling require separate Ivy-controlled authorization.

3.6 PostgreSQL

The initial static launch may use no SJC PostgreSQL.

After VPS admission, PostgreSQL Option B may be used narrowly for:

* locks;
* run state;
* source health;
* transfer manifests;
* transfer acknowledgements;
* bounded operational queues.

It must not become a hidden launch prerequisite.

Option C or D must remain deferred unless operational evidence later justifies them.

3.7 Agent runtime

There is no production Hermes runtime for SJC.

Do not make a new Hermes platform a launch dependency.

Initial automation should rely on bounded deterministic scripts and the existing task/report harness.

Agentic discovery may initially remain manually triggered and bounded, producing candidates only.

3.8 Reusability

The roadmap should preserve this separation:

generic intelligence patterns
        ↓
SJC domain implementation
        ↓
SilverLeaf publication lens

Make only the minimum generic boundaries needed now.

Do not require broad extraction-framework, identity, database, or multi-domain redesign before launch.

⸻

4. Required roadmap structure

Rewrite ROADMAP.md around stable numbered sections that can be referenced by agents, such as:

§1
§2
§3A
§3A-G1

Choose a clear scheme and use it consistently.

The roadmap must contain the following sections.

4.1 Purpose and finish line

State:

* what SJC_Intel is;
* what the launch product is;
* what “publishable” means;
* what is explicitly not part of launch;
* the three-layer generic/SJC/SilverLeaf model.

Keep this section brief.

4.2 Current verified baseline

Use current verified facts from Task 08, including:

* file-backed authority;
* working evidence/review spine;
* current validation limitations;
* absence of publication state/export;
* absence of public UI/search;
* absence of Hermes runtime;
* absence of SJC VPS deployment;
* current dirty/uncommitted repository condition where relevant.

Do not copy stale README counts into the roadmap.

Use only counts that are useful to execution.

4.3 Launch gates

Define explicit gates for:

1. data and publication readiness;
2. SilverLeaf relevance;
3. static export;
4. public UI;
5. VPS pilot;
6. limited scheduling;
7. post-launch subscriptions.

Each gate must state:

* required outcome;
* dependencies;
* acceptance criteria;
* verification;
* stop conditions;
* required authority;
* suggested agent strength.

4.4 Work phases

Use the Task 08 phases as the starting point:

* P1 — Publication contract and clean corpus
* P2 — SilverLeaf lens and static release
* P3 — Portfolio UI
* P4 — Bounded operations pilot
* P5 — Limited automation and post-launch subscriptions

You may rename or divide phases if needed, but preserve the core sequence unless there is a documented dependency reason not to.

4.5 Launch milestone

Define one unambiguous launch milestone.

It should require at minimum:

* explicit publication state or release manifest;
* complete-corpus validation for publication-relevant fields;
* deterministic reviewed-only export;
* defensible SilverLeaf inclusion rules;
* static portfolio UI;
* search and filters;
* source links;
* methodology/limitations;
* rollbackable release;
* documented operator release workflow.

The initial launch must not depend on VPS automation.

4.6 Operational activation milestone

Define a separate post-launch or parallel milestone for VPS activation.

It must require:

* clean deployable revision;
* Ivy admission;
* read-only capacity evidence;
* approved source list;
* single runner/scheduler authority;
* lock and timeout behavior;
* bounded run bundle;
* checksums or manifest;
* Mac receipt acknowledgment;
* prune gate;
* real health producer;
* shadow runs;
* natural-run evidence;
* rollback.

Do not merge operational activation with public launch.

4.7 Deferred architecture

Create an explicit deferred section covering:

* live incidents;
* full GIS/PostGIS;
* corpus PostgreSQL;
* bounded staging PostgreSQL;
* generic SourceAdapter framework;
* universal agent runtime/Hermes;
* broad multi-domain generalization;
* autonomous publishing;
* public API;
* complete subscriptions platform.

For each, state the trigger that would justify reconsideration.

4.8 Responsibility and authority

Define responsibility for:

* Buddy decisions;
* Strong Codex work;
* medium OpenCode implementation;
* privileged Ivy/VPS operations;
* human editorial review.

Make it clear that agents cannot commit, deploy, publish, install services, enable timers, migrate databases, or alter protected Ivy state without explicit authority.

4.9 Verification conventions

Require roadmap tasks to include:

* bounded scope;
* explicit input and output artifacts;
* acceptance criteria;
* validation commands;
* evidence;
* stop/escalation conditions;
* clean Git-state reporting.

Use the existing tasks/ and reports/ flow.

Do not introduce another task ledger.

⸻

5. Required phase detail

Each roadmap phase or goal must include the fields below.

Goal identity

Use a stable identifier.

Example:

§3A-G1

Outcome

Describe the observable result, not merely the activity.

Why it matters

One or two sentences only.

Dependencies

List only real dependencies.

Mark assumptions or human decisions separately.

In scope

Define the bounded implementation.

Out of scope

Prevent scope expansion.

Acceptance criteria

Use measurable statements.

Verification

Include exact commands or artifact checks where known.

Examples may include:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/build_public_release.py --check
git status --short

Do not invent commands as established facts if the script does not yet exist. Mark proposed commands clearly.

Stop and escalation conditions

State when the agent should stop rather than improvising.

Agent strength

Use:

* Medium OpenCode
* Strong Codex
* Buddy decision
* Privileged Ivy/VPS packet
* Editorial review

Required artifacts

Name expected files, tests, reports, or release outputs.

⸻

6. Specific planning requirements

6.1 Publication contract

The roadmap must make publication-contract design the first architectural task.

It must resolve:

* review versus publication;
* explicit publication status or release manifest;
* published and withdrawn semantics;
* reviewer attribution;
* release identity;
* publication timestamps;
* sensitivity eligibility;
* source attribution requirements;
* duplicate/canonical-item selection;
* public projection fields;
* handling of legacy/incomplete items.

This design task should be assigned to Strong Codex before medium implementation.

6.2 Corpus validation

The roadmap must include machine-enforced validation of the full corpus, not only parsing schema files.

At minimum plan for validation of:

* required fields;
* enums;
* ID format;
* ID uniqueness/canonical selection;
* registry references;
* source URLs;
* timestamps;
* source-event linkage policy;
* dedupe fields;
* publication eligibility;
* SilverLeaf relevance;
* internal-field exclusion from public exports.

Keep the implementation file-backed and SQL-ready.

6.3 SilverLeaf registry

The roadmap must define the smallest defensible SilverLeaf scope model.

It should likely include:

* canonical IDs;
* names and aliases;
* included communities/neighborhoods;
* nearby relevant roads;
* schools;
* utilities;
* tracked entities;
* explicit exclusions;
* inclusion rationale;
* needs-review state.

Do not require polygons or PostGIS for launch.

6.4 Static export

Plan a versioned, deterministic public projection.

Expected outputs should include a form of:

release.json
search-index.json
release-manifest.json

Exact names may be proposed rather than locked if repository conventions suggest better names.

The export must:

* contain published-only items;
* exclude internal/private fields;
* be deterministic;
* support rollback;
* include release metadata;
* provide stable filter IDs;
* support client-side search.

6.5 Portfolio integration

The roadmap must identify that portfolio-site technology and deployment details are a required context-gathering task before implementation if they are not already present in SJC_Intel.

Do not pretend the SJC repository can determine another repository’s framework or deployment method.

This work may belong to a separate project/repository packet.

6.6 VPS pilot

Limit the pilot to two deterministic sources unless evidence supports another choice.

The roadmap should propose source-selection criteria rather than silently choose sources if the choice requires current source-health context.

The pilot must not run agentic discovery automatically at first.

6.7 Agentic discovery

Keep agentic discovery as:

* bounded;
* candidate-producing;
* non-publishing;
* explicitly budgeted;
* manually triggered initially;
* independently reviewed.

State what evidence would justify later scheduling.

6.8 Subscriptions

Treat subscriptions as immediate post-launch work unless Task 08 evidence shows a simpler existing portfolio mechanism.

Plan only the stable prerequisites during launch:

* topic/entity/place IDs;
* release events;
* publish/withdraw events;
* reviewed-only matching.

⸻

7. Document changes

7.1 Required edit

Rewrite:

ROADMAP.md

It must become the sole current execution roadmap.

7.2 Allowed supporting edits

Update only as necessary for consistency:

README_INTERNAL.md
VPS_ROADMAP.md
docs/VPS_CONTINUITY.md

Possible changes:

* correct stale current-state summaries;
* point clearly to ROADMAP.md;
* mark VPS_ROADMAP.md as supporting/deferred if retained;
* align continuity with Mac file authority and optional PostgreSQL Option B;
* distinguish launch from VPS activation.

Do not expand supporting documents into duplicate roadmaps.

7.3 Do not modify

Do not modify:

* application code;
* data artifacts;
* schemas;
* tests;
* registry contents;
* prompts;
* VPS state;
* PostgreSQL;
* services or timers;
* Ivy control records;
* BACKLOG.md, unless a very small correction is strictly required to prevent contradiction.

Prefer listing recommended BACKLOG.md updates in the report for a later bounded task.

Do not commit or push.

⸻

8. Roadmap quality requirements

The roadmap must be:

* authoritative;
* concise;
* executable;
* dependency-aware;
* verifiable;
* understandable by a new medium-strength agent;
* resistant to scope expansion;
* explicit about human and privileged gates.

Avoid:

* narrative session history;
* duplicated architecture essays;
* speculative implementation detail;
* stale counts that will immediately drift;
* tasks such as “build platform” or “finish automation”;
* combining design, implementation, deployment, and publication into one task;
* making the VPS or PostgreSQL part of the launch definition;
* presenting deferred architecture as current work.

The roadmap should be usable as the basis for generating the next bounded tasks/NN-*.md packets.

⸻

9. Required report

Write:

reports/09-codex-redesign-2.md

Include:

1. Executive summary

State what roadmap authority now exists and the key sequencing decision.

2. Starting state

Include Git status and relevant pre-existing changes.

3. Files inspected

List primary and supporting authorities.

4. Files changed

Explain why each file changed.

5. Roadmap structure

Summarize sections, phases, gates, and stable identifiers.

6. Decisions preserved

List accepted Task 08 decisions retained in the roadmap.

7. Corrections or pushback

Identify any Task 08 conclusion changed and why.

8. Validation

Record exact commands and results.

9. Authority cleanup

Explain which documents are authoritative, supporting, stale, or deferred after this task.

10. Candidate next tasks

Propose the next bounded tasks with exact names or slugs where practical.

The first likely task should be a Strong Codex publication-contract design packet, followed by medium-agent implementation tasks.

11. Unresolved decisions

List only decisions that genuinely require Buddy, another repository, or privileged Ivy context.

12. Final status

Use the established report status vocabulary.

⸻

10. Validation

Run relevant safe validation.

At minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
git diff --check
git status --short

Also inspect internal links or references introduced by the roadmap rewrite.

Do not run:

* networked source fetches;
* backfills;
* migrations;
* deployment;
* service commands;
* timers;
* PostgreSQL writes;
* destructive retention;
* Git commit or push.

⸻

11. Success criteria

Task 09 is complete when:

1. ROADMAP.md is the single clear current execution roadmap.
2. It defines a launch path independent of VPS automation.
3. It separates public launch from operational activation.
4. It turns Task 08 phases into bounded, gated work packages.
5. It makes publication contract and corpus validation the first implementation foundation.
6. It defines the minimum SilverLeaf scope and static-export path.
7. It reserves most implementation for medium OpenCode agents.
8. It identifies Strong Codex, Buddy, editorial, and privileged VPS gates.
9. It preserves Mac file authority and optional narrow PostgreSQL use.
10. It clearly defers nonessential platform work.
11. It contains stable references suitable for future task packets.
12. Supporting documents no longer conflict materially with the roadmap.
13. The report identifies the next bounded tasks needed to begin execution.

⸻

12. Governing instruction

Rewrite the roadmap so medium-strength agents can finish SJC_Intel quickly and safely. Make the static reviewed SilverLeaf product the launch target, keep VPS automation as a separate gated activation track, and prevent database, runtime, GIS, live-incident, or platform-generalization work from becoming accidental launch dependencies.


Reusability and future-location portability

The roadmap must preserve and document the intention that SJC_Intel can later be adapted to other locations and bounded intelligence domains.

This is a planning and architecture requirement, not a requirement to build a complete generic platform before the SilverLeaf launch.

Codex must ensure that the roadmap:

1. distinguishes clearly between:
    * generic intelligence-system behavior;
    * SJC-specific domain configuration;
    * SilverLeaf-specific publication policy;
2. identifies which current components are intended to be reusable, including:
    * source and source-event semantics;
    * intelligence-item and evidence contracts;
    * deduplication;
    * review and publication separation;
    * task/report workflow;
    * validation interfaces;
    * public release/export contracts;
    * VPS run-bundle, transfer, acknowledgment, and retention patterns;
3. identifies which components should remain domain-specific, including:
    * source registries;
    * source-specific extractors;
    * taxonomy and audience-interest rules;
    * communities and geographic entities;
    * local authority and verification rules;
    * SilverLeaf inclusion and exclusion policy;
4. avoids introducing new SJC-specific assumptions into code that is intended to serve the generic pipeline;
5. preserves stable domain, topic, entity, place, source, and release identifiers where practical;
6. plans a post-launch portability proof using either:
    * another St. Johns County community;
    * another geographic location;
    * or a small synthetic example domain;
7. defines the documentation needed for future reuse, potentially including:
    * an architecture overview;
    * a generic-versus-domain-specific responsibility map;
    * a “new domain” checklist;
    * a sample or sanitized domain configuration;
    * source-adapter guidance;
    * environment and deployment requirements;
    * known limitations;
    * licensing and public-repository readiness;
8. ensures these future-reuse requirements are retained in durable authority documents rather than only in task reports or conversation history.

The roadmap should create a clearly labeled post-launch portability and reuse track with stable roadmap references. It should include triggers, dependencies, expected outputs, and verification, but it must not become part of the first SilverLeaf launch gate.

At minimum, the post-launch track should produce:

* a documented domain boundary;
* one reusable public-export contract;
* one reusable validation contract;
* a new-domain onboarding checklist;
* a portability demonstration;
* a review of remaining SJC assumptions in shared pipeline code.

Codex may recommend whether this belongs entirely in ROADMAP.md or whether the roadmap should require a later dedicated architecture document. Do not create multiple competing strategy documents. If a dedicated document is proposed, the roadmap must remain authoritative and link to it explicitly.

The public portfolio narrative should eventually be able to state accurately:

SJC_Intel is a working reference implementation of an agent-led domain intelligence architecture. St. Johns County is the first domain, and SilverLeaf is the first public product lens.

Do not describe the repository as a turnkey multi-domain platform until a portability proof exists.