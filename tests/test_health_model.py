"""Tests for the pipeline-health model and coverage health."""
import datetime as dt

from scripts.live_adaptive import HEALTH_COMPONENTS, coverage_health_from, health_from, initialize, read, write
from scripts import adaptive_backtest as ab


def fake_run(completed="2026-08-06T00:00:00Z", failure=None, artifact="runtime/adaptive_discovery/runs/R/run.yaml"):
    return {"run_id": "R", "mode": "supervised-live-pilot", "completed_at": completed,
            "artifact": artifact, "normalized_findings": [], "proposals": [],
            "evaluator_rejected": [], "search_failure": failure,
            "known_source_capture": True, "normalization": True, "dedupe": True,
            "identity_reconciliation": True, "strategist": True, "editor": True,
            "evaluator": True, "proposal_storage": True, "timeline_state": True,
            "milestones": True, "coverage_health": True,
            "publication_candidate_handoff": True, "report_generation": True,
            "state_persistence": True}


def test_all_required_components_present(tmp_path):
    r = initialize(tmp_path / "h")
    run = fake_run()
    write(r / "runs" / "R" / "run.yaml", run)
    write(r / "runs" / "R" / "receipts.yaml", {"receipts": []})
    health = health_from(run, r)
    assert set(health["components"].keys()) == set(HEALTH_COMPONENTS)
    for key in HEALTH_COMPONENTS:
        comp = health["components"][key]
        for field in ("status", "last_success", "last_failure", "evidence_artifact",
                      "freshness_threshold_hours", "failure_count", "warning_count", "action_required"):
            assert field in comp


def test_healthy_overall(tmp_path):
    r = initialize(tmp_path / "h")
    run = fake_run()
    health = health_from(run, r)
    assert health["overall_health"] == "HEALTHY"


def test_degraded_overall_on_failure(tmp_path):
    r = initialize(tmp_path / "h")
    run = fake_run(failure="timeout")
    write(r / "runs" / "R" / "run.yaml", run)
    write(r / "runs" / "R" / "receipts.yaml", {"receipts": []})
    health = health_from(run, r)
    assert health["overall_health"] == "DEGRADED"
    assert health["components"]["live_search"]["status"] == "DEGRADED"


def test_blocked_overall(tmp_path):
    r = initialize(tmp_path / "h")
    run = fake_run()
    run["blocked"] = True
    health = health_from(run, r)
    assert health["overall_health"] == "BLOCKED"


def test_stale_subject_detection(tmp_path):
    r = initialize(tmp_path / "h")
    state = {"mode": "supervised-live-pilot", "last_run": "R", "accepted": {
        "entities": [{"label": "Old Subject", "available_on": "2026-01-01"}],
        "search_profiles": [{"subject": "Fresh Subject", "available_on": "2026-01-01"}],
        "lanes": [], "milestones": [], "timelines": [], "aliases": []}}
    write(r / "accepted_state.yaml", state)
    run = fake_run()
    run["normalized_findings"] = [
        {"subject": "Fresh Subject", "evidence_date": "2026-08-05T00:00:00Z"},
        {"subject": "New", "evidence_date": "2026-08-05T00:00:00Z"}]
    write(r / "runs" / "R" / "run.yaml", run)
    write(r / "runs" / "R" / "receipts.yaml", {"receipts": []})
    cov = coverage_health_from(run, r, stale_days=35)
    assert "Fresh Subject" not in cov["stale"]
    assert "Old Subject" in cov["stale"]


def test_no_yield_and_source_gap(tmp_path):
    r = initialize(tmp_path / "h")
    write(r / "accepted_state.yaml", {"mode": "supervised-live-pilot", "last_run": "R", "accepted": {
        "entities": [], "search_profiles": [], "lanes": [], "milestones": [], "timelines": [], "aliases": []}})
    run = fake_run()
    run["source_health"] = {"sjc_county_news": {"status": "DEGRADED", "error": "x"}}
    write(r / "runs" / "R" / "run.yaml", run)
    write(r / "runs" / "R" / "receipts.yaml", {"receipts": [
        {"query": "\"nothing\"", "accepted_result_count": 0, "failure": None}]})
    cov = coverage_health_from(run, r)
    assert "\"nothing\"" in cov["no_yield_queries"]
    assert "sjc_county_news" in cov["source_gaps"]


def test_backtest_milestone_overdue_and_met(tmp_path):
    old = ab.BACKTESTS
    ab.BACKTESTS = tmp_path / "bt"
    try:
        cfg = {"start": "2025-05-05", "seed_entities": [], "evaluator_baseline": [],
               "end": "2026-08-03"}
        ab.init("m", cfg)
        state = ab.initial_state(cfg)
        state["milestones"] = [
            {"subject": "School QQ", "available_on": "2025-05-12",
             "expected": ["opening"], "milestone_due": {"opening": "2026-07-01"}},
            {"subject": "CR 2209 connector", "available_on": "2025-08-27",
             "expected": ["completion"], "milestone_due": {"completion": "2026-01-15"}},
        ]
        state["findings"] = [
            {"subject": "School QQ", "event_type": "opened", "available_on": "2026-07-22"},
        ]
        overdue, met = ab.milestone_status(state, ab.day("2026-08-03"))
        assert [m["subject"] for m in overdue] == ["CR 2209 connector"]
        assert [m["subject"] for m in met] == ["School QQ"]
        assert ab.stale_subjects(state, ab.day("2026-08-03"), stale_days=60) == []
    finally:
        ab.BACKTESTS = old


def test_backtest_search_profile_yield(tmp_path):
    old = ab.BACKTESTS
    ab.BACKTESTS = tmp_path / "bt"
    try:
        cfg = {"start": "2025-05-05", "seed_entities": [], "evaluator_baseline": [], "end": "2026-08-03"}
        ab.init("y", cfg)
        (tmp_path / "bt" / "y" / "weeks" / "2025-05-05").mkdir(parents=True)
        ab.dump(tmp_path / "bt" / "y" / "weeks" / "2025-05-05" / "report.yaml",
                {"searches_executed": [{"subject": "School QQ", "queries": ["q"], "yielded": True}],
                 "findings": [{"subject": "School QQ"}]})
        ab.dump(tmp_path / "bt" / "y" / "state.json", {"search_profiles": [{"subject": "School QQ"}]})
        result = ab.search_profile_yield(tmp_path / "bt" / "y")
        assert result["profile_yield_rate"] == 1.0
        assert result["query_attempts"] == 1
    finally:
        ab.BACKTESTS = old
