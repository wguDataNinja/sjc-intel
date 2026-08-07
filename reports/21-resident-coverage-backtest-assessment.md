# Task 21 — Resident Coverage Strategy and Historical Backtest Assessment

**Task identity:** 21-resident-coverage-backtest-assessment.md
**Date:** 2026-08-04
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Final status:** COMPLETE

**Read-only scope honored:** no full backtest run, no publication/review state
changed, no source records altered, no taxonomy changes, no promotions, no
commit/push, no Ivy/VPS/PostgreSQL activation. Two read-only live source checks
performed (recorded in §18/§28).

---

## 1. Executive result

**The repository already contained the beginnings of an adaptive resident-led
discovery system — and most of it was designed, partially built, and then
stopped.** The backtest is not a green-field build; it is completing an
architecture that was substantially specified on 2026-07-06 and abandoned at
the "designed but not orchestrated" stage.

The strongest evidence:

1. **A complete adaptive-search design already exists.** `docs/reviews/SJC_SCHEMA_FIT_AND_SEARCH_DISCOVERY_DESIGN_20260706.md`
   specifies entities, aliases, events (merged with milestones), temporal
   assertions, relationships, search runs, and search candidates; 15 search
   templates including **milestone monitoring** (`project_milestone`),
   **delay detection** (`delay_check`), **stale-temporal follow-up**
   (`stale_temporal`), and entity-triggered recurring searches — the exact
   "recurring targeted searches for important subjects" behavior this task
   proposes.
2. **The prompt-led discovery architecture was designed** (`docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md`)
   with recurring-discovery and evidence-triggered-investigation prompts,
   structured search-run records, and a staged implementation sequence — then
   only the first prompt was built and piloted once.
3. **Most registries already exist**: `tracked_entities.yaml` (15 entities with
   aliases + lifecycle + search queries), `search_profiles.yaml` (7 profiles),
   `search_terms.yaml` (52 terms), `source_candidates.yaml` (46 candidates),
   `interest_filters.yaml` (10). The **adaptive loop that consumes them does
   not exist.**
4. **The workflow stops after entity creation.** The single most damaging
   demonstration: the SilverLeaf K-8 (School QQ) was tracked, but when it was
   officially named **Magnolia Oaks Academy** and **opened July 22, 2026**, the
   repository never captured either event — the name exists only in a planning
   doc (with an incorrect `type: private` flag) and the opening is entirely
   absent from the corpus (§10).
5. **No historical simulation exists**, and the corpus's reconstructability is
   **PARTIAL**: item-level timestamps are reliable, but entity/profile/alias
   creation dates are only inferable from Git history and `last_checked`
   fields.

**Bottom line for Buddy/GPT:** dispatch Strong Codex to complete the
already-specified adaptive discovery loop as a **file-backed, historically
isolated simulation**, with a Resident Coverage Strategist role, promotion
review, weekly state, and a hidden-corpus evaluator. The existing weekly runner
and registries are reusable; the missing pieces are search orchestration, a
historical clock, isolated state, proposal/acceptance state, timeline
reconciliation, and the evaluation harness.

## 2. Starting repository state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `9c985c7` (local == origin) |
| Working tree | Clean except `reports/20-expanded-corpus-editorial-review.md` (untracked, prior task) |
| Tests | 217 passed |
| Validators | `validate.py` ALL PASSED; corpus 0 errors / 321 warnings; scope PASS; portability PASS |
| Corpus | 231 unique items (May 2025 – Aug 2026), 83 verified / 133 pending / 4 archived / 1 duplicate / 1 rejected / 9 CDD legacy |
| Publication decisions | 4 (current release) |

## 3. Documents, tasks, reports, and history inspected

Read/verified: README.md, README_INTERNAL.md, AGENTS.md, ROADMAP.md,
BACKLOG.md, VPS_ROADMAP.md, docs/VPS_CONTINUITY.md, docs/ARCHITECTURE.md,
docs/cadence.md, docs/discovery_loops.md, docs/operator_mode.md,
docs/data_model.md, docs/taxonomy.md, docs/news_ingestion_readiness.md,
docs/deep_research_ingestion.md, docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md,
docs/planning/SJC_PROMPT_LED_DISCOVERY_STANDARDS_20260706.md,
docs/reviews/SJC_SCHEMA_FIT_AND_SEARCH_DISCOVERY_DESIGN_20260706.md,
docs/reviews/SJC_KNOWLEDGE_BASE_CROSS_PROJECT_COMPARISON_20260706.md,
docs/reviews/SJC_ACTUAL_DATA_EVIDENCE_PACKET_20260706.md, tasks/README.md,
reports/README.md, tasks 01–20 and reports 01–20 (incl. report 20 in full),
logs/agents/, logs/runs/, prompts/ (all 13), `.opencode/agents/*` (both),
`agents/resident-interest-classifier.md`, all registries + schemas,
`data/monthly/*` (incl. crosscut + wraps), `data/search_runs/`,
`data/source_events/`, `deploy/sjc-weekly-task.yaml`, and the Git history.

## 4. Original discovery architecture

`docs/discovery_loops.md` defines six loops — A known-source monitoring, B
search discovery (incl. a local-media sub-loop), C historical backfill, D
cross-section/beat, E taxonomy, F review — explicitly rejecting a single linear
pipeline. Status per that doc and current evidence:

| Loop | Designed | Piloted | Automated | Current evidence |
|------|----------|---------|-----------|------------------|
| A monitoring | Yes | Yes (county, sheriff, NBOR, utility, BCC) | Partial (`extract_nbor.py`, `extract_bcc_agenda.py`, `run_weekly.py` bundle foundation) | extractors + weekly runner + source_events |
| B search discovery | Yes | Yes (one SilverLeaf run 2026-07-06) | No | `agentic_silverleaf_discovery.md`, `data/search_runs/2026-07-06/`, `silverleaf_search_discovery_task.md` |
| C backfill | Yes | Yes (May 2026; Aug–Sep 2025) | No | `data/monthly/` |
| D cross-section/beat | Yes | No | No | `beat_candidates.yaml` is **empty** |
| E taxonomy | Yes | Partial (cdd_governance, water_restrictions, budget_millage promoted) | No | `docs/taxonomy.md` |
| F review | Yes | Yes (review queue + publication decisions) | Yes (tooling) | queue, decisions, static release |

## 5. Previously intended resident-led behavior

Classification of every adaptive concept from the task's list:

| Concept | Classification | Evidence |
|---------|----------------|----------|
| Discovery loops not linear pipeline | **INTENDED_AND_IMPLEMENTED** (docs) | `docs/discovery_loops.md` |
| Search discovery | **PILOTED** (once) | `data/search_runs/2026-07-06/`, `prompts/agentic_silverleaf_discovery.md` |
| Search terms as data | **INTENDED_AND_IMPLEMENTED** | `registry/search_terms.yaml` (52) |
| Tracked entities | **INTENDED_AND_IMPLEMENTED** | `registry/tracked_entities.yaml` (15) |
| Entity aliases | **INTENDED_AND_IMPLEMENTED** (partial) | aliases fields on entities; **missing Magnolia Oaks** |
| Entity-to-item matching | **INTENDED_AND_IMPLEMENTED** | `data_model.md`, review-queue builder (ENT-002) |
| Source-watch gap detection | **INTENDED_AND_PARTIAL** | `sjc-intel-source-watch` agent exists; no scheduled gap report |
| Resident-interest classification | **INTENDED_AND_IMPLEMENTED** | `resident-interest-classifier` agent + prompt + pipeline fields |
| Resident-oriented search profiles | **INTENDED_AND_IMPLEMENTED** | `registry/search_profiles.yaml` (7) |
| Agentic investigation | **DOCUMENTED_ONLY** | design in product-direction + prompt-led standards; `agentic_investigation.md` prompt **never created** |
| Source proposals | **INTENDED_AND_PARTIAL** | `schemas/source_proposal.schema.yaml`, bundle `source_proposals/`, `review_source_proposals.py`; not an adaptive loop |
| Source promotion | **INTENDED_AND_IMPLEMENTED** | Tier 1/2 promotions (Task 12-era) |
| Recurring targeted search | **PILOTED** | one run; profile `sl_core` designed weekly |
| Historical backfill | **INTENDED_AND_IMPLEMENTED** | May 2026 + Aug–Sep 2025 |
| Timeline / durable memory | **DOCUMENTED_ONLY** | entity/event/temporal schema design; no file-backed timeline state |
| Milestone monitoring | **DOCUMENTED_ONLY** | `project_milestone`/`delay_check`/`stale_temporal` search templates designed, never run |
| Coverage expansion | **PILOTED** | source-candidate review + SilverLeaf discovery |
| Weekly cadence | **INTENDED_AND_IMPLEMENTED** | `docs/cadence.md`, `run_weekly.py`, LAST_RUN markers |
| Reports / review gates | **INTENDED_AND_IMPLEMENTED** | run logs, agent logs, monthly wraps, task/report flow |

**Absent entirely (MISSING):** a Resident Coverage Strategist, promotion-review
state, weekly-adaptive state, milestone expectation records, and any historical
simulation/backtest.

## 6. Existing implementations

- Deterministic monitoring: `extract_nbor.py`, `extract_bcc_agenda.py`,
  `run_weekly.py` (workspace + bundle), source events.
- Corpus + review: intel items, dedupe index, review queue builder (entity
  matching), `batch_review.py`, `update_review_status.py`.
- Publication: decision registry + tool, corpus validator, selector, static
  export, SilverLeaf Brief site.
- Registries: sources (28 canonical), source_candidates (46), search_terms
  (52), search_profiles (7), tracked_entities (15), interest_filters (10),
  communities, silverleaf_scope.
- Agentic discovery: one search run (2026-07-06) → `agentic_search_results.yaml`,
  candidates absorbed into the review queue (Task 02), 5 SilverLeaf items.
- RI classification: applied in NBOR + utility extraction.
- Source proposal review: `review_source_proposals.py` (PROP-public_safety-0001
  proof).

## 7. Partial implementations

| Component | What exists | What's missing |
|-----------|-------------|----------------|
| Search orchestration | Prompt + one manual run + profile registry | No runner, no provider abstraction, no cadence `is_due()`, no budgets enforced, no `search_runs` state beyond one file |
| Entity/alias/event/temporal/relationship | Full PG schema design; `tracked_entities.yaml` subset | No file-backed entities/events/temporal assertions/relationships; no timeline reconciliation |
| Source promotion | candidates + review tool | No promotion criteria rules, no per-source gap feedback loop |
| Milestone monitoring | search-template designs | No milestone expectation records, no triggers, no delay/stale detection |
| Beat/cross-section | `docs/discovery_loops.md` Loop D + `beat_candidates.yaml` | **`beat_candidates.yaml` is empty** — Loop D never ran; no lane state |
| Taxonomy loop | `taxonomy_gap` field + manual promotions | No collection/processing loop |
| Agentic investigation | Design docs | `prompts/agentic_investigation.md` never created; no trigger records |
| Weekly ops | bundle/import/receipt foundation | No Stage B (bounded discovery) execution; only Stage A monitor |

## 8. Superseded or conflicting designs

- **`VPS_ROADMAP.md`** (single-lane, VPS-centric) was **superseded** by the
  2026-07-06 three-lane product direction; ROADMAP.md §3 now owns sequencing.
- **`reports/08`/`09`** (Codex redesign) **re-scoped** the roadmap: static
  reviewed-only release first, agentic discovery deferred as a bounded manual
  task; this is consistent with the current direction, not conflicting.
- **PostgreSQL schema design** (9 tables, 2026-07-06) was **designed but never
  activated** — `docs/postgresql_adapter.md` marks it
  DORMANT_FUTURE_READY. The file-backed corpus remains authoritative. This is
  the single largest "designed but not built" artifact and the natural
  substrate for the entity/event/temporal state the backtest needs.
- **`beat_candidates.yaml`** contains an empty list despite Loop D's design —
  a **partially-abandoned** component.
- No other agent/prompt overlaps were found; the architect, source-watch, RI
  classifier, and Hermes roles have distinct ownership (§12).

## 9. Where the current workflow stops

The pipeline reliably performs **capture → classify → review → (recently)
publish**. It stops at the boundary of **persistent subject management**:

1. An important subject is captured (e.g., School QQ topping-out).
2. Someone manually creates a tracked entity + profile.
3. **No recurring search runs.** `sl_core` is `cadence: weekly` but nothing
   executes it; the sole search run was manual (2026-07-06).
4. **No milestone expectations** are recorded (expected opening Aug 2026 was
   never stored as a temporal assertion).
5. **No naming/alias reconciliation** — when the school became Magnolia Oaks
   Academy, nothing updated the entity.
6. **No "overdue/opening-approaching" triggers** — the July 22, 2026 opening
   was missed entirely.
7. **No timeline reconciliation** — CR 2209 has 2 records, SR 207 WRF has 2,
   the water shortage has 3, K-8 has 3; none are linked into a timeline.
8. **Source-gap feedback** is manual and episodic (monthly wraps), not a loop.

Handoff failures: **Loop B → entity creation** works once; **entity → recurring
search** never closes; **search → proposal review** has no promotion state;
**milestone → follow-up search** does not exist.

## 10. Magnolia Oaks Academy case study

Traced end-to-end with one live source check (2026-08-04):

| Step | Evidence in repo | Date known | Status |
|------|------------------|------------|--------|
| School QQ discovered | SJC-SL-20260704-0002 (topping-out, 190k sq ft, 73 rooms) | article 2025-05-07 (captured retroactively 2026-07-04) | ✅ captured |
| Tracked as entity | ENT-EDU-SILVERLEAF-K8 (aliases: "SilverLeaf K-8", "SilverLeaf school", "SilverLeaf K-8 school QQ") | 2026-07-04 | ✅ captured |
| Naming engagement | SJC-BF-202509-0008 (School QQ/RR naming + mascot meetings) | 2025-09-25 (backfilled 2026-06-26) | ✅ captured |
| Construction update | SJC-BF-202509-0006 (QQ/RR under construction) | 2025-09-15 | ✅ captured |
| **Official name: Magnolia Oaks Academy** | `docs/planning/SJC_DIRECTION_RECONCILIATION_20260706.md` (name present, **`type: private`** — a data-quality error) | 2026-07-06 | ⚠️ known in one doc, **never added as an entity alias, never an intel item** |
| **Opening** | **SJCSD live: "St. Johns County School District Opens First School in Silverleaf Community" — July 22, 2026** | 2026-07-22 | ❌ **not in corpus** (newest school item is Sep 2025) |
| School microsite | Magnolia Oaks Academy listed in the live SJCSD school directory | live | ❌ not tracked |

**Result:** a resident could open the current SilverLeaf Brief and find no
school information at all — the single most important neighborhood story was
missed ~2 weeks before "now." The alias-reconciliation and milestone-trigger
gaps are the systemic causes, not an individual miss.

## 11. Construction and growth case studies

| Subject | First known | Entity? | Aliases? | Recurring search? | Milestones? | Follow-ups? | Timeline? | Current gap |
|---------|-------------|---------|----------|-------------------|-------------|-------------|-----------|-------------|
| CR 2209 connector | 2025-08-20 (county) / opened 2025-10-28 | ✅ ENT-ROAD-CR-2209-CONNECTOR | ✅ | ❌ | partial (opened) | ❌ 2026 status unknown | ❌ | no 2026 status, no timeline |
| First Coast Expressway / CR 16A | 2026-07-20 (CR 16A closures) | ❌ | ❌ | ❌ | ❌ | partial (closure dates) | ❌ | no FCE project tracking |
| Baptist SilverLeaf campus | registry only | ✅ ENT-HEALTH-BAPTIST-SILVERLEAF | ✅ | ❌ | ❌ | ❌ | ❌ | **no items at all** |
| Mega Publix | 2026-03-26 | ✅ ENT-RETAIL-PUBLIX-SILVERLEAF | ✅ | ❌ | opened | ❌ | ❌ | opening captured once, no follow-up |
| Harris Teeter | 2025-12-02 | ✅ ENT-RETAIL-HARRIS-TEETER-SILVERLEAF | ✅ | ❌ | proposal | ❌ | ❌ | status unknown since Dec 2025 |
| Silverleaf Commons | registry only | ✅ ENT-RETAIL-SILVERLEAF-COMMONS | ✅ | ❌ | ❌ | ❌ | ❌ | no items |
| Beach Valley Mini Golf | 2026-04-08 | ✅ ENT-REC-BEACH-VALLEY-MINI-GOLF | ✅ | ❌ | proposal | ❌ | ❌ | status unknown |
| SR 207 WRF | 2025-12-19 | ✅ ENT-INFRA-SR-207-WRF | ✅ | ❌ | approved→operational | ⚠️ 2 records | ❌ | no construction-start, no timeline |
| Phase III water | 2026-05-11 | ❌ (no entity) | ❌ | ❌ | ongoing | ⚠️ multiple | ❌ | active, no end date |
| SR 16 / CR 210 corridors | 2025-08 | ❌ | ❌ | ❌ | partial | ❌ | ❌ | no 2026 status |

**Systemic failure pattern:** capture happens; **persistent follow-through does
not.** Every subject above stalls at "entity created, then nothing runs."

## 12. Existing agent responsibility map

| Role | Type | Loop | Responsibilities | Gap for strategist |
|------|------|------|------------------|--------------------|
| `sjc-intel-architect` | Interactive OpenCode | all | Architecture, workflows, schemas, registries, promotion review, editorial | Overloaded; no dedicated coverage-planning pass |
| `sjc-intel-source-watch` | Interactive OpenCode | B | Source health, source discovery, gap tracking | Sources only; not subject/entity coverage |
| `resident-interest-classifier` | Role + prompt | A/B/C | Adds resident lens to individual items | Item-level; not subject-level |
| `search-discovery-worker` (Hermes) | Prompt | B | Runs term lists, returns candidates | One-shot; no state, no promotion judgment |
| `silverleaf-discovery-worker` | Prompt | B | Recurring SilverLeaf search | Candidates only; no strategist layer |

No existing role **reviews accumulated findings and gaps, proposes persistent
tracked subjects, and prepares promotion packets** — the missing responsibility.

## 13. Resident Coverage Strategist recommendation

**Recommendation: a new interactive OpenCode agent (`sjc-intel-coverage-strategist`)
with a deterministic-rules pre-pass, backed by a reusable role prompt for
weekly Hermes execution.**

- Why not just expand the architect: the architect is already overloaded with
  architecture + editorial + orchestration; coverage planning is a distinct,
  recurring, reviewable function.
- Why not just expand source-watch: source-watch is source-centric (Loop B);
  the strategist is subject/entity/lane-centric (a new Loop G).
- Why not a pure Hermes worker: promotion proposals need resident judgment and
  cross-subject synthesis; the strategist should **propose**, with Buddy/architect
  **accept** (matches the no-auto-canonical-promotion rule).
- Design: **deterministic rules pass** (thresholds on §14 signals → candidate
  subjects) **plus agent synthesis** (strategist writes the promotion packet) —
  a combination, with a weekly cadence and a monthly synthesis.

## 14. Subject-promotion model

Promotion targets (all existing or proposed file-backed types): `tracked
entity`, `tracked project`, `tracked place/corridor`, `tracked facility`,
`tracked business`, `tracked development`, `coverage lane`, `search profile`,
`source investigation`, `milestone plan`.

Evidence-based signals (weighted; a subject advances when it meets ≥2 weighted
signals or 1 dominant signal + resident impact):

1. Direct SilverLeaf relevance (scope registry).
2. Repeated mentions across sources/weeks (≥2 items or ≥2 sources).
3. Large resident impact (household-facing: schools, roads, utilities, taxes).
4. Long expected duration (months-years).
5. Multiple future milestones (approval → groundbreaking → opening).
6. New facility or infrastructure.
7. Major traffic/commute implications.
8. School or healthcare impact.
9. Significant commercial center.
10. Unresolved resident questions (temporal gaps, pending approvals).
11. Multiple sources (official + media corroboration).
12. Strong official-source evidence.

Thresholds: a **proposal** is produced when score ≥ threshold; **acceptance**
always requires Buddy/architect approval — no automatic canonical promotion.
Proposals carry evidence, expected benefit, and cost/budget (§29).

## 15. Adaptive weekly state

Persist (extending existing files, not new parallel registries):

| State | Location (recommended) |
|-------|------------------------|
| Known sources + status | `registry/sources.yaml` (extend with `last_checked`) |
| Entities + aliases + lifecycle | `registry/tracked_entities.yaml` (extend with `first_known_at`, `milestones`) |
| Search profiles + cadence | `registry/search_profiles.yaml` (extend with `last_run_at`) |
| Active search terms + effectiveness | `registry/search_terms.yaml` (extend with last-run/result metadata) |
| Expected milestones + temporal assertions | **new** `data/coverage/milestones.yaml` (or a `temporal_assertions.yaml`) |
| Unresolved gaps + latest known state + timeline events | **new** `data/coverage/subjects.yaml` (subject timeline state) |
| Source candidates + proposal status + rejected proposals | `registry/source_candidates.yaml` + **new** `data/coverage/proposals.yaml` |
| Search budgets + resident priority + confidence + review owner | `data/coverage/state.yaml` |

Files that can be extended: `sources.yaml`, `tracked_entities.yaml`,
`search_profiles.yaml`, `search_terms.yaml`, `source_candidates.yaml`. Files
that must be **new**: `data/coverage/` (weekly state, milestones, proposals,
timeline reconciliation). The PG 9-table schema (§7) is the target if/when a
relational store is activated — do not build a parallel relational store now.

## 16. Coverage-lane model

**Recommend `growth_and_construction` as a first-class resident coverage lane**
(transportation infrastructure, schools, healthcare, shopping centers, major
retail, major residential phases, growth utilities, recreation, new public
facilities). It is partially supported today (taxonomy topics development/
infrastructure; beats in `docs/taxonomy.md`; a few search profiles) but has no
owning state.

Recommended mapping (avoid uncontrolled taxonomy expansion):
- **Lane** = editorial/coverage concept owned by the strategist (`data/coverage/lanes.yaml`).
- **Beat** = existing taxonomy grouping (already present).
- **Search-profile family** = one profile per lane with `profile_defaults`.
- **Project/entity class** = `entity_type` on tracked entities.
- Ownership: strategist proposes lane membership; architect approves; no new
  taxonomy topics needed for lanes (reuse existing topics).

Full lane set to seed: schools & family; roads & mobility; utilities &
household operations; **growth & construction**; community services & amenities;
government decisions; preparedness.

## 17. Historical knowledge reconstructability

| State class | Best evidence | Availability |
|-------------|---------------|--------------|
| Source discovered | Git history + `discovered_at` on sources | **RELIABLE** |
| Source promoted | Git history + promotion reports | **RELIABLE** |
| Item observed | `discovered_at` / `source_published_at` | **RELIABLE** |
| Entity created | Git history of `tracked_entities.yaml` (commit date); `tracked_since` field | **PARTIAL** (records intent, not knowledge) |
| Alias added | Git history | **PARTIAL** |
| Search profile created | Git history; `search_profiles.yaml` header date | **PARTIAL** |
| Task executed | task/report timestamps | **RELIABLE** |
| Report produced | file date + generated_at | **RELIABLE** |
| Milestone inferred | only in design docs (none recorded) | **UNAVAILABLE** |
| Source candidate recorded | Git history of `source_candidates.yaml` | **PARTIAL** |

**Conservative rule (adopt):** a knowledge item is only "available at time T"
if its first defensible evidence date ≤ T. Where provenance cannot be defended
(date missing, `last_checked` only, or retroactive capture), the item must not
be exposed until its first evidenced date. **Corpus-wide implication:** many
2026-06-26/07-04 items carry `observed` dates from the capture, not the source
date; the backtest must use `source_published_at` for availability and treat
the *capture* date as the "discovery simulation would have found it by" bound.

## 18. Future-data leakage risks and controls

Leakage vectors (all confirmed present): current `tracked_entities.yaml`
aliases and lifecycle (future-known), current `search_profiles.yaml`,
the full current `sources.yaml` (sources promoted later, e.g.
`st_johns_citizen`), `search_terms.yaml`, `silverleaf_scope.yaml`,
`communities.yaml` neighborhoods (added later), the **Magnolia Oaks name** in
`SJC_DIRECTION_RECONCILIATION_20260706.md`, Task 20 conclusions, the 4 current
publication decisions, monthly wraps (retroactive synthesis), Git history,
live web (retrospective pages + current redirects), and file names containing
future dates.

Controls (recommend the strongest practical combination):

1. **Time-filtered state snapshots** (primary): regenerate visible
   entities/aliases/profiles/sources/scope from Git history at each simulated
   date via `git show <sha>:<path>`.
2. **Record-level availability masks**: every registry entry carries
   `first_known_at`; the loader filters to ≤ T. Records without defensible
   dates are excluded until proven.
3. **Query cutoff + publication-date enforcement**: search results filtered to
   `published_at ≤ T`; retrospective/current pages excluded.
4. **Hidden baseline separation**: the full corpus is read only by the
   evaluator (separate workspace, separate env var, never on the agent path).
5. **Agent prompt isolation**: agents receive only the visible state; a
   "no-future" instruction + a list of forbidden phrases/names (e.g., the
   Magnolia Oaks name before its announcement).
6. **Git history checkout** as an offline fallback for determinism.
7. **Leakage tests**: assertions that no item/alias/source visible at T has an
   evidence date > T; a named-entity blacklist test (e.g., "Magnolia Oaks must
   not be visible before 2026-07-22").

## 19. Recommended backtest architecture

```
Baseline corpus (full)  ──read-only──▶  Hidden evaluator (never on agent path)
                                             ▲
  Simulated date T
      │
      ▼
 Historical-visible state builder
   (git-history snapshots + availability masks, filtered to ≤ T)
      │
      ▼
 Weekly cycle (agents):
   1. deterministic known-source monitor (run_weekly-style, workspace-safe)
   2. bounded search discovery (search_profiles, terms, budgets, cutoff T)
   3. entity/alias reconciliation (match findings → existing subjects)
   4. Resident Coverage Strategist (proposals: entities/aliases/searches/
      sources/lanes/milestones) — proposes only
   5. proposal-review simulation (rubric accept/reject — see below)
   6. timeline reconciliation (link findings into subject timelines)
   7. weekly report (sections §23, minus evaluator)
   8. hidden evaluator compares to baseline (section 23.23)
      │
      ▼
 State transition: only accepted proposals enter next week's visible state
      │
      ▼
 advance T += 7 days → repeat
```

**Acceptance mode recommendation: dual-mode.** Deterministic rubric for the
backtest (a fixed scoring function on §14 signals so runs are reproducible),
human/Buddy acceptance in production. The rubric must be published with the
backtest results so Buddy can see exactly which proposals the simulation would
have accepted.

## 20. Recommended historical period

**Start: 2025-08-01 (not May 2025).** Rationale:
- Captures the full **Aug–Sep 2025 backfill** (budget cycle, school QQ/RR,
  CR 210, SR 16, CR 2209 construction start) — the earliest corpus period with
  dense SilverLeaf-relevant evidence.
- May 2025 (K-8 topping-out) is a single item; its source date (2025-05-07) can
  be the first **discovery event** without starting the simulation that early.
- Run **full period Aug 2025 → Aug 2026** (≈57 weeks), with:
  - weekly machine artifacts (reports + state);
  - monthly synthesis (report §24);
  - milestone-week human reviews (pilot weeks §21);
  - a final scorecard (§25).

Do not assume every week needs manual review; automation + rubric covers
routine weeks.

## 21. Pilot weeks

Select **10 historically important weeks** for the first pilot (evidence-based):

| # | Week (approx) | Should be available at start | Evidence appearing | What strategist should notice | Expected proposal | Enables | Baseline compare |
|---|---------------|-------------------------------|--------------------|-------------------------------|-------------------|---------|-------------------|
| 1 | 2025-08-18 | CR 2209 construction start (Aug 20) | CR 2209 county release | new corridor project, direct SL | tracked entity + profile + milestones | CR 2209 timeline | CR 2209 items |
| 2 | 2025-08-25 | — | SR 16/IGP groundbreak, SR 16 widening hearings | corridor + commute impact | entity + profile | SR 16 timeline | SR 16 items |
| 3 | 2025-09-15 | — | School QQ/RR construction update + naming engagement | school + naming event pending | entity + **naming milestone watch** | K-8 timeline | QQ naming items |
| 4 | 2025-10-27 | CR 2209 entity | CR 2209 opened (Oct 28) | completion milestone | timeline update | completed-project record | CR 2209 opening |
| 5 | 2025-12-01 | — | Harris Teeter proposal (Dec 2) | proposed supermarket in SL | entity (conditional) + grocery lane | HT status searches | Harris Teeter items |
| 6 | 2026-03-23 | Publix entity | Mega Publix opened (Mar 26) | opening milestone | timeline + follow-up | Publix record | Publix opening |
| 7 | 2026-04-06 | — | Beach Valley Mini Golf proposal | amenity proposal | entity (conditional) | rec lane | mini-golf items |
| 8 | 2026-05-11 | — | Phase III water shortage (May 11) | ongoing restriction | lane + recurring restriction watch | water timeline | water items |
| 9 | 2026-06-22 | SR 207 WRF entity | WRF operational (Jun 23) | completion milestone | timeline update | WRF record | WRF items |
| 10 | 2026-07-20 | K-8 entity + naming watch | Magnolia Oaks opening (Jul 22) | **milestone triggered on expected opening** | alias update + opening item + boundary search | K-8 opening | **Magnolia Oaks opening (currently absent)** |

Pilot week 10 is the highest-value single test: the rubric must generate the
opening search from the expected-opening milestone.

## 22. Weekly state-transition model

- **Accepted proposals** (rubric or human) mutate next week's visible state:
  entities, aliases, profiles, terms, milestones, lanes, source candidates.
- **Rejected proposals** are retained (visible to the strategist to avoid
  re-proposing) but never promoted.
- Deterministic transitions: new findings → dedupe → subject match → timeline
  append; source health updates.
- Simulation rule: **no state change except through an explicit accepted
  transition record** — gives full auditability and replay.

## 23. Weekly report contract

Authoritative schema (`data/coverage/weekly/{run_id}/report.yaml` + a
human-readable `.md`):

1. run identity (run_id, generator revision, simulated T)
2. simulated date range (T, T+7)
3. starting visible state (snapshot hash + counts)
4. sources monitored (+ health)
5. searches executed (queries, providers, budgets, result counts)
6. source-health outcomes
7. findings (items + matches vs subjects)
8. no-match results
9. important new subjects
10. entity proposals (evidence, benefit, cost)
11. alias proposals
12. source proposals
13. search-profile proposals
14. lane proposals
15. milestone proposals
16. timeline updates
17. resident-priority rationale
18. unresolved gaps
19. false positives
20. proposed state transition (full diff)
21. accepted/rejected simulated decisions (rubric scores)
22. next-week state (snapshot)
23. hidden-evaluator metrics — **never present in agent-visible report**; written
    only to the evaluator's private workspace.

Storage: `data/coverage/weekly/` (simulated) — **never mixed into
`logs/runs/{daily,weekly,monthly}/`** which is reserved for real operations.

## 24. Monthly report contract

`data/coverage/monthly/{YYYY-MM}/report.md`:
subjects discovered; searches promoted; sources added; timelines advanced;
recurring blind spots; false-positive patterns; resident-coverage health;
missed baseline subjects (evaluator-fed); upcoming expected milestones.

## 25. Final evaluation report

`data/coverage/final/{run_id}/report.md`: total recall; total precision;
subject-promotion quality; median discovery lag; alias performance; source
expansion; lane discovery; milestone anticipation; failure analysis; proposed
production changes; **go/no-go judgment** for the production adaptive loop.

## 26. Evaluation metrics

| Metric | Formula / rubric |
|--------|------------------|
| Discovery recall | known-baseline findings rediscovered ÷ total baseline findings |
| Subject recall | important baseline subjects identified as subjects ÷ total |
| Promotion quality | correctly promoted ÷ (correct + wrongly promoted + missed promotions) |
| Alias reconciliation | aliases resolved (temp/former/new names → one subject) ÷ alias events |
| Source expansion | relevant new sources proposed ÷ relevant sources in baseline |
| Search expansion | useful searches generated (returned novel results) ÷ searches run |
| Milestone anticipation | upcoming events found from expected-milestone searches ÷ upcoming events |
| Discovery lag | days between public evidence date and simulated detection |
| Precision | true-positive proposals ÷ total proposals |
| Timeline quality | findings reconciled into one evolving subject ÷ total related findings |
| Resident usefulness | proportion of promoted subjects rated resident-relevant by Buddy |
| Reporting quality | Buddy-approvable state-transition proposals (subjective, scored 1–5) |

## 27. Existing code reuse assessment

| Tool | Verdict | Notes |
|------|---------|-------|
| `scripts/run_weekly.py` | **Reusable with adapter** | workspace isolation + bundle; needs historical-clock + isolated state root; Stage A monitors only |
| `scripts/bundle_build.py` / `bundle_verify.py` / `import_weekly_bundle.py` | **Production-only** | fine for real transfers; not needed for simulation |
| `scripts/accept_candidates.py` | **Reusable** | candidate acceptance pattern → promotion-review simulation |
| `scripts/rebuild_dedupe_index.py` | **Reusable as-is** | deterministic dedupe for findings |
| `scripts/build_review_queue.py` | **Reusable** | entity/alias matching already wired (ENT-002) |
| `scripts/storage_adapter.py` / `file_adapter.py` | **Reusable** | file adapter is the simulation's state root; `pg_adapter.py` **do not use** (DORMANT) |
| `scripts/retention.py`, `metrics_snapshot.py`, `portability_check.py` | **Unrelated** | leave alone |

**Missing implementation seams Strong Codex must add:** search-provider
abstraction (no runner exists), historical-clock, isolated simulation
workspace, historical-visible-state builder, proposal/acceptance state,
milestone/temporal state, timeline reconciliation, evaluation harness, leakage
tests.

## 28. Missing schemas and tooling

- `schemas/` has no: `search_run`, `search_candidate`, `coverage_subject`,
  `milestone`/`temporal_assertion`, `coverage_lane`, `promotion_proposal`,
  `weekly_report`, `backtest_run`. The 2026-07-06 PG design (§7) is the
  reference; Strong Codex should port it to file-backed YAML schemas.
- No `scripts/` for: search runner, coverage strategist executor, proposal
  reviewer, timeline reconciler, backtest harness, evaluator, leakage checker.
- **Live checks performed this task (recorded):** (1) `stjohns.k12.fl.us/newschools/`
  → School QQ (SilverLeaf DRI) "Under Construction"; (2) `stjohns.k12.fl.us/news/?s=Magnolia+Oaks`
  → "St. Johns County School District Opens First School in Silverleaf
  Community" (Jul 22, 2026) = **Magnolia Oaks Academy**. Both confirm the
  highest-value case study.

## 29. Production observability requirements

- **Weekly resident-coverage report** (production): what mattered; what was
  found; new subjects proposed; searches added; remaining gaps; upcoming
  milestones; delta vs last week.
- **Coverage-health report**: subjects with stale timelines; missed expected
  milestones; failing sources; profiles returning no useful results;
  high-priority lanes with low coverage; proposals awaiting review.
- **Promotion-review report**: proposed entities/aliases/profiles/sources/lanes
  with evidence, expected benefit, cost/budget.
- **Backtest comparison report**: discovered vs baseline; misses; lag;
  false positives; promotion failures.
- Locations: `data/coverage/` (state + reports); `logs/runs/weekly/` for real
  run logs only; retention per `docs/retention.md`; simulated artifacts in a
  git-ignored `runtime/backtest/` + committed summaries.

## 30. SJC versus Ivy ownership

**Confirmed boundary:** SJC owns resident-coverage strategy, search profiles,
entity promotion, subject timelines, backtest data + evaluation rules, weekly
task behavior, and reports. Ivy owns deployment, scheduling, runtime,
credentials, VPS resource limits, health execution, transport, retention, and
operational evidence. The **backtest framework stays repository-local**
(`data/coverage/` + `scripts/`); no Ivy work is needed for it.

## 31. Strong Codex implementation packet

Instruct Strong Codex to (authorize broad read-only + file-backed stateful
execution in SJC; no Ivy/PostgreSQL activation; no publication/review-state
changes):

1. **Preserve the current corpus as the hidden baseline** — copy/snapshot
   `data/` (read-only reference) into a clearly marked baseline that the
   evaluator alone reads.
2. **Formalize the Resident Coverage Strategist** — new OpenCode agent
   (`.opencode/agents/sjc-intel-coverage-strategist.md`) + role prompt
   (`prompts/coverage_strategist_task.md`) + deterministic rules pre-pass
   (§14).
3. **Reconcile/extend existing agents** — source-watch stays Loop B; RI
   classifier stays item-level; architect owns acceptance; no role duplication.
4. **Build historical-visible-state generation** — `git show` snapshots +
   `first_known_at` masks + record-level availability (§17–18).
5. **Implement future-data leakage controls** — filters, hidden-baseline
   separation, agent prompt isolation, leakage tests (§18).
6. **Add isolated simulation workspaces** — `runtime/backtest/{run_id}/`;
   never touch authoritative `data/`.
7. **Add a simulated clock** — injectable `now(T)` for every stage.
8. **Add weekly state transitions** — only accepted proposals mutate state;
   full diff records.
9. **Add agent proposal schemas** — entity/alias/source/search-profile/lane/
   milestone proposal records (YAML).
10. **Add promotion-review schemas** — evidence, rubric score, expected
    benefit, cost, decision.
11. **Add timeline reconciliation** — link findings into `subjects.yaml`
    timelines by entity/alias/name matching.
12. **Add weekly/monthly/final reporting** (§23–25).
13. **Add a hidden baseline evaluator** — recall/precision/lag/§26 metrics.
14. **Define scoring** — publish the rubric.
15. **Run selected pilot weeks** (§21) — start with week 10 (Magnolia Oaks).
16. **Inspect pilot failures** — iterate the harness/rubric.
17. **Refine the harness** — until pilot weeks reproduce expected outcomes
    without leaking the baseline.
18. **Prepare but do not necessarily execute the full 57-week run**.
19. **Update roadmap and durable docs** — mark the adaptive loop as implemented
    vs designed; update data_model/backlog.
20. **Preserve production/backtest separation** — sim never touches real state.
21. **Avoid PostgreSQL activation unless strictly justified** — file-backed
    first; PG only if the file store demonstrably fails.
22. **Leave medium-agent follow-up packets** — e.g., per-lane profile builds,
    source-candidate promotion runs.

Strong Codex may push back on the architecture (e.g., replace the 9-table PG
design with a leaner file model, or recommend a different promotion rubric).

## 32. Medium-agent follow-up opportunities

- Build per-lane search profiles + terms from `search_terms.yaml`/`search_profiles.yaml`.
- Run the recurring SilverLeaf discovery prompt on a schedule and reconcile to
  the coverage state.
- Populate `data/coverage/subjects.yaml` for the §11 subject set.
- Wire milestone records for the 2026-27 school year + FY2027 TRIM cycle.
- A "current coverage health" one-pager for Buddy before each approval.

## 33. Risks and unresolved issues

- **Reconstructability is PARTIAL** for entity/profile/alias creation dates —
  the backtest must use conservative availability rules or discard those
  states' earliest weeks.
- **Live-web leakage** is the hardest control; search in the simulation should
  prefer archived snapshots (Git-tracked captures) or strictly date-filtered
  results, not live engines.
- **Magnolia Oaks name is in a planning doc with an error** (`type: private`);
  the backtest's alias test must treat the name's first *defensible public*
  date as its announcement, not the repo-doc date.
- **`beat_candidates.yaml` is empty** — Loop D has no seed data; either backfill
  beats from §16 lanes or drop the beat concept in favor of lanes.
- **Volume of manual review**: 57 weeks is only tractable with the rubric +
  monthly synthesis; Buddy review is reserved for milestone weeks + final
  scorecard.
- **Scope drift risk**: the strategist must propose, never auto-promote; the
  rubric must be strict enough to keep precision high.
- The 4 current publication decisions and Task 20 conclusions must never be
  visible to simulation agents (leakage).

## 34. Files changed

**None.** This task is read-only (report only): `reports/21-resident-coverage-backtest-assessment.md`
is the sole new file (required deliverable). No authoritative data, review, or
publication state was modified.

## 35. Validation results

```
python3 -m pytest tests/ -v            → PASS, 217 passed
python3 scripts/validate.py            → PASS — ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS — 0 errors, 321 warnings
python3 scripts/validate_silverleaf_scope.py  → PASS — 0 errors, 0 warnings
python3 scripts/portability_check.py   → PASS
git diff --check                       → clean
git status --short                     → only reports/20-… (untracked, prior task)
```

## 36. Final Git status

`master` @ `9c985c7`, clean except the untracked Task 20 report. No commits,
no push, no publication/review changes, no source/entity/taxonomy promotions.

## 37. Final task status

| Area | Status |
|------|--------|
| Prior intent reconstruction | COMPLETE |
| Existing adaptive-discovery inventory | COMPLETE |
| Duplicate-agent risk | COMPLETE (none; strategist is a distinct role) |
| Workflow failure point | COMPLETE (stops after entity creation) |
| Magnolia Oaks + construction case studies | COMPLETE (incl. live verification) |
| Historical reconstructability | COMPLETE (PARTIAL overall) |
| Leakage controls | COMPLETE |
| Strategist design | COMPLETE |
| Promotion model + weekly state + lanes | COMPLETE |
| Weekly/monthly/final reports + metrics | COMPLETE |
| Pilot weeks | COMPLETE (10) |
| Code reuse + missing schemas | COMPLETE |
| Strong Codex packet | COMPLETE |
| SJC/Ivy ownership | COMPLETE (confirmed) |
| Validation | COMPLETE (read-only) |
| Backtest execution | NOT RUN (per scope) |

**Final status vocabulary:** COMPLETE — the repository's prior intent is fully
reconstructed (the adaptive search/discovery system was designed 2026-07-06 and
stopped at "designed not orchestrated"), the failure point is demonstrated by
the missed Magnolia Oaks opening, and Strong Codex can begin implementation
from this report without broad rediscovery. No authoritative state was changed.
