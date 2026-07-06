-- Validation: 20260705_004_create_intel_items
-- Verify intel_items table exists with all required constraints.

SELECT 'intel_items table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'intel_items') AS passed;

SELECT 'intel_items has FK to sources' AS check_name,
       EXISTS (
           SELECT 1 FROM information_schema.table_constraints tc
           JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
           WHERE tc.table_schema = 'app' AND tc.table_name = 'intel_items'
           AND tc.constraint_type = 'FOREIGN KEY' AND kcu.column_name = 'source_id'
       ) AS passed;

SELECT 'dedupe_key unique index exists' AS check_name,
       EXISTS (
           SELECT 1 FROM pg_indexes
           WHERE schemaname = 'app' AND tablename = 'intel_items'
           AND indexdef LIKE '%dedupe_key%' AND indexdef LIKE '%UNIQUE%'
       ) AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 4;
