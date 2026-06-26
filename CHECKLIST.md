# SJC_Intel Operating Checklists

## Start Of Session

- Read `STATE.md`.
- Read `.opencode/agent_memory/sjc-intel-architect.memory.md`.
- Check `BACKLOG.md` for the highest-priority open item.
- Check `docs/operator_mode.md` if Buddy says "get to work".
- Check `docs/cadence.md` and evaluate due work from LAST_RUN markers.
- Confirm the task does not require live monitoring, backfill execution,
  source promotion, or publishing without explicit approval.

## Before Hermes Delegation

- Define the exact input files and output files.
- State whether web access is needed.
- Confirm public-source-only boundaries.
- Include dedupe and sensitivity rules.
- Specify what should be logged.
- Make the task small enough to verify.

## After Hermes Completion

- Inspect output files for schema shape and obvious overreach.
- Check source URLs and public accessibility assumptions.
- Confirm sensitive items are `pending_review` and human-review-required.
- Update `STATE.md`, `BACKLOG.md`, and agent memory if durable state changed.
- Add or update an agent log.

## Before Canonical Promotion

- Confirm the candidate exists in `registry/source_candidates.yaml`.
- Dedupe against `registry/sources.yaml`.
- Verify source is public and not login-gated.
- Classify source family, topics, communities, cadence, and reliability.
- Record Buddy approval for source promotion.
- Update both candidate and canonical source records.

## Before Taxonomy Change

- Check whether existing topics/interest tags already cover the need.
- Require real item evidence, not just a hypothetical gap.
- Add a concise definition and classification rule.
- Update any dependent prompts/docs.
- Record the decision in logs if it changes operating behavior.

## End Of Session

- Update changed source-of-truth docs.
- Update `STATE.md`.
- Update `BACKLOG.md` statuses if items changed.
- Write meta-run log to `logs/runs/{cadence}/{YYYY-MM-DD}_{task}.md`.
- Update `logs/runs/{cadence}/LAST_RUN` timestamp.
- Keep agent memory concise.
- Create or update an agent log.
- Do not leave unreported blockers.

## Before Publishing

- Confirm publishing is explicitly in scope.
- Confirm every claim has a public source URL.
- Confirm sensitive/legal/public-safety/school/crime items had human review.
- Do not copy local media content; summarize and attribute.
- Do not publish private screenshots or private-group content.
- Confirm corrections workflow exists before public launch.
