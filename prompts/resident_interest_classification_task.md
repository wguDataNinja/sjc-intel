# Resident Interest Classification Task

You are classifying a structured intel item from a St. Johns County,
Florida resident perspective. Your job is not to re-extract facts but
to identify **why local residents would care** about this information.

## Instructions

1. Read the intel item's `title`, `summary`, `raw_excerpt`, `topics`,
   `communities`, and `geographic_scope`.

2. Determine the **single primary topic** from the SJC_Intel taxonomy
   that best captures this item. Set `primary_topic`.

3. Add **interest tags** — these go beyond topical category to capture
   resident-interest dimensions (e.g., `traffic_impact`, `school_zones`,
   `public_safety_awareness`). See `docs/taxonomy.md` for allowed values.

4. Write a **resident_relevance.summary** — one or two sentences
   explaining why this matters to a St. Johns County resident.
   Use plain language. Avoid jargon.

5. Identify **affected_audiences** from the audience vocabulary.
   Be specific — if only commuters on CR 210 care, say
   `["commuters", "nearby_residents"]`, not just `["residents"]`.

6. Write **why_it_matters** — the concrete impact on daily life:
   traffic changes, safety concerns, cost impact, quality of life,
   school attendance boundaries, property values, etc.

7. Set **confidence**:
   - `high`: Impact is directly stated (e.g., "road closed until June").
   - `medium`: Impact is reasonably inferred (e.g., construction likely
     to cause delays, though not stated).
   - `low`: Impact is speculative or unclear.

8. Note what was inferred vs. directly stated in **inference_notes**.

9. If you need a tag that doesn't exist in the taxonomy, note it in
   `taxonomy_gap`. Do not add it to the canonical list.

10. Set `human_review_required` to `true` for any item involving:
    - Crime, arrest, suspect, or victim
    - Minors
    - Active emergency or safety incident
    - Unresolved allegations or ongoing investigation
    - Controversial public policy

## Classification Rules

- If affected community is unclear: leave communities empty (countywide).
- Sensitive items (crime, safety, legal): `human_review_required: true`.
- Public safety items: `recommended_channels: ["website_review_queue"]`
  unless clearly broad public-interest.
- Do not name private individuals unless essential and already public.
- Do not imply guilt beyond the official source.
- Use neutral, factual language — no sensationalism.

## Output Format

Return a YAML block with only the added fields:

```yaml
primary_topic: "topic_name"
interest_tags: ["tag1", "tag2"]
resident_relevance:
  summary: "Why this matters to residents"
  affected_audiences: ["audience1", "audience2"]
  why_it_matters: "Concrete impact description"
  confidence: "high|medium|low"
  inference_notes: "What was inferred vs. directly stated"
taxonomy_gap: ~  # or "proposed_tag_name"
human_review_required: true|false
```
