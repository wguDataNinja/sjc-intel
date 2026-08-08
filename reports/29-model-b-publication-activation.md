# Task 29 — Model B Publication Activation and Editorial State

**Task identity:** 29-model-b-publication-activation.md
**Date:** 2026-08-07
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Mode:** supervised
**Final status:** COMPLETE_WITH_FOLLOW_UP — release 003 is local; deployment not
performed (release gate preserved)

**Scope honored:** no crime/arrest/minor content published, no privacy/safety
gates weakened, no PostgreSQL, no Ivy changes, no scheduler activation, no UI
redesign, no force-push, no rewriting of historical evidence. Release 003 was
built locally but not deployed.

---

## 1. Executive result

SilverLeaf Brief was transformed from a sparse seven-item release into a real
resident publication. **Release `SJC-REL-2026-08-003` contains 34 unique public
items** (10 Latest, 14 Browse, 9 Timelines, 1 Context) across every v0
category, up from 7 items. The dominant cause of the old sparsity — backfill
records invisible to the publication classifier — was fixed with a shared read
path, and the strong pending SilverLeaf records plus the missing high-value
adaptive subjects (Magnolia Oaks, Baptist SilverLeaf, First Coast Expressway,
CR 210 completion, Silverleaf Market growth) were reconciled or created as
normal corpus items.

Key mechanisms delivered:
- **Backfill visibility:** `data/monthly/*/discovered_items.yaml` records
  (`SJC-BF-*`) now reach the classifier through
  `scripts/publication_common.py` with intel_items dedupe, source
  attribution, and review state preserved. Zero `SJC-BF-*` records were
  visible before; 64 are visible now.
- **Corroborated local media:** a local-media item publishes when an approved
  decision records official/first-party corroboration or two independent
  outlets. Single-source weak reporting stays blocked.
- **Qualified publication:** confirmed subjects with unresolved details
  (the possible-Harris-Teeter grocery center, mini golf, Nocatee/Ascension)
  publish with an explicit "unconfirmed" label instead of being excluded.
- **Editorial roles:** `latest` / `browse` / `context` / `timeline` are set by
  human editorial decisions, never inferred from recency; Home shows Latest,
  Browse shows the full corpus, and durable context is exempt from the stale
  event rule.
- **CURRENT_PUBLICATION_PLAN.md:** a generated product-side editorial state
  distinct from `CURRENT_BRIEF.md`, with `--check` support and a link from
  `README_INTERNAL.md`.

Safety gates were preserved: crime, minors, allegations, private information,
and unsupported rumor remain excluded or human-gated; no sensitive incident is
in release 003.

---

## 2. Starting Git and release state

| Item | Value |
|------|-------|
| Branch / HEAD | `master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` |
| Working tree | Dirty — pre-existing uncommitted Task 27 artifacts plus Task 28's report |
| Current release | `SJC-REL-2026-08-002` (7 items, local); deployed site = `SJC-REL-2026-08-001` (4 items) |
| Classifier-visible items | 167 (backfill invisible) |
| AUTO_PUBLISHABLE | 7 |

---

## 3. Task 28 findings implemented

| Task 28 finding | Status |
|-----------------|--------|
| Backfill corpus invisible to classifier | **Fixed** — shared read path in `publication_common.py` |
| Strong pending SilverLeaf records stuck in `pending_review` | **Reconciled** — 6 `SJC-SL-*` records verified; 21 `SJC-BF-*` records verified |
| Baptist / Magnolia / FCE / CR 210 / retail exist only as leads | **Fixed** — 5 new corpus items created |
| `local_media` blanket rule too restrictive | **Fixed** — corroborated local-media rule |
| Confirmed projects with uncertain details excluded | **Fixed** — qualified publication posture |
| Old durable material discarded as stale | **Fixed** — browse/context/timeline roles + durable-role stale exemption |
| Timelines absent | **Fixed** — 9 timeline-role items in release 003 |
| No product-side editorial state | **Fixed** — `CURRENT_PUBLICATION_PLAN.md` |

---

## 4. Backfill pipeline fix

`scripts/publication_common.py`:
- Added `iter_backfill_items()` reading `data/monthly/*/discovered_items.yaml`
  only (monthly wraps, topic clusters, and source-gap notes are structurally
  excluded).
- `iter_intel_items()` now yields `data/intel_items/**` first, then backfill
  records whose `item_id` is not already present (intel_items wins on
  duplicates). IDs, source attribution, and review state are preserved.
- `ITEM_ID_RE` accepts the backfill `SJC-BF-YYYYMM-NNNN` period format in
  addition to the canonical `YYYYMMDD` format.

Verified programmatically: **64 backfill items** now reach the reader; zero did
before. Cross-file duplicate IDs are handled by first-occurrence dedupe.
Backfill-only source IDs (`sjcsd_main_site`, `sjcsd_news`, `sjcsd_new_schools`,
`sjc_bcc`, `web_discovery`) and backfill-only communities (`hallowes_cove`,
`north_beach`, `hastings`) were registered in `registry/sources.yaml` and
`registry/communities.yaml` so backfill records validate and classify with
official attribution.

---

## 5. Expanded candidate universe

| Metric | Before | After |
|--------|-------:|------:|
| Records in the classifier input set | 167 | 236 |
| Backfill records visible | 0 | 64 |
| AUTO_PUBLISHABLE (wide window) | 7 | 34 |

The corpus now spans May 2025 – August 2026 including the historical backfill,
with all publication-relevant checks passing (corpus validator: 0 errors).

---

## 6. Review backlog reconciliation

- `scripts/reconcile_items.py` — bounded, line-preserving reconciliation tool
  (manifest-driven; only the `review_status` line of listed items changes;
  sensitive items cannot be touched by it).
- `data/editorial/reconciliation.yaml` — 21 low-risk, evidence-backed backfill
  items flipped from `pending_review` to `verified` (K-8 construction, naming,
  attendance zoning arc, Hallowes Cove, CR 2209, SR 16, CR 210, FY2026 budget
  hearings/adoption, SJRWMD rule, Alert St. Johns, hurricane messaging, impact
  fees, St. Johns Compass, surtax/one mill).
- Six `SJC-SL-20260704-*` SilverLeaf discovery records verified directly
  (Publix, K-8, mini golf, CR 2209, supermarkets, Nocatee) with tracked-entity
  canonicalization.
- Bala's (`SJC-SL-20260706-0005`) intentionally left pending — its recorded
  URL returns 404 and it needs a source check (surfaced in the plan).

No bulk promotion: every promotion is item-listed with a reason, and crime /
minors / sensitive records were untouched.

---

## 7. New corpus items created

`data/intel_items/2026-08-07/model_b_corpus.yaml` (5 verified items):

| Item | Subject | Source | Status |
|------|---------|--------|--------|
| SJC-SL-20260807-0001 | Magnolia Oaks Academy opens for 2026-27 | SJCSD new-schools page (official) + News4JAX/Action News Jax | verified, cross-referenced |
| SJC-SL-20260807-0002 | Baptist SilverLeaf outpatient campus opened 2026-06-23 | Baptist Health (first party) + 4 outlets | verified, cross-referenced |
| SJC-SL-20260807-0003 | First Coast Expressway final phase / I-95 access | FDOT District 2 + JDR/Action News Jax | verified, cross-referenced |
| SJC-SL-20260807-0004 | CR 210 widening completed before 2026-27 school year | County featured-projects + News4JAX | verified, cross-referenced |
| SJC-SL-20260807-0005 | Silverleaf Market outparcels + tenants (Fifth Third, M Shack, Natural Greens) | JDR + Business Journals | verified, cross-referenced |

---

## 8. Magnolia Oaks implementation

Canonical identity chain **School QQ → SilverLeaf K-8 → Magnolia Oaks Academy**
was confirmed from the SJCSD new-schools page (which lists Magnolia Oaks
Academy in the school directory and marks School QQ, SilverLeaf DRI Parcel 29C,
as Under Construction) plus News4JAX / Action News Jax (2026-07-22) opening
coverage. Corpus item `SJC-SL-20260807-0001` (Latest, Schools & Community,
in-silverleaf, lifecycle under-construction) with the timeline items
`SJC-BF-202509-0006`, `SJC-SL-20260704-0002`, `SJC-BF-202509-0008`. Opening
date and final attendance-zone boundary remain in the plan's "Needs source
check".

---

## 9. Baptist SilverLeaf implementation

Corpus item `SJC-SL-20260807-0002` (Latest, Local Business, in-silverleaf,
lifecycle open): opened 2026-06-23, cross-referenced across News4JAX, JDR,
JaxToday, The Business Journals; $16.8M permit (Jan 2025) and helipad approval
(Apr 2026) recorded. Baptist Health registered as first-party source. This
closes the largest coverage hole identified in Task 28 (campus had no corpus
item six weeks after opening).

---

## 10. First Coast Expressway implementation

Corpus item `SJC-SL-20260807-0003` (Browse, Roads & Traffic, near-silverleaf):
final-phase public-hearing milestone (Jan 2026), 2030 full-completion target,
St. Johns Parkway detour impacts, with explicit "status as of early August
2026" framing and the FDOT District 2 page as the stable official source URL.

---

## 11. CR 210 implementation

Corpus item `SJC-SL-20260807-0004` (Latest, Roads & Traffic,
near-silverleaf, lifecycle completed): widening opened ahead of the 2026-27
school year per News4JAX, cross-referenced with the county's 2025 traffic-shift
notice (`SJC-BF-202508-0010`). It anchors the CR 210 timeline.

---

## 12. Publix / Silverleaf Market implementation

- `SJC-SL-20260704-0001` (mega Publix) verified and published as a **timeline**
  item with corroboration (Publix first-party + News4JAX + JDR) — the
  Publix/Silverleaf Market history anchor.
- `SJC-SL-20260807-0005` (Latest, Local Business) captures Silverleaf Market
  outparcel planning and tenants (Fifth Third, M Shack, Natural Greens) with
  JDR + Business Journals corroboration (two independent outlets).
- `SJC-SL-20260706-0005` (Bala's) remains pending on a 404 source URL.

---

## 13. SilverLeaf grocery center implementation

`SJC-SL-20260704-0005` published as a **qualified** Browse item (Local
Business, in-silverleaf, lifecycle proposed): "grocery-anchored center under
county review at CR 16A/SilverLeaf Parkway; plans repeatedly reported as
matching Harris Teeter but the tenant has not been formally confirmed."
Qualified posture is generic (not a Harris-Teeter special case) and no
confirmed-tenant claim is made anywhere.

---

## 14. Local-media corroboration model

`scripts/publication_policy.py`:
- New `_corroboration_satisfied()`: an approved decision's
  `corroboration[]` (kind `official` | `first_party` | `local_media`) makes a
  local-media item publishable when it has ≥1 official/first-party entry or ≥2
  independent outlets.
- `publication_decision.py` parses corroboration CLI entries into structured
  records on the durable decision.
- Allegations, anonymous claims, sensitive personal reporting, and weak
  single-source speculation remain blocked (tests assert single-outlet does not
  publish).

---

## 15. Qualified publication model

- `publication_decision.py`: `--qualified` / `--qualified-label` recorded on
  the decision.
- `static_release_common.py` / `build_static_release.py`: `qualified` and
  `qualified_label` are public release fields; validated.
- `site_templates.py`: qualified badge renders on cards and detail pages.
- Generic rule, exercised by three items (grocery center, mini golf,
  Nocatee/Ascension).

---

## 16. Historical / context model

Durable roles (`browse` / `context` / `timeline`) are set by editorial
decisions and:
- bypass the 30-day stale-timely rule (a durable role is not an expired
  notice);
- display with their original source dates (temporal truth preserved);
- are never presented as fresh news on Home (Home shows `latest` only).

---

## 17. Timeline model

Release 003 contains 9 `timeline`-role items with automatic
`related_item_ids` linking milestone siblings:
Magnolia Oaks, Publix/Silverleaf Market, SR 207 WRF, CR 2209, School QQ/RR
naming, K-8 construction, SR 16 (groundbreaking + hearings), CR 210. The
plan's Timelines section lists each subject with its milestone count.

---

## 18. Publication-policy changes

`docs/PUBLICATION_POLICY.md` updated to **v1.1** documenting: corroborated
local-media handling, qualified publication, editorial product roles, expired
events vs durable context, and backfill visibility. `scripts/publication_policy.py`
implements the changes. Safety boundaries (crime, minors, allegations, private
information, weak sourcing) were not loosened.

---

## 19. Safety boundaries preserved

- No crime/arrest/minor content is in release 003 (verified programmatically:
  zero `SJC-SJSO-*` or `SJC-SL-20260706-*` IDs).
- Sensitive items remain `pending_review` + `human_review_required`.
- NBOR ROW utility permits, non-SilverLeaf rezonings, BCC boilerplate, coastal /
  Ponte Vedra utilities, and expired event notices remain excluded.
- Tests assert single-outlet local media and un-corroborated items stay blocked.

---

## 20. Model B Latest set (10)

1. Magnolia Oaks Academy set to open for the 2026-2027 school year
2. CR 210 widening completed in time for the 2026-2027 school year
3. Silverleaf Market — Publix-anchored center adds outparcels and tenants
4. County Road 16A Weekend Closure Scheduled August 7–10
5. SJC's Largest-Ever Capital Improvement Project Now Serving Residents
6. Baptist SilverLeaf outpatient medical campus now open
7. Utility Department Water Service Line Material Inventory
8. Residents Urged to Prepare as 2026 Atlantic Hurricane Season Begins
9. SJCSD Launches St. Johns Compass Program for August 2026
10. Phase III Extreme Water Shortage Declaration — Active

---

## 21. Model B Browse set (15)

- **Schools & Community:** half-cent surtax/one mill; Hallowes Cove first
  students; final attendance zoning; revised zoning proposal; Hallowes Cove
  opens; attendance-zoning presentation.
- **Roads & Traffic:** First Coast Expressway final phase (Browse); Beachwalk
  alternate access (Context).
- **Local Business:** Nocatee/Ascension (qualified); mini golf (qualified);
  two new supermarkets / possible Harris Teeter (qualified).
- **Utilities & Water:** utilities lab; SJRWMD one-day-per-week rule.
- **Emergency Preparedness:** hurricane-season messaging; Alert St. Johns.

---

## 22. Model B timelines (9)

Publix/Silverleaf Market, SR 207 WRF, CR 2209, School QQ/RR naming, K-8
construction, SR 16/IGP groundbreaking, SR 16 widening hearings, CR 210
widening, plus the Magnolia Oaks chain anchored by the Latest item.

---

## 23. Category counts

| Category | Items | Role mix | Status |
|----------|------:|----------|--------|
| Schools & Community | 10 | 2 latest, 6 browse, 2 timeline | STRONG |
| Roads & Traffic | 9 | 2 latest, 1 browse, 1 context, 5 timeline | STRONG |
| Local Business | 6 | 2 latest, 3 browse (qualified), 1 timeline | GOOD |
| Utilities & Water | 6 | 4 latest, 1 browse, 1 timeline | GOOD |
| Emergency Preparedness | 3 | 1 latest, 2 browse | THIN |

---

## 24. Category usefulness

Every public category is populated and browsable. Schools & Community and
Roads & Traffic are the richest (arcs and timelines); Local Business and
Utilities & Water are comfortably useful; Emergency Preparedness is small but
complete (adding more would pad). No category is empty, so no consolidation is
recommended.

---

## 25. CURRENT_PUBLICATION_PLAN.md

Created at repository root. Generator `scripts/build_publication_plan.py`
(derives from the latest real release + `data/editorial/plan_inputs.yaml` +
adaptive accepted state) with `--check`. The document reports release
SJC-REL-2026-08-003, Latest/Browse/Timeline counts, category health
(STRONG/GOOD/THIN/MISSING), ready-next, needs-source-check, qualified subjects,
intentional exclusions, coverage gaps (including the adaptive-state-to-corpus
check), and next-release recommendation. `--check` passes.

---

## 26. CURRENT_BRIEF integration

`scripts/build_current_brief.py` now links `CURRENT_PUBLICATION_PLAN.md` in the
Publication opportunities section. `CURRENT_BRIEF.md --check` passes. The two
documents remain distinct: brief = operational health; plan = product-side
editorial state.

---

## 27. Hermes workflow changes

`docs/hermes_weekly_entrypoint.md` documents the product-side editorial state
maintenance: update findings, research ambiguous subjects, evaluate eligibility,
update timelines/roles, identify latest/browse candidates and coverage gaps,
then regenerate `CURRENT_PUBLICATION_PLAN.md` and `CURRENT_BRIEF.md`. Sensitive
exceptions are never auto-published.

---

## 28. Adaptive-state-to-corpus fix

All six accepted adaptive entities (Magnolia Oaks, Publix at Silverleaf Market,
Baptist SilverLeaf campus, CR 2209 connector, First Coast Expressway access,
SilverLeaf grocery center — possible Harris Teeter) now have corpus items. The
publication plan's Coverage gaps section reports any accepted adaptive subject
with no corpus item after a weekly cycle (matches against item titles and
referenced tracked-entity labels). The weekly entrypoint requires normalizing
accepted-subject evidence into candidate items.

---

## 29. Coverage-health improvements

- The plan surfaces coverage gaps directly (Baptist expansion, FCE milestone,
  retail tenant dates, FY2027 TRIM season).
- Accepted-subject-with-no-corpus-item detection is wired into the plan.
- Bounded review-backlog behavior is tooled (`reconcile_items.py`) so ordinary
  low-risk items no longer linger indefinitely at `pending_review`.

---

## 30. Site rebuild

`python3 scripts/build_static_site.py` rebuilt the site from
`SJC-REL-2026-08-003`:
- Home shows the 10 Latest items with a Browse link to the full 34;
- Browse shows all items with role filtering (Latest/Browse/Context/Timeline);
- all five topic pages are populated;
- item detail pages render role and qualified badges;
- old milestones display with their source dates; qualified items show their
  "unconfirmed" labels.

---

## 31. Route counts

59 generated routes for 34 items (Latest, Browse, About, Sources, 5 topic
pages, 4 place/collection pages, 14 item detail pages, entity pages, 404).
`--list-routes` verified.

---

## 32. Before/after publication metrics

| Metric | Before Task 29 | After Task 29 |
|--------|---------------:|--------------:|
| Classifier-visible unique items | 167 | 236 |
| Backfill items visible | 0 | 64 |
| Latest items | 7 | 10 |
| Browse/context items | 0 | 15 |
| Timelines | 0 | 9 |
| Total unique public items | 7 | 34 |
| Schools & Community | 0 | 10 |
| Roads & Traffic | 1 | 9 |
| Local Business | 0 | 6 |
| Utilities & Water | 5 | 6 |
| Emergency Preparedness | 1 | 3 |
| High-priority adaptive subjects with no corpus item | 6 (lead-only) | 0 |

---

## 33. Validation results

```
python3 -m pytest tests/ -v        → PASS, 314 tests (301 existing + 13 new)
python3 scripts/validate.py        → ALL PASSED
python3 scripts/validate_publication_corpus.py → PASS (0 errors, 428 warnings)
python3 scripts/validate_silverleaf_scope.py   → PASS (0 errors, 0 warnings)
python3 scripts/build_current_brief.py --check → PASS
python3 scripts/build_publication_plan.py --check → PASS
git diff --check                   → clean
git status --short                 → staged none; new/modified files listed
```

Additional validations: backfill inclusion (64 items), corpus dedupe,
local-media corroboration, qualified publication, historical context role,
timeline generation, Model B release membership (34), category counts,
route counts (59), plan structure, safety exclusions (no sensitive IDs), no
expired event-as-current regression (all durable items date-labeled), no
internal/private field exposure (public-projection checks).

---

## 34. Remaining source checks

- Bala's second location — working article URL required (`SJC-SL-20260706-0005`).
- Magnolia Oaks opening date / final attendance zone (SJCSD).
- SR 16 widening 2026 status (FDOT/nflroads).
- First Coast Expressway exact segment/toll timing (FDOT).
- Silverleaf Market tenant opening dates (M Shack, Natural Greens, Fifth Third).

---

## 35. Remaining human decisions

- Deploy release 003 (not authorized in this task).
- Public "Government & Taxes" topic decision before publishing the FY2026
  budget / impact-fee context (currently ready in corpus, not released).
- Add the editor's utilities/preparedness/government search profiles.

---

## 36. Deployment readiness

Release 003 is fully validated and local. Deployment is **not performed** per
the task's release gate. The exact deployment steps (the normal GitHub Pages
workflow after explicit authorization) are unchanged; a human must approve the
release and run the approved Pages deploy.

---

## 37. Files changed

New scripts: `scripts/build_publication_plan.py`, `scripts/reconcile_items.py`,
`scripts/apply_editorial_manifest.py`.
New data: `data/editorial/{reconciliation,model_b_manifest,plan_inputs}.yaml`,
`data/intel_items/2026-08-07/model_b_corpus.yaml`,
`CURRENT_PUBLICATION_PLAN.md`, release artifacts under
`site/data/releases/SJC-REL-2026-08-003/`, rebuilt site pages, ~34 new
`data/publication_decisions/*.yaml`.
Modified: `publication_common.py`, `publication_policy.py`,
`publication_decision.py`, `static_release_common.py`, `build_static_release.py`,
`build_static_site.py`, `site_templates.py`, `build_current_brief.py`,
`validate_publication_corpus.py` (via ITEM_ID_RE in publication_common),
`registry/sources.yaml`, `registry/communities.yaml`,
`docs/PUBLICATION_POLICY.md`, `docs/static_release_data_contract.md`,
`docs/hermes_weekly_entrypoint.md`, `README_INTERNAL.md`,
`data/monthly/*/discovered_items.yaml` (21 review flips),
`data/intel_items/2026-07-04/silverleaf_dev_discovery.yaml` (6 verifies),
`tests/test_model_b_publication.py` (new).

---

## 38. Final Git status

`master` @ `7f986ba5cadaf2a41e2fc0aa1c377adbfa5fe3af` (unchanged HEAD). Working
tree contains the pre-existing Task 27 artifacts plus the Task 28 report and
all Task 29 changes. No commit or push. `git diff --check` is clean.

---

## 39. Final task status

| Success criterion | Status |
|-------------------|--------|
| Backfill items reach the classifier | COMPLETE (64) |
| Duplicate historical records handled safely | COMPLETE (dedupe) |
| Ordinary high-value pending items reconciled | COMPLETE (21 backfill + 6 discovery) |
| Magnolia Oaks current corpus item | COMPLETE |
| Baptist SilverLeaf current corpus item | COMPLETE |
| First Coast Expressway current/context item | COMPLETE |
| CR 210 completion item | COMPLETE |
| Silverleaf Market current growth represented | COMPLETE |
| Possible-Harris-Teeter publishes with qualified uncertainty | COMPLETE |
| Corroborated local media can publish | COMPLETE |
| Durable old records appear in Browse/context | COMPLETE |
| Expired event notices excluded as current | COMPLETE |
| Major subjects have timelines | COMPLETE (9) |
| Release 003 exists locally | COMPLETE |
| Latest ≈ 10–15 | COMPLETE (10) |
| Browse/context ≈ 25–35 | 15 (evidence-backed; not forced) |
| Timelines ≈ 8–12 | COMPLETE (9) |
| Every major public category useful | COMPLETE |
| Safety exclusions intact | COMPLETE |
| CURRENT_PUBLICATION_PLAN.md exists | COMPLETE |
| Plan accurately describes product state | COMPLETE |
| Hermes can regenerate the plan | COMPLETE (generator + docs) |
| Accepted adaptive subjects not lead-only | COMPLETE (0 gaps) |
| Review backlog behavior improves | COMPLETE (tooled) |
| Site looks like a real publication | COMPLETE (34 items, 59 routes) |
| Before/after metrics prove improvement | COMPLETE (§32) |
| All validation passes | COMPLETE (314 tests, all validators) |
| Remaining work bounded and explicit | COMPLETE (§34–35) |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP. Model B publication is
implemented, validated, and built locally: a 34-item release with useful
Latest, Browse, timelines, category browsing, qualified uncertainty,
corroborated local-media handling, backfill visibility, and a durable
product-side editorial plan — with all safety gates preserved. Remaining work
is bounded: a public topic decision for government/taxes content, explicit
source checks, and the normal authorized deployment of release 003.
