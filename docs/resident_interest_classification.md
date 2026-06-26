# SJC_Intel — Resident Interest Classification

> Adding a resident-perspective layer to every intel item so we can answer
> "why does this matter to someone living in St. Johns County?"

## Purpose

Factual extraction tells us *what* happened. Resident interest
classification tells us *why people should care*. This layer:

- Bridges the gap between raw government/safety announcements and
  community awareness.
- Ensures consistent audience targeting across sources.
- Flags sensitive items for mandatory human review.
- Separates source facts from reasonable inference.

## Workflow Placement

```
source monitor → factual extraction → resident-interest classification
                                      → verification/sensitivity review
                                      → editorial review
```

The RI classifier runs after extraction but before verification review.
It adds fields to the existing intel item; it does not modify extracted
facts.

## Fields Added

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `primary_topic` | string | yes | Single most relevant topic from taxonomy |
| `interest_tags` | array<string> | no | Interest dimensions (see below) |
| `resident_relevance.summary` | string | yes | Why-this-matters in 1-2 sentences |
| `resident_relevance.affected_audiences` | array<string> | yes | Who specifically should care |
| `resident_relevance.why_it_matters` | string | yes | Concrete resident impact |
| `resident_relevance.confidence` | enum | yes | high / medium / low |
| `resident_relevance.inference_notes` | string | no | What was inferred vs. stated |
| `taxonomy_gap` | string | no | Proposed new tag (null if none) |
| `human_review_required` | boolean | yes | Whether item needs human review |

## Interest Tags Vocabulary

Interest tags capture *why* a resident would engage with an item.
They complement (not replace) topical tags.

| Tag | Meaning | Example |
|-----|---------|---------|
| `traffic_impact` | Affects roads, commute, or parking | Road closure, construction detour |
| `safety_concern` | Raises personal or community safety | Crime near schools, unsafe intersection |
| `cost_impact` | Affects personal finances | Tax change, utility rate, fee increase |
| `property_values` | May affect home values | New development, rezoning, school quality |
| `school_zones` | Affects school attendance, safety, or capacity | School boundary changes, new school |
| `quality_of_life` | Affects daily living experience | Park opening, noise complaint, event disruption |
| `development_watch` | New construction or land-use change | Commercial development, subdivision |
| `utility_impact` | Affects water, power, internet | Boil water notice, outage, new service |
| `emergency_awareness` | Alerts requiring awareness or action | Evacuation order, shelter opening |
| `community_event` | Gathering, program, or engagement opportunity | Library program, town hall, festival |

## Affected Audience Vocabulary

| Audience | Definition |
|----------|-----------|
| `residents` | General county residents (broadest) |
| `nearby_residents` | Residents in immediate vicinity of an event/location |
| `parents` | Parents of school-age children |
| `students` | K-12 and college students |
| `commuters` | People who drive for work/errands |
| `homeowners` | Property owners |
| `renters` | Rental tenants |
| `business_owners` | Local business operators |
| `retirees` | Retired or older residents |
| `visitors` | Tourists and non-resident visitors |
| `prospective_movers` | People considering moving to the area |
| `local_workers` | People employed in St. Johns County |

## Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| `high` | Resident impact directly stated in source | "Road closed until June 15" — commuters directly affected |
| `medium` | Impact reasonably inferred | New subdivision approved — construction traffic likely but not stated |
| `low` | Impact speculative or unclear | Award recognition — unclear day-to-day resident impact |

## Classification Rules (Summary)

| Rule | Applies When |
|------|-------------|
| `human_review_required: true` | Crime, arrest, suspect, victim, minors, emergencies, unresolved allegations |
| `recommended_channels: ["website_review_queue"]` | Public safety / crime items (unless broad public-interest) |
| `confidence: low` | Impact is unclear or speculative |
| Communities empty (countywide) | Affected community is unclear |
| `taxonomy_gap` for new tag proposals | A needed tag doesn't exist in canonical taxonomy |

## Worked Examples

### Example 1: County Roadwork Item
**Source type:** SJC County News / Infrastructure notice

```
Source says: "CR 210 will be closed between I-95 and US-1 for
utility work June 10-14. Detour routed via Roberts Road."

primary_topic: "infrastructure"
interest_tags: ["traffic_impact", "utility_impact"]
resident_relevance.summary: >
  A major commuter route through northern St. Johns County will
  be closed for five days, forcing detours during the work week.
resident_relevance.affected_audiences:
  - commuters
  - nearby_residents
  - local_workers
resident_relevance.why_it_matters: >
  Anyone driving CR 210 between I-95 and US-1 will need to plan
  alternate routes. The detour via Roberts Road may add 10-20
  minutes during peak hours.
resident_relevance.confidence: "high"
resident_relevance.inference_notes: >
  Directly stated closure dates and detour. Impact on commute
  times is a reasonable inference from known traffic patterns.
human_review_required: false
```

### Example 2: School Capacity / New School Item
**Source type:** SJC School District / BoardDocs

```
Source says: "School Board approves schematic design for
SilverLeaf K-8 school. Capacity: 1,200 students. Opening
projected Fall 2028."

primary_topic: "education"
interest_tags: ["school_zones", "property_values", "development_watch"]
resident_relevance.summary: >
  A new K-8 school planned for the SilverLeaf area signals
  continued growth in northwestern St. Johns County and may
  affect school attendance boundaries.
resident_relevance.affected_audiences:
  - parents
  - students
  - homeowners
  - prospective_movers
resident_relevance.why_it_matters: >
  New school capacity may shift attendance boundaries for
  existing SilverLeaf-area schools. The projected 2028 opening
  indicates the timeline for community growth. Property values
  in the area may be affected by school proximity.
resident_relevance.confidence: "medium"
resident_relevance.inference_notes: >
  School capacity and opening date are directly stated. Boundary
  impacts and property value effects are reasonable but unstated
  inferences based on typical growth patterns.
human_review_required: false
```

### Example 3: Development Tracker Commercial Parcel
**Source type:** SJC Development Tracker

```
Source says: "Parcel #123-45-678: 15-acre commercial zoning
application submitted at CR 210 and Twincreeks Court. Proposed
use: retail and restaurant."

primary_topic: "development"
interest_tags: ["development_watch", "traffic_impact", "quality_of_life"]
resident_relevance.summary: >
  A 15-acre commercial development proposed at a major northern
  St. Johns intersection could bring new retail and restaurants
  to the area.
resident_relevance.affected_audiences:
  - nearby_residents
  - commuters
  - business_owners
  - homeowners
resident_relevance.why_it_matters: >
  New retail and dining options nearby. However, increased
  traffic at CR 210 and Twincreeks Court may affect commute
  times and neighborhood traffic patterns. Property values
  could be influenced by commercial proximity.
resident_relevance.confidence: "medium"
resident_relevance.inference_notes: >
  Zoning application details are directly stated. Traffic impact
  and property value effects are reasonable inferences based on
  typical development outcomes. Actual tenant mix and timeline
  unknown.
human_review_required: false
```

### Example 4: Sheriff / Public Safety Item
**Source type:** SJSO News Stories

```
Source says: "SJSO arrested a 34-year-old St. Augustine man on
June 2 in connection with an armed robbery of a pharmacy on US-1.
No injuries reported. Investigation ongoing."

primary_topic: "crime"
interest_tags: ["safety_concern", "emergency_awareness"]
resident_relevance.summary: >
  An armed robbery occurred at a pharmacy on US-1. While no
  injuries were reported, the incident raises safety awareness
  for residents and businesses along the corridor.
resident_relevance.affected_audiences:
  - nearby_residents
  - business_owners
  - commuters
resident_relevance.why_it_matters: >
  Armed robbery on a major county corridor raises safety
  concerns for nearby businesses and residents. The suspect
  is in custody, but ongoing investigation means more
  information may follow.
resident_relevance.confidence: "high"
resident_relevance.inference_notes: >
  Incident details directly from SJSO press release. Safety
  concern inference is a standard community awareness response
  to known criminal activity in an area.
human_review_required: true
```

### Example 5: Library Summer Reading Item
**Source type:** SJC County News / Library notice

```
Source says: "SJCPLS Summer Reading Program runs May 31-July 25.
Free reading logs, prizes, 100+ events across six branches.
Theme: Stars, Stripes, and Stories."

primary_topic: "library"
interest_tags: ["community_event", "quality_of_life"]
resident_relevance.summary: >
  A free, county-wide summer reading program offering prizes
  and events at all six library branches — a low-cost way to
  keep kids engaged during summer break.
resident_relevance.affected_audiences:
  - parents
  - students
  - residents
resident_relevance.why_it_matters: >
  Free summer enrichment for families. Helps prevent summer
  reading loss. Accessible at any of six branch locations
  across the county.
resident_relevance.confidence: "high"
resident_relevance.inference_notes: >
  All details directly stated. Value to parents and students
  is obvious from the program description.
human_review_required: false
```

### Example 6: Water Shortage Item
**Source type:** SJC County News / Environmental notice

```
Source says: "Phase III Extreme Water Shortage declared. Mandatory
one-day-per-week irrigation. SJRWMD cites Extreme Drought (D3) —
worst since 2000."

primary_topic: "environment"
interest_tags: ["cost_impact", "utility_impact", "emergency_awareness"]
resident_relevance.summary: >
  The most severe water shortage declaration in Florida since
  2000 imposes mandatory one-day-per-week watering restrictions
  for all St. Johns County residents.
resident_relevance.affected_audiences:
  - residents
  - homeowners
  - business_owners
resident_relevance.why_it_matters: >
  All residents with irrigation systems must reduce watering to
  one day per week or face penalties. Landscaping-dependent
  properties (HOAs, commercial) need immediate schedule changes.
  Long-term drought may lead to higher water costs or further
  restrictions.
resident_relevance.confidence: "high"
resident_relevance.inference_notes: >
  Declaration details and restrictions directly stated. Cost
  impact inference is reasonable given typical utility rate
  structures during scarcity.
human_review_required: false
```
