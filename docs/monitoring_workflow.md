# SJC_Intel — Monitoring Workflow

> Hermes-compatible workflow for monitoring a public source, extracting
> candidate intel items, deduplicating, classifying, and creating review
> tasks.

## Overview

The monitoring workflow is the core operational loop of SJC_Intel. It runs
periodically (daily, weekly, or monthly depending on the source) and
produces structured intel items ready for verification and editorial review.

```
┌───────────────────────────────┐
│    1. FETCH SOURCE            │  HTTP GET source URL
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  2. EXTRACT CANDIDATES        │  Parse HTML, identify new items
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  3. DEDUPLICATE               │  Check against prior items
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  4. FACTUAL CLASSIFICATION    │  Tag topics, communities, urgency,
│                               │  verification_status, sensitivity,
│                               │  recommended_channels
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  5. RESIDENT-INTEREST CLASS   │  Add primary_topic, interest_tags,
│                               │  resident_relevance, taxonomy_gap,
│                               │  human_review_required
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  6. STRUCTURE ITEM            │  Build full intel_item record
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  7. VERIFICATION / SENSITIV   │  Apply sensitivity defaults,
│     REVIEW                    │  set review_status, flag human
│                               │  review if required
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  8. CREATE REVIEW TASK        │  Queue for human review if needed
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│  9. WRITE OUTPUT              │  Write artifact + update dedupe index
└────────────┬──────────────────┘
             ▼
┌───────────────────────────────┐
│ 10. COMPLETE / BLOCK          │  kanban_complete or report error
└───────────────────────────────┘
```

## Workflow Task Definition

Below is the Hermes-compatible workflow definition. Each step maps to a
discrete Hermes task or tool call.

```yaml
name: "monitor_source"
description: >
  Monitor a single public source, detect new items, extract structured
  intelligence, and create a review task.

trigger:
  type: cron
  # Frequency is set per source; worker determines schedule from
  # the source record's monitor_frequency field.

inputs:
  source_id:
    type: string
    description: "source_id from registry/sources.yaml"
    required: true

steps:
  - step_id: 1
    name: "fetch_source"
    description: "HTTP GET the source URL and capture raw HTML"
    tool: "webfetch"
    inputs:
      url: "{{ source.url }}"
    outputs:
      raw_html: "string"
      http_status: "integer"
      fetched_at: "ISO 8601 timestamp"
    error_handling:
      - if: "http_status != 200"
        action: "block with error"
        message: "Source returned HTTP {status}"

  - step_id: 2
    name: "extract_candidates"
    description: "Parse HTML and identify new candidate items"
    tool: "hermes_task"  # or a custom extraction agent
    inputs:
      raw_html: "{{ fetch_source.raw_html }}"
      source_type: "{{ source.source_type }}"
    outputs:
      candidates:
        type: "array"
        description: "List of extracted candidate items (title, url, date, excerpt)"
    error_handling:
      - if: "candidates is empty"
        action: "warn and continue"
        message: "No items found on source page"

  - step_id: 3
    name: "deduplicate"
    description: >
      Cross-check candidate items against previously discovered items
      (stored in a prior_items index) to avoid duplicates.
    tool: "hermes_task"
    inputs:
      candidates: "{{ extract_candidates.candidates }}"
      prior_items: "{{ read_prior_items() }}"
    outputs:
      new_items:
        type: "array"
        description: "Candidates that have NOT been seen before"
    error_handling:
      - if: "new_items is empty"
        action: "complete"
        message: "No new items found — monitor is up to date"

  - step_id: 4
    name: "classify_items"
    description: >
      For each new item, assign topics, communities, geographic_scope,
      urgency, verification_status, sensitivity, and recommended_channels.
      All classification values must be drawn from the controlled
      vocabularies in docs/taxonomy.md. Community values must match
      entries in registry/communities.yaml.
    tool: "hermes_task"  # or a classification agent
    inputs:
      new_items: "{{ deduplicate.new_items }}"
      source: "{{ source }}"
    outputs:
      classified_items:
        type: "array"
        description: "New items with factual classification fields populated"

  - step_id: 5
    name: "resident_interest_classify"
    description: >
      For each classified item, add the resident-interest layer:
      primary_topic, interest_tags, resident_relevance block,
      taxonomy_gap, and human_review_required. Uses the
      resident-interest-classifier agent. Must stay evidence-bound;
      separates source facts from inference via confidence levels.
    tool: "hermes_task"
    agent: "resident-interest-classifier"
    inputs:
      classified_items: "{{ classify_items.classified_items }}"
    outputs:
      enriched_items:
        type: "array"
        description: "Items with resident-interest fields added"

  - step_id: 6
    name: "structure_items"
    description: >
      Build full intel_item records following the intel_item.schema.yaml
      structure (v2.0+), including all resident-interest fields.
    tool: "hermes_task"
    inputs:
      enriched_items: "{{ resident_interest_classify.enriched_items }}"
      source: "{{ source }}"
    outputs:
      intel_items:
        type: "array"
        description: "Complete intel_item records"

  - step_id: 7
    name: "apply_sensitivity_review"
    description: >
      Apply sensitivity defaults and review rules:
      - Items with human_review_required=true stay in review queue.
      - Items with sensitivity=high get priority flagging.
      - Apply public-safety defaults to recommended_channels.
      - Set review_status to pending_review.
    tool: "hermes_task"
    inputs:
      intel_items: "{{ structure_items.intel_items }}"
    outputs:
      reviewed_items:
        type: "array"
        description: "Items with sensitivity/review rules applied"

  - step_id: 8
    name: "create_review_tasks"
    description: >
      For each item, create an editorial review task in the Hermes kanban.
      Items with sensitivity=high go directly to human review; others may
      auto-advance or batch-review.
    tool: "kanban_create"
    inputs:
      items: "{{ structure_items.intel_items }}"
      priority: "{{ derive_priority(item) }}"
    outputs:
      task_ids:
        type: "array"
        description: "Kanban task IDs for review queue"

  - step_id: 9
    name: "write_output"
    description: >
      Write the new intel items as a single YAML artifact file in the
      repo under data/intel_items/{YYYY-MM-DD}/{source_id}.yaml.
      Also update the dedupe index at data/index/prior_items.yaml.
    tool: "file_write"
    inputs:
      items: "{{ reviewed_items.intel_items }}"
      path_pattern: "data/intel_items/{date}/{source_id}.yaml"
      index_update: "data/index/prior_items.yaml"
    outputs:
      output_file: "string"
      dedupe_entries: "integer"

  - step_id: 10
    name: "complete_monitor_cycle"
    description: >
      Mark the monitor cycle as complete in the kanban board.
    tool: "kanban_complete"
    inputs:
      task_id: "{{ task.task_id }}"
      summary: "Monitored {source_id}: {n} new items, {n} review tasks created"
    outputs:
      completed: "boolean"

output:
  summary: >
    Monitor cycle summary: source {source_id} checked, {n} new items
    extracted, {n} review tasks queued.
```

## Classification Defaults

All classification fields must use values from the controlled vocabularies
in `docs/taxonomy.md`. Communities must be drawn from `registry/communities.yaml`.

When classifying a new item from an official government source, use these
defaults unless the content clearly requires otherwise:

| Field | Default Value | Override When |
|-------|--------------|---------------|
| `topics` | `["general_government"]` | Source content suggests a specific topic |
| `communities` | `[]` (countywide) | Specific community is named in the item |
| `geographic_scope` | `county_wide` | Item references a specific location |
| `urgency` | `ongoing` | Item has a deadline, date, or active impact |
| `verification_status` | `source_confirmed` | Source is an official government site |
| `sensitivity` | `low` | Item involves safety, legal, crime, or named individuals |
| `recommended_channels` | `["website_review_queue", "weekly_brief_candidate"]` | Urgent items should add `alert` |
| `review_status` | `pending_review` | Always — new items start in review queue |

## Per-Source Configuration

Each source in `registry/sources.yaml` may include a `monitor_config` block
that customizes how this workflow runs:

| Config Field | Description | Example |
|-------------|-------------|---------|
| `check_url` | URL to fetch (may differ from source url) | `https://www.sjso.org/news-stories/` |
| `check_interval_hours` | Hours between cycles | `24` |
| `extract_selector` | CSS selector for item extraction | `article.post` |
| `item_url_pattern` | Pattern for individual item URLs | `https://www.sjso.org/news-stories/{slug}/` |

## Recommended First Monitors

Based on the feasibility test (2026-06-03), the first three sources to
implement monitoring for are:

### 1. `sjc_county_news`
- **URL:** https://www.sjcfl.us/news/
- **Why first:** Highest signal-to-noise ratio for county government intelligence. WordPress blog with simple HTML structure. Easy parsing.
- **Schedule:** Daily
- **Automation:** YES — plain HTTP GET, no JS required.

### 2. `sjso_news_stories`
- **URL:** https://www.sjso.org/news-stories/
- **Why second:** Primary public safety intelligence source. Same WordPress pattern as sjc_county_news — reuses the same extraction logic.
- **Schedule:** Daily
- **Automation:** YES — identical pattern.

### 3. `sjc_school_district`
- **URL:** https://www.stjohns.k12.fl.us/
- **Why third:** Education is a core community concern. Board agendas and district news are high-value. Combined with BoardDocs as a secondary target.
- **Schedule:** Weekly (board cycle) + daily during school year
- **Automation:** YES — WordPress portal + BoardDocs integration.

## Pilot Lessons (sjc_county_news, 2026-06-03)

The first monitor pilot revealed the following operational insights:

### Sidebar Discovery Strategy
The main listing page for WordPress blog sources may only show a subset
of "Featured" items (e.g., 4 on sjcfl.us/news/). Additional recent items
appear in the "Latest News" sidebar on individual article pages.

**Recommended approach:**
1. Fetch the source listing page — extract visible featured items.
2. For each featured item, fetch the individual article page.
3. On each article page, extract the "Latest News" sidebar as a secondary
   source of recent items.
4. Deduplicate the combined set against the prior_items index.

### Known Source Characteristics
| Characteristic | Notes |
|---------------|-------|
| Featured items only | Main listing may show 4-6 items; full list via AJAX |
| Sidebar helpful | Article pages list 5 recent items in sidebar |
| Dates lack year on listing | Full dates with year on individual article pages |
| No structured timestamps | Source provides dates only, not times |

## Error Handling

| Scenario | Action |
|----------|--------|
| HTTP error (non-200) | Block with error, notify operator |
| Empty response / no items found | Warn, complete with zero items |
| Parsing failure | Retry once, then block with error |
| Dedupe failure (index unavailable) | Treat all candidates as new |
| Classification timeout | Proceed with default classifications |
| Kanban create failure | Write items to disk, retry on next cycle |
| Partial success (some items fail) | Report per-item status, complete partial |

## Future Enhancements

- **Incremental deduplication** — Store seen item fingerprints in a local
  SQLite database for efficient cross-cycle deduplication.
- **Alerting** — Auto-flag items with `urgency: urgent` for immediate human
  attention via notification channel.
- **Multi-source batch runs** — Group multiple daily sources into a single
  workflow run for efficiency.
- **Source health reporting** — Generate weekly reports on source status
  (uptime, item counts, error rates).
