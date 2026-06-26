# Monitor Pilot Report: `sjc_utility_department`

**Date:** 2026-06-03  
**Source:** St. Johns County Utility Department — Water and Boil Notices  
**URL:** `https://www.sjcfl.us/departments/utility-department/`  
**Worker:** `hermes-sjc_utility_department`  
**Status:** Success — 5 items extracted

---

## Results Summary

| Metric | Value |
|--------|-------|
| HTTP status | 200 |
| Candidates found | 5 |
| New items | 5 |
| Duplicates skipped | 0 (first cycle) |
| Items requiring human review | 0 |
| Taxonomy gaps proposed | 1 (`water_restrictions`) |

## Items by Category

- **Water restriction:** 1 (Phase III — active, ongoing)
- **Infrastructure/timely:** 1 (Chlorine burnout — active June 1-21)
- **Capital project:** 1 (SR 207 WRF — $191M)
- **Completed project:** 1 ($4.6M Utilities Lab)
- **Safety/compliance:** 1 (Lead service line inventory)

## Source Suitability for Daily Monitoring

**EXCELLENT.** The utility department page is a productive, reliable source.

Strengths:
- Consistent page structure with "Announcements" section
- Plain HTML — no JavaScript dependencies
- Dated announcements with clear headings
- Mix of urgent (water restrictions), timely (maintenance), and reference (projects) content
- No boilewater notices were active during this cycle, but the alert link is present — this confirms the monitor spec's fallback path works

Considerations:
- The Announcements section is not a chronological feed — it shows highlighted/featured announcements. Old but still-relevant items (Phase III, $191M project) remain visible.
- New urgent items (boil notices) should appear at the top of the Announcements section when active.
- The page also has a "Featured Department News" sidebar that may contain additional items (2025 Annual Report was present but not extracted — it's in the sidebar, not the main Announcements section).

## Comparison Against Monitor Spec

| Spec Item | Verified? | Notes |
|-----------|-----------|-------|
| HTTP GET main page | ✅ | 200 response |
| Parse Announcements section | ✅ | 5 blocks parsed |
| Extract title, date, summary | ✅ | All items have complete fields |
| Check boil water alerts | ✅ | Link present; no active notices |
| Dedupe by title + date | ✅ | All 5 new |
| Classification defaults | ✅ | Applied per spec |
| RI defaults | ✅ | Applied per spec |
| Sensitivity rules | ✅ | No items triggered human review |
| Output YAML | ✅ | Valid |
| Prior index updated | ✅ | 5 new entries |

## Taxonomy Gaps

| Tag | Evidence | Items |
|-----|----------|-------|
| `water_restrictions` | Phase III Extreme Water Shortage — ongoing, highest resident impact | SJC-UTIL-20260603-0001 |

This is the same gap identified in the May 2026 backfill. Now has additional
real-time monitoring evidence.

## Recommendations

1. **Run daily.** This source is productive and easy to extract.
2. **Add "Featured Department News" sidebar** to extraction scope on next cycle —
   it contained the 2025 Annual Report which may be of interest to residents.
3. **Monitor alarm pattern** — if the Announcements section adds a new
   announcement at the top, that likely signals a high-priority item.
4. **Consider adding `sjrwmd_watering_restrictions`** as a companion monitor
   — the Phase III declaration originates from SJRWMD.
