# SJC_Intel — Deep Research Ingestion Workflow

> How to ingest a ChatGPT Deep Research report into SJC_Intel's candidate
> registries and, after review, promote select findings into canonical
> sources, beats, search terms, and taxonomy.

---

## 1. Save Raw Report

**Location:** `docs/deep_research/reports/`

**Filename:** `{YYYY-MM-DD}_{topic}.md`

**Action:** Save the complete Deep Research output as a markdown file.
Do not edit, truncate, or summarize. The raw report is the source of
truth for evidence extraction.

**Owner:** Whoever receives the Deep Research output.

---

## 2. Extract Candidate Sources

**Target:** `registry/source_candidates.yaml`

**Action:** Read the report for any mention of websites, pages, or
channels that could be monitored. For each:

1. Create a candidate source record in `registry/source_candidates.yaml`.
2. Include the evidence from the report in `evidence_from_report`.
3. Set `review_status: pending_review`.

**Deduplication:** Before adding, check:
- `registry/sources.yaml` (canonical sources)
- `registry/source_candidates.yaml` (existing candidates)

**Conflict marking:** If the candidate overlaps with an existing source
or candidate, set `promotion_decision: duplicate` and note the overlap.

---

## 3. Extract Candidate Beats

**Target:** `registry/beat_candidates.yaml`

**Action:** Read the report for any recurring themes, topics, or
"beats" that cut across sources and communities. For each:

1. Create a candidate beat record in `registry/beat_candidates.yaml`.
2. Include example search terms from the report.
3. Map to related taxonomy terms where applicable.
4. Set `review_status: pending_review`.

**Deduplication:** Check existing candidate beats and any active beats
that may already be tracked. Mark conflicts.

---

## 4. Extract Search Terms

**Target:** `registry/search_terms.yaml`

**Action:** Read the report for specific search queries, search
strategies, or recommended terms. For each:

1. Add a search term record in the appropriate category section.
2. Set `effectiveness: untested`.
3. Note the source as `deep_research`.

**No deduplication needed** — search terms are operational and can
have multiple variations. Duplicates can be merged during review.

---

## 5. Deduplicate Against Canonical Registries

**Action:** For each candidate source and beat:

1. Compare with `registry/sources.yaml` (sources) and `docs/taxonomy.md`
   (taxonomy terms).
2. If the candidate already exists in canonical form:
   - Set `promotion_decision: rejected_duplicate`
   - Note which canonical record covers it.
3. If the candidate partially overlaps:
   - Set `promotion_decision: merged_into_existing`
   - Note what would need to be added to the canonical record.
4. If the candidate is genuinely new:
   - Leave `promotion_decision` empty for architect/Buddy review.

---

## 6. Mark Conflicts

**Action:** For each conflict found during deduplication:

1. Record the conflict in the candidate's `notes` field.
2. If the conflict is significant (e.g., the report recommends a source
   that conflicts with an existing canonical source), flag it for
   architect review.

---

## 7. Recommend Promotions

**Action:** For candidates that are genuinely new and relevant:

1. Draft a brief promotion recommendation in the candidate's `notes`.
2. For sources: what `source_id` would it get? What `monitor_config`
   would it need?
3. For beats: what would it take to start tracking this beat?
4. For search terms: how often should they be searched?

---

## 8. Require Approval

**Rules:**
- **Source promotions** require Buddy approval before any change to
  `registry/sources.yaml`.
- **Beat promotions** require sjc-intel-architect or Buddy approval.
- **Search term additions** can be made directly to
  `registry/search_terms.yaml` by any agent.
- **Taxonomy changes** require Buddy approval (per existing rules).

---

## 9. Promote Approved Candidates

Once approved:

| Candidate Type | Promotion Action |
|---------------|-----------------|
| Source | Add to `registry/sources.yaml` with `status: observed` |
| Beat | Add to active beat tracking (future: `registry/beats.yaml`) |
| Search term | Add to `registry/search_terms.yaml` with `effectiveness: untested` |
| Taxonomy | Update `docs/taxonomy.md` per taxonomy improvement loop |

After promotion:
- Update the candidate's `review_status: approved`
- Update the candidate's `promotion_decision` with the outcome
- Note the promotion in the intake review notes

---

## Ingestion Checklist

```
[ ] 1. Save raw report to docs/deep_research/reports/
[ ] 2. Extract candidate sources to registry/source_candidates.yaml
[ ] 3. Extract candidate beats to registry/beat_candidates.yaml
[ ] 4. Extract search terms to registry/search_terms.yaml
[ ] 5. Deduplicate against canonical registries
[ ] 6. Mark conflicts
[ ] 7. Recommend promotions
[ ] 8. Route for approval
[ ] 9. Promote approved candidates
[ ] 10. Update intake review notes
```

## Role Assignments

| Step | Role |
|------|------|
| 1. Save report | Anyone who receives Deep Research output |
| 2-4. Extract candidates | `search-discovery-worker` or `sjc-intel-architect` |
| 5-7. Dedupe, conflict, recommend | `sjc-intel-architect` |
| 8. Approve | Buddy (sources, taxonomy) or architect (beats, search terms) |
| 9. Promote | `sjc-intel-architect` |
