# Agent Log — 2026-08-04 publication-foundation-and-ui-discovery (Task 16)

## Session

`sjc-intel-architect` executed `tasks/16-publication-foundation-and-ui-discovery.md`.
Medium-strength implementation + discovery. SJC code/docs/data approved
changes only. Ivy read-only. Portfolio-site repo not discoverable — context
packet requested in report §22. No publication/review decision, no item
approved, no VPS/PostgreSQL/systemd/Hermes/Ivy mutation, no commit/push.

## Files read (SJC)

README, README_INTERNAL, AGENTS, ROADMAP, BACKLOG, VPS_ROADMAP, VPS_CONTINUITY,
ARCHITECTURE, publication_release_contract, weekly_operational_contract,
weekly_operator_guide, weekly_scheduling, backup-restore, retention,
postgresql_adapter, data_model, taxonomy, planning/* (product direction,
scope packet refs), tasks/README, reports/README, reports 08–15 (full 08, 09,
10, 11, 12, 13, 14, 15), registry (sources, communities, tracked_entities),
schemas (intel_item), scripts (validate, build_review_queue,
batch_review_queue), tests/conftest, data inventory + review queue summary,
full corpus scan (192 records, 167 unique IDs, 25 NBOR duplicate captures,
9 legacy CDD records, 5 missing created_at, 46 missing dedupe).

## Files read (Ivy, read-only)

README, docs/README (doc classification), REPOSITORY_CONTROL_MODEL,
VPS_ADMISSION_CHECKLIST, VPS_INVENTORY, DATABASE, PORTFOLIO_CONVENTIONS,
PORTFOLIO_INTENT, PORTFOLIO_UNIVERSE, DATA_LIFECYCLE_STANDARD,
BACKUP_MANIFEST_STANDARD, HEALTH_CONTRACT (referenced), agents/VPS_ORCHESTRATION
(referenced), repos/sjc-intel/CONTROL.md, repos/reckless-ben/CONTROL.md,
orchestration archive (sjc-intel), outbox runs (2026-08-02-sjc-rb-resume,
2026-08-03-sjc-codex-followup), git log/status/diff. Portfolio-site repo not
discoverable from SJC or Ivy authority — `Portfolio/` is job-search positioning
(not a website), `projects_portfolio/` is an empty shell.

## Implementation delivered

- `scripts/publication_common.py` — shared decision/validation/selector helpers,
  public projection allowlist + internal denylist.
- `scripts/publication_decision.py` — human operator tool (approve/reject/defer/
  withdraw), transitions, audit history, idempotency, dry-run, never publishes.
- `scripts/select_publication_items.py` — deterministic selector, `--check`
  no-mutation, window config, 9 exclusion gates.
- `scripts/validate_publication_corpus.py` — per-record corpus validator,
  machine + human summary, legacy exception handling, exit code contract.
- `data/publication_decisions/` — decision registry + `legacy_exceptions.yaml`
  (4 exceptions: NBOR dup, CDD legacy, missing created_at, rural_sjc ref).
- `schemas/publication_decision.schema.yaml`; `docs/public_ui_v0_spec.md`;
  `docs/static_release_data_contract.md`;
  `docs/planning/SILVERLEAF_SCOPE_DECISION_PACKET_20260804.md`.
- `tests/test_publication.py` (21 tests) + real-shaped fixtures.
- `scripts/validate.py` — added §8 publication-decision checks.
- ROADMAP.md §3A-G2 status, §3D sequence, builder-task reference updated.

## Key findings

- Corpus: 0 blocking errors; 320 warnings (legacy). 83 unique verified items
  (BCC 40, NBOR 25, CN 8, UTIL 5, SJSO 4, EM 1); 54 reviewed release-eligible
  preview. No publication decisions exist → selector correctly selects 0.
- `rural_sjc` community referenced but not registered — flagged for registry
  fix; NBOR 06-08/06-26 duplicate capture documented as non-canonical.
- Portfolio-site repo NOT discoverable — exact context-gathering packet
  prepared for next agent.
- Ivy: CONTROL.md still stale (remote null, approved SHA 35a0246 vs local
  master 1be2ade), RELEASE_GATES.md absent; doc sprawl confirmed.

## Validation

`pytest` 161 passed (140 baseline + 21 new); `validate.py` ALL PASSED;
`validate_publication_corpus.py` PASS (0 errors); `portability_check.py` PASS;
`git diff --check` clean; Ivy read-only status/log/diff inspected, untouched.

## Decisions / friction

- NBOR M/D/YYYY meeting dates treated as documented legacy date format (warn,
  not block).
- Publication statuses follow operator vocabulary (approved/rejected/deferred/
  withdrawn); `published` reserved for release manifests.
- No item approved; no release generated; no publication decision made.
