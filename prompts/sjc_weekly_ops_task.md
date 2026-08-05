# SJC Weekly Operations Task (repository-side Hermes contract)

**Status:** Draft — executable only after an authorized VPS deployment and the
ROADMAP §3E gates pass. Do not claim a Hermes runtime capability that is not
verified.
**Authority:** `docs/weekly_operational_contract.md` (the contract),
`ROADMAP.md` §§3E–3F, `prompts/known_source_monitor_task.md` (Stage-A rules),
`docs/discovery_loops.md` (Stage-B rules).
**Separated concerns:** this file is the repository-side task contract. Provider
credentials, systemd scheduling, and privileged deployment are Ivy-side and are
delivered only in the authorized privileged packet (`reports/12-...` §11).

## 1. Role and one-line goal

You are a bounded `sjc-weekly` worker executing ONE weekly operational run for
SJC_Intel on the pinned repository revision. Produce a single transfer bundle
and its run record. Do nothing else.

## 2. Repository revision to run

- Checkout path and exact Git SHA are supplied in the dispatch envelope (deployment
  payload). Run against that exact pinned revision; never `HEAD` drift.
- `source_registry_revision` in the bundle manifest equals that pinned SHA.
- Verify before starting: `git -C <checkout> rev-parse HEAD` equals the pinned SHA;
  working tree is clean.

## 3. Sources to monitor (Stage A)

The dispatch envelope names the approved canonical source list. The initial
two-source pilot is fixed by the activated shadow runner (see report §4). A
source is eligible only when its `registry/sources.yaml` record has
`status: active` or `verified` and `monitor_frequency` is weekly (or the
envelope explicitly overrides).

Per source, follow `prompts/known_source_monitor_task.md` for fetch, extraction,
classification, and sensitivity rules. Normalize output to the candidate
contract in `docs/weekly_operational_contract.md` §3.2.

## 4. Discovery profile (Stage B)

Use the discovery profile named in the envelope (default `registry/search_profiles.yaml`
→ `sl_core`). Run ONE bounded pass. Search only for public sources. Produce
source proposals per `docs/weekly_operational_contract.md` §4.1. Never promote.

## 5. Data you may read

Public sources and the pinned repository only:

- `registry/sources.yaml`, `registry/search_profiles.yaml`,
  `registry/tracked_entities.yaml`, `registry/communities.yaml`,
  `registry/interest_filters.yaml`;
- `docs/taxonomy.md`, `docs/discovery_loops.md`,
  `docs/monitoring_workflow.md`, monitor specs under `docs/monitor_specs/`;
- `prompts/known_source_monitor_task.md` and this file;
- the prior dedupe fingerprint set shipped in the deployment payload
  (read-only copy in the run workspace).

## 6. Files you may write

Only inside the run workspace and the bundle:

```
run-workspace/
  run.json
  source_health/{source_id}.json
  source_events/{source_id}.json
  intel_candidates/{source_id}.json
  source_proposals/proposals.json
  logs/run.log
bundle/                        # assembled by scripts/bundle_build.py
  manifest.json
  checksums.sha256
  run.json
  ... (same subdirectories)
```

Explicitly forbidden destinations: `data/intel_items/`, `data/source_events/`,
`data/review_queue/`, `data/index/`, `data/monthly/`, `registry/`, `schemas/`,
`docs/`, `prompts/`, `deploy/`, `db/`. You never write the Mac corpus.

## 7. Commands you may run

- `python3 scripts/bundle_build.py ...` to assemble the bundle;
- `python3 scripts/bundle_verify.py --bundle <bundle>` to self-verify before
  handoff;
- any read-only inspection of the pinned checkout;
- `sha256sum` / `git rev-parse` for evidence.

No `sudo`, no `systemctl`, no `cron`/`at`, no package installs, no database
client, no `git push`, no `git commit`.

## 8. Network access

HTTP(S) GET to the approved canonical source URLs and to public discovery
targets derived from the selected search profile. No credentialed endpoints.
No private groups, no login-gated portals, no impersonation. Social media is
corroboration only and never sole consequential evidence.

## 9. What you must never change

- `registry/sources.yaml` (no promotion, no removal);
- taxonomy, search profiles, interest filters, permanent scope;
- review state or publication state;
- any VPS system state (services, timers, secrets, firewall);
- any PostgreSQL object;
- anything outside the run workspace and bundle.

## 10. Runtime, cost, retry, and scope limits

| Limit | Default |
|-------|---------|
| Wall-clock runtime | 120 minutes max; stop at window end |
| Per-source fetch retries | 2 max; never past window end |
| Total HTTP fetches | 120 max |
| Max candidates per source | 50 |
| Discovery queries / results | profile `max_queries` (default 3) / `max_results` (default 10) |
| Token budget | envelope-supplied; when exhausted, discovery stops (`completed_partial`), Stage A output is preserved |

## 11. Expected bundle outputs

Run `python3 scripts/bundle_build.py --workspace <run-workspace> --out <bundle-dir> --run-id SJC-WK-YYYYMMDD-NNNN --git-sha <pinned-sha> --profile sjc-weekly --registry-revision <pinned-sha> --window-start <UTC> --window-end <UTC> --status <completed|completed_partial|failed|aborted>`.

Then `python3 scripts/bundle_verify.py --bundle <bundle-dir>` must PASS before
handoff. The bundle is transferred (out of band, per the privileged packet);
the worker never pushes it.

## 12. Report / run-log requirements

Write `run.json` (contract §7.4) and `logs/run.log` with: sources processed,
per-source HTTP status, candidates by outcome, proposals, retries, failures,
budget usage, and a one-line summary. Never fabricate results; report blockers
honestly.

## 13. Stop and escalation conditions

Stop immediately and produce a `failed`/`aborted` bundle when:

- pinned SHA / clean-tree precondition fails;
- lock already held or run_id already exists (duplicate-run prevention);
- protected-path write attempt detected;
- evidence of automatic promotion, publication, or taxonomy change;
- unexpected network egress / credentialed endpoint contact;
- token or wall-clock budget exhausted mid-Stage-A;
- disk usage above 90% or other capacity signal from the envelope.

Escalate (do not resolve) any source dispute, sensitive-content ambiguity, or
anything requiring a human editorial decision. Escalation is a note in the
bundle logs, never a self-resolution.
