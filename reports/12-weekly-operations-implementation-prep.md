# Task 12 — Weekly Operations Implementation Preparation

**Task identity:** 12-weekly-operations-implementation-prep.md
**Date:** 2026-08-03
**Repository:** SJC_Intel (`/Users/buddy/projects/sjc_intel`)
**Repositories inspected (read-only):** Ivy Control VPS (`/Users/buddy/projects/ivy-control-vps`)
**Final status:** COMPLETE_WITH_FOLLOW_UP

## 1. Executive result

SJC_Intel now has a precisely documented bounded weekly VPS/Hermes operational
workflow, a versioned transfer-bundle contract, and a working local
bundle/import foundation with tests — with the weekly workflow permanently
separated from source promotion, publication, taxonomy change, and corpus
mutation.

Delivered:

- `docs/weekly_operational_contract.md` — the authoritative weekly contract
  (inputs, Stage A canonical monitoring, Stage B bounded discovery, outputs,
  runtime controls, review boundary, and the transfer-bundle/receipt/prune
  semantics).
- `schemas/bundle_manifest.schema.yaml` — bundle manifest field spec.
- `scripts/bundle_build.py`, `scripts/bundle_verify.py`,
  `scripts/bundle_import.py`, `scripts/bundle_common.py` — producer-side
  builder, both-sides verifier, and idempotent Mac staging importer.
- `tests/fixtures/bundle_workspace/`, `tests/fixtures/sample_bundle/`,
  `tests/test_bundle.py` — deterministic sample bundle + 11 tests.
- `prompts/sjc_weekly_ops_task.md` — bounded repository-side Hermes weekly
  task specification.
- ROADMAP.md §3E now carries the exact contract/tooling references and the
  decomposed builder tasks; §8 notes the foundation is already landed.

Nothing was deployed, published, promoted, committed, or pushed. No VPS,
PostgreSQL, systemd, or secrets state was touched. Pre-existing dirty data
files were left untouched.

## 2. Starting Git and remote state

| Item | Observed |
|------|----------|
| Current branch | `master` |
| Current HEAD | `1be2ade` (docs: define SilverLeaf publication and execution roadmap) |
| Working tree | Dirty (pre-existing, not from this task): `data/intel_items/2026-07-06/agentic_search_results.yaml`, `data/review_queue/queue.yaml`, `data/review_queue/summary.yaml`; plus untracked `reports/11-...` and `tasks/12-...` |
| Configured remotes | `origin https://github.com/wguDataNinja/sjc-intel.git` (fetch + push) |
| origin/master now exists? | **Yes** — `git ls-remote --heads origin master` → `1be2ade2ad600627e69bca382e47af54a4690363`, identical to local HEAD |
| SHA 1be2ade present remotely | Yes (as `origin/master`) |
| GitHub main content | Unrelated root history: single `Initial commit` (33b65a6) containing only `LICENSE` (1 file). No common ancestor with master. |
| Can master be pushed safely? | Already pushed; local master == origin/master (0 ahead / 0 behind). No overwrite of main is possible (disjoint histories), and no force-push is needed or authorized. |

**Authentication:** No longer blocked. The push that Task 11 could not complete
has since succeeded. No minimal Buddy action is required for the remote;
Buddy only needs to update the Ivy control record with the deployed SHA when
admission proceeds (a privileged step).

## 3. Sources and current monitor capabilities

Canonical sources in `registry/sources.yaml` (28 records; active/verified
eligible for Stage A):

| Source | Method | Cadence | Pilot status | Current outputs |
|--------|--------|---------|--------------|-----------------|
| `sjc_nbor_public_notices` | **Deterministic script** `scripts/extract_nbor.py` (plain HTTP GET) | daily | Extractor ready; pilot 2026-06-08 (25 records) | intel_items + source_event + fixture |
| `sjc_bcc_calendar` | **Deterministic script** `scripts/extract_bcc_agenda.py` | weekly | Spec ready; BCC pilot 2026-06-26 | intel_items + source_event |
| `sjc_county_news` | Prompt-led / manual (no script) | daily | Pilot passed 2026-06-03 | intel_items + source_event |
| `sjso_news_stories` | Prompt-led / manual (no script) | daily | Pilot passed 2026-06-03 | intel_items + source_event |
| `sjc_utility_department` | Manual (no script) | daily | Daily-ready | source_event only |
| `sjc_emergency_management` | Manual | daily/seasonal | Designed | none |
| `sjc_school_stack` (`sjcsd_boarddocs`, `sjc_school_district`) | Prompt-led | weekly | Pilot run 2026-06-03 | intel_items |
| Other 20 canonical | Manual / investigation | weekly-monthly | Mixed | varies |

- **Deterministic scripts:** only `extract_nbor.py` and `extract_bcc_agenda.py`.
- **Prompt-led / manual:** county_news, SJSO, utility, emergency, school stack.
- **Pilots passed:** `sjc_county_news`, `sjso_news_stories` (2026-06-03),
  `sjc_nbor_public_notices` (extractor pilot 2026-06-08), utility daily-ready,
  school stack pilot.
- **Where dedupe and review-queue rebuild occur:** Mac-only.
  `data/index/prior_items.yaml` via `scripts/rebuild_dedupe_index.py` /
  `update_dedupe_index.py`; `data/review_queue/queue.yaml` via
  `scripts/build_review_queue.py` / `batch_review_queue.py`.
- **What outputs each monitor currently creates:** per-source YAML under
  `data/intel_items/{date}/{source}.yaml` + `data/source_events/{date}/{source}.yaml`;
  these are **corpus paths the VPS must never write**.
- **Assumptions currently requiring local execution:** all live fetching and
  extraction runs on the Mac; extraction scripts hardcode corpus output paths;
  dedupe/queue rebuilds are Mac-side; prior dedupe state must be shipped to the
  VPS as a read-only payload; no VPS runtime, service, or timer exists.

## 4. Recommended initial two-source pilot

**Recommendation: `sjc_nbor_public_notices` + `sjc_county_news`.**

Evidence:

- **`sjc_nbor_public_notices`** — the only canonical source with a
  deterministic stdlib-only script (`extract_nbor.py`) using a single plain
  HTTP GET of server-rendered HTML (no JS, no auth). Highest proven yield (25
  records/single fetch). Classification is mostly low-sensitivity
  (transportation/infrastructure/permits); only contested hearings rise to
  medium. It is the strongest deterministic anchor for a VPS shadow run.
- **`sjc_county_news`** — pilot passed, WordPress plain-HTTP GET (no JS),
  county-government press releases, predominantly low sensitivity and low
  human-review-flag density. It shares the `known_source_monitor_task` prompt
  path with SJSO but is safer than SJSO, whose public-safety content defaults
  to medium sensitivity with more `human_review_required` flags.

Explicitly **not** chosen: `sjso_news_stories` (public-safety sensitivity
concentration), `sjc_utility_department` and `sjc_emergency_management` (no
script, manual), `sjc_bcc_calendar` (agenda/PDF handling, weekly meeting
dependency).

Both chosen sources transfer **candidates only**; neither pilot can promote,
publish, or touch the corpus.

## 5. Weekly operational contract

`docs/weekly_operational_contract.md` defines:

- **Inputs:** approved canonical sources, source-registry revision pin,
  tracked entities, search profiles, taxonomy/config revision, run time window,
  prior dedupe state, explicit runtime budget.
- **Stage A — canonical-source monitoring:** source-health results, source
  events, normalized intelligence candidates (marked `candidate`), source URLs,
  evidence excerpts, duplicate/no-match/partial/failed outcomes, and bounded
  raw captures only where required. Candidates are never `verified`.
- **Stage B — bounded source discovery:** proposals only, with the full
  candidate-ID/URL/family/authority/evidence/relevance/geography/gap/
  disposition/confidence/review-status contract.
- **Outputs:** exact artifact classes and proposed bundle paths.
- **Runtime controls:** one run ID, one writer, duplicate-run prevention, max
  runtime, retry ceiling, query/fetch ceiling, token/cost ceiling, partial-run,
  failure, no-match, restart/replay, and stop conditions.
- **Review boundary:** `candidate ≠ verified`, `verified ≠ published`,
  `source proposal ≠ canonical source`.

## 6. Bounded source-discovery contract

Stage B is bounded to one discovery pass using the selected search profile
(default `sl_core`). It may search for newly relevant public sources, missing
coverage, moved/replaced sources, SilverLeaf-specific sources, and gaps across
schools/roads/utilities/development/government/communities/tracked entities.
Proposals carry the full §4.1 contract and a `review_status: candidate`. Stage B
is prohibited from promoting into `registry/sources.yaml`, removing sources,
changing taxonomy/scope, publishing, or treating social media as sole
consequential evidence. Documented in `docs/weekly_operational_contract.md` §4.

## 7. Bundle and manifest contract

`docs/weekly_operational_contract.md` §7 defines bundle schema `1.0`:

```
bundle/
  manifest.json          # schema version, run_id, git SHA, registry pin, window,
                         # retention_deadline, run_status, included_files,
                         # bundle_total_bytes, candidate_counts, failure_counts,
                         # replay_identity
  checksums.sha256       # sha256, two-space format, sorted; covers manifest.json
  run.json               # run record + failure summary + next_check_after
  source_health/         # {source_id}.json
  source_events/         # {source_id}.json
  intel_candidates/      # {source_id}.json
  source_proposals/      # proposals.json
  logs/                  # run.log
```

Semantics specified: deterministic layout; SHA-256 checksums; duplicate-bundle
idempotency keyed by `run_id`; partial-transfer rejection; safe replay by
`replay_identity`; import-failure behavior (no receipt, no corpus write, no
LAST_RUN advance, no prune); Mac-offline retention; acknowledgement format
(`data/receipts/{run_id}.receipt.json`, `receipt_schema_version 1.0`,
`status: acknowledged`); delayed-prune eligibility (verified receipt matching
`bundle_sha256` **plus** `retention_deadline` elapsed, default `window_end +
14d`); and the prohibition on pruning before verified acknowledgement. These
satisfy Ivy's off-VPS bundle-transfer admission requirement verbatim.

## 8. Local tooling implemented

All new, stdlib-only, no network in tests:

| Tool | Purpose | Command |
|------|---------|---------|
| `scripts/bundle_common.py` | Shared constants/helpers | — |
| `scripts/bundle_build.py` | Assemble bundle + run.json + manifest + checksums (producer side) | `python3 scripts/bundle_build.py --workspace ... --out ... --run-id ... --git-sha ... --profile ... --registry-revision ... --window-start ... --window-end ... [--status ...]` |
| `scripts/bundle_verify.py` | Full integrity/contract verification (both sides) | `python3 scripts/bundle_verify.py --bundle <dir>` |
| `scripts/bundle_import.py` | Idempotent Mac staging import + receipt | `python3 scripts/bundle_import.py --bundle <dir> [--incoming-root data/incoming] [--receipt-root data/receipts] [--git-sha ...]` |

Design guarantees: import writes **only** under the incoming and receipt roots
(`data/incoming/{run_id}/`, `data/receipts/{run_id}.receipt.json`); it never
touches the authoritative corpus (`data/intel_items/`, `data/source_events/`,
`data/review_queue/`, `data/index/`), never runs when verification fails, and
returns a conflict on same-`run_id` different-content. Sample bundle fixture
`tests/fixtures/sample_bundle/` (build workspace at
`tests/fixtures/bundle_workspace/`) verifies as PASS; 11 new tests
(`tests/test_bundle.py`).

## 9. Hermes weekly task specification

`prompts/sjc_weekly_ops_task.md` is the reusable repository-side execution
contract. It tells VPS Hermes exactly: the repository revision to run (pinned
SHA + clean tree); sources to monitor; discovery profile; data it may read;
files it may write (run workspace + bundle only, with an explicit forbidden-path
list); commands it may run; permitted network access (public HTTP(S) only); what
it must never change; runtime/cost/retry/scope limits; expected bundle outputs;
report/run-log requirements; and stop/escalation conditions. It explicitly
separates repository-side contract from Ivy-side credentials, systemd
scheduling, and privileged deployment, and does not claim an unverified Hermes
runtime capability.

## 10. Ivy compatibility assessment

Read-only review of `repos/sjc-intel/CONTROL.md`, `docs/VPS_ADMISSION_CHECKLIST.md`
(including its bundle-transfer addition), `docs/HERMES_ORCHESTRATION_CONTRACTS.md`,
`docs/VPS_ACCESS.md`, and the general tools/templates.

- **Fit:** the proposed weekly contract matches the generic Ivy process. Every
  item in Ivy's off-VPS bundle-transfer admission addition is addressed by
  `docs/weekly_operational_contract.md` §7 (versioned manifest with producer
  revision/run ID/counts/byte bounds/checksums/`retention_deadline`; pull/import
  outside the checkout; idempotent import + replay identity; receipt only after
  verification + successful import; acknowledgement observation; prune
  predicate = verified receipt + retention delay; offline/partial/duplicate/
  failed/lost-ack/disk-pressure behaviors; manual proof + timer-disabled gate).
- **Reusable Ivy components:** `tools/verify_exact_sha.sh`,
  `tools/vps_paths.sh`, `tools/check_vps_readiness.sh`,
  `tools/report_deployed_revision.sh`, `tools/plan_rollback.sh`,
  `docs/VPS_ADMISSION_CHECKLIST.md`, `templates/exact-sha-deployment-checklist.md`,
  `templates/vps-config.env.example`, `deploy/systemd` naming conventions,
  health contract (`docs/HEALTH_CONTRACT.md`, `scripts/health_export.py`).
- **Project-specific work required:** deployable exact-SHA payload; a
  `run_weekly.sh` wrapper; bundle/import tooling already shipped; extractor
  workspace-output mode (see §18); shadow-run sequence; ack observation path.
- **Missing Ivy helpers/templates:** none blocking; a dedicated transfer/ack
  endpoint is a privileged Ivy addition, not a repo item.
- **Contradictions/stale docs:** `repos/sjc-intel/CONTROL.md` is stale — it
  reports `remote: null`, approved SHA `35a0246`, and `state: source-only`,
  while the local checkout now has `origin` configured and `origin/master` at
  `1be2ade`. Updating CONTROL.md is a privileged cross-repo change (in the
  packet, not performed here).
- **Exact privileged changes required:** itemized in §11.
- **PostgreSQL:** provides no concrete value for the first file-only
  deterministic workflow (§12).

## 11. Exact privileged VPS packet

For a later authorized Ivy operator / Strong Codex execution. Items marked
(verify) require live confirmation at admission time. This task performed no
privileged mutation.

1. **Deployable remote and exact SHA:** `git@github.com:wguDataNinja/sjc-intel.git`
   (or HTTPS), branch `master`; SHA `1be2ade2ad600627e69bca382e47af54a4690363`
   (refreshed at admission; deploy whatever SHA the control record pins after
   Buddy approval).
2. **VPS checkout path:** `/home/scraper/apps/sjc-intel` (task 10 showed SJC
   absent from `/home/scraper/apps`).
3. **Service account:** `scraper` (existing VPS user, per `docs/VPS_ACCESS.md`).
4. **Directories** (owned by `scraper`):
   - `/home/scraper/apps/sjc-intel` (checkout; read-only during runs)
   - `/home/scraper/data/sjc-intel/workspace` (per-run workspace; 0700)
   - `/home/scraper/data/sjc-intel/bundles` (ready-to-transfer bundles; 0750)
   - `/home/scraper/data/sjc-intel/archive` (retained bundles)
   - `/home/scraper/data/sjc-intel/ack` (receipt copies from Mac)
   - `/home/scraper/data/sjc-intel/health` (health JSON)
   - `/home/scraper/data/sjc-intel/logs`
5. **Permissions:** `scraper` owner; workspace 0700, bundles 0750, health/logs
   0750.
6. **Python environment:** `/home/scraper/apps/sjc-intel/.venv`.
7. **Dependency command:**
   `cd /home/scraper/apps/sjc-intel && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
8. **Environment variables and secret names (values never committed):**
   `SJC_INTEL_VPS_PROFILE`, `SJC_INTEL_VPS_RUN_ID`, `SJC_INTEL_VPS_WINDOW_START`,
   `SJC_INTEL_VPS_WINDOW_END`, `SJC_INTEL_VPS_REGISTRY_REV`,
   `SJC_INTEL_DATA_ROOT=/home/scraper/data/sjc-intel` via
   `/home/scraper/config/sjc_intel.env` (per `deploy/env.example`). **No
   credentials are required for the two-source public-HTTP pilot.**
9. **Hermes provider requirement:** none for the deterministic two-source
   shadow run. A model provider + token budget is required only if agentic
   discovery (Stage B) is later included; do not claim that capability.
10. **Manual invocation command (shadow, no timer):**
    ```
    cd /home/scraper/apps/sjc-intel && \
    .venv/bin/python scripts/run_weekly.py \
      --workspace /home/scraper/data/sjc-intel/workspace \
      --out /home/scraper/data/sjc-intel/bundles/${SJC_INTEL_VPS_RUN_ID} \
      --run-id ${SJC_INTEL_VPS_RUN_ID} \
      --git-sha 1be2ade --profile ${SJC_INTEL_VPS_PROFILE} \
      --registry-revision 1be2ade \
      --window-start ${SJC_INTEL_VPS_WINDOW_START} \
      --window-end ${SJC_INTEL_VPS_WINDOW_END}
    ```
    (Note: `scripts/run_weekly.py` and an extractor workspace-output mode are
    the remaining medium-agent implementation; the privileged operator should
    verify these exist in the pinned SHA before deployment.)
11. **systemd service design:** `sjc-intel-weekly.service` — `User=scraper`,
    `EnvironmentFile=/home/scraper/config/sjc_intel.env`,
    `ExecStart=/home/scraper/apps/sjc-intel/run_weekly.sh`,
    `TimeoutStartSec=0`, `TimeoutStopSec=30`.
12. **Weekly timer design:** `sjc-intel-weekly.timer` — `OnCalendar=Mon
    *-*-* 03:00:00` (staggered; verify against active workloads),
    `Persistent=false`, `RandomizedDelaySec=15m`. **Remains disabled until the
    activation gate.**
13. **Lock method:** `flock -n /home/scraper/data/sjc-intel/.weekly.lock` plus
    run_id existence check in the workspace `run.json`.
14. **Timeout:** 2 hours wall-clock (matches contract §8).
15. **Resource limits:** `MemoryMax=1G`, `CPUQuota` deferred to capacity
    evidence, `Nice=10`.
16. **Logs:** journald + `/home/scraper/data/sjc-intel/logs/{run_id}.log`; the
    bundle carries `logs/run.log`.
17. **Health output:** `/home/scraper/data/sjc-intel/health/sjc_intel.health.json`
    (reuse `scripts/health_export.py`, sanitized format per Ivy health contract).
18. **Bundle output path:** `/home/scraper/data/sjc-intel/bundles/{run_id}/`
    (layout per §7).
19. **Mac pull contract:** Mac runs
    `scp -r scraper@ih-market-vps:/home/scraper/data/sjc-intel/bundles/{run_id}/ data/incoming/`,
    then `python3 scripts/bundle_verify.py --bundle data/incoming/{run_id}` then
    `python3 scripts/bundle_import.py --bundle data/incoming/{run_id}`.
20. **Receipt/acknowledgement path:** importer writes
    `data/receipts/{run_id}.receipt.json`; the puller copies it back to
    `/home/scraper/data/sjc-intel/ack/{run_id}.receipt.json` (this is the
    producer-observed acknowledgement).
21. **Retention period:** `retention_deadline` (default `window_end` + 14 days).
22. **Delayed-prune command (privileged, separate from the run):** verify
    `ack/{run_id}.receipt.json` exists and `bundle_sha256` matches, verify
    `now >= retention_deadline`, archive to `/home/scraper/data/sjc-intel/archive`,
    then remove `bundles/{run_id}`.
23. **Rollback:** disable timer, redeploy prior pinned SHA, restore prior bundle
    from archive, replay by `replay_identity`, no prune without receipt.
24. **Shadow-run sequence:** 4 manual invocations of step 10; each verified by
    `scripts/bundle_verify.py` and imported on Mac with receipts; manifests,
    checksums, and receipts reconciled; then natural run under §3F.
25. **Activation gates:** ROADMAP §3F — four healthy shadow runs + seven-day
    healthy evidence + Buddy/Ivy approval before the timer is enabled.

## 12. PostgreSQL recommendation

**No SJC PostgreSQL for the first weekly workflow.** Option B (locks, run/source
health, transfer manifests/acknowledgements) would add value only under
multi-writer contention or long retention histories. A single scheduler/writer
on one VPS is fully served by the file lock, `run.json`, bundle manifests, and
receipt files. PostgreSQL remains deferred per ROADMAP §5 and `VPS_ROADMAP.md`.
The existing `scripts/pg_adapter.py` / migrations stay dormant.

## 13. Validation results

```
python3 -m pytest tests/ -v                 → PASS, 120 passed (109 pre-existing + 11 new bundle tests)
python3 scripts/validate.py                 → PASS — ALL PASSED
python3 scripts/portability_check.py        → PASS
git diff --check                            → clean (exit 0)
git status --short                          → only intended new files + pre-existing dirty data files
git branch --show-current                   → master
git remote -v                               → origin https://github.com/wguDataNinja/sjc-intel.git (fetch/push)
scripts/bundle_verify.py --bundle tests/fixtures/sample_bundle → PASS (all 9 checks)
scripts/bundle_import.py standalone run     → staged + receipt; second run idempotent
```

No live production sources were fetched; no VPS, PostgreSQL, service, secret,
timer, commit, or push was performed.

## 14. Files changed

Added:

- `docs/weekly_operational_contract.md`
- `prompts/sjc_weekly_ops_task.md`
- `schemas/bundle_manifest.schema.yaml`
- `scripts/bundle_common.py`
- `scripts/bundle_build.py`
- `scripts/bundle_verify.py`
- `scripts/bundle_import.py`
- `tests/fixtures/bundle_workspace/*`
- `tests/fixtures/sample_bundle/*`
- `tests/test_bundle.py`

Modified:

- `ROADMAP.md` (§3E-G1/G2 contract rows; new §3E-G3 foundation table; §8 note)

Pre-existing dirty/untracked files preserved (not staged): `ROADMAP.md` was the
only tracked file intentionally modified by this task. The modified
`data/intel_items/2026-07-06/agentic_search_results.yaml`,
`data/review_queue/queue.yaml`, `data/review_queue/summary.yaml` and untracked
`reports/11-operational-admission-continuation.md`,
`tasks/12-weekly-operations-implementation-prep.md` were pre-existing and left
untouched. Nothing was committed.

## 15. Remaining Buddy actions

1. No remote/auth action needed — origin/master already exists at `1be2ade`.
2. When proceeding: approve the §3E-G1 admission packet (exact SHA, two-source
   selection, transfer/rollback plan) as the high-reasoning VPS gate.
3. Editorial/publication gate remains separate and independent of this work.

## 16. Remaining privileged actions

1. Update `repos/sjc-intel/CONTROL.md` in Ivy Control VPS (remote, deployed
   SHA `1be2ade`, state).
2. Refresh live VPS capacity (Task 10: 83% disk, reboot pending) and
   workload-window assessment.
3. Clone/deploy exact SHA; create directories/permissions; venv + deps.
4. Install `sjc-intel-weekly.service` + `.timer` (timer **disabled**).
5. Provide transfer route + ack observation (`/home/scraper/data/sjc-intel/ack`).
6. Run 4 manual shadow runs; reconcile manifests/checksums/receipts.
7. Health registration; delayed-prune procedure; rollback rehearsal.
8. Only then, separate timer-enablement decision per §3F.

## 17. Next medium-agent tasks

From ROADMAP §3E-G3 (foundation already landed; no rediscovery required):

- **13-candidate-to-corpus-import.md** (medium, non-privileged): deterministic,
  human-gated promotion of bundle candidates from `data/incoming/{run_id}/` into
  `data/intel_items/` + `data/review_queue/` with dedupe and replay safety;
  **never automatic**. Also add a workspace-output mode to
  `scripts/extract_nbor.py` (and a bundle-ready `scripts/run_weekly.py`) so the
  deterministic extractor writes to the run workspace instead of corpus paths.
- **14-vps-admission-packet.md** (§3E-G1, privileged): execute §11 packet —
  exact-SHA deployment, systemd unit, disabled weekly timer, lock, capacity
  evidence, secrets route, transfer endpoint, rollback.
- **15-shadow-run-proof.md** (§3E-G2, privileged): four healthy shadow runs,
  receipt reconciliation, prune-gate evidence.

The launch sequence (publication contract §3A-G2, SilverLeaf registry §3B-G1,
static export §3B-G2, portfolio UI §3C) is unaffected and independent of this
operational work.

## 18. Risks and unresolved issues

- **`extract_nbor.py` writes to corpus paths** (`data/intel_items/`,
  `data/source_events/`, and the fixture) and is therefore not bundle-safe as
  written. A workspace-output mode is a required medium task before the shadow
  run (item 13).
- **`sjc_county_news` has no deterministic script**; its shadow-run extraction
  is prompt-led. The pilot's determinism claim is scoped to the bundle layout,
  checksums, and verification, with NBOR as the deterministic anchor. Flagged so
  the §3E-G1 evidence names this.
- **Ivy CONTROL.md is stale** (no remote, SHA 35a0246, source-only) versus the
  real pushed `origin/master @ 1be2ade`. Privileged update required.
- **Capacity evidence is stale** (Task 10: 83% disk, reboot pending, active
  unrelated workloads). Refresh before any deployment.
- **Hermes provider auth is not configured**; the deterministic pilot does not
  need it, but any future agentic discovery does — do not claim that runtime.
- Retention default is 14 days (configurable); prune still requires a verified
  receipt regardless of date.
- This report and its task file are untracked and uncommitted by design.

## 19. Final status

| Area | Status |
|------|--------|
| Weekly operational contract | COMPLETE |
| Source-discovery contract (proposals-only) | COMPLETE |
| Bundle + manifest contract | COMPLETE |
| Bundle tooling (build/verify/import) | COMPLETE |
| Sample fixture + tests | COMPLETE |
| Hermes weekly task spec | COMPLETE |
| Ivy compatibility assessment | COMPLETE |
| Privileged VPS packet | COMPLETE (documented, not executed) |
| PostgreSQL recommendation | COMPLETE (defer) |
| Roadmap elaboration | COMPLETE |
| Git remote state | COMPLETE (origin/master @ 1be2ade) |
| Candidate→corpus import tooling | READY_FOR_MEDIUM_AGENT |
| Extractor workspace-output mode | READY_FOR_MEDIUM_AGENT |
| VPS deployment / shadow run | BLOCKED (privileged; awaiting admission gate) |

**Final status vocabulary:** COMPLETE_WITH_FOLLOW_UP — all task-12 deliverables
are done and validated; the remaining work is deliberately out of scope
(privileged VPS admission) or decomposed into named medium-agent tasks.
