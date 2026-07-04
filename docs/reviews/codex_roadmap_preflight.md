# Codex Roadmap Preflight

> Prepared 2026-07-04 before the next Codex planning session.
> This is an honest current-state assessment, not a roadmap.

---

## 1. Executive Summary

SJC_Intel has completed its first buildout cycle. The pipeline works end to
end: sources → source_events → intel_items → review queue + dedupe + interest
filters + tracked entities. Daily and weekly monitoring exists for about a
third of registered sources. Coverage is heavily concentrated on June 2026
and SilverLeaf. Large gaps remain in time periods, communities, source
families, automation, and human-readable output.

The system currently serves developers and agents well but produces no output
a resident could read. The review queue (132 items, 43 pending) is the closest
thing to a deliverable — but it is a YAML file with no human-friendly view.

The next roadmap must decide between deepening existing coverage, expanding
to new communities, building search/automation, creating resident-facing
output, or some combination. These are not compatible without prioritization.

---

## 2. Stakeholder Definition

**Current primary:** Residents of SilverLeaf and nearby St. Johns County
master-planned communities (Nocatee, Shearwater, TrailMark, Beachwalk).

**Expected expansion:** All St. Johns County residents.

**What residents cannot currently do:**
- See what was discovered this week in their community
- Filter items by relevance (entity, beat, urgency)
- Get notified about tracked entities that changed status
- Browse or search collected intelligence
- Distinguish official-record items from local-media leads

**What residents could do if the right reports existed:**
- "What road projects are happening near me?"
- "What's the status of the new school?"
- "Any development applications for my neighborhood?"
- "Has the CDD board changed anything recently?"
- "Is there a boil water notice I missed?"

---

## 3. Resident Questions the System Should Answer

| Question | Data Needed | Currently Answerable? |
|----------|-------------|----------------------|
| What's being built near me? | Intel items with development topic + community | Partially — 19 rezoning, 17 permit items; SilverLeaf coverage exists |
| Are there road closures? | NBOR ROW items | Yes for NBOR-covered areas |
| Is my school district changing? | School board docs, zoning items | No — BoardDocs pilot not active |
| Are there boil water notices? | Utility items with emergency_alerts | Only if NBOR or utility dept published |
| What did the BCC decide? | BCC agenda items | Only Jan 20, 2026 meeting extracted |
| What CDD business is happening? | CDD items | 9 CDD items (3 per CDD) — all vacancies/agenda notices |

---

## 4. Current Capabilities

### Existing
- Source registry (24 canonical, 46 candidates)
- Source_event model (NBOR, BCC, utility — partial coverage)
- Intel_item extraction (NBOR, BCC, utility, county news, sheriff, CDDs)
- Review queue (132 entries, 43 pending, 83 verified)
- Dedupe index (115 ids)
- Interest filters (9 rule groups, 219 lines)
- Tracked entities (10 entities, matched against queue)
- Run logs and agent logs
- Cadence system (daily/weekly/monthly with LAST_RUN markers)
- 2 extraction scripts (NBOR, BCC)
- Hermes task contracts (monitor, backfill, promotion, search discovery)
- YAML-based data storage
- Editorial review status model (pending → verified/rejected)

### Missing or Weak
- No automated daily monitoring
- No Hermes runtime
- No human-readable reports or dashboards
- No search-discipline execution (search terms untested)
- No web browser automation for interactive sources
- No St. Johns Citizen monitoring (tip/context only)
- No school district monitoring (BoardDocs pilot pending)
- No development tracker extraction (GIS map)
- No permit portal extraction (form-based)
- No FDOT/county roads extraction
- No PZA board records extraction
- No utility department extractor script (manual only)
- No monthly closeout since June 8
- No published output
- source_event coverage incomplete (county news, sheriff, utility lack events)

---

## 5. Current Data Inventory

| Source | Items | Date Range | Source Events? |
|--------|-------|------------|----------------|
| sjc_nbor_public_notices | 50 | Jun 8–Jul 4 | ✅ NBOR snapshots |
| sjc_bcc_calendar | 44 | Jan 20 only | ✅ (Jan 20 meeting; others flagged) |
| sjc_county_news | 9 | Jun 3–Jun 26 | ❌ |
| sjc_utility_department | 8 | Jun 3–Jul 4 | ❌ (partial) |
| sjso_news_stories | 5 | Jun 3–Jun 26 | ❌ |
| silverleaf_discovery | 6 | Jul 4 | ❌ (one-off discovery) |
| CDDs (3) | 9 | Jun 26 | ❌ |
| sjc_emergency_management | 1 | Jun 3 | ❌ |

Backfill data (non-monitored):
| Period | Items | Type |
|--------|-------|------|
| Aug-Sep 2025 | 43 | One-off backfill |
| May 2026 | 21 | One-off backfill |

### Queue Breakdown
| Status | Count |
|--------|-------|
| Verified | 83 |
| Pending | 43 |
| Escalated/high | 88 |
| Normal | 7 |
| Low | 30 |
| Immediate | 2 |

---

## 6. Current Architecture

```
             ┌──────────────┐
             │  sources.yaml │──24 canonical, 46 candidates
             └──────┬───────┘
                    │ HTTP GET / browser
                    ▼
          ┌──────────────────┐
          │  source_event    │──meeting, snapshot, press batch
          └──────┬───────────┘
                 │ parse + extract
                 ▼
          ┌──────────────────┐
          │   intel_item     │──structured finding
          └──────┬───────────┘
                 │
          ┌──────┴──────────┐
          ▼                 ▼
   ┌────────────┐   ┌──────────────┐
   │ review_queue│   │  dedupe      │
   │ 132 entries │   │  115 keys    │
   └────────────┘   └──────────────┘
          │
          ▼
   ┌──────────────────────┐
   │  interest_filters    │──keyword matching
   │  tracked_entities   │──entity matching
   └──────────────────────┘
```

Supporting: community registry, beat candidates, search terms, Hermes prompts.

---

## 7. Current Source and Community Coverage

### Communities with items
| Community | Items | Sources |
|-----------|-------|---------|
| Countywide | Most NBOR + BCC + utility + sheriff | Multiple |
| silverleaf | 6+ (discovery), plus ~12 NBOR items in area | st_johns_citizen, NBOR |
| nocatee | 3 (Ascension) + NBOR items | st_johns_citizen, NBOR |
| cr_210_corridor | BCC + NBOR items | Multiple |

### Communities with zero items
rivertown, shearwater, trailmark, beacon_lake, beachwalk, etown, seven_pines,
everrange, wildlight, ponte_vedra, st_augustine_beach, us_1_corridor.

These communities exist in the registry but have never been monitored or
searched. They represent the full-county expansion risk: adding 20+
communities will multiply surface area without a search/discovery system.

---

## 8. Current Gaps

### Time gaps
- Entirety of 2025 (except Aug-Sep backfill)
- Jan–Apr 2026 (except Jan 20 BCC)
- June 1–2, June 4–7 (cold start)
- No regular monthly closeout since June 8

### Source gaps
- School district (BoardDocs) — not monitored since May backfill
- Emergency management — seasonal, checked ad-hoc
- FDOT, county roads — not monitored
- Development tracker (GIS) — not automated
- Permit portal — not accessed
- PZA board records — not extracted
- Property appraiser, tax collector — not accessed
- St. Johns Citizen — no monitor; one-off search only
- CDD websites — not monitored (Tier 3 sources exist but no extraction)
- Nocatee community page — not monitored

### Workflow gaps
- No Hermes runtime for automation
- No utility extractor script (manual HTML parse)
- No search-discovery execution (search terms drafted but untested)
- No entity-search Hermes prompt
- No monthly report/wrap since June 8

### Output gaps
- No resident-facing report, dashboard, or digest
- Review queue is YAML-only — no human-readable view
- No "what's new this week" summary
- No tracked-entity status dashboard
- No notification system for tracked-entity status changes

---

## 9. Search/Browser-Automation Opportunities

Browser automation is available but currently unused. LLM agents could:
- Search St. Johns Citizen for community+entity+beat combinations
- Search county news, NBOR, BCC, and school sites for updates
- Navigate the development tracker GIS map for new projects
- Check CDD websites for meeting agendas and minutes
- Search property appraiser for ownership/tax changes
- Search FDOT/NFLRoads for project updates

### Search-query generation
The existing registries (communities, entities, beats, search_terms) already
contain the components for parameterized query generation:

```
"{community}" "{entity}" "{beat}" site:stjohns.k12.fl.us
"{community}" rezoning permit site:sjcfl.us
"{entity}" status update
```

### What is missing for search
1. Query prioritization (which entity to search first)
2. Query de-duplication (don't search the same thing twice)
3. Result deduplication (same article matching multiple queries)
4. Evidence-level classification (official vs news vs developer claim)
5. Browser-automation task definitions (page load, form fill, result scrape)

### Evidence hierarchy
| Level | Source Type | Example | Handling |
|-------|-------------|---------|----------|
| Official | Government website | sjcfl.us, sjso.org | Direct extraction, source_confirmed |
| News | Local media | sjcitizen.com | Tip/context, needs cross-ref |
| Developer | Community/developer site | nocatee.com | Lead, must verify with official |
| Lead | Social, forums, rumors | Facebook, Reddit | Excluded by policy |

---

## 10. Neighborhood Expansion Model Concerns

### Current community schema
```yaml
- id: "silverleaf"
  name: "SilverLeaf"
  type: "master_planned_community"
  parent_area: "northwest_st_johns"
  status: "active"
```

### What the schema lacks
- **Aliases** — "Silverleaf", "Silver Leaf", "SilverLeaf Florida"
- **Search keywords** — community-specific search shortcuts
- **Related sources** — CDD website, community website, developer page
- **Related entities** — Publix, K-8 school, mini golf (tracked entities)
- **Priority** — how important is this community to monitor
- **Geographic boundaries** — no GIS, street bounds, or zip codes
- **Adjacent communities** — "silverleaf adjacent to nocatee" not modeled

### Expansion risk
Adding 20+ communities without updating the community schema means each new
community requires scattered config changes across search_terms.yaml,
interest_filters.yaml, and manually maintained keyword lists. The community
registry should be the single source of truth for a community's search
profile, and the other registries should derive from it.

### Recommendation for Codex
Decide whether to enrich the community schema first or accept manual
registration for a few pilot expansions.

---

## 11. Knowledgebase Inclusion Workflow

### Current flow
```
source → source_event → intel_item → review queue → [human review] → verified
```

The "knowledgebase" is currently the set of verified intel items in the
review queue (83 verified). There is no separate curated layer.

### What is missing
- A "published" or "knowledgebase" status that marks items as curated
- A searchable index of verified items by community, entity, date, beat
- A way to bundle related items into stories/projects (cross-item clusters)
- An "entity timeline" — what happened with this entity over time

### Questions for Codex
1. Are verified queue items already the knowledgebase, or is a separate
   `data/knowledge/` directory needed?
2. Should items be promoted from `pending_review` → `verified` → `published`
   (3 states), or is a 2-state pipeline (pending → verified) sufficient for
   non-publishing mode?
3. Does "knowledgebase" mean "curated for a human to read later" or "ready
   for automated inclusion in a report"?

---

## 12. Missing Human-Readable Outputs

No current output is readable by a non-technical resident. The system
produces YAML files, markdown logs, and structured data — all invisible to
stakeholders.

### Minimal viable outputs (in rough priority)
1. **Community digest** — what happened this week in SilverLeaf (markdown)
2. **Entity status dashboard** — what stage is each tracked entity at
3. **Review queue top items** — what needs attention (for Buddy)
4. **Tracked entity timeline** — all intel items per entity, sorted by date

### Format recommendation
Markdown reports under `data/reports/{YYYY-MM-DD}/` — easy to read in any
viewer, no build toolchain needed.

---

## 13. Documentation/Stakeholder-Value Critique

### Docs that explain implementation well
- `README_INTERNAL.md` — architecture tables, open loops, agent cautions
- `docs/data_model.md` — object model, relationships, ID conventions
- `docs/design/tracked_entities_design.md` — entity design rationale

### Docs that explain purpose poorly
- `docs/taxonomy.md` — extensive vocabulary definitions, but no "why this
  matters to a resident"
- `docs/cadence.md` — operational detail, no stakeholder value linkage
- `docs/monitoring_workflow.md` — pipeline steps, no resident outcome
- `docs/discovery_loops.md` — process model, no "what residents will see"

### Missing explanations
- No doc answers "What can a resident do with this system today?"
- No doc explains what the review queue contains in human terms
- No doc shows an example of an output a resident would receive
- No doc describes the difference between verified and pending items for
  a reader

### Recommended changes
Not another doc sprawl pass. Add a `docs/stakeholder_value.md` (~20 lines)
that answers:
- Who this is for
- What concrete questions it answers
- What outputs exist today
- What outputs are coming next

---

## 14. Decisions Codex Must Make

### Critical
1. **Deepen or expand?** Deepen SilverLeaf/Nocatee coverage (fix BCC links,
   add PZA, automate school, add utility extractor) OR expand to new
   communities (RiverTown, Shearwater, TrailMark, etc.) OR build search
   automation (Hermes runtime + browser automation).

2. **Output layer priority.** Build human-readable reports first (maximize
   stakeholder value) or build infrastructure first (search, automation,
   expansion).

3. **Community schema upgrade.** Enrich the community registry before or
   after expansion. If after, accept manual config churn for each new
   community.

### Important
4. **Hermes runtime priority.** Is automated daily monitoring the highest
   value next step, or can manual cadence runs continue?

5. **Knowledgebase model.** Is the set of verified intel items sufficient,
   or is a separate curated index needed?

6. **School district.** BoardDocs pilot has been pending since June 26. Is
   school coverage a priority for Phase 3?

### Deferrable
7. **Tier 3/4 source promotion.** 11 CDD and community sources remain
   unpromoted. These are lower value than fixing BCC/utility/school gaps.
8. **ENTITY-003 (additional seeding).** 5+ more entities could be added to
   tracked_entities.yaml. Should not block other work.
9. **Publishing/newsletter.** Explicitly out of scope per durable decisions.
10. **Local-media monitoring.** St. Johns Citizen integration would increase
    volume but adds uncertainty. Defer unless search automation is built.

---

## 15. Constraints for the Next Roadmap

1. **Public sources only.**
2. **No cron, launchd, or scheduled automation.**
3. **No publishing or newsletter.**
4. **No private Facebook groups or login-gated content.**
5. **Implementation-ready for weaker Workers** — each task must specify
   exact input files, output files, context files, and validation criteria.
6. **Git Steward commits after each session** — no broad `git add .`.
7. **HITL checkpoints** — Buddy must review between major phases.
8. **Durable decisions not reversed** — official records first, local media
   context-only, memory stays concise.
9. **Data-model changes require schema updates** — no silent field additions.
10. **Stakeholder value before infrastructure** — prefer features someone
    can see over features that make the system tidier.

---

## 16. Recommended Codex Prompt

```
You are a high-reasoning Codex planning agent for SJC_Intel, an AI-assisted
local-intelligence system for St. Johns County, Florida.

## Repo State
Working tree is clean at commit cf9a8e3.
Latest commits built the tracked-entities model and queue integration.
Prior work established: source registry (24 sources), source_events,
intel_items, review queue (132 items, 83 verified), dedupe (115 keys),
interest filters (9 groups), tracked entities (10), cadence system (daily/
weekly/monthly), Hermes task contracts, agent definitions.

## Current Pipeline
sources → source_events → intel_items → review queue → [interest filters +
tracked entities matching at build time]

## Key Data Profile
- 132 review queue entries (43 pending, 83 verified)
- Items from: NBOR (50), BCC (44), county news (9), utility (8), sheriff (5),
  CDDs (9), silverleaf_discovery (6), emergency (1)
- Coverage concentrated Jun 3–Jul 4; one BCC meeting (Jan 20) and one-off
  Aug-Sep 2025 backfill (43 items)
- Tracked entities: 10 (Publix, Harris Teeter, K-8 school, mini golf,
  CR 2209, Ascension, Fairfield Inn, Nocatee retail, SR 207 WRF, SilverLeaf)
- Entity matching: 11 matches across 8 items, 0 false positives

## Stakeholder
Primary: SilverLeaf/St. Johns County residents wanting to know about
development, roads, schools, utilities, CDD decisions, and safety changes
affecting their daily lives.

## What You Must Produce
A phased roadmap that:

### Phase Requirements
Each phase must be:
1. A bounded work session (single Worker, single session ideally)
2. Implementable by a weaker (intern-level) Worker
3. Explicit about:
   - Required context files (exact paths)
   - Files to create/modify
   - Schema/data-model changes, if any
   - Validation and pass/fail criteria
   - HITL review point
   - Git Steward commit boundary
4. Ordered by:
   - Stakeholder value (what does a resident gain?)
   - Architectural dependency (what must exist first?)
   - Risk (prefer safe, reversible changes over risky ones)

### Topics Codex Must Address
1. **Resident output layer.** What is the minimum viable human-readable
   report/digest? How should it be formatted and where stored?
2. **Source gaps closure.** Which of these gaps are highest value to fix:
   BCC June agendas, school BoardDocs, utility extractor, PZA records,
   FDOT/roads, development tracker, emergency management daily check?
3. **Search/discovery automation.** How should the search discovery loop
   (Loop B) be implemented using browser automation and LLM agents?
   Consider query generation from existing registries, result handling,
   and evidence classification.
4. **Neighborhood expansion.** Should the community schema be enriched
   (aliases, search keywords, related sources, priority) before expanding
   to new communities? Or can safe manual registration continue for a few
   more communities?
5. **Knowledgebase inclusion.** Define what "knowledgebase" means in this
   repo. Is it the set of verified queue items? A separate curated layer?
   How do items flow into it?
6. **Tracked entities — ENT-003 and ENT-004.** Are additional entity
   seeding and the stakeholder onboarding doc worth a dedicated phase, or
   should they be merged into other phases?
7. **Cadence system maturity.** Are the LAST_RUN markers sufficient, or
   should the cadence system track per-source last-checked timestamps?

### Output Format
Return a structured document with:
1. Executive summary of roadmap priorities
2. Phase table (phase #, focus, stakeholder value, estimated sessions, dependencies)
3. For each phase:
   - Purpose (1-2 sentences)
   - Stakeholder value (what a resident gains)
   - Context files to read
   - Files to create/change
   - Schema changes (if any)
   - Validation criteria
   - HITL checkpoint location
   - Git commit boundary
4. Deferred items (explicitly listed as not in scope)
5. Architectural risks and open questions

### Key Files to Inspect
- README_INTERNAL.md
- AGENTS.md
- BACKLOG.md
- docs/data_model.md
- docs/taxonomy.md
- docs/cadence.md
- docs/discovery_loops.md
- docs/monitoring_workflow.md
- docs/design/tracked_entities_design.md
- docs/data_inventory/GAPS.md
- docs/reviews/codex_roadmap_preflight.md (this file)
- registry/sources.yaml
- registry/communities.yaml
- registry/interest_filters.yaml
- registry/tracked_entities.yaml
- data/review_queue/summary.yaml
- schemas/*.yaml
- scripts/build_review_queue.py
- scripts/extract_nbor.py
- scripts/extract_bcc_agenda.py
- prompts/known_source_monitor_task.md
- logs/runs/daily/LAST_RUN
- data/monthly/aug_sep_2025_crosscut.md
```

---

## 17. Key Files Codex Should Inspect

Listed in the recommended prompt above. The preflight file (`this file`) is
the distillation.
