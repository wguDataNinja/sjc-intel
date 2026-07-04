# Aug-Sep 2025 Historical Backfill — Hermes Execution Template

> Execution-ready dispatch plan. Break into 4 workers.
> Do not run without explicit instruction from Buddy.

---

## Window

| Field | Value |
|-------|-------|
| Start date | 2025-08-01 |
| End date | 2025-09-30 |
| Month keys | `2025-08`, `2025-09` |
| Output root | `data/monthly/` |
| ID prefix | `SJC-BF-202508-{NNNN}` (Aug), `SJC-BF-202509-{NNNN}` (Sep) |

## Why This Period

1. **TRIM season** — Property tax notices mailed August, budget hearings/millage-rate adoption September. Baseline for year-over-year tax comparisons.
2. **School rezoning** — Boundary changes adopted in Jun-Jul 2025, implemented Aug-Sep. Capture final adoption and community reaction.
3. **Hurricane season peak** — Aug-Sep = peak Atlantic. Emergency management, storm prep, potential impacts.

---

## Dispatch Plan: 4 Workers

### Worker 1 — Budget / Millage / TRIM (highest priority)
**Files:** `data/monthly/2025-08/discovered_items.yaml`, `data/monthly/2025-09/discovered_items.yaml`

**Source stacks (in order):**
1. **Property Appraiser** — `https://www.sjcpa.gov/` → search for TRIM notices, proposed rates, rolled-back rates, comparison tables
   - Archive.org fallback: `https://web.archive.org/web/202508*/https://www.sjcpa.gov/`
2. **BCC Calendar/Agendas** — `https://www.sjcfl.us/bccmeetings/` → search for Aug-Sep 2025 budget hearings, millage rate resolutions, FY2026 budget ordinances
   - Archive.org: `https://web.archive.org/web/*/sjcfl.us/bccmeetings/*`
3. **Tax Collector** — `https://www.sjctax.us/` → TRIM payment info, deadlines
4. **Budget Transparency** — `https://www.sjcfl.us/budget/` → FY2026 adopted budget documents

**Search queries (date-restricted to 2025-08 to 2025-09):**
```
"St. Johns County" TRIM notice 2025
"St. Johns County" millage rate 2025 proposed
"St. Johns County" FY2026 budget adoption
"St. Johns County" "truth in millage" 2025
"property appraiser" "St. Johns County" "proposed rate" 2025
"rolled-back rate" "St. Johns County" 2025
site:sjcfl.us "budget hearing" 2025
site:sjcpa.gov TRIM 2025
"tax notice" "St. Johns County" August 2025
"public hearing" "budget" "St. Johns County" 2025
```

**Expected:** 5-15 items per month for budget/millage alone.

**Validation:** Count items per month. Budget/millage should be the largest topic group.

---

### Worker 2 — School Rezoning
**Files:** `data/monthly/2025-08/discovered_items.yaml`, `data/monthly/2025-09/discovered_items.yaml`

**Source stacks:**
1. **SJCSD BoardDocs** — `https://go.boarddocs.com/fl/sjcsd/Board.nsf/Public` → search Aug-Sep 2025 meetings for boundary-related agenda items
   - Archive.org: `https://web.archive.org/web/*/boarddocs.com/fl/sjcsd/*`
2. **SJCSD main site** — `https://www.stjohns.k12.fl.us/` → news, boundary maps, school start announcements
3. **School board meeting minutes** — Check Jun-Jul 2025 too (rezoning votes often happen then, implemented Aug-Sep)

**Search queries:**
```
"St. Johns County School District" rezoning 2025
"attendance boundary" "St. Johns County" 2025
"school boundary" "SJCSD" 2025
"new school opening" "St. Johns County" 2025
"school zone" "St. Johns County" 2025
"first day of school" "St. Johns County" 2025
"School QQ" OR "School RR" 2025
site:stjohns.k12.fl.us boundary 2025
site:boarddocs.com "St. Johns" rezoning 2025
"attendance zone" "SilverLeaf" OR Nocatee 2025
```

**Expected:** 3-8 items per month. Aug may have heavy back-to-school content; Sep may be quieter.

**Validation:** School topics should be the second-largest group after budget.

---

### Worker 3 — Emergency / Development / Everything Else
**Files:** `data/monthly/2025-08/discovered_items.yaml`, `data/monthly/2025-09/discovered_items.yaml`

**Source stacks:**
1. **Emergency Management** — `https://www.sjcfl.us/emergencymanagement/` → storm prep, EOC activations
   - Archive.org: `https://web.archive.org/web/202508*/https://www.sjcfl.us/emergencymanagement/`
2. **NWS Jacksonville** — `https://www.weather.gov/jax/` → tropical advisories, severe weather
   - Archive.org: `https://web.archive.org/web/202508*/weather.gov/jax/*`
3. **SJSO** — `https://www.sjso.org/` → news releases
4. **Planning & Zoning** — `https://www.sjcfl.us/planning-zoning/` → PZA meetings, DRIs
5. **Development Tracker** — `https://www.sjcfl.us/development-tracker/`
6. **County Roads** — `https://www.sjcfl.us/engineering/` → road projects
7. **NFLRoads / FDOT** — `https://www.nflroads.com/` → SJC projects
8. **SJC Utility** — `https://www.sjcfl.us/utilities/` → boil notices, restrictions
9. **Permit Status** — `https://www.sjcfl.us/permit-status/` → notable permits

**Search queries:**
```
"St. Johns County" "tropical storm" OR hurricane 2025
"St. Johns County" "emerg management" OR "EOC" 2025
"St. Johns County" "boil water" 2025
site:sjcfl.us "road closure" 2025
site:sjcfl.us PZA OR rezoning 2025
site:sjso.org news 2025
site:nflroads.com "St. Johns" 2025
"CR 210" widening OR closure 2025
"SR 16" widening OR closure 2025
"permit" "SilverLeaf" OR Nocatee 2025
```

**Expected:** 3-10 items per month, highly dependent on storm activity.

**Validation:** Emergency items should be clearly absent if no storms threatened; record the absence.

---

### Worker 4 — Media Cross-Ref + Clustering + Wrap
**Depends on:** Workers 1-3 completing

**Source stacks:**
1. **St. Johns Citizen** — `https://sjcitizen.com/` → search Aug-Sep 2025
2. **Jacksonville Daily Record** — `https://www.jaxdailyrecord.com/` → search for SJC content
3. **Ponte Vedra Recorder** — `https://www.pontevedrarecorder.com/`
4. **Local TV** — Action News Jax, News4Jax, First Coast News (web searches only)

**Worker 4 does:**
1. Cross-reference official-source items against media coverage
2. Add media-sourced items (with `verification_status: unverified` unless official-confirmed)
3. Classify all items with RI fields (primary_topic, interest_tags, resident_relevance)
4. Cluster into `topic_clusters.yaml` per month
5. Write `source_gaps.md` per month
6. Write `monthly_wrap.md` per month
7. Write cross-month synthesis note if Aug-Sep items span both months

**Search queries:**
```
site:sjcitizen.com "budget" OR "rezoning" 2025
site:sjcitizen.com TRIM OR millage 2025
site:jaxdailyrecord.com "St. Johns County" 2025
site:pontevedrarecorder.com "county" OR "school" 2025
"Action News Jax" "St. Johns County" August 2025
"News4Jax" "St. Johns County" September 2025
```

---

## Output Schema

### Per-month files (8 total, 4 per month)

| File | Purpose |
|------|---------|
| `data/monthly/2025-08/discovered_items.yaml` | All extracted items (schema below) |
| `data/monthly/2025-08/topic_clusters.yaml` | Clusters + unclustered items |
| `data/monthly/2025-08/source_gaps.md` | Gaps, thin coverage, new source recommendations |
| `data/monthly/2025-08/monthly_wrap.md` | Narrative summary |

### Cross-month file (optional)

| File | Purpose |
|------|---------|
| `data/monthly/aug_sep_2025_crosscut.md` | Only if items span both months (budget rate comparison, rezoning continuity, storm sequence) |

### Item schema (per intel_item v2.0)

Every item in `discovered_items.yaml`:

```yaml
- item_id: "SJC-BF-202508-0001"       # SJC-BF-202508-* for Aug, SJC-BF-202509-* for Sep
  title: "Concise headline from source or summary"
  summary: "1-3 sentence factual summary"
  source_id: "sjc_county_news"         # canonical source_id or "web_discovery"
  source_url: "https://..."            # direct URL
  source_published_at: "2025-08-15"    # ISO 8601 or null
  discovered_at: "2026-06-26T..."      # extraction timestamp
  topics: ["taxes_exemptions_trim_vab"]  # from docs/taxonomy.md
  communities: []                      # from communities.yaml; [] = countywide
  geographic_scope: "county_wide"      # county_wide | multi_community | single_community | neighborhood | address_specific
  urgency: "timely"                    # urgent | timely | ongoing | archival
  verification_status: "source_confirmed"  # source_confirmed | unverified
  sensitivity: "low"                   # low | medium | high
  recommended_channels:
    - "website_review_queue"
    - "weekly_brief_candidate"
  raw_excerpt: "First paragraph or key sentence from source"
  review_status: "pending_review"
  primary_topic: "taxes_exemptions_trim_vab"
  interest_tags: ["property_taxes", "budget"]
  resident_relevance:
    summary: "Why this matters to residents"
    affected_audiences: ["homeowners", "property_owners"]
    why_it_matters: "Concrete impact on daily life"
    confidence: "high"
    inference_notes: "What was inferred vs directly stated"
  taxonomy_gap: ~
  human_review_required: false
  created_at: "2026-06-26T..."
```

### Defaults for official sources

| Field | Default | Override when |
|-------|---------|---------------|
| topics | `["general_government"]` | Content maps to a specific topic |
| communities | `[]` (countywide) | Item names a specific community |
| geographic_scope | `county_wide` | Item references specific location |
| urgency | `ongoing` | Item has deadline or active impact |
| verification_status | `source_confirmed` | Source is official government site |
| sensitivity | `low` | Item involves safety/legal/minors |
| human_review_required | `false` | Crime, minors, emergency, named individuals, controversy |

### Mandatory human-review triggers
Set `human_review_required: true` for any item involving:
- Crime, arrest, suspect, or victim
- Minors
- Active emergency or safety incident
- Unresolved allegations or ongoing investigation
- Controversial public policy
- Named individuals (unless elected/appointed officials in official capacity)
- School-safety incidents

---

## Dedupe Rules

### Within-month dedupe (applies per month, by worker)
1. **Normalized URL** — trailing-slash-insensitive, protocol-insensitive
2. **source_id + title + date** — fallback when URL differs
3. **Cross-source duplicates** — same fact from multiple sources → one canonical item with `supporting_sources`

### Cross-month dedupe (applies after Workers 1-3, checked by Worker 4)
- If the same budget rate, rezoning decision, or storm event appears in both Aug and Sep:
  - Keep the item in the month of the primary event date
  - In the secondary month, add a cross-reference note
  - Do NOT duplicate the full item
- Track cross-month items in the crosscut synthesis note

### ID format
- Aug: `SJC-BF-202508-{NNNN}` (zero-padded sequential)
- Sep: `SJC-BF-202509-{NNNN}` (zero-padded sequential, reset numbering)
- Cross-month IDs (if needed): `SJC-BF-20250809-{NNNN}`

### Do not update prior_items.yaml
Backfill items should NOT affect live monitor dedupe unless Buddy explicitly requests it.

---

## Archive.org Fallback Procedure

When a source URL returns 404, redirects, or is unreachable:

1. **Try archive.org with month-scoped URL:**
   ```
   https://web.archive.org/web/202508*/{original_url}
   ```
2. **Try broad archive search for the source domain:**
   ```
   https://web.archive.org/web/*/{source_domain}/*
   ```
3. **Try Google cache:**
   ```
   http://webcache.googleusercontent.com/search?q=cache:{original_url}
   ```
4. **If all fail:** Record in `source_gaps.md` as a dead link. Do not fabricate.

---

## Sensitivity / Privacy Rules

1. **Public sources only.** No login-gated content, private Facebook groups, HOA portals, paywalled full articles.
2. **No fake accounts or impersonation.**
3. **Do not publish anything.** All outputs are internal.
4. **Store minimal personal information.** Prefer parcel IDs, agenda item numbers, permit numbers, CDD names, and official document URLs.
5. **Named individuals** acceptable only when the original source names them publicly.
6. **Local media items** are context/tips only. Set `verification_status: unverified` unless the claim is a direct quote from an official record.
7. **Boil water notices, evacuation orders, active emergencies:** flag `urgency: urgent`, `sensitivity: high`, and `human_review_required: true`.
8. **Do not copy full article text.** `raw_excerpt` = first paragraph or key sentence only.
9. **No speculation beyond reasonable resident-interest inference.** Label inference in `inference_notes`.

---

## Completion Criteria

For each month (2025-08 and 2025-09):

- [ ] All official source stacks in the dispatch plan were attempted
- [ ] `discovered_items.yaml` exists with all extracted items
- [ ] `topic_clusters.yaml` exists (or note explaining no clusters met minimum size)
- [ ] `source_gaps.md` exists (or explicit "no gaps found")
- [ ] `monthly_wrap.md` exists with all required sections
- [ ] All items have required schema fields
- [ ] Sensitive items have `human_review_required: true`
- [ ] No items use unsanctioned taxonomy values
- [ ] No publishing, scheduling, or live monitor run occurred

Cross-month:
- [ ] If items span both months, `aug_sep_2025_crosscut.md` exists

---

## Block Conditions

| Condition | Action |
|-----------|--------|
| Cannot access any source (network/down) | Report specific failures; block if >50% of sources unreachable |
| Schema ambiguity that could produce invalid YAML | Flag for architect |
| Discovery of private/gated content referenced publicly | Flag for architect; do not extract |
| Progress won't complete in remaining budget | Flag remaining items; deliver partial output with block notice |

## Partial completion

If some sources produced items but others failed:
- Write complete output for what was found
- Report failures in `source_gaps.md`
- Complete with warnings, not errors
- Do not omit items because the "important" source failed — deliver what you have

## Reference Paths (from repo root)

| Resource | Path |
|----------|------|
| Source registry | `registry/sources.yaml` |
| Candidate sources | `registry/source_candidates.yaml` |
| Search terms | `registry/search_terms.yaml` |
| Taxonomy | `docs/taxonomy.md` |
| RI classification | `docs/resident_interest_classification.md` |
| RI classification prompt | `prompts/resident_interest_classification_task.md` |
| Intel item schema | `schemas/intel_item.schema.yaml` |
| Discovery loops | `docs/discovery_loops.md` |
| Backfill plan (previous) | `docs/backfill/aug_sep_2025_backfill_plan.md` |
| May 2026 template | `prompts/hermes_may_2026_backfill_task.md` |
| Communities | `registry/communities.yaml` |
| Beat candidates | `registry/beat_candidates.yaml` |

---

*End of Hermes execution template. Do not execute without explicit instruction from Buddy.*
