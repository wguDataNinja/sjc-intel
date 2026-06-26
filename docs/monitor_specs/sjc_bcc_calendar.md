# Monitor Spec: `sjc_bcc_calendar`

## 1. Source Identification

- **source_id:** `sjc_bcc_calendar`
- **Name:** County Commission Calendar
- **Primary URL:** `https://stjohnsclerk.com/board-records/agendas/` (Clerk Board Records)
- **Secondary URL:** `https://www.sjcfl.us/bcc-calendar/` (upcoming meetings only)
- **Source type:** government_portal (WordPress + Clerk document management)
- **Source family:** `county_decision_stack`
- **Companion sources:** GovTV (video archive)
- **2026-06-26 update:** The BCC calendar page is NOT the primary archive. The
  **Clerk Board Records page** (`stjohnsclerk.com/board-records/agendas/`) is
  the correct primary source with full meeting history.

## 2. Homeowner Relevance

**VERY_HIGH.** The Board of County Commissioners is the top elected decision
body for St. Johns County. Their votes affect development approvals, budgets,
tax rates, road projects, utilities, and every major county policy. Missing
BCC decisions was the single biggest gap in the May 2026 backfill — now closed
by the Clerk Board Records extractor.

## 3. Proven Signal from May 2026 Backfill

**No items extracted** during the backfill (calendar page was dead end).
**Post-backfill resolution (2026-06-26):** Clerk Board Records page confirmed
as the real data source. 11 meetings extracted via HTML table parser. 3 meetings
identified with broken agenda links. Agenda PDF naming pattern documented.
Extractor script created at `scripts/extract_bcc_agenda.py`.

## 4. Source URLs

| Page | URL | Purpose |
|------|-----|---------|
| Clerk Board Records (PRIMARY) | `https://stjohnsclerk.com/board-records/agendas/` | Full meeting archive — Agenda PDFs, Minutes PDFs, GovTV links |
| BCC Calendar (secondary) | `https://www.sjcfl.us/bcc-calendar/` | Upcoming meeting schedule only |
| GovTV | `https://www.sjcfl.us/govtv/` | Video archive of meetings |

## 5. Monitor Cadence

**Weekly with pre-meeting and post-meeting intensification.**

BCC meets first and third Tuesdays at 9:00 AM. The monitor has two phases:

### Pre-Meeting Monitor (2 days before each meeting)

- Check calendar for agenda publication
- Extract agenda item titles and descriptions
- Identify public hearings, development items, budget items, contract awards

### Post-Meeting Monitor (2 days after each meeting)

- Check for minutes publication
- Extract votes taken, decisions made, public hearing outcomes
- Cross-reference with GovTV video for major items

### Between Meetings

- Weekly check for new agenda postings, special meeting notices, or
  schedule changes

## 6. Extraction Approach

### Real Data Source (Discovered 2026-06-26)

The BCC calendar page (`sjcfl.us/bcc-calendar`) only shows upcoming meetings
and has no inline agenda data. The **Clerk Board Records page**
(`stjohnsclerk.com/board-records/agendas/`) is the correct primary source —
it has a complete HTML table of all BCC meetings with Agenda PDF, Minutes PDF,
and GovTV links.

### Extraction Script

A working extractor exists at `scripts/extract_bcc_agenda.py`. It:

1. **Fetches** the Clerk Board Records HTML page.
2. **Parses** the meeting table rows using HTML parser.
3. **Extracts** per-meeting: date, Agenda URL, Minutes URL.
4. **Detects broken links** — agenda links that incorrectly point to minutes
   PDFs are flagged. The script attempts the deterministic URL as a fallback.
5. **Downloads** agenda PDFs and **extracts text** using `pypdf`.
6. **Parses** agenda text into individual items by item number.
7. **Classifies** each item by resident-impact signal level and beat.
8. **Normalizes** into intel_item schema (per-item records).
9. **Saves** raw HTML and PDF text fixtures for repeatable parsing.

Dependency: `pypdf` (added 2026-06-26, listed in `requirements.txt`).

### PDF Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Agenda PDF | `MMDDYYarbcc.pdf` | `051926arbcc.pdf` (May 19, 2026) |
| Minutes PDF | `MMDDYYmrbcc.pdf` | `061626mrbcc.pdf` (June 16, 2026) |

### Phase 2 Status (2026-06-26) — PDF Text Extraction Implemented

`pypdf` was installed and integrated. Calibration across two meetings
(Jan 20 and May 19, 2026) produced **75 total agenda items**:
- 59 high-signal (78.7%), 12 medium, 5 low/routine
- 7 resident-interest beats represented
- Section detection handles Regular + Consent agenda numbering
- Numbers >100 are correctly filtered (statutory references)
- Decision: **stay with `pypdf`** — no quality issues; no table-heavy PDFs encountered

Calibration doc: `data/intel_items/2026-06-26/bcc_calibration_notes.md`

Meeting-level metadata is now stored as `source_event` records in
`data/source_events/`. Per-item extraction in `data/intel_items/` links
back via `source_event_id`. See `schemas/source_event.schema.yaml` for
the source_event schema definition.

### What Still Needs Work

1. **Live agenda extraction** — the latest accessible agenda (May 19, 2026)
   could be processed in a future cycle. June 2026 agenda links remain broken.
2. **Per-item classification tuning** — some items may be over-classified as
   high-signal due to keyword matching on routine consent items.
3. **Minutes extraction** — minutes PDFs (`mrbcc`) contain vote tallies and
   decisions. Could be added as Phase 3.

## 7. Dedupe Strategy

- **Across BCC + companion sources:** A single BCC decision may appear in
  the calendar (agenda), the minutes, Clerk records, and GovTV video.
  Dedupe by meeting date + item title.
- **Across county stacks:** A BCC vote on a development project may also
  appear in PZA or Development Tracker records. Cross-source dedupe is
  valuable but complex — start with within-source dedupe.
- **Item ID prefix:** `SJC-BCC-{YYYYMMDD}-{NNNN}`

## 8. Classification Defaults

| Field | Default | Override When |
|-------|---------|---------------|
| `topics` | `["county_government"]` | Development item → add `development`; Budget → add `taxes` |
| `communities` | `[]` (countywide) | Item names specific community or project location |
| `geographic_scope` | `county_wide` | Project-specific → `single_community` or `neighborhood` |
| `urgency` | `timely` (before meeting) / `ongoing` (after) | Decision with deadline → `urgent` |
| `verification_status` | `source_confirmed` | Official agenda/minutes |
| `sensitivity` | `low` | Controversial hearing → `medium`; legal → `high` |
| `review_status` | `pending_review` | Always |

## 9. Resident-Interest Defaults

| Item Type | primary_topic | interest_tags | affected_audiences |
|-----------|---------------|---------------|-------------------|
| Development approval | `development` | `["development_watch", "property_values", "traffic_impact"]` | `["homeowners", "nearby_residents", "commuters"]` |
| Budget / millage | `taxes` | `["cost_impact", "community_trust"]` | `["residents", "homeowners"]` |
| Road project | `transportation` | `["traffic_impact", "quality_of_life"]` | `["commuters", "nearby_residents"]` |
| Public hearing | `public_notices` | `["quality_of_life", "community_trust"]` | `["residents", "nearby_residents"]` |
| Ordinance / policy | `county_government` | `["quality_of_life", "community_trust"]` | `["residents"]` |
| Contract award | `county_government` | `["community_trust"]` | `["residents"]` |

## 10. Sensitivity / Privacy Rules

- **Public hearings** with resident input: factual reporting only. Do not
  editorialize on resident testimony.
- **Development approvals:** factual — project name, location, vote tally.
  Do not speculate on impacts beyond what is stated in agenda materials.
- **Legal matters, litigation, personnel:** `sensitivity: high`.
  `human_review_required: true`.
- **Budget / millage decisions:** factual. Flag for editorial review only
  if controversial.

## 11. Expected Failure Modes

| Failure Mode | Handling |
|-------------|----------|
| Agenda link not yet published | Note "agenda not published"; check again post-meeting |
| Minutes not yet published | Note "minutes pending"; check weekly after meeting |
| Agenda PDF is scanned image | Extract title only; flag for manual review |
| Clerk portal requires search | Skip; note as manual-review gap |
| GovTV video not captioned | Use agenda/minutes as primary; video is supplementary |
| Special meeting called with short notice | Calendar should update; check daily if no regular meeting for 2+ weeks |

## 12. Hermes Readiness

**YES — Phases 1 and 2 are Hermes-ready.** The extractor
`scripts/extract_bcc_agenda.py` now handles both meeting metadata and PDF
text extraction via `pypdf`. It produces 44+ agenda-item intel_items per
meeting cycle. The only gap is broken agenda links (June 2026 meetings),
which require Clerk's office follow-up.

**Phase 3 (minutes extraction)** would require minutes PDF text extraction
but the same `pypdf` dependency applies — no additional tools needed.

## 13. Browser/PDF/Manual Requirements

- **No browser automation needed.** Both the BCC calendar and Clerk Board
  Records pages render as plain HTML server-side.
- **PDF parsing** requires a Python PDF library (PyMuPDF, pdfplumber).
  Not available in current environment. Deferred.
- **Manual review** is recommended for the first 2-3 BCC cycles to validate
  meeting extraction and calibrate resident-interest classification.

## 14. Pilot Results (2026-06-26)

**Extraction pilot passed.** The Clerk Board Records page was confirmed as
the correct primary source. 11 meetings extracted, 3 broken agenda links
detected. Extractor script at `scripts/extract_bcc_agenda.py`.

### Current Capability (Phase 2 Complete)

- 11 meeting-level intel_items + 44 agenda-item intel_items per cycle
- PDF text extraction via `pypdf`
- Agenda item parsing by item number
- Resident-impact classification (high/medium/low/routine)
- Beat and topic mapping using existing taxonomy
- Broken link detection with deterministic URL fallback
- Fixture-based validation (HTML + PDF text)

### What Still Needs Work

1. **Minutes extraction (Phase 3)** — minutes PDFs contain vote tallies.
2. **Per-item classification tuning** — see `bcc_calibration_notes.md` for
   detailed analysis. Current calibration: 78.7% high-signal, which is
   reasonable for BCC agendas dominated by actionable decisions.
3. **Download May 19 agenda live** — PDF is accessible but was processed
   from downloaded file; automated fetch is ready.
