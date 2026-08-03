# Task 08 — Codex Redesign 1

**Task identity:** architecture, publishability, deployment, and completion assessment  
**Executor:** Codex  
**Date:** 2026-08-03  
**Scope:** read-only assessment of SJC_Intel, Ivy Control VPS, and the supplied harness notes; this report is the sole task artifact.  
**Final status:** COMPLETE_WITH_FOLLOW_UP

## 1. Executive recommendation

Build a small, reviewed **SilverLeaf Intelligence** section on Buddy's portfolio site. It should present a curated feed of SilverLeaf-relevant, human-reviewed items with source links, an explanation of method, keyword search, and topic/entity/place filters. Generate it from a versioned, reviewed-only static export on the Mac. The site must continue to work when the VPS does not.

Use a deliberately narrow three-layer shape:

```text
generic intelligence patterns  ->  SJC source/taxonomy implementation  ->  SilverLeaf publication lens
registry, evidence, dedupe,        county sources, rules, entities,       inclusion rules, UI, public copy
review, export contract            monitor adapters                       filters and reviewed releases
```

Keep the Mac file corpus authoritative. Use the VPS only after a two-source shadow run proves a bounded collector and transfer contract. Start with **PostgreSQL Option B, operational metadata only**, if a VPS deployment needs durable locks, run/transfer acknowledgements, and source-health history. Do not put the SJC corpus or search API in PostgreSQL for launch. Option A is also viable for the first manual/static release; B becomes useful only at operational activation.

The shortest credible sequence is: (1) repair and enforce publication/data eligibility, (2) establish the minimal SilverLeaf registry and reviewed export, (3) build the static portfolio UI and search, (4) prove one or two deterministic sources on the VPS with an acknowledged bundle transfer, then (5) enable a limited schedule. Subscriptions are an immediate follow-up, not a launch gate. Live incidents, PostGIS, a generic SourceAdapter plugin framework, a new Hermes platform, and a broad source estate are explicitly deferred.

The strongest reasons are verified in the repository: there are 192 file-backed items and 83 `verified` records, durable IDs/dedupe/review tooling, passing offline tests, and an existing portfolio control plane; but there is no publication state or export, no public UI/search, no running Hermes runtime, no VPS clone/service/timer, and current validation parses schemas rather than validating each corpus item against them.

Major workstreams: publication contract and corpus cleanup; SilverLeaf scope registry; static export/UI; two-source operational pilot; then limited scheduling and evidence. This is a portfolio-worthy proof of evidence-first intelligence without converting the launch into a database or platform rewrite.

## 2. Verified current state

### Git and repository state

- **VERIFIED:** SJC_Intel is on `master`, at `4262169 data: absorb July 2026 SilverLeaf search candidates into dedupe index and review queue`; no remote was reported by the SJC roadmap/control record.
- **VERIFIED:** Its working tree was already dirty before this task: modified `BACKLOG.md`, dedupe/review/data-inventory/cadence/fixture files, and untracked August data, June/July monthly data, run logs, `tasks/`, and `reports/`. Those changes were not modified by this assessment.
- **VERIFIED:** Ivy Control VPS is `main...origin/main [ahead 2]` and has pre-existing modified/untracked governance artifacts. Its SJC control record is therefore useful evidence, but not a clean immutable snapshot.
- **CONFLICT:** `repos/sjc-intel/CONTROL.md` says its approved SHA is `35a0246…`, while the local SJC HEAD is `4262169`; it also says no database, no deployment, and no active scheduler. Task 09 must not treat the control record's SHA or status as current without reconciliation.

### Code, data, and tests

- **VERIFIED:** The real file spine is `registry/sources.yaml` -> `data/source_events/YYYY-MM-DD/*.yaml` -> `data/intel_items/YYYY-MM-DD/*.yaml` -> `data/index/prior_items.yaml` -> `data/review_queue/queue.yaml`. `build_review_queue.py` preserves review fields and matches tracked-entity aliases.
- **VERIFIED:** Current corpus scan: 192 item records in 22 files; 19 source events; 167 review-queue entries; 83 `verified`, 95 `pending_review`, 4 `archived`, and 1 `rejected_noise` item statuses. There are 10 sources represented. The corpus is approximately 536 KiB; all `data/` is approximately 1.1 MiB.
- **VERIFIED:** 9 legacy/irregular records lack `source_url`, `summary`, `topics`, `review_status`, `verification_status`, and `sensitivity`; 47 lack `source_event_id`; 173 have no community entry; only 5 have a tracked-entity link; **all 192 lack `publication_status`**. There are 167 distinct `item_id` values among 192 rows, so IDs repeat across records/files or items were retained as duplicate representations. This is a launch blocker until a canonical export selector resolves it.
- **VERIFIED:** 109 offline tests pass. They cover parser fixtures, adapters, migrations as files, redaction, retention, metrics, and a PostgreSQL adapter mock/behavior. `scripts/validate.py` parses schema files, compiles scripts, checks fixtures and registries; it does **not** validate every corpus record against the declared schema or enforce publication eligibility.
- **VERIFIED:** The default storage facade is file-backed. PostgreSQL adapter/migrations and a deliberate `pilot_loader.py --apply` exist, but no live connection or applied migration was inspected. `health_export.py` is explicitly inert/fake dry-run output.
- **VERIFIED:** Deterministic extractor implementations exist for NBOR and BCC agenda; the remaining source workflows are documentation, manually executed work, prompt-led work, or fixtures. No broad SourceAdapter implementation exists; `adapter_base.py` is a storage interface, not an extractor-plugin framework.

### Runtime and deployment

- **VERIFIED:** `runtime/workers/` holds historical Markdown work reports, not an executable worker runtime. `prompts/` contains reusable task contracts. There is no SJC code that invokes a model/provider, manages credentials/cost, controls retries/concurrency, establishes locks, or prevents duplicate agent runs.
- **VERIFIED:** Hermes for SJC is **prompt convention only**, not a production-ready or project-specific runtime. This agrees with the architect memory, roadmap, monitor docs, and the historical audit despite some documents calling extractors “Hermes-ready.” That phrase means technically suitable for a future runner, not scheduled.
- **VERIFIED:** `deploy/` contains inert systemd templates for NBOR, BCC, dedupe, review queue, health, and PostgreSQL backup. SJC docs and Ivy's control record say there is no SJC VPS clone, service, timer, health producer, or database. No VPS was contacted: public Ivy authority requires approved private runbook context before live inspection.
- **DOCUMENTED BUT NOT VERIFIED:** Ivy inventory describes a Hetzner CX23 / 4 GB Ubuntu VPS with existing workload(s). Current disk, RAM, load, timer overlap, journal growth, and available database capacity were not safely established from this repository. No scenario can be called safe until a privileged read-only capacity packet produces dated evidence.

### Documentation authority and drift

- **Authoritative now:** `ROADMAP.md` calls itself the current roadmap; `README_INTERNAL.md` is the detailed development entrypoint; `BACKLOG.md` is near-term task state; `AGENTS.md` governs SJC execution; `tasks/` and `reports/` govern the current dispatched-task flow.
- **Supporting / planning:** `VPS_ROADMAP.md`, `docs/VPS_CONTINUITY.md`, data-model, retention, backup, migration, monitor, and planning documents. They should not authorize deployment alone.
- **Historical or stale/conflicting:** architect memory is dated 2026-06-03 and understates current counts; `README_INTERNAL.md` says 115 fingerprints/132 queue entries, while current artifacts show 192 items/167 queue entries; `VPS_ROADMAP.md` targets a PostgreSQL operational corpus, while locked provisional decisions and current evidence support file authority; `docs/monitoring_workflow.md` models cron/Hermes tasks that do not exist; the Ivy SJC control record is stale as noted above.

## 3. Publishable finish line

### Required for launch

1. A reviewed-only static publication export with a tested selector: `review_status: verified`, valid source URL/attribution, low or explicitly approved sensitivity, and an explicit `publication_status: published` (or a separate reviewed release manifest that is equally explicit).
2. A small, manually curated SilverLeaf inclusion registry: canonical community/entity IDs, aliases, inclusion reason, and exclusions. Full polygons are not required.
3. A portfolio-site page with item cards, original-source links, date, topic/entity/place filters, client-side keyword search, “last updated,” an accessible methodology/limitations page, and a no-results/failure state.
4. An operator release workflow: validate corpus -> generate deterministic export -> review diff/count -> approve -> deploy static site. It must be idempotent and retain the prior static export for rollback.
5. A bounded current-content promise: periodic reviewed updates, not real-time alerts; source attribution; no claim of comprehensive coverage.
6. Repository hygiene decision: establish a canonical remote, public/private review, and clean deployable revision before VPS or public portfolio claims.

### Valuable but non-blocking

- Two-source VPS shadow pilot (NBOR plus one simple WordPress/HTML source), health record, bundle transfer, and a natural-run evidence card.
- SilverLeaf pages for a handful of tracked entities and a basic weekly summary.
- Search index compression and static-site build integration.

### Post-launch

- Opt-in subscriptions based on the same published release events and stable IDs.
- More sources, editorial improvements, entity pages, and better geographic matching.
- A limited daily schedule after a successful shadow period.

### Intentionally deferred / non-goals

- Real-time emergency/incident service, browser automation, complete county coverage, full GIS polygons/PostGIS, a SJC public API, autonomous publication, a multi-domain platform, a PostgreSQL corpus, and a custom Hermes runtime.

## 4. Recommended system topology

```text
Public sources
     |                         targeted discovery (manual/bounded model call)
     v                                      |
VPS: 1–2 deterministic fetchers ----------> candidate bundle
     | (timeout, lock, manifest, health)             |
     +---------------- signed/checksummed transfer --+--> Mac intake/ack
                                                            |
Mac file authority: source events -> intel items -> dedupe -> review queue
                                                            |
                                             human review + publication decision
                                                            |
                                deterministic reviewed-release JSON + compact search index
                                                            |
                                 Buddy portfolio static site / CDN (works without VPS)
                                                            |
                                 later: subscription worker consumes release events only
```

The VPS has one scheduler/writer authority. It fetches only approved source contracts, stores bounded temporary files and operational records, and never publishes. The Mac owns corpus history, review, archives, release preparation, and restore. Transfer uses a dated run bundle (`manifest.json`, checksums, source/event/item files, run log), an idempotency key, receipt acknowledgement, and an explicit prune gate; VPS retention begins only after acknowledgement plus archive verification.

## 5. Data and contract readiness

The current schemas establish a good conceptual model (stable IDs, source attribution, source events, review/sensitivity, entity references, controlled taxonomy), and deterministic dedupe exists. They are not yet machine-enforced at corpus boundary. The minimum pre-automation/publication contract is not a redesign:

- validate each changed item against required fields, enum values, ID pattern/uniqueness, registry references, source URL, timestamp, source-event linkage policy, and dedupe key;
- define one canonical storage location/record for an item so export can reject duplicate `item_id`s deterministically;
- add an explicit publication decision with `publication_status`, `published_at`, `published_release_id`, reviewer, and unpublish/withdraw semantics, either in the item or a separate release manifest; preserve review as separate from publication;
- require a `silverleaf_relevance` record (included / excluded / needs_review plus reason and matching IDs) for anything in the release;
- produce a compact, versioned public projection that excludes raw excerpts when unnecessary, reviewer fields, internal notes, source file paths, and sensitive metadata.

SQL readiness is already adequate in principle: stable IDs, normalized migration vocabulary, adapter boundary, and idempotent upsert intent exist. Keep those; do not make PostgreSQL authority a prerequisite. Add field-level validation and export tests before adding further migration complexity.

## 6. VPS operating model

**Productized:** Ivy has an inventory, control records, health/evidence conventions, exact-SHA/deployment templates, database templates, and an orchestration contract. SJC has inert systemd units, retention/backup documents, and a health-export shape.

**Documented but manual:** admission, approved SHA selection, service user/config, virtual environment, secrets, unit installation, health registration, backup/restore, rollback, and evidence bundle. The SJC control record says Gate 4/5 are not assessed/admitted.

**Missing/proven only by documentation:** an SJC clone, approved revision, resource snapshot, service account/config, production environment, a real health producer, transfer endpoint/process, restore drill, and natural-run proof.

Use an admission packet under Ivy's existing workflow; do not invent SJC deployment conventions. A Strong Codex/Buddy packet must approve operational intent, exact SHA, source list, retention, secrets, service/timer installation, and rollback. Medium agents can prepare unit/env/manifest drafts and fixture tests, but cannot activate services/timers or claim capacity.

Capacity scenarios are recommendations, not verified operating facts:

| Scenario | Recommended status | Bounds |
|---|---|---|
| A. Weekly deterministic fetches | Candidate after capacity/read-only admission evidence | One job at a time, 2 sources, 5–10 min timeout each, 1 retry, small raw cap, transfer same day. |
| B. Weekly fetches + agentic discovery | Defer until A proves 4 healthy runs | Separate window, single model call with token/time budget, no direct corpus write, candidates only. |
| C. Daily fetches + weekly discovery | Post-pilot only | Staggered timers, `Persistent=true` only with lock/idempotency, explicit max runtime, journal cap, transfer acknowledgement and 7–14 day raw retention. |

## 7. Hermes and agent-runtime recommendation

Do not build “Hermes” as a launch dependency. SJC has task prompts and historical worker artifacts but no installed runtime, invocation, provider/model, credential, cost envelope, queue, retry policy, timeout manager, concurrency control, duplicate guard, or scheduled execution. Classify it honestly as **prompt convention only**.

For launch, deterministic Python extractors run under one systemd service/timer only after the pilot gates. Agentic discovery is a manually triggered, bounded task packet on the Mac or a separately budgeted VPS job; it writes candidate artifacts, never publication-ready items. Ivy Hermes may remain a read-only orchestrator/reviewer where actually provisioned, but should not be asserted as the SJC runner.

## 8. PostgreSQL recommendation

Choose **Option B — operational metadata only, after SJC VPS admission**. Store run state, source freshness, locks, bounded transfer manifests/acknowledgements, and sanitized health references. The file corpus remains authoritative on the Mac. Option B gives concrete operational value and visibility without a two-truth corpus.

| Option | Launch value | Recommendation |
|---|---|---|
| A: no SJC PostgreSQL | Fastest static/manual launch; zero DB operations | Use until a VPS workload is activated. |
| B: operational metadata | Locks, health, transfer acknowledgement, bounded queues | Recommended narrow VPS option. |
| C: bounded staging | May simplify short disconnections, but increases reconciliation/retention work | Defer; only revisit after observed transfer failures. |
| D: active operational corpus | Adds sync, backup, authority, and search failure modes | Reject for first release. |

Neither subscriptions nor static search need a database. The existing migrations are useful design evidence, but their presence is not evidence of an applied, backed-up database.

## 9. Public UI and search recommendation

Generate a public `release.json` plus a compact lowercased token/field index during portfolio-site build. Load it client-side and filter on stable `primary_topic`/topic, `tracked_entity_ids`, and `place_id`/SilverLeaf inclusion IDs. At 83 initially verified records (and even several thousand compact rows), this is fast, cheap, cacheable, and VPS-independent. Source cards must link directly to original public sources and show the publication/review date separately from the source date.

Do not use a serverless API, direct database access, or a read-only VPS endpoint for v1. A static release can be cached, versioned, inspected in Git/artifact storage, and rolled back by re-deploying the prior release. The UI should say when the static release was generated and degrade to browse/filter if client-side search fails.

## 10. Subscription recommendation

Subscriptions are not launch-blocking. Design now for stable topic/entity/place IDs, publication release IDs, published/withdrawn events, and reviewed-only matching. Immediately after launch, use a managed email provider and a minimal subscriber store with consent timestamp, preferences, unsubscribe token, data minimization, and no source/internal metadata. Do not have a collector trigger email directly; a release-generation step emits eligible events after human review.

## 11. Reusability boundary

**Make generic now:** a written domain-agnostic publication-export contract, item/source-event/review/dedupe semantics, task/report acceptance template, run bundle manifest/acknowledgement, and deterministic validation interface.

**Keep SJC-specific:** source registry, taxonomy, resident-interest rules, monitoring scripts, county geography, community registry, and source authority rules.

**Keep SilverLeaf-specific:** launch inclusion/exclusion registry, entity ordering, UI copy, default filters, and editorial relevance policy.

**Defer:** pluginized extractor framework, generic UI product, cross-domain Postgres schema authority, PostGIS, and a universal agent runtime. Two extractors do not justify a framework; make their outputs conform first.

## 12. Harness and orchestration recommendation

Adopt one authority model without new parallel folders:

| Concern | Authority |
|---|---|
| Product direction, gates, phases | `ROADMAP.md` after Task 09 |
| Immediate prioritized work | `BACKLOG.md` |
| Bounded dispatched work / outcome | `tasks/` / `reports/` |
| Reusable worker instructions | `prompts/` and `.opencode/agents/` |
| Execution/cadence state | `logs/runs/*/LAST_RUN` plus future run manifests |
| Agent narrative/memory | `logs/agents/`; concise `.opencode/agent_memory/` pointers |
| VPS admission/deployment evidence | Ivy `repos/sjc-intel/CONTROL.md` and its existing private orchestration archive |

The harness notes apply strongly to bounded tasks, external verification, durable handoff, restartability, evaluator separation, and stop conditions. Do not copy their proposed artifact tree: SJC already has task/report/log conventions and Ivy has its own private control-plane queues. The missing harness link is contract enforcement: corpus validation, release tests, exact acceptance conditions, and an independent review before enabling timers.

## 13. Roadmap authority recommendation

Task 09 must rewrite **`ROADMAP.md`** as the sole current SJC execution roadmap. It should incorporate the product direction but not duplicate every supporting document. Update `README_INTERNAL.md` with a short current-state pointer/count correction, reconcile or demote `VPS_ROADMAP.md` to a supporting deployment plan, and update `docs/VPS_CONTINUITY.md` to match the Mac-authority/Option-B decision. Refresh `BACKLOG.md` only after the roadmap is accepted. Mark the dated architect memory and historical reviews as history; do not delete them. Coordinate the corrected SJC SHA/lifecycle with Ivy's `repos/sjc-intel/CONTROL.md` in a separate, authorized cross-repo packet.

## 14. Prioritized blockers

| Blocker | Dependency / acceptance condition | Strength | Privileged operation |
|---|---|---|---|
| B1: no publication contract/export | Schema decision; deterministic export test rejects unreviewed, incomplete, duplicate, or unscoped rows | Strong design + medium implementation | No |
| B2: SilverLeaf scope not operational | Curated aliases/entities/inclusion-exclusion rules with test fixtures | Medium after scoped task | No |
| B3: no public UI/search | Approved portfolio integration; static release renders/searches/filters with source links | Medium | Website deployment authorization |
| B4: corpus irregularities | Repair/disposition of 9 incomplete rows and duplicate IDs; validation passes | Medium, human review for content | No |
| B5: no reliable automatic update path | Two source contracts, shadow evidence, manifest/ack/prune contract, 4 healthy runs | Strong design + medium implementation | VPS admission, service/timer approval |
| B6: no public repo/deployable revision | Buddy remote/visibility decision; clean-history/security review | Buddy + Strong Codex | Remote/push approval |

## 15. False blockers and deferrals

PostgreSQL corpus authority, PostGIS/full polygons, browser automation, all county sources, real-time incidents, newsletters, a generic extractor plugin framework, and a bespoke Hermes platform are not launch blockers. Conversely, treating “verified” as automatically public, relying on prompts as a runtime, or deploying the existing templates without corpus/export validation are false signs of readiness and must not be accepted.

## 16. Recommended completion sequence

### P1 — Publication contract and clean corpus

**Outcome:** a release selector that proves what may be public. **Dependencies:** Task 09 roadmap. **Packages:** publication state/release manifest, corpus validator, duplicate/legacy disposition, export fixture tests. **Verification:** complete-corpus validation, export snapshot, negative tests. **Stop:** any ambiguity about sensitive/public eligibility. **Strength:** Strong Codex design; medium implementation.

### P2 — SilverLeaf lens and static release

**Outcome:** credible scoped public dataset. **Dependencies:** P1. **Packages:** manual registry, entity/place mapping, explicit exclusions, versioned `release.json` and search index. **Verification:** representative inclusion/exclusion fixtures; only published rows export. **Stop:** inability to state why each item is SilverLeaf-relevant. **Strength:** medium with Buddy editorial review.

### P3 — Portfolio UI

**Outcome:** accessible static UI on the portfolio site. **Dependencies:** P2 and site authority. **Packages:** list/cards/detail link, filters/search, methodology/limitations, release timestamp, rollbackable deploy. **Verification:** build, browser/accessibility smoke test, no internal data leak. **Stop:** source attribution or reviewed-only guarantee missing. **Strength:** medium.

### P4 — Bounded operations pilot

**Outcome:** two deterministic sources reliably transfer candidates to Mac. **Dependencies:** clean deployable revision, Ivy admission, capacity evidence, P1 contracts. **Packages:** single runner/lock/timeout, manifest/checksum/ack, real health producer, disabled systemd templates, shadow runs. **Verification:** four natural runs, zero unexplained duplicate processing, receipt/restore evidence. **Stop:** capacity, transfer, or content divergence failure. **Strength:** Strong Codex for packet/review; medium implementation; privileged VPS actions.

### P5 — Limited automation and post-launch subscription

**Outcome:** approved periodic updates and optional subscriptions. **Dependencies:** P4; publication flow stable. **Packages:** one scheduler authority, staggered cadence, metrics/alerts, managed subscriptions from releases. **Verification:** seven-day operational window; unsubscribe and publication-event tests. **Stop:** missed/duplicate runs or review bypass. **Strength:** Strong review + medium implementation + Buddy/VPS gates.

## 17. Strong Codex versus medium-agent allocation

**Strong Codex:** Task 09 authority rewrite; publication eligibility/withdrawal model; transfer authority and pilot gate packet; cross-repo control-record reconciliation; any security/privacy or two-truth decision.

**Medium OpenCode:** corpus validation implementation; export generator/tests; SilverLeaf registry population from supplied authorities; static UI; unit templates/wrappers; fixture-based extractor hardening; docs strictly owned by an approved task.

**Buddy decisions:** product/page name and public claims; remote/visibility; initial SilverLeaf scope/editorial policy; public publication acceptance; subscription provider/privacy; VPS activation and all deployment gates.

**Privileged VPS packets:** capacity inspection; repository clone/configuration; secret provisioning; systemd install/enable; PostgreSQL creation/migrations if Option B is accepted; backup/restore; production rollback.

## 18. Risks and unresolved decisions

- The chief risk is reputational: a public feed can imply completeness or automated alerting. Mitigate with scoped language, static timestamp, source links, and reviewed release gates.
- The current `verified` label is a review queue state, not an explicit publishing authorization. Separate those meanings before release.
- Current SJC/Ivy authority documents disagree on state and SHA; the roadmap/control record must be reconciled before deployment.
- Actual VPS capacity and scheduling contention are **MISSING**, not inferable from its plan name. The smallest next verification is an authorized Ivy read-only capacity/evidence packet.
- The public portfolio site's technology and deployment route were not in this repository. The smallest next verification is its existing build/deploy contract before assigning P3.

## 19. Proposed Task 09 instructions

Rewrite `ROADMAP.md` as the single authoritative SJC execution roadmap using this report as supporting analysis. Preserve the locked product decisions: SilverLeaf reviewed periodic intelligence; Mac file corpus authority; static publication export; no live-incident launch; SQL-ready but no database rewrite; minimal reusable seams; Option B PostgreSQL only upon VPS activation. Define P1–P5 above as gated work packages with owner strength, acceptance tests, stop conditions, and explicit Buddy/VPS gates. Reclassify supporting/historical documents, reconcile stale count/status claims, and list exact follow-up task packets. Do not edit application code/data, deploy, enable timers, apply migrations, publish, or change the VPS.

## 20. Candidate next tasks

1. **Task 09 — authoritative roadmap rewrite** (Strong Codex, assessment/doc-only).
2. **Publication contract design packet** (Strong Codex; decide release manifest versus item fields and privacy projection).
3. **Corpus validation and export implementation** (medium agent after #2).
4. **SilverLeaf inclusion registry and fixtures** (medium agent with Buddy-reviewed source list).
5. **Static portfolio UI integration packet** (medium agent after export exists).
6. **Ivy/SJC VPS admission and capacity inspection packet** (Strong Codex + explicitly authorized read-only VPS inspection).
7. **Two-source shadow runner/transfer pilot** (medium implementation under an approved privileged packet).

## Work performed

Read the required SJC entrypoints, roadmap/VPS/planning/data/schema/workflow/task/report/agent artifacts; inspected storage, extractors, migrations, adapters, deployment templates, tests, current data shapes/counts, and task/runtime artifacts; read the relevant Ivy control-plane authorities and SJC control record; evaluated the supplied harness notes as supporting guidance. No code, data, schema, infrastructure, migration, timer, service, VPS, or Git mutation was performed.

## Files and repositories inspected

SJC: `README_INTERNAL.md`, `README.md`, `AGENTS.md`, `BACKLOG.md`, `ROADMAP.md`, `VPS_ROADMAP.md`, `docs/VPS_CONTINUITY.md`, data model/retention/snapshot/backup/news/taxonomy/planning/monitor documents, schemas, registries, data, scripts, migrations, tests, `deploy/`, `runtime/`, `.opencode/`, `tasks/`, and `reports/`.

External read-only: `/Users/buddy/projects/ivy-control-vps` (`README.md`, `AGENTS.md`, VPS inventory, database/health/portfolio conventions, VPS orchestration, SJC control record, relevant templates/tools) and `/Users/buddy/projects/alori/learn-harness-engineering/notes.md`.

## Validation commands and results

```text
python3 -m pytest tests/ -v                         PASS — 109 passed in 10.21s
python3 scripts/validate.py                         PASS — all schema/compile/fixture/registry checks
python3 scripts/portability_check.py                PASS — migration/env portability checks
python3 scripts/retention.py --json                 PASS — dry run; no destructive actions
python3 scripts/metrics_snapshot.py --backend file --json
                                                    PASS — read-only generation, 192 total items reported
git status --short; git branch --show-current       inspected — master; pre-existing dirty tree
git -C /Users/buddy/projects/ivy-control-vps status --short --branch
                                                    inspected — main ahead 2; pre-existing dirty tree
```

## Evidence provenance

All claims marked VERIFIED derive from current local file/code/data inspection or the recorded command results above. DOCUMENTED BUT NOT VERIFIED claims derive from SJC/Ivy authority documents and were not confirmed against a live VPS. INFERRED recommendations are reasoned from the verified state and the locked provisional decisions. No private credentials, host details beyond public inventory context, or secret-adjacent material is reproduced.

## Final Git status

SJC remains on `master`; its pre-existing modified/untracked files were preserved. This task added only `reports/08-codex-redesign-1.md`. No commit, push, staging, or other Git write was performed.

## Unresolved issues

The precise SilverLeaf public inclusion list, portfolio-site integration path, remote/publication decision, real VPS resource evidence, and whether Option B is needed before the static launch require subsequent bounded decisions/packets.
