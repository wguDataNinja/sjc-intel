SET ROLE sjc_intel_owner;

-- Migration: 20260705_001_create_schemas_and_roles
-- Creates project schemas and migration tracking table.
-- Forward-only. Idempotent via IF NOT EXISTS.

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS health;

-- Migration tracking table
CREATE TABLE IF NOT EXISTS app.sjc_intel_migrations (
    version    integer PRIMARY KEY,
    name       text NOT NULL,
    checksum_sha256 text NOT NULL,
    applied_at timestamptz NOT NULL DEFAULT now(),
    applied_by text NOT NULL DEFAULT current_user,
    duration_ms integer NOT NULL CHECK (duration_ms >= 0)
);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (1, '20260705_001_create_schemas_and_roles', sha256('20260705_001_create_schemas_and_roles'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
