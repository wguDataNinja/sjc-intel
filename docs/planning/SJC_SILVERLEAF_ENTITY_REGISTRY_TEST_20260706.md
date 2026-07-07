# SilverLeaf Entity Registry — Storage Model Test

**Date:** 2026-07-06
**Purpose:** Test the proposed storage model against 26 newly researched
SilverLeaf entity names. Confirm that the recommended registries can represent
neighborhoods, commercial centers, medical facilities, and provisional unnamed
entities with correct verification status, types, and relationships.

---

## Recommended Storage Architecture (Two Registries)

### 1. `registry/communities.yaml` — Geographic areas

For: master-planned communities, neighborhoods, corridors, municipalities.
Already exists. Has `type: neighborhood` and `parent_area` support.
**New neighborhoods go here** — not in tracked_entities.

### 2. `registry/tracked_entities.yaml` — Durable monitored things

For: developments, schools, roads, businesses, medical facilities, shopping
centers, projects. Already exists with 11 entities.
**New commercial/institutional entities go here.**

### 3. `registry/silverleaf_geo.yaml` — (Future)

For geometry (polygons, coordinates), street segments, entrances, monitored
road segments. Proposed but not yet created. Not tested here.

### 4. `registry/search_profiles.yaml` — (Future)

For search templates keyed to entity IDs. Proposed but not yet created.
Tested conceptually below.

---

## Part 1 — Neighborhoods (in `registry/communities.yaml`)

### Verified from SilverLeaf Official Resident Directory

These 11 neighborhoods are confirmed by SilverLeaf's official resident
directory. They go in `registry/communities.yaml` with:

| Field | Value |
|-------|-------|
| `type` | `neighborhood` |
| `parent_area` | `silverleaf` |
| `status` | `active` (directory-confirmed) |

**Complete example record:**

```yaml
- id: "silverleaf_village"
  name: "SilverLeaf Village"
  type: "neighborhood"
  parent_area: "silverleaf"
  notes: >
    Neighborhood within SilverLeaf master-planned community. Confirmed by
    official SilverLeaf resident directory. Not to be confused with
    Silverleaf Commons (shopping center) or Silverleaf Market
    (Publix-anchored shopping center).
  status: "active"
```

**Full list of neighborhood IDs to add:**

```yaml
- id: "sl_brandon_lakes"       # Brandon Lakes
- id: "sl_brook_forest"        # Brook Forest
- id: "sl_elm_creek"           # Elm Creek
- id: "sl_holly_forest"        # Holly Forest
- id: "sl_johns_island"        # Johns Island
- id: "sl_newbrook"            # Newbrook
- id: "sl_silver_falls"        # Silver Falls
- id: "sl_silver_landing"      # Silver Landing
- id: "sl_silver_meadows"      # Silver Meadows
- id: "sl_silverleaf_village"  # SilverLeaf Village
- id: "sl_waterford_lakes"     # Waterford Lakes
```

All share: `type: neighborhood`, `parent_area: silverleaf`, `status: active`.

These 11 replace the stale single-entry `cherry_elm` that currently exists
(which was listed as "includes neighborhoods like Cherry Elm, Cherrywood,
and Silverleaf Village" — the directory now provides authoritative names).

**Existing `cherry_elm` entry:** Keep it. It was mentioned by a resident as
an area of specific interest. Its status is `active`. Confirm it appears in
the official directory or mark it as a historical/builder name.

### Builder-Confirmed (Parent/Peer Classification)

These 4 names are builder-confirmed but may have a different status:

```yaml
- id: "sl_courtney_chase"
  name: "Courtney Chase"
  type: "neighborhood"
  parent_area: "silverleaf"
  notes: >
    Builder-confirmed name. May be a sub-phase or collection rather than
    a standalone neighborhood. Parent/peer relationship to SilverLeaf
    master development requires verification against official plats.
  status: "observed"   # NOT "active" — builder-confirmed but not
                       # yet verified as a distinct neighborhood
                       # vs. a lot-size collection

- id: "sl_courtney_grove"
  name: "Courtney Grove"
  type: "neighborhood"
  parent_area: "silverleaf"
  notes: Same pattern as Courtney Chase.
  status: "observed"

- id: "sl_courtney_oaks"
  name: "Courtney Oaks"
  type: "neighborhood"
  parent_area: "silverleaf"
  notes: Same pattern as Courtney Chase.
  status: "observed"

- id: "sl_hidden_creek"
  name: "Hidden Creek"
  type: "neighborhood"
  parent_area: "silverleaf"
  notes: Builder-confirmed name. Verify against official plats.
  status: "observed"
```

**Important:** `status: observed` means "identified but not yet verified."
This is distinct from `active` (confirmed and in use). If future plat
verification shows these are product-line names rather than neighborhoods,
they get downgraded or removed — but the YAML entry preserves the evidence
trail.

### What NOT to Add

The user explicitly stated: "Do not treat builder lot-size collections or
product lines as neighborhoods." The Courtney* names may turn out to be
product lines. The `status: observed` and `evidence_notes` fields preserve
this uncertainty. If confirmed as product lines, these entries are removed
or marked as `stale`.

---

## Part 2 — Commercial and Institutional Entities (in `registry/tracked_entities.yaml`)

### Silverleaf Commons (Shopping Center)

```yaml
- entity_id: "ENT-RETAIL-SILVERLEAF-COMMONS"
  entity_type: "retail_development"
  label: "Silverleaf Commons"
  description: >
    Shopping center inside or directly associated with SilverLeaf.
    Known tenant: Jersey Mike's Subs. Distinguish from Silverleaf Market
    (Publix-anchored center) and SilverLeaf Village (neighborhood).
  lifecycle_status: "tracked"      # operating center, not a project lifecycle
  priority: "medium"
  communities:
    - silverleaf
  aliases:
    - "Silverleaf Commons shopping center"
  search_queries:
    - '"Silverleaf Commons" St. Johns'
    - '"Jersey Mikes" Silverleaf'
  sources:
    - url: ""
      label: ""
      source_id: ""
    # No source URLs yet — sourced from SilverLeaf resident directory
  evidence_notes: >
    Confirmed by SilverLeaf official resident directory. Tenant (Jersey
    Mike's Subs) listed. No separate news article or county permit record
    independently verified at this time.
  last_checked: "2026-07-06"
  tracked_since: "2026-07-06"
  notes: >
    Note spelling: "Silverleaf Commons" (lowercase 'l' in 'leaf').
    This is the registered name. Do not confuse with "SilverLeaf
    Village" (residential neighborhood) or "Silverleaf Market"
    (separate shopping center).
```

### Silverleaf Market (Publix-anchored Shopping Center)

```yaml
- entity_id: "ENT-RETAIL-SILVERLEAF-MARKET"
  entity_type: "retail_development"
  label: "Silverleaf Market"
  description: >
    Publix-anchored shopping center in SilverLeaf. Distinct from
    Silverleaf Commons. The Publix at 1975 SilverLeaf Parkway may be
    the anchor tenant of this center. Relationship to
    ENT-RETAIL-PUBLIX-SILVERLEAF needs verification.
  lifecycle_status: "tracked"
  priority: "medium"
  communities:
    - silverleaf
  aliases:
    - "Silverleaf Market shopping center"
    - "SilverLeaf Publix shopping center"     # provisional
  search_queries:
    - '"Silverleaf Market" St. Johns'
  sources:
    - url: ""
      label: ""
      source_id: ""
  evidence_notes: >
    Listed in SilverLeaf official resident directory. Relationship to
    ENT-RETAIL-PUBLIX-SILVERLEAF (the individual Publix store) not
    yet established — the Publix may be in this center or may be a
    standalone store.
  last_checked: "2026-07-06"
  tracked_since: "2026-07-06"
  notes: >
    Note spelling: "Silverleaf Market" (lowercase 'l'). The existing
    entity ENT-RETAIL-PUBLIX-SILVERLEAF may be the anchor tenant of
    this center, or may be separate. Verify center boundaries.
```

### Baptist SilverLeaf Medical Campus

```yaml
- entity_id: "ENT-HEALTH-BAPTIST-SILVERLEAF"
  entity_type: "healthcare_facility"
  label: "Baptist SilverLeaf Medical Campus"
  description: >
    Medical campus in SilverLeaf. Not a full-service hospital unless
    evidence supports that classification. Baptist Health is a major
    regional healthcare system.
  lifecycle_status: "tracked"
  priority: "medium"
  communities:
    - silverleaf
  aliases:
    - "Baptist Health SilverLeaf"
    - "Baptist Medical Campus SilverLeaf"
  search_queries:
    - '"Baptist" SilverLeaf medical'
    - '"Baptist Health" SilverLeaf'
  sources:
    - url: ""
      label: ""
      source_id: ""
  evidence_notes: >
    Listed in SilverLeaf official resident directory as "Baptist
    SilverLeaf Medical Campus." Classified as medical campus, not
    hospital, unless evidence supports hospital-level services.
  last_checked: "2026-07-06"
  tracked_since: "2026-07-06"
```

### Shoppes of St. Johns Parkway (Adjacent)

```yaml
- entity_id: "ENT-RETAIL-SHOPS-ST-JOHNS-PKWY"
  entity_type: "retail_development"
  label: "Shoppes of St. Johns Parkway"
  description: >
    Shopping center adjacent to SilverLeaf near St. Johns Parkway and
    CR 210. Not inside SilverLeaf — use adjacent/direct-impact
    relationship rather than inside_silverleaf classification.
  lifecycle_status: "tracked"
  priority: "low"
  communities:
    - cr_210_corridor
  aliases:
    - "Shoppes of St. Johns Parkway SilverLeaf"
  search_queries:
    - '"Shoppes of St. Johns Parkway" SilverLeaf'
  sources:
    - url: ""
      label: ""
      source_id: ""
  evidence_notes: >
    Listed in SilverLeaf official resident directory. Adjacent to
    SilverLeaf — affects SilverLeaf residents as nearby shopping
    destination. Not inside the SilverLeaf boundary.
  last_checked: "2026-07-06"
  tracked_since: "2026-07-06"
```

### CR 16A / SilverLeaf Parkway Grocery Center (Provisional)

```yaml
- entity_id: "ENT-RETAIL-CR16A-SL-PKWY-GROCERY"
  entity_type: "retail_development"
  label: "CR 16A and SilverLeaf Parkway Grocery Center"
  description: >
    Grocery-anchored shopping center at or near the intersection of
    CR 16A and SilverLeaf Parkway. Formal center name not yet verified.
    Possible Harris Teeter anchor remains unconfirmed. Use provisional
    descriptive identity until formal name is established — do not
    name after "Harris Teeter."
  lifecycle_status: "proposed"
  priority: "low"
  communities:
    - silverleaf
  aliases: []
  search_queries:
    - '"CR 16A" SilverLeaf grocery'
    - '"SilverLeaf Parkway" grocery center'
  sources:
    - url: ""
      label: ""
      source_id: ""
  evidence_notes: >
    Provisional identity. Formal center name not yet known. Harris
    Teeter as possible anchor is unconfirmed. Existing entity
    ENT-RETAIL-HARRIS-TEETER-SILVERLEAF may be related but this is
    not yet established. Update when formal name or confirmed anchor
    tenant is verified.
  last_checked: "2026-07-06"
  tracked_since: "2026-07-06"
  notes: >
    IMPORTANT: Do not rename this to "Harris Teeter" or assume the
    grocery center name. The Harris Teeter entity exists separately
    as ENT-RETAIL-HARRIS-TEETER-SILVERLEAF. They may be the same
    project, different projects, or related-but-not-identical. Keep
    separate until evidence resolves the relationship.
```

---

## Part 3 — Critical Disambiguation

Three entities with similar names that must remain separate:

| Name | Type | Registry | Entity ID |
|------|------|----------|-----------|
| SilverLeaf Village | Residential neighborhood | `communities.yaml` | `sl_silverleaf_village` |
| Silverleaf Commons | Shopping center | `tracked_entities.yaml` | `ENT-RETAIL-SILVERLEAF-COMMONS` |
| Silverleaf Market | Publix-anchored shopping center | `tracked_entities.yaml` | `ENT-RETAIL-SILVERLEAF-MARKET` |

Deduplication rule: Any future intel item mentioning "SilverLeaf Village"
should link to the neighborhood entity, not either shopping center. Any
mention of "Silverleaf Commons" should link to the Commons. The aliases
and `evidence_notes` fields document the distinction.

---

## Part 4 — Alias and Capitalization Handling

SilverLeaf entities use inconsistent capitalization in source data:

| Source Spelling | Canonical Name | Registry |
|----------------|---------------|----------|
| "SilverLeaf" (camelCase) | SilverLeaf | `communities.yaml` master entry |
| "Silverleaf Commons" (lowercase l) | Silverleaf Commons | `tracked_entities.yaml` |
| "Silverleaf Market" (lowercase l) | Silverleaf Market | `tracked_entities.yaml` |
| "SilverLeaf Village" (camelCase) | SilverLeaf Village | `communities.yaml` |

The canonical name in the registry preserves the official spelling from the
source. Search aliases include alternate capitalizations for fuzzy matching.
The entity_id always uses uppercase slug convention (`SILVERLEAF`).

---

## Part 5 — Provenance and Verification Fields

Every entry in both registries uses these standard fields for evidence:

| Field | Purpose | Required? |
|-------|---------|-----------|
| `evidence_notes` | Quality and basis of evidence | Always |
| `sources[].url` | Source URL | When available |
| `sources[].label` | Short source description | When available |
| `sources[].source_id` | Registry source reference | When available |
| `last_checked` | Last verification date | Always |
| `tracked_since` | When tracking began | Always |
| `notes` | Open questions, risks, caveats | When needed |
| `status` | Verification level | Always in communitites.yaml |
| `lifecycle_status` | Lifecycle stage | Always in tracked_entities.yaml |

For neighborhoods, the `status` field (`active` vs `observed`) is the primary
verification signal. `active` = confirmed by authoritative source (official
directory). `observed` = identified but not fully verified (builder-confirmed
but may be a product line).

---

## Part 6 — Relationship Records

Relationships between entities are stored as text notes and cross-references
in both registries, not as a separate relationship table:

```yaml
# In tracked_entity.yaml, within an entity record:
notes: >
  May be the anchor tenant of ENT-RETAIL-SILVERLEAF-MARKET. Verify
  center boundaries.
  Adjacent to: ENT-RETAIL-SHOPS-ST-JOHNS-PKWY (nearby but outside boundary).
  Distinct from: ENT-RETAIL-SILVERLEAF-COMMONS (separate center).
```

For stronger relationship typing, add a `relationships` field to the
entity schema (future addition, not in current schema):

```yaml
relationships:
  - type: "located_in"         # inside_silverleaf, adjacent_to, serves
    target_id: "sl_silverleaf_village"
  - type: "distinct_from"
    target_id: "ENT-RETAIL-SILVERLEAF-COMMONS"
```

---

## Part 7 — Search Profile References

Search profiles reference entities by `entity_id`, not by duplicating names
and aliases:

```yaml
# In registry/search_profiles.yaml (future):
- profile_id: "sl_retail_commons"
  entity_id: "ENT-RETAIL-SILVERLEAF-COMMONS"
  cadence: monthly
  sources:
    - domain: "sjcitizen.com"
      search_terms: ["Silverleaf Commons"]
    - domain: "sjcfl.us"
      path: "/news/"
      search_terms: ["Silverleaf Commons"]
  date_window_days: 90
  match_rules:
    exact: ["Silverleaf Commons", "Silverleaf Commons shopping"]
    # No probable/related for single-tenant center
```

The search profile does NOT repeat the canonical name, aliases, or
description — those live in the entity record. The profile only adds
search-specific configuration (cadence, date windows, match rules).

When search discovery runs, it loads the entity registry for names/aliases
and the search profile registry for cadence/windows/rules.

---

## Summary

| Entity Type | Count | Registry | New Type Needed? |
|------------|-------|----------|-----------------|
| Residential neighborhoods (directory-confirmed) | 11 | `communities.yaml` | No — `neighborhood` type exists |
| Builder-confirmed (may be product lines) | 4 | `communities.yaml` | No — `status: observed` handles uncertainty |
| Shopping centers | 2 | `tracked_entities.yaml` | No — `retail_development` type exists |
| Medical campus | 1 | `tracked_entities.yaml` | No — `healthcare_facility` type exists |
| Adjacent shopping center | 1 | `tracked_entities.yaml` | No — `retail_development` with relationship notes |
| Provisional unnamed center | 1 | `tracked_entities.yaml` | No — `proposed` lifecycle with provisional ID |
| Cherry Elm (existing) | 1 | `communities.yaml` | Keep — resident-sourced, may overlap with directory names |

**No new types or registries needed.** The existing `communities.yaml` and
`tracked_entities.yaml` can represent all 20 new entities. The proposed
`silverleaf_geo.yaml` and `search_profiles.yaml` are separate future files
for geometry and search configuration, not entity storage.
