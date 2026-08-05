#!/usr/bin/env python3
"""
SJC_Intel — Mac-side weekly bundle importer (staging-only).

Validates and stages a transferred weekly bundle into data/incoming/{run_id}/,
writes a durable receipt, and NEVER writes the authoritative corpus
(data/intel_items/, data/source_events/, data/review_queue/, data/index/) or
promotes source proposals.

Contract authority: docs/weekly_operational_contract.md §7.5–7.6.
Usage:

    python3 scripts/import_weekly_bundle.py <bundle-path> \
        [--incoming-root data/incoming] [--receipt-root data/receipts] \
        [--git-sha <mac-sha>] [--preview]

Receipt: data/incoming/{run_id}/receipt.json (colocated) mirrored to
data/receipts/{run_id}.receipt.json (canonical acknowledgement path observed by
the producer for prune eligibility). A bundle is never prune-eligible before a
complete receipt exists.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

try:
    from scripts.bundle_common import (
        MANIFEST_REQUIRED_FIELDS,
        checksums_path,
        manifest_path,
        read_json,
        valid_run_id,
        write_json,
    )
    from scripts.bundle_verify import run_checks
except ImportError:  # standalone: python3 scripts/import_weekly_bundle.py
    from bundle_common import (
        MANIFEST_REQUIRED_FIELDS,
        checksums_path,
        manifest_path,
        read_json,
        valid_run_id,
        write_json,
    )
    from bundle_verify import run_checks

DEFAULT_INCOMING_ROOT = "data/incoming"
DEFAULT_RECEIPT_ROOT = "data/receipts"

RECEIPT_SCHEMA_VERSION = "1.0"

CANDIDATE_REQUIRED_FIELDS = [
    "item_id", "title", "summary", "source_id", "source_url",
    "discovered_at", "raw_excerpt", "topics", "geographic_scope", "urgency",
    "verification_status", "sensitivity", "human_review_required",
    "status", "review_status",
]


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bundle_digest(bundle_dir):
    """sha256 of checksums.sha256 file content = checksum-set identity."""
    h = hashlib.sha256()
    with open(checksums_path(bundle_dir), "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def validate_candidates(bundle_dir):
    """Validate intel_candidates/*.json. Returns (issues, total, duplicates, rejected)."""
    issues = []
    total = 0
    duplicates = 0
    rejected = 0
    cand_dir = os.path.join(bundle_dir, "intel_candidates")
    if not os.path.isdir(cand_dir):
        return issues, total, duplicates, rejected
    for name in sorted(os.listdir(cand_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(cand_dir, name)
        try:
            data = read_json(path)
        except Exception as e:
            issues.append(f"{name}: malformed JSON ({e})")
            rejected += 1
            continue
        items = data.get("items", [])
        total += len(items)
        for i, item in enumerate(items):
            missing = [f for f in CANDIDATE_REQUIRED_FIELDS if f not in item]
            if missing:
                issues.append(f"{name}[{i}] {item.get('item_id', '?')}: missing {missing}")
                rejected += 1
                continue
            if item.get("status") != "candidate" or item.get("review_status") != "candidate":
                issues.append(f"{name}[{i}] {item.get('item_id')}: not a candidate "
                              f"(status={item.get('status')!r}, review_status={item.get('review_status')!r})")
                rejected += 1
                continue
            if item.get("outcome") == "duplicate":
                duplicates += 1
    return issues, total, duplicates, rejected


def validate_proposals(bundle_dir):
    """Validate source_proposals/proposals.json. Returns (issues, count)."""
    issues = []
    count = 0
    path = os.path.join(bundle_dir, "source_proposals", "proposals.json")
    if not os.path.isfile(path):
        return issues, count
    try:
        data = read_json(path)
    except Exception as e:
        return [f"source_proposals/proposals.json malformed ({e})"], 0
    for i, p in enumerate(data.get("source_proposals", [])):
        count += 1
        if "proposal_id" not in p or "url" not in p or "review_status" not in p:
            issues.append(f"proposals.json[{i}]: missing proposal_id/url/review_status")
        elif p.get("review_status") not in ("candidate", "pending_review", "under_review", "decided", "deferred"):
            issues.append(f"proposals.json[{i}] {p.get('proposal_id')}: unexpected review_status")
    return issues, count


def run_full_checks(bundle_dir):
    """bundle_verify.run_checks plus Task 13 import-only checks."""
    checks, errors = run_checks(bundle_dir)
    issues = list(errors)

    manifest = {}
    if os.path.isfile(manifest_path(bundle_dir)):
        try:
            manifest = read_json(manifest_path(bundle_dir))
        except Exception as e:
            issues.append(f"manifest unreadable: {e}")

    # Path traversal / undeclared file safety.
    for f in manifest.get("included_files", []):
        rel = f.get("path", "")
        if rel.startswith("/") or ".." in rel.split("/"):
            issues.append(f"unsafe path in manifest: {rel!r}")
            break

    # Malformed JSON detection across declared files.
    for f in manifest.get("included_files", []):
        rel = f.get("path", "")
        if not rel.endswith(".json"):
            continue
        full = os.path.join(bundle_dir, rel)
        if not os.path.isfile(full):
            continue
        try:
            read_json(full)
        except Exception as e:
            issues.append(f"malformed JSON {rel}: {e}")

    cand_issues, _total, _dup, _rej = validate_candidates(bundle_dir)
    issues.extend(cand_issues)
    prop_issues, _pc = validate_proposals(bundle_dir)
    issues.extend(prop_issues)

    return checks, issues, manifest


def build_preview(bundle_dir, manifest):
    cand_issues, total, duplicates, rejected = validate_candidates(bundle_dir)
    _piss, proposals = validate_proposals(bundle_dir)
    return {
        "run_id": manifest.get("run_id"),
        "run_status": manifest.get("run_status"),
        "producing_git_sha": manifest.get("producing_git_sha"),
        "source_registry_revision": manifest.get("source_registry_revision"),
        "files": len(manifest.get("included_files", [])),
        "bundle_total_bytes": manifest.get("bundle_total_bytes"),
        "candidates": total,
        "duplicates": duplicates,
        "rejected_candidates": rejected,
        "proposals": proposals,
        "validation": "PASS",
    }


def write_receipt(bundle_dir, incoming_root, receipt_root, run_id, manifest,
                  preview, git_sha):
    digest = bundle_digest(bundle_dir)
    now = utc_now_iso()
    receipt = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_id": f"RCP-{run_id}",
        "bundle_id": run_id,
        "run_id": run_id,
        "checksum_set_identity": digest,
        "bundle_sha256": digest,
        "imported_at": now,
        "importer_git_sha": git_sha,
        "files_accepted": preview["files"],
        "candidate_counts": preview["candidates"],
        "proposal_counts": preview["proposals"],
        "duplicate_counts": preview["duplicates"],
        "rejected_counts": preview["rejected_candidates"],
        "validation_result": "PASS",
        "staging_location": os.path.join(incoming_root, run_id),
        "acknowledgment_eligible": True,
        "status": "acknowledged",
    }
    # Colocated per-bundle receipt + canonical acknowledgement-path mirror.
    write_json(os.path.join(incoming_root, run_id, "receipt.json"), receipt)
    os.makedirs(receipt_root, exist_ok=True)
    write_json(os.path.join(receipt_root, f"{run_id}.receipt.json"), receipt)
    return receipt


def stage_bundle(bundle_dir, incoming_root, run_id, manifest):
    """Copy declared files into the staging area, sanitizing paths."""
    stage = os.path.join(incoming_root, run_id)
    os.makedirs(stage, exist_ok=True)
    for f in manifest.get("included_files", []):
        rel = f.get("path", "")
        if rel.startswith("/") or ".." in rel.split("/"):
            raise ValueError(f"refusing unsafe staged path: {rel!r}")
        src = os.path.join(bundle_dir, rel)
        dst = os.path.join(stage, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    # Top-level bundle bookkeeping files.
    for top in ("manifest.json", "checksums.sha256"):
        shutil.copy2(os.path.join(bundle_dir, top), os.path.join(stage, top))
    return stage


def main():
    parser = argparse.ArgumentParser(description="Import a weekly bundle (staging-only).")
    parser.add_argument("bundle_path", help="Path to the verified bundle directory.")
    parser.add_argument("--incoming-root", default=DEFAULT_INCOMING_ROOT)
    parser.add_argument("--receipt-root", default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--git-sha", default=None, help="Mac repository SHA at import time.")
    parser.add_argument("--preview", action="store_true",
                        help="Validate and print preview only; no staging, no receipt.")
    args = parser.parse_args()

    bundle_dir = args.bundle_path
    if not os.path.isdir(bundle_dir):
        print(f"ERROR: bundle not found: {bundle_dir}", file=sys.stderr)
        sys.exit(1)

    checks, issues, manifest = run_full_checks(bundle_dir)
    preview = build_preview(bundle_dir, manifest)

    if issues:
        print(f"Bundle validation FAILED ({len(issues)} issue(s)):")
        for c in checks:
            if not c["passed"]:
                print(f"  FAIL {c['name']} — {c.get('detail', '')}")
        for issue in issues[:20]:
            print(f"  FAIL {issue}")
        print("No staging occurred; no receipt written; corpus untouched.")
        sys.exit(1)

    if not valid_run_id(manifest.get("run_id", "")):
        print(f"ERROR: invalid run_id in manifest: {manifest.get('run_id')!r}", file=sys.stderr)
        sys.exit(1)

    print("Bundle validation PASS")
    print(f"  run_id: {preview['run_id']}")
    print(f"  files: {preview['files']}  total_bytes: {preview['bundle_total_bytes']}")
    print(f"  candidates: {preview['candidates']}  duplicates: {preview['duplicates']}  "
          f"proposals: {preview['proposals']}")

    if args.preview:
        print("\nPREVIEW ONLY — no staging, no receipt.")
        return

    run_id = manifest["run_id"]
    existing_receipt = os.path.join(args.receipt_root, f"{run_id}.receipt.json")
    if os.path.exists(existing_receipt):
        prior = read_json(existing_receipt)
        if prior.get("checksum_set_identity") == bundle_digest(bundle_dir):
            print(f"run {run_id} already imported (idempotent replay). "
                  f"Receipt: {existing_receipt}")
            return
        print(f"ERROR: run {run_id} already imported with different bundle content (conflict).",
              file=sys.stderr)
        sys.exit(1)

    stage = stage_bundle(bundle_dir, args.incoming_root, run_id, manifest)
    receipt = write_receipt(bundle_dir, args.incoming_root, args.receipt_root,
                            run_id, manifest, preview, args.git_sha)
    print(f"Staged to {stage}")
    print(f"Receipt: {os.path.join(stage, 'receipt.json')}")
    print(f"Acknowledgement path: {existing_receipt}")
    print(f"Acknowledgment eligible: {receipt['acknowledgment_eligible']}")


if __name__ == "__main__":
    main()
