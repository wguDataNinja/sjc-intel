# Future News Ingestion Readiness

## Boundary

No open-ended autonomous news agent is implemented. No unapproved source list,
paywall bypass, scraping expansion, or full-body article archive is authorized.

The current implementation prepares the core model for a later approved
relevant-news phase by keeping source typing, provenance, dedupe, review, and
retention generalized.

## Existing Model Support

The current schema can represent approved future news candidates through:

- `app.sources.source_type` for `local_media`, `third_party_news`, or another
  approved source type;
- `app.intel_items.source_url`;
- `app.intel_items.source_published_at`;
- `app.intel_items.source_type`;
- `app.intel_items.title`;
- `app.intel_items.summary`;
- `app.intel_items.raw_excerpt`;
- `app.intel_items.citation`;
- `app.intel_items.resident_relevance`;
- `app.intel_items.review_status`;
- `app.intel_items.human_review_required`;
- `app.intel_items.tracked_entity_ids`;
- `app.intel_items.dedupe_key`;
- `app.dedupe_index_entries`;
- `app.raw_artifact_records` for external artifact metadata and content hashes;
- `app.source_retention_policies` for bounded retention decisions.

## Intended Later Flow

1. Candidate discovery from an approved source list.
2. Deterministic domain, date, and topic narrowing.
3. Fetch and normalize approved candidates.
4. Exact and near-duplicate checks.
5. Optional constrained relevance or extraction step.
6. Structured validation.
7. Provenance capture.
8. Human review where required.
9. Approved intel-item linkage.
10. Snapshot and UI availability.
11. Bounded retention or archive treatment.

## Storage Rule

Do not store unlimited full article bodies in PostgreSQL. Store normalized
metadata, approved excerpts, hashes, source URLs, provenance, and review state
unless a later legal/product/storage decision explicitly expands retention.

## Open Design Items

- approved news source list;
- near-duplicate algorithm and thresholds;
- excerpt policy;
- human-review categories;
- whether article snapshots are archived on the MacBook;
- public API visibility for third-party reporting versus official records.
