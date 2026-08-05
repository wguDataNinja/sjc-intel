#!/usr/bin/env python3
"""
SJC_Intel — bundle verifier (both sides).

Validates an incoming/produced bundle against the contract in
docs/weekly_operational_contract.md §7:

  * layout and required files present;
  * manifest.json fields complete and valid;
  * run.json fields complete and consistent with the manifest;
  * every manifest-included file exists with matching size and sha256;
  * no unexpected files (except manifest.json + checksums.sha256);
  * checksums.sha256 covers all included files and manifest.json;
  * replay_identity recomputes correctly.

Usage (repo root):

    python3 scripts/bundle_verify.py --bundle <bundle-dir> [--json]
"""
import argparse
import hashlib
import json
import os
import sys

try:
    from scripts.bundle_common import (
        BUNDLE_SCHEMA_VERSION,
        MANIFEST_REQUIRED_FIELDS,
        OUTCOME_LABELS,
        RUN_JSON_REQUIRED_FIELDS,
        RUN_STATUSES,
        bundle_files,
        checksums_path,
        manifest_path,
        read_json,
        replay_identity,
        run_json_path,
        sha256_hex,
    )
except ImportError:  # standalone: python3 scripts/bundle_verify.py
    from bundle_common import (
        BUNDLE_SCHEMA_VERSION,
        MANIFEST_REQUIRED_FIELDS,
        OUTCOME_LABELS,
        RUN_JSON_REQUIRED_FIELDS,
        RUN_STATUSES,
        bundle_files,
        checksums_path,
        manifest_path,
        read_json,
        replay_identity,
        run_json_path,
        sha256_hex,
    )

CHECK_NAMES = [
    "layout_and_required_files",
    "manifest_fields",
    "run_json_fields",
    "manifest_run_consistency",
    "file_sizes_and_checksums",
    "no_unexpected_files",
    "checksums_file_covers_manifest",
    "replay_identity",
    "candidate_outcome_labels",
]


def checksum_file_entries(checksums_path):
    """Parse checksums.sha256 into {rel_path: sha256}."""
    entries = {}
    with open(checksums_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if len(line) < 66 or "  " not in line:
                raise ValueError(f"malformed checksum line: {line[:80]!r}")
            digest, rel = line.split("  ", 1)
            entries[rel] = digest
    return entries


def run_checks(bundle_dir):
    """Return (checks, failures) where checks is a list of dicts."""
    checks = []
    errors = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            errors.append(name)

    # 1. Layout and required files.
    if not os.path.isdir(bundle_dir):
        check("layout_and_required_files", False, f"bundle dir missing: {bundle_dir}")
        return checks, errors
    required = [
        manifest_path(bundle_dir),
        checksums_path(bundle_dir),
        run_json_path(bundle_dir),
        os.path.join(bundle_dir, "logs", "run.log"),
    ]
    missing = [p for p in required if not os.path.isfile(p)]
    check("layout_and_required_files", not missing, f"missing: {missing}")

    files = bundle_files(bundle_dir)
    fileset = set(files)
    for req in required:
        fileset.add(os.path.relpath(req, bundle_dir).replace(os.sep, "/"))

    manifest = {}
    run = {}
    if not missing:
        # 2. Manifest fields.
        try:
            manifest = read_json(manifest_path(bundle_dir))
        except Exception as e:
            check("manifest_fields", False, f"manifest unreadable: {e}")
        else:
            absent = [f for f in MANIFEST_REQUIRED_FIELDS if f not in manifest]
            ok = not absent
            detail = f"missing: {absent}" if absent else ""
            if ok and manifest.get("bundle_schema_version") != BUNDLE_SCHEMA_VERSION:
                ok = False
                detail = f"unsupported schema version: {manifest.get('bundle_schema_version')!r}"
            if ok and manifest.get("run_status") not in RUN_STATUSES:
                ok = False
                detail = f"invalid run_status: {manifest.get('run_status')!r}"
            if ok:
                included = manifest["included_files"]
                if not isinstance(included, list) or not all(
                    isinstance(f, dict) and all(k in f for k in ("path", "size_bytes", "sha256"))
                    for f in included
                ):
                    ok = False
                    detail = "included_files must be a list of {path, size_bytes, sha256}"
            check("manifest_fields", ok, detail)

        # 3. run.json fields.
        try:
            run = read_json(run_json_path(bundle_dir))
        except Exception as e:
            check("run_json_fields", False, f"run.json unreadable: {e}")
        else:
            absent = [f for f in RUN_JSON_REQUIRED_FIELDS if f not in run]
            check("run_json_fields", not absent, f"missing: {absent}")

        # 4. Manifest / run consistency.
        consistent = (
            manifest.get("run_id") == run.get("run_id")
            and manifest.get("run_status") == run.get("run_status")
            and manifest.get("replay_identity") == run.get("replay_identity")
            and manifest.get("window_start") == run.get("window_start")
            and manifest.get("window_end") == run.get("window_end")
        )
        check("manifest_run_consistency", consistent)

        # 5. File sizes and checksums.
        size_mismatch = []
        hash_mismatch = []
        for f in manifest.get("included_files", []):
            full = os.path.join(bundle_dir, f["path"])
            if not os.path.isfile(full):
                size_mismatch.append(f"{f['path']}: missing")
                continue
            if os.path.getsize(full) != f["size_bytes"]:
                size_mismatch.append(f"{f['path']}: size")
                continue
            if sha256_hex(full) != f["sha256"]:
                hash_mismatch.append(f["path"])
        detail = ""
        if size_mismatch:
            detail += f" size-mismatch: {size_mismatch}"
        if hash_mismatch:
            detail += f" hash-mismatch: {hash_mismatch}"
        check("file_sizes_and_checksums", not (size_mismatch or hash_mismatch), detail)

        # 6. No unexpected files.
        manifest_paths = {f["path"] for f in manifest.get("included_files", [])}
        allowed = manifest_paths | {"manifest.json", "checksums.sha256"}
        unexpected = sorted(fileset - allowed)
        check("no_unexpected_files", not unexpected, f"unexpected: {unexpected}")

        # 7. checksums.sha256 covers manifest and all included files.
        try:
            cksum_entries = checksum_file_entries(checksums_path(bundle_dir))
        except Exception as e:
            check("checksums_file_covers_manifest", False, str(e))
        else:
            uncovered = [p for p in (manifest_paths | {"manifest.json"}) if cksum_entries.get(p) is None]
            check(
                "checksums_file_covers_manifest",
                not uncovered,
                f"no checksum entry: {uncovered}",
            )

        # 8. replay_identity recomputes.
        expected = replay_identity(
            manifest.get("run_id"),
            manifest.get("producing_git_sha"),
            manifest.get("source_registry_revision"),
        )
        check(
            "replay_identity",
            manifest.get("replay_identity") == expected,
            f"expected {expected}",
        )

        # 9. Candidate outcome labels.
        bad = []
        cand_dir = os.path.join(bundle_dir, "intel_candidates")
        if os.path.isdir(cand_dir):
            for name in sorted(os.listdir(cand_dir)):
                if not name.endswith(".json"):
                    continue
                try:
                    data = read_json(os.path.join(cand_dir, name))
                except Exception:
                    continue
                for item in data.get("items", []):
                    outcome = item.get("outcome") or item.get("status", "")
                    if outcome and outcome not in OUTCOME_LABELS and outcome != "candidate":
                        bad.append((name, outcome))
        check("candidate_outcome_labels", not bad, f"invalid labels: {bad}")

    return checks, errors


def main():
    parser = argparse.ArgumentParser(description="Verify an SJC weekly transfer bundle.")
    parser.add_argument("--bundle", required=True, help="Bundle directory to verify.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    checks, errors = run_checks(args.bundle)
    passed = not errors

    if args.json:
        print(
            json.dumps(
                {
                    "status": "PASS" if passed else "FAIL",
                    "checks": checks,
                    "failed_checks": errors,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for c in checks:
            status = "PASS" if c["passed"] else "FAIL"
            print(f"{status} {c['name']}" + (f" — {c['detail']}" if c.get("detail") else ""))
        print(f"\nBundle verification: {'PASS' if passed else 'FAIL'}")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
