# SilverLeaf Geographic Registry

**Status:** Active evidence-and-scope contract; not a boundary dataset.
**Owner:** Buddy owns changes to public-product scope. The file registry is
authoritative for the current editorial decision; official planning records are
the authority for their own legal/planning claims.
**Primary registry:** `registry/silverleaf_scope.yaml`.
**Last reviewed:** 2026-08-08.

## Purpose

This contract answers a narrower question than a GIS system: *when does a
public record have a defensible SilverLeaf resident connection?* It provides
repeatable scope review while preserving the distinction between legal planning
areas, editorial relevance, and future machine geometry.

It does not determine property ownership, school assignment, road access,
zoning entitlement, or precise point-in-polygon containment.

## Three layers that must not be collapsed

| Layer | What it means | Current authority | What it may support | What it must not support |
|---|---|---|---|---|
| Legal/planning geography | County DRI/PUD areas and individual planning records. | County Planning & Zoning documents in `geographic_authority.sources`. | Identifying an explicitly named Silverleaf planning application; high-level orientation. | A public-product boundary or automatic item inclusion. |
| Editorial resident scope | The community, verified neighborhoods, access roads, nearby corridors, tracked entities, and countywide-material rules defined in the registry. | `registry/silverleaf_scope.yaml` plus policy approval. | `in_silverleaf`, `near_silverleaf`, or `countywide_impact` reasoning. | Claims that a location is legally within a PUD/DRI. |
| Machine geometry (future) | Versioned polygons, road segments, entrances, parcels, and school zones. | A separately reviewed official GIS/plats dataset. | Point-in-polygon and proximity calculations after validation. | Any current selection or publication decision. |

## Authoritative evidence currently registered

The registry records three public county documents. They establish planning
context and orientation, but no geometry is loaded from them.

| ID | Authority | What it supports | Limitation |
|---|---|---|---|
| `SJC-DRIMOD-2024-01` | [County Planning & Zoning DRI agenda item](https://www.sjcfl.us/wp-content/uploads/2024/09/6.-drimod-2024-01-silverleaf-dri.pdf) | Silverleaf DRI identity, approximately 8,884-acre planning context, and high-level northwest-county orientation. | Map/narrative evidence only; not a versioned GIS boundary in this repository. |
| `SJC-MAJMOD-2024-04` | [County Planning & Zoning PUD agenda item](https://www.sjcfl.us/wp-content/uploads/2024/09/7.-majmod-2024-04-silverleaf-pud.pdf) | Silverleaf PUD identity and master-development-plan context. | Not a complete or current parcel-by-parcel entitlement record. |
| `SJC-COMP-PLAN-2050-LAND-USE` | [County 2050 Comprehensive Plan—Land Use](https://www.sjcfl.us/wp-content/uploads/2026/06/A-Land-Use-2050.pdf) | Parcel 40 constraints and edge/access exclusions, including no SilverLeaf connection to Hardwood Landing Road or Collier Road. | Does not provide a public-product boundary or attendance-zone assignment. |

These URLs are evidence references, not new canonical monitoring sources.
They do not authorize an automated planning-document monitor.

## Current editorial scope procedure

When reviewing an item, apply the first matching grounded connection and
record the evidence; do not use vague county proximity.

1. **Direct — `in_silverleaf`:** The record names a registered SilverLeaf
   neighborhood, direct-serving road, school, development, business, or
   service. Cite the matching registry record.
2. **Nearby — `near_silverleaf`:** The record affects a named adjacent
   corridor or registered adjacent entity. State the route/entity connection;
   "nearby" alone is not an explanation.
3. **Countywide material — `countywide_impact`:** The record has a concrete
   household impact such as county utility service continuity, water
   restrictions, emergency preparedness, or a decision demonstrably changing
   SilverLeaf conditions. Generic civic news does not qualify.
4. **No grounded connection:** retain it outside the SilverLeaf public corpus,
   or create a bounded proposal for new evidence. Do not stretch the DRI/PUD
   map to manufacture relevance.

The policy classifier and any human publication decision remain the final
gates. Scope relevance never changes an item from `pending_review` to
`verified`, nor does it authorize public release.

## Initial verified anchors and known limitations

The scope registry already contains verified community aliases, 11
directory-backed neighborhoods, direct-serving roads, adjacent corridors,
tracked entities, inclusion/exclusion rules, and a `needs_review` list. Its
strongest remaining limits are intentional:

- no official machine-readable SilverLeaf boundary or parcel geometry;
- no reviewed internal-street/entrance segment list;
- no official school attendance-zone relationship for all SilverLeaf addresses;
- no exact I-95/I-295 commute segments;
- no automatic conclusion that the full DRI or PUD equals the resident product
  footprint.

The high-level DRI description may help a reviewer find the right planning
record, but cannot prove that an address or project lies inside SilverLeaf.

## Geometry acquisition gate

Do not add coordinates or a polygon to `silverleaf_scope.yaml`. First create a
separate, versioned geometry registry only after all of the following are
available and reviewed:

1. A public official GIS feature service, recorded plat geometry, or
   county-approved boundary dataset—not a builder map or a hand-drawn shape.
2. Publisher, direct URL/service endpoint, layer name, version/date, CRS,
   license/public-access status, and acquisition date.
3. A written statement of what the shape represents (DRI, PUD, phase, plat,
   neighborhood, road centerline, entrance, etc.) and what it excludes.
4. A human comparison against the county planning documents and known
   neighborhood/entity records.
5. Tests for geometry validity, source provenance, version pinning, and safe
   fallback when a location is absent or uncertain.

Until then, use the evidence-only scope model. A missing geometry produces an
"unresolved geographic relevance" review outcome, never an inferred inclusion.

## Next bounded follow-ups

| Backlog item | Deliverable needed | Explicit boundary |
|---|---|---|
| `DIR-009` | Official plats or county GIS references for internal streets, private/public status, and entrances. | Do not scrape a builder map into a road network. |
| `DIR-010` | School-year-specific SJCSD attendance-zone authority for each claimed serving-school relationship. | Do not infer a zone from proximity or a school name. |
| `DIR-011` | Named access and commute segments with endpoints, direction, and source authority. | Do not monitor whole I-95/I-295 corridors by keyword alone. |
| `DIR-007` | A geometry/proximity design that consumes only the separately versioned future geometry registry. | Do not add PostGIS or point containment before authoritative shapes exist. |

## Validation

Run from the repository root:

```bash
python3 scripts/validate_silverleaf_scope.py
python3 -m pytest tests/test_silverleaf_scope.py -v
```

The validator checks the official evidence IDs/URLs, source links, the
evidence-only/no-geometry contract, existing cross-references, provenance, and
stable relevance identifiers. It validates internal consistency; it does not
replace a human review of the linked county documents.
