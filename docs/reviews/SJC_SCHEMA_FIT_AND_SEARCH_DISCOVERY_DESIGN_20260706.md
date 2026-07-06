# SJC Intel — Schema Fit and Search Discovery Design

**Date:** 2026-07-06
**Purpose:** Test proposed entity/event/time/claim schema against actual SJC
records. Evaluate search-driven news discovery layer design.

---

## Executive Summary

The proposed schema fits the actual SJC data well but has three areas of
overlap: **event** and **milestone** share substantial structure and should
be merged; **temporal assertion** is essential but can be modeled as a
specialization of the merged event/milestone rather than a separate table;
and **claim** can remain a thin JSON layer until a publication workflow exists.

**Worst fit:** `source_document` is redundant with the existing `source_event`
pattern. The file-backed `intel_item` YAML + `source_event` YAML already capture
document provenance.

**Best fit:** `entity`, `alias`, `location`, and `relationship` map cleanly onto
actual data patterns. The temporal assertion concept correctly models the
"changing dates" pattern seen in real records.

**Minimum viable schema: 9 tables** (not 15+): entities, entity_aliases,
locations, entity_locations, events (merged with milestones), temporal_assertions,
relationships, search_runs, search_candidates.

---

## Section 1 — Schema Applied to Real Records

### 1.1 SR 207 Water Reclamation Facility (2 items, 2 milestones)

```
Item A: SJC-UTIL-20260603-0003     Item B: SJC-CN-20260626-0001
Date:   2025-12-19                   Date:   2026-06-23
Title:  "$191 Million SR 207 WRF    "SJC's Largest-Ever Capital Improvement
         Phase 2 Approved"           Project Now Serving Residents"
Beat:   (none)                       utilities_water
Topics: infrastructure,              infrastructure, environment
         county_government
Status: verified                     verified
```

**Schema mapping:**

| Concept | Field | Source | Derivation |
|---------|-------|--------|------------|
| **Entity** | entity_id | NEW: `ENT-INFRA-SR-207-WRF` | Already in tracked_entities.yaml |
| | canonical_name | "SR 207 Water Reclamation Facility Phase 2" | Directly present |
| | entity_type | infrastructure_project | Already classified |
| | status | operational | Derived from latest milestone |
| **Event A** | event_id | NEW: `EVT-PROJ-SR207WRF-APPROVAL` | | |
| | event_type | approval | LLM from text |
| | subject_entity_id | ENT-INFRA-SR-207-WRF | Directly present |
| | scheduled_start | 2025-12-19 | Directly present (meeting date) |
| | title | "Phase 2 Approved" | Directly present |
| **Event B** | event_id | NEW: `EVT-PROJ-SR207WRF-OPERATIONAL` | | |
| | event_type | substantial_completion | LLM from text |
| | subject_entity_id | ENT-INFRA-SR-207-WRF | Directly present |
| | actual_start | 2026-06-23 | Directly present |
| **Temporal A1** | assertion_type | actual_approval | LLM |
| | asserted_date | 2025-12-19 | Directly present |
| | superseded_by | (none — first record) | |
| **Temporal A2** | assertion_type | actual_opening | LLM |
| | asserted_date | 2026-06-23 | Directly present |
| **Relationship** | relationship_type | same_project | Entity link |
| | subject_id | EVT-PROJ-SR207WRF-APPROVAL | |
| | object_id | EVT-PROJ-SR207WRF-OPERATIONAL | |
| **Claim** | subject | SR 207 WRF | |
| | predicate | cost | |
| | object_text | "$191.8 million" | LLM from text |
| | numeric_value | 191800000 | LLM from text |

**Fields marked:**
- `directly_present`: entity_id, entity_type, event dates, titles
- `LLM candidate`: dollar amount extraction, event_type classification,
  milestone_type classification
- `deterministically_derivable`: relationship linking (matching entity name),
  timeline ordering (by date)

### 1.2 Phase III Water Shortage (2 sources, same event)

```
Item A: SJC-UTIL-20260603-0001    Item B: SJC-CN-20260603-0005
Source: sjc_utility_department     Source: sjc_county_news
Date:   2026-05-11                  Date:   2026-05-13
Title:  "Phase III Extreme Water    "SJC Enters Phase III Extreme
         Shortage Declaration"        Water Shortage Declaration"
Urgency: URGENT                     Urgency: URGENT
Topics: environment, infrastructure, environment, public_notices,
        emergency_alerts            emergency
Status: verified                    Status: verified
```

**Schema mapping:**

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | NEW: `ENT-ENV-PHASE-III-WATER-SHORTAGE` (event-entity) | LLM — it's a recurring event type |
| | entity_type: restriction | LLM |
| **Event** | NEW: `EVT-ENV-WATER-PHASEIII-20260511` | |
| | event_type: restriction | LLM |
| | scheduled_start: 2026-05-11 | Directly present |
| | scheduled_end: (unknown, ongoing) | LLM from text |
| **Temporal** | assertion_type: restriction_active | |
| | asserted_start: 2026-05-11 | Directly present |
| | asserted_end: (not announced) | Directly missing |
| | supersession: (first record) | |
| **Relationship** | same_event between both items | Deterministic (same title, same date range) |
| | entity: SJRWMD (issuing agency) | LLM from text |
| **Claim** | "Residential irrigation limited to 1 day/week" | LLM from text |
| | "Phase III Extreme Water Shortage declared by SJRWMD" | Directly present |

**Key finding:** Two sources, same event. No entity links. Dedupe keys differ.
This is the clearest example of why relationship linking is essential.

### 1.3 Bushrangers Brewery (2 permits, 1 entity)

```
Item A: SJC-NBOR-20260704-0008      Item B: SJC-NBOR-20260704-0009
Title:  ZVAR 2025000035 Bushrangers  SUPMAJ 2025000030 Bushrangers
         Brewery                      Brewery
App ID: ZVAR 2025000035              SUPMAJ 2025000030
Date:   7/9/2026                     7/9/2026
Beat:   rezoning_comp_plan_dri       site_plans_permits_construction
```

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | NEW: `ENT-BIZ-BUSHRANGERS-BREWERY` | Directly present (title) |
| | entity_type: business | LLM |
| | status: proposed | Derived |
| **Event A** | event_type: application_submitted | |
| | title: "Zoning Variance for alcohol sales near church" | Directly present |
| | scheduled_start: 2026-07-09 | Directly present |
| **Event B** | event_type: application_submitted | |
| | title: "Special Use Permit for microbrewery in IW zoning" | Directly present |
| **Relationship** | related_to between Event A and Event B | Deterministic (same entity name) |
| | located_at: 470 SR 207 | LLM from description |

### 1.4 St. Thomas Island Cell Tower (single application)

```
Item: SJC-NBOR-20260704-0001
Title: SUPMAJ 2025000029 St. Thomas Island Parkway Cell Tower
Date: 7/23/2026
App ID: SUPMAJ 2025000029
Description: 180-foot monopole tower in Open Rural (OR) zoning
```

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | NEW: `ENT-INFRA-ST-THOMAS-TOWER` | Directly present (title) |
| | entity_type: infrastructure_project | LLM |
| **Event** | event_type: public_hearing | Directly present (category=Meeting) |
| | scheduled_start: 2026-07-23 | Directly present |
| **Location** | raw_address: St. Thomas Island Parkway | Directly present (title) |
| | normalized: (need geocoding) | External lookup |
| **Temporal** | assertion_type: scheduled_hearing | |
| | asserted_start: 2026-07-23 | Directly present |

### 1.5 Nothing Putt Fun Rezoning (BCC agenda item)

```
Item: SJC-BCC-20260120-0002
Title: Public Hearing * REZ 2025-11 Nothing Putt Fun
Date: 2026-01-20
Address: 7250 and 7280 US 1 North
Action type: public_hearing
Signal: high_signal
```

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | NEW: `ENT-BIZ-NOTHING-PUTT-FUN` | Directly present (title) |
| | entity_type: business | LLM |
| **Entity** | NEW: `ENT-PARCEL-7250-US-1` | Deterministic from address |
| **Event** | event_type: agenda_item | Deterministic (action_type) |
| | actually_occurred: 2026-01-20 | Directly present |
| **Location** | raw_address: 7250 and 7280 US 1 North | Directly present |
| | parcel_size: 3.98 acres | LLM from text |
| **Temporal** | assertion_type: scheduled_hearing | |
| | asserted_start: 2026-01-20 | Directly present |
| | status: occurred | Deterministic |
| **Claim** | "REZ 2025-11 proposes rezoning 3.98 acres from CN to CHT" | LLM from text |

### 1.6 SilverLeaf Publix Opening (local media)

```
Item: SJC-SL-20260704-0001
Source: st_johns_citizen (local media)
Title: SilverLeaf's new 55,000 sq. ft. mega Publix
Date: 2026-03-26
Address: 1975 SilverLeaf Parkway
Community: silverleaf
```

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | ENT-RETAIL-PUBLIX-SILVERLEAF | Already in tracked_entities |
| **Event** | event_type: opening | Directly present |
| | actual_start: 2026-03-26 | Directly present |
| **Location** | raw_address: 1975 SilverLeaf Parkway | Directly present |
| | community_id: silverleaf | Directly present |
| **Temporal** | assertion_type: actual_opening | |
| | asserted_start: 2026-03-26 | Directly present |
| | source_confidence: medium (media source) | Derivable from source_type |
| **Claim** | "55,701 sq ft store with pharmacy, beer/wine cafe, scratch bakery" | Directly present |

### 1.7 SilverLeaf K-8 School (expected opening)

```
Item: SJC-SL-20260704-0002
Title: "St. Johns officials give sneak peek of new Silverleaf K-8 school"
Date: 2025-05-07 (article) / expected opening: 2026-2027 school year (Aug 2026)
Status: under_construction
```

| Concept | Value | Derivation |
|---------|-------|------------|
| **Entity** | ENT-EDU-SILVERLEAF-K8 | Already in tracked_entities |
| | status: under_construction | Already in tracked_entities |
| **Event** | event_type: construction_progress | LLM |
| | title: "Sneak peek/topping-out ceremony" | Directly present |
| **Temporal C1** | assertion_type: expected_opening | LLM from text |
| | asserted_start: 2026-08 (approximate) | LLM from "2026-2027 school year" |
| | date_precision: season | Human decision |
| | supersession: (first record) | |
| **Claim** | "190,000 sq ft, 3 stories, 73 classrooms, ~1,500 students" | Directly present |

**CRITICAL PATTERN:** "expected opening for 2026-2027 school year" is the
canonical example of why `date_precision` and `temporal_language` exist.
The source says "August 2026" implicitly. If a later item says "opening
delayed to January 2027," the temporal assertion model captures the delta.

### 1.8 CR 2209 Connector (completed road project)

```
Item: SJC-SL-20260704-0004
Title: "Road relief: Here's your first look at St. Johns County's newest highway"
Date: 2025-10-28
Description: 3-mile, 4-lane divided roadway connecting IGP to SilverLeaf Pkwy
Community: silverleaf
Geographic scope: multi_community
```

| Concept | Value |
|---------|-------|
| **Entity** | ENT-ROAD-CR-2209-CONNECTOR (already tracked) |
| | entity_type: road_project |
| | status: completed |
| **Event** | event_type: substantial_completion |
| | actual_start: 2025-10-28 |
| **Temporal** | assertion_type: actual_opening |
| | asserted_start: 2025-10-28 |
| **Location** | from: International Golf Parkway |
| | to: SilverLeaf Parkway |
| | LLM from text |

### 1.9 BCC Septic-to-Sewer Policy (policy discussion)

```
Item: SJC-BCC-20260120-0005
Title: "Septic-to-Sewer Connection Policy Discussion"
Action type: regular_agenda
Signal: high_signal
```

| Concept | Value |
|---------|-------|
| **Entity** | NEW: `ENT-POLICY-SEPTIC-TO-SEWER` (policy entity) |
| | entity_type: other |
| **Event** | event_type: agenda_item |
| | actually_occurred: 2026-01-20 |
| **Relationship** | affects: countywide residents |
| **Claim** | "BOCC discussed septic-to-sewer connection policy" |
| | "Policy discussion follows Oct 7, 2025 BOCC direction" |

### 1.10 Free Chlorine Burnout (utility interruption with window)

```
Item: SJC-UTIL-20260603-0002
Title: "Free Chlorine Burnout Scheduled June 1–21"
Date: 2026-05-26
Urgency: timely
```

| Concept | Value |
|---------|-------|
| **Entity** | NEW: `ENT-INFRA-CR214-WTP` (County Road 214 Water Treatment Plant) |
| | entity_type: utility_facility |
| **Event** | event_type: utility_interruption |
| | scheduled_start: 2026-06-01 |
| | scheduled_end: 2026-06-21 |
| **Temporal** | assertion_type: estimated_duration |
| | asserted_start: 2026-06-01 |
| | asserted_end: 2026-06-21 |
| | date_precision: exact_day |
| **Claim** | "Temporary switch to free chlorine disinfection — water remains safe" |

### 1.11 East Peyton Parkway Traffic Light Activation (road action)

```
Item: SJC-NBOR-20260704-0019
Title: "NBR - EAST PEYTON PKWY TRAFFIC LIGHT ACTIVATION"
Date: 7/14/2026
Beat: roadwork_traffic
Description: Three intersections switching from flash to full operation
```

| Concept | Value |
|---------|-------|
| **Entity** | NEW: `ENT-ROAD-EAST-PEYTON-PKWY` |
| | entity_type: road_segment |
| **Entities** | Intersections: Bowling Green Way, UF Health North, UF Health South |
| **Event** | event_type: road_closure (signal change) |
| | scheduled_start: 2026-07-14 |
| **Location** | Three intersections on East Peyton Parkway |
| **Temporal** | assertion_type: scheduled_closure |
| | asserted_start: 2026-07-14 |

### 1.12 CDD Election (governance event)

```
Item: six_mile_creek_cdd-002
Title: "Notice of Qualifying Period for Six Mile Creek CDD Board Candidates"
Content: Qualifying period for Seats 2 and 4, coincides with Nov 2026 election
Interest: HIGH
```

| Concept | Value |
|---------|-------|
| **Entity** | `six_mile_creek_cdd` (source_id → CDD entity) |
| | entity_type: cdd |
| **Event** | event_type: election |
| | scheduled_start: (qualifying period) |
| **Temporal** | assertion_type: scheduled_election |
| | "November 2026 general election" — date_precision: month |
| **Claim** | "Two CDD board seats up for election — four-year terms" |

### 1.13 Hurricane Season Prep (seasonal)

```
Item: SJC-EM-20260626-0001
Title: "Residents Urged to Prepare as 2026 Atlantic Hurricane Season Begins"
Date: 2026-06-01
Urgency: timely
```

| Concept | Value |
|---------|-------|
| **Event** | event_type: emergency_notice |
| **Temporal** | assertion_type: seasonal_window |
| | asserted_start: 2026-06-01 |
| | asserted_end: 2026-11-30 (season end, not specified) |
| | date_precision: season |

### 1.14 Double Murder Arrest (sensitive crime)

```
Item: SJC-SJSO-20260603-0004
Title: "Arrest made in connection to 2023 double murders"
Sensitivity: high
Human review: required
```

| Concept | Value |
|---------|-------|
| **Entity** | NEW: `ENT-PERSON-DERRICK-WALDEN` (extreme caution — privacy) |
| **Entity** | NEW: `ENT-INCIDENT-2023-DOUBLE-MURDER` (incident entity) |
| **Event** | event_type: other (arrest) |
| | actually_occurred: 2025-11-25 |
| **Review** | publication_status: human_review_required |
| **Privacy** | Named individuals should not auto-enter entity registry |

### 1.15 Recycling Driver (rejected noise)

```
Item: SJC-CN-20260626-0004
Title: "SJC Highlights Special Bond Between Recycling Driver and Three-Year-Old"
Status: rejected_noise
```

| Concept | Value |
|---------|-------|
| **Event** | event_type: other |
| **Temporal** | no date assertion needed |
| **Status** | review_status: rejected_noise |
| **Schema implication:** Not every item produces events or claims. |
| The schema must accept that some items are noise. |

---

## Section 2 — Temporal Model Stress Test

### 2.1 SR 207 WRF Date Chain

```
Source A (utility, Dec 19 2025):
  "Phase 2 approved during Dec 19 BOCC meeting"
  → temporal_assertion: approval_date = 2025-12-19 (exact_day, actual)

Source B (county news, Jun 23 2026):
  "Now serving residents"
  → temporal_assertion: operational_date = 2026-06-23 (exact_day, actual)

Timeline:
  [2025-12-19] → approved
  [2026-06-23] → operational
  Gap: ~6 months from approval to operational
  Question: was there a construction start date? Not in current records.
  → temporal_assertion: construction_start = UNKNOWN (gaps are acceptable)
```

### 2.2 SilverLeaf Publix Date Chain

```
Current records:
  [2026-03-26] opened (St. Johns Citizen article)
  No "proposed" or "under construction" dates exist in current data.
  The tracked_entity says lifecycle_status: completed.
  
If we had hypothetical earlier articles:
  [2025-06-??] "Publix planned for SilverLeaf" → expected_opening: 2026-Q1
  [2025-12-??] "Publix construction underway" → construction_start: 2025-12
  [2026-03-01] "Publix opening March 26" → scheduled_opening: 2026-03-26
  [2026-03-26] opened → actual_opening: 2026-03-26

Temporal assertions:
  TA1: expected_opening = 2026-Q1 (superseded)
  TA2: scheduled_opening = 2026-03-26 (supersedes TA1)
  TA3: actual_opening = 2026-03-26 (supersedes TA2)

Key: TA1 is preserved even though superseded. Historical estimates matter.
```

### 2.3 SilverLeaf K-8 School — Expected Opening

```
Current:
  [2025-05-07] "opening for 2026-2027 academic year"
  → expected_opening: 2026-08 (month_precision)

  tracked_entity lifecycle: under_construction

Missing:
  Construction start date? Not in records.
  Delays? Not in records.
  Name announcement? Not in records.
  
Temporal assertion:
  TA1: expected_opening = 2026-08 (approximate_month)
       source: st_johns_citizen (media)
       date_precision: season ("2026-2027 school year")
       confidence: medium

If a future article says:
  [2026-07-15] "School opening delayed to January 2027"
  TA2: expected_opening = 2027-01 (supersedes TA1)
       change_detected: +5 months delay
       alert_trigger: YES
```

### 2.4 CR 2209 Connector — Completion

```
Current:
  [2025-10-28] opened (St. Johns Citizen)
  tracked_entity lifecycle: completed

Single event, no date changes. Simple temporal:
  TA1: actual_opening = 2025-10-28 (exact_day)
       supersession: none (single source)
       confidence: medium (media source)

If a county record says:
  [2025-10-28] "County road CR 2209 connector opened"
  → matched to same event via entity link (ENT-ROAD-CR-2209-CONNECTOR)
  → two source_assertions for same temporal fact → confidence increases
```

### 2.5 Phase III Water Shortage — Active Period

```
Source A: "Beginning May 11, 2026"
Source B: "issued Phase III declaration"

Current temporal:
  TA1: restriction_start = 2026-05-11 (exact_day)
  TA2: restriction_end = UNKNOWN (not announced)

The water shortage may be ongoing. Temporal assertions with no end date
are common for restrictions. "No end date announced" is itself a finding.
```

### 2.6 Railroad Crossing Closure — Short Closure Window

```
Item: SJC-CN-20260626-0002
"Temporarily close W. King Street and Kinlaw Road crossings"
No specific closure dates in current records.

TA1: scheduled_closure = (unknown date)
     date_precision: unknown
     status: announced
     
If a follow-up item provides dates:
  TA2: scheduled_closure = 2026-07-10
       scheduled_reopening = 2026-07-11
       supersedes TA1
```

### 2.7 Free Chlorine Burnout — Windowed Work

```
Item: SJC-UTIL-20260603-0002
"Scheduled June 1–21"

TA1: scheduled_start = 2026-06-01
     scheduled_end = 2026-06-21
     date_precision: exact_day (both)
     status: announced

If completed on time:
  TA2: actual_end = 2026-06-21
       matches scheduled → no alert needed, confidence increases
```

### 2.8 Hypothetical: Hospital Expected April → Delayed June → Opened

```
Sequence:
1. [2025-11-01] "Ascension St. Vincent's Nocatee expected late April"
   TA1: expected_opening = 2026-04
        date_precision: late_month
        source: st_johns_citizen

2. [2026-03-15] "Ascension opening pushed to June"
   TA2: expected_opening = 2026-06
        date_precision: month
        supersedes: TA1
        change: +2 months
        alert: YES

3. [2026-06-15] "Ascension St. Vincent's Nocatee now open"
   TA3: actual_opening = 2026-06-15
        date_precision: exact_day
        supersedes: TA2
        alert: YES
```

### 2.9 Hypothetical: Road Project Q3 → +6 Weeks

```
1. [2026-01-20] "BUILD grant applications for SR 16 / CR 210 projects"
   TA1: expected_completion = 2026-Q3
        date_precision: quarter
        source: BCC agenda item (official)

2. [2026-06-01] "SR 16 widening delayed by materials shortage"
   TA2: expected_completion = 2026-Q3 + 6 weeks ≈ 2026-11-15
        date_precision: approximate_month
        supersedes: TA1
        delay_reason: materials shortage (stored as temporal_language)
        alert: YES
```

### 2.10 Hypothetical: School Opening August → January

```
1. [2025-05-07] "Opening for 2026-2027 school year"
   TA1: expected_opening = 2026-08
        date_precision: season

2. [2026-04-01] "SilverLeaf K-8 construction delayed"
   TA2: expected_opening = 2027-01
        supersedes: TA1
        delay: +5 months
        alert: YES
```

### Schema Recommendation: Merge Event and Milestone

**Finding:** `event` and `milestone` are the same concept at different granularity.
An approval "event" IS the "approved" milestone. A construction_progress "event"
IS the construction_started milestone. There is no clear boundary.

**Recommendation:** Single `event` table with `event_type` encompassing both
current event types and milestone types. Remove separate `milestone` concept.
**Simplifies queries, avoids double-entry, preserves all temporal semantics.**

For entity lifecycle aggregation, use a VIEW or query:
`SELECT entity_id, event_type AS milestone_type, effective_at`
`FROM events WHERE entity_id = X ORDER BY effective_at`

**Verdict on temporal_assertion:** Essential and distinct from event.
One event may have multiple temporal assertions (scheduled vs actual, different
sources). The temporal_assertion table preserves all historical estimates.
**Keep separate.**

---

## Section 3 — “What Changed?” Query Test

### Q1: What changed since last week?

```sql
-- New intel items since last week
SELECT item_id, title, source_id, discovered_at
FROM intel_items
WHERE discovered_at >= now() - interval '7 days'
  AND review_status IN ('verified', 'pending_review');

-- New events since last week
SELECT e.event_id, e.title, e.event_type, e.occurred_at
FROM events e
WHERE e.discovered_at >= now() - interval '7 days';

-- New temporal assertions (date changes)
SELECT ta.assertion_id, ta.subject_entity_id, ta.assertion_type,
       ta.asserted_start, ta.supersedes_assertion_id,
       ta_prev.asserted_start AS previous_date
FROM temporal_assertions ta
JOIN temporal_assertions ta_prev ON ta.supersedes_assertion_id = ta_prev.assertion_id
WHERE ta.observed_at >= now() - interval '7 days';

-- New relationships
SELECT r.* FROM relationships r
WHERE r.discovered_at >= now() - interval '7 days';
```

### Q2: Which projects were delayed?

```sql
-- Entities where most recent temporal assertion supersedes an earlier one
-- with a LATER date than previously asserted
SELECT ta.subject_entity_id, e.canonical_name,
       ta.asserted_start AS current_estimate,
       ta_prev.asserted_start AS previous_estimate,
       ta.asserted_start - ta_prev.asserted_start AS delay_days
FROM temporal_assertions ta
JOIN temporal_assertions ta_prev ON ta.supersedes_assertion_id = ta_prev.assertion_id
JOIN entities e ON e.entity_id = ta.subject_entity_id
WHERE ta.assertion_type IN ('expected_opening', 'expected_completion', 'expected_start')
  AND ta.asserted_start > ta_prev.asserted_start
  AND ta.observed_at >= (SELECT max(observed_at) FROM temporal_assertions) - interval '30 days';
```

### Q3: What is scheduled in the next 30 days?

```sql
SELECT e.canonical_name, ev.event_type, ta.asserted_start
FROM temporal_assertions ta
JOIN entities e ON e.entity_id = ta.subject_entity_id
JOIN events ev ON ev.event_id = ta.event_id
WHERE ta.assertion_type IN ('scheduled_hearing', 'scheduled_start', 'expected_opening')
  AND ta.asserted_start BETWEEN now() AND now() + interval '30 days'
  AND ta.status = 'current'
ORDER BY ta.asserted_start;
```

### Q4: What opened recently?

```sql
SELECT e.canonical_name, ta.asserted_start AS opened_date
FROM temporal_assertions ta
JOIN entities e ON e.entity_id = ta.subject_entity_id
WHERE ta.assertion_type = 'actual_opening'
  AND ta.asserted_start >= now() - interval '90 days'
  AND ta.status = 'current'
ORDER BY ta.asserted_start DESC;
```

### Q5: What is overdue?

```sql
-- Entities where expected completion has passed but no actual completion
SELECT e.canonical_name, ta.asserted_start AS expected_by
FROM temporal_assertions ta
JOIN entities e ON e.entity_id = ta.subject_entity_id
LEFT JOIN temporal_assertions ta_actual
  ON ta_actual.subject_entity_id = e.entity_id
  AND ta_actual.assertion_type IN ('actual_completion', 'actual_opening')
WHERE ta.assertion_type IN ('expected_completion', 'expected_opening')
  AND ta.asserted_start < now()
  AND ta_actual.assertion_id IS NULL
  AND ta.status = 'current';
```

### Q6: Which estimates are unconfirmed?

```sql
-- Temporal assertions from media sources without official confirmation
SELECT ta.*
FROM temporal_assertions ta
JOIN source_documents sd ON sd.source_document_id = ta.source_document_id
JOIN sources s ON s.source_id = sd.source_id
WHERE s.source_type = 'local_media'
  AND NOT EXISTS (
    SELECT 1 FROM temporal_assertions ta2
    JOIN source_documents sd2 ON sd2.source_document_id = ta2.source_document_id
    JOIN sources s2 ON s2.source_id = sd2.source_id
    WHERE ta2.subject_entity_id = ta.subject_entity_id
      AND ta2.assertion_type = ta.assertion_type
      AND s2.authority_level = 'official'
  );
```

### Q7: Conflicting dates from different sources?

```sql
-- Two temporal assertions for same entity+type with different dates
SELECT ta1.subject_entity_id, ta1.assertion_type,
       ta1.asserted_start AS date_from_source_a,
       ta2.asserted_start AS date_from_source_b,
       ta1.source_document_id, ta2.source_document_id
FROM temporal_assertions ta1
JOIN temporal_assertions ta2
  ON ta1.subject_entity_id = ta2.subject_entity_id
  AND ta1.assertion_type = ta2.assertion_type
  AND ta1.assertion_id <> ta2.assertion_id
  AND ta1.status = 'current'
  AND ta2.status = 'current'
  AND ta1.asserted_start <> ta2.asserted_start;
```

### Q8: Entities with no update after expected completion?

```sql
SELECT e.canonical_name, ta.asserted_start AS expected_by
FROM temporal_assertions ta
JOIN entities e ON e.entity_id = ta.subject_entity_id
WHERE ta.assertion_type IN ('expected_completion', 'expected_opening')
  AND ta.asserted_start < now() - interval '30 days'
  AND ta.status = 'current'
  AND NOT EXISTS (
    SELECT 1 FROM intel_items ii
    WHERE ii.source_id IN (
      SELECT sd.source_id FROM source_documents sd
      JOIN source_document_entities sde ON sde.source_document_id = sd.source_document_id
      WHERE sde.entity_id = e.entity_id
    )
    AND ii.discovered_at > ta.asserted_start
  );
```

### Q9: What changed specifically for SilverLeaf?

```sql
SELECT e.canonical_name, ev.event_type, ta.assertion_type,
       ta.asserted_start, ta.date_precision
FROM entities e
JOIN entity_locations el ON el.entity_id = e.entity_id
JOIN locations l ON l.location_id = el.location_id
JOIN events ev ON ev.subject_entity_id = e.entity_id
LEFT JOIN temporal_assertions ta ON ta.event_id = ev.event_id AND ta.status = 'current'
WHERE l.community_id = 'silverleaf'
ORDER BY ta.asserted_start DESC NULLS LAST;
```

---

## Section 4 — News Search Discovery Design

### 4.1 Search Templates

| # | Template Name | Trigger | Cadence | Query Terms | Date Window | Source Pref | Browser? | LLM? | Human? |
|---|--------------|---------|---------|-------------|-------------|-------------|----------|------|--------|
| 1 | `entity_name` | Entity created or interest added | Weekly | `"{entity.canonical_name}" ({entity.aliases})` | Since last run | Authority: official > media | No | No | No |
| 2 | `project_milestone` | Entity with expected completion approaching | Weekly/Ad hoc | `"{entity.name}" update|progress|delay|opening` | Expected date - 3mo | All | Low | No |
| 3 | `delay_check` | Entity past expected completion | Daily/Weekly | `"{entity.name}" delayed|postponed|rescheduled` | Now - 30d | Media | No | Medium | Yes |
| 4 | `site_specific` | Entity with address | Weekly | `"{address}" {entity.name}"` | Since last run | Official records | No | Low | No |
| 5 | `road_closure` | Road projects | Weekly | `"{road_name}" closure|maintenance|detour` | Since last run | County + media | No | Low | No |
| 6 | `school_opening` | School entity with future opening | Monthly | `"{school_name}" opening|construction|delay` | Next 6 months | School + media | No | Low | No |
| 7 | `hospital_opening` | Healthcare entity with future opening | Monthly | `"{hospital_name}" opening|construction|delayed` | Next 6 months | Health + media | No | Low | No |
| 8 | `development_approval` | Development entity under review | Weekly | `"{project_name}" approval|denied|hearing|permit` | Since last run | Official + media | No | Low | No |
| 9 | `utility_outage` | Utility facility | Daily/Seasonal | `"{utility_name}" outage|boil|maintenance|alert` | Since last run | Utility site | No | Low | Yes (alerts) |
| 10 | `cdd_meeting` | CDD entity | Monthly | `"{CDD_name}" meeting|agenda|workshop` | Next 60 days | CDD site + notices | No | No | No |
| 11 | `official_confirmation` | Media-reported claim needing verification | Ad hoc | `"{claim_keywords}" site:sjcfl.us OR site:stjohnsclerk.com` | After media report | Official .gov | No | Medium | Yes |
| 12 | `media_coverage` | Official action needing public context | Ad hoc | `"{action_keywords}" site:sjcitizen.com OR site:staugustine.com` | After official action | Local media | No | Low | No |
| 13 | `project_hearing` | Entity with upcoming hearing | Weekly before hearing | `"{project_name}" hearing|public meeting|agenda` | Next 60 days | Official + media | No | Low | No |
| 14 | `tracked_entity_all` | All tracked entities (catch-all) | Weekly | All entity names and aliases OR'd | Since last run | All | No | Medium | No |
| 15 | `stale_temporal` | Entity with no update near expected date | Daily | `"{entity.name}" {date_keywords}` | Expected date ± 2mo | All | No | Medium | Yes |

### 4.2 Search Runner Interface

```python
@dataclass
class SearchTemplate:
    template_id: str
    name: str
    query_terms: list[str]          # May contain {entity.name} placeholders
    source_preference: list[str]    # Domain or source_type hints
    requires_browser: bool
    requires_llm_relevance: bool    # For ambiguous results
    
@dataclass
class SearchRun:
    run_id: str
    template_id: str
    cadence: str                    # hourly, daily, weekly, monthly, ad_hoc, event_triggered
    triggered_by: str               # entity_id, event_id, manual
    target_entity_ids: list[str]
    started_at: datetime
    completed_at: datetime | None
    provider_used: str              # google, bing, site_search, etc.
    query_executed: str             # Actual search query sent
    result_count: int
    accepted_count: int
    run_status: str                 # planned, running, ok, partial, failed
    
@dataclass
class SearchCandidate:
    candidate_id: str
    search_run_id: str
    url: str
    title: str
    snippet: str
    publisher: str
    published_at: datetime | None
    retrieved_at: datetime
    matched_entity_ids: list[str]
    matched_event_ids: list[str]
    relevance_score: float          # 0.0 - 1.0
    relevance_reason: str
    duplicate_of_document_id: str | None
    fetch_status: str               # pending, fetched, rejected, accepted
    review_status: str              # pending, confirmed, rejected
```

---

## Section 5 — Search Orchestration Model

### 5.1 Frequency Without Hard-Coding

The data model should store cadence as a string/computed field, not hard-code
polling intervals:

```python
# Cadence evaluation: given last_run and cadence_string, is it due?
def is_due(last_run: datetime | None, cadence: str, now: datetime) -> bool:
    match cadence:
        case 'hourly':    return not last_run or (now - last_run).hours >= 1
        case 'daily':     return not last_run or (now - last_run).days >= 1
        case 'weekly':    return not last_run or (now - last_run).days >= 7
        case 'monthly':   return not last_run or (now - last_run).days >= 30
        case 'ad_hoc':    return False  # manually triggered only
        case 'event_triggered': return False  # triggered by event/date evaluation
        case _:           return False
```

### 5.2 Trigger Sources

| Trigger | Source | Mechanism |
|---------|--------|-----------|
| Scheduled (hourly/daily/weekly/monthly) | Search template | Interval check (is_due) |
| Entity created | Entity registry | Immediate first search |
| Expected date approaching | Temporal assertion | Date math: expected - 4 weeks ≤ now |
| Entity past due | Temporal assertion | Date math: expected + 1 week < now |
| Stale check | Last search | No update for entity in N days |
| Media report received | Intel item ingestion | Search for official confirmation |
| Official action received | Intel item ingestion | Search for media coverage |
| Manual/Buddy request | CLI or UI | Immediate execution |

### 5.3 Search Provider Abstraction

```python
@runtime_checkable
class SearchProvider(Protocol):
    def search(self, query: str, **kwargs) -> list[SearchResult]: ...
    def search_batch(self, queries: list[str]) -> list[list[SearchResult]]: ...

class GoogleSearchProvider:
    def search(self, query, **kwargs): ...
    
class BingSearchProvider:
    def search(self, query, **kwargs): ...
    
class SiteSearchProvider:
    """Direct HTTP GET on known .gov/.org pages"""
    def search(self, query, **kwargs): ...
```

**Browser automation** is a separate concern. Sources requiring JS execution
(scrolling, clicking, form submission) should use a distinct `BrowserSearchProvider`
that wraps Playwright/Selenium. This should be a later implementation phase.

**LLM relevance filtering** applies after the search provider returns results:
- Deterministic: domain filter, date filter, exact entity name match
- LLM: relevance classification for ambiguous results

### 5.4 Deduplication

```sql
-- Before creating SearchCandidate, check:
SELECT 1 FROM source_documents
WHERE content_hash = %(content_hash)s
   OR canonical_url = %(url)s
LIMIT 1;
```

### 5.5 Run Budget

```python
@dataclass
class SearchBudget:
    max_searches_per_run: int = 50
    max_results_per_search: int = 10
    max_total_results: int = 500
    rate_limit_per_second: float = 1.0
    max_browser_sessions: int = 1
```

---

## Section 6 — Discovery-to-Knowledge Flow

### 6.1 SR 207 WRF: Complete Flow

```
Step 1: Entity exists (ENT-INFRA-SR-207-WRF)
        → already in tracked_entities.yaml
        → aliases: ["SR 207 WRF Phase 2", "SR 207 Water Reclamation Facility"]
        
Step 2: Search template evaluated
        template_1 (entity_name): cadence=weekly, due=True
        
Step 3: Search run created
        query: '"SR 207 Water Reclamation Facility" OR "SR 207 WRF" update'
        provider: Google
        date_window: since last run
        
Step 4: Results returned → SearchCandidates created
        If duplicate of existing source_document → mark as duplicate
        If new → fetch_status = pending
        
Step 5: Candidate fetched → SourceDocument created
        HTML/PDF fetched, content_hash computed
        
Step 6: Intel item extracted
        From fetched document: title, summary, topics, etc.
        extraction_method: hermes-search-worker (future)
        
Step 7: Entity/Event/Time extraction
        entity: matched to ENT-INFRA-SR-207-WRF
        event: operational status update
        temporal: actual_update_date
        
Step 8: Relationship linking
        linked to existing approval event → "same project, new milestone"
        
Step 9: Review queue entry
        new item in review queue
        marked with search_run provenance
        
Step 10: After review (if approved):
         → entity.status potentially updated
         → temporal assertion chain extended
         → resident-facing outputs updated (timeline, digest, entity page)
```

### 6.2 SilverLeaf K-8: Unknown Discovery from News

```
Step 1: No entity yet, but search discovers article
        search_template: site_specific on "SilverLeaf K-8 school"
        OR: general search on "SilverLeaf" + "school" + "construction"
        
Step 2: Article fetched, intel item created
        title: "SilverLeaf K-8 school topping-out ceremony"
        
Step 3: Entity extraction (LLM)
        candidate entity: "SilverLeaf K-8 School"
        candidate type: education_facility
        
Step 4: Entity created (pending review)
        entity_id: (to be assigned)
        status: proposed (entity registry sense)
        created_from: source document
        
Step 5: Event extraction
        event_type: construction_progress
        date: 2025-05-07
        
Step 6: Temporal assertion
        expected_opening: 2026-2027 school year
        date_precision: season
        source: media
        
Step 7: Human review
        Is this a real entity? Yes.
        Is the date reliable? Medium (media source, needs official confirmation).
        
Step 8: Entity promoted to tracked
        Added to entity registry
        Search templates created for this entity
        
Step 9: Later: official confirmation search triggered
        template: official_confirmation
        query: "SilverLeaf K-8 school site:stjohns.k12.fl.us"
```

---

## Section 7 — Schema-Fit Findings

### 7.1 Essential Now

| Concept | Why | Implementation |
|---------|-----|---------------|
| **entity** | Cross-source linking, search, alerts, timelines | Expand `tracked_entities` → full entities table |
| **entity_alias** | Multiple names for same thing (Comcast ROW, Bushrangers) | Sub-table of entities |
| **location** | Geo-filtering, map, proximity, neighborhood pages | New table, geocode from existing addresses |
| **event** | Calendar, timeline, change detection, alerts | Merge with milestone — single events table |
| **relationship** | Cross-source linking (same_project, same_event) | Link table with type enum |
| **search_run** | Provenance for discovered items, budget tracking | New table |
| **search_candidate** | Review queue for search results | New table |

### 7.2 Useful Soon

| Concept | Why | When |
|---------|-----|------|
| **temporal_assertion** | Date change tracking, delay detection, historical estimates | After events table is populated |
| **claim** | Publication-quality output, social posts, digests | After 50+ approved items |
| **publication** | Track what was sent to newsletter/social/web | After first downstream product |
| **source_document** | Raw fetch provenance, content de-dup | After search runner is active |

### 7.3 Defer

| Concept | Why Defer |
|---------|-----------|
| **full claim register** (BSDA-style) | Too early — need publication workflow first |
| **contradiction tracking** | Only relevant when multiple sources disagree on same claim |
| **versioned accepted claims** | Only relevant when claims are being published externally |
| **publication metrics** | Only relevant after publication exists |

### 7.4 Merge

| Concept | Merge Into | Reason |
|---------|-----------|--------|
| **milestone** | **event** | Same concept at same granularity. Every milestone IS an event. |
| **entity_alias** | entity table JSON | Could store as JSONB array initially, normalize later if needed |
| **intel_item** fields `topics[]`, `communities[]` | **relationship** table | These are relationships between items and topics/communities |

### 7.5 Remove (or Don't Add)

| Concept | Reason |
|---------|--------|
| **source_document** | Redundant with existing `source_event` + file-backed YAML. Add only when full-text search or raw artifact tracking is needed beyond current `raw_artifact_records`. |
| **separate claim table** | Claims should be a field on intel_item or a thin JSON layer until publication workflow exists. BSDA's full claim register is too heavy for SJC's current volume. |

### 7.6 Schema-Verified Questions

**Should event and milestone be merged?** YES. Every milestone is an event.
Approval event = approved milestone. Construction start event = construction_started milestone.
No query needs both tables.

**Should temporal_assertion be separate from event?** YES. One event can have
multiple temporal assertions (scheduled date, actual date, media-reported date,
official-confirmed date). The temporal_assertion table captures the "date said
by whom" provenance that enables change detection.

**Should entity_alias be a separate table?** Optional. JSONB array on entity
table is sufficient for initial implementation. Normalize when alias matching
performance becomes a concern.

**Should search_run be a table?** YES. Without it, discovered items have no
provenance chain. Cross-referencing search results back to search parameters
is essential for quality improvement.

---

## Section 8 — Minimum Viable Implementation Schema

### Recommended Tables (9 tables + link tables)

```sql
-- 1. ENTITIES
CREATE TABLE entities (
    entity_id       text PRIMARY KEY,       -- ENT-TYPE-SLUG
    canonical_name  text NOT NULL,
    entity_type     text NOT NULL,           -- development, road, school, cdd, business, etc.
    description     text,
    status          text NOT NULL DEFAULT 'tracked',  -- proposed, tracked, completed, etc.
    parent_entity_id text REFERENCES entities(entity_id),
    aliases         jsonb DEFAULT '[]',      -- [{alias: "SilverLeaf Publix", source: "st_johns_citizen", confidence: "high"}]
    authority_status text DEFAULT 'unconfirmed',  -- unconfirmed, source_confirmed, reviewed
    created_from_item_id text,               -- source intel_item that prompted creation
    created_at      timestamptz NOT NULL DEFAULT now(),
    reviewed_at     timestamptz,
    review_notes    text
);

-- 2. LOCATIONS
CREATE TABLE locations (
    location_id     text PRIMARY KEY,
    entity_id       text REFERENCES entities(entity_id),
    normalized_address text,
    raw_address     text,
    parcel_id       text,
    latitude        numeric(10,7),
    longitude       numeric(10,7),
    community_id    text,                    -- from communities.yaml
    district_id     text,
    geometry        jsonb,                  -- GeoJSON point/polygon
    precision       text DEFAULT 'approximate',  -- exact_address, intersection, community_level, county_wide
    geocoding_source text,
    confidence      text DEFAULT 'low'
);

-- 3. EVENTS (merged milestone)
CREATE TABLE events (
    event_id        text PRIMARY KEY,        -- EVT-TYPE-DATE-SEQ
    event_type      text NOT NULL,           -- approval, public_hearing, construction_start,
                                            -- substantial_completion, opening, delay, etc.
    subject_entity_id text REFERENCES entities(entity_id),
    location_id     text REFERENCES locations(location_id),
    title           text NOT NULL,
    description     text,
    source_item_ids text[] NOT NULL,         -- array of intel item IDs
    discovered_at   timestamptz NOT NULL,
    review_status   text DEFAULT 'pending_review'
);

-- 4. TEMPORAL ASSERTIONS
CREATE TABLE temporal_assertions (
    assertion_id        text PRIMARY KEY,
    event_id            text REFERENCES events(event_id),
    subject_entity_id   text REFERENCES entities(entity_id),
    assertion_type      text NOT NULL,       -- expected_opening, actual_opening, scheduled_hearing,
                                            -- estimated_duration, seasonal_window, etc.
    asserted_start      date,
    asserted_end        date,
    date_precision      text NOT NULL DEFAULT 'exact_day',
                                            -- exact_day, week, month, quarter, season, year, date_range, unknown
    temporal_language   text,               -- original source text ("early April", "by summer 2027")
    status              text DEFAULT 'current',  -- current, superseded, cancelled
    source_item_id      text,               -- intel item that provided this assertion
    supersedes_assertion_id text REFERENCES temporal_assertions(assertion_id),
    superseded_by_assertion_id text REFERENCES temporal_assertions(assertion_id),
    contradiction_group_id text,            -- group ID for contradictory assertions
    confidence          text DEFAULT 'medium',
    review_status       text DEFAULT 'pending_review',
    observed_at         timestamptz NOT NULL  -- when this assertion was observed/discovered
);

-- 5. RELATIONSHIPS
CREATE TABLE relationships (
    relationship_id     text PRIMARY KEY,
    subject_type        text NOT NULL,       -- event, entity, intel_item
    subject_id          text NOT NULL,
    relationship_type   text NOT NULL,       -- same_project, same_event, update_to,
                                            -- supersedes, located_in, developed_by, etc.
    object_type         text NOT NULL,
    object_id           text NOT NULL,
    confidence          text DEFAULT 'medium',
    evidence_item_ids   text[],
    extraction_method   text DEFAULT 'deterministic',  -- deterministic, llm, human
    review_status       text DEFAULT 'pending_review',
    UNIQUE (subject_type, subject_id, relationship_type, object_type, object_id)
);

-- 6. SEARCH RUNS
CREATE TABLE search_runs (
    run_id              text PRIMARY KEY,
    template_id         text,
    cadence             text NOT NULL,       -- hourly, daily, weekly, monthly, ad_hoc, event_triggered
    triggered_by_type   text,               -- entity, event, manual, schedule
    triggered_by_id     text,
    target_entity_ids   text[],
    query_executed      text NOT NULL,
    provider_used       text DEFAULT 'google',
    started_at          timestamptz NOT NULL,
    completed_at        timestamptz,
    result_count        integer DEFAULT 0,
    accepted_count      integer DEFAULT 0,
    error_count         integer DEFAULT 0,
    run_status          text DEFAULT 'planned'  -- planned, running, ok, partial, failed
);

-- 7. SEARCH CANDIDATES
CREATE TABLE search_candidates (
    candidate_id        text PRIMARY KEY,
    search_run_id       text REFERENCES search_runs(run_id),
    result_url          text NOT NULL,
    result_title        text,
    result_snippet      text,
    publisher           text,
    published_at        timestamptz,
    retrieved_at        timestamptz NOT NULL,
    matched_entity_ids  text[],
    matched_event_ids   text[],
    matched_topics      text[],
    relevance_score     numeric(4,3),
    duplicate_of_item_id text,              -- if exact duplicate of known item
    fetch_status        text DEFAULT 'pending',  -- pending, fetched, rejected, duplicate
    review_status       text DEFAULT 'pending'
);

-- 8. INTEL ITEMS (existing, extended)
-- Add columns: source_document_id, extraction_method
-- Keep existing columns

-- 9. SOURCE EVENTS (existing, extended)
-- Add columns: search_run_id, supersedes_event_id
-- Keep existing columns
```

### What Can Remain JSON Initially

- `entities.aliases` jsonb → normalize to entity_aliases table later
- `locations.geometry` jsonb → PostGIS later when needed
- `relationships.evidence_item_ids` text[] → separate table for full normalization
- `intel_item.citation` jsonb → keep as-is
- `intel_item.resident_relevance` jsonb → keep as-is

### What Must Be Relational Immediately

- `entities` — primary search target, needs indexed lookups
- `events` — timeline ordering, date filtering
- `temporal_assertions` — date math, supersession chains
- `locations` — geospatial queries (even with just community_id)

---

## Section 9 — LLM Boundaries

| Step | Classification | Example Items | Notes |
|------|---------------|---------------|-------|
| **Search query generation** | Deterministic + template | All entities | Template-based: `"{name}" {keywords}`. LLM only needed for novel query strategies. |
| **Search result dedup** | Deterministic | All | URL hash, content hash |
| **Search result relevance** | Mixed | Ambiguous results | Deterministic: domain filter, entity name match. LLM: relevance classification for results where entity name is absent but content is relevant. |
| **Entity extraction** | LLM-assisted | NBOR items + BCC + news | Current keyword parsing misses partials. LLM extraction from item text with structured entity output (name, type, aliases, confidence). Human verification on first pass. |
| **Entity resolution** | Mixed | SR 207 WRF across 2 sources | Deterministic: exact name/alias match. LLM: fuzzy name match ("SR 207 Water Reclamation Facility" == "SR 207 WRF"). |
| **Location extraction** | LLM-assisted | NBOR items with addresses | Regex catches "470 SR 207". LLM needed for "at 7250 and 7280 US 1 North" or intersection descriptions. |
| **Date normalization** | Deterministic + library | Chlorine burnout "June 1–21" | dateparser library handles most formats. LLM for "2026-2027 school year" → August 2026. |
| **Event type classification** | Deterministic + LLM | NBOR category=Meeting → public_hearing | Deterministic for obvious types (hearing, ROW permit). LLM for ambiguous items (is policy discussion an "agenda_item" or "policy_update"?). |
| **Temporal assertion supersession** | Deterministic | Date chain | Same entity + same assertion_type + different date → supersedes. Deterministic. |
| **Contradiction detection** | Human + LLM | Two different opening dates from different sources | LLM flags potential contradictions. Human resolves. |
| **Relationship linking** | Mixed | Phase III water (2 sources) | Deterministic: same event type + same date + similar title → candidate relationship. LLM: confirm or reject the relationship. |
| **Claim extraction** | LLM-assisted | Dollar amounts, decisions, restrictions | Extraction from item text. Human review for all claims before any publication. |
| **Digest generation** | LLM | Weekly email summary from approved items | Accept prompts, accept framing, require HITL before send. |
| **Social drafting** | LLM + Human | Urgent items → alert posts | Draft from facts, review before any output. |
| **Query interpretation** | LLM | "What's happening in SilverLeaf?" | Natural language → structured query (entities=[silverleaf], date_range=last_30d). Required for consumer-facing search. |

---

## Section 10 — UI Implications

### Resident Project Page

```
Project: SR 207 Water Reclamation Facility Phase 2
Status: ✅ Operational (since June 23, 2026)
Type: Infrastructure Project
Cost: $191.8 million
Location: CR 210 / SR 207 corridor

Timeline:
  Dec 19, 2025 — Approved (BOCC vote)
  Jun 23, 2026 — Operational ("now serving residents")
  [gap: construction start not in records]

Related Sources:
  SJC-UTIL-20260603-0003 — Approval announcement (verified)
  SJC-CN-20260626-0001 — Operational announcement (verified)

[🔔 Follow this project]  [📧 Get email updates]
```

Required schema: entities, events, temporal_assertions, intel_items.

### Community Digest

```
SilverLeaf — Weekly Update (July 6, 2026)
════════════════════════════════════════

🟢 COMPLETED (since last report)
  • None new this week

🟡 IN PROGRESS / EXPECTED
  • SilverLeaf K-8 School → expected Aug 2026 (est. by St. Johns Citizen)
  • Beach Valley Mini Golf → proposed (status needs verification)

🔵 UPCOMING (next 30 days)
  • No upcoming events found

ℹ️ No changes since last week.

[View all SilverLeaf items] [Manage subscriptions]
```

Required schema: entities (by community query), events (by date range),
temporal_assertions (by status = current).

### Search Page

```
🔍 Search SJC Intel

Filters:
  Entity: [_______________]  (autocomplete from entities table)
  Community: [▾ silverleaf | nocatee | st_augustine | ...]
  Topic: [▾ development | transportation | education | ...]
  Event Type: [▾ all | hearing | approval | opening | ...]
  Status: [▾ all | proposed | active | completed | delayed]
  Date Range: [from ___] [to ___]
  Expected Completion: [from ___] [to ___]
  □ Delayed only
  □ Opening soon (next 30 days)
  Source Type: [▾ all | official | media | cdd]
```

Required schema: entities (text search), locations (community filter),
events (type filter, date range), temporal_assertions (expected completion).

### Reviewer UI

```
📋 REVIEW QUEUE — with schema gaps

🔴 UNRESOLVED ENTITY (8 items)
  Click to create entity from item text [LLM-assisted entity extraction]

🔴 MISSING LOCATION (140+ items)
  Click to extract address from description [LLM-assisted]

🟡 CONFLICTING DATES (2 potential)
  SR 207 WRF: approval Dec 19 vs operational Jun 23 → check gap

🟡 SEARCH CANDIDATES (N items)
  Results from weekly search run. Accept or reject.

🟢 PUBLICATION READY (83 items verified)
  Select items for digest, newsletter, or social.
```

Required schema: all tables, plus candidate entity/location extraction.

---

## Section 11 — Summary

### Best-Fitting Schema Parts

1. **Entity** — maps directly to current tracked_entities and latent entities
2. **Event** (merged with milestone) — maps to NBOR categories, BCC action types
3. **Temporal assertion** — maps to the "changing dates" pattern seen in real data
4. **Relationship** — maps to known cross-source clusters (SR 207 WRF, Phase III water)
5. **Search run** — provides provenance for discovered items

### Concepts to Merge or Remove

| Action | Concept | Reason |
|--------|---------|--------|
| **Merge** | milestone → event | Same thing, different name |
| **Defer** | source_document | Redundant with existing source_event |
| **Defer** | full claim register | Too heavy for current volume |
| **JSON initially** | entity_alias | JSONB array is sufficient |
| **Remove** | separate milestone table | Absorbed into event |

### Strongest Actual Timeline Examples

1. **SR 207 WRF**: approved Dec 2025 → operational Jun 2026. 2 items, 2 events,
   6-month gap. Real timeline with a real gap.
2. **SilverLeaf K-8**: under construction → expected Aug 2026. Shows
   temporal assertion with approximate month precision.
3. **CR 2209 Connector**: opened Oct 2025. Single-event timeline, no date changes.

### Minimum Viable Schema Recommendation

**9 tables:** entities, locations, events, temporal_assertions, relationships,
search_runs, search_candidates, intel_items (existing, extended), source_events
(existing, extended). Event and milestone are merged.

### Search Orchestration Recommendation

Store cadence as text field (`hourly`, `daily`, `weekly`, `monthly`, `ad_hoc`,
`event_triggered`). Evaluate with `is_due()` function. No hard-coded intervals.
Search templates with `{entity.name}` placeholders for entity-specific queries.

### First Five Search Templates

1. **entity_name** — weekly, template-based, all entities
2. **delay_check** — daily, entities past expected completion
3. **project_milestone** — weekly/ad hoc, entities with approaching expected dates
4. **official_confirmation** — ad hoc, triggered by media items
5. **media_coverage** — ad hoc, triggered by official actions

### First Five Implementation Tasks

1. Create `entities` table with expanded entity types and aliases (JSONB)
2. Create `events` table (merged milestone), migrate from intel_item _beat/category
3. Create `temporal_assertions` table, populate from existing dates
4. Create `search_runs` and `search_candidates` tables (no search provider yet)
5. Backfill entities from existing 182 items (LLM-assisted entity extraction)

### Unresolved Product Decisions for Buddy

1. Should entities include people (officials, suspects) or stay project-focused?
2. Should CDD items be migrated to main schema or stay as a separate system?
3. What is the first search provider? (Google API, Bing, direct site scraping?)
4. Should temporal assertions from media sources ever be auto-approved?
5. Who reviews entity creations? (Buddy only, or trusted agent?)
6. Should the first search run be a one-time batch or a recurring weekly?
7. Conflicting dates: always flag for review, or auto-resolve by authority level?

### Exact Next Planning Prompt

To proceed with the first implementation phase:

```
Test the proposed MVP schema (9 tables: entities, locations, events,
temporal_assertions, relationships, search_runs, search_candidates) against
the full SJC dataset. Create the entities table from existing tracked_entities.
Backfill events from existing NBOR/BCC/CDD items. Build temporal assertion
chains for SR 207 WRF and SilverLeaf K-8. Do not create SQL migrations yet.
Do not implement search providers.
```

---

## Chat Summary

- **Schema fits?** YES, with three adjustments:
  1. Merge milestone into event
  2. Keep temporal_assertion separate (essential for date changes)
  3. Defer source_document and full claim register

- **Event, milestone, and temporal assertion all remain necessary?** NO.
  Event and milestone should merge. Temporal assertion stays separate.

- **Most important schema change:** Merging milestone into event. Every
  milestone IS an event. One table simplifies everything.

- **Most important search-discovery capability:** Template-based entity
  searching with `{entity.name}` placeholders, supporting any cadence
  without hard-coding intervals.

- **Minimum viable tables:** 9 — entities, locations, events (merged),
  temporal_assertions, relationships, search_runs, search_candidates,
  intel_items (extended), source_events (extended).

- **First implementation phase:** Create entities + events + temporal_assertions
  tables; backfill from existing 182 items; entity extraction (LLM-assisted).
  No search providers yet.

- **Files created:**
  `docs/reviews/SJC_SCHEMA_FIT_AND_SEARCH_DISCOVERY_DESIGN_20260706.md`

- **Commit created:** `docs: add SJC schema fit and search discovery design`

- **Repository status:** Clean. 1 new file committed. No data files, schemas,
  registries, or scripts modified.
