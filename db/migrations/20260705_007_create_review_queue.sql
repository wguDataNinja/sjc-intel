SET ROLE sjc_intel_owner;

-- Migration: 20260705_007_create_review_queue
-- Review queue and dedupe index tables.
-- Forward-only. Idempotent via IF NOT EXISTS.

-- Review queue entries (table, not view — stores human review state)
CREATE TABLE IF NOT EXISTS app.review_queue_entries (
    queue_id              text PRIMARY KEY,
    item_id               text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    dedupe_key            text,
    source_id             text NOT NULL REFERENCES app.sources(source_id),
    source_file           text,
    title                 text NOT NULL,
    summary               text,
    beat                  text,
    topics                text[],
    signal                text CHECK (signal IN ('high', 'medium', 'low_signal')),
    urgency               text CHECK (urgency IN ('urgent', 'timely', 'ongoing', 'archival')),
    escalation            text CHECK (escalation IN ('immediate', 'high', 'normal', 'low')),
    sensitivity           text CHECK (sensitivity IN ('low', 'medium', 'high')),
    interest_tags         text[],
    matched_filters       text[],
    tracked_entity_ids    text[],
    matched_entities      text[],
    entity_match_basis    jsonb,
    review_status         text NOT NULL DEFAULT 'pending_review' CHECK (review_status IN ('pending_review', 'in_review', 'approved', 'changes_requested', 'rejected', 'published')),
    human_review_required boolean NOT NULL DEFAULT false,
    source_url            text,
    discovered_at         timestamptz,
    meeting_date          date,
    agenda_item_number    text,
    app_id                text,
    reviewer              text,
    review_notes          text,
    reviewed_at           timestamptz,
    ingested_at           timestamptz NOT NULL DEFAULT now(),
    updated_at_db         timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_rqe_review_status_escalation ON app.review_queue_entries(review_status, escalation, discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_rqe_item_id ON app.review_queue_entries(item_id);
CREATE INDEX IF NOT EXISTS idx_rqe_source_id ON app.review_queue_entries(source_id);
CREATE INDEX IF NOT EXISTS idx_rqe_review_status ON app.review_queue_entries(review_status);
CREATE INDEX IF NOT EXISTS idx_rqe_human_review ON app.review_queue_entries(human_review_required) WHERE human_review_required = true;

-- Dedupe index entries (table backed by unique dedupe_key)
CREATE TABLE IF NOT EXISTS app.dedupe_index_entries (
    key            text PRIMARY KEY,
    item_id        text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    title          text,
    source_id      text REFERENCES app.sources(source_id),
    beat           text,
    discovered_at  timestamptz,
    status         text NOT NULL DEFAULT 'pending_review'
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_die_key ON app.dedupe_index_entries(key);
CREATE INDEX IF NOT EXISTS idx_die_item_id ON app.dedupe_index_entries(item_id);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (7, '20260705_007_create_review_queue', sha256('20260705_007_create_review_queue'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
