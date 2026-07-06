# Snapshots and Metrics

## Purpose

The UI should read compact current-state and historical aggregates instead of
requiring unlimited operational history. Snapshot generation is deterministic
and idempotent for the same date, grain, metric name, and dimensions.

## Implemented Table

Migration `20260706_011_create_metric_snapshots.sql` adds:

- `app.metric_snapshots`

Unique key:

- `snapshot_date`
- `grain`
- `metric_name`
- `dimensions_hash`

## Generator

Dry-run from file authority:

```bash
python3 scripts/metrics_snapshot.py --backend file --json
```

Dry-run from PostgreSQL:

```bash
SJC_INTEL_ADAPTER_BACKEND=pg \
SJC_INTEL_PG_ADAPTER_ENABLED=true \
python3 scripts/metrics_snapshot.py --backend pg --json
```

Writing snapshots to PostgreSQL is separately gated:

```bash
SJC_INTEL_SNAPSHOT_WRITE_ENABLED=true \
python3 scripts/metrics_snapshot.py --backend pg --write --json
```

## Current Metrics

- `intel_items_total`
- `intel_items_by_source`
- `intel_items_by_status`
- `intel_items_by_category`
- `sources_by_type`
- `sources_by_status`
- `tracked_entities_by_type`
- `review_queue_by_status`
- `source_latest_discovery`

All current generated metrics are marked `public_safe`; do not add private or
sensitive contents to public-facing metrics.

## Retention

Daily snapshots are expected to be compact. High-resolution snapshots may be
pruned later after weekly/monthly aggregates exist. No pruning is implemented or
authorized in this session.
