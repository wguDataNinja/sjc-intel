# Hermes Task Contract

> Defines the standardized interface between the orchestrator (sjc-intel-architect)
> and worker/middle subagents in the three-tier coding workflow.

---

## 1. Worker Prompt Format

Every dispatched worker task follows this exact structure:

```
Task: <session-id>: <concise one-line goal>
Read: WORKER_CONTEXT.md
Read: <specific files needed>
Inspect only: <file paths — limited scope>
Do: <numbered checklist items — one action per bullet>
Validation: <exact terminal command to verify output>
Write output to: runtime/workers/<session-id>.md
Return: "Complete. See runtime/workers/<session-id>.md"
Do NOT commit. Do NOT explore. Do NOT add scope.
```

### Rules
- **Inline over reference.** If the worker needs registry data, inline the relevant rows in the prompt context rather than saying "Read: sources.yaml". The subagent has no memory of your conversation.
- **One task per dispatch.** Do not bundle unrelated work into a single worker.
- **Validation must be an exact command.** Not "verify with a test" — give the concrete `python3 -c "..."` or `grep -c` command.
- **Output always goes to `runtime/workers/`.** Not to the root, not to logs. Use the session ID as the filename.

## 2. Middle Tier Review Format

Every worker that modifies source-of-truth (SOT) files gets a middle review.

```
Read: runtime/workers/<session-id>.md
Read: ROADMAP.md <relevant checklist>
Read: <any SOT files the worker claimed to modify>
Check:
1. Did they actually run the validation commands? (evidence, not claims)
2. Do file diffs cover all claimed changes?
3. No scope creep (did not touch files outside their brief)?
4. No SOT damage (did not break YAML/Markdown/formatting)?
5. Cross-consistency (counts add up, references consistent)?

Returns one word: APPROVED | FLAG:<reason> | ESCALATE:<reason>
Return nothing else.
```

### When to dispatch middle review
- **Always** after SOT modifications: registry edits (sources.yaml, source_candidates.yaml, communities.yaml), taxonomy changes, backlog updates.
- **Never** for read-only tasks (audits, investigations, reports).
- **Never** for new-file-only tasks (draft plans, scoping docs).

### Verdict meanings
| Verdict | Meaning | Orc Action |
|---------|---------|------------|
| `APPROVED` | Worker output verified correct | Update WORKER_CONTEXT.md, update backlog, proceed |
| `FLAG:<reason>` | Minor issue found | Read worker output, fix, re-review or decide to accept |
| `ESCALATE:<reason>` | Blocking issue, wrong approach, or needs human decision | Pause pipeline, inform user |

## 3. File Output Conventions

| Artifact | Location | Purpose |
|----------|----------|---------|
| Worker reports | `runtime/workers/<session-id>.md` | Generic bounded-task record; weekly Hermes uses its own workspace contract |
| Extracted items | `data/intel_items/<YYYY-MM-DD>/<source_id>.yaml` | Daily extraction output |
| Backlog patches | Inline `BACKLOG.md` patch | Always update backlog after every completed session |
| Context updates | Inline `WORKER_CONTEXT.md` patch | Log every session outcome here |
| Registry changes | Inline patch to `registry/*.yaml` | Source-of-truth — never overwrite whole file |

For `sjc-weekly-001`, `docs/hermes_weekly_entrypoint.md` and
`docs/weekly_operational_contract.md` override the generic worker-output
location: the worker writes only to `runtime/weekly/<run-id>/` and its verified
bundle. It never writes the corpus directly.

## 4. Token Discipline

- **Chat is for traffic lights.** Details go in markdown on disk.
- Worker returns: ~7 words ("Complete. See <path>").
- Middle returns: 1 word.
- Orc tells user: toggle only (status update + next move).
- Pre-read files and inline only relevant rows. Never dump entire files into the prompt.
- Worker context must be self-contained — they have no chat memory.

## 5. Rules of Engagement

### Workers must
- Read WORKER_CONTEXT.md first for session context
- Run the exact validation command specified
- Write output to `runtime/workers/<session-id>.md`
- Output WARNING lines to stdout if schema drift detected
- Flag unknowns (broken URLs, unexpected pagination, JS-gated content) — do not fabricate

### Workers must NOT
- Commit to git
- Explore beyond their brief
- Modify source-of-truth files (registries, schemas, ROADMAP.md, STATE.md, BACKLOG.md, WORKER_CONTEXT.md)
- Dispatch sub-tasks
- Assume anything not in their inlined context
- Fabricate results — report blockers honestly

### Orchestrator must NOT
- Parallelize tasks that write to the same files
- Modify worker output files after the fact
- Skip middle review for SOT modifications
- Override a FLAG or ESCALATE without reading the worker output

## 6. Session Lifecycle

```
1. Orc reads ROADMAP.md, git state, current context
2. Orc selects next item from BACKLOG.md
3. Orc dispatches worker(s) — inline relevant context
4. Worker runs, writes output, returns verdict
5. If SOT modified → Orc dispatches middle review
6. Middle returns verdict
7. If APPROVED → Orc updates WORKER_CONTEXT.md + BACKLOG.md
8. If FLAG → Orc reads output, decides fix or proceed
9. If ESCALATE → Orc informs user
10. Orc selects next task (loop to step 2)
```

## 7. Scope Boundaries

| Priority | Do automously | Ask Buddy |
|----------|---------------|-----------|
| P0 | Fix broken registries, update stale docs, run monitors | Blocked extraction pipelines, unreachable sources |
| P1 | Backfill execution (when plan exists), CDD promotion, taxonomy eval | Approving new source families, Codex usage |
| P2 | Data inventory updates, doc improvements, search-term tuning | Adding new monitor cadences, cron automation |
| P3 | Deferred items (media audits, community dev stacks) | Publishing strategy, product naming |
