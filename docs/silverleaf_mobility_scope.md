# SilverLeaf Mobility Scope

**Status:** Active evidence-and-selection contract; not a live traffic service.
**Primary registry:** `registry/silverleaf_mobility.yaml`.
**Last reviewed:** 2026-08-08.

## Purpose

This registry limits road and transportation monitoring to links that have a
defensible SilverLeaf resident relationship. It prevents a broad mention of
"I-95," "SR 16," or "CR 210" from becoming a SilverLeaf alert without a
concrete connection.

It does not provide travel times, crash data, camera feeds, navigation,
private-road status, road access rights, or a GIS road network.

## Scope hierarchy

| Relationship | Segment | What can qualify | What cannot qualify automatically |
|---|---|---|---|
| Direct access | CR 2209 / St. Johns Parkway between Silverleaf Parkway and IGP | A closure, detour, signal, construction, or access-management notice tied to this segment/endpoints. | Every CR 2209 notice. |
| Direct connection interface | SR 16 / IGP / CR 2209 interface | Official notices for the named intersection or SR 16 improvement limits between IGP and CR 2209. | Generic SR 16 notices. |
| Nearby commute corridor | SR 16 from IGP to I-95 | Project milestones, hearings, or material closures expressly within the documented 5.9-mile study limits. | All SR 16 or I-95 incidents. |
| Context only | CR 210 I-95-to-US 1 and the I-95/SR 16 interface | Background, or a record with a specific documented connection to SilverLeaf access. | Generic CR 210 congestion, Beachwalk-only work, or generic I-95 incidents. |

The hierarchy is intentionally conservative: a route used by some residents is
not enough to make every incident on that route a SilverLeaf product item.

## Official sources and established facts

- [St. Johns County’s CR 2209 opening record](https://www.sjcfl.us/sjc-opens-county-road-2209-segment-silverleaf-international-golf-parkway/)
  identifies the opened four-lane section between Silverleaf Parkway and
  International Golf Parkway.
- [The County’s CR 2209 project record](https://www.sjcfl.us/county-road-2209-roadway-expansion-underway/)
  distinguishes that connection from the larger 7.7-mile CR 2209 Central
  Project extending from CR 210 to SR 16.
- [The County’s SR 16/IGP project record](https://www.sjcfl.us/sjc-groundbreaking-sr-16-international-golf-parkway-project/)
  supports the SR 16–IGP–CR 2209 interface improvements.
- [FDOT’s SR 16 PD&E project page](https://nflroads.com/ProjectDetails?p=5615)
  defines the 5.9-mile IGP-to-I-95 study limits. Its schedule remains TBD, so
  no completion-date claim should be made.
- [The County’s completed CR 210 project record](https://www.sjcfl.us/cr-210-roadway-improvements-completed-2026/)
  supports background context but does not establish every CR 210 notice as
  SilverLeaf-relevant.

## Notice-selection procedure

1. Match the official notice to a registered segment, endpoint, linked entity,
   or explicit SilverLeaf impact.
2. Apply the segment’s relationship label: `direct_access`,
   `direct_connection_interface`, `nearby_commute_corridor`, or
   `contextual_only`.
3. Retain the source URL and exact limit/closure language. A route name by
   itself is insufficient.
4. If the notice is a crash, camera, congestion, or emergency incident, stop:
   live-incident sources and the incident schema are separate future work.
5. For an unregistered internal street or entrance, require direct source
   evidence of the SilverLeaf relationship; do not infer it from a map.

## Explicit unknowns

- No reviewed official internal-street/entrance inventory or public/private
  road-status dataset is stored yet (`DIR-009` remains in progress).
- No official FCE alignment/access segment is registered for live incident
  selection.
- No live incident provider, crash schema, congestion API, or camera product
  is activated (`DIR-003` through `DIR-005`).

## Validation

```bash
python3 scripts/validate_silverleaf_mobility.py
python3 -m pytest tests/test_silverleaf_mobility.py -v
```
