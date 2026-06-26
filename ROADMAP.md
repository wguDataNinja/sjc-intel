# SJC_Intel Roadmap

Last updated: 2026-06-03

## Current Phase

**Monitor pilots and cadence operations. Tier 1+2 sources promoted, backfill complete, daily-ready monitors running.**

All 24 canonical sources are registered. May 2026 backfill is complete (21 items).
Monitor specs exist for all priority sources. `sjc_utility_department` is the
first daily-ready Hermes monitor. Cadence system is operational. Source-discovery
agent is defined. Remaining work is running the queued pilots, resolving blocked
items, and eventually building the editorial/review pipeline.

## Phase Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Repo foundation, schemas, first pilots | Complete |
| 1 | Discovery loops, Deep Research intake, candidate registries | Complete |
| 2 | Operator readiness: backlog, checklists, agent instructions, May plan | Complete |
| 3 | Source promotion review and monitor design for official stacks | Complete |
| 4 | May 2026 backfill pilot | Complete |
| 5 | Hermes workflow/task definitions | Partially complete (contracts exist, runtime needed) |
| 6 | Editorial/review pipeline | Planned |
| 7 | Publishing/newsletter | Future; out of current scope |

## Next Milestones

1. Run recurring daily monitor cycles (utility, county news, sheriff).
2. Run NBOR app extraction pilot (road closures + meetings + permits).
3. Run BCC calendar pre/post meeting pilot with agenda PDFs.
4. Evaluate and promote `budget_millage` taxonomy gap (TAX-004).
5. Plan and execute Aug-Sep 2025 historical backfill (TRIM/budget/school).
6. Design editorial review queue (ED-001) before any publishing work.

## Operator Mode Readiness Criteria

Current verdict: **ready for supervised operator mode** — cadence system operational,
daily-ready monitors exist, Hermes contracts drafted, backfill complete.

Ready when:

- `STATE.md`, `BACKLOG.md`, `CHECKLIST.md`, and `docs/operator_mode.md` are current. ✅
- The architect can choose a next task without Buddy re-explaining context. ✅
- All live monitoring/backfill runs remain opt-in and explicit. ✅
- Source promotions are gated by Buddy approval. ✅
- Logs and memory are concise and point to durable artifacts. ✅
- Cadence system with LAST_RUN markers is operational. ✅

Not yet ready for autonomous scheduled operation (no cron/launchd by design).

## Out Of Scope

- Publishing or newsletter launch.
- Cron, launchd, or scheduled automation.
- Private Facebook/private forum scraping.
- Login-gated HOA or resident portals.
- Broad regional expansion beyond St. Johns County and relevant adjacent
  spillover sources.
