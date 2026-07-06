# PostgreSQL Adapter

## Current Authority

File-backed data remains the operating authority until a later cutover Gate is
explicitly approved. The PostgreSQL adapter is available for local Mac
development, portability rehearsal, shadow reads, snapshots, and later VPS use.

Do not connect application code as `sjc_intel_owner` or `sjc_intel_migrator`.

## Backend Selection

Default:

```bash
SJC_INTEL_ADAPTER_BACKEND=file
```

PostgreSQL shadow or test mode:

```bash
SJC_INTEL_ADAPTER_BACKEND=pg
SJC_INTEL_PG_ADAPTER_ENABLED=true
SJC_INTEL_FILE_FALLBACK_ENABLED=true
```

The facade falls back to the file adapter for read/list paths when PostgreSQL is
disabled or unavailable. Writes are not redirected to the fallback backend.

## Connection Contract

Preferred:

```bash
SJC_INTEL_PG_READER_URL=postgresql://sjc_intel_reader:...@localhost:5432/sjc_intel
SJC_INTEL_PG_WRITER_URL=postgresql://sjc_intel_writer:...@localhost:5432/sjc_intel
```

Compatibility fallback:

```bash
SJC_INTEL_PG_URL=postgresql://...@localhost:5432/sjc_intel
```

Host/user fields are also supported:

```bash
SJC_INTEL_PG_DATABASE=sjc_intel
SJC_INTEL_PG_HOST=localhost
SJC_INTEL_PG_PORT=5432
SJC_INTEL_PG_READER_USER=sjc_intel_reader
SJC_INTEL_PG_WRITER_USER=sjc_intel_writer
```

Secrets stay in local environment files or root-readable credential files
outside Git.

## Supported Adapter Operations

`PgAdapter.read_item(item_id)` searches:

- `app.intel_items.item_id`
- `app.sources.source_id`
- `app.source_events.event_id`
- `app.tracked_entities.entity_id`
- `app.review_queue_entries.queue_id`

`PgAdapter.list_items(filter_dict)` supports:

- default `app.intel_items`
- `entity_type=sources`
- `entity_type=source_events`
- `entity_type=tracked_entities`
- `entity_type=queue_entries`
- filters for `source_id`, `review_status` or `status`, `category`, `since`,
  `limit`, and `offset`

`PgAdapter.write_item(item_id, data)` performs a single transaction:

- upsert source metadata if the source does not exist;
- upsert the intel item using deterministic `item_id`;
- upsert the dedupe index when `dedupe_key` or `_dedupe_key` is present.

The adapter maps current file-backed underscore fields into PostgreSQL columns,
including `_dedupe_key`, `_category`, `_beat`, `_signal`, `_app_id`,
`_pdf_urls`, `_map_url`, `_district`, `_raw_text`, `_meeting_date`,
`_agenda_item_number`, and `_action_type`.

`PgAdapter.get_health()` returns sanitized connection state, PostgreSQL version,
database name, current database user, and source/item counts.

## Boundaries

- No owner or migrator credentials for application operations.
- No global mutable connection state.
- SQL is parameterized.
- Writes are explicit transactions with rollback on failure.
- PostgreSQL location is configuration, not business logic.
- The adapter does not run the real-data pilot or change file authority.
