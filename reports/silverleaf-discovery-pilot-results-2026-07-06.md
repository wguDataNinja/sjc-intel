# SilverLeaf Agentic Discovery — Pilot Results

**Run ID:** SRCH-20260706-0001
**Date:** 2026-07-06

---

## What happened

I ran the first manual pilot of the SilverLeaf recurring discovery prompt
(`prompts/agentic_silverleaf_discovery.md`), executing 3 of 7 enabled search
profiles via OpenCode `websearch`/`webfetch`.

## What was found

5 new candidate articles surfaced from St. Johns Citizen — all missed by
the existing deterministic pipeline:

| # | Title | Match | Sensitivity | Action |
|---|-------|-------|-------------|--------|
| 1 | Man charged in SilverLeaf murder case faces ICE detainer | probable | **HIGH** — crime, named individual, ICE | Verify URL, human review |
| 2 | Man Charged with Shooting Three at SilverLeaf Construction Site, Killing One | exact | **HIGH** — violent crime, fatality | Verify URL, human review |
| 3 | Suspected lightning strike zaps St. Augustine home in SilverLeaf | exact | low | Verify URL, promote if accurate |
| 4 | Officials give update on 6-year-old airlifted out of Silverleaf amenities center | exact | **HIGH** — minor, medical emergency | Verify URL, human review |
| 5 | St. Johns Pizza favorite Bala's close to opening second location in Silverleaf | exact | low | Verify URL, promote if accurate |

5 existing intel items were correctly identified as duplicates and excluded.

3 profiles returned `no_match` with valid explanations.

## What didn't work

- **Article page URLs timed out** — St. Johns Citizen appears to rate-limit
  direct fetches. Candidate titles and classifications came from the search
  results page, not the articles themselves.
- **Baptist Health SilverLeaf location** — baptistjax.com returned 404.
  Entity name is from the resident directory only — not yet confirmed by
  Baptist Health's own website.
- **"Silverleaf Market"** — no news results found under that name. The
  entity exists only in the resident directory; it may not be publicly
  referenced by that name.

## Where the output lives

| File | What |
|------|------|
| `data/search_runs/2026-07-06/SRCH-20260706-0001.yaml` | Full structured run record |
| `data/intel_items/2026-07-06/agentic_search_results.yaml` | 5 candidate records (all `pending_review`) |
| `logs/agents/sjc-intel-architect/2026-07-06_agentic_search.md` | Agent log |

Generated data is **not committed** — per repo rules.

## What you should do next

1. **Review the 5 candidates** — especially the 3 high-sensitivity items
   (crime, minor, named individual)
2. **Decide whether to open the ICE detainer + construction shooting URLs**
   manually to verify content before promoting
3. **Consider adjusting** `sl_baptist_medical` and `sl_market_publix` profiles
   — both returned no_match with valid explanations
