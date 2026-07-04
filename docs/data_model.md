# SJC_Intel — Data Model Reference

## 1. Purpose

This document is the project's lightweight entity-relationship / data model
reference. It defines the core object types, their grain, IDs, relationships,
lifecycle fields, and known modeling risks. It is not a formal ERD — it is a
practical map for Workers, Codex reviewers, and Buddy to understand how data
flows and connects across the repo.

Schema files (`schemas/*.yaml`) are the authoritative field-level specs.
This doc links to them rather than duplicating all fields.

---

## 2. Core Object Model

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐     ┌─────────────────────┐
│    source    │────→│  source_event │────→│  intel_item  │────→│ review_queue_entry  │
│ (registry)   │     │  (data/)      │     │  (data/)     │     │ (data/review_queue/) │
└──────────────┘     └───────────────┘     └──────┬───────┘     └─────────────────────┘
                                                   │
                                                   ▼
                                           ┌───────────────┐
                                           │tracked_entity │
                                           │ (registry/)   │
                                           └───────────────┘
```

Supporting registries:
- `source_candidate` → promotes to `source`
- `interest_filter` → flags items in review queue
- `community` → controlled vocabulary for intel items
- `beat_candidate` → proposed homeowner beat

---

## 3. Object Table

| Object | Location | Grain | Primary ID | Key Relationships | Status |
|--------|----------|-------|------------|-------------------|--------|
| `source` | `registry/sources.yaml` | One monitored public source | `source_id` (e.g. `sjc_nbor_public_notices`) | Has many source_events, is referenced by intel_items | **implemented** |
| `source_candidate` | `registry/source_candidates.yaml` | One candidate source awaiting promotion | `candidate_id` (e.g. `CAND-SRC-0001`) | Promotes to source | **implemented** |
| `source_event` | `data/source_events/{date}/{source_id}.yaml` | One source occurrence (meeting, fetch, snapshot, press batch) | `event_id` (e.g. `EVT-BCC-20260120-0011`) | Belongs to source; has many intel_items | **implemented** (NBOR, BCC, utility active; partial coverage) |
| `intel_item` | `data/intel_items/{date}/{source_id}.yaml` | One extracted resident-impact finding | `item_id` (e.g. `SJC-NBOR-20260704-0001`) | Belongs to source_event; links to tracked_entity (planned); is reviewed via review_queue_entry | **implemented** |
| `review_queue_entry` | `data/review_queue/queue.yaml` | One editorial review task for one intel item | `queue_id` (e.g. `Q-SJC-NBOR-20260626-0001`) | References one intel_item | **implemented** |
| `dedupe_entry` | `data/index/prior_items.yaml` | One known intel item fingerprint | `key` (16-char hex hash) | References one intel_item | **implemented** |
| `interest_filter` | `registry/interest_filters.yaml` | One keyword-based priority rule | `id` (e.g. `utility_disruption`) | Matches intel_items via keyword scan | **implemented** |
| `community` | `registry/communities.yaml` | One geographic community/corridor/municipality | `id` (e.g. `silverleaf`) | Referenced by intel_items, sources | **implemented** |
| `beat_candidate` | `registry/beat_candidates.yaml` | One proposed homeowner beat | `beat_id` (e.g. `CAND-BEAT-0001`) | Maps to taxonomy topics + interest tags | **implemented** |
| `tracked_entity` | `registry/tracked_entities.yaml` | One durable thing watched over time | `entity_id` (e.g. `ENT-RETAIL-PUBLIX-SILVERLEAF`) | Has many intel_items (via tracked_entity_ids — not yet wired) | **implemented** |

---

## 4. Grain Definitions

One **source_event** = one discrete source occurrence:
- A BCC meeting (includes date, agenda URL, minutes URL)
- An NBOR page snapshot (one HTTP fetch of the public notices app)
- A utility department page fetch
- A press release batch from a single fetch cycle
- An agenda packet publication

One **intel_item** = one extracted resident-impact finding:
- A BCC agenda action item (rezoning, resolution, contract approval)
- An NBOR individual notice (road closure, public hearing, permit)
- A county press release
- A sheriff news story
- A utility alert (boil water notice, water shortage)

One **review_queue_entry** = one editorial review task:
- Exactly one item from the review queue, with escalation level,
  review status, reviewer notes

One **dedupe_entry** = one known intel item:
- Exactly one fingerprint key, linked to one item_id

One **tracked_entity** (planned) = one durable thing:
- SilverLeaf community, CR 2209 highway project, a specific CDD,
  a retail development, a utility project — anything tracked over time

---

## 5. Relationship Map

```
source ──has_many──→ source_event ──has_many──→ intel_item ──has_one──→ review_queue_entry
                                                     │
                                                     ▼
                                               tracked_entity

intel_item ──has_one──→ dedupe_entry (via _dedupe_key)
intel_item ──referenced_by──→ review_queue_entry (via item_id)
intel_item ──classified_by──→ interest_filter (via keyword match)
intel_item ──tags──→ community (via communities[])
intel_item ──tags──→ topic (via taxonomy.md controlled vocab)
```

Pending (ENT-002):
```
intel_item ──has_many──→ tracked_entity (via tracked_entity_ids[])
tracked_entity ──has_many──→ intel_item (reverse link)
```

---

## 6. ID Conventions

| Object | Pattern | Examples |
|--------|---------|---------|
| `source_id` | Snake case prefixed by domain | `sjc_nbor_public_notices`, `sjc_bcc_calendar`, `sjso_news_stories` |
| `event_id` | `EVT-{prefix}-{YYYYMMDD}-{NNNN}` (sequential per source) | `EVT-BCC-20260120-0011`, `EVT-NBOR-20260704-0001` |
| `item_id` | `SJC-{prefix}-{YYYYMMDD}-{NNNN}` (sequential per day per source) | `SJC-NBOR-20260704-0001`, `SJC-BCC-20260120-0001`, `SJC-CN-20260603-0001`, `SJC-SL-20260704-0001` |
| `queue_id` | `Q-{item_id}` | `Q-SJC-NBOR-20260626-0001` |
| `dedupe_key` | 16-char hex hash (MD5-based, deterministic) | `e686c07578f7530e` |
| `candidate_id` | `CAND-SRC-{NNNN}` or descriptive | `CAND-SRC-0001`, `st_johns_citizen` |
| `beat_id` | `CAND-BEAT-{NNNN}` | `CAND-BEAT-0001` |
| `entity_id` | `ENT-{TYPE_PREFIX}-{DESCRIPTIVE-SLUG}` | `ENT-RETAIL-PUBLIX-SILVERLEAF`, `ENT-EDU-SILVERLEAF-K8` |

Item ID source prefixes observed: `NBOR`, `BCC`, `CN` (county_news), `SJSO`,
`UTIL` (utility), `SL` (silverleaf_discovery), `EM` (emergency_management),
`UD` (utility_department), `TCDD`/`SMCDD`/`TOLOCDD` (CDDs).

---

## 7. Status / Lifecycle Fields

### source_event.status
`discovered` → `extracted` / `partially_extracted` → `blocked` / `archived`
- See `schemas/source_event.schema.yaml` for full allowed values

### source_event.extraction_status
Free-text detail on extraction outcome (e.g. "Agenda PDF extracted (44 items).")

### review_status (on intel_item + review_queue_entry)
`pending_review` → `in_review` → `verified` / `needs_followup` / `rejected_noise` / `duplicate` / `escalated` / `archived`
- `pending_review` is the default for new items
- `published` reserved for future publishing phase
- `verified` confirms factual accuracy and classification

### escalation (on review_queue_entry only)
`immediate` (active emergency) → `high` (48h) → `normal` (weekly) → `low` (batch)
- Derived from urgency + sensitivity + interest filter matches

### signal / _signal (on review_queue_entry / intel_item)
`high_signal`, `medium_signal`, `low_signal`, `routine_noise`

### source.status (on source)
`active` / `verified` / `stale` — lifecycle of a monitored source

### community.status (on community)
`active` / `observed` — whether community is actively used or just identified

### tracked_entity.lifecycle_status
`proposed` → `approved` → `under_construction` → `completed` → `dormant` → `cancelled` → `archived`
Non-project types: `tracked` → `dormant` → `archived`
See `schemas/tracked_entity.schema.yaml` for field-level spec.

---

## 8. Source_Event vs Intel_Item Distinction

This is the project's most important data modeling decision.

| Aspect | source_event | intel_item |
|--------|-------------|------------|
| What it is | A container/context record | A discrete finding |
| Examples | BCC meeting metadata, NBOR page fetch, press release batch | BCC agenda decision/action item, NBOR individual notice/permit/hearing, individual press release |
| Enters review queue? | No | Yes |
| Enters dedupe index? | No | Yes |
| Has extracted_item_ids? | Yes (reverse link to items) | No |
| Has source_event_id? | No (is itself) | Yes (backlink to parent event) |

Concrete examples:

- BCC meeting on 2026-01-20 is a **source_event** (EVT-BCC-20260120-0011).
  Each agenda item (rezoning, resolution, contract) is an **intel_item**
  (SJC-BCC-20260120-0001).

- NBOR page fetch on 2026-07-04 is a **source_event**
  (EVT-NBOR-20260704-0001). Each individual notice (SUPMAJ, REZ, ZVAR)
  is an **intel_item** (SJC-NBOR-20260704-0001).

- County press release page fetch is a **source_event**. Each individual
  press release article is an **intel_item**.

---

## 9. Review Queue and Dedupe Rules

- **source_events do NOT enter the review queue.** Only intel_items in
  `data/intel_items/` are scanned by `scripts/build_review_queue.py`.
- **source_events do NOT enter the dedupe index.** Only intel_items are
  fingerprinted in `data/index/prior_items.yaml`.
- **Review queue tracks intel items only.** Each entry references one
  `item_id`. The queue is a flat YAML file (`data/review_queue/queue.yaml`).
- **Dedupe index tracks intel items only.** Each entry holds a deterministic
  `_dedupe_key` (16-char hex hash) plus the `item_id` and metadata.
- Cross-source clustering (same project across NBOR + BCC) is manual via
  `supporting_sources` array; no automated cluster detection.

---

## 10. Tracked Entities

Tracked entities are **implemented** (ENT-001 complete 2026-07-04). Registry at
`registry/tracked_entities.yaml`, schema at `schemas/tracked_entity.schema.yaml`.

Entity IDs follow the pattern `ENT-{TYPE_PREFIX}-{DESCRIPTIVE-SLUG}` (no date —
entities are durable across sessions). See §6 ID Conventions.

Intel item linkage (`tracked_entity_ids` field on intel_item) is pending ENT-002.
Entity names/aliases are manually mirrored to `registry/interest_filters.yaml`
until auto-generation is built.

---

## 11. Modeling Risks / Open Questions

1. **BCC linkage contradiction** — EVT-BCC events for May 2025–May 2026 have
   `extracted_item_ids: []` despite `status: extracted`. Only the Jan 20, 2026
   meeting links to items. This should be audited: are items missing, or were
   these calendar-only extractions?

2. **source_event adoption is incomplete** — Outside BCC and NBOR, many sources
   (county news, sheriff, utility department) do not have source_event records.
   Some early items were extracted before the source_event pattern was designed.

3. **LAST_RUN markers** — Three files (`logs/runs/*/LAST_RUN`) hold a single
   timestamp each. This may be too thin for future operational state (per-source
   run tracking, error counts, item volumes).

4. **Entity proliferation risk** — Avoid creating a tracked_entity for every
   one-off item. Only durable, multi-event things should get entity records.

6. **Official evidence vs leads/context** — Items from official government
   sources use `verification_status: source_confirmed`. Items from local media
   (St. Johns Citizen) are useful but need cross-referencing. There is no
   automated downgrade for non-official sources.

7. **SilverLeaf discovery items use source_id "silverleaf_discovery"** which is
   not a registered source in `registry/sources.yaml`. These are orphan items
   from a one-off discovery run, stored with `source_id: st_johns_citizen`
   in the actual item records. This creates a loose coupling.

8. **BCC agenda items are from a single meeting (Jan 20, 2026)** — 44 items
   extracted. No other BCC meetings have been extracted yet. The pipeline
   works but has low coverage.

---

## 12. Examples

### Example 1: BCC meeting → agenda item → review queue

```
source: sjc_bcc_calendar
  └── source_event: EVT-BCC-20260120-0011 (BCC Regular Meeting)
        └── intel_item: SJC-BCC-20260120-0002 (REZ 2025-11 Nothing Putt Fun)
              └── review_queue_entry: Q-SJC-BCC-20260120-0002
                    reviewed: verified, escalation: high
```

### Example 2: NBOR page snapshot → notice → review queue

```
source: sjc_nbor_public_notices
  └── source_event: EVT-NBOR-20260704-0001 (NBOR snapshot)
        └── intel_item: SJC-NBOR-20260704-0001 (SUPMAJ cell tower)
              └── review_queue_entry: Q-SJC-NBOR-20260704-0001
                    status: pending_review, escalation: high
```

### Example 3: Future tracked entity → multiple intel items

```
tracked_entity: ENT-SILVERLEAF-PUBLIX-001 (planned)
  ├── intel_item: SJC-SL-20260704-0001 (SilverLeaf mega Publix opens)
  ├── intel_item: SJC-NBOR-20260704-00XX (permit for Publix site work)
  └── intel_item: SJC-BCC-20260XXX-00XX (BCC approval of Publix-related easement)
```

---

## 13. Maintenance Rules

- Update this doc when adding new object types, IDs, schema files, or
  lifecycle statuses.
- Keep it concise. Link to `schemas/*.yaml` for field-level specs rather
  than duplicating.
- If this doc conflicts with schemas, schemas win for validation. But
  this doc should be updated to reflect the schema change.
- Update when `tracked_entities` is designed and implemented.
- Update when source_event coverage expands significantly.
