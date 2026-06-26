# SJC_Intel Session — 2026-06-26 (Afternoon)

## Task
Apply the `source_event` model to NBOR public notice page fetches.

## Summary
Implemented the source_event parent-child pattern for the `sjc_nbor_public_notices` source. Each NBOR page fetch now produces a `source_event` record of type `public_notice_snapshot`, and all extracted intel_items link back to it via `source_event_id`.

## Changes Made

### Source Event Data
- Created `data/source_events/2026-06-26/sjc_nbor_public_notices.yaml` — NBOR source event `EVT-NBOR-20260626-0001` with 25 linked item_ids

### Intel Item Updates
- Added `source_event_id: EVT-NBOR-20260626-0001` to all 25 items in `data/intel_items/2026-06-26/sjc_nbor_public_notices.yaml`
- Added `source_event_id: EVT-NBOR-20260626-0001` to all 25 items in `data/intel_items/2026-06-08/sjc_nbor_public_notices.yaml`

### Script Update
- Updated `scripts/extract_nbor.py` to:
  - Use dynamic date-based output directories (instead of hardcoded `2026-06-08`)
  - Generate a `source_event` of type `public_notice_snapshot` per fetch
  - Add `source_event_id` to each intel_item
  - Write source_event to `data/source_events/{date}/sjc_nbor_public_notices.yaml`

### Rebuilt Artifacts
- Rebuilt `data/index/prior_items.yaml` — 77 entries, no source_events leaked
- Rebuilt `data/review_queue/queue.yaml` — 89 entries, review states preserved (25 NBOR items remain `verified`)
- Rebuilt `data/review_queue/summary.yaml`

### Documentation Updates
- Updated `docs/monitor_specs/sjc_nbor_public_notices.md` — added source event model section and updated output paths
- Updated `docs/cadence.md` — daily output now lists source_events before intel_items
- Updated `docs/monitoring_workflow.md` — added source_event creation step (1b), updated step descriptions

### BCC Impact
- BCC files untouched: `data/intel_items/2026-06-26/sjc_bcc_agenda_items.yaml` and `data/source_events/2026-06-26/sjc_bcc_calendar.yaml` unchanged

## Validation
- All YAML files parse correctly ✓
- Source event schema compliant (event_type: public_notice_snapshot, status: extracted) ✓
- All 50 NBOR items (across both files) linked to EVT-NBOR-20260626-0001 ✓
- Dedupe index: 0 source_events leaked, 77 entries ✓
- Review queue: 0 source_events leaked, 89 entries, review states preserved ✓
- Dedupe rebuild idempotent ✓
- BCC files intact and parseable ✓

## Next Steps
- MON-008: Run recurring daily NBOR monitor (extractor updated, Hermes-ready)
- MON-005: BCC calendar weekly monitor pilot
- SW-002: Source-watch first discovery cycle
