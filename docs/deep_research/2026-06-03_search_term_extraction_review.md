# Deep Research Search Term Extraction Review

Date: 2026-06-03  
Report: `docs/deep_research/reports/2026-06-03_homeowner_public_source_monitoring_map.md`

## Summary

- Search terms added: 52
- Registry updated: `registry/search_terms.yaml`
- Canonical source changes made: 0
- Terms are operational and untested.

## Categories Added Or Updated

- `community`
- `corridor`
- `school`
- `homeowner_beat`
- `source_discovery`
- `historical_backfill`
- `topic`
- `local_media_discovery`
- `cdd_governance`
- `utilities_water`
- `transportation`
- `permits_development`
- `taxes_property`

Some entries use more specific categories such as `utilities_water` or
`permits_development` instead of the broader `homeowner_beat` category because
they are directly tied to the report's first monitoring priorities.

## Most Useful For May 2026 Backfill

Start with these terms:

- `ST-0001` SilverLeaf rezoning/permit/reclaimed water/school/road closure
- `ST-0101` CR 210 lane closure/widening/interchange/signal/school
- `ST-0102` SR 16 widening/I-95/closure/public meeting
- `ST-0201` SJCSD attendance zoning/capacity/new school
- `ST-0301` site:sjcfl.us development/PZA/rezoning/major modification
- `ST-0303` site:nflroads.com St. Johns County roads
- `ST-0304` site:sjrwmd.com St. Johns County permits/water
- `ST-0601` SJC utility boil water/outage/reclaimed/irrigation/billing
- `ST-0602` SJRWMD water shortage/restrictions/drought/declaration
- `ST-0604` watering restrictions St. Johns/Ponte Vedra/St. Augustine

## Useful For Local-Media Discovery

- `ST-0701` `"St. Johns County" local news`
- `ST-0702` `"St. Johns County" community news`
- `ST-0703` `"St. Johns County" newsletter`
- `ST-0704` `"Nocatee" news`
- `ST-0705` `"Ponte Vedra" local news`

These should discover public local outlets, newsletters, and community pages.
Do not search or scrape private/login-gated groups.

## Useful For CDD/Governance Discovery

- `ST-0003` Nocatee CDD/Tolomato
- `ST-0006` RiverTown CDD/assessment/public notice
- `ST-0008` Shearwater/Trout Creek CDD
- `ST-0009` TrailMark/Six Mile Creek CDD
- `ST-0012` Beachwalk/Twin Creeks North CDD
- `ST-0014` Beacon Lake/Meadow View at Twin Creeks CDD
- `ST-0305` public notice across SJC communities
- `ST-0403` named CDD bundle
- `ST-0404` assessment roll/annual assessment/budget hearing

## Notes

- All terms should log effectiveness after first use.
- Backfill runs should record which terms returned no useful results.
- Search-term additions do not require Buddy approval, but source promotions
  discovered from those terms do.
