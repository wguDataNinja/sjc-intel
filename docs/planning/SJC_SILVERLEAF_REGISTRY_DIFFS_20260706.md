# SilverLeaf Registry — Proposed Implementation Diffs

**Date:** 2026-07-06
**Status:** Implementation recommendation. Do not apply until Buddy approves.

---

## Schema Notes

- `communities.yaml` has no `.schema.yaml` file — schema is implicit from
  existing entries. All proposed fields (`id`, `name`, `type`, `parent_area`,
  `notes`, `status`) are present in current entries.
- `tracked_entities.yaml` is governed by `schemas/tracked_entity.schema.yaml`.
  All proposed fields exist in the schema. No schema expansion needed.
- The `sources[].url` field is used only when a source URL exists. Entries
  sourced from the resident directory have no URL and use `evidence_notes`
  alone.

---

## Part 1 — `registry/communities.yaml`

### 1a. SilverLeaf Neighborhood Section

Replace the note in the SilverLeaf master entry to reference the new
neighborhood section instead of hardcoding "Cherry Elm, Cherrywood, and
Silverleaf Village".

**Change to `silverleaf` entry (line 49):**

```
Current: Includes neighborhoods like Cherry Elm, Cherrywood, and Silverleaf Village.
Proposed: See Neighborhoods section below for the complete list.
```

### 1b. New Neighborhood Entries (insert after section header)

Add this section after the `cherry_elm` entry, before any next section:

```yaml
  # ---------------------------------------------------------------------------
  # SilverLeaf Neighborhoods
  # ---------------------------------------------------------------------------
  # Verified from SilverLeaf official resident directory (2026-07).
  # All are type: neighborhood, parent_area: silverleaf.
  # Status "active" = confirmed by official directory.
  # Status "observed" = builder-confirmed, awaiting plat verification.

  - id: "sl_brandon_lakes"
    name: "Brandon Lakes"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_brook_forest"
    name: "Brook Forest"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_elm_creek"
    name: "Elm Creek"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_holly_forest"
    name: "Holly Forest"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_johns_island"
    name: "Johns Island"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_newbrook"
    name: "Newbrook"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_silver_falls"
    name: "Silver Falls"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_silver_landing"
    name: "Silver Landing"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_silver_meadows"
    name: "Silver Meadows"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"

  - id: "sl_silverleaf_village"
    name: "SilverLeaf Village"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Residential neighborhood within SilverLeaf master-planned
      community. Verified from SilverLeaf official resident directory.
      IMPORTANT: Not to be confused with Silverleaf Commons (shopping
      center) or Silverleaf Market (Publix-anchored shopping center).
      Those are commercial entities in tracked_entities.yaml.
    status: "active"

  - id: "sl_waterford_lakes"
    name: "Waterford Lakes"
    type: "neighborhood"
    parent_area: "silverleaf"
    notes: >
      Neighborhood within SilverLeaf master-planned community.
      Verified from SilverLeaf official resident directory.
    status: "active"
```

### 1c. Builder-Confirmed (Blocked)

The four Courtney* names and Hidden Creek are **not ready to add**. They are
builder-confirmed but may be lot-size collections rather than neighborhoods.
Add only when plat verification confirms they are distinct neighborhoods.

**Current recommendation: Do NOT add yet.** Document them in the planning doc
only. When plats are verified, add with `status: "observed"` (not `"active"`)
and notes indicating the evidence source.

### 1d. Cherry Elm — No Change

Keep existing `cherry_elm` entry. It was sourced from a resident mentioning
it as an area of specific interest. It may overlap with one of the 11
directory-conformed names (e.g., "Cherry Elm" may be an earlier name for a
sub-area now listed under a different directory name). No evidence to merge
or remove it.

### 1e. Count Summary

| Action | Count | Ready? |
|--------|-------|--------|
| Add SilverLeaf neighborhoods (directory-confirmed) | 11 | ✅ Ready now |
| Update SilverLeaf master entry notes line | 1 | ✅ Ready now |
| Add Courtneys (builder-confirmed, plat needed) | 4 | ❌ Blocked — await plat verification |
| Keep Cherry Elm as-is | 1 | ✅ No change needed |

---

## Part 2 — `registry/tracked_entities.yaml`

### 2a. Silverleaf Commons

```yaml
  - entity_id: "ENT-RETAIL-SILVERLEAF-COMMONS"
    entity_type: "retail_development"
    label: "Silverleaf Commons"
    description: >
      Shopping center inside or directly associated with SilverLeaf.
      Known tenant: Jersey Mike's Subs. This is an ordinary tenant,
      not an identity-defining anchor — listed for context only.
    lifecycle_status: "tracked"
    priority: "medium"
    communities:
      - silverleaf
    aliases:
      - "Silverleaf Commons shopping center"
    search_queries:
      - '"Silverleaf Commons" St. Johns'
    sources: []
    evidence_notes: >
      Listed in SilverLeaf official resident directory. Tenant (Jersey
      Mike's Subs) is an ordinary tenant, not an anchor. No separate
      news article or county permit record independently verified.
      Note spelling: "Silverleaf" (lowercase 'l') is the registered name.
    last_checked: "2026-07-06"
    tracked_since: "2026-07-06"
    notes: >
      Distinguish from Silverleaf Market (separate Publix-anchored
      center) and SilverLeaf Village (residential neighborhood in
      communities.yaml). "Silverleaf Commons" uses lowercase 'l'.
```

**Schema check:** All fields exist in `tracked_entity.schema.yaml`.
`lifecycle_status: "tracked"` is allowed (non-project value). `sources: []`
is valid — empty array, no URLs. `evidence_notes` serves the verification
documentation role when no source URL is available.

### 2b. Silverleaf Market (Publix-Anchored)

```yaml
  - entity_id: "ENT-RETAIL-SILVERLEAF-MARKET"
    entity_type: "retail_development"
    label: "Silverleaf Market"
    description: >
      Publix-anchored shopping center in SilverLeaf. Publix is the
      identity-defining anchor tenant. May be the center containing
      the Publix at 1975 SilverLeaf Parkway
      (ENT-RETAIL-PUBLIX-SILVERLEAF) — relationship to be verified.
    lifecycle_status: "tracked"
    priority: "medium"
    communities:
      - silverleaf
    aliases:
      - "Silverleaf Market shopping center"
    search_queries:
      - '"Silverleaf Market" St. Johns'
    sources: []
    evidence_notes: >
      Listed in SilverLeaf official resident directory. Publix anchor
      status noted from directory. Relationship to
      ENT-RETAIL-PUBLIX-SILVERLEAF not yet established — the Publix
      store may be in this center or may be a standalone store. Verify
      center boundaries and whether 1975 SilverLeaf Parkway is within
      this center.
    last_checked: "2026-07-06"
    tracked_since: "2026-07-06"
    notes: >
      Note spelling: "Silverleaf Market" (lowercase 'l'). Publix anchor
      is identity-defining and documented in description. Distinguish
      from Silverleaf Commons (separate center, different tenant mix).
```

**Anchor-tenant rule applied:** Publix is the identity-defining anchor of
this center, so it is mentioned in the description. This is not the same
as creating a separate tenant entity — Jersey Mike's at Silverleaf Commons
is an ordinary tenant and only gets a mention in `notes`, not the
description.

### 2c. Baptist SilverLeaf Medical Campus

```yaml
  - entity_id: "ENT-HEALTH-BAPTIST-SILVERLEAF"
    entity_type: "healthcare_facility"
    label: "Baptist SilverLeaf Medical Campus"
    description: >
      Medical campus in SilverLeaf operated by Baptist Health, a major
      regional healthcare system. Classified as medical campus, not
      full-service hospital, unless evidence supports hospital-level
      services (emergency department, inpatient beds, surgical suites).
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
    sources: []
    evidence_notes: >
      Listed in SilverLeaf official resident directory as "Baptist
      SilverLeaf Medical Campus." The entity_type "healthcare_facility"
      is used rather than "hospital" because no evidence supports
      hospital-level services. If emergency department or inpatient
      capacity is confirmed, reclassify. Baptist Health operates
      multiple facilities in the region including Baptist Medical Center
      Jacksonville (downtown) and Baptist Medical Center South.
    last_checked: "2026-07-06"
    tracked_since: "2026-07-06"
    notes: >
      Do not reclassify to "hospital" without evidence of emergency
      department, inpatient beds, or surgical services. The term
      "Medical Campus" in the name does not imply hospital status.
```

### 2d. Shoppes of St. Johns Parkway (Adjacent)

```yaml
  - entity_id: "ENT-RETAIL-SHOPS-ST-JOHNS-PKWY"
    entity_type: "retail_development"
    label: "Shoppes of St. Johns Parkway"
    description: >
      Shopping center adjacent to SilverLeaf near St. Johns Parkway
      and CR 210. Affects SilverLeaf residents as nearby shopping
      destination but is NOT inside the SilverLeaf boundary.
    lifecycle_status: "tracked"
    priority: "low"
    communities:
      - cr_210_corridor        # NOT silverleaf — it's adjacent, not inside
    aliases:
      - "Shoppes of St. Johns Parkway SilverLeaf"
    search_queries:
      - '"Shoppes of St. Johns Parkway" SilverLeaf'
    sources: []
    evidence_notes: >
      Listed in SilverLeaf official resident directory as an adjacent
      commercial area. Relationship type: adjacent/direct-impact,
      not inside_silverleaf. May have tenants of interest to SilverLeaf
      residents.
    last_checked: "2026-07-06"
    tracked_since: "2026-07-06"
    notes: >
      Uses communities: cr_210_corridor, not silverleaf. This preserves
      the adjacent relationship rather than implying the center is
      inside SilverLeaf. The SilverLeaf resident directory listing it
      confirms direct-impact relevance.
```

### 2e. CR 16A / SilverLeaf Parkway Grocery Center (Provisional)

```yaml
  - entity_id: "ENT-RETAIL-CR16A-SL-PKWY-GROCERY"
    entity_type: "retail_development"
    label: "CR 16A and SilverLeaf Parkway Grocery Center"
    description: >
      Grocery-anchored shopping center at or near the intersection of
      CR 16A and SilverLeaf Parkway. Formal center name not yet
      verified. Provisional descriptive identity — do not treat as
      confirmed name. Possible Harris Teeter anchor remains UNCONFIRMED.
    lifecycle_status: "proposed"
    priority: "low"
    communities:
      - silverleaf
    aliases: []
    search_queries:
      - '"CR 16A" SilverLeaf grocery'
      - '"SilverLeaf Parkway" grocery center'
    sources: []
    evidence_notes: >
      Provisional identity. Formal center name not yet known. Harris
      Teeter as possible anchor is unconfirmed — do not reference
      ENT-RETAIL-HARRIS-TEETER-SILVERLEAF in this record's description
      until evidence establishes the relationship. The existing Harris
      Teeter entity may describe the same project, a different project,
      or a related-but-not-identical development. Keep separate until
      evidence resolves the relationship.
    last_checked: "2026-07-06"
    tracked_since: "2026-07-06"
    notes: >
      CRITICAL: Do NOT rename this to "Harris Teeter" or assume the
      grocery center name. The label is a deliberate provisional
      descriptive ID. If the formal center name is later confirmed,
      add it as an alias and update the label. If Harris Teeter is
      confirmed as anchor, add that to the description. If they are
      the same project, merge with ENT-RETAIL-HARRIS-TEETER-SILVERLEAF.
```

**Anchor-tenant rule applied:** Harris Teeter is explicitly kept
unconfirmed. The description and evidence_notes both state the uncertainty.
No reference to ENT-RETAIL-HARRIS-TEETER-SILVERLEAF is made in the
description — only in `notes` as a caveat.

### 2f. Existing Entity Updates (Minor)

**ENT-RETAIL-PUBLIX-SILVERLEAF** (line 25): No change needed. The Publix
entity stands independently. If future evidence confirms it is the anchor
tenant of Silverleaf Market, add a note referencing ENT-RETAIL-SILVERLEAF-MARKET.

**ENT-RETAIL-HARRIS-TEETER-SILVERLEAF** (line 56): No change needed. The
existing entity correctly has `lifecycle_status: "proposed"` and
`evidence_notes` stating no permit found. The new provisional center
entity is deliberately kept separate.

### 2g. Count Summary

| Action | Count | Ready? |
|--------|-------|--------|
| Add Silverleaf Commons | 1 | ✅ Ready now |
| Add Silverleaf Market (Publix-anchored) | 1 | ✅ Ready now |
| Add Baptist SilverLeaf Medical Campus | 1 | ✅ Ready now |
| Add Shoppes of St. Johns Parkway (adjacent) | 1 | ✅ Ready now |
| Add CR 16A/Pkwy Grocery Center (provisional) | 1 | ✅ Ready now (provisional ID) |
| Update existing entities | 0 | ❌ No change needed |

**All 5 commercial entities are ready to add now.** The provisional entity
is explicitly labeled as provisional in its `label` and `notes`. Future
evidence may merge it with the existing Harris Teeter entity or rename it.

---

## Part 3 — Validation Implications

### communities.yaml

- All 11 new entries use `type: "neighborhood"` — already in the
  `community_types` list.
- All use `parent_area: "silverleaf"` — existing master-planned community.
- All use `status: "active"` — consistent with verified sources.
- No new community types needed.

### tracked_entities.yaml

- All 5 new entries use `entity_type` values already in the schema:
  `retail_development`, `healthcare_facility`.
- All use `lifecycle_status` values in the schema: `tracked`, `proposed`.
- `sources: []` is valid YAML. The schema marks `sources` as optional
  (`required: false`).
- No new entity types needed.

### No Schema Changes Required

| Proposed field | In current schema? |
|---------------|-------------------|
| `entity_id` | ✅ Required |
| `entity_type` | ✅ Required, values exist |
| `label` | ✅ Required |
| `description` | ✅ Optional |
| `lifecycle_status` | ✅ Required, values exist |
| `priority` | ✅ Required |
| `communities` | ✅ Optional array |
| `aliases` | ✅ Optional array |
| `search_queries` | ✅ Optional array |
| `sources` | ✅ Optional array of objects |
| `evidence_notes` | ✅ Optional (free text) |
| `last_checked` | ✅ Optional |
| `tracked_since` | ✅ Required |
| `notes` | ✅ Optional (free text) |

---

## Part 4 — Ready vs Blocked Summary

| Entity | Registry | Ready Now? | Condition |
|--------|----------|-----------|-----------|
| Brandon Lakes | communities.yaml | ✅ Yes | Directory-confirmed |
| Brook Forest | communities.yaml | ✅ Yes | Directory-confirmed |
| Elm Creek | communities.yaml | ✅ Yes | Directory-confirmed |
| Holly Forest | communities.yaml | ✅ Yes | Directory-confirmed |
| Johns Island | communities.yaml | ✅ Yes | Directory-confirmed |
| Newbrook | communities.yaml | ✅ Yes | Directory-confirmed |
| Silver Falls | communities.yaml | ✅ Yes | Directory-confirmed |
| Silver Landing | communities.yaml | ✅ Yes | Directory-confirmed |
| Silver Meadows | communities.yaml | ✅ Yes | Directory-confirmed |
| SilverLeaf Village | communities.yaml | ✅ Yes | Directory-confirmed |
| Waterford Lakes | communities.yaml | ✅ Yes | Directory-confirmed |
| SilverLeaf master notes fix | communities.yaml | ✅ Yes | Trivial edit |
| Silverleaf Commons | tracked_entities.yaml | ✅ Yes | Directory + ordinary tenants |
| Silverleaf Market | tracked_entities.yaml | ✅ Yes | Directory + Publix anchor |
| Baptist SilverLeaf Medical Campus | tracked_entities.yaml | ✅ Yes | Directory, healthcare_facility |
| Shoppes of St. Johns Parkway | tracked_entities.yaml | ✅ Yes | Directory, adjacent relationship |
| CR 16A/Pkwy Grocery Center | tracked_entities.yaml | ✅ Yes | Provisional ID, explicit uncertainty |
| Courtney Chase | communities.yaml | ❌ Blocked | Await plat verification |
| Courtney Grove | communities.yaml | ❌ Blocked | Await plat verification |
| Courtney Oaks | communities.yaml | ❌ Blocked | Await plat verification |
| Hidden Creek | communities.yaml | ❌ Blocked | Await plat verification |

**16 entries ready to add now. 4 entries blocked pending stronger evidence.**
