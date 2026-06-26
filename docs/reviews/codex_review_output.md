**1. What Is Working Well?**

The first buildout loop has produced a coherent supervised intelligence workflow. The system now has canonical source registries, monitor specs, extraction scripts, dedupe, review queue construction, batch review rules, and explicit cadence markers.

The strongest parts are:

- Clear separation between source discovery, extraction, dedupe, review, and editorial judgment.
- Daily and weekly lanes are documented instead of implicit.
- Review state preservation appears to be treated as a first-class requirement.
- Batch review is useful but bounded, with sensitive categories still requiring human review.
- The project has resisted premature publishing or automation, which is appropriate for the risk profile.
- Tests and fixtures exist for the core first-pass extractors.

**2. Architectural Risks Before More Source Expansion**

The biggest architectural risk is that the system is accumulating source-specific extracted “intel items” without a clearly separate event/source-record layer. BCC meetings, NBOR notices, BoardDocs agendas, sheriff releases, and utility updates are not the same kind of object. Treating them all as peer intel items will make clustering, provenance, review, and updates harder.

Other risks:

- No Git baseline means expansion increases rollback and audit risk.
- No Hermes runtime exists yet, so operator judgment is carrying orchestration complexity.
- LAST_RUN markers are simple and useful, but they may become too thin once failed, partial, source-health, and extraction runs overlap.
- Source expansion before model stabilization will multiply cleanup work.
- The source registry and candidate registry are becoming operational infrastructure; they need stricter validation as they grow.

**3. Data Model Risks Visible Now**

The current model appears item-centric, but several workflows need more durable relationships:

- `source_event`: needed for meetings, agenda packets, press-release pages, source snapshots, and monitor runs.
- `source_document`: needed for PDFs, agendas, backup materials, notices, attachments, and broken-link resolution.
- `intel_item`: should represent reviewed/derived facts or resident-relevant items, not every raw source artifact.
- `cluster`: needed for shared application IDs such as REZ, PUD, ZVAR, COMPAMD, etc.
- `review_decision`: should remain distinct from source data so review history survives rebuilds.

The dedupe index is working, but application-ID clustering should not be forced into dedupe. Duplicate detection and cross-source relationship detection are different problems.

**4. Review / Editorial Workflow Risks**

The review queue is in good shape for the current scale, but the editorial workflow still has risks:

- Batch rules may create false confidence if applied to sensitive or ambiguous items.
- Sheriff, school safety, legal, public-safety, controversy, and crime items need explicit review gates.
- “Verified” needs a stable definition: verified against source presence, official record, factual claim, or editorial publishability.
- There is no publishing path now, which is fine, but the system should avoid letting internal labels imply public readiness.
- Needs-follow-up is currently zero, but source gaps like broken BCC links and Clerk follow-up suggest the workflow needs a stronger unresolved-evidence state.

**5. Source-Monitoring Gaps That Matter Most**

Highest priority gaps:

1. School stack activation  
   Schools are resident-critical, seasonal, and high-impact. Since the spec is ready and pilot work exists, this is the cleanest next weekly lane.

2. BCC broken agenda links  
   Broken Clerk agenda links affect trust in the BCC extraction lane. They should be tracked as source defects, not just backlog notes.

3. Application-ID clustering  
   NBOR and BCC likely describe the same land-use matters from different procedural angles. Without clustering, the system may fragment important stories.

4. Property Appraiser URL conflict  
   SRC-002 sounds like a source identity/canonicalization issue. Those should be fixed before many more property/development sources are added.

5. Source-watch first discovery cycle  
   The source-watch role exists, but its first cycle is still pending. That is a process gap.

CDD/community expansion matters, but it should follow the model cleanup above.

**6. Test / Validation Gaps**

The current tests cover the first extractors and queue rebuild behavior, but the next gaps are:

- Schema validation for intel items, source candidates, canonical sources, review queue entries, and dedupe keys.
- Regression fixtures for broken or malformed BCC links.
- Tests proving review status survives repeated rebuilds across changed source input.
- Tests for application-ID extraction and clustering.
- Negative tests for sheriff/sensitive items to ensure they are not batch-verified.
- Validation that LAST_RUN markers are only advanced after successful runs.
- A lightweight integrity check that reports orphaned review entries, duplicate IDs, missing source refs, and unrecognized taxonomy tags.

**7. Next Phase Priority**

Prioritize the `source_event` model first, then activate the school stack.

Reason: school stack activation is high-value, but adding BoardDocs and school-board material before separating source events from intel items will increase model ambiguity. A minimal `source_event` layer does not need to be elaborate; it just needs to distinguish source artifacts from resident-relevant derived items.

Recommended ordering of listed options:

1. `source_event` model
2. Git baseline
3. School stack activation
4. Application-ID clustering
5. Aug-Sep 2025 backfill
6. CDD/community expansion
7. Hermes runtime

Hermes should wait until the data contracts and supervised workflow are stable.

**8. Refreshed 3-Phase Roadmap**

**Phase 1: Stabilize the Core Model and Baseline**

- Add/document `source_event` and related source artifact concepts.
- Define relationship between source events, documents, intel items, review queue entries, and clusters.
- Add schema/integrity validation.
- Resolve Git baseline requirements.
- Track BCC broken links as source defects.
- Preserve current supervised operator mode.

**Phase 2: Activate High-Value Weekly Coverage**

- Activate school stack as the second weekly lane.
- Add BoardDocs extraction only after basic source-event modeling exists.
- Add application-ID clustering across NBOR and BCC.
- Run source-watch first discovery cycle.
- Close SRC-002 Property Appraiser URL conflict.
- Strengthen sensitive-item review gates.

**Phase 3: Expand Coverage Deliberately**

- Run Aug-Sep 2025 backfill for TRIM/budget and school-season context.
- Promote and pilot Tier 3 CDD governance sources.
- Evaluate Tier 4 community/developer sources.
- Revisit Hermes runtime only after repeated supervised cycles expose stable automation boundaries.
- Consider richer clustering and longitudinal entity tracking.

**9. Next Best Worker Task**

Create a bounded worker task for source-event modeling:

> Review current intel item, review queue, dedupe index, NBOR extractor output, and BCC agenda extractor output. Propose a minimal `source_event` schema and migration plan that separates raw source artifacts from derived resident-interest intel items. Do not edit files. Output: proposed fields, example records for NBOR and BCC, affected scripts, validation rules, and migration risks.

This is the right next task because it reduces future rework before school, CDD, BoardDocs, or backfill expansion.

**10. Cleanup Items Git Steward Should Require Before Baseline Commit**

- Confirm no generated junk, cache files, or local temporary files are present.
- Add or verify `.gitignore` for Python caches, virtualenvs, logs that should not be versioned, local secrets, and transient run outputs.
- Decide which `logs/` artifacts are source-of-truth enough to commit.
- Verify `data/` policy: which fixtures, indexes, queues, and extracted items belong in Git.
- Run YAML validation.
- Run extractor fixture tests.
- Run dedupe rebuild idempotency check.
- Run review queue rebuild preservation check.
- Confirm no secrets, tokens, private resident data, or login-gated source content exists.
- Confirm `STATE.md`, `BACKLOG.md`, and `ROADMAP.md` reflect current state.
- Commit the review packet and current monitor specs together with the baseline so future architectural changes have a clear reference point.
