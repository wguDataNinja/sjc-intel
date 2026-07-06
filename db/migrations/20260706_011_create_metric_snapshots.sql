SET ROLE sjc_intel_owner;

-- Migration: 20260706_011_create_metric_snapshots
-- Compact aggregate snapshots for future API/UI reads.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS app.metric_snapshots (
    snapshot_id       text PRIMARY KEY,
    snapshot_date     date NOT NULL,
    grain             text NOT NULL CHECK (grain IN ('daily', 'weekly', 'monthly', 'current')),
    metric_name       text NOT NULL,
    dimensions        jsonb NOT NULL DEFAULT '{}'::jsonb,
    dimensions_hash   text NOT NULL,
    metric_value      numeric NOT NULL,
    generated_at      timestamptz NOT NULL,
    source_run_id     text REFERENCES app.pipeline_runs(run_id),
    retention_until   timestamptz,
    visibility        text NOT NULL DEFAULT 'internal'
        CHECK (visibility IN ('public_safe', 'internal', 'private')),
    notes             text,
    created_at        timestamptz NOT NULL DEFAULT now(),
    updated_at        timestamptz NOT NULL DEFAULT now(),
    UNIQUE (snapshot_date, grain, metric_name, dimensions_hash)
);

CREATE INDEX IF NOT EXISTS idx_metric_snapshots_metric_date
    ON app.metric_snapshots(metric_name, snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_metric_snapshots_grain_date
    ON app.metric_snapshots(grain, snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_metric_snapshots_visibility
    ON app.metric_snapshots(visibility);

INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (11, '20260706_011_create_metric_snapshots',
        sha256('20260706_011_create_metric_snapshots'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
