# Task 15 — Publication Readiness Review and Ivy Onboarding Retrospective

**Task identity:** 15-publication-readiness-review.md
**Date:** 2026-08-03
**Repositories:** SJC_Intel (`/Users/buddy/projects/sjc_intel`), Ivy Control VPS (`/Users/buddy/projects/ivy-control-vps`, read-only)
**Final status:** COMPLETE_WITH_FOLLOW_UP

## 1. Executive result

SJC_Intel is technically mature and the remaining path to a public
SilverLeaf release is short and code-light: the release is gated primarily on
**editorial decisions and UI implementation**, not architecture. The full
onboarding history is reconstructed here; the dominant finding is that SJC
outpaced Ivy's formal gate tracking for most of its lifecycle, and Ivy's SJC
control record still lags reality. Ownership between the two repositories was
largely correct but inconsistently recorded.

Decision-ready outputs in this report: the first-release candidate pool and
exclusion rules (§15–16), the exact publication blockers (§19), the reusable
Ivy onboarding sequence and Reckless Ben checklist (§21–22), the VPS storage
philosophy translated into artifact-level rules (§24–25), and a Strong Codex
live-storage packet (§26).

Approved SJC changes applied this task: **MIT LICENSE added** (matching
origin/main), public README license section, PostgreSQL disposition labeled
`DORMANT_FUTURE_READY` in `docs/postgresql_adapter.md`, backup deferral
clarified in `docs/backup-restore.md`, and a §6A ownership-boundary note added
to ROADMAP.md. No publication decision was made; no review decision was
altered; no VPS/PostgreSQL/systemd/Hermes/Ivy state was touched; nothing was
committed or pushed.

## 2. Starting SJC state

| Item | Value | Label |
|------|-------|-------|
| Branch / HEAD | `master` @ `1be2ade` | VERIFIED |
| Remote | origin `https://github.com/wguDataNinja/sjc-intel.git`; origin/master == local (0/0) | VERIFIED |
| Working tree | 45 lines (8 modified, 37 untracked) — pre-existing dirty data + Tasks 12–14 outputs | VERIFIED |
| Tests / validation | 140 passed; `validate.py` ALL PASSED; portability PASS | VERIFIED |
| Review queue | 167 entries (83 verified / 78 pending / 5 archived / 1 rejected_noise) | VERIFIED |
| Human-review-required | 8 items | VERIFIED |
| Publication state | None — no `publication_status`, no release manifest, no export | VERIFIED |
| Release artifacts | None | VERIFIED |
| SilverLeaf classifications | Partial — `communities.yaml` + `tracked_entities.yaml` seed; no inclusion registry/decision fields | PARTIAL |
| README | Public-safe (Task 14) | VERIFIED |
| Architecture doc | `docs/ARCHITECTURE.md` public (Task 14) | VERIFIED |
| License | Added MIT LICENSE (this task, matching origin/main) | VERIFIED |
| Ignored/runtime footprint | `runtime/` 176 KB (ignored), `.opencode/node_modules` 57 MB (ignored) | VERIFIED |

## 3. Starting Ivy state

| Item | Value | Label |
|------|-------|-------|
| Branch / HEAD | `main` @ `3e94197`, 2 ahead of origin | VERIFIED |
| Working tree | 17 dirty lines (pre-existing control-plane work incl. `repos/sjc-intel/CONTROL.md` modified) | VERIFIED |
| SJC control record | `repos/sjc-intel/CONTROL.md`: `remote: null`, `approved_sha: 35a0246`, gate 1 `NOT YET ADMITTED`, gate 3 `BLOCKED` | **CONFLICT** (lags reality) |
| SJC release-gate record | `RELEASE_GATES.md` does not exist | MISSING |
| Approved SHA | `35a0246` (record) vs local `4262169`/`1be2ade` | CONFLICT |
| Documented blockers | "No remote configured" (record) — remote now exists | CONFLICT |
| Capacity | 83% disk, reboot pending (report 10, self-reported Mode 2) | DOCUMENTED BUT NOT VERIFIED |
| Hermes | v0.18.2 read-only; provider auth not configured | VERIFIED |
| Scheduling | No SJC timer; WGU-Reddit ~07:00 UTC + backup + Launchpad active | VERIFIED |
| Backup disposition | No explicit gate (Task 14 proposed patch not applied) | MISSING |
| Ivy SJC evidence | Intake 2026-07-28 (INTAKE_COMPLETE); orchestration archive for resume-roadmap-assessment; Task 10 Hermes validation ACCEPT_WITH_NOTE | VERIFIED |

## 4. SJC work-history reconstruction

| # | Phase | Where | Evidence | Ivy updated? | Ivy gate passed? | Gate should have been updated? | Status |
|---|-------|-------|----------|--------------|------------------|-------------------------------|--------|
| 1 | Initial local buildout (Jun 2026): operational intake, review queue, source events, taxonomy, interest filters, CDD registries, BCC extractor, NBOR source_event model, data-model doc, dedupe/queue tooling, backfill | SJC | commits `8187eb0`→`f4eb0b4`, `b70a631`, `961ee39`, `5270461`, `04144db`, `cf9a8e3` | No | No | No (pre-portfolio) | DONE (pre-Ivy) |
| 2 | VPS planning discovery (Jun–Jul): VPS-aligned discovery briefs, review packet, deployment config, VPS continuity, backup/restore docs | SJC | commits `2fd14f7`, `e1e9023`, `ab0faed`, `6280bc3` | No | No | No (planning) | DONE (SJC-only) |
| 3 | PostgreSQL foundation (Jul): migrations/validation/fixtures, adapter layer, pilot loader, health export, storage adapter, GitHub Actions, portable PG adapter | SJC | commits `4be23e2`, `40560d3`, `6695da2`, `f4cd039`, `6cd9bf5`, `f1659d6` | No | No | No | DONE — dormant future-ready |
| 4 | Product-direction pivot → SilverLeaf (Jul 6): product/sourcing direction, schema-fit + search design, actual-data evidence packet, cross-project comparison, comprehensive review, direction reconciliation | SJC | `18e143a`, `fe93c5f`, `dc73a48`, `9d2d9aa`, `48f9dae`, `ba837be`, `b19f9ed`, `3383e2d` + `docs/planning/` | No | No | No | DONE (SJC-only) |
| 5 | SilverLeaf scope: entity registry model/test/diffs, neighborhoods + commercial entities, prompt-led discovery standards, recurring discovery prompt, search profiles | SJC | `5be20e9`, `0656e70`, `2bfd458`, `12e25aa`, `45bd9c4`, `35a0246` | No | No | No | DONE (SJC-only) |
| 6 | Hermes-readiness roadmap restore; 29d cadence gap | SJC | `f0d9b25` | No | No | No | DONE |
| 7 | Resume assessment (Task 01, 2026-08-02, read-only); July artifact disposition (Task 02 → `4262169`); monthly closeout (03); daily catchups (04, 06) + independent checks (05, 07) | SJC | reports 01–07; Ivy orchestration archived `2026-08-02-resume-roadmap-assessment` | Partially — orchestration intake/task archive recorded it | No formal gate | Yes (control record should reflect current SHA) | DONE |
| 8 | Codex redesign 1 (Task 08): architecture/publishability/deployment assessment | SJC | report 08 | No (SJC-only) | No | No | DONE |
| 9 | Codex redesign 2 (Task 09): ROADMAP rewrite, VPS_ROADMAP + VPS_CONTINUITY correction | SJC | report 09, commit 1be2ade | No | No | No | DONE |
| 10 | Ivy operational admission (Task 10): publication_release_contract, ROADMAP §8, Ivy VPS_ADMISSION_CHECKLIST bundle-transfer addition | SJC + Ivy | report 10; Ivy `docs/VPS_ADMISSION_CHECKLIST.md` | **Yes** (cross-repo checklist edit) | No (PARTIAL — preconditions failed) | Yes | DONE (admission not granted) |
| 11 | Admission continuation (Task 11): remote configured + master pushed → origin/master @ 1be2ade | SJC | report 11; git | **No** (CONTROL.md not updated) | No | **Yes** (Gate 2/3 now effectively passed, unrecorded) | DONE — gate record stale |
| 12 | Weekly operations implementation (Task 12): weekly contract, bundle tooling, manifest schema, Hermes task spec, roadmap §3E | SJC | report 12 | No | No | No | DONE |
| 13 | Candidate-to-corpus import (Task 13): run_weekly, importer, acceptance, proposal review, SJSO RSS proposal proof | SJC | report 13 | No | No | No | DONE |
| 14 | Publish readiness + onboarding (Task 14): public README, ARCHITECTURE, backup policy, task declaration, SJSO RSS monitor, scheduling doc | SJC | report 14 | No (patches proposed) | No | No | DONE |
| 15 | This task (Task 15): publication review + Ivy retrospective; MIT LICENSE; doc clarifications | SJC | this report | No (patches proposed) | No | Yes | DONE |

**Cross-cutting:** The Hermes validation of Task 10 (Ivy `_internal/outbox/runs/2026-08-03-sjc-codex-followup`) independently re-ran SJC validations and confirmed evidence — the first true Ivy-side verification of SJC work.

## 5. Material work outside formal Ivy gates

- All of Phases 1–9 (§4) occurred before Ivy intake (2026-07-28). This is legitimate pre-admission work, but it means Ivy had no visibility into architecture/product/VPS/PostgreSQL decisions until Task 08–10 (2026-08-03).
- Approvals were informal within SJC (Buddy + architect memory + task/report flow) — no Ivy gate evidence was produced until Task 10.
- Artifacts existed before corresponding gates: e.g., inert systemd templates, migration/backup docs, and a VPS_ROADMAP existed before any VPS admission gate.
- CONTROL.md became stale immediately after Task 11 (remote + push) and was never reconciled.
- Ivy only learned about the pushed remote and reviewed SHA through this report series, not through its own gate tracking.

## 6. Gate-by-gate SJC status

Ivy's five-gate model (from `REPOSITORY_CONTROL_MODEL.md` + CONTROL.md):

| Gate | Documented requirement | Required evidence | Actual SJC evidence | True status | CONTROL.md says | Missing records | Out of order | Classification |
|------|------------------------|-------------------|---------------------|-------------|-----------------|----------------|--------------|----------------|
| 1 — Portfolio Admission | Control record + portfolio fit | CONTROL.md, fit rationale | CONTROL.md created as portfolio batch 1; PORTFOLIO_INTENT lists SJC Active | Admitted de facto | `NOT YET ADMITTED` | Gate-1 approval record | — | **PASSED_NOT_RECORDED** |
| 2 — Public Repository Readiness | Public-readiness review | Hygiene, public/private review, reviewed SHA | Clean tracked tree, no secrets, remote now configured | Effectively ready (needs formal review) | `UNKNOWN` | Readiness review evidence | — | **PARTIAL** |
| 3 — GitHub Publication | Publication gate | Published repo, reviewed SHA, history review | origin/master @ 1be2ade pushed (Task 11) | Published to GitHub (unreviewed claim) | `BLOCKED — no remote` | Publication-gate record | Push preceded gate | **PASSED_NOT_RECORDED** |
| 4 — Deployment Readiness | Service/runtime/health proof | Service-user, unit, health, secrets, rollback | Repo foundation (task declaration, bundle, systemd templates inert) | Not assessed (correct) | `NOT YET ASSESSED` | Gate-4 packet | — | **NOT_STARTED** |
| 5 — VPS Deployment | Deployment | Live deployment evidence | None | Not deployed (correct) | `NOT APPLICABLE` | — | — | **NOT_STARTED** |

**Assessment:**
- **Gate 2 vs Gate 3 are NOT distinct enough in practice.** Gate 2 (readiness) and Gate 3 (publication) collapsed: pushing to GitHub (Task 11) was both the readiness proof and the publication act. Recommendation: merge into one "Public Repository Publication" gate with a single hygiene+publication review.
- **Gate 4 is overloaded** — it mixes deployment readiness, runtime authority, health, secrets, and (in SJC's case) weekly-task/bundle/transfer concerns. Recommendation: split "Deployment Readiness" from "Operational Activation" and treat canonical-ingestion admission (source monitor admission) as a project-owned concern, not a Gate 4 subgate.
- **Static public launch should NOT depend on Gate 5.** Launch (§3D) is Mac-only and VPS-independent. Gate 4/5 govern the optional VPS pilot. This is already true in ROADMAP but Ivy's CONTROL.md gate table implies deployment readiness precedes launch. Recommendation: document "public static launch does not require VPS deployment."
- **Project agents do not know when to request a gate update.** CONTROL.md was last touched by Ivy-side work; SJC agents correctly avoided editing it but also never requested an update. Recommendation: add a documented "request gate update" step to the task/report template.

## 7. Admission-checklist effectiveness

Evaluation of `VPS_ADMISSION_CHECKLIST.md` (10 items + bundle-transfer addition) against the real SJC experience:

| Item | SJC supplied | Evidence lives in | Clear? | Checked at right time? | Needs template? | Needs automation? | Gate vs checklist? | Repeated work? |
|------|--------------|-------------------|--------|------------------------|-----------------|-------------------|---------------------|----------------|
| 1 Identity/fit | Purpose, portfolio fit | SJC README/ARCHITECTURE; PORTFOLIO_INTENT | Yes | Late (post-intake) | Minor | No | Checklist | No |
| 2 GitHub authority | Remote + SHA @ 1be2ade | Git + report 11 | Yes | **Late** — happened before formal readiness review | Yes (SHA pin template) | No | **Gate** | Yes (recorded in 3+ places) |
| 3 Hygiene | Clean tracked tree, no secrets | git status, Task 08 | Yes | On-time | No | Yes (secret scan) | Gate | No |
| 4 Data lifecycle | Retention + backup docs | docs/retention.md, backup-restore.md | Partly | On-time | Yes | No | Checklist | Some |
| 5 PostgreSQL | DORMANT_FUTURE_READY declared | postgresql_adapter.md, VPS_ROADMAP | Yes | On-time | No | No | Checklist | No |
| 6 Capacity | 83% disk / reboot (self-reported) | report 10 | Yes | On-time but self-reported | Yes (evidence card) | Yes (re-verify) | **Gate** | No |
| 7 Placement/deployment | Exact-SHA packet | reports 12/13/14 | Yes | Not yet executed | Yes | No | **Gate** | No |
| 8 Runtime authority | Task declaration, bundle/import/receipt | deploy/sjc-weekly-task.yaml, weekly contract | Yes | On-time (design) | Yes (unit template) | Partial | **Gate** | No |
| 9 Secrets/recovery | None required + backup policy | weekly task manifest, backup-restore | Yes | On-time | No | No | Checklist | No |
| 10 Acceptance/cleanup | Shadow-run sequence | weekly_scheduling §5, report 13 | Yes | Not yet executed | Yes (proof-run card) | No | **Gate** | No |
| 11 Backup disposition (proposed) | Defined in SJC; Ivy gate missing | backup-restore.md §0 | Yes (SJC) | Not yet in Ivy | Yes | No | **Gate** | No (would remove future rework) |

**Effectiveness verdict:** the checklist is a good evidence inventory but (a) several items are really gates with binary decisions (2, 3, 6, 7, 8, 10, 11), (b) most evidence must be re-collected in reports and CONTROL.md (duplication), and (c) it was applied only after SJC had already passed most readiness work.

## 8. Repository-versus-Ivy ownership findings

The expected boundary (§ task) was **mostly respected but inconsistently recorded**:

- **Correct:** SJC owns roadmap, tasks/reports, registries, schemas, extractors, tests, editorial workflow, release artifacts, operator docs. Ivy owns VPS/database/runtime standards and gate state. Task 10 correctly edited the Ivy checklist (shared contract) while keeping SJC reports in SJC.
- **Violations/overlaps found:**
  1. **Stale CONTROL.md** (approved SHA, remote, gate state) — Ivy's gate record is Ivy's to maintain but it lags reality; no process ensured reconciliation.
  2. **Duplicated next-task state** — ROADMAP §8, BACKLOG, CONTROL.md `next_task`, and architect memory each record overlapping "what's next" in different wording.
  3. **Planning doc location sprawl** — SJC `docs/planning/` reconciles against the older `ivy-control` repo standards (three locations: SJC, ivy-control, ivy-control-vps).
  4. **Ivy outbox/orchestration** archived some SJC task work (resume-roadmap-assessment) while CONTROL.md wasn't updated — evidence routing and gate records were inconsistent.
  5. **`RELEASE_GATES.md` referenced but never created** for SJC.
- **Recommendation (formal):** Ivy owns admission, shared VPS/database/runtime standards, gate/control records, operational evidence, and activation/offboarding. Project repos own implementation tasks/reports, product roadmap, domain behavior, workload code, output contents, tests, editorial review, and publication. Adopt the §6A ownership note (added to ROADMAP) as the reference, and have Ivy's next agent reconcile CONTROL.md to it.

## 9. Documentation-location conflicts

| Artifact | Where it lives now | Recommended owner | Conflict |
|----------|--------------------|-------------------|----------|
| Roadmap / sequencing | SJC ROADMAP.md; Ivy ROADMAP.md has its own priorities | SJC (project) | Overlapping "roadmap" nouns across repos |
| Weekly/bundle/transfer contract | SJC docs/weekly_operational_contract.md | SJC + Ivy shared (bundle-transfer part already in Ivy checklist) | Duplicated requirement (Ivy checklist §bundle + SJC contract) |
| Backup requirements | SJC backup-restore.md; Ivy DATA_LIFECYCLE + BACKUP_MANIFEST standards | Shared with Ivy authority | SJC policy references Ivy standards (good); Ivy has no per-repo backup-disposition gate |
| PostgreSQL standards | Ivy DATABASE.md; SJC postgresql_adapter.md | Ivy (standards) + SJC (disposition) | SJC adopted Ivy roles/naming; disposition now labeled |
| Task/report flow | SJC tasks/ + reports/; Ivy orchestration archives some | SJC (project) | Duplication when Ivy archives copies |
| Hermes | Ivy HERMES_OPERATOR_GUIDE + SJC prompts/ | Shared | Terminology confusion ("Hermes-ready" in SJC docs vs Ivy Hermes runtime) |
| Editorial/publication | SJC publication_release_contract.md | SJC + Buddy | Correct |

## 10. Publication-plan synthesis

Every material proposal about public release:

| Proposal | Source | Classification |
|----------|--------|----------------|
| SilverLeaf-first public product | product-direction 2026-07-06 | accepted + roadmap |
| Static reviewed-only release | Task 08/09 | accepted + roadmap |
| Publication ≠ verified | Task 10 contract | accepted + implemented as contract |
| Three-lane architecture | product-direction | accepted; lanes 2–3 deferred |
| Geographic registry foundational | product-direction | accepted; §3B-G1 task pending |
| PostGIS preferred for geo filtering | product-direction | deferred (not launch) |
| Option B operational metadata | Task 08 | accepted (post-admission, optional) |
| Mac file corpus authority | Task 08/09 | accepted + implemented |
| No live-incident launch | Task 08/09 | accepted |
| Subscriptions post-launch | Task 08/09 | deferred |
| Public traffic map UI | product-direction | tabled/deferred |
| Screenshots/diagram | Task 14 | proposed — not yet produced |
| "Reference implementation" claim | ROADMAP §4 | accepted — must not overstate |

**Claims to avoid publicly:** "automated alerts," "real-time," "complete county coverage," "multi-domain platform," "autonomous." The public README/ARCHITECTURE already avoid these. Ideas only in task reports (e.g., subscription UX details, incident-page spec) should not appear publicly until implemented.

## 11. Repository publication readiness

| Element | Status | Class |
|---------|--------|-------|
| GitHub repository | remote configured; master pushed @ 1be2ade | ready (formal gate review pending) |
| README | public-safe (Task 14) | ready |
| Architecture doc | docs/ARCHITECTURE.md | ready |
| MIT license | added this task | ready |
| Setup/validation instructions | README | ready |
| Examples | none dedicated | optional (post-launch) |
| Screenshots/diagrams | none | optional (after first release) |
| Limitations | ARCHITECTURE §12 | ready |
| Security/privacy notes | implicit; not a dedicated section | ready with minor edit (add a "Privacy and sources" line) |
| Internal-doc exposure | README points to ARCHITECTURE only; `README_INTERNAL.md`/`AGENTS.md` remain internal but tracked | **private** — keep out of public narrative; consider a `.github`-level public-safe profile later |
| Public-safe roadmap references | ROADMAP is internal; public site should not link it | private |

**Verdict:** repository is **ready with minor edits** (privacy note; decision whether internal docs remain in the public repo or move). No blocker.

## 12. Product-data publication readiness

- **Eligible items:** only `verified` + valid source URL + low/medium approved sensitivity + SilverLeaf-relevant + explicit publication decision. All 83 verified have source URLs (0 missing).
- **Issue:** verified set is dominated by BCC agenda action items (40) and NBOR notices (25), most countywide and not SilverLeaf-relevant. Only ~8 verified items have loose SilverLeaf keyword proximity, none strongly SilverLeaf-specific.
- **Sensitivity:** 1 verified item is high-sensitivity (`SJC-SJSO-20260603-0004`, double-murder arrest); 8 items are human-review-required. Crime items are excluded by default.
- **Duplicates/obsolescence:** dedupe index healthy; some June items are stale for a fresh release window.
- **Editorial review:** 78 pending items must be triaged before a meaningful release.
- **No items are marked published** — correct.

## 13. UI and portfolio requirements

Minimum launch pages (all static, VPS-independent):
- Homepage + latest-intelligence list (launch-critical);
- SilverLeaf overview + methodology + limitations (launch-critical);
- topic/entity/place filters + client-side search (launch-critical);
- item detail with source attribution + review/source dates (launch-critical);
- architecture/case-study page (optional — README/ARCHITECTURE can carry it).

Optional/post-launch: entity pages, weekly summary, screenshots, demo video, subscriptions.

**Portfolio emphasis** (per PORTFOLIO_INTENT: SJC = "scheduled autonomous intelligence generation" demonstration): the public presentation should lead with the research/automation pipeline proof — deterministic monitoring, evidence model, human review, bounded automation, low-cost Mac/VPS split, portability — with SilverLeaf as the concrete domain example. Assign: README + ARCHITECTURE (done); portfolio-site copy (future UI task); screenshots after first release.

## 14. Editorial queue summary

| Metric | Count |
|--------|-------|
| Total entries | 167 |
| Verified | 83 |
| Pending review | 78 |
| Archived | 5 |
| Rejected noise | 1 |
| Human-review-required | 8 |
| High sensitivity | 5 (3 SilverLeaf crime/minor items pending; 1 SJSO verified high; 1 other) |
| Likely SilverLeaf-relevant (keyword proximity) | ~10 |
| Likely release-eligible (verified + low/medium) | ~75 (but mostly countywide BCC/NBOR) |
| Likely noise | few (1 rejected already); many NBOR notices low-value for public |
| Likely duplicates | dedupe prevents most; BCC item_id repeats flagged in Task 08 |

Verified by source: BCC 40, NBOR 25, county_news 8, utility 5, SJSO 4, emergency 1.
Pending by source: NBOR 50, silverleaf_discovery 11, county_news 4, utility 3, CDDs 9, SJSO 1.

## 15. Candidate first-release set

**Finding:** the corpus has almost no *verified* SilverLeaf-specific items. A defensible first release is therefore **small and curated**, combining (a) the strongest SilverLeaf-adjacent verified items and (b) SilverLeaf-relevant pending items after editorial verification. Proposed **starter pool** for Buddy/GPT to curate (not a final release):

| Item | Title | Source | Sens. | Status | Why considered | Open issue |
|------|-------|--------|-------|--------|----------------|------------|
| SJC-UTIL-20260603-0002 | Free Chlorine Burnout June 1–21 | utility | low | verified | Affects all county utility customers incl. SilverLeaf; service continuity | Older date — refresh check |
| SJC-CN-20260626-0002 | Railroad Crossing Maintenance closures | county news | low | verified | Transportation; corridor relevance (West King/Kinlaw — north county) | Confirm SL access relevance |
| SJC-CN-20260603-0001 | Surplus Public Auction | county news | low | verified | Countywide civic | Low SL relevance — likely exclude |
| SJC-UTIL-20260603-0003 | SR 207 Water Reclamation Phase 2 | utility | low | verified | Water infrastructure | SR 207 is south county — likely exclude |
| SJC-NBOR-20260626-0017 | REZ 3025 Old Moultrie Rd | NBOR | medium | verified | Development | Not SilverLeaf — exclude unless CR 210 corridor |
| Pending SilverLeaf items (SJC-SL-20260706-0003, -0005 low) | lightning damage / Bala's opening | silverleaf_discovery | low | pending | Directly SilverLeaf | Need editorial verification of URLs/dates |

**Recommendation:** start from the SilverLeaf-pending low-sensitivity items (verify URLs → mark verified → release) plus 1–3 verified countywide items that materially affect SilverLeaf residents (utility service, access roads). Keep the first release to ~5 items; do not inflate to countywide scale.

## 16. Exclusion categories

- **Not SilverLeaf-relevant** — most BCC agenda items, most NBOR notices, countywide press without SL impact.
- **Unverified / pending** — 78 pending items; no pending item is release-eligible.
- **Duplicate / repeated item_ids** — BCC legacy duplicates (Task 08).
- **Stale** — June items past a sensible freshness window.
- **Incomplete** — legacy records missing source_url/summary (Task 08 flagged 9).
- **Sensitive** — crime/arrest/named-individuals/minors: SJC-SL-20260706-0001/0002/0004, SJC-SJSO-20260603-0004 (verified high), all 8 human-review items by default.
- **Weak attribution** — items whose URLs were never fetch-verified (3 SilverLeaf high-sens candidates).
- **Internal-only / contract failure** — anything without a public-safe projection.

## 17. Buddy/GPT editorial questions

1. **Release size** — approve a ~5-item curated first set vs a larger curated countywide set?
2. **Freshness window** — what publication window (e.g., last 30/60 days) for release eligibility?
3. **Countywide relevance** — may a countywide item appear when it affects SilverLeaf residents (roads/utilities)? Under what rule?
4. **School/road adjacency** — confirm adjacency rules (schools serving SL; access roads CR 210, SR 16, I-95 segments) for inclusion.
5. **Crime/public-safety** — policy for crime items: exclude entirely, or curate verified non-sensitive summaries with explicit approval?
6. **Summary editing** — may editorially reviewed summaries be edited for public release, or verbatim only?
7. **Publication timestamps** — show source date and review date separately (recommended).
8. **Withdrawal** — confirm withdraw/correct procedure (new release vs supersession).
9. **Methodology visibility** — approve methodology/limitations page content.
10. **Source screenshots** — allow screenshots of source pages (yes/no, and whether they are public-safe).
11. **Unresolved gap items** — GAP-001 (BCC June links), GAP-003 (schools), and the 3 SilverLeaf URL-unverified candidates: resolve or exclude. (Note: GAPS.md currently ends at GAP-008; "GAP-009" referenced in the task does not exist — treat the open gaps as GAP-001–008.)
12. **Sensitivity threshold** — confirm that verified medium-sensitivity items require explicit editorial approval to publish.

## 18. SilverLeaf readiness

| Input | Existing | Missing | Launch-required | Deferred |
|-------|----------|---------|-----------------|----------|
| Community record (silverleaf) | `registry/communities.yaml` | — | Yes | — |
| Neighborhoods | `communities.yaml` child records (partial) | Verified SL neighborhoods | Yes (inclusion) | — |
| Aliases | tracked_entities aliases | SilverLeaf + "Silver Leaf" spelling | Yes | — |
| Roads (access + I-95/295 segments) | partial (CR 16A/16A Parkways) | Segment list, entrances, intersections | Yes (adjacency rule) | — |
| Schools | none dedicated | Serving schools (K-8 etc.), boundaries | Yes | — |
| Utilities | none dedicated | Providers serving SL | Yes (relevance) | — |
| Entities | tracked_entities (retail/health) | More SL entities | Yes (filters) | — |
| Interest filters | interest_filters.yaml | SL-specific rules | Yes | — |
| Inclusion rules / relevance fields | none | `silverleaf_relevance` decision field | **Yes (blocker)** | — |
| Exclusions / needs_review | none | exclusion list + needs_review | Yes | — |
| PostGIS / polygons | none | — | No | Deferred |

**Conclusion:** the SilverLeaf scope registry task (§3B-G1) is the single biggest data-side prerequisite for publication; it is medium-sized and requires Buddy's authoritative source list. PostGIS is not required.

## 19. Publication implementation gaps

| Component | Status | Note |
|-----------|--------|------|
| Corpus validator (per-record) | MISSING | `validate.py` validates schemas/registries, not each corpus item |
| Publication selector | MISSING | reviewed-only selector not implemented |
| Publication decision storage | DOCUMENTED ONLY | contract §2 defines semantics; no field/manifest |
| Reviewed-only export | MISSING | |
| Release builder | MISSING | |
| Search index | MISSING | design described (Task 08 §9) |
| Release manifest | MISSING | contract §4 defines shape |
| Rollback | DOCUMENTED ONLY | contract §6 |
| Allowlist/denylist | DOCUMENTED ONLY | contract §4 |
| Deterministic ordering | DOCUMENTED ONLY | contract §4 |
| Tests | MISSING | negative cases listed in contract §5 |

**Smallest coherent task grouping (avoid tiny tasks):**
1. **publication-implementation** (§3A-G2): corpus validator + publication selector + publication-decision storage + allowlist/denylist + tests (one medium task).
2. **silverleaf-scope-registry** (§3B-G1): inclusion/exclusion registry + relevance field (one medium task; Buddy source list).
3. **static-public-export** (§3B-G2): release builder + search index + release manifest + deterministic ordering + rollback + tests (one medium task).
4. **portfolio-integration + UI** (§3C): context packet then UI (after export exists).

## 20. Ivy Control VPS — SJC Onboarding Retrospective and Next-Repository Readiness

### 20.1 Actual SJC onboarding story

local-only repository (Jun–Jul, pre-Ivy) → architecture/product stabilization (Jul, SJC-only) → Ivy portfolio admission (intake 2026-07-28, control record batch) → GitHub readiness (Aug 2 assessment) → GitHub remote + reviewed SHA (Task 11, 2026-08-03) → operational contracts (Task 10/12) → weekly task declaration (Task 14) → transfer/import/receipt model (Task 12/13) → VPS admission preparation (Task 10/12/14) → scheduling model (Task 14) → deployment/shadow-run readiness (this task). Documented: SJC reports 01–15, ROADMAP, docs; Ivy: CONTROL.md, intake, orchestration archives, VPS_ADMISSION_CHECKLIST, hermes-validation-task10.

### 20.2 Missing Ivy updates

- CONTROL.md approved_sha/remote/gate-state (stale since Task 11).
- Gate 2/3 evidence not recorded despite push.
- `RELEASE_GATES.md` never created.
- Backup-disposition gate not yet added (Task 14 patch pending).
- Operational standards discovered in SJC (bundle/import/receipt, weekly contract, task declaration) not yet promoted into Ivy templates (only the bundle-transfer addition landed).
- Decisions that should have triggered Ivy documentation earlier: Mac file-corpus authority, PostgreSQL Option B/DORMANT, static-launch-does-not-need-VPS.

### 20.3 Recommended Ivy authority model

Ivy owns: admission; gate/control records; VPS/DB/runtime standards; task scheduling; backup disposition; resource/capacity; secrets; health; rollback; operational evidence; activation/offboarding. Project owns: implementation tasks/reports; product roadmap; domain behavior; workload code; output contents; tests; editorial review; publication. (ROADMAP §6A now states this.)

### 20.4 Reusable onboarding sequence (see §21).

### 20.5 Reckless Ben preparation (see §22).

### 20.6 Exact Ivy agent handoff (see §23).

## 21. Reusable Ivy onboarding sequence

For the next repository (concise generic sequence):

1. Portfolio-fit decision (PORTFOLIO_INTENT) → 2. repository-control record (CONTROL.md) → 3. public-readiness preflight (hygiene/secret/large-file scan, automated) → 4. GitHub publication (single gate: hygiene + reviewed SHA + push) → 5. data-authority declaration (Mac vs VPS authority) → 6. VPS storage declaration (what stays vs transfers) → 7. PostgreSQL disposition (one of NOT_USED/DORMANT/OPERATIONAL_METADATA/…) → 8. backup disposition (scope → first backup → checksum → restore path → restore test) → 9. task declaration (repo manifest, disabled) → 10. deployment manifest (exact SHA, service account, env) → 11. exact-SHA deployment → 12. shadow run (manual) → 13. near-future timer proof → 14. transfer/import/receipt/prune proof → 15. natural run → 16. activation (Buddy + healthy window) → 17. health/review cadence → 18. offboarding (documented removal).

Each step names owner (project/Ivy), evidence, and gate-vs-checklist classification. Reuse directly from SJC: bundle/import/receipt contract, task-declaration shape, deterministic-runner pattern, minutes-from-now test packet, backup-policy shape. Project-specific: domain registries, extractors, taxonomy, editorial rules, UI.

## 22. Reckless Ben pre-onboarding checklist

Before onboarding work begins, establish (placeholders marked `[TBD]`):

- Repo location: `[TBD]` (Ivy CONTROL.md exists under `repos/reckless-ben/`).
- Purpose: `[TBD]`.
- Public/private target: `[TBD]`.
- Git status / remote: `[TBD]` (clean? remote configured?).
- Data classes: enumerate durable vs ephemeral.
- Durable authority: Mac file? VPS? database?
- Runtime: none / script / service; language/deps.
- Network needs: public HTTP only? any credentialed endpoint?
- Secrets: names only.
- Database role: NOT_USED / DORMANT / OPERATIONAL_METADATA / ….
- VPS role: none / bounded collection / UI-serving.
- UI-serving needs: static only? data volumes?
- Backup disposition: define scope + restore path before any VPS production status.
- Scheduling: does it need recurring tasks? timer? deterministic or agentic?
- Health: producer? contract conformance.
- Rollback: exact-SHA + artifact replay.
- Publication target: portfolio site? separate?
- Reuse from SJC (generic): bundle/import/receipt contract, task-declaration format, deterministic-runner pattern, minutes-from-now test packet, backup-policy shape, Ivy gate/checklist templates.
- Keep project-specific: domain registries, extractors, taxonomy, editorial rules, UI, any credentialed sources.

## 23. Exact Ivy-agent handoff

Proposed task packet outline for an Ivy-focused agent (do not modify Ivy in this session):

- **Inspect:** `repos/sjc-intel/CONTROL.md`, `docs/REPOSITORY_CONTROL_MODEL.md`, `docs/VPS_ADMISSION_CHECKLIST.md`, `docs/PORTFOLIO_CONVENTIONS.md`, `docs/PORTFOLIO_INTENT.md`, `docs/DATA_LIFECYCLE_STANDARD.md`, `docs/BACKUP_MANIFEST_STANDARD.md`, `docs/HEALTH_CONTRACT.md`, `_internal/orchestration/repos/sjc-intel/`, `_internal/outbox/runs/2026-08-03-sjc-codex-followup/`.
- **Update:** `repos/sjc-intel/CONTROL.md` (remote, approved SHA `1be2ade` or latest approved, gate table → reconcile to §6/§20.3), create `repos/sjc-intel/RELEASE_GATES.md` (Gate 1 PASSED_NOT_RECORDED, Gate 2/3 PARTIAL/PASSED_NOT_RECORDED, Gate 4/5 NOT_STARTED).
- **Checklist changes:** add backup-disposition item 11 (report 14 §12 patch); add "request gate update" step to task/report template.
- **Templates to create:** exact-SHA pin template; proof-run/natural-run evidence card; offboarding template.
- **Helpers to consider:** automated secret/large-file hygiene scan; a "gate status" diff helper to detect CONTROL.md staleness.
- **Duplicated docs to consolidate:** next-task state (ROADMAP/BACKLOG/CONTROL.md continuity) → single pointer; SJC-vs-ivy-control-vs-ivy-control standards mapping.
- **Validation:** Ivy `git diff --check`; parse CONTROL.md front-matter; re-run SJC validations after any cross-repo evidence handoff.
- **Live verification:** refresh VPS capacity via approved Mode 2 (83% disk/reboot pending) before any deployment decision.
- **Buddy decisions:** activate backup-disposition gate; approve CONTROL.md reconcile; approve publishing language.
- **Strong Codex gates:** VPS admission packet, live-storage audit (§26), any cross-repo security/privacy decision.

## 24. VPS storage and retention assessment

Governing model: VPS = ingestion, bounded processing, temporary bundles, health, scheduler state, minimal UI-serving data; Mac = full corpus, review state, history, release generation, archive, restore authority.

| Artifact | VPS treatment | Mac treatment |
|----------|---------------|---------------|
| Raw captures (HTML/XML) | Temporary; bounded raw window (per retention.md); prune after verified receipt | Fixtures only; corpus stores excerpts not raws |
| Source events / candidates / proposals | Immediate transfer via bundle; retain until receipt + retention | Import to incoming; accept to corpus |
| Logs | Bounded journal (e.g., 7 days) + run.log in bundle | Run logs (curated) |
| Manifests / checksums | Bounded retention until prune | Durable in incoming + receipts |
| Receipts / acknowledgements | Retain ack copy until prune; never prune before verified receipt | Durable `data/receipts/` |
| Health | Bounded operational history | Durable evidence |
| Review queue / corpus | **Never VPS** | Durable authority |
| Release files / search index | **Never VPS** (static host) | Generated + deployed to static host |
| Current summaries / metrics | Bounded snapshot | Durable snapshots |
| Historical published items | **Never VPS** | Static release history |
| Database state | None (DORMANT_FUTURE_READY); Option B metadata later | N/A |

Compression: raw captures gzip; old bundles tar+gzip; text corpus already tiny. Prune-after-receipt + retention-deadline rules apply (weekly contract §7.7). Regenerate: derived indexes/summaries.

## 25. Minimum SJC UI-serving state

**Recommendation: no SJC UI data on the VPS for launch.** The static release + search index live on the portfolio static host (generated on the Mac), and the VPS holds only temporary run bundles/health. This satisfies "useful even when the VPS is unavailable." A later, separately approved option is a bounded release-history cache on the VPS or Option-B operational metadata; neither is a launch dependency. The UI reads the latest static release + search index only.

## 26. Strong Codex storage-audit packet

Bounded task outline (do not execute here): live disk audit (`df -h`, `du` per workload) via approved Mode 2; per-workload footprints (WGU-Reddit, backup, Launchpad, Chrome/collector, browser caches, journals); safe-cleanup candidate list with dry-run; retention conformance vs `DATA_LIFECYCLE_STANDARD` thresholds; per-repo budget declarations; UI-data declarations; capacity thresholds; journal growth; browser/cache cleanup; PostgreSQL disk (if any); old release retention; deployment/rollback evidence; capacity re-verification after the pending reboot. Output: dated evidence card + cleanup packet for Buddy gate.

## 27. Hermes and scheduling readiness

- **Hermes (VPS resident assistant):** read-only; provider auth not configured; coordinates/verifies only.
- **Deterministic scheduled execution:** `run_weekly.py` under a systemd service + timer (disabled). This is **not** "Hermes execution" — do not conflate the deterministic runner with the Hermes assistant.
- **Agentic discovery:** bounded, candidate-only, manually triggered; not scheduled.
- **Project task declaration:** `deploy/sjc-weekly-task.yaml` (disabled).
- **Ivy scheduler authority:** owns units/timer/enablement/schedule/env/limits/health/rollback.
- **Systemd readiness:** inert templates exist; service/timer names standardized; lock + run-id prevention designed.
- **Provider authentication:** not configured; not required for Stage A.
- **Near-future test:** packet in `docs/weekly_scheduling.md` §5 (systemd-run one-shot).
- **Weekly activation:** gated on §3E-G2 (4 shadow runs) + §3F (7-day window) + Buddy.

## 28. Backup deferral status

- SJC requirements: documented (`docs/backup-restore.md` §0; restore objectives §0.4).
- External destination: **deferred** (Buddy choice; provider-neutral).
- Automation: **deferred** (portfolio-wide).
- Ivy generic requirement: **pending** (Task 14 patch not applied).
- Static publication: **not blocked** (backup is not a launch gate).
- VPS production activation: **does require an explicit backup disposition or Buddy-approved exception** before production workload status — record the deferral in Ivy CONTROL.md `data_locations.backup` + the admission checklist item 11 once applied.

## 29. SJC files changed

Approved changes only:
- `LICENSE` — **added** (MIT, Copyright (c) 2026 wguDataNinja, identical to origin/main).
- `README.md` — license section now references LICENSE.
- `docs/postgresql_adapter.md` — mode labeled `DORMANT_FUTURE_READY`; no-corpus-authority + no-launch-dependency notes.
- `docs/backup-restore.md` — deferral note (destination/automation deferred to shared Ivy policy).
- `ROADMAP.md` — added §6A ownership boundary (SJC vs Ivy).

No review/publication decision was altered; no item was marked published; no UI, deploy, credentials, timers, or Ivy changes.

## 30. Validation results

```
SJC:
python3 -m pytest tests/ -v            → PASS, 140 passed
python3 scripts/validate.py            → PASS — ALL PASSED
python3 scripts/portability_check.py   → PASS
git diff --check                       → clean
git status --short                     → intended changes + pre-existing dirty files
git branch --show-current              → master
git remote -v                          → origin https://github.com/wguDataNinja/sjc-intel.git

Ivy (read-only):
git -C ivy-control-vps status --short  → 17 pre-existing lines; untouched
git -C ivy-control-vps branch --show-current → main
git -C ivy-control-vps log -n 10 --oneline → 3e94197…412082b (inspected)
git -C ivy-control-vps diff --check    → clean (pre-existing tree)
```

## 31. Remaining medium-agent tasks

| Task | Dependency | Outcome | Publication blocker? | Report |
|------|-----------|---------|----------------------|--------|
| publication-implementation (§3A-G2) | none | validator + selector + decision storage + tests | **Yes** | reports/16-… |
| silverleaf-scope-registry (§3B-G1) | Buddy source list | inclusion/exclusion registry + relevance field | **Yes** | reports/17-… |
| static-public-export (§3B-G2) | §3A-G2 + §3B-G1 | release.json + search index + manifest + rollback | **Yes** | reports/18-… |
| portfolio-integration (§3C-G1) | §3B-G2 + site authority | target-repo context packet | Yes (deploy route) | reports/19-… |
| static SilverLeaf UI (§3C-G2) | §3C-G1 | pages/search/filters | Yes | reports/20-… |
| extract-bcc-workspace-mode | none | BCC workspace-safe | No | reports/… |
| public presentation polish | after first release | screenshots/diagram/privacy note | No | reports/… |

## 32. Remaining Buddy/GPT decisions

Editorial review of the 78 pending items; first-release set approval (§17); sensitivity/summary/date/freshness policies; SilverLeaf authority source list; portfolio-site deploy route; launch approval; backup destination (deferred but eventually needed); publish language/claims review; MIT holder confirmation (uses wguDataNinja per origin/main).

## 33. Remaining Ivy tasks

Reconcile SJC CONTROL.md + create RELEASE_GATES.md; apply backup-disposition gate (report 14 §12); update reusable onboarding docs + templates (report 15 §20–23); promote SJC bundle/import/receipt and task-declaration patterns into Ivy templates; prepare Reckless Ben onboarding checklist (§22); define offboarding; add "request gate update" step; consolidate duplicated next-task state.

## 34. Remaining privileged actions

Refresh VPS capacity (Mode 2) after reboot; deploy approved exact SHA; install `sjc-intel-weekly.service` + `.timer` (disabled); run the minutes-from-now test; four shadow runs; transfer/import/receipt/prune proof; health registration; rollback rehearsal; §3F activation; apply the Ivy storage audit (§26). Static publication needs no VPS.

## 35. Risks and unresolved issues

- **Editorial backlog (78 pending)** is the real launch gate; it is human effort, not code.
- **Crime/safety items** (verified high-sens SJSO + 3 SilverLeaf high-sens pending) must be excluded or explicitly approved — a public-reputation risk if mishandled.
- **SilverLeaf relevance determination** is currently weak in data (no decision field); the §3B-G1 registry must make inclusion reproducible.
- **Stale Ivy CONTROL.md** could mislead the next operator; reconcile before any deployment claim.
- **Capacity evidence self-reported** (83% disk, reboot pending) must be refreshed before VPS activation.
- **GAPS.md ends at GAP-008** (the task referenced "GAP-009"; no such record exists — treat open gaps as GAP-001–008).
- **Internal docs (`README_INTERNAL.md`, AGENTS.md) remain tracked in a public repo**; decide whether to keep internal or move to a private structure before final public presentation.
- **Portfolio-site technology unknown** from this repo; §3C-G1 must discover it before UI work.

## 36. Final Git status

SJC `master` @ `1be2ade`, origin/master == local. Working tree: intended Task 15 changes (LICENSE, README, postgresql_adapter, backup-restore, ROADMAP) + pre-existing dirty data files + Tasks 12–14 outputs. Nothing staged/committed/pushed. Ivy untouched (read-only).

## 37. Final task status

| Area | Status |
|------|--------|
| Publication decision packet | COMPLETE |
| First-release candidate pool + exclusions | COMPLETE (recommendation) |
| Publication blockers | COMPLETE (exact) |
| Work-history reconstruction | COMPLETE |
| Missed/stale Ivy gate records | COMPLETE (identified) |
| Ownership boundary | COMPLETE (ROADMAP §6A) |
| Ivy gate/checklist evaluation | COMPLETE |
| Reusable onboarding sequence | COMPLETE |
| Reckless Ben checklist | COMPLETE |
| Ivy agent handoff | COMPLETE |
| VPS storage rules + UI-serving state | COMPLETE |
| Strong Codex storage-audit packet | COMPLETE |
| Backup deferral | COMPLETE (documented) |
| PostgreSQL disposition | COMPLETE (DORMANT_FUTURE_READY) |
| MIT license + doc clarifications | COMPLETE |
| Publication pipeline (§3A-G2/§3B) | READY_FOR_MEDIUM_AGENT |
| Editorial review + release approval | AWAITING BUDDY |
| VPS deployment/shadow run | BLOCKED (privileged) |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP — the decision packet, reconstruction, ownership model, and reusable onboarding plan are complete and validated; the remaining publication work is exact medium-agent tasks plus Buddy editorial decisions and privileged Ivy/VPS actions, with no further broad SJC architectural discovery required.
