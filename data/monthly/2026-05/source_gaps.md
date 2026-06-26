# Source Gaps — May 2026 Backfill

## Gap 1: County Commission BCC Regular Meetings (May 5, May 19)

**Evidence:** BCC calendar shows meetings on first and third Tuesdays (May 5
and May 19). No extracted items for BCC decisions, votes, or hearings. Meeting
agendas and minutes were not directly accessible from the calendar page —
agendas link to external PDFs that require individual parsing.

**Recommendation:** Design a monitor spec for `sjc_bcc_calendar` that checks
for new agenda PDFs and minutes after each meeting date. The calendar page
itself shows upcoming meetings but does not archive past agendas inline.

**Search terms used:** BCC calendar page direct fetch; `site:sjcfl.us "Board of County Commissioners" May 2026`

---

## Gap 2: Planning and Zoning Board Meetings

**Evidence:** No PZA meeting items found for May 2026. The PZA page may not
have a directly scrapable meeting archive. Rezonings and comp-plan amendments
are high-resident-impact items that likely occurred but were not captured.

**Recommendation:** Check `sjc_pza_boards` for meeting schedule and agenda
archive. A direct page inspection of meeting minutes/agendas is needed.

**Search terms used:** `site:sjcfl.us "Planning and Zoning" May 2026`

---

## Gap 3: County Roads — Closure and Project Updates

**Evidence:** The road closures page provides links to the SJC Road Closures
application and FDOT closure map but does not list current closures inline.
No specific May 2026 road closure items were discovered.

**Recommendation:** The road closures page appears to be a landing page, not a
listing. The actual road closure data may live in the SJC Neighborhood Bill of
Rights application or require API access. Direct page scraping of the road
closure application may be needed.

**Search terms used:** Direct fetch of `sjcfl.us/road-closures/`

---

## Gap 4: FDOT District Two and NFLRoads — May 2026 Projects

**Evidence:** No FDOT or NFLRoads items found for May 2026. State road projects
on SR 16, CR 210, and US 1 are likely ongoing but were not captured.

**Recommendation:** FDOT's page is a district landing page. Active projects may
be on separate project-specific pages. NFLRoads may have a searchable project
database. Direct API or site search needed.

**Search terms used:** `site:fdot.gov "St. Johns" May 2026`

---

## Gap 5: $191M SR 207 Water Reclamation Facility — Follow-up

**Evidence:** The utility department page references a Dec 2025 BCC approval
of Phase 2 of this project. No May 2026 updates were found. Given the scale
($191M), construction updates are likely occurring.

**Recommendation:** Add search terms for SR 207 WRF construction updates.
This may be a recurring beat item.

---

## Gap 6: SilverLeaf, Nocatee, RiverTown — Community-Specific Items

**Evidence:** Community-specific items (SilverLeaf, Nocatee, RiverTown,
Shearwater, TrailMark) were not searched in this first pass because
CDD/community sources were excluded. These communities likely had HOA,
developer, or CDD activity in May 2026.

**Recommendation:** Second-pass backfill should include community/CDD sources.

---

## Gap 7: St. Johns Citizen as Media Context (Limited Use)

**Evidence:** St. Johns Citizen was used for limited context only per scope
rules. The Citizen likely covered several May 2026 stories with more detail
than official press releases, including budget workshops, development
hearings, and community features.

**Recommendation:** Second-pass could include St. Johns Citizen as a
cross-reference source, with consequential claims verified against official
records.

---

## Summary

| Gap | Priority | Source Type | Action |
|-----|----------|-------------|--------|
| BCC meeting decisions | High | Official | Design monitor for agenda/minutes |
| PZA meetings | High | Official | Inspect meeting archive page |
| Road closures | High | Official | Find data source (app/API) |
| FDOT projects | Medium | Official | Deeper search of FDOT pages |
| SR 207 WRF updates | Medium | Official | Add recurring search term |
| Community/CDD items | Medium | Community | Second pass |
| Local media context | Low | Media | Second pass if needed |
