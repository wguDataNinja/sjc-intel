# Tracked Entities — Design

> Design proposal for ENT-001..004. Defines schema, relationships, lifecycle,
> and implementation boundaries before any code is written.

---

## 1. Motivation

The Silverleaf discovery session (2026-07-04) proved we regularly find
durable things worth watching over time — developments, businesses, road
projects, schools — but have no formal way to track them. Currently these
get dumped into `interest_filters.yaml` as keywords (which over time will
make that file bloated and conflate two concerns: keyword matching vs
entity lifecycle).

A `tracked_entity` is a named thing with:
- A current status (proposed → approved → under_construction → complete)
- Known search queries that surface updates
- A list of intel items mentioning it
- Related communities, sources, and external URLs

---

## 2. Relationships

```
interest_filter (keyword rules)
       │
       │ drives (entity names → keywords)
       ▼
tracked_entity ←── has_many ──→ intel_item (via tracked_entity_ids[])
       │
       │ belongs_to (optional)
       ▼
community (for geographic entities)
source    (if entity has a dedicated source, e.g. CDD website)
```

### Entity ↔ Intel Item

- An intel_item mentions zero or more tracked_entities.
- A tracked_entity is mentioned by zero or more intel_items.
- Linkage: `intel_item.tracked_entity_ids: ["ENT-PUBLIX-SILVERLEAF"]`
- This is a soft link (intel items reference entities by ID; entities don't
  store reverse links in YAML but can be derived via grep).

### Entity ↔ Interest Filter

- Interest filters remain keyword-based match rules for the review queue.
- Tracked entities are the authoritative record for what we're watching.
- Interest filters should be **auto-generated** from tracked_entities where
  practical, rather than duplicated. Each entity contributes its name and
  aliases as interest_filter keywords.
- Until auto-generation exists, maintain by convention: when adding an
  entity, add its name/aliases to the relevant interest_filter.

### Entity ↔ Community

- An entity may belong to a community (e.g., SilverLeaf Publix → silverleaf).
- Not all entities are geographic (e.g., "Phase III Water Shortage" is a
  topic, not a community-bound entity).

### Entity ↔ Source

- An entity may have a dedicated source (e.g., Tolomato CDD → mytcdd.com).
- Most entities don't; they're found via generic sources.

---

## 3. Schema (`schemas/tracked_entity.schema.yaml`)

```yaml
# tracked_entity.schema.yaml (proposed)

entity_id:           # Required. `ENT-{type}-{descriptive-slug}`
  type: string
  pattern: "^ENT-[A-Z0-9]+-[a-z0-9-]+$"
  example: "ENT-RETAIL-PUBLIX-SILVERLEAF"

entity_type:         # Required. Controlled vocabulary (see §4)
  type: string
  allowed:
    - retail_development
    - education_facility
    - recreational_attraction
    - transportation_project
    - healthcare_facility
    - mixed_use_development
    - hospitality
    - residential_development
    - road_project
    - infrastructure_project
    - cdd
    - community
    - business
    - other

label:               # Required. Human-readable name
  type: string
  example: "SilverLeaf Mega Publix"

description:         # Optional. What this entity is
  type: string
  example: "55,701 sq ft Publix at 1975 SilverLeaf Parkway with Pours lounge"

lifecycle_status:    # Required. See §5
  type: string
  allowed:
    - proposed         # Announced but not yet approved
    - approved         # Permitted/approved by county
    - under_construction
    - completed        # Open/operational
    - dormant          # No activity for 6+ months
    - cancelled        # No longer happening
    - tracked          # Ongoing monitoring; no fixed lifecycle (e.g. CDD)

priority:            # Required. How important to track
  type: string
  allowed: [critical, high, medium, low]
  example: "high"

communities:         # Optional. Related community IDs
  type: array<string>
  example: ["silverleaf"]

aliases:             # Optional. Alternative names/search terms
  type: array<string>
  example: ["Publix at SilverLeaf", "1975 SilverLeaf Parkway Publix"]

sources:             # Optional. Source URLs where this entity is discussed
  type: array<object>
  fields:
    url: string
    label: string
    source_id: string   # If a registered source, reference it
  example:
    - url: "https://sjcitizen.com/heres-your-first-look-at-silverleafs-new-55000-sq-ft-mega-publix/"
      label: "Grand opening article"
      source_id: "st_johns_citizen"

search_queries:      # Optional. Queries that find this entity
  type: array<string>
  example:
    - '"SilverLeaf" Publix'
    - '"1975 SilverLeaf Parkway"'
    - '"SilverLeaf" grocery'

last_checked:        # Optional. ISO 8601 timestamp of last search
  type: string
  example: "2026-07-04"
  nullable: true

tracked_since:       # Required. When tracking began
  type: string
  example: "2026-07-04"

notes:               # Optional. Free text
  type: string
```

---

## 4. Entity Types (Controlled Vocabulary)

| Type | When to Use | Example |
|------|-------------|---------|
| `retail_development` | Grocery, restaurant, shopping center | SilverLeaf Publix, Harris Teeter |
| `education_facility` | Schools, educational facilities | SilverLeaf K-8 school |
| `recreational_attraction` | Parks, mini golf, sports facilities | Beach Valley Mini Golf |
| `transportation_project` | Roads, highways, interchanges | CR 2209 highway connector |
| `healthcare_facility` | Hospitals, clinics, urgent care | Ascension St. Vincent's Nocatee |
| `mixed_use_development` | Multi-purpose commercial/residential | Marketplace at Nocatee |
| `hospitality` | Hotels, resorts | Fairfield Inn & Suites CR 210 |
| `residential_development` | New home communities, apartment complexes | Water Lily, SilverLeaf phases |
| `road_project` | Specific road closures, widenings | CR 210 widening |
| `infrastructure_project` | Utilities, water/sewer, broadband | Phase III Water Shortage |
| `cdd` | Community Development District | Tolomato CDD, Trout Creek CDD |
| `community` | Master-planned community (broader watch) | SilverLeaf, Nocatee |
| `business` | Standalone business or chain | Shores Fine Wine & Spirits |
| `other` | Anything that doesn't fit above | |

---

## 5. Lifecycle Statuses

```
proposed ──→ approved ──→ under_construction ──→ completed
   │            │                                      │
   └──→ cancelled                                     │
                                                       │
                                          dormant (6+ mo no activity)
                                                       │
                                                   archived
```

Non-project entities (CDDs, communities) use:
```
tracked ──→ dormant ──→ archived
```

### Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| `proposed` | Announced but not yet permitted | Check monthly for approval news |
| `approved` | Permitted/approved by county | Check quarterly for groundbreaking |
| `under_construction` | Active construction | Check monthly for completion updates |
| `completed` | Open/operational | Check once more for follow-up, then archive |
| `dormant` | No activity for 6+ months | Stop active searches; keep in registry |
| `cancelled` | No longer happening | Mark and archive |
| `tracked` | Ongoing monitoring; no end state | Check per community cadence (CDDs = weekly) |

---

## 6. ID Convention

```
ENT-{TYPE_PREFIX}-{DESCRIPTIVE-SLUG}
```

| Type | Prefix | Example ID |
|------|--------|------------|
| retail_development | `RETAIL` | `ENT-RETAIL-PUBLIX-SILVERLEAF` |
| education_facility | `EDU` | `ENT-EDU-SILVERLEAF-K8` |
| recreational_attraction | `REC` | `ENT-REC-BEACH-VALLEY-MINI-GOLF` |
| transportation_project | `TRANS` | `ENT-TRANS-CR-2209-CONNECTOR` |
| healthcare_facility | `HEALTH` | `ENT-HEALTH-ASCENSION-NOCATEE` |
| mixed_use_development | `MIXED` | `ENT-MIXED-MARKETPLACE-NOCATEE` |
| hospitality | `HOSP` | `ENT-HOSP-FAIRFIELD-CR210` |
| road_project | `ROAD` | `ENT-ROAD-CR-210-WIDENING` |
| cdd | `CDD` | `ENT-CDD-TOLOMATO` |
| community | `COMM` | `ENT-COMM-SILVERLEAF` |
| business | `BIZ` | `ENT-BIZ-SHORES-WINE-NOCATEE` |
| infrastructure_project | `INFRA` | `ENT-INFRA-PHASE-III-WATER` |
| other | `OTHER` | `ENT-OTHER-MISC-NAME` |

Why not date-based: Entities are durable across sessions. A date in the ID
adds no value and makes it harder to reference.

---

## 7. File Location

`registry/tracked_entities.yaml`

Top-level structure:

```yaml
# =============================================================================
# SJC_Intel — Tracked Entities Registry
# =============================================================================
# Durable things watched over time. Each entity has a lifecycle status,
# search queries, and linked intel items.
#
# Schema version: 1.0
# Status: active
# Last updated: {date}
# =============================================================================

tracked_entities:
  - entity_id: "ENT-RETAIL-PUBLIX-SILVERLEAF"
    entity_type: "retail_development"
    label: "SilverLeaf Mega Publix"
    ...
```

---

## 8. Interaction with Interest Filters

Current (as of 2026-07-04): interest_filters.yaml contains entity names as
keywords. This is a maintenance burden because entity names appear in two
places.

**Proposed future state:** The build_review_queue.py script loads both
registries. Interest filters remain for rule-based matching (emergency
keywords, topic patterns). Tracked entities contribute their aliases and
names as an additional match layer. The `matched_filters` field in the
review queue would expand to include `matched_entities`.

This is deferred to ENT-002 or later. For ENT-001, the convention is:
- Entity registry is the source of truth for what we track.
- When adding an entity, also add its keywords to the relevant
  interest_filter in `registry/interest_filters.yaml` as a manual step.

---

## 9. ENT-001 Implementation Scope

| What | In scope for ENT-001? | Detail |
|------|-----------------------|--------|
| Create `registry/tracked_entities.yaml` | ✅ Yes | Schema v1.0, seeded with Silverleaf entities |
| Create `schemas/tracked_entity.schema.yaml` | ✅ Yes | Field-level spec |
| Seat with ~8 entities | ✅ Yes | Publix, K-8 school, Beach Valley Mini Golf, CR 2209, Harris Teeter, Ascension St. Vincent's, Fairfield Inn, Nocatee retail center |
| Update `docs/data_model.md` | ✅ Yes | Add entity to object table, relationship map, ID table |
| Update `README_INTERNAL.md` | ✅ Yes | Add entity count to Review Pipeline table |
| Auto-generate interest filters from entities | ❌ No | ENT-002 scope |
| Update `scripts/build_review_queue.py` | ❌ No | ENT-002 scope (entity matching in queue builder) |
| Create `prompts/hermes_entity_search_task.md` | ❌ No | ENT-002 scope |
| Write `docs/tracked_entities.md` | ❌ No | ENT-004 scope |

---

## 10. Deferred Items (ENT-002..004)

- **ENT-002**: Hermes entity search task prompt + auto-generation of
  interest filter keywords from tracked entities + review queue entity
  matching.
- **ENT-003**: Populate additional entities from Silverleaf discoveries
  beyond the initial seed (~6 more: Shores Wine, BODYBAR Pilates, Taco
  Bell CR 210, Beachwalk lagoon dining, Nothing Putt Fun & Games, the
  two new Harris Teeter locations).
- **ENT-004**: `docs/tracked_entities.md` — stakeholder onboarding
  workflow ("Buddy finds interesting thing → add to tracking → pipeline
  discovers updates").

---

## 11. Seed Entities (for ENT-001)

| # | Entity | Type | Status | Priority |
|---|--------|------|--------|----------|
| 1 | SilverLeaf Mega Publix | retail_development | completed | high |
| 2 | SilverLeaf K-8 School | education_facility | under_construction | high |
| 3 | Beach Valley Mini Golf | recreational_attraction | proposed | medium |
| 4 | CR 2209 Connector (IGP ↔ SilverLeaf Pkwy) | road_project | completed | high |
| 5 | Harris Teeter — SilverLeaf | retail_development | proposed | medium |
| 6 | Ascension St. Vincent's — Nocatee | healthcare_facility | proposed | high |
| 7 | Fairfield Inn & Suites — CR 210 | hospitality | proposed | medium |
| 8 | Nocatee Crosswater Retail Center | mixed_use_development | under_construction | medium |

---

## 12. Modeling Risks

1. **Entity proliferation** — Every news article mentions a named thing.
   Not every named thing needs an entity record. Rule of thumb: only create
   an entity when you expect multiple intel items across multiple sessions.
   One-off mentions do not need entities.

2. **ID stability** — Entity IDs are descriptive slugs. If a project is
   renamed (e.g., "Beach Valley Mini Golf" changes name), the entity ID
   stays the same; the `label` and `aliases` update. Use the original
   slug unless the entity fundamentally changes.

3. **Interest filter overlap** — Entities and interest filters both match
   against item text. Until auto-generation exists, the two registries
   can drift. Mitigation: the ENT-001 convention manual step ("add entity
   keywords to interest filter").

4. **Stale statuses** — Entity lifecycle statuses will go stale without
   active checking. The cadence system should add entity status checks
   as a monthly task. Deferred to ENT-002.
