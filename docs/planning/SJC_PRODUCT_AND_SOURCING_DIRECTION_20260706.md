# SJC Intel — Product and Sourcing Direction

**Date:** 2026-07-06
**Status:** Planning artifact. No implementation authorized by this document.
**Source:** Buddy brainstorming session with GPT.

---

## Authority Summary

This section records the accepted planning decisions from the session. They are
not implementation orders — they establish direction for downstream planning,
sourcing, and roadmap documents.

### Product Scope

**First public product:** SilverLeaf neighborhood intelligence. The initial
public-facing scope is SilverLeaf (master-planned community in northwestern
St. Johns County). Items from outside SilverLeaf appear only when they
materially affect SilverLeaf residents.

**Internal collection scope:** Remains broader than the public product.
County government, district schools, FDOT, utilities, emergency sources,
countywide news, nearby communities, and regional transportation continue
to be collected.

### Architecture — Three Lanes

1. **Durable knowledge lane** — projects, schools, businesses, roads,
   government decisions, utilities, expected dates, construction, openings,
   long-term change. This is the current SJC Intel pipeline.

2. **Live incident lane** — crashes, disabled vehicles, closures, fires,
   flooding, emergency activity, roadblocks, temporary disruptions.
   New lane; not yet implemented.

3. **Agentic investigation lane** — news searches, social searches,
   official-source checks, evidence extraction, reconciliation,
   resident-impact summaries, proposed updates. New lane; not yet implemented.

### Source Policy

- Deterministic official capture first, agentic search second.
- Social media as lead or corroboration, never as sole primary detection.
- Cameras as observational evidence, not official incident classification.
- Failed search is not proof of absence.
- Temporary incident records must be captured before they disappear.

### Geographic Registry

A versioned SilverLeaf geographic registry is now a foundational dependency.
It must include: boundary, neighborhoods, internal streets, entrances,
intersections, schools, direct access roads, relevant I-95/I-295 segments,
major businesses and facilities, active projects, aliases, and exclusion rules.

Coordinate-based filtering (point-in-polygon, corridor proximity) is the
target mechanism. PostGIS is the preferred database support.

### Sourcing

- **Traffic incidents:** FHP live incident page (structured endpoint
  investigation needed), FL511, county notices.
- **Congestion data:** Open research question. TomTom is the strongest
  low-cost pilot candidate. Google and Apple APIs remain alternatives.
  Any pilot must have strict quotas, billing alerts, and route limits.
- **Schools:** Expand beyond board meetings to athletics, activities,
  recognition, and community achievements.
- **FDOT contracts:** Durable project and infrastructure lane (not live).
- **Community news:** Broad countywide news exists (News4Jax model).
  Public filter applies SilverLeaf relevance test.
- **Emergency/fire:** Jacksonville and Duval sources exist but are out of
  scope for initial SilverLeaf product. Retain as future expansion note.

### Deferred

- Public traffic-map UI
- FL511 camera embedding and custom streaming
- TomTom/Google traffic API implementation
- Public incident pages
- Nocatee or countywide public coverage
- Direct X/Twitter dependence
- Camera integration

### Boundary Decisions

| Area | Public Scope | Internal Collection | Rationale |
|------|-------------|-------------------|-----------|
| SilverLeaf | Primary focus | Full | Active development, large community, distinctive neighborhood focus |
| Nocatee | Exclude initial scope | Retain backend | Mature separate community; crossover stories only |
| Beachwalk | CR 210 impact only | Monitor | Nearby corridor relevance |
| Shearwater | Adjacent impact | Monitor | Closest adjacent community |
| TrailMark | Conditional (shared SR 16) | Monitor | Shared infrastructure relevance |
| RiverTown | Exclude initial scope | Monitor | Distant, separate community |
| Durbin/Bartram | Regional destinations only | Monitor | Transportation impact areas |
| Jacksonville/Duval | Exclude initial scope | Research only | Future expansion consideration |

---

## Full Session Record

### 1. Starting Question: More Current, Live Local Information

The session began with the question of whether SJC Intel should go beyond
periodic news and public-record monitoring to capture much more current
information, including:

- traffic incidents;
- road closures;
- crashes;
- flooding;
- signal outages;
- emergency detours;
- utility work;
- social-media reports.

The initial conclusion was that this required a distinct real-time incident
lane, separate from the slower knowledge and project-monitoring lane.

The first source classes discussed were:

- FL511;
- Florida Highway Patrol live incidents;
- St. Johns County notices;
- emergency management sources;
- sheriff and fire-rescue sources;
- local news;
- X/Twitter;
- community traffic reports.

The main architectural principle established:

```
official live source
→ deterministic capture
→ normalized incident
→ optional agentic enrichment
```

### 2. Traffic ETA and Congestion Monitoring

The conversation then moved from explicit incidents to live traffic
intelligence (Apple Maps ETA predictions). Potential providers discussed:

- Google Maps Routes API;
- Apple Maps Server API and MapKit;
- TomTom traffic and routing APIs.

Useful outputs identified:

- current traffic-aware duration;
- non-traffic/free-flow duration;
- segment-level speed;
- current travel time;
- free-flow travel time;
- route geometry;
- incident information;
- traffic-state classification.

Important analytical distinction:

```
ordinary rush-hour congestion
≠
unusual congestion for this weekday and time
```

Proposed model: build historical baselines by route/road segment, direction,
day of week, and time bucket.

### 3. Cost Sensitivity

Traffic APIs are only interesting if actual cost stays minimal. Working
conclusion: a small pilot could remain in free tier or near zero cost if it:

- monitored only a limited set of routes (5–10);
- checked mainly during commute windows;
- reduced polling frequency outside those periods;
- temporarily increased frequency only after an anomaly;
- used strict quotas and billing alerts.

TomTom appeared to be the strongest low-cost pilot candidate, though exact
licensing, overage, retention, and display rules still require verification.
No traffic provider was selected for implementation during this session.

### 4. Regional Traffic-Map Concept (Tabled)

The discussion expanded into a possible map covering northern St. Augustine
through downtown Jacksonville. The proposed map would show not just
conventional red/yellow/green congestion but also unusual congestion compared
with baselines, crashes, closures, flooding, construction, disabled vehicles,
and nearby cameras.

The combined source strategy:

```
traffic-flow provider → current speeds and travel times
FL511 / FHP → official incidents and closures
historical observations → anomaly scoring
news and social agents → explanation and context
```

The map idea was considered useful, but the user explicitly tabled the UI
because architecture and sourcing were more urgent.

### 5. Agentic Sourcing Architecture

The agreed architecture:

**Deterministic source layer:**
- FHP incidents
- FL511 incidents
- county notices
- school records
- public meetings
- project records
- official feeds

**Agentic investigation layer:**
- targeted news searches
- official social-account searches
- X/Twitter searches
- source reconciliation
- cause investigation
- status updates
- broader context
- resident impact

Controlled flow:

```
detected fact or knowledge gap
→ investigation
→ targeted searches
→ source retrieval
→ evidence extraction
→ reconciliation
→ proposed knowledge update
→ review
```

Agents may:
- inspect the database;
- identify what is already known;
- identify gaps;
- formulate searches;
- search official sources, news, and social media;
- compare results with existing entities and events;
- propose updates.

Agents should not:
- silently create accepted entities;
- overwrite dates;
- resolve contradictions without evidence;
- treat a social post as definitive;
- publish automatically;
- interpret "nothing found" as proof of absence.

### 6. FHP Live Traffic Incident Source

The Florida Highway Patrol live incident page:

```
https://trafficincidents.flhsmv.gov/SmartWebClient/CadView.aspx
```

A current example:

- disabled vehicle in roadway;
- Duval County;
- I-295 northbound entrance ramp;
- mile marker 3;
- entrance ramp blockage.

Likely fields: incident type, county, roadway, direction, location,
mile marker, road condition, timestamps, latitude, longitude.

Key architectural conclusion:

```
FHP live source
→ deterministic incident adapter
→ normalized incident record
→ geographic relevance filter
→ optional investigation
```

It should not depend on GPT or general web search to rediscover the incident
later. Source-feasibility investigation remains open.

### 7. OpenStreetMap Distinction

FHP links incidents to OpenStreetMap. The distinction:

- **FHP:** incident facts and coordinates.
- **OpenStreetMap:** geographic context and road geometry (road geometry,
  intersection resolution, point-in-polygon checks, route/corridor mapping,
  map display).

OSM's public tile infrastructure should not be treated as unlimited production
infrastructure. Attribution and licensing must be respected. Because the UI
was tabled, this remains a future concern.

### 8. GPT Traffic-Search Experiments

The user supplied GPT search logs for two live incidents. GPT attempted to
find news reports, X/Twitter posts, FL511 alerts, and FHP records but found
no exact matching news or social coverage.

Lessons:

- routine incidents often receive no news coverage;
- temporary incident records disappear;
- X posts are inconsistently indexed;
- public X pages do not expose reliable chronological feeds;
- date and approximate time are essential;
- nearby similar reports are not proof of a match;
- lack of search results does not disprove the incident.

This reinforced the need to capture transient official records before they
disappear. The correct interpretation of a failed search:

```
search_outcome: no_exact_match_found
not:
incident_did_not_happen: true
```

### 9. X/Twitter Limitations

The FL511 Northeast X account was examined. The public logged-out page
showed the account existed with a very large post count but non-chronological
content. GPT could find the profile and read public posts but could not
reliably retrieve the newest posts, search the complete archive, or prove
a post never existed.

Source policy:

```
X/Twitter
= optional fast context or corroboration
≠ authoritative archive
≠ complete incident feed
```

Possible future access paths: approved API, authenticated browser automation,
official or partner feed, general web search as weak fallback. The system
should remain functional without X.

### 10. Emergency and Fire Sources

Potential Jacksonville and Duval sources considered:

- Jacksonville Fire and Rescue Department incident dashboard;
- JFRD social accounts;
- JaxReady;
- AlertJax;
- Jacksonville Sheriff's Office;
- City of Jacksonville news releases;
- formal public-record requests.

Source hierarchy for a reported fire:

1. live emergency incident dashboard;
2. fire department social accounts;
3. emergency-alert systems;
4. sheriff;
5. local news;
6. formal incident reports.

Key lesson: routine incidents may appear only in operational systems; lack
of a post does not mean an event did not occur.

### 11. FDOT Construction Records

The FDOT State Construction Office contract page is useful for long-term
projects: contract numbers, financial project numbers, contractors, project
descriptions, construction categories, county filtering, and project history.
Not suitable as a live construction or traffic feed (list results may include
"final payment made" statuses). Belongs in the durable project/infrastructure
lane.

### 12. FL511 Cameras

FL511 camera directory for St. Johns County shows multiple I-95 cameras
with mile-marker locations. Cameras are useful for observing congestion,
blocked lanes, emergency vehicles, smoke, weather, flooding, construction,
and apparent clearance. Camera imagery cannot establish official incident
type, whether a crash was hit-and-run, cause, injuries, arrests, or precise
timestamps.

Evidence model:

```yaml
observation_type: traffic_camera
observed_at: ...
visible_conditions:
  congestion: heavy
  emergency_vehicles: possible
  blocked_lanes: 1
confidence: medium
limitations:
  - partial field of view
  - no official incident classification
```

### 13. FL511 Camera-Stream Inspection (Research Only)

Browser-network findings after opening FL511 video revealed HLS streaming
with tokenized access. Observed: .m3u8 playlists, tokenized access, external
DIVAS infrastructure. Token lifetime, cookie requirements, IP binding, and
rate limits were not established.

Rejected as implementation assumptions: copying permanent HLS URLs,
reproducing undocumented token exchange, proxying streams, restreaming video,
recording feeds, or building an unsupported standalone player.

An official FL511 embedded-map tool appears to be the preferred future
integration route. Camera integration remains research-only.

### 14. Future Incident-Page Concept (Tabled)

A future incident page would include: incident type, road and direction,
mile marker, nearby interchange, lane/ramp impact, first observed, last
confirmed, active/clearing/reopened/stale status, official source, nearby
camera links, related articles, official posts, social reports (marked
unverified), affected routes/communities, and an incident timeline.

Remains a future product idea, not an immediate implementation task.

### 15. Expanding Beyond Government and Development News

The user proposed broader article sourcing:

- school and community coverage;
- high school athletics (state qualification; championships);
- school awards, activities, academic recognition, performances;
- student achievements.

This broadens the product from a development monitor into a resident-oriented
local intelligence service.

Potential resident beats:

- schools and youth;
- roads and transportation;
- utilities and emergencies;
- development and construction;
- businesses;
- local government;
- CDDs;
- public safety;
- parks and recreation;
- community achievements;
- events.

For schools, the search portfolio should cover:

**Operations:** construction, openings, enrollment, attendance zones,
principals, closures.

**Athletics and activities:** basketball, football, championships, state
qualification, band, robotics, competitions.

**Recognition:** awards, scholarships, graduation, teacher recognition,
student accomplishments.

The system should avoid becoming a generic sports-results archive. Items
should be ranked for resident relevance, significance, uniqueness, and
geographic connection.

### 16. News4Jax Countywide Example

The News4Jax St. Johns County topic page showed: commercial developments,
road closures, crime, public safety, schools, construction fraud, utilities,
transportation, restaurant openings/closures, and county projects. Broad
countywide news already exists.

### 17. Public Scope Decision

**SilverLeaf-first public product.** Reasoning:

- SilverLeaf is large enough to generate substantial ongoing news;
- remains under active development;
- has internal neighborhoods, schools, parks, roads, retail, utilities,
  and projects;
- countywide sources already cover broad St. Johns County news;
- a neighborhood-focused service is more distinctive;
- neighborhood relevance can answer practical resident questions that
  countywide pages do not.

### 18. Public Versus Internal Scope

**Internal collection scope:** remains broader: county government, district
schools, FDOT, utilities, emergency sources, countywide news, nearby
communities, regional transportation.

**Public editorial scope:** SilverLeaf-centered.

Public inclusion test:

```
Why would a SilverLeaf resident care about this?
```

Acceptable reasons: inside SilverLeaf; affects a school serving SilverLeaf;
affects a major access or commute route; changes nearby shopping, healthcare,
parks, or services; affects taxes, utilities, zoning, or emergency conditions;
notable local achievement involving residents.

"Somewhere in St. Johns County" is not sufficient.

### 19–21. SilverLeaf Geographic Registry

A versioned SilverLeaf registry is now foundational. First useful version
must include:

1. SilverLeaf master boundary;
2. verified neighborhoods (canonical names, aliases, builder, status,
   geometry, entrances, HOA/CDD relationship, construction phase);
3. internal streets (every street, aliases, geometry, intersections,
   start/end, neighborhoods served, entrances, planned streets);
4. entrances and intersections;
5. schools (physical, serving, future sites, attendance zones, feeder
   patterns, athletic names, official accounts);
6. direct access roads (SilverLeaf Parkway, St. Johns Parkway/CR 2209,
   SR 16 West, CR 210, CR 16A, International Golf Parkway);
7. regional commute segments (specific I-95 and I-295 segments with
   start/end anchors, exits, mile markers);
8. major businesses and facilities;
9. active development and infrastructure projects;
10. aliases and exclusion rules.

Evidence for every registry assertion: source, source type, retrieval date,
effective date, expiration/review date, confidence, verification status,
reviewer, supersession history.

### 22. GPS Coordinates and Boundaries

Coordinate-based filtering strategy:

```
source coordinates
→ point-in-polygon test
→ corridor and distance checks
→ relevance classification
```

When coordinates exist: inside polygon → direct inclusion; near an entrance
→ likely direct impact; on monitored route → traffic relevance; outside all
zones → exclude or review.

When only an address exists: geocode once, retain normalized address and
coordinates, store provider and confidence, avoid repeated paid geocoding.

When only road text exists: resolve intersections, use mile-marker registry,
use street-segment geometry, match landmarks, send unresolved cases to review.

Preferred boundary sources (ranked):

1. county GIS or official parcel data;
2. official planning exhibits;
3. subdivision plats;
4. OpenStreetMap;
5. manually curated polygons;
6. rough radii (temporary fallback only).

PostGIS is the cleanest database support for point-in-polygon, distance
checks, corridor intersection, nearest entrance, nearby-camera selection,
and neighborhood matching.

---

## Accepted Decisions

| # | Decision | Detail |
|---|----------|--------|
| 1 | SilverLeaf-first public product | First public-facing scope is SilverLeaf neighborhood intelligence |
| 2 | Broader internal collection | Internal scope remains countywide + regional |
| 3 | Three-lane architecture | Durable knowledge, live incident, agentic investigation |
| 4 | Deterministic official capture first | Official sources are primary detection mechanism |
| 5 | Agentic search second | Agents search, enrich, reconcile, and explain |
| 6 | Social media as corroboration only | Not sole primary detection source |
| 7 | Geographic registry is foundational | SilverLeaf registry with boundary, streets, schools, roads, aliases |
| 8 | Coordinate-based filtering | Point-in-polygon, corridor proximity, PostGIS |
| 9 | Live incident lane | Crashes, closures, flooding, utility work, emergency activity |
| 10 | School expansion | Athletics, activities, recognition, community achievements |
| 11 | Public traffic map deferred | UI tabled; architecture and sourcing are more urgent |
| 12 | No direct X/Twitter dependence | System must function without X |
| 13 | Camera integration research-only | No streaming, recording, or undocumented token exchange |

---

## Open Questions

1. How does the FHP incident page retrieve its live data?
2. Is there a clean structured endpoint or is browser automation required?
3. What are FL511's permitted incident and camera integration methods?
4. Which official source provides the best SilverLeaf development boundary?
5. Which SilverLeaf neighborhood names are authoritative?
6. What are all internal SilverLeaf streets and entrances?
7. Which schools serve SilverLeaf by school year?
8. Which exact I-95 and I-295 segments should be monitored?
9. Which source records include reliable coordinates?
10. Should PostGIS be included in the first PostgreSQL implementation?
11. What geographic confidence thresholds should allow deterministic publication?
12. What should require human review?
13. What article-search programs should run for schools, businesses, roads,
    utilities, and community achievements?
14. What source-retention rules are needed for transient incidents?
15. What should count as an exact, probable, related, or unverified match?

---

## Roadmap Implications

- The SilverLeaf geographic registry now sits near the front of the
  implementation sequence.
- The live incident lane requires new source adapters (FHP, FL511) and
  a new normalized incident schema.
- The agentic investigation lane requires search infrastructure, LLM
  integration, and review gates.
- The durable knowledge lane continues but public output is now
  SilverLeaf-filtered.
- VPS deployment sequencing (from `VPS_ROADMAP.md`) must accommodate
  the SilverLeaf registry and geographic filtering before live incident
  sources can be routed correctly.
- School sourcing expands significantly beyond BoardDocs.
- Nocatee, countywide, and regional public coverage are deferred but
  internal collection continues.
