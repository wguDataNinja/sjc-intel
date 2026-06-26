# Hermes Task: Promotion Review

**Worker:** `hermes-promotion-reviewer`  
**Task:** `tier-1-2-promotion-review-2026-06-03`  
**Dependency:** Tier 1 and Tier 2 promotions complete

## Scope

Review Tier 1 and Tier 2 promotions for correctness, scope compliance, schema
validity, and data integrity. Report findings.

## Inputs

- `docs/source_promotion/first_wave_source_promotion_packet.md`
- `registry/sources.yaml` (post-Tier-1-and-2)
- `registry/source_candidates.yaml` (post-Tier-1-and-2)
- `logs/agents/hermes/2026-06-03_tier_1_promotion.md`
- `logs/agents/hermes/2026-06-03_tier_2_promotion.md`

## Review Checks

1. **Count check:** 15 sources should be promoted (10 Tier 1 + 5 Tier 2).
2. **Scope check:** Verify no Tier 3, Tier 4, or media sources were promoted.
3. **Canonical integrity:** St. Johns Citizen (`st_johns_citizen`) remains
   canonical and unmodified.
4. **Candidate update:** Each promoted source has a corresponding candidate
   record with `promotion_decision: promoted`.
5. **Schema compliance:** Every new source record has required fields.
6. **YAML validity:** Both files parse as valid YAML.
7. **Uniqueness:** No duplicate `source_id` values.
8. **Manual review:** Note any remaining manual-review items.

## Output

Write `docs/source_promotion/2026-06-03_tier_1_2_promotion_review.md` with:
- Pass/fail per check
- Source ID list (promoted)
- Source ID list (should NOT have been promoted — verify empty)
- Any issues found
- Overall verdict
