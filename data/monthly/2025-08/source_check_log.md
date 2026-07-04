# Source Check Log — August 2025 (BF-005-W1 Budget/Millage/TRIM)

**Worker**: BF-005-W1
**Month**: 2025-08
**Checked**: 2026-06-26T13:23:29Z
**Status**: Complete

## Source Stack Results

### 1. Property Appraiser — sjcpa.gov ✅
- **URL**: https://www.sjcpa.gov/
- **Status**: HTTP 200 — Fully operational
- **Checked**: TRIM Notice page, News page, search for TRIM
- **Found**: 
  - TRIM Notice informational page at https://www.sjcpa.gov/trim-notice/ ✅
  - News: Notice of Certification of Tax Roll ✅
  - Site is WordPress-based, search endpoint `/?s=TRIM` works
- **Items extracted**: 2 (SJC-BF-202508-0001, SJC-BF-202508-0002)
- **Notes**: Site uses significant JavaScript (Slider Revolution 7, Ajax Search Pro) making content extraction via curl challenging. Plain HTML navigation reveals key pages.

### 2. BCC Calendar/Agendas — sjcfl.us/bcc-calendar/ ✅ (partial)
- **URL**: https://www.sjcfl.us/bcc-calendar/
- **Status**: HTTP 200 — Operational
- **Checked**: Current calendar view, August 2025 calendar query
- **Found**: Calendar interface operational but predominantly shows current/upcoming events, not August 2025 historical data.
- **Dead URL**: https://www.sjcfl.us/bccmeetings/ — HTTP 404 (stale from sources.yaml)
  - **Archive.org fallback**: https://web.archive.org/web/202508*/https://www.sjcfl.us/bccmeetings/ — Not found
- **Items extracted**: 0 directly from calendar
- **Notes**: Budget hearing dates confirmed via FY2026 Budget page, not the calendar itself. Agenda documents for August 2025 individual meetings not retrievable through this search.

### 3. Tax Collector — sjctax.us ✅ (limited)
- **URL**: https://www.sjctax.us/
- **Status**: HTTP 301/200 — Operational
- **Checked**: Main page, Property Tax section navigation
- **Found**: Property Tax information pages including Millage Rates and Annual Budget sections; however direct sub-pages `/property-tax/millage-rates/` and `/about/annual-budget/` return 404.
- **Items extracted**: 0 directly for August (activity picks up in September after budget adoption)
- **Notes**: Tax Collector site primarily active in October–March for payment collection. August is primarily Property Appraiser's TRIM notice period.

### 4. Budget Transparency — sjcfl.us/2026budget/ ✅
- **URL**: https://www.sjcfl.us/2026budget/
- **Status**: HTTP 200 — Fully operational
- **Checked**: Full page extraction
- **Found**: 
  - FY2026 Budget overview with key highlights ✅
  - Budget calendar PDF at /wp-content/uploads/2025/02/calendar.26.pdf ✅
  - Press release link at /sjc-fy-2026-budget-historic-investments-property-tax-reduction-public-safety-expansion/ ✅
  - Recommended Budget presented July 22, 2025 (antecedent)
- **Dead URL (from sources.yaml)**: https://www.sjcfl.us/budget/ — HTTP 404
  - **Alternative found**: /2026budget/ works perfectly
- **Items extracted**: 2 (SJC-BF-202508-0003, SJC-BF-202508-0004)

## Archive.org Fallback Summary
| Original URL | Fallback | Result |
|---|---|---|
| https://www.sjcfl.us/bccmeetings/ | https://web.archive.org/web/202508*/https://www.sjcfl.us/bccmeetings/ | Not captured |
| https://www.sjcfl.us/budget/ | — | Replaced by live /2026budget/ |

## Overall Assessment
- **4/4 source stacks attempted** ✅
- **4 items extracted by W1 for August 2025** ✅
- **Key findings**: TRIM notices mailed mid-August, FY2026 proposed budget published, budget calendar with Sep 3 & Sep 16 hearing dates confirmed
- **No sensitive items requiring human review** ✅
- **Cross-source duplicates**: None within August month

---

# School Rezoning — Source Check (BF-005-W2)

**Worker**: BF-005-W2
**Month**: 2025-08
**Checked**: 2026-06-26T13:40:00Z
**Status**: Complete

## Source Stack Results

### 1. SJCSD BoardDocs — ❌ (Blocked)
- **URL**: https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public
- **Status**: HTTP 403 Forbidden — Direct scraping impossible
- **Fallback**: https://web.archive.org/web/*/go.boarddocs.com/fl/sjcsd/*
- **Archive.org result**: Generic Wayback Machine JS config page — no specific meeting minutes or agenda PDFs recovered for Jun-Sep 2025
- **Items extracted**: 0
- **Notes**: BoardDocs remains blocked to direct access. Agenda/minutes for June-July 2025 rezoning votes could not be confirmed via this route.

### 2. SJCSD Main Site — stjohns.k12.fl.us ✅ (Primary Source)
- **URL**: https://www.stjohns.k12.fl.us/
- **Status**: HTTP 200 — Fully operational (Tirith WAF blocks certain request patterns but content accessible)
- **Checked**: Homepage, zoning page, new schools page, Hallowes Cove Academy page, enrollment page, calendar page, news section
- **Found**:
  - Hallowes Cove Academy active website at https://www-hca.stjohns.k12.fl.us/ ✅ (K-8, Principal Jessley Hathaway, Hurricanes mascot, extended day program)
  - "Attendance Zoning" mega-menu link at /zoning/ ✅
  - New School Construction page at /newschools/ ✅ (QQ and RR info)
  - Three attendance zoning news articles: /news/attendance-zoning-presentation/, /news/revised-attendance-zoning-proposal/, /news/attendance-zoning-plans/ ✅
  - AI Guidelines PDF uploaded July 2025
  - 2025-2026 Pre-K Enrollment Application available
- **Items extracted**: 4 (SJC-BF-202508-0005 through SJC-BF-202508-0008)

### 3. School Board Meeting Minutes — ❌ (Same BoardDocs block)
- **URL**: https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public
- **Status**: HTTP 403 — Blocked
- **Fallback**: Web archive for boarddocs.com — No actionable data recovered
- **Items extracted**: 0
- **Notes**: Rezoning votes typically occur in Jun-Jul for Aug-Sep implementation. Without BoardDocs access, individual meeting dates and vote records could not be confirmed.

### 4. Google Search (Date-restricted) — Partial
- **Search queries tried**: multiple restricted queries (results not stored)
- **Findings**: Cross-referenced community meeting dates for School QQ/RR naming discussions; external news coverage referenced later (Feb 2026 article by Action News Jax)

## Key Archive.org/Dead URL Results
| Original URL | Fallback | Result |
|---|---|---|
| https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public | https://web.archive.org/web/*/go.boarddocs.com/fl/sjcsd/* | Only generic Wayback config; no meeting data |
| https://www.stjohns.k12.fl.us/news/attendance-zoning-presentation/ | — | Live, content partially retrievable |
| https://www.stjohns.k12.fl.us/news/revised-attendance-zoning-proposal/ | — | Live, content partially retrievable |
| https://www.stjohns.k12.fl.us/news/attendance-zoning-plans/ | — | Live, content partially retrievable |

## Notable Gaps
- BoardDocs minutes for Jun-Jul 2025 rezoning votes not accessible
- Exact first day of school 2025-2026 date not confirmed from calendar page
- Specific rezoning agenda items from school board meetings not extracted
- Hallowes Cove attendance zone boundary map not directly retrieved

## School Rezoning Items Added
- **4 items added** (SJC-BF-202508-0005 through SJC-BF-202508-0008)
- **Topics covered**: new school opening (Hallowes Cove Academy), attendance zoning presentation, revised zoning proposal, final zoning plans
- **No sensitive items requiring human review** ✅
