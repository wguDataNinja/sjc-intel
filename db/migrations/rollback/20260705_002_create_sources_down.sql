-- Rollback: 20260705_002_create_sources
-- Drops sources table. Destructive — all source registry data lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.sources CASCADE;
