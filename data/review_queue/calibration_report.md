# ED-001 Review Queue Calibration Report

**Date:** 2026-06-26  
**Session type:** Review calibration — 16 items reviewed across 6 sources

## Summary

| Metric | Value |
|--------|-------|
| Total queue entries | 99 |
| Reviewed this session | 16 |
| Statuses used | 4 (verified, archived, rejected_noise, pending_review) |
| Sources sampled | 6 (all) |
| Beats sampled | 8 |
| Escalation changes | Fixed — immediate went from 9 → 2 |

## Status Distribution After Review

| Status | Count | % |
|--------|-------|---|
| `pending_review` | 83 | 83.8% |
| `verified` | 14 | 14.1% |
| `archived` | 1 | 1.0% |
| `rejected_noise` | 1 | 1.0% |

## Canonical Review Statuses (Final)

| Status | When to Use |
|--------|-------------|
| `pending_review` | Default for all new items |
| `in_review` | Being reviewed |
| `verified` | Factually correct, classification confirmed |
| `needs_followup` | Requires additional verification |
| `rejected_noise` | Not resident-impactful; correctly classified as noise |
| `duplicate` | Same event already in queue under different ID |
| `escalated` | Flagged for priority human/architect review |
| `archived` | Historical reference, no action needed |

(Published statuses removed — internal-only; may be added in future publishing phase.)

## Escalation Logic Fixes

| Fix | Before | After | Rationale |
|-----|--------|-------|-----------|
| `human_review_required` | immediate | high | Crime reports need review but are not emergencies |
| `public_safety_livability` beat | immediate | high | Routine safety items (ambulance certs, fire apparatus) are not immediate |
| Active emergency keywords | Not checked | Checked | Boil water, evacuation, hazmat now detected |
| Immediate items | 9 | 2 | Only Phase III water shortage correctly immediate |

## Examples of Review Decisions

### Verified (14 items)
- **Phase III Water Shortage** — Active emergency. Correctly classified. Verified.
- **2050 Comprehensive Plan** — Major land-use policy. Verified.
- **Bargfrede Shed variance** — Zoning hearing. Correct classification. Verified.
- **Railroad crossing closure** — Active traffic impact. Verified.
- **Jail escape plot** — Human review confirms factual. Verified.

### Archived (1 item)
- **March 2026 DUI Wolfpack Operation** — 3+ months old. Archived.

### Rejected as Noise (1 item)
- **Recycling driver feel-good story** — Community interest, not resident-impact intel. Correct for noise rejection.

### Not Sampled (83 items remain pending)
- Most are NBOR ROW permits (utilities_water) and BCC consent agenda items — routine but resident-relevant.

## Escalation Calibration Results

| Level | Count | Appropriate? |
|-------|-------|-------------|
| immediate | 2 | ✅ Phase III water shortage |
| high | 63 | ✅ Rezonings, utilities, transportation, crime reports |
| normal | 7 | ✅ Medium-signal items |
| low | 27 | ✅ Archival, routine, ceremonial |

## Preservation Behavior

Confirmed: `build_review_queue.py` preserves `review_status`, `review_notes`, `reviewer`, and `reviewed_at` across rebuilds. 18 existing review states were preserved during the test rebuild.

## Recommendations for Future Reviewers

1. **Start with immediate items** (2 items, both already verified).
2. **Then high items** (63 items). Focus on human-review-required first (5 items, all already done).
3. **Use `verified`** for items where the source is official and classification is correct.
4. **Use `rejected_noise`** for items that are correctly extracted but have no resident impact.
5. **Use `archived`** for items older than 3 months with no ongoing relevance.
6. **Use `needs_followup`** when a source claim needs official confirmation.
7. **Use `duplicate`** when the same event appears under multiple source_ids.
8. **Rebuild the queue after each review session** — review decisions are preserved across rebuilds.

## Remaining Work

- 83 items still `pending_review`. At 16 per session, ~5 more sessions to clear.
- Utility ROW permits (Comcast, AT&T, JEA) are the largest single category (23 items). These are routine but resident-relevant — batch `verified` is appropriate once the classification is confirmed.
- BCC consent agenda items (resolutions for utility easements, donations) are the next largest (11 items). Review one batch to confirm pattern.
