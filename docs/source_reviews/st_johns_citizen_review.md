# Source Review: St. Johns Citizen

> Public web source review performed on 2026-06-03.
> Review method: Website review (sjcitizen.com) — About, Advertise, Contact pages.
> Facebook public page was not accessible programmatically (HTTP 400).

---

## What Is St. Johns Citizen?

A legitimate local news and media organization serving St. Johns County,
Florida. It presents as a professional digital news outlet with multiple
contributors, regular daily publishing, advertising infrastructure, and
a newsletter program. It calls itself "Your Community-Driven News Leader."

## Who Operates / Contributes to It

**Publishers:**
- **Selim Algar** — Former Florida Bureau Chief for the New York Post.
  Has written for The New York Times, New York Magazine, NBC Sports,
  The Austin American-Statesman, The San Francisco Examiner. Ponte Vedra
  resident. Co-authored #1 Amazon bestselling book "At Any Cost"
  (Macmillan Publishers). Has appeared on NBC, CNN, Fox News.
- **Rebecca Rosenberg** — Former senior criminal justice reporter for
  Fox News. Covered Alex Murdaugh double murder trial, Johnny Depp
  defamation case, Harvey Weinstein case. Has appeared on ABC's 20/20,
  CBS's 48 Hours, NBC's Dateline.

**Named Contributors (9+):**
- Paul Sebess — Contributing Food Columnist
- Susan Johnson — Contributor
- Melissa Hernandez — Contributor
- Alex Barnhart — Contributing Reporter
- Brennan Ambrose — Contributing Reporter
- Grimm Bergh — Multimedia Contributing Reporter
- Noah De Haan — Contributor
- Audrey Cress — Contributing Reporter
- (Additional unnamed contributors)

**Contact:** (904) 228 5885, [email protected]

## Sections / Categories Published

1. **News** — Local government, crime, public safety, development
2. **Eats** — Restaurant openings, food news, dining
3. **Sports** — Local sports coverage
4. **Lifestyle** — Quality of life, community features
5. **Real Estate** — Property news, housing, development
6. **Vacations** — Travel and tourism (in footer navigation)
7. **Florida** — State-wide news relevant to the county

## Publishing Cadence

**Daily.** The site displays the current date ("Wednesday, June 3, 2026"
on the homepage as of review). Multiple articles are published daily.
The homepage showed 12+ articles in the main feed and 6 more in a
"Trending" sidebar. This is a high-volume, active news operation.

## Communities / Corridors Covered

Based on article content visible on the homepage:
- St. Johns County (county-wide)
- St. Augustine (multiple articles)
- Ponte Vedra / Ponte Vedra Beach
- Nocatee
- Palm Valley
- Northwest St. Johns County
- Jacksonville (regional — Alhambra Theatre coverage)

## Homeowner-Relevant Beats Covered

Directly from visible articles on the homepage:
1. **Development** — "Exclusive: Here's what coming to new Nocatee
   retail center across from water park"
2. **Housing / Neighborhood disputes** — "Storage Wars: Oversized Palm
   Valley garage mistakenly approved by county sparks neighborhood fight"
3. **Local government / Politics** — "St. Johns County Board Chair Clay
   Murphy says 'radical leftists' have infiltrated local Republican party"
4. **Public safety / Crime** — Multiple crime articles (beach crash,
   homeless arrest, teacher arrest, elder scam)
5. **Infrastructure** — "County Finishes Major Flood Mitigation, Access
   Improvements at Porpoise Point" (overlaps with SJC County News pilot)
6. **Restaurants / Food** — Prohibition Kitchen distillery proposal,
   restaurant lease dispute
7. **Legal / Lawfare** — County attorney contract, food truck park vote
8. **Transportation** — Pedicab drivers at Amphitheatre
9. **Education** — Teacher arrested for inappropriate communication with
   student
10. **Real estate** — Multiple real estate tagged articles

## What the Website Does

- Serves as a full-content news hub (not a link-aggregator)
- Each article appears to be original reporting
- Has newsletter signup (multiple placements on page)
- Has search functionality
- Has trending sidebar
- Has social media links (X/Twitter, Instagram, Facebook)
- Has advertising/sponsorship page with rate card
- Has "Has been cited by" section (social proof/authority building)
- Professional WordPress theme with custom development

## How Facebook Appears to Support the Website

Facebook page exists at `/stjohnscitizen` but was not accessible
programmatically. Based on the site's social links in header/footer
and the advertising page claiming "67,000 social media followers,"
Facebook appears to be a primary distribution channel. The ads page
lists social media followers as a metric, suggesting active cross-
platform distribution.

## Newsletter / Audience Capture

**Yes.** The site has a prominent newsletter signup:
- Multiple placements (homepage, footer, pop-up footer bar)
- Advertising page claims: **7,800 subscribers with 61% open rate**
- This is a high open rate, suggesting strong audience engagement
- Newsletter appears to be a core channel, not an afterthought

## Advertising / Sponsorship Infrastructure

**Yes, professional-grade.**
- Dedicated "Advertise With Us" page with rate card
- Claims: 280,000 page views/month, 170,000 readers/month,
  67,000 social media followers
- Audience demographics: 72% women, 75% ages 35-64,
  predominantly homeowners, primarily upper middle class
- Offers category exclusivity
- Provides third-party analytics reports
- Contact form for advertising inquiries
- Phone: (904) 228 5885

## Suitability as a Monitor Source

**HIGH — Strongly suitable.**

| Factor | Assessment |
|--------|-----------|
| Content quality | High — veteran journalists, original reporting |
| Publishing cadence | Daily — multiple articles per day |
| Topic overlap with SJC_Intel | High — development, government, safety, real estate |
| Geographic focus | Direct — St. Johns County |
| Extraction difficulty | Low — standard website structure |
| Reliability | High — named contributors with verifiable backgrounds |
| Value to SJC_Intel | High — covers beats SJC_Intel would track independently |

## Recommended Monitor Cadence

**Daily.** The site publishes multiple articles every day. A daily
check will capture new content promptly. Weekly would miss too much.

## Extraction Challenges

- **Standard website structure.** No obvious JS-gating or authentication
  walls. Articles appear to be accessible without login.
- **WordPress-based.** Likely follows standard WordPress URL patterns.
- **No RSS feed visible.** Would need HTML parsing.
- **Facebook not accessible programmatically.** Would need to rely on
  website content or use social media monitoring tools for Facebook
  distribution.

## Reliability Level

**High.** Both publishers have extensive, verifiable journalism careers
at major national outlets (NY Post, Fox News, NY Times). The organization
is transparent about who operates it. The site has professional
advertising infrastructure. Multiple named contributors. This is a
legitimate media outlet, not an anonymous or unreliable source.

However, as with any news outlet, editorial bias is expected. The site's
publishers have backgrounds in conservative media (NY Post, Fox News),
which may influence story selection and framing. SJC_Intel should treat
its content as **news reporting with potential editorial perspective**,
not as raw government data.

## Promotion Decision

**Recommendation: PROMOTE to canonical sources.**

St. Johns Citizen should be promoted to `registry/sources.yaml` as an
active monitored source. It covers nearly every beat SJC_Intel tracks,
publishes daily original reporting, and is operated by verified
professional journalists.

**Not yet promoted.** This recommendation requires Buddy approval before
the canonical registry is modified. After approval:
- source_id: `st_johns_citizen`
- source_type: `local_media`
- status: `active`
- monitor_frequency: `daily`
- relevance: `HIGH`

---

## Competitive / Comparable Analysis

### Where It Overlaps with SJC_Intel

- **Geographic focus:** Both target St. Johns County residents
- **Topic coverage:** Both cover local government, development, public
  safety, community events, real estate
- **Audience:** Both aim to serve homeowners and residents with
  actionable local intelligence
- **Newsletter:** Both see newsletter as a primary owned channel
- **Distribution:** Both use social media (though SJC_Intel hasn't
  launched a public presence yet)

### What It Does Well

1. **Original reporting.** They produce original journalism, not
   aggregation. This gives them authority and differentiation.
2. **Professional pedigree.** The publishers' backgrounds at NY Post
   and Fox News lend instant credibility.
3. **Multiple revenue streams.** Advertising, sponsorships, and
   potentially newsletter monetization — a real business model.
4. **Clear audience demographics.** They know their reader base
   (72% women, homeowners, upper-middle-class) and sell to it.
5. **Daily cadence.** They maintain a professional publishing schedule.
6. **Section depth.** They don't just cover news — they have dedicated
   sections for food, sports, lifestyle, and real estate, making the
   site a destination, not just a feed.

### What SJC_Intel Can Learn

1. **Professional presentation signals legitimacy.** The clean website,
   named contributors, and advertising page create trust. SJC_Intel's
   future public face should aim for the same.
2. **Newsletter metrics matter.** 7,800 subscribers with 61% open rate
   is a strong benchmark. SJC_Intel should track its own newsletter
   metrics against this if it launches one.
3. **Category exclusivity is a selling point.** The ads page promises
   "you would be the only business in your specialty on our site."
   This is a smart differentiator.
4. **Social proof via citations.** The "Has been cited by" section
   builds authority. SJC_Intel should consider how to build citation
   relationships.
5. **Daily cadence is achievable.** If a small team can publish multiple
   articles daily, SJC_Intel's monitoring pipeline can certainly produce
   daily summaries.

### What SJC_Intel Can Do Differently or Better

1. **Broader source coverage.** St. Johns Citizen publishes one
   organization's reporting. SJC_Intel can synthesize across 10+
   sources, providing a more complete picture.
2. **Systematic monitoring.** SJC_Intel doesn't need human journalists
   to find stories — it monitors automatically. This means broader
   coverage with less bias.
3. **Resident-interest classification.** St. Johns Citizen reports what
   happened. SJC_Intel classifies *why it matters to residents* — a
   different value proposition.
4. **Cross-source verification.** SJC_Intel can cross-reference claims
   across multiple sources (county news, sheriff, school district, etc.)
   rather than relying on one outlet's reporting.
5. **No editorial perspective.** SJC_Intel is an intelligence system,
   not a news outlet. It can position itself as neutral/objective
   compared to outlets with editorial voice.

### What SJC_Intel Should Avoid Copying

1. **Original reporting.** SJC_Intel should NOT try to produce original
   journalism. It's an aggregation/classification system. Trying to
   compete on reporting would require journalists, fact-checking, legal
   review, and editorial liability that are out of scope.
2. **Editorial voice.** The St. Johns Citizen articles have perspective
   and framing. SJC_Intel summaries should remain neutral and factual.
3. **Advertising-dependent model.** St. Johns Citizen needs page views.
   SJC_Intel's value is in curation and classification, not page views.

---

## Review Checklist Results

| # | Question | Answer |
|---|----------|--------|
| 1 | Website publicly accessible without login? | YES |
| 2 | Content original reporting or curated aggregation? | ORIGINAL REPORTING |
| 3 | Sources and authors attributed? | YES (named contributors with bios) |
| 4 | About page or editorial mission statement? | YES (detailed About page) |
| 5 | Clear distinction between news and opinion? | NOT CLEARLY LABELED — potential concern |
| 6 | Facebook page shares original content or links? | LIKELY YES (not directly verifiable) |
| 7 | Content reliably factual? | LIKELY YES (professional journalists) |
| 8 | Corrections policy? | NOT VISIBLE — not found on site |
| 9 | Named contributors with bylines? | YES (9+ named) |
| 10 | Contact/ownership information public? | YES (phone, email, physical address implied) |

**Areas to monitor:** The site does not appear to clearly label opinion
vs. news content, and no corrections policy was found. These are common
gaps for smaller news operations and do not disqualify it as a source,
but SJC_Intel should be aware of editorial framing when extracting items.

---

## Updated Discovery Pipeline Signals

Based on this review, the following signals indicate a **high-quality
local media source** worth monitoring:

1. **Named publishers with verifiable journalism backgrounds**
2. **Multiple named contributors** (not anonymous)
3. **Daily publishing cadence** (multiple articles per day)
4. **Professional website with dedicated sections** (not a single-topic blog)
5. **Original reporting** (not aggregation or republishing)
6. **Advertising/sponsorship infrastructure with rate card**
7. **Newsletter with measurable subscriber metrics**
8. **Social media following as a tracked distribution channel**
9. **Contact information and physical presence** (phone, address)
10. **Clear geographic focus** (St. Johns County)
11. **Topic breadth** covering multiple homeowner-relevant beats
12. **"Has been cited by" or similar authority signals**

These signals should be added to the Local Media Discovery Sub-Loop in
`docs/discovery_loops.md` as criteria for evaluating newly discovered
organizations.
