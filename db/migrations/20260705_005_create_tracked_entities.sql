SET ROLE sjc_intel_owner;

-- Migration: 20260705_005_create_tracked_entities
-- Durable tracked entities (developments, projects, communities).
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.tracked_entities (
    entity_id          text PRIMARY KEY,
    entity_type        text NOT NULL CHECK (entity_type IN (
        'retail_development', 'education_facility', 'recreational_attraction',
        'transportation_project', 'healthcare_facility', 'mixed_use_development',
        'hospitality', 'residential_development', 'road_project',
        'infrastructure_project', 'cdd', 'community', 'business', 'other'
    )),
    label              text NOT NULL,
    description        text,
    lifecycle_status   text NOT NULL CHECK (lifecycle_status IN (
        'proposed', 'approved', 'under_construction', 'completed',
        'dormant', 'cancelled', 'tracked', 'archived'
    )),
    priority           text NOT NULL CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    communities        text[],
    aliases            text[],
    search_queries     text[],
    sources            jsonb,
    evidence_notes     text,
    last_checked       timestamptz,
    tracked_since      timestamptz NOT NULL,
    notes              text,
    ingested_at        timestamptz NOT NULL DEFAULT now(),
    updated_at_db      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tracked_entities_type_status_priority ON app.tracked_entities(entity_type, lifecycle_status, priority);
CREATE INDEX IF NOT EXISTS idx_tracked_entities_lifecycle_status ON app.tracked_entities(lifecycle_status);
CREATE INDEX IF NOT EXISTS idx_tracked_entities_priority ON app.tracked_entities(priority);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (5, '20260705_005_create_tracked_entities', sha256('20260705_005_create_tracked_entities'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
