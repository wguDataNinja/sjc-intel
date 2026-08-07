# Operational readiness audit

**Date:** 2026-08-06
**Scope:** Repository structure, operator path, weekly Hermes workflow, human
review, backtest/simulation evidence, and static website. No public sources,
publication, source promotion, scheduler, or deployment was run.

## Verdict

The repository has the required major pieces: a supervised intelligence
workflow, versioned adaptive governance, an offline-verifiable weekly bundle
runner, a deterministic historical replay, and a deployable static website.
It is ready for supervised weekly operation, not autonomous operation.

The principal operational risk was discoverability rather than missing code:
two weekly paths and their human gates were documented separately. This audit
adds explicit front doors and resolves the one direct-corpus-write ambiguity in
the generic monitor prompt.

## Project goal and authority

SJC_Intel turns public St. Johns County signals into source-linked,
resident-relevant intelligence. The first public product is SilverLeaf Brief.
Collection and adaptive discovery may surface candidates or proposals, but
humans decide tracking, corpus, source, and publication state.

Operator path:

```text
README_INTERNAL.md
  → CURRENT_BRIEF.md
  → human_review.md / live_adaptive_operations.md
  → weekly Hermes entry point (when a weekly bundle is authorized)
```

## Improvements completed

| Area | Finding | Improvement |
|---|---|---|
| Hermes entry | Weekly task files existed but no single first-read instruction | Added `docs/hermes_weekly_entrypoint.md` and linked it from the weekly worker prompt |
| Human review | Proposal, candidate, source, and publication decisions were spread across contracts | Added `docs/human_review.md` with decision boundaries, commands, and required checks |
| Worker safety | Generic monitor prompt implied direct corpus writes even when invoked by the weekly bundle prompt | Added explicit `direct_supervised` vs. `weekly_bundle` write modes |
| Governance references | Task 23 historical report still described runtime as authority | Added a follow-up correction; current authority remains the operational docs and `CURRENT_BRIEF.md` |
| Website discoverability | Static site existed but was not prominent in the internal entry point | Added a public-website section and core-doc link in `README_INTERNAL.md` |
| Agent state | Architect memory was materially stale | Replaced it with concise current operational state and gates |

## Verification performed

### Offline weekly-run simulation

Executed `SJC-WK-20260806-0001` using only repository fixtures:

- `sjc_nbor_public_notices`: 25 candidates
- `sjso_news_stories`: 2 candidates
- bundle verification: PASS (layout, manifest, checksums, replay identity,
  and candidate outcome labels)
- protected corpus/registry state: not written by the runner

Artifacts are intentionally transient under `runtime/weekly/` and
`runtime/weekly-bundles/`.

### Historical replay

Re-evaluated `data/backtests/task22_replay/`:

- 66-week deterministic fixture replay
- item/subject/resident-coverage recall: 1.0 against the declared fixture
  baseline
- precision proxy: 0.818
- leakage violations: 0
- known limitations are retained: sparse lane coverage, stale subjects, and
  seven overdue fixture milestones require human interpretation.

### Website

`python3 scripts/build_static_site.py --list-routes` passed:

- current reviewed release: `SJC-REL-2026-08-001`
- four reviewed items
- 13 generated static routes
- no public host selected or activated

## Remaining decisions and cautions

1. Review the 22 adaptive proposals in manageable groups before another live
   adaptive run; `CURRENT_BRIEF.md` is correctly `NEEDS_REVIEW`.
2. Do not enable `sjc-weekly-001`: the declaration is intentionally
   `enabled: false`, and scheduler gates remain unmet.
3. Select a static host only when deployment is explicitly authorized. The
   website is build-ready but not publicly hosted.
4. Treat the historical replay as a quality/control simulation, not proof of
   live-web recall or a substitute for human source review.
