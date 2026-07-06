-- Validation: 20260705_003_create_source_events
-- Verify source_events table exists with FK to sources.

SELECT 'source_events table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'source_events') AS passed;

SELECT 'source_events has FK to sources' AS check_name,
       EXISTS (
           SELECT 1 FROM information_schema.table_constraints tc
           JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
           WHERE tc.table_schema = 'app' AND tc.table_name = 'source_events'
           AND tc.constraint_type = 'FOREIGN KEY' AND kcu.column_name = 'source_id'
       ) AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 3;
