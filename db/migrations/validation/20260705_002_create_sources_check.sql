-- Validation: 20260705_002_create_sources
-- Verify sources table exists with correct structure.

SELECT 'sources table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'sources') AS passed;

SELECT 'sources has primary key' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'app' AND table_name = 'sources' AND constraint_type = 'PRIMARY KEY') AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 2;
