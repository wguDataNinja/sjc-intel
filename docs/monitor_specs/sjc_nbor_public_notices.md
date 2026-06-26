# Monitor Spec: `sjc_nbor_public_notices`

> **2026-06-08 update:** Source renamed from `sjc_road_closures` to
> `sjc_nbor_public_notices`. The NBOR application is far broader than road
> closures — it covers hearings, utility permits, rezonings, and more.
> The old `sjc_road_closures` landing page was a dead end; the real data
> lives in the NBOR web app.

## 1. Source Identification

- **source_id:** `sjc_nbor_public_notices` (formerly `sjc_road_closures`)
- **Name:** Neighborhood Bill of Rights Public Notices
- **Primary URL:** `https://webapp.sjcfl.us/webnews/NBRscreend.aspx`
- **Landing page:** `https://www.sjcfl.us/road-closures/`
- **Source type:** ASP.NET WebForms (server-side rendered HTML)
- **Source family:** `roads_transportation_stack` / `planning_development_stack`
- **Companion sources:** `sjc_transportation_infrastructure`, `fdot_district_two_nflroads`

## 2. Homeowner Relevance

**VERY_HIGH.** Road closures, construction detours, and traffic projects
directly affect daily commutes, school drop-offs, emergency response times,
and quality of life for every SJC resident. The May 2026 backfill found
**zero** road closure items — the biggest operational gap, now closed.

## 3. Proven Signal from May 2026 Backfill

**No items extracted** during the backfill — the old `sjc_road_closures`
landing page was a dead end linking to an external app. The NBOR application
was discovered and extracted in a subsequent investigation (2026-06-08),
yielding 25 records across 4 categories in a single page fetch.

## 4. Source URLs

| Page | URL | Purpose |
|------|-----|---------|
| NBOR web app (primary) | `https://webapp.sjcfl.us/webnews/NBRscreend.aspx` | All data — plain HTML |
| Road Closures landing (entry) | `https://www.sjcfl.us/road-closures/` | Entry point only |
| FDOT Closure Map | `https://northeastfloridatraffic.com/live-traffic-camera-map/` | Secondary |
| Transportation & Infrastructure | `https://www.sjcfl.us/departments/transportation-development-division/` | Project pipeline context |

## 5. Monitor Cadence

**Daily.** The NBOR app updates as new notices are filed. Check daily for
new ROW entries (road closures, utility work) and upcoming meetings.

## 6. Extraction Approach — Structured HTML Parser

The NBOR app renders server-side as plain ASP.NET WebForms HTML.
**No browser automation, no JavaScript execution, no Camoufox, no auth needed.**
A simple HTTP GET returns the full current dataset in structured HTML tables.

A working extractor exists at `scripts/extract_nbor.py`.

### Extraction Steps

1. **HTTP GET** `https://webapp.sjcfl.us/webnews/NBRscreend.aspx`
2. **Locate the data section** — between `<!--end Header row-->` and
   `Records per page` markers in the HTML.
3. **Split by `<hr class="mt-0">`** to isolate individual rows.
4. **Parse each row** for columns:
   - `col-sm-12 col-md-6` → Project name (title in `<strong>`, description after `<br/>`, PDF links in `<ul>`)
   - `col-sm-12 col-md-2` → District(s)
   - `col-sm-12 col-md-2` → Category (ROW or Meeting)
   - `col-sm-12 col-md-2` → Notice date
5. **Normalize** into intel_item schema.

### Classification Mapping

| NBOR Category | Beat | Topics |
|---------------|------|--------|
| ROW (road closure/drainage) | `roadwork_traffic` | transportation, infrastructure |
| ROW (utility company) | `utilities_water` | infrastructure, environment |
| ROW (construction/site work) | `site_plans_permits_construction` | development, infrastructure |
| Meeting (rezoning) | `rezoning_comp_plan_dri` | development, county_government, public_notices |
| Meeting (variance/PUD/CPA) | `rezoning_comp_plan_dri` | development, county_government, public_notices |
| Meeting (special use permit) | `site_plans_permits_construction` | development, infrastructure |

### Dedupe Key Strategy

Primary: `source_id + category + app_id/permit_number + date`
Fallback: `source_id + category + normalized_title + date`
Final: SHA256 hash of raw row text

## 7. Dedupe Strategy

- **Primary key:** NBOR category + app_id/permit number + notice date
- **Secondary key:** Normalized title + category + date
- **Cross-source:** The same project may appear in NBOR + county news.
  Keep one canonical item with supporting sources.
- **Item ID prefix:** `SJC-NBOR-{YYYYMMDD}-{NNNN}`

## 8. Classification Defaults

| Field | Default | Override When |
|-------|---------|---------------|
| `topics` | `["transportation", "infrastructure"]` | Meeting → development, county_government; Utility → environment |
| `communities` | `[]` (countywide) | Description names specific location |
| `geographic_scope` | `county_wide` | Specific road/neighborhood named |
| `urgency` | `ongoing` (ROW) / `timely` (Meeting) | — |
| `verification_status` | `source_confirmed` | Always for official source |
| `sensitivity` | `low` | Controversial hearing → medium |
| `review_status` | `pending_review` | Always |

## 9. Resident-Interest Defaults

| Item Type | primary_topic | interest_tags | affected_audiences |
|-----------|---------------|---------------|-------------------|
| Road closure | `transportation` | `["traffic_impact", "safety_concern"]` | `["commuters", "nearby_residents"]` |
| Utility ROW work | `infrastructure` | `["utility_impact", "quality_of_life"]` | `["residents", "nearby_residents"]` |
| Zoning hearing | `development` | `["development_watch", "property_values"]` | `["homeowners", "prospective_movers"]` |
| Rezoning | `development` | `["development_watch", "property_values"]` | `["homeowners", "residents"]` |
| Construction permit | `development` | `["development_watch", "quality_of_life"]` | `["residents", "nearby_residents"]` |

## 10. Sensitivity / Privacy Rules

- Road closures and ROW permits are factual, low-sensitivity information.
- Public hearings (zoning, rezonings, variances): factual — agenda item
  descriptions are public record.
- Project contacts are public officials — store only if relevant.
- No private individual information present in NBOR records.
- Controversial hearings (denials, appeals): flag `sensitivity: medium`.

## 11. Expected Failure Modes

| Failure Mode | Handling |
|-------------|----------|
| NBOR app returns non-200 | Block with error; retry next cycle |
| ASP.NET viewstate expired | Refresh session; retry |
| No records in current view | Complete with zero items; normal for clear days |
| App structure changes (new columns) | Flag for architect; update parser |
| PDF link broken | Skip individual link; log warning |
| Date filtering postback not working | Use default current view only |

## 12. Hermes Readiness

**YES — ready for Hermes daily monitoring.** The NBOR app renders server-side
as plain HTML. The extractor `scripts/extract_nbor.py` is a single-file Python
script with no dependencies beyond stdlib. HTTP GET + HTML parsing only.

The extractor has been tested against the live page and fixture, producing
25 normalized records across 4 classification categories.

## 13. Browser/PDF/Manual Requirements

- **No browser automation needed.** The NBOR app renders server-side as plain HTML.
- **PDF links** are included in each row; the extractor captures and absolutizes
  them. PDF content extraction is not needed — listing metadata is sufficient.
- **Date filtering** is available via ASP.NET form fields (Start Date, End Date)
  but requires postback. Not yet automated — current-page-only for now.

## 14. Pilot Results

**Investigation complete 2026-06-08.** Extraction script built and tested.

- `scripts/extract_nbor.py` fetches and parses the current NBOR page
- 25 records extracted in the test run (19 ROW, 6 Meeting)
- 4 classification categories mapped
- YAML output matching intel_item schema, stored at `data/intel_items/{date}/`
- Fixture saved at `tests/fixtures/nbor_raw.html`
- Dedupe key strategy: primary = source_id + category + app_id + date

### Next Steps

1. **Run daily.** Extractor is Hermes-ready — plain HTTP GET + HTML parsing.
2. **Add date-filtered extraction** as a future enhancement (ASP.NET postback).
3. **Deprecate old `sjc_road_closures` ID** in registry — replaced by
   `sjc_nbor_public_notices`.
4. **No FDOT or Florida 511 fallback needed** — the NBOR app covers road
   closures directly.

### Extraction Script

`scripts/extract_nbor.py` is available and tested. Run with:

```
python3 scripts/extract_nbor.py
```

Output:
- `data/intel_items/{YYYY-MM-DD}/sjc_nbor_public_notices.yaml` — normalized records
- `tests/fixtures/nbor_raw.html` — raw HTML fixture (updated each run)

### NBOR Data Categories (Confirmed 2026-06-08)

| Category | Records | Beats |
|----------|---------|-------|
| ROW — utility work (Comcast, AT&T, JEA, etc.) | 11 | utilities_water |
| Meeting — zoning variances, rezonings, PUDs | 6 | rezoning_comp_plan_dri |
| ROW — construction/site work permits | 7 | site_plans_permits_construction |
| ROW — road closure (lane closure) | 1 | roadwork_traffic |

### Monitor Cadence

**Daily.** The NBOR app updates as new notices are filed. Check daily for
new ROW entries (road closures, utility work) and upcoming meetings.
