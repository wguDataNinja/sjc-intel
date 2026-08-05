#!/usr/bin/env python3
"""
SJC_Intel — idempotent Mac-side bundle importer (staging-only).

Verifies an incoming weekly bundle, stages it into an explicit incoming area,
and writes a verified receipt. It never writes to the authoritative corpus
paths (data/intel_items/, data/source_events/, data/review_queue/,
data/index/). Converting candidates into corpus/review state is a separate,
human-gated step.

Behavior (contract: docs/weekly_operational_contract.md §7.5–7.6):

  * verify the bundle fully (scripts/bundle_verify.py rules); refuse on failure;
  * import keyed by run_id; a second import of the same run_id is a no-op
    returning the existing receipt;
  * a receipt is written only after full verification and a successful stage;
  * same run_id with different bundle content is a conflict and is rejected.

Usage (repo root):

    python3 scripts/bundle_import.py \
        --bundle <bundle-dir> \
        [--incoming-root data/incoming] \
        [--receipt-root data/receipts] \
        [--git-sha <mac-sha>]
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

try:
    from scripts.bundle_common import manifest_path, read_json, write_json
    from scripts.bundle_verify import run_checks
except ImportError:  # standalone: python3 scripts/bundle_import.py
    from bundle_common import manifest_path, read_json, write_json
    from bundle_verify import run_checks

RECEIPT_SCHEMA_VERSION = "1.0"

DEFAULT_INCOMING_ROOT = "data/incoming"
DEFAULT_RECEIPT_ROOT = "data/receipts"


def bundle_digest(checksums_file):
    """sha256 of the checksums.sha256 file content (bundle identity)."""
    h = hashlib.sha256()
    with open(checksums_file, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def receipt_path(receipt_root, run_id):
    return os.path.join(receipt_root, f"{run_id}.receipt.json")


def import_bundle(bundle_dir, incoming_root, receipt_root, git_sha=None):
    """Return (status, message, receipt_or_None). status in
    {"imported", "idempotent", "failed", "conflict"}."""
    checks, errors = run_checks(bundle_dir)
    if errors:
        return ("failed", f"bundle verification failed: {errors}", None)

    manifest = read_json(manifest_path(bundle_dir))
    run_id = manifest["run_id"]

    existing = receipt_path(receipt_root, run_id)
    if os.path.exists(existing):
        prior = read_json(existing)
        if prior.get("bundle_sha256") == bundle_digest(os.path.join(bundle_dir, "checksums.sha256")):
            return ("idempotent", f"run {run_id} already imported", prior)
        return ("conflict", f"run {run_id} already imported with different bundle content", None)

    stage_dir = os.path.join(incoming_root, run_id)
    os.makedirs(stage_dir, exist_ok=True)
    try:
        if os.path.isdir(bundle_dir) and os.path.abspath(stage_dir) != os.path.abspath(bundle_dir):
            shutil.copytree(bundle_dir, stage_dir, dirs_exist_ok=True)
    except Exception as e:
        return ("failed", f"staging failed: {e}", None)

    verified_files = len(manifest.get("included_files", []))
    receipt = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_id": f"RCP-{run_id}",
        "run_id": run_id,
        "bundle_sha256": bundle_digest(os.path.join(bundle_dir, "checksums.sha256")),
        "verified_files": verified_files,
        "verified_checksums": True,
        "imported_at": utc_now_iso(),
        "importing_git_sha": git_sha,
        "status": "acknowledged",
        "staging_path": stage_dir,
    }
    os.makedirs(receipt_root, exist_ok=True)
    write_json(existing, receipt)
    return ("imported", f"run {run_id} staged and acknowledged", receipt)


def main():
    parser = argparse.ArgumentParser(description="Idempotent staging import of an SJC weekly bundle.")
    parser.add_argument("--bundle", required=True, help="Bundle directory to import.")
    parser.add_argument("--incoming-root", default=DEFAULT_INCOMING_ROOT)
    parser.add_argument("--receipt-root", default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--git-sha", default=None, help="Mac repository SHA at import time.")
    args = parser.parse_args()

    if not os.path.isdir(args.bundle):
        print(f"ERROR: bundle not found: {args.bundle}", file=sys.stderr)
        sys.exit(1)

    status, message, receipt = import_bundle(
        args.bundle, args.incoming_root, args.receipt_root, args.git_sha
    )
    print(message)
    if status in ("imported", "idempotent") and receipt is not None:
        print(f"Receipt: {receipt_path(args.receipt_root, receipt['run_id'])}")
        sys.exit(0)
    sys.exit(1 if status in ("failed", "conflict") else 0)


if __name__ == "__main__":
    main()
