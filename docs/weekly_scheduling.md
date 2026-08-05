# SJC_Intel — Weekly Scheduling and Hermes Task-Submission Model

**Status:** Authoritative supporting reference for how SJC declares and schedules
its weekly operational task.
**Authority:** `docs/weekly_operational_contract.md` (run contract),
`ROADMAP.md` §§3E–3F (gates), `deploy/sjc-weekly-task.yaml` (task declaration).
**Last reconciled:** 2026-08-03 (Task 14).

## 1. Hermes runtime reality

Verified facts (report 10, `ivy-control-vps/docs/HERMES_OPERATOR_GUIDE.md`):

- Hermes Agent v0.18.2 is installed on the VPS as a **read-only** resident
  assistant; provider authentication is **not** configured.
- Hermes observes, inspects, summarizes, and produces bounded bridge artifacts.
  It has no production write authority and is not a general task executor.

**Consequence:** the SJC weekly run is executed by a **deterministic runner**
(`scripts/run_weekly.py`) — no model provider is required for Stage A. Hermes
may read and coordinate, but it does not execute the run. This document does
not claim an unverified Hermes runtime capability.

## 2. Reusable repository-to-task model

The preferred model, consistent with current Ivy conventions:

```
project repo
  declares task specification        deploy/sjc-weekly-task.yaml (+ prompts/sjc_weekly_ops_task.md)
        ↓
Ivy admission/review                 VPS_ADMISSION_CHECKLIST + CONTROL.md
        ↓
Ivy deploy manifest references task  exact SHA + systemd unit EnvironmentFile
        ↓
systemd service invokes the runner   sjc-intel-weekly.service → run_weekly.py
        ↓
systemd timer controls schedule      sjc-intel-weekly.timer (disabled until gates)
        ↓
project output contract governs      docs/weekly_operational_contract.md §7 (bundle)
```

### 2.1 Responsibility split

| Owner | Owns |
|-------|------|
| **Repository (SJC)** | Task declaration (`deploy/sjc-weekly-task.yaml`), prompt (`prompts/sjc_weekly_ops_task.md`), runner + extractors, output/bundle contract, tests, validation, run/import tooling, operator guide. |
| **Ivy (privileged)** | Admission/review, exact-SHA deployment, service + timer units, enablement, schedule + randomized delay, environment file, resource limits, health registration, secrets route, rollback, backup disposition, prune procedure. |
| **Buddy** | Activation decision after §3E-G2 evidence; editorial/source decisions. |

## 3. Weekly task scope (declared)

`deploy/sjc-weekly-task.yaml` declares:

- task ID `sjc-weekly-001`, enabled `false`;
- approved sources: `sjc_nbor_public_notices` (deterministic), `sjso_news_stories`
  (verified RSS 2.0), with `sjc_county_news` reserved (prompt-led, no script);
- discovery: `sl_core` profile, proposals only;
- runtime limits: 120 min wall clock, 120 fetches, retry ceiling 2, 50
  candidates/source, no token budget (deterministic Stage A), explicit stop
  conditions;
- outputs: run.json, source health/events/candidates, bundle at
  `/home/scraper/data/sjc-intel/bundles`, health JSON, logs;
- secrets: **none required** (public HTTP only);
- schedule recommendation and activation gates.

Stage A produces source health, source events, candidates with
duplicate/no-match/partial/failed outcomes, and bundle artifacts. Stage B
produces source proposals only. The run never promotes sources, changes
taxonomy, publishes, edits reviewed corpus, or bypasses human review.

## 4. Ivy-side scheduling authority

Ivy owns the systemd service and timer units, enablement, exact schedule,
randomized delay, environment, resource limits, deployed SHA, health, and
rollback. The timer remains **disabled** until the §3E/§3F activation gates
pass (admission packet, four healthy shadow runs, seven-day healthy window).
No agent enables a timer without explicit authority.

## 5. Minutes-from-now automation test packet

Purpose: prove timer activation → service invocation → deterministic run →
output creation → logging → health → bundle generation → transfer readiness
without waiting a week. Execution is privileged (systemd) and is **not run by
this agent**; this is the exact packet for the authorized Ivy operator.

1. Deploy the pinned exact SHA (`git -C /home/scraper/apps/sjc-intel rev-parse HEAD`
   must equal the approved SHA).
2. Create a transient test override (never touching the permanent unit):
   ```bash
   systemctl --user set-property sjc-intel-weekly.service \
     Environment="SJC_INTEL_VPS_RUN_ID=SJC-WK-TEST-<DATE>-0001"
   ```
   or a transient timer:
   ```bash
   systemctl --user start sjc-intel-weekly.timer
   systemctl --user list-timers sjc-intel-weekly.timer
   # Record the exact next-elapse time; or use:
   # systemd-analyze calendar 'Wed *-*-* 01:30:00' to confirm the template,
   # then create a one-shot override at now + 3 minutes.
   ```
   A one-shot test can be scheduled minutes ahead with a transient unit:
   ```bash
   systemd-run --user --on-calendar "now + 3min" \
     --unit sjc-intel-weekly-test-$(date +%s) \
     /home/scraper/apps/sjc-intel/run_weekly.sh
   ```
3. Before the test, record: exact start time, expected completion window
   (start + 120 min max), and current bundle/health/log state.
4. After elapse, verify:
   - `systemctl --user status sjc-intel-weekly-test-*` → success exit;
   - `logs/` contains the run log with `run_status`; 
   - health JSON exists at the declared health path;
   - bundle exists at the bundle root with `manifest.json` + `checksums.sha256`;
   - `scripts/bundle_verify.py` passes locally on the produced bundle;
   - no corpus/registry mutation on the VPS.
5. Disable/clean the test unit:
   ```bash
   systemctl --user stop sjc-intel-weekly-test-*.timer 2>/dev/null
   systemctl --user reset-failed sjc-intel-weekly-test-* 2>/dev/null
   ```
6. Rollback: redeploy the prior SHA and restore the prior bundle; never prune
   without a verified receipt.

Duplicate-run prevention: `run_weekly.py` rejects an existing run ID, and the
service uses `flock` on the lock path — a second concurrent invocation exits.

## 6. Recommended recurring weekly window

**Recommended: `Wed 01:30–03:00 UTC`** (roughly Tue 21:30–23:00 ET).

Rationale (verified workload overlap from report 10 / Ivy runbook):

- WGU-Reddit daily timer fires ~07:00 UTC; a 01:30 UTC window avoids it.
- WGU-Reddit backup and Launchpad cleanup timers and the collector/Chrome
  workloads are active during the day; the late-night/early-UTC slot has the
  least overlap.
- Randomized delay 900 s keeps SJC clear of any co-scheduled minute.
- Must be re-verified against fresh capacity evidence (Task 10 showed 83% disk,
  reboot pending) before activation.

## 7. Prohibitions

No timer is enabled by this document. No agent modifies production scheduling
without explicit authority. The weekly run never publishes, promotes, changes
taxonomy, or bypasses human review.
