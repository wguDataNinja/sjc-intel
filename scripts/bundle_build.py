#!/usr/bin/env python3
"""
SJC_Intel — bundle builder (producer-side).

Assembles a weekly operational transfer bundle from a run workspace and run
metadata, generating run.json, manifest.json, and checksums.sha256 in the
deterministic layout defined by docs/weekly_operational_contract.md §7.

Usage (repo root):

    python3 scripts/bundle_build.py \
        --workspace <run-workspace> \
        --out <bundle-dir> \
        --run-id SJC-WK-YYYYMMDD-0001 \
        --git-sha <producing-sha> \
        --profile <profile-id> \
        --registry-revision <registry-pin-sha> \
        --window-start <ISO-8601-UTC> \
        --window-end <ISO-8601-UTC> \
        [--status completed|completed_partial|failed|aborted]

Workspace layout (all optional except where noted):

    workspace/
      source_health/{source_id}.json
      source_events/{source_id}.json
      intel_candidates/{source_id}.json
      source_proposals/proposals.json
      logs/run.log
      run.json        # optional seed; builder merges/overrides run metadata

The builder never reads or writes the authoritative corpus paths.
"""
import argparse
import datetime
import json
import os
import shutil
import sys

try:
    from scripts.bundle_common import (
        BUNDLE_SCHEMA_VERSION,
        RETENTION_DAYS_DEFAULT,
        RUN_STATUSES,
        RUN_JSON_REQUIRED_FIELDS,
        bundle_files,
        checksums_path,
        manifest_path,
        read_json,
        replay_identity,
        run_json_path,
        sha256_hex,
        valid_run_id,
        write_json,
    )
except ImportError:  # standalone: python3 scripts/bundle_build.py
    from bundle_common import (
        BUNDLE_SCHEMA_VERSION,
        RETENTION_DAYS_DEFAULT,
        RUN_STATUSES,
        RUN_JSON_REQUIRED_FIELDS,
        bundle_files,
        checksums_path,
        manifest_path,
        read_json,
        replay_identity,
        run_json_path,
        sha256_hex,
        valid_run_id,
        write_json,
    )

WORKSPACE_SUBDIRS = [
    "source_health",
    "source_events",
    "intel_candidates",
    "source_proposals",
    "logs",
]


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def count_candidates(workspace):
    """Count candidate outcomes across intel_candidates/*.json files."""
    counts = {"by_source": {}, "new": 0, "duplicate": 0, "partial": 0, "failed": 0}
    cand_dir = os.path.join(workspace, "intel_candidates")
    if not os.path.isdir(cand_dir):
        return counts
    for name in sorted(os.listdir(cand_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(cand_dir, name)
        try:
            data = read_json(path)
        except Exception:
            counts["failed"] += 1
            continue
        source = data.get("source_id") or name[:-5]
        per_source = {"new": 0, "duplicate": 0, "partial": 0, "failed": 0}
        for item in data.get("items", []):
            outcome = item.get("outcome") or item.get("status", "")
            key = outcome if outcome in {"duplicate", "no_match", "partial", "failed"} else "no_match"
            if key == "no_match":
                key = "new"
            per_source[key] += 1
            counts[key] += 1
        counts["by_source"][source] = per_source
    return counts


def build_run_json(workspace, args, counts):
    """Merge a workspace run.json seed (if any) with authoritative metadata."""
    seed = {}
    seed_path = os.path.join(workspace, "run.json")
    if os.path.exists(seed_path):
        try:
            seed = read_json(seed_path)
        except Exception as e:
            print(f"WARNING: unreadable workspace run.json ({e}); regenerating", file=sys.stderr)

    run = dict(seed)
    run.update(
        {
            "run_id": args.run_id,
            "run_status": args.status,
            "started_at": seed.get("started_at") or utc_now_iso(),
            "ended_at": utc_now_iso(),
            "window_start": args.window_start,
            "window_end": args.window_end,
            "retention_deadline": args.retention_deadline,
            "profile_id": args.profile,
            "replay_identity": replay_identity(args.run_id, args.git_sha, args.registry_revision),
        }
    )
    run.setdefault("failure_summary", {"total": 0, "by_source": {}, "by_reason": {}})
    return run


def assemble_bundle(workspace, out, args, counts):
    os.makedirs(out, exist_ok=True)
    for sub in WORKSPACE_SUBDIRS:
        src = os.path.join(workspace, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(out, sub), dirs_exist_ok=True)
    # Stable empty containers so bundle shape is deterministic.
    for sub, default in (
        ("source_health", {}),
        ("source_events", {}),
        ("intel_candidates", {}),
        ("source_proposals", {"source_proposals": []}),
    ):
        sub_dir = os.path.join(out, sub)
        os.makedirs(sub_dir, exist_ok=True)
        marker = "proposals.json" if sub == "source_proposals" else f"{args.run_id}.placeholder"
        marker_path = os.path.join(sub_dir, marker)
        if not os.listdir(sub_dir):
            write_json(marker_path, default)
    log_dir = os.path.join(out, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "run.log")
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write(f"run_id={args.run_id} status={args.status}\n")


def write_manifest_and_checksums(out, run, git_sha, profile, registry_revision):
    counts = run["candidate_counts"]
    run["producing_git_sha"] = git_sha
    run["producing_task_or_profile"] = profile
    run["source_registry_revision"] = registry_revision
    run["candidate_counts"] = counts
    # run.json must exist before the file scan so it is manifest-included.
    write_json(run_json_path(out), run)

    manifest = {
        "bundle_schema_version": BUNDLE_SCHEMA_VERSION,
        "run_id": run["run_id"],
        "producing_git_sha": git_sha,
        "producing_task_or_profile": profile,
        "source_registry_revision": registry_revision,
        "window_start": run["window_start"],
        "window_end": run["window_end"],
        "retention_deadline": run["retention_deadline"],
        "run_status": run["run_status"],
        "included_files": None,  # set below
        "bundle_total_bytes": None,  # set below
        "candidate_counts": counts,
        "failure_counts": run["failure_summary"],
        "replay_identity": run["replay_identity"],
    }
    files = bundle_files(out)
    included = []
    for rel in files:
        if rel in ("manifest.json", "checksums.sha256"):
            continue
        full = os.path.join(out, rel)
        included.append(
            {
                "path": rel,
                "size_bytes": os.path.getsize(full),
                "sha256": sha256_hex(full),
            }
        )
    included.sort(key=lambda f: f["path"])
    manifest["included_files"] = included
    manifest["bundle_total_bytes"] = sum(f["size_bytes"] for f in included)
    write_json(manifest_path(out), manifest)

    # Recompute the file set so manifest.json is checksummed too.
    checksum_lines = []
    for rel in bundle_files(out):
        if rel == "checksums.sha256":
            continue
        full = os.path.join(out, rel)
        checksum_lines.append(f"{sha256_hex(full)}  {rel}")
    with open(checksums_path(out), "w") as f:
        f.write("\n".join(sorted(checksum_lines)) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Build an SJC weekly operational transfer bundle.")
    parser.add_argument("--workspace", required=True, help="Run workspace directory.")
    parser.add_argument("--out", required=True, help="Destination bundle directory.")
    parser.add_argument("--run-id", required=True, help="e.g. SJC-WK-20260809-0001")
    parser.add_argument("--git-sha", required=True, help="Producing repository SHA.")
    parser.add_argument("--profile", required=True, help="Hermes weekly task ID / run profile.")
    parser.add_argument("--registry-revision", required=True, help="Registry pin SHA.")
    parser.add_argument("--window-start", required=True, help="ISO 8601 UTC window start.")
    parser.add_argument("--window-end", required=True, help="ISO 8601 UTC window end.")
    parser.add_argument(
        "--retention-deadline",
        default=None,
        help="ISO 8601 UTC prune eligibility deadline. Default: window_end + 14 days.",
    )
    parser.add_argument("--status", default="completed", choices=sorted(RUN_STATUSES))
    args = parser.parse_args()

    if not valid_run_id(args.run_id):
        print(f"ERROR: invalid run_id '{args.run_id}' (expected {RUN_ID_PATTERN})", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.workspace):
        print(f"ERROR: workspace not found: {args.workspace}", file=sys.stderr)
        sys.exit(1)
    if args.retention_deadline is None:
        end = datetime.datetime.strptime(args.window_end, "%Y-%m-%dT%H:%M:%SZ")
        end = end.replace(tzinfo=datetime.timezone.utc)
        args.retention_deadline = (end + datetime.timedelta(days=RETENTION_DAYS_DEFAULT)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    counts = count_candidates(args.workspace)
    run = build_run_json(args.workspace, args, counts)
    run["candidate_counts"] = counts
    run["producing_git_sha"] = args.git_sha
    run["producing_task_or_profile"] = args.profile
    run["source_registry_revision"] = args.registry_revision

    assemble_bundle(args.workspace, args.out, args, counts)
    write_manifest_and_checksums(args.out, run, args.git_sha, args.profile, args.registry_revision)

    missing = [f for f in RUN_JSON_REQUIRED_FIELDS if f not in run]
    if missing:
        print(f"ERROR: run.json missing fields: {missing}", file=sys.stderr)
        sys.exit(1)

    n = len(run["candidate_counts"].get("by_source", {}))
    print(f"Bundle written to {args.out}")
    print(f"  run_id: {args.run_id}  status: {args.status}")
    print(f"  sources with candidates: {n}")
    print("  run.json, manifest.json, checksums.sha256 written")


if __name__ == "__main__":
    main()
