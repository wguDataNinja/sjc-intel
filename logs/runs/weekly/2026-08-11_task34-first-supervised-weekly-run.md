# Weekly Run Log — 2026-08-11 (Task 34)

**Run IDs:** SJC-WK-20260811-0001 (Stage A) · SJC-LIVE-20260811-0001 (adaptive)
**Window:** 2026-08-07T06:34:00Z → 2026-08-11T10:00:00Z
**Pinned SHA:** ffa3ab2 (clean checkout verified)
**Mode:** supervised · **Status:** completed

## Stage A — known-source capture

| Source | Candidates | Duplicate | Failed | Health |
|---|---|---|---|---|
| sjc_nbor_public_notices | 25 | 0 | 0 | accessible |
| sjso_news_stories | 8 | 0 | 0 | accessible |

## Adaptive supervised cycle

- Findings: 47 · Evaluator-rejected: 18 · New pending proposals: 4
- All stages executed: known_source_capture, normalization, dedupe,
  identity_reconciliation, strategist, editor, evaluator, proposal_storage
- Proposals (all stale-milestone escalations):
  LIVE-95de8a8e1879 (Publix) · LIVE-67772ec07c67 (Baptist campus) ·
  LIVE-d149ebe299cd (FCE access) · LIVE-d52075d2692f (CR 2209 connector)

## Coverage health

- source_gaps: [] · missed_milestones: [] · stale: 4 (escalated SEARCH_NOW)
- no_yield_queries: 3 (CR 16A grocery, CR 2209 connector, Silverleaf Retail Marketplace)

## Outputs

- `runtime/weekly/SJC-WK-20260811-0001/` (ignored)
- `runtime/adaptive_discovery/runs/SJC-LIVE-20260811-0001/` (ignored)
- `data/adaptive_discovery/pending_proposals.yaml` (4 new)
- `CURRENT_BRIEF.md` + `reports/briefs/20260811T100258Z.md`
- `reports/34-first-supervised-weekly-run.md`

## Boundary

No import, acceptance, promotion, publication, or scheduler change. Human
review (Buddy) decides the 4 proposals.
