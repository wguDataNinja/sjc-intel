-- Validation: 20260705_005_create_tracked_entities
-- Verify tracked_entities table exists.

SELECT 'tracked_entities table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'tracked_entities') AS passed;

SELECT 'tracked_entities has primary key' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'app' AND table_name = 'tracked_entities' AND constraint_type = 'PRIMARY KEY') AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 5;
