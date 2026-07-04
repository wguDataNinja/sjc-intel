# SJC_Intel — Taxonomy

> Controlled vocabularies for intel item classification.
> All Hermes workers and human classifiers must use these values.

This document defines the allowed values for every classification field
in the `intel_item.schema.yaml` schema. Using a consistent vocabulary
enables filtering, deduplication, and downstream publishing automation.

---

## Topics

Topic tags categorize the subject matter of an intel item. At least one
topic is required. Choose the **most specific** applicable topic(s).
Multiple topics are allowed when an item spans categories.

| Topic | Description | Used When |
|-------|-------------|-----------|
| `county_government` | County administration, elected officials, budgets, policies | General government operations, non-specific notices |
| `public_safety` | Law enforcement, fire, EMS, emergency management | SJSO releases, fire rescue, disaster response |
| `crime` | Specific criminal incidents, arrests, investigations | Arrest reports, crime alerts, warrants |
| `education` | K-12 schools, school board, district programs | School district news, board meetings, student programs |
| `development` | Residential/commercial construction, zoning, planning | Development tracker updates, new projects, permits |
| `infrastructure` | Roads, utilities, public works, facilities | Road projects, water/sewer, building improvements |
| `environment` | Conservation, drought, hurricanes, ecosystems | Water shortages, beach projects, wildlife, climate |
| `transportation` | Roads, bridges, transit, traffic | Road closures, traffic alerts, transit projects |
| `community_events` | Public events, programs, meetings | Library programs, community celebrations, workshops |
| `public_notices` | Official announcements, legal notices | Auctions, public hearings, declaration notices |
| `emergency_alerts` | Active emergencies, hazards, urgent warnings | Boil water notices, evacuation orders, shelter openings |
| `economic_development` | Business growth, jobs, commerce | Small business initiatives, economic reports |
| `parks_recreation` | Parks, trails, recreation programs, beaches | Park closures, program registration, facility updates |
| `library` | Public library system, programs, services | Summer reading, branch events, library services |
| `coastal_projects` | Beach access, erosion control, coastal infrastructure | Beach ramp projects, dune restoration, seawalls |
| `organizational_excellence` | Awards, recognition, strategic plan | Communications awards, employee recognition |
| `community_trust` | Transparency, public engagement, resident outreach | Government transparency initiatives, surveys |
| `health_wellness` | Public health, mental health, wellness programs | Health department notices, wellness events |
| `water_restrictions` | Watering limits, drought declarations, reclaimed water changes, SJRWMD restrictions | Phase III Extreme Water Shortage, irrigation limits, drought orders |
| `budget_millage` | Budget workshops, millage, TRIM season, tax-bill implications | School funding surtax, millage elections, budget hearings |
| `housing` | Affordable housing, residential development | Housing policy, development proposals |
| `taxes` | Property tax, tax collection, deadlines | Tax notices, deadlines, payment information |
| `elections` | Voting, registration, candidates, ballots | Election notices, voter registration deadlines |
| `cdd_governance` | Community Development District board meetings, budgets, assessments, vacancies, elections, and district operations | CDD meeting agendas, workshop notices, board vacancies, assessment schedules, district governance actions |
| `general_government` | Catch-all for unclassified government notices | Use only when no other topic is clearly applicable |

### Classification Rule

If the topic is unclear from the source content, use `general_government`.

### Taxonomy Gaps From Deep Research

Do not expand the topic list until real extracted items prove the need, but
track these as likely proposals:

- `public_records` — Clerk records, official records, board records, deeds,
  liens, tax deeds, and VAB context.
- `permit_status` — permit search/status, certificate of occupancy, plan review,
  and vertical-construction movement.
- *(cdd_governance promoted to canonical topic 2026-06-26)*
- *(budget_millage promoted to canonical topic 2026-06-26)*

Use `taxonomy_gap` on intel items when these are materially clearer than the
existing topic and interest-tag values.

---

## Source Families

Source families are operational groupings for monitoring and verification.
They are not intel item field values unless a future schema adds them.

| Family | Primary Use | Authority Rule |
|--------|-------------|----------------|
| `county_decision_stack` | BCC, Clerk board records, GovTV, agendas, packets | First authority for county votes/hearings |
| `planning_development_stack` | PZA, Growth Management, Development Tracker, GIS Hub | First authority for rezonings and mapped projects |
| `permit_construction_stack` | Permit status, public permit search, CO/plan review | First authority for what is actually under review/built |
| `roads_transportation_stack` | County road closures, Traffic Ops, Public Works, FDOT, NFLRoads, FL511 | First authority for closures and project delivery |
| `utilities_water_stack` | County utility, boil notices, water conservation, SJRWMD | First authority for water/irrigation/reuse restrictions |
| `school_stack` | SJCSD, BoardDocs, zoning, new schools, planning | First authority for attendance zones and school delivery |
| `resident_cost_stack` | Property Appraiser, Tax Collector, budget, Clerk/VAB | First authority for taxes, exemptions, bill cycles |
| `cdd_governance_stack` | CDD sites, packets, Florida Public Notices | First authority for CDD assessments and district governance |
| `community_developer_stack` | Official community/developer/amenity sites | Useful for amenities, builders, phases, events; verify governance elsewhere |
| `local_media_context_stack` | St. Johns Citizen, JDR, TV, Recorder | Tip-surfacing/context; verify consequential claims |

---

## Homeowner Beat Groups

Beat groups support clustering and backfill planning. They map onto topics,
interest tags, and source families; they are not canonical item values yet.

| Beat Group | Canonical Topics Usually Used | Interest Tags Usually Used |
|------------|-------------------------------|----------------------------|
| `rezoning_comp_plan_dri` | `development`, `county_government`, `public_notices` | `property_values`, `development_watch`, `traffic_impact` |
| `permits_construction` | `development`, `infrastructure`, `economic_development` | `development_watch`, `property_values`, `quality_of_life` |
| `transportation` | `transportation`, `infrastructure`, `public_safety` | `traffic_impact`, `safety_concern`, `quality_of_life` |
| `school_capacity` | `education`, `development` | `school_zones`, `property_values`, `traffic_impact` |
| `utilities_water` | `infrastructure`, `environment`, `emergency_alerts`, `water_restrictions` | `utility_impact`, `cost_impact`, `emergency_awareness` |
| `cdd_governance` | `cdd_governance`, `taxes`, `parks_recreation`, `infrastructure` | `cost_impact`, `quality_of_life`, `property_values` |
| `taxes_exemptions_trim_vab` | `taxes`, `county_government` | `cost_impact`, `property_values` |
| `public_safety_livability` | `public_safety`, `crime`, `transportation` | `safety_concern`, `quality_of_life` |
| `retail_openings` | `economic_development`, `development` | `quality_of_life`, `property_values`, `traffic_impact` |
| `parks_amenities` | `parks_recreation`, `library`, `community_events` | `quality_of_life`, `community_event` |
| `local_government_budget_procurement` | `county_government`, `taxes`, `infrastructure` | `cost_impact`, `community_trust` |
| `elections_district_politics` | `elections`, `county_government` | `community_trust` |
| `emergency_weather_fire_flood` | `emergency_alerts`, `environment`, `public_safety` | `emergency_awareness`, `safety_concern` |
| `property_values_market` | `housing`, `taxes`, `economic_development` | `property_values`, `cost_impact` |

---

## Communities

The `communities` field identifies which specific geographic communities
are directly affected by an intel item. Values must match entries in
`registry/communities.yaml`.

### Common Values

| Community ID | Type | Scope |
|-------------|------|-------|
| `countywide` | countywide | Entire county (default when no specific community) |
| `nocatee` | master_planned_community | Northern St. Johns |
| `silverleaf` | master_planned_community | Northwest St. Johns |
| `rivertown` | master_planned_community | Northwest St. Johns |
| `shearwater` | master_planned_community | Northern St. Johns |
| `trailmark` | master_planned_community | Northwest St. Johns |
| `beacon_lake` | master_planned_community | Northwest St. Johns |
| `beachwalk` | master_planned_community | Coastal St. Johns |
| `etown` | master_planned_community | Northern St. Johns |
| `seven_pines` | master_planned_community | Northern St. Johns |
| `everrange` | master_planned_community | Northwest St. Johns |
| `wildlight` | master_planned_community | Northern St. Johns |
| `cr_210_corridor` | corridor | County Road 210 corridor |
| `sr_16_corridor` | corridor | State Road 16 corridor |
| `us_1_corridor` | corridor | US Highway 1 corridor |
| `ponte_vedra` | municipality | Coastal northeastern St. Johns |
| `st_augustine` | municipality | Central St. Johns / county seat |
| `st_augustine_beach` | municipality | Coastal Anastasia Island |
| `vilano_beach` | neighborhood | Coastal north of St. Augustine |
| `porpoise_point` | neighborhood | Within Vilano Beach |

See `registry/communities.yaml` for the complete list with descriptions
and parent areas. New communities must be registered there before use.

### Classification Rule

If the affected community is unclear or the item is county-wide,
use an empty array `[]`.

---

## Geographic Scope

Describes the geographic breadth of an intel item.

| Value | Description | Example |
|-------|-------------|---------|
| `county_wide` | Affects all of St. Johns County | County emergency declaration |
| `multi_community` | Affects multiple named communities | Development impacting several HOA areas |
| `single_community` | Affects one specific community | Park opening in Nocatee |
| `neighborhood` | Affects a specific subdivision or street | Road closure on a specific street |
| `address_specific` | Affects a single address or parcel | Property-specific permit or auction |

---

## Urgency

Time-sensitivity of an intel item for the community.

| Value | Definition | Examples | Action |
|-------|-----------|----------|--------|
| `urgent` | Immediate action or awareness needed | Safety alert, road closure, boil water notice, evacuation order | Flag for immediate human review |
| `timely` | Relevant in the near term | Meeting tonight, deadline this week, event this weekend | Include in next available briefing |
| `ongoing` | Evergreen or background information | Completed project, policy explanation, general awareness | Pool for weekly brief or newsletter |
| `archival` | Historical reference, not time-sensitive | Past event recap, historical information | Store for reference, no publication urgency |

---

## Sensitivity

Sensitivity level for editorial handling. Determines whether human
review is required before publication.

| Value | Definition | Requires Human Review? | Examples |
|-------|-----------|----------------------|----------|
| `low` | Routine information, safe to publish | No (can auto-advance) | Community events, library programs, general notices |
| `medium` | May involve named individuals, minor controversy, or partially verified claims | Yes | Arrest reports, budget controversies, named officials |
| `high` | Public safety, active incidents, legal matters, major controversy | Yes — mandatory before any publication | Active shooter, lawsuit filings, major scandal |

### Classification Rules

- Set to `low` unless the item involves safety, emergency, legal matters,
  crime, named individuals, or controversy.
- When in doubt, err toward `medium` — the review queue will handle it.
- `high` items should be rare and must always trigger immediate human
  notification.

---

## Verification Status

How thoroughly the item has been verified against its source(s).

| Value | Definition | When to Use |
|-------|-----------|-------------|
| `unverified` | Raw extract, not cross-checked | First-pass extraction before any validation |
| `source_confirmed` | Original source is real and accessible | Default for direct extractions from official sources |
| `cross_referenced` | Information matches at least one other independent source | After confirming with a second source |
| `fact_checked` | Specific claims have been independently verified | After detailed verification of factual claims |
| `disputed` | Contradictory information exists from reliable sources | When sources disagree on key facts |

### Classification Rule

For direct extractions from official government sources
(e.g., sjcfl.us, sjso.org, stjohns.k12.fl.us), set to
`source_confirmed` as the default.

---

## Review Status

Status of the editorial review process for an intel item.

| Value | Definition | Action |
|-------|-----------|--------|
| `pending_review` | Awaiting editorial review | Item is in the review queue |
| `in_review` | Being reviewed by an editor | Editor has claimed the item |
| `approved` | Ready for publication | Passed editorial review |
| `changes_requested` | Needs edits before approval | Editor has requested changes |
| `rejected` | Will not be published | Final decision, not for publication |
| `published` | Has been published to one or more channels | Item is live |

### Classification Rule

New items from the monitor pipeline should always be created with
`pending_review`.

---

## Recommended Channels

Suggested output channels for an intel item. Multiple channels can
be specified. This field guides the publishing workflow but does not
guarantee publication on any particular channel.

| Value | Definition | Example Use |
|-------|-----------|-------------|
| `newsletter` | Include in the next email newsletter | Community events, notable developments |
| `website` | Publish on the SJC_Intel website | All approved items that are public-ready |
| `website_review_queue` | Add to website review queue for editorial decision | Items that need a publication decision |
| `social_brief` | Include in social media summary post | Quick updates, alerts, event reminders |
| `weekly_brief_candidate` | Candidate for the weekly community briefing | Items worth summarizing in a weekly digest |
| `internal_only` | For internal reference, not for public publishing | Raw extracts, pending items, sensitive background |
| `alert` | Push notification or urgent broadcast | Emergency alerts, critical safety information |

### Classification Rules

- Most items should be tagged `website_review_queue` and
  `weekly_brief_candidate`.
- Use `alert` only for items with `urgency: urgent`.
- Use `internal_only` for unverified or sensitive background items.

---

## Interest Tags

Interest tags capture *why* a resident would engage with an item.
They complement (not replace) topical tags. Assigned by the
resident-interest classifier agent.

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

### Classification Rule

- Propose new tags via `taxonomy_gap`; do not silently add new tags.
- Only `sjc-intel-architect` or Buddy may approve taxonomy changes.

---

## Affected Audience Vocabulary

Identifies which specific resident groups are affected by an intel item.

| Audience | Definition | Typical Trigger |
|----------|-----------|----------------|
| `residents` | General county residents (broadest) | County-wide policy or event |
| `nearby_residents` | Residents in immediate vicinity | Construction, incident, closure |
| `parents` | Parents of school-age children | School news, youth programs |
| `students` | K-12 and college students | School events, programs |
| `commuters` | People who drive for work/errands | Road work, traffic alerts |
| `homeowners` | Property owners | Tax changes, development, HOA |
| `renters` | Rental tenants | Housing policy, rent changes |
| `business_owners` | Local business operators | Economic development, regulations |
| `retirees` | Retired or older residents | Senior programs, tax notices |
| `visitors` | Tourists and non-resident visitors | Beach access, events, tourism |
| `prospective_movers` | People considering moving to area | Development, schools, quality of life |
| `local_workers` | People employed in St. Johns County | Business news, commuting, economy |

### Classification Rule

Be specific — if only commuters on CR 210 are affected,
use `["commuters", "nearby_residents"]`, not just `["residents"]`.

---

## Quick Reference for Monitors

When creating a new intel item from an official government source,
use these defaults unless the content clearly requires otherwise:

| Field | Default Value |
|-------|--------------|
| `topics` | `["general_government"]` |
| `communities` | `[]` (countywide) |
| `geographic_scope` | `county_wide` |
| `urgency` | `ongoing` |
| `verification_status` | `source_confirmed` |
| `sensitivity` | `low` |
| `recommended_channels` | `["website_review_queue", "weekly_brief_candidate"]` |
| `review_status` | `pending_review` |
