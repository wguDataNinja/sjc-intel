# Backfill Lessons — May 2026

Less learned from the first official-source historical backfill run,
used to inform monitor spec design and future backfill passes.

---

## Sources That Produced Signal

| Source ID | Items Found | Signal Quality | Notes |
|-----------|-------------|----------------|-------|
| `sjc_school_district` | 10 | High (40% signal, 30% noise) | Most productive source; needs aggressive signal/noise filtering |
| `sjc_county_news` | 4 | High | Already has working monitor spec; continue daily |
| `sjc_utility_department` | 3 | High | Newly promoted; ready for daily monitor |
| `sjso_news_stories` | 2 | Medium | Already has working monitor spec; continue daily |
| `sjrwmd_watering_restrictions` | 1 | High | Newly promoted; companion to utility monitor |
| `sjc_emergency_management` | 1 | Low (seasonal) | Pre-hurricane-season messaging; daily in season |
| `sjcsd_boarddocs` | 1 | Medium | Meeting existence confirmed; full extraction not yet done |

## Sources That Failed or Were Thin

| Source ID | Issue | Root Cause | Resolution |
|-----------|-------|------------|------------|
| `sjc_bcc_calendar` | No items | Calendar shows upcoming meetings only; agendas/minutes are PDFs | Design pre/post meeting monitor with PDF extraction |
| `sjc_road_closures` (now `sjc_nbor_public_notices`) | No items (backfill) → 25 records (post-backfill) | Landing page was dead end; NBOR app is the real data source | ✅ CLOSED — NBOR extractor built, 25 records, daily-ready |
| `sjc_pza_boards` | No items | Board listing page; meeting archive not scrapable | Direct inspection of meeting minutes archive |
| `fdot_district_two_nflroads` | No items | District landing page; no per-project updates | Use NFLRoads project-level pages |
| `sjc_transportation_infrastructure` | No items | Division landing page; no dated items | Add project page-level search |
| `sjc_budget_transparency` | No items | Off-season (budget cycle is Jul-Sep) | Activate Jul-Sep; revisit for TRIM season |
| `sjc_permit_status` | No items | Requires form interaction | Deferred — needs browser automation |
| `sjc_clerk_online_research` | No items | Portal-based search | Deferred — needs form interaction |

## Taxonomy Gaps (with Real Evidence)

| Proposed Tag | Evidence | Items | Recommendation |
|-------------|----------|-------|----------------|
| `water_restrictions` | Phase III Extreme Water Shortage — not well covered by existing `environment` or `infrastructure` topics | SJC-BF-202605-0001, SJC-BF-202605-0005 | Promote to canonical topic. Affects watering limits, drought declarations, reclaimed water changes, SJRWMD restrictions. |
| `budget_millage` | School surtax/millage item spans `education` + `taxes` but lacks a specific tax-policy or budget tag | SJC-BF-202605-0011 | Promote to canonical topic. Covers budget workshops, millage, TRIM season, tax-bill implications. |

Both tags were identified as likely gaps in the Deep Research report. They now
have real item evidence. Ready for TAX-002 and TAX-003 evaluation.

## Recommended Next Pilots

| Priority | Source | Spec | Reasoning |
|----------|--------|------|-----------|
| 1 | `sjc_utility_department` | `docs/monitor_specs/sjc_utility_department.md` | Proven signal, daily, easy extraction |
| 2 | `sjc_school_district` + `sjcsd_boarddocs` | `docs/monitor_specs/sjc_school_stack.md` | Highest volume source; needs signal filtering |
| 3 | `sjc_bcc_calendar` | `docs/monitor_specs/sjc_bcc_calendar.md` | Biggest gap; needs PDF approach first |
| 4 | `sjc_nbor_public_notices` | `docs/monitor_specs/sjc_nbor_public_notices.md` | Gap closed — NBOR extractor built, 25 records, daily-ready |

## Source-Family Monitor Patterns Learned

### Easy/Productive Pattern (WordPress + Announcements)

Sources like `sjc_county_news`, `sjc_utility_department`, `sjso_news_stories`
share a pattern:
- WordPress-based with dated news listings or announcement sections
- Plain HTML — no JavaScript rendering
- Headlines visible on main page
- Individual article pages with full content
- Straightforward CSS selector extraction

**Monitor pattern:** Daily HTTP GET → extract featured + sidebar items →
dedupe → classify → output.

### Noisy Portal Pattern (WordPress + Multiple Content Types)

`sjc_school_district` is the example:
- WordPress portal with multiple content sections (news, video, events, media)
- ~40% high-signal, ~30% medium, ~30% noise
- External media references in "In other news" section
- Companion system (BoardDocs) for governance content

**Monitor pattern:** Weekly baseline + daily around Board meetings.
Aggressive signal/noise filtering. Extract all items but tag signal level.
Editorial queue handles noise dismissal.

### PDF-Gated Pattern (Calendar + Agenda PDFs)

`sjc_bcc_calendar` and `sjc_pza_boards` share this:
- Calendar shows meeting dates but not content
- Decisions live in agenda PDFs and minutes PDFs
- PDFs may be text or scanned images
- Clerk portal may require form interaction for historical records

**Monitor pattern:** Weekly pre-meeting check (agenda posted?) + post-meeting
check (minutes published?). PDF extraction for content. Manual review for
scanned documents.

### External-App Pattern (Landing Page + Data Behind App)

`sjc_road_closures` is the example:
- County landing page links to external application
- Real data is in a separate app (Neighborhood Bill of Rights, FDOT map)
- Apps may require JavaScript, browser automation, or have hidden APIs
- Fallback sources exist (FDOT map, Florida 511) but are less complete

**Monitor pattern:** Investigate app first. If accessible, use browser
automation. If not, fall back to alternative sources. Document the gap.

## Recommended Next Actions

1. **Design `sjc_utility_department` monitor** (spec exists; run pilot).
2. **Run `sjc_school_stack` pilot** — start with homepage; add BoardDocs
   metadata extraction.
3. **Investigate SJC Road Closures app** — visit the app URL; determine
   extraction feasibility.
4. **Inspect BCC agenda PDFs** — manually check May 5 and May 19 meeting
   archives to validate the PDF-gated pattern.
5. **Promote taxonomy gaps** — `water_restrictions` and `budget_millage`
   have real evidence.
