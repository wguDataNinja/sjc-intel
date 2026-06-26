# ED-001: Editorial Review Queue Requirements

## Context

SJC_Intel now produces structured intel_items from multiple daily and weekly
sources. Before any publishing, a review queue must exist to gate content.

Current sources producing items:
- Daily: sjc_nbor_public_notices, sjc_utility_department, sjc_county_news,
  sjso_news_stories, sjc_emergency_management (seasonal)
- Weekly: sjc_bcc_calendar (meeting metadata + agenda items)
- Backfill: May 2026 (21 items, archival)

## Canonical Review Statuses (Final, 2026-06-26)

| State | Definition | Action |
|-------|------------|--------|
| `pending_review` | New item, not yet reviewed | Default for all new items |
| `in_review` | Being reviewed by an editor | Editor claims the item |
| `verified` | Factually correct, classification confirmed | Review completed |
| `needs_followup` | Requires additional information or verification | Flag for follow-up |
| `rejected_noise` | Not resident-impactful; correctly classified as noise | Record reason |
| `duplicate` | Duplicate of another item (not caught by dedupe) | Link to canonical item |
| `escalated` | Flagged for priority human/architect review | Priority handling |
| `archived` | Historical reference, no action needed | Store for reference |

Note: `published` status is reserved for a future publishing phase and is not
currently active. The review queue is internal-only.

## Required Fields for Review Queue

Each review queue entry must include:

| Field | Source | Notes |
|-------|--------|-------|
| `item_id` | intel_item | Primary key |
| `title` | intel_item | Display title |
| `source_id` | intel_item | Origin source |
| `source_url` | intel_item | Evidence URL |
| `topics` | intel_item | Classification |
| `interest_tags` | intel_item | Resident-interest dimensions |
| `signal` | Classification | `high`/`medium`/`low`/`routine` |
| `beat` | Classification | Resident-interest beat |
| `urgency` | intel_item | Time sensitivity |
| `sensitivity` | intel_item | Low/medium/high |
| `human_review_required` | intel_item | Boolean flag |
| `meeting_date` | BCC items only | Meeting date for agenda items |
| `agenda_item_number` | BCC items only | Item number in agenda |
| `supporting_sources` | Cross-source | Related NBOR/BCC/etc. item IDs |

## Source-Event vs Intel-Item Distinction (Implemented 2026-06-26)

| Concept | Definition | Examples |
|---------|------------|----------|
| **Intel item** | A discrete piece of actionable information | "REZ 2025-11 Nothing Putt Fun rezoning hearing", "Phase III water shortage" |
| **Source event** | A container that produced items | "BCC meeting on Jan 20, 2026", "NBOR page fetch on June 26" |

Source events are stored in `data/source_events/` using the schema defined
in `schemas/source_event.schema.yaml`. Intel items link back to their parent
source event via `source_event_id`.

**Source events are excluded from the review queue.** Only true intel_items
in `data/intel_items/` enter `data/review_queue/queue.yaml`. This is enforced
by `scripts/build_review_queue.py`, which scans only `data/intel_items/` and
skips deprecated/event-only files.

## Duplicate/Cluster Handling

| Cluster Type | Detection | Action |
|-------------|-----------|--------|
| **Exact duplicate** | Same `_dedupe_key` | Skip / dedupe index blocks |
| **Cross-source same event** | NBOR hearing notice + BCC agenda item | Link as `supporting_sources`; keep one canonical item |
| **Same project, different milestone** | SR 207 WRF: approval vs completion | Keep separate items, link via `superseded_by` or `supporting_sources` |
| **Likely cluster** | Same title/beat within 7 days | Flag for editorial review |

Current dedupe index (`data/index/prior_items.yaml`) handles exact duplicates.
Cross-source clustering is manual.

## Human-Review Triggers

Set `human_review_required: true` when:

- Crime, arrest, suspect, victim, named individuals in public safety context
- Active emergencies (boil water, evacuation, hazmat)
- Legal matters, litigation, personnel actions
- Unresolved allegations or ongoing investigations
- Controversial public policy (contentious hearings, split votes)
- Content that could cause panic if misinterpreted
- Items where source authority is unclear

Currently implemented in monitor specs. Review queue should filter on this
field.

## Escalation Levels

| Level | Definition | SLA |
|-------|------------|-----|
| `routine` | Low sensitivity, no human review needed | Batch review weekly |
| `standard` | Medium sensitivity | Review within 48 hours |
| `priority` | High sensitivity or urgency | Review within 4 hours |
| `immediate` | Active emergency, public safety | Immediate notification |

These are requirements for the queue design, not yet implemented.

## Rejection/Noise Handling

Items may be rejected when:
- Classification is wrong (e.g., routine item tagged as high-impact)
- Source authority is insufficient (media claim without official confirmation)
- Duplicate of existing item (not caught by dedupe)
- Content is purely ceremonial with no resident impact
- Item is a false positive from keyword matching

Rejected items should record:
- `item_id`
- Rejection reason
- Reviewer notes
- Whether the rejection implies a classifier fix

## Evidence Preservation

Every review queue entry must preserve:
- `source_url` — direct link to original
- `raw_excerpt` — verbatim source text
- `citation` block — source name, type, access date
- PDF URL (for BCC items) — link to agenda PDF page
- Clerk source page URL (for BCC)

These are all already in the intel_item schema. No changes needed.

## Cross-Source Linking

NBOR and BCC records should be linked when they reference the same project:
- NBOR: public hearing notice (pre-meeting)
- BCC: agenda item (meeting), minutes decision (post-meeting)

Current linking is manual via `supporting_sources` array. Future automation
could match by application ID (e.g., `REZ 2025-11`, `MAJMOD 2025000011`).

## Suggested File/Schema Location

| Artifact | Location | Status |
|----------|----------|--------|
| Review queue schema | `schemas/review_queue.schema.yaml` | Needs creation |
| Review queue data | `data/review_queue/` | Needs creation |
| Review queue item | `data/review_queue/{status}/{item_id}.yaml` | Per-item file |
| Or: flat queue | `data/review_queue/queue.yaml` | Single file |

Recommendation: Start with a single flat YAML file (`queue.yaml`) listing all
items with `pending_review` status. Move to per-status directories when volume
exceeds 100 items.

## Implementation Status

| Phase | Description | Status | Artifacts |
|-------|-------------|--------|-----------|
| 0 | Items have `review_status: pending_review` | ✅ Complete | All intel_item YAML files |
| 1 | Flat review queue (`data/review_queue/queue.yaml`) | ✅ Complete | `scripts/build_review_queue.py`, `data/review_queue/queue.yaml`, `data/review_queue/summary.yaml` |
| 2 | Review-action status updates | ✅ Complete | `scripts/update_review_status.py` — updates queue + source intel_item file |
| 3 | Filtering and batch operations | ⬜ Not started | Future |
| 4 | Cross-source cluster detection | ⬜ Not started | Future |

## Current Queue State (2026-06-26, post-calibration)

- **99 items** in queue, **83 pending_review**, **14 verified**, **1 archived**, **1 rejected_noise**
- **2 immediate** (Phase III water shortage — both verified)
- **63 high** (rezoning, utilities, transportation, crime reports)
- **7 normal** (medium-signal items)
- **27 low** (routine, archival, low-signal)
- **5 items** flagged `human_review_required` (all 5 reviewed and verified)
- **54 BCC items**, **25 NBOR items**, **20 other sources**
- Calibration report: `data/review_queue/calibration_report.md`

## Scripts

### Build the queue
```bash
python3 scripts/build_review_queue.py
```
Scans all `data/intel_items/*.yaml`, dedupes by item_id, computes escalation
levels, writes `data/review_queue/queue.yaml` and `data/review_queue/summary.yaml`.
Idempotent — safe to run after each daily/weekly cycle.

### Update review status
```bash
python3 scripts/update_review_status.py <item_id> <new_status> [--note "reason"]
```
Updates status in both the queue YAML and the source intel_item YAML.
Supported statuses: `pending_review`, `in_review`, `approved`,
`changes_requested`, `rejected`, `published`.

## Operator Workflow

After each daily or weekly monitor cycle:
1. Run `python3 scripts/build_review_queue.py` to refresh the queue.
2. Review items by escalation level: `immediate` → `high` → `normal` → `low`.
3. Update status with `scripts/update_review_status.py`.
4. The queue is internal-only — no publishing, no public output.

## Escalation Logic (calibrated 2026-06-26)

| Level | Triggers | SLA |
|-------|----------|-----|
| `immediate` | `urgency: urgent` OR active emergency keywords (boil water, evacuation, hazmat) | As soon as possible |
| `high` | Rezoning, utilities, transportation, budget, crime/human-review-required, `urgency: timely`, `_signal: high_signal` | Within 48 hours |
| `normal` | Medium-signal, `_signal: medium_signal` | Batch weekly |
| `low` | Archival, routine, ceremonial, low-signal | Before publishing |

Note: `human_review_required` maps to `high`, not `immediate`. Crime reports
and press releases need human review but are not emergencies. Only active
emergencies with `urgency: urgent` map to `immediate`.
