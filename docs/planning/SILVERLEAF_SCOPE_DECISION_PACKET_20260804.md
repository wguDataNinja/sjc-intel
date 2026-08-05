# SilverLeaf Scope — Decision-Ready Packet

**Status:** Decision input for Buddy and GPT. No scope is final until approved.
**Purpose:** Let Buddy and GPT make the remaining SilverLeaf inclusion/exclusion
decisions without reading the entire corpus (Task 16 §13; `ROADMAP.md` §3B-G1).
**Date:** 2026-08-04
**Provenance legend:** each element is labeled `REPO-VERIFIED` (from a
repository file/registry), `INFERRED` (reasoned from repo evidence, needs
confirmation), `MISSING-AUTHORITY` (no authoritative source found yet), or
`EDITORIAL` (a proposed rule for Buddy/GPT to decide).

---

## 1. Known neighborhoods

`REPO-VERIFIED` — `registry/communities.yaml` (SilverLeaf official resident
directory, 2026-07): Brandon Lakes, Brook Forest, Elm Creek, Holly Forest,
Johns Island, Newbrook, Silver Falls, Silver Landing, Silver Meadows,
SilverLeaf Village, Waterford Lakes, plus `cherry_elm` (resident-mentioned,
may overlap a directory-confirmed neighborhood).

- **Decision needed:** accept this set as the SilverLeaf neighborhood scope?
  (EDITORIAL: yes, unless Buddy adds/removes.)

## 2. Aliases

`REPO-VERIFIED` — `registry/tracked_entities.yaml`:
- "SilverLeaf" / "Silver Leaf" (spelling variant) — needs a deliberate alias.
- "Silverleaf" (lowercase 'l') is the **registered commercial spelling**
  (Silverleaf Commons/Market) — distinct from the community spelling
  SilverLeaf. **Decision needed:** treat "Silverleaf"/"Silver Leaf" as aliases
  of community SilverLeaf for matching, with a note that the commercial
  entities use lowercase-l.
- Neighborhood aliases exist per record (`SilverLeaf Village` vs
  `Silverleaf Commons` vs `Silverleaf Market` confusion documented in
  communities/tracked entities).

## 3. Likely access roads

`REPO-VERIFIED`/`INFERRED`:
- SilverLeaf Parkway (primary internal/external road).
- St. Johns Parkway / CR 2209 connector (opened Oct 2025) — `ENT-ROAD-CR-2209-CONNECTOR`.
- CR 210 corridor (major east-west arterial) — `cr_210_corridor` community.
- SR 16 corridor (western access) — `sr_16_corridor`.
- CR 16A — mentioned in tracked entities (grocery center at CR 16A & SilverLeaf
  Parkway).
- International Golf Parkway (IGP) — connector endpoint.
- **Decision needed:** confirm the exact access-road set for adjacency
  inclusion. `MISSING-AUTHORITY` for an official boundary/road map.

## 4. Likely serving schools

`REPO-VERIFIED`/`INFERRED`:
- SilverLeaf K-8 (QQ) — `ENT-EDU-SILVERLEAF-K8`, under construction, expected
  to open 2026-2027. `MISSING-AUTHORITY` for the official attendance zone map
  (DIR-010).
- Tocoi Creek High School — mentioned in CR 2209 entity evidence (2,700+
  students; congestion around it). `INFERRED` as likely serving school.
- **Decision needed:** which schools count as "serving SilverLeaf" for
  inclusion (school-adjacent items). Requires attendance-zone authority
  (DIR-010).

## 5. Utilities

`REPO-VERIFIED`:
- County utility service: St. Johns County Utility Department
  (`sjc_utility_department`) — water/sewer/reclaimed. Free chlorine burnout and
  Phase III water shortage items affect all county utility customers incl.
  SilverLeaf.
- `ENT-INFRA-SR-207-WRF` — SR 207 Water Reclamation Facility Phase 2
  ($191M), serves CR 210 / SR 207 corridor (capacity for growth incl.
  SilverLeaf area). `INFERRED` adjacency.
- **Decision needed:** countywide utility items count as SilverLeaf-relevant
  when they affect all customers (recommended: yes, with a "countywide" bucket).

## 6. Nearby entities

`REPO-VERIFIED` — `registry/tracked_entities.yaml` (15 entities):
- Retail: Silverleaf Commons, Silverleaf Market, Shoppes of St. Johns Parkway
  (adjacent), CR 16A & SilverLeaf Parkway Grocery Center (provisional),
  SilverLeaf Mega Publix (completed), Harris Teeter (proposed).
- Education: SilverLeaf K-8 (under construction).
- Recreation: Beach Valley Mini Golf (proposed).
- Roads: CR 2209 connector (completed).
- Health: Baptist SilverLeaf Medical Campus (tracked), Ascension St. Vincent's
  Nocatee (proposed, Nocatee — **likely exclude** or mark adjacent-only).
- Hospitality: Fairfield Inn CR 210 (proposed, corridor).
- Mixed-use: Nocatee Crosswater Retail Center (Nocatee — **likely exclude**).
- Community: ENT-COMM-SILVERLEAF (master scope).

## 7. Tracked businesses / services

`REPO-VERIFIED`: Publix SilverLeaf (mega Publix), Jersey Mike's (tenant of
Silverleaf Commons), Baptist Health campus. `INFERRED`: Bala's Pizza second
location (SilverLeaf) — pending verification (SJC-SL-20260706-0005).

## 8. Proposed inclusion rules

`EDITORIAL` — for approval:
1. Item is inside the SilverLeaf boundary or a SilverLeaf neighborhood.
2. Item affects a school serving SilverLeaf.
3. Item affects a major access/commute route (SilverLeaf Parkway, St. Johns
   Parkway/CR 2209, CR 210, SR 16, IGP, CR 16A).
4. Item changes nearby shopping, healthcare, parks, or services that SilverLeaf
   residents use (adjacent centers, Baptist campus).
5. Item affects taxes, utilities, zoning, or emergency conditions for
   SilverLeaf residents.
6. Notable local achievement involving SilverLeaf residents.
- "Somewhere in St. Johns County" is NOT sufficient (product-direction rule,
  2026-07-06).

## 9. Proposed exclusion rules

`EDITORIAL`:
1. Nocatee-only items (crossover only if corridor/shared infrastructure).
2. RiverTown-only items.
3. Beachwalk-only items unless CR 210 impact.
4. Countywide items with no SilverLeaf household/commute/school impact.
5. Crime/public-safety items unless explicit editorial approval.
6. Items whose relevance depends on unverified local-media claims.

## 10. Adjacency rules

`EDITORIAL`:
- CR 210 corridor: include items on CR 210 segments that serve SilverLeaf
  access (INFERRED; exact segments need DIR-011).
- SR 16 corridor: include only if they affect SilverLeaf access (e.g.
  railroad crossings on West King/Kinlaw — county news item).
- Nearby retail/health centers (Shoppes of St. Johns Parkway, Baptist campus):
  include as "adjacent" with a clearly labeled adjacency note.
- Nocatee/Shearwater/TrailMark: include only cross-boundary shared
  infrastructure.

## 11. Countywide-material-impact rule

`EDITORIAL` — proposed: a countywide item may be published in the SilverLeaf
release only when it materially affects SilverLeaf residents (utility service
continuity, water restrictions, public-safety conditions, county-wide tax/land
decisions that change local conditions). Pure countywide civic items (auctions,
library programs, awards) are excluded by default.

## 12. needs_review cases

`REPO-VERIFIED` — items requiring human decision before any inclusion:
- SJC-SL-20260706-0001 (ICE detainer, high sens) — crime/legal; exclude unless
  explicitly approved.
- SJC-SL-20260706-0002 (construction-site shooting, high sens) — crime; exclude.
- SJC-SL-20260706-0004 (airlifted minor, high sens) — minors; exclude.
- SJC-SL-20260706-0003 (lightning strike, low sens) — needs URL/date
  verification (unverified).
- SJC-SL-20260706-0005 (Bala's second location, low sens) — needs verification.
- SJSO items (SJC-SJSO-20260603-0001..0004, high/medium) — public-safety;
  default exclude.

## 13. Source provenance summary

| Element | Source | Label |
|---------|--------|-------|
| Neighborhoods | `registry/communities.yaml` (SilverLeaf resident directory) | REPO-VERIFIED |
| Aliases | `registry/tracked_entities.yaml` | REPO-VERIFIED |
| Access roads | communities.yaml + tracked entities (CR 2209) | REPO-VERIFIED (partial) / INFERRED (segments) |
| Schools | tracked entities (K-8) + CR 2209 evidence | REPO-VERIFIED (entity) / INFERRED (zones) |
| Utilities | sources.yaml + tracked entities (SR 207 WRF) | REPO-VERIFIED |
| Entities | tracked_entities.yaml | REPO-VERIFIED |
| Boundary / streets / entrances | **none** | MISSING-AUTHORITY (DIR-001/009) |
| Attendance zones | **none** | MISSING-AUTHORITY (DIR-010) |
| I-95/I-295 commute segments | **none** | MISSING-AUTHORITY (DIR-011) |

## 14. Bottom line for decision

- The **registry is already seeded** with the SilverLeaf neighborhood and
  entity set. What is missing is: (a) an explicit boundary/road/school scope
  decision (authorities), and (b) the `silverleaf_relevance` decision per item.
- The §3B-G1 registry task can proceed with Buddy approving §8–§11 rules and
  naming the authoritative sources for the missing elements (DIR-001, DIR-009,
  DIR-010, DIR-011). Nothing here requires waiting for GIS/PostGIS.
