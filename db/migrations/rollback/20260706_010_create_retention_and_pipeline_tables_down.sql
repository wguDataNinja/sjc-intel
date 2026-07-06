-- Rollback: 20260706_010_create_retention_and_pipeline_tables
-- Drops retention metadata, raw-artifact metadata, and pipeline-run history.
-- Destructive: requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.pipeline_runs CASCADE;
DROP TABLE IF EXISTS app.raw_artifact_records CASCADE;
DROP TABLE IF EXISTS app.source_retention_policies CASCADE;
DELETE FROM app.sjc_intel_migrations WHERE version = 10;
