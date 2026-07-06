-- Rollback: 20260705_006_create_relationship_tables
-- Drops all relationship tables. Destructive.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.intel_item_tracked_entities CASCADE;
DROP TABLE IF EXISTS app.source_event_related_events CASCADE;
DROP TABLE IF EXISTS app.intel_item_topics CASCADE;
DROP TABLE IF EXISTS app.intel_item_communities CASCADE;
DROP TABLE IF EXISTS app.intel_item_interest_tags CASCADE;
DROP TABLE IF EXISTS app.source_event_items CASCADE;
