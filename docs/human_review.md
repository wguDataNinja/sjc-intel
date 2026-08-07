# Human review guide

**Purpose:** Human review is the control point between collection and durable
state. An LLM or Hermes worker may surface evidence and propose changes; it
does not make an editorial, registry, publication, or scheduling decision.

Read this after `CURRENT_BRIEF.md` or after importing a verified weekly bundle.

## First classify the decision

| Decision type | Authority | Where to review | Allowed outcome |
|---|---|---|---|
| Adaptive discovery proposal | `data/adaptive_discovery/` | `CURRENT_BRIEF.md` + proposal detail | Track it in isolated adaptive state, reject/defer, or roll back |
| Weekly candidate item | `data/incoming/<run-id>/` | Imported bundle candidate evidence | Add as `pending_review`, reject, or defer |
| Source proposal | `data/incoming/<run-id>/` | Bundle source-proposal evidence | Record a proposal/rejection/deferral only |
| Editorial/public release | Publication decision + release contract | Existing review queue and release workflow | Verify and explicitly approve/withdraw publication membership |

Do not use an adaptive acceptance as proof that an item is verified or public.
Do not use an imported candidate as permission to promote a source or publish.

## Adaptive discovery review

1. Read `CURRENT_BRIEF.md` for the prioritized group and pipeline/coverage
   context.
2. Inspect each proposal before deciding:

   ```bash
   python3 scripts/review_adaptive_proposal.py show --proposal-id <ID>
   ```

3. Check the original public source, whether the subject is truly distinct,
   the proposed tracking benefit, and whether it fits the SilverLeaf scope.
   RSS and media are leads; consequential claims need primary-source support.
4. Ambiguous proposals should already carry a research-resolution record (from
   `scripts/research_adaptive_proposal.py`). Review confirmed facts, strong
   inferences, and unresolved questions; never accept a confirmed claim that
   research shows is only inferred.
5. Make one recorded decision at a time:

   ```bash
   python3 scripts/review_adaptive_proposal.py accept --proposal-id <ID> --reviewer Buddy --rationale "official source checked; useful recurring subject"
   python3 scripts/review_adaptive_proposal.py reject --proposal-id <ID> --reviewer Buddy --rationale "duplicate or insufficient evidence"
   python3 scripts/review_adaptive_proposal.py defer --proposal-id <ID> --reviewer Buddy --rationale "wait for official confirmation"
   ```

6. To correct a proposal before acceptance (canonical name, aliases, location,
   queries, or timeline language), edit it first — this preserves the original
   and records why — then accept only the corrected record:

   ```bash
   python3 scripts/review_adaptive_proposal.py edit --proposal-id <ID> --reviewer Buddy \
     --subject "Canonical Name" --aliases "Alias A,Alias B" --rationale "reason"
   python3 scripts/review_adaptive_proposal.py accept --proposal-id <ID> --reviewer Buddy --rationale "verified corrected record"
   ```

7. To undo an acceptance, use the original decision ID:

   ```bash
   python3 scripts/review_adaptive_proposal.py rollback --proposal-id <ID> --decision-id <DECISION_ID> --reviewer Buddy --rationale "reason"
   ```

Each non-dry-run decision regenerates `CURRENT_BRIEF.md`. The durable audit
record is `data/adaptive_discovery/decisions.yaml`; pending proposals, accepted
state, and research resolutions are also versioned there.

## Weekly bundle review

1. Verify the bundle before import:

   ```bash
   python3 scripts/bundle_verify.py --bundle <bundle-dir>
   python3 scripts/import_weekly_bundle.py <bundle-dir> --git-sha <pinned-sha> --preview
   ```

2. Import only a passing bundle, then inspect its candidates and source
   proposals. Candidate acceptance is intentionally one item at a time:

   ```bash
   python3 scripts/accept_candidates.py --run-id <RUN_ID> --candidate-id <ITEM_ID> --decision accept --reviewer Buddy --notes "reason"
   python3 scripts/review_source_proposals.py --run-id <RUN_ID> --proposal-id <ID> --decision defer_pending_verification --reviewer Buddy --notes "reason"
   ```

3. An accepted candidate is only `pending_review`; it is not verified or
   published. Source-proposal review never edits `registry/sources.yaml`.

## Required review questions

- Is the evidence public, accessible, attributable, and sufficiently specific?
- Is the claim current and relevant to a SilverLeaf resident?
- Is this duplicate, a weak identity match, a stale item, or merely context?
- Does it involve safety, crime, legal matters, minors, controversy, or named
  individuals? If so, retain `pending_review` and obtain the required human
  editorial review before any public use.
- Is the proposed change narrowly reversible and correctly classified?

## Publication is a separate final gate

Use `docs/publication_release_contract.md` and the existing publication
decision workflow only after an item is verified and editorially approved.
The static [SilverLeaf Brief](../site/index.html) contains reviewed release
items only. Nothing in this guide automatically changes it.
