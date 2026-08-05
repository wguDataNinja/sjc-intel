Task 13 — Candidate-to-Corpus Import and First Source-Proposal Proof

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
docs/weekly_operational_contract.md
tasks/README.md
reports/README.md
reports/10-ivy-operational-admission.md
reports/11-operational-admission-continuation.md
reports/12-weekly-operations-implementation-prep.md

Inspect relevant recent source-discovery artifacts, source-watch logs, candidate registries, Hermes outputs, run reports, and repository history to locate the recent St. Johns County Sheriff’s Office feed discovery.

Buddy recalls this approximately as a Sheriff’s Office RSS, SSL, or feed-related discovery. Do not assume that shorthand is exact.

Identify the actual:

* source;
* URL;
* feed type;
* discovery artifact;
* prior evidence;
* technical issue, if any;
* current registry status;
* recommended disposition.

Use that verified discovery as the first end-to-end proof of the new source-proposal workflow if it is suitable.

If it is not suitable, explain why and use the closest verified recent source discovery that provides a better proof. Do not silently substitute another source.

Required report

Write:

reports/13-candidate-to-corpus-import.md

Follow reports/README.md.

Mission

Implement the first safe candidate-to-corpus path for weekly VPS/Hermes outputs.

The task must:

1. add workspace-safe execution so remote or VPS runs never write directly into the authoritative Mac corpus;
2. implement a human-gated and idempotent candidate import path from incoming run bundles;
3. preserve dedupe and review state;
4. keep imported candidates distinct from accepted corpus records until explicitly approved;
5. prove the source-proposal process using the recent Sheriff’s Office feed discovery;
6. ensure source proposals cannot promote themselves into the canonical source registry;
7. leave the repository ready for a future bounded weekly Hermes run.

The intended lifecycle is:

weekly run workspace
    ↓
source events and intelligence candidates
    ↓
source-discovery proposals
    ↓
versioned transfer bundle
    ↓
Mac incoming staging
    ↓
validation and dedupe preview
    ↓
human approval
    ↓
candidate import
    ↓
review queue

This task is local and non-privileged.

Do not:

* deploy to the VPS;
* modify PostgreSQL;
* configure Hermes credentials;
* install systemd units;
* enable timers;
* change protected Ivy state;
* publish anything;
* promote a source automatically;
* commit or push without explicit instruction.

⸻

1. Verify current state

Inspect and report:

* current branch;
* current HEAD;
* working-tree status;
* configured remotes;
* whether local commits are present on origin/master;
* whether Task 12 outputs exist;
* current tests and validation state;
* current incoming, bundle, candidate, and proposal directories;
* any unfinished or conflicting prior implementation.

Do not discard unrelated changes.

Do not rewrite history.

If the GitHub push is still incomplete, continue the local implementation and report the exact remaining Buddy action.

⸻

2. Inspect Task 12 implementation

Read the actual Task 12 report and changed files.

Determine what already exists for:

* weekly workspace layout;
* bundle construction;
* manifests;
* checksums;
* bundle validation;
* incoming staging;
* receipt generation;
* acknowledgment;
* delayed-prune eligibility;
* Hermes task specification;
* source-proposal schema or examples.

Classify each as:

* implemented and tested;
* documented only;
* partial;
* missing;
* conflicting.

Do not duplicate existing tooling.

Extend the established design.

⸻

3. Locate and verify the Sheriff’s Office discovery

Search repository evidence for the recent St. Johns County Sheriff’s Office source or feed discovery.

Inspect at minimum where applicable:

registry/source_candidates.yaml
registry/sources.yaml
registry/search_terms.yaml
registry/search_profiles.yaml
data/search_runs/
data/source_events/
data/intel_items/
logs/agents/
logs/runs/
reports/
docs/source_discoveries/
docs/source_reviews/
prompts/
runtime/

Also inspect Git history if needed.

Determine:

* canonical or proposed source name;
* exact URL;
* whether it is RSS, Atom, XML, JSON, HTML, or another feed;
* whether SSL/TLS caused a fetch or validation issue;
* whether it duplicates an existing Sheriff’s Office source;
* whether it is a new endpoint for an existing canonical source;
* whether it should be:
    * a new candidate source;
    * an alias;
    * a replacement endpoint;
    * a monitor improvement;
    * rejected;
    * deferred;
* what coverage gap it addresses;
* its authority level;
* its expected cadence;
* whether it produces discrete intelligence items or only source-health information.

Use repository evidence first.

A bounded network verification is allowed only if:

* repository policy permits it;
* it is necessary to verify the current endpoint;
* no credentials are required;
* the request is read-only;
* the result is recorded with timestamp and provenance.

Do not perform broad source discovery in this task.

⸻

4. Define candidate states and authority boundaries

Inspect the current schemas and workflow before introducing new fields.

The implementation must distinguish:

discovered proposal
≠ approved source candidate
≠ canonical source

And:

incoming intelligence candidate
≠ accepted corpus item
≠ verified item
≠ published item

Use existing status vocabularies where they are sufficient.

If additions are required, use the smallest compatible extension.

The candidate-to-corpus path must preserve:

* source provenance;
* run ID;
* bundle ID;
* producing Git SHA;
* source ID or proposed source ID;
* evidence;
* original URL;
* observed timestamp;
* proposed classification;
* dedupe fingerprint;
* import status;
* human decision;
* reviewer;
* decision timestamp;
* rejection reason;
* replay identity.

Do not make imported candidates appear reviewed or publishable.

⸻

5. Implement workspace-safe weekly execution

Inspect the current extractors and weekly tooling.

Add a safe workspace-output mode for the initial deterministic monitor path.

At minimum evaluate:

scripts/extract_nbor.py
scripts/extract_bcc_agenda.py
scripts/run_weekly.py

If scripts/run_weekly.py does not exist, implement it as the bounded local weekly runner.

The runner should:

* accept a run ID or generate a stable one;
* create an isolated workspace;
* use an explicit output root;
* never write directly to authoritative corpus paths by default;
* run only explicitly approved monitors;
* capture source-health status;
* capture source events;
* capture intelligence candidates;
* support no-match, partial, failed, and success outcomes;
* record the producing Git SHA;
* record configuration and registry revisions;
* produce bounded logs;
* fail safely;
* be replayable;
* avoid duplicate concurrent runs;
* return meaningful exit codes.

Suggested workspace structure:

runtime/weekly/{run_id}/
  run.json
  source_health/
  source_events/
  intel_candidates/
  source_proposals/
  raw/
  logs/

Use a different location only if Task 12 established another authoritative convention.

Existing local operator commands may retain their current behavior if needed for compatibility, but remote/VPS execution must require an explicit workspace root.

Add tests proving that weekly execution does not mutate:

data/intel_items/
data/source_events/
data/review_queue/
data/index/
registry/sources.yaml

⸻

6. Implement candidate bundle ingestion

Implement or extend a Mac-side command that validates and stages a transferred weekly bundle.

Suggested command:

python3 scripts/import_weekly_bundle.py <bundle-path>

Use a different name only when existing conventions clearly support it.

The importer must:

* verify manifest schema;
* verify all checksums;
* verify bundle completeness;
* verify producing revision metadata;
* reject path traversal;
* reject undeclared files;
* reject malformed YAML or JSON;
* validate candidate schemas;
* detect duplicate bundle IDs;
* detect replayed run IDs;
* stage files idempotently;
* never overwrite authoritative corpus files;
* never alter review status;
* never promote source proposals;
* produce an import preview;
* produce a durable receipt only after successful staging.

Suggested staging location:

data/incoming/{run_id}/

Suggested receipt location:

data/incoming/{run_id}/receipt.json

The receipt should include:

* bundle ID;
* run ID;
* checksum-set identity;
* import timestamp;
* importer Git SHA;
* files accepted;
* candidate counts;
* proposal counts;
* duplicate counts;
* rejected counts;
* validation result;
* staging location;
* acknowledgment eligibility.

Do not mark the bundle prune-eligible until the import receipt is complete.

⸻

7. Implement human-gated candidate acceptance

Implement the smallest safe acceptance command or workflow.

Suggested command:

python3 scripts/accept_candidates.py --run-id <run_id> --candidate-id <id>

The exact interface may differ if repository conventions suggest a better pattern.

The acceptance path must:

* require explicit candidate selection;
* require explicit source or proposal disposition;
* show a dry-run diff before mutation;
* validate the candidate again;
* check dedupe against the authoritative corpus;
* preserve existing review states;
* assign stable IDs using current repository conventions;
* write accepted records only to appropriate authoritative paths;
* rebuild or update dedupe state safely;
* rebuild or update the review queue safely;
* record reviewer and decision timestamp;
* record origin run and bundle;
* remain idempotent;
* be replay-safe;
* reject already accepted candidates cleanly;
* support explicit rejection or deferral without deleting evidence.

Do not accept all candidates by default.

Do not turn source-proposal acceptance into automatic canonical promotion unless the existing approved source-promotion workflow is explicitly invoked.

It is acceptable for Task 13 to implement:

* candidate staging;
* candidate decision records;
* a dry-run acceptance plan;

while leaving final canonical-source promotion to the established source-review process.

⸻

8. Prove the source-proposal workflow

Use the verified Sheriff’s Office discovery as the first proof when appropriate.

Create a real proposal artifact through the new workflow.

The proposal should include:

* proposal ID;
* run ID;
* discovered timestamp;
* proposed source name;
* exact URL;
* feed type;
* current source relationship;
* source family;
* authority level;
* geographic relevance;
* coverage gap;
* evidence;
* SSL/TLS or feed issue, if applicable;
* recommended disposition;
* confidence;
* human-review status;
* next verification step.

The proof should demonstrate:

repository evidence
    ↓
proposal created
    ↓
bundle or incoming staging
    ↓
validation
    ↓
human review record
    ↓
no automatic promotion

Choose one of these dispositions based on evidence:

* propose as new source;
* propose as alias;
* propose as replacement endpoint;
* propose monitor update;
* reject as duplicate;
* defer pending verification.

Do not force a “new source” outcome merely to prove the workflow.

The workflow proof is successful if the system reaches a clear, reviewable proposal decision without changing registry/sources.yaml.

If the Sheriff’s Office discovery is unsuitable, document the reason and use the nearest suitable recent discovery. Preserve the Sheriff’s Office finding as a test case, rejected proposal, or deferred proposal where appropriate.

⸻

9. Preserve dedupe and review state

Add tests proving:

* duplicate candidate imports do not create duplicate staged records;
* replaying the same bundle is safe;
* accepting one candidate does not reset unrelated review states;
* rebuilding the review queue preserves prior decisions;
* rejected candidates remain auditable;
* deferred source proposals remain auditable;
* accepted intelligence candidates retain their origin run and evidence;
* source proposals cannot enter the canonical registry through the candidate importer;
* public release eligibility remains false unless separately approved.

Use existing queue and dedupe tooling rather than creating a parallel implementation.

⸻

10. Validation and operator usability

Add or update operator documentation for:

* running a weekly local workspace;
* building a bundle;
* importing a bundle;
* inspecting candidates;
* accepting one candidate;
* rejecting or deferring a candidate;
* reviewing source proposals;
* generating a receipt;
* replaying a bundle safely;
* recovering from a failed import.

Keep documentation concise and link from the weekly operational contract or roadmap.

Do not create a second roadmap.

Update ROADMAP.md only if actual implementation materially changes the stated task sequence, commands, dependencies, or status.

⸻

11. Required validation

Run at minimum:

python3 -m pytest tests/ -v
python3 scripts/validate.py
python3 scripts/portability_check.py
git diff --check
git status --short

Also run targeted tests for:

* workspace-safe execution;
* bundle validation;
* checksum failure;
* duplicate bundle import;
* path traversal rejection;
* candidate staging;
* dry-run acceptance;
* accepted candidate dedupe;
* review-state preservation;
* source-proposal non-promotion;
* Sheriff’s Office proposal proof.

Use fixtures and bounded local artifacts where possible.

Network access should not be required for the test suite.

⸻

12. Scope restrictions

Do not:

* deploy to the VPS;
* modify ivy-control-vps;
* modify PostgreSQL;
* install systemd units;
* configure provider credentials;
* enable timers;
* publish;
* promote the Sheriff’s Office proposal automatically;
* change taxonomy without approval;
* run broad backfills;
* delete candidate evidence;
* commit;
* push;
* discard unrelated working-tree changes.

If implementation reveals a privileged or high-reasoning dependency, document it as a specific follow-up gate rather than improvising.

⸻

13. Required report structure

Write reports/13-candidate-to-corpus-import.md with:

1. Executive result
2. Starting Git and repository state
3. Task 12 foundation inspected
4. Sheriff’s Office discovery identified
5. Verified source/feed facts
6. Recommended source disposition
7. Workspace-safe weekly execution implemented
8. Bundle-import path implemented
9. Candidate decision path implemented
10. Source-proposal proof
11. Dedupe and review-state protections
12. Files changed
13. Validation commands and results
14. Operator workflow
15. Remaining privileged VPS work
16. Remaining Buddy decisions
17. Candidate next tasks
18. Risks and unresolved issues
19. Final Git status
20. Final task status

Use the established final-status vocabulary.

Final status guidance

Use:

* COMPLETE when the local candidate-to-corpus path and proposal proof are fully implemented and validated;
* COMPLETE_WITH_FOLLOW_UP when local work is complete but a bounded source-verification or VPS action remains;
* PARTIAL when important implementation remains;
* BLOCKED only when no meaningful local work can proceed;
* HUMAN_DECISION_REQUIRED only when the next step depends primarily on Buddy’s editorial or source-promotion decision.

⸻

14. Success criteria

This task is complete when:

1. weekly execution can write to an isolated workspace;
2. authoritative corpus paths remain untouched during remote-style runs;
3. bundles can be verified and staged idempotently;
4. candidate acceptance is explicit and human-gated;
5. dedupe and review state are preserved;
6. source proposals remain distinct from canonical sources;
7. the Sheriff’s Office discovery has passed through the proposal workflow with an evidence-backed disposition;
8. no source was automatically promoted;
9. operator commands and tests are documented;
10. the repository is ready for the privileged Ivy/VPS admission packet without further candidate-flow architecture work.