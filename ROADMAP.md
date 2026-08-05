# SJC_Intel Roadmap

**Status:** Authoritative execution roadmap
**Owner:** Buddy
**Last reconciled:** 2026-08-03
**Planning basis:** [Task 08 assessment](reports/08-codex-redesign-1.md). This document owns sequencing and gates. `BACKLOG.md` owns immediate approved work; no supporting document overrides this roadmap.

## §1. Purpose and publishable finish line

SJC_Intel is an evidence-first, agent-led local intelligence system. St. Johns County is its first domain; SilverLeaf is its first public product lens.

The first release is a reviewed, static SilverLeaf Intelligence experience on Buddy’s portfolio site: original-source links, keyword search, topic/entity/place filters, a release timestamp, methodology, and limitations. It is periodic neighborhood intelligence, not a complete county service or alert system. It remains useful while the VPS is unavailable.

Publishable means a human has made an explicit publication decision; a deterministic reviewed-only static release passes validation; SilverLeaf relevance is defensible; and the release/UI/operator workflow are rollbackable. `verified` does not mean `published`.

### §1A. Deliberate boundaries

~~~
Generic intelligence behavior
  source/source-event semantics; evidence/item contracts; dedupe;
  review/publication separation; validation; task/report workflow; public
  release contract; VPS run-bundle, transfer, acknowledgement, retention
                    ↓
SJC domain configuration
  source registries/extractors; taxonomy and audience rules; authority and
  verification rules; communities, geographic and tracked entities
                    ↓
SilverLeaf publication policy
  inclusion/exclusion, relevance rationale, editorial framing, UI defaults/copy
~~~

Generic pipeline code must not acquire SJC names, source assumptions, or SilverLeaf policy. Preserve stable domain, topic, entity, place, source, item, and release identifiers where practical. This is a reference implementation, not a turnkey multi-domain platform until a portability proof exists.

### §1B. Excluded from launch

Live incidents/emergency alerting, real-time traffic/outages, complete county coverage, autonomous publication, broad subscriptions, full GIS/PostGIS, a public API, corpus PostgreSQL, a generic SourceAdapter framework, and a universal Hermes runtime are not launch work.

## §2. Current verified baseline

- The Mac file corpus is authoritative for durable items, source events, review, archive/restore, and release preparation. PostgreSQL is SQL-readiness infrastructure, not corpus authority.
- The working spine is source → source event → intel item → dedupe → review queue. Task 08 inspected 192 item records, 167 queue entries, and 83 `verified` records; counts are not release eligibility.
- Offline validation passed on 2026-08-03 (109 tests and `scripts/validate.py`), but it does not validate every corpus record or publication eligibility. No explicit publication state/export or public UI exists.
- Hermes is a prompt/task convention, not an installed SJC runtime. No SJC VPS clone, live service/timer, or operational health producer was verified.
- The local tree has pre-existing uncommitted data/docs/log changes. A dirty checkout is not deployable; preserve unrelated work.

## §3. Gates and phases

Every derived task must use the existing `tasks/` → `reports/` flow and name inputs/outputs, acceptance criteria, validation, evidence, Git state, and stop/escalation conditions. Agents cannot commit, publish, deploy, enable services/timers, migrate databases, alter Ivy state, or modify protected data without explicit authority.

### §3A. P1 — Publication contract and clean corpus

#### §3A-G1. Publication-contract design

| Field | Requirement |
|---|---|
| Outcome | Approved file-compatible contract separating review from published/withdrawn release membership. |
| Why | Public credibility requires a publication decision beyond `verified`. |
| Dependencies | None; first architecture task. |
| In scope | Reviewer attribution, release ID/timestamps, sensitivity/source-attribution eligibility, canonical selection, legacy records, public fields, withdrawal/rollback. |
| Out of scope | Code/data/schema changes, UI, deployment, automatic publication. |
| Acceptance | Design packet names authoritative artifacts, public projection, negative cases, and compatibility approach. |
| Verification | Strong Codex review against §1 and Task 08; no invented implementation commands. |
| Stop/escalate | Ambiguous editorial authority, sensitive-content rule, or public-data privacy decision. |
| Agent strength | Strong Codex; Buddy and editorial review approve policy. |
| Required artifacts | [Publication and SilverLeaf Release Contract](docs/publication_release_contract.md), task/report design packet, and implementation task path. |

#### §3A-G2. Corpus validation and publication implementation

| Field | Requirement |
|---|---|
| Outcome | File-backed, SQL-ready full-corpus validation and canonical publication selector. |
| Dependencies | §3A-G1 approved. |
| In scope | Required fields/enums; ID format and uniqueness/canonical selection; registry references; URLs/timestamps; source-event linkage; dedupe; publication eligibility; SilverLeaf relevance; internal-field exclusion. |
| Out of scope | Database authority, backfill, source promotion, publishing. |
| Acceptance | Deterministic pass/fail disposition; incomplete/duplicate/withdrawn/unreviewed fixtures reject; legacy handling is explicit. |
| Verification | `python3 -m pytest tests/ -v`; `python3 scripts/validate.py`; `python3 scripts/validate_publication_corpus.py`; `python3 scripts/select_publication_items.py --release-id ... --check`; `git diff --check`. |
| Stop/escalate | Content correction, sensitive classification, or destructive disposition is required. |
| Agent strength | Medium OpenCode; editorial review for records; Strong Codex design review. |
| Required artifacts | Validator, tests/fixtures, contract, result report. |
| Status | **IMPLEMENTED (Task 16, 2026-08-04):** `scripts/validate_publication_corpus.py` (per-record corpus validation, legacy exceptions), `scripts/select_publication_items.py` (deterministic selector, `--check` no-mutation), `scripts/publication_decision.py` (human decision tool), `data/publication_decisions/` (file-backed decision registry + `legacy_exceptions.yaml`), `schemas/publication_decision.schema.yaml`, `docs/public_ui_v0_spec.md`, `docs/static_release_data_contract.md`, 21 tests. Current corpus: 0 blocking errors; 83 unique verified items; 54 reviewed release-eligible preview; nothing approved or published. |

### §3B. P2 — SilverLeaf lens and static release

#### §3B-G1. Minimum SilverLeaf registry

| Field | Requirement |
|---|---|
| Outcome | Defensible non-GIS public-relevance model. |
| Dependencies | §3A-G1; Buddy-approved source authorities. |
| In scope | Stable IDs, names/aliases, included communities/neighborhoods, nearby roads, schools, utilities, tracked entities, rationale, exclusions, `needs_review`. |
| Out of scope | Polygons, point-in-polygon, PostGIS, full county gazetteer. |
| Acceptance | Inclusion/exclusion fixtures pass; every public item has reproducible relevance rationale. |
| Verification | Registry parse/reference validation, proposed scope tests, existing offline suite. |
| Stop/escalate | Authority choice unavailable or relevance is editorially ambiguous. |
| Agent strength | Medium OpenCode; Buddy/editorial scope approval. |
| Required artifacts | Registry/spec, fixtures/tests, task report. |
| Status | **IMPLEMENTED (Task 18, 2026-08-04):** `registry/silverleaf_scope.yaml` (launch-ready minimum: identity/aliases, neighborhoods, direct/adjacent roads, schools, utilities, developments, businesses, inclusion/exclusion rules, direct/nearby/countywide relevance, needs_review, evidence + verified/inferred/editorial-policy/needs-review provenance, no GIS claims), `schemas/silverleaf_scope.schema.yaml`, `scripts/validate_silverleaf_scope.py`, 8 tests, `validate.py` §10. Editorial-policy rules still require Buddy approval before publication use. |

#### §3B-G2. Deterministic static export

| Field | Requirement |
|---|---|
| Outcome | Versioned public projection suitable for static hosting and rollback. |
| Dependencies | §3A-G2 and §3B-G1. |
| In scope | Proposed `release.json`, `search-index.json`, `release-manifest.json` (or approved equivalents); stable filter IDs; published-only selector; public allowlist; deterministic ordering; release metadata; prior-release retention. |
| Out of scope | API, database reads, subscriptions, website deployment. |
| Acceptance | Repeated generation is byte-stable; no internal/reviewer/raw-path fields export; release selection and rollback work. |
| Verification | Proposed `python3 scripts/build_public_release.py --check`, export snapshot/negative tests, offline suite. |
| Stop/escalate | Contract conflict, data leak, or reviewed-only guarantee cannot be demonstrated. |
| Agent strength | Medium OpenCode after Strong Codex design approval. |
| Required artifacts | Export tool/tests, release artifacts per approved repo policy, report. |
| Status | **IMPLEMENTED (Task 17, 2026-08-04):** `scripts/build_static_release.py` (real + demo modes, `--check`, deterministic byte-stable output, checksums, content-quality validation, `release.json`/`search-index.json`/`release-manifest.json` per `docs/static_release_data_contract.md`), `scripts/static_release_common.py`, `scripts/site_search.py`. Demo output isolated under `site/data/demo/`; real output under `site/data/releases/{release-id}/`. Nothing approved or published. |

### §3C. P3 — Portfolio UI

#### §3C-G1. Portfolio integration context

| Field | Requirement |
|---|---|
| Outcome | Bounded, accurate packet for the portfolio-site repository. |
| Dependencies | Buddy authorization and target site's actual context. |
| In scope | Read-only framework/static-route/build/deploy/accessibility/ownership discovery. |
| Out of scope | Assuming site technology from SJC; deployment or publication. |
| Acceptance | Packet gives inputs, exact target repo/path, validation, rollback, authority gates. |
| Verification | Target-repository read-only checks specified by packet. |
| Stop/escalate | Missing site access/authority or unsafe deployment route. |
| Agent strength | Strong Codex or bounded cross-repo reviewer. |
| Required artifacts | Cross-repo task/report. |

#### §3C-G2. Static SilverLeaf UI

| Field | Requirement |
|---|---|
| Outcome | Accessible static portfolio page usable without VPS. |
| Dependencies | §3B-G2 and §3C-G1. |
| In scope | Source cards/links, search, topic/entity/place filters, release timestamp, methodology/limitations, empty/error state, architecture explanation. |
| Out of scope | API, live alerts, subscriptions, collector access. |
| Acceptance | Published-only data renders; filter/search/source links work; prior release restores; no internal data shown. |
| Verification | Target-site build and browser/accessibility checks defined by §3C-G1. |
| Stop/escalate | Attribution, release validation, accessibility, or deployment approval fails. |
| Agent strength | Medium OpenCode; Buddy publication approval. |
| Required artifacts | UI test/build evidence and release report in owning repo. |
| Status | **DESIGN ACCEPTED + IMPLEMENTATION UNDERWAY (Task 17, 2026-08-04):** The synthesized SilverLeaf Brief v0 design is accepted and preserved in `docs/public_ui_v0_spec.md`. Portable static v0 implemented in `site/` (generated by `scripts/build_static_site.py`): Latest, Browse (search + topic/relevance/place/entity filters), topic/place/entity collection routes, item detail, About, Data & Sources, 404, mobile bottom navigation, demo release under `site/data/demo/`. Remaining: editorial approval, real release generation, final polish, deployment. |

### §3D. Launch milestone — SilverLeaf static release

**Outcome:** Buddy-approved, publicly deployable periodic intelligence release.

**Requires:** explicit publication state/release manifest; complete-corpus publication validation; deterministic reviewed-only export; defensible SilverLeaf rules; static UI/search/filters/source links; methodology/limitations; prior-release retention; documented operator workflow.

**Does not require:** VPS, PostgreSQL, automation, subscriptions, GIS, real-time data, or a generic platform. Buddy makes publication decision; human editorial review is mandatory.

### §3D. Publish-ready sequence (ordered)

The shortest safe path to public launch (Task 16 update; repository state at 2026-08-04):

1. ~~**§3A-G2 publication implementation**~~ **DONE (Task 16):** `validate_publication_corpus.py`, `select_publication_items.py`, `publication_decision.py`, `data/publication_decisions/` + `legacy_exceptions.yaml`, UI v0 spec + static release data contract, 21 tests. Current corpus validates with 0 blocking errors; nothing approved or published.
2. **Editorial review pass** (Buddy/human): resolve the 78 `pending_review` queue items to `verified`/`rejected_noise` so the reviewed-only selector has eligible corpus.
3. ~~**§3B-G1 minimum SilverLeaf registry**~~ **DONE (Task 18):** `registry/silverleaf_scope.yaml` + schema + `validate_silverleaf_scope.py` + 8 tests; editorial-policy rules await Buddy approval.
4. ~~**§3B-G2 deterministic static export**~~ **DONE (Task 17):** `scripts/build_static_release.py` produces `release.json`, `search-index.json`, `release-manifest.json` per `docs/static_release_data_contract.md`, reviewed-only selector, byte-stable output, checksums, demo isolation.
5. **§3C-G1 portfolio integration context** (Strong Codex/Buddy authorized cross-repo): target-site discovery packet (SJC repo has no discoverable portfolio-site repo; packet requested in Task 16 report §22).
6. ~~**§3C-G2 static SilverLeaf UI**~~ **DONE as portable v0 (Task 17):** `site/` (Latest, Browse, collection routes, item detail, About, Data & Sources) generated by `scripts/build_static_site.py` per `docs/public_ui_v0_spec.md`; portfolio integration remains blocked on §3C-G1.
7. **Buddy publication decision + first release** (§3D).
8. **Public presentation** (concurrent, non-blocking): public `README.md` (DONE), `docs/ARCHITECTURE.md` (DONE), LICENSE (Buddy decision), screenshots/diagram (after first release).

Non-blocking operational track (does not gate launch): weekly VPS shadow run (§3E), SJSO RSS monitor (DONE locally), BCC workspace mode, backup automation, subscriptions, portability proof.

### §3E. P4 — Bounded operations pilot

#### §3E-G1. VPS admission and pilot design

| Field | Requirement |
|---|---|
| Outcome | Ivy-authorized bounded two-source deterministic pilot packet. |
| Contract | `docs/weekly_operational_contract.md` (weekly run + transfer bundle) and `docs/VPS_CONTINUITY.md` govern the pilot. Task 12 report `reports/12-weekly-operations-implementation-prep.md` names the two pilot sources with evidence. |
| Dependencies | Clean deployable revision, Ivy admission, current read-only capacity evidence, approved source-selection rationale (Task 12 §4). |
| In scope | One runner/scheduler; source criteria; locks/timeouts; raw-size/retention budget; run bundle; checksum/manifest; Mac receipt acknowledgement; prune gate; health; rollback. |
| Out of scope | Automatic agentic discovery, corpus database, public serving, timer enablement. |
| Acceptance | Exact SHA, source list, service/config, capacity, secrets route, transfer endpoint, rollback/evidence requirements approved. |
| Verification | Privileged Ivy read-only capacity/admission evidence and packet review; bundle fixtures verified by `python3 scripts/bundle_verify.py --bundle tests/fixtures/sample_bundle`. |
| Stop/escalate | Dirty deployable state, capacity shortfall, missing secrets/transfer authority, undefined rollback. |
| Agent strength | Strong Codex + Buddy; Privileged Ivy/VPS packet. |
| Required artifacts | Ivy admission/pilot/evidence packet; no runtime mutation in planning. |

#### §3E-G2. Shadow and natural-run proof

| Field | Requirement |
|---|---|
| Outcome | Two deterministic sources transfer bounded candidates to Mac without authority drift. |
| Dependencies | §3E-G1, explicit installation/service authority, and the bundle/import tooling from §3E-G3 already landed. |
| Contract | `docs/weekly_operational_contract.md` §7 (transfer semantics), §8 (runtime controls), §7.7 (prune gate). |
| In scope | Disabled/manual shadow runner, idempotency lock, retries/timeouts, real health, dated bundle, checksum, receipt acknowledgement, prune gate. |
| Out of scope | Publication, scheduled agentic discovery, corpus PostgreSQL, more than two sources. |
| Acceptance | Four healthy runs, no unexplained duplicate processing, reconciled manifests/checksums/acknowledgements, demonstrated rollback. |
| Verification | Approved service/health/transfer evidence; `python3 scripts/bundle_verify.py --bundle <incoming>` PASS; Mac `python3 scripts/bundle_import.py` receipts; run logs. |
| Stop/escalate | Divergence, acknowledgement gap, capacity pressure, health failure, or review bypass. |
| Agent strength | Medium OpenCode under privileged Ivy/VPS execution; Strong Codex review. |
| Required artifacts | Bundles, receipts, health/rollback/natural-run evidence. |

#### §3E-G3. Weekly contract, bundle, and import foundation (medium-agent work)

This foundation landed with Tasks 12–13. It is the precise dependency
substrate for §3E-G1/G2. Subsequent medium agents implement only what remains;
no rediscovery is required.

| Item | State | Reference |
|---|---|---|
| Weekly operational contract | DONE | `docs/weekly_operational_contract.md` — inputs, Stage A/B, outputs, runtime controls, review boundary |
| Operator guide | DONE | `docs/weekly_operator_guide.md` — run/build/import/accept/review commands |
| Bundle schema | DONE | `schemas/bundle_manifest.schema.yaml` |
| Candidate + proposal schemas | DONE | `schemas/intel_candidate.schema.yaml`, `schemas/source_proposal.schema.yaml` |
| Workspace-safe weekly runner | DONE | `python3 scripts/run_weekly.py` (runtime/weekly/{run_id}/; NBOR + SJSO RSS monitors; offline fixture mode) |
| NBOR extractor workspace mode | DONE | `python3 scripts/extract_nbor.py --workspace <dir>` |
| SJSO RSS workspace monitor | DONE | `run_weekly.py --monitor sjso_news_stories` (verified RSS 2.0 feed; implements `PROP-public_safety-0001` next step) |
| Weekly task declaration | DONE | `deploy/sjc-weekly-task.yaml` (schema-validated by `scripts/validate.py`) |
| Scheduling + task-submission model | DONE | `docs/weekly_scheduling.md` (Hermes reality, responsibility split, test packet, recommended window) |
| Bundle builder / verifier | DONE | `python3 scripts/bundle_build.py`, `python3 scripts/bundle_verify.py` |
| Mac bundle importer (staging-only) | DONE | `python3 scripts/import_weekly_bundle.py <bundle>` — preview, idempotent replay, receipt |
| Human-gated candidate acceptance | DONE | `python3 scripts/accept_candidates.py --run-id ... --candidate-id ... --decision accept\|reject\|defer --reviewer ...` |
| Source-proposal review record | DONE | `python3 scripts/review_source_proposals.py` — never writes registry/sources.yaml |
| External-backup policy | DONE | `docs/backup-restore.md` §0 (file-corpus authoritative; PG runbook dormant) |
| Public architecture artifact | DONE | `docs/ARCHITECTURE.md` |
| Public README | DONE | `README.md` (public-safe; LICENSE is a Buddy decision) |
| Sample bundle fixture + tests | DONE | `tests/fixtures/sample_bundle/`, `tests/fixtures/bundle_workspace/`; test_run_weekly.py, test_import_weekly.py, test_accept_candidates.py, test_bundle.py |
| First proposal proof | DONE | SJSO RSS feed (`https://www.sjso.org/feed/`) → `PROP-public_safety-0001`, staged + reviewed, registry untouched (Task 13 report §10) |

Builder task boundaries for remaining work:

- **extract-bcc-workspace-mode.md** (medium OpenCode): add the same
  workspace-output mode to `scripts/extract_bcc_agenda.py` before BCC becomes a
  VPS-capable monitor. Validation: `python3 -m pytest tests/ -v`,
  `python3 scripts/validate.py`, `git diff --check`.
- **publication-implementation.md** (§3A-G2; medium): full-corpus validator +
  canonical publication selector per `docs/publication_release_contract.md`.
  **DONE (Task 16, 2026-08-04)** — see §3A-G2 status row.
- **silverleaf-scope-registry.md** (§3B-G1; medium): minimum SilverLeaf
  inclusion/exclusion registry.
- **static-public-export.md** (§3B-G2; medium): reviewed-only deterministic
  release export (`release.json`, `search-index.json`, `release-manifest.json`).
- **14-vps-admission-packet.md** (§3E-G1; privileged): executes the privileged
  packet in report 12 §11 / report 13 §15 — exact SHA deployment, service
  account, systemd unit, weekly timer (disabled), lock, capacity evidence,
  secrets route, transfer endpoint, rollback.
- **15-shadow-run-proof.md** (§3E-G2; privileged): manual/disabled two-source
  shadow runs, four healthy runs, receipt reconciliation, prune-gate evidence.
  Stop on divergence, acknowledgement gap, capacity pressure, or health failure.
- Optional **16-weekly-contract-docs-check.md**: verify the contract, prompts,
  and bundle tools stay consistent as the pilot evolves.

Required preceding report evidence: `reports/12-weekly-operations-implementation-prep.md`
(clean remote state, pilot source selection, bundle/receipt semantics, exact
privileged packet), `reports/13-candidate-to-corpus-import.md` (workspace
runner, importer, acceptance, SJSO proposal proof), and
`reports/14-publish-readiness-and-vps-onboarding.md` (backup policy, PG
disposition, task-submission model, publish-ready sequence). No task below may
promote sources, change taxonomy, enable timers, or publish.

### §3F. Operational activation milestone — limited scheduling

Scheduling is separate from launch. It may be proposed only after §3E-G2: approved exact SHA/source list, one scheduler/writer, staggered timer window, locks/timeouts, bounded retention, real health, acknowledged transfer, rollback, and seven-day healthy evidence.

SJC weekly task declaration: `deploy/sjc-weekly-task.yaml` (disabled). Scheduling model, responsibility split, and the minutes-from-now test packet: `docs/weekly_scheduling.md`. Recommended window: Wed 01:30–03:00 UTC (avoids the WGU-Reddit ~07:00 UTC timer; re-verify against fresh capacity). No timer is enabled by any document here.

PostgreSQL Option B may hold locks, run/source-health state, transfer manifests/acknowledgements, and small operational queues after separate Ivy/database authorization. It is optional and must not hold durable corpus authority.

### §3G. P5 — Post-launch subscriptions

**Outcome:** opt-in notifications derived only from approved publication events. **Dependencies:** §3D stable release semantics and Buddy-selected provider/privacy approach. Launch work only preserves stable topic/entity/place/release IDs and published/withdrawn semantics.

Implementation requires consent, preferences, unsubscribe, data minimization, and reviewed-only matching tests. A collector never sends email. This is not a launch gate.

## §4. Post-launch portability and reuse track

This track is post-launch. Trigger it only after §3D has a stable release/export/validation workflow; it never delays launch.

### §4A-G1. Reuse boundary and documentation

| Field | Requirement |
|---|---|
| Outcome | One dedicated future architecture reference linked from this roadmap, not a competing roadmap. |
| Dependencies | §3D and representative release artifacts. |
| In scope | Domain boundary; generic-vs-domain map; reusable public-export/validation contracts; new-domain checklist; sanitized/sample config; source-adapter guidance; environment/deployment requirements; limitations; licensing/public-repo readiness. |
| Out of scope | Generic platform or launch-code abstraction for its own sake. |
| Acceptance | Reference explains stable IDs and how a new domain supplies configuration without SJC assumptions in shared pipeline code. |
| Verification | Architecture review against §1A and onboarding dry run using sample config. |
| Stop/escalate | Reuse requires unsupported abstraction or changes public semantics. |
| Agent strength | Strong Codex design; Medium OpenCode documentation. |
| Required artifacts | One dedicated architecture/reuse document linked here and task report. |

### §4B-G1. Portability demonstration

| Field | Requirement |
|---|---|
| Outcome | Evidence that reusable contracts work beyond SilverLeaf. |
| Dependencies | §4A-G1 and Buddy choice: another SJC community, another location, or synthetic bounded domain. |
| In scope | Small configuration and fixture-backed run through reusable validation/export; audit remaining SJC assumptions in shared code. |
| Out of scope | Public second-product launch, broad monitoring, framework rewrite. |
| Acceptance | Valid release-shaped output, reusable validation pass, documented exceptions, and every remaining SJC assumption classified as config or refactoring debt. |
| Verification | Reusable contract tests and independent assumption-audit review. |
| Stop/escalate | Private data/live service/unsupported geographic claims/multi-domain commitment required. |
| Agent strength | Strong Codex review; Medium OpenCode; Buddy selects proof. |
| Required artifacts | Sanitized config/fixtures, validation/export evidence, assumption-audit report. |

Until §4B-G1 passes, portfolio language may say: “SJC_Intel is a working reference implementation of an agent-led domain intelligence architecture. St. Johns County is the first domain, and SilverLeaf is the first public product lens.” It must not claim a turnkey multi-domain platform.

## §5. Deferred architecture and reconsideration triggers

| Deferred work | Reconsider only when |
|---|---|
| Live incidents/emergency alerts | Dedicated source feasibility, transient model, safety policy, and human operating model are approved. |
| Full GIS/PostGIS | Manual relevance rules measurably fail or a later product needs spatial queries. |
| PostgreSQL staging/corpus | Option B/file transfer have observed limits that a measured alternative resolves. |
| Generic SourceAdapter framework | Three or more approved extractors share stable tested lifecycle needs. |
| Universal Hermes runtime | Provider, budget, locking, retry, timeout, audit, and stop controls exist. |
| Broad multi-domain product | §4B proof passes and Buddy makes a separate product decision. |
| Autonomous publishing | An explicitly approved safer evidence-backed exception exists; otherwise never. |
| Public API | Static export cannot meet a demonstrated user need. |
| Full subscription platform | Minimal post-launch service proves insufficient with consent/privacy evidence. |

## §6. Responsibility and authority

| Role | Responsibility |
|---|---|
| Buddy decision | Product/publication scope, editorial policy, remote/visibility, provider/source choices, VPS/deployment authorization. |
| Strong Codex | Cross-cutting contract design, roadmap/authority resolution, portability architecture, gate/privileged-packet review. |
| Medium OpenCode | Bounded code/docs/tests after approved packet; report evidence; stop on policy/production ambiguity. |
| Editorial review | Source verification, sensitivity, relevance, publication/withdrawal decision. |
| Privileged Ivy/VPS packet | Capacity, clone/config/secrets, services/timers, database, backup/restore, deployment/rollback. |

### §6A. Ownership boundary (SJC vs Ivy)

This repository owns its roadmap, implementation tasks/reports, domain
architecture, source registries, schemas, extractors, runtime behavior, task
declaration (`deploy/sjc-weekly-task.yaml`), tests, editorial workflow,
release artifacts, and operator documentation. Ivy Control VPS owns portfolio
admission, gate/control records, VPS/database/runtime standards, deployment
authority, scheduling, backup disposition, health/rollback, and operational
evidence. Project implementation tasks and reports live **here**, not in Ivy;
Ivy tracks gate state and control records. Cross-repo ownership conflicts are
resolved through an approved Ivy task, never silently in either repository.

## §7. Verification conventions

Baseline offline checks for applicable code/data work:

~~~
python3 -m pytest tests/ -v
python3 scripts/validate.py
git diff --check
git status --short
~~~

Tasks add only real task-specific checks. Future-tool commands are proposed until implemented. Reports record starting/final Git state, changed paths, exact command results, provenance, risks, unresolved decisions, and the next bounded task. Passing tests never authorize deployment, publishing, scheduler activation, source promotion, or database mutation.
+

## §8. Builder packet and GPT coordination requirements

For every remaining goal, GPT creates one task file and requests one report using the existing flow:

~~~
ROADMAP.md → tasks/NN-*.md → Medium OpenCode or approved Hermes execution
           → reports/NN-*.md → GPT evidence review → next bounded task
~~~

A builder packet must name: stable roadmap goal; exact input and output paths; in/out of scope; dependencies; acceptance criteria; exact validation; expected report; stop/escalation conditions; Git policy; network permission; cross-repository boundary; and whether privileged execution is required. The agent may not infer any omitted authority.

The next builder tasks are: publication contract implementation (§3A-G2); SilverLeaf scope registry (§3B-G1); static export (§3B-G2); portfolio integration context (§3C-G1); static UI (§3C-G2); reviewed release; then the separate §3E VPS admission packet. The §3E weekly/bundle/import foundation already exists (§3E-G3 + Tasks 12–13) so the VPS admission packet only needs the exact-SHA privileged execution and Ivy evidence, not architecture rediscovery. GPT should reject reports that do not demonstrate the goal's acceptance criteria, preserve review/publication separation, or distinguish live proof from documented intent.

### §8A. Remaining high-reasoning gates

| Gate | Required preceding evidence | GPT question / output |
|---|---|---|
| Publication edge cases | §3A-G2 validator/exclusion report and draft contract test results | “Approve these sensitivity, withdrawal, and legacy-item rules?” Produce an editorial decision record. |
| Portfolio-site deployment | §3C-G1 target-repo context report | “Approve this exact static deployment/rollback route?” Produce the target-repo implementation packet. |
| VPS capacity/activation | §3E-G1 fresh capacity, exact SHA, source selection, rollback packet | “Does current capacity and workload window safely permit this pilot?” Produce Ivy gate evidence. |
| Source authority dispute | Source/relevance evidence and conflicting URL/record report | “Which authority controls this claim?” Produce editorial/source decision. |
| Subscription privacy/provider | Provider comparison and required data-flow diagram | “Approve this provider/data boundary?” Produce provider decision record. |
| Portability architecture | §4A reuse reference plus onboarding dry run | “Does the proof show a reusable contract without a platform claim?” Produce assumption-audit acceptance. |

Buddy may decide each policy/product gate. A small Strong Codex review is useful only when evidence exposes a cross-cutting contract conflict; it is not a planned fourth architecture pass.
