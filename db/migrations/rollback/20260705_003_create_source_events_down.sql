-- Rollback: 20260705_003_create_source_events
-- Drops source_events table. Destructive — all event data lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.source_events CASCADE;
