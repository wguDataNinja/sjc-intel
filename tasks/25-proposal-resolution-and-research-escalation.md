# Task 25 — Resolve Adaptive Proposals, Add Research Escalation, and Refresh Current Brief

**Session:** OpenCode agent session working from `/Users/buddy/projects/sjc_intel`.
**Mode:** supervised-live-pilot. Resolve the current adaptive-discovery proposal
set and add bounded research escalation to the Hermes weekly workflow so
unclear, conflicting, stale, or weakly supported findings trigger follow-up
research before human review. Keep `CURRENT_BRIEF.md` the single current
operational document. Write the report to
`reports/25-proposal-resolution-and-research-escalation.md`.

## Locked human decisions (apply unless repository evidence contradicts)

### Accept entities
- `LIVE-ad9eee3e390e` Magnolia Oaks Academy
- `LIVE-b19cc8fc4ed7` Publix — canonical name **Publix at Silverleaf Market**,
  retain aliases SilverLeaf Mega Publix / Silverleaf Publix / Publix Silverleaf Market
- `LIVE-476ade9e84c0` Baptist SilverLeaf campus
- `LIVE-74cf426eb727` CR 2209 connector
- `LIVE-bab9fbe90d95` First Coast Expressway access

### Accept coverage lanes
- `LIVE-030b26e86bbf` schools and families
- `LIVE-6eef856c960b` roads and mobility
- `LIVE-fc3ae8103d4e` retail and amenities
- `LIVE-60f81408c018` healthcare and services

### Accept search profiles
- `LIVE-04b7748729e1` Magnolia Oaks Academy
- `LIVE-0f19a7c7afb8` Publix at Silverleaf Market
- `LIVE-9cff5aeb112e` Baptist SilverLeaf campus
- `LIVE-7d08478f8645` CR 2209 connector
- `LIVE-55b639933dba` First Coast Expressway access

### Accept timelines
- `LIVE-833d0d9beed7` Magnolia Oaks Academy (identity progression School QQ →
  SilverLeaf K-8 → Magnolia Oaks Academy → opening)

### Defer timelines (valid subject, insufficient milestone payload)
- `LIVE-0285b35d3662` Publix timeline
- `LIVE-05c5ea4073e1` Baptist campus timeline
- `LIVE-caf4c3d8e30e` CR 2209 connector timeline
- `LIVE-1f7b9d109de0` First Coast Expressway timeline

### Harris Teeter / SilverLeaf grocery project
Canonical subject: **SilverLeaf grocery center — possible Harris Teeter**;
location CR 16A and SilverLeaf Parkway. Tenant unconfirmed by first-party
source. Accept as a qualified tracked development with uncertain-safe timeline
language. Do not record "Harris Teeter confirmed".

## Research escalation (add to Hermes workflow)
Trigger bounded public-source research when: identity uncertainty, geographic
conflict, stale evidence, conflicting sources, or material resident importance.
Produce a research-resolution record (schema
`schemas/research_resolution.schema.yaml`) with confirmed facts, strong
inferences, conflicting evidence, unresolved questions, recommended canonical
name/aliases/state, and recommended action (`ACCEPT`, `ACCEPT_QUALIFIED`,
`DEFER`, `REJECT`, `RESEARCH_AGAIN`). Default budget: max 8 queries, 10 results,
official sources first. The strategist never evaluates its own research.

## Required work
1. Read authority docs and inspect proposal records.
2. Perform bounded Harris Teeter public-source research; record the
   determination.
3. Add proposal editing (preserve original, record reason, accept corrected).
4. Add research escalation module, schema, and CLI.
5. Execute all locked decisions one at a time (reviewer Buddy, precise
   rationales). Confirm decision history, accepted state, rollback, and
   CURRENT_BRIEF regeneration.
6. Update the Hermes weekly workflow (known-source → discovery → reconciliation
   → ambiguity detection → research escalation → strategist → evaluator → human
   review → CURRENT_BRIEF).
7. Add recurring searches for Magnolia Oaks Academy, Publix at Silverleaf
   Market, Baptist SilverLeaf campus, CR 2209, First Coast Expressway access,
   and the SilverLeaf grocery center.
8. Regenerate CURRENT_BRIEF with decisions completed, research findings,
   coverage health, active searches, remaining decisions, and next-run plan.
9. Prepare or verify a GitHub Pages workflow (official Pages actions; upload
   only `site/`; manual dispatch; minimum permissions; no internal material).
10. Add tests; run validation; write the report.

## Scope restrictions
No publication decisions, review-queue status, release changes, scheduler
activation, deployment, PostgreSQL, Ivy, private sources, secret exposure,
auto-acceptance, or competing current-status documents. No commit or push.
