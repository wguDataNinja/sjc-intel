SET ROLE sjc_intel_owner;

-- Migration: 20260705_009_create_health_schema
-- Health schema and tables for monitoring and workflow status.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE SCHEMA IF NOT EXISTS health;

-- Health runs table: private record of each health check execution
CREATE TABLE IF NOT EXISTS health.health_runs (
    run_id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project                 text NOT NULL DEFAULT 'sjc_intel',
    workflow                text NOT NULL,
    status                  text NOT NULL CHECK (status IN ('ok', 'warn', 'fail', 'skip')),
    started_at              timestamptz NOT NULL,
    finished_at             timestamptz,
    last_success_at         timestamptz,
    expected_cadence        interval,
    freshness_age_seconds   integer,
    records_read            integer DEFAULT 0,
    records_written         integer DEFAULT 0,
    records_rejected        integer DEFAULT 0,
    backlog                 integer DEFAULT 0,
    retry_count             integer DEFAULT 0,
    error_class             text,
    error_code              text,
    error_message_private   text,
    deployed_revision       text,
    schema_version          integer,
    migration_version       integer,
    scheduler_state         text,
    backup_state            text CHECK (backup_state IN ('ok', 'stale', 'fail')),
    storage_bytes           bigint,
    storage_growth_bytes_24h bigint,
    incident_state          text DEFAULT 'none' CHECK (incident_state IN ('none', 'active', 'resolved')),
    created_at              timestamptz NOT NULL DEFAULT now(),
    ingested_at             timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_health_runs_workflow_status ON health.health_runs(workflow, status);
CREATE INDEX IF NOT EXISTS idx_health_runs_started_at ON health.health_runs(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_health_runs_status ON health.health_runs(status);

-- Workflow status: summary view/table of latest health per workflow
CREATE TABLE IF NOT EXISTS health.workflow_status (
    workflow                text PRIMARY KEY,
    status                  text NOT NULL CHECK (status IN ('ok', 'warn', 'fail', 'skip')),
    last_run_at             timestamptz,
    last_success_at         timestamptz,
    expected_cadence        interval,
    freshness_age_seconds   integer,
    backlog                 integer DEFAULT 0,
    incident_state          text DEFAULT 'none' CHECK (incident_state IN ('none', 'active', 'resolved')),
    backup_state            text CHECK (backup_state IN ('ok', 'stale', 'fail')),
    migration_version       integer,
    updated_at              timestamptz NOT NULL DEFAULT now()
);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (9, '20260705_009_create_health_schema', sha256('20260705_009_create_health_schema'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
