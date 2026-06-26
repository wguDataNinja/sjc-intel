# SJC_Intel Monitor Pilot Report

## Source Checked

**Source ID:** `sjc_county_news`
**Name:** SJC County News
**URL:** https://www.sjcfl.us/news/

## Access Method

- **Tool:** `webfetch` (HTTP GET, text format)
- **HTTP Status:** 200 (OK)
- **Auth required:** No
- **JS required:** No for main page content; Archive section uses AJAX for load-more pagination
- **Date accessed:** 2026-06-03

## Items Extracted

**Total items found on page:** 4 (Featured News section)
**Additional items found via sidebar navigation:** 2
**Items selected for output:** 5 (latest 5 by publication date)

### Extracted Items

| # | item_id | Title | Date | Category |
|---|---------|-------|------|----------|
| 1 | SJC-CN-20260603-0001 | Surplus Goods Public Auction Scheduled for June 20 | May 26 | SJC News |
| 2 | SJC-CN-20260603-0002 | SJC Highlights Long-Term Resiliency Improvements at Porpoise Point | May 26 | SJC News |
| 3 | SJC-CN-20260603-0003 | Public Library Announces 2026 Summer Reading Program | May 18 | SJC News |
| 4 | SJC-CN-20260603-0004 | St. Johns County Earns Statewide Communications Recognition | May 14 | SJC News |
| 5 | SJC-CN-20260603-0005 | St. Johns County Enters Phase III Extreme Water Shortage Declaration | May 13 | Community Well-Being |

### Items Not Included (available but older)

- "St. Johns County Celebrates Small Business Week" (May 7) — 6th most recent, omitted to keep 5-item limit.

## Schema Issues (Resolved)

The following issues were identified during the pilot and have been resolved
in subsequent reconciliation (see session 4):

1. ~~**`recommended_channels` values not yet in schema vocabulary.**~~ **RESOLVED.** Schema v1.1 adds `website_review_queue` and `weekly_brief_candidate` to the allowed values. See `schemas/intel_item.schema.yaml` and `docs/taxonomy.md`.

2. ~~**`review_status` value `pending_review` not in schema.**~~ **RESOLVED.** Schema v1.1 renames `pending` → `pending_review` for clarity. The pilot's values are now canonical. See `schemas/intel_item.schema.yaml`.

3. ~~**`communities` controlled vocabulary not yet defined.**~~ **RESOLVED.** Community registry created at `registry/communities.yaml` with 20+ entries. The ad-hoc names from the pilot (`vilano_beach`, `porpoise_point`) have been formally registered.

4. ~~**`topics` controlled vocabulary not yet defined.**~~ **RESOLVED.** Taxonomy document created at `docs/taxonomy.md` with controlled vocabularies for all classification fields.

5. **Still open — minor.** `source_published_at` lacks a time component (source provides dates only). `discovered_by` uses a descriptive string rather than a Hermes worker name — acceptable for pilot, will use proper worker names in automation.

## Dedupe / Index Issues

1. **Index file created:** `data/index/prior_items.yaml` with 5 entries.
   - Dedupe key format: `{source_id}||{item_url}` (concatenation of source_id and full URL).
   - This is effective for URL-based dedup but would not catch re-published items with different URLs.

2. **No prior index existed before this run.** All 5 items were treated as new. Future runs will use this index for dedup.

3. **Index maintenance:** The flat-file YAML index will grow linearly. For a daily monitor, this is manageable for months. Consider switching to SQLite once the index exceeds ~500 entries.

4. **No dedup across sources.** If the same story is published on sjc_county_news and another source, the current index would not catch the duplicate. Cross-source dedup is a future enhancement.

## Suitability for Daily Monitoring

**Verdict: SUITABLE — Strong candidate for daily monitoring.**

### Strengths
- **Reliable HTTP 200** — Page consistently returns 200 OK.
- **No auth/JS gating** — Core Featured News content is server-rendered HTML.
- **Rich content** — Each article has full text, date, category tags, and structured "Key Takeaways" sections that are easily extractable.
- **Stable URL structure** — WordPress permalink pattern (`/slug/`), predictable category/date metadata.
- **High community value** — Mix of actionable items (auction, water restrictions), infrastructure news, and community events.

### Challenges
- **No RSS/Atom feed** — Requires full-page HTML fetch every cycle.
- **Archive pagination uses AJAX** — Only the 4 Featured News items are in the initial HTML. Older items load via `admin-ajax.php` POST. For daily monitoring this is acceptable (4 items is a typical daily volume), but a full archive scrape would need AJAX integration.
- **Sidebar "Latest News" only accessible from individual article pages** — The sidebar with 5 recent items is only rendered when you load an individual article. The main listing page only shows the Featured News section by default.
- **No structured timestamps** — Dates are shown as "May 26" without years in the listing. Individual article pages show full dates (e.g., "26 May 2026").

### Recommended Approach for Automation
1. Fetch `https://www.sjcfl.us/news/` daily and parse Featured News section.
2. For each featured item, fetch the individual article page to get full text, date, and category.
3. Use the sidebar "Latest News" from any fetched article as a secondary check for items that may have been bumped from Featured.
4. Store dedup key as `{article_url}` against the prior_items index.

## Recommended Next Source

**`sjso_news_stories`** (https://www.sjso.org/news-stories/)

- Same WordPress architecture as sjc_county_news — extraction logic is directly reusable.
- High community value for public safety intelligence.
- Daily frequency aligns with the established monitoring cadence.
- The WP-to-WP pattern match would validate whether the monitoring workflow generalizes across sources.

---

*Report generated: 2026-06-03T04:30:00Z*
*Generated by: sjc-intel-architect (pilot)*
*Run type: Interactive pilot (not automated Hermes cronjob)*
