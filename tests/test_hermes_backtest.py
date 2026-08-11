"""Tests for the Task 30 Hermes-operated historical backtest infrastructure.

Covers: feed bucketing/dedupe, seed-state visibility, weekly packet assembly,
output validation + simulated acceptance, hidden evaluation (subject discovery
and alias learning), and production-state isolation.
"""
import os
import sys
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from scripts import hermes_backtest as hb  # noqa: E402
from scripts import publication_common as pc  # noqa: E402
import publication_common as bare_pc  # noqa: E402  (same file, top-level import as hermes_backtest uses)


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _seed(tmp_path):
    root = tmp_path / "test-bt"
    (root / "weeks").mkdir(parents=True)
    _write(str(root / "seed.yaml"), {
        "available_on": "2025-05-05",
        "sources": [{"source_id": "sjc_county_news", "name": "County", "kind": "official"}],
        "entities": [{"id": "seed-c", "label": "St. Johns County", "aliases": []}],
        "search_profiles": [], "lanes": [], "milestones": [], "timelines": [],
    })
    _write(str(root / "config.yaml"), {
        "backtest_id": "test-bt", "start": "2025-05-05", "end": "2025-08-31",
        "simulated_acceptance": {"reviewer": "sim-eval", "allow_sensitivity": ["low"],
                                 "max_accepted_per_week": 12},
        "hidden_evaluator": {"subjects": [{"subject": "School QQ", "priority": "high"},
                                          {"subject": "Future Subject", "priority": "high"}],
                             "lanes": []},
        "budgets": {"max_model_calls_per_week": 5,
                    "max_search_profiles_executed_per_week": 3,
                    "max_research_escalations_per_week": 1,
                    "max_research_queries_per_escalation": 3},
    })
    _write(str(root / "feed" / "overrides.yaml"), [])
    return root


def _corpus(tmp_path, rows):
    """Write dated corpus records so iter_corpus_records sees them."""
    # Patch the intel-items dirs publication_common uses.
    intel = tmp_path / "data" / "intel_items" / "2025-05-05"
    _write(str(intel / "x.yaml"), {"items": rows})
    hb_old_intel = pc.INTEL_ITEMS_DIR
    hb_old_monthly = pc.MONTHLY_DIR
    pc.INTEL_ITEMS_DIR = str(tmp_path / "data" / "intel_items")
    pc.MONTHLY_DIR = str(tmp_path / "data" / "monthly")
    return hb_old_intel, hb_old_monthly


def test_feed_buckets_and_dedupes(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"),
           {"items": []})
    rows = [
        {"item_id": "SJC-BF-202508-0013", "title": "CR 2209", "summary": "x",
         "source_id": "sjc_county_news", "source_published_at": "2025-08-20"},
        {"item_id": "SJC-BF-202508-0013", "title": "dup copy", "summary": "x",
         "source_id": "sjc_county_news", "source_published_at": "2025-08-20"},
        {"item_id": "SJC-BF-202508-0010", "title": "CR 210", "summary": "x",
         "source_id": "sjc_county_news", "source_published_at": "2025-08-09"},
    ]
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"), {"items": rows})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    hb.build_feed("test-bt")
    wk = yaml.safe_load(open(str(root / "feed" / "weeks" / "2025-08-18.yaml")))
    ids = [e["item_id"] for e in wk["entries"]]
    assert "SJC-BF-202508-0013" in ids  # in its publication week
    assert ids.count("SJC-BF-202508-0013") == 1  # deduped
    wk2 = yaml.safe_load(open(str(root / "feed" / "weeks" / "2025-08-04.yaml")))
    assert [e["item_id"] for e in wk2["entries"]] == ["SJC-BF-202508-0010"]


def test_visible_state_carries_accepted_transitions_and_blocks_future(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    # A transition accepted on week 1, available next week.
    w1 = root / "weeks" / "2025-05-05"
    w1.mkdir(parents=True)
    _write(str(w1 / "accepted_state.yaml"), {
        "week_start": "2025-05-05", "available_on": "2025-05-12",
        "accepted": [{"proposal_id": "A1", "type": "entity", "subject": "School QQ",
                      "available_on": "2025-05-12", "evidence": []}],
        "rejected": [], "accepted_ids": ["A1"], "rejected_ids": []})
    # Week 1 state must NOT contain the accepted entity (not yet available).
    s1 = hb.visible_state("test-bt", hb.day("2025-05-05"))
    assert "School QQ" not in {e["label"] for e in s1["entities"]}
    # Week 2 state must contain it (available).
    s2 = hb.visible_state("test-bt", hb.day("2025-05-12"))
    assert "School QQ" in {e["label"] for e in s2["entities"]}


def test_assemble_week_packet(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"), {"items": []})
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"),
           {"items": [{"item_id": "SJC-BF-202508-0013", "title": "CR 2209", "summary": "x",
                       "source_id": "sjc_county_news", "source_published_at": "2025-08-20"}]})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    hb.build_feed("test-bt")
    w = hb.assemble_week("test-bt", "2025-08-18")
    assert (w / "hermes_task.md").exists()
    task = (w / "hermes_task.md").read_text()
    assert "2025-08-18" in task and "2025-08-24" in task
    assert "Sources you monitor" in task or "monitored sources" in task.lower()
    all_feed = yaml.safe_load(open(str(w / "feed" / "all.yaml")))
    assert [e["item_id"] for e in all_feed["entries"]] == ["SJC-BF-202508-0013"]


def test_ingest_validates_and_applies_simulated_acceptance(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"), {"items": []})
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"),
           {"items": [{"item_id": "SJC-BF-202508-0013", "title": "CR 2209", "summary": "x",
                       "source_id": "sjc_county_news", "source_published_at": "2025-08-20"}]})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    hb.build_feed("test-bt")
    w = hb.assemble_week("test-bt", "2025-08-18")
    _write(str(w / "findings.yaml"), [
        {"finding_id": "F1", "subject": "CR 2209 connector", "title": "CR 2209",
         "summary": "county begins construction", "source": "sjc_county_news",
         "source_date": "2025-08-20", "feed_id": "SJC-BF-202508-0013",
         "lane": "roads and mobility", "resident_importance": "high",
         "evidence": [{"feed_id": "SJC-BF-202508-0013", "source_date": "2025-08-20"}]}])
    _write(str(w / "proposals.yaml"), [
        {"proposal_id": "P1", "type": "entity", "subject": "CR 2209 connector",
         "simulated_week": "2025-08-18",
         "evidence": [{"feed_id": "SJC-BF-202508-0013", "source_date": "2025-08-20"}],
         "resident_impact": "commute", "expected_duration": "multi-year",
         "proposed_searches": ['"CR 2209"'], "proposed_sources": [],
         "cost": 1, "confidence": "high", "rationale": "commute corridor",
         "review_status": "proposed"},
        {"proposal_id": "P2", "type": "entity", "subject": "sensitive shooting subject",
         "simulated_week": "2025-08-18",
         "evidence": [{"feed_id": "SJC-BF-202508-0013", "source_date": "2025-08-20"}],
         "resident_impact": "x", "expected_duration": "x", "proposed_searches": [],
         "proposed_sources": [], "cost": 1, "confidence": "low",
         "rationale": "shooting incident coverage", "review_status": "proposed"}])
    _write(str(w / "coverage_editor.yaml"), [])
    _write(str(w / "weekly_report.md"), "# report")
    _write(str(w / "research.yaml"), [])
    res = hb.ingest_week("test-bt", "2025-08-18")
    assert res["accepted"] == 1
    assert res["rejected"] == 1  # sensitive subject rejected
    acc = yaml.safe_load(open(str(w / "accepted_state.yaml")))
    assert acc["accepted"][0]["subject"] == "CR 2209 connector"
    # Next week state carries the accepted entity.
    nxt = hb.visible_state("test-bt", hb.day("2025-08-25"))
    assert "CR 2209 connector" in {e["label"] for e in nxt["entities"]}


def test_evaluate_all_hidden_and_alias_learned(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    w1 = root / "weeks" / "2025-05-05"
    w1.mkdir(parents=True)
    _write(str(w1 / "meta.yaml"), {"status": "completed", "week_start": "2025-05-05",
                                   "week_end": "2025-05-11"})
    _write(str(w1 / "findings.yaml"), [{"subject": "School QQ"}])
    _write(str(w1 / "accepted_state.yaml"), {
        "week_start": "2025-05-05", "available_on": "2025-05-12",
        "accepted": [{"proposal_id": "A1", "type": "alias",
                      "subject": "Magnolia Oaks Academy", "target": "School QQ",
                      "available_on": "2025-05-12"},
                     {"proposal_id": "A2", "type": "search_profile",
                      "subject": "School QQ", "available_on": "2025-05-12"}],
        "rejected": [], "accepted_ids": ["A1", "A2"], "rejected_ids": []})
    _write(str(w1 / "coverage_editor.yaml"), [])
    _write(str(w1 / "feed" / "all.yaml"), {"week_start": "2025-05-05", "entries": []})
    ev = hb.evaluate_all("test-bt", "2025-05-12")
    assert "School QQ" in ev["subjects_found"]
    assert ev["aliases_learned"] == [{"value": "Magnolia Oaks Academy",
                                      "target": "School QQ", "week": "2025-05-05"}]
    # Hidden subject 'Future Subject' was never shown to Hermes and is missed.
    assert "Future Subject" in ev["subjects_missed"]


def test_backtest_writes_only_isolated_root(tmp_path, monkeypatch):
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    # Set up the corpus before the before-snapshot so only backtest output is new.
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"), {"items": []})
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"),
           {"items": [{"item_id": "SJC-BF-202508-0013", "title": "CR 2209", "summary": "x",
                       "source_id": "sjc_county_news", "source_published_at": "2025-08-20"}]})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    before = set()
    for dirpath, dirnames, filenames in os.walk(str(tmp_path)):
        for fn in filenames:
            before.add(os.path.join(dirpath, fn))
    # Simulate an assemble+ingest cycle.
    hb.build_feed("test-bt")
    w = hb.assemble_week("test-bt", "2025-08-18")
    _write(str(w / "findings.yaml"), [])
    _write(str(w / "proposals.yaml"), [])
    _write(str(w / "coverage_editor.yaml"), [])
    _write(str(w / "weekly_report.md"), "# r")
    _write(str(w / "research.yaml"), [])
    hb.ingest_week("test-bt", "2025-08-18")
    after = set()
    for dirpath, dirnames, filenames in os.walk(str(tmp_path)):
        for fn in filenames:
            after.add(os.path.join(dirpath, fn))
    # The only new files must live under the isolated backtest root, never in
    # production data/intel_items, data/adaptive_discovery, registry, etc.
    produced = after - before
    assert produced, "expected backtest output"
    for p in produced:
        assert str(root) in p, f"backtest wrote to production path: {p}"


# --------------------------------------------------------------------------- #
# Task 33 — generalized defect regressions (acceptance asymmetry, entity
# dedupe, evaluator matcher).
# --------------------------------------------------------------------------- #

def test_acceptance_allows_search_profile_for_tracked_entity(tmp_path, monkeypatch):
    """Defect #1: an entity-first subject may later gain a search profile."""
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    # Week 1 accepts an entity.
    w1 = root / "weeks" / "2025-05-05"
    w1.mkdir(parents=True)
    _write(str(w1 / "accepted_state.yaml"), {
        "week_start": "2025-05-05", "available_on": "2025-05-12",
        "accepted": [{"proposal_id": "A1", "type": "entity", "subject": "SR 16 / IGP improvements",
                      "available_on": "2025-05-12", "evidence": []}],
        "rejected": [], "accepted_ids": ["A1"], "rejected_ids": []})
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"), {"items": []})
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"),
           {"items": [{"item_id": "SJC-BF-202508-0013", "title": "SR 16", "summary": "x",
                       "source_id": "sjc_county_news", "source_published_at": "2025-08-20"}]})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    hb.build_feed("test-bt")
    w = hb.assemble_week("test-bt", "2025-08-18")
    _write(str(w / "findings.yaml"), [])
    _write(str(w / "proposals.yaml"), [
        {"proposal_id": "P1", "type": "search_profile", "subject": "SR 16 / IGP improvements",
         "simulated_week": "2025-08-18",
         "evidence": [{"feed_id": "SJC-BF-202508-0013", "source_date": "2025-08-20"}],
         "resident_impact": "commute", "proposed_searches": ['"SR 16" IGP'],
         "cost": 1, "confidence": "high", "rationale": "profile for tracked entity",
         "review_status": "proposed"}])
    _write(str(w / "coverage_editor.yaml"), [])
    _write(str(w / "weekly_report.md"), "# r")
    _write(str(w / "research.yaml"), [])
    res = hb.ingest_week("test-bt", "2025-08-18")
    assert res["accepted"] == 1, res
    assert res["rejected"] == 0


def test_acceptance_rejects_duplicate_entity(tmp_path, monkeypatch):
    """Defect #1: a duplicate entity for an already-tracked subject is rejected."""
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    w1 = root / "weeks" / "2025-05-05"
    w1.mkdir(parents=True)
    _write(str(w1 / "accepted_state.yaml"), {
        "week_start": "2025-05-05", "available_on": "2025-05-12",
        "accepted": [{"proposal_id": "A1", "type": "entity", "subject": "CR 2209 connector",
                      "available_on": "2025-05-12", "evidence": []}],
        "rejected": [], "accepted_ids": ["A1"], "rejected_ids": []})
    _write(str(tmp_path / "data" / "monthly" / "2025-08" / "discovered_items.yaml"), {"items": []})
    _write(str(tmp_path / "data" / "intel_items" / "2025-05-05" / "x.yaml"),
           {"items": [{"item_id": "SJC-BF-202508-0013", "title": "CR 2209", "summary": "x",
                       "source_id": "sjc_county_news", "source_published_at": "2025-08-20"}]})
    monkeypatch.setattr(bare_pc, "INTEL_ITEMS_DIR", str(tmp_path / "data" / "intel_items"))
    monkeypatch.setattr(bare_pc, "MONTHLY_DIR", str(tmp_path / "data" / "monthly"))
    hb.build_feed("test-bt")
    w = hb.assemble_week("test-bt", "2025-08-18")
    _write(str(w / "findings.yaml"), [])
    _write(str(w / "proposals.yaml"), [
        {"proposal_id": "P1", "type": "entity", "subject": "CR 2209 connector",
         "simulated_week": "2025-08-18",
         "evidence": [{"feed_id": "SJC-BF-202508-0013", "source_date": "2025-08-20"}],
         "resident_impact": "commute", "proposed_searches": [], "proposed_sources": [],
         "cost": 1, "confidence": "high", "rationale": "duplicate entity",
         "review_status": "proposed"}])
    _write(str(w / "coverage_editor.yaml"), [])
    _write(str(w / "weekly_report.md"), "# r")
    _write(str(w / "research.yaml"), [])
    res = hb.ingest_week("test-bt", "2025-08-18")
    assert res["accepted"] == 0
    assert res["rejected"] == 1


def test_apply_proposal_dedupes_entity_by_label(tmp_path, monkeypatch):
    """Defect #3: apply_proposal is idempotent by normalized label."""
    root = _seed(tmp_path)
    monkeypatch.setattr(hb, "HERMES_BACKTESTS", root.parent)
    state = hb.visible_state("test-bt", hb.day("2025-05-05"))
    hb.apply_proposal(state, {"type": "entity", "subject": "Budget / taxes",
                              "proposal_id": "E1", "available_on": "2025-05-12", "evidence": []})
    hb.apply_proposal(state, {"type": "entity", "subject": "  budget   / Taxes ",
                              "proposal_id": "E2", "available_on": "2025-05-12", "evidence": []})
    labels = [e["label"] for e in state["entities"]]
    assert labels.count("Budget / taxes") == 1, labels


def test_evaluator_matches_zoning_and_avoids_bare_water_false_positive():
    """Defect #2: medium subjects stay matchable; generic 'water' is not a hit."""
    assert "school zoning" in hb._alias_terms("school zoning / attendance boundaries")
    assert hb._subject_keywords("school zoning / attendance boundaries")  # non-empty
    # A bare boil-water item must NOT satisfy the Phase III shortage subject:
    # the bare token "water" is not a majority of its distinctive tokens.
    hay = "boil water notice issued"
    kws = hb._subject_keywords("Phase III water shortage / irrigation restrictions")
    assert not hb._token_hit(kws, hay)
    # A real shortage finding matches via its distinctive tokens.
    assert hb._token_hit(kws, "phase iii extreme water shortage declared irrigation")
    # A tracked zoning subject matches when a majority of its tokens appear
    # (the profile "SilverLeaf area school attendance zoning" carries both
    # "zoning" and "attendance", even though "boundaries" is absent).
    zkws = hb._subject_keywords("school zoning / attendance boundaries")
    assert hb._token_hit(zkws, "silverleaf area school attendance zoning")
    # The alias matcher recognizes the precise shortage subject.
    assert "phase iii" in hb._alias_terms("Phase III water shortage / irrigation restrictions")
