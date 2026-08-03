# Source Gaps — June 2026 Closeout

Generated: 2026-08-02
Task: 03-monthly-cadence-closeout
Scope: Sources that should have produced June 2026 items (per monitor
frequency in `registry/sources.yaml` and `docs/cadence.md`) but did not.

---

## Gap 1: BCC June Regular Meetings (Jun 2, Jun 16) — GAP-001 (still blocked)

**Expected:** BCC meets on first and third Tuesdays; June had Jun 2 and
Jun 16 regular meetings. Both are regular, high-value county-decision events.

**Evidence:** `data/source_events/2026-06-26/sjc_bcc_calendar.yaml` records
both meetings as `status: blocked`, `source_health: broken_link`. Agenda links
on the Clerk's page point to minutes PDFs; deterministic `arbcc` URLs also
404. No extracted items for either meeting. Only the Jan 20, 2026 agenda was
recoverable (44 items, retroactive).

**Recommendation:** Clerk's office verification remains required (long-running
GAP-001). Until resolved, June BCC decision coverage will stay limited to the
retroactive January agenda.

---

## Gap 2: School District — No June Coverage (GAP-003, still open)

**Expected:** `sjc_school_district` and `sjcsd_boarddocs` are weekly-frequent
sources (verified). School Board meetings and district news should produce
items in June.

**Evidence:** Zero school-stack items in June (and July). No school items in
the review queue for either month. `docs/cadence.md` marks the school monitor
as spec-ready with BoardDocs extraction pending.

**Recommendation:** BoardDocs pilot remains the top school-stack action. June
is the end of the school year and the start of summer session — no signals
were captured at all.

---

## Gap 3: Emergency Management — Under-Monitored for Hurricane Season

**Expected:** `sjc_emergency_management` is daily/seasonal (June–November,
hurricane season), per `docs/cadence.md` (activated 2026-06-26).

**Evidence:** Only 1 June item (hurricane-season preparedness messaging,
`SJC-EM-20260626-0001`). No other emergency-management checks are recorded.

**Recommendation:** Add emergency management to the daily cycle for the
hurricane season. June–November is the high-risk window; the page should be
checked regularly.

---

## Gap 4: No SJRWMD Watering-Restriction Items Despite Active Phase III

**Expected:** `sjrwmd_watering_restrictions` is daily-frequent (verified). The
Phase III Extreme Water Shortage was active all of June.

**Evidence:** No `sjrwmd_watering_restrictions` items in June. The Phase III
declaration is represented via `sjc_county_news` and `sjc_utility_department`
carrying the notice, but SJRWMD itself was not directly captured.

**Recommendation:** Re-check SJRWMD for June declarations/order updates and
add a recurring SJRWMD check to the utility daily cycle.

---

## Gap 5: Planning & Zoning (PZA) — No Records Extracted (GAP-005)

**Expected:** `sjc_pza_boards` (verified, weekly) — PZA is the second most
important official decision stack after BCC.

**Evidence:** Zero PZA items in June. NBOR rezoning/variance notices (6) are
the only planning-stack signal.

**Recommendation:** PZA board record extraction remains planned (GAP-005,
P2). No extractor configured.

---

## Gap 6: Development Tracker, Permit Status, FDOT, NWS — No Coverage

**Expected:** `sjc_development_tracker`, `sjc_permit_status`
(`daily`/`weekly`, verified), `fdot_district_two_nflroads` (daily), and
`nws_jacksonville` (daily) are all in the registry as verified.

**Evidence:** Zero items from any of these in June.

**Recommendation:** Development-tracker (browser automation needed) and
permit-status (form interaction needed) remain investigation-backed;
FDOT/NWS lack monitor specs. Unchanged from prior gaps.

---

## Gap 7: St. Johns Citizen / Local Media — Not Captured in June

**Expected:** `st_johns_citizen` is daily/active and now carries
`silverleaf_discovery` profiles (Jul 4–6).

**Evidence:** Zero `st_johns_citizen`/silverleaf_discovery items in June. All
SilverLeaf discovery items are dated July.

**Recommendation:** The SilverLeaf search profiles became active in July;
June may have had SilverLeaf media coverage that is now unrecoverable without
backfill (which is out of scope).

---

## Summary

| Gap | Priority | Source Type | Status |
|-----|----------|-------------|--------|
| BCC June meetings (Jun 2, 16) | High | Official | 🔴 Blocked (GAP-001) |
| School district June coverage | High | Official | 🟡 Open (GAP-003) |
| Emergency mgmt daily during hurricane season | Medium | Official | 🟡 Open |
| SJRWMD active declaration updates | Medium | Official | 🟡 Open |
| PZA board records | Medium | Official | 🔵 Planned (GAP-005) |
| Dev tracker / permits / FDOT / NWS | Low | Official | 🔵 Planned |
| Local media / SilverLeaf June | Low | Media | 🔵 Deferred |
