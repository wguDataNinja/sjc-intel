# SJC_Intel Roadmap

**Status:** Current repository roadmap.
**Owner:** Buddy.
**Last reconciled:** 2026-07-28.

## Purpose

`sjc_intel` is an AI-assisted local intelligence and reporting repository for
St. Johns County, Florida. It discovers, monitors, classifies, verifies, and
organizes public-source information for homeowner/resident review.

The repository produces structured intelligence and review queues. It does not
authorize public publishing, private-source access, scheduled automation, source
promotion, or sensitive-claim publication without Buddy review.

## Current Verified State

- The local Git branch is `master`; no remote is configured.
- The repository operates in supervised operator mode: no cron, launchd, or
  scheduled automation.
- Canonical source, candidate source, review queue, monitor, and prompt
  infrastructure already exist.
- `README_INTERNAL.md` remains the detailed development entrypoint.
- `BACKLOG.md` is the executable near-term work queue.
- Curated project data under `data/` and logs under `logs/` may be committed
  when reviewed; secrets, raw transcripts, credentials, and large dumps may not.
- Untracked July 2026 SilverLeaf/search-discovery artifacts exist locally and
  require validation before they become durable repository state.

## Completed Foundations

- Public-source-only operating boundary.
- Monitor specs for utility, NBOR, school, BCC, and related sources.
- Review queue, dedupe index, resident-interest classification, and source
  promotion workflow.
- Prompt-led Hermes task contracts for bounded worker execution.
- PostgreSQL adapter, storage adapter, retention dry-run, snapshot, metrics, and
  portability references.
- Product direction: first public product candidate is SilverLeaf neighborhood
  intelligence.

## Current Phase

Repository readiness for Hermes read-only orchestration and supervised operator
work.

Normal operation is still human-supervised. Hermes may inspect, validate, and
prepare bounded task packets, but live monitor runs, backfills, publishing, and
source promotion remain explicit Buddy gates.

## Next Bounded Milestones

1. Validate and either commit or disposition the July 2026 SilverLeaf/search
   discovery artifacts.
2. Reconcile `BACKLOG.md` with the current roadmap and mark stale completed
   items historical where appropriate.
3. Confirm validation commands remain green on a clean checkout.
4. Decide whether the repository should gain an origin remote and tracking
   branch.
5. Create a Hermes control record only after Buddy confirms the desired Hermes
   scope.

## Dependencies

- Buddy decision on remote strategy and publication boundaries.
- Buddy review before any public product, newsletter, or website output.
- Official-record source verification for consequential claims.
- Human review for sensitive, legal, public-safety, school-safety, crime, or
  controversy items.

## Stop Gates

- Do not publish.
- Do not access private Facebook groups, login-gated portals, or non-public
  sources.
- Do not run live monitors, backfills, cron, launchd, or scheduled automation
  without explicit approval.
- Do not promote sources or taxonomy changes without review.
- Do not treat local media as sole authority for consequential claims.
- Do not push until remote/tracking strategy is explicitly approved.

## Validation Expectations

Run offline validation before committing source, schema, or curated data changes:

```bash
python3 -m pytest tests/ -q
python3 scripts/validate.py
git status --short --branch
```

Structured YAML/JSON changes must also be parsed or covered by the validation
suite before commit.

## VPS Relevance

The repository has future VPS relevance for PostgreSQL-backed storage,
retention, metrics, and possibly scheduled or operator-triggered collection.
No VPS deployment or scheduler is currently authorized.

## Deferred Work

- Public product naming and launch flow.
- Newsletter or website pipeline.
- Live incident lane.
- Coordinate-based geographic filtering and PostGIS integration.
- External traffic API evaluation.

## Human Decisions

- Whether and where to publish the repository.
- Whether to add a remote and tracking branch.
- Whether Hermes should operate read-only, prepare task packets, or execute
  bounded repository work.
- Whether the July 2026 SilverLeaf/search-discovery artifacts are accepted as
  curated durable repository state.
