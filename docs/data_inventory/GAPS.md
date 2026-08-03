# GAPS.md — Data Coverage Gaps Analysis

> Generated: 2026-06-26
> Updated: 2026-08-02 (closeout)
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
| **July 1–3, 5–31, 2026** | ❌ Missing | 0 | No daily monitoring runs recorded after 07-04. ~29-day catch-up overdue (see reports/01-resume-roadmap-assessment.md). |
| **July 2026** | ⏳ Partial | 38 | Single daily cycle (07-04): NBOR(25) + utility(2) + SilverLeaf discovery(11). County news, SJSO, emergency mgmt, BCC, CDD, school: 0. All 38 items still `pending_review`. |

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
| **school_stack** | 🟡 Backfill only | 12 items from May backfill. **No June or July monitoring**. BoardDocs full extraction not yet implemented. School board agenda items, budget, and rezoning data missing for both months. |

### ❌ Missing Coverage
| Source Family | Items | What's Blocking |
|---------------|-------|-----------------|
| **resident_cost_stack** | 0 | Budget page is off-season. No property appraiser or tax collector data extracted. TRIM season (Aug-Sep) is priority window. |
| **cdd_governance_stack** | 0 July | June spike (9 items, retro 06-26) not sustained. Trout Creek Jul 7 / Jul 23 outcomes not captured. Tier 3 still not promoted to active monitoring. |
| **community_developer_stack** | 0 (11 SilverLeaf discovery items are the exception, see below) | Tier 4 sources not promoted. No Nocatee HOA, Ponte Vedra, or other community developer feeds. |
| **local_media_context_stack** | 11 (SilverLeaf discovery, July) | **Status changed 07-04:** St. Johns Citizen now active via the `silverleaf_discovery` search profile. Media remains tip-surfacing context, but the SilverLeaf candidates (3 high-sensitivity crime items) are unverified and need human review before use. |

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
| School district June & July data | School district monitor pilot started but not yet running daily/weekly. May backfill showed 12 items but June and July have none. | 🟡 Medium |
| Emergency management frequency | Currently checked ad-hoc. Should be daily during hurricane season (June-November). Zero July items. | 🟡 Medium |
| June NBOR double-count | `2026-06-08` and `2026-06-26` NBOR YAMLs are byte-identical duplicates (same 25 IDs). Counted once in closeout totals (June = 99, not 115). | 🟢 Resolved (2026-08-02) |
| July daily cadence | Only one daily cycle ran in July (07-04). ~29-day catch-up overdue. County news, SJSO, emergency mgmt produced 0 July items. | 🔴 High — catch-up needed |

### Strategic Gaps (Deferred)

| Gap | Rationale | ETA |
|-----|-----------|-----|
| Local media | Deferred — media is tip-surfacing, not primary intel. **Note (07-04):** stjohnscitizen.com is now partially active via the `silverleaf_discovery` search profile. SilverLeaf candidates are unverified and need human review. | Not scheduled (partial via SilverLeaf) |
| CDD governance | Tier 3 sources not promoted. Requires source evaluation and extractor development. June capture proved extractable; needs active cadence. | Not scheduled |
| Community developer | Tier 4 sources. Lowest priority. | Not scheduled |

## 4. Recommendations

### Immediate (This Week)

1. **Catch up the daily monitoring (~29 days overdue)** — Highest priority. Run daily sources (NBOR, utility, county news, SJSO, emergency mgmt) until caught up. This closes the July 1-3 and 5-31 gaps.
2. **Human review of July SilverLeaf candidates** — 11 SilverLeaf items, 3 high-sensitivity crime items (ICE detainer, construction-site shooting, airlifted minor). Verify URLs + official records before any promotion. Human decision required.
3. **Fix BCC agenda links (GAP-001)** — Contact Clerk's office or find alternative access. Two June meetings (Jun 2, Jun 16) + all July meetings blocked.
4. **Add sjc_emergency_management to daily cycle** — Hurricane season (Jun-Nov). Zero July checks recorded.
5. **Activate school district weekly monitor** — No June or July school data. BoardDocs pilot start is overdue.

### Short-Term (Next 2 Weeks)

6. **Extract May 19, 2026 BCC agenda** — Confirmed working agenda link. Would add ~40 items and validate the BCC extractor on a second meeting.
7. **Build PZA board records extractor** — Planning & Zoning Agency agendas are the second-most important official decision stack after BCC.
8. **Add weekly development tracker check** — Even partial static-page extraction would add value.
9. **Run July review backfill** — All 38 July items are `pending_review`; run the same review cycle that produced June's 83 verified.

### Medium-Term (Next Month)

10. **Backfill Aug-Sep 2025** — High priority for TRIM/budget season school rezoning context. Extractors need to exist first.
11. **NBOR daily automation** — Already daily-ready. Ensure no gaps between cycles.
12. **Resident cost stack pilot** — Property appraiser and tax collector pages. Most useful during TRIM season (Aug-Sep).

### Long-Term

13. **Local media integration** — Only after official stacks are complete. SilverLeaf discovery profile is the active partial path.
14. **CDD and community developer stacks** — Lowest priority. Useful for hyperlocal Nocatee/Ponte Vedra coverage but not needed for county-wide intel.

---

## 5. Gap Closure Tracker

| Gap ID | Description | Priority | Owner | Status |
|--------|-------------|----------|-------|--------|
| GAP-001 | BCC agenda links broken (June + July) | P0 | sjc-intel-architect | 🔴 Blocked |
| GAP-002 | Emergency mgmt not in daily cycle | P1 | sjc-intel-source-watch | 🟡 Open |
| GAP-003 | School district monitoring (June + July) | P1 | sjc-intel-source-watch | 🟡 Open |
| GAP-004 | May 19 BCC agenda not extracted | P2 | hermes-bcc-worker | 🟡 Open |
| GAP-005 | PZA board records not extracted | P2 | sjc-intel-architect | 🔵 Planned |
| GAP-006 | Development tracker not monitored | P3 | sjc-intel-source-watch | 🔵 Planned |
| GAP-007 | Pre-May 2026 data not backfilled | P4 | sjc-intel-architect | 🔵 Deferred |
| GAP-008 | Aug-Sep 2025 budget/TRIM season | P2 | — | 🔵 Planned |
| GAP-009 | July SilverLeaf candidates unverified (3 high-sensitivity) | P0 | human / sjc-intel-architect | ⚠️ Human decision required |
| GAP-010 | Daily monitoring catch-up (~29 days overdue) | P1 | sjc-intel-source-watch | 🟡 Open |
