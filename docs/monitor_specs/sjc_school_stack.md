# Monitor Spec: `sjc_school_stack`

## 1. Source Identification

- **Source family:** `school_stack`
- **Member sources:**
  - `sjc_school_district` (main district website — WordPress portal)
  - `sjcsd_boarddocs` (Board agenda and document management system)
  - `sjcsd_zoning_planning` (attendance zones, new schools — static pages)
- **Primary URL:** `https://www.stjohns.k12.fl.us/`
- **Source types:** wordpress_portal, government_portal

## 2. Homeowner Relevance

**VERY_HIGH.** School quality, attendance zones, capacity, safety, and bond
issues directly affect property values, family decisions, and daily life.
The May 2026 backfill found 10 school items — the most from any source
family.

## 3. Proven Signal from May 2026 Backfill

| Item | Date | Signal Type |
|------|------|-------------|
| St. Johns Compass program launch | May 26 | **High-impact** — new educational access program |
| Programs of Choice space-available | May 27 | **High-impact** — enrollment deadline for families |
| Student Code of Conduct survey results | May 27 | Medium — policy update |
| Internet safety podcast (State Attorney) | May 21 | Low — awareness content |
| Surtax/millage funding confirmation | May 18 | **High-impact** — tax/funding signal |
| Family Tech Toolkit sessions | May 29 | Low — routine event |
| A-grade maintenance | May 21 | Medium — reputation signal |
| STAR Awards | May 26 | Noise — recognition |
| CTE Awards | May 1 | Noise — recognition |
| SAHS graduation | May 20 | Noise — annual event |
| School Board meeting (May 12) | May 12 | Medium — governance signal |
| All Access video series | May 22 | Noise — PR content |

**Pattern:** ~40% high-impact signal, ~30% medium, ~30% noise (awards,
graduations, routine PR). The monitor must filter aggressively.

## 4. Source URLs

| Page | URL | Purpose |
|------|-----|---------|
| District homepage | `https://www.stjohns.k12.fl.us/` | Primary — news feed + events + videos |
| BoardDocs | `https://www.boarddocs.com/fl/stjohns/Board.nsf/Public` | Meeting agendas, packets, votes |
| Attendance zoning | `https://www.stjohns.k12.fl.us/zoning/` | Zone changes (static; check periodically) |

## 5. Monitor Cadence

**Weekly, with daily checks around Board meeting dates.**

School Board meetings occur approximately twice monthly (2nd and 4th Tuesdays).
The week before and after each meeting is the highest-signal period.

- **Weekly (baseline):** Scan district homepage for new items. Review BoardDocs
  for new agenda postings.
- **Meeting-week (daily):** Check BoardDocs 2 days before and 2 days after
  each Board meeting for agenda publications and minutes/votes.
- **Seasonal adjustments:** Higher frequency during budget season (Jul-Sep),
  attendance zone changes (spring), and legislative sessions.

## 6. Extraction Approach

### A. District Homepage (sjc_school_district)

The homepage is a WordPress portal with multiple content sections:

1. **News feed** — scrollable list of headlines with dates. Extract title,
   date, summary (first sentence or two), and link.
2. **"In other news"** section — linked headlines from external media.
   Extract title, source name, date. Tag as `verification_status: unverified`
   since these are media references, not district-authored content.
3. **Video archive** — "All Access" and other video posts. Extract title,
   date, description. Tag as low-signal unless topic is substantive
   (budget, safety, zoning).
4. **Meeting notices** — event announcements for School Board meetings.
   Link to BoardDocs for full extraction.

### B. BoardDocs (sjcsd_boarddocs)

BoardDocs is a document management system. Extraction approach:

1. **Check for new agenda postings** — compare against last-checked date.
2. **For each new meeting** with published agenda, extract:
   - Meeting date and type (regular, workshop, special)
   - Agenda items (titles and descriptions from packet)
   - Key action items: votes, approvals, public hearings
3. **Flag for human review** items involving: budget approvals, rezoning
   recommendations, policy changes, safety/security, personnel matters.

**Challenge:** BoardDocs is a complex web application. Full extraction may
require browser automation or API inspection. Start with surface-level
agenda metadata; expand to packet content as capability grows.

### C. Attendance Zoning (sjcsd_zoning_planning)

Static page. **No routine extraction needed.** Check manually once per month
for zone map or boundary changes. Changes are rare but high-impact when they
occur.

## 7. Signal vs. Noise Filtering

This is the most important part of the school stack monitor. The district
homepage produces many items. Not all are worth extracting.

### High-Signal Items (always extract)

| Topic | Examples | Beat |
|-------|----------|------|
| Attendance zone changes | New boundaries, school openings | `school_capacity` |
| School capacity / crowding | Enrollment numbers, portable classrooms | `school_capacity` |
| Budget / funding | Millage, surtax, legislative funding, shortfalls | `taxes_exemptions_trim_vab` |
| Safety / security | Drills, incidents, policy changes | `public_safety_livability` |
| New school construction | Groundbreakings, openings, planning | `school_capacity` |
| Board policy changes | Code of Conduct, curriculum, personnel | `school_capacity` |
| Rezoning / DRI impact | Development-related school impacts | `rezoning_comp_plan_dri` |

### Medium-Signal Items (extract with `urgency: ongoing`)

| Topic | Examples | Beat |
|-------|----------|------|
| Program announcements | St. Johns Compass, Programs of Choice | `school_capacity` |
| Survey results | Public feedback, community input | `local_government_budget_procurement` |
| School grades / rankings | A-grade maintenance, state rankings | `property_values_market` |
| Grant awards | Funding for specific programs | `local_government_budget_procurement` |

### Low-Signal / Noise Items (skip unless they trend)

| Topic | Examples | Why Skip |
|-------|----------|----------|
| Awards / recognition | STAR Awards, CTE Awards employee of month | Annual cycle; no resident impact change |
| Graduation ceremonies | Per-school graduations | Annual cycle; predictable |
| All Access video series | Superintendent school visits | PR content; rarely contains actionable info |
| Community events (routine) | Book fairs, spirit nights | Better captured by community events sources |
| Student spotlights | Individual student achievements | Low resident-impact; privacy concern |

### Filtering Rule

When in doubt, extract the item with `recommended_channels: ["internal_only"]`.
It's better to have a low-signal item in the archive than to miss a high-signal
one. The editorial review queue can bulk-dismiss noise.

## 8. Dedupe Strategy

- **Within school stack:** Dedupe across `sjc_school_district` and
  `sjcsd_boarddocs` by title + date. The same Board meeting may appear in
  both the district news feed and BoardDocs. Keep one canonical item.
- **External media references:** The "In other news" section links to media
  coverage. Extract only the reference, not the full article. Tag as
  `source_id: sjc_school_district` with a note about the external source.
- **Item ID prefix:** `SJC-SCH-{YYYYMMDD}-{NNNN}`

## 9. Classification Defaults

| Field | Default | Override When |
|-------|---------|---------------|
| `topics` | `["education"]` | Budget → add `taxes`; Safety → add `public_safety`; Zoning → add `development` |
| `communities` | `[]` (countywide) | Item names specific community or school |
| `geographic_scope` | `county_wide` | School-specific item → `single_community` |
| `urgency` | `ongoing` | Enrollment deadline → `timely`; Safety incident → `urgent` |
| `verification_status` | `source_confirmed` | External media refs → `unverified` |
| `sensitivity` | `low` | Safety, personnel, or legal matters → `medium` or `high` |
| `review_status` | `pending_review` | Always |

## 10. Resident-Interest Defaults

| Item Type | primary_topic | interest_tags | affected_audiences |
|-----------|---------------|---------------|-------------------|
| Zone change | `education` | `["school_zones", "property_values"]` | `["parents", "homeowners"]` |
| Budget/funding | `education` | `["cost_impact", "quality_of_life"]` | `["parents", "residents", "homeowners"]` |
| Safety/security | `public_safety` | `["safety_concern", "school_zones"]` | `["parents", "students", "nearby_residents"]` |
| Program announcement | `education` | `["quality_of_life"]` | `["parents", "students"]` |
| School grade | `education` | `["property_values", "quality_of_life"]` | `["parents", "prospective_movers", "homeowners"]` |
| New school | `education` | `["school_zones", "development_watch", "property_values"]` | `["parents", "homeowners", "prospective_movers"]` |

## 11. Sensitivity / Privacy Rules

- **Student safety incidents:** `human_review_required: true`. Do not publish
  details that could identify individual students.
- **Personnel matters:** `sensitivity: medium` or `high`. Flag for human review.
- **Budget shortfalls:** `sensitivity: medium`. Factual but potentially
  controversial.
- **Awards/recognition:** No special handling. Low sensitivity.
- **External media references:** Verify consequential claims against district
  official sources before publishing.

## 12. Expected Failure Modes

| Failure Mode | Handling |
|-------------|----------|
| BoardDocs authentication required | Try public access first; if gated, note and skip |
| Agenda PDF too large to parse | Extract metadata only; flag for manual review |
| Homepage structure changes (WordPress update) | Flag for architect; update extractor |
| Video-only content (no text) | Use video title + description only; low signal |
| "In other news" links stale or broken | Skip individual broken links; report count | 

## 13. Hermes Readiness

**PARTIAL.** The district homepage (sjc_school_district) is ready for Hermes
with `prompts/known_source_monitor_task.md`. BoardDocs needs browser automation
or API inspection for full extraction. Zoning pages are static — manual check.

## 14. Browser/PDF/Manual Requirements

- **Browser automation:** BoardDocs agenda packets may need browser automation
  for full item extraction.
- **PDF parsing:** Agenda packets are PDFs. Start with surface-level metadata;
  add full PDF parsing later.
- **Manual review:** Required for safety, personnel, and legal items. Also
  recommended for the first month to calibrate signal/noise filtering.

## 15. First Pilot Recommendation

1. **Week 1:** Run manual pilot on district homepage only. Extract all items.
   Classify each as high/medium/low signal. Validate filtering rules.
2. **Week 2:** Automate homepage extraction. Add BoardDocs metadata check
   (meeting dates, agenda existence — not full agenda content).
3. **Week 3:** Run full automated pilot. Review output against signal/noise
   rules. Adjust filtering thresholds.
4. **Month 2:** Add BoardDocs agenda item extraction if feasible. Add
   zoning page monthly check.
