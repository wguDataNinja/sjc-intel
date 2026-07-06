SET ROLE sjc_intel_owner;

-- Migration: 20260705_006_create_relationship_tables
-- Many-to-many and link tables for SJC Intel.
-- Forward-only. Idempotent via IF NOT EXISTS.

-- intel_item <-> tracked_entity M:N
CREATE TABLE IF NOT EXISTS app.intel_item_tracked_entities (
    item_id     text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    entity_id   text NOT NULL REFERENCES app.tracked_entities(entity_id) ON DELETE CASCADE,
    match_basis text,
    PRIMARY KEY (item_id, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_iite_entity_id ON app.intel_item_tracked_entities(entity_id);

-- source_event <-> source_event self-referential M:N
CREATE TABLE IF NOT EXISTS app.source_event_related_events (
    event_id          text NOT NULL REFERENCES app.source_events(event_id) ON DELETE CASCADE,
    related_event_id  text NOT NULL REFERENCES app.source_events(event_id) ON DELETE CASCADE,
    relationship_type text,
    PRIMARY KEY (event_id, related_event_id),
    CHECK (event_id <> related_event_id)
);

-- intel_item <-> topics (stored as array on intel_items; this is a materialized view alternative)
CREATE TABLE IF NOT EXISTS app.intel_item_topics (
    item_id text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    topic   text NOT NULL,
    PRIMARY KEY (item_id, topic)
);

CREATE INDEX IF NOT EXISTS idx_iit_topic ON app.intel_item_topics(topic);

-- intel_item <-> communities M:N
CREATE TABLE IF NOT EXISTS app.intel_item_communities (
    item_id     text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    community   text NOT NULL,
    PRIMARY KEY (item_id, community)
);

CREATE INDEX IF NOT EXISTS idx_iic_community ON app.intel_item_communities(community);

-- intel_item <-> interest_tags M:N
CREATE TABLE IF NOT EXISTS app.intel_item_interest_tags (
    item_id      text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    interest_tag text NOT NULL,
    PRIMARY KEY (item_id, interest_tag)
);

CREATE INDEX IF NOT EXISTS idx_iiit_interest_tag ON app.intel_item_interest_tags(interest_tag);

-- source_event <-> intel_item M:N for extracted items
CREATE TABLE IF NOT EXISTS app.source_event_items (
    event_id text NOT NULL REFERENCES app.source_events(event_id) ON DELETE CASCADE,
    item_id  text NOT NULL REFERENCES app.intel_items(item_id) ON DELETE CASCADE,
    PRIMARY KEY (event_id, item_id)
);

CREATE INDEX IF NOT EXISTS idx_sei_item_id ON app.source_event_items(item_id);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (6, '20260705_006_create_relationship_tables', sha256('20260705_006_create_relationship_tables'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
