# Deep Research Beat Extraction Review

Date: 2026-06-03  
Report: `docs/deep_research/reports/2026-06-03_homeowner_public_source_monitoring_map.md`

## Summary

- Beats extracted: 14
- Registry updated: `registry/beat_candidates.yaml`
- Canonical beat promotions made: 0
- Recommended top-five beats marked in registry: 5

## Beats Extracted

1. Rezoning, comp-plan, and DRI changes
2. Site plans, permits, and vertical construction
3. Roadwork and traffic impacts
4. School capacity, rezoning, and new-school delivery
5. Utilities, irrigation, reclaimed water, and boil notices
6. CDD governance, assessments, and amenity operations
7. Property taxes, exemptions, TRIM, and VAB
8. Public safety and neighborhood livability
9. Retail, grocery, restaurant, and service openings
10. Parks, libraries, trails, and amenity expansion
11. Local government, budgets, and procurement
12. Elections and district politics
13. Emergency, weather, fire, flood, and beach conditions
14. Property values and market liquidity

## Overlap With Existing Taxonomy

Most beats map cleanly to existing `docs/taxonomy.md` topics and interest tags:

- `development`, `transportation`, `education`, `infrastructure`, `environment`, `taxes`, `public_safety`, `community_events`, `parks_recreation`, `economic_development`, `elections`
- `traffic_impact`, `school_zones`, `utility_impact`, `cost_impact`, `property_values`, `development_watch`, `quality_of_life`, `safety_concern`, `emergency_awareness`

## New Taxonomy Needs

No immediate schema change is required, but the following should remain
`taxonomy_gap` candidates until proven by real items:

- `cdd_governance` as a topic or beat group
- `public_records` as a topic for Clerk/records items
- `permit_status` as a more specific development tag
- `water_restrictions` as an interest tag or utility subtag
- `budget_millage` as a taxes/government subtag

## Recommended Top 5 Beats

1. Rezoning, comp-plan, and DRI changes
2. Roadwork and traffic impacts
3. School capacity, rezoning, and new-school delivery
4. Utilities, irrigation, reclaimed water, and boil notices
5. Site plans, permits, and vertical construction

These five should drive the May 2026 backfill plan and the first operator-mode
source promotion reviews.

## Canonical Topic/Interest Group Recommendations

Recommended for eventual canonical beat or interest-group treatment:

- CDD governance, assessments, and amenity operations
- Property taxes, exemptions, TRIM, and VAB
- Local government, budgets, and procurement
- Emergency, weather, fire, flood, and beach conditions

Do not add a separate canonical beat registry until the May 2026 backfill
produces enough items to prove the shape of the data.
