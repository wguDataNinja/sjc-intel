"""Tests for publication-candidate preparation (never mutates publication state)."""
from pathlib import Path

import scripts.live_adaptive as la
from scripts import prepare_publication_candidates as ppc


def test_candidates_prepared_without_mutation(tmp_path, monkeypatch):
    r = la.initialize(tmp_path / "adaptive")
    la.write(r / "accepted_state.yaml", {"mode": "supervised-live-pilot", "last_run": "R1", "accepted": {
        "entities": [], "aliases": [], "search_profiles": [], "lanes": [],
        "milestones": [], "timelines": []}})
    run_dir = r / "runs" / "R1"
    run_dir.mkdir(parents=True)
    la.write(run_dir / "run.yaml", {"run_id": "R1", "mode": "supervised-live-pilot",
                                    "completed_at": "2026-08-06T00:00:00Z",
                                    "normalized_findings": [
                                        {"subject": "Magnolia Oaks Academy", "title": "School opens",
                                         "url": "https://x.example.com/1", "evidence_date": "2026-07-22",
                                         "confidence": "medium", "lane": "schools and families"}],
                                    "proposals": [], "evaluator_rejected": []})
    la.write(run_dir / "receipts.yaml", {"receipts": []})
    la.write(r / "health.yaml", {"mode": "supervised-live-pilot", "generated_at": "2026-08-06T00:00:00Z",
                                 "overall_health": "HEALTHY", "components": {}})
    monkeypatch.setattr(ppc, "ROOT", tmp_path)
    monkeypatch.setattr(ppc, "RUNTIME", r)
    text = ppc.render_candidates(la.read(run_dir / "run.yaml", {}), "R1")
    assert "NOT_APPROVED" in text
    assert "Magnolia Oaks Academy" in text
    assert "was modified by this script" in text
    # No publication paths were created.
    assert not (tmp_path / "data" / "publication_decisions").exists()
    assert not (tmp_path / "site").exists()
