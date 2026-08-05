# Task 14 — Publish Readiness and VPS Onboarding

**Task identity:** 14-publish-readiness-and-vps-onboarding.md
**Date:** 2026-08-03
**Repositories:** SJC_Intel (`/Users/buddy/projects/sjc_intel`), Ivy Control VPS (`/Users/buddy/projects/ivy-control-vps`, read-only)
**Final status:** COMPLETE_WITH_FOLLOW_UP

## 1. Executive result

SJC_Intel is materially closer to portfolio publication and Ivy onboarding.
The path to launch is now short and explicit; the repository cleanup is fully
classified; the external-backup policy is defined with evidence-based sizing;
the PostgreSQL disposition is unambiguous; the repository-to-Hermes
task-submission model and a minutes-from-now test packet exist; and a
recommended weekly schedule is documented.

Delivered (repo-local, tested):

- Public-safe `README.md` and public architecture `docs/ARCHITECTURE.md`.
- `docs/backup-restore.md` extended to the authoritative file-corpus
  external-backup policy (dormant PG runbook retained as future-ready scope).
- `deploy/sjc-weekly-task.yaml` — repository-side weekly task declaration,
  schema-validated by `scripts/validate.py`.
- SJSO RSS workspace monitor in `run_weekly.py` (+ fixture + 2 tests) — the
  concrete next step of the Task 13 proposal.
- `docs/weekly_scheduling.md` — Hermes reality, responsibility split,
  minutes-from-now test packet, recommended weekly window.
- ROADMAP.md: ordered publish-ready sequence, SJC onboarding status, updated
  task statuses.

Ivy-side generic backup-onboarding requirement is specified as an exact
proposed patch (not applied — cross-repo authority edits were not authorized
for this agent). No privileged VPS, timer, database, secret, commit, or push
action occurred.

## 2. Starting SJC Git state

| Item | Observed |
|------|----------|
| Branch | `master` |
| HEAD | `1be2ade` |
| origin/master | Exists, == local (0 ahead / 0 behind) |
| Working tree | Dirty (pre-existing): `ROADMAP.md`, `scripts/extract_nbor.py`, `data/intel_items/2026-07-06/agentic_search_results.yaml`, `data/review_queue/queue.yaml`, `data/review_queue/summary.yaml`; plus untracked Tasks 12–13 outputs |
| LICENSE | **None in local master** (origin/main has one in unrelated history) |
| Public README | Thin, pointed at internal entrypoint |

## 3. Starting Ivy state

- Branch `main`, 2 commits ahead of origin, with pre-existing uncommitted
  control-plane work (including `repos/sjc-intel/CONTROL.md` modified — the
  remote/SHA update Task 12 flagged is still uncommitted on Ivy's side).
- `VPS_ADMISSION_CHECKLIST.md` covers identity, GitHub, hygiene, data lifecycle,
  PostgreSQL, capacity, placement, runtime authority, secrets/recovery, and
  acceptance + the bundle-transfer addition — but has **no explicit external
  backup disposition gate** (the gap this task addresses).
- Hermes v0.18.2 installed read-only on VPS; provider auth **not** configured.
- Active VPS timers: WGU-Reddit daily ~07:00 UTC, WGU backup, Launchpad cleanup;
  plus Chrome/collector workloads (report 10 evidence).

## 4. Publish-readiness assessment

The repository is architecturally ready to publish; the remaining work is
implementation of the publication path plus editorial review. Git hygiene is
good (5.2 MB tracked, no secrets tracked, only `.env.example`).

## 5. Required launch work

Ordered (see ROADMAP §3D):

1. §3A-G2 full-corpus validator + canonical publication selector (medium, no
   network, no privileged access).
2. Human editorial review pass — resolve the 78 `pending_review` queue items to
   `verified`/`rejected_noise` (Buddy/editorial).
3. §3B-G1 minimum SilverLeaf scope registry (medium).
4. §3B-G2 deterministic static release export (`release.json`,
   `search-index.json`, `release-manifest.json`) (medium).
5. §3C-G1 portfolio integration context packet (Strong Codex / authorized
   cross-repo, read-only).
6. §3C-G2 static SilverLeaf UI (medium).
7. Buddy publication decision + first reviewed release.
8. Public presentation: LICENSE (Buddy decision — none applied; MIT recommended),
   screenshots/diagram (after first release). `README.md` and
   `docs/ARCHITECTURE.md` are already DONE.

## 6. Non-blocking work (valuable, does not gate launch)

- Weekly VPS shadow run (§3E) — foundation DONE (Tasks 12–13), privileged
  admission + shadow proof remain.
- SJSO RSS monitor — **DONE locally** (Task 14); registry `check_url` change
  stays behind the approved source-review path.
- BCC workspace mode — exact next medium task.
- Backup automation (first external archive + restore drill).
- Subscriptions; second-domain portability proof; operational PostgreSQL
  metadata (all deferred by policy).

## 7. Deferred work

Live incidents/emergency alerting; PostGIS/GIS; semantic search; public API;
full multi-domain platform; autonomous publication; real-time alerts; user
accounts — all per ROADMAP §1B/§5, none launch work.

## 8. Repository-cleanup preflight

Measurements (safe, read-only): tracked working tree 330 files / 5.2 MB;
`.git` 4.6 MB; `data/` 75 files / 1.2 MB; `docs/` 1.0 MB; `tests/` 2.4 MB
(mostly fixtures); `runtime/` 176 KB (ignored); `.opencode/` 57 MB (ignored,
`node_modules`).

| Artifact | Classification | Why it exists | Authoritative? | Regenerable? | Commit? | Backup? | Action |
|----------|----------------|---------------|----------------|--------------|---------|---------|--------|
| `registry/*.yaml` | authoritative | Canonical config | Yes | No | Yes | Yes | Keep |
| `data/intel_items/` | authoritative | Corpus | Yes | No | Yes (curated) | Yes | Keep |
| `data/source_events/` | authoritative | Provenance | Yes | No | Yes | Yes | Keep |
| `data/review_queue/` | authoritative | Review decisions | Yes | No (rebuild preserves decisions) | Yes | Yes | Keep |
| `data/index/prior_items.yaml` | generated but durable | Dedupe | Derived | Yes (rebuild) | Yes | Yes | Keep; rebuild is safe |
| `data/incoming/` | generated but durable | Staged bundles + receipts | Yes (accepted) | Re-importable | Yes | Yes | Keep (staging cleaned only after verified receipt + retention) |
| `data/receipts/` | generated but durable | Acknowledgment | Yes | No | Yes | Yes | Keep |
| `data/monthly/` | historical + derived | Cadence wraps | Mixed | Partly | Yes | Yes | Keep; older wraps compressible |
| `data/search_runs/` | generated but durable | Search evidence | Yes | No | Yes | Yes | Keep |
| `runtime/weekly/`, `runtime/workers/` | runtime-only | Run workspaces + worker outputs | No | Yes | **No** (gitignored) | Optional (proof only) | Safe to ignore; clean after verified import |
| `.opencode/node_modules/` | runtime-only | OpenCode runtime deps | No | Yes | No (gitignored) | No | Safe to ignore/prune (57 MB) |
| `.venv/`, `__pycache__/` | runtime-only | Env/cache | No | Yes | No | No | Safe to ignore |
| `tests/fixtures/*.html/pdf` | test fixture | Offline parser fixtures | Yes (tests) | Re-fetchable | Yes | Optional | Keep (used by tests) |
| `db/migrations/` + `validation/` | authoritative (dormant-ready) | SQL-readiness | Yes | No | Yes | Yes | Keep |
| `deploy/systemd/*` | current implementation (inert) | Deployment templates | No (inert) | Yes | Yes | Yes | Keep; not installed |
| `deploy/sjc-weekly-task.yaml` | authoritative | Task declaration | Yes | No | Yes | Yes | Keep (new) |
| `docs/` (70 files incl. archive/reviews) | mixed | Authority + history | Mixed | Mostly no | Yes | Yes | Keep; review-only docs compressible to archive later |
| `tasks/`, `reports/`, `logs/` | historical + audit | Session record | Yes (audit) | No | Yes | Yes | Keep |
| `README.md` | current implementation | Public entry | Yes | No | Yes | Yes | Updated to public-safe |
| `README_INTERNAL.md`, `AGENTS.md` | internal authority | Operate the repo | Yes | No | Yes | Yes | Keep internal (not public presentation) |
| `.opencode/agents+memory/` | internal authority | Agent config | Yes | No | Yes | Yes | Keep |

**Safety rule honored:** nothing was deleted, compressed, or archived. The only
mutations were the four implementation files this task authored (README,
ARCHITECTURE, backup-restore §0, weekly_scheduling, task manifest) and the
SJSO monitor + tests. `.opencode/node_modules` (57 MB) is the single largest
prunable item and is already gitignored — deleting it is safe and frees ~57 MB,
but was left to Buddy's explicit call.

## 9. Backup scope classification

Defined in `docs/backup-restore.md` §0.1:

- **Must back up:** registry, intel items, source events, review decisions,
  dedupe state, accepted staged bundles + receipts, monthly wraps, schemas +
  migrations, config (`deploy/`, incl. task manifest), secret-name contracts
  (never values), docs, prompts, task/report/log history.
- **Reconstructable but worth backing up:** search runs, topic clusters, metric
  snapshots, generated summaries, future release projections.
- **Optional/excluded:** `.venv`, caches, `.opencode/node_modules`, `runtime/`,
  transient raw downloads, duplicate bundle copies, `.git`, logs beyond
  retention, local secrets.

## 10. Backup size and compression findings

| Metric | Value (measured) |
|--------|------------------|
| Tracked working tree | 330 files / 5.2 MB |
| `data/` (durable corpus) | 75 files / 1.2 MB |
| `data/` gzip-1 archive | ~225 KB |
| `data/` gzip-9 archive | ~175 KB (≈7× compression) |
| `.git` | 4.6 MB (re-clonable, not backed up) |
| `db/` | 168 KB |
| `logs/` + `reports/` + `tasks/` | ~530 KB |
| Expected growth | ~1–2 MB/session corpus; weekly bundles KB-scale |
| Backup type | Full archives (size makes incremental unnecessary now) |
| Compression | `gzip -9` for text corpus; raw HTML/XML fixtures already in Git at fixture scale; old bundles tar+gzip when archived |
| Content-addressed dedupe | Not needed at current scale; revisit only if >50 MB sustained growth |
| Retention | 4 weekly + 1 month-end; latest verified = restore baseline; immutable pre-launch snapshots |
| Frequency | Full after each meaningful session; minimum weekly |

## 11. SJC external-backup policy

`docs/backup-restore.md` is now the authoritative policy. §0 defines scope,
exclusions, archive layout (Ivy-compatible dated tree + manifest), compression,
frequency, manifest/checksum requirements, encryption boundary (encrypted
archive volume, verified in manifest), retention, restore procedure + order,
restore verification, responsibility (Mac operator initiates, checksum +
monthly restore-sample verification), and failure handling. The former
PostgreSQL runbook is explicitly marked **dormant future-ready scope**, not the
active backup path.

**Destination:** undecided (Buddy choice). The policy is provider-neutral:
any encrypted cold-archive volume or object store satisfying the Ivy
`BACKUP_MANIFEST_STANDARD.md` layout. No credentials or providers were invented.

## 12. Ivy generic backup-onboarding requirement

Gap confirmed: `VPS_ADMISSION_CHECKLIST.md` has no explicit external-backup
disposition gate. Recommended smallest authority: **add item 11 (Backup
disposition) to `docs/VPS_ADMISSION_CHECKLIST.md`** — not a new document — and
reference the existing `docs/DATA_LIFECYCLE_STANDARD.md` and
`docs/BACKUP_MANIFEST_STANDARD.md`. Exact proposed patch (for the authorized
Ivy operator; not applied by this agent):

```
11. **Backup disposition (external):** every repo must answer before production
    VPS workload status:
    - what data is durable vs ephemeral (docs/DATA_LIFECYCLE_STANDARD.md);
    - what remains on the VPS vs transfers elsewhere;
    - what is backed up externally, with frequency, retention, compression,
      encryption, manifest, and checksums (docs/BACKUP_MANIFEST_STANDARD.md);
    - restore procedure and restore-test evidence (sample or full drill);
    - ownership, failure alerting, and prune gate.
    Gate: scope defined → first backup completed → checksum verified → restore
    path documented → restore test scheduled or completed. No repository becomes
    a production VPS workload without an explicit backup disposition; deployment
    must not begin before backup is configured unless Buddy approves an
    exception with a restore path.
```

Additionally recommended: update `repos/sjc-intel/CONTROL.md` (remote
configured, approved SHA `1be2ade`, bundle-transfer admission) — already an
outstanding privileged step.

## 13. Restore requirements

`docs/backup-restore.md` §0.4 defines the restore objective and order:
registry → schemas/migrations → corpus + source events → review state + dedupe
→ receipts/incoming → docs/config/tooling. After restore, run
`python3 scripts/validate.py`, `python3 -m pytest tests/`, and rebuild the
dedupe index + review queue (idempotent). Restore to a clean Mac checkout is a
supported target. Weekly operations resume from the restored bundle/receipt
state; public releases are reproducible from reviewed corpus + release
manifest (future).

## 14. SJC PostgreSQL disposition

**Classified: `DORMANT_FUTURE_READY`** — verified against ROADMAP.md (§1B, §5),
VPS_ROADMAP.md, docs/VPS_CONTINUITY.md, docs/postgresql_adapter.md,
docs/backup-restore.md, and Task 08–13 reports.

- **Intentionally unused:** no SJC corpus, staging, or operational metadata is
  stored in VPS PostgreSQL; the Mac file corpus is authoritative.
- **Future-ready:** migrations `20260705_001`…`20260706_011`, roles, adapter
  (`scripts/pg_adapter.py`), storage backend selection, retention + metric
  migrations all remain valid, tested SQL-readiness material.
- **Activation triggers (only when needed):** Option-B operational metadata
  (locks, run/source-health state, transfer manifests/acknowledgements) under
  multi-writer contention or long retention history — after separate
  Ivy/database authorization.
- **Never:** an accidental second authority for the corpus, a launch
  dependency, or a search API. Contradictions resolved: `docs/backup-restore.md`
  formerly read as PG-centric; it is now explicitly dormant for SQL scope with
  the active file-corpus policy in §0.

## 15. Hermes runtime reality

Verified: Hermes Agent v0.18.2 on the VPS is a read-only resident assistant;
provider authentication is **not** configured; it has no production write
authority and is not a general task executor. Therefore the SJC weekly run is
executed by the deterministic runner (`scripts/run_weekly.py`) — no model
provider is required for Stage A. Hermes may read/coordinate but does not
execute the run. No unverified Hermes capability is claimed.

## 16. Repository-to-Hermes task-submission model

Reusable model (documented in `docs/weekly_scheduling.md` §2):

```
project repo declares task specification  deploy/sjc-weekly-task.yaml + prompts/sjc_weekly_ops_task.md
  ↓ Ivy admission/review                  VPS_ADMISSION_CHECKLIST + CONTROL.md
  ↓ Ivy deploy manifest references task   exact SHA + systemd EnvironmentFile
  ↓ systemd service invokes the runner    sjc-intel-weekly.service → run_weekly.py
  ↓ systemd timer controls schedule       sjc-intel-weekly.timer (disabled until gates)
  ↓ project output contract governs       docs/weekly_operational_contract.md §7 (bundle)
```

Repository side (`deploy/sjc-weekly-task.yaml`) declares: task ID, prompt path,
profile, approved sources, discovery budget, output paths, timeout/retries,
secrets (none required), schedule recommendation, health output, bundle
contract version, enabled state. Ivy owns the service/timer units, enablement,
schedule + randomized delay, environment, resource limits, SHA, health,
rollback. This extends the existing task/prompt contract rather than adding a
parallel registry.

## 17. Systemd scheduling model

Single service (`sjc-intel-weekly.service`) invoking the deterministic runner
via `run_weekly.sh`; single timer (`sjc-intel-weekly.timer`) with randomized
delay; `flock` lock + run-ID uniqueness for duplicate prevention; memory/CPU
limits; journald + file logs; health JSON output; disabled until the §3F gate.
No timer is enabled by any document or action here.

## 18. Near-future test schedule packet

`docs/weekly_scheduling.md` §5 contains the exact privileged packet: deploy
pinned SHA, use a transient `systemd-run --user --on-calendar "now + 3min"`
one-shot (never the permanent timer), record exact start time and expected
completion window, verify run log/health/bundle/`bundle_verify.py`, then stop
and `reset-failed` the test unit. Purpose: prove timer activation, service
invocation, deterministic execution, output creation, logging, health, bundle
generation, and transfer readiness without waiting a week. Execution is
privileged and not performed by this agent.

## 19. Recommended recurring weekly schedule

**`Wed 01:30–03:00 UTC`** (≈ Tue 21:30–23:00 ET), randomized delay 900 s.

Rationale: avoids the WGU-Reddit daily ~07:00 UTC timer, WGU backup, and
Launchpad cleanup, and has the least overlap with active daytime
Chrome/collector workloads (report 10 evidence). Must be re-verified against
fresh capacity (Task 10: 83% disk, reboot pending) before activation.

## 20. SJC weekly task scope

Stage A (canonical monitoring): `sjc_nbor_public_notices` + `sjso_news_stories`
(verified RSS), producing source health, source events, candidates with
duplicate/no-match/partial/failed outcomes, and bundle artifacts. Stage B
(bounded discovery): `sl_core` profile → source proposals only. The run never
promotes sources, changes taxonomy, publishes, edits reviewed corpus, or
bypasses human review. The SJSO RSS monitor-update proposal
(`PROP-public_safety-0001`) is incorporated through the approved source-review
path; its concrete next verification step (an RSS capture path) is now
implemented in `run_weekly.py`.

## 21. Ivy onboarding completeness review

SJC onboarding coverage (via `repos/sjc-intel/CONTROL.md` + admission
materials): identity ✓, remote ✓ (pending CONTROL.md update), approved SHA ✓
(pending update to `1be2ade`), deployment path ✗ (privileged), service account
✗, permissions ✗, environment ✗, secrets ✓ (none required), runtime deps ✓
(`requirements.txt`), Hermes task declarations ✓ (new `deploy/sjc-weekly-task.yaml`),
schedule ✓ (recommended; privileged), output contract ✓ (weekly contract),
transfer ✓, acknowledgements ✓ (receipts), pruning ✓ (receipt + retention),
backup ✗ (defined in SJC; Ivy gate proposed), restore ✓ (policy + drill
procedure), health ✓ (contract + `scripts/health_export.py`), alerting ✗
(privileged), logs ✓, retention ✓, resource budget ✓ (runtime limits), network
policy ✓ (public HTTP only), PostgreSQL disposition ✓ (DORMANT_FUTURE_READY),
rollback ✓ (exact SHA + bundle replay), removal/offboarding ✗ (not yet
specified — proposed generic item), ownership ✓, documentation ✓, proof run ✗
(privileged shadow), natural-run verification ✗ (§3E-G2). SJC is a strong
reference onboarding case once the privileged packet lands.

## 22. Implementation completed

| Item | Status |
|------|--------|
| Public-safe `README.md` | COMPLETE |
| `docs/ARCHITECTURE.md` (public portfolio artifact) | COMPLETE |
| `docs/backup-restore.md` §0 authoritative external-backup policy | COMPLETE |
| `deploy/sjc-weekly-task.yaml` + `validate.py` schema check | COMPLETE |
| SJSO RSS workspace monitor (`run_weekly.py`) + fixture + 2 tests | COMPLETE |
| `docs/weekly_scheduling.md` (task-submission + test packet + window) | COMPLETE |
| ROADMAP.md updates (§3D sequence, §3E-G3, §3F) | COMPLETE |
| LICENSE | DEFERRED — Buddy decision (MIT recommended) |
| Corpus validator / publication selector (§3A-G2) | DEFERRED — next medium task |
| SilverLeaf registry (§3B-G1), static export (§3B-G2), UI (§3C) | DEFERRED — next medium tasks |
| BCC workspace mode | DEFERRED — next medium task |
| Ivy doc edits (backup gate, CONTROL.md) | NOT APPLIED — proposed patch in §12 |

## 23. Files changed

Added:

- `docs/ARCHITECTURE.md`
- `docs/weekly_scheduling.md`
- `deploy/sjc-weekly-task.yaml`
- `tests/fixtures/sjso_feed.xml`

Modified:

- `README.md` (public-safe rewrite)
- `docs/backup-restore.md` (authoritative §0; PG runbook marked dormant)
- `scripts/run_weekly.py` (SJSO RSS monitor)
- `scripts/validate.py` (task-declaration check)
- `tests/test_run_weekly.py` (2 new tests)
- `ROADMAP.md` (§3D sequence, §3E-G3, §3F)

Pre-existing dirty/untracked files (data + Task 12–13 outputs) preserved
untouched. Nothing committed or pushed. No Ivy files modified.

## 24. Validation results

```
SJC:
python3 -m pytest tests/ -v           → PASS, 140 passed (120 pre-existing + 20 new)
python3 scripts/validate.py            → PASS — ALL PASSED (incl. new task-declaration check)
python3 scripts/portability_check.py   → PASS
python3 scripts/retention.py --json    → PASS (exit 0; dry-run only)
python3 scripts/metrics_snapshot.py --backend file --json → PASS (exit 0; 49 snapshots, no destructive actions)
git diff --check                       → clean
git status --short                     → only intended files + pre-existing dirty files
git branch --show-current              → master
git remote -v                          → origin https://github.com/wguDataNinja/sjc-intel.git

Ivy (read-only):
git -C ivy-control-vps diff --check    → clean (Ivy working tree left untouched)
```

Backup analysis used safe size commands only (du/tar-to-stdout); no archive
was written to a destination and no deletion occurred.

## 25. Remaining Buddy actions

1. **Choose the external-backup destination** (encrypted volume or object
   store) and approve the `docs/backup-restore.md` §0 policy; run the first
   archive + restore sample.
2. **Decide LICENSE** (MIT recommended) for public publication.
3. **Editorial review pass** on the 78 `pending_review` items for the first
   release; approve the reviewed-only selection.
4. Approve the §3E-G1 VPS admission packet and, separately, the SJSO
   `propose_monitor_update` disposition.
5. Approve the Ivy backup-onboarding patch (§12) and the CONTROL.md update.

## 26. Remaining medium-agent tasks

- `publication-implementation.md` (§3A-G2 corpus validator + selector).
- `silverleaf-scope-registry.md` (§3B-G1).
- `static-public-export.md` (§3B-G2).
- `extract-bcc-workspace-mode.md`.
- `portfolio-integration-context.md` (§3C-G1, authorized cross-repo read-only).

## 27. Remaining privileged Ivy actions

- Apply the backup-disposition checklist item (§12 patch).
- Update `repos/sjc-intel/CONTROL.md` (remote + approved SHA `1be2ade`).
- Refresh VPS capacity after reboot; deploy exact SHA; install
  `sjc-intel-weekly.service` + `.timer` (disabled); transfer route + ack
  observation; run the minutes-from-now test (§18); four shadow runs;
  health registration; rollback rehearsal; then §3F activation decision.

## 28. Risks and unresolved issues

- **External backup destination undecided** — policy is provider-neutral; the
  first archive is blocked on Buddy's destination choice.
- **LICENSE undecided** — public publication cannot be final without it.
- **Review queue backlog** (78 pending, incl. 8 human-review items) is the
  editorial gating item for launch; it is a Buddy/editorial effort, not code.
- **Ivy CONTROL.md stale + uncommitted Ivy control work** — privileged update
  required; not touched.
- **Fresh VPS capacity not re-measured** (Task 10: 83% disk, reboot pending);
  the recommended schedule and shadow runs depend on refreshed evidence.
- **`.opencode/node_modules` (57 MB) prunable** but left to Buddy's explicit
  call.
- **BCC workspace mode + SJSO registry `check_url` change** remain behind
  approved tasks; SJSO capture path is implemented but the registry endpoint
  change still requires the source-review path.
- Queue `summary.yaml` (pre-existing modified state) reports 167 entries / 78
  pending; it reflects the 2026-08-02 catch-up, not a Task 14 change.

## 29. Final Git status

SJC: `master` @ `1be2ade`, origin/master == local. Working tree contains only
intended Task 14 files plus pre-existing dirty data files and Task 12–13
outputs. Nothing staged, committed, or pushed. Ivy: untouched.

## 30. Final task status

| Area | Status |
|------|--------|
| Publish-ready sequence | COMPLETE |
| Repository-cleanup preflight | COMPLETE |
| External-backup policy (SJC) | COMPLETE (destination = Buddy) |
| Ivy backup-onboarding requirement | COMPLETE (patch proposed, not applied) |
| PostgreSQL disposition | COMPLETE (DORMANT_FUTURE_READY) |
| Hermes task-submission model | COMPLETE |
| Scheduling split + test packet + window | COMPLETE |
| Public README + architecture doc | COMPLETE |
| SJSO RSS monitor | COMPLETE (local) |
| Weekly task declaration | COMPLETE |
| Publication implementation (§3A-G2) | READY_FOR_MEDIUM_AGENT |
| VPS deployment / shadow run | BLOCKED (privileged) |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP — all repo-local
deliverables are done and validated; the remaining work is a small set of named
medium-agent tasks, Buddy decisions (backup destination, LICENSE, editorial
review), and the privileged Ivy/VPS packet, none of which require further broad
architecture rediscovery.
