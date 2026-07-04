# Aug-Sep 2025 Historical Backfill Plan

Status: planned only  
Do not run without explicit instruction from Buddy.

## Window

- Start date: 2025-08-01
- End date: 2025-09-30
- Output month keys: `2025-08`, `2025-09`

## Why This Period

Deep Research identified Aug-Sep 2025 as high-value for three intersecting reasons:

1. **TRIM (Truth in Millage) season** — Property tax notices are mailed in August, and budget hearings / millage-rate adoption happens in September. SJC FY2026 budget adoption typically occurs in September. This window provides the baseline for year-over-year tax rate comparisons.

2. **School rezoning** — The St. Johns County School District typically announces attendance boundary changes over the summer for fall implementation. Aug-Sep captures both the final adoption decisions and the community reaction as families adjust before the school year starts.

3. **Hurricane season peak** — August and September are the peak of Atlantic hurricane season. This window may include emergency-management activations, storm prep guidance, and any storm impacts.

This supersedes any earlier plan to backfill Aug-Sep 2025 later; the three factors together make this the highest-priority window after the May 2026 baseline.

## Expected Outputs

- `data/monthly/2025-08/discovered_items.yaml`
- `data/monthly/2025-08/topic_clusters.yaml`
- `data/monthly/2025-08/source_gaps.md`
- `data/monthly/2025-08/monthly_wrap.md`
- `data/monthly/2025-09/discovered_items.yaml`
- `data/monthly/2025-09/topic_clusters.yaml`
- `data/monthly/2025-09/source_gaps.md`
- `data/monthly/2025-09/monthly_wrap.md`

A single cross-month synthesis note (`aug_sep_2025_crosscut.md`) capturing TRIM rate comparisons, rezoning decisions, and budget outcomes that span the two months — *only if* the individual monthly outputs justify it and Buddy explicitly requests it.

## Source Stacks To Check

### Official — Must Check (prioritized)

1. **County Commission / Clerk / GovTV stack** — BCC agendas and minutes for Aug-Sep 2025; TRIM notice approval, FY2026 budget ordinances, millage rate resolutions, public hearings on the budget
2. **Property Appraiser / Tax Collector** — TRIM notice verification, proposed vs. rolled-back rates, property value assessments, tax rate comparison tables
3. **SJCSD / BoardDocs / school board** — School board agendas and minutes; attendance boundary changes, rezoning votes, school start date adjustments, new school openings, capacity reports
4. **Planning and Zoning / Growth Management** — Development approvals during the window; comprehensive plan amendments; zoning changes
5. **Development Tracker and GIS Hub** — Notable project applications, site-plan approvals, DRI amendments
6. **County utility / water conservation / boil notices** — Utility rate changes tied to budget; watering restrictions (Aug is typically dry); boil-water notices
7. **Sheriff / Emergency Management / NWS Jacksonville** — Hurricane season activity; severe weather reports; crime trends; back-to-school safety messaging
8. **County roads / traffic / featured projects** — Road projects starting or completing in the window; school-zone traffic changes
9. **Permit status and public permit search** — Notable building permits (new schools, large developments)

### Context and Tip-Surfing

- St. Johns Citizen — school rezoning coverage, budget commentary, TRIM explainers
- Jacksonville Daily Record — development deals, county finance, school board reporting
- Ponte Vedra Recorder — PV-specific rezoning and development impacts
- Local TV stack (Action News Jax, News4Jax, First Coast News) — storm tracking, county commission coverage
- Chamber calendar — economic development events, State of the County
- Community/developer pages and public CDD sites — CDD budget hearings (typically late summer)

## Search Strategy

### Phase 1 — Budget / Millage (highest priority)

Search terms derived from `registry/search_terms.yaml`:

| Category | Target Terms |
|---|---|
| Budget/millage | TRIM notice, millage rate, proposed budget, FY2026 budget, tax rate, rolled-back rate, truth in millage, public hearing budget |
| Property tax | property assessment, taxable value, tax notice, tax referendum |
| County finance | county budget adoption, budget workshop, capital improvement plan |

### Phase 2 — School Rezoning

| Category | Target Terms |
|---|---|
| Attendance boundaries | rezoning, boundary change, attendance zone, school assignment, student reassignment |
| School operations | first day of school, school start date, new school opening, school capacity, overcrowding |
| School board | school board meeting, boundary approval, rezoning vote |

### Phase 3 — Hurricane / Emergency

| Category | Target Terms |
|---|---|
| Storms | tropical storm, hurricane, NWS advisory, storm prep, emergency declaration |
| Safety | boil water notice, shelter opening, evacuation, emergency operations center |

### Phase 4 — Development / Government

| Category | Target Terms |
|---|---|
| Development | site plan approval, comprehensive plan amendment, DRI, PUD, development order |
| County commission | BCC agenda, county commission resolution, public hearing, land use change |

## Extraction Approach

1. **Search official stacks first** — start with SJC BCC agendas/minutes, Property Appraiser millage tables, and SJCSD BoardDocs for the Aug-Sep window.
2. **Harvest all TRIM/budget items** — proposed rates, final adopted rates, public hearing dates, and key budget line items.
3. **Capture school boundary decisions** — map of before/after attendance zones, effective date, number of affected students.
4. **Scan for hurricane/storm activity** — any NWS advisories, EOC activations, or storm impacts.
5. **Collect development approvals** — notable projects approved during the window.
6. **Cross-reference with local media** — use St. Johns Citizen, Jacksonville Daily Record, and Ponte Vedra Recorder for context, quotes, and community reaction.
7. **Dedupe within each month** by normalized URL; cross-source duplicates become one canonical item with `supporting_sources`.
8. **Classify every item** with factual fields and resident-interest fields per taxonomy and RI rules.

## Classification Requirements

Every discovered item must include:

- source URL and source type
- title or concise label
- date observed and event/publication date when available
- topics from `docs/taxonomy.md`
- communities from `registry/communities.yaml`
- geographic scope
- urgency
- sensitivity
- verification status
- review status
- taxonomy_gap when existing vocabulary is insufficient

## Resident-Interest Requirements

Use the resident-interest classifier rules for:

- primary topic
- interest tags
- affected audiences
- resident relevance level
- plain-language why-it-matters note
- human_review_required

Treat public-safety, crime, legal, school-safety, and controversy items as human-review-required.

## Dedupe And Index Handling

- Do not update `data/index/prior_items.yaml` during exploratory backfill unless Buddy explicitly wants backfill items to affect live monitor dedupe.
- Within each monthly `discovered_items.yaml`, dedupe by normalized URL first, then by source/date/title.
- Keep cross-source duplicates as one canonical item with `supporting_sources` when the same fact appears in multiple places.
- Store source IDs when canonical; use `web_discovery` or `source_candidate` when not yet canonical.

## Sensitivity Rules

- Official records can be `source_confirmed`, but publication still requires review.
- Local media can surface tips/context; consequential claims need official confirmation.
- Private Facebook groups, private forums, login-gated HOA/resident portals, private screenshots, and forwarded texts are out of scope.
- Store minimal personal information. Prefer parcel IDs, agenda item numbers, permit numbers, CDD names, and official document URLs.

## Publishable Vs Exploratory

Publishable requires:

- public source URL
- factual claim traceable to source
- no unresolved sensitive-claim ambiguity
- human review for sensitive or consequential items
- clear resident relevance

Exploratory includes:

- source-discovery leads
- search results needing confirmation
- local-media-only claims not confirmed by official records
- taxonomy/source gaps
- monthly clustering observations

Do not publish the monthly wraps. These are internal baselines until editorial review and corrections workflow exist.

## Known Risks / Challenges

1. **TRIM notice URL churn** — Property Appraiser pages may have moved or been reorganized since Aug-Sep 2025. Archive.org or cached versions may be needed.
2. **School board agendas — seasonal structure** — Aug-Sep agendas are typically heavy on start-of-year operational items. Rezoning votes may appear in July or late Spring instead, and Aug-Sep may only capture implementation. Check June-July 2025 board meetings for the actual boundary votes.
3. **Hurricane-dependent volume** — If no named storms threatened N Florida in Aug-Sep 2025, emergency-management content will be minimal. This is fine; record the absence.
4. **Two-month scope is larger than May 2026** — Budget season generates substantial material. Volume could be 2-3x a typical single-month backfill. Plan for a longer extraction pass.
5. **CDD budget schedules** — Many CDD budgets are set earlier in the year. Aug-Sep may only contain rate implementation, not the policy debate.
6. **School calendar changes** — If the school board approved a new academic calendar, that decision may have happened in Spring 2025, not Aug-Sep. Check for references but don't expect the primary decision in this window.
7. **Source gap risk** — Some BCC agenda items from Aug-Sep 2025 may only exist as PDF links that have since been moved or deleted. Record broken-link gaps in `source_gaps.md`.

## Timeline Estimate

| Step | Estimated Effort |
|---|---|
| Phase 1: Budget/millage extraction (official) | 1-2 hours |
| Phase 2: School rezoning extraction (official) | 1-2 hours |
| Phase 3: Hurricane/emergency scan | 30 min |
| Phase 4: Development approvals | 30-60 min |
| Phase 5: Local media cross-reference | 1 hour |
| Phase 6: Classification and dedupe | 1-2 hours |
| Phase 7: Topic clustering and gap analysis | 30-60 min |
| Phase 8: Monthly wrap writing | 30 min per month |
| **Total** | **~6-10 hours** |

## Hermes Task Template

The execution-ready task template is at `prompts/hermes_aug_sep_2025_backfill_task.md`.
Do NOT execute from this plan doc — use the template. Requires explicit instruction from Buddy.

The task template includes:
- 4 dispatches (Budget/Millage, School Rezoning, Emergency/Development, Media Cross-Ref)
- Concrete search queries with date restrictions
- Source-specific check URLs with archive.org fallbacks
- Full output schema (discovered_items.yaml, topic_clusters.yaml, source_gaps.md, monthly_wrap.md)
- Cross-month dedupe rules for items spanning both August and September
- Completion criteria and block conditions
