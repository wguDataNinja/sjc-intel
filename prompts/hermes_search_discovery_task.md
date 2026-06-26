# Hermes Task: Search Discovery

**Worker:** `search-discovery-worker`  
**Task:** `search-discovery-{YYYY-MM-DD}`  
**Status:** Template only — execute only with explicit instruction.

## Purpose

Search the public web for St. Johns County information sources and items NOT
already in the source registry. This is Loop B of the SJC_Intel discovery model.

## Inputs

- `registry/search_terms.yaml` — search term list
- `registry/sources.yaml` — existing sources (to avoid rediscovery)
- `registry/source_candidates.yaml` — existing candidates
- `docs/taxonomy.md` — controlled vocabularies
- `schemas/intel_item.schema.yaml` — output schema

## Source Scope

Search web/news/social platforms for:

1. **New source discovery** — websites, Facebook pages, Instagram accounts,
   Substacks, independent journalists covering SJC
2. **Community-specific content** — SilverLeaf, Nocatee, RiverTown, Shearwater,
   TrailMark, Beachwalk, Beacon Lake
3. **Corridor-specific content** — CR 210, SR 16, US 1, I-95
4. **Topic-specific content** — development, schools, roads, utilities, CDDs
5. **Local media** — news orgs, blogs, newsletters covering SJC

## Output

- New candidate sources → note in `registry/source_candidates.yaml`
- Orphan items → `data/intel_items/{YYYY-MM-DD}/web_discovery.yaml`
- Search term effectiveness log

## Completion

Return:
- sources discovered
- items found
- search terms that worked
- search terms that returned nothing
