# Task 16 — Publication Foundation, Resident UI Discovery, and Ivy Codex Preparation

**Task identity:** 16-publication-foundation-and-ui-discovery.md
**Date:** 2026-08-04
**Repositories:** SJC_Intel (`/Users/buddy/projects/sjc_intel`, implementation);
Ivy Control VPS (`/Users/buddy/projects/ivy-control-vps`, read-only);
portfolio-site repo — **not discoverable** (see §22).
**Final status:** COMPLETE_WITH_FOLLOW_UP

---

## 1. Executive result

SJC_Intel is now **publication-capable**: the publication foundation that did
not require architectural input is implemented, validated, and tested. The
remaining path to a public SilverLeaf v0 is editorial (human review + item
approval), the §3B-G1 SilverLeaf scope registry, the §3B-G2 static export, and
the §3C-G2 UI — no further broad architecture discovery is required.

Delivered (repo-local, offline, tested):

- **Publication-decision model** — file-backed decisions under
  `data/publication_decisions/{item_id}.yaml`, operator tool
  (`scripts/publication_decision.py` approve/reject/defer/withdraw), schema,
  audit history, transitions, idempotency, dry-run. `verified` never becomes
  publication approval; nothing is published.
- **Complete corpus validation** — `scripts/validate_publication_corpus.py`
  validates every actual corpus record (not just schemas), with deterministic
  machine (`--json`) and human output, exit-code contract, and a documented
  legacy-exception registry. Current corpus: **0 blocking errors**.
- **Deterministic publication selector** — `scripts/select_publication_items.py
  --release-id <id> --check` (no mutations in check mode) implements every
  contract gate and default exclusion.
- **Resident UI discovery + v0 spec** — `docs/public_ui_v0_spec.md`
  (six-page static v0, search/filter/detail/empty/accessibility) and
  `docs/static_release_data_contract.md` (release.json / search-index.json /
  release-manifest.json field contract, allowlist/denylist, rollback).
- **SilverLeaf scope decision packet** —
  `docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md` (Buddy/GPT-ready;
  registry already seeded; boundary/roads/school authorities still
  MISSING-AUTHORITY → DIR-001/009/010/011).
- **Strong Codex task specification** (report §29) — Ivy doc consolidation,
  SJC reconciliation, live VPS storage audit, reusable onboarding, Reckless
  Ben preparation, privileged SJC operational work.

Validation: 161 tests pass (140 baseline + 21 new); `validate.py` ALL PASSED;
`validate_publication_corpus.py` PASS; `portability_check.py` PASS;
`git diff --check` clean. No publication/review decision was made; no item was
approved; no release was generated; nothing was committed or pushed.

---

## 2. Starting SJC state

| Item | Value | Label |
|------|-------|-------|
| Branch / HEAD | `master` @ `1be2ade` | VERIFIED |
| Remote | origin `https://github.com/wguDataNinja/sjc-intel.git`; origin/master == local (0/0) | VERIFIED |
| Working tree | Intended Task 15 changes (README, ROADMAP, LICENSE, docs) + pre-existing dirty data + Tasks 12–14 outputs | VERIFIED |
| Tests / validation | 140 passed; `validate.py` ALL PASSED; portability PASS | VERIFIED |
| Review queue | 167 entries (83 verified / 78 pending / 5 archived / 1 rejected_noise) | VERIFIED |
| Corpus scan | 192 item records in data/intel_items; 167 unique item_ids; 25 duplicated (NBOR 06-08 vs 06-26 capture); 9 legacy CDD records; 5 records missing created_at; 46 missing `_dedupe_key` | VERIFIED |
| Publication state | None — no `publication_status`, no decision registry, no release manifest | VERIFIED |
| SilverLeaf relevance | Partial — `communities.yaml` + `tracked_entities.yaml` seeded; no per-item decision field | PARTIAL |
| Public README / ARCHITECTURE / LICENSE | Present (Tasks 14–15) | VERIFIED |

**Task 15 changes confirmed in tree:** `LICENSE`, `README.md` license section,
`docs/postgresql_adapter.md` (DORMANT_FUTURE_READY), `docs/backup-restore.md`
(deferral), `ROADMAP.md` §6A. No conflict between current files and report 15.
Prior task outputs (reports 11–15, Tasks 12–15, LICENSE) are present but
**uncommitted** (as designed). The repository was safe for a medium
implementation session; unrelated work was preserved untouched.

## 3. Starting Ivy state

| Item | Value | Label |
|------|-------|-------|
| Branch / HEAD | `main` @ `3e94197`, 2 ahead of origin | VERIFIED |
| Working tree | 17 dirty lines (pre-existing control-plane work incl. `repos/sjc-intel/CONTROL.md` modified) | VERIFIED |
| SJC control record | `repos/sjc-intel/CONTROL.md`: `remote: null`, `approved_sha: 35a0246`, gate 1 `NOT YET ADMITTED`, gate 3 `BLOCKED` | **CONFLICT** (stale) |
| SJC release-gate record | `RELEASE_GATES.md` does not exist (CONTROL.md links to it) | MISSING |
| Reckless Ben control record | `repos/reckless-ben/CONTROL.md`: local-only, `approved_sha: d6b99f77`, gates PARTIAL/UNKNOWN | VERIFIED (input for §33) |
| Doc authority | `docs/README.md` classifies active/supporting/historical; new-doc governance rule present | VERIFIED |
| SJC evidence | intake 2026-07-28, orchestration archive, hermes-validation-task10, outbox runs 2026-08-02/2026-08-03 | VERIFIED |
| Portfolio-site repo | **Not discoverable** from SJC or Ivy authority (§22) | MISSING |

## 4. Publication foundation implemented

The §3A-G2 foundation is implemented and coherent with
`docs/publication_release_contract.md`:

- review/publication separation enforced by code (`verified` never implies
  publication approval; the selector requires an explicit approved decision);
- a separate file-backed **publication-decision registry** (per-item YAML)
  instead of rewriting legacy intelligence items — preferred by the task;
- explicit human-controlled decisions with audit history;
- deterministic corpus validation with machine-readable output;
- deterministic publication selection with no mutations in `--check`;
- release-level `published` state is reserved for the (future) release
  manifest; decision tooling never sets it.

## 5. Publication-decision model

**Location:** `data/publication_decisions/{item_id}.yaml` (one file per item,
append-safe). **Schema:** `schemas/publication_decision.schema.yaml`.

Supported fields (contract §2 + task §5): `item_id`, `publication_status`
(`approved`/`rejected`/`deferred`/`withdrawn` — following operator vocabulary;
`published` reserved for releases), `reviewer`, `decision_timestamp`,
`rationale`, `release_eligible`, `sensitivity_review`, `public_summary_override`,
`withdrawn`, `withdrawal_reason`, `superseded_by`,
`source_attribution_confirmed`, `silverleaf_relevance` (decision/rationale/
place_ids/entity_ids), `origin_review_status`, and an append-safe `history`
audit trail.

Terminology follows the contract and existing vocabulary:
`candidate ≠ verified ≠ publication-approved ≠ published`. Statuses used by the
operator tool are `approved` (≡ publication-approved), `rejected`, `deferred`,
`withdrawn` — matching the suggested operator operations. `published` is
release-level only.

## 6. Corpus validator

`scripts/validate_publication_corpus.py` validates **actual records**, not only
schema files. Checks implemented (task §6): item ID format; item ID uniqueness
with canonical-file treatment for duplicate captures; source ID existence;
source-event linkage policy; source URL presence/format; observed/source
timestamps (with documented legacy M/D/YYYY tolerance); required evidence;
dedupe fingerprint presence; enum values (sensitivity, review_status, topics);
sensitivity/review combination; publication-decision references; entity
references; community/place references; topic references; public-field safety
and internal-only field exclusion (via `public_projection` +
`validate_public_safe`); canonical/superseded relationships; duplicate/repeated
IDs; release-eligibility preview; SilverLeaf relevance state; legacy
exceptions.

Outputs: deterministic human summary and `--json` machine summary; failure and
warning counts; exact item IDs; exit 0 when no blocking errors, exit 1
otherwise. Legacy treatment is documented in
`data/publication_decisions/legacy_exceptions.yaml` (4 exceptions: NBOR
06-08 duplicate capture, 9 legacy CDD records, 5 records missing created_at,
`rural_sjc` unregistered community reference).

**Current corpus result:** 192 items, **0 blocking errors**, 320 warnings,
54 reviewed release-eligible preview, 0 decisions.

## 7. Publication selector

`scripts/select_publication_items.py --release-id <id> [--window-start]
[--window-end] [--check] [--json]`.

Requires (contract §2): `review_status: verified`; explicit approved decision;
allowed sensitivity (low; medium only with recorded editorial approval; high
excluded); valid source attribution and URL; non-withdrawn; non-superseded
canonical; SilverLeaf `included` decision; public-safe projection; within the
release window. Default exclusions: pending, high-sensitivity, unresolved
human review, rejected noise, archived-only, duplicates, incomplete
attribution, invalid URLs, internal-only artifacts, missing SilverLeaf
decision, withdrawn.

Outputs: selected IDs (deterministic order), excluded IDs with reasons, counts
by source/topic/status, window. `--check` performs no mutations. The selector
never marks anything published. On the current corpus it correctly selects
**0** items (no publication decisions exist).

## 8. Operator decision workflow

`scripts/publication_decision.py approve|reject|defer|withdraw|show
--item-id <id> --reviewer <name> --rationale "..." [--silverleaf included ...]
[--dry-run] [--json]`.

Enforced: explicit item ID; reviewer identity (flag or `SJC_PUB_REVIEWER`);
rationale required (except defer); current state + source URL + communities +
SilverLeaf shown; dry-run diff before write; validation before mutation;
invalid-transition rejection (e.g. `withdrawn` from `rejected` is rejected;
`withdraw` requires prior `approved`); idempotency (repeat is a no-op); audit
history appended (never replaced); high-sensitivity approval blocked;
one-item-only (no bulk); never publishes or creates a release. Writes only
under `data/publication_decisions/`.

## 9. Tests and negative cases

`tests/test_publication.py` (21 tests) + real-shaped fixtures under
`tests/fixtures/publication/`. Coverage: validator on real-shaped records;
public projection excludes internal fields; selector selection/exclusions
(pending, high-sensitivity, withdrawn, superseded, missing SilverLeaf
decision, missing decision, deterministic ordering); decision tool (dry-run
no-write, invalid transitions, withdraw-after-approve, high-sensitivity
block, audit preservation, idempotency). Negative cases required by the task
are all covered: invalid transitions; corpus errors; legacy warnings; selector
exclusions; sensitivity exclusions; missing source links; missing SilverLeaf
relevance; withdrawn items; superseded items; deterministic ordering; audit
preservation; dry-run safety.

## 10. Actual corpus viewed as a SilverLeaf resident

I read the real intelligence items, review queue, source events, tracked
entities, communities, taxonomy, and publication candidates as a SilverLeaf
resident asking "what may affect my household, commute, utilities, schools,
development, services, and community?"

What a resident would actually find:

- **Genuinely useful:** Phase III water shortage (countywide, affects every
  lawn/irrigation); free chlorine burnout (water taste/odor, dialysis/business
  guidance); hurricane-season preparedness; SilverLeaf K-8 school construction
  (kids, boundary, traffic); CR 2209 connector relief; the new mega Publix;
  Bala's second location (pending verify); proposed Harris Teeter; Beach
  Valley mini golf; Baptist campus; NBOR **development hearings** with
  application IDs (rezonings, PUD modifications, cell towers) — these are the
  "what's being built near me" signal.
- **Too countywide / bureaucratic:** most BCC consent agenda items (utility
  easement/resolution boilerplate "Motion to adopt Resolution..."), surplus
  auction, library program promos, recycling-driver human-interest story,
  awards/recognition items.
- **Too stale for a fresh release window:** January BCC items (44 verified,
  ~6 months old), most June items if the release window is 60 days.
- **Needs context / source explanation:** NBOR "Comcast"/"AT&T"/"FPL" ROW
  permits are utility pole/fiber permits — a resident needs a "what is this"
  hint; BCC "Resolution 2026-____" items are meaningless without the agenda
  link; "SUPMAJ/REZ/ZVAR/MAJMOD/CPA(SS)" codes need a legend.
- **What residents would browse:** roads & traffic; utilities & water;
  development & zoning; schools; local government; community & amenities;
  public safety (only if approved).
- **Entities to follow:** SilverLeaf K-8, CR 2209 connector, Publix
  SilverLeaf, Silverleaf Commons/Market, Harris Teeter (proposed), Beach
  Valley Mini Golf, Baptist campus.
- **Places/corridors that matter:** SilverLeaf + neighborhoods; CR 210
  corridor; SR 16 corridor; I-95/IGP access (segments not yet registered).
- **Date context:** source date must be shown separately from review/publish
  date; residents need to know the water notice is from May/June.
- **Source types needing explanation:** NBOR (notices app), BoardDocs/agenda
  PDFs, ROW permits, CDD governance.
- **Should link directly to source records:** everything; the source remains
  authoritative.
- **Should remain excluded:** crime/public-safety by default; unverified
  local-media items; internal-only/archival records; legacy CDD records.

## 11. Resident information needs

1. What changed recently in/around SilverLeaf and why it matters to my
   household/commute/schools/utilities.
2. Is it verified, and what's the original source I can check?
3. What is being built near me (development/rezoning/permits) and when are the
   public hearings?
4. Is my water/utility service affected (restrictions, maintenance, boil
   notices)?
5. Are my commute roads affected (CR 210, SR 16, IGP/CR 2209, railroad
   crossings)?
6. What is happening with my kids' school (K-8 construction, boundary)?
7. What's opening near me (retail, services, healthcare) and when?
8. What decisions is the county making that change local conditions (taxes,
   zoning, budget, utilities)?

## 12. Useful topics, entities, and places

- **Topics (corpus evidence):** infrastructure, development, county_government,
  environment, public_notices, transportation, public_safety (conditional),
  community_events, economic_development, parks_recreation, water_restrictions,
  health_wellness, education.
- **Entities:** SilverLeaf K-8 (`ENT-EDU-SILVERLEAF-K8`), CR 2209 connector
  (`ENT-ROAD-CR-2209-CONNECTOR`), Publix SilverLeaf
  (`ENT-RETAIL-PUBLIX-SILVERLEAF`), Silverleaf Commons/Market, Harris Teeter
  (proposed), Beach Valley Mini Golf, Baptist SilverLeaf campus,
  `ENT-COMM-SILVERLEAF`.
- **Places:** `silverleaf` + its 11 registered neighborhoods, `cr_210_corridor`,
  `sr_16_corridor`, and (for adjacency) the IGP/CR 2209 corridor.

## 13. Low-value or confusing data

- BCC consent/resolution boilerplate ("Motion to adopt Resolution…" without
  agenda context) — high volume, low resident signal.
- NBOR single-word utility ROW permits ("Comcast") without a legend.
- NBOR/planning code acronyms (SUPMAJ, REZ, ZVAR, MAJMOD, CPA(SS), PVZVAR,
  NZVAR) — need a plain-language legend.
- Countywide civic items with no SilverLeaf impact (auctions, awards, library
  promos, recycling human-interest).
- Stale January items outside a sensible release window.
- Unverified local-media items (URL/date not yet confirmed) must not publish
  until verified.

## 14. Recommended v0 information architecture

Home/Latest → Item detail; Browse by Topic; Browse by Place; Browse by Entity;
About (methodology/limitations); Data & Sources. Six pages; topic/place/entity
are one Browse template with a filter bar. Filter dimensions are stable
taxonomy topic IDs, place IDs, and entity IDs. Search covers title, summary,
why-it-matters, topic/place/entity labels, source name.

## 15. Recommended v0 pages

- **Home/Latest** — dated feed, "why it matters" cards, topic/place chips,
  source name + date, verified indicator, release footer.
- **Item detail** — full field set (§17).
- **Browse by topic / place / entity** — counts + filtered cards; place page
  marks adjacency ("nearby corridor"); entity page shows lifecycle label.
- **About** — public sources, human review, periodic, not alerts, not complete
  coverage, source links authoritative.
- **Data & sources** — source list with what each provides and why.

Full spec: `docs/public_ui_v0_spec.md`.

## 16. Search and filter behavior

Searchable fields: title, summary, why-it-matters, topic labels, place labels,
entity labels, source name. Ranking: exact phrase > title word > summary word >
label match (deterministic; no learned ranking). Filters (topic/place/entity)
combine AND with search; chips removable; no-results empty state; source/date
always shown; internal review fields never shown.

## 17. Item-detail requirements

title; plain-language summary; why it matters; affected place(s); topic(s);
entity(ies); source name + source URL (opens original); source date; review
date; publication date; verification level; sensitivity display (minimal);
limitations note; related items. See `docs/public_ui_v0_spec.md` §4.2.

## 18. Static UI data contract

Defined in `docs/static_release_data_contract.md` — `release.json`,
`search-index.json`, `release-manifest.json` with exact public fields,
stable filter IDs, deterministic ordering, public allowlist, internal
denylist, release version/rollback identity, validation, file-size
expectations, client caching, no-results behavior. Implementation-ready for
the §3B-G2 static-export task without further architectural decisions.

## 19. SilverLeaf scope decision packet

`docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md` — Buddy/GPT-ready.
Key elements (provenance-labeled):
- **Known neighborhoods (REPO-VERIFIED):** 11 directory-confirmed + `cherry_elm`
  (resident-mentioned; may overlap).
- **Aliases (REPO-VERIFIED):** SilverLeaf / Silver Leaf / Silverleaf (lowercase
  'l' is the registered commercial spelling for Silverleaf Commons/Market).
- **Access roads (REPO-VERIFIED partial / INFERRED):** SilverLeaf Parkway, St.
  Johns Parkway / CR 2209, CR 210, SR 16, CR 16A, IGP. Missing official
  boundary/segments (DIR-001/009/011).
- **Serving schools (REPO-VERIFIED entity / INFERRED zones):** SilverLeaf K-8,
  Tocoi Creek HS (evidence); attendance zones MISSING-AUTHORITY (DIR-010).
- **Utilities (REPO-VERIFIED):** county utility department; SR 207 WRF Phase 2
  (corridor capacity).
- **Nearby entities (REPO-VERIFIED):** 15 tracked entities (retail, education,
  rec, roads, health, community). Nocatee entities → likely exclude/adjacent.
- **Proposed inclusion/exclusion/adjacency/countywide-material-impact rules**
  (EDITORIAL — for approval).
- **needs_review cases (REPO-VERIFIED):** 3 high-sensitivity SilverLeaf crime/
  minor items, 2 unverified low-sensitivity SilverLeaf items, SJSO items.
- **Source provenance table** and a bottom-line: registry is seeded; missing
  pieces are the boundary/road/school authorities (DIR-001/009/010/011) and
  the per-item `silverleaf_relevance` decision — not GIS/PostGIS.

## 20. Updated editorial packet (Task 15 baseline + new evidence)

- **Candidate first-release items:** start from verified low-sensitivity
  SilverLeaf-relevant items (utility service, corridor roads) plus SilverLeaf
  pending items after verification. Current verified set is countywide-heavy;
  a defensible first release is small and curated (~5 items), matching Task 15.
- **Stronger exclusion reasons (new evidence):** the selector now
  machine-enforces exclusions (pending, high-sensitivity, missing SilverLeaf
  decision, withdrawn, superseded, invalid URL, duplicate, legacy); the
  validator surfaces 320 warnings; `rural_sjc` unregistered reference flagged.
- **Possible replacements for weak candidates:** verified county news corridor
  item (railroad crossing) + utility service items as the countywide
  SilverLeaf-impact bucket.
- **Freshness options:** release window is configurable in the selector
  (default 60 days); recommend a 30–60 day window so stale Jan/June items drop.
- **Countywide relevance rule:** countywide item publishes only when it
  materially affects SilverLeaf (utility continuity, water restrictions,
  tax/land decisions); civic-only countywide items excluded.
- **Crime/public-safety recommendation:** exclude by default; any exception
  requires explicit editorial approval and is never in the v0 launch set.
- **Source-date vs publish-date display:** show both (recommended; see UI
  spec §2/§17).
- **Likely first-release size:** ~5–15 items after editorial review of the
  SilverLeaf pending + verified countywide-impact set.
- **Gaps that still block a credible release:** 78 pending items need human
  review; SilverLeaf scope authority (boundary/schools/roads) needs approval;
  per-item `silverleaf_relevance` decisions need to be recorded; portfolio-site
  repo must be located for §3C-G1.

## 21. Candidate first-release items

Evidence-backed starter pool (NOT approved; requires editorial review +
explicit publication decisions + SilverLeaf relevance decisions):

| Item | Title | Source | Sens. | Status | Why considered |
|------|-------|--------|-------|--------|----------------|
| SJC-UTIL-20260603-0002 | Free Chlorine Burnout June 1–21 | utility | low | verified | Utility service continuity for SL residents; countywide |
| SJC-UTIL-20260603-0001 | Phase III Water Shortage — Active | utility | medium | verified | Direct impact (irrigation rules); needs editorial approval for medium |
| SJC-CN-20260603-0005 | Phase III Extreme Water Shortage Declaration | county news | low | verified | Countywide material impact |
| SJC-CN-20260626-0002 | Railroad Crossing Maintenance (West King/Kinlaw) | county news | low | verified | Corridor access relevance (needs SL relevance decision) |
| SJC-SL-20260706-0005 | Bala's opening second location in Silverleaf | silverleaf discovery | low | pending | Directly SilverLeaf; needs URL/date verification |
| SJC-SL-20260706-0003 | Lightning strike at SilverLeaf home | silverleaf discovery | low | pending | Directly SilverLeaf; needs verification |

Excluded by default (machine-enforced): 3 SilverLeaf crime/minor items, all
SJSO items, all pending items without decisions, NBOR 06-08 duplicate capture,
all legacy CDD records.

## 22. Portfolio-site context

**Not discoverable.** Searched SJC repo, Ivy authority docs
(PORTFOLIO_INTENT, PORTFOLIO_UNIVERSE, PORTFOLIO_BASELINE, README, CONTROL),
and the workspace. `Portfolio/` is Buddy's **job-search positioning** repo
(resumes, applications, project_info) — not a website, no build/deploy, no
static hosting. `projects_portfolio/` is an empty shell (2 JSON files, no
manifest, no docs). No website repo exists under any expected name
(astro/hugo/jekyll/eleventy/vite/nextjs/package.json scan → none).

**Exact missing context (packet for the next agent / Buddy):**
1. Portfolio-site repository path (or hosting provider/account if not a local
   repo).
2. Framework / static generator, if any (README/package.json hints absent).
3. Deployment route (GitHub Pages, Netlify, Vercel, self-hosted static, CDN).
4. Build/deploy commands and expected artifact directory.
5. Design system / CSS conventions.
6. Whether SJC UI belongs **inside** the portfolio repo (a section/page) or as
   a **separately deployed static app** linked from it.
7. Access authority to read the target repo (read-only).
Nothing about the site technology should be assumed. §3C-G1 must produce a
target-repo context packet before any UI build.

## 23. Remaining UI unknowns

- Target portfolio-site repo/framework/deploy route (blocked on §22 packet).
- Approved SilverLeaf scope (boundary, roads, schools) for place/entity pages.
- Public-safety display policy (exclude vs curated).
- Release window choice (30 vs 60 days).
- Whether raw excerpts ever appear publicly (default: no).
- First-release editorial approval + item decisions.

## 24. SJC files changed

Added:
- `scripts/publication_common.py`
- `scripts/publication_decision.py`
- `scripts/select_publication_items.py`
- `scripts/validate_publication_corpus.py`
- `schemas/publication_decision.schema.yaml`
- `data/publication_decisions/legacy_exceptions.yaml`
- `docs/public_ui_v0_spec.md`
- `docs/static_release_data_contract.md`
- `docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md`
- `tests/test_publication.py`
- `tests/fixtures/publication/**` (real-shaped corpus, registry, source events)
- `logs/agents/sjc-intel-architect/2026-08-04_publication_foundation_and_ui_discovery.md`

Modified:
- `scripts/validate.py` (§8 publication-decision checks)
- `ROADMAP.md` (§3A-G2 status, §3D sequence, builder-task reference)

Pre-existing dirty/untracked files (data + Tasks 12–15 outputs) preserved
untouched. Nothing committed or pushed. No item approved or published.

## 25. Validation results

```
python3 -m pytest tests/ -v            → PASS, 161 passed (140 baseline + 21 new)
python3 scripts/validate.py            → PASS — ALL PASSED (incl. new §8 publication-decision checks)
python3 scripts/validate_publication_corpus.py → PASS — 0 blocking errors, 320 warnings, 192 items
python3 scripts/select_publication_items.py --release-id SJC-REL-2026-08 --check → CHECK: no items currently eligible (0 selected, expected)
python3 scripts/portability_check.py   → PASS
git diff --check                       → clean
git status --short                     → only intended new files + pre-existing dirty files
git branch --show-current              → master
git remote -v                          → origin https://github.com/wguDataNinja/sjc-intel.git

Ivy (read-only):
git -C ivy-control-vps status --short  → 17 pre-existing lines; untouched
git -C ivy-control-vps branch --show-current → main
git -C ivy-control-vps log -n 10 --oneline → 3e94197…412082b
git -C ivy-control-vps diff --check    → clean
```

## 26. Ivy lessons carried forward

- SJC matured substantially before Ivy gate tracking caught up; CONTROL.md
  still lags reality (stale remote/SHA/gates) and `RELEASE_GATES.md` is
  absent.
- Bundle/import/receipt/prune and decision/validation patterns now exist in
  SJC and should become Ivy standards (bundle-transfer already added to
  `VPS_ADMISSION_CHECKLIST.md`; backup-disposition gate still pending).
- Ownership model (project owns products/implementation; Ivy owns
  admission/operations) is correct but inconsistently recorded; ROADMAP §6A is
  the reference.
- Task/report flow stays in the project; Ivy archives some orchestration
  copies (duplication noted).
- SJC's file-backed publication-decision + legacy-exception pattern is a
  reusable generic shape for other repos.

## 27. Documentation-sprawl findings

Overlapping Ivy authorities identified (report 15 + this inspection):
working memory vs repository-control model vs VPS admission checklist vs
portfolio conventions vs database docs vs lifecycle docs vs backup manifest
docs vs per-repo CONTROL.md vs (missing) per-repo RELEASE_GATES.md vs private
runbook vs onboarding evidence. Real overlaps:
- `VPS_ADMISSION_CHECKLIST.md` vs `PORTFOLIO_CONVENTIONS.md` admission
  requirements (checklist references conventions — good, but several checklist
  items are really gates).
- `PORTFOLIO.md` vs `PORTFOLIO_INTENT.md` vs `PORTFOLIO_UNIVERSE.md`
  (working view / intent / inventory — three "portfolio" nouns; mostly
  complementary but easy to confuse).
- `PORTFOLIO_BASELINE.md` (historical) vs current CONTROL records.
- SJC `docs/planning/` vs old `ivy-control` tree standards (three locations).
- `DATABASE.md` consolidates architecture/operations/migrations/backup for all
  workloads — a large single file that mixes per-workload history.
- Next-task state duplicated across ROADMAP/BACKLOG/CONTROL.md next_task/
  architect memory.
- New-doc governance rule exists (`docs/README.md` §Repository Documentation
  Contract) but has not been applied to the sprawl.

## 28. Recommended Ivy authority hierarchy

One authority per concern, clear entrypoint, clear per-repo record:

1. **Entrypoint:** `docs/README.md` (exists; keep as the map).
2. **Intent:** `PORTFOLIO_INTENT.md` (Buddy-only).
3. **Portfolio working view:** `PORTFOLIO.md`.
4. **Portfolio inventory:** `PORTFOLIO_UNIVERSE.md` (asset universe).
5. **Portfolio roadmap/sequencing:** `ROADMAP.md`.
6. **Operating model:** `OPERATING_MODEL.md`.
7. **Repository governance model:** `REPOSITORY_CONTROL_MODEL.md`.
8. **Shared technical conventions:** `PORTFOLIO_CONVENTIONS.md` (absorb the
   gate-like items from `VPS_ADMISSION_CHECKLIST.md`, leaving a pure evidence
   checklist).
9. **Data lifecycle / backup standards:** `DATA_LIFECYCLE_STANDARD.md` +
   `BACKUP_MANIFEST_STANDARD.md` (one each; no new docs).
10. **Health:** `HEALTH_CONTRACT.md` + `health/` registry.
11. **Per-repo control:** `repos/<repo>/CONTROL.md` (lifecycle, gates, SHA,
    blockers).
12. **Per-repo gate evidence:** `repos/<repo>/RELEASE_GATES.md` (create for
    SJC; reconcile for Reckless Ben later).
13. **Task/report flow:** stays in each project repo; Ivy tracks gate state,
    not project tasks.

## 29. Strong Codex task specification

**Task proposal (later task file): "Consolidate Ivy documentation and
operational workflows; reconcile SJC; audit live VPS storage; productize
reusable onboarding; prepare Reckless Ben."**

Scope:

1. **Ivy documentation consolidation** — inventory all active authorities
   (working memory, repository-control model, VPS admission checklist,
   portfolio conventions, database docs, lifecycle docs, backup manifest docs,
   per-repo control files, per-repo release gates, private runbook, onboarding
   evidence); identify conflicts/duplicates; define one authority hierarchy
   (report §28); consolidate or deprecate documents; preserve public/private
   boundaries; reduce stale state; define what belongs in per-repo control
   records vs shared standards; avoid tracking project tasks/reports in Ivy.
2. **SJC reconciliation** — update `repos/sjc-intel/CONTROL.md` (remote,
   approved SHA `1be2ade`, gate table per report 15 §6/§20.3); create
   `RELEASE_GATES.md` (Gate 1 PASSED_NOT_RECORDED, Gates 2–3 PARTIAL/
   PASSED_NOT_RECORDED, Gates 4–6 NOT_STARTED); record actual remote + approved
   SHA; record backup deferral; record PostgreSQL DORMANT_FUTURE_READY; record
   static launch VPS-independence; record current operational blockers; apply
   the backup-disposition checklist item (report 14 §12).
3. **Live VPS storage audit** — verify disk use (`df -h`, `du` per workload)
   via approved Mode 2; identify large consumers (WGU-Reddit, backup,
   Launchpad, Chrome/collector, browser caches, journals, PostgreSQL); classify
   durable/temporary/cache/logs/backups/browser/PostgreSQL/releases/checkouts/
   venv; propose safe cleanup (dry-run); define per-repo storage budgets,
   reserve thresholds (85%/1GB), temporary-data retention, minimal UI-serving
   state; verify reboot status; avoid disrupting unrelated workloads.
4. **Reusable onboarding** — turn SJC lessons into templates: gate-update
   requests, exact-SHA workflow, data-authority declaration, VPS-storage
   declaration, database disposition, backup disposition, task declaration,
   near-future timer proof, natural-run proof, transfer/receipt/prune proof,
   offboarding.
5. **Reckless Ben preparation** — inspect the existing control record
   (`repos/reckless-ben/CONTROL.md`); identify missing intake data (report 15
   §22 checklist with `[TBD]`s); create a bounded onboarding packet reusing SJC
   generic patterns (bundle/import/receipt, task declaration, deterministic
   runner, minutes-from-now test, backup-policy shape) without copying
   domain-specific artifacts; sequence work to begin immediately after Ivy
   consolidation.
6. **Privileged SJC operational work** (where safe and authorized): deploy
   approved SHA; install service/timer disabled; run minutes-from-now proof;
   verify deterministic Stage A; verify bundle creation; verify Mac
   pull/import/receipt; test prune eligibility; register health; verify
   rollback; leave activation gated.

Validation: Ivy `git diff --check`; parse CONTROL.md front-matter;
`tools/show_portfolio_status.sh`; SJC `validate.py` + `pytest` + corpus
validator re-run after any cross-repo handoff; capacity evidence card.

This is an **execution + consolidation** task, not another abstract assessment:
it consolidates, corrects, executes safe operational work, and leaves exact
follow-ups.

## 30. SJC reconciliation requirements

- `CONTROL.md`: remote `https://github.com/wguDataNinja/sjc-intel.git`,
  approved SHA `1be2ade2ad600627e69bca382e47af54a4690363`, gate table
  reconciled (report 15 §6), blockers updated to current editorial/scope
  blockers, next_task updated.
- Create `repos/sjc-intel/RELEASE_GATES.md`.
- Record: backup deferral; PostgreSQL DORMANT_FUTURE_READY; static launch
  independence from VPS; current operational blockers; project authority
  preserved (ROADMAP §6A).
- Apply the backup-disposition gate (report 14 §12 patch).

## 31. VPS storage-audit requirements

Mode-2 live audit: `df -h` + per-workload `du`; classify durable vs temporary
vs cache vs logs vs backups vs browser state vs PostgreSQL vs releases vs
checkouts vs venv; safe-cleanup candidate list (dry-run) with thresholds
(<75% nominal, 75–85% warning, 85–90% critical, >90% emergency);
per-repo storage budgets; temporary-data retention; minimal UI-serving state
(none for SJC launch — static host); reboot status verification; no disruption
to unrelated workloads. Output: dated evidence card + cleanup packet for Buddy
gate (report 15 §26).

## 32. Reusable onboarding requirements

Templates to productize from SJC: gate-update request; exact-SHA pin +
deploy manifest; data-authority declaration (Mac vs VPS); VPS-storage
declaration; PostgreSQL disposition (NOT_USED/DORMANT/OPERATIONAL_METADATA);
backup disposition (scope → first backup → checksum → restore path → restore
test); task declaration (repo manifest, disabled); near-future timer proof
(minutes-from-now one-shot); natural-run proof; transfer/receipt/prune proof
(bundle + receipt + delayed prune); offboarding. Each names owner
(project/Ivy), evidence, gate-vs-checklist classification (report 15 §21).

## 33. Reckless Ben preparation

Existing control record: local-only, `approved_sha: d6b99f77`, dirty working
tree since early July, gates PARTIAL/UNKNOWN, `NO_LAUNCH` superseded by
"promoted to current work 2026-08-02", currently stopped at high-reasoning
gates C1 (DB campaign go/no-go), C4 (Buddy incremental execution scope),
C2 (dashboard Stage 4 design). Missing intake data per report 15 §22:
repo location confirmed (`/Users/buddy/projects/reckless_ben`), purpose,
public/private target, git status/remote, data classes, durable authority,
runtime, network/secrets, database role, VPS role, UI needs, backup
disposition, scheduling, health, rollback, publication target. Onboarding
packet should reuse SJC generic patterns (bundle/import/receipt,
task-declaration shape, deterministic-runner pattern, minutes-from-now test,
backup-policy shape) without copying Reckless-Ben-specific domain artifacts;
sequence to begin immediately after Ivy consolidation.

## 34. Remaining medium-agent tasks

| Task | Dependency | Outcome | Blocker? | Report |
|------|-----------|---------|----------|--------|
| Editorial review pass (Buddy/human) | none | resolve 78 pending → verified/rejected_noise | **Yes** | — |
| silverleaf-scope-registry (§3B-G1) | Buddy scope approval (§19) | inclusion/exclusion registry + per-item relevance decisions | **Yes** | reports/17-… |
| static-public-export (§3B-G2) | §3B-G1 | release.json/search-index/manifest per `docs/static_release_data_contract.md` | **Yes** | reports/18-… |
| portfolio-integration (§3C-G1) | site authority (§22) | target-repo context packet | Yes (deploy route) | reports/19-… |
| static SilverLeaf UI (§3C-G2) | §3C-G1 | pages per `docs/public_ui_v0_spec.md` | Yes | reports/20-… |
| extract-bcc-workspace-mode | none | BCC workspace-safe | No | reports/… |
| record per-item publication decisions | editorial approval | `publication_decision.py` for approved items | Yes | — |
| public presentation polish | after first release | screenshots/diagram/privacy note | No | reports/… |

## 35. Remaining Buddy/GPT decisions

1. Editorial review of the 78 pending items (the real launch gate).
2. SilverLeaf scope approval (§19 packet): neighborhoods, aliases, access
   roads, serving schools, adjacency rules, countywide-material-impact rule.
3. Sensitive/crime policy (default: exclude; v0 launches without crime items).
4. Release window (30 vs 60 days).
5. First-release set approval (§21).
6. Portfolio-site repo location + integration authority (§22).
7. Public-claims review and publish language.
8. Backups: destination (deferred); provider-neutral policy ready.
9. Strong Codex/Ivy consolidation authorization (report §29).

## 36. Remaining Strong Codex/privileged work

- Ivy documentation consolidation + SJC CONTROL.md/RELEASE_GATES.md
  reconciliation (§29–30).
- Live VPS storage audit (§31).
- Reusable onboarding productization + Reckless Ben packet (§32–33).
- Privileged SJC operational packet: exact-SHA deploy, disabled service/timer,
  minutes-from-now proof, bundle/import/receipt/prune proof, health, rollback,
  activation gated (§29.6).
- Static publication needs no VPS.

## 37. Risks and unresolved issues

- **Editorial backlog (78 pending)** is the true launch gate — human effort,
  not code.
- **Crime/safety items** excluded by default; any exception is a
  public-reputation risk.
- **SilverLeaf scope authority missing** (boundary, streets, schools,
  I-95 segments) — the §3B-G1 registry is seeded but the authoritative
  geography decisions (DIR-001/009/010/011) remain open.
- **`rural_sjc` unregistered community reference** — flagged as a legacy
  exception; needs a registry addition or field fix (do not silently register).
- **Stale Ivy CONTROL.md + absent RELEASE_GATES.md** could mislead operators;
  reconcile before any deployment claim.
- **Portfolio-site repo undiscovered** — UI integration cannot be specified
  until located (§22).
- **Corpus warnings (320)** are legacy-only; new items must meet the strict
  contract (validators will catch drift).
- **NBOR 06-08 duplicate capture** documented non-canonical; a future cleanup
  task may consolidate, but nothing here alters it.

## 38. Final Git status

SJC `master` @ `1be2ade`, origin/master == local (0/0). Working tree: intended
Task 16 files (scripts, schema, data/publication_decisions, docs, tests,
fixtures, log) + pre-existing dirty data files + Tasks 12–15 outputs. Nothing
staged, committed, or pushed. Ivy untouched (read-only; 17 pre-existing dirty
lines preserved).

## 39. Final task status

| Area | Status |
|------|--------|
| Publication-decision model | COMPLETE |
| Operator decision tooling | COMPLETE |
| Complete corpus validation | COMPLETE |
| Legacy exception registry | COMPLETE |
| Deterministic publication selector | COMPLETE |
| Tests + negative cases | COMPLETE (21 new) |
| Resident-perspective corpus review | COMPLETE |
| v0 UI specification | COMPLETE |
| Static UI data contract | COMPLETE |
| SilverLeaf scope decision packet | COMPLETE (decision-ready) |
| Editorial packet update | COMPLETE |
| Portfolio-site context discovery | COMPLETE (repo not discoverable; packet requested) |
| Ivy retrospective consolidation | COMPLETE |
| Strong Codex task specification | COMPLETE |
| SJC reconciliation requirements | COMPLETE (documented) |
| VPS storage-audit requirements | COMPLETE (documented) |
| Reusable onboarding requirements | COMPLETE (documented) |
| Reckless Ben preparation | COMPLETE (documented) |
| Publication decisions / release | AWAITING BUDDY (none made) |
| Ivy consolidation / VPS storage audit | BLOCKED (privileged) |
| §3B-G1 registry / §3B-G2 export / §3C UI | READY_FOR_MEDIUM_AGENT |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP — the publication
foundation, resident UI discovery, scope packet, and Strong Codex task are
complete and validated; remaining work is exactly: human editorial review +
item approval, SilverLeaf scope approval, static export, UI implementation
(blocked on locating the portfolio-site repo), and the privileged Ivy/VPS
packet. No further broad SJC product or architecture discovery is required.
