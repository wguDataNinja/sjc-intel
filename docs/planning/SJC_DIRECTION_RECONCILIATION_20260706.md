# SJC Intel — Direction Reconciliation

**Date:** 2026-07-06
**Purpose:** Reconcile the newly accepted SilverLeaf product and three-lane
architecture against the existing VPS roadmap, PostgreSQL schema, architecture
docs, and session logs.

---

## 1. Current-State Summary

The repository has three active planning layers:

| Layer | Document | Status |
|-------|----------|--------|
| Product direction | `docs/planning/SJC_PRODUCT_AND_SOURCING_DIRECTION_20260706.md` | Just created, accepted |
| VPS/infrastructure | `VPS_ROADMAP.md` (2026-07-04) | Pre-dates product direction |
| Database schema | 11 migrations (20260705_001 through 20260706_011) | Applied, empty, file authority |

The product direction introduces three changes that the VPS roadmap and schema
do not anticipate:

1. **SilverLeaf geographic registry** as a foundational dependency
2. **Three-lane architecture** (durable knowledge + live incident + agentic investigation)
3. **Coordinate-based geographic filtering** with PostGIS as preferred target

---

## 2. Conflict and Reconciliation Table

### 2.1 VPS Roadmap Target End State

| Planning Doc Says | VPS Roadmap Says | Conflict | Resolution |
|---|---|---|---|
| Three-lane architecture (knowledge + incident + investigation) | "SJC Intel runs deterministic source checks on the VPS" — single lane | VPS roadmap describes only the durable knowledge lane. Incident and investigation lanes are absent. | VPS roadmap target end state remains valid for the durable knowledge lane. Add a note: incident and investigation lanes follow in a later phase after the geographic registry and live-source feasibility are resolved. No change to VPS workflow classification. |
| Live incident lane needs transient storage | VPS design tables: `sources`, `source_events`, `intel_items`, `tracked_entities`, etc. — no incident table | Existing schema has no room for transient incident records. | Incidents are a new table family, not an extension of intel_items. They belong in a separate `incidents` schema or as a distinct table set in `app` with very different retention rules. |
| Agentic investigation lane needs LLM infrastructure | VPS roadmap workflow classification has no category for LLM-driven searches | Agentic investigation requires search APIs, LLM calls, and review gates not in the VPS timeline. | Defer to Phase 4 (after durable lane is on VPS and incident lane is proven locally). |

### 2.2 PostgreSQL Schema

| Planning Doc Says | Schema Says | Conflict | Resolution |
|---|---|---|---|
| SilverLeaf geographic registry (boundaries, streets, neighborhoods, points) | No spatial tables. Communities stored as `text[]` on intel_items. `registry/communities.yaml` has 20 flat entries. | The geographic registry needs geometry types (polygon, linestring, point), spatial indexes, and coordinate lookup — none of which exist. | Geographic registry data initially lives in a new YAML registry file (`registry/silverleaf_geo.yaml`) with hand-curated coordinates and boundaries. PostGIS migration deferred until the registry is complete and VPS migration is ready. |
| Coordinate-based filtering (point-in-polygon, corridor proximity) | No PostGIS extension. No `geometry` columns. No spatial indexes. | Point-in-polygon without PostGIS requires either PostGIS or application-side computation (shapely). | Defer PostGIS to when the geographic registry is populated and VPS database is active. Use shapely or manual geography in the interim for local development. |
| Live incidents: coordinates, severity, road, direction, mile marker, start/end timestamps | `app.intel_items` has `geographic_scope` (enum), `communities[]` (text), `map_url` (text), `district` (text) — none suitable for incident coordinates | Incidents are structurally different from intel items. They need lat/lng, not community name. They need timestamps, not review status. | New `incidents` table family. Separate from `intel_items`. See schema boundary section below. |
| Durable knowledge lane continues using existing schema | Existing `app.intel_items` table (40+ columns) | Compatible — no change needed. The durable lane is the existing pipeline. | Keep. File authority remains. |

### 2.3 Architecture Docs

| Planning Doc Says | Discovery Loops Doc Says | Conflict | Resolution |
|---|---|---|---|
| Three-lane architecture | Six discovery loops (A–F): known-source monitoring, search discovery, backfill, emerging-source, editorial review, taxonomy | Three-lane model is orthogonal to the six loops. They are different decompositions: lanes = data flow, loops = process triggers. | No conflict. Update discovery_loops.md to note the three-lane data flow as the underlying pipeline model. The loops continue as trigger/process definitions for each lane. |
| Live incident lane: crashes, closures, flooding | Loop A (known-source monitoring) covers registered sources only. No loop for real-time transient sources. | Live incident sources are not registered sources in the traditional sense. They publish ephemeral records, not durable articles. | Add a new discovery loop G (Live Incident Monitoring) to discovery_loops.md. |
| Agentic investigation: targeted searches triggered by gaps or events | Loop B (search discovery) covers proactive new-source finding. Loop A covers known-source polling. | Agentic investigation is event-triggered, not cadence-triggered. It starts from a known entity, event, or gap, not from a schedule. | Agentic investigation is a new loop type — event-triggered rather than cadence-triggered. Add to discovery_loops.md as a new operational pattern. |

### 2.4 Existing Entity and Community Registries

| Planning Doc Says | Registry Says | Conflict | Resolution |
|---|---|---|---|
| SilverLeaf geographic registry with boundary, neighborhoods, streets, schools, roads | `registry/communities.yaml` lists SilverLeaf as one entry with `type: master_planned_community` and `parent_area: northwest_st_johns`. No boundary, no streets, no neighborhoods. | The community entry is too shallow for the geographic registry's purpose. | The geographic registry is a new, expanded data set. It does not replace the community entry — it extends it. Keep `registry/communities.yaml` for the controlled vocabulary. Create `registry/silverleaf_geo.yaml` for the detailed geography. |
| 10+ schools serving SilverLeaf, athletic programs, attendance zones | `registry/tracked_entities.yaml` has one education entity: `ENT-EDU-SILVERLEAF-K8` | School coverage in entities is minimal. The planning doc envisions a much wider school scope. | Expand tracked_entities for schools in a later pass. For now the geographic registry captures school locations and service relationships. |

---

## 3. Recommended Schema Boundaries

### 3.1 What Incidents Are (and Are Not)

Incidents are NOT intel items. They differ on every important dimension:

| Dimension | Intel Item | Incident |
|-----------|-----------|----------|
| Lifetime | Months to years (durable) | Hours to days (transient) |
| Primary key | `SJC-{source}-{date}-{NNNN}` | `INC-{FHP|FL511}-{date}-{id}` |
| Coordinates | Optional, text-based | Required, lat/lng |
| Status | Review status (pending→verified→rejected) | Incident status (active→clearing→reopened→cleared) |
| Source | Government document or news article | Live official feed (FHP, FL511, county) |
| Processing | Deterministic classify → review → publish | Deterministic capture → relevance filter → optional agentic enrichment |
| Retention | Unbounded normalized, bounded raw | Strict: retain 7-30 days normalized, expire raw immediately |
| Alert trigger | Human review gate | Automatic (in SilverLeaf boundary or on monitored route) |
| Update model | New intel item supersedes old | Status transitions on same incident record |
| Queue | Editorial review queue | Live incident feed (no editorial queue for basic incidents) |

### 3.2 Recommended Incident Tables (Future Migration)

```sql
-- Schema: app (or new incidents schema)
CREATE TABLE app.incidents (
    incident_id       text PRIMARY KEY,         -- INC-FHP-20260706-001
    external_id       text,                     -- upstream ID from FHP/FL511
    source_id         text NOT NULL REFERENCES app.sources(source_id),
    incident_type     text NOT NULL,            -- crash, disabled_vehicle, closure, flooding, etc.
    status            text NOT NULL DEFAULT 'active',
                                                  -- active, clearing, reopened, cleared, stale
    road              text,
    direction         text,                     -- NB, SB, EB, WB, both
    mile_marker       numeric(6,2),
    intersection      text,
    location_text     text,
    latitude          numeric(10,7),
    longitude         numeric(10,7),
    severity          text,                     -- minor, moderate, major, unknown
    lanes_affected    integer,
    description       text,
    started_at        timestamptz NOT NULL,
    ended_at          timestamptz,
    last_confirmed_at timestamptz,
    discovered_at     timestamptz NOT NULL,
    source_url        text,
    raw_payload       jsonb,
    created_at        timestamptz NOT NULL DEFAULT now(),
    updated_at        timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_incidents_status ON app.incidents(status);
CREATE INDEX idx_incidents_road_date ON app.incidents(road, started_at DESC);
CREATE INDEX idx_incidents_active ON app.incidents(status) WHERE status = 'active';
CREATE INDEX idx_incidents_coords ON app.incidents(latitude, longitude) WHERE latitude IS NOT NULL;
```

### 3.3 Recommended Observation Records

Camera observations are separate from incidents — they are evidence, not facts:

```sql
CREATE TABLE app.incident_observations (
    observation_id    text PRIMARY KEY,
    incident_id       text REFERENCES app.incidents(incident_id),
    observation_type  text NOT NULL,            -- traffic_camera, social_post, news_report, officer_report
    observed_at       timestamptz NOT NULL,
    source            text,                     -- camera_id, URL, agency
    visible_conditions jsonb,                   -- {congestion: heavy, emergency_vehicles: true, blocked_lanes: 1}
    raw_url           text,
    content_hash      text,
    confidence        text DEFAULT 'medium',
    limitations       text[],                   -- ["partial field of view", "no official classification"]
    created_at        timestamptz NOT NULL DEFAULT now()
);
```

### 3.4 How Durable Knowledge and Incidents Relate

```
Incident detected (FHP/FL511)
  → Geographic filter (in/affects SilverLeaf?)
  → If yes: live incident feed, optional alert
  → If unusual/interesting: agentic investigation triggered
      → Search for news articles, social posts
      → If found: create intel item (enters durable knowledge lane)
      → If not found: search_outcome = no_exact_match_found
  → Incident expires after 7-30 days (retention policy)
  → If intel item exists, it persists (durable)
  → Link: incident_id ↔ intel_item_id (optional, for evidence)
```

The key insight: **an incident can produce an intel item, but an intel item
does not require an incident.** A rezoning hearing is not an incident; a
crashed vehicle on I-95 is not a rezoning hearing. They belong in separate
tables with an optional link.

### 3.5 PostGIS Decision

**Defer PostGIS to VPS rollout.** For local development:

- The geographic registry starts as a YAML file (`registry/silverleaf_geo.yaml`)
  with manually curated coordinates and boundaries.
- Point-in-polygon checks can use `shapely` (pure Python, no DB required).
- Corridor proximity can use `haversine` distance in application code.
- PostgreSQL geometry columns are added in a single migration when PostGIS
  is installed on the VPS database. Until then, coordinates stay in
  `numeric(10,7)` columns and the application does geometry in Python.

**Do not add PostGIS as a dependency now.** The schema_fit doc already
recommends keeping coordinates as numeric columns initially, with PostGIS
deferred. The planning document's "PostGIS is the preferred database support"
is a long-term target, not an immediate blocker.

### 3.6 Geographic Registry Format (Immediate)

The geographic registry is a new YAML file, not a database migration:

```yaml
# registry/silverleaf_geo.yaml (proposed structure)
schema_version: "1.0"
last_updated: "2026-07-06"

boundary:
  type: polygon
  coordinates: []  # lat/lng pairs
  source: "TBD — county GIS or official planning exhibit"
  source_date: null
  confidence: draft

neighborhoods:
  - name: "Cherry Elm"
    aliases: []
    parent_development: "SilverLeaf"
    builder: null
    status: built
    entrances:
      - road: "SilverLeaf Parkway"
        at: null
    geometry: null  # polygon coordinates
    hoa_cdd: null

streets:
  - name: "SilverLeaf Parkway"
    aliases: []
    type: arterial
    start_intersection: null
    end_intersection: null
    neighborhoods_served: []
    geometry: null  # linestring coordinates

schools:
  - name: "Magnolia Oaks Academy"
    type: private
    address: null
    lat_lng: null
    serves_silverleaf: true
    attendance_zone_effective: null

roads_monitored:
  - segment_id: "I-95-NB-IGP-I295"
    road: "I-95"
    direction: NB
    start_anchor: "International Golf Parkway"
    end_anchor: "I-295"
    relevance: primary_commute
```

This file is new, separate from `registry/communities.yaml` and
`registry/tracked_entities.yaml`. It holds geometry and spatial relationships
that the other registries do not.

---

## 4. Concrete Migration Sequence

### 4.1 Updated VPS Roadmap Sequence

| Step | Original (VPS_ROADMAP.md) | Adjusted | Rationale |
|------|--------------------------|----------|-----------|
| SJC-VPS-001 | Current-state verification | Keep — covers existing pipeline | No change |
| SJC-VPS-002 | GitHub readiness docs | Keep | No change |
| SJC-VPS-003 | Schema design package | Keep — existing app schema | Add note: geographic registry YAML runs in parallel, not a dependency |
| SJC-VPS-004 | Collector contract wrappers | Keep — durable lane only | Incident lane wrappers follow later |
| SJC-VPS-005 | Local parity rehearsal | Keep | No change |
| SJC-VPS-006 | Service/timer definitions | Keep — durable lane only | Incident and investigation services are future |
| SJC-VPS-007 | Backup/restore plan | Keep | No change |
| SJC-VPS-008 | VPS shadow deployment | Keep — durable lane only | Incident lane may skip VPS entirely (transient, local ok) |
| SJC-VPS-009 | Enable approved timers | Keep — durable lane only | No change |
| SJC-VPS-010 | Dashboard and Hermes | Keep | Add SilverLeaf filter scope to health export |

**New VPS items added:**

| Step | Title | Lane | Priority | Prerequisites |
|------|-------|------|----------|---------------|
| SJC-VPS-011 | Deferred: PostGIS research and test migration | Geographic | Medium | SJC-VPS-003, silverleaf_geo.yaml populated |
| SJC-VPS-012 | Deferred: Live incident source feasibility | Incident | High* | None (can run in parallel with VPS-001) |
| SJC-VPS-013 | Deferred: Agentic investigation framework design | Investigation | Low | Incident lane proven locally |

*High priority for investigation, but NOT a VPS blocker. FHP/FL511 feasibility
can be done locally.

### 4.2 Geographic Registry Sequence (Parallel Track)

Not in VPS roadmap — this is a local data-compilation task:

1. Create `registry/silverleaf_geo.yaml` with boundary (draft from OSM/county GIS)
2. Populate verified neighborhoods (start with Cherry Elm, add as verified)
3. Add internal streets (from plats, OSM, county GIS)
4. Add schools serving SilverLeaf (research attendance zones)
5. Add monitored road segments (I-95, I-295 defined sections)
6. Add exclusion rules (what is NOT SilverLeaf)
7. Add relevance relationships
8. Update evidence for each entry (source, date, confidence)
9. Create shapely-based verification script (point-in-polygon, corridor proximity)

### 4.3 Live Incident Schema Sequence (Local Track)

1. Investigate FHP incident page data source (DIR-003)
2. Investigate FL511 incident/camera integration (DIR-004)
3. Design incidents table (adapter first, YAML storage, no PG migration yet)
4. Build FHP adapter (deterministic, no LLM)
5. Build geographic relevance filter (using shapely + silverleaf_geo.yaml)
6. Design observation records (for cameras)
7. Design incident/intel-item link (optional, for durable records)

### 4.4 Existing Backlog Updates Already Applied

From the previous session: BACKLOG.md now has DIR-001 through DIR-015 tracking
all actionable items derived from the planning session. No additional changes
needed to the backlog.

---

## 5. Unresolved Decisions Blocking Implementation

| # | Decision | Blocking | Options | Needs |
|---|----------|----------|---------|-------|
| 1 | SilverLeaf boundary source | Geographic registry population | County GIS / official planning exhibit / OSM + manual curation | Buddy: which source to start with? |
| 2 | FHP data source mechanism | Live incident adapter | Structured JSON endpoint / HTML parse / browser automation | Focused investigation session |
| 3 | FL511 camera integration method | Camera observation records | Embedded map tool / HLS stream / undocumented API — only first option is clearly permitted | FL511 terms review |
| 4 | Incident retention period | Incident table design | 7 days / 30 days / depends on type | Buddy decision |
| 5 | PostGIS vs shapely for initial development | Geographic filtering implementation | PostGIS requires DB and extension; shapely is pure Python | Defer: use shapely for local, PostGIS for VPS |
| 6 | Incidents schema: `app` or new `incidents` schema | Migration design | `app.incidents` (simpler, fewer grants) vs new schema (cleaner separation) | Minor — choose `app.incidents` initially |
| 7 | Should incidents enter the review queue? | Review queue design | No (auto-filtered by geography) / Yes (only unusual ones) / Yes (all, but separate queue) | Buddy: automatic for basic incidents, review queue for unusual ones? |
| 8 | School expansion scope: which programs count? | School search portfolio | All athletics and activities / only major sports / only notable achievements (state qualification, championships) | Buddy: what is the resident threshold? |
| 9 | Agentic investigation: which LLM provider first? | Investigation lane design | opencode-go (current default) / Ollama local / OpenAI API | Budge: cost and privacy preference |

---

## 6. Document Updates

### 6.1 VPS_ROADMAP.md

Already has cross-reference to the planning document (added in previous session).
Need to add a lane-separation note and the deferred incident/investigation items.

### 6.2 README_INTERNAL.md

Already updated in previous session. Current Phase, Open Loops, and Durable
Decisions all reference the new direction. No additional changes needed.

### 6.3 discovery_loops.md

Needs a new Loop G (Live Incident Monitoring) and a note that the six existing
loops primarily serve the durable knowledge lane. Not modifying in this session
to keep changes scoped.

### 6.4 docs/postgresql_adapter.md

No change needed. The adapter manages the durable knowledge lane. Incident and
investigation lanes will need their own adapter patterns when implemented, but
that is future work.

### 6.5 news_ingestion_readiness.md

No change needed. The agentic investigation lane overlaps with news ingestion,
but both are future work. The existing document's boundaries remain valid:
no autonomous news agent, no paywall bypass, no full-body archive.

### 6.6 VPS_ROADMAP.md Update

Add a lane context section and note about deferred items.

<｜｜DSML｜｜parameter name="editFile" value="true" />
