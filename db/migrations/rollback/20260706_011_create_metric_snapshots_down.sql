-- Rollback: 20260706_011_create_metric_snapshots
-- Drops compact metric snapshots.
-- Destructive: requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.metric_snapshots CASCADE;
DELETE FROM app.sjc_intel_migrations WHERE version = 11;
