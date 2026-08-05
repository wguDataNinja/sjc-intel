"""SJC_Intel — shared bundle helpers.

Used by scripts/bundle_build.py, scripts/bundle_verify.py, and
scripts/bundle_import.py. Contract authority:
docs/weekly_operational_contract.md §7.
"""
import hashlib
import json
import os

BUNDLE_SCHEMA_VERSION = "1.0"

RUN_STATUSES = {"completed", "completed_partial", "failed", "aborted"}
OUTCOME_LABELS = {"duplicate", "no_match", "partial", "failed"}

RUN_ID_PATTERN = "SJC-WK-YYYYMMDD-NNNN"

# manifest.json required fields
MANIFEST_REQUIRED_FIELDS = [
    "bundle_schema_version",
    "run_id",
    "producing_git_sha",
    "producing_task_or_profile",
    "source_registry_revision",
    "window_start",
    "window_end",
    "retention_deadline",
    "run_status",
    "included_files",
    "bundle_total_bytes",
    "candidate_counts",
    "failure_counts",
    "replay_identity",
]

# run.json required fields
RUN_JSON_REQUIRED_FIELDS = [
    "run_id",
    "run_status",
    "started_at",
    "ended_at",
    "window_start",
    "window_end",
    "retention_deadline",
    "profile_id",
    "replay_identity",
    "failure_summary",
]

# Default retention delay before a bundle is eligible for pruning
# (verified receipt must also exist; see docs/weekly_operational_contract.md §7.7).
RETENTION_DAYS_DEFAULT = 14


def sha256_hex(path):
    """Return lowercase hex sha256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
        f.write("\n")


def replay_identity(run_id, git_sha, registry_revision):
    """Deterministic replay identity for a bundle."""
    return f"{BUNDLE_SCHEMA_VERSION}::{run_id}::{git_sha}::{registry_revision}"


def bundle_files(bundle_dir):
    """Return all files in a bundle as posix relative paths, sorted."""
    out = []
    for root, _dirs, names in os.walk(bundle_dir):
        for name in sorted(names):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, bundle_dir).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)


def manifest_path(bundle_dir):
    return os.path.join(bundle_dir, "manifest.json")


def checksums_path(bundle_dir):
    return os.path.join(bundle_dir, "checksums.sha256")


def run_json_path(bundle_dir):
    return os.path.join(bundle_dir, "run.json")


def valid_run_id(run_id):
    parts = run_id.split("-")
    if len(parts) != 4 or parts[0] != "SJC" or parts[1] != "WK":
        return False
    if not (len(parts[2]) == 8 and parts[2].isdigit()):
        return False
    if not (len(parts[3]) == 4 and parts[3].isdigit()):
        return False
    return True
