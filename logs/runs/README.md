# SJC_Intel — Run Logs

Every agent session writes a meta-run log to `logs/runs/{cadence}/`. These
records are used to track what work was done, what was skipped, and why.

## Run Log Format

```markdown
# Meta-Run Log: {YYYY-MM-DD}_{short_description}

**Run date/time:** {ISO 8601}
**Operator:** {agent name}
**Trigger:** {what initiated the run — "get to work" or specific request}
**Cadence evaluated:** daily / weekly / monthly / all

## Cadence Status

| Cadence | Last Run | Days Since | Work Due? |
|---------|----------|------------|-----------|
| Daily | {timestamp} | {N} | {yes/no} |
| Weekly | {timestamp} | {N} | {yes/no} |
| Monthly | {timestamp} | {N} | {yes/no} |

## Work Due (by cadence bucket)

- Daily: {list of sources due}
- Weekly: {list of sources due}
- Monthly: {list of tasks due}

## Work Selected

**Task:** {task title}
**Why:** {rationale for selecting this task}
**Cadence bucket:** daily / weekly / monthly

## Hermes Tasks

| Task ID | Worker | Status | Output |
|---------|--------|--------|--------|
| {task_id} | {worker} | completed/blocked | {output file} |

## Outputs Created

- {file path} — {description}

## Skipped Work

| Work Item | Why Skipped |
|-----------|-------------|
| {item} | {reason — blocked, deferred, lower priority, needs approval} |

## Blockers

- {blocker description}

## Next Recommended Action

{what the agent recommends for the next run}

## LAST_RUN Updated

- daily: {timestamp} / weekly: {timestamp} / monthly: {timestamp}
```

## Subdirectories

| Directory | Contents |
|-----------|----------|
| `daily/` | Run logs for daily cadence sessions |
| `weekly/` | Run logs for weekly cadence sessions |
| `monthly/` | Run logs for monthly cadence sessions |

## LAST_RUN Files

Each subdirectory contains a `LAST_RUN` file with the ISO 8601 timestamp of
the last completed run for that cadence. Format:

```
2026-06-03T23:30:00Z
```

If a `LAST_RUN` file does not exist, treat all sources in that cadence as due.
