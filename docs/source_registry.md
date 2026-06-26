# SJC_Intel — Source Registry

> Central catalog of all monitored public information sources for St. Johns
> County, Florida.

## Purpose

The source registry (`registry/sources.yaml`) is the authoritative list of
every public channel that SJC_Intel monitors, scrapes, or reads for
intelligence. It ensures that:

- Every source has a stable identifier and clear documentation.
- Monitor frequency and automation feasibility is explicit.
- Topic and community coverage gaps are visible.
- No private or unauthorized sources are tracked.

## Schema

Each source record follows the schema defined in `schemas/source.schema.yaml`.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | string | Unique stable identifier (snake_case) |
| `name` | string | Human-readable display name |
| `description` | string | What the source provides |
| `url` | string | Primary URL |
| `base_domain` | string | Domain root for grouping |
| `source_type` | string | Platform/technology classification |
| `relevance` | string | HIGH / MEDIUM / LOW |
| `monitor_frequency` | string | daily / weekly / monthly / realtime / per_event |
| `automatable` | string | YES / PARTIALLY / LIKELY / CHALLENGING / NO |
| `status` | string | observed / configured / verified / active / failing / stale / retired |

### Optional Fields

- `topics` — Array of topic tags.
- `communities` — Array of community names (from community registry).
- `notes` — Free-form operational notes.
- `monitor_config` — (future) Hermes monitor worker configuration.
- `discovered_at` / `discovered_by` — Discovery metadata.
- `updated_at` / `updated_by` — Change tracking.

## Source Types

| Type | Description | Examples |
|------|-------------|---------|
| `wordpress_blog` | WordPress blog/ news listing | SJC County News, SJSO News Stories |
| `wordpress_portal` | Full WordPress site with multiple sections | SJC School District |
| `government_portal` | Standard government website | SJC Property Appraiser |
| `cms` | Non-WordPress CMS | Nocatee (HubSpot CMS) |
| `gis_map` | Interactive GIS/mapping application | SJC Development Tracker |
| `social_media` | Public social media channel | SJSO X/Twitter, Facebook |
| `document_management` | Document management system (future) | BoardDocs |
| `video_archive` | Recorded meeting videos (future) | School Board Video Archive |

## Status Lifecycle

```
observed → configured → verified → active → (failing → active)
                                       ↓
                                    stale → retired
```

- **observed** — Identified but not yet tested.
- **configured** — Registry entry exists.
- **verified** — Connectivity confirmed (HTTP 200, parseable).
- **active** — Being actively monitored by a Hermes worker.
- **failing** — Monitor is broken; needs attention.
- **stale** — No new items detected for an extended period.
- **retired** — No longer monitored.

## Adding a New Source

1. Ensure the source is **public** — no private groups, locked content, or
   authentication-gated pages without explicit permission.
2. Copy the YAML template from `schemas/source.schema.yaml`.
3. Fill in all required fields.
4. Set `status` to `observed` until connectivity is verified.
5. Append the record to `registry/sources.yaml`.
6. Update this documentation if a new source type is introduced.

## Current Sources

See `registry/sources.yaml` for the current list of registered sources.

As of 2026-06-03, the registry contains **10 sources** across 5 categories:

- **County Government:** SJC County News, SJC Development Tracker
- **Law Enforcement:** SJSO News Stories, SJSO Social Media
- **Education:** SJC School District
- **Community:** Nocatee Community
- **Constitutional Officers:** SJC Property Appraiser, SJC Tax Collector
- **Placeholder (future):** Supervisor of Elections, Clerk of Court
