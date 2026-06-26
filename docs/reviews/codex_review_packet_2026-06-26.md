# Codex Review Packet — SJC_Intel

**Generated:** 2026-06-26  
**Status:** First buildout loop complete. All 99 queue items reviewed.

---

## 1. Project Purpose

SJC_Intel is an AI-assisted local intelligence/reporting system for St. Johns
County, Florida. It discovers, monitors, classifies, and organizes public
information about master-planned communities, government decisions, utilities,
schools, roads, and development. It produces structured intelligence items
for editorial review. It is **internal-only** — no publishing, no newsletter.

Operating mode: **supervised operator mode** — no cron/launchd/scheduled
automation. Buddy says "get to work", agent evaluates cadence, picks task,
executes, logs.

---

## 2. Current Architecture

### Sources: 24 canonical, 46 candidates

| Tier | Count | Status |
|------|-------|--------|
| Pre-existing (county, sheriff, schools, etc.) | 9 | Active |
| Tier 1 (official stacks: BCC, PZA, roads, utilities, etc.) | 10 | Active |
| Tier 2 (school, transportation, weather, elections) | 5 | Active |
| Tier 3 (CDD governance) | 4 candidates | Not promoted |
| Tier 4 (community/developer) | 6 candidates | Not promoted |
| Deferred | 13 | Lower priority |

### Monitor Lanes

| Lane | Cadence | Status | Items/Cycle |
|------|---------|--------|-------------|
| `sjc_nbor_public_notices` | Daily | ✅ Extractor ready | ~25 |
| `sjc_utility_department` | Daily | ✅ Pilot passed | ~0-3 |
| `sjc_county_news` | Daily | ✅ Pilot passed | ~4 |
| `sjso_news_stories` | Daily | ✅ Pilot passed | ~1-2 |
| `sjc_emergency_management` | Seasonal daily | ✅ Activated | ~1 |
| `sjc_bcc_calendar` | Weekly | ✅ Phase 2 complete | ~44 agenda items |
| `sjc_school_stack` | Weekly | ⬜ Spec ready, pilot done | ~2-10 |

### Cadence System

`docs/cadence.md` defines daily/weekly/monthly rhythms with LAST_RUN markers
at `logs/runs/{daily,weekly,monthly}/LAST_RUN`. Run-type rules distinguish
source-health pilots from extraction runs from failed runs.

---

## 3. Implemented Scripts (12)

| Script | Purpose |
|--------|---------|
| `scripts/extract_nbor.py` | NBOR public notices extractor (plain HTML, 25 records) |
| `scripts/extract_bcc_agenda.py` | BCC agenda PDF extractor (pypdf, 44 items per meeting) |
| `scripts/rebuild_dedupe_index.py` | Full dedupe index rebuild (idempotent) |
| `scripts/build_review_queue.py` | Review queue builder (idempotent, preserves review state) |
| `scripts/update_review_status.py` | Single-item review status updater |
| `scripts/batch_review_queue.py` | Rule-based batch review (17 rules) |

---

## 4. Data Assets Created

| Asset | Count |
|-------|-------|
| Intel items | 125 raw → 88 unique (after dedupe) |
| Review queue entries | 99 (all reviewed: 83 verified, 15 archived, 1 rejected) |
| Dedupe index | 88 unique keys |
| Backfill items (May 2026) | 21 items, 4 clusters, 7 source gaps |
| Monitor specs | 6 documents |
| Hermes task contracts | 6 prompts |
| Tests/fixtures | 5 files (HTML, PDF, text) |

---

## 5. Taxonomy Changes

| Tag | Status | Evidence |
|-----|--------|----------|
| `water_restrictions` | ✅ Promoted to canonical | Phase III water shortage (backfill + live monitor) |
| `budget_millage` | ✅ Promoted to canonical | School funding surtax item (backfill) |
| `cdd_governance` | ⬜ Proposed, pending items | No CDD data yet |

---

## 6. Dedupe & Review Queue Status

- **Dedupe index:** 88 keys, automated rebuild, idempotent
- **Review queue:** 99 entries — 83 verified, 15 archived, 1 rejected_noise
- **Pending:** 0
- **Needs follow-up:** 0
- **Batch review rules:** Documented for 12 item families

---

## 7. Remaining Source Gaps

| Gap | Status |
|-----|--------|
| BCC broken agenda links (June 16, June 2, April 21) | ⬜ Needs Clerk's office follow-up |
| BCC consent agenda item context | ⬜ Backup documents needed for 11 items (now resolved) |
| CDD governance sources | ⬜ Tier 3 not yet promoted |
| Community/developer pages | ⬜ Tier 4 not yet promoted |
| Property Appraiser URL conflict | ⬜ SRC-002 unresolved |
| Source-watch first discovery cycle | ⬜ SW-002 pending |
| Local media discovery terms | ⬜ MEDIA-001 pending |
| Aug-Sep 2025 backfill | ⬜ BF-005 pending |

---

## 8. Known Risks

- No PDF extraction library was available at start — `pypdf` was added; works well
- 3 BCC meeting agenda links are broken (Clerk's page points to minutes PDFs)
- Sheriff press releases (crime/safety) require individual human review — batch rules can't handle them
- No Hermes runtime exists for fully automated daily cycles
- All extracted content is drafts for editorial review — nothing publishable yet
- repo is not under git — no version history, no snapshot

---

## 9. Testing/Validation Status

| Check | Status |
|-------|--------|
| YAML validation (all files) | ✅ Pass |
| NBOR fixture parser | ✅ 25 records, idempotent |
| BCC agenda PDF extraction | ✅ Two meetings, 75 items |
| Dedupe rebuild idempotency | ✅ 88 keys, stable |
| Review queue rebuild preservation | ✅ 125 states preserved |
| Batch review coverage | ✅ 0 unmatched items |

---

## 10. Recommended Next Questions for Codex

1. **Source event model:** Should BCC meeting-level records use a separate
   `source_event` schema to distinguish from intel items?

2. **School stack priority:** The school district monitor spec is ready and
   a pilot was run. Should the school stack be activated as a second weekly
   lane before expanding to new sources?

3. **Aug-Sep 2025 backfill vs. new monitors:** Which provides more value:
   backfilling TRIM/budget season or activating CDD/community source monitors?

4. **Hermes runtime:** Should a lightweight Hermes-style execution layer be
   designed to automate daily cycles, or is the current supervised operator
   mode sufficient for the near term?

5. **CDD source promotion:** Tier 3 CDD sources (Tolomato, Trout Creek, Six
   Mile Creek) are in the candidate registry. Should they be promoted and
   piloted next?

6. **Clustering:** NBOR and BCC share application IDs (REZ, PUD, ZVAR, etc.).
   Should cross-source clustering be automated, or is manual linking sufficient?

7. **Git:** The repo has no version history. Should Git Steward initiate a
   baseline commit?

---

## 11. Candidate Next Phases

| Phase | Focus | Suggested Priority |
|-------|-------|-------------------|
| School stack activation | Weekly monitor for SJCSD news + BoardDocs | High |
| BCC broken agenda links | Clerk's office contact or recheck | Medium |
| CDD source promotion | Tolomato, Trout Creek, Six Mile Creek | Medium |
| Source-watch first cycle | Test search terms, check source health | Medium |
| Aug-Sep 2025 backfill | TRIM/budget season, school rezoning | Medium |
| Hermes runtime evaluation | Lightweight daily automation | Low (future) |
| BoardDocs full extraction | School board agenda items | Low (future) |
| Publishing/newsletter | Out of current scope | Future-only |

---

## 12. Files Summary (Key Paths)

| Category | Path |
|----------|------|
| Source registry | `registry/sources.yaml` |
| Candidate registry | `registry/source_candidates.yaml` |
| Taxonomy | `docs/taxonomy.md` |
| Cadence system | `docs/cadence.md` |
| Monitor specs | `docs/monitor_specs/` |
| Daily cycle summary | `data/intel_items/2026-06-26/daily_cycle_summary.yaml` |
| NBOR extractor | `scripts/extract_nbor.py` |
| BCC extractor | `scripts/extract_bcc_agenda.py` |
| Dedupe index | `data/index/prior_items.yaml` |
| Review queue | `data/review_queue/queue.yaml` |
| Batch review rules | `docs/editorial/batch_review_rules.md` |
| ED-001 requirements | `docs/editorial/ed001_review_queue_requirements.md` |
| Backlog | `BACKLOG.md` |
| Internal memory | `README_INTERNAL.md` |
| Architect agent | `.opencode/agents/sjc-intel-architect.md` |
| Source-watch agent | `.opencode/agents/sjc-intel-source-watch.md` |
