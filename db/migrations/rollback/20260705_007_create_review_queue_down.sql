-- Rollback: 20260705_007_create_review_queue
-- Drops review queue and dedupe index tables. Destructive — review state lost.
-- Requires Destructive Operation Gate.

DROP TABLE IF EXISTS app.review_queue_entries CASCADE;
DROP TABLE IF EXISTS app.dedupe_index_entries CASCADE;
