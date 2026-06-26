# SJC_Intel Monitor Pilot Report — sjso_news_stories

## Source Checked

**Source ID:** `sjso_news_stories`
**Name:** SJSO News Stories
**URL:** https://www.sjso.org/news-stories/

## Access Method

- **Tool:** `webfetch` (HTTP GET, text format)
- **HTTP Status:** 200 (OK)
- **Auth required:** No
- **JS required:** No — WordPress listing page renders server-side
- **Date accessed:** 2026-06-03

## Items Extracted

**Total items found on page:** 6 (across main feed grid)
**Items selected for output:** 4 (latest by publication date)
**Items skipped:** 1 (older homicide development story — Feb 2025, duplicated in Cold Cases); 1 (30+ Arrested internet predator operation — URL malformed)

### Extracted Items

| # | item_id | Title | Date | Topics | Sensitivity |
|---|---------|-------|------|--------|-------------|
| 1 | SJC-SJSO-20260603-0001 | Inmate charged; woman arrested for contraband drop on SJSO property | May 21, 2026 | public_safety, crime | medium |
| 2 | SJC-SJSO-20260603-0002 | Lifesaving rescue highlights local programs for vulnerable individuals | May 5, 2026 | public_safety, health_wellness | low |
| 3 | SJC-SJSO-20260603-0003 | Nine arrested during SJSOs March 2026 DUI Wolfpack Operation | April 20, 2026 | public_safety, crime | medium |
| 4 | SJC-SJSO-20260603-0004 | Arrest made in connection to 2023 double murders of Bennett and Lyons | Nov 25, 2025 | public_safety, crime | high |

## Sensitivity Handling Notes

This pilot exercised the sensitivity classification rules defined for
public-safety sources:

| Item | Sensitivity | Rationale | Human Review |
|------|-------------|-----------|--------------|
| Contraband drop | medium | Crime, arrest, named individuals | Required |
| Lifesaving rescue | low | Positive community program story; minor mentioned but focus is on program enrollment | Required (minor named) |
| DUI Wolfpack | medium | DUI arrests, crime category | Required |
| Double murder arrest | high | Double murder, named victims, named suspect, ongoing investigation | Required (mandatory) |

### Sensitivity Defaults Applied

- **Public safety / crime items:** `recommended_channels` set to
  `["website_review_queue"]` only — no `weekly_brief_candidate` for
  items involving crime, arrests, or named individuals, per classification
  rules.
- **High-sensitivity item (double murder):** Flagged with explicit
  reviewer_notes warning against implying guilt beyond official charges.
- **Minor in story (lifesaving rescue):** `human_review_required: true`
  even though content is positive and educational, because a minor is
  named in the source release.

## Resident Interest Backfill

**Context:** The SJSO news pilot was configured after the
resident-interest classification layer was designed (see
`agents/resident-interest-classifier.md`,
`prompts/resident_interest_classification_task.md`,
`docs/resident_interest_classification.md`). This means the data file
was created with resident-interest fields populated inline, rather than
requiring a separate backfill step.

Fields populated per item:
- `primary_topic` — single canonical topic from taxonomy
- `interest_tags` — resident-interest dimensions (e.g., `safety_concern`,
  `community_event`, `quality_of_life`, `emergency_awareness`)
- `resident_relevance.summary` — why-this-matters from resident perspective
- `resident_relevance.affected_audiences` — specific audience targeting
- `resident_relevance.why_it_matters` — concrete resident impact
- `resident_relevance.confidence` — evidence-bound (all high for SJSO items)
- `resident_relevance.inference_notes` — what was inferred vs. stated
- `human_review_required` — flag for sensitive items

### Backfill Assessment

**No retroactive changes needed.** The sheriff pilot was created after
the RI classifier layer was defined. The data file complies with v2.0
schema out of the gate. All items have complete resident-interest blocks.

If a prior sheriff pilot had existed without these fields, the backfill
would have required:
1. Reading each item's `title`, `summary`, `raw_excerpt` and `topics`
2. Running through the RI classification rules
3. Adding `primary_topic`, `interest_tags`, `resident_relevance` block,
   `taxonomy_gap`, and `human_review_required`
4. Updating the YAML file in place

No such migration was needed in this case.

## Schema Compatibility

All 4 items comply with `schemas/intel_item.schema.yaml` v2.0.

### v2.0 Fields Used

| Field | Status |
|-------|--------|
| `primary_topic` | Populated on all items |
| `interest_tags` | Populated on all items |
| `resident_relevance` (block) | Populated on all items |
| `taxonomy_gap` | Not used — no gap identified |
| `human_review_required` | Populated on all items (true for 4/4) |

### Notes

- `taxonomy_gap` was not needed — all items fit existing taxonomy values.
- No new interest tags or audience values were required beyond the
  defined vocabularies.
- The `emergency_awareness` interest tag was used for the double murder
  item (ongoing investigation, police seeking public help).

## Dedupe / Index Issues

1. **Index updated:** 4 entries added to `data/index/prior_items.yaml`
   under a new `# --- sjso_news_stories` section.
2. **No cross-source dedup risk:** SJSO URLs are distinct from
   sjc_county_news URLs (different domain, different slug patterns).
3. **URL encoding note:** One item on the SJSO listing page had a
   malformed URL (Unicode percent-encoding from the CMS). It was skipped
   because the URL was not reliably fetchable. This should be investigated
   — the CMS slug generation may produce non-ASCII URLs for certain
   article titles.
4. **Total index size:** 9 entries (5 sjc_county_news + 4 sjso_news_stories).

## Suitability for Daily Monitoring

**Verdict: SUITABLE — Strong candidate for daily monitoring.**

### Strengths
- **Reliable HTTP 200** — Page consistently returns 200 OK.
- **No auth/JS gating** — Content renders server-side.
- **Rich content** — Full press release text on individual article pages.
- **Clear date stamps** — Every article has a visible publication date.
- **High community value** — Public safety information is consistently
  the most-engaged category for local news.

### Challenges
- **No RSS/Atom feed** — Requires full-page HTML fetch every cycle.
- **Listing page uses Elementor** — The CMS renders article listings
  through a page builder; the HTML structure is more complex than the
  simple WordPress loop on sjcfl.us. Extraction selectors will differ.
- **Unicode URL issue** — One article had a CMS-generated URL with
  percent-encoded Unicode characters. This may cause fetch failures
  for certain articles. Monitor should handle this gracefully.
- **Lower volume than county news** — SJSO posts less frequently
  (roughly 1-2 per month). Daily monitoring will mostly return "no new
  items," which is expected.

### Recommended Approach for Automation
1. Fetch `https://www.sjso.org/news-stories/` daily.
2. Parse the Elementor post-grid widget for article links and dates.
3. For each new article URL (not in dedupe index), fetch the full
   article page for text extraction.
4. Classify with `sensitivity: medium` as default for SJSO content,
   override to `low` for community program notices, `high` for
   active incidents or named victims.

## Recommended Next Source

**`sjc_school_district`** (https://www.stjohns.k12.fl.us/)

- Covers education — the third major intelligence domain after county
  government and public safety.
- Different architecture (WordPress + BoardDocs integration) — tests
  extraction complexity.
- Weekly monitoring frequency aligns with school board meeting cycles.

---

*Report generated: 2026-06-03T06:30:00Z*
*Generated by: sjc-intel-architect (pilot)*
*Run type: Interactive pilot with resident-interest classification*
