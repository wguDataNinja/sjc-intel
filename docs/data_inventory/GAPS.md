# GAPS.md — Data Coverage Gaps Analysis

> Generated: 2026-06-26
> Purpose: Identify what's missing from the SJC_Intel data inventory, why, and what to prioritize next.

---

## 1. Time Periods With No Data

| Time Period | Status | Items | Blocking Issue |
|-------------|--------|-------|----------------|
| **2025 (all months)** | ❌ Not started | 0 | Not backfilled. Aug-Sep 2025 flagged as high priority for TRIM/budget season and school rezoning, but no extractors configured. |
| **Jan 2026** | ⏳ Partial | 44 (retro BCC) | Only Jan 20 BCC agenda extracted. No county news, sheriff, utility, school, or emergency mgmt data for this month. Deferred by design — backfill scope was May+. |
| **Feb 2026** | ❌ Not started | 0 | No extractors. No backfill planned. |
| **Mar 2026** | ❌ Not started | 0 | No extractors. |
| **Apr 2026** | ❌ Not started | 0 | No extractors. |
| **May 2026** | ✅ First pass | 21 | First pass complete (official sources only). Gaps: no local media, no CDD, no development tracker. |
| **June 1–2, 2026** | ❌ Missing | 0 | No coverage at all. NBOR runs started Jun 8, other monitors started Jun 3. Gaps before first monitor date. |
| **June 4–7, 2026** | ❌ Missing | 0 | No coverage between first monitor and NBOR activation. |
| **June 9–25, 2026** | ⏳ Partial | 44 (BCC) | Only BCC Jan 20 agenda retroactively captured. No daily monitoring results between cycles. NBOR was running but results only stored on the extraction date. |

## 2. Source Families With Thin or Missing Coverage

### 🟢 Good Coverage
| Source Family | Coverage | Notes |
|---------------|----------|-------|
| **utilities_water_stack** | ✅ Strong | 30 items across May + June. Covered by NBOR ROW permits, county news, and utility department page. Primary gap: no direct SJRWMD alerts feed. |
| **county_decision_stack** | ✅ Good (BCC) | 57 items across May + June. BCC agenda extractor working (44 items from Jan 20). County news adding 9 items. **June 2026 agenda links broken** — only Jan 20 extracted. |
| **public_safety (sheriff)** | 🟡 Adequate | 7 items across May + June. SJSO news monitor running daily. Volume is source-limited (SJSO publishes ~2-5 stories/month). |

### 🟡 Thin Coverage
| Source Family | Coverage | Issue |
|---------------|----------|-------|
| **planning_development_stack** | 🟡 Partial | 12 NBOR rezoning items in June. No PZA board records from Clerk's website extracted. No direct development tracker data. |
| **permit_construction_stack** | 🟡 Partial | 14 NBOR ROW permit items in June. No building permit data from county portal. |
| **roads_transportation_stack** | 🟡 Partial | 3 items (NBOR roadwork + county news railroad closure). No FDOT or county roads department direct monitoring. |
| **emergency_mgmt** | 🟡 Thin | 2 items total (1 May, 1 June). Emergency management page only checked once. Hurricane season (Jun-Nov) needs daily monitoring. |
| **school_stack** | 🟡 Backfill only | 12 items from May backfill. **No June monitoring**. BoardDocs full extraction not yet implemented. School board agenda items, budget, and rezoning data missing for June. |

### ❌ Missing Coverage
| Source Family | Items | What's Blocking |
|---------------|-------|-----------------|
| **resident_cost_stack** | 0 | Budget page is off-season. No property appraiser or tax collector data extracted. TRIM season (Aug-Sep) is priority window. |
| **cdd_governance_stack** | 0 | Tier 3 sources not promoted to active monitoring. No CDD board agendas extracted. |
| **community_developer_stack** | 0 | Tier 4 sources not promoted. No Nocatee HOA, Ponte Vedra, or other community developer feeds. |
| **local_media_context_stack** | 0 | Deferred. St. Johns Citizen identified as high-value source but no monitor implemented. Media is tip-surfacing context, not primary intel. |

## 3. What's Blocking Each Gap

### Extraction Blockers

| Gap | Blocker | Severity |
|-----|---------|----------|
| June 2026 BCC agendas | Clerk's website has broken agenda links for June 2026 meetings — links point to minutes PDFs instead. Deterministic URL patterns also 404. | 🔴 High — 2 regular BCC meetings (Jun 2, Jun 16) not extractable |
| PZA board records | No extractor configured for Planning & Zoning Agency board records on Clerk's website. | 🟡 Medium |
| School BoardDocs | BoardDocs is a separate document management system. Pending pilot implementation. | 🟡 Medium |
| Development tracker | Interactive GIS map with JS-rendered data layer. Requires browser automation or API discovery. | 🟡 Medium |
| Property appraiser | Government portal with search interfaces. Value increases during tax assessment cycles. | 🔵 Low (off-season) |

### Data Quality Blockers

| Gap | Blocker | Severity |
|-----|---------|----------|
| Missing June 1-2, June 4-7 | No monitors were running before Jun 3 (pilot) or Jun 8 (NBOR). This is a cold-start gap — data was never captured and cannot be recovered retroactively for live sources. | 🔴 Permanent gap |
| School district June data | School district monitor pilot started but not yet running daily/weekly. May backfill showed 12 items but June has none. | 🟡 Medium |
| Emergency management frequency | Currently checked ad-hoc. Should be daily during hurricane season (June-November). | 🟡 Medium |

### Strategic Gaps (Deferred)

| Gap | Rationale | ETA |
|-----|-----------|-----|
| Local media | Deferred — media is tip-surfacing, not primary intel. Adding stjohnscitizen.com would increase volume but add uncertainty. | Not scheduled |
| CDD governance | Tier 3 sources not promoted. Requires source evaluation and extractor development. | Not scheduled |
| Community developer | Tier 4 sources. Lowest priority. | Not scheduled |

## 4. Recommendations

### Immediate (This Week)

1. **Fix BCC June 2026 agenda links** — Contact Clerk's office or find alternative access. Two meetings (Jun 2, Jun 16) blocked. Highest-value extraction gap.
2. **Add sjc_emergency_management to daily cycle** — Hurricane season started Jun 1. Should run daily through November.
3. **Activate school district weekly monitor** — No June school data at all. BoardDocs pilot start is overdue.

### Short-Term (Next 2 Weeks)

4. **Extract May 19, 2026 BCC agenda** — Confirmed working agenda link. Would add ~40 items and validate the BCC extractor on a second meeting.
5. **Build PZA board records extractor** — Planning & Zoning Agency agendas are the second-most important official decision stack after BCC.
6. **Add weekly development tracker check** — Even partial static-page extraction would add value.

### Medium-Term (Next Month)

7. **Backfill Aug-Sep 2025** — High priority for TRIM/budget season school rezoning context. Extractors need to exist first.
8. **NBOR daily automation** — Already daily-ready. Ensure no gaps between cycles.
9. **Resident cost stack pilot** — Property appraiser and tax collector pages. Most useful during TRIM season (Aug-Sep).

### Long-Term

10. **Local media integration** — Only after official stacks are complete.
11. **CDD and community developer stacks** — Lowest priority. Useful for hyperlocal Nocatee/Ponte Vedra coverage but not needed for county-wide intel.

---

## 5. Gap Closure Tracker

| Gap ID | Description | Priority | Owner | Status |
|--------|-------------|----------|-------|--------|
| GAP-001 | June 2026 BCC agenda links broken | P0 | sjc-intel-architect | 🔴 Blocked |
| GAP-002 | Emergency mgmt not in daily cycle | P1 | sjc-intel-source-watch | 🟡 Open |
| GAP-003 | School district June monitoring | P1 | sjc-intel-source-watch | 🟡 Open |
| GAP-004 | May 19 BCC agenda not extracted | P2 | hermes-bcc-worker | 🟡 Open |
| GAP-005 | PZA board records not extracted | P2 | sjc-intel-architect | 🔵 Planned |
| GAP-006 | Development tracker not monitored | P3 | sjc-intel-source-watch | 🔵 Planned |
| GAP-007 | Pre-May 2026 data not backfilled | P4 | sjc-intel-architect | 🔵 Deferred |
| GAP-008 | Aug-Sep 2025 budget/TRIM season | P2 | — | 🔵 Planned |
