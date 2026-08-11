# Task 33 — Production Workflow Hardening and Corpus Deepening

**Owner:** sjc-intel-architect
**Mode:** supervised
**Date:** 2026-08-09
**Report:** `reports/33-production-hardening-and-corpus-deepening.md`

## Mission

SJC_Intel is now a live product (Release `SJC-REL-2026-08-003`, 34 items,
Model B publication active, 66-week Hermes production backtest complete). The
next problem is whether the production workflow can reliably research, resolve,
classify, and surface resident-relevant information every week without
accumulating unresolved routine work. Task 33 answers that through
implementation.

## Objectives

1. Harden the weekly Hermes workflow.
2. Fix the generalized defects exposed by the 66-week backtest (acceptance
   asymmetry, evaluator matcher, entity/proposal dedupe, FDOT/FCE coverage,
   stale-milestone escalation, production/backtest prompt alignment).
3. Reconcile the production workflow with the proven backtest behavior.
4. Aggressively reduce the publication/research exception backlog through
   bounded evidence work.
5. Deepen the resident-relevant corpus.
6. Prepare the next public release candidate (`SJC-REL-2026-08-004`).
7. Leave SJC_Intel ready for its first normal supervised weekly production
   cycle.

## Boundaries

- Do NOT deploy, commit, push, or activate a scheduler.
- Do NOT promote sources, change taxonomy, or weaken human safety gates.
- Public sources only; official records are first authority for consequential
  claims; qualified uncertainty is preserved.

## Validation

`python3 -m pytest tests/ -q`; `python3 scripts/validate.py`;
`python3 scripts/validate_publication_corpus.py`;
`python3 scripts/validate_silverleaf_scope.py`;
`python3 scripts/validate_silverleaf_mobility.py`;
`python3 scripts/build_current_brief.py --check`;
`python3 scripts/build_publication_plan.py --check`;
`git diff --check`.

## Exit judgment

`READY_FOR_FIRST_SUPERVISED_WEEKLY_RUN` or `NOT_READY`, with evidence.
