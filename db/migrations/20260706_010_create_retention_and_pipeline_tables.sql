SET ROLE sjc_intel_owner;

-- Migration: 20260706_010_create_retention_and_pipeline_tables
-- Retention policy metadata, raw-artifact tracking, and bounded pipeline runs.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.source_retention_policies (
    source_id                  text PRIMARY KEY REFERENCES app.sources(source_id),
    source_type                text NOT NULL,
    fetch_frequency            text NOT NULL,
    expected_records_per_run   integer NOT NULL DEFAULT 0 CHECK (expected_records_per_run >= 0),
    raw_payload_format         text NOT NULL DEFAULT 'none',
    raw_artifact_retention_days integer NOT NULL DEFAULT 0 CHECK (raw_artifact_retention_days >= 0),
    normalized_retention_days  integer CHECK (normalized_retention_days IS NULL OR normalized_retention_days >= 0),
    retry_window_days          integer NOT NULL DEFAULT 7 CHECK (retry_window_days >= 0),
    snapshot_required          boolean NOT NULL DEFAULT true,
    archive_before_prune       boolean NOT NULL DEFAULT false,
    prune_key                  text NOT NULL DEFAULT 'discovered_at',
    ui_dependency              text NOT NULL DEFAULT 'current_and_recent',
    notes                      text,
    created_at                 timestamptz NOT NULL DEFAULT now(),
    updated_at                 timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_source_retention_policies_source_type
    ON app.source_retention_policies(source_type);

CREATE TABLE IF NOT EXISTS app.raw_artifact_records (
    artifact_id          text PRIMARY KEY,
    source_id            text NOT NULL REFERENCES app.sources(source_id),
    source_event_id      text REFERENCES app.source_events(event_id),
    item_id              text REFERENCES app.intel_items(item_id),
    artifact_type        text NOT NULL CHECK (artifact_type IN ('html', 'pdf', 'json', 'text', 'csv', 'image', 'other')),
    storage_uri          text NOT NULL,
    content_sha256       text NOT NULL,
    byte_size            bigint CHECK (byte_size IS NULL OR byte_size >= 0),
    fetched_at           timestamptz NOT NULL,
    retain_until         timestamptz NOT NULL,
    archive_required     boolean NOT NULL DEFAULT false,
    archived_at          timestamptz,
    prune_status         text NOT NULL DEFAULT 'retained'
        CHECK (prune_status IN ('retained', 'eligible', 'pruned', 'protected')),
    protected_reason     text,
    created_at           timestamptz NOT NULL DEFAULT now(),
    updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_artifact_records_source_retain_until
    ON app.raw_artifact_records(source_id, retain_until);
CREATE INDEX IF NOT EXISTS idx_raw_artifact_records_prune_status
    ON app.raw_artifact_records(prune_status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_artifact_records_content_sha256
    ON app.raw_artifact_records(content_sha256);

CREATE TABLE IF NOT EXISTS app.pipeline_runs (
    run_id              text PRIMARY KEY,
    source_id           text REFERENCES app.sources(source_id),
    run_type            text NOT NULL,
    status              text NOT NULL CHECK (status IN ('planned', 'running', 'ok', 'warn', 'fail', 'skipped')),
    started_at          timestamptz NOT NULL,
    finished_at         timestamptz,
    records_seen        integer NOT NULL DEFAULT 0 CHECK (records_seen >= 0),
    records_written     integer NOT NULL DEFAULT 0 CHECK (records_written >= 0),
    records_updated     integer NOT NULL DEFAULT 0 CHECK (records_updated >= 0),
    records_rejected    integer NOT NULL DEFAULT 0 CHECK (records_rejected >= 0),
    duplicate_count     integer NOT NULL DEFAULT 0 CHECK (duplicate_count >= 0),
    artifact_count      integer NOT NULL DEFAULT 0 CHECK (artifact_count >= 0),
    error_class         text,
    error_message       text,
    source_revision     text,
    config_digest       text,
    created_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_source_started_at
    ON app.pipeline_runs(source_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status_started_at
    ON app.pipeline_runs(status, started_at DESC);

INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (10, '20260706_010_create_retention_and_pipeline_tables',
        sha256('20260706_010_create_retention_and_pipeline_tables'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
