# Hermes Task: May 2026 Historical Backfill

**Worker:** `historical-backfill-worker`  
**Task:** `historical-backfill-2026-05`  
**Status:** Template only — do not execute without explicit instruction from Buddy.

---

## 1. Purpose

Systematically search public web archives and official source records for
St. Johns County, Florida information during May 2026. Build the first
intelligence baseline month for SJC_Intel by extracting structured items,
clustering by topic, identifying source gaps, and producing an internal
monthly wrap.

This is an **exploratory** exercise, not definitive journalism. The output
is an internal intelligence baseline, not publishable content. It will miss
things, get emphases wrong, and may occasionally hallucinate. Every claim
must be traceable back to a source item.

### Learning goals (in priority order)

1. Test whether the backfill loop (Loop C) produces useful output.
2. Identify sources we should register that are not yet in the registry.
3. Identify taxonomy gaps where existing vocabularies don't fit.
4. Give the project a sense of what a monthly intelligence summary looks like.

---

## 2. Source Scope — First Pass (Official Sources Only)

Only check the following official/high-authority source stacks. Do **not** check
Tier 3 (CDD), Tier 4 (community/developer), or media sources (St. Johns Citizen,
JDR, Recorder, TV) in this first pass — they may be added in a second pass.

### Official stacks to check

| Stack | Source IDs to check | Topics likely | Suggested search approach |
|-------|-------------------|---------------|--------------------------|
| County news | `sjc_county_news` | county_government, public_notices, community_events | Web search restricted to `site:sjcfl.us` + date range |
| County Commission | `sjc_bcc_calendar` | county_government, development, taxes | Web search for BCC meetings, votes, hearings in May 2026 |
| Planning & Zoning | `sjc_pza_boards` | development, county_government, public_notices | Search for PZA, DRC, board of adjustment meetings |
| NBOR public notices / roads | `sjc_nbor_public_notices`, `sjc_transportation_infrastructure` | transportation, infrastructure, public_notices | Search for road closures, projects, traffic impacts, hearings |
| Utilities / water | `sjc_utility_department`, `sjrwmd_watering_restrictions` | infrastructure, environment, emergency_alerts | Search for boil notices, water restrictions, irrigation |
| Emergency management | `sjc_emergency_management` | public_safety, emergency_alerts | Search for EOC updates, hurricane prep, emergency notices |
| School district | `sjc_school_district`, `sjcsd_boarddocs`, `sjcsd_zoning_planning` | education, development, public_notices | Search for Board meetings, agenda items, zoning changes |
| FDOT / roads | `fdot_district_two_nflroads` | transportation, infrastructure | Search for FDOT projects in SJC |
| Budget / transparency | `sjc_budget_transparency` | taxes, county_government | Search for budget workshops, millage, TRIM (FY2027 context) |
| Sheriff (if relevant to May) | `sjso_news_stories` | public_safety, crime | Search for notable May 2026 incidents |
| NWS weather | `nws_jacksonville` | environment, emergency_alerts | Search for May 2026 weather events, drought status |
| Supervisor of Elections | `sjc_supervisor_of_elections` | elections | Search for May 2026 election-related activity |
| Permit activity | `sjc_permit_status` | development, construction | Search for notable permits, COs, plan reviews |
| Clerk records | `sjc_clerk_online_research` | county_government, public_notices, taxes | Search for deeds, liens, board records |
| Development tracker | `sjc_development_tracker` | development, construction, zoning | Search for mapped project updates |

### Context/tip-surfacing (limited use only)

| Source | Use as | Authority rule |
|--------|--------|----------------|
| St. Johns Citizen | Tip/context only | Do not use as sole authority for consequential claims |

Do **not** check Jacksonville Daily Record, Ponte Vedra Recorder, local TV,
Chamber calendar, CDD sites, or community/developer pages in this first pass.

---

## 3. Date Scope

| Field | Value |
|-------|-------|
| Start date | 2026-05-01 |
| End date | 2026-05-31 |
| Month key | `2026-05` |
| Output directory | `data/monthly/2026-05/` |

Filter all searches to this window. If a source page lists items without dates
and the date cannot be determined, mark `source_published_at: null` and flag in
backfill_report.md.

---

## 4. Search / Source-Check Instructions

### Approach

For each source in scope, use one or both of the following:

**A. Direct source check:** If the source has a searchable archive or listing
pages that can be filtered by date, fetch and parse those pages directly.
This is preferred for official government sites with dated listings.

**B. Public web search:** Use web search with `site:` or date-range operators
to find May 2026 content from official sources. Use search terms from
`registry/search_terms.yaml` (see §Search Terms Priority below).

### Search Terms Priority

From `registry/search_terms.yaml`, prioritize these categories and term IDs:

1. **Utilities/water:** `ST-0601` through `ST-0604`
   - Search for boil water notices, water restrictions, drought, irrigation
2. **Transportation/corridor:** `ST-0101` through `ST-0106`, `ST-0303`
   - Search for road closures, CR 210, SR 16, US 1 projects
3. **School:** `ST-0201` through `ST-0205`
   - Search for school board meetings, attendance zones, new schools
4. **Permits/development:** `ST-0301`, `ST-0302`
   - Search for permit activity, development projects
5. **Community terms** for SilverLeaf, Nocatee, RiverTown, Shearwater,
   TrailMark, Beachwalk, Beacon Lake
   - Use `ST-0001` through `ST-0011` patterns limited to May 2026
6. **County governance:** supplement with targeted queries for BCC,
   PZA, emergency management, budget

### Recording attempts

For every source you attempt to check, record:
- Whether it was found or not found
- Whether May 2026 items existed
- If not found: why (no archive, no date filter, paywall, etc.)

This goes in the `backfill_report.md` source-check log section.

---

## 5. Deduping Rules

Within the month, deduplicate items using this priority:

1. **Normalized URL** — match by URL (trailing-slash-insensitive, protocol-insensitive)
2. **source_id + title + date** — fallback when URL differs but content is the same
3. **Cross-source duplicates** — if the same fact appears in multiple sources
   (e.g., county news + St. Johns Citizen), keep one canonical item and list
   additional sources in a `supporting_sources` array

**Do not** update `data/index/prior_items.yaml` during this exploratory run
unless explicitly instructed. Backfill dedupe is within-month only.

IDs for deduped items use the format:
`SJC-BF-202605-{NNNN}` (sequential, zero-padded)

For items from canonical sources, also record the `source_id`.
For items from non-canonical sources (web discovery), use `source_id: "web_discovery"`.

---

## 6. Factual Extraction Rules

Every discovered item must include these fields (per intel_item schema v2.0):

| Field | Required | Notes |
|-------|----------|-------|
| `item_id` | Yes | `SJC-BF-202605-{NNNN}` |
| `title` | Yes | Headline from source, or concise summary |
| `summary` | Yes | 1-3 sentence factual summary |
| `source_id` | Yes | Canonical source_id, or `"web_discovery"` |
| `source_url` | Yes | Direct URL to original item |
| `source_published_at` | Yes (if available) | ISO 8601 date from source; null if unknown |
| `discovered_at` | Yes | Timestamp when you found the item |
| `topics` | Yes | 1+ from `docs/taxonomy.md` topic list |
| `communities` | Yes | From `registry/communities.yaml`; empty = countywide |
| `geographic_scope` | Yes | `county_wide`, `multi_community`, `single_community`, `neighborhood`, `address_specific` |
| `urgency` | Yes | `urgent`, `timely`, `ongoing`, `archival` |
| `verification_status` | Yes | `source_confirmed` for official sources; `unverified` for web/orphan items |
| `sensitivity` | Yes | `low`, `medium`, `high` |
| `recommended_channels` | No | Default: `["website_review_queue", "weekly_brief_candidate"]` |
| `raw_excerpt` | Yes | Verbatim first paragraph or key sentence from source |
| `review_status` | Yes | Always `"pending_review"` |
| `citation` | No | Structured attribution block |
| `created_at` | Yes | Timestamp of record creation |

### Classification defaults for official sources

| Field | Default | Override when |
|-------|---------|---------------|
| `topics` | `["general_government"]` | Content clearly maps to a specific topic |
| `communities` | `[]` (countywide) | Item names a specific community |
| `geographic_scope` | `county_wide` | Item references specific location |
| `urgency` | `ongoing` | Item has a deadline, date, or active impact |
| `verification_status` | `source_confirmed` | Source is official government site |
| `sensitivity` | `low` | Item involves safety, legal, crime, named individuals |
| `review_status` | `pending_review` | Always |

---

## 7. Resident-Interest Classification Rules

For each extracted item, add the resident-interest layer. Use rules from
`docs/resident_interest_classification.md` and
`prompts/resident_interest_classification_task.md`.

Required fields:

| Field | Required | Notes |
|-------|----------|-------|
| `primary_topic` | Yes | Single most relevant topic from taxonomy |
| `interest_tags` | Yes | From interest_tags vocabulary |
| `resident_relevance.summary` | Yes | 1-2 sentences why this matters to residents |
| `resident_relevance.affected_audiences` | Yes | Specific groups affected |
| `resident_relevance.why_it_matters` | Yes | Concrete impact on daily life |
| `resident_relevance.confidence` | Yes | `high`, `medium`, or `low` |
| `resident_relevance.inference_notes` | Yes | What was inferred vs. directly stated |
| `taxonomy_gap` | No | Proposed new tag if existing vocab doesn't fit |
| `human_review_required` | Yes | `true` for crime/safety/legal/minors/controversy |

### Mandatory human-review triggers

Set `human_review_required: true` for any item involving:
- Crime, arrest, suspect, or victim
- Minors
- Active emergency or safety incident
- Unresolved allegations or ongoing investigation
- Controversial public policy
- Named individuals (unless they are elected/appointed officials acting in
  official capacity)

---

## 8. Sensitivity / Privacy Rules

1. **Public sources only.** Do not access login-gated, private, or
   members-only content.
2. **No fake accounts or impersonation.** Do not create accounts or bypass
   access controls.
3. **Do not publish anything.** All output files are internal. The monthly
   wrap is not for distribution.
4. **Store minimal personal information.** Prefer parcel IDs, agenda item
   numbers, permit numbers, CDD names, and official document URLs over
   named individuals.
5. **Named individuals** are acceptable only when the original source names
   them publicly. Do not add names not in the source.
6. **Local media items** are context/tips only. Set `verification_status` to
   `unverified` unless the claim is a direct quote from an official record.
7. **Boil water notices, evacuation orders, active emergencies:** flag
   `urgency: urgent` and `sensitivity: high`, but do not alert — log for
   editorial review.
8. **Do not copy full article text.** `raw_excerpt` should be first paragraph
   or key sentence only — enough for context and verification.
9. **No speculation beyond reasonable resident-interest inference.**
   Label all inferences in `resident_relevance.inference_notes`.

---

## 9. Topic / Beat Clustering Rules

After all items are extracted, cluster them into `topic_clusters.yaml`.

### Cluster format

```yaml
cluster_id: "2026-05-cluster-001"
label: "CR 210 widening project"
item_ids:
  - "SJC-BF-202605-0001"
  - "SJC-BF-202605-0002"
count: 2
source_types: ["sjc_county_news", "sjc_nbor_public_notices"]
communities: ["cr_210_corridor", "silverleaf"]
beat_candidate: "CR 210 construction impacts"
severity: "high"  # recurring, high-impact
```

### Clustering rules

- Minimum cluster size: **2 items** (single items are "unclustered").
- Group by: shared topics, interest_tags, communities, or corridor.
- For each cluster, propose a `beat_candidate` label from the beat groups in
  `docs/taxonomy.md` (e.g., `utilities_water`, `school_capacity`,
  `transportation`, `cdd_governance`).
- Assign severity: `high` (recurring/high-impact), `medium` (notable),
  `low` (background).
- Clusters that span 3+ communities → note as potential county-wide summary.
- Items that don't fit any cluster → list as "unclustered" with reasons.

---

## 10. Source Gap Rules

After extraction and clustering, write `source_gaps.md` identifying:

- Topics or communities that had thin or no coverage
- Known sources not yet in the registry that would have covered May items
- Canonical sources that should have had items during May but didn't
  (possibly because they weren't monitored retroactively)
- New source recommendations for the candidate registry

### Gap format

```markdown
## Source Gap: SilverLeaf Community Page

**Evidence:** Multiple May 2026 search results reference
"SilverLeaf HOA updates" from a community website not in the registry.

**Recommendation:** Find and register the SilverLeaf community page
as a new source.

**Search terms used:** "SilverLeaf" "St. Johns County", "SilverLeaf"
HOA
```

---

## 11. Output Schema Expectations

Create the directory `data/monthly/2026-05/` and write five output files.

### Output 1: `data/monthly/2026-05/discovered_items.yaml`

```yaml
# May 2026 Discovered Items
# Generated: {ISO 8601}
# Worker: historical-backfill-2026-05
# Total items: {N}

items:
  - item_id: "SJC-BF-202605-0001"
    title: "..."
    summary: "..."
    source_id: "sjc_county_news"
    source_url: "https://..."
    source_published_at: "2026-05-..."
    discovered_at: "2026-06-03T..."
    topics: ["..."]
    communities: []
    geographic_scope: "county_wide"
    urgency: "ongoing"
    verification_status: "source_confirmed"
    sensitivity: "low"
    recommended_channels:
      - "website_review_queue"
      - "weekly_brief_candidate"
    raw_excerpt: "..."
    citation:
      source_name: "St. Johns County"
      source_type: "government_website"
      accessed_at: "2026-06-03T..."
      url: "https://..."
    review_status: "pending_review"
    primary_topic: "..."
    interest_tags: ["..."]
    resident_relevance:
      summary: "..."
      affected_audiences: ["..."]
      why_it_matters: "..."
      confidence: "high|medium|low"
      inference_notes: "..."
    taxonomy_gap: ~
    human_review_required: false
    created_at: "2026-06-03T..."
```

### Output 2: `data/monthly/2026-05/topic_clusters.yaml`

```yaml
clusters:
  - cluster_id: "2026-05-cluster-001"
    label: "Cluster label"
    item_ids: ["SJC-BF-202605-0001", "..."]
    count: 2
    source_types: ["source_id_1", "source_id_2"]
    communities: ["community_1", "community_2"]
    beat_candidate: "beat_name"
    severity: "high|medium|low"
unclustered:
  - item_id: "SJC-BF-202605-000N"
    reason: "No shared topic with >=2 items"
```

### Output 3: `data/monthly/2026-05/source_gaps.md`

Markdown document with source gap observations. See §10 for format.

### Output 4: `data/monthly/2026-05/monthly_wrap.md`

Narrative summary. See §Monthly Wrap Contents in `docs/discovery_loops.md`
for the full structure:
- Executive summary (3-5 bullets)
- Major themes (3-5 with source references)
- Community mentions
- Construction/development
- Traffic/roads
- Schools
- Public safety
- Events/community life
- Source gaps
- Taxonomy gaps
- Recommended next searches

### Output 5: `data/monthly/2026-05/backfill_report.md`

Operational report covering:
- Source-check log (which sources were checked, what was found)
- Search term effectiveness (which terms returned results, which returned nothing)
- Items extracted (total count, by source, by topic)
- Issues encountered (broken URLs, paywalls, ambiguous dates)
- Recommendations for next backfill pass (Aug-Sep 2025)

---

## 12. Completion / Block Protocol

### Completion criteria

The task is complete when:

- [ ] All official source stacks in §2 were attempted (results recorded even
      if no items found).
- [ ] `discovered_items.yaml` exists with all extracted items.
- [ ] `topic_clusters.yaml` exists with clusters (or a note explaining no
      clusters met minimum size).
- [ ] `source_gaps.md` exists with observations (or explicit "no gaps found").
- [ ] `monthly_wrap.md` exists with all required sections.
- [ ] `backfill_report.md` exists with source-check log and recommendations.
- [ ] All items have required schema fields.
- [ ] Sensitive items have `human_review_required: true`.
- [ ] No items use unsanctioned taxonomy values.
- [ ] No publishing, scheduling, or live monitor run occurred.

### Block conditions

Block the task (do not produce partial output) if:

| Condition | Action |
|-----------|--------|
| Cannot access any source (network/down) | Report specific failures; block if >50% of sources unreachable |
| Schema ambiguity that could produce invalid YAML | Request clarification from architect |
| Discovery of private/gated content referenced publicly | Flag for architect; do not extract |

### Partial completion

If a subset of sources produced items but some failed:
- Write complete output for what was found.
- Report failures in `backfill_report.md`.
- Complete with warnings, not errors.

---

## 13. Do Not Publish

**This is an internal intelligence baseline.** Do not:
- Publish the monthly wrap anywhere public.
- Distribute items outside the repo.
- Copy content to any publishing channel.
- Create newsletter drafts from this data.
- Share with anyone outside the project.

The output files exist for architect review and future editorial pipeline
testing only. A corrections workflow and editorial review queue must exist
before any content from this run can be considered publishable.

---

## 14. Public Sources Only

**All sources checked must be publicly accessible.**
- No private Facebook groups.
- No login-gated HOA or resident portals.
- No members-only forums.
- No private screenshots or forwarded messages.
- No content behind paywalls (note it, skip it).
- No scraping that would violate terms of service.

If a search result points to a private or gated source, record it as a
source gap but do not attempt to access it.

---

## 15. Exploratory, Not Definitive Journalism

This backfill is an **experiment**, not a news operation.

- The monthly wrap is an AI-generated intelligence summary based on public
  web search and official source pages. It will miss things, get some
  emphases wrong, and occasionally hallucinate.
- Every claim should be traceable back to a source item via `source_url`.
- Do not treat the wrap as authoritative.
- The primary value is:
  1. Testing the backfill loop's usefulness.
  2. Finding sources to register.
  3. Finding taxonomy gaps.
  4. Learning what a monthly summary looks like.

---

## Reference Paths (from repo root)

| Resource | Path |
|----------|------|
| Source registry | `registry/sources.yaml` |
| Candidate sources | `registry/source_candidates.yaml` |
| Search terms | `registry/search_terms.yaml` |
| Taxonomy | `docs/taxonomy.md` |
| RI classification | `docs/resident_interest_classification.md` |
| RI classification prompt | `prompts/resident_interest_classification_task.md` |
| Intel item schema | `schemas/intel_item.schema.yaml` |
| Discovery loops | `docs/discovery_loops.md` |
| Backfill plan | `docs/backfill/may_2026_backfill_plan.md` |
| Communities | `registry/communities.yaml` |
| Community IDs | `docs/taxonomy.md` (Communities section) |
| Beat candidates | `registry/beat_candidates.yaml` |

---

*End of Hermes task template. Do not execute without explicit instruction from Buddy.*
