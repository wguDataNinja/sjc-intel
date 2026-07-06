-- Validation: 20260705_008_create_registry_tables
-- Verify all registry/config tables exist.

SELECT 'interest_filters exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'interest_filters') AS passed;

SELECT 'source_candidates exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'source_candidates') AS passed;

SELECT 'beat_candidates exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'beat_candidates') AS passed;

SELECT 'communities exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'communities') AS passed;

SELECT 'search_terms exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'search_terms') AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 8;
