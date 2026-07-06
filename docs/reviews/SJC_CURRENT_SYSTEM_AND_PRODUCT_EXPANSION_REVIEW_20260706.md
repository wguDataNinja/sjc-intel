# SJC Intel — Current System and Product Expansion Review

**Date:** 2026-07-06
**Purpose:** Evidence-based report for Buddy and ChatGPT to review the SJC Intel
project from first principles and decide broader product direction.
**Scope:** Investigation only. No features implemented, no migrations added,
no sources changed.

---

## Executive Summary

SJC Intel is a file-backed, AI-assisted local intelligence system for St. Johns
County, Florida. It discovers, monitors, classifies, and organizes public
information from 28 registered sources (9 actively extracted, ~17 configured but
not yet producing items). The system produces structured YAML records called
"intel items" — each representing one discrete resident-impact finding.

**What exists today:**
- A source registry with 28 canonical sources, 46 candidates, 13 deferred
- Two proven extractors: NBOR public notices (ASP.NET WebForms) and BCC agenda
  PDFs (with pypdf text extraction)
- A classification taxonomy with 24 topics, 10 interest tags, 14 communities,
  11 tracked entities, 7 interest filter categories
- A flat YAML review queue (132 entries, 43 pending, 83 verified)
- A deterministic dedupe index (115 unique fingerprints)
- A PostgreSQL foundation (11 migrations, 24 app/health tables, 6 project roles)
- A storage adapter pattern (FileAdapter authoritative, PgAdapter disabled by
  default, StorageFacade with fallback)
- A pilot loader (dry-run/plan/apply/rollback/parity) — blocked pending approval
- Retention dry-run tooling for 28 sources
- Compact metric snapshot generator (9 metric types)
- 109 tests passing; portability checks passing

**What does NOT exist:**
- No resident-facing UI, website, or API
- No email, alerts, social media, or newsletters
- No LLM-driven classification or extraction (all rules are deterministic)
- No Hermes runtime for automated monitoring
- No scheduled automation (no cron, launchd, or timers)
- No real-data PostgreSQL pilot (all PG tables empty)
- No VPS PostgreSQL installation
- No search, no maps, no entity pages, no timelines
- No near-duplicate detection (exact dedupe only)
- No news ingestion pipeline
- No user accounts or personalization

**28 registered sources, 9 actively producing items.**
The backlog reports 132 intel items from 10 distinct source_ids across 4 date
directories in `data/intel_items/`.

**The most important data-flow finding:** Source_events (containers) and
intel_items (findings) are correctly separated, but source_event coverage is
incomplete — only NBOR and BCC produce them. Early extracts from county news,
sheriff, and utility lack parent events.

**The most important schema limitation:** Entities, locations, topics, projects,
and documents are stored as flat text, JSON blobs, or YAML arrays — not as
relational model objects. The PostgreSQL schema has link tables
(`intel_item_tracked_entities`, `intel_item_topics`, `intel_item_communities`)
that are empty — no data has been loaded.

**The most important UI/product gap:** Zero resident-facing output exists.
132 items have been extracted and classified, but no one except Buddy and the
agent can see them. The entire pipeline produces internal artifacts only.

**Strongest candidate LLM stages:** Relevance/interest classification (currently
keyword-based with weak recall), entity extraction (currently label/alias
substring matching), topic classification refinement, relationship linking
between items, and newsletter/alert generation.

---

## Section 1 — Repository and Execution Map

### Directory Structure

```
sjc_intel/
├── AGENTS.md              # Agent roles, Git policy, logging rules
├── README.md               # Public entrypoint → README_INTERNAL.md
├── README_INTERNAL.md      # Primary dev entrypoint (current state)
├── SESSION.md              # Session narrative append-only log
├── LOG.md                  # Durable activity log
├── BACKLOG.md              # All actionable tasks with status
├── CHECKLIST.md            # (deprecated stub)
├── ROADMAP.md              # (deprecated stub)
├── STATE.md                # (deprecated stub)
├── WORKER_CONTEXT.md       # (deprecated stub)
├── VPS_ROADMAP.md          # (deprecated stub)
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── .env.example            # Documented environment variables
├── .gitignore              # Repo-specific ignores
├── .github/                # GitHub Actions workflow(s)
│
├── registry/               # -*- SOURCE-OF-TRUTH REGISTRIES -*-
│   ├── sources.yaml            # 28 canonical sources
│   ├── source_candidates.yaml  # 46 candidates, 13 deferred
│   ├── communities.yaml        # 20+ geographic communities
│   ├── interest_filters.yaml   # 7 keyword-based filter categories
│   ├── tracked_entities.yaml   # 11 durable tracked entities
│   ├── beat_candidates.yaml    # Proposed homeowner beats
│   └── search_terms.yaml       # (historical)
│
├── data/                  # -*- FILE-BACKED APPLICATION DATA -*-
│   ├── intel_items/          # YAML, organized by {date}/{source_id}.yaml
│   │   ├── 2026-06-03/          # County news, sheriff, utility (pilot)
│   │   ├── 2026-06-08/          # NBOR public notices (initial)
│   │   ├── 2026-06-26/          # BCC, emergency, utility, CDDs
│   │   └── 2026-07-04/          # NBOR, SilverLeaf discovery, CDDs
│   ├── source_events/        # YAML, organized by {date}/{source_id}.yaml
│   │   ├── 2026-06-26/          # BCC meeting events
│   │   └── 2026-07-04/          # NBOR, BCC events
│   ├── review_queue/         # Editorial review queue
│   │   ├── queue.yaml           # 132 queue entries
│   │   └── summary.yaml         # Aggregated metrics
│   ├── index/                # Dedupe index
│   │   └── prior_items.yaml     # 115 unique fingerprints
│   └── monthly/              # Monthly wrap artifacts (Aug-Sep 2025)
│
├── schemas/               # -*- YAML SCHEMA DEFINITIONS -*-
│   ├── intel_item.schema.yaml       # v2.0 — primary record type
│   ├── source_event.schema.yaml     # v1.0 — container/context records
│   ├── source.schema.yaml           # v1.0 — source registry definition
│   └── tracked_entity.schema.yaml   # v1.0 — entity tracking definition
│
├── scripts/               # -*- EXECUTABLE SCRIPTS -*-
│   ├── extract_nbor.py              # ACTIVE: NBOR page fetcher + parser
│   ├── extract_bcc_agenda.py        # ACTIVE: BCC agenda PDF extractor
│   ├── build_review_queue.py         # ACTIVE: Review queue builder
│   ├── rebuild_dedupe_index.py       # ACTIVE: Dedupe index rebuilder
│   ├── update_dedupe_index.py        # SUPPORT: Incremental dedupe update
│   ├── update_review_status.py       # SUPPORT: Review status update
│   ├── batch_review_queue.py         # SUPPORT: Batch queue operations
│   ├── batch_review.py               # SUPPORT: Batch review operations
│   ├── adapter_base.py               # ACTIVE: Abstract storage adapter
│   ├── file_adapter.py               # ACTIVE: File-backed adapter (default)
│   ├── pg_adapter.py                 # ACTIVE: PostgreSQL adapter (disabled)
│   ├── storage_adapter.py            # ACTIVE: Facade with fallback
│   ├── parity_report.py              # ACTIVE: File vs PG comparison
│   ├── pilot_loader.py               # ACTIVE: Real-data PG loader (gated)
│   ├── pilot_readiness_report.py     # ACTIVE: Pilot eligibility report
│   ├── metrics_snapshot.py           # ACTIVE: Metric snapshot generator
│   ├── retention.py                  # ACTIVE: Retention policy dry-run
│   ├── health_export.py              # ACTIVE: Health export producer
│   ├── portability_check.py          # ACTIVE: Migration/env portability
│   ├── validate.py                   # ACTIVE: Deterministic validation
│   └── migration_readiness_check.sh  # SUPPORT: Migration readiness script
│
├── tests/                 # -*- PYTEST TEST SUITE -*-
│   ├── conftest.py                # Fixtures (nbor_html, bcc_agenda, etc.)
│   ├── fixtures/                  # Test fixtures (HTML, PDF, YAML, JSON)
│   ├── test_nbor_parser.py        # 7 NBOR parser tests
│   ├── test_bcc_parser.py         # 12 BCC parser tests
│   ├── test_adapter.py            # 22 adapter tests
│   ├── test_parity.py             # 10 parity tests
│   ├── test_pilot_loader.py       # 11 pilot loader tests
│   ├── test_retention.py          # 3 retention tests
│   ├── test_metrics_snapshot.py   # 2 snapshot tests
│   ├── test_health_export.py      # 10 health export tests
│   ├── test_schemas.py            # 5 schema validation tests
│   ├── test_migration_sql.py      # 7 migration SQL tests
│   ├── test_scripts_compile.py    # 1 compilation test
│   └── test_redaction.py          # (see health_export for redaction)
│
├── db/                   # -*- DATABASE SCHEMA AND VALIDATION -*-
│   ├── migrations/           # 11 forward-only SQL migrations
│   │   ├── 20260705_001_create_schemas_and_roles.sql
│   │   ├── 20260705_002_create_sources.sql
│   │   ├── 20260705_003_create_source_events.sql
│   │   ├── 20260705_004_create_intel_items.sql
│   │   ├── 20260705_005_create_tracked_entities.sql
│   │   ├── 20260705_006_create_relationship_tables.sql
│   │   ├── 20260705_007_create_review_queue.sql
│   │   ├── 20260705_008_create_registry_tables.sql
│   │   ├── 20260705_009_create_health_schema.sql
│   │   ├── 20260706_010_create_retention_and_pipeline_tables.sql
│   │   └── 20260706_011_create_metric_snapshots.sql
│   ├── rollback/            # Down-migrations for each forward migration
│   ├── validation/          # Per-migration validation + 999_full_validation.sql
│   └── fixtures/            # YAML test fixtures
│
├── docs/                  # -*- DOCUMENTATION -*-
│   ├── cadence.md               # Daily/weekly/monthly rhythm
│   ├── taxonomy.md              # Controlled vocabularies
│   ├── data_model.md            # Entity-relationship reference
│   ├── operator_mode.md         # Session startup routine
│   ├── discovery_loops.md       # 6 discovery loop designs
│   ├── postgresql_adapter.md    # PG adapter behavior contract
│   ├── retention.md             # Retention policy reference
│   ├── snapshots_and_metrics.md # Metric snapshot behavior
│   ├── news_ingestion_readiness.md  # Future news boundaries
│   ├── VPS_CONTINUITY.md        # VPS continuity record
│   ├── monitoring_workflow.md   # Monitoring workflow spec
│   ├── hermes_task_contract.md  # Hermes delegation contracts
│   ├── monitor_specs/           # Per-source monitor specs (5 files)
│   ├── reviews/                 # Review artifacts (this report, preflight, etc.)
│   ├── design/                  # Design docs (tracked_entities, etc.)
│   └── archive/                 # Deprecated docs
│
├── logs/                  # -*- LOGS -*-
│   ├── agents/             # Agent logs per agent per session
│   ├── runs/               # Cadence run logs + LAST_RUN markers
│   │   ├── daily/LAST_RUN
│   │   ├── weekly/LAST_RUN
│   │   └── monthly/LAST_RUN
│   ├── sessions/           # Full session narratives
│   └── conversations/      # Buddy's GPT research threads (curated)
│
├── deploy/                # Deployment templates (inert)
│   ├── env.example
│   ├── services/sjc-intel-monitor.service
│   └── timers/
│
├── agents/                # Role definitions (non-interactive)
├── prompts/               # Hermes task contract prompts
├── runtime/               # (future runtime support)
└── .opencode/             # OpenCode agent definitions and memory
```

### Main Execution Paths

All execution paths are manual — no automation:

**Source discovery** (manual agent investigation):
```
registry/source_candidates.yaml
  → agent reads → evaluates connectivity → promotes to sources.yaml
```

**Fetching** (manual per-source scripts or Hermes delegation):
```
scripts/extract_nbor.py        → HTTP GET → NBOR HTML → parse_rows() → records
scripts/extract_bcc_agenda.py  → HTTP GET → Clerk HTML → parse_meetings() → download PDF → extract text → parse_agenda_items()
Manual HTTP GET (county news, sheriff, utility) → inspect page → extract items
```

**Parsing + Normalization** (within each extractor):
```
records → classify_category() → classify_topic() → classify_urgency() → normalize_records() → intel_item records
```

**Classification** (deterministic keyword/regex in extractors):
```
classify_category: regex on title + description → beat categories
classify_topic: mapping dict beat → topics[]
classify_urgency: category-based (ROW→ongoing, hearing→timely)
classify_sensitivity: beat-based (rezoning→medium, else→low)
Interest filter matching: build_review_queue.py checks keyword lists
Entity matching: label/alias exact substring against title/summary/excerpt
```

**Persistence** (file-backed only):
```
normalized intel_item → YAML → data/intel_items/{date}/{source_id}.yaml
source_event metadata → YAML → data/source_events/{date}/{source_id}.yaml
```

**Review queue** (rebuild from all intel_items):
```
scripts/rebuild_dedupe_index.py  → reads all intel_items → dedupes → data/index/prior_items.yaml
scripts/build_review_queue.py    → reads all intel_items + dedupe + filters + entities → queue.yaml + summary.yaml
```

**Metrics** (from file adapter):
```
scripts/metrics_snapshot.py --backend file
  → FileAdapter.list_items() → 9 metric counter snapshots
```

**Retention** (from source registry):
```
scripts/retention.py --json
  → reads registry/sources.yaml → builds RetentionPolicy per source → dry run
```

**Pilot** (gated real-data load):
```
scripts/pilot_loader.py --dry-run|--plan|--apply|--rollback|--parity
  → selects eligible records → classifies → maps to PG → upserts (or rollback)
```

### End-to-End Flow (Plain Language)

```
Source registry (sources.yaml)
  └── Extractor script (HTTP GET → parse HTML/PDF)
        └── Raw records (list of dicts)
              └── Normalizer (classify, summarize, dedupe key)
                    └── Intel item (intel_item.schema.yaml format)
                          ├── YAML file (data/intel_items/{date}/{source_id}.yaml)
                          ├── Source event YAML (data/source_events/{date}/{source_id}.yaml)
                          ├── Dedupe index (data/index/prior_items.yaml)
                          ├── Review queue (data/review_queue/queue.yaml)
                          │     └── Human reviews (manual review_status updates)
                          ├── Metric snapshots (scripts/metrics_snapshot.py)
                          └── Future: PostgreSQL adapter → app.intel_items table
                                └── Future: API/UI/Website
```

---

## Section 2 — Complete Source Inventory

### Confirmed: 28 canonical sources in `registry/sources.yaml`

The README_INTERNAL.md reports 28 canonical sources. The registry file at
`registry/sources.yaml` contains exactly 27 active/verified entries plus 1
deprecated alias (`sjc_road_closures`). Not all are producing intel items.

### Source Table

| # | Source ID | Name | Type | Status | Fetch Mechanism | Items? | Parser |
|---|-----------|------|------|--------|-----------------|--------|--------|
| **Daily priority** | | | | | | | |
| 1 | `sjc_nbor_public_notices` | NBOR Public Notices | gov_portal | verified | HTTP GET (ASP.NET) | ✅ 50 | `extract_nbor.py` |
| 2 | `sjc_utility_department` | Utility Dept | gov_portal | verified | HTTP GET | ✅ 8 | Manual |
| 3 | `sjc_county_news` | County News | wordpress_blog | active | HTTP GET | ✅ 10 | Manual |
| 4 | `sjso_news_stories` | SJSO News | wordpress_blog | active | HTTP GET | ✅ 5 | Manual |
| 5 | `sjc_emergency_management` | Emergency Mgmt | gov_portal | verified | HTTP GET | ✅ 1 | Manual |
| 6 | `st_johns_citizen` | St. Johns Citizen | local_media | active | HTTP GET | ❌ 0 | Manual (context only) |
| **Weekly priority** | | | | | | | |
| 7 | `sjc_bcc_calendar` | BCC Calendar | gov_portal | verified | HTTP GET + PDF | ✅ 44 | `extract_bcc_agenda.py` |
| 8 | `sjc_school_district` | School District | wordpress_portal | verified | HTTP GET | ❌ 0 | None |
| 9 | `sjc_development_tracker` | Dev Tracker | gis_map | verified | Browser needed | ❌ 0 | None |
| 10 | `nocatee_community` | Nocatee Community | cms | verified | HTTP GET | ❌ 0 | None |
| 11 | `sjc_pza_boards` | Planning & Zoning | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 12 | `sjc_budget_transparency` | Budget/OMB | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 13 | `sjc_clerk_online_research` | Clerk Online | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 14 | `sjc_permit_status` | Permit Search | gov_portal | verified | Browser/form needed | ❌ 0 | None |
| 15 | `sjc_transportation_infrastructure` | Transportation | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 16 | `sjrwmd_watering_restrictions` | SJRWMD | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 17 | `fdot_district_two_nflroads` | FDOT District 2 | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 18 | `nws_jacksonville` | NWS Jacksonville | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 19 | `sjc_supervisor_of_elections` | Supervisor of Elections | gov_portal | verified | HTTP GET | ❌ 0 | None |
| **CDD sources** | | | | | | | |
| 20 | `tolomato_cdd` | Tolomato CDD | official_special_district | active | HTTP GET | ✅ 3 | Manual |
| 21 | `trout_creek_cdd` | Trout Creek CDD | official_special_district | active | HTTP GET (RSS) | ✅ 3 | Manual |
| 22 | `six_mile_creek_cdd` | Six Mile Creek CDD | official_special_district | active | HTTP GET (RSS) | ✅ 3 | Manual |
| **Monthly/seasonal** | | | | | | | |
| 23 | `sjc_property_appraiser` | Property Appraiser | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 24 | `sjc_tax_collector` | Tax Collector | gov_portal | verified | HTTP GET | ❌ 0 | None |
| **School stack** | | | | | | | |
| 25 | `sjcsd_boarddocs` | BoardDocs | gov_portal | verified | HTTP GET | ❌ 0 | None |
| 26 | `sjcsd_zoning_planning` | School Zoning | gov_portal | verified | HTTP GET | ❌ 0 | None |
| **Social media** | | | | | | | |
| 27 | `sjso_social_media` | SJSO Social Media | social_media | verified | API needed | ❌ 0 | None |
| **Deprecated** | | | | | | | |
| — | `sjc_road_closures` | Road Closures (DEPRECATED) | alias | stale | — | ❌ 0 | Replaced by #1 |

### Items by Source (from review queue summary)

| Source ID | Items |
|-----------|-------|
| `sjc_nbor_public_notices` | 50 |
| `sjc_bcc_calendar` | 44 |
| `sjc_county_news` | 9 |
| `sjc_utility_department` | 8 |
| `silverleaf_discovery` (not a registered source) | 6 |
| `sjso_news_stories` | 5 |
| `tolomato_cdd` | 3 |
| `trout_creek_cdd` | 3 |
| `six_mile_creek_cdd` | 3 |
| `sjc_emergency_management` | 1 |
| **Total** | **132** |

### Sources Not Yet Producing Items (17 of 28)

These sources have registry entries but no extraction scripts, no items, and
no automated fetching:

- County school district, development tracker, Nocatee community, PZA boards,
  budget transparency, Clerk online research, permit status, transportation,
  SJRWMD, FDOT, NWS Jacksonville, elections, property appraiser, tax collector,
  BoardDocs, school zoning, SJSO social media

### Geographic and Subject Gaps

- **Northwest St. Johns / SilverLeaf** is the best-covered area (50+ items)
- **Nocatee, TrailMark, Shearwater** have sparse coverage (CDDs only)
- **St. Augustine, Ponte Vedra** have near-zero coverage
- **South county** has zero coverage
- Subject gaps: Crime (5 items), education (1), environment (1), housing (0),
  coastal projects (0)

---

## Section 3 — Data Lifecycle Walkthrough

### 3a. NBOR Public Notice (road closure)

**Fetched input:** HTTP GET to `https://webapp.sjcfl.us/webnews/NBRscreend.aspx`
→ ~150KB of ASP.NET WebForms HTML.

**Raw fields:** `{title, description, district, category, date, pdf_urls, map_url, app_id}`

**Cleaning:** HTML tags stripped from description. Line noise removed.

**Parser output:** `parse_rows()` → 25 records. Example:

```python
{
  "title": "MAJMOD 2023000011 Canopy Shores",
  "description": "Major modification to Canopy Shores PUD...",
  "district": "DISTRICT 4",
  "category": "PUBLIC HEARING",
  "date": "8/7/2026",
  "pdf_urls": ["https://webapp.sjcfl.us/webnews/vu.aspx?..."],
  "map_url": "",
  "app_id": "MAJMOD 2023000011"
}
```

**Normalization:** `normalize_records()` → intel_item:

```yaml
item_id: "SJC-NBOR-20260704-0001"
title: "MAJMOD 2023000011 Canopy Shores"
summary: "Public hearing: MAJMOD 2023000011 Canopy Shores — Major modification..."
source_id: sjc_nbor_public_notices
topics: [development, county_government, public_notices]
urgency: timely
sensitivity: medium
beat: rezoning_comp_plan_dri
interest_tags: [development_watch]
resident_relevance:
  summary: "Public hearing affecting St. Johns County residents."
  affected_audiences: [residents, homeowners, homeowners, prospective_movers]
  confidence: high
```

**Generated ID:** `SJC-NBOR-20260704-0001`

**Deduplication:** `_dedupe_key` = SHA256 of `"sjc_nbor_public_notices||PUBLIC HEARING||MAJMOD 2023000011||8/7/2026"`[:16]

**Classification:** `classify_category()` matches `MAJMOD` regex → `rezoning_comp_plan_dri` → topics `[development, county_government, public_notices]`

**Provenance:** `source_event_id: EVT-NBOR-20260704-0001`

**File representation:**
- Intel item: `data/intel_items/2026-07-04/sjc_nbor_public_notices.yaml`
- Source event: `data/source_events/2026-07-04/sjc_nbor_public_notices.yaml`

**PostgreSQL representation:** Not loaded (all PG tables empty).

**Review state:** `pending_review` (default). Escalation = `high` (via priority beat `rezoning_comp_plan_dri`).

**Metric effect:** Would increment `intel_items_total`, `intel_items_by_source[sjc_nbor_public_notices]`, `intel_items_by_status[pending_review]`, `intel_items_by_category[PUBLIC HEARING]`.

**Retention outcome:** Gov portal type → 30-day raw retention, unbounded normalized.

### 3b. BCC Agenda Item (rezoning)

**Fetched:** Clerk Board Records HTML → parsed to meeting list → agenda PDF downloaded → pypdf text extraction.

**Raw fields:** From PDF: `{number, title, text, lines, section, action_type}`

**Parser:** `parse_agenda_items()` splits PDF text by numbered items, handles section transitions (consent/regular/public_hearing).

**Normalized:** Interest tags `[development_watch, property_values]`. Signal `high_signal`. Beat `rezoning_comp_plan_dri`.

**Dedupe key:** SHA256 of `"sjc_bcc_calendar||2026-01-20||regular.2||REZ 2025-11 Nothing Putt Fun"`[:16]

**Review:** `pending_review`, escalation `high`.

### 3c. Rejected/Filtered Record

Items with `sensitivity: low` and `urgency: archival` and no matched entities get
`escalation: low` — they remain in the queue but are deprioritized.

From the summary: 35 items have `escalation: low` — these are archival items
from CDD sources and some county news that don't match interest filters.

### 3d. Duplicate/Update Case

If the exact same NBOR page is fetched twice, items with the same `_dedupe_key`
are detected as duplicates by `rebuild_dedupe_index.py`. The index has 115 unique
keys from 132 total items — about 17 items were duplicates or had null keys.

The review queue builder (`build_review_queue.py`) deduplicates by `item_id`,
keeping the first occurrence. Existing review state is preserved across rebuilds.

---

## Section 4 — Current Domain Model

### 4a. Implemented Entities

**source** (schema: `schemas/source.schema.yaml`)
- Purpose: Represents one monitored public information channel
- Key fields: `source_id`, `name`, `url`, `source_type`, `relevance`, `monitor_frequency`, `status`, `topics`
- Relationships: Has many source_events; referenced by intel_items
- Lifecycle: `observed → configured → verified → active → failing/stale/retired`
- Authority: File (`registry/sources.yaml`); PostgreSQL `app.sources` exists but empty
- Status: **fully implemented**, 28 entries
- Currently populated: ✅ YAML

**source_event** (schema: `schemas/source_event.schema.yaml`)
- Purpose: Container/context record for one source occurrence
- Key fields: `event_id`, `source_id`, `event_type`, `title`, `event_date`, `discovered_at`, `source_url`, `status`, `extracted_item_ids`
- Relationships: Belongs to a source; has many intel_items (via `extracted_item_ids` and `source_event_id`)
- Lifecycle: `discovered → extracted/partially_extracted → blocked/archived`
- Authority: File (`data/source_events/{date}/{source_id}.yaml`); PG `app.source_events` exists but empty
- Status: **implemented but incomplete** — only NBOR and BCC produce source_events
- Currently populated: ✅ YAML for NBOR + BCC only

**intel_item** (schema: `schemas/intel_item.schema.yaml`)
- Purpose: One discrete resident-impact finding — the atomic unit of intelligence
- Key fields: `item_id`, `title`, `summary`, `source_id`, `source_url`, `discovered_at`, `topics`, `geographic_scope`, `urgency`, `verification_status`, `sensitivity`, `review_status`, `interest_tags`, `resident_relevance`, `tracked_entity_ids`, `_dedupe_key`, `_beat`
- Relationships: Belongs to source_event; may link to tracked_entities; enters review queue; fingerprinted in dedupe index
- Lifecycle: Via review_status: `pending_review → in_review → verified/rejected_noise/duplicate/archived`
- Authority: File (`data/intel_items/{date}/{source_id}.yaml`); PG `app.intel_items` exists but empty
- Status: **fully implemented**, 132 items
- Currently populated: ✅ YAML

**review_queue_entry** (generated artifact, no schema file)
- Purpose: One editorial review task for one intel item
- Key fields: `queue_id`, `item_id`, `title`, `summary`, `source_id`, `beat`, `topics`, `escalation`, `sensitivity`, `review_status`, `matched_filters`, `matched_entities`, `application_id`
- Relationships: References one intel_item by `item_id`
- Lifecycle: `pending_review → in_review → verified/needs_followup/rejected_noise/duplicate/escalated/archived`
- Authority: File (`data/review_queue/queue.yaml`); PG `app.review_queue_entries` exists but empty
- Status: **fully implemented**, 132 entries
- Currently populated: ✅ YAML

**dedupe_entry** (generated artifact)
- Purpose: One unique fingerprint of a known intel item
- Key fields: `key` (16-char hex hash), `item_id`, `title`, `source_id`, `beat`, `discovered_at`, `status`
- Relationships: References one intel_item by `item_id`
- Authority: File (`data/index/prior_items.yaml`); PG `app.dedupe_index_entries` exists but empty
- Status: **fully implemented**, 115 entries
- Currently populated: ✅ YAML

**interest_filter** (registry)
- Purpose: Keyword-based rules that flag priority items
- Key fields: `id`, `label`, `type`, `priority_boost`, `match_on` (fields), `keywords`
- Relationships: Matched against intel_items at queue build time
- Authority: File (`registry/interest_filters.yaml`); PG `app.interest_filters` exists but empty
- Status: **implemented**, 7 filter groups
- Currently populated: ✅ YAML

**tracked_entity** (registry)
- Purpose: Durable thing watched over time (development project, road, school, etc.)
- Key fields: `entity_id`, `entity_type`, `label`, `description`, `lifecycle_status`, `priority`, `communities`, `aliases`, `search_queries`, `sources`, `evidence_notes`
- Relationships: Linked to intel_items via `tracked_entity_ids[]` (array on intel_item) and inferred by review queue builder
- Lifecycle: `proposed → approved → under_construction → completed / dormant / cancelled / tracked → archived`
- Authority: File (`registry/tracked_entities.yaml`); PG `app.tracked_entities` exists but empty
- Status: **implemented**, 11 entities
- Currently populated: ✅ YAML

**community** (registry)
- Purpose: Controlled vocabulary for geographic areas
- Key fields: `id`, `name`, `type`, `parent_area`, `status`
- Relationships: Referenced by intel_items (via `communities[]` array), sources, tracked_entities
- Authority: File (`registry/communities.yaml`); PG `app.communities` exists but empty
- Status: **implemented**, 20+ entries
- Currently populated: ✅ YAML

### 4b. PostgreSQL-Only Entities (Tables Exist, Empty)

These tables have no data because no real-data pilot has been executed:

- `app.source_retention_policies` (migration 010)
- `app.raw_artifact_records` (migration 010)
- `app.pipeline_runs` (migration 010)
- `app.metric_snapshots` (migration 011)
- `health.health_runs` (migration 009)
- `health.workflow_status` (migration 009)

Link tables (migration 006, all empty):
- `app.intel_item_tracked_entities`
- `app.intel_item_topics`
- `app.intel_item_communities`
- `app.intel_item_interest_tags`
- `app.source_event_items`
- `app.source_event_related_events`

### 4c. Concepts Flattened into Text or JSON

The following important concepts exist only as text, arrays, or JSON blobs
rather than as relational model objects:

1. **Topics** — Stored as `text[]` on intel_items. No separate topics table
   with descriptions, allowed values list, or relationship tracking (the
   `app.intel_item_topics` table exists but is empty).

2. **Communities** — Stored as `text[]` on intel_items. Same limitation.
   The `app.communities` table exists but is empty.

3. **Interest tags** — Stored as `text[]` on intel_items.

4. **Entity linkages** — Stored as `tracked_entity_ids text[]` on intel_items.
   The M:N table `app.intel_item_tracked_entities` exists but is empty.

5. **Location data** — No structured location model. Items have `geographic_scope`
   (enum) and `communities` (text array) but no lat/lng, address, parcel ID, or
   map coordinates.

6. **Document references** — Stored as `pdf_urls text[]` and `map_url text`
   fields. No structured document/attachment model.

7. **Source citations** — Stored as `jsonb` (citation block). No structured
   citation model.

8. **Resident relevance** — Stored as `jsonb` (nested block with summary,
   audiences, why_it_matters, confidence, inference_notes).

### 4d. Important Missing Concepts

These product-relevant concepts are not modeled at all:

- **Neighborhoods** (only as community type, no spatial or relational model)
- **Developments** (only as tracked_entity type or keyword match)
- **Parcels** (not modeled)
- **Roads infrastructure** (not modeled)
- **Schools** (not as entity; just a topic)
- **Government bodies** (not modeled; captured in source_id naming only)
- **Developers/contractors** (not extracted from source text)
- **Projects** (only as tracked_entities; no project structure with phases,
  dates, statuses, documents)
- **Infrastructure work** (only as topic keyword)
- **Dates and milestones** (only as `source_published_at` and `discovered_at`;
  no structured date/milestone model)
- **Geographic coverage** (only `geographic_scope` enum)
- **Affected residents** (only `affected_audiences` text array in
  `resident_relevance` JSON)
- **Issue types** (only via beat/category keywords)
- **Source claims** (not modeled separately from intel items)
- **Relationships between official records and news coverage** (not modeled;
  items from different sources are not automatically linked)

---

## Section 5 — File and PostgreSQL Authority

### Current Storage Arrangement

**Authoritative:** YAML/JSON files on the local MacBook filesystem.

**File organization:**
- `data/intel_items/{YYYY-MM-DD}/{source_id}.yaml` — one file per source per day
- `data/source_events/{YYYY-MM-DD}/{source_id}.yaml` — one file per source per day
- `data/review_queue/queue.yaml` — single flat file
- `data/review_queue/summary.yaml` — single flat file
- `data/index/prior_items.yaml` — single flat file
- `registry/*.yaml` — source-of-truth registries

**PostgreSQL schema** (11 migrations, 24 tables):

| Schema | Tables | Status |
|--------|--------|--------|
| `app` | 22 tables | All created, all empty |
| `archive` | 0 tables | Empty schema |
| `health` | 2 tables | Created, empty |

**6 project roles:** `sjc_intel_owner`, `sjc_intel_writer`, `sjc_intel_reader`,
`sjc_intel_migrator`, `sjc_intel_monitor`, `sjc_intel_backup`

**Backend selection:**
- Env var `SJC_INTEL_ADAPTER_BACKEND` (default: `file`)
- Env var `SJC_INTEL_PG_ADAPTER_ENABLED` (default: `false`)
- `StorageFacade` wraps primary/fallback pattern

**Fallback behavior:** When PG is primary but disabled or fails, `read_item` and
`list_items` fall back to FileAdapter. Writes are not redirected.

**Parity:** `scripts/parity_report.py` compares file vs PG counts, distributions
by source_id and review_status, and dedupe key sets.

**Rollback:** `pilot_loader.py --rollback` deletes rows by specific `item_id` set
from `app.intel_items`, `app.dedupe_index_entries`, `app.source_events`, and
`app.source_event_items`.

**Pilot:** `pilot_loader.py` supports dry-run/plan/apply/rollback/parity. Apply
requires recent backup and explicit `--apply` flag. Currently blocked because
all PG tables are empty.

**What cutover would mean:** Migrating authority from files to PostgreSQL would
require: (1) loading all existing YAML items into PG, (2) verifying parity,
(3) switching the default adapter, (4) updating all scripts to use the adapter,
(5) decommissioning file writes. This has NOT been planned or approved.

**What remains intentionally blocked:**
- PG adapter is disabled by default (`_enabled = False`)
- Snapshot writes require `SJC_INTEL_SNAPSHOT_WRITE_ENABLED=true`
- Pilot apply requires backup + explicit flag
- No VPS PostgreSQL installation
- No service/timer activation

**Current schema intent:** The PostgreSQL schema is designed as a broader
long-term application model, not merely a shadow of file records. The 24 tables
include relationship tables, registry tables, health tracking, retention
policies, pipeline runs, and metric snapshots — all beyond what the file layer
supports. However, the file layer remains authoritative and the PG schema
mirrors the file structure exactly for intel_items, sources, source_events,
and dedupe entries.

---

## Section 6 — Classification and Intelligence Logic

### 6a. Current Categories

All classification is **deterministic** — keyword/regex rules in Python. No LLM.

**Beat categories** (assigned by extractors):
- `roadwork_traffic` — road closures, drainage, traffic keywords
- `utilities_water` — utility company names in NBOR
- `rezoning_comp_plan_dri` — REZ, CPA, ZVAR, PUD, MAJMOD codes
- `site_plans_permits_construction` — construction keywords (catch-all)
- `transportation` — BCC agenda road/traffic keywords
- `taxes_exemptions_trim_vab` — budget/millage/fee keywords
- `parks_amenities` — park/library/beach keywords
- `public_safety_livability` — safety/emergency/fire keywords
- `local_government_budget_procurement` — contract/procurement keywords
- `emergency_weather_fire_flood` — (from taxonomy, rare)

**Topics** (mapped from beat): 24 canonical topics in `docs/taxonomy.md`.

**Interest tags** (from beat or keyword):
- `traffic_impact`, `safety_concern`, `cost_impact`, `property_values`,
  `school_zones`, `quality_of_life`, `development_watch`, `utility_impact`,
  `emergency_awareness`, `community_event`

**Interest filters** (7 categories, keyword-scan at queue-build time):
- `neighborhood_silverleaf`, `neighborhood_nocatee`, `corridor_cr210`,
  `corridor_sr16`, `school_zoning_changes`, `silverleaf_northwest_dev`,
  `major_development`, `utility_disruption`, `emergency_alerts`

### 6b. How NBOR Classification Works

Example: `classify_category()` in `extract_nbor.py`:
1. Check title for `REZ \d+` → `rezoning_comp_plan_dri`
2. Check title for `CPA` or "comp plan" → `rezoning_comp_plan_dri`
3. Check title for `ZVAR` or `PVZVAR` or "variance" → `rezoning_comp_plan_dri`
4. Check title for `MAJMOD` or `MINMOD` or "PUD" → `rezoning_comp_plan_dri`
5. Check title for `PLNAPPL` or "appeal" → `rezoning_comp_plan_dri`
6. Check title for `SUPMIN` or "special use" → `site_plans_permits_construction`
7. Check description for road keywords → `roadwork_traffic`
8. Check for utility company names → `utilities_water`
9. Check for construction keywords → `site_plans_permits_construction`
10. Default → `site_plans_permits_construction`

### 6c. How BCC Agenda Classification Works

`classify_action_type()`:
- "public hearing" → `public_hearing`
- "ordinance" → `ordinance`
- "resolution" → `resolution`
- "contract/agreement/award" → `contract`
- "budget/millage/appropriation" → `budget`
- "rezoning/rez/comp plan/pud" → `land_use`
- "procurement/bid/rfb/rfq/rfi" → `procurement`
- "proclamation" → `proclamation`
- "consent/minutes" → `consent`
- Default → `regular_agenda`

`classify_resident_impact()`: Keyword scan against ~25 high-signal keywords,
~10 medium, ~6 low/routine.

### 6d. Review Queue Classification

`build_review_queue.py` adds dynamic classification:

**Escalation** (computed from item + queue state):
- `urgency=urgent` or emergency keywords → `immediate`
- `human_review_required` or `sensitivity=high` → `high`
- Beat in `PRIORITY_BEATS` → `high` (rezoning, transportation, utilities, taxes, public_safety)
- `urgency=timely` → `high`
- `signal=high_signal` → `high`
- `signal=medium_signal` → `normal`
- Default → `low`

**Interest filter matching:** Each item's title/summary/raw_excerpt/description/
communities are checked as substrings against each filter's keyword list.

**Entity matching:** Entity labels and aliases checked as exact case-insensitive
substrings against title/summary/raw_excerpt.

### 6e. Classification Gaps

- **Multi-label vs single:** Items can have multiple topics (array), but
  confidence is binary (present/absent).
- **No confidence scoring:** Classification rules produce deterministic output
  with no uncertainty measure.
- **No false-positive controls:** Rules are simple — any rezoning code match
  gives the beat, even if the item is actually unrelated.
- **No false-negative tracking:** No way to measure items that should have been
  classified differently.
- **No re-classification:** Items keep their original classification.
  Rebuilding the queue recomputes escalation and filter/entity matches but
  doesn't change topics/beats/interest_tags from the extractor.
- **No relationship linking:** Items from different sources about the same
  project/event are not automatically linked.
- **Weak recall on entity matching:** Only label and aliases (multi-word exact
  phrases) are matched. Single-word entities, partial names, and typos are missed.

---

## Section 7 — Current LLM Posture

### 7a. LLM Usage: NONE

No LLM is used anywhere in the current codebase. All classification, extraction,
normalization, filtering, and deduplication is deterministic Python.

### 7b. LLM Stubs: NONE

No LLM client imports, no API call patterns, no stubbed inference functions,
no mock LLM output handlers exist in scripts/ or anywhere in the repo.

### 7c. LLM Planning: YES

LLMs are referenced in documentation as planned/possible:

- `prompts/hermes_*.md` — Hermes workers are expected to use LLMs for
  extraction and classification when delegated
- `docs/discovery_loops.md` — Hermes workers "parse HTML, extract candidate
  items" (may use LLM)
- `docs/resident_interest_classification.md` — RI classifier could use LLM
- `docs/design/tracked_entities_design.md` — entity extraction from text
  mentioned as possible LLM use
- `docs/news_ingestion_readiness.md` — "Optional constrained relevance or
  extraction step" could be LLM

### 7d. LLM-Explicitly-Prohibited: NOWHERE

No explicit prohibition of LLM use exists in the codebase. AGENTS.md safety
rules require public sources only but don't ban LLM calls.

### 7e. Deterministic Alternatives Assessment

For each plausible LLM stage, here is what exists now:

| Stage | Current | Deterministic Quality | LLM Would Help? |
|-------|---------|----------------------|------------------|
| Relevance classification | Keyword/regex beat mapping | Weak recall, misses context | Yes — better if topically ambiguous |
| Topic classification | Beat→topics dict mapping | Binary, no confidence | Medium — taxonomy is small enough for rules |
| Entity extraction | Label/alias exact substring | Misses partials, abbreviations | Yes — especially for people/orgs |
| Location extraction | Not done (`communities[]` from source) | N/A | Yes — address/place extraction |
| Event/milestone extraction | Not done | N/A | Yes — infer dates from text |
| Relationship linking | Not done | N/A | Yes — link items across sources |
| Summarization | Truncated text fields | Raw excerpts only | Yes — better resident summaries |
| Duplicate detection | Exact SHA256 dedupe key | Exact only | Yes — near-duplicate text comparison |
| Claim extraction | Not done | N/A | Yes — extract specific claims |
| Impact assessment | Keyword-based audience lists | Generic | Yes — nuanced impact description |
| Newsletter generation | Not done | N/A | Yes — required |
| Social media drafts | Not done | N/A | Yes — required |
| Alert matching | Interest filter keywords | Basic | Medium — personalization needs LLM |
| Question answering | Not done | N/A | Yes — for resident Q&A later |

### 7f. Areas Where LLM May Be Inappropriate

- **Official record extraction** — NBOR ASP.NET tables, BCC PDF agenda items.
  Deterministic parsing is correct and transparent. LLM would add cost, latency,
  and hallucination risk for structured government data.
- **Deduplication** — Exact dedupe by deterministic hash is correct.
  LLM could help with near-duplicates but should not replace exact matching.
- **Sensitivity classification** — Rules-based (by beat) is safer than
  LLM judgment for legal/safety content.
- **Verification status** — `source_confirmed` for official sources is
  deterministic by source type. LLM not needed.

---

## Section 8 — Current UI and Publication Assumptions

### 8a. Implemented: NOTHING

There is no UI, API, website, or publication mechanism.

### 8b. Partially Implemented: Queue Review

The `data/review_queue/queue.yaml` and `summary.yaml` are designed to feed a UI,
but no frontend exists. Manual JSON/YAML inspection is the only way to browse items.

**`batch_review.py`** and **`update_review_status.py`** provide CLI-based
review operations (set review_status, add notes).

### 8c. Planned (in documentation)

| Feature | Where | Current State |
|---------|-------|---------------|
| Public feed | `docs/taxonomy.md` (recommended_channels) | Only field values defined |
| Search | `registry/search_terms.yaml` | Stale, unused |
| Filters | `registry/interest_filters.yaml` | Used for queue only, not UI |
| Map | `schemas/intel_item.schema.yaml` (`geographic_scope`) | Enum field only, no coordinates |
| Entity pages | `registry/tracked_entities.yaml` | Registry exists, no UI |
| Source pages | `registry/sources.yaml` | Registry exists, no UI |
| Item detail pages | `schemas/intel_item.schema.yaml` | Schema exists, no UI |
| Review queue UI | `data/review_queue/` | Flat YAML, CLI only |
| Status/metrics dashboard | `docs/snapshots_and_metrics.md` | Pipeline generates snapshots, no UI |
| Timelines | Not designed | N/A |
| User accounts | Not designed | N/A |
| Saved interests | Not designed | N/A |
| Alerts | `docs/taxonomy.md` (`alert` channel) | Field exists, no alerting |
| Email | `docs/taxonomy.md` (`newsletter` channel) | Field exists, no email |
| Social media output | `docs/taxonomy.md` (`social_brief` channel) | Field exists, no output |
| Exports | Not designed | N/A |

### 8d. Database Queries for Views

No database queries exist because:
1. No data has been loaded into PostgreSQL
2. No UI exists to query against
3. The file adapter's `list_items(filter_dict)` is the closest thing to
   runnable queries

The metric snapshot generator produces data that could feed UI widgets:
- `intel_items_total`
- `intel_items_by_source`
- `intel_items_by_status`
- `intel_items_by_category`
- `sources_by_type`
- `sources_by_status`
- `tracked_entities_by_type`
- `review_queue_by_status`
- `source_latest_discovery`

---

## Section 9 — Broader End-User Use Cases

### 9a. Public Website

| Requirement | Current Support | Gap |
|-------------|----------------|-----|
| Browse recent updates | 132 items exist, no browse UI | No web server, no API, no HTML |
| Search records | No search index | No Elasticsearch/Meili/FTS |
| Filter by topic/source/location/entity/date | Item fields support filtering, no UI | Frontend + API needed |
| Inspect source provenance | Source events & citations exist | No UI for provenance view |
| View related items | Not linked automatically | No cross-source linking |
| View maps/timelines | No geo data, no timeline model | Schema, data, and UI needed |

### 9b. Personalized Alerts

| Requirement | Current Support | Gap |
|-------------|----------------|-----|
| User selects neighborhoods | Communities registry exists | No user model, no preferences |
| User selects tracked entities | Entity registry exists | No user→entity subscription |
| User selects topics | Topic taxonomy exists | No user→topic subscription |
| User selects frequency | Cadence system exists | No per-user frequency |
| System sends matching changes | No alert engine | Pipeline, trigger, delivery needed |

### 9c. Email Reports

Fully absent. Required: HTML template engine, subscriber list, send mechanism,
digest builder that selects approved items matching user preferences.

### 9d. Social Media

Fully absent. Required: post generator, platform APIs, approval queue,
post-tracking, fact-vs-interpretation labeling.

### 9e. News Ingestion

Partially anticipated by `docs/news_ingestion_readiness.md`:
- Schema prepared for source_type `local_media` / `third_party_news`
- Raw artifact records for content hashes
- Retention policies for local media (7d raw, 180d normalized)
- Excerpt policy: store metadata + approved excerpts, not full bodies
- Open items: approved source list, near-duplicate detection, human review scope

### 9f. Knowledge Base and Analysis

Not implemented. Required: cross-item query engine, timeline builder,
entity-specific aggregator, claim comparison.

---

## Section 10 — Structure and Granularity Gaps

### Candidate Missing Structured Concepts

| Concept | Where It Lives Now | Why It Matters | Which Use Cases Require It | Feasibility |
|---------|-------------------|----------------|---------------------------|-------------|
| **Parcel/Address** | In NBOR description text | Map-based views, proximity alerts | Website, alerts, map | Deterministic regex for parcel IDs; reverse geocoding for addresses |
| **Lat/Lng Coordinates** | Not stored | Map view, proximity search, location-based alerts | Website, map, alerts | Would require geocoding step |
| **Developer/Contractor Names** | In raw text only | Track entities beyond government | Entity pages, development tracking, alerts | LLM extraction likely needed |
| **Project Phases/Milestones** | Not modeled | Timeline views, project history | Knowledge base, entity pages | LLM extraction from series of items |
| **Meeting/Docket Numbers** | BCC: `_agenda_item_number` field | Cross-reference official records | Knowledge base, legal tracking | Already partially captured |
| **Budget Amounts** | In raw text only | Financial tracking, cost alerting | Cost alerts, budget reports | Deterministic regex |
| **Decision/Vote Records** | Not modeled separately | Track how officials voted | Knowledge base, public accountability | LLM from minutes |
| **Public Comments/Testimony** | Not captured | Community engagement tracking | Website, transparency | PDF text extraction |
| **Hearing Dates** | In NBOR `date` field | Calendar views, deadline alerts | Alerts, website, email | Already partially captured |
| **Document IDs / File Numbers** | In NBOR app_id field | Cross-reference across sources | Knowledge base | Already partially captured |
| **Service Area / District** | NBOR has `district` field | Geographic filtering | Maps, filtering | Already partially captured |
| **Relationship: item is update of prior item** | `superseded_by` field exists (not used) | Timeline, change tracking | Website, entity pages | Schema exists, needs population |
| **Relationship: item confirms/corroborates another** | Not modeled | Cross-source verification | Knowledge base | LLM linking |
| **Relationship: item is response to** | Not modeled | Follow-up tracking | Alerts, entity pages | Needs schema + LLM |

---

## Section 11 — Tests and Quality Controls

### 11a. Current Test Coverage (109 tests total)

| Test File | Tests | Area | Network? |
|-----------|-------|------|----------|
| `test_nbor_parser.py` | 7 | NBOR HTML parsing, classification | No (fixture) |
| `test_bcc_parser.py` | 12 | BCC agenda PDF text parsing, action type classification | No (fixture) |
| `test_adapter.py` | 22 | FileAdapter read/write/list, PgAdapter disabled/enabled, StorageFacade | No |
| `test_parity.py` | 10 | Parity report structure, field comparison, dedupe key compare | No |
| `test_pilot_loader.py` | 11 | Pilot record selection, classification, digest, dry-run/plan modes | No |
| `test_retention.py` | 3 | Policy building, prunable artifact selection, dry-run | No |
| `test_metrics_snapshot.py` | 2 | Snapshot determinism, same-day identity stability | No |
| `test_health_export.py` | 10 | Health export dry-run, redaction, schema version, prohibited fields | No |
| `test_schemas.py` | 5 | YAML schema parse validation (4 schemas) | No |
| `test_migration_sql.py` | 7 | Migration file structure, naming, syntax, rollback pairing | No |
| `test_scripts_compile.py` | 1 | All 8 core scripts compile | No |
| `test_redaction.py` | N/A | (redaction logic tested in health_export) | — |

### 11b. Fixture Coverage

- NBOR: `nbor_raw.html` (live-captured)
- BCC: `clerk_agendas.html`, `1202026_agenda.pdf/txt`, `051926_agenda.pdf/txt`
- Utility: `utility_department.html`
- Health export: `health_export_valid.json`, `health_export_stale.json`,
  `health_export_prohibited.json`
- Adapter: `test_intel_items.yaml`, `test_sources.yaml`, `test_tracked_entities.yaml`

### 11c. Important Missing Tests

| Behavior | Risk | Priority |
|----------|------|----------|
| Dedupe index rebuild idempotency | Dedupe logic could regress | High |
| Interest filter matching correctness | Priority/alert accuracy | High |
| Escalation computation logic | Wrong urgency classification | High |
| Entity matching edge cases | Missing/mis-identified entities | High |
| Source registry schema validation | Invalid registries | Medium |
| Community/parent_area validation | Broken community hierarchy | Medium |
| Taxonomy value enforcement | Invalid classification values | Medium |
| NBOR pagination or empty page | Missing source coverage | Medium |
| BCC PDF extraction edge cases | Missing agenda items | Medium |
| YAML file write integrity | Corrupted data files | Medium |
| Retry/resilience for HTTP fetches | Failed extractions | Low (manual) |
| Cross-source item consistency | Invisible data issues | Low |

---

## Section 12 — Cross-Project Reusable Patterns

### 12a. Storage Adapter Pattern (traderie)

**Repository:** traderie
**File:** `scripts/traderie_storage_adapter.py`
**Pattern:** Abstract `TraderieStorageAdapter(ABC)` with file-backed and
(future) PG adapters. Methods: `get_segments()`, `get_items()`, etc.
**SJC learnings:** SJC already has this pattern (`scripts/adapter_base.py`,
`file_adapter.py`, `pg_adapter.py`). Traderie's method names are more
domain-specific (get_segments vs generic list_items). Consider whether SJC
should migrate to domain-specific methods.

### 12b. 3-Tier Snapshot I/O (traderie)

**Repository:** traderie
**File:** `scripts/lib/snapshot_io.py`
**Pattern:** `write_raw_snapshot()` → raw API response file,
`write_normalized_snapshot()` → normalized observations,
`append_history()` → deduplicated JSONL
**Maturity:** Live
**SJC learnings:** SJC should adopt raw→normalized→history for monitor data.
Currently only normalized intel_items are saved.

### 12c. LLM Provider Layer (bsda_courses)

**Repository:** bsda_courses
**File:** `scripts/llm_provider.py`
**Pattern:** Multi-provider client: `OpenAIClient`, `AnthropicClient`,
`OllamaClient`, `opencode-go`. Factory `make_client()` with auto-resolution.
`ChatClient` Protocol. Structured output via JSON schema.
**Maturity:** Live
**SJC learnings:** When SJC adopts LLMs, use or adapt this layer directly.
It supports 4 providers, has structured JSON output, and is proven in
multi-stage pipelines.

### 12d. LLM Run Metadata (idlehacking_kb)

**Repository:** idlehacking_kb
**File:** `scripts/llm/run_metadata.py`
**Pattern:** `RunMetadata` dataclass capturing provider, model, prompt_version,
prompt_hash, schema versions, tokens, cost, latency, run_id, tags.
**Maturity:** Draft
**SJC learnings:** Essential for SJC prompt/model provenance tracking.
SHARED-011 requires exactly this.

### 12e. LLM Fixture/Test Provider (idlehacking_kb)

**Repository:** idlehacking_kb
**File:** `scripts/llm/fixture_provider.py`
**Pattern:** Canned-response provider implementing same `ProviderInterface`.
Deterministic, no API calls.
**SJC learnings:** Critical for SJC test infrastructure when adopting LLMs.

### 12f. Claim/Entity/Source Registry Schemas (reckless_ben)

**Repository:** reckless_ben
**Files:** `docs/scaffolds/entity_register_schema.csv`,
`docs/scaffolds/claim_ledger_schema.csv`,
`docs/scaffolds/source_registry_schema.csv`
**Pattern:** Full entity, claim, and source registry schemas with cross-references.
Claim status taxonomy (5 canonical + 5 lead statuses). Source trust roles (7 types).
**Maturity:** Draft
**SJC learnings:** Directly adaptable to SJC's intel item provenance modeling.

### 12g. Public Boundary Architecture (reckless_ben)

**Repository:** reckless_ben
**File:** `docs/ops/public_site/public_boundary_architecture.md`
**Pattern:** Three build modes (internal/preview/release), route gating,
public object types, promotion manifest, publication manifest, 13+ fail gates.
**Maturity:** Draft
**SJC learnings:** Directly applicable to SJC's publish/not-publish gates.

### 12h. Source Trust Roles and Support Matrix (reckless_ben)

**Repository:** reckless_ben
**Files:** `docs/method/status_taxonomy.md`,
`docs/ops/public_site/policies/source_support_matrix.md`
**Pattern:** Every source type has CAN support / CANNOT support / required
limitation label. Source trust roles: `direct_evidence`, `party_position`,
`reporting`, `lead_generator`, etc.
**SJC learnings:** SJC's current source typing lacks trust/authority annotations.

### 12i. Calibration Stage + Staged Review Gates (idlehacking_kb)

**Repository:** idlehacking_kb
**Files:** `scripts/kb_agents/scout.py`, `AGENTS.md`
**Pattern:** Dry-run (limit 10) → review → full run. Staged review sizes:
smoke → calibration → gold → unlabeled.
**SJC learnings:** SJC should adopt this sizing for classifier calibration.

### 12j. Publication Status Lint Pipeline (bsda_courses)

**Repository:** bsda_courses
**Files:** `scripts/run_fresh_pipeline_batch.py`, `scripts/validate_claim_register.py`
**Pattern:** Stage-by-stage validation gates, claim register builder with
`publication_status` (publishable/publishable_with_caveat/hold_for_review/do_not_publish).
**SJC learnings:** Directly applicable to SJC's review → publication pipeline.

---

## Section 13 — Unresolved Decisions

### 13a. Product Decisions

1. **What is the final product name and identity?** Currently "SJC Intel" —
   not consumer-friendly. PUB-001 deferred.

2. **Who is the primary audience?** Homeowner/resident-first is stated. But
   which segment? All residents? Only homeowners? Nerdy civic-data people?

3. **What is the public-facing output format?** Website? Newsletter? Both?
   Social media? Mobile app? The current pipeline produces internal artifacts
   only. No output design exists.

4. **Publication policy:** What items are publishable automatically? What
   requires human review? What is never published? No corrections policy
   (ED-002 deferred).

5. **Monetization / sustainability:** Free? Donations? Subscription?
   Advertising? The St. Johns Citizen comparison suggests newsletter
   subscription model is viable.

### 13b. Data Model Decisions

6. **PostgreSQL cutover:** When does PostgreSQL become authoritative?
   What is the rollback plan? How long does file/dual operation continue?

7. **Relationship model:** Are link tables (intel_item_tracked_entities,
   intel_item_topics, etc.) populated from file data or only from new
   items? Are they transactional (loaded with pilot) or rebuilt?

8. **Entity model scope:** Should entities expand beyond 11 current entries?
   Should every development project, road, school, and business be tracked?
   What threshold for entity creation?

9. **Location/gis data:** Is parcel geometry needed? What coordinate system?
   Is reverse geocoding required?

10. **Topic model granularity:** Are 24 topics enough? Should topics be
    hierarchical?

### 13c. Source Policy Decisions

11. **Tier 3/4 promotion:** When to promote CDD and community/developer sources?

12. **Hermes runtime:** Build custom Hermes runtime? Use existing framework?
    Is an MVP scheduled runner sufficient?

13. **Browser automation:** Which sources require it (development tracker,
    permit status)? What browser framework? Is this authorized?

14. **St. Johns Citizen treatment:** Continue as tip-surfacing only? Or
    extract items with "media" verification status?

### 13d. LLM Decisions

15. **When to introduce LLMs:** After pipeline hardening? After VPS deploy?
    Before UI launch?

16. **Which LLM stages first:** Classification refinement? Entity extraction?
    Summarization? Newsletter generation?

17. **Provider choice:** Local (Ollama) or cloud (OpenAI/Anthropic)?
    Cost model? Privacy boundary?

18. **Structured output schema:** Pydantic? JSON schema? How is inference
    provenance tracked?

19. **Human-review requirement for LLM output:** Always? Only for certain
    stages? Configurable per stage?

### 13e. Retention Decisions

20. **Raw artifact storage:** Local MacBook only? VPS? Both? S3/R2?

21. **Archive target:** Approved archival location for long-term storage?

22. **Pruning automation:** Who authorizes the first destructive prune?

### 13f. Publication Decisions

23. **Newsletter cadence:** Weekly? Daily digest? Per-community?

24. **Social media channels:** Which platforms? Who manages accounts?

25. **Attribution policy:** How to cite sources? What credit is required?

### 13g. Personalization Decisions

26. **User accounts:** Required for alerts? How to authenticate?

27. **Preference storage:** In database? In cookies? In file?

### 13h. UI Decisions

28. **Frontend framework:** Static site generator? SPA? Server-rendered?

29. **Map provider:** Leaflet? MapLibre? Google Maps?

30. **Hosting:** VPS? GitHub Pages? Vercel/Netlify?

### 13i. Operational Decisions

31. **Scheduling:** Launchd timers? systemd? GitHub Actions cron?

32. **VPS provisioning:** When does ih-market-vps get PostgreSQL?
    What is the capacity resolution plan?

33. **Secrets management:** Password files in `~/.local/secure/`?
    Keychain? Vault?

34. **CI/CD:** GitHub Actions workflow? What is the deploy trigger?

---

## Section 14 — Recommended Discussion Order for Buddy and ChatGPT

1. **Product identity and audience** (13a: 1-3)
   — Without knowing the output, all downstream decisions are provisional.

2. **LLM introduction strategy** (13d: 15-19)
   — This is the biggest leverage point and the most transformative decision.
   Decide which stages get LLM, which stay deterministic, and the provider model.

3. **Publication policy** (13a: 4, 13f: 23-25)
   — What can be published, what must be reviewed, and how sources are credited.
   This gates the entire outward-facing pipeline.

4. **PostgreSQL cutover plan** (13b: 6-7)
   — File→PG migration timing, data loading strategy, rollback safety.
   This gates operational reliability.

5. **Source expansion strategy** (13c: 11-14)
   — Tiers 3/4, Hermes runtime, browser automation.
   This gates coverage breadth.

6. **Personalization scope** (13g: 26-27, 13e: 20-22)
   — User accounts, alerts, retention.
   This gates the resident-facing feature set.

7. **UI and hosting** (13h: 28-30, 13i: 31-34)
   — Technology stack, deployment target.
   This is implementation detail after higher-level decisions.

---

## Section 15 — Exact Follow-Up Questions

These should be answered before the next implementation plan:

**Must-answer:**
1. What is the intended public name and format for SJC Intel output?
2. Which LLM stage should be implemented first?
3. What is the threshold for an item to be published without human review?
4. When should the PostgreSQL cutover occur?
5. Should the next phase focus on: deepening coverage (more from existing
   sources), expanding coverage (Tier 3/4 sources), or building output
   (UI/newsletter)?
6. Do you want to continue the Hermes delegation model or build a scheduled
   runner?

**Should-answer:**
7. What is the budget/constraint for LLM API costs?
8. Should user accounts be planned from day one of the UI?
9. Should geographic data (parcels, coordinates) be part of the core model?
10. What is the archive strategy for raw source content?

---

## Section 16 — Chat Summary

- **What SJC does today:** File-backed local intelligence system that manually
  fetches public sources, classifies items with deterministic rules, builds a
  review queue, and stores structured YAML records. No automation, no UI, no
  LLM, no output.
- **Sources confirmed:** 28 registered canonical sources. 9 have produced items
  (50 NBOR, 44 BCC, 9 county news, 8 utility, 6 SilverLeaf discovery, 5 SJSO,
  3 each for 3 CDDs, 1 emergency). 17 sources have zero items.
- **Most important data-flow finding:** Source_events and intel_items are
  correctly separated, but source_event coverage is incomplete. Early extracts
  from county news, sheriff, and utility lack parent events.
- **Most important schema limitation:** Entities, topics, communities are stored
  as flat arrays/JSON — not relational. The PostgreSQL link tables exist but
  are empty.
- **Most important UI/product gap:** Zero resident-facing output exists.
  132 classified items are invisible to residents.
- **Strongest candidate LLM stages:** Entity extraction, relationship linking,
  newsletter generation, and near-duplicate detection. Official-record
  extraction (NBOR, BCC PDFs) should stay deterministic.
- **Most reusable pattern from another repository:** Traderie's snapshot I/O
  (raw→normalized→history 3-tier pattern) maps directly to SJC's monitor
  pipeline.
- **Report file created:** `docs/reviews/SJC_CURRENT_SYSTEM_AND_PRODUCT_EXPANSION_REVIEW_20260706.md`
- **Commit created:** `docs: add comprehensive SJC Intel system review report`
- **Repository status:** Clean — only the new report file is untracked plus
  pre-existing session docs. No data files, scripts, schemas, or registries
  were modified.
