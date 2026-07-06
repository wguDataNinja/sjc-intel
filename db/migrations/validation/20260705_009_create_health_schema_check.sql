-- Validation: 20260705_009_create_health_schema
-- Verify health schema and tables exist.

SELECT 'health schema exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'health') AS passed;

SELECT 'health_runs table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'health' AND table_name = 'health_runs') AS passed;

SELECT 'workflow_status table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'health' AND table_name = 'workflow_status') AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 9;
