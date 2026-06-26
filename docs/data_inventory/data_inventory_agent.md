# Agent: data-inventory

**Purpose:** Catalog what data SJC_Intel has across time periods, what's
missing, what source families contributed, and what resident-interest themes
are covered.

**Reports to:** sjc-intel-architect  
**Triggers:** After any backfill or monitor run; monthly cadence

## Inputs

- `data/monthly/{YYYY-MM}/` — backfill artifacts
- `data/intel_items/` — live monitor items
- `data/index/prior_items.yaml` — dedupe index

## Outputs

- `docs/data_inventory/COVERAGE.md` — time period coverage map
- `docs/data_inventory/GAPS.md` — what's missing
- Updates to the coverage map in `docs/data_inventory/README.md`

## Responsibilities

1. After each backfill run, update the coverage map.
2. After each monthly cycle, produce a coverage summary.
3. Flag time periods with no data.
4. Flag source families with thin coverage.
5. Track item counts per period per source.
