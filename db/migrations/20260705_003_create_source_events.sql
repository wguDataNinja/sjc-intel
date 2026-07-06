SET ROLE sjc_intel_owner;

-- Migration: 20260705_003_create_source_events
-- Context containers for monitoring events.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.source_events (
    event_id                text PRIMARY KEY,
    source_id               text NOT NULL REFERENCES app.sources(source_id),
    event_type              text NOT NULL CHECK (event_type IN ('meeting', 'agenda_packet', 'page_snapshot', 'press_release_batch', 'public_notice_snapshot')),
    title                   text NOT NULL,
    event_date              date NOT NULL,
    discovered_at           timestamptz NOT NULL,
    source_url              text NOT NULL,
    document_urls           jsonb,
    status                  text NOT NULL CHECK (status IN ('discovered', 'extracted', 'partially_extracted', 'blocked', 'archived')),
    extraction_status       text,
    source_health           text CHECK (source_health IN ('accessible', 'broken_link', 'unavailable')),
    notes                   text,
    raw_source_file         text,
    created_at              timestamptz NOT NULL DEFAULT now(),
    updated_at              timestamptz,
    ingested_at             timestamptz NOT NULL DEFAULT now(),
    updated_at_db           timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_source_events_source_id ON app.source_events(source_id);
CREATE INDEX IF NOT EXISTS idx_source_events_event_date ON app.source_events(event_date DESC);
CREATE INDEX IF NOT EXISTS idx_source_events_source_id_event_date ON app.source_events(source_id, event_date DESC);
CREATE INDEX IF NOT EXISTS idx_source_events_status ON app.source_events(status);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (3, '20260705_003_create_source_events', sha256('20260705_003_create_source_events'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
