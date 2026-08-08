# SilverLeaf School Service Authority

**Status:** Active, school-year-specific evidence contract.
**Primary registry:** `registry/silverleaf_scope.yaml` → `school_authority` and
`schools`.
**Last reviewed:** 2026-08-08.

## What this establishes

For the **2026–2027** school year, St. Johns County School District (SJCSD)
has an approved attendance-zone plan for K-8 School QQ, now Magnolia Oaks
Academy. The plan serves a named **portion** of SilverLeaf, not all SilverLeaf
addresses. Magnolia Oaks is in the Silverleaf community at 800 Courtney Vista
Drive and serves kindergarten through seventh grade in its first year.

This is a scope/review relationship. The SJCSD attendance-zone locator is the
only current authority for an individual address, and normal enrollment,
capacity, grade-transition, transfer, and choice rules still apply.

## Official evidence

| ID | Authority | Determination |
|---|---|---|
| `SJCSD-ZONING-2026-27` | [SJCSD Attendance Zoning](https://www.stjohns.k12.fl.us/zoning/) | The page identifies the 2026–27 zone locator and records that the Board approved K-8 QQ Plan C–Modified on November 18, 2025. It also explains the separate eighth-grade locator context. |
| `SJCSD-QQ-PLAN-C-2026-27` | [K-8 QQ Plan C–Modified](https://www.stjohns.k12.fl.us/zoning/wp-content/uploads/sites/44/2025/10/Attendance-Zoning-2026-2027-K-8-QQ_Plan-C-Modified.pdf) | The approved plan lists the named portion of SilverLeaf served by K-8 QQ for the 2026–27 change. |
| `SJCSD-MAGNOLIA-OPENING-2026` | [SJCSD Magnolia Oaks announcement](https://www.stjohns.k12.fl.us/news/silverleaf-school/) | Confirms the school identity, its location in Silverleaf, and its K–7 first-year grade span. |

The current relationship is deliberately bounded to the references above. No
media article, driving distance, road connection, or town-hall location is
attendance-zone evidence.

## Registry outcome for 2026–2027

| Relationship | Status | Meaning |
|---|---|---|
| Magnolia Oaks Academy / K-8 QQ ↔ named portion of SilverLeaf | verified partial service | The registry records seven existing neighborhood IDs: Cherry Elm, Elm Creek, Silver Landing, Silver Falls, Silver Meadows, SilverLeaf Village, and Newbrook. |
| Other named areas in the approved plan | evidence retained, not yet community records | Aspire, Elm Ridge, Hartford, Hammock Oaks, and listed parcels remain district names until independently reconciled with `registry/communities.yaml`. |
| Tocoi Creek High School ↔ SilverLeaf | unverified | No school-year-specific district attendance authority was found/registered. It must not be presented as a serving school. |
| Any specific SilverLeaf address ↔ any school | unresolved by this registry | Use the district locator and district confirmation. |

The registry does not claim that every listed neighborhood is entirely inside
the new school zone. The plan and locator govern individual addresses and may
contain partial neighborhoods, parcel exceptions, grade-specific rules, or
later amendments.

## How to use this in SJC_Intel

1. A record about Magnolia Oaks, its opening, K–7 operations, or an approved
   2026–27 K-8 QQ zone change has a concrete SilverLeaf resident connection.
2. A record about another school requires an explicit school-year-specific
   SJCSD source before treating that school as serving SilverLeaf.
3. A record about an individual family, address, enrollment result, or
   student must never be inferred from this registry; it is normally private
   and outside the public intelligence product.
4. At the next school-year zoning cycle, refresh the three official sources
   before retaining the relationship. If there is no new authority, mark this
   relationship stale rather than carrying it forward as current.

## Follow-up needed

`DIR-010` is substantially advanced but remains open until the district's
address-level locator/service or a versioned official map layer can be reviewed
for the next school year. The next bounded task is to reconcile the district's
remaining named areas with the community registry, only where a public,
authoritative source establishes they are distinct SilverLeaf neighborhoods.
No school assignment should be inferred while doing that work.
