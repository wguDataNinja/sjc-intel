# SJC_Intel Backlog

Last updated: 2026-06-26

Status values: `todo`, `in_progress`, `blocked`, `done`, `deferred`.

## Operator Readiness

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| OP-001 | Keep state/backlog/memory aligned | done | high | none | sjc-intel-architect | Maintain at each session end |
| OP-002 | Define operator mode docs | done | high | none | sjc-intel-architect | Use `docs/operator_mode.md` |
|| OP-003 | Define Hermes task contracts | done | high | source promotion review | sjc-intel-architect | Created docs/hermes_task_contract.md. Standardized worker prompt format, middle review format, output conventions, token discipline, session lifecycle. |
| OP-004 | Trim stale narrative memory | done | high | logs available | sjc-intel-architect | Keep memory concise |

## Deep Research Ingestion

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| DR-001 | Archive report and intake note | done | high | report received | sjc-intel-architect | None |
| DR-002 | Extract source candidates | done | high | report archived | sjc-intel-architect | Review promotions |
| DR-003 | Extract beat candidates | done | high | report archived | sjc-intel-architect | Use in May plan |
| DR-004 | Extract search terms | done | high | report archived | sjc-intel-architect | Log effectiveness after use |
|| DR-005 | Review extraction quality | done | medium | DR-002..004 | Buddy + architect | Ran Session 7. 8 flags found: 2 red (URL conflict fixed Session 8, 11 candidates stuck in pending_review), 3 yellow, 3 minor. |

## Source Promotion / Review

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| SRC-001 | Approve and execute first official-stack promotions | done | high | Buddy approval | Buddy + Hermes | Tier 1 (10) + Tier 2 (5) promoted 2026-06-03 |
|| SRC-002 | Resolve Property Appraiser URL conflict | done | medium | manual verification | sjc-intel-architect | Verified Session 8. sjcpa.gov is authoritative (HTTP 200). sjcpa.us redirects (301). Fixed sources.yaml. |
| SRC-003 | Replace stale Clerk placeholder | done | medium | manual verification | sjc-intel-architect | Clerk promoted as `sjc_clerk_online_research` from CAND-SRC-0014. Stale `sjcclerk.gov` placeholder remains commented-out but irrelevant. |
|| SRC-004 | Review CDD source candidates | done | high | source candidate extraction | sjc-intel-architect | All 3 CDDs reviewed Session 4. Ready for promotion. |
| SRC-005 | Review JDR as media/context source | deferred | medium | official stack first | sjc-intel-architect | Assess after core official sources |

## Known-Source Monitoring

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| MON-001 | Run SJC School District monitor pilot | done | high | explicit instruction | Hermes/architect | Pilot run 2026-06-03 — 2 new items, signal/noise filtering validated. Log: `logs/runs/weekly/2026-06-03_sjc_school_stack_pilot.md` |
| MON-002 | Design county roads daily monitor | done | high | source approval | sjc-intel-architect | Spec rewritten as `sjc_nbor_public_notices`. NBOR app: plain HTML, 25 records extracted, daily-ready. |
| MON-003 | Design utility/water daily monitor | done | high | source approval | sjc-intel-architect | Pilot passed. Spec updated with sidebar extraction. First daily-ready source. |
|| MON-006 | Run recurring daily utility monitor (sjc_utility_department) | done | high | MON-003 | Hermes/architect | Ran Session 5. 1 new item (Annual Report). Page otherwise unchanged. |
| MON-004 | Do not create cron/scheduled automation | deferred | high | Buddy approval required | sjc-intel-architect | Wait |
| MON-005 | Design BCC calendar weekly monitor (pre/post meeting) | done | high | backfill evidence | sjc-intel-architect | Pilot passed 2026-06-26. Source corrected to Clerk Board Records. 11 meetings extracted. PDF extraction deferred (no library). Extractor at `scripts/extract_bcc_agenda.py`. |
| MON-007 | Investigate NBOR application URL for road closures data | done | high | road closures investigation | sjc-intel-architect | URL found: https://webapp.sjcfl.us/webnews/NBRscreend.aspx — fully public, plain HTML, rich data source (road closures + hearings + permits) |
|| MON-008 | Run recurring daily NBOR monitor | done | high | MON-002 | Hermes/architect | Ran Session 2. 25 items extracted, dedupe 77, review queue 89. |

## Historical Backfill

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| BF-001 | Create May 2026 backfill plan | done | high | Deep Research | sjc-intel-architect | Use `docs/backfill/may_2026_backfill_plan.md` |
| BF-002 | Run May 2026 backfill | done | high | explicit instruction | Hermes/architect | Ran 2026-06-03 — 21 items, 4 clusters, 7 source gaps |
| BF-003 | Defer January 2026 backfill | deferred | medium | May baseline first | sjc-intel-architect | Revisit after May results |
| BF-004 | Plan Aug-Sep 2025 second pass | deferred | medium | May results | sjc-intel-architect | Scope budget/TRIM/school context |
||| BF-005 | Plan and run Aug-Sep 2025 backfill (TRIM/budget/school rezoning/emergency/dev/media cross-ref) | done | high | none | sjc-intel-architect | Executed 2026-06-26. 43 items (24 Aug + 19 Sep), 14 clusters, 8 source gaps identified. 4 workers dispatched: Budget/Millage (W1), School Rezoning (W2), Emergency/Development (W3), Media Cross-Ref/Clustering/Wrap (W4). Full output: data/monthly/2025-08/*, data/monthly/2025-09/*, data/monthly/aug_sep_2025_crosscut.md, prompts/hermes_aug_sep_2025_backfill_task.md. |

## Taxonomy / Beat Improvement

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| TAX-001 | Add source families and beat groups | done | high | Deep Research | sjc-intel-architect | Use as operational, not schema values |
|| TAX-002 | Evaluate `cdd_governance` taxonomy gap | done | high | CDD items (now available) | sjc-intel-architect | Promoted to canonical topic in taxonomy.md 2026-06-26. Beat group mapping and CAND-BEAT-0006 updated. |
| TAX-003 | Evaluate `water_restrictions` taxonomy gap | done | high | real items | sjc-intel-architect | Promoted to canonical topic in `docs/taxonomy.md` 2026-06-03 |
| TAX-004 | Evaluate `budget_millage` taxonomy gap | done | medium | real items | sjc-intel-architect | Promoted to canonical topic in `docs/taxonomy.md` 2026-06-26 |

## Resident-Interest Classification

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
|| RI-001 | Apply RI rules to future items | done | high | monitor/backfill run | resident-interest-classifier | Already applied in NBOR + utility extraction pipelines. No action needed. |
| RI-002 | Review May backfill RI friction | deferred | medium | BF-002 | sjc-intel-architect | Summarize issues after run |

## Hermes Workflows

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| HERMES-001 | Draft known-source monitor task template | done | high | operator docs | sjc-intel-architect | Created `prompts/known_source_monitor_task.md` |
| HERMES-002 | Draft May backfill task template | done | high | BF-001 | sjc-intel-architect | Created `prompts/hermes_may_2026_backfill_task.md`; executed via BF-002 |
| HERMES-003 | Draft search discovery task template | done | medium | search terms | sjc-intel-architect | Created `prompts/hermes_search_discovery_task.md` |

## Local-Media Discovery

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
|| MEDIA-001 | Run local-media discovery terms | done | medium | explicit instruction | search-discovery-worker | Ran Session 6. 8 candidates found. 3 terms should be retired. |
| MEDIA-002 | Competitive audit of St. Johns Citizen | deferred | low | higher priorities | sjc-intel-architect | Revisit before publishing strategy |

## Editorial / Review

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| ED-001 | Create editorial review queue design | done | medium | items flowing | sjc-intel-architect | Phase 1+2 implemented. Status model reconciled. 99 items, 16 reviewed in calibration. Immediate fixed 9→2. Rebuild preserves review state. |
| DATA-001 | Create data inventory and coverage tracking | done | medium | backfill data | data-inventory | Created `docs/data_inventory/` with coverage map, gaps, agent role |
| DATA-002 | Create homeowner perspective summary docs | done | medium | backfill data | data-inventory | Created `docs/homeowner_perspective/` with current themes |
|| DATA-003 | Run data inventory update after each backfill/monitor cycle | done | medium | DATA-001 | data-inventory | Updated COVERAGE.md + GAPS.md Session 10. June total 115. |
| SW-001 | Define sjc-intel-source-watch agent | done | high | none | sjc-intel-architect | Created `.opencode/agents/sjc-intel-source-watch.md` + memory |
|| SW-002 | Run first source-discovery cycle | done | high | SW-001 | sjc-intel-source-watch | Ran Session 3. 21/25 reachable, 10 new candidates, 2 overlap FLAG resolved. |
| ED-002 | Draft corrections policy | deferred | medium | publishing plan | Buddy + architect | Do before public launch |

## Tracked Entities / Stakeholder Interest

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| ENT-001 | Create tracked_entities.yaml registry and discovery workflow | todo | high | none | sjc-intel-architect | Design entity schema, create registry, seed with Silverleaf findings (Publix, K-8 school, Beach Valley Mini Golf, CR 2209, Harris Teeter, Ascension St. Vincent's), update discovery_loops.md with workflow docs |
| ENT-002 | Create `prompts/hermes_entity_search_task.md` | todo | high | ENT-001 | sjc-intel-architect | Hermes contract for running entity-directed search queries against tracked_entities.yaml |
| ENT-003 | Populate tracked_entities from Silverleaf discoveries | todo | high | ENT-001 | sjc-intel-architect | Add 6+ entities with search queries, source URLs, and status from July 4 discovery run |
| ENT-004 | Document stakeholder interest onboarding process | todo | medium | ENT-001 | sjc-intel-architect | Write docs/tracked_entities.md with workflow for "Buddy finds interesting thing → add to tracking → pipeline discovers updates" |

## Future Publishing / Newsletter

| ID | Title | Status | Priority | Dependencies | Owner/Agent | Next Action |
|----|-------|--------|----------|--------------|-------------|-------------|
| PUB-001 | Define public product name | deferred | low | editorial pipeline | Buddy | Decide later |
| PUB-002 | Build newsletter/website pipeline | deferred | low | review/corrections workflow | future | Not in current scope |
