# SJC Intel — Actual Data Evidence Packet

**Date:** 2026-07-06
**Purpose:** Data-grounded review packet showing the actual shape, strengths,
weaknesses, and latent structure in the current SJC intel items. Intended for
Buddy and ChatGPT to inspect and reason about the future knowledge model.
**Scope:** Read-only inspection. No code, data, or status modified.

---

## Section 1 — Dataset Profile

### Counts and Distributions

| Metric | Count | Notes |
|--------|-------|-------|
| **Total intel items** | 182 | Across 4 date directories, 18 YAML files |
| **Total source events** | 15 | 11 BCC meetings, 2 NBOR snapshots, 2 utility fetches |
| **Sources producing items** | 10 | See breakdown below |
| **Unique dedupe keys** | ~115 | Some collisions (duplicate items share keys) |
| **Review queue entries** | 132 | Queue built from a subset; 50 items not in queue |

### Items per Source

| Source | Items | % of Total | Producing Since |
|--------|-------|-----------|-----------------|
| `sjc_nbor_public_notices` | 75 | 41% | 2026-06-08 |
| `sjc_bcc_calendar` | 44 | 24% | 2026-06-26 |
| `sjc_county_news` | 9 | 5% | 2026-06-03 |
| `sjc_utility_department` | 8 | 4% | 2026-06-03 |
| `st_johns_citizen` (local media) | 6 | 3% | 2026-07-04 |
| `sjso_news_stories` | 5 | 3% | 2026-06-03 |
| `tolomato_cdd` | 3 | 2% | 2026-06-26 |
| `trout_creek_cdd` | 3 | 2% | 2026-06-26 |
| `six_mile_creek_cdd` | 3 | 2% | 2026-06-26 |
| `sjc_emergency_management` | 1 | 1% | 2026-06-26 |

### Items per Review Status

| Status | Count | % |
|--------|-------|---|
| `verified` | 108 | 59% |
| `pending_review` | 63 | 35% |
| (no status — CDD items) | 9 | 5% |
| `archived` | 1 | 1% |
| `rejected_noise` | 1 | 1% |

Note: 25 NBOR items appear in TWO files (2026-06-08 and 2026-06-26) — the
2026-06-08 copy has `fetched_at: 2026-06-26` indicating it was misplaced.

### Items per Topic (top 10)

| Topic | Items | % |
|-------|-------|---|
| `infrastructure` | 83 | 46% |
| `development` | 54 | 30% |
| `environment` | 45 | 25% |
| `county_government` | 44 | 24% |
| `public_notices` | 27 | 15% |
| `community_events` | 11 | 6% |
| `transportation` | 9 | 5% |
| `public_safety` | 8 | 4% |
| `parks_recreation` | 8 | 4% |
| `crime` | 4 | 2% |

### Items per Beat

| Beat | Items | % |
|------|-------|---|
| `utilities_water` | 43 | 24% |
| (no beat — CDD + early items) | 30 | 16% |
| `rezoning_comp_plan_dri` | 25 | 14% |
| `site_plans_permits_construction` | 24 | 13% |
| `local_government_budget_procurement` | 11 | 6% |
| `parks_amenities` | 10 | 5% |
| `roadwork_traffic` | 4 | 2% |
| `transportation` | 4 | 2% |
| `public_safety_livability` | 3 | 2% |
| `taxes_exemptions_trim_vab` | 2 | 1% |
| `emergency_weather_fire_flood` | 1 | 1% |

### Items per Interest Tag

| Tag | Items |
|-----|-------|
| `development_watch` | 56 |
| `utility_impact` | 47 |
| `quality_of_life` | 46 |
| `community_trust` | 24 |
| `cost_impact` | 15 |
| `property_values` | 9 |
| `traffic_impact` | 8 |
| `safety_concern` | 6 |
| `emergency_awareness` | 3 |
| `community_event` | 2 |

### Items per Urgency

| Urgency | Items | Notes |
|---------|-------|-------|
| `ongoing` | 62 | Evergreen background items |
| `archival` | 50 | Historical BCC agenda items, completed projects |
| `timely` | 34 | Upcoming hearings, current notices |
| (no urgency) | 9 | CDD items |
| `urgent` | 2 | Phase III water shortage (2 sources, same event) |

### Items per Sensitivity

| Sensitivity | Items |
|-------------|-------|
| `low` | 124 |
| `medium` | 23 |
| (no sensitivity) | 9 |
| `high` | 1 (double murder arrest, SKIP-20260603-0004) |

### Items per Geographic Scope

| Scope | Items |
|-------|-------|
| `county_wide` | 139 |
| (no scope) | 9 |
| `single_community` | 7 |
| `multi_community` | 1 |
| `neighborhood` | 1 |

### Community References

| Community | Items | Sources |
|-----------|-------|---------|
| `silverleaf` | 6 | SilverLeaf discovery items |
| `countywide` | 4 | SJSO, emergency, library |
| `st_augustine` | 2 | SJSO, county news |
| `vilano_beach` | 1 | County news |
| `porpoise_point` | 1 | County news |
| `nocatee` | 1 | SilverLeaf discovery |

### Items with Tracked Entity References

**0 items** have explicit `tracked_entity_ids` on the intel item. The review
queue builder infers entity matches (11 entity matches across 8 items), but
these are not stored on the source items themselves.

### Items with Source Event Parents

120/182 items have `source_event_id`. These are:
- All 75 NBOR items (2 snapshots)
- All 44 BCC items (1 meeting extracted)
- 1 utility item (SJC-UD-20260626-0001)

**62 items lack source_event parents:** 8 utility items, 9 county news,
5 SJSO, 6 SilverLeaf, 1 emergency, 9 CDD items.

### Items with Dates

146/182 have meaningful dates (`source_published_at` or `_meeting_date`).
9 CDD items have `source_created_at` instead. 0 items have _no_ temporal
information.

### Items with Location Information

13/182 have `communities` set. 1 has `neighborhood` scope. 0 have lat/lng,
parcel IDs, addresses, or coordinates. Location information is embedded in
raw_excerpt text for most items (e.g., "at 2416 Dobbs Road", "7250 US 1 North").

### Duplicate Groups

| Dedupe Key | Items | Source |
|------------|-------|--------|
| `e1e7b41af72ede8d` | 2 | SJC-NBOR-20260626-0001 (in 2 files) |
| `2e18f0cb7cddda69` | 3 | NBOR items 15,16,17 (2026-07-04) |
| `38cd637d1d0ea2fe` | 3 | NBOR items 21,22,23 (2026-06-26) |
| `a2b6c0939090f8e6` | 3 | NBOR items 5,6,11 (2026-06-26) |
| `04e882567677c934` | 2 | NBOR items 24,25 (2026-06-26) |

The duplicate dedupe keys suggest that some ROW permit items (e.g., Comcast
fiber cable in different locations) generate the same hash from
`source||category||title||date` when title is generic ("Comcast") and date
is empty/missing.

---

## Section 2 — Representative Item Packet

### Item 1: NBOR ROW Permit (Low Information)
```
ID:         SJC-NBOR-20260626-0001
Source:     sjc_nbor_public_notices (NBOR Public Notices)
Title:      Comcast
Type:       ROW permit
Excerpt:    "Fiber cable"
Date:       6/22/2026
Topics:     infrastructure, environment
Beat:       utilities_water
Interest:   utility_impact, quality_of_life
Urgency:    ongoing
Sensitivity: low
Status:     pending_review (also verified in duplicate file)
Geography:  county_wide (no district, no community)
Entity:     none
SE parent:  EVT-NBOR-20260626-0001
```

**What's present:** Source, date, type (ROW), app_id is empty.
**What's buried:** Which road? Which neighborhood? Exact location. What kind of
fiber (residential/commercial)? Duration of work? Traffic impact?
**Uses:** Utility disruption alerting — needs better location extraction.
**Extraction opportunity:** The NBOR page likely has more detail in the full
description field that wasn't captured in the excerpt.

### Item 2: NBOR Public Hearing (High Information)
```
ID:         SJC-NBOR-20260704-0001
Source:     sjc_nbor_public_notices
Title:      SUPMAJ 2025000029 St. Thomas Island Parkway Cell Tower
Excerpt:    "Request for Special Use Permit to allow construction of a
             180-foot monopole tower in Open Rural (OR) zoning."
Date:       7/23/2026
Topics:     development, infrastructure
Beat:       site_plans_permits_construction
Interest:   development_watch
Urgency:    timely
Sensitivity: low
Status:     pending_review
Geography:  county_wide (but location known: St. Thomas Island Parkway)
Entity:     none
SE parent:  EVT-NBOR-20260704-0001
```

**What's present:** Application ID, title, date, hearing type, zoning details.
**What's buried:** Exact address, neighborhood impact, nearby residents affected,
visual/environmental impact.
**Uses:** Development alert, project timeline, neighborhood notification.
**Extraction opportunity:** Zoning code (OR), structure height (180ft), type
(monopole cell tower) — all extractable from description. Needs entity creation
for the cell tower project.

### Item 3: BCC Agenda Item (Structured Meeting Record)
```
ID:         SJC-BCC-20260120-0002
Source:     sjc_bcc_calendar (BCC Calendar)
Title:      Public Hearing * REZ 2025-11 Nothing Putt Fun
Excerpt:    "REZ 2025-11 to rezone 3.98 acres at 7250 and 7280 US 1 North
             from CN to CHT"
Date:       2026-01-20 (meeting)
Topics:     development, county_government, public_notices
Beat:       rezoning_comp_plan_dri
Interest:   development_watch, property_values
Signal:     high_signal
Urgency:    archival
Sensitivity: low
Status:     verified
Geography:  county_wide (but address known: 7250-7280 US 1 North)
Entity:     none
SE parent:  EVT-BCC-20260120-0011
```

**What's present:** Meeting date, agenda item number, action type, rezoning
details, address, parcel size. Full structure from PDF extraction.
**What's buried:** Current use of the land, developer name, nearby community
impact, economic details.
**Uses:** Zoning change tracking, development timeline, neighborhood alert.
**Extraction opportunity:** Address is available — could be geocoded. Parcel size
(3.98 acres) is structured. Business name "Nothing Putt Fun" is in title.

### Item 4: County News (Capital Project)
```
ID:         SJC-CN-20260626-0001
Source:     sjc_county_news (County News)
Title:      SJC's Largest-Ever Capital Improvement Project Now Serving Residents
Excerpt:    "SJC's $191.8M SR 207 Water Reclamation Facility now operational"
Date:       2026-06-23 (published)
Topics:     infrastructure, environment
Beat:       utilities_water
Interest:   utility_impact, quality_of_life
Urgency:    ongoing
Sensitivity: low
Status:     verified
Geography:  county_wide
Entity:     ENT-INFRA-SR-207-WRF (inferred by queue builder)
SE parent:  none
```

**What's present:** Project milestone (now operational), dollar amount ($191.8M),
project name (SR 207 WRF Phase 2).
**What's buried:** Specific service area, capacity increase, timeline details.
**Uses:** Infrastructure project tracking, budget transparency, timeline.
**Important:** Cross-source relationship with SJC-UTIL-20260603-0003 (same
project, different milestone — "approved" vs "now operational"). These would be
powerful linked on a timeline.

### Item 5: Utility Department (Urgent Alert)
```
ID:         SJC-UTIL-20260603-0001
Source:     sjc_utility_department (Utility Department)
Title:      Phase III Extreme Water Shortage Declaration — Active
Excerpt:    "SJRWMD Phase III Extreme Water Shortage remains in effect...
             Residential irrigation limited to one day per week."
Date:       2026-05-11 (published)
Topics:     environment, infrastructure, emergency_alerts
Interest:   utility_impact, cost_impact, emergency_awareness
Taxonomy:   water_restrictions (gap proposed)
Urgency:    URGENT
Sensitivity: medium
Status:     verified
Geography:  county_wide
Entity:     none
SE parent:  none
```

**What's present:** Alert type (Phase III), start date, restrictions (1-day/week
irrigation), issuing agency (SJRWMD).
**What's buried:** Specific penalties, exemption details, duration estimate.
**Uses:** Emergency alert, newsletter top item, social media post.
**Cross-source:** Duplicate with SJC-CN-20260603-0005 (same declaration from
county news). Only 2 items marked urgent in entire dataset.

### Item 6: Sheriff (Safety/Sensitive)
```
ID:         SJC-SJSO-20260603-0001
Source:     sjso_news_stories (SJSO News)
Title:      Inmate charged; woman arrested for executing contraband drop
Excerpt:    "Inmate Devin Delaney and girlfriend Jacqueline Mottor charged
             for planning contraband drop of nicotine products onto restricted
             SJSO property."
Date:       2026-05-21 (published)
Topics:     public_safety, crime
Interest:   safety_concern
Urgency:    ongoing
Sensitivity: medium
Status:     verified
Geography:  county_wide
Entity:     none
SE parent:  none
Human_rev:  true
```

**What's present:** Incident narrative, names of individuals, charges.
**What's buried:** Facility location, specific security implications.
**Uses:** Public safety transparency. Requires human review.
**Concerns:** Names of individuals — privacy boundary needs clear policy.

### Item 7: CDD Board Notice (Different Schema)
```
ID:         tolomato_cdd-001
Source:     tolomato_cdd (Tolomato CDD)
Title:      Tolomato CDD Board Meeting Agenda — June 23, 2026
Content:    "Board meeting agenda for Tolomato CDD meeting on June 23, 2026"
Date:       2026-06-23
Topics:     county_government, public_notices
Status:     (NONE — CDD schema lacks review_status)
Geography:  (NONE — CDD schema lacks geographic_scope)
Entity:     none
SE parent:  none
```

**What's present:** Event type, date, CDD name, topic.
**What's missing:** Review status, urgency, sensitivity, geographic scope,
summary field, dedupe key. Different schema from main system — uses
`content` instead of `summary`/`raw_excerpt`.
**Uses:** CDD governance tracking, community board notifications.
**Note:** 9 CDD items across 3 files all use this alternative schema.

### Item 8: SilverLeaf Local Media (Rich Resident Relevance)
```
ID:         SJC-SL-20260704-0001
Source:     st_johns_citizen (St. Johns Citizen — local media)
Title:      Here's your first look at SilverLeaf's new 55,000 sq. ft. mega Publix
Excerpt:    "A massive new Publix (55,701 sq ft) opened at 1975 SilverLeaf
             Parkway with specialty departments."
Date:       2026-03-26 (published)
Topics:     development, infrastructure
Interest:   development_watch, property_values, quality_of_life
Urgency:    ongoing
Sensitivity: low
Status:     pending_review
Geography:  single_community (silverleaf)
Entity:     ENT-COMM-SILVERLEAF (inferred), ENT-RETAIL-PUBLIX-SILVERLEAF (inferred)
SE parent:  none
Type:       local_media
```

**What's present:** Specific address (1975 SilverLeaf Parkway), store details
(55,701 sq ft, beer/wine cafe, scratch bakery, pharmacy), opening date (March
26, 2026), developer details.
**What's buried:** Employment impact, traffic study, competitive landscape.
**Uses:** Community newsletter lead item, development timeline, entity page.
**Note:** Best resident relevance framing in the dataset: "SilverLeaf residents
now have a premier grocery anchor in their backyard."

### Item 9: Emergency Management (Seasonal)
```
ID:         SJC-EM-20260626-0001
Source:     sjc_emergency_management (Emergency Management)
Title:      Residents Urged to Prepare as 2026 Atlantic Hurricane Season Begins
Excerpt:    "Emergency Management highlights simple steps to protect lives
             and property ahead of potential storms."
Date:       2026-06-01 (published)
Topics:     public_safety, emergency_alerts, environment
Interest:   emergency_awareness
Urgency:    timely
Sensitivity: low
Status:     verified
Geography:  county_wide
Entity:     none
SE parent:  none
```

**What's present:** Seasonal reminder, general preparedness information.
**What's buried:** Specific shelters, evacuation zone information, updated
contact information.
**Uses:** Seasonal newsletter item, weather preparedness campaign.
**Note:** Only 1 emergency item. Seasonal source (hurricane season June-Nov).

### Item 10: Low-Information/Rejected (Noise Detection)
```
ID:         SJC-CN-20260626-0004
Source:     sjc_county_news (County News)
Title:      SJC Highlights Special Bond Between Recycling Driver and
            Three-Year-Old Resident
Excerpt:    "Heartwarming story about a recycling driver and a young resident"
Date:       2026-06-24
Topics:     community_events
Interest:   community_event
Urgency:    ongoing
Sensitivity: low
Status:     REJECTED_NOISE
Geography:  county_wide
Entity:     none
SE parent:  none
```

**What's present:** Human-interest story, feel-good content.
**What's missing:** Actionable resident information. No development, no alert,
no change that affects residents.
**Uses:** None for intelligence purposes. Correctly classified as noise.
**Important:** This is the only `rejected_noise` item. The classification
demonstrates that the system can identify and filter out non-actionable content.

---

## Section 3 — Full Record Traces

### Trace 1: NBOR Public Hearing
```
Source Registry:
  source_id: sjc_nbor_public_notices
  url: https://webapp.sjcfl.us/webnews/NBRscreend.aspx
  type: government_portal
  status: verified

Source Event:
  event_id: EVT-NBOR-20260704-0001
  type: public_notice_snapshot
  date: 2026-07-04
  items: 25 extracted
  health: accessible

Parser Output (raw record):
  {title: "SUPMAJ 2025000029 St. Thomas Island Parkway Cell Tower",
   category: "Meeting", date: "7/23/2026", district: "",
   app_id: "SUPMAJ 2025000029", pdf_urls: [...], description: "..."}

Intel Item YAML fields present:
  item_id, title, summary, source_id, source_url, source_event_id,
  source_published_at, discovered_at, discovered_by, topics, communities,
  geographic_scope, urgency, verification_status, sensitivity,
  recommended_channels, raw_excerpt, citation, review_status,
  primary_topic, interest_tags, resident_relevance, taxonomy_gap,
  human_review_required, created_at,
  _dedupe_key, _category, _beat, _app_id, _pdf_urls, _district, _raw_text

Review Queue:
  queue_id: Q-SJC-NBOR-20260704-0001
  escalation: high (via priority beat)
  matched_filters: [] (not matched by any interest filter)
  review_status: pending_review

PostgreSQL Mapping (if loaded):
  app.sources: upsert from source_id
  app.source_events: upsert from source_event
  app.intel_items: full column mapping (40+ columns)
  app.dedupe_index_entries: dedupe_key

Metrics:
  increments: intel_items_total, intel_items_by_source[nbor],
              intel_items_by_status[pending_review],
              intel_items_by_category[Meeting],
              intel_items_by_beat[rezoning_comp_plan_dri]

Retention:
  raw HTML: 30-day retention (government_portal type)
  normalized: unbounded
  snapshot: compact daily

Gap: No entity link (should link to cell tower project).
      No community link (St. Thomas Island location not mapped).
      No app_id visible in summary (buried in _app_id only).
```

### Trace 2: BCC Agenda Item
```
Source Registry:
  source_id: sjc_bcc_calendar
  url: https://www.sjcfl.us/bcc-calendar/  (Clerk board records)
  type: government_portal
  status: verified

Source Event:
  event_id: EVT-BCC-20260120-0011
  type: meeting
  date: 2026-01-20
  items: 44 extracted from agenda PDF

PDF Flow:
  Clerk HTML → parse_meetings() → download 1202026_agenda.pdf
  → pypdf extract_text() → parse_agenda_items() → 44 items

Intel Item YAML:
  All 44 items share _meeting_date: 2026-01-20
  Include _action_type, _signal, _agenda_item_number, _beat
  Example signal breakdown: 35 high, 7 medium, 1 low, 1 routine_noise

Review Queue:
  42 verified, 1 pending_review (item 11), 2 archived

PostgreSQL:
  Same mapping as NBOR plus meeting-specific columns:
  meeting_date, agenda_item_number, action_type, source_type

Gap: No BCC meetings other than Jan 20 have been extracted.
      June 2026 agenda links are broken (noted in source_event: blocked).
```

### Trace 3: County News (With Cross-Source Link)
```
Source Registry:
  source_id: sjc_county_news
  url: https://www.sjcfl.us/news/
  type: wordpress_blog
  status: active

Fetch: Manual HTTP GET (no extractor script)
Raw: WordPress blog HTML

Intel Item: SJC-CN-20260626-0001
  title: "SJC's Largest-Ever Capital Improvement Project Now Serving Residents"
  source_published_at: 2026-06-23
  topics: infrastructure, environment
  beat: utilities_water

Cross-source link:
  Related to SJC-UTIL-20260603-0003 ($191M SR 207 WRF Phase 2 Approved)
  Same project, different milestones (approval → operational)
  Current detection: NONE — no automated linking

Gap: No source_event parent. No cross-source link to utility item.
      Link table (intel_item_tracked_entities) would need population.
```

### Trace 4: Utility Alert (Urgent)
```
Source Registry:
  source_id: sjc_utility_department
  url: https://www.sjcfl.us/departments/utility-department/
  type: government_portal
  status: verified

Intel Item: SJC-UTIL-20260603-0001
  title: "Phase III Extreme Water Shortage Declaration — Active"
  urgency: URGENT
  topics: environment, infrastructure, emergency_alerts
  taxonomy_gap: water_restrictions
  recommended_channels: [alert]

Cross-source duplicate:
  SJC-CN-20260603-0005 — same declaration from county news
  Different framing, same underlying event

Gap: No single "event" record that both items reference.
      Urgent items should trigger notification workflow (none exists).
```

### Trace 5: CDD Item (Alternative Schema)
```
Source Registry:
  source_id: six_mile_creek_cdd
  url: https://sixmilecreekcdd.com/
  type: official_special_district
  status: active

Intel Item: six_mile_creek_cdd-001
  Schema: CDD-specific (content, topic_classification, resident_interest)
  Missing: review_status, urgency, sensitivity, geographic_scope, dedupe_key

Gap: CDD schema is incompatible with main system.
      Items don't enter review queue correctly (no review_status field).
      No source_event linking.
```

### Trace 6: Sheriff Item (Sensitive/Human Review)
```
Source Registry:
  source_id: sjso_news_stories
  url: https://www.sjso.org/news-stories/
  type: wordpress_blog
  status: active

Intel Item: SJC-SJSO-20260603-0004
  title: "Arrest made in connection to 2023 double murders of Cody Bennett
          and Tre' Lyons"
  sensitivity: high
  human_review_required: true
  communities: [st_augustine]

Gap: Only 1 high-sensitivity item. No publication policy for crime items.
      Names of individuals present — privacy boundary unclear.
```

### Trace 7: Local Media News-Like Item
```
Source Registry:
  source_id: st_johns_citizen (not a registered source in sources.yaml)
  url: https://sjcitizen.com/
  type: local_media (stored as source_type field on items)
  status: not in registry as canonical source

Intel Item: SJC-SL-20260704-0003
  title: "Fore! Major new 2-acre recreational attraction proposed for SilverLeaf"
  source_type: local_media
  communities: [silverleaf]
  geographic_scope: single_community

Gap: source_id "st_johns_citizen" is NOT in registry/sources.yaml as
      a tracked source with monitoring config. Items exist but source
      is not officially canonical. Verification_status is "source_confirmed"
      but the source is media, not government.
```

### Trace 8: Duplicate/Update Case
```
File 1: data/intel_items/2026-06-08/sjc_nbor_public_notices.yaml
  fetched_at: 2026-06-26T07:16:16Z  ← NOTE: wrong directory!
  items count: 25
  review_status: verified

File 2: data/intel_items/2026-06-26/sjc_nbor_public_notices.yaml
  fetched_at: 2026-06-26T07:16:16Z (same timestamp)
  items count: 25
  review_status: pending_review

Same content, same fetch time, different review statuses.
Stored in two date directories.
Dedupe index has both sets of keys (50 entries for 25 unique items).

Gap: Data inconsistency — same items in two directories.
      No mechanism to detect and reconcile duplicate file storage.
```

---

## Section 4 — Latent Entities

### Candidate Entities Not Currently Tracked

| Candidate | Aliases | Example Items | Source Count | Tracked? | Deterministic? | LLM Needed? |
|-----------|---------|---------------|-------------|----------|---------------|-------------|
| **Bushrangers Brewery** | (none yet) | SJC-NBOR-20260704-0008, -0009 | 2 | No | No (text only) | Yes (entity extraction) |
| **St. Thomas Island Cell Tower** | (none yet) | SJC-NBOR-20260704-0001 | 1 | No | Partial (app_id) | Low |
| **Nothing Putt Fun** | (none yet) | SJC-BCC-20260120-0002 | 1 | No | Partial (address) | No |
| **Porpoise Point Beach Access** | Vilano Beach Ramp | SJC-CN-20260603-0002 | 1 | No | No (text only) | No (regex) |
| **SR 207 Water Reclamation Facility** | SR 207 WRF | SJC-UTIL-20260603-0003, SJC-CN-20260626-0001 | 2 | **YES** ENT-INFRA-SR-207-WRF | Yes (entity label) | No |
| **Daily's Place** | 600 SR 13 North | SJC-NBOR-20260704-0007 | 1 | No | No (text only) | No (regex) |
| **Canopy Shores PUD** | (none) | SJC-NBOR-20260704-0006 | 1 | No | Partial (app_id) | Low |
| **Deerfield Estates** | (none) | SJC-BCC-20260120-0012 | 1 | No | No (text only) | No (regex) |
| **Trailmark East** | (none) | SJC-BCC-20260120-0013 | 1 | No | No (text only) | No |
| **Summer Haven** | (none) | SJC-BCC-20260120-0017, -0018 | 2 | No | No (text only) | No (regex) |
| **Flagler Estates** | (none) | SJC-BCC-20260120-0004 | 1 | No | No (text only) | No |
| **Shores Boulevard Median** | (none) | SJC-BCC-20260120-0008 | 1 | No | No (text only) | No |
| **Tolomato CDD** | (none) | tolomato_cdd-001, -002, -003 | 3 | No | Yes (source_id) | No |
| **Six Mile Creek CDD** | TrailMark CDD | six_mile_creek_cdd-001, -002, -003 | 3 | No | Yes (source_id) | No |
| **Trout Creek CDD** | Shearwater CDD | trout_creek_cdd-001, -002, -003 | 3 | No | Yes (source_id) | No |
| **Devin Delaney** | (individual) | SJC-SJSO-20260603-0001 | 1 | No | Yes (explicit name) | No (privacy concern) |
| **Jacqueline Mottor** | (individual) | SJC-SJSO-20260603-0001 | 1 | No | Yes (explicit name) | No (privacy concern) |
| **Charlie Ryan** | (juvenile, name redacted) | SJC-SJSO-20260603-0002 | 1 | No | Yes (explicit name) | No (PRIVACY) |
| **James-Cogo Commercial** | (none) | SJC-BCC-20260120-0003 | 1 | No | Partial (address) | No |
| **Golfway Centre PUD** | (none) | SJC-NBOR-20260626-0014 | 1 | No | Partial (app_id) | Low |
| **East Peyton Parkway** | (none) | SJC-NBOR-20260704-0019 | 1 | No | Partial (name) | No (regex) |

### Ambiguity Risks

- "Comcast" appears as a title for 19+ ROW permit items — these are different
  projects at different locations, but the title is identical. Entity resolution
  would need to consider app_id or description to distinguish.
- "Bushrangers Brewery" appears in two related items but with different app_ids
  (ZVAR + SUPMAJ). An LLM could determine they're the same entity.

---

## Section 5 — Latent Events and Milestones

### Recurring Event Types in Actual Data

| Event Type | Examples | Items | Fields Available | Fields Buried |
|-----------|---------|-------|-----------------|---------------|
| **Public Hearing Scheduled** | NBOR Meeting notices | 25+ | date, category, app_id, description | hearing time, location, staff contact |
| **ROW Permit Filed** | NBOR ROW items | 40+ | date, category, title, description | exact road, duration, company |
| **BCC Agenda Item Added** | BCC items | 44 | meeting date, action type, signal | staff recommendation, fiscal impact |
| **BCC Decision/Vote** | BCC items (action_type keys) | 44 | action_type (resolution, contract, etc.) | vote count, fiscal amount |
| **Road Closure** | NBOR ROW items with keywords | 3 | date, title | exact location, duration, detour |
| **Traffic Signal Activation** | NBOR item 19 | 1 | date, intersection names | exact timing |
| **Utility Interruption** | Utility boil notice/chlorine | 2 | date, title | affected area, duration |
| **Water Shortage Declaration** | Phase III items | 2 | date, level, restrictions | duration, penalties |
| **Project Approval** | BCC decisions, utility items | 3 | date, project name, amount | approval conditions |
| **Project Milestone (completed/operational)** | County news items | 2 | date, project name | timeline, budget comparison |
| **CDD Board Meeting** | CDD items | 4 | date, CDD name | agenda items, decisions |
| **CDD Board Vacancy/Election** | CDD items | 2 | date, seat numbers | candidate qualifications |
| **CDD Assessment/FY Budget** | CDD item | 1 | tax/fiscal topic | dollar amount, rate |
| **Emergency Notice** | Hurricane prep, water shortage | 3 | date, alert type | specific actions |
| **Surplus Auction** | County news item | 1 | date, location | items list |
| **Summer Reading Program** | County news library item | 1 | date range | event schedule |
| **Police Incident Report** | SJSO arrest/rescue items | 5 | date, incident narrative | specific charges, court dates |

### Structured Event Schema (Proposed)

```yaml
event:
  event_id: unique
  event_type: public_hearing | permit_filing | bcc_decision | road_closure |
              utility_interruption | water_restriction | project_milestone |
              cdd_meeting | cdd_election | emergency_notice | other
  source_item_ids: [item IDs that provide evidence]
  date: event date
  title: short description
  status: scheduled | occurred | cancelled | rescheduled
  entities: [linked entity IDs]
  locations: [linked location IDs]
```

**Feasibility:** Most event types can be extracted with deterministic rules
from the current data (checking `_beat`, `_category`, `_action_type`, etc.).
Event detail extraction (specifics like "vote count" or "fiscal amount") would
benefit from LLM extraction.

---

## Section 6 — Latent Claims and Facts

### Candidate Claims from Actual Data

These are **candidate interpretations** for design analysis, not approved claims.

| # | Item ID | Candidate Claim | Subject | Predicate | Object | Date | Deterministic? | LLM? | Review? |
|---|---------|----------------|---------|-----------|--------|------|---------------|------|---------|
| 1 | SJC-UTIL-20260603-0001 | Phase III Extreme Water Shortage is in effect | Water restrictions | is_active | Phase III | 2026-05-11 | Yes (field) | No | Low |
| 2 | SJC-UTIL-20260603-0001 | Residential irrigation limited to 1 day/week | Irrigation | limited_to | 1 day/week | 2026-05-11 | Partial (text) | Yes | Low |
| 3 | SJC-UTIL-20260603-0003 | BOCC approved $191.8M SR 207 WRF Phase 2 | SR 207 WRF | approved | $191.8M | 2025-12-19 | Partial (text) | Yes | Low |
| 4 | SJC-CN-20260626-0001 | SR 207 WRF is now operational | SR 207 WRF | is_operational | true | 2026-06-23 | Partial (text) | Yes | Low |
| 5 | SJC-NBOR-20260704-0001 | Cell tower proposed at St. Thomas Island Pkwy | Cell tower | proposed | 180ft monopole | 2026-07-23 | Partial (text) | Yes | Low |
| 6 | SJC-BCC-20260120-0002 | REZ 2025-11 proposes rezoning 3.98 acres at US 1 North | Nothing Putt Fun | proposed_rezone | CN to CHT | 2026-01-20 | Yes (field) | No | Low |
| 7 | SJC-CN-20260603-0002 | $524,000 resiliency improvements completed at Porpoise Point | Porpoise Point | completed_improvements | $524,000 | 2026-05-26 | Partial (text) | Yes | Low |
| 8 | SJC-UTIL-20260603-0002 | Free chlorine burnout scheduled June 1-21 | CR 214 WTP | scheduled | chlorine burnout | 2026-06-01 | Partial (text) | Yes | Low |
| 9 | SJC-CN-20260626-0002 | Railroad crossing maintenance to close W. King Street and Kinlaw Road | Railroad crossing | closing_for_maintenance | W. King + Kinlaw | 2026-06-22 | Partial (text) | Yes | Low |
| 10 | SJC-UD-20260704-0001 | $1.6M capital improvement completed at Plantation WTP | Plantation WTP | completed_improvement | $1.6M | 2026-07-04 | Partial (text) | Yes | Low |
| 11 | SJC-SJSO-20260603-0001 | Inmate and accomplice charged for contraband drop | Devin Delaney | charged_with | contraband drop | 2026-05-21 | Yes (field) | No | High |
| 12 | SJC-SJSO-20260603-0004 | Arrest made in 2023 double murders | Suspect | arrested_for | 2023 double murder | 2026-05-21 | Yes (field) | No | High |
| 13 | SJC-EM-20260626-0001 | 2026 Atlantic hurricane season began June 1 | Hurricane season | started | 2026-06-01 | 2026-06-01 | Yes (field) | No | Low |
| 14 | SJC-NBOR-20260704-0008 | Bushrangers Brewery requests alcohol variance near church | Bushrangers Brewery | requested_variance | alcohol sales near church | 2026-07-21 | Partial (text) | Yes | Medium |
| 15 | SJC-NBOR-20260704-0019 | Traffic lights at 3 East Peyton Pkwy intersections activating July 14 | East Peyton Pkwy | activating | traffic lights | 2026-07-14 | Partial (text) | Yes | Low |
| 16 | SJC-BCC-20260120-0004 | Interlocal agreement for Flagler Estates road paving approved | Flagler Estates | approved | road paving | 2026-01-20 | Partial (text) | Yes | Low |
| 17 | SJC-SJSO-20260603-0003 | DUI Wolfpack operation resulted in 9 arrests, 173 stops | DUI Wolfpack | resulted_in | 9 arrests | 2026-03-20 | Yes (field) | No | Medium |
| 18 | SJC-BCC-20260120-0005 | BOCC discussed septic-to-sewer connection policy | Septic-to-sewer | discussed | connection policy | 2026-01-20 | Yes (field) | No | Low |
| 19 | SJC-BCC-20260120-0007 | LAMP funding increase of $1.5M requested | LAMP program | requested_funding_increase | $1.5M | 2026-01-20 | Partial (text) | Yes | Low |
| 20 | SJC-SL-20260704-0001 | Publix at 1975 SilverLeaf Pkwy opened March 26, 2026 | SilverLeaf Publix | opened | March 26, 2026 | 2026-03-26 | Yes (field) | No | Low |

---

## Section 7 — Cross-Source Relationship Examples

### Group 1: SR 207 Water Reclamation Facility (2 sources, 2 milestones)
```
Relationship: Same project, different lifecycle phases
Confidence: HIGH

Item A: SJC-UTIL-20260603-0003 (2025-12-19)
  Source: sjc_utility_department
  "Phase 2 approved for $191.8M"

Item B: SJC-CN-20260626-0001 (2026-06-23)
  Source: sjc_county_news
  "Now operational" (same $191.8M project)

Detection: EXACT — entity label "SR 207 Water Reclamation Facility Phase 2"
           matches ENT-INFRA-SR-207-WRF. Both items are linked by the
           review queue builder via entity matching.

Resident-facing: "SR 207 WRF approved Dec 2025, opened June 2026 — $191.8M"
```

### Group 2: Phase III Water Shortage (2 sources, same event)
```
Relationship: Same event reported by different sources
Confidence: HIGH

Item A: SJC-UTIL-20260603-0001 (2026-05-11)
  Source: sjc_utility_department
  "Phase III Extreme Water Shortage Declaration — Active"

Item B: SJC-CN-20260603-0005 (2026-05-18)
  Source: sjc_county_news
  "SJC Enters Phase III Extreme Water Shortage Declaration"

Detection: NEAR-EXACT — same topic, same urgency (urgent), same date range.
           No entity link exists. Dedupe keys are different.

Resident-facing: "Phase III water restrictions remain in effect — irrigation
                 limited to 1 day/week"
```

### Group 3: Bushrangers Brewery (Same source, 2 related applications)
```
Relationship: Same entity, two different permit applications
Confidence: HIGH

Item A: SJC-NBOR-20260704-0008
  "ZVAR 2025000035 Bushrangers Brewery — alcohol variance near church"

Item B: SJC-NBOR-20260704-0009
  "SUPMAJ 2025000030 Bushrangers Brewery — microbrewery SUP"
  (Both at 470 SR 207)

Detection: EASY — same address (470 SR 207), same entity name in title.
           No automated linking currently.

Resident-facing: "Bushrangers Brewery applying for both microbrewery permit
                 and alcohol sales variance at 470 SR 207"
```

### Group 4: BCC Rezonings Cluster (Single meeting, multiple related items)
```
Relationship: Multiple agenda items from same meeting
Confidence: HIGH (share source_event_id EVT-BCC-20260120-0011)

Items: SJC-BCC-20260120-0001 through -0044
  Same meeting, different agenda items.
  Some are related: items 12-16 are all utility easement resolutions
  for different subdivisions (Deerfield Estates, Trailmark East, etc.)

Detection: TRIVIAL — same source_event_id.
           Sub-cluster detection (easement resolutions) not automated.

Resident-facing: "January 20 BCC meeting covered 44 items including
                 rezoning, utility easements, and budget items"
```

### Group 5: NBOR File Duplication (Storage error)
```
Relationship: Exact duplicate files in different directories
Confidence: HIGH

File A: data/intel_items/2026-06-08/sjc_nbor_public_notices.yaml (25 items)
File B: data/intel_items/2026-06-26/sjc_nbor_public_notices.yaml (25 items)
Same fetched_at timestamp, same item IDs, different review_status.

This is a data storage bug, not a meaningful cross-source relationship.
```

### Group 6: CDD Trifecta (3 CDDs, similar event types)
```
Relationship: Parallel CDD governance events across different communities
Confidence: MEDIUM

tolomato_cdd-001: Meeting agenda June 23
six_mile_creek_cdd-003: Meeting agenda June 10 (TrailMark)
trout_creek_cdd-001: Meeting agenda June 25 revised (Shearwater)

Detection: Same source_type (official_special_district), same topic structure.
           Useful for "CDD governance roundup" newsletter feature.

Resident-facing: "This week's CDD meetings: Tolomato (Nocatee), Six Mile
                 Creek (TrailMark), Trout Creek (Shearwater)"
```

---

## Section 8 — Query Examples Using Current Data

### Q1: What changed recently in SilverLeaf?
```
Result: 6 items from silverleaf_dev_discovery.yaml
  SJC-SL-20260704-0001: SilverLeaf Mega Publix opened (March 2026)
  SJC-SL-20260704-0002: SilverLeaf K-8 school under construction (opens Aug 2026)
  SJC-SL-20260704-0003: Beach Valley Mini Golf proposed
  SJC-SL-20260704-0004: CR 2209 connector opened (Oct 2025)
  SJC-SL-20260704-0005: Harris Teeter proposed
  SJC-SL-20260704-0006: (Nocatee item — not SilverLeaf)

Fields used: communities=["silverleaf"] (deterministic)
Answer quality: HIGH — 6 items with clear titles, dates, summaries
```

### Q2: What road or traffic issues affect the area?
```
Result: 9 items (transportation topic + roadwork beat + traffic tag)
  SJC-NBOR-20260704-0019: East Peyton Pkwy traffic light activation
  SJC-NBOR-20260626-0016: Drainage improvement (roadwork_traffic)
  SJC-CN-20260626-0002: Railroad crossing closure
  SJC-BCC-20260120-0008: Median Opening — Shores Boulevard
  SJC-BCC-20260120-0019: BUILD grant applications for SR 16 / CR 210
  SJC-BCC-20260120-0039: Grant applications for CR 2209 connector
  SJC-SL-20260704-0004: CR 2209 connector opened (archival)
  NBOR ROW items: utility work affecting roads (40+ items, low signal)

Fields used: topics=["transportation"] OR beat="roadwork_traffic"
             OR interest_tags=["traffic_impact"]
Limitation: Many NBOR ROW items affect roads but aren't tagged as
            transportation (tagged as utilities). Need better classification.
```

### Q3: What school-related updates exist?
```
Result: 3 items
  SJC-CN-20260603-0003: Summer Reading Program (library, not school)
  SJC-SL-20260704-0002: SilverLeaf K-8 school construction
  SJC-BCC-20260120-00??: Possible school-related item

Fields used: topics=["education"] OR interest_tags=["school_zones"]
Coverage: VERY LOW — only 3 items. School district sources not producing.
```

### Q4: What CDD-related updates exist?
```
Result: 9 items
  3 Tolomato CDD (meeting agenda, minutes, assessment info)
  3 Six Mile Creek CDD (vacancy announcement, qualifying period, meeting)
  3 Trout Creek CDD (meeting agenda, workshop, regular meeting)

Fields used: source_type="official_special_district" OR source_id matches
Answer quality: HIGH for meeting notices. Missing: actual meeting outcomes,
                financial details, assessment amounts.
```

### Q5: What public-safety items exist?
```
Result: 5 SJSO items + 1 emergency + 1 county jail item
  SJC-SJSO-20260603-0001: Contraband drop (medium sensitivity)
  SJC-SJSO-20260603-0002: Autistic juvenile rescue (low)
  SJC-SJSO-20260603-0003: DUI Wolfpack operation (archived)
  SJC-SJSO-20260603-0004: Double murder arrest (HIGH sensitivity)
  SJC-SJSO-20260626-0001: Jail escape plot (medium sensitivity)
  SJC-EM-20260626-0001: Hurricane season prep

Review: 5 items require human review (all SJSO items)
```

### Q6: What items concern a named tracked entity?
```
Direct match: 0 items have explicit tracked_entity_ids
Inferred match: 11 entity matches across 8 items (from queue builder)
  ENT-COMM-SILVERLEAF (5 items)
  ENT-INFRA-SR-207-WRF (2 items)
  ENT-ROAD-CR-2209-CONNECTOR (2 items)
  ENT-EDU-SILVERLEAF-K8 (1 item)
  ENT-REC-BEACH-VALLEY-MINI-GOLF (1 item)
```

### Q7: Which items remain unresolved or unverified?
```
60 items with pending_review:
  - 25 NBOR items (2026-07-04)
  - 25 NBOR items (2026-06-26 — the other copy)
  - 1 utility item
  - 6 SilverLeaf discovery items
  - 1 BCC item (item 11)
  - 1 utility item (UD 20260704)
```

### Q8: Which items came from official sources vs local media?
```
Official gov sources (source_confirmed): 148 items
Local media (st_johns_citizen): 6 items
No verification_status: 9 CDD items
CDD items: ambiguous — official special district but schema is different
```

### Q9: Which records describe the same underlying issue?
```
Known clusters (detected manually):
  1. Phase III Water Shortage: 2 items, 2 sources
  2. SR 207 WRF: 2 items, 2 sources, 2 milestones
  3. Bushrangers Brewery: 2 items, 1 source, 2 permits
  4. NBOR duplicate: 25 items x2, stored in 2 dirs
```

### Additional Queries Suggested by Data

**Q10: What utility work is happening or planned?**
→ 47 items with utility_impact tag + 8 utility department + 40+ NBOR ROW items

**Q11: What development approvals are pending?**
→ 25 rezoning/comp_plan items + NBOR hearing items with future dates

**Q12: What happened at recent BCC meetings?**
→ 44 items from Jan 20 meeting. No other meetings extracted.

**Q13: What emergency alerts are active?**
→ 2 urgent items (water shortage). No other active alerts.

**Q14: Which items have a specific application/permit number?**
→ 25+ items with _app_id (REZ, ZVAR, SUPMAJ, MAJMOD, etc.)

**Q15: What items affect St. Augustine specifically?**
→ 2 items with st_augustine community. Many more likely buried in text.

---

## Section 9 — Resident-Facing Output Mock Content

### A. SilverLeaf Community Digest (5 bullets)

```
SilverLeaf Development Update — July 2026
══════════════════════════════════════════

🟢 COMPLETED:
• Mega Publix opened March 26 at 1975 SilverLeaf Parkway — 55,701 sq ft
  with pharmacy, beer/wine café [SJC-SL-20260704-0001] [source_confirmed]
• CR 2209 Connector (IGP to SilverLeaf Parkway) opened October 2025 —
  3-mile, 4-lane divided highway [SJC-SL-20260704-0004] [source_confirmed]

🟡 IN PROGRESS:
• SilverLeaf K-8 School under construction — 190,000 sq ft, 3 stories,
  73 classrooms, opening August 2026 [SJC-SL-20260704-0002] [source_confirmed]

🔵 PROPOSED:
• Beach Valley Mini Golf — 36-hole course on 2 acres, pre-application
  submitted Aug 2025, DRC review Apr 2026 [SJC-SL-20260704-0003] [pending]
• Harris Teeter (Kroger) — 61,000 sq ft supermarket proposed for
  SilverLeaf shopping center [SJC-SL-20260704-0005] [pending]
```

### B. Tracked Entity Timeline: SR 207 Water Reclamation Facility

```
SR 207 Water Reclamation Facility Phase 2
══════════════════════════════════════════
Entity: ENT-INFRA-SR-207-WRF

📅 Dec 19, 2025 — APPROVED
  BOCC approved Phase 2, awarded $191.8M design-build agreement
  Source: SJC-UTIL-20260603-0003 [verified]

📅 Jun 23, 2026 — OPERATIONAL
  "SJC's Largest-Ever Capital Improvement Project Now Serving Residents"
  Source: SJC-CN-20260626-0001 [verified]

📅 Jul 2026 — SERVING
  Facility now serving CR 210 / SR 207 corridor
  (No further items — monitoring gap)
```

### C. Weekly Email Digest (Mock)

```
SJC Intel Weekly — June 26, 2026
═════════════════════════════════

📋 NEW PUBLIC NOTICES (25 items)
• Rezoning requests: ZVAR 2026000011 (Bargfrede Shed), ZVAR 2026000019
  (Aspinwall Variance), REZ 2026000012 (St. Augustine Airport East)
• Special use permits: SUPMAJ St. Thomas Island Parkway Cell Tower (180ft)
• ROW permits: Comcast fiber, Beaches Energy, JEA, FPL — multiple locations

🏛️ COUNTY GOVERNMENT
• SR 207 Water Reclamation Facility now operational ($191.8M)
• Railroad crossing maintenance closing W. King Street and Kinlaw Road

🚨 EMERGENCY MANAGEMENT
• Hurricane season reminder — prepare now (season began June 1)

💧 UTILITIES
• $1.6M capital improvement at Plantation Water Treatment Plant completed
• Utility Department receives high Moody's rating

📌 CDD MEETINGS
• Tolomato CDD: Agenda June 23, Minutes April 28, FY2026 Assessment
• Six Mile Creek CDD: Board vacancy, Candidate qualifying period
• Trout Creek CDD: Meeting June 25 (revised), Workshop July 7

Source: All items verified or from official sources.
Contact: [future subscription link]
```

### D. Social Post Drafts (3 Examples)

```
Draft 1 (Facebook/Nextdoor):
  ⚠️ WATER RESTRICTIONS REMAIN IN EFFECT
  St. Johns County is under Phase III Extreme Water Shortage.
  Residential irrigation: 1 day per week only.
  [source: SJC-UTIL-20260603-0001] [verified]
  Review note: Confirmed with SJRWMD notice. No sensitive content.
  [NOT FOR PUBLICATION UNTIL PUBLICATION WORKFLOW EXISTS]

Draft 2 (Twitter/X):
  🏗️ SilverLeaf's mega Publix is now open at 1975 SilverLeaf Pkwy —
  55,701 sq ft with pharmacy, beer/wine cafe, and scratch bakery.
  [source: SJC-SL-20260704-0001] [St. Johns Citizen / source_confirmed]
  Review note: Media source, not government. Link to article, don't
  reproduce copyrighted text.
  [NOT FOR PUBLICATION UNTIL PUBLICATION WORKFLOW EXISTS]

Draft 3 (Nextdoor — neighborhood-specific):
  🔧 East Peyton Parkway traffic signals activating July 14
  Three intersections switching from flash to full operation:
  • Racetrack Road
  • Pacetti Road
  • Roberts Road
  [source: SJC-NBOR-20260704-0019] [official notice]
  Review note: Directly from NBOR. Safe to publish.
  [NOT FOR PUBLICATION UNTIL PUBLICATION WORKFLOW EXISTS]
```

### E. Reviewer Queue View (Grouped by Gap)

```
📋 REVIEW QUEUE — GROUPED BY GAP TYPE

🔴 MISSING ENTITY (8 items)
  SJC-NBOR-20260704-0001 — St. Thomas Island cell tower (new entity)
  SJC-NBOR-20260704-0006 — Canopy Shores PUD (new entity)
  SJC-NBOR-20260704-0007 — Daily's Place (new entity)
  SJC-NBOR-20260704-0008 — Bushrangers Brewery (new entity)
  SJC-NBOR-20260704-0009 — Bushrangers Brewery (same entity)
  SJC-BCC-20260120-0004 — Flagler Estates (new entity)
  SJC-BCC-20260120-0012 — Deerfield Estates (new entity)
  SJC-BCC-20260120-0017 — Summer Haven (new entity)

🔴 MISSING LOCATION (all 9 CDD items + 140 county_wide items)
  Most items have no community or geographic detail.
  Many NBOR items have district info (_district field) not used.

🟡 POSSIBLE RELATIONSHIP (4 clusters)
  SR 207 WRF: SJC-UTIL-20260603-0003 ↔ SJC-CN-20260626-0001
  Phase III Water: SJC-UTIL-20260603-0001 ↔ SJC-CN-20260603-0005
  Bushrangers: SJC-NBOR-20260704-0008 ↔ SJC-NBOR-20260704-0009
  NBOR duplicate: 2026-06-08 copy ↔ 2026-06-26 copy

🟡 CANDIDATE CLAIM (20 items)
  See Section 6 — all 20 candidate claims need review

🟢 PUBLICATION READY (83 items marked verified)
  These have been reviewed and confirmed.
  No publication workflow exists to actually publish them.
```

---

## Section 10 — Proposed Structured Before/After Examples

### Example 1: NBOR Public Hearing (SJC-NBOR-20260704-0001)

**Current:**
```yaml
item_id: SJC-NBOR-20260704-0001
title: SUPMAJ 2025000029 St. Thomas Island Parkway Cell Tower
summary: "Public hearing: Request for Special Use Permit to allow
          construction of a 180-foot monopole tower in OR zoning."
source_id: sjc_nbor_public_notices
topics: [development, infrastructure]
communities: []
_beat: site_plans_permits_construction
_app_id: SUPMAJ 2025000029
```

**Proposed Enriched:**
```yaml
item_id: SJC-NBOR-20260704-0001
# All current fields preserved...

# Proposed additions:
entity_links:
  - entity_id: (new — St. Thomas Island Cell Tower)
    basis: directly_present          # explicit name in title
  - entity_id: (new — cell tower project)
    basis: llm_extraction            # inferred from hearing purpose

location:
  address: "St. Thomas Island Parkway"  # directly_present
  community_id: null                     # not determinable
  district: null                         # not in NBOR record
  lat_lng: null                          # geocoding needed

event:
  type: public_hearing
  date: 2026-07-23
  status: scheduled
  hearing_type: special_use_permit

milestone:
  project: cell_tower
  status: proposed

claims:
  - text: "180-foot monopole cell tower proposed at St. Thomas Island Pkwy"
    predicate: proposed
    object: 180ft_monopole_cell_tower
    date: 2026-07-23
    confidence: high                  # directly from source
    evidence: item_summary

provenance:
  extraction_method: deterministic_html
  source_event: EVT-NBOR-20260704-0001

review_decision:
  status: pending_review
  publication_ready: false
  review_notes: null
```

### Example 2: BCC Agenda Item (SJC-BCC-20260120-0002)

**Current:**
```yaml
item_id: SJC-BCC-20260120-0002
title: Public Hearing * REZ 2025-11 Nothing Putt Fun
topics: [development, county_government, public_notices]
_action_type: public_hearing
_signal: high_signal
_meeting_date: 2026-01-20
```

**Proposed Enriched:**
```yaml
# Proposed additions:
entity_links:
  - entity_id: (new — Nothing Putt Fun)
    basis: directly_present
  - entity_id: (new — 7250 US 1 North parcel)
    basis: llm_extraction           # address in description

location:
  address: "7250 and 7280 US 1 North"    # directly_present in raw_excerpt
  parcel_size: 3.98_acres                # llm_extraction
  community_id: null

event:
  type: bcc_agenda_item
  date: 2026-01-20
  status: occurred
  meeting: BCC Regular Meeting
  action_type: public_hearing

claims:
  - text: "REZ 2025-11 proposes rezoning 3.98 acres at US 1 North from CN to CHT"
    predicate: proposed_rezone
    subject: "Nothing Putt Fun parcel"
    object: "CN to CHT"
    confidence: high
    evidence: item_text
    deterministically_extractable: true   # address + parcel size from description
```

---

## Section 11 — LLM Opportunity Matrix

| Stage | Item Examples | Expected Input | Expected JSON | Deterministic Pre | Validation | Review | Error Mode | Items Benefiting |
|-------|--------------|---------------|---------------|-------------------|------------|--------|------------|-----------------|
| **Entity extraction** | NBOR + BCC + SJSO items | title + summary + raw_excerpt | [{entity: "Bushrangers Brewery", type: "business", evidence: "title"}] | Extract app_id patterns | Manual verify on sample | Medium | False positives on common words | 150+ (most items) |
| **Entity resolution** | Cross-source SR 207 WRF items | Two entity names | {same: true, confidence: 0.95} | Exact label match | Manual verify | High | Merging distinct entities | 50+ (multi-source items) |
| **Location extraction** | NBOR with addresses in description | raw_excerpt | [{address: "470 SR 207", type: "business", confidence: 0.9}] | Regex for addresses | Manual verify | Low | Missing non-standard formats | 75+ NBOR items |
| **Event extraction** | All items with dates | Full item | {type: "public_hearing", date: "2026-07-23", status: "scheduled"} | _category, _action_type fields | Sample verify | Low | Wrong event type | 150+ (most items) |
| **Milestone extraction** | SR 207 WRF items (2 milestones) | Series of related items | [{date: "2025-12-19", milestone: "approved"}, {date: "2026-06-23", milestone: "operational"}] | Entity grouping by name | Entity timeline review | Medium | Misordered milestones | ~20 (project items) |
| **Claim extraction** | All 20 candidate claims from §6 | title + summary | [{claim: "...", predicate: "approved", object: "$191.8M"}] | _app_id, _action_type | Full register review | **High** | Hallucinated claims | 100+ (substantive items) |
| **Relationship linking** | Water shortage (2 items), SR 207 (2 items) | Two item texts | {relationship: "same_event", confidence: 0.95} | Same topic + date range | Cluster review | High | False linking of separate events | ~20 (cross-source clusters) |
| **Near-duplicate detection** | NBOR Comcast items (multiple identical titles) | Two item texts | {near_duplicate: true, similarity: 0.92} | Same dedupe key base | Threshold tuning | Low | False positives on genuine similar items | 40+ ROW items |
| **News→official linking** | SJC Citizen article + gov NBOR/BCC item | News item + official item | {relationship: "covers_same", official_item: "SJC-NBOR-..."} | Source type filter | Manual verification | **High** | Incorrectly linking unrelated | ~6 (media + gov pairs) |
| **Digest generation** | All items from a period | 10-25 items | {sections: [{topic: "development", items: [...]}]} | Sort by topic + beat | HITL | **High** | Important omissions | All items (weekly) |
| **Social drafting** | Approved items | One item | {post: "⚠️ Water restrictions...", source: "..."} | Filter by urgency | HITL | **High** | Misleading framing | Urgent + high-interest items |
| **NL query interpretation** | All queries from §8 | Natural language | {filters: {community: "silverleaf", topic: "development"}} | Structured query parsing | Query result review | Low | Incorrect filter mapping | All users |

---

## Section 12 — Source-Specific Implications

### sjc_nbor_public_notices (75 items, 41%)
**Unique value:** Highest-volume source. Rich structure (app_id, category, date,
district, description, PDF links). Covers road closures, hearings, permits.
**Structure:** HTML tables with app IDs, dates, categories. Description has
zoning codes and details. PDF attachments for full notices.
**Missing:** Exact addresses (some in description), community mapping,
neighborhood impact, developer names.
**Event coverage:** ✅ Full (EVT-NBOR events).
**Strategy:** Keep deterministic. LLM entity extraction from descriptions.
**Retention:** 30-day raw, unbounded normalized.
**Resident use:** Development watch, road closure alerts, public hearing
notifications, utility work tracking.
**LLM value:** Entity extraction (project names, addresses, parcel info).
Deterministic parsing is already excellent for the table structure.

### sjc_bcc_calendar (44 items, 24%)
**Unique value:** Official county decisions — rezonings, budget approvals,
contracts, policy discussions. Highest authority layer.
**Structure:** PDF-text agenda items with action types, signals, meeting dates.
**Missing:** Decisions/votes (only available from minutes, not extracted), fiscal
amounts buried in text, staff recommendations.
**Event coverage:** ✅ Single meeting (Jan 20). Other meetings blocked (broken links).
**Strategy:** PDF extraction deterministic. Claim extraction from items.
**Retention:** 30-day raw, unbounded normalized.
**Resident use:** Development tracking, budget monitoring, policy awareness.
**LLM value:** High — dollar amounts, policy implications, staff recommendations
from agenda item text. Minutes extraction would require LLM.

### sjc_county_news (9 items, 5%)
**Unique value:** Official county announcements. Press releases about projects,
programs, events. High authority.
**Structure:** WordPress blog posts with titles, dates, summaries.
**Missing:** Source events (no parent events). Some items lack _beat and interest_tags.
**Event coverage:** ❌ None — early items pre-date source_event system.
**Strategy:** Manual fetch remains acceptable for volume. Add source_event wrapper.
**Retention:** 14-day raw, unbounded normalized.
**Resident use:** Project updates, program announcements, budget news.
**LLM value:** Medium — summaries are already good. Entity extraction useful.

### sjc_utility_department (8 items, 4%)
**Unique value:** Water restrictions, boil notices, infrastructure projects.
High resident impact. Only urgent items in dataset.
**Structure:** Varied — some structured (date, title), some prose-heavy.
**Missing:** Source events for 6/8 items. Consistent app_id/beat coverage.
**Event coverage:** Partial — 2 recent items have events.
**Strategy:** Daily check during hurricane/drought season. LLM for alert
extraction from unstructured announcements.
**Retention:** 30-day raw, unbounded normalized.
**Resident use:** **Alert-ready.** Water restrictions, boil notices, rate changes.
**LLM value:** High — urgent alert extraction, exemption details, affected areas.

### CDD sources (9 items, 5%, 3 sources)
**Unique value:** CDD governance — meeting notices, elections, assessments.
Direct homeowner financial impact.
**Structure:** Alternative schema (content, topic_classification, resident_interest)
— incompatible with main system.
**Missing:** Review status, urgency, sensitivity, geographic_scope, dedupe key,
source_event linkage.
**Event coverage:** ❌ None.
**Strategy:** Migrate to main schema. Add source_event wrapper. RSS feeds make
automation easy.
**Retention:** 30-day raw, unbounded normalized.
**Resident use:** CDD assessment alerts, board election notices, meeting agendas.
**LLM value:** Low — CDD notices are already structured. Schema migration is
the priority.

### sjso_news_stories (5 items, 3%)
**Unique value:** Public safety, crime, arrests, incidents.
**Structure:** WordPress blog posts with narrative text.
**Missing:** Source events (no parent events). Non-standard metadata (no beat,
no dedupe key, no app_id).
**Event coverage:** ❌ None.
**Strategy:** Human review required. Privacy policy needed for named individuals.
**Retention:** 14-day raw, unbounded normalized.
**Resident use:** Public safety awareness, crime alerts (sensitive).
**LLM value:** Medium — entity extraction for incident types. Privacy concerns
with name extraction.

### st_johns_citizen (6 items, 3%, not in registry as canonical)
**Unique value:** Local media context. Rich resident relevance framing.
Development details unavailable in official records.
**Structure:** Media articles with titles, dates, summaries, source_type field.
**Missing:** Registry entry (not in sources.yaml). Source events. Dedupe keys.
**Event coverage:** ❌ None.
**Strategy:** Decide whether to promote to canonical source. Cross-reference with
official records before any action.
**Retention:** 7-day raw, 180-day normalized (media retention).
**Resident use:** Context and story surfacing. Newsletter feature items.
**LLM value:** High — summarization, entity extraction, relationship linking to
official records.

### sjc_emergency_management (1 item, <1%)
**Unique value:** Seasonal emergency preparedness. Hurricane season context.
**Structure:** Simple — one WordPress-style notice.
**Missing:** Volume (only 1 item). No alert-specific structure.
**Event coverage:** ❌ None.
**Strategy:** Monitor seasonally (June-November). Daily during active storms.
**Resident use:** Hurricane prep, evacuation info, shelter updates.
**LLM value:** Low at current volume. Would become important during active events.

### Inactive Sources (Not Producing Items)

**Most important inactive:**
- `sjc_school_district` + `sjcsd_boarddocs` — Education is a critical gap
  (only 2 items). School boundaries, new schools, board decisions are top
  resident concerns.
- `sjc_development_tracker` — GIS map of active projects. Would provide the
  spatial data SJC currently lacks.
- `sjc_permit_status` — Building permits. Would provide construction pipeline
  before it reaches NBOR.
- `sjc_property_appraiser` + `sjc_tax_collector` — Tax and property data.
  Seasonal millage/TRIM value.
- `nws_jacksonville` — Official weather/hurricane source.

---

## Section 13 — Top 10 Lists

### 10 Most Informative Actual Records

1. **SJC-UTIL-20260603-0001** — Phase III water shortage (only urgent item
   with alert channel, taxonomy gap, cross-source duplicate)
2. **SJC-SL-20260704-0001** — Best resident relevance framing in dataset
3. **SJC-BCC-20260120-0002** — Shows full BCC item structure with rezoning detail
4. **SJC-CN-20260626-0001** — Shows cross-source timeline potential with
   utility item
5. **SJC-NBOR-20260704-0001** — Highest-quality NBOR item (cell tower, specific
   location, clear description)
6. **SJC-NBOR-20260704-0008** — Bushrangers Brewery (shows multi-permit entity)
7. **SJC-SJSO-20260603-0004** — Double murder arrest (high sensitivity,
   privacy boundary)
8. **SJC-UTIL-20260603-0003** — $191.8M project approval (fiscal amount,
   cross-source timeline)
9. **SJC-CN-20260626-0004** — Rejected noise item (shows classification working)
10. **six_mile_creek_cdd-002** — CDD board election (shows CDD governance
    value, also shows schema gap)

### 10 Biggest Structure Gaps Revealed by Actual Data

1. **No entity links on items** — 0/182 items have explicit `tracked_entity_ids`
2. **3 incompatible schemas** — Main, NBOR/BCC, and CDD schemas are not
   interchangeable
3. **CDD items lack all metadata** — No review_status, urgency, sensitivity,
   geographic_scope on 9 items
4. **62 items lack source_event parents** — Early county, SJSO, utility,
   SilverLeaf, emergency, CDD items have no provenance chain
5. **No geographic coordinates** — 0 items have lat/lng, parcel IDs, or
   machine-readable addresses
6. **Communities set on only 13/182 items** — 93% of items have no community
   link despite many having location information in text
7. **No relationship links** — 4 known cross-source clusters are undetected
   by automated logic
8. **Flat arrays instead of relational model** — topics, communities, entities,
   interest_tags are all text arrays, not modeled relationships
9. **NBOR file in wrong directory** — 25 items in 2026-06-08 belong in 2026-06-26
   (same fetch timestamp)
10. **No publication workflow** — 83 verified items have no publishing mechanism

### 10 Strongest Resident-Facing Opportunities

1. **Water restriction alert** — SJC-UTIL-20260603-0001 (urgent, actionable)
2. **SilverLeaf development roundup** — 6 discovery items + NBOR items
3. **CDD governance summary** — 9 CDD items across 3 communities
4. **Weekly development watch** — 25 rezoning/comp_plan/permits items
5. **Monthly BCC decision summary** — 44 agenda items (once extraction resumes)
6. **Public hearing calendar** — 25 NBOR hearing items with future dates
7. **Emergency/hurricane preparedness** — Seasonal items + NWS integration
8. **Road work and traffic alert** — NBOR ROW items (need location extraction)
9. **Public safety digest** — SJSO items (need sensitivity review)
10. **Project milestones tracker** — SR 207 WRF cross-source timeline works today

### 10 Strongest LLM Opportunities

1. **Entity extraction from NBOR descriptions** — 75 items with project names,
   addresses, zoning codes in prose
2. **Claim extraction from BCC agenda items** — 44 items with fiscal amounts,
   policy decisions
3. **Location extraction from all items** — 146 items with dates but no
   machine-readable locations
4. **Cross-source relationship linking** — 4 known clusters, likely more undetected
5. **Near-duplicate detection for ROW items** — 40+ Comcast/fiber items with
   near-identical titles
6. **Milestone extraction for project tracking** — SR 207 WRF shows the pattern
7. **News→official record linking** — 6 SilverLeaf items + related NBOR/BCC items
8. **Alert framing from urgent items** — Transform "Phase III" into actionable alert
9. **Community assignment from item text** — Many county_wide items have location
   in description
10. **Digest/summary generation** — All items per period (weekly email)

### 10 Questions Buddy and ChatGPT Should Discuss Next

1. Should the first claim register prototype work with existing verified items?
2. Should entity extraction target the 132+ existing items, or only new items?
3. What is the minimum geographic model for launch? (community names, or lat/lng?)
4. Should CDD items be migrated to the main schema or kept separate?
5. Is the 2026-06-08 NBOR duplicate a one-time error or a recurring storage issue?
6. Which inactive source should produce items first: school district or
   development tracker?
7. Should the first public website be a flat digest or a searchable database?
8. Should social media drafts be generated for all approved items or only urgent?
9. What is the threshold for auto-publishing a source-confirmed item?
10. Should the Phase III water shortage be treated as one event or two items?

---

## Chat Summary

- **Exact dataset counts:** 182 intel items, 18 YAML files, 10 sources,
  15 source events, 132 review queue entries, ~115 unique dedupe keys
- **Strongest actual entity example:** SR 207 Water Reclamation Facility —
  appears in 2 items across 2 sources (utility department + county news),
  at 2 different milestones (approval Dec 2025, operational Jun 2026).
  Entity ENT-INFRA-SR-207-WRF correctly links them in the queue builder.
- **Strongest actual timeline example:** SR 207 WRF — the same entity shows
  a complete lifecycle: approved → operational → serving residents. Only
  2 items, but they demonstrate the full timeline concept.
- **Strongest cross-source relationship:** Phase III Extreme Water Shortage —
  same event reported by sjc_utility_department (SJC-UTIL-20260603-0001) and
  sjc_county_news (SJC-CN-20260603-0005). Both marked urgent. No automated
  linking currently.
- **Most informative item:** SJC-UTIL-20260603-0001 — one of only 2 urgent
  items, proposes water_restrictions taxonomy gap, has alert channel,
  cross-source duplicate, rich resident relevance framing.
- **Most common missing structure:** Geographic/community information. 93% of
  items have no community link. 0% have coordinates.
- **Best resident-facing output supported now:** SilverLeaf community digest
  (6 items, all with single_community scope, rich resident relevance, clear
  lifecycle status). Works immediately with current data.
- **First LLM stage justified by the data:** Entity extraction from NBOR and
  BCC item descriptions. 75 NBOR items + 44 BCC items have project names,
  addresses, and organization names buried in prose. Current keyword matching
  misses partial names and context.
- **Report files created:**
  `docs/reviews/SJC_ACTUAL_DATA_EVIDENCE_PACKET_20260706.md`
  `docs/reviews/SJC_ACTUAL_DATA_EVIDENCE_PACKET_20260706.json`
- **Commit created:** `docs: add SJC actual data evidence packet`
- **Repository status:** Clean. 2 new files committed. No data files,
  schemas, registries, or scripts modified.
