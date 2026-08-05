import json
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.bundle_build import count_candidates, build_run_json
from scripts.bundle_import import import_bundle
from scripts.bundle_verify import run_checks, checksum_file_entries
from scripts.bundle_common import (
    BUNDLE_SCHEMA_VERSION,
    bundle_files,
    manifest_path,
    replay_identity,
    valid_run_id,
)

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
WORKSPACE = os.path.join(FIXTURE_DIR, "bundle_workspace")
SAMPLE_BUNDLE = os.path.join(FIXTURE_DIR, "sample_bundle")

GIT_SHA = "1be2ade"
REGISTRY_REV = "1be2ade"
RUN_ID = "SJC-WK-20260803-0001"


def _copy_tree(src, dst):
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)


def test_valid_run_id():
    assert valid_run_id("SJC-WK-20260803-0001")
    assert not valid_run_id("SJC-WK-20260803")
    assert not valid_run_id("SJC-WK-20260803-0001-extra")
    assert not valid_run_id("bad-run")


def test_sample_bundle_layout_is_deterministic():
    files = bundle_files(SAMPLE_BUNDLE)
    assert files == sorted(files)
    assert "manifest.json" in files
    assert "checksums.sha256" in files
    assert "run.json" in files
    assert "logs/run.log" in files
    assert "intel_candidates/sjc_county_news.json" in files


def test_sample_bundle_verifies():
    checks, errors = run_checks(SAMPLE_BUNDLE)
    assert not errors, errors
    names = [c["name"] for c in checks]
    assert len(names) == len(set(names))


def test_manifest_fields_and_replay_identity():
    with open(manifest_path(SAMPLE_BUNDLE)) as f:
        manifest = json.load(f)
    assert manifest["bundle_schema_version"] == BUNDLE_SCHEMA_VERSION
    assert manifest["run_id"] == RUN_ID
    assert manifest["run_status"] == "completed"
    assert manifest["candidate_counts"]["by_source"]["sjc_county_news"]["new"] == 1
    assert manifest["replay_identity"] == replay_identity(RUN_ID, GIT_SHA, REGISTRY_REV)


def test_checksums_cover_all_files_including_manifest():
    entries = checksum_file_entries(os.path.join(SAMPLE_BUNDLE, "checksums.sha256"))
    for rel in bundle_files(SAMPLE_BUNDLE):
        if rel == "checksums.sha256":
            continue
        assert rel in entries, f"missing checksum entry for {rel}"
    assert "manifest.json" in entries


def test_verify_detects_tampered_candidate(tmp_path):
    tampered = tmp_path / "tampered"
    _copy_tree(SAMPLE_BUNDLE, tampered)
    cand = tampered / "intel_candidates" / "sjc_county_news.json"
    data = json.loads(cand.read_text())
    data["items"][0]["title"] = "Tampered Title"
    cand.write_text(json.dumps(data))
    checks, errors = run_checks(str(tampered))
    assert "file_sizes_and_checksums" in errors


def test_verify_rejects_extra_unexpected_file(tmp_path):
    extra = tmp_path / "extra"
    _copy_tree(SAMPLE_BUNDLE, extra)
    (extra / "surprise.json").write_text("{}")
    checks, errors = run_checks(str(extra))
    assert "no_unexpected_files" in errors


def test_import_stages_and_receipt_then_idempotent(tmp_path):
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    status, _msg, receipt = import_bundle(SAMPLE_BUNDLE, str(incoming), str(receipts), "abc123")
    assert status == "imported"
    assert receipt["status"] == "acknowledged"
    assert receipt["run_id"] == RUN_ID
    assert (incoming / RUN_ID / "manifest.json").exists()
    assert (receipts / f"{RUN_ID}.receipt.json").exists()
    assert (receipts / f"{RUN_ID}.receipt.json").is_file()

    status2, _msg2, receipt2 = import_bundle(SAMPLE_BUNDLE, str(incoming), str(receipts), "abc123")
    assert status2 == "idempotent"
    assert receipt2["receipt_id"] == receipt["receipt_id"]
    assert receipt2["bundle_sha256"] == receipt["bundle_sha256"]


def test_import_fails_without_receipt_on_bad_bundle(tmp_path):
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    bad = tmp_path / "bad"
    _copy_tree(SAMPLE_BUNDLE, bad)
    (bad / "intel_candidates" / "sjc_county_news.json").write_text("broken json{")
    status, msg, receipt = import_bundle(str(bad), str(incoming), str(receipts))
    assert status == "failed"
    assert receipt is None
    assert not list(receipts.glob("*.receipt.json"))


def test_import_stages_are_contained_and_corpus_untouched(tmp_path):
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    import_bundle(SAMPLE_BUNDLE, str(incoming), str(receipts))
    stage = incoming / RUN_ID
    root = os.path.abspath(stage)
    staged = list(stage.rglob("*"))
    assert staged  # bundle content staged
    assert all(os.path.abspath(str(p)).startswith(root) for p in staged)
    # The only side effects are under the incoming and receipt roots.
    side_effects = [p for p in tmp_path.rglob("*") if p != tmp_path]
    assert all(
        os.path.abspath(str(p)).startswith(os.path.abspath(str(incoming)))
        or os.path.abspath(str(p)).startswith(os.path.abspath(str(receipts)))
        for p in side_effects
    )


def test_import_same_run_id_different_content_is_conflict(tmp_path):
    incoming = tmp_path / "incoming"
    receipts = tmp_path / "receipts"
    import_bundle(SAMPLE_BUNDLE, str(incoming), str(receipts))
    altered = tmp_path / "altered"
    _copy_tree(SAMPLE_BUNDLE, altered)
    cand = altered / "intel_candidates" / "sjc_county_news.json"
    data = json.loads(cand.read_text())
    data["items"][0]["title"] = "Different content, same run_id"
    cand.write_text(json.dumps(data))
    # rebuild manifest + checksums for the altered bundle so verification passes
    from scripts.bundle_build import write_manifest_and_checksums
    run = build_run_json(str(altered), _Args(), count_candidates(str(altered)))
    run["candidate_counts"] = count_candidates(str(altered))
    write_manifest_and_checksums(str(altered), run, GIT_SHA, "sjc-weekly-001", REGISTRY_REV)
    status, msg, receipt = import_bundle(str(altered), str(incoming), str(receipts))
    assert status == "conflict"
    assert receipt is None


class _Args:
    run_id = RUN_ID
    git_sha = GIT_SHA
    profile = "sjc-weekly-001"
    registry_revision = REGISTRY_REV
    window_start = "2026-08-03T10:00:00Z"
    window_end = "2026-08-03T11:00:00Z"
    retention_deadline = "2026-08-17T11:00:00Z"
    status = "completed"
