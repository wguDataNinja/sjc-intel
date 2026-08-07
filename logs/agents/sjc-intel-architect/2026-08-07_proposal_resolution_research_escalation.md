# Task 25 proposal resolution and research escalation

- Resolved all 22 pending adaptive proposals per the locked decision set:
  accepted 6 entities (including canonical "Publix at Silverleaf Market" and
  qualified "SilverLeaf grocery center — possible Harris Teeter"), 4 coverage
  lanes, 6 search profiles, and 2 timelines; deferred 4 incomplete timelines.
- Added 5 proposal edits that preserve the original and record why (Publix
  canonical name/aliases, Harris Teeter qualified subject/location/queries/
  timeline language).
- Performed bounded Harris Teeter public-source research: project exists and
  strongly matches a Harris Teeter prototype, but the tenant is unconfirmed by
  any first-party source. Persisted an ACCEPT_QUALIFIED research resolution.
- Built `scripts/research_escalation.py` + `research_adaptive_proposal.py` CLI +
  `schemas/research_resolution.schema.yaml`: identity/geographic/stale/
  conflicting trigger detection, bounded budgets (8 queries, 10 results),
  receipts, and recommended actions.
- Updated the Hermes weekly workflow (prompt + entrypoint + live ops doc) to
  run bounded research before human review for ambiguous proposals.
- Refreshed CURRENT_BRIEF with Decisions completed, Research findings, Remaining
  decisions, and Active search profiles sections; added Scheduler/Deployment
  status headers.
- Prepared `.github/workflows/pages.yml` (official Pages actions, uploads only
  `site/`, workflow_dispatch, minimum permissions, internal-leak guard).
- Tests: 300 passed; validate/corpus/scope/portability/brief-check all PASS.
- No publication, review-queue, release, scheduler, PostgreSQL, Ivy, deploy, or
  commit changes.
