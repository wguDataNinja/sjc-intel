import shutil
from pathlib import Path
import yaml

from scripts import adaptive_backtest as ab


def make_sim(tmp_path):
    root = tmp_path / "backtests"
    old = ab.BACKTESTS
    ab.BACKTESTS = root
    cfg = {"start": "2025-05-05", "seed_entities": [{"label": "Seed", "available_on": "2025-05-05", "aliases": []}],
           "evaluator_baseline": [{"subject": "School QQ", "priority": "high"}]}
    ab.init("test", cfg)
    ab.dump(ab.root("test") / "replay_evidence.yaml", [{"id":"E1","available_on":"2025-05-07","source":"official","title":"School QQ update","subject":"School QQ","event_type":"proposed","lane":"schools and families","expected_milestones":["opening"]}, {"id":"E2","available_on":"2025-05-21","source":"official","title":"Magnolia Oaks Academy opens","subject":"Magnolia Oaks Academy","alias_for":"School QQ","event_type":"opened","lane":"schools and families"}])
    return old


def test_future_evidence_and_alias_are_withheld(tmp_path):
    old = make_sim(tmp_path)
    try:
        r = ab.run_week("test", "2025-05-05", "2025-05-11")
        assert {x["subject"] for x in r["findings"]} == {"School QQ"}
        state = ab.state_for(ab.root("test"), ab.day("2025-05-12"))
        assert state["entities"][-1]["label"] == "School QQ"
        assert "Magnolia" not in str(state)
        r = ab.run_week("test", "2025-05-19", "2025-05-25")
        assert any(p["type"] == "alias" and p["subject"] == "Magnolia Oaks Academy" for p in r["evaluator"]["accepted"])
    finally:
        ab.BACKTESTS = old


def test_deterministic_resume_and_no_baseline_in_generator(tmp_path):
    old = make_sim(tmp_path)
    try:
        one = ab.run_week("test", "2025-05-05", "2025-05-11")
        two = ab.run_week("test", "2025-05-05", "2025-05-11", dry_run=True)
        assert one["findings"] == two["findings"]
        assert "evaluator_baseline" not in ab.generate.__code__.co_varnames
        assert ab.metrics(ab.root("test"))["leakage_violations"] == 0
    finally:
        ab.BACKTESTS = old


def test_evaluator_rejects_future_evidence_and_duplicate_transition(tmp_path):
    old = make_sim(tmp_path)
    try:
        state = ab.state_for(ab.root("test"), ab.day("2025-05-05"))
        future = ab.proposal(ab.day("2025-05-05"), "entity", "Future", {"id":"F", "source":"x", "available_on":"2025-05-20", "excerpt":"future"})
        accepted, rejected = ab.evaluate(state, [future], ab.day("2025-05-11"))
        assert not accepted and "future evidence" in rejected[0]["rationale"]
        valid = ab.proposal(ab.day("2025-05-05"), "entity", "Valid", {"id":"V", "source":"x", "available_on":"2025-05-05", "excerpt":"now"})
        accepted, rejected = ab.evaluate(state, [valid, valid], ab.day("2025-05-11"))
        assert len(accepted) == 1 and len(rejected) == 1
    finally:
        ab.BACKTESTS = old


def test_milestone_overdue_and_met(tmp_path):
    old = make_sim(tmp_path)
    try:
        cfg = {"start": "2025-05-05", "end": "2026-08-03", "seed_entities": [], "evaluator_baseline": []}
        ab.init("ms", cfg)
        state = ab.initial_state(cfg)
        state["milestones"] = [
            {"subject": "School QQ", "available_on": "2025-05-12",
             "expected": ["opening"], "milestone_due": {"opening": "2026-07-01"}},
            {"subject": "CR 2209", "available_on": "2025-08-27",
             "expected": ["completion"], "milestone_due": {"completion": "2026-01-15"}},
        ]
        state["findings"] = [
            {"subject": "School QQ", "event_type": "opened", "available_on": "2026-07-22"},
        ]
        overdue, met = ab.milestone_status(state, ab.day("2026-08-03"))
        assert [m["subject"] for m in overdue] == ["CR 2209"]
        assert [m["subject"] for m in met] == ["School QQ"]
    finally:
        ab.BACKTESTS = old


def test_stale_subject_detection(tmp_path):
    old = make_sim(tmp_path)
    try:
        cfg = {"start": "2025-05-05", "end": "2026-08-03", "seed_entities": [], "evaluator_baseline": []}
        ab.init("st", cfg)
        state = ab.initial_state(cfg)
        state["entities"] = [{"label": "Old", "available_on": "2025-05-05"}]
        state["search_profiles"] = [{"subject": "Fresh", "queries": [], "available_on": "2025-05-05"}]
        state["findings"] = [{"subject": "Fresh", "available_on": "2026-07-01"}]
        stale = ab.stale_subjects(state, ab.day("2026-08-03"), stale_days=60)
        assert "Old" in stale and "Fresh" not in stale
    finally:
        ab.BACKTESTS = old


def test_search_profile_yield(tmp_path):
    old = make_sim(tmp_path)
    try:
        cfg = {"start": "2025-05-05", "end": "2026-08-03", "seed_entities": [], "evaluator_baseline": []}
        ab.init("y", cfg)
        w = ab.root("y") / "weeks" / "2025-05-05"
        w.mkdir(parents=True)
        ab.dump(w / "report.yaml", {
            "searches_executed": [{"subject": "School QQ", "queries": ["q1"], "yielded": True}],
            "findings": [{"subject": "School QQ"}],
        })
        ab.dump(ab.root("y") / "state.json", {"search_profiles": [{"subject": "School QQ"}]})
        result = ab.search_profile_yield(ab.root("y"))
        assert result["profile_yield_rate"] == 1.0 and result["query_attempts"] == 1
    finally:
        ab.BACKTESTS = old


def test_lane_coverage_health(tmp_path):
    old = make_sim(tmp_path)
    try:
        cfg = {"start": "2025-05-05", "end": "2026-08-03", "seed_entities": [], "evaluator_baseline": []}
        ab.init("lc", cfg)
        for wk in ("2025-05-05", "2025-05-12"):
            w = ab.root("lc") / "weeks" / wk
            w.mkdir(parents=True)
            ab.dump(w / "report.yaml", {"findings": [{"subject": "School QQ", "lane": "schools and families"}]})
        health = ab.lane_coverage_health(ab.root("lc"))
        assert health["total_weeks"] == 2
        assert health["lanes"]["schools and families"]["weeks_covered"] == 2
        assert health["lanes"]["schools and families"]["coverage_rate"] == 1.0
    finally:
        ab.BACKTESTS = old


def test_broader_fixture_honest_misses(tmp_path):
    """Expanded fixture must report overdue milestones rather than all-pass."""
    old = make_sim(tmp_path)
    try:
        cfg = {"start": "2025-05-05", "end": "2026-08-03", "seed_entities": [], "evaluator_baseline": [
            {"subject": "School QQ", "priority": "high"},
            {"subject": "CR 2209 connector", "priority": "high"}]}
        ab.init("honest", cfg)
        ab.dump(ab.root("honest") / "replay_evidence.yaml", [
            {"id": "E1", "available_on": "2025-05-07", "source": "official", "title": "School QQ build",
             "subject": "School QQ", "event_type": "construction_started", "lane": "growth and construction",
             "expected_milestones": ["opening"], "milestone_due": {"opening": "2026-08-15"}},
        ])
        ab.run_backtest("honest", "2025-05-05", "2026-08-03")
        result = ab.metrics(ab.root("honest"))
        # CR 2209 connector is an honest miss; School QQ opening not yet due.
        assert "CR 2209 connector" in result["subjects_missed"]
        assert result["overdue_milestones"] == 0
        assert result["leakage_violations"] == 0
    finally:
        ab.BACKTESTS = old
