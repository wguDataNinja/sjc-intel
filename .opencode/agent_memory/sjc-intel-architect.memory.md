# sjc-intel-architect Memory

Last updated: 2026-08-06

## Current State

- Phase: supervised, file-first local intelligence workflow with a static
  SilverLeaf Brief MVP; no scheduler, deployment, or autonomous publication.
- Current operational handoff: `README_INTERNAL.md` → `CURRENT_BRIEF.md` →
  `docs/live_adaptive_operations.md` / `docs/human_review.md`.
- Adaptive governance authority is versioned in `data/adaptive_discovery/`;
  raw live runs and receipts remain transient in `runtime/adaptive_discovery/`.
- `CURRENT_BRIEF.md`: pipeline HEALTHY; operator/overall NEEDS_REVIEW because
  22 adaptive proposals are pending. No accepted adaptive records currently.

## Weekly Hermes Path

- Entry point: `docs/hermes_weekly_entrypoint.md`; worker prompt:
  `prompts/sjc_weekly_ops_task.md`; task declaration:
  `deploy/sjc-weekly-task.yaml` (`enabled: false`).
- Initial weekly runner supports NBOR public notices and SJSO RSS. It writes an
  isolated bundle only; human review/import owns corpus transitions.
- Offline two-source simulation passed 2026-08-06: 27 candidates and verified
  manifest/checksums. Do not enable a timer without explicit gate approval.

## Evidence and Website

- Historical replay: `data/backtests/task22_replay/` spans 66 weekly windows;
  final evaluation reports zero leakage violations. It is deterministic fixture
  validation, not a claim of historical search-rank replay.
- Static site: `site/` is generated from reviewed release
  `SJC-REL-2026-08-001` (4 items, 13 routes). No host/deployment target chosen.

## Active Blockers / Next Action

- Human review of 22 adaptive proposals in small evidence-backed groups;
  strongest entity/search/timeline proposals first.
- Scheduler, live weekly Hermes execution, source promotion, publication, and
  deployment all require explicit Buddy approval.
- Keep docs coherent: generic source-monitor tasks must state whether they are
  direct-supervised or weekly-bundle mode.

## Latest Logs

- `logs/agents/sjc-intel-architect/2026-08-06_adaptive_governance_durability.md`
- `logs/agents/sjc-intel-architect/2026-08-06_operational_readiness_audit.md`
