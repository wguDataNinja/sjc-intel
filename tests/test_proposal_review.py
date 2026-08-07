"""Tests for the human proposal-review workflow (accept/reject/defer/rollback)."""
import pytest

from scripts.live_adaptive import initialize, read, write, review


@pytest.fixture
def runtime(tmp_path):
    r = initialize(tmp_path / "adaptive")
    write(r / "accepted_state.yaml", {"mode": "supervised-live-pilot", "accepted": {
        "entities": [], "aliases": [], "search_profiles": [], "lanes": [],
        "milestones": [], "timelines": []}, "last_run": None})
    write(r / "pending_proposals.yaml", {"proposals": [
        {"proposal_id": "P1", "type": "entity", "subject": "Magnolia Oaks Academy",
         "proposed_state_transition": "isolated only", "status": "pending_human_review",
         "evidence": [{"url": "https://x.example.com/1", "title": "t", "date": "2026-07-22", "query_id": "q"}]},
        {"proposal_id": "P2", "type": "search_profile", "subject": "CR 2209 connector",
         "proposed_state_transition": "isolated only", "status": "pending_human_review", "evidence": []},
    ]})
    write(r / "decisions.yaml", {"decisions": []})
    return r


def make_proposal(pid, kind, subject):
    return {"proposal_id": pid, "type": kind, "subject": subject,
            "proposed_state_transition": "isolated only", "status": "pending_human_review",
            "evidence": [{"url": "https://x.example.com/1", "title": "t", "date": "2026-07-22", "query_id": "q"}]}


def test_accept_applies_to_isolated_state(runtime):
    review("P1", "accept", "Buddy", "verified", runtime)
    state = read(runtime / "accepted_state.yaml", {})
    assert [e["proposal_id"] for e in state["accepted"]["entities"]] == ["P1"]
    assert read(runtime / "pending_proposals.yaml", {})["proposals"] == [
        x for x in read(runtime / "pending_proposals.yaml", {})["proposals"] if x["proposal_id"] != "P1"]
    assert not any(p["proposal_id"] == "P1" for p in read(runtime / "pending_proposals.yaml", {})["proposals"])


def test_reject_preserves_decision_and_removes_pending(runtime):
    review("P1", "reject", "Buddy", "not verifiable", runtime)
    assert not any(p["proposal_id"] == "P1" for p in read(runtime / "pending_proposals.yaml", {})["proposals"])
    decisions = read(runtime / "decisions.yaml", {})["decisions"]
    assert decisions and decisions[-1]["action"] == "reject" and decisions[-1]["proposal_id"] == "P1"


def test_defer_moves_out_of_pending_with_record(runtime):
    review("P1", "defer", "Buddy", "follow up later", runtime)
    assert not any(p["proposal_id"] == "P1" for p in read(runtime / "pending_proposals.yaml", {})["proposals"])
    decisions = read(runtime / "decisions.yaml", {})["decisions"]
    assert decisions[-1]["action"] == "defer"


def test_dry_run_mutates_nothing(runtime):
    review("P1", "accept", "Buddy", "dry", runtime, dry_run=True)
    assert read(runtime / "accepted_state.yaml", {})["accepted"]["entities"] == []
    assert any(p["proposal_id"] == "P1" for p in read(runtime / "pending_proposals.yaml", {})["proposals"])
    assert read(runtime / "decisions.yaml", {})["decisions"] == []


def test_invalid_action_rejected(runtime):
    with pytest.raises(ValueError):
        review("P1", "publish", "Buddy", "x", runtime)


def test_unknown_proposal_rejected(runtime):
    with pytest.raises(ValueError):
        review("NOPE", "accept", "Buddy", "x", runtime)


def test_rollback_restores_pending_and_clears_state(runtime):
    result = review("P1", "accept", "Buddy", "yes", runtime)
    assert read(runtime / "accepted_state.yaml", {})["accepted"]["entities"]
    review("P1", "rollback", "Buddy", "undo", runtime, decision_id=result["decision_id"])
    assert read(runtime / "accepted_state.yaml", {})["accepted"]["entities"] == []
    assert any(p["proposal_id"] == "P1" for p in read(runtime / "pending_proposals.yaml", {})["proposals"])
    decisions = read(runtime / "decisions.yaml", {})["decisions"]
    assert decisions[-1]["action"] == "rollback" and decisions[-1]["reverses"] == result["decision_id"]


def test_rollback_requires_matching_acceptance(runtime):
    with pytest.raises(ValueError):
        review("P1", "rollback", "Buddy", "x", runtime, decision_id="DEC-missing")


def test_rollback_wrong_proposal_mismatch(runtime):
    result = review("P1", "accept", "Buddy", "yes", runtime)
    with pytest.raises(ValueError):
        review("P2", "rollback", "Buddy", "x", runtime, decision_id=result["decision_id"])


def test_decision_history_append_only(runtime):
    review("P1", "accept", "Buddy", "a", runtime)
    review("P1", "rollback", "Buddy", "b", runtime, decision_id=read(runtime / "decisions.yaml", {})["decisions"][0]["decision_id"])
    decisions = read(runtime / "decisions.yaml", {})["decisions"]
    assert [d["action"] for d in decisions] == ["accept", "rollback"]
    assert [d["proposal_id"] for d in decisions] == ["P1", "P1"]


def test_unsupported_type_accept_rejected(runtime):
    r2 = initialize(runtime / "other")
    write(r2 / "pending_proposals.yaml", {"proposals": [make_proposal("P9", "timeline_reconciliation", "X")]})
    review("P9", "accept", "Buddy", "ok", r2)
    state = read(r2 / "accepted_state.yaml", {})
    assert len(state["accepted"]["timelines"]) == 1
