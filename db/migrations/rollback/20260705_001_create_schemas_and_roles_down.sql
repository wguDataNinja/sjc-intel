-- Rollback: 20260705_001_create_schemas_and_roles
-- Drops migration tracking table and schemas (destructive).
-- Requires Destructive Operation Gate — contains data loss risk.

DROP TABLE IF EXISTS app.sjc_intel_migrations CASCADE;
DROP SCHEMA IF EXISTS health CASCADE;
DROP SCHEMA IF EXISTS app CASCADE;
