# Monitor Spec: `sjc_utility_department`

**Pilot status:** PASSED 2026-06-03 — 5 items extracted, YAML valid, Hermes-ready
**Daily-readiness:** ✅ Confirmed — source is ready for daily automated monitoring
**Next spec update target:** Add "Featured Department News" sidebar extraction (see §6)

## 1. Source Identification

- **source_id:** `sjc_utility_department`
- **Name:** Utility Department — Water and Boil Notices
- **URL:** `https://www.sjcfl.us/departments/utility-department/`
- **Source type:** government_portal (WordPress with Announcements section)
- **Source family:** `utilities_water_stack`

## 2. Homeowner Relevance

**VERY_HIGH.** Water restrictions, boil notices, outages, reclaimed water
rules, and utility rates directly affect every SJC resident's daily life and
finances. The May 2026 Phase III Extreme Water Shortage was the highest-impact
event discovered in the backfill.

## 3. Proven Signal from May 2026 Backfill

| Item | Date | Type |
|------|------|------|
| Phase III Extreme Water Shortage Declaration | May 13 | Emergency alert / regulatory |
| Free Chlorine Burnout Maintenance (June 1-21) | May 26 | Planned infrastructure |
| $191M SR 207 Water Reclamation Facility (Phase 2) | Ongoing reference | Capital project |
| $4.6M Utilities Lab ribbon-cutting | Reference | Completed project |

Three discoverable items in one month. Source is **productive and reliable**.

## 4. Source URLs

| Page | URL | Purpose |
|------|-----|---------|
| Main utility department | `https://www.sjcfl.us/departments/utility-department/` | Primary — contains Announcements section |
| Boil water alerts | Referenced on main page; links to Alert St. Johns | Secondary — emergency alerts |
| Water conservation | Referenced on main page | Secondary — current restrictions |
| SJRWMD (companion) | `https://www.sjrwmd.com/permitting/` | Companion — drought orders, permits |

## 5. Monitor Cadence

**Daily.** Water alerts (boil notices, outages) and restriction changes can
appear at any time. The main page's Announcements section updates promptly
for urgent items.

## 6. Extraction Approach

The utility department page is a WordPress page with an Announcements section
containing dated entries. Extraction strategy:

1. **HTTP GET** the main utility department page.
2. **Parse the Announcements section** — look for the announcement blocks
   with headings, dates, and "Learn More" links.
3. **For each announcement block**, extract:
   - Title (heading text)
   - Date (check for inline date or date associated with the block)
   - Summary/excerpt (paragraph text following the heading)
   - URL (from "Learn More" link or related button)
4. **Boil water notices:** Check the "Boil Water Alerts" section for active
   notices. If present, extract notice title, date issued, affected areas.
5. **Cross-reference** with the SJRWMD page for watering restriction updates.

6. **Featured Department News sidebar:** After extracting the main
   Announcements section, scan the "Featured Department News" area in the
   right sidebar. Extract the same fields (title, summary, link) for any
   items present there.

   **Pilot lesson (2026-06-03):** The sidebar contained the "SJC Utilities
   2025 Annual Report" which was not captured in the first cycle. Sidebar
   items are typically lower urgency (annual reports, completed projects)
   but may contain resident-interest information.

**WordPress note:** The page is standard WordPress. No JS-rendered content
issues observed. The Announcements section is in the page HTML. The sidebar
is also plain HTML.

## 7. Dedupe Strategy

- **Primary key:** Title + date published
- **Secondary key:** URL (if each announcement has a unique page)
- **Scope:** Within-source only. Do not cross-dedupe with `sjc_county_news`
  (they may cover the same story from a different angle — keep both as
  supporting sources).
- **Item ID prefix:** `SJC-UTIL-{YYYYMMDD}-{NNNN}`

## 8. Classification Defaults

| Field | Default | Override When |
|-------|---------|---------------|
| `topics` | `["infrastructure"]` | Boil notices → add `emergency_alerts`; rates → add `county_government` |
| `communities` | `[]` (countywide) | Notice names a specific community |
| `geographic_scope` | `county_wide` | Area-specific boil notice → `multi_community` or `single_community` |
| `urgency` | `ongoing` | Boil notice → `urgent`; rate change deadline → `timely` |
| `verification_status` | `source_confirmed` | Always for official source |
| `sensitivity` | `low` | Boil notice → `medium`; contamination → `high` |
| `review_status` | `pending_review` | Always |

## 9. Resident-Interest Defaults

| Field | Default | Notes |
|-------|---------|-------|
| `primary_topic` | `infrastructure` | Override to `emergency_alerts` for boil notices |
| `interest_tags` | `["utility_impact"]` | Add `cost_impact` for rate changes; `emergency_awareness` for boil notices |
| `affected_audiences` | `["residents", "homeowners"]` | Add `business_owners` for commercial rate changes |
| `human_review_required` | `false` | Set `true` for contamination, health-related notices |

**Specific RI patterns for this source:**

- **Boil water notice:** `urgency: urgent`, `sensitivity: medium`,
  `interest_tags: ["utility_impact", "emergency_awareness", "safety_concern"]`,
  `human_review_required: true`
- **Water restriction change:** `urgency: timely`,
  `interest_tags: ["utility_impact", "cost_impact"]`,
  `taxonomy_gap: "water_restrictions"`
- **Rate/fee change:** `urgency: timely`,
  `interest_tags: ["cost_impact", "utility_impact"]`
- **Infrastructure project:** `urgency: ongoing`,
  `interest_tags: ["utility_impact", "quality_of_life"]`

## 10. Sensitivity / Privacy Rules

- Boil water notices and health-related items: `human_review_required: true`.
  These affect public health and require editorial review before any
  publication.
- Do not publish specific contamination test results without verification.
- Rate/fee changes are factual and low-sensitivity; can auto-advance.
- No private customer information is present on the public page.

## 11. Expected Failure Modes

| Failure Mode | Handling |
|-------------|----------|
| Page returns non-200 | Block with error; notify operator |
| Announcements section empty | Warn; complete with zero items |
| Announcement date missing | Use discovered_at; flag in notes |
| Boil water alert link broken | Check Alert St. Johns directly |
| Page structure changes | Flag for architect; update extractor |
| SJRWMD companion page changes | Monitor separately (separate spec) |

## 12. Hermes Readiness

**YES — ready for Hermes daily monitoring.** The page is plain HTML, no
JavaScript rendering, no forms, no PDFs. Extraction is straightforward from
visible announcement blocks.

## 13. Browser/PDF/Manual Requirements

**None.** No browser automation needed. No PDF parsing needed. No form
interaction needed for the main page. Boil water alerts link to Alert
St. Johns (external system) — may need separate integration.

## 14. Pilot Results and Next Steps

**Pilot completed:** 2026-06-03 — 5 items extracted, YAML valid, spec
compliance 14/14.

### What the Pilot Confirmed

- Page structure is stable and extractable — Announcements section renders in
  plain HTML with clear headings, dates, and body text.
- Boil water alerts link is present but was inactive during this cycle — the
  fallback path works as designed.
- The Featured Department News sidebar contains additional items (2025 Annual
  Report) that the initial spec scope missed — extraction approach now updated
  in §6.

### Taxonomy Gap Confirmed

The Phase III Extreme Water Shortage item confirmed the need for a
`water_restrictions` topic tag. Existing `environment` + `infrastructure`
topics do not adequately capture water-restriction-specific content.

### Daily Monitoring Readiness

**Ready for daily automation.** Steps for the next phase:

1. **Run automated daily** using `prompts/known_source_monitor_task.md` at
   8:00 AM. Include both Announcements section and Featured Department News
   sidebar in extraction scope.
2. **Week 1 review:** Check for new announcements, boil notices, restriction
   changes, rate updates. Validate sidebar extraction.
3. **Companion monitor:** Add `sjrwmd_watering_restrictions` as a companion
   for drought order updates originating from SJRWMD.
