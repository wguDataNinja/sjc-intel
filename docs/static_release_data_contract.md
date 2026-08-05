# Static Release Data Contract

**Status:** Accepted for v0 implementation (SilverLeaf Brief).
**Authority:** `docs/publication_release_contract.md` §4–§5; the v0 UI
specification (`docs/public_ui_v0_spec.md`) is authoritative for product/UI
behavior and links here.
**Owner:** Buddy for publication decisions; implementation follows an approved
task packet.
**Last reconciled:** 2026-08-04 (Task 17).

This contract defines the exact static artifacts the SilverLeaf Brief site
consumes. It is designed so the static-export task implements it without
architectural decisions.

The export task (Task 17) implemented this contract as
`scripts/build_static_release.py` and added the v0 fields in §2A and §2B
(relevance, source-unavailable state, optional event dates, lifecycle, and a
self-describing `dimensions` block). §2A–§2B are authoritative for those
fields.

---

## 1. Artifacts

Three deterministic, versioned JSON files per release, produced on the Mac:

```
release-<release_id>/
  release.json              # release metadata + public items
  search-index.json         # normalized client-search fields only
  release-manifest.json     # input identity, generator revision, checksums,
                            # prior-release reference (rollback identity)
```

The exact directory/file naming is finalized by the export task; the *field
contract* below is authoritative now.

## 2. release.json

```json
{
  "release_id": "SJC-REL-2026-08-001",
  "schema_version": "1.0",
  "environment": "real",
  "status": "published",
  "created_at": "2026-08-04T12:00:00Z",
  "published_at": "2026-08-04T12:00:00Z",
  "reviewer": "<reviewer identity>",
  "generator_revision": "<git sha>",
  "source_corpus_input_identity": "<manifest/checksum ref>",
  "prior_release_id": "SJC-REL-2026-07-001",
  "dimensions": {
    "relevance": {
      "in_silverleaf": {"label": "In SilverLeaf"},
      "near_silverleaf": {"label": "Near SilverLeaf"},
      "countywide_impact": {"label": "Countywide impact"}
    },
    "topics": {
      "infrastructure": {"label": "Infrastructure", "description": "Roads, utilities, public works"}
    },
    "places": {
      "silverleaf": {"label": "SilverLeaf", "type": "master_planned_community"}
    },
    "entities": {
      "ENT-EDU-SILVERLEAF-K8": {"label": "SilverLeaf K-8 School", "lifecycle": "under_construction", "lifecycle_label": "Under construction"}
    },
    "sources": {
      "sjc_utility_department": {"name": "St. Johns County Utility Department", "url": "https://www.sjcfl.us/departments/utility-department/", "source_type": "official"}
    }
  },
  "items": [
    {
      "public_item_id": "SJC-UTIL-20260603-0002",
      "title": "Free Chlorine Burnout Scheduled June 1–21",
      "summary": "CR 214 WTP free chlorine burnout June 1–21; water safe.",
      "why_it_matters": "Customers may notice chlorine odor/discoloration.",
      "source_name": "St. Johns County Utility Department",
      "source_url": "https://www.sjcfl.us/departments/utility-department/",
      "source_date": "2026-05-26",
      "published_date": "2026-08-04",
      "relevance": "countywide_impact",
      "topic_ids": ["infrastructure", "environment"],
      "entity_ids": [],
      "place_ids": [],
      "sensitivity_display": "none",
      "verification_display": "Confirmed from source",
      "related_item_ids": ["SJC-CN-20260603-0005"]
    }
  ]
}
```

### 2A. Public item field contract (v0)

| Field | Type | Required | Source | Notes |
|-------|------|----------|--------|-------|
| `public_item_id` | string | yes | item `item_id` | Stable; canonical. |
| `title` | string | yes | item `title` | Editorially reviewed. |
| `summary` | string | yes | item `summary` or approved override | Plain language. |
| `why_it_matters` | string | yes | `resident_relevance.why_it_matters` or summary | Resident framing. |
| `source_name` | string | yes | registry `name` or `citation.source_name` | Human-readable. |
| `source_url` | string | yes* | item `source_url` | Direct public record. Omit when unavailable and set `source_unavailable: true`. |
| `source_unavailable` | boolean | no | derived | `true` only when no working source URL is available. UI shows "The original source link is currently unavailable." |
| `source_date` | string | yes | `source_published_at` else `discovered_at` | Display date. |
| `event_date` | string | no | approved decision/editorial | Explicit event/effective/hearing date, never substituted for `source_date`. |
| `event_date_label` | string | no | approved decision/editorial | e.g. "Hearing date", "Effective date". |
| `published_date` | string | yes | decision/release timestamp | When published in SilverLeaf Brief. |
| `relevance` | string | yes | derived from decision | One of `in_silverleaf`, `near_silverleaf`, `countywide_impact`. |
| `display_topic` | string | yes | approved decision / derived | Resident-facing v0 topic category. One of `roads_traffic`, `utilities_water`, `emergency_preparedness`, `schools_community`, `local_business`. The public interface shows ONLY this value — raw taxonomy ids never render. |
| `lifecycle` | string | no | approved decision/editorial | Render only when explicitly present. |
| `lifecycle_label` | string | no | approved decision/editorial | Human label for `lifecycle`. |
| `topic_ids` | array<string> | yes | item `topics` | Stable taxonomy IDs. |
| `entity_ids` | array<string> | no | item `tracked_entity_ids` | Stable entity IDs. |
| `place_ids` | array<string> | no | item `communities` | Stable place IDs. |
| `sensitivity_display` | string | yes | derived | `none` or `reviewed_sensitive` only. |
| `verification_display` | string | yes | derived from `verification_status` | User-facing. |
| `related_item_ids` | array<string> | no | computed | Shared topic/entity within release. |
| `release_id` | string | yes | this release | Rollback identity. |

`*` Exactly one of `source_url` or `source_unavailable: true` must be present.

### 2B. dimensions block (v0, self-describing release)

`release.json` includes a `dimensions` block so the UI is fully self-describing
and portable (no registry access at runtime). It maps every stable ID used by
release items to its public label and minimal display metadata:

- `relevance` — id → `{label}`;
- `display_topics` — v0 resident topic id → `{label, description?}` (the only
  topic layer exposed to the UI);
- `places` — place id → `{label, type?}`;
- `entities` — entity id → `{label, lifecycle?, lifecycle_label?, description?}`;
- `sources` — source id → `{name, url?, source_type?}`.

Only IDs present in the release (or referenced by its items) need entries.
Unknown/extra dimension entries are not permitted.

## 3. search-index.json

Normalized client-search fields only. One entry per item:

```json
{
  "release_id": "SJC-REL-2026-08-001",
  "schema_version": "1.0",
  "environment": "real",
  "items": [
    {
      "id": "SJC-UTIL-20260603-0002",
      "tokens": "free chlorine burnout scheduled june 1 21 cr 214 wtp water",
      "title": "free chlorine burnout scheduled june 1 21",
      "summary": "cr 214 wtp free chlorine burnout june 1 21 water safe",
      "why_it_matters": "customers may notice chlorine odor discoloration",
      "topics": ["infrastructure", "environment"],
      "places": [],
      "entities": [],
      "source": "st. johns county utility department",
      "source_date": "2026-05-26"
    }
  ]
}
```

- **Normalization:** lowercase, strip punctuation, collapse whitespace.
- No review fields, no internal notes, no raw excerpts unless approved.
- `tokens` is the concatenated normalized searchable text for lexical search.
- `topics` is the item's `display_topic` (resident-facing v0 category); raw
  taxonomy ids are never exposed to client search.

## 4. release-manifest.json

```json
{
  "manifest_version": "1.0",
  "release_id": "SJC-REL-2026-08-001",
  "environment": "real",
  "release_status": "published",
  "created_at": "2026-08-04T12:00:00Z",
  "published_at": "2026-08-04T12:00:00Z",
  "generator_revision": "<git sha>",
  "source_corpus_input_identity": "<sha256 of corpus snapshot input>",
  "item_ids": ["SJC-UTIL-20260603-0002", "..."],
  "checksums": {
    "release.json": "<sha256>",
    "search-index.json": "<sha256>"
  },
  "prior_release_id": "SJC-REL-2026-07-001",
  "rollback_reference": "SJC-REL-2026-07-001"
}
```

`environment` is `real` for approved production releases and `demo` for
nonproduction fixtures. A `demo` release is byte-isolated under
`site/data/demo/` and must never be presented as production.

## 5. Stable filter IDs

Filter dimensions use stable IDs that never change:

- **domain:** `sjc`
- **topic:** taxonomy topic IDs (see `docs/taxonomy.md`)
- **entity:** `tracked_entity_ids`
- **place/community:** community IDs (see `registry/communities.yaml`)
- **source:** `source_id`

## 6. Deterministic ordering

- Selected publication ordering: source date descending, then `item_id`
  ascending. Stable across runs. The UI renders this order and does not
  reorder it (§2.6 of the UI spec).

## 7. Validation

Before a release is eligible:

1. Corpus validator (`scripts/validate_publication_corpus.py`) passes with 0
   blocking errors.
2. Selector (`scripts/select_publication_items.py --check`) returns the
   approved, reviewed, SilverLeaf-included item set.
3. The exporter (`scripts/build_static_release.py`) projects only allowlisted
   fields; denylist check passes (see §8).
4. Content-quality validation passes for every exported item (required
   resident-facing copy, relevance/place relationship, no unexplained internal
   acronyms, conditional wording for proposals, no internal fields, stable
   public ID). Missing required copy excludes/fails the item.
5. Repeated generation is byte-stable for identical inputs (fixed timestamps).
6. Checksums in `release-manifest.json` match artifact bytes.

## 8. Public allowlist / internal denylist

- **Allowlist:** the fields in §2–§3 only.
- **Denylist (never export):** reviewer notes, reviewer identity (except
  release-level reviewer on manifest, per approved policy), `reviewed_at`,
  `_dedupe_key`, `_signal`, `_beat`, `matched_entities`,
  `entity_match_basis`, internal file paths, `raw_excerpt` (unless explicitly
  approved), secrets, credentials, `citation` internals beyond source name.
- Enforced by `scripts/publication_common.py::public_projection` +
  `validate_public_safe` and by `scripts/build_static_release.py` (exporter
  writes only the §2A field set; unknown keys are rejected).

## 9. Rollback

- Prior release artifacts are retained (release history directory).
- `release-manifest.json.prior_release_id` identifies the rollback target.
- Rollback = redeploy the prior release artifacts; no silent mutation of the
  current release.

## 10. Client-side behavior

- Cache keyed by `release_id` + checksums.
- No-results: UI empty state from `docs/public_ui_v0_spec.md` §5.
- VPS-independent: files are served from the static host; no runtime needed.

## 11. Non-goals

- No API, no database reads, no subscriptions, no live incidents, no
  PostGIS/GIS, no editing.
- The export task implements this contract only; it does not decide
  publication policy.
