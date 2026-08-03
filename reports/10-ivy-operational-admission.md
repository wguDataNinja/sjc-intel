# Task 10 — Ivy Operational Admission

**Task identity:** final Strong Codex operational-admission pass  
**Date:** 2026-08-03  
**Repositories:** SJC_Intel; Ivy Control VPS  
**Final status:** PARTIAL

## 1. Executive outcome

The high-risk product contracts are finalized and durable. Publication/release semantics, corpus-validation requirements, SilverLeaf release safeguards, GPT/builder handoff rules, and a reusable Ivy off-VPS bundle/receipt/prune admission requirement are now documented.

SJC is **not operationally admitted or deployed**. No weekly timer, SJC runtime, transfer, database change, or service was enabled. This is the correct safe outcome: live evidence shows a dirty/no-remote SJC checkout with no approved deployable revision, an already busy VPS at 83% disk use with reboot pending, and Hermes installed but without configured provider authentication. The first public release remains independent of this operational work and is ready for the planned medium-agent contract implementation sequence.

## 2. Authorization used

Used Task 10's direct authorization for cross-repository edits and Mode 2 live VPS inspection. No secret/config file was read. No privileged mutation was performed because the deployment preconditions failed; no unrelated workload was touched.

## 3. Starting state

### SJC

- Branch: master; pre-existing dirty/untracked task, report, data, cadence, and fixture state.
- No remote; Ivy's control record has a stale approved SHA and reports source-only/not-deployed state.
- Existing deployment units are inert; no SJC VPS checkout was present.

### Ivy

- Branch: main, ahead of origin/main by two, with pre-existing modified/untracked governance work.
- Existing admission material had broad requirements but did not explicitly require the full off-VPS bundle-to-receipt-to-prune sequence.

### Live VPS (2026-08-03T09:00Z)

- Host reachable through the approved alias; disk 38G total / 30G used / 6.2G available (83%); inodes 17%.
- RAM 3.7 GiB total / 1.3 GiB available; swap 1.8 GiB used; load 2.34/2.43/2.29; reboot required.
- Existing active timers: WGU Reddit run and backup plus Launchpad cleanup. Active unrelated Chrome, collector-helper, Hermes Desktop/backend, and OpenCode processes were observed and left unchanged.
- PostgreSQL listens loopback-only on the VPS. A passwordless monitor query was unavailable; no password/config was requested or exposed.
- Hermes Agent v0.18.2 is installed, but provider authentication is not configured. It is not a safe automatic SJC execution runtime today.

## 4. Architecture decisions finalized

- Review and publication are separate; verified never authorizes publication.
- The file-compatible release manifest is the publication authority; explicit draft/published/withdrawn/superseded semantics, canonical selection, public allowlist, denylist, checksums, rollback, and legacy disposition are defined.
- Full-corpus validation and public-export negative cases are mandatory before release.
- SilverLeaf inclusion requires a stable-ID, rationale-bearing decision; no GIS/PostGIS is required for launch.
- Mac file corpus remains durable/review/release authority. VPS only prepares bounded operational bundles.
- PostgreSQL remains deliberately unused for SJC until it provides a concrete approved Option-B operational value.
- Hermes is installed portfolio tooling, not an approved SJC model runtime. Deterministic scripts and task/report control remain the initial runtime path.
- A generic Ivy admission contract now requires manifest/checksum, idempotent import/replay, receipt, acknowledgement, delayed prune predicate, and failure behavior for off-VPS durable authority.

## 5. Ivy changes

Updated docs/VPS_ADMISSION_CHECKLIST.md with a reusable off-VPS bundle-transfer admission addition. It distinguishes Ivy's operational/evidence ownership from project-owned bundle contents and domain validation, and forbids pruning merely because a transfer started.

## 6. SJC repository changes

- Added docs/publication_release_contract.md, the supporting authority for ROADMAP §§3A–3D.
- Extended ROADMAP.md with a link to that contract and §8 builder-packet/GPT coordination requirements, including high-reasoning gate evidence/questions.
- Retained VPS_ROADMAP.md and docs/VPS_CONTINUITY.md as supporting, Mac-authority-aligned documents from Task 09.

No runtime, transfer, data, schema, registry, or deploy-unit code changed because there is no approved clean revision to deploy.

## 7. VPS changes

None. No paths, users, permissions, environment files, health registrations, services, or timers changed. SJC remains absent from /home/scraper/apps.

## 8. PostgreSQL changes

None. No SJC database/role/schema/table/grant/migration/backup/restore operation occurred. Existing SJC migrations/adapters remain dormant, future-ready material. VPS PostgreSQL remains loopback-only and unrelated workloads were not queried or modified.

## 9. Hermes/runtime changes

None. Verified reality: Hermes Agent v0.18.2 is installed as a desktop/backend process; provider auth is not configured; no SJC profile, lock, budget, structured output, health producer, or schedule exists. Therefore it cannot be represented as a bounded weekly SJC runtime. A future weekly deterministic runner needs a separate exact-SHA deployment and explicit model/provider budget only if agentic discovery is included.

## 10. Transfer proof

No production transfer was attempted because SJC has no deployed runtime and the required importer/bundle implementation does not exist in an approved revision.

The new admission contract defines the required proof sequence: bundle manifest/checksum → Mac pull → checksum verification → idempotent import → receipt → producer acknowledgement → retention delay → prune. It also requires replay and failure behavior for offline Mac, partial transfer, duplicate bundles, failed import, delayed/lost acknowledgement, and disk pressure. Pruning is disabled until that evidence exists.

## 11. Validation

~~~text
SJC: python3 -m pytest tests/ -q
PASS — 109 passed (9.38s)

SJC: python3 scripts/validate.py
PASS — schemas, scripts, fixtures, registries, requirements

SJC: python3 scripts/portability_check.py
PASS

SJC: python3 scripts/retention.py --json
PASS — dry run only

SJC: python3 scripts/metrics_snapshot.py --backend file --json
PASS — file backend, no write requested

SJC: git diff --check -- ROADMAP.md VPS_ROADMAP.md docs/VPS_CONTINUITY.md docs/publication_release_contract.md
PASS

Ivy: git diff --check -- docs/VPS_ADMISSION_CHECKLIST.md
PASS

VPS: approved Mode 2 SSH preflight and read-only capacity/service/runtime inspection
PASS — evidence captured; no mutation
~~~

The full SJC diff check still reports pre-existing whitespace in tests/fixtures/nbor_raw.html, which this task did not change. Ivy's full test suite began successfully but did not yield a final result within this task window; no inference is made from its partial output.

## 12. Rollback and recovery

Documentation changes rollback through normal Git review. No live state requires rollback. For future SJC operation: keep timer disabled; rollback runtime to the recorded exact SHA; retain prior static release; replay a bundle by manifest identity; accept no prune until a verified import receipt has been acknowledged. Restore/migration activity remains separately gated.

## 13. Roadmap elaboration

ROADMAP §8 now requires GPT-issued packets to specify input/output paths, scope, dependencies, validation, report, stop/escalation, Git/network/cross-repo/privilege boundaries. It gives the ordered builder sequence and precise high-reasoning questions/evidence artifacts. This enables medium agents to implement rather than re-decide the architecture.

## 14. High-reasoning gates

- Editorial publication edge cases: GPT asks Buddy to approve the validator/exclusion report; output is an editorial decision record.
- Portfolio-site deployment: requires the §3C-G1 target-repo context report; GPT asks Buddy to approve the exact static route.
- VPS activation: requires fresh capacity, clean SHA, source selection, transfer/rollback packet; GPT asks whether the specific pilot is safe.
- Subscription/privacy and post-launch portability remain Buddy decisions with the evidence specified in ROADMAP §8A.

A new broad Strong Codex pass is not required; a narrow review is contingent only on a demonstrated contract conflict.

## 15. Medium-agent work plan

1. 10-publication-contract-implementation.md (§3A-G2; no network, no privileged access).
2. 11-silverleaf-scope-registry.md (§3B-G1; public authoritative sources only; editorial review gate).
3. 12-static-public-release-export.md (§3B-G2; no publish/deploy).
4. 13-portfolio-integration-context.md (§3C-G1; authorized cross-repo read-only).
5. 14-static-silverleaf-ui.md (§3C-G2; target-repo packet determines validation).
6. 15-first-reviewed-release.md (§3D; Buddy/editorial publication decision).
7. 16-sjc-vps-admission-packet.md (§3E-G1; privileged Ivy/VPS planning/evidence).
8. 17-sjc-shadow-run-proof.md (§3E-G2; only after clean exact-SHA deployment).
9. 18-weekly-activation-verification.md (§3F; timer remains disabled until proof).
10. 19-subscriptions.md and 20-portability-proof.md (post-launch).

## 16. Hermes work plan

Until deployment proof, Hermes may only perform existing read-only portfolio inspection and dispatched artifact coordination. It may not operate an SJC weekly job. After §3E-G2, an approved deterministic weekly runner may collect the two selected sources under one scheduler/writer, lock, timeout, bounded output, health, bundle, and receipt controls. Agentic discovery stays manual/candidate-only until a separate provider/cost/runtime packet passes.

## 17. GPT coordination notes

For each report, verify: exact goal acceptance evidence; publication/review separation; no scope or authority drift; clean versus protected Git state; no claim of live proof from documentation; checksum/receipt evidence before prune; and explicit Buddy decisions. Update tasks/reports/roadmap only through the defined roles.

## 18. Risks and unresolved items

The deployment blockers are real and minimal: a clean reviewed exact SHA/remote path, fresh capacity after reboot and workload-window assessment, and a deliberate runtime/provider decision. SJC must not be copied from its dirty local checkout. The VPS has limited disk headroom and active unrelated Chrome/collector workloads, so no additional recurring task should be enabled before its specific capacity and schedule packet passes.

## 19. Final system status

| Area | Status |
|---|---|
| Publication foundation | COMPLETE |
| Corpus validation | READY_FOR_MEDIUM_AGENT |
| SilverLeaf registry | READY_FOR_MEDIUM_AGENT |
| Static export | READY_FOR_MEDIUM_AGENT |
| Portfolio UI | READY_FOR_MEDIUM_AGENT |
| Ivy admission contract | COMPLETE |
| VPS deployment | BLOCKED |
| PostgreSQL | DEFERRED |
| Hermes | PARTIAL |
| Transfer | READY_FOR_MEDIUM_AGENT |
| Weekly scheduling | BLOCKED |
| Portability | DEFERRED |

## 20. Final Git and VPS state

SJC changed ROADMAP.md and added docs/publication_release_contract.md plus this report; Task 09’s supporting VPS docs remain modified. Ivy changed docs/VPS_ADMISSION_CHECKLIST.md. All other dirty/untracked files in both repositories were pre-existing and preserved. Nothing was staged, committed, pushed, deployed, or altered on the VPS.

The live VPS remains unchanged: no SJC checkout, service, timer, database object, bundle, receipt, or prune action exists.

