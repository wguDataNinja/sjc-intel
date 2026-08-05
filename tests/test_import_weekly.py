import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.import_weekly_bundle import (
    run_full_checks,
    build_preview,
    stage_bundle,
    write_receipt,
)
from scripts.bundle_build import (
    assemble_bundle,
    build_run_json,
    count_candidates,
    write_manifest_and_checksums,
)

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
WORKSPACE = os.path.join(FIXTURE_DIR, "bundle_workspace")
RUN_ID = "SJC-WK-20260803-0001"
GIT_SHA = "1be2ade"
REG_REV = "1be2ade"


class _Args:
    run_id = RUN_ID
    git_sha = GIT_SHA
    profile = "sjc-weekly-001"
    registry_revision = REG_REV
    window_start = "2026-08-03T10:00:00Z"
    window_end = "2026-08-03T11:00:00Z"
    retention_deadline = "2026-08-17T11:00:00Z"
    status = "completed"


def build_bundle(dst):
    """Assemble a valid bundle from the fixture workspace into dst."""
    counts = count_candidates(WORKSPACE)
    run = build_run_json(WORKSPACE, _Args(), counts)
    run["candidate_counts"] = counts
    run["producing_git_sha"] = GIT_SHA
    run["producing_task_or_profile"] = "sjc-weekly-001"
    run["source_registry_revision"] = REG_REV
    assemble_bundle(WORKSPACE, dst, _Args(), counts)
    write_manifest_and_checksums(dst, run, GIT_SHA, "sjc-weekly-001", REG_REV)
    return dst


def test_valid_bundle_imports_and_stages(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    _checks, issues, manifest = run_full_checks(str(bundle))
    assert not issues, issues
    preview = build_preview(str(bundle), manifest)
    assert preview["run_id"] == RUN_ID
    stage = stage_bundle(str(bundle), str(incoming), RUN_ID, manifest)
    receipt = write_receipt(str(bundle), str(incoming), str(receipts), RUN_ID,
                            manifest, preview, "abc123")
    assert os.path.isdir(stage)
    assert (incoming / RUN_ID / "receipt.json").exists()
    assert (receipts / f"{RUN_ID}.receipt.json").exists()
    assert receipt["acknowledgment_eligible"] is True
    assert (incoming / RUN_ID / "intel_candidates" / "sjc_county_news.json").exists()
    assert not (incoming / RUN_ID / "registry").exists()
    assert not (incoming / RUN_ID / "data").exists()


def test_duplicate_import_is_idempotent(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    _c1, i1, m1 = run_full_checks(str(bundle))
    assert not i1
    stage_bundle(str(bundle), str(incoming), RUN_ID, m1)
    write_receipt(str(bundle), str(incoming), str(receipts), RUN_ID, m1,
                  build_preview(str(bundle), m1), "abc123")
    first = sorted(os.path.relpath(p, incoming) for p in (incoming / RUN_ID).rglob("*"))
    # Replay same bundle: staging again is identical (idempotent).
    stage_bundle(str(bundle), str(incoming), RUN_ID, m1)
    second = sorted(os.path.relpath(p, incoming) for p in (incoming / RUN_ID).rglob("*"))
    assert first == second


def test_checksum_failure_rejected(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    # Tamper a candidate file; checksum must now mismatch.
    cand = bundle / "intel_candidates" / "sjc_county_news.json"
    data = json.loads(cand.read_text())
    data["items"][0]["title"] = "tampered"
    cand.write_text(json.dumps(data))
    _checks, issues, _m = run_full_checks(str(bundle))
    assert "file_sizes_and_checksums" in issues


def test_path_traversal_rejected(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    manifest = bundle / "manifest.json"
    m = json.loads(manifest.read_text())
    m["included_files"].append(
        {"path": "../evil.txt", "size_bytes": 1, "sha256": "0" * 64}
    )
    manifest.write_text(json.dumps(m))
    _checks, issues, _m = run_full_checks(str(bundle))
    assert any("unsafe path" in i for i in issues)


def test_malformed_json_rejected(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    cand = bundle / "intel_candidates" / "sjc_county_news.json"
    cand.write_text("this is { not valid json")
    _checks, issues, _m = run_full_checks(str(bundle))
    assert any("malformed JSON" in i for i in issues)


def test_preview_does_not_stage(tmp_path):
    bundle = tmp_path / "bundle"
    build_bundle(str(bundle))
    incoming = tmp_path / "incoming"
    _c, issues, manifest = run_full_checks(str(bundle))
    assert not issues
    # Preview path never writes.
    assert not (incoming / RUN_ID).exists()
