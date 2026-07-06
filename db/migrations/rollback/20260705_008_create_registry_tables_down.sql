-- Rollback: 20260705_008_create_registry_tables
-- Drops all registry/config tables. Destructive.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.interest_filters CASCADE;
DROP TABLE IF EXISTS app.source_candidates CASCADE;
DROP TABLE IF EXISTS app.beat_candidates CASCADE;
DROP TABLE IF EXISTS app.communities CASCADE;
DROP TABLE IF EXISTS app.search_terms CASCADE;
