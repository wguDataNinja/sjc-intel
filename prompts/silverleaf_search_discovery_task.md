# SilverLeaf / Northwest St. Johns Search Discovery Task

## Objective

Find and extract intel items about development activity in the SilverLeaf
area and northwest St. Johns County growth corridor. The current data
pipeline misses these because the St. Johns Citizen (local media) is not
monitored, and county government sources don't use neighborhood names.

## Confirmed Developments to Find

| Project | Source | Keywords |
|---------|--------|----------|
| SilverLeaf mega-Publix (55k sq ft) | sjcitizen.com | "SilverLeaf Publix", "SilverLeaf Parkway" |
| Harris Teeter in SilverLeaf | sjcitizen.com | "Harris Teeter SilverLeaf" |
| SilverLeaf K-8 school (opening 2026-27) | sjcitizen.com | "SilverLeaf K-8" |
| Beach Valley Mini Golf (2 acres) | sjcitizen.com | "Beach Valley Mini Golf" |
| CR 2209 highway (IGP to SilverLeaf) | sjcitizen.com | "CR 2209", "International Golf Parkway" |
| Nocatee retail strip (Crosswater Pkwy) | sjcitizen.com | "Crosswater Parkway Nocatee" |
| Ascension St. Vincent's primary care (Nocatee) | sjcitizen.com | "Ascension St. Vincent's Nocatee" |
| Shores Fine Wine & Spirits (Nocatee) | sjcitizen.com | "Shores Fine Wine Nocatee" |
| Fairfield Inn & Suites (CR 210) | sjcitizen.com | "Fairfield Inn CR 210" |
| Taco Bell (CR 210/I-95) | sjcitizen.com | "Taco Bell CR 210" |

## Search Locations

1. **St. Johns Citizen** (sjcitizen.com) — use site search for each keyword
2. **SJC County News** (sjcfl.us/news) — check for any NW corridor press releases
3. **NBOR portal** (webapp.sjcfl.us/webnews/NBRscreend.aspx) — check for ROW permits on CR 2209, IGP, SilverLeaf Parkway
4. **SJSO News** (sjso.org/news-stories) — any incident reports mentioning SilverLeaf
5. **Nocatee community site** (nocatee.com) — community updates

## Output Format

For each found item, extract into this schema:

```yaml
item_id: "SJC-DISC-{YYYYMMDD}-{NNNN}"
title: "<article headline>"
summary: "<1-3 sentence summary from a resident perspective>"
source_id: "st_johns_citizen"  # or appropriate source
source_url: "<full article URL>"
source_published_at: "<date>"
topics:
  - development
  - infrastructure  # or appropriate
communities:
  - silverleaf
  - nocatee  # or appropriate
geographic_scope: "neighborhood"  # or single_community
urgency: "ongoing"  # development projects are ongoing
verification_status: "source_confirmed"
sensitivity: "low"
primary_topic: "development"
interest_tags:
  - "development_watch"
  - "property_values"
  - "quality_of_life"
resident_relevance:
  summary: "<why SilverLeaf residents should care>"
  affected_audiences:
    - "residents"
    - "homeowners"
    - "nearby_residents"
  why_it_matters: "<concrete impact on daily life>"
  confidence: "high"
  inference_notes: "Directly reported by St. Johns Citizen."
human_review_required: false
```

## Output File

Write all extracted items to:
`data/intel_items/{YYYY-MM-DD}/silverleaf_discovery.yaml`
