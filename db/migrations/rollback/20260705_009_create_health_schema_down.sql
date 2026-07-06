-- Rollback: 20260705_009_create_health_schema
-- Drops health schema and tables. Destructive — health history lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS health.workflow_status CASCADE;
DROP TABLE IF EXISTS health.health_runs CASCADE;
DROP SCHEMA IF EXISTS health CASCADE;
