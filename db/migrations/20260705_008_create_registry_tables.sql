SET ROLE sjc_intel_owner;

-- Migration: 20260705_008_create_registry_tables
-- Registry and config tables for SJC Intel.
-- Forward-only. Idempotent via IF NOT EXISTS.

-- Interest filters (keyword-based priority rules)
CREATE TABLE IF NOT EXISTS app.interest_filters (
    id              text PRIMARY KEY,
    label           text NOT NULL,
    type            text NOT NULL CHECK (type IN ('neighborhood', 'corridor', 'school', 'development', 'utility', 'emergency')),
    priority_boost  text NOT NULL CHECK (priority_boost IN ('high', 'immediate')),
    match_on        text[],
    keywords        text[] NOT NULL,
    notes           text,
    ingested_at     timestamptz NOT NULL DEFAULT now(),
    updated_at_db   timestamptz NOT NULL DEFAULT now()
);

-- Source candidates (discovery queue)
CREATE TABLE IF NOT EXISTS app.source_candidates (
    candidate_id            text PRIMARY KEY,
    name                    text NOT NULL,
    url                     text NOT NULL,
    source_type             text NOT NULL,
    homeowner_relevance     text,
    communities             text[],
    topics                  text[],
    update_frequency        text,
    automation_feasibility  text CHECK (automation_feasibility IN ('easy', 'moderate', 'challenging')),
    reliability             text,
    review_status           text NOT NULL DEFAULT 'pending_review' CHECK (review_status IN ('pending_review', 'reviewed')),
    promotion_decision      text CHECK (promotion_decision IN ('promoted', 'deferred', 'duplicate_of_canonical')),
    ingested_at             timestamptz NOT NULL DEFAULT now(),
    updated_at_db           timestamptz NOT NULL DEFAULT now()
);

-- Beat candidates (resident-interest beat discovery)
CREATE TABLE IF NOT EXISTS app.beat_candidates (
    beat_id                text PRIMARY KEY,
    name                   text NOT NULL,
    homeowner_relevance    text,
    source_types           text[],
    example_search_terms   text[],
    communities            text[],
    monitor_cadence        text,
    related_taxonomy_terms text[],
    review_status          text NOT NULL DEFAULT 'pending_review' CHECK (review_status IN ('pending_review', 'reviewed')),
    promotion_decision     text CHECK (promotion_decision IN ('promoted', 'deferred')),
    ingested_at            timestamptz NOT NULL DEFAULT now(),
    updated_at_db          timestamptz NOT NULL DEFAULT now()
);

-- Communities (geographic area registry)
CREATE TABLE IF NOT EXISTS app.communities (
    community_id    text PRIMARY KEY,
    name            text NOT NULL,
    parent_region   text,
    community_type  text,
    notes           text,
    ingested_at     timestamptz NOT NULL DEFAULT now(),
    updated_at_db   timestamptz NOT NULL DEFAULT now()
);

-- Search terms (Hermes search discovery queries)
CREATE TABLE IF NOT EXISTS app.search_terms (
    term_id         text PRIMARY KEY,
    query           text NOT NULL,
    source_type     text,
    frequency       text,
    last_searched   timestamptz,
    notes           text,
    ingested_at     timestamptz NOT NULL DEFAULT now(),
    updated_at_db   timestamptz NOT NULL DEFAULT now()
);

-- Record this migration
INSERT INTO app.sjc_intel_migrations (version, name, checksum_sha256, duration_ms)
VALUES (8, '20260705_008_create_registry_tables', sha256('20260705_008_create_registry_tables'), 0)
ON CONFLICT (version) DO NOTHING;

RESET ROLE;
