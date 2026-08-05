import hashlib
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
NBOR_HTML = os.path.join(FIXTURE_DIR, "nbor_raw.html")
SJSO_RSS = os.path.join(FIXTURE_DIR, "sjso_feed.xml")
RUN_ID = "SJC-WK-20260803-0001"


def fingerprint(paths):
    """Return {relative_path: sha256} for a set of directory trees."""
    out = {}
    for root in paths:
        for dirpath, _dirs, fnames in os.walk(root):
            for fname in sorted(fnames):
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, REPO_ROOT)
                h = hashlib.sha256()
                with open(full, "rb") as f:
                    h.update(f.read())
                out[rel] = h.hexdigest()
    return out


def run_weekly(args):
    return subprocess.run(
        [sys.executable, "scripts/run_weekly.py"] + args,
        cwd=REPO_ROOT, capture_output=True, text=True,
    )


BASE_ARGS = [
    "--run-id", RUN_ID,
    "--monitor", "sjc_nbor_public_notices",
    "--offline-html", NBOR_HTML,
    "--git-sha", "1be2ade",
    "--registry-revision", "1be2ade",
    "--window-start", "2026-08-03T10:00:00Z",
    "--window-end", "2026-08-03T11:00:00Z",
]


def test_workspace_safe_run_does_not_mutate_corpus(tmp_path):
    protected = ["data", "registry"]
    before = fingerprint(protected)
    ws_root = tmp_path / "runtime" / "weekly"
    bundle_out = tmp_path / "bundles"
    result = run_weekly(BASE_ARGS + [
        "--workspace-root", str(ws_root),
        "--bundle-out", str(bundle_out),
    ])
    assert result.returncode == 0, result.stderr
    after = fingerprint(protected)
    assert after == before, "weekly run mutated protected corpus/registry paths"


def test_run_produces_expected_workspace_artifacts(tmp_path):
    ws_root = tmp_path / "runtime" / "weekly"
    result = run_weekly(BASE_ARGS + ["--workspace-root", str(ws_root)])
    assert result.returncode == 0, result.stderr
    ws = ws_root / RUN_ID
    assert (ws / "run.json").exists()
    assert (ws / "logs" / "run.log").exists()
    assert (ws / "raw" / "sjc_nbor_public_notices.html").exists()
    run = json.loads((ws / "run.json").read_text())
    assert run["run_id"] == RUN_ID
    assert run["run_status"] == "completed"
    assert run["producing_git_sha"] == "1be2ade"
    assert run["candidate_counts"]["by_source"]["sjc_nbor_public_notices"]["new"] == 25
    cands = json.loads((ws / "intel_candidates" / "sjc_nbor_public_notices.json").read_text())
    assert len(cands["items"]) == 25
    assert cands["items"][0]["status"] == "candidate"
    assert cands["items"][0]["review_status"] == "candidate"
    assert (ws / "source_health" / "sjc_nbor_public_notices.json").exists()
    assert (ws / "source_events" / "sjc_nbor_public_notices.json").exists()


def test_duplicate_run_id_is_rejected(tmp_path):
    ws_root = tmp_path / "runtime" / "weekly"
    first = run_weekly(BASE_ARGS + ["--workspace-root", str(ws_root)])
    assert first.returncode == 0
    second = run_weekly(BASE_ARGS + ["--workspace-root", str(ws_root)])
    assert second.returncode != 0
    assert "already exists" in second.stderr


def test_unknown_monitor_rejected(tmp_path):
    result = run_weekly([
        "--run-id", RUN_ID,
        "--monitor", "not_a_monitor",
        "--git-sha", "1be2ade",
        "--registry-revision", "1be2ade",
        "--window-start", "2026-08-03T10:00:00Z",
        "--window-end", "2026-08-03T11:00:00Z",
        "--workspace-root", str(tmp_path / "ws"),
    ])
    assert result.returncode == 2
    assert "not an approved monitor" in result.stderr


def test_bundle_out_is_verifiable(tmp_path):
    ws_root = tmp_path / "runtime" / "weekly"
    bundle_out = tmp_path / "bundles"
    result = run_weekly(BASE_ARGS + [
        "--workspace-root", str(ws_root),
        "--bundle-out", str(bundle_out),
    ])
    assert result.returncode == 0
    bundle = bundle_out / RUN_ID
    assert (bundle / "manifest.json").exists()
    assert (bundle / "source_proposals" / "proposals.json").exists()
    from scripts.bundle_verify import run_checks
    checks, errors = run_checks(str(bundle))
    assert not errors, errors


SJSO_ARGS = [
    "--run-id", RUN_ID,
    "--monitor", "sjso_news_stories",
    "--offline-rss", SJSO_RSS,
    "--git-sha", "1be2ade",
    "--registry-revision", "1be2ade",
    "--window-start", "2026-08-03T10:00:00Z",
    "--window-end", "2026-08-03T11:00:00Z",
]


def test_sjso_rss_monitor_produces_candidates(tmp_path):
    ws_root = tmp_path / "runtime" / "weekly"
    result = run_weekly(SJSO_ARGS + ["--workspace-root", str(ws_root)])
    assert result.returncode == 0, result.stderr
    ws = ws_root / RUN_ID
    cands = json.loads((ws / "intel_candidates" / "sjso_news_stories.json").read_text())
    assert len(cands["items"]) == 2
    by_title = {c["title"]: c for c in cands["items"]}
    # Crime/safety item flags human review; community event does not.
    jail = [c for c in cands["items"] if "Escape" in c["title"]][0]
    forum = [c for c in cands["items"] if "Forum" in c["title"]][0]
    assert jail["human_review_required"] is True
    assert jail["sensitivity"] == "medium"
    assert forum["human_review_required"] is False
    assert all(c["status"] == "candidate" and c["review_status"] == "candidate"
               for c in cands["items"])
    assert all(c["_dedupe_key"] for c in cands["items"])
    assert (ws / "source_events" / "sjso_news_stories.json").exists()
    assert (ws / "raw" / "sjso_news_stories.xml").exists()


def test_sjso_rss_does_not_mutate_corpus(tmp_path):
    protected = ["data", "registry"]
    before = fingerprint(protected)
    ws_root = tmp_path / "runtime" / "weekly"
    result = run_weekly(SJSO_ARGS + ["--workspace-root", str(ws_root)])
    assert result.returncode == 0
    after = fingerprint(protected)
    assert after == before
