-- Validation: 20260705_001_create_schemas_and_roles
-- Verify schemas exist and migration tracking table was created.

SELECT 'app schema exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'app') AS passed;

SELECT 'health schema exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'health') AS passed;

SELECT 'migration tracking table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'sjc_intel_migrations') AS passed;

SELECT 'initial migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 1;
