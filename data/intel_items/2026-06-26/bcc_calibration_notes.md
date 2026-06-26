# BCC Agenda Extraction Calibration Notes — 2026-06-26

## Meetings Processed

| Meeting | PDF Source | Items Parsed | High | Medium | Low/Routine |
|---------|-----------|-------------|------|--------|-------------|
| Jan 20, 2026 | Fixture | 44 | 35 | 4 | 5 |
| May 19, 2026 | Live fetch | 31 | 24 | 8 | 0 |
| **Combined** | | **75** | **59 (78.7%)** | **12** | **5** |

## pypdf Extraction Quality

| Measure | Jan 20 | May 19 |
|---------|--------|--------|
| Pages | 8 | 6 |
| Chars extracted | 24,198 | 17,320 |
| Item boundaries | Clean | Clean (after section fix) |
| Table structure | N/A | N/A |
| Verdict | Excellent | Excellent |

**Decision: Stay with `pypdf`.** No quality issues found. Table-heavy PDFs were not encountered. If future agendas contain complex tables, `pdfplumber` can be evaluated at that point.

## Classification Calibration

### Corrections Applied

| Issue | Before | After | Evidence |
|-------|--------|-------|----------|
| Item numbers >100 treated as agenda items | Parsed "403." as an item (statutory ref) | Skipped numbers >100 | May 19 agenda had "403." from Florida Statute reference |
| Re-numbering across sections caused duplicate item numbers | Regular Agenda items 1-8, then Consent items 1-N overwrote | Section prefix added (`public_hearing.1`, `consent.1`) | Both agendas have multi-section numbering |
| "Public Hearing" items were sometimes classified as low_signal | Low keyword check ran before high keyword check | Fixed: high_signal keywords now checked first | Items #3-5 on May 19 were rezonings classified as low |

### Remaining Calibration Notes

| Item Type | Current Behavior | Recommended |
|-----------|-----------------|-------------|
| Utility easement acceptances (consent) | Classified as `utilities_water` high_signal | Correct — these are property-rights transactions |
| Contract awards (consent) | `local_government_budget_procurement` high_signal | Correct — procurement is resident-relevant |
| Proclamations (4 per May 19 meeting) | `low_signal` `parks_amenities` | Correct — ceremonial only |
| Budget/funding items | `taxes_exemptions_trim_vab` or `local_government_budget_procurement` | The `budget_millage` tag should be used for tax-policy items specifically, not general budget line items |
| Road impact fees | `rezoning_comp_plan_dri` | Borderline — could be `transportation`. Current mapping is acceptable. |

### Unresolved Ambiguities

- Should routine consent agenda utility easements use `taxonomy_gap: permit_status`?
- Donation/resolutions (parks facilities): currently `parks_amenities` — is there a `gifts_donations` gap?

## Taxonomy Note

`budget_millage` is correctly placed in the taxonomy as a topic tag. It is primarily used for:
- Millage rate hearings
- TRIM season budget workshops
- Tax levy ordinances
- School funding surtax items

It should NOT be used for routine contract awards or departmental budget line items. Those are better classified as `local_government_budget_procurement` or `county_government`.
