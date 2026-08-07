# SJC_Intel — Discovery Loops

> Operating model: SJC_Intel runs as a set of independent but coordinated
> discovery loops, not a single linear pipeline. Each loop has a purpose,
> a trigger, inputs, outputs, and an owner.

## Why Loops?

The repo audit showed a system designed around a single linear pipeline:

```
source → fetch → extract → classify → review → publish
```

But St. Johns County intelligence doesn't work that way. Information
arrives through multiple channels at different cadences:

- **Known sources** (county news, sheriff press releases) can be polled daily.
- **Unknown sources** (community Facebook groups, HOA pages, developer sites)
  must be searched for.
- **History** (what happened in May 2026?) must be backfilled.
- **Cross-cutting themes** (traffic, school capacity, development) emerge from
  many sources and need their own aggregation.
- **Taxonomy** must evolve as new topics and communities are discovered.
- **Editorial review** must gate everything before publication.

The loop model makes each of these a first-class process with its own
trigger, its own agent role, and its own output artifacts.

## Deep Research Operating Principles

The 2026-06-03 homeowner public-source report changed the operating baseline:

- Official records are the first authority for consequential claims. Local
  media is useful for tips, context, and story surfacing, but official records
  should resolve claims about votes, permits, taxes, CDD assessments, roads,
  schools, utilities, public safety, and legal notices.
- Source families matter more than isolated URLs. Monitor stacks such as
  County Commission/Clerk/GovTV, PZA/Growth Management, utility/SJRWMD,
  SJCSD/BoardDocs/zoning, and CDD/public notices.
- CDD governance is a first-class homeowner source family because assessments,
  district debt, amenities, and maintenance decisions directly affect carrying
  costs and daily life.
- Utilities/water and transportation/roadwork are daily resident-impact beats.
- Community/developer pages are useful for amenities, phases, retail hints, and
  events; governance and financial claims should resolve to public records.
- May 2026 is the first historical backfill baseline. January 2026 is deferred.

---

## A. Known-Source Monitoring Loop

**Purpose:** Poll registered sources in `registry/sources.yaml` for new items.

**Trigger:** Cron schedule (daily/weekly/monthly per source record).

**Inputs:**
- Source record from `registry/sources.yaml`
- Prior items index from `data/index/prior_items.yaml`

**Steps:**
1. Fetch source URL (HTTP GET or browser)
2. Parse HTML, extract candidate items
3. Deduplicate against prior items index
4. Factual classify (topics, communities, geographic scope, urgency)
5. Resident-interest classify (primary_topic, interest_tags, relevance)
6. Structure into intel_item (v2.0 schema)
7. Apply sensitivity defaults (sensitivity, review_status, channels)
8. Write output to `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml`
9. Update dedupe index
10. Route to editorial review queue

**Owner:** `source-monitor` worker role

**Status:** Design complete. Two pilots proven (county, sheriff).
Not yet automated via Hermes.

---

## B. Search Discovery Loop

**Purpose:** Discover sources and items NOT in the registry by searching
the public web for community names, neighborhood names, school names,
roads, corridors, builders, developments, and topics.

**Trigger:** Weekly or after registry changes. Adaptive operation uses an
explicit visible-state cutoff, bounded search budget, independent proposal
evaluation, and next-week-only accepted transitions; see
`docs/adaptive_discovery_backtest.md`.

**Inputs:**
- Search term list generated from `registry/communities.yaml`,
  `registry/sources.yaml`, known topics, school names, corridor names,
  builder/developer names, and prior monthly wraps.
- Optionally: prior months' topic clusters for gap detection.

**Steps:**
1. Generate search terms from registries and taxonomy (see §How Search
   Terms Are Generated below).
2. For each term, search public web / news (from within current month
   or unbounded if backfilling).
3. For each result:
   a. Classify: Is this a new **source** (website/channel to monitor)?
      Or a one-off **item** (news article, event, post)?
   b. If it's a new source: create a proposed source record and add
      to a candidate-sources queue for human review.
   c. If it's a one-off item: extract into an intel_item and route
      to editorial review.
4. Track which terms returned useful results and which returned nothing.
5. Propose new registry entries, taxonomy additions, or search term
   refinements as `taxonomy_gap` or source-gap notes.

**Outputs:**
- Candidate source records (for registry addition)
- Orphan intel_items (items from non-registered sources)
- Search term effectiveness log
- Source gap notes

**Owner:** `search-discovery-worker` role

**Status:** Design only. Not yet piloted.

### Why This Loop Exists (Real Example)

**St. Johns Citizen** was discovered accidentally by Buddy on Facebook
(see `docs/source_discoveries/st_johns_citizen.md`). It appears to be a
legitimate local reporting/media organization covering St. Johns County
government, development, public safety, and community life — directly
overlapping with SJC_Intel's mission.

This accidental discovery proves that:
1. Similar organizations probably exist and haven't been found.
2. The search discovery loop must include **social-platform search**
   (Facebook, Instagram, Substack), not only Google/news web search.
3. Discovered organizations should first enter `registry/source_candidates.yaml`
   as candidates, not directly into canonical monitoring.

### Local Media Discovery Sub-Loop

The Search Discovery Loop now includes an explicit **local media discovery**
sub-category for finding local reporting/social-news organizations.
Search patterns are defined in `registry/search_terms.yaml` under the
`local_media_discovery` category.

Discovery targets include:
- Local news websites and blogs
- Facebook pages focused on St. Johns County news
- Community/neighborhood Facebook groups with regular reporting
- Instagram accounts doing local coverage
- Substack and other newsletter platforms
- Independent journalists covering the county
- HOA and community association publications

Each discovered organization should be:
1. Documented in `docs/source_discoveries/{name}.md` with assessment
2. Added to `registry/source_candidates.yaml` as a candidate
3. Reviewed for source quality, reliability, and mission alignment
4. Promoted to canonical sources only after review

#### Lessons from St. Johns Citizen Source Review

The St. Johns Citizen source review (see `docs/source_reviews/st_johns_citizen_review.md`)
revealed the following signals that indicate a **high-quality local media source**
worth flagging for promotion:

| # | Signal | Source Review Finding |
|---|--------|---------------------|
| 1 | Named publishers with verifiable journalism backgrounds | Former NY Post Bureau Chief, former Fox News senior reporter |
| 2 | Multiple named contributors | 9+ named contributors with bios |
| 3 | Daily publishing cadence | Multiple articles published every day |
| 4 | Professional website with dedicated sections | 6+ sections: News, Eats, Sports, Lifestyle, Real Estate, Florida |
| 5 | Original reporting (not aggregation) | Each article appears to be original journalism |
| 6 | Advertising/sponsorship infrastructure | Dedicated rate card with measurable metrics |
| 7 | Newsletter with subscriber metrics | 7,800 subscribers, 61% open rate |
| 8 | Social media as tracked distribution channel | 67,000 social media followers claimed |
| 9 | Public contact information | Phone, email, physical presence |
| 10 | Clear geographic focus | St. Johns County + specific communities |
| 11 | Topic breadth across homeowner-relevant beats | Gov, crime, development, real estate, food, sports, events |
| 12 | Authority signals ("Has been cited by" or similar) | "Has been cited by" section on homepage |

**Key insight:** If a local media org has 4+ of these signals, it is
likely legitimate and worth promoting to candidate status. If it has 8+,
it is likely a high-value source suitable for daily monitoring.

#### Search Pattern Refinements from the Review

The St. Johns Citizen review identified additional discovery patterns:
- Former national journalists (bureau chiefs, senior reporters) who
  relocate to St. Johns County often start local news outlets
- Look for journalists on LinkedIn with St. Johns County connections
- Search for "former" + journalist/reporter + community name
- Search for community-specific news outlets (Nocatee news, Ponte Vedra
  news, St. Augustine citizen news)
- Search for "publisher" or "journalist" or "reporter" + community name

These patterns are added to `registry/search_terms.yaml` under the
`local_media_discovery` category.

---

## C. Historical Backfill Loop

**Purpose:** Systematically work backward month-by-month through 2026
(and earlier if useful) to:
- Build an intelligence baseline for each month
- Discover recurring issues and source gaps
- Train taxonomy and beat identification
- Produce monthly wraps

**Trigger:** Manual start, then sequential after results are reviewed. Start
with May 2026, then consider August-September 2025 for TRIM/budget and
school-rezoning context, then older months as needed.

**Inputs:**
- Community registry
- Known topics and interest tags
- Prior months' wraps (for gap detection)
- Public web search results for each target month

**Steps:**
1. Select target month (start with May 2026).
2. Search public web for St. Johns County + community names + topics
   filtered to that month.
3. Extract all discovered items into `data/monthly/{YYYY-MM}/discovered_items.yaml`.
4. Cluster items by topic → `data/monthly/{YYYY-MM}/topic_clusters.yaml`.
5. Identify source gaps → `data/monthly/{YYYY-MM}/source_gaps.md`.
6. Write monthly wrap → `data/monthly/{YYYY-MM}/monthly_wrap.md`.
7. Collect taxonomy_gap proposals for architect review.
8. Proceed to next month.

**Outputs:**
- `data/monthly/{YYYY-MM}/discovered_items.yaml`
- `data/monthly/{YYYY-MM}/topic_clusters.yaml`
- `data/monthly/{YYYY-MM}/source_gaps.md`
- `data/monthly/{YYYY-MM}/monthly_wrap.md`

**Owner:** `historical-backfill-worker` role

**Status:** Design only. Not yet piloted. First experiment proposed for
May 2026 (see §First Historical Backfill Experiment below).

---

## D. Cross-Section / Beat Discovery Loop

**Purpose:** Detect recurring themes that cut across multiple sources and
communities — beats like "construction," "school capacity," "traffic,"
"new retail," "CDD/HOA," "water restrictions," "public safety." These
beats don't come from any single source. They emerge from clustering.

**Trigger:** Monthly, after monthly wrap is produced.

**Inputs:**
- All intel items from the past month (from monitoring + backfill)
- Topic clusters from monthly backfill
- Prior beat assignments

**Steps:**
1. Collect all items from the past month across all sources.
2. Cluster items by shared topics, interest_tags, and communities.
3. For each cluster with ≥3 items:
   a. Propose a beat label (e.g., "CR 210 construction impacts").
   b. Assign a severity/attention level.
   c. Check if the beat has appeared in prior months (recurring? new?).
4. For recurring beats with no dedicated source, propose a new
   source discovery search.
5. For beats that span 3+ communities, propose a county-wide summary.
6. For beats that don't fit existing taxonomy, propose new tags.

**Outputs:**
- Beat registry (living document of identified beats)
- Source discovery recommendations
- Taxonomy addition proposals
- Cross-section summary candidates

**Owner:** `beat-clustering-worker` role

**Status:** Design only. Requires at least 1-2 months of data to function.

---

## E. Taxonomy Improvement Loop

**Purpose:** Collect taxonomy_gap proposals from all other loops,
group similar proposals, and recommend controlled vocabulary changes.
Only `sjc-intel-architect` or Buddy may approve canonical changes.

**Trigger:** After any loop produces a `taxonomy_gap` proposal, or weekly
review of accumulated gaps.

**Inputs:**
- `taxonomy_gap` fields from intel items
- Source gap notes from search discovery
- Beat proposals from cross-section clustering
- Manual observations from editorial review

**Steps:**
1. Collect all open taxonomy_gap proposals.
2. Group by similarity (aliases, near-duplicates).
3. For each group:
   a. Assess: Does this fill a real gap? Or does an existing tag work?
   b. If real gap: draft the proposed addition with definition and
      classification rule.
   c. If existing tag covers it: close with reference to existing tag.
4. Present grouped proposals for approval.
5. On approval, update `docs/taxonomy.md` and `schemas/intel_item.schema.yaml`
   if needed.
6. Close processed proposals.

**Outputs:**
- Taxonomy change proposals
- Updated taxonomy doc
- Closed gap proposals

**Owner:** `taxonomy-steward` role (initially sjc-intel-architect)

**Status:** Design only. `taxonomy_gap` field exists in schema v2.0 but
no collection/processing loop has been run.

---

## F. Review / Editorial Loop

**Purpose:** Review candidate intel items from all other loops and decide
publish, reject, needs-verification, or archive. Keeps sensitive items
from becoming public automatically.

**Trigger:** Continuous — as items arrive in the review queue.

**Inputs:**
- Intel items from monitoring loop (with RI classification)
- Orphan items from search discovery
- Monthly wrap candidates from backfill
- Cross-section summaries from beat clustering

**Steps:**
1. Present items in priority order: `urgency: urgent` first,
   `sensitivity: high` second, then FIFO.
2. For each item:
   a. Review factual accuracy against source excerpt.
   b. Review RI classification for overreach.
   c. Check sensitivity and human_review_required flags.
   d. Decide: approve, reject, needs-verification, needs-changes, archive.
   e. If approve: assign to publishing channel(s).
   f. If reject: record reason (for training).
   g. If needs-verification: route back with specific questions.
   h. If archive: store for reference, no publication.
3. For items with `human_review_required: true`: MUST be reviewed by
   a human before any publication.
4. For items with `sensitivity: high`: flag for priority human review.

**Outputs:**
- Published items (ready for newsletter/website/social)
- Rejected items (with reasons, for loop improvement)
- Verification requests (routed back to discovery/monitoring)
- Archive items (stored for reference)

**Owner:** `editorial-reviewer` role (human or human-supervised AI)

**Status:** Design only. No review queue exists yet outside of documented
rules in the agent prompt.

---

## Loop Relationships

```
                    ┌──────────────────────────────┐
                    │   SEARCH DISCOVERY LOOP (B)   │
                    │  Finds new sources + items    │
                    └──────┬──────────────┬─────────┘
                           │              │
                    new sources      orphan items
                           │              │
                           ▼              ▼
                    ┌──────────┐   ┌──────────────┐
                    │ SOURCE   │   │  MONITORING  │
                    │ REGISTRY │──►│  LOOP (A)    │
                    └──────────┘   └──────┬───────┘
                                          │
                                    intel items
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │  REVIEW LOOP (F)      │
                              │  publish/reject/verify │
                              └───────────────────────┘
                                          ▲
                    ┌──────────────┐      │
                    │  BACKFILL    │──────┤
                    │  LOOP (C)    │ items│
                    └──────┬───────┘      │
                           │              │
                           ▼              │
                    ┌──────────────┐      │
                    │  BEAT /      │      │
                    │  CROSS-SEC   │──────┘
                    │  LOOP (D)    │ summaries
                    └──────┬───────┘
                           │
                    taxonomy_gap proposals
                           │
                           ▼
                    ┌──────────────────────┐
                    │ TAXONOMY LOOP (E)     │
                    │ Approve/reject gaps   │
                    └──────────────────────┘
```

---

## How Search Terms Are Generated

Search terms feed the Search Discovery Loop (B) and the Historical
Backfill Loop (C). They are generated from existing registries and
taxonomy.

### From Community Registry (`registry/communities.yaml`)

For each community with status `active` or `observed`:
- `"{community_name}" "St. Johns County"`
- `"{community_name}" news`
- `"{community_name}" development`
- `"{community_name}" HOA`

Examples:
- `"SilverLeaf" "St. Johns County"`
- `"Nocatee" news`
- `"RiverTown" development`
- `"CR 210" corridor`

### From Source Registry (`registry/sources.yaml`)

For each source with status `verified` or `active`:
- Search for the source's domain/topic uncovered by existing monitoring
  (e.g., if sjc_development_tracker is verified but not piloted, search
  for development news)

### From School Names

Schools in St. Johns County that may appear in news or community pages:
- Search `"{school name}" "St. Johns County"`
- Search `"{school}" rezoning boundary`
- Search `"{school}" construction expansion`

### From Corridor Names

Corridors are already in the community registry (`cr_210_corridor`,
`sr_16_corridor`, `us_1_corridor`). Additional corridor terms:
- `"I-95" "St. Johns County" construction`
- `"State Road 9B" extension`
- `"St. Johns Parkway"`

### From Known Topics

Generated from `docs/taxonomy.md` topics list + geography:
- `"St. Johns County" development`
- `"St. Johns County" traffic road construction`
- `"St. Johns County" school capacity`
- `"St. Johns County" water restrictions`
- `"St. Johns County" building permits`

### From Resident-Interest Tags

Generated from `docs/taxonomy.md` interest_tags + geography:
- `"St. Johns County" traffic impact`
- `"St. Johns County" safety concern`
- `"St. Johns County" cost impact`
- `"St. Johns County" property values`

### From Taxonomy Gaps

Any open `taxonomy_gap` values from intel items become candidate search
terms. Example: if a water-shortage item proposes a `drought_impact` tag,
search for `"St. Johns County" drought water restrictions`.

### From Prior Monthly Wraps

Key names and topics from the executive summaries of prior months become
follow-up search terms. Example: if May's wrap mentions "SilverLeaf
reclaimed-water restrictions," the next search pass should include
`"SilverLeaf" "reclaimed water" restriction`.

---

## First Historical Backfill Experiment: May 2026

### Target

Build a baseline month for May 2026 — the most recent full month before the
2026-06-03 Deep Research report.

### Approach

1. Search public web/news for St. Johns County + community names + major
   topics restricted to May 2026.
2. Extract all discovered items (sources + one-off items).
3. Cluster by topic.
4. Identify gaps vs. current source registry.
5. Write monthly wrap.

### Outputs

#### `data/monthly/2026-05/discovered_items.yaml`

All intel items found via search for May 2026. Each item follows the
intel_item schema v2.0. Source_id for one-off items: `web_discovery`.
May include items from sources not yet in the registry.

#### `data/monthly/2026-05/topic_clusters.yaml`

Groups of related items. Each cluster has:
```yaml
cluster_id: "2026-05-cluster-001"
label: "CR 210 widening project"
items:
  - "SJC-{id}"
  - "SJC-{id}"
count: 3
source_types: ["sjc_county_news", "web_discovery"]
communities: ["cr_210_corridor", "silverleaf"]
beat_candidate: "CR 210 construction impacts"
severity: "high"  # recurring, high-impact
```

#### `data/monthly/2026-05/source_gaps.md`

Sources that should have covered May 2026 items but aren't in the
registry, or are in the registry but weren't monitored retroactively.

Example:
```markdown
## Source Gap: SilverLeaf Community Page

**Evidence:** Multiple May 2026 search results reference
"SilverLeaf HOA updates" and "SilverLeaf construction phase 4"
from a community website not in the registry.

**Recommendation:** Find and register the SilverLeaf community
page as a new source.

**Search terms used:** "SilverLeaf" "St. Johns County", "SilverLeaf"
HOA
```

#### `data/monthly/2026-05/monthly_wrap.md`

Narrative summary of the month. See §Monthly Wrap Contents below.

### Treat as Exploratory

This is not journalism. The monthly wrap is an AI-generated intelligence
summary based on public web search. It will miss things, get some
emphases wrong, and occasionally hallucinate. Every claim should be
traceable back to a source item. The purpose is to:

1. Test whether the backfill loop produces useful output.
2. Identify sources we should register.
3. Identify taxonomy gaps.
4. Give the project a sense of what a monthly intelligence summary
   looks like.

---

## Monthly Wrap Contents

Each monthly wrap (`data/monthly/{YYYY-MM}/monthly_wrap.md`) should include:

### 1. Executive Summary
- 3-5 bullet points capturing the most significant developments
- Tone: neutral, factual, concise

### 2. Major Themes
- Top 3-5 themes that emerged during the month
- Each theme: 1-2 paragraphs with source references
- Examples: "Development approvals accelerated on CR 210 corridor,"
  "Water restrictions were a dominant concern county-wide"

### 3. Community Mentions
- Which communities appeared in discovered items
- Number of items per community
- Notable: communities with *no* mentions (gaps)

### 4. Construction / Development
- New projects announced
- Project phases (approvals, groundbreaking, completion)
- Building permits or zoning changes (if discoverable)
- Developer activity

### 5. Traffic / Roads
- Road closures and construction projects
- Accident patterns or safety concerns
- Transit or infrastructure updates

### 6. Schools
- School board decisions
- Capacity / rezoning news
- Safety / security updates
- New school construction

### 7. Public Safety
- Notable incidents and trends
- SJSO operations and press releases
- Fire / EMS activity (if discoverable)
- Emergency declarations

### 8. Events / Community Life
- Major community events
- Library programs, park openings, cultural events
- HOA or neighborhood association activity

### 9. Source Gaps
- Topics or communities with thin coverage
- Known sources not yet registered
- Sources in registry that should have had items but didn't

### 10. Taxonomy Gaps
- Proposed new topics, interest_tags, or audience types
- Proposed new communities for the registry
- Any recurring classification friction

### 11. Recommended Next Searches
- Search terms that worked well (keep for next month)
- Search terms that returned nothing (drop or refine)
- New search terms suggested by this month's findings

---

## Agent/Worker Roles by Loop

| Role | Loop | Input | Output | Status |
|------|------|-------|--------|--------|
| `source-monitor` | A (monitoring) | Source URL + dedupe index | Intel items + index update | Designed, 2 pilots |
| `search-discovery-worker` | B (search) | Search term list (incl. social-platform terms) | Candidate sources, orphan items, discovered local media orgs | Design only |
| `historical-backfill-worker` | C (backfill) | Month target + search terms | Monthly artifacts (items, clusters, gaps, wrap) | Design only |
| `resident-interest-classifier` | A, B, C | Intel item (partial) | Intel item (with RI fields) | Designed, agent exists |
| `beat-clustering-worker` | D (cross-section) | All items from a period | Beat registry + cross-section summaries | Design only |
| `taxonomy-steward` | E (taxonomy) | taxonomy_gap proposals | Taxonomy changes (after approval) | Design only (architect fills this) |
| `editorial-reviewer` | F (review) | Intel items in queue | Publish/reject/verify decisions | Design only |

Note: These are role definitions, not necessarily separate agents. One
agent (or human) may fill multiple roles. The roles exist so that when
Hermes tasks are defined, each has a clear owner and contract.

---

## Deep Research Extraction Status

The 2026-06-03 homeowner public-source report has been archived and extracted.
It now seeds the loops as follows:

### Loop B — Search Discovery
- Candidate sources from official, CDD, community/developer, media, public
  notice, and municipal stacks are in `registry/source_candidates.yaml`.
- Local-media discovery terms are active in `registry/search_terms.yaml`.
- New source promotions still require Buddy approval.

### Loop C — Historical Backfill
- May 2026 is the first backfill baseline.
- The plan is `docs/backfill/may_2026_backfill_plan.md`.
- Backfill execution has not run and requires explicit instruction.

### Loop D — Cross-Section / Beat Discovery
- Fourteen homeowner beats are in `registry/beat_candidates.yaml`.
- The first focus beats are rezoning/DRI, roadwork/traffic, schools,
  utilities/water, and permits/construction.

### Loop E — Taxonomy Improvement
- Source families and homeowner beat groups are documented in
  `docs/taxonomy.md`.
- Likely gaps such as `cdd_governance`, `permit_status`,
  `water_restrictions`, and `budget_millage` remain proposals until real
  extracted items justify canonical changes.

### Intake Artifacts
- `docs/deep_research/README.md` — raw-report storage
- `docs/deep_research_ingestion.md` — ingestion workflow
- `docs/deep_research/2026-06-03_source_extraction_review.md`
- `docs/deep_research/2026-06-03_beat_extraction_review.md`
- `docs/deep_research/2026-06-03_search_term_extraction_review.md`

---

## Current Status

| Loop | Designed | Piloted | Automated |
|------|----------|---------|-----------|
| A — Known-source monitoring | Yes | Yes (2 pilots) | No |
| B — Search discovery (incl. local-media sub-loop) | This doc | No (triggered by St. Johns Citizen discovery) | No |
| C — Historical backfill | This doc | No | No |
| D — Cross-section / beat | This doc | No | No |
| E — Taxonomy improvement | This doc | No | No |
| F — Review / editorial | Documented elsewhere | No | No |

The school district pilot remains valid as a Loop A exercise. Source-promotion
review and Hermes task planning are now equally important operator-mode tracks.
The May 2026 historical backfill is planned but should not run without explicit
instruction.
