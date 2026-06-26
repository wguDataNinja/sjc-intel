# SJC_Intel Buildout Plan

**Goal:** Move SJC_Intel from supervised operator mode to autonomous daily
monitoring with an editorially controlled public site.

**Planning status:** Engineering and operations plan only. No monitor runs,
source promotions, scheduled automation, or public publishing are authorized by
this plan.

---

## 1. Current State Assessment

### What Already Works

| Area | Current Capability | Evidence |
|------|--------------------|----------|
| Source registry | 24 canonical public sources registered across county, sheriff, schools, transportation, utilities, budget, Clerk, permits, weather, and elections | `registry/sources.yaml`, `STATE.md` |
| Candidate registry | CDD, community/developer, media, public-notice, municipal, and spillover sources captured for later review | `registry/source_candidates.yaml` |
| Cadence model | Manual daily/weekly/monthly cadence with `LAST_RUN` markers and catch-up rules | `docs/cadence.md`, `logs/runs/README.md` |
| Known-source monitor contract | Bounded monitor task prompt exists, with fetch, extract, dedupe, classify, RI layer, and YAML output | `prompts/known_source_monitor_task.md` |
| Backfill contract | May 2026 historical backfill template exists and has been executed once | `prompts/hermes_may_2026_backfill_task.md` |
| Search discovery starter | HERMES-003 placeholder exists but needs a full contract | `prompts/hermes_search_discovery_task.md` |
| Data schema | Intel item schema v2.0 includes source attribution, taxonomy, RI layer, review status, and human-review flag | `schemas/intel_item.schema.yaml` |
| Taxonomy | Controlled topics, communities, urgency, sensitivity, verification, review states, channels, interest tags, and audiences exist | `docs/taxonomy.md` |
| Dedupe | Pilot `prior_items.yaml` tracks seen monitor items | `data/index/prior_items.yaml` |
| Logging | Agent logs and run logs exist; meaningful work has been recorded | `logs/agents/`, `logs/runs/` |

### What Has Been Tested

| Tested Area | Result | Notes |
|-------------|--------|-------|
| `sjc_county_news` pilot | Passed | 5 items extracted; WordPress sidebar lesson documented. |
| `sjso_news_stories` pilot | Passed | 4 public-safety items extracted; medium-sensitivity defaults validated. |
| `sjc_utility_department` pilot | Passed; daily-ready | 5 items extracted; plain HTML; first confirmed daily-ready source. |
| `sjc_school_stack` pilot | Passed for district homepage | 7 candidates found, 2 new items extracted, 4 backfill duplicates skipped, 1 low-signal PR item skipped. |
| May 2026 backfill | Completed | 21 items, 5 source families, monthly wrap, clusters, gaps, and taxonomy evidence. |
| Road closures investigation | Completed after initial gap | NBOR app discovered: `https://webapp.sjcfl.us/webnews/NBRscreend.aspx`; public, plain HTML, high-value source. |
| Tier 1/Tier 2 promotions | Completed | 15 promoted sources added to canonical registry. |

### What Is Missing Or Blocked

| Gap | Impact | Next Action |
|-----|--------|-------------|
| No automation runtime | Monitor cycles cannot run autonomously; cadence is manual-only | Build a local runtime that executes bounded source jobs and writes logs without scheduling until approved. |
| No scheduled automation | Daily monitoring depends on Buddy invoking work | Decide automation boundary, then add cron/launchd/GitHub Actions only after approval. |
| No editorial review queue | Items can be extracted but not reliably reviewed or published | Build ED-001 queue artifact before public site. |
| No corrections policy | Public launch would lack accountability workflow | Draft ED-002 before launch. |
| No public site | Data remains internal | Build static site only after review pipeline exists. |
| HERMES-003 is underspecified | Search discovery cannot be repeated safely | Expand prompt with source/item/search-effectiveness outputs. |
| Several weekly sources lack monitor specs | BCC, school homepage, utility, and road specs exist; other weekly sources still need design | Design source-specific specs before automation. |
| Some registry/docs are stale or inconsistent | Road closures and Clerk status are partly newer than old notes; ROADMAP still calls Phase 2 current | Run source-of-truth cleanup as Phase 3 support work. |

### Open Items Needing Buddy Decisions

| Decision | Why It Matters | Recommended Default |
|----------|----------------|---------------------|
| Property Appraiser URL: `sjcpa.gov` vs `sjcpa.us` | Canonical registry uses `.us`; candidate/report references `.gov` | Manually verify official current domain, then update registry notes. |
| CDD source promotion approval | CDDs are high homeowner value but Tier 3 requires explicit approval | Approve a small first wave: Tolomato, Trout Creek, Six Mile Creek, plus one Twin Creeks/Meadow View source after URL split. |
| Clerk placeholder cleanup | `sjc_clerk_online_research` exists, but backlog still says stale Clerk replacement is open | Confirm whether cleanup is documentation-only or still needs URL validation. |
| Automation boundary | The repo currently forbids scheduled automation | Approve local supervised runtime first; defer unattended scheduler. |
| Public/private data boundary | Review queue and site need rules for what can appear publicly | Public only after source URL, review status, sensitivity check, and corrections workflow. |

---

## 2. Phase 3 Plan: Source Promotion Review & Monitor Design

Phase 3 should produce monitor-ready source specs, not full public automation.
The work should prioritize sources that already have proven extraction patterns
or high resident impact.

### Daily Sources From `docs/cadence.md`

| Priority | Source | Current Status | Daily-Ready Requirements | Investigation Needed | Effort | Dependencies |
|----------|--------|----------------|--------------------------|----------------------|--------|--------------|
| 1 | `sjc_utility_department` | Pilot passed; Hermes-ready | Keep spec current; include Announcements plus Featured Department News sidebar; run duplicate-zero cycle; define alert handling for boil notices and water restrictions | None for main page; companion Alert St. Johns/SJRWMD can be later | Small | Automation runtime; human review for urgent water/safety items |
| 2 | `sjc_county_news` | Pilot passed; active | Convert pilot notes into a formal monitor spec; codify main listing plus article sidebar extraction; validate selector drift; add source health checks | Confirm whether AJAX archive exposes older items | Small | Runtime; dedupe index; editorial queue |
| 3 | `sjso_news_stories` | Pilot passed; active | Create source-specific spec for public-safety sensitivity; handle Unicode URLs; default crime/arrest/legal items to human review | Confirm current listing pagination and archive depth | Small | Editorial queue required before public use |
| 4 | `sjc_emergency_management` | Registered, seasonal daily | Create spec with hurricane-season cadence, EOC update patterns, preparedness pages, Alert St. Johns companion, and mandatory high-sensitivity routing | Determine whether alerts are inline, linked, RSS/email, or external service | Medium | Human alert policy; no auto-publish |
| 5 | `sjc_road_closures` | Investigation complete; NBOR found | Update registry/check URL to NBOR or monitor config; build extractor for ASP.NET table rows; classify ROW/Meeting categories; keep county landing page as entry source | Test date-range parameters, pagination, PDF links, and historical coverage | Medium | Browser not required for initial NBOR HTML; PDF parsing later |
| 6 | `st_johns_citizen` | Canonical local media context source | Create media-source spec: headline/link/excerpt only, no copying, verification status `unverified`, official-record follow-up for consequential claims | Check public archive/feed structure and robots/terms; define minimum extraction | Medium | Editorial rules; official-source verification policy |

### Weekly Sources From `docs/cadence.md`

| Priority | Source / Weekly Item | Current Status | Weekly-Ready Requirements | Investigation Needed | Effort | Dependencies |
|----------|----------------------|----------------|---------------------------|----------------------|--------|--------------|
| 1 | `sjc_bcc_calendar` | Spec ready; metadata feasible | Implement Phase 1 metadata extraction: meetings, agenda link, minutes link, PDF URLs; route agenda PDFs to review queue | Confirm agenda/minutes URL patterns and PDF text quality | Medium | PDF parsing later; editorial queue |
| 2 | `sjcsd_boarddocs` | Part of school stack; partial readiness | Start with meeting metadata and agenda existence; avoid full packet parsing until stable | Inspect BoardDocs public app/API behavior; determine whether browser automation needed | Large | Browser automation likely; human review for school/safety/personnel |
| 3 | `sjc_school_district` | Homepage pilot passed | Promote homepage monitor to weekly-ready; preserve signal/noise rules; add spec notes from pilot; dedupe against backfill and BoardDocs | Confirm homepage sections and external media handling | Small | Runtime; editorial queue |
| 4 | `sjc_pza_boards` | Registered; investigation needed | Create monitor spec for hearing calendar, agendas, and public notices; link to NBOR where overlapping | Find agenda/packet location and date patterns | Medium | PDF parsing likely; Buddy approval not needed for design |
| 5 | `sjc_development_tracker` | Registered GIS map | Create investigation report: identify GIS layer/API endpoints, export options, and change-detection key | Browser/network inspection of map layers | Large | Browser automation or API discovery |
| 6 | `sjc_permit_status` | Registered permit source | Create investigation spec for search forms, reports, filters, and safe query scope | Determine whether public search supports date-filtered reports without personal data overcollection | Large | Browser automation/API assessment; privacy minimization |
| 7 | `fdot_district_two_nflroads` | Registered daily in source registry, weekly in cadence list | Create transportation companion spec for project pages, notices, lane closures, and St. Johns filtering | Determine whether NFLRoads has structured pages/feed | Medium | May need separate FDOT/NFLRoads extractors |
| 8 | Source candidate review | Direct repo work | Review Tier 3 CDD and high-value public-notice candidates; produce promotion packet, not canonical changes | Verify CDD URLs and split combined candidates where needed | Medium | Buddy approval for promotions |
| 9 | Backlog review | Direct repo work | Reconcile stale statuses: ROADMAP phase, Clerk placeholder, monthly log path, road-closure readiness, HERMES-003 status | None | Small | None |

### Phase 3 Deliverables

1. Formal monitor specs for `sjc_county_news`, `sjso_news_stories`,
   `sjc_emergency_management`, NBOR-backed `sjc_road_closures`,
   `st_johns_citizen`, `sjc_pza_boards`, `sjc_development_tracker`,
   `sjc_permit_status`, and `fdot_district_two_nflroads`.
2. Updated `sjc_school_stack` and `sjc_bcc_calendar` specs reflecting pilot
   findings.
3. A Phase 3 readiness table classifying every daily/weekly source as:
   `monitor_ready`, `metadata_ready`, `investigation_needed`, or `blocked`.
4. A source-of-truth cleanup pass for stale docs and backlog statuses.

---

## 3. Phase 4 Plan: Backfill Pipeline

### Remaining Backfill Passes

| Backfill | Purpose | Scope | Outputs | Effort |
|----------|---------|-------|---------|--------|
| Aug-Sep 2025 TRIM/budget/school pass | Capture property-tax, millage, budget adoption, school planning, and rezoning context | Budget/OMB, Property Appraiser, Tax Collector, Clerk, BCC, School Board/BoardDocs, PZA, public notices | `data/monthly/2025-08/` and `data/monthly/2025-09/` with discovered items, clusters, source gaps, wraps, reports | Large |
| May 2026 second pass | Fill gaps left by official-only first pass | BCC decisions, PZA, NBOR road/development notices, CDDs if approved, community/developer pages, St. Johns Citizen context | Addendum report and possibly updated source gaps; avoid rewriting original baseline without review | Medium |
| Budget/TRIM seasonal template | Reusable backfill/runbook for Jul-Sep cycles | Search terms `ST-0401` to `ST-0404`, budget stack, PA/Tax Collector, Clerk/VAB, BCC | `prompts/hermes_budget_trim_backfill_task.md` or generalized backfill task | Medium |
| School rezoning template | Reusable backfill/runbook for attendance-boundary cycles | SJCSD, BoardDocs, zoning/new schools, school-capacity search terms, relevant communities | School-capacity source gap report and monitor updates | Medium |

### Ongoing Backfill Cadence

- Run one historical month or focused seasonal window per month while the live
  monitor stack is still maturing.
- Prefer focused backfills over broad archives: budget/TRIM, school zoning,
  road projects, CDD assessments, or development approvals.
- Do not update the live dedupe index from exploratory backfill unless Buddy
  approves; keep backfill dedupe month-scoped.
- After every backfill, update source gaps, taxonomy gaps, search-term
  effectiveness, and monitor specs.

### How Backfill Feeds Improvements

| Backfill Finding | Feeds Into |
|------------------|------------|
| Repeated source gap | New source candidate or monitor spec |
| Repeated taxonomy gap | Taxonomy proposal with real item evidence |
| High-noise source | Filter rules and editorial bulk-dismiss policy |
| Missing official authority | Source-family verification rule |
| Repeated community/corridor mention | Community registry or beat candidate update |
| Successful search term | Search discovery prompt priority list |

---

## 4. Phase 5 Plan: Workflow Automation

The repo does not need "Hermes" specifically. It needs a small automation
runtime that can execute bounded source jobs, write deterministic artifacts,
and stop safely.

### Minimum Runtime Requirements

| Capability | Requirement |
|------------|-------------|
| Source selection | Read registry plus cadence state; select one source per run unless catch-up rules allow two. |
| Fetch/extract | Support HTTP HTML first; add browser and PDF workers only for sources that need them. |
| Dedupe | Read/write `data/index/prior_items.yaml`; keep normalized URL and title/date fallback. |
| Validation | Validate YAML shape and taxonomy values before marking run complete. |
| Logging | Write run logs, worker logs, warnings, and source health status. |
| Failure handling | Record HTTP errors, parse failures, zero-item runs, stale data, and selector drift. |
| Review queue handoff | Every extracted item starts `pending_review`; sensitive items get priority flags. |
| No publication | Runtime must never publish or alert externally until those boundaries are approved. |

### HERMES-003 Search Discovery Task Design

Expand `prompts/hermes_search_discovery_task.md` into a full contract with:

- Inputs: search-term IDs, date window, source/candidate registries, taxonomy,
  community registry, and allowed source scope.
- Source rules: public web only; no private groups, login-gated portals,
  paywalled extraction, fake accounts, or impersonation.
- Search plan: local media discovery (`ST-0701` to `ST-0705`), community terms,
  CDD terms, corridor terms, and source-gap-driven terms.
- Output 1: candidate source records in a review artifact, not silent registry
  promotion.
- Output 2: orphan intel items in `data/intel_items/{YYYY-MM-DD}/web_discovery.yaml`.
- Output 3: search-term effectiveness log with useful, noisy, zero-result, and
  private/gated results.
- Output 4: recommended registry/search-term changes for architect review.
- Completion criteria: every assigned term attempted, duplicates checked
  against canonical and candidate registries, sensitive/orphan items flagged,
  and no publication.

### Daily Cadence Handling

Daily automation should stay intentionally narrow:

1. Read `logs/runs/daily/LAST_RUN`.
2. Select one due daily source by priority.
3. Execute one bounded monitor job.
4. Validate output YAML and taxonomy values.
5. Update prior index only for valid new items.
6. Write worker log and meta-run log.
7. Update `LAST_RUN`.
8. Stop.

Catch-up rule: if more than two daily runs were missed, run two daily sources
maximum, then stop. Avoid batch-monitoring all daily sources until reliability
is proven.

### Alerting For Failures And Stale Data

Before public alerts exist, use internal alert artifacts:

| Condition | Internal Alert |
|-----------|----------------|
| Source HTTP error | Add entry to `logs/runs/{cadence}/` and source health report. |
| Parser returns zero candidates unexpectedly | Mark `warning`; compare to expected zero-item behavior for source. |
| Source stale beyond expected cadence | Add weekly source-health item for review. |
| Sensitive urgent item | Add priority review queue item; do not publish or send external alert. |
| Repeated failure 3 times | Mark source `failing` or create backlog item after architect review. |

---

## 5. Phase 6 Plan: Editorial & Review Pipeline

Phase 6 must come before public publishing. The review queue is the boundary
between internal intelligence collection and public-facing information.

### ED-001 Review Queue Design

Start with file-based artifacts before building UI:

```text
data/review_queue/
  pending.yaml
  in_review.yaml
  approved.yaml
  rejected.yaml
  published.yaml
  corrections.yaml
```

Each queue entry should include:

- `item_id`
- `title`
- `source_id`
- `source_url`
- `source_published_at`
- `summary`
- `topics`
- `interest_tags`
- `urgency`
- `sensitivity`
- `human_review_required`
- `verification_status`
- `recommended_channels`
- `review_status`
- `review_priority`
- `reviewer_notes`
- `decision`
- `decision_reason`
- `approved_channels`
- `reviewed_at`
- `reviewed_by`

Priority order:

1. `urgency: urgent`
2. `sensitivity: high`
3. `human_review_required: true`
4. Timely meeting/deadline items
5. FIFO for normal items

### ED-002 Corrections Policy Draft

The policy should define:

- How a resident reports an error.
- What counts as correction, clarification, update, or retraction.
- Requirement that every public item has source URL(s).
- How corrected items link to original `item_id`.
- How `superseded_by`, `updated_at`, and `reviewer_notes` are used.
- Who can approve corrections before public site launch.
- How sensitive/legal/public-safety corrections are escalated to Buddy.

### Item Flow

```text
monitor/backfill/search discovery
  -> intel item YAML (`pending_review`)
  -> review queue ingest
  -> editorial review
  -> approved / rejected / changes_requested / archive
  -> public site build consumes approved items only
  -> published item gets `review_status: published`
  -> corrections workflow handles updates
```

Publication rules:

- `pending_review`, `in_review`, `changes_requested`, `rejected`, and
  `internal_only` items are never public.
- Crime, legal, school-safety, public-safety, active emergency, controversy,
  named-individual, and minor-related items require human review.
- Local media context can point to tips, but consequential claims need official
  confirmation before public use.

---

## 6. Phase 7 Plan: Public Site

### What Should Be Public

Public site should only include reviewed, approved, source-backed information:

- Approved item summaries with direct source links.
- Weekly resident briefings.
- Monthly wraps that have been reviewed and edited.
- Source directory for public official sources.
- Topic pages for roads, utilities, schools, development, budget/taxes,
  emergency/weather, and CDDs after CDD approval.
- Corrections page and contact method.

### What Should Stay Private

- Raw monitor outputs before review.
- `pending_review`, rejected, archived, and internal-only items.
- Reviewer notes that include uncertainty or operational details.
- Search-discovery leads not yet verified.
- Sensitive crime/legal/school-safety details beyond official reviewed facts.
- Any private, login-gated, paywalled, forwarded, or resident-group material.
- Automation logs, errors, and source-health internals.

### Publishing Cadence

Recommended launch cadence:

| Channel | Cadence | Rationale |
|---------|---------|-----------|
| Website item feed | Daily after approval | Only approved items; no automatic public release. |
| Weekly resident brief | Weekly | Best initial product; controlled editorial workload. |
| Monthly wrap | Monthly | Builds from existing backfill/monthly structure. |
| Alerts | Later | Only after human review and clear urgent-item policy. |

### Infrastructure Options

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| GitHub Pages static site | Simple, cheap, versioned, fits YAML-to-static workflow | Public repo visibility must be considered; build pipeline needed | Best first option if repo/public-data boundary is clear. |
| Static site in separate public repo | Keeps internal data private; publishes approved JSON/Markdown only | Requires export step and repo sync | Best safety posture. |
| Netlify/Vercel static deploy | Easy previews and build hooks | More moving parts/accounts | Good later if UI needs grow. |
| Full database/CMS | Review UI possible | Overbuilt for first launch | Defer. |

Recommended architecture: keep this repo internal, export approved public
items to a separate static-site artifact/repo. Build the site from approved
Markdown/JSON only.

### Corrections Before Launch

Do not launch until:

- Review queue exists and has processed real monitor/backfill items.
- Corrections policy exists.
- Approved item export excludes internal fields.
- Public pages show source links and update timestamps.
- Sensitive categories have documented human-review rules.
- Buddy approves publishing name/brand and public/private boundary.

---

## 7. Priority-Ordered Build Plan

### Phase 3: Monitor Readiness And Source Cleanup

| Priority | Work | Effort | Dependencies | Buddy Decision? |
|----------|------|--------|--------------|-----------------|
| 1 | Reconcile stale state/docs/backlog: road closure readiness, ROADMAP phase, Clerk task, missing monthly run-log path | Small | None | No |
| 2 | Write formal specs for `sjc_county_news` and `sjso_news_stories` from pilot lessons | Small | Existing pilots | No |
| 3 | Finalize NBOR-backed `sjc_road_closures` monitor design and registry monitor config | Medium | NBOR findings | No for design; yes before unsupervised live runs |
| 4 | Create `sjc_emergency_management` monitor spec | Medium | Human review policy for urgent items | No for design |
| 5 | Create `st_johns_citizen` media-context monitor spec | Medium | Media verification policy | No for design |
| 6 | Update school and BCC specs with pilot/investigation findings | Small | Existing specs/logs | No |
| 7 | Create specs for PZA, Development Tracker, Permit Status, FDOT/NFLRoads | Medium/Large | Browser/API investigations | No for design |
| 8 | Prepare Tier 3 CDD promotion packet | Medium | Candidate URL verification | Yes for promotion |

### Phase 4: Backfill Pipeline

| Priority | Work | Effort | Dependencies | Buddy Decision? |
|----------|------|--------|--------------|-----------------|
| 1 | Draft Aug-Sep 2025 backfill plan | Medium | May backfill lessons | No |
| 2 | Build generalized backfill prompt from May template | Medium | Plan approval | No for template |
| 3 | Run Aug-Sep 2025 backfill | Large | Explicit instruction | Yes |
| 4 | Run May 2026 second pass for NBOR/BCC/PZA/CDD/media gaps | Medium/Large | CDD/media scope decision | Yes if live backfill |
| 5 | Promote taxonomy proposals with evidence (`budget_millage`; `water_restrictions` already present) | Small | Real item evidence | Yes for taxonomy changes |

### Phase 5: Automation Runtime

| Priority | Work | Effort | Dependencies | Buddy Decision? |
|----------|------|--------|--------------|-----------------|
| 1 | Define local runtime interface: `source_id`, date, dry-run/write modes, output paths | Medium | Monitor specs | No |
| 2 | Implement HTML monitor runner for easy sources | Medium | Specs for utility/county/SJSO/school | No if manual-only |
| 3 | Add validation and source-health reports | Medium | Schema/taxonomy stable | No |
| 4 | Expand HERMES-003 search discovery contract | Small/Medium | Search terms | No |
| 5 | Add browser/PDF worker path for BoardDocs/BCC/development map/permit portal | Large | Investigations | No for manual tooling |
| 6 | Enable unattended scheduling | Small | Runtime stable | Yes |

### Phase 6: Editorial Review

| Priority | Work | Effort | Dependencies | Buddy Decision? |
|----------|------|--------|--------------|-----------------|
| 1 | Design file-based review queue | Medium | Schema fields | No |
| 2 | Build queue ingest from monitor/backfill outputs | Medium | Runtime outputs | No |
| 3 | Draft corrections policy | Small | Publishing intent | Yes for policy approval |
| 4 | Add approval/export artifact for public site | Medium | Review queue stable | Yes before publishing |

### Phase 7: Public Site

| Priority | Work | Effort | Dependencies | Buddy Decision? |
|----------|------|--------|--------------|-----------------|
| 1 | Decide public name/brand | Small | None | Yes |
| 2 | Define public data export schema | Medium | Review queue | Yes for public/private boundary |
| 3 | Build static site prototype from approved sample items | Medium | Approved sample items | Yes before launch |
| 4 | Add weekly brief/monthly wrap pages | Medium | Editorial cadence | Yes |
| 5 | Launch | Medium | Corrections, review, approved content, hosting | Yes |

---

## 8. Open Decisions For Buddy

### Phase 3 Decisions

- Approve whether Tier 3 CDD sources should be promoted now:
  Tolomato CDD, Trout Creek CDD, Six Mile Creek CDD, and the correct Twin
  Creeks/Meadow View source split for Beachwalk/Beacon Lake.
- Decide whether community/developer sources should wait until after official
  CDD governance is active.
- Resolve Property Appraiser canonical URL: `sjcpa.gov` vs `sjcpa.us`.
- Confirm whether stale Clerk cleanup is complete with
  `sjc_clerk_online_research`, or whether additional registry cleanup is
  required.
- Confirm whether St. Johns Citizen should be daily headline/context-only or
  less frequent until editorial review exists.

### Phase 4 Decisions

- Authorize or defer Aug-Sep 2025 backfill execution.
- Decide whether May 2026 second pass may include CDD/community/media sources.
- Decide whether backfill items should ever update the live dedupe index.
- Approve taxonomy additions beyond existing `water_restrictions`, especially
  `budget_millage` and future `cdd_governance` evidence.

### Phase 5 Decisions

- Define automation boundary:
  - Manual local runner only.
  - Semi-automated runner invoked by Buddy.
  - Scheduled local cron/launchd.
  - Hosted CI schedule.
- Decide who receives internal failure/urgent-item alerts and by what channel.
- Decide whether browser automation is acceptable for public, non-login-gated
  sources such as BoardDocs, GIS maps, and permit search.

### Phase 6 Decisions

- Decide who can approve items for publication.
- Decide whether low-sensitivity official items may be AI-reviewed with human
  spot checks, or whether every public item needs human approval at launch.
- Approve corrections policy.
- Define escalation rules for public safety, legal, school safety, crime,
  controversy, and named individuals.

### Phase 7 Decisions

- Choose public product name/brand.
- Decide public hosting model: same repo artifact vs separate public repo.
- Decide what data fields are public:
  recommended public fields are title, summary, source name, source URL,
  source date, topics, communities, urgency, update timestamp, and correction
  status.
- Decide what stays private:
  raw excerpts, reviewer notes, internal-only channels, source-health logs,
  rejected items, search leads, and sensitive operational notes.
- Decide initial launch cadence: weekly brief first, daily reviewed feed later.

---

## Next Step Recommendation

Buddy should approve **Phase 3 first**: source-of-truth cleanup plus monitor
readiness design for the daily and weekly sources. The agent should start by
reconciling stale docs/backlog entries, then write formal monitor specs for
`sjc_county_news`, `sjso_news_stories`, NBOR-backed `sjc_road_closures`, and
`sjc_emergency_management`.
