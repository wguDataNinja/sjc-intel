import hashlib
import os
import shutil
import sys
import yaml

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.accept_candidates import (
    decide,
    load_candidates,
    REQUIRED_CANDIDATE_FIELDS,
)

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE_BUNDLE = os.path.join(FIXTURE_DIR, "sample_bundle")
RUN_ID = "SJC-WK-20260803-0001"
CAND_ID = "SJC-CN-20260803-0001"

REAL_REGISTRY = os.path.join(REPO_ROOT, "registry", "sources.yaml")
_REGISTRY_BEFORE = None


def setup_module():
    global _REGISTRY_BEFORE
    with open(REAL_REGISTRY, "rb") as f:
        _REGISTRY_BEFORE = hashlib.sha256(f.read()).hexdigest()


def teardown_module():
    with open(REAL_REGISTRY, "rb") as f:
        assert hashlib.sha256(f.read()).hexdigest() == _REGISTRY_BEFORE, \
            "registry/sources.yaml was mutated by a test"


def stage_fixture(tmp_path):
    """Copy the sample bundle into a staged incoming/{run_id} area."""
    incoming = tmp_path / "incoming"
    dst = incoming / RUN_ID
    shutil.copytree(SAMPLE_BUNDLE, dst)
    return str(incoming)


def corpus_dirs(tmp_path):
    return (
        str(tmp_path / "intel"),
        str(tmp_path / "index" / "prior_items.yaml"),
        str(tmp_path / "queue"),
    )


def test_decide_rejects_invalid_decision(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    with pytest.raises(ValueError):
        decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "auto", "buddy", "",
               incoming, *corpus_dirs(tmp_path))


def test_dry_run_accept_does_not_mutate(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)
    status, _msg, plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "accept",
                                "buddy", "", incoming, intel_root, index_file,
                                queue_dir, dry_run=True)
    assert status == "dry_run"
    assert plan["decision"] == "accept"
    assert not os.path.isdir(intel_root)
    assert not os.path.exists(index_file)


def test_accept_writes_pending_review_record_with_provenance(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)
    status, _msg, _plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "accept",
                                 "buddy", "approve", incoming, intel_root,
                                 index_file, queue_dir)
    assert status == "accepted"

    corpus_file = os.path.join(intel_root, "2026-08-03", "sjc_county_news.yaml")
    assert os.path.isfile(corpus_file)
    with open(corpus_file) as f:
        data = yaml.safe_load(f)
    item = data["items"][0]
    # Candidate ≠ accepted ≠ verified ≠ published.
    assert item["review_status"] == "pending_review"
    assert "status" not in item
    assert "outcome" not in item
    assert item["_origin_run_id"] == RUN_ID
    assert item["_reviewer"] == "buddy"
    assert item["source_url"].startswith("https://")
    # Dedupe + queue rebuilt with accepted record.
    with open(index_file) as f:
        index = yaml.safe_load(f)
    assert any(e["item_id"] == CAND_ID for e in index["prior_items"])
    with open(os.path.join(queue_dir, "queue.yaml")) as f:
        queue = yaml.safe_load(f)
    assert any(e["item_id"] == CAND_ID for e in queue["queue"])
    # Decision record auditable.
    dec = os.path.join(incoming, RUN_ID, "decisions", f"{CAND_ID}.yaml")
    assert os.path.isfile(dec)


def test_accept_is_idempotent(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)
    decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "accept", "buddy", "",
           incoming, intel_root, index_file, queue_dir)
    status, _msg, _plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "accept",
                                 "buddy", "", incoming, intel_root, index_file,
                                 queue_dir)
    assert status == "already_accepted"
    with open(os.path.join(intel_root, "2026-08-03", "sjc_county_news.yaml")) as f:
        data = yaml.safe_load(f)
    assert len(data["items"]) == 1


def test_reject_is_auditable_without_corpus_write(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)
    status, _msg, _plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "reject",
                                 "buddy", "noise", incoming, intel_root,
                                 index_file, queue_dir)
    assert status == "rejected"
    assert not os.path.isdir(intel_root)
    dec = os.path.join(incoming, RUN_ID, "decisions", f"{CAND_ID}.yaml")
    with open(dec) as f:
        record = yaml.safe_load(f)
    assert record["decision"] == "reject"
    assert record["rejection_reason"] == "noise"
    # Evidence preserved (staged candidate still present).
    assert os.path.isfile(os.path.join(incoming, RUN_ID, "intel_candidates",
                                       "sjc_county_news.json"))


def test_reject_is_idempotent(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)
    decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "defer", "buddy", "verify",
           incoming, intel_root, index_file, queue_dir)
    status, _msg, _plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "defer",
                                 "buddy", "verify", incoming, intel_root,
                                 index_file, queue_dir)
    assert status == "already_decided"


def test_rebuild_preserves_prior_review_decisions(tmp_path):
    incoming = stage_fixture(tmp_path)
    cands = load_candidates(incoming, RUN_ID)
    intel_root, index_file, queue_dir = corpus_dirs(tmp_path)

    # Pre-existing corpus item A that is already verified.
    os.makedirs(os.path.join(intel_root, "2026-07-01"))
    item_a = {
        "item_id": "SJC-A-20260701-0001",
        "title": "Unrelated verified item",
        "summary": "Already reviewed.",
        "source_id": "source_a",
        "source_url": "https://example.org/a",
        "discovered_at": "2026-07-01T00:00:00Z",
        "topics": ["general_government"],
        "geographic_scope": "county_wide",
        "urgency": "ongoing",
        "verification_status": "source_confirmed",
        "sensitivity": "low",
        "raw_excerpt": "unrelated",
        "human_review_required": False,
        "review_status": "verified",
    }
    with open(os.path.join(intel_root, "2026-07-01", "source_a.yaml"), "w") as f:
        yaml.dump({"source_id": "source_a", "items": [item_a]}, f)

    # Pre-existing queue decision for A.
    os.makedirs(queue_dir, exist_ok=True)
    entry_a = {
        "queue_id": "Q-SJC-A-20260701-0001",
        "item_id": "SJC-A-20260701-0001",
        "title": "Unrelated verified item",
        "review_status": "verified",
        "reviewer": "alice",
        "review_notes": "approved earlier",
        "reviewed_at": "2026-07-02T00:00:00Z",
    }
    with open(os.path.join(queue_dir, "queue.yaml"), "w") as f:
        yaml.dump({"queue": [entry_a]}, f)

    # Accept candidate B; rebuild must preserve A's verified state.
    status, _msg, _plan = decide(RUN_ID, CAND_ID, cands[CAND_ID][1], "accept",
                                 "buddy", "", incoming, intel_root, index_file,
                                 queue_dir)
    assert status == "accepted"

    with open(os.path.join(queue_dir, "queue.yaml")) as f:
        queue = yaml.safe_load(f)
    by_id = {e["item_id"]: e for e in queue["queue"]}
    assert by_id["SJC-A-20260701-0001"]["review_status"] == "verified"
    assert by_id["SJC-A-20260701-0001"]["reviewer"] == "alice"
    assert by_id[CAND_ID]["review_status"] == "pending_review"
