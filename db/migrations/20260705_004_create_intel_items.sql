SET ROLE sjc_intel_owner;

-- Migration: 20260705_004_create_intel_items
-- Core intelligence items table.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.intel_items (
    item_id                text PRIMARY KEY,
    title                  text NOT NULL,
    summary                text NOT NULL,
    source_id              text NOT NULL REFERENCES app.sources(source_id),
    source_event_id        text REFERENCES app.source_events(event_id),
    source_url             text NOT NULL,
    source_published_at    timestamptz,
    discovered_at          timestamptz NOT NULL,
    discovered_by          text,
    topics                 text[] NOT NULL,
    communities            text[],
    geographic_scope       text NOT NULL CHECK (geographic_scope IN ('county_wide', 'multi_community', 'single_community', 'neighborhood', 'address_specific')),
    urgency                text NOT NULL CHECK (urgency IN ('urgent', 'timely', 'ongoing', 'archival')),
    verification_status    text NOT NULL CHECK (verification_status IN ('unverified', 'source_confirmed', 'cross_referenced', 'fact_checked', 'disputed')),
    sensitivity            text NOT NULL CHECK (sensitivity IN ('low', 'medium', 'high')),
    recommended_channels   text[],
    raw_excerpt            text NOT NULL,
    citation               jsonb,
    primary_topic          text,
    interest_tags          text[],
    resident_relevance     jsonb,
    taxonomy_gap           text,
    human_review_required  boolean NOT NULL DEFAULT false,
    review_status          text NOT NULL DEFAULT 'pending_review' CHECK (review_status IN ('pending_review', 'in_review', 'approved', 'changes_requested', 'rejected', 'published')),
    reviewer_notes         text,
    tracked_entity_ids     text[],
    superseded_by          text REFERENCES app.intel_items(item_id),
    dedupe_key             text,
    beat                   text,
    signal                 text CHECK (signal IN ('high', 'medium', 'low_signal')),
    category               text,
    app_id                 text,
    pdf_urls               text[],
    map_url                text,
    district               text,
    raw_text               text,
    meeting_date           date,
    agenda_item_number     text,
    action_type            text,
    source_type            text,
    internal_metadata      jsonb,
    created_at             timestamptz NOT NULL,
    updated_at             timestamptz,
    ingested_at            timestamptz NOT NULL DEFAULT now(),
    updated_at_db          timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_intel_items_dedupe_key ON app.intel_items(dedupe_key) WHERE dedupe_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_intel_items_source_id ON app.intel_items(source_id);
CREATE INDEX IF NOT EXISTS idx_intel_items_source_id_discovered_at ON app.intel_items(source_id, discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_intel_items_source_event_id ON app.intel_items(source_event_id);
CREATE INDEX IF NOT EXISTS idx_intel_items_review_status ON app.intel_items(review_status);
CREATE INDEX IF NOT EXISTS idx_intel_items_discovered_at ON app.intel_items(discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_intel_items_urgency ON app.intel_items(urgency);
CREATE INDEX IF NOT EXISTS idx_intel_items_created_at ON app.intel_items(created_at DESC);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (4, '20260705_004_create_intel_items', sha256('20260705_004_create_intel_items'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
