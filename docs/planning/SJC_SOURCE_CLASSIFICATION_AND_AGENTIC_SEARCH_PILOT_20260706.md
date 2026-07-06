# SJC Intel — Source Classification and Agentic Search Pilot Design

**Date:** 2026-07-06
**Purpose:** Correct source classification terminology, analyze the existing
SilverLeaf search prompt, report FHP feasibility findings, and define a bounded
OpenCode-based agentic-search pilot.

---

## Part 1 — Corrected Source Classification

### Terminology

| Term | Definition | SJC Examples |
|------|-----------|-------------|
| **Operational automated** | Runs unattended via a deterministic script | NBOR (`extract_nbor.py`), BCC (`extract_bcc_agenda.py`) |
| **Operational manual** | Requires interactive agent `webfetch` or manual script invocation | County news, SJSO, utility dept, emergency mgmt, CDDs |
| **Registered inactive** | Has a registry entry but zero extractions, no collector code | School district, development tracker, 17 others |
| **Planned** | Listed in product direction but not yet in registry | FHP incidents, FL511, school athletics, business news |

### Full Source Inventory (28 Canonical + 1 Deprecated)

| # | Source ID | Registry Status | Collection Class | Implementation | Runs Unattended? | Tests? | Last Evidence | Lane |
|---|-----------|----------------|-----------------|---------------|-----------------|--------|-------------|------|
| 1 | `sjc_nbor_public_notices` | `verified` | **Operational automated** | `scripts/extract_nbor.py` | ✅ Yes | ✅ 7 tests | 2026-07-04 (25 items) | Durable |
| 2 | `sjc_bcc_calendar` | `verified` | **Operational automated** | `scripts/extract_bcc_agenda.py` | ✅ Yes | ✅ 12 tests | 2026-06-26 (44 items) | Durable |
| 3 | `sjc_county_news` | `active` | **Operational manual** | Interactive `webfetch` | ❌ No | ❌ | 2026-06-26 (4 items) | Durable |
| 4 | `sjso_news_stories` | `active` | **Operational manual** | Interactive `webfetch` | ❌ No | ❌ | 2026-06-26 (1 item) | Durable |
| 5 | `sjc_utility_department` | `verified` | **Operational manual** | Interactive `webfetch` | ❌ No | ❌ | 2026-07-04 (2 items) | Durable |
| 6 | `sjc_emergency_management` | `verified` | **Operational manual** | Interactive `webfetch` | ❌ No | ❌ | 2026-06-26 (1 item) | Durable |
| 7 | `tolomato_cdd` | `active` | **Operational manual** | Interactive `webfetch` (Hermes backfill) | ❌ No | ❌ | 2026-06-26 (3 items) | Durable |
| 8 | `trout_creek_cdd` | `active` | **Operational manual** | Interactive `webfetch` (Hermes backfill) | ❌ No | ❌ | 2026-06-26 (3 items) | Durable |
| 9 | `six_mile_creek_cdd` | `active` | **Operational manual** | Interactive `webfetch` (Hermes backfill) | ❌ No | ❌ | 2026-06-26 (3 items) | Durable |
| 10 | `st_johns_citizen` | `active` | **Operational manual** | Interactive research, `websearch` | ❌ No | ❌ | 2026-07-04 (6 items, one-shot) | Durable |
| 11 | `sjc_school_district` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 12 | `sjc_development_tracker` | `verified` | **Registered inactive** | None (needs browser) | — | ❌ | Never produced items | Durable |
| 13 | `nocatee_community` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 14 | `sjc_pza_boards` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 15 | `sjc_budget_transparency` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 16 | `sjc_clerk_online_research` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 17 | `sjc_permit_status` | `verified` | **Registered inactive** | None (needs form/API) | — | ❌ | Never produced items | Durable |
| 18 | `sjc_transportation_infrastructure` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 19 | `sjrwmd_watering_restrictions` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 20 | `fdot_district_two_nflroads` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 21 | `nws_jacksonville` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 22 | `sjc_supervisor_of_elections` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 23 | `sjc_property_appraiser` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 24 | `sjc_tax_collector` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 25 | `sjcsd_boarddocs` | `verified` | **Registered inactive** | None (needs browser) | — | ❌ | Never produced items | Durable |
| 26 | `sjcsd_zoning_planning` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 27 | `sjso_social_media` | `verified` | **Registered inactive** | None | — | ❌ | Never produced items | Durable |
| 28 | `sjc_road_closures` | `stale` | **Deprecated** | Aliased to NBOR | — | — | Replaced | — |

**9 operational sources, but only 2 are automated.** The remaining 7 operational
sources require interactive agent work or manual script invocation. The phrase
"10 sources actively producing" is misleading — correct wording is:

> "2 automated collectors, 7 manually collected sources, 17 registered inactive sources"

### Recommended Next Disposition by Collection Class

**Operational manual → operational automated candidates:**
- `sjc_county_news` — WordPress, RSS-like listing page. High volume, high value.
  Write a deterministic extractor script. 1 session.
- `sjc_utility_department` — County WordPress page with sidebar announcements.
  Low volume but high urgency when items appear. Write a deterministic extractor. 1 session.
- `sjso_news_stories` — WordPress/Elementor. Same pattern as county news. 1 session.

**Registered inactive → investigate first:**
- `sjc_school_district` / `sjcsd_boarddocs` — Highest resident-impact gap.
  School board decisions, attendance zones, construction. Browser investigation needed.
- `nws_jacksonville` — Official NWS feed, likely has structured alert feeds.
  Simple HTTP GET.

**Registered inactive → defer:**
- `sjc_development_tracker` — Requires browser automation (GIS map).
  Defer to Phase 2.
- `sjc_permit_status` — Form interaction. Defer.

---

## Part 2 — SilverLeaf Search Prompt Analysis

### Current State

`prompts/silverleaf_search_discovery_task.md` is a Hermes-compatible task prompt
that was never executed. It lists 10 target developments with keywords and
source URLs, drawn entirely from St. Johns Citizen articles.

### Strengths

- Correctly identifies the 10 most relevant SilverLeaf developments
- Provides per-development keywords and suggested source URLs
- Output schema matches intel_item format
- Output file path is prescribed (`data/intel_items/{date}/silverleaf_discovery.yaml`)

### Weaknesses

- **No date filtering** — Would rediscover old articles on every run
- **No deduplication** — No dedupe key generation or prior-items check
- **No match classification** — All results treated equally; no exact/probable/unverified states
- **No geographic relevance rules** — Cannot distinguish SilverLeaf-specific from general county news
- **Search locations are hardcoded** — Not parameterized from a registry
- **No evidence requirements** — No citation or excerpt policy
- **Source type `st_johns_citizen` is not in `registry/sources.yaml`** — The 6 existing SilverLeaf items use this source_id but the source registry does not list it as a canonical monitored source
- **No entity matching** — Discovered items are not linked to existing tracked_entities

### Recommendation: Extract Search Profiles to Data

The search targets should move from the prompt into a structured data file.
The prompt should become a reference to the data, not the sole definition.

**Recommended: `registry/search_profiles.yaml`** (new file, file-authoritative):

```yaml
schema_version: "1.0"
last_updated: "2026-07-06"

search_profiles:
  - profile_id: "sl_retail_publix"
    entity_id: "ENT-RETAIL-PUBLIX-SILVERLEAF"
    display_name: "SilverLeaf Mega Publix"
    cadence: monthly
    sources:
      - domain: "sjcitizen.com"
        search_terms: ["SilverLeaf Publix", "1975 SilverLeaf Parkway grocery"]
      - domain: "sjcfl.us"
        path: "/news/"
        search_terms: ["Publix", "SilverLeaf"]
    date_window_days: 90
    match_rules:
      exact: ["SilverLeaf Publix", "Publix at SilverLeaf", "1975 SilverLeaf Parkway"]
      probable: ["Publix", "SilverLeaf Parkway", "grocery"]
      exclude: ["Publix Nocatee", "Publix St. Augustine"]

  - profile_id: "sl_education_k8"
    entity_id: "ENT-EDU-SILVERLEAF-K8"
    display_name: "SilverLeaf K-8 School"
    cadence: monthly
    sources:
      - domain: "sjcitizen.com"
        search_terms: ["SilverLeaf K-8"]
      - domain: "stjohns.k12.fl.us"
        path: "/zoning/"
        search_terms: ["SilverLeaf", "K-8 QQ"]
    date_window_days: 90
    match_rules:
      exact: ["SilverLeaf K-8", "SilverLeaf school"]
      probable: ["SilverLeaf", "K-8", "elementary"]
      exclude: []

  # ... 8 more profiles for Beach Valley Mini Golf, CR 2209, Harris Teeter,
  #     Nocatee retail, Ascension St. Vincent's, Shores Fine Wine,
  #     Fairfield Inn, Taco Bell
```

The prompt is then updated to reference `registry/search_profiles.yaml` rather
than hardcoding the 10 developments.

---

## Part 3 — FHP Live Incident Feasibility

### Investigation Results

The FHP SmartWebClient page at
`https://trafficincidents.flhsmv.gov/SmartWebClient/CadView.aspx` is a
DevExpress ASP.NET WebForms application with:

- **RSS feed discovered:** `CADrss.aspx` provides structured incident data
  in RSS XML format. Each item includes: incident ID, CAD date, dispatched
  time, arrived time, incident type (code), location text, city, county,
  latitude, longitude, and remarks.
- **County filter:** The dropdown list contains 26 Florida counties.
  **St. Johns County is NOT in the list.** The closest adjacent county is
  Duval (Jacksonville area). St. Johns County may share FHP coverage with
  Duval or may use a different reporting system.
- **Data mechanism:** The grid loads data via ASP.NET AJAX callbacks
  (`grid.cpLocations`). The RSS feed provides a simpler read-only structured
  alternative that does not require ASP.NET postback simulation.

### Classification: Path B / Path D

```
B. Undocumented but stable structured endpoint (RSS feed: YES)
D. ASP.NET stateful postback (grid requires it, but RSS avoids it)

Verdict: Path B for the RSS feed. Path D if the grid columns are needed.
```

### Recommended Implementation Path

**Use the RSS feed** (`CADrss.aspx`) as the primary data source. It returns
standard RSS XML with incident records. This avoids ASP.NET postback simulation.

**Remaining unknowns:**
1. Does the RSS feed accept county filtering parameters? The test with
   `?County=ST.+JOHNS` was inconclusive. Need to test with `?County=DUVAL`.
2. Does FHP cover St. Johns County or is it handled by a different agency?
   The county dropdown does not list St. Johns. This needs verification.
3. What is the RSS feed's retention window? (hours, days)
4. Is there rate limiting or terms-of-service for automated polling?

### Adapter Design Sketch

```python
FHP_RSS_URL = "https://trafficincidents.flhsmv.gov/SmartWebClient/CADrss.aspx"

def fetch_incidents(county_filter=None):
    url = FHP_RSS_URL
    if county_filter:
        url += f"?County={county_filter}"
    resp = urllib.request.urlopen(url, timeout=30)
    feed = xml.etree.ElementTree.fromstring(resp.read())
    incidents = []
    for item in feed.findall('.//item'):
        title = item.findtext('title', '')
        desc_html = item.findtext('description', '')
        pub_date = item.findtext('pubDate', '')
        # Parse CAD Date, Dispatched Time, Arrived Time, Incident Type,
        # Location, County, Latitude, Longitude, Remarks from description
        incidents.append(parse_incident(title, desc_html, pub_date))
    return incidents

def parse_incident(title, desc_html, pub_date):
    # Extract <BR>-delimited fields from description
    # Fields: CAD Date, Dispatched Time, Arrived Time, Incident Type,
    #         Location, District, City, County, Latitude, Longitude, Remarks
    ...
```

### Test Fixture Strategy

- Save one RSS response as `tests/fixtures/fhp_rss_sample.xml`
- Parse with elementtree, extract fields
- Test county filtering, missing fields, and date parsing
- No live network required for tests

---

## Part 4 — Bounded OpenCode Agentic-Search Pilot

### Design Principle

The pilot uses existing OpenCode tools (`websearch`, `webfetch`) and the
existing interactive agent workflow. No new runtime, no autonomous daemon,
no Hermes infrastructure.

Both discovery modes share a common output schema and review boundary.

### Common Output Schema

```yaml
# Written to data/intel_items/{YYYY-MM-DD}/agentic_search_results.yaml
search_run:
  run_id: "SRCH-{YYYYMMDD}-{NNNN}"
  initiated_by: sjc-intel-architect
  mode: scheduled | event_triggered
  profile_ids: [list of search_profile IDs searched]
  started_at: "{ISO datetime}"
  completed_at: "{ISO datetime}"

results:
  - candidate_id: "CAND-{YYYYMMDD}-{NNNN}"
    profile_id: "sl_retail_publix"
    entity_id: "ENT-RETAIL-PUBLIX-SILVERLEAF"
    search_source: "sjcitizen.com"
    url: "https://sjcitizen.com/..."
    title: "..."
    snippet: "..."        # excerpt from search result or page
    published_at: "{date}"
    retrieved_at: "{ISO datetime}"
    match_class: exact | probable | related | unverified | no_match
    evidence:              # required for exact and probable
      - field: "article_text"
        excerpt: "..."
    duplicate_of:          # optional — item_id if already in system
    notes: ""
    review_status: pending_review

summary:
  profiles_searched: 3
  total_results: 5
  by_match_class:
    exact: 1
    probable: 2
    related: 1
    unverified: 1
    no_match: 0
```

### Scheduled Discovery Pilot

**Trigger:** Human starts an OpenCode task.
**Input:** `registry/search_profiles.yaml` (subset — start with 3 profiles).
**Tool:** OpenCode `websearch` (for initial discovery), `webfetch` (for
content retrieval).
**Output:** `data/intel_items/{date}/agentic_search_results.yaml` with
candidates.
**Review:** `sjc-intel-architect` reviews candidates, promotes to intel_items
by writing to the appropriate YAML file.
**Log:** Written to `logs/agents/sjc-intel-architect/{date}_agentic_search.md`.

**Session brief template:**

```
Session: Agentic Search Pilot — Scheduled Discovery
Profiles: sl_retail_publix, sl_education_k8, sl_recreation_minigolf
Cadence: First run — catch up. Future runs: monthly.

Steps:
1. Read registry/search_profiles.yaml
2. For each profile:
   a. websearch each search term (site-restricted query)
   b. For each promising result, webfetch the URL
   c. Classify match as exact/probable/related/unverified
   d. Record in output schema
3. Write results to data/intel_items/{date}/agentic_search_results.yaml
4. Log any already-known items as duplicates
5. Report findings

Do not:
- Write intel_items directly (review first)
- Search outside the profile list
- Follow links beyond the first page
- Spend more than 15 minutes on any one profile
```

### Event-Triggered Investigation Pilot

**Trigger:** A deterministic source (NBOR, BCC, county news) produces an item
with a new entity name, unfamiliar project code, or changed date.
**Input:** The triggering intel item's fields (entity name, location, date,
source claim).
**Tool:** OpenCode `websearch`, `webfetch`.
**Output:** Same schema as scheduled discovery.

**Example trigger scenarios:**
- NBOR notice mentions a new developer name → search for their other projects
- BCC agenda item references an unfamiliar project number → search for context
- Utility item mentions a contractor → search for their SJC work history
- County news announces a new school name → search for the naming source
- Sheriff incident mentions a specific location → search for news coverage

**Session brief template:**

```
Session: Agentic Search Pilot — Event-Triggered Investigation
Trigger: {item_id} — {trigger_type}
Entity/Claim: {entity_name or claim}

Steps:
1. Read triggering intel_item fields
2. Formulate search queries:
   - Entity name + "St. Johns County"
   - Entity name + related topic
   - If address: address + context
3. websearch each query
4. webfetch promising results
5. Classify and record in output schema

Do not:
- Treat "no results" as proof entity doesn't exist
- Write intel_items directly
- Search beyond 3 queries
```

### Review Boundary

- `sjc-intel-architect` reviews all candidates before any become intel_items
- Candidates with `match_class: exact` are fast-track: if the source is an
  official government domain and the content is clearly about the tracked
  entity, they can become intel_items immediately
- Candidates with `match_class: probable` require a second source or manual
  verification
- `related` and `unverified` are informational only — no intel_item created
- `no_match` is logged but produces no output — this is a valid outcome

---

## Deliverables Summary

1. **Corrected terminology:** "2 automated, 7 manual, 17 inactive" replaces
   "10 sources actively producing"
2. **Full source inventory:** Table of all 28 + 1 sources with collection class
3. **Search profile recommendation:** Move from hardcoded prompt to
   `registry/search_profiles.yaml`
4. **FHP finding:** RSS feed exists and works. St. Johns County may not be in
   FHP's county list — needs verification before adapter development
5. **Agentic-search pilot:** Two bounded OpenCode-based modes defined with
   common output schema, review boundary, and session brief templates
6. **Next implementation prompt:** See below

### Exact Next Implementation Prompt

```
Part 1: Create registry/search_profiles.yaml with 3 search profiles
(ENT-RETAIL-PUBLIX-SILVERLEAF, ENT-EDU-SILVERLEAF-K8,
ENT-REC-BEACH-VALLEY-MINI-GOLF), following the schema in
docs/planning/SJC_SOURCE_CLASSIFICATION_AND_AGENTIC_SEARCH_PILOT_20260706.md.
Trim the silverleaf_search_discovery_task.md prompt to reference the registry.

Part 2: Fetch and save a sample FHP RSS feed as
tests/fixtures/fhp_rss_sample.xml. Confirm whether County=DUVAL returns
incidents and whether St. Johns appears under any county code.

Part 3: Verify which FHP dispatch area covers St. Johns County by checking
the FHP district map at https://www.flhsmv.gov/florida-highway-patrol/.

Do not build the FHP adapter or full search runtime yet.
```
