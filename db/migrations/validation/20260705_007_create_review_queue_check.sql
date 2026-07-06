-- Validation: 20260705_007_create_review_queue
-- Verify review queue and dedupe index tables exist.

SELECT 'review_queue_entries table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'review_queue_entries') AS passed;

SELECT 'dedupe_index_entries table exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'dedupe_index_entries') AS passed;

SELECT 'review_queue_entries has FK to intel_items' AS check_name,
       EXISTS (
           SELECT 1 FROM information_schema.table_constraints tc
           JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
           WHERE tc.table_schema = 'app' AND tc.table_name = 'review_queue_entries'
           AND tc.constraint_type = 'FOREIGN KEY' AND kcu.column_name = 'item_id'
       ) AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 7;
