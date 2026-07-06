-- Rollback: 20260705_005_create_tracked_entities
-- Drops tracked_entities table. Destructive — all entity data lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.tracked_entities CASCADE;
