-- Validation: 20260705_006_create_relationship_tables
-- Verify all relationship tables exist.

SELECT 'intel_item_tracked_entities exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'intel_item_tracked_entities') AS passed;

SELECT 'source_event_related_events exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'source_event_related_events') AS passed;

SELECT 'intel_item_topics exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'intel_item_topics') AS passed;

SELECT 'intel_item_communities exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'intel_item_communities') AS passed;

SELECT 'intel_item_interest_tags exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'intel_item_interest_tags') AS passed;

SELECT 'source_event_items exists' AS check_name,
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'app' AND table_name = 'source_event_items') AS passed;

SELECT 'migration recorded' AS check_name,
       COUNT(*) = 1 AS passed
FROM app.sjc_intel_migrations
WHERE version = 6;
