# Source Gaps — July 2026 Closeout

Generated: 2026-08-02
Task: 03-monthly-cadence-closeout
Scope: Sources that should have produced July 2026 items (per monitor
frequency in `registry/sources.yaml` and `docs/cadence.md`) but did not.

---

## Gap 1: Daily Monitoring Ran Only Once in July

**Expected:** Daily sources (`sjc_nbor_public_notices`, `sjc_utility_department`,
`sjc_county_news`, `sjso_news_stories`, `sjc_emergency_management`,
`st_johns_citizen`) should be checked on a daily cadence.

**Evidence:** Only one daily cycle ran in July — on 2026-07-04 — and it
covered only `sjc_nbor_public_notices` (25 items), `sjc_utility_department`
(2 items), and the `silverleaf_discovery` profile (6 items). County news,
sheriff, and emergency management produced zero July items. `logs/runs/`
shows no other July daily runs.

**Recommendation:** Daily catch-up is the highest-priority cadence action
(29+ days overdue per `reports/01-resume-roadmap-assessment.md`). Run
2 sources/session until caught up, prioritizing NBOR + utility, then county
news + sheriff.

---

## Gap 2: BCC — No July Meetings Extracted

**Expected:** BCC regular meetings occur on first/third Tuesdays (Jul 7,
Jul 21) and should be monitored per `sjc_bcc_calendar` (weekly).

**Evidence:** Zero BCC items in July. The June meeting-blocking issue
(GAP-001) persists; no July Clerk verification is recorded.

**Recommendation:** GAP-001 (broken Clerk agenda links) remains the blocker.
No July BCC decision coverage exists.

---

## Gap 3: School District — No July Coverage (GAP-003 persists)

**Expected:** `sjc_school_district` / `sjcsd_boarddocs` (weekly). Summer
session and 2026-27 planning (SilverLeaf K-8 opening, Programs of Choice
deadlines) are in play.

**Evidence:** Zero school items in July. The SilverLeaf K-8 school item came
via `silverleaf_discovery`, not the school stack.

**Recommendation:** BoardDocs pilot remains the top school action. School
coverage has now been missing for two consecutive months.

---

## Gap 4: Emergency Management — Not Monitored During Peak Hurricane Season

**Expected:** `sjc_emergency_management` daily/seasonal (June–November).

**Evidence:** Zero July items. July is peak hurricane season (peak typically
Aug–Oct) and no checks are recorded.

**Recommendation:** Add emergency management to the daily cycle immediately.
This is a safety-critical gap.

---

## Gap 5: CDDs — No July Items

**Expected:** `tolomato_cdd`, `trout_creek_cdd`, `six_mile_creek_cdd` are
`active` weekly sources. Trout Creek had July 7 workshop and July 23 regular
meeting scheduled (captured in June items).

**Evidence:** Zero CDD items in July. Trout Creek's July 7 and July 23
meetings were pre-announced in June but no July outcome/minutes captured.

**Recommendation:** Weekly CDD checks should resume; the June extraction
proved the CDD sites are extractable.

---

## Gap 6: PZA, Development Tracker, Permits, FDOT, NWS — No Coverage

**Expected:** `sjc_pza_boards`, `sjc_development_tracker`, `sjc_permit_status`,
`fdot_district_two_nflroads`, `nws_jacksonville` (all verified in registry).

**Evidence:** Zero items from any in July.

**Recommendation:** Unchanged from June — development tracker (browser
automation) and permit portal (form interaction) still need investigation;
FDOT/NWS lack monitor specs.

---

## Gap 7: SilverLeaf Incident Candidates — Unverified

**Expected:** The `silverleaf_discovery` profile found 5 candidate articles on
07-06 (3 high-sensitivity).

**Evidence:** All 5 have unresolved direct-fetch URLs (St. Johns Citizen
rate-limiting/timeout). Titles verified from search results only. No
official-record confirmation exists in captured data.

**Recommendation:** Manual URL verification + official-record cross-check
before any promotion. Human decision required. These are the highest-risk
items in the current queue.

---

## Summary

| Gap | Priority | Source Type | Status |
|-----|----------|-------------|--------|
| Daily monitoring gap (1 run in July) | High | All daily | 🟡 Open — needs catch-up |
| Emergency mgmt not monitored (hurricane season) | High | Official | 🟡 Open |
| BCC July meetings not extracted (GAP-001) | High | Official | 🔴 Blocked |
| School district July coverage (GAP-003) | High | Official | 🟡 Open |
| CDD July outcomes not captured | Medium | Community | 🟡 Open |
| PZA / dev tracker / permits / FDOT / NWS | Low | Official | 🔵 Planned |
| SilverLeaf incident candidates unverified | High | Media | ⚠️ Human decision required |
