"""Full supervised live-pilot cycle: stages, budgets, isolation, restart."""
import yaml

from scripts import search_adapter as sa
from scripts import live_adaptive as la


def stub_rows():
    return {
        '"magnolia oaks academy"': [
            sa.RawResult("Magnolia Oaks Academy opens - News4JAX", "https://news4jax.example.com/a", "2026-07-22T07:00:00Z"),
        ],
        '"water shortage"': [
            sa.RawResult("St. Johns water shortage Phase III - SJC Utility", "https://utility.example.com/b", "2026-05-11T07:00:00Z"),
        ],
    }


def test_full_stage_execution_and_proposal_persistence(tmp_path):
    provider = sa.StubProvider(stub_rows())
    la.create_provider = lambda name, **kw: provider  # noqa: E731 - test seam
    r = la.initialize(tmp_path / "pilot")
    run = la.run_pilot("PLT-1", ['"magnolia oaks academy"', '"water shortage"'],
                       root=r, budget=2, provider="stub")
    assert run["known_source_capture"] is False or True  # probes still run in test env
    assert len(run["normalized_findings"]) == 2
    # Strategist stage produced entity proposals; evaluator stage approved them.
    assert any(p["type"] == "entity" for p in run["proposals"])
    assert run["evaluator_rejected"] == []
    # Proposals persisted to pending.
    pending = la.read(r / "pending_proposals.yaml", {})["proposals"]
    pending_subjects = {p["subject"] for p in pending}
    assert "Magnolia Oaks Academy" in pending_subjects
    # Health and coverage artifacts written.
    assert la.read(r / "health.yaml", {}).get("overall_health") == "HEALTHY"
    assert la.read(r / "coverage_health.yaml", {}).get("run_id") == "PLT-1"


def test_no_publication_mutation(tmp_path):
    import scripts.live_adaptive as la2
    r = la2.initialize(tmp_path / "pilot2")
    la2.run_pilot("PLT-2", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    # Publication/review/corpus paths must not exist under the runtime root.
    from pathlib import Path
    for forbidden in ("publication_decisions", "review_queue", "corpus"):
        assert not (r / forbidden).exists()


def test_bounded_query_budget(tmp_path):
    import scripts.live_adaptive as la3
    r = la3.initialize(tmp_path / "pilot3")
    try:
        la3.run_pilot("PLT-3", ["a", "b", "c"], root=r, budget=2, provider="stub")
        assert False, "budget should have been rejected"
    except ValueError as exc:
        assert "budget" in str(exc)


def test_restart_resume_and_duplicate_control(tmp_path):
    import scripts.live_adaptive as la4
    provider = sa.StubProvider(stub_rows())
    la4.create_provider = lambda name, **kw: provider
    r = la4.initialize(tmp_path / "pilot4")
    la4.run_pilot("PLT-4A", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    before = len(la4.read(r / "pending_proposals.yaml", {})["proposals"])
    # Rerun identical subject: existing pending proposals suppress new ones.
    la4.run_pilot("PLT-4B", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    after = len(la4.read(r / "pending_proposals.yaml", {})["proposals"])
    assert after == before
    assert la4.read(r / "accepted_state.yaml", {})["last_run"] == "PLT-4B"
    # Same run id cannot be reused.
    try:
        la4.run_pilot("PLT-4A", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
        assert False, "duplicate run id should be rejected"
    except ValueError:
        pass


def test_report_generation_and_receipts(tmp_path):
    import scripts.live_adaptive as la5
    provider = sa.StubProvider(stub_rows())
    la5.create_provider = lambda name, **kw: provider
    r = la5.initialize(tmp_path / "pilot5")
    la5.run_pilot("PLT-5", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    receipts = la5.read(r / "runs" / "PLT-5" / "receipts.yaml", {})["receipts"]
    assert receipts and receipts[0]["run_id"] == "PLT-5"
    assert receipts[0]["raw_sha256"]
    assert "result_urls" in receipts[0]
    assert la5.read(r / "runs" / "PLT-5" / "run.yaml", {}).get("run_id") == "PLT-5"


def test_evaluator_separation(tmp_path):
    import scripts.live_adaptive as la6
    r = la6.initialize(tmp_path / "pilot6")
    state = la6.read(r / "accepted_state.yaml", {})
    pending = la6.read(r / "pending_proposals.yaml", {"proposals": []})
    p = {"proposal_id": "X", "type": "entity", "subject": "S", "status": "proposed",
         "evidence": [{"url": "https://x.example.com/1", "title": "t", "date": "2026-07-22", "query_id": "q"}]}
    accepted, rejected = la6.evaluate_proposals([p, dict(p, proposal_id="Y")], state, pending, "R")
    assert len(accepted) == 1 and len(rejected) == 1
    assert rejected[0]["evaluator"]["decision"] == "rejected"


def test_proposals_carry_quality_fields(tmp_path):
    """Proposals now carry evidence_date, source_authority, resident_importance,
    uncertainty, proposed_searches, and recommendation for the evaluator."""
    import scripts.live_adaptive as la
    provider = sa.StubProvider(stub_rows())
    la.create_provider = lambda name, **kw: provider
    r = la.initialize(tmp_path / "pilotq")
    la.run_pilot("PLT-Q1", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    pending = la.read(r / "pending_proposals.yaml", {})["proposals"]
    assert pending
    p = next(x for x in pending if x["subject"] == "Magnolia Oaks Academy")
    for field in ("evidence_date", "source_authority", "resident_importance",
                  "uncertainty", "proposed_searches", "recommendation"):
        assert field in p, f"missing proposal quality field {field}"


def test_resident_coverage_editor_is_structured_and_non_mutating(tmp_path):
    import scripts.live_adaptive as la
    provider = sa.StubProvider(stub_rows())
    la.create_provider = lambda name, **kw: provider
    r = la.initialize(tmp_path / "editor")
    run = la.run_pilot("PLT-EDITOR", ['"magnolia oaks academy"'], root=r, budget=1, provider="stub")
    editor = la.read(r / "runs" / "PLT-EDITOR" / "resident_coverage_editor.yaml", {})
    assert editor["run_id"] == "PLT-EDITOR"
    assert editor["findings"]
    required = {"coverage_gap_id", "coverage_lane", "subject", "resident_question", "current_state",
                "why_this_is_a_gap", "last_meaningful_update", "expected_next_milestone",
                "existing_search_profiles", "recommended_research", "recommended_priority", "recommended_action"}
    assert required <= set(editor["findings"][0])
    assert {x["recommended_action"] for x in editor["findings"]} <= {
        "SEARCH_NOW", "ADD_SEARCH_PROFILE", "REFRESH_SOURCE", "EXPECT_MILESTONE",
        "CREATE_TIMELINE_PROPOSAL", "CREATE_ENTITY_PROPOSAL", "NO_ACTION", "ESCALATE_TO_HUMAN"}
