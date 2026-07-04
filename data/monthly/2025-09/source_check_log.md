# Source Check Log — September 2025 (BF-005-W1 Budget/Millage/TRIM)

**Worker**: BF-005-W1
**Month**: 2025-09
**Checked**: 2026-06-26T13:23:29Z
**Status**: Complete

## Source Stack Results

### 1. Property Appraiser — sjcpa.gov ✅
- **URL**: https://www.sjcpa.gov/
- **Status**: HTTP 200 — Fully operational
- **Checked**: News page, Important Dates page, TRIM Notice page
- **Found**: No September-specific news items (TRIM notices already mailed in August; site content mostly static informational pages)
- **Items extracted**: 0 for September (activity peaks in August for TRIM notice mailing)
- **Notes**: Property Appraiser's role in the budget cycle is largely complete by September after tax roll certification and TRIM mailing.

### 2. BCC Calendar/Agendas — sjcfl.us/bcc-calendar/ ✅ (limited historical)
- **URL**: https://www.sjcfl.us/bcc-calendar/
- **Status**: HTTP 200 — Operational
- **Checked**: September 2025 calendar view (timed out — calendar likely uses JS-loaded events)
- **Found**: Unable to retrieve September 2025 historical events directly from the calendar
- **Items extracted**: 0 directly
- **Notes**: The FY2026 Budget page confirmed both hearing dates (Sep 3 and Sep 16, 2025 at 5:01 PM). Actual meeting agendas/minutes not retrievable through these tools.

### 3. Tax Collector — sjctax.us ✅ (limited)
- **URL**: https://www.sjctax.us/
- **Status**: HTTP 200 — Operational
- **Checked**: Main site, Property Tax information
- **Found**: General property tax information pages
- **Items extracted**: 1 (SJC-BF-202509-0004 — inferred timeline for tax bill mailing)
- **Notes**: Sub-pages for Millage Rates and Annual Budget return 404. Site primarily active for payment processing October–March.

### 4. Budget Transparency — sjcfl.us/2026budget/ ✅ (primary source)
- **URL**: https://www.sjcfl.us/2026budget/
- **Status**: HTTP 200 — Fully operational
- **Checked**: Full page extraction, Press Release page
- **Found**:
  - Confirmation of both public hearing dates ✅
  - Press release: "SJC Adopts $1.8 Billion Fiscal Year 2026 Budget with Historic Investments, Property Tax Reduction, and Public Safety Expansion" ✅
  - Confirmation of first property tax rate reduction since FY2021 ✅
- **Items extracted**: 3 (SJC-BF-202509-0001, SJC-BF-202509-0002, SJC-BF-202509-0003)
- **Notes**: This was the most productive source for September budget/millage content.

## Archive.org Fallback Summary
| Original URL | Fallback | Result |
|---|---|---|
| https://www.sjcfl.us/bccmeetings/ | https://web.archive.org/web/*/sjcfl.us/bccmeetings/* | No snapshots of historical agenda pages found |
| https://www.sjcfl.us/budget/ | — | Replaced by live /2026budget/ |

## Overall Assessment
- **4/4 source stacks attempted** ✅
- **4 items extracted by W1 for September 2025** ✅
- **Key findings**: First public hearing Sep 3, final adoption Sep 16, $1.8B budget adopted with first property tax rate reduction since FY2021
- **No sensitive items requiring human review** ✅
- **Cross-source duplicates**: None within September month (hearing items from budget page vs. press release are distinct)

## Notable Gaps
- Actual meeting agenda PDFs and minutes for Sep 3 and Sep 16 hearings not retrieved
- FY2026 Final Budget Workbook PDF not directly linked on the budget page
- Millage rate resolution document not separately archived

---

# School Rezoning — Source Check (BF-005-W2)

**Worker**: BF-005-W2
**Month**: 2025-09
**Checked**: 2026-06-26T13:40:00Z
**Status**: Complete

## Source Stack Results

### 1. SJCSD BoardDocs — ❌ (Blocked)
- **URL**: https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public
- **Status**: HTTP 403 Forbidden
- **Archive.org fallback**: https://web.archive.org/web/*/go.boarddocs.com/fl/sjcsd/*
- **Result**: No September-specific meeting minutes or rezoning agenda items recovered
- **Items extracted**: 0
- **Notes**: BoardDocs remains inaccessible. Any school board rezoning discussions or votes in September could not be confirmed.

### 2. SJCSD Main Site — stjohns.k12.fl.us ✅ (Primary Source)
- **URL**: https://www.stjohns.k12.fl.us/
- **Status**: HTTP 200 — Operational
- **Checked**: Hallowes Cove Academy page, new schools page, zoning page, enrollment page, news section
- **Found**:
  - Hallowes Cove Academy fully operational with K-8 enrollment open ✅
  - New School Construction page updated with School QQ and School RR details ✅
  - SJCSD community naming meetings referenced for Schools QQ and RR ✅
  - Attendance zoning pages maintained with boundary information ✅
  - Home Education Notice of Intent form dated September 30, 2025 ✅
- **Items extracted**: 4 (SJC-BF-202509-0005 through SJC-BF-202509-0008)

### 3. School Board Meeting Minutes — ❌ (Blocked)
- **URL**: https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public
- **Status**: HTTP 403
- **Fallback**: Archive.org — No actionable results
- **Items extracted**: 0
- **Notes**: September school board meeting minutes for enrollment review or zoning updates not accessible.

### 4. New School Construction page — newschools/ ✅
- **URL**: https://www.stjohns.k12.fl.us/newschools/
- **Status**: HTTP 200 — Fully operational
- **Found**:
  - School QQ: K-8, SilverLeaf (Parcel 29C), 1,500 capacity, completion 2026-2027 SY ✅
  - School RR: K-8, Nocatee Seabrook/Snowden Village, 1,500 capacity, completion 2026-2027 SY ✅
  - Renderings and location maps for both schools ✅
  - "Under Construction" status labels
- **Items extracted**: Referenced in SJC-BF-202509-0006

## Key Archive.org/Dead URL Results
| Original URL | Fallback | Result |
|---|---|---|
| https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public | https://web.archive.org/web/*/go.boarddocs.com/fl/sjcsd/* | No September data recovered |
| https://www.stjohns.k12.fl.us/newschools/ | — | Live, fully operational |
| https://www-hca.stjohns.k12.fl.us/ | — | Live, fully operational |

## Notable Gaps
- School board meeting minutes for September rezoning discussions not accessible
- Exact Hallowes Cove attendance zone boundary map not directly retrieved
- Community input sessions for School QQ/RR naming exact dates not confirmed
- Controlled open enrollment application window dates for 2025-2026 not confirmed

## School Rezoning Items Added
- **4 items added** (SJC-BF-202509-0005 through SJC-BF-202509-0008)
- **Topics covered**: Hallowes Cove inaugural year, School QQ/RR construction update, enrollment/capacity review, community naming engagement
- **No sensitive items requiring human review** ✅
