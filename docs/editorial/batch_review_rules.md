# ED-001 Batch Review Rules

Defined 2026-06-26 during the first full queue review (99 items, 83 batch-reviewed).

## When to Batch Verify

The following item families can be batch-verified without individual review,
because their source, structure, and resident relevance are consistent:

| Family | Source | Beat | Verification Rule |
|--------|--------|------|-------------------|
| Utility ROW permits | `sjc_nbor_public_notices` | `utilities_water` | Public ROW notice with project description, district, date, and PDF evidence |
| Construction/site work permits | `sjc_nbor_public_notices` | `site_plans_permits_construction` | Same structure as utility ROW |
| Development hearing notices | `sjc_nbor_public_notices` | `rezoning_comp_plan_dri` | Application ID + hearing date + description |
| Road closure notices | `sjc_nbor_public_notices` | `roadwork_traffic` | Lane closure with project details |
| BCC utility/water consent items | `sjc_bcc_calendar` | `utilities_water` | Utility easement or infrastructure resolution from agenda PDF |
| BCC parks/amenities consent items | `sjc_bcc_calendar` | `parks_amenities` | Facility donation, license agreement, park resolution |
| BCC rezoning/development items | `sjc_bcc_calendar` | `rezoning_comp_plan_dri` | Land-use resolution from agenda PDF |
| BCC transportation items | `sjc_bcc_calendar` | `transportation` | Road/infrastructure resolution from agenda PDF |
| BCC budget/tax items | `sjc_bcc_calendar` | `taxes_exemptions_trim_vab` | Budget/funding resolution from agenda PDF |
| BCC public safety items | `sjc_bcc_calendar` | `public_safety_livability` | Safety/emergency services resolution |
| County news items | `sjc_county_news` | Any | Official county press release with source URL |
| Utility department announcements | `sjc_utility_department` | Any | Official county utility notice with source URL |

## When Individual Review Is Required

| Item Type | Required Check |
|-----------|----------------|
| Sheriff press releases (crime) | Human review for factual accuracy, sensitivity |
| Active emergencies | Verify active status and source authority |
| BCC procurement/contract items | Limited agenda PDF context — may need backup document |
| Items with empty or unclear beats | Check source classification |
| Cross-source duplicates | Verify same event, link as supporting sources |

## When to Mark `needs_followup`

| Condition | Example |
|-----------|---------|
| Item text lacks enough context for resident impact assessment | BCC consent item: "Motion to adopt Resolution 2026-___" with no project description |
| Source URL is broken or redirects | BCC agenda link returns 404 |
| Classification is uncertain | Item could be `utilities_water` or `site_plans_permits_construction` — needs reviewer decision |
| Application ID is present but no matching detail | BCC agenda references a project but description is "see backup" |

## When to Mark `archived`

| Condition | Example |
|-----------|---------|
| Item is older than 3 months with no ongoing relevance | March 2026 DUI operation |
| Source event tracker, not individual intel item | BCC meeting-level metadata records |
| Completed project with no current impact | Utilities lab ribbon-cutting (completed) |

## When to Mark `rejected_noise`

| Condition | Example |
|-----------|---------|
| Feel-good/PR story with no resident-intel value | Recycling driver bond story |
| Ceremonial proclamation with no policy content | "Proclamation Recognizing Month" (if alone) |
| Purely internal administrative item | "Approval of minutes" |

## Evidence Requirements for Batch Verification

Before batch-verifying a family, confirm:
1. Source is official government (sjcfl.us, stjohnsclerk.com, sjso.org, stjohns.k12.fl.us)
2. Item has a `source_url` pointing to the original page
3. Item has a `raw_excerpt` or `summary` describing the content
4. Resident impact is clear from the beat classification
5. No `human_review_required` flag is set (those need individual review)

## Warning Signs That Block Batch Review

- Missing `source_url` or empty `raw_excerpt`
- `human_review_required: true`
- Beat is empty or `unknown`
- Escalation is `immediate` (verify individually)
- Application ID suggests a cluster with another item
- Item text is truncated or unreadable

## Examples from the 2026-06-26 Queue Review

### Verified (batch-compatible)
```yaml
item_id: "SJC-NBOR-20260626-0008"
source_id: "sjc_nbor_public_notices"
title: "Comcast"
beat: "utilities_water"
source_url: "https://webapp.sjcfl.us/webnews/NBRscreend.aspx"
raw_excerpt: "Fiber cable"
review_notes: "Batch verified: NBOR utility ROW permit. Public notice..."
```

### Needs Follow-up
```yaml
item_id: "SJC-BCC-20260120-0020"
source_id: "sjc_bcc_calendar"
beat: "local_government_budget_procurement"
title: "Motion to adopt Resolution..."
review_notes: "Needs follow-up: BCC procurement/contract item. Limited agenda PDF context..."
```

### Archived
```yaml
item_id: "SJC-SJSO-20260603-0003"
source_id: "sjso_news_stories"
title: "Nine arrested during SJSOs March 2026 DUI Wolfpack Operation"
review_notes: "Batch archived: BCC meeting-level metadata record..."
```

### Rejected as Noise
```yaml
item_id: "SJC-CN-20260626-0004"
source_id: "sjc_county_news"
title: "SJC Highlights Special Bond Between Recycling Driver and Three-Year-Old Resident"
review_notes: "Batch verified: county news low-impact item..."
```
