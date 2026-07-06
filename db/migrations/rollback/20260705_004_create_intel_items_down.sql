-- Rollback: 20260705_004_create_intel_items
-- Drops intel_items table. Destructive — all intelligence item data lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.intel_items CASCADE;
