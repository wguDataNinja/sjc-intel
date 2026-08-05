# Task 18 — First Real Release Preparation and Portfolio Integration

**Task identity:** 18-first-release-and-portfolio-integration.md
**Date:** 2026-08-04
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`, implementation);
`wguDataNinja/buddyowens-site` (portfolio repo, **read-only**, GitHub);
`ivy-control-vps` (read-only).
**Final status:** COMPLETE_WITH_FOLLOW_UP

---

## 1. Executive result

SilverLeaf Brief is now **one bounded decision/deployment step from a public
v0**. This task replaced demo assumptions with real SJC evidence, finalized the
launch-ready SilverLeaf scope registry, prepared a small first-release editorial
packet with exact (non-executed) publication commands, proved the real release
path nonmutatingly in a sandbox, and identified the exact portfolio integration
route.

Delivered:

- **Visual/functional review** of the Task 17 v0; one real layout defect fixed
  (item-detail pages lost the page gutter) plus objective polish; mobile
  "overflow" reported by an automated vision reviewer was disproved with real
  layout metrics.
- **SilverLeaf scope registry** (`registry/silverleaf_scope.yaml`) — launch-ready
  minimum with verified / inferred / editorial-policy / needs-review provenance,
  stable IDs, no GIS claims; schema, `scripts/validate_silverleaf_scope.py`,
  8 tests, `validate.py` §10.
- **First-release candidate set** — a recommended 4-item core
  (water shortage, hurricane preparedness, service-line inventory, CR 16A
  closures) with a conditional/orientation tier; every candidate classified
  READY_TO_APPROVE / READY_AFTER_COPY_EDIT / READY_AFTER_SOURCE_CHECK /
  DEFER / EXCLUDE / BUDDY_DECISION.
- **Exact publication commands** (not executed) including copy-edit overrides
  (`--public-summary-override`, `--relevance`, event/lifecycle flags added to
  the operator tool); a **simulated post-approval release** proven end-to-end
  in a sandbox: 4 items, correct relevance labels, overrides honored, 17 routes,
  checksums verified, no internal leaks.
- **Selector fix**: legacy exceptions with `warning_timestamp_default` treatment
  no longer block release (the 5 fresh 2026-08-02 items were previously
  unreleasable); blocking treatments still exclude.
- **Portfolio repository identified**: `wguDataNinja/buddyowens-site`
  (Hugo + PaperMod, GitHub Pages). Integration approach selected:
  **copy the generated static output into the portfolio's public directory**
  (`static/silverleaf/`) plus a case-study post — the smallest credible route.
- **Commit plan + Ivy handoff** prepared; no approvals, no publication, no
  commit, no push, no deploy.

## 2. Starting SJC state

| Item | Value | Label |
|------|-------|-------|
| Branch / HEAD | `master` @ `1be2ade` | VERIFIED |
| Remote | origin `https://github.com/wguDataNinja/sjc-intel.git`; origin/master == local | VERIFIED |
| Working tree | 75 dirty/untracked lines (Tasks 12–17 uncommitted by design + pre-existing data changes) | VERIFIED |
| Tests / validation | 203 passed; `validate.py` ALL PASSED; corpus validator 0 errors; portability PASS | VERIFIED |
| Publication decisions | None (only `legacy_exceptions.yaml`) | VERIFIED |
| Review queue | 167 entries (83 verified / 78 pending / 5 archived / 1 rejected_noise) | VERIFIED |
| SilverLeaf-signal items | 10 (5 high/medium-sensitivity discovery items; 5 lower-sensitivity tracked-entity items) | VERIFIED |
| Real release eligibility | 0 selected (no decisions) | VERIFIED |
| Generated demo | `site/` built from 8-item demo fixture | VERIFIED |
| Portfolio repository | **Discovered** this task: `wguDataNinja/buddyowens-site` (was "not discoverable" in Tasks 16–17) | VERIFIED |

Nothing was discarded, committed, or pushed.

## 3. Task 17 visual review

Built and served the demo site; reviewed Latest (desktop/mobile), Browse
(desktop/mobile, filtered, search, zero-results), item detail (desktop/mobile),
topic/place/entity collections, About, Data & Sources, empty release, 404 with
headless Chrome (screenshots + DOM layout measurement).

Findings:

- **Resident comprehension (first 10s):** good — brand, tagline, release date,
  item count, trust statement and topic shortcuts are above the fold; cards are
  scannable.
- **Card density / hierarchy / spacing / typography:** correct and consistent.
- **Mobile navigation:** sticky 3-item bottom nav works; content padded above
  it.
- **Filter usability:** sidebar on desktop, bottom sheet on mobile; chips,
  clear-all, result count present.
- **Source prominence / date clarity / Reviewed / relevance labels:** present
  per spec; dates absolute and labeled.
- **Source table / footer:** clean.
- **Demo labeling:** visible banner on every page.
- **External-link behavior:** `target="_blank" rel="noopener noreferrer"` with
  visible "opens in a new tab" label.
- **Accessibility:** single H1 per page, skip link, landmarks, focus visible,
  reduced-motion honored (automated structure tests pass).

An automated vision review repeatedly reported mobile text "clipping." This was
**disproved with real browser layout metrics**: at 390 px, `scrollWidth ==
clientWidth` and the max element right edge equals the viewport on both Latest
and Browse (verified twice, Task 17 and 18). The reports are a perception
artifact of the review model on downscaled screenshots; the rendered site has no
horizontal overflow.

## 4. UI fixes implemented

| Fix | Before | After | Reasoning |
|-----|--------|-------|-----------|
| Item-detail page gutter | Detail content flush at x=0 (breadcrumb, h1, badges touched the viewport edge) | Content wrapped in the shared `.page` container; aligns at the same left edge (≈96 px) as Home/Browse/About/Sources | Objective layout defect; every other page had the gutter. |
| Sources table "Updates" column | Left-aligned numeric column | Right-aligned, `nowrap` | Objective polish: numeric columns scan better right-aligned. |
| "Current release" block on Sources | Plain stacked rows | Subtle row separators | Objective polish: improves scanability. |

No accepted product decision was changed or redesigned. Before/after confirmed
by `getBoundingClientRect` measurements (item h1 left 0 → 96).

## 5. SilverLeaf scope registry

`registry/silverleaf_scope.yaml` implements the launch-ready minimum
(ROADMAP.md §3B-G1), authored from the scope decision packet, communities
registry, tracked entities, source evidence, and the intelligence corpus. It
supports every element the task requires:

- canonical identity (`silverleaf`, aliases Silver Leaf / Silverleaf,
  parent `northwest_st_johns`);
- 12 verified neighborhoods (+ `cherry_elm` needs-review) cross-referenced to
  `communities.yaml`;
- direct-serving roads (SilverLeaf Parkway, CR 16A, St. Johns Parkway / CR 2209
  connector, IGP) and materially adjacent corridors (CR 210, SR 16, US 1),
  each with role + provenance + evidence;
- schools (SilverLeaf K-8 verified with attendance zone needs-review; Tocoi
  Creek HS inferred), utilities (SJC utility department verified; SR 207 WRF
  inferred regional capacity);
- tracked developments (Publix, Commons, Market, Harris Teeter, mini-golf, etc.)
  cross-referenced to `tracked_entities.yaml`;
- community businesses/services (Bala's needs-review, Jersey Mike's, Baptist
  campus, Ascension adjacent-only);
- inclusion rules (INC-01…06), exclusion rules (EXC-01…07), the
  direct/nearby/countywide-material relevance rules with the exact stable ids
  `in_silverleaf` / `near_silverleaf` / `countywide_impact`;
- a `needs_review` list (crime/minor items, unverified URLs, provisional
  identities, inferred zone);
- every element carries `verification: verified | inferred |
  editorial-policy | needs-review` and an `evidence_source`.

**No precise boundaries, polygons, coordinates, or mileage claims** — the
registry states this explicitly and a test enforces it.

## 6. Registry validation

`schemas/silverleaf_scope.schema.yaml` documents the field contract;
`scripts/validate_silverleaf_scope.py` enforces: provenance vocabulary,
neighborhood→communities.yaml references, ENT-* development→tracked_entities
references, entity_id link resolution, corridor typing, relevance-id integrity,
and soft checks on needs-review corpus references. Wired into `validate.py`
§10. 8 tests in `tests/test_silverleaf_scope.py` (including the no-GIS-claims
test). Result: PASS (0 errors, 0 warnings).

## 7. Review queue and corpus summary

| Metric | Count |
|--------|-------|
| Corpus items | 192 |
| Review queue entries | 167 (83 verified / 78 pending / 5 archived / 1 rejected_noise) |
| Verified by source | BCC 40, NBOR 25, county_news 8, utility 5, SJSO 4, emergency 1 |
| SilverLeaf-signal items | 10 |
| SilverLeaf crime/minor (high sens) | 3 (excluded by default) |
| Fresh 2026-08-02 candidates | 4 county news + 1 SJSO (verified-eligible after review; the 4 county-news ones are SilverLeaf-relevant candidates) |

The verified set is countywide-heavy (BCC January boilerplate, NBOR utility ROW
permits). The genuinely SilverLeaf-relevant, fresh, actionable pool is small —
which the first release reflects honestly.

## 8. First-release candidate set

Recommended **4-item core** (all within a 90-day window back to 2026-05-01):

| Item | Title | Source | Source date | Rel. | Status | Sens. | Class |
|------|-------|--------|-------------|------|--------|-------|-------|
| SJC-UTIL-20260603-0001 | Phase III Extreme Water Shortage Declaration — Active | SJC Utility Dept | 2026-05-11 (still active Aug 4) | countywide_impact | verified | medium | READY_AFTER_COPY_EDIT (needs medium editorial approval) |
| SJC-EM-20260626-0001 | Residents Urged to Prepare as 2026 Atlantic Hurricane Season Begins | SJC Emergency Mgmt | 2026-06-01 | countywide_impact | verified | low | READY_TO_APPROVE |
| SJC-UTIL-20260603-0005 | Utility Department Water Service Line Material Inventory | SJC Utility Dept | 2026-06-03 (observed) | countywide_impact | verified | low | READY_TO_APPROVE (copy edit) |
| SJC-CN-20260802-0001 | County Road 16A Closures and Detours | SJC County News | 2026-07-20 (closures Aug 7–10 upcoming) | near_silverleaf | pending_review | low | READY_AFTER_REVIEW (verify → approve) |

Conditional / decision-tier:

| Item | Title | Class | Action |
|------|-------|-------|--------|
| SJC-CN-20260802-0002 | Daily's withdraws CPA amendment | BUDDY_DECISION | Confirm Daily's location (CR 210/IGP-area = near; else countywide → EXCLUDE). Default DEFER. |
| SJC-SL-20260706-0005 | Bala's second location | READY_AFTER_SOURCE_CHECK | Article exists on St. Johns Citizen but URL is 404; find correct URL + confirm location. |
| SJC-SL-20260704-0002 | SilverLeaf K-8 sneak peek | DEFER (orientation-tier) | Old (May 2025), local media; re-source current opening for a future release. |
| SJC-SL-20260704-0001 | Mega Publix first look | DEFER (orientation-tier) | Completed Mar 2026; one-time orientation exception is a Buddy call. |
| SJC-SL-20260704-0005 | Two new supermarkets (Harris Teeter) | DEFER (orientation-tier) | Proposed; conditional wording; one-time orientation exception. |

Rationale: the core is **utilities/water (3) + roads/traffic (1)** — the
highest-confidence, freshest, most household-actionable records. Schools and
community/services appear only in the orientation tier because the only records
are old local-media items (the SilverLeaf K-8 school, Publix, Harris Teeter),
which need either a source refresh or a one-time window exception. No category
was included merely for balance, and no public-safety/crime material is
included.

## 9. Proposed release order

The release renders in the deterministic order defined by the data contract
(source date desc, then item id asc): **CR 16A closures (Jul 20) → service-line
inventory (Jun 3) → hurricane preparedness (Jun 1) → water shortage (May 11)**.

Why this serves a resident: the time-critical, actionable item (CR 16A weekend
closures beginning Aug 7) surfaces first; the ongoing countywide conditions
(service line, hurricane season, water restrictions) follow as durable
household awareness items. The UI never reorders.

## 10. Candidate copy edits

Repository mutation is permitted because the publication-decision model
explicitly supports a separate `public_summary_override` without altering the
source intelligence record (schema + `public_projection`). The operator CLI now
exposes it (plus `--relevance`, `--event-date`, `--lifecycle`) so the packet is
executable. Proposed public-facing copy (original → proposed):

1. **SJC-UTIL-20260603-0001 (water)**
   - Original summary: "SJRWMD Phase III Extreme Water Shortage remains in
     effect as of June 2026 due to Extreme Drought (D3)…"
   - Proposed (override): *"The Phase III Extreme Water Shortage remains in
     effect: outdoor irrigation is limited to one day per week and is
     prohibited 8 a.m.–6 p.m. Reclaimed-water irrigation is not included in the
     schedule."*
   - Temporal wording: "remains in effect" (no stale-date inference); relevance
     `countywide_impact`.
2. **SJC-UTIL-20260603-0005 (service line)**
   - Proposed (override): *"The county utility is inventorying water service
     line materials under the EPA Community Lead-Safe Hub program. Customers
     may be contacted to allow an inspection of the pipe from the street to the
     home."*
3. **SJC-CN-20260802-0001 (CR 16A)**
   - Proposed (override): *"Weekend closures of County Road 16A between
     Timberwolf Trail and River Reach Parkway are scheduled 8 p.m. Friday to
     5 a.m. Monday (Jul 31–Aug 3 and Aug 7–10) for First Coast Expressway pipe
     installation. Detour via SR 16 and SR 13."* — relevance `near_silverleaf`.
4. **SJC-EM-20260626-0001 (hurricane)** — no override needed; copy is clear.

Overrides add no facts beyond the linked sources; acronyms are explained
(First Coast Expressway, EPA program); proposals remain conditional. The
orientation-tier items would require fresh source-check copy edits before any
approval.

## 11. Exclusions and deferrals

| Item(s) | Reason |
|---------|--------|
| SJC-SL-20260706-0001 / -0002 / -0004 | High-sensitivity crime / minors; public-safety default exclude (EXC-06). |
| SJC-SL-20260706-0003 | Lightning strike; unverified URL/date, low value. |
| SJC-UTIL-20260603-0002 | Free chlorine burnout; event ended Jun 21 — stale, not actionable. |
| SJC-UTIL-20260603-0003 | SR 207 WRF Phase 2; south county, low SilverLeaf relevance (DEFER; could reframe "now online" later). |
| SJC-UTIL-20260603-0004 | Utilities lab ribbon-cutting; low resident value (DEFER). |
| SJC-UD-20260704-0001 | Plantation WTP $1.6M; located in Ponte Vedra Beach (DEFER). |
| SJC-UD-20260704-0002 | Moody's Aa1 rating; countywide civic/financial (DEFER). |
| SJC-UD-20260626-0001 | 2025 annual report; low value (DEFER). |
| SJC-CN-20260626-0002 | Railroad crossing closures; likely completed by release (DEFER — revisit on next closure). |
| SJC-CN-20260603-0005 | Phase III declaration from county news; marked `duplicate` in corpus (SJC-UTIL-20260603-0001 is the authoritative utility record). |
| SJC-CN-20260603-0001/0003/0004 | Surplus auction, library promos, awards — pure civic, no SilverLeaf material impact (EXC-05). |
| SJSO items (4) | Public safety/crime default exclude. |
| NBOR notices (25) | Utility ROW permits / St. Augustine-specific; countywide, low resident signal. |
| BCC January items (40) | Stale (Jan 2026), resolution boilerplate. |

## 12. Buddy/GPT decision table

| # | Decision | Recommendation | Options |
|---|----------|----------------|---------|
| 1 | Approve the 4-item core release set | Yes | Add/remove any core item |
| 2 | Approve medium-sensitivity editorial approval for SJC-UTIL-20260603-0001 | Yes (it is the authoritative, still-active water record) | Swap to county-news duplicate after un-marking it |
| 3 | Approve copy-edit overrides (§10) | Yes | Edit wording |
| 4 | Release window | 90 days back to 2026-05-01 for this release | 60 days (drops water + hurricane) or explicit ongoing exception |
| 5 | CR 16A relevance | near_silverleaf (CR 16A is a direct access road) | countywide_impact |
| 6 | Daily's item | DEFER until location confirmed | Include as near/countywide if location confirmed |
| 7 | Bala's item | DEFER until correct URL found | Include after source check |
| 8 | Orientation tier (K-8, Publix, Harris Teeter) | DEFER for v0; optional one-time window exception | Include as orientation set |
| 9 | Countywide-material-impact rule | Adopt scope registry rule (utility/water, emergency, tax/land) | Tighten/loosen |
| 10 | Public safety | Exclude entirely for v0 | — |
| 11 | Cadence language | "Periodic; no fixed schedule" | — |
| 12 | Portfolio integration | Copy static output to `static/silverleaf/` + case-study post (§19) | Independent deploy, Hugo embed |

## 13. Proposed publication commands (NOT executed)

Verify-then-approve for pending items (step 1 only when item is pending):

```
python3 scripts/update_review_status.py SJC-CN-20260802-0001 verified --note "Editorial review: CR 16A SilverLeaf access road closures; verified against county page Aug 4 2026"
```

Proposed approvals (Buddy runs after approving §12):

```
python3 scripts/publication_decision.py approve \
  --item-id SJC-UTIL-20260603-0001 --reviewer Buddy \
  --rationale "Ongoing Phase III water shortage materially affects SilverLeaf households; verified still active Aug 2026; medium sensitivity approved editorially." \
  --silverleaf included --silverleaf-rationale "Countywide-material impact: irrigation rules change local household conditions." \
  --relevance countywide_impact \
  --public-summary-override "The Phase III Extreme Water Shortage remains in effect: outdoor irrigation is limited to one day per week and is prohibited 8 a.m.-6 p.m. Reclaimed-water irrigation is not included in the schedule."

python3 scripts/publication_decision.py approve \
  --item-id SJC-EM-20260626-0001 --reviewer Buddy \
  --rationale "Hurricane-season preparedness is countywide material for SilverLeaf households." \
  --silverleaf included --silverleaf-rationale "Countywide-material impact: emergency preparedness." \
  --relevance countywide_impact

python3 scripts/publication_decision.py approve \
  --item-id SJC-UTIL-20260603-0005 --reviewer Buddy \
  --rationale "EPA service-line inventory affects all county utility customers incl. SilverLeaf." \
  --silverleaf included --silverleaf-rationale "Countywide utility material impact." \
  --relevance countywide_impact \
  --public-summary-override "The county utility is inventorying water service line materials under the EPA Community Lead-Safe Hub program. Customers may be contacted to allow an inspection of the pipe from the street to the home."

python3 scripts/publication_decision.py approve \
  --item-id SJC-CN-20260802-0001 --reviewer Buddy \
  --rationale "CR 16A is a SilverLeaf access road; weekend closures materially affect resident commutes." \
  --silverleaf included --silverleaf-rationale "Direct access road (scope registry roads.direct_serving.cr_16a)." \
  --relevance near_silverleaf --place-ids cr_210_corridor \
  --public-summary-override "Weekend closures of County Road 16A between Timberwolf Trail and River Reach Parkway are scheduled 8 p.m. Friday to 5 a.m. Monday (Jul 31-Aug 3 and Aug 7-10) for First Coast Expressway pipe installation. Detour via SR 16 and SR 13."
```

Then generate the real release:

```
python3 scripts/build_static_release.py \
  --release-id SJC-REL-2026-08-001 --reviewer Buddy \
  --published-at <approval time> --now <approval time> \
  --window-start 2026-05-01 --window-end <approval date> \
  --out-dir site/data/releases/SJC-REL-2026-08-001
python3 scripts/build_static_site.py --source site/data/releases/SJC-REL-2026-08-001
```

Deferred/excluded items use `defer` / no command (no decision file is required
for exclusion; optional `defer` commands can record rationale).

## 14. Real-release dry-run evidence

- `build_static_release.py --release-id SJC-REL-2026-08-001 --check --reviewer Buddy`
  → **CHECK: READY — 0 item(s); no files written** (current real state: no
  decisions, correct).
- `select_publication_items.py --release-id SJC-REL-2026-08-001 --check`
  → no items currently eligible (0 selected; expected).
- Decision-tool dry-run for SJC-UTIL-20260603-0001 prints the exact plan
  (would-write path, `publication_status: approved`, `release_eligible: True`,
  history 1) with **no file written**.
- Corpus validator: PASS (0 errors). Scope validator: PASS.

## 15. Simulated post-approval evidence

A **sandbox copy** of `data/` + `registry/` was created (no production files
touched). CR 16A was flipped to `verified` in the sandbox, the four core
decisions were written with copy-edit overrides via the real tool, and the real
exporter + site generator were run against it:

- Selected: 4 items — SJC-CN-20260802-0001 (near_silverleaf),
  SJC-UTIL-20260603-0005 (countywide_impact),
  SJC-EM-20260626-0001 (countywide_impact),
  SJC-UTIL-20260603-0001 (countywide_impact).
- Copy edits honored: CR 16A + service-line + water summaries show the
  overrides; `public_projection` never altered the source records.
- `release-manifest.json` checksums **VERIFY** against bytes; `environment:
  real`; `item_ids` correct; search-index has 4 entries; 17 routes generated;
  the simulated site shows **no demo banner**, correct relevance badges
  (3 countywide + 1 near), and **no internal-field leaks**.
- **Selector fix proven**: without the legacy-treatment change, CR 16A was
  excluded by `LEG-0802-MISSING-CREATED`; after the fix, `warning_timestamp_default`
  no longer blocks release while blocking treatments (duplicate capture,
  archival, registry-fix) still do (tests added).

Current real state (0 items) / simulated post-approval state (4 items) / demo
state (8 items) are clearly separated and never mixed.

## 16. Recommended v0 release policy

| Parameter | Recommendation |
|-----------|----------------|
| Release ID | `SJC-REL-2026-08-001` |
| Publication date | The date Buddy approves; `published_at` = approval timestamp; deterministic build flags pin it. |
| Item count | 4 core (up to 4–8 with conditional/orientation tiers). |
| Release window | 90 days back to 2026-05-01 for this release. |
| Countywide-material rule | Adopt scope registry rule: utility/water continuity, emergency preparedness, tax/land changes; pure civic excluded. |
| Old-but-ongoing items | Allowed within the window when verified still active (water shortage); older orientation-tier local-media items need a one-time exception. |
| Proposals | Include only with conditional wording (proposed/planned/expected). |
| Sensitive items | Medium requires editorial approval recorded on the decision; high excluded. |
| Public safety | Excluded entirely for v0. |
| Ordering | Deterministic source-date desc, item id asc; UI never reorders. |
| Withdrawal | New explicit `withdraw` decision → new release; prior artifacts retained. |
| Correction | `public_summary_override` + new release decision; no silent mutation. |
| Cadence | "Periodic; no fixed weekly schedule." |

## 17. Portfolio repository identified

- **`wguDataNinja/buddyowens-site`** — the personal portfolio website.
  - Live: `https://wguDataNinja.github.io/buddyowens-site/`
  - Framework: **Hugo** (extended 0.149.1, pinned in CI) + **PaperMod** theme
    (git submodule `adityatelange/hugo-PaperMod`).
  - Default branch `main`; deployment: `.github/workflows/deploy.yml` →
    `actions/deploy-pages@v4` (GitHub Pages, artifact `./public`, env
    `github-pages`). `has_pages: true`.
  - Content model: `content/posts/{slug}/index.md` case-study posts (front
    matter: title/date/draft/tags/categories) with supporting data + images;
    `content/about/_index.md`; PaperMod client search; `content/tags/_index.md`.
  - Static assets under `static/`; author Buddy Owens; `mainSections = ["posts"]`.
  - **Archived** (last push 2025-09-09); **no local clone** in
    `/Users/buddy/projects` (remote-only). BaseURL is a project-site subpath, so
    subdirectory hosting works.
  - No local repo matched web-framework signals except `wgu-atlas` (WGU catalog
    explorer, not the portfolio) — confirmed via GitHub API that `buddyowens-site`
    is the only personal-site repo.

## 18. Portfolio architecture and deployment

Hugo builds `public/`; Pages serves `https://wguDataNinja.github.io/buddyowens-site/`.
Static files placed under `static/<path>` are copied verbatim to
`public/<path>`. Our app uses only relative URLs and is **path-independent**
(verified: the demo runs correctly from any subpath), so a copied directory
works without Hugo template changes. No route rewrites needed (real directory
paths). Re-activating the archived repo and enabling the Pages workflow are the
only GitHub-side prerequisites (Buddy).

## 19. Recommended integration approach

**Selected: Option C — copy the generated static output into a
portfolio-controlled public directory** (`static/silverleaf/` in
`buddyowens-site`), plus a case-study post
(`content/posts/sjc-intel/index.md`) that links to `/silverleaf/` and embeds
screenshots.

| Criterion | Why C wins |
|-----------|------------|
| Speed to publication | Fastest: copy `site/` → `static/silverleaf/`, one Hugo post, existing Pages deploy. |
| Deployment complexity | None beyond the existing workflow; no second host. |
| Portability | App is path-independent; re-deployable anywhere. |
| Search/routes | Full Browse search works; routes are real paths (no rewrites). |
| Static asset paths | Relative URLs resolve at `/buddyowens-site/silverleaf/`. |
| Maintenance | Release = regenerate + copy + push; SJC repo stays the authority. |
| Repository boundaries | Portfolio holds only deployable static output + post; SJC owns generation. |
| Failure isolation | Independent directory; a release defect doesn't break the portfolio shell. |
| Future reuse | Same bundle can be copied to any host later. |

Rejected: **A (embed via Hugo templates)** — full rewrite of the app into Hugo
is large and fragile; **B (independent deploy + link)** — adds a second hosting
target and deploy workflow for no v0 benefit; **D** — no other convention
applies.

## 20. Portfolio case-study specification

Post: `content/posts/sjc-intel/index.md` (title "SJC_Intel — Agent-Led Local
Intelligence for SilverLeaf"; draft:false; tags e.g. `data-engineering`,
`public-data`, `static-site`, `ai-agents`; categories `projects`). Story arc:
agent-led intelligence architecture → St. Johns County implementation →
SilverLeaf resident product → reviewed static release → bounded VPS automation
later. Sections: one-sentence description; short overview; problem (fragmented
public information in a growing master-planned community); solution
(evidence-first discovery → human review → reviewed static release); architecture
(pipeline diagram); resident UI (Latest/Browse/detail); evidence and review
(publication decisions, checksums, rollback); reusable patterns (deterministic
export, file-backed decisions, portable static site); Mac/VPS split; limitations;
repository link (`https://github.com/wguDataNinja/sjc-intel`); live demo link
(`/silverleaf/`); screenshots; technology (Python, YAML, semantic HTML/CSS/JS,
GitHub Pages); validation proof (tests, checksums); lessons learned. **Do not
overclaim:** multi-domain platform, live automation, real-time alerts,
autonomous publication, production PostgreSQL, completed VPS deployment.

## 21. Screenshot plan and evidence

Generated (temp dir `/var/folders/…/T/opencode/sjc_shots18/`, not committed):
Latest desktop + mobile, Browse filtered (transportation), item detail (before
and after the gutter fix), Data & Sources, simulated real Latest. Minimum
portfolio evidence: Latest desktop (1280×~1500), Latest mobile (390×~1400),
Browse/filter view, item detail, plus an architecture diagram (SVG/text). Spec:
crop to content, label "demo data" where applicable, alt text + captions
describing each screen. Screenshots can be committed in the portfolio repo under
`static/images/sjc-intel/` (Hugo's convention) — not in SJC_Intel.

## 22. Commit-readiness preflight

75 dirty/untracked lines, all Tasks 12–18. No secrets, no `.env`, no credentials
(scan clean). Largest files are reports/docs/tasks (≤ 48 KB) and generated
`data/review_queue/queue.yaml` (184 KB, curated state). No line-ending or
permission issues. Missing `.gitignore` coverage: generated site output
(`site/*.html`, `site/data/**`, `site/build.json`) and staging dirs
(`data/incoming/`, `runtime/`) should be ignored; nothing should be deleted.

## 23. Proposed commit groups

Dependency order (each group validates independently):

1. **Weekly ops + bundle/import (Tasks 12–13)** — `feat:` "weekly operational
   bundle/import foundation" — `scripts/{run_weekly,accept_candidates,bundle_*,import_weekly_bundle,review_source_proposals}.py`, `schemas/{bundle_manifest,intel_candidate,source_proposal}.schema.yaml`, `deploy/sjc-weekly-task.yaml`, `docs/weekly_*`, `prompts/sjc_weekly_ops_task.md`, `tests/test_{bundle,import_weekly,accept_candidates,run_weekly}.py`, `tests/fixtures/{sample_bundle,bundle_workspace}/`, `tests/fixtures/sjso_feed.xml`, `data/receipts/`. Tracked: yes.
2. **Publication foundation (Task 16)** — `feat:` "file-backed publication decisions and corpus validation" — `scripts/publication_*.py`, `scripts/{select_publication_items,validate_publication_corpus}.py`, `schemas/publication_decision.schema.yaml`, `data/publication_decisions/` (incl. legacy exceptions), `docs/{publication_release_contract,static_release_data_contract,public_ui_v0_spec}.md`, `docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_*.md`, `tests/test_publication.py`, `tests/fixtures/publication/`. Tracked: yes.
3. **SilverLeaf scope (Task 18)** — `data:`/`feat:` "SilverLeaf scope registry" — `registry/silverleaf_scope.yaml`, `schemas/silverleaf_scope.schema.yaml`, `scripts/validate_silverleaf_scope.py`, `tests/test_silverleaf_scope.py`, `validate.py` §10. Tracked: yes.
4. **Static export + site (Tasks 17–18)** — `feat:` "SilverLeaf Brief static export and portable site" — `scripts/{build_static_release,build_static_site,static_release_common,site_search,site_templates}.py`, `scripts/{publication_decision,select_publication_items}.py` (relevance/override/legacy fixes), `site/assets/`, `site/fixtures/`, `site/README.md`, `tests/{test_static_release,test_site_build}.py`, `validate.py` §9. Tracked: yes (sources only — see #7).
5. **Docs + reports (Tasks 11–18)** — `docs:`/`chore:` — `README.md`, `ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/{backup-restore,postgresql_adapter}.md`, `LICENSE`, `reports/11…18`, `tasks/12…18`, `logs/agents/…`. Tracked: yes.
6. **Durable data updates** — `data:` — `data/intel_items/2026-07-06/agentic_search_results.yaml`, `data/review_queue/queue.yaml` + `summary.yaml` (curated state; validate YAML before commit). Tracked: yes.
7. **Generated site output** — `site/*.html`, `site/data/**`, `site/build.json` — **do not track**; add `.gitignore` (`site/data/`, `site/index.html`, `site/browse/`, `site/about/`, `site/sources/`, `site/item/`, `site/topic/`, `site/place/`, `site/entity/`, `site/404.html`, `site/build.json`) since it is deterministic output of committed scripts + fixtures.
8. **Keep ignored/uncommitted** — `data/incoming/` (staging), `runtime/`, `__pycache__/`, `.DS_Store`, screenshots (temp). `data/incoming/` decision: ignore unless a staging policy is adopted.

Git Steward should stage explicit paths per group; never `git add .`.

## 24. Ivy handoff

Public v0 is **independent of VPS work**:

- Public v0 = static release (Mac-generated) + portfolio deployment (Hugo
  Pages). No VPS, no database, no UI backend.
- Operational follow-up = Ivy admission, VPS deployment, scheduled collection,
  bundle transfer, Mac review (separate, non-blocking for launch).
- Handoff for Strong Codex/Ivy: public release status AWAITING Buddy approval;
  exact reviewed Git SHA required for the release (Buddy-approved commit of the
  groups above); deployment-independent static architecture (copy `site/` →
  portfolio `static/silverleaf/`); minimum SJC VPS workload = two deterministic
  sources (NBOR + SJSO RSS) with weekly bundle/import; **no corpus PostgreSQL**
  (DORMANT_FUTURE_READY), no UI backend; VPS holds only temporary ingest data;
  bundle lifecycle per `docs/weekly_operational_contract.md` (run → bundle →
  transfer → import → receipt → prune); remaining capacity + scheduling proof
  (reports 12–15) still required before any VPS activation. No Ivy work was
  performed.

## 25. Files changed

Added: `registry/silverleaf_scope.yaml`; `schemas/silverleaf_scope.schema.yaml`;
`scripts/validate_silverleaf_scope.py`; `tests/test_silverleaf_scope.py`;
`reports/18-first-release-and-portfolio-integration.md`;
`logs/agents/sjc-intel-architect/2026-08-04_first_release_portfolio_integration.md`.
Modified: `scripts/select_publication_items.py` (legacy-treatment gate);
`scripts/publication_decision.py` (`--relevance`, `--public-summary-override`,
`--event-date`, `--event-date-label`, `--lifecycle`, `--lifecycle-label`);
`scripts/publication_common.py` (`legacy_treatment_for_item`);
`scripts/validate_publication_corpus.py` (relevance-override validation);
`scripts/build_static_release.py` (relevance override honored);
`scripts/build_static_site.py` (item-page gutter fix);
`site/assets/css/silverleaf.css` (table/row polish); `schemas/publication_decision.schema.yaml`;
`scripts/validate.py` (§9 site, §10 scope); `ROADMAP.md` (§3B-G1 status);
`tests/test_publication.py` (5 new tests). Pre-existing dirty data and Tasks
12–17 outputs preserved.

## 26. Validation results

```
python3 -m pytest tests/ -v            → PASS, 216 passed (203 baseline + 13 new)
python3 scripts/validate.py            → PASS — ALL PASSED (incl. §9 site + §10 scope)
python3 scripts/validate_publication_corpus.py → PASS — 0 errors, 320 warnings, 192 items
python3 scripts/validate_silverleaf_scope.py  → PASS — 0 errors, 0 warnings
python3 scripts/select_publication_items.py --release-id SJC-REL-2026-08-001 --check
                                         → CHECK: no items currently eligible (0 selected)
python3 scripts/build_static_release.py --release-id SJC-REL-2026-08-001 --check --reviewer Buddy
                                         → CHECK: READY — 0 item(s); no files written
python3 scripts/build_static_release.py --release-id SJC-REL-DEMO-20260804 --demo
                                         → built demo release (8 items)
python3 scripts/build_static_site.py --list-routes
                                         → 30 routes (demo, 8 items); simulated real → 17 routes (4 items)
python3 scripts/portability_check.py   → PASS
node --check site/assets/js/browse.js  → syntax OK
git diff --check                       → clean
git status --short                     → intended new files + pre-existing dirty files
```

Recorded: test count 216; route count 30 demo / 17 simulated real; current
eligible count 0; proposed candidate count 4 core (+ conditional/orientation);
output sizes — `site/` ≈ 376 KB, demo release.json 13.3 KB, search-index 8.9 KB,
browse.js 11.6 KB, css 19.8 KB; screenshots in the temp dir listed in §21;
portfolio repo facts in §17.

## 27. Remaining Buddy actions

1. Review §12 decision table and §16 release policy; 2. approve the copy edits
   (§10); 3. approve + run the §13 command packet (verify CR 16A, approve 4
   items); 4. generate the real release and preview; 5. un-archive
   `buddyowens-site` and re-enable the Pages workflow; 6. approve the commit
   plan (§23) for Git Steward; 7. approve portfolio post copy + integration
   (implementation is a bounded medium-agent task after un-archiving).

## 28. Remaining medium-agent work

- Run the approved command packet + generate `SJC-REL-2026-08-001` + build the
  real site (one bounded session after Buddy approval).
- Implement the portfolio integration in `buddyowens-site` (copy `site/` →
  `static/silverleaf/`, write `content/posts/sjc-intel/index.md`, screenshots),
  after un-archive and with explicit authority.
- Optional: expose the release-history browsing route; add a CI check for
  release reproducibility; draft the remaining editorial backlog pass.

## 29. Remaining deployment work

Un-archive `buddyowens-site` (Buddy/GitHub); confirm Pages is enabled and the
deploy workflow runs; push the integration commit; verify
`https://wguDataNinja.github.io/buddyowens-site/silverleaf/`. No VPS, database,
or backend deployment is required for the public v0.

## 30. Risks and unresolved issues

- **No item approved yet** — the release is one Buddy approval away; the
  simulator proves the path.
- **Legacy/corpus reality**: SJC-CN-20260603-0005 is marked `duplicate` in the
  corpus (the utility record is the water authority); the 2026-08-02 items
  needed the legacy-treatment selector fix to be releasable.
- **Portfolio repo archived + not cloned locally** — un-archive and cloning are
  prerequisite GitHub actions; integration implementation is blocked on them
  (not on SJC work).
- **Orientation tier** relies on older local-media records; including it
  requires a one-time window exception and source checks (Buddy decision).
- **Bala's URL 404** and **Daily's location** unresolved (both classified
  accordingly).
- Automated vision review has a persistent false "mobile clipping" perception;
  real layout metrics show no overflow (documented).
- SilverLeaf scope **editorial-policy rules require Buddy approval** before
  publication use.

## 31. Final Git status

SJC `master` @ `1be2ade`, origin/master == local. Working tree: Task 18 files +
pre-existing dirty data + Tasks 12–17 outputs. Nothing staged, committed, or
pushed. No publication/review decision made; no item approved; nothing
deployed; Ivy and the portfolio repo untouched (read-only inspection only).

## 32. Final task status

| Area | Status |
|------|--------|
| Task 17 UI visual/functional review | COMPLETE |
| Objective UI fixes (item gutter + polish) | COMPLETE |
| SilverLeaf scope registry + validation + tests | COMPLETE |
| Review queue / corpus inspection | COMPLETE |
| First-release candidate set + editorial packet | COMPLETE (recommendation) |
| Copy edits (original vs proposed) | COMPLETE |
| Publication commands (non-executed) | COMPLETE |
| Real-release dry-run evidence | COMPLETE |
| Simulated post-approval evidence | COMPLETE (4 items, nonmutating sandbox) |
| v0 release policy recommendation | COMPLETE |
| Portfolio repository identified + architecture | COMPLETE |
| Integration approach selected | COMPLETE (Option C) |
| Case-study + screenshot spec | COMPLETE |
| Commit-readiness preflight + plan | COMPLETE |
| Ivy handoff | COMPLETE |
| Release approval + real generation + portfolio integration + deployment | AWAITING BUDDY / BLOCKED (portfolio un-archive) |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP — the real first release is
decision-ready and the portfolio path is exact; the remaining work is Buddy
approval of a short packet, running the prepared commands, bounded release
generation, the (blocked-on-unarchive) portfolio integration implementation, and
deployment/commit. No item was approved or published; nothing was committed,
pushed, deployed, or modified outside SJC_Intel.
