# SJC Intel — Rollback / Uninstall Runbook

**Scope:** systemd service and timer units for SJC Intel workflows.
**Authority:** Rollback requires Buddy approval. Do not execute these commands
without confirmation.
**Gate preserved:** Scheduler Gate, Database Authority Gate, Backup/Restore Gate.

## Prerequisites

- SSH access to `ih-market-vps` as `scraper` or root.
- `sudo` access for systemd operations.
- Backup of current data if rollback involves PG → file fallback.

## Step 1: Stop and Disable All Timers

```bash
# Stop each timer to prevent new triggers
sudo systemctl stop sjc-intel-ingest-nbor.timer
sudo systemctl stop sjc-intel-ingest-bcc-agenda.timer
sudo systemctl stop sjc-intel-process-dedupe.timer
sudo systemctl stop sjc-intel-process-review-queue.timer
sudo systemctl stop sjc-intel-check-health.timer
sudo systemctl stop sjc-intel-backup-postgres.timer

# Disable each timer (removes symlink from timers.target.wants/)
sudo systemctl disable sjc-intel-ingest-nbor.timer
sudo systemctl disable sjc-intel-ingest-bcc-agenda.timer
sudo systemctl disable sjc-intel-process-dedupe.timer
sudo systemctl disable sjc-intel-process-review-queue.timer
sudo systemctl disable sjc-intel-check-health.timer
sudo systemctl disable sjc-intel-backup-postgres.timer
```

## Step 2: Remove Service Files

```bash
# Remove unit files from systemd directory
sudo rm /etc/systemd/system/sjc-intel-ingest-nbor.service
sudo rm /etc/systemd/system/sjc-intel-ingest-nbor.timer
sudo rm /etc/systemd/system/sjc-intel-ingest-bcc-agenda.service
sudo rm /etc/systemd/system/sjc-intel-ingest-bcc-agenda.timer
sudo rm /etc/systemd/system/sjc-intel-process-dedupe.service
sudo rm /etc/systemd/system/sjc-intel-process-dedupe.timer
sudo rm /etc/systemd/system/sjc-intel-process-review-queue.service
sudo rm /etc/systemd/system/sjc-intel-process-review-queue.timer
sudo rm /etc/systemd/system/sjc-intel-check-health.service
sudo rm /etc/systemd/system/sjc-intel-check-health.timer
sudo rm /etc/systemd/system/sjc-intel-backup-postgres.service
sudo rm /etc/systemd/system/sjc-intel-backup-postgres.timer

# Reload systemd daemon
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

## Step 3: Verify Removal

```bash
# Confirm no SJC Intel units remain
systemctl list-units --all | grep sjc-intel
systemctl list-timers --all | grep sjc-intel

# Confirm no failed units
systemctl --failed | grep sjc-intel
```

## Step 4: Remove Lock Files

```bash
# Remove lock directory and all locks
rm -rf /home/scraper/data/sjc-intel/.locks
```

## Step 5: Restore File-Based Fallback

If rollback is from PG-enabled mode back to file mode:

1. Confirm `SJC_INTEL_PG_ADAPTER_ENABLED=false` in
   `/home/scraper/config/sjc_intel.env`.
2. Verify the file adapter has recent data:

```bash
ls -la /home/scraper/data/sjc-intel/intel_items/
ls -la /home/scraper/data/sjc-intel/index/prior_items.yaml
ls -la /home/scraper/data/sjc-intel/review_queue/queue.yaml
```

3. If file data is stale, export current PG state to YAML before disabling PG:

```bash
# Export intel items from PG to YAML (requires _reader or _writer role)
python3 /home/scraper/apps/sjc-intel/scripts/storage_adapter.py --export-to-files
```

4. Run a manual parity check before committing to file-only mode:

```bash
python3 /home/scraper/apps/sjc-intel/scripts/parity_report.py
```

5. If PG was the sole data store and no file backup exists, restore from
   latest `pg_dump` backup first (requires Backup/Restore Gate).

## Step 6: Revert Env File (if changed)

```bash
# Restore env file to safe defaults
# Ensure SJC_INTEL_PG_ADAPTER_ENABLED=false
# Remove or comment out SJC_INTEL_PG_URL
vi /home/scraper/config/sjc_intel.env
```

## Step 7 (Optional): Remove Deploy Artifacts

Remove the local `deploy/` directory if no longer needed:

```bash
# WARNING: Set $REPO_DIR to the actual repository path first
# export REPO_DIR=/home/scraper/apps/sjc-intel
rm -rf "${REPO_DIR:?REPO_DIR not set}/deploy/"
```

## Recovery

To re-enable the service later:

1. Copy unit files to `/etc/systemd/system/`.
2. Run `sudo systemctl daemon-reload`.
3. Enable individual timers: `sudo systemctl enable sjc-intel-{name}.timer`.
4. Start: `sudo systemctl start sjc-intel-{name}.timer`.
5. Verify: `sudo systemctl status sjc-intel-{name}.timer`.

**Do not re-enable without Scheduler Gate approval.**
