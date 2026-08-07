"""Tests for CURRENT_BRIEF generation, structure, modes, and safety."""
import importlib

import pytest

import scripts.live_adaptive as la
import scripts.build_current_brief as bc
from scripts.live_adaptive import initialize, read, write


@pytest.fixture
def runtime(tmp_path):
    r = initialize(tmp_path / "adaptive")
    write(r / "accepted_state.yaml", {"mode": "supervised-live-pilot", "accepted": {
        "entities": [], "aliases": [], "search_profiles": [], "lanes": [],
        "milestones": [], "timelines": []}, "last_run": "R1"})
    write(r / "health.yaml", {"mode": "supervised-live-pilot", "generated_at": "2026-08-06T00:00:00Z",
                              "overall_health": "HEALTHY", "components": {}})
    write(r / "coverage_health.yaml", {"mode": "supervised-live-pilot", "fresh": ["Magnolia Oaks Academy"],
                                "stale": [], "missed_milestones": [], "no_yield_queries": [],
                                "source_gaps": [], "lanes_covered": []})
    run_dir = r / "runs" / "R1"
    run_dir.mkdir(parents=True)
    write(run_dir / "run.yaml", {"run_id": "R1", "mode": "supervised-live-pilot", "completed_at": "2026-08-06T00:01:00Z",
                                 "artifact": "runtime/adaptive_discovery/runs/R1/run.yaml",
                                 "normalized_findings": [], "proposals": [], "evaluator_rejected": [],
                                 "search_failure": None})
    write(run_dir / "receipts.yaml", {"receipts": []})
    return r


def test_required_sections_present_and_ordered(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "reports/briefs/X.md", "2026-08-06T00:02:00Z", root=runtime)
    positions = [text.find(f"## {s}") for s in bc.REQUIRED_SECTIONS]
    assert all(p >= 0 for p in positions)
    assert positions == sorted(positions)


def test_header_fields(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    for h in bc.REQUIRED_HEADERS:
        assert f"**{h}" in text


def test_mode_labeling(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    for mode in bc.VALID_MODES:
        text = bc.render(mode, "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
        assert f"**Mode:** {mode}" in text


def test_health_evidence_required(runtime, monkeypatch):
    r = runtime
    write(r / "health.yaml", {"mode": "supervised-live-pilot", "components": {}})  # no generated_at
    import shutil
    shutil.rmtree(r / "runs" / "R1")  # no run artifact either
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    with pytest.raises(ValueError):
        bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=r)


def test_stale_input_warning(runtime, monkeypatch):
    r = runtime
    write(r / "health.yaml", {"mode": "supervised-live-pilot", "generated_at": "2026-07-20T00:00:00Z",
                              "overall_health": "HEALTHY", "components": {}})
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=r)
    assert "WARNING" in text and "stale" in text


def test_atomic_replacement(runtime, monkeypatch, tmp_path):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "reports/briefs/atom.md", "2026-08-06T00:02:00Z", root=runtime)
    la.atomic(tmp_path / "adaptive" / "CURRENT_BRIEF.md", text)
    assert (tmp_path / "adaptive" / "CURRENT_BRIEF.md").read_text() == text


def test_check_mode(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert bc.validate(text) == []


def test_check_detects_private_path(runtime):
    good = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert bc.validate(good) == []
    leaked = good + "\nsecret=/Users/buddy/.ssh/id_rsa\npassword=hunter2\n"
    problems = bc.validate(leaked)
    assert any("private marker" in p for p in problems)


def test_deterministic_generation(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    a = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    b = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert a == b


def test_brief_includes_research_and_active_search_sections(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    write(runtime / "research_resolutions.yaml", {"resolutions": [
        {"subject": "SilverLeaf grocery center — possible Harris Teeter",
         "summary": "project exists with inferred identity; tenant unconfirmed",
         "recommended_action": "ACCEPT_QUALIFIED", "confidence": 0.6}]})
    state = read(runtime / "accepted_state.yaml", {})
    state["accepted"]["search_profiles"] = [
        {"subject": "Magnolia Oaks Academy", "queries": ['"Magnolia Oaks Academy"']}]
    state["accepted"]["entities"] = [
        {"subject": "Publix at Silverleaf Market"},
        {"subject": "SilverLeaf grocery center — possible Harris Teeter"}]
    write(runtime / "accepted_state.yaml", state)
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert "## Research findings" in text
    assert "ACCEPT_QUALIFIED" in text
    assert "## Active search profiles" in text
    assert '"Magnolia Oaks Academy"' in text
    assert "Publix at Silverleaf Market" in text
    assert "## Decisions completed" in text


def test_brief_status_headers_include_scheduler_and_deployment(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert "**Scheduler status:**" in text
    assert "**Deployment status:**" in text


def test_bucket_mapping_complete():
    for kind in ("entity", "search_profile", "coverage_lane", "timeline_reconciliation",
                 "milestone", "alias"):
        assert bc._bucket(kind) is not None


def test_pending_decisions_require_operator_review(runtime, monkeypatch):
    write(runtime / "pending_proposals.yaml", {"proposals": [{
        "proposal_id": "P1", "type": "entity", "subject": "Subject",
        "evidence": [{"url": "https://example.com", "title": "Evidence"}],
        "expected_benefit": "follow up", "cost_or_budget": 1, "risk": "unverified",
        "proposed_state_transition": "isolated only",
    }]})
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert "**Pipeline health:** HEALTHY" in text
    assert "**Operator status:** NEEDS_REVIEW" in text
    assert "**Overall status:** NEEDS_REVIEW" in text


def test_no_pending_uses_pipeline_health_as_overall_status(runtime, monkeypatch):
    monkeypatch.setattr(bc, "sha", lambda: "abc123")
    text = bc.render("supervised-live-pilot", "R1", "snap.md", "2026-08-06T00:02:00Z", root=runtime)
    assert "**Operator status:** CLEAR" in text
    assert "**Overall status:** HEALTHY" in text
