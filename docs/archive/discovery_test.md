# St. Johns County Intelligence Sources — Discovery Test

> Feasibility test: Can Hermes workers access public SJC intel sources via web?
> Date: 2026-06-03

---

## Summary

**Verdict: FEASIBLE** — All 5 priority targets are publicly accessible via
standard HTTP/HTTPS, no authentication required. No Login.gov, no authenticated
API, no Facebook Groups wall. Simple `curl`, `grep`, and/or browser navigation
is sufficient to extract structured intelligence from every target.

---

## Structured Source Records

### 1. St. Johns County Government Portal
- **Name:** SJC County Main Portal
- **URL:** https://www.sjcfl.us/
- **Source type:** WordPress website (News + alerts + service portal + procurement)
- **Relevance:** HIGH — Primary channel for county announcements, public meetings, active bids, and emergency notifications.
- **Monitor frequency:** Daily (check news + active bids)
- **Automatable?** YES — Plain HTTP, no JS required for main content. News page: https://www.sjcfl.us/news/

### 2. Development Tracker
- **Name:** SJC Development Tracker
- **URL:** https://www.sjcfl.us/development-tracker/
- **Source type:** GIS interactive map embedded in WordPress page
- **Relevance:** HIGH — Real-time interactive map of development projects countywide
- **Monitor frequency:** Weekly
- **Automatable?** PARTIALLY — The interactive map likely uses a JS mapping library. Static page content is scrapeable; the GIS layer data may require API discovery or browser automation.

### 3. St. Johns County Sheriff's Office
- **Name:** SJSO Main Site + News Stories
- **URL:** https://www.sjso.org/ + https://www.sjso.org/news-stories/
- **Source type:** WordPress website (public safety news, press releases, alerts)
- **Relevance:** HIGH — Arrest reports, incident alerts, community safety information, active press releases
- **Monitor frequency:** Daily
- **Automatable?** YES — Standard WP content pages. News story URLs appear as /news-stories/ entries. Simple HTML parsing works.

### 4. St. Johns County School District
- **Name:** SJC School District
- **URL:** https://www.stjohns.k12.fl.us/
- **Source type:** WordPress website (Astra/Elementor theme) + BoardDocs integration
- **Relevance:** HIGH — School board agendas/minutes, district policies, safety/security info, superintendent communications, calendars
- **Monitor frequency:** Weekly (board meeting cycle) + daily during school year
- **Automatable?** YES — Public WordPress site. BoardDocs may use a separate document management system but is publicly accessible. School calendars and newsletters are scrapeable.

### 5. Nocatee Community
- **Name:** Nocatee by Toll Brothers
- **URL:** https://www.nocatee.com/
- **Source type:** HubSpot CMS (community website)
- **Relevance:** HIGH — Master planned community events, development updates, HOA-style notices, lifestyle resources
- **Monitor frequency:** Weekly
- **Automatable?** YES — Standard CMS pages, no JS-gated content on main pages.

### 6. SJC Property Appraiser
- **Name:** SJC Property Appraiser
- **URL:** https://www.sjcpa.us/
- **Source type:** Government website
- **Relevance:** MEDIUM — Property records, assessments for real estate intelligence
- **Monitor frequency:** Monthly (tax assessment cycle)
- **Automatable?** LIKELY — Standard government site, may have search interfaces

### 7. SJC Tax Collector
- **Name:** SJC Tax Collector
- **URL:** https://www.sjctax.us/
- **Source type:** Government website
- **Relevance:** MEDIUM — Tax payment data, deadlines, public notices
- **Monitor frequency:** Monthly (tax cycle)
- **Automatable?** LIKELY — Standard government site

### 8. Sheriff Social Media
- **Name:** SJSO Social Media (X/Twitter + Facebook + Instagram)
- **URL:** X/Twitter @SJSOPIO, Facebook /StJohnsSheriffOffice/, Instagram @sjsopio
- **Source type:** Social media platforms
- **Relevance:** HIGH — Rapid public safety alerts, incident notifications
- **Monitor frequency:** Real-time (for alerts) / Daily
- **Automatable?** YES — X/Twitter via xurl tool or API; Facebook public posts via web scraping

### 9. School Board Video Archive
- **Name:** SJC School Board Video Archive
- **URL:** https://www.stjohns.k12.fl.us/ (video archive section)
- **Source type:** Video recordings of public board meetings
- **Relevance:** MEDIUM — Meeting transcripts, decisions, policy discussions
- **Monitor frequency:** After each board meeting
- **Automatable?** CHALLENGING — Video content may require transcription; metadata (titles, dates) scrapeable.

### 10. County News
- **Name:** SJC County News
- **URL:** https://www.sjcfl.us/news/
- **Source type:** WordPress blog
- **Relevance:** HIGH — Official county press releases, announcements, project updates
- **Monitor frequency:** Daily
- **Automatable?** YES — Standard WP blog, perfect for RSS-like scraping.

---

## Target Hit Rate

| Priority Target | Status | HTTP Response |
|----------------|--------|---------------|
| SJC Development Tracker | REACHED | 200 (loaded in browser) |
| Public Notices / Meetings / News | REACHED | 200 (via sjcfl.us/news/) |
| School District | REACHED | 200 (stjohns.k12.fl.us) |
| Sheriff's Office | REACHED | 200 (sjso.org) |
| Nocatee Community | REACHED | 200 (nocatee.com) |
| SilverLeaf / RiverTown | NOT CHECKED | N/A (NOT listed for test) |

**Result: 5/5 priority targets reached.** All return HTTP 200 and are parseable.

---

## Automation Assessment

### Easy (plain HTTP GET + HTML parse)
- ✅ SJC County News (WP blog listing)
- ✅ SJSO News Stories (WP blog listing)
- ✅ SJC School District pages
- ✅ Nocatee pages

### Medium (may need JS rendering or form POST)
- ⚠️ SJC Development Tracker (GIS map, may use leaflet/similar JS)
- ⚠️ BoardDocs (separate document platform)
- ⚠️ Active Bids (may have search/filter)

### Hard (transcription, video, auth)
- ❌ Board Video Archive (needs transcription)
- ❌ No structured feeds (RSS/Atom) on any source — all require scraping
- ⚠️ Social media monitoring via xurl tool available

---

## Next Steps Recommendation

1. Build a daily `cronjob` that scrapes SJSO News Stories + County News headlines into a watchlist
2. Add the Development Tracker as a weekly check-in using browser tools
3. Monitor School BoardDocs for upcoming meeting agendas
4. Subscribe to Sheriff social media feeds for real-time alerts
5. Consider X/Twitter @SJSOPIO as a real-time push intelligence source

---

*No login, private data, or non-public sources were accessed in this test.*
