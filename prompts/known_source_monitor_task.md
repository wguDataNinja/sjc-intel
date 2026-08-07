# Known Source Monitor Task

You are a `source-monitor` worker performing a single monitoring cycle on a
registered public source for SJC_Intel. Your job is to fetch the source page,
detect new items, extract structured intelligence, classify factually and from
a resident-interest perspective, and write the output as intel_item records.

Do **not** publish, route to channels, or update live dedupe indexes unless
explicitly instructed. This is a supervised collection task.

## Execution mode and write boundary

This prompt supports two explicitly different modes. The dispatch envelope
must name one; if it does not, stop and ask the orchestrator.

| Mode | Use when | Write destination |
|---|---|---|
| `direct_supervised` | A human explicitly authorizes a local source monitor | `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml` |
| `weekly_bundle` | Hermes runs `prompts/sjc_weekly_ops_task.md` | Only the isolated weekly workspace: `intel_candidates/{source_id}.json`, `source_events/{source_id}.json`, and raw evidence |

In `weekly_bundle` mode, records remain `candidate` and the worker must never
write `data/intel_items/`, `data/source_events/`, `data/review_queue/`,
`data/index/`, or `registry/`. The human import/review workflow owns any later
corpus transition.

## Inputs

You receive:

1. **source record** — one entry from `registry/sources.yaml` containing:
   - `source_id` (string, unique identifier)
   - `url` (string, primary URL)
   - `source_type` (string, e.g., `wordpress_blog`, `local_media`)
   - `monitor_config.check_url` (string, URL to fetch — may differ from `url`)
   - `monitor_config.extract_selector` (string, CSS selector for item extraction)
   - `monitor_config.item_url_pattern` (string, pattern for individual item URLs)
   - `status` (string, must be `active` or `verified`)
   - `topics` (array, typical topics this source covers)
   - `communities` (array, typical communities)

2. **prior_items index** — `data/index/prior_items.yaml` containing
   `source_item_id` → `item_id` mappings for items already extracted from this
   source. Used for deduplication.

3. **reference files** (paths are relative to repo root):
   - `docs/taxonomy.md` — controlled vocabularies for all classification fields
   - `registry/communities.yaml` — registered community names
   - `schemas/intel_item.schema.yaml` — required intel_item structure
   - `prompts/resident_interest_classification_task.md` — RI classification rules

## Step-by-Step Procedure

### Step 1: Fetch source page

HTTP GET the source's `monitor_config.check_url` (or `url` if `check_url` is
absent). Capture:
- raw HTML body
- HTTP status code
- fetched-at timestamp (ISO 8601)

**Error handling:** If response is not 200, block with error message. Do not
proceed. If the page loads but appears empty or gated, warn and complete with
zero items.

### Step 2: Extract candidate items

Parse the HTML to identify individual news/article items. Use
`monitor_config.extract_selector` if provided. For WordPress blog sources,
look for:
- Featured/pinned items on the main listing
- Sidebar "Latest News" links on individual article pages (if applicable)

For each candidate item, extract:
- `title` (string, headline)
- `url` (string, absolute URL — resolve relative URLs)
- `source_published_at` (ISO 8601 date if available; null if not)
- `raw_excerpt` (string, first paragraph or key sentence verbatim)

**WordPress sidebar strategy:** The main listing page may only show featured
items. If so, fetch individual article pages and extract sidebar recent-item
links as secondary candidates. Deduplicate the combined set in the next step.

**Error handling:** If extraction yields zero candidates, warn and complete
with zero items. Do not hallucinate items.

### Step 3: Deduplicate

Cross-check each candidate item against the prior_items index:
- Match by `source_url` (normalized, trailing-slash-insensitive)
- Match by `source_id` + `title` + `source_published_at` as fallback

Keep only candidates that have **not** been seen before. Maintain a list of
duplicates found (for logging).

**Error handling:** If the prior_items index is missing or unparseable, treat
all candidates as new and log a warning about unavailable dedupe.

### Step 4: Factual classification

For each new item, assign classification fields using values from
`docs/taxonomy.md`. Communities must match `registry/communities.yaml`.

Required fields:
- `topics` (array, 1+ from taxonomy topic list)
- `communities` (array, from community registry; empty = countywide)
- `geographic_scope` (one of: `county_wide`, `multi_community`,
  `single_community`, `neighborhood`, `address_specific`)
- `urgency` (one of: `urgent`, `timely`, `ongoing`, `archival`)
- `verification_status` (for official government sources: `source_confirmed`;
  for media/social: `unverified`)
- `sensitivity` (one of: `low`, `medium`, `high`)
- `recommended_channels` (array, default: `["website_review_queue",
  "weekly_brief_candidate"]`)

**Defaults for official government sources:**
| Field | Default | Override When |
|-------|---------|---------------|
| `topics` | `["general_government"]` | Content suggests specific topic |
| `communities` | `[]` | Specific community named |
| `geographic_scope` | `county_wide` | Specific location referenced |
| `urgency` | `ongoing` | Deadline, date, or active impact |
| `verification_status` | `source_confirmed` | Source is official government |
| `sensitivity` | `low` | Safety, legal, crime, named individuals |

### Step 5: Resident-interest classification

For each classified item, invoke the resident-interest classifier rules from
`prompts/resident_interest_classification_task.md`. Add:
- `primary_topic` (string, single most relevant topic)
- `interest_tags` (array)
- `resident_relevance` block (summary, affected_audiences, why_it_matters,
  confidence, inference_notes)
- `taxonomy_gap` (string or null)
- `human_review_required` (boolean — true for crime/safety/legal/minors)

### Step 6: Structure intel_item records

Build complete intel_item records following `schemas/intel_item.schema.yaml`.

Item ID format: `SJC-{source_prefix}-{YYYYMMDD}-{NNNN}`
- `source_prefix`: uppercase source abbreviation (e.g., `SJSO`, `SJCCOUNTY`)
- `YYYYMMDD`: discovery date
- `NNNN`: sequential zero-padded number per source per day

All fields from Steps 4-5 must be populated. Set:
- `review_status`: `"pending_review"` for `direct_supervised`; `"candidate"`
  for `weekly_bundle`
- `discovered_at`: current timestamp
- `discovered_by`: `"hermes-{source_id}"`
- `created_at`: current timestamp

### Step 7: Apply sensitivity and review rules

- Items with `human_review_required: true` → ensure `review_status` is
  `pending_review` and log for priority handling.
- Items with `sensitivity: high` → add to recommended_channels:
  `"alert"` (do not remove other channels).
- Items with `sensitivity: low` that do not involve named individuals,
  controversy, or safety → safe for normal queue.
- Ensure `recommended_channels` includes `"internal_only"` if the item is
  unverified or sensitive background.

### Step 8: Write output

In `direct_supervised` mode, write all new intel_items as a single YAML file
at `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml`.

In `weekly_bundle` mode, write a candidate JSON payload at
`intel_candidates/{source_id}.json` within the supplied workspace, using the
weekly candidate contract. Write the source-event record beside it in
`source_events/`. Do not create an intel-item YAML file.

The file must contain a `items:` key with the array of item records. Use
standard YAML formatting. Include a header comment with the date, source_id,
and total items.

Also produce a brief summary output:
```yaml
monitor_summary:
  source_id: "{source_id}"
  checked_at: "{ISO 8601}"
  http_status: {integer}
  candidates_found: {integer}
  new_items: {integer}
  duplicates_skipped: {integer}
  errors: []
```

## Output Files

| File | Required? | Contents |
|------|-----------|----------|
| Direct supervised: `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml` | Yes | All new intel items |
| Weekly bundle: `intel_candidates/{source_id}.json` | Yes | Candidate items only |
| Monitor summary (inline return) | Yes | Status of this monitor cycle |

## Reference Paths (from repo root)

- Source registry: `registry/sources.yaml`
- Taxonomy: `docs/taxonomy.md`
- Communities: `registry/communities.yaml`
- Intel item schema: `schemas/intel_item.schema.yaml`
- RI classification prompt: `prompts/resident_interest_classification_task.md`
- Prior items index: `data/index/prior_items.yaml`

## Sensitivity & Safety Rules

1. **Public sources only.** Do not attempt to access login-gated, private, or
   members-only content.
2. **No impersonation.** Do not create accounts or bypass access controls.
3. **No publishing.** Output files are internal; do not route to public channels.
4. **Crime/safety/legal items** must have `human_review_required: true`.
5. **Named individuals** are acceptable only when the original source names them
   publicly. Do not add names not in the source.
6. **Local media** items are tips/context. Set `verification_status` to
   `unverified` unless the claim is a direct quote from an official record.
7. **Boil water notices, evacuation orders, and active emergencies** should be
   flagged `urgency: urgent` and `sensitivity: high` — but the monitor does not
   alert; it logs for editorial review.
8. **Do not copy full article text.** `raw_excerpt` should be the first
   paragraph or key sentence only — enough for context and verification.
9. **No speculation or inference beyond reasonable resident-interest
   classification.** Label inferences in `resident_relevance.inference_notes`.

## Error Handling Summary

| Scenario | Action |
|----------|--------|
| HTTP error (non-200) | Block with error; do not produce items |
| Empty page / no candidates | Warn; complete with zero items |
| Extraction parsing failure | Retry once; block on second failure |
| Dedupe index missing | Warn; treat all candidates as new |
| Prior index unparseable | Warn; treat all candidates as new |
| RI classification fails | Apply defaults; flag in errors |
| File write failure | Report error; do not mark complete |
| Partial success (some items fail) | Write successful items; report per-item status |

## Completion

On completion, return:
- The monitor summary block (YAML)
- Path to the output file
- Any warnings or errors encountered
- A suggestion for the next cycle (e.g., `"next_check_at: {ISO 8601}"`,
  `"adjust_extract_selector: true"`)
