# Retention and Pruning

## Operating Rule

The VPS should keep current normalized state, recent working artifacts, compact
snapshots, bounded pipeline/health history, and one bounded backup staging
artifact. Complete raw historical archives belong on the MacBook or another
approved archival target.

No destructive pruning is authorized by this document. `scripts/retention.py`
produces dry-run policy reports and selectors only.

## Implemented Tables

Migration `20260706_010_create_retention_and_pipeline_tables.sql` adds:

- `app.source_retention_policies`
- `app.raw_artifact_records`
- `app.pipeline_runs`

Raw HTML, PDFs, repeated payloads, and downloaded attachments are not stored in
PostgreSQL. PostgreSQL stores metadata: source, external storage URI, content
hash, byte size, fetch time, retain-until timestamp, archive requirement, and
prune status.

## Source Policies

| Source | Type | Cadence | Expected/run | Raw window | Normalized window | Archive before prune | UI dependency |
|---|---|---:|---:|---:|---|---|---|
| `sjc_county_news` | wordpress_blog | daily | 10 | 14d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjso_news_stories` | wordpress_blog | daily | 10 | 14d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjso_social_media` | social_media | realtime | 20 | 3d | 90d | true | current_normalized_state_and_compact_snapshots |
| `st_johns_citizen` | local_media | daily | 10 | 7d | 180d | true | current_normalized_state_and_compact_snapshots |
| `sjc_school_district` | wordpress_portal | weekly | 25 | 14d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_development_tracker` | gis_map | weekly | 25 | 7d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `nocatee_community` | cms | weekly | 25 | 14d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `tolomato_cdd` | official_special_district | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `trout_creek_cdd` | official_special_district | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `six_mile_creek_cdd` | official_special_district | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_property_appraiser` | government_portal | monthly | 30 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_tax_collector` | government_portal | monthly | 30 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_bcc_calendar` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_pza_boards` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_nbor_public_notices` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_road_closures` | alias | daily | 10 | 0d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_utility_department` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_budget_transparency` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_emergency_management` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_clerk_online_research` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_permit_status` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_transportation_infrastructure` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjrwmd_watering_restrictions` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjcsd_boarddocs` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjcsd_zoning_planning` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `fdot_district_two_nflroads` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `nws_jacksonville` | government_portal | daily | 10 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |
| `sjc_supervisor_of_elections` | government_portal | weekly | 25 | 30d | current/unbounded until policy | false | current_normalized_state_and_compact_snapshots |

## Pruning Selector

`select_prunable_artifacts(records, as_of)` selects a raw artifact only when:

- `retain_until <= as_of`;
- `prune_status` is not `protected`;
- if `archive_required=true`, `archived_at` is already set.

The selector does not delete files or rows.

## Storage Estimate

Initial SJC PostgreSQL footprint after schema, empty operational tables, and
current pilot-scale data should remain under 100 MB. With the source policies
above, expected normalized growth is approximately 250 to 450 rows/month before
future news ingestion, plus compact metric snapshots. Raw-artifact metadata is
small; raw payload bytes remain outside PostgreSQL and are bounded by source
windows.

Largest uncertainties:

- future approved local-news source count;
- attachment-heavy agenda or PDF workflows;
- whether social/media captures are retained as metadata only or archived;
- review queue and classification history once the application UI exists.
