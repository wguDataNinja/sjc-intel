SET ROLE sjc_intel_owner;

-- Migration: 20260705_002_create_sources
-- Core source registry table.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.sources (
    source_id          text PRIMARY KEY,
    name               text NOT NULL,
    description        text NOT NULL,
    url                text NOT NULL,
    base_domain        text NOT NULL,
    source_type        text NOT NULL,
    relevance          text NOT NULL CHECK (relevance IN ('HIGH', 'MEDIUM', 'LOW')),
    monitor_frequency  text NOT NULL CHECK (monitor_frequency IN ('daily', 'weekly', 'monthly', 'realtime', 'per_event')),
    automatable        text NOT NULL CHECK (automatable IN ('YES', 'PARTIALLY', 'LIKELY', 'CHALLENGING', 'NO')),
    status             text NOT NULL CHECK (status IN ('observed', 'configured', 'verified', 'active', 'failing', 'stale', 'retired')),
    topics             text[],
    communities        text[],
    notes              text,
    monitor_config     jsonb,
    discovered_at      timestamptz,
    discovered_by      text,
    updated_at         timestamptz,
    updated_by         text,
    ingested_at        timestamptz NOT NULL DEFAULT now(),
    updated_at_db      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sources_status ON app.sources(status);
CREATE INDEX IF NOT EXISTS idx_sources_source_type ON app.sources(source_type);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (2, '20260705_002_create_sources', sha256('20260705_002_create_sources'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
