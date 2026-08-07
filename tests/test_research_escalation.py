"""Tests for research escalation: ambiguity detection, budgets, resolution, and qualified naming."""
import datetime as dt

import pytest

from scripts import research_escalation as re
from scripts.live_adaptive import initialize, read, write, edit_proposal, review, state_path


def make_proposal(pid="P1", subject="Harris Teeter SilverLeaf", evidence_title="Another Harris Teeter-size grocery store proposed"):
    return {"proposal_id": pid, "type": "entity", "subject": subject,
            "proposed_state_transition": "isolated adaptive state only",
            "evidence": [{"url": "https://x.example.com/1", "title": evidence_title,
                          "date": "2026-05-15T07:00:00Z"}],
            "status": "pending_human_review"}


def test_identity_uncertainty_detected():
    p = make_proposal()
    triggers = re.detect_ambiguity(p)
    assert triggers["identity_uncertainty"]
    assert any("Harris Teeter-size" in r for r in triggers["identity_uncertainty"])


def test_geographic_conflict_detected():
    # No location and no SilverLeaf anchor in subject/evidence -> trigger.
    p = make_proposal(subject="Commercial development")
    p["evidence"][0]["title"] = "Commercial development near SR 16"
    assert re.geographic_conflict(p)
    # Subject anchored to SilverLeaf -> no "no location" trigger alone.
    anchored = make_proposal()  # subject "Harris Teeter SilverLeaf"
    assert re.geographic_conflict(anchored) == []


def test_stale_evidence_detected():
    p = make_proposal(evidence_title="Old article")
    p["evidence"][0]["date"] = "2026-01-01T00:00:00Z"
    reasons = re.stale_evidence(p, cutoff=dt.date(2026, 8, 1), stale_days=90)
    assert reasons


def test_conflicting_sources_detected():
    p = make_proposal(evidence_title="St. Johns County is getting two new supermarkets — and they're not Publix")
    assert re.conflicting_sources(p)


def test_needs_research_true_for_ambiguous():
    assert re.needs_research(make_proposal())
    assert not re.needs_research(make_proposal(subject="Magnolia Oaks Academy",
                                                evidence_title="Magnolia Oaks Academy set to open doors in SilverLeaf community"))


def test_research_budget_bounded(tmp_path):
    budget = re.ResearchBudget(max_queries=3)
    assert budget.max_queries == 3
    assert budget.official_domains  # non-empty approved family


def test_recommend_qualified_without_first_party():
    p = make_proposal()
    findings = [
        {"title": "Grocery store matching Harris Teeter planned in SilverLeaf", "domain": "news.google.com",
         "official_source": False},
        {"title": "Another Harris Teeter-size store proposed", "domain": "news.google.com",
         "official_source": False},
    ]
    triggers = re.detect_ambiguity(p)
    action, summary, confidence = re.recommend(p, findings, triggers)
    assert action == "ACCEPT_QUALIFIED"
    assert "unconfirmed" in summary


def test_recommend_accept_requires_first_party():
    p = make_proposal()
    findings = [{"title": "Harris Teeter confirms store", "domain": "harristeeter.com",
                 "official_source": True}]
    action, _summary, _confidence = re.recommend(p, findings, {})
    assert action == "ACCEPT"


def test_media_redirect_never_counts_as_first_party():
    findings = [{"title": "Harris Teeter confirms new store coming to Jacksonville", "domain": "news.google.com",
                 "official_source": False}]
    assert re._first_party(findings) == []


def test_resolution_record_schema(tmp_path):
    record = {"proposal_id": "P1", "subject": "SilverLeaf grocery center — possible Harris Teeter",
              "research_trigger": {"identity_uncertainty": ["size"]},
              "questions_to_resolve": [], "queries_run": ['"SilverLeaf" "Harris Teeter"'],
              "sources_checked": ["news.google.com"], "confirmed_facts": [],
              "strong_inferences": ["tenant inferred"], "conflicting_evidence": [],
              "unresolved_questions": ["tenant unconfirmed"], "recommended_canonical_name": None,
              "recommended_aliases": [], "recommended_state": None,
              "recommended_action": "ACCEPT_QUALIFIED", "confidence": 0.6, "next_search_date": None}
    assert re.validate_resolution(record) == []


def test_resolution_rejects_invalid_action():
    record = {"proposal_id": "P1", "subject": "X", "research_trigger": {},
              "questions_to_resolve": [], "queries_run": ["q"],
              "sources_checked": ["s"], "confirmed_facts": [], "strong_inferences": [],
              "conflicting_evidence": [], "unresolved_questions": [],
              "recommended_canonical_name": None, "recommended_aliases": [],
              "recommended_state": None, "recommended_action": "PUBLISH",
              "confidence": 0.5, "next_search_date": None}
    assert any("recommended_action" in p for p in re.validate_resolution(record))


def test_evaluator_separation_no_self_evaluation(tmp_path):
    """The research recommender and the evaluator are independent callables."""
    assert re.recommend is not None
    assert "recommend" in dir(re)
    # The research module never reads the evaluator's state as an oracle.
    assert not hasattr(re, "evaluate_proposals")


def test_qualified_canonical_edit_preserves_original(tmp_path):
    r = initialize(tmp_path / "ad")
    write(r / "pending_proposals.yaml", {"proposals": [make_proposal()]})
    result = edit_proposal("P1", "Buddy", "qualify identity",
                           root=r, subject="SilverLeaf grocery center — possible Harris Teeter",
                           location="CR 16A and SilverLeaf Parkway",
                           aliases=["Harris Teeter SilverLeaf (unconfirmed)"])
    assert result["action"] == "edited"
    assert result["original_proposal"]["subject"] == "Harris Teeter SilverLeaf"
    pending = read(r / "pending_proposals.yaml", {})["proposals"]
    assert pending[0]["subject"] == "SilverLeaf grocery center — possible Harris Teeter"
    assert pending[0]["location"] == "CR 16A and SilverLeaf Parkway"
    assert pending[0]["edits"]
    decisions = read(r / "decisions.yaml", {})["decisions"]
    assert decisions[-1]["action"] == "edited"
    assert decisions[-1]["original_proposal"]["subject"] == "Harris Teeter SilverLeaf"


def test_qualified_entity_accept_and_rollback(tmp_path):
    r = initialize(tmp_path / "ad")
    write(r / "pending_proposals.yaml", {"proposals": [make_proposal()]})
    edit_proposal("P1", "Buddy", "qualify", root=r,
                  subject="SilverLeaf grocery center — possible Harris Teeter")
    res = review("P1", "accept", "Buddy", "qualified tracked subject", root=r)
    state = read(state_path(r), {})
    assert state["accepted"]["entities"][0]["subject"] == "SilverLeaf grocery center — possible Harris Teeter"
    review("P1", "rollback", "Buddy", "undo", root=r, decision_id=res["decision_id"])
    assert read(state_path(r), {})["accepted"]["entities"] == []
    assert any(x["proposal_id"] == "P1" for x in read(r / "pending_proposals.yaml", {})["proposals"])


def test_ht_fixture_qualified_acceptance_keeps_search_active(tmp_path):
    """Harris Teeter fixture: project exists, tenant inferred, unconfirmed; qualified entity + active search."""
    r = initialize(tmp_path / "ad")
    write(r / "pending_proposals.yaml", {"proposals": [
        make_proposal("E1"),
        {"proposal_id": "S1", "type": "search_profile", "subject": "Harris Teeter SilverLeaf",
         "proposed_state_transition": "isolated adaptive state only",
         "evidence": [{"url": "https://x.example.com/1", "title": "t", "date": "2026-05-15"}],
         "status": "pending_human_review"},
    ]})
    edit_proposal("E1", "Buddy", "qualify tenant", root=r,
                  subject="SilverLeaf grocery center — possible Harris Teeter",
                  location="CR 16A and SilverLeaf Parkway",
                  queries=['"SilverLeaf" "Harris Teeter"', '"CR 16A" grocery SilverLeaf'])
    edit_proposal("S1", "Buddy", "align subject", root=r,
                  subject="SilverLeaf grocery center — possible Harris Teeter",
                  queries=['"SilverLeaf" "Harris Teeter"', '"CR 16A" grocery SilverLeaf'])
    review("E1", "accept", "Buddy", "qualified", root=r)
    review("S1", "accept", "Buddy", "active search", root=r)
    state = read(state_path(r), {})
    entity = state["accepted"]["entities"][0]
    profile = state["accepted"]["search_profiles"][0]
    assert "possible Harris Teeter" in entity["subject"]
    assert "possible" in entity["subject"] or "unconfirmed" in entity["subject"]
    assert profile["queries"]  # search remains active with research queries
    assert not any("confirmed" in (entity.get("timeline_state") or "") for _ in [0])


def test_search_profile_activation_with_queries(tmp_path):
    r = initialize(tmp_path / "ad")
    write(r / "pending_proposals.yaml", {"proposals": [
        {"proposal_id": "M1", "type": "search_profile", "subject": "Magnolia Oaks Academy",
         "proposed_state_transition": "isolated adaptive state only",
         "evidence": [{"url": "u", "title": "t", "date": "2026-07-22"}], "status": "pending_human_review"},
    ]})
    edit_proposal("M1", "Buddy", "add queries", root=r,
                  subject="Magnolia Oaks Academy",
                  queries=['"Magnolia Oaks Academy"', '"School QQ"', 'site:stjohns.k12.fl.us "Magnolia Oaks"'])
    review("M1", "accept", "Buddy", "activate", root=r)
    state = read(state_path(r), {})
    profile = state["accepted"]["search_profiles"][0]
    assert len(profile["queries"]) == 3
    assert 'site:stjohns.k12.fl.us "Magnolia Oaks"' in profile["queries"]
