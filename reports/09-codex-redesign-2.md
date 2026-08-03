# Task 09 — Codex Redesign 2

**Task identity:** authoritative roadmap rewrite and completion-plan consolidation
**Executor:** Codex
**Date:** 2026-08-03
**Final status:** COMPLETE_WITH_FOLLOW_UP

## 1. Executive summary

ROADMAP.md is now the single current execution roadmap. It makes the static, reviewed SilverLeaf release the launch milestone and keeps VPS activation separate. The first execution task is a Strong Codex publication-contract design packet (§3A-G1), followed by medium-agent corpus validation (§3A-G2).

The roadmap retains Mac file-corpus authority, treats PostgreSQL Option B as optional post-admission metadata only, classifies Hermes as a non-launch prompt convention, and adds a stable post-launch portability/reuse track (§4A-G1, §4B-G1). The track documents reusable boundaries and demands a portability proof before any multi-domain product claim.

## 2. Starting state

SJC_Intel began on master with a pre-existing dirty working tree: modified backlog/data/review/cadence/fixture files and untracked data, logs, tasks, and reports. These unrelated artifacts were preserved. Task 08 had already established the verified planning baseline and identified stale/conflicting VPS documents.

## 3. Files inspected

Primary authorities: reports/08-codex-redesign-1.md, README_INTERNAL.md, AGENTS.md, BACKLOG.md, prior ROADMAP.md, VPS_ROADMAP.md, docs/VPS_CONTINUITY.md, tasks/README.md, reports/README.md, and the Task 09 packet.

Supporting references consulted as needed: product-direction planning, data/schema/workflow materials, and the Task 08 Ivy-control findings.

## 4. Files changed

- ROADMAP.md — fully rewritten as the authoritative, stable-identifier execution roadmap.
- VPS_ROADMAP.md — reduced to a supporting VPS plan explicitly subordinate to roadmap §§3E–3F; removed the superseded PostgreSQL-corpus trajectory.
- docs/VPS_CONTINUITY.md — replaced stale/internally conflicting operational assertions with concise current continuity/routing requirements.
- reports/09-codex-redesign-2.md — this task result report.

No application code, data, schemas, tests, registries, prompts, Ivy control record, VPS, PostgreSQL, services, timers, or BACKLOG.md were changed.

## 5. Roadmap structure

- §1 establishes product finish line, launch exclusions, and the generic → SJC → SilverLeaf responsibility boundary.
- §2 records the verified file-backed baseline without stale operational counts.
- §§3A–3G define P1–P5 as gated work: publication contract, corpus validation, SilverLeaf registry/export, portfolio integration/UI, launch, two-source VPS pilot, operational activation, and subscriptions.
- §4 is an explicitly post-launch portability/reuse track with stable goals §4A-G1 and §4B-G1.
- §§5–7 cover deferred architecture triggers, authority allocation, and verification conventions.

Each executable goal states outcome, dependencies, scope, acceptance, verification, stop conditions, agent strength, and artifacts.

## 6. Decisions preserved

- First public product: reviewed static SilverLeaf Intelligence on the portfolio site.
- Human-reviewed publication; verified is not automatically published.
- Mac file corpus remains durable authority and release source.
- VPS is optional for launch and bounded/gated for later operations.
- PostgreSQL Option B is optional narrow metadata after admission; corpus authority/staging are deferred.
- No SJC Hermes runtime exists; no new Hermes platform is a launch dependency.
- Static export/search precedes APIs and stays VPS-independent.
- Subscriptions are post-launch; live incidents, GIS, broad automation, and generic platform work are deferred.

## 7. Corrections and pushback

No accepted Task 08 recommendation was reversed. The supporting VPS documents were corrected because their prior language presented a PostgreSQL operational corpus/cutover trajectory inconsistent with Task 08 and the accepted Task 09 direction. The rewritten roadmap also rejects treating existing systemd templates or “Hermes-ready” documentation as evidence of deployable automation.

## 8. Validation

~~~text
python3 -m pytest tests/ -v
PASS — 109 passed in 10.19s

python3 scripts/validate.py
PASS — all schema, compilation, fixture, registry, and requirements checks passed

git diff --check -- ROADMAP.md VPS_ROADMAP.md docs/VPS_CONTINUITY.md
PASS — no whitespace errors in Task 09 documentation changes

git status --short --untracked-files=all
INSPECTED — Task 09 changes plus preserved pre-existing working-tree changes
~~~

A full git diff --check reports pre-existing whitespace in tests/fixtures/nbor_raw.html; that unrelated file was not changed by this task.

## 9. Authority cleanup

- **Authoritative:** ROADMAP.md for execution sequencing/gates; BACKLOG.md for immediate approved work; AGENTS.md for agent rules; tasks/ and reports/ for bounded task workflow.
- **Supporting:** VPS_ROADMAP.md and docs/VPS_CONTINUITY.md, now explicitly subordinate to §§3E–3F.
- **Historical/supporting only:** Task 08, dated architectural reviews, and historical VPS assertions. They may inform work but cannot override the roadmap.
- **Follow-up reconciliation:** Ivy's SJC control record remains outside this task’s authorized scope and needs a separate cross-repo packet before privileged VPS work.

## 10. Candidate next tasks

1. 10-publication-contract-design.md — Strong Codex design packet for review/publication/release/withdrawal semantics.
2. 11-corpus-validation-and-publication-selector.md — medium implementation after Task 10 approval.
3. 12-silverleaf-scope-registry.md — medium implementation with Buddy/editorial scope approval.
4. 13-static-public-release-export.md — medium implementation after Tasks 10–12.
5. 14-portfolio-integration-context.md — authorized cross-repo read-only packet.
6. 15-vps-admission-and-capacity-packet.md — Strong Codex/Ivy packet; post-launch or parallel only.

## 11. Unresolved decisions

- Buddy must approve publication policy, SilverLeaf inclusion authorities, public naming/claims, remote/visibility, and any publication/deployment.
- The portfolio-site repository and deployment contract require an authorized context packet.
- Real VPS capacity, service configuration, and Ivy control-record reconciliation need a privileged, read-only cross-repo/VPS packet.
- The portability proof domain is intentionally deferred for Buddy selection after launch.

## 12. Evidence provenance

The roadmap follows Task 08’s verified local code/data/test inspection. Current validation results above were produced locally. VPS facts are intentionally limited to documented evidence; no live VPS or private infrastructure access occurred.

## 13. Final Git status

The task changed only ROADMAP.md, VPS_ROADMAP.md, docs/VPS_CONTINUITY.md, and this report. Pre-existing modified/untracked files were preserved. No staging, commit, push, deployment, service action, migration, or data mutation occurred.

