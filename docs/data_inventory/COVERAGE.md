# Data Coverage Map

## 2026

| Month | Items | Sources | Source Families | Complete? |
|-------|-------|---------|-----------------|-----------|
| January | 44† | sjc_bcc_calendar | county_decision_stack | ⏳ Partial (BCC agenda extracted retroactively 2026-06-26) |
| February | 0 | — | — | ❌ Not started |
| March | 0 | — | — | ❌ Not started |
| April | 0 | — | — | ❌ Not started |
| May | 21 | sjc_county_news, sjc_utility_department, sjc_school_district, sjcsd_boarddocs, sjso_news_stories, sjc_emergency_management, sjrwmd_watering_restrictions | county_decision_stack, utilities_water_stack, school_stack, public_safety, emergency_mgmt | ✅ First pass (official only) |
| June (total) | **99** | 9 sources (see breakdown below) | 7 families | ⏳ Closeout complete (2026-08-02) |
| July (total) | **38** | 4 sources (see breakdown below) | 4 families | ⏳ Closeout complete (2026-08-02) |

† BCC agenda items from Jan 20, 2026 meeting were extracted retroactively on 2026-06-26. They count as June extraction but provide January content coverage.

**June count correction (2026-08-02):** `data/intel_items/2026-06-08/sjc_nbor_public_notices.yaml` and `data/intel_items/2026-06-26/sjc_nbor_public_notices.yaml` are byte-identical duplicates (same 25 IDs `SJC-NBOR-20260626-*`). Earlier counts listed June as 115 by double-counting NBOR and omitting 9 CDD items. Corrected June total = 99 unique (25 NBOR counted once + 44 BCC + 9 county news + 6 utility + 5 SJSO + 9 CDD + 1 emergency mgmt).

### June 2026 Detail

| Window | Items | Sources | Source Families (Beats) |
|--------|-------|---------|------------------------|
| June 3 | 14 | sjc_county_news(5), sjc_utility_department(5), sjso_news_stories(4) | county_decision_stack, utilities_water_stack, public_safety |
| June 8 | 25 | sjc_nbor_public_notices(25) — **byte-identical to Jun 26 NBOR (duplicate capture), counted once in totals** | utilities_water_stack(11), planning_development_stack(6), permit_construction_stack(7), roads_transportation_stack(1) |
| June 26 | 76 | sjc_bcc_calendar(44), sjc_nbor_public_notices(25), sjc_county_news(4), sjc_utility_department(1), sjc_emergency_management(1), sjso_news_stories(1) | county_decision_stack(44), utilities_water_stack(12), planning_development_stack(6), permit_construction_stack(7), roads_transportation_stack(2), parks_amenities(2), public_safety(2), emergency_mgmt(1) |
| CDD (six_mile_creek, tolomato, trout_creek) | 9 | six_mile_creek_cdd(3), tolomato_cdd(3), trout_creek_cdd(3) | cdd_governance_stack(9) |
| **June total (unique)** | **99** | **9 sources** | **7 source families** |

### July 2026 Detail

| Window | Items | Sources | Source Families (Beats) |
|--------|-------|---------|------------------------|
| July 4 | 27 | sjc_nbor_public_notices(25), sjc_utility_department(2) | utilities_water_stack, planning_development_stack, permit_construction_stack, roads_transportation_stack |
| July 4 | 6 | silverleaf_discovery via st_johns_citizen(6) | local_media_context_stack, community_developer_stack |
| July 6 | 5 | silverleaf_discovery via st_johns_citizen(5) | local_media_context_stack, community_developer_stack |
| **July total** | **38** | **4 sources** | **4 source families** |

> All 38 July items are `pending_review` / `unverified`. 11 are
> SilverLeaf discovery candidates (3 high-sensitivity crime items needing
> human review). July capture is a near-single-snapshot (one daily cycle on
> 07-04) — volume reflects capture cadence, not true activity.

### Item Counts by Source (June 2026)

| Source ID | Source Name | Jun 3 | Jun 8 | Jun 26 | CDD | June Total |
|-----------|-------------|-------|-------|--------|-----|------------|
| sjc_county_news | SJC County News | 5 | — | 4 | — | **9** |
| sjc_utility_department | Utility Department | 5 | — | 1 | — | **6** |
| sjso_news_stories | SJSO News Stories | 4 | — | 1 | — | **5** |
| sjc_nbor_public_notices | NBOR Public Notices | — | 25* | 25* | — | **25** (unique) |
| sjc_bcc_calendar | BCC Agenda Items | — | — | 44 | — | **44** |
| sjc_emergency_management | Emergency Management | — | — | 1 | — | **1** |
| six_mile_creek_cdd | Six Mile Creek CDD | — | — | — | 3 | **3** |
| tolomato_cdd | Tolomato CDD | — | — | — | 3 | **3** |
| trout_creek_cdd | Trout Creek CDD | — | — | — | 3 | **3** |
| **Total (unique)** | | | | | | **99** |

\* The Jun 8 and Jun 26 NBOR files are byte-identical duplicates (same 25 IDs `SJC-NBOR-20260626-*`). Counted once → 25 unique, not 50.

### Item Counts by Source (July 2026)

| Source ID | Source Name | Jul 4 | Jul 6 | July Total |
|-----------|-------------|-------|-------|------------|
| sjc_nbor_public_notices | NBOR Public Notices | 25 | — | **25** |
| silverleaf_discovery | St. Johns Citizen (SilverLeaf search) | 6 | 5 | **11** |
| sjc_utility_department | Utility Department | 2 | — | **2** |
| **Total** | | | | **38** |

*The main utility department page was unchanged (same 5 duplicates from Jun 3). The 1 new item (SJC Utilities 2025 Annual Report) was discovered via the Featured Department News sidebar.

## 2025

| Month | Items | Sources | Complete? |
|-------|-------|---------|-----------|
| Aug-Sep | 0 | — | ❌ Planned (TRIM/budget) |
| All others | 0 | — | ❌ Not started |

## Source Family Coverage

| Source Family | May 2026 | June 2026 | July 2026 | Gap? |
|---------------|----------|-----------|-----------|------|
| county_decision_stack | ✅ 4 items | ✅ 53 items (Jun 3: 5 county_news, Jun 26: 44 BCC + 4 county_news) | ❌ 0 | June 2026 BCC agenda links broken — only Jan 20 extracted so far; no July BCC |
| planning_development_stack | ❌ | ✅ 12 items (NBOR rezoning hearings) | ✅ 7 items (NBOR rezoning/variances) | Still no Clerk PZA board records extracted |
| permit_construction_stack | ❌ | ✅ 14 items (NBOR site/ROW permits) | ✅ 10 items (NBOR site plans) | No building permit data from county portal |
| roads_transportation_stack | ❌ | ✅ 3 items (NBOR roadwork + county news) | ✅ 1 item (NBOR roadwork) | No FDOT or county roads department direct feeds |
| utilities_water_stack | ✅ 2 items | ✅ 28 items (NBOR utility ROW + county news + utility dept) | ✅ 10 items (NBOR utility ROW 8 + utility dept 2) | Good coverage from NBOR + county news; SJRWMD direct still absent |
| school_stack | ✅ 12 items | ❌ | ❌ | School district not monitored since May backfill. BoardDocs pilot pending. |
| resident_cost_stack | ❌ | ❌ | ❌ | Budget page off-season; no property tax/TRIM data |
| cdd_governance_stack | ❌ | ✅ 9 items (3 CDDs, retro 06-26) | ❌ | Tier 3 not promoted to active monitoring; June capture spike not sustained |
| community_developer_stack | ❌ | ❌ | 🟡 11 items (SilverLeaf discovery) | SilverLeaf discovery profile active since 07-04 |
| local_media_context_stack | ❌ | ❌ | 🟡 11 items (SilverLeaf discovery) | St. Johns Citizen now active via silverleaf_discovery profile |
| emergency_mgmt | ✅ 1 item | ✅ 1 item | ❌ 0 | Hurricane season (Jun-Nov) — needs daily monitoring |
| public_safety (sheriff) | ✅ 2 items | ✅ 5 items | ❌ 0 | SJSO monitor active; low volume is normal |

*Last updated: 2026-08-02*
