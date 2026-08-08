"""Tests for the Task 29 Model B publication activation.

Covers: backfill visibility + dedupe, corroborated local media, qualified
publication, editorial roles, stale-context handling, and the publication plan
generator. Uses monkeypatched module constants so it is independent of the
shared fixture environment used by other test modules.
"""
import os
import sys
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from scripts import publication_common as pc  # noqa: E402
from scripts import publication_policy as pol  # noqa: E402
from scripts.build_publication_plan import render, check_doc, REQUIRED_SECTIONS  # noqa: E402

# --------------------------------------------------------------------------- #
# Backfill visibility + dedupe
# --------------------------------------------------------------------------- #


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def test_backfill_items_reach_reader(tmp_path, monkeypatch):
    intel = tmp_path / "intel_items" / "2026-06-03"
    monthly = tmp_path / "monthly" / "2025-08"
    _write(str(intel / "county.yaml"), {"items": [
        {"item_id": "SJC-CN-20260603-0001", "title": "A",
         "source_id": "sjc_county_news"}]})
    _write(str(monthly / "discovered_items.yaml"), {"items": [
        {"item_id": "SJC-BF-202508-0001", "title": "B",
         "source_id": "sjc_county_news"}]})
    # Non-item monthly artifacts must not be treated as items.
    _write(str(monthly / "monthly_wrap.md"), "# wrap")
    _write(str(monthly / "topic_clusters.yaml"), {"clusters": []})

    monkeypatch.setattr(pc, "INTEL_ITEMS_DIR", str(tmp_path / "intel_items"))
    monkeypatch.setattr(pc, "MONTHLY_DIR", str(tmp_path / "monthly"))
    items = [it["item_id"] for _, it in pc.iter_intel_items()]
    assert "SJC-CN-20260603-0001" in items
    assert "SJC-BF-202508-0001" in items
    assert len(items) == 2  # wrap + clusters not counted


def test_backfill_dedupe_against_intel_items(tmp_path, monkeypatch):
    intel = tmp_path / "intel_items" / "2026-06-03"
    monthly = tmp_path / "monthly" / "2025-08"
    _write(str(intel / "county.yaml"), {"items": [
        {"item_id": "SJC-BF-202508-0001", "title": "canonical",
         "source_id": "sjc_county_news"}]})
    _write(str(monthly / "discovered_items.yaml"), {"items": [
        {"item_id": "SJC-BF-202508-0001", "title": "duplicate-copy",
         "source_id": "sjc_county_news"}]})
    monkeypatch.setattr(pc, "INTEL_ITEMS_DIR", str(tmp_path / "intel_items"))
    monkeypatch.setattr(pc, "MONTHLY_DIR", str(tmp_path / "monthly"))
    items = [(it["item_id"], it["title"]) for _, it in pc.iter_intel_items()]
    assert items == [("SJC-BF-202508-0001", "canonical")]  # intel_items wins


# --------------------------------------------------------------------------- #
# Corroborated local media
# --------------------------------------------------------------------------- #

SOURCES = {
    "sjc_county_news": {"source_type": "government_portal"},
    "st_johns_citizen": {"source_type": "local_media"},
    "baptist_health": {"source_type": "wordpress_blog"},
}


def _media_item(item_id="SJC-SL-20260704-0001", source="st_johns_citizen"):
    return {
        "item_id": item_id,
        "title": "Publix opened",
        "summary": "A 55,701 sq ft Publix opened in SilverLeaf.",
        "topics": ["development"],
        "source_id": source,
        "source_url": "https://sjcitizen.com/example",
        "source_published_at": "2026-03-26",
        "review_status": "verified",
        "verification_status": "source_confirmed",
        "sensitivity": "low",
        "urgency": "ongoing",
        "communities": ["silverleaf"],
        "primary_topic": "development",
        "resident_relevance": {"why_it_matters": "x" * 30,
                               "affected_audiences": ["residents"]},
    }


def test_local_media_without_corroboration_stays_blocked():
    cls, reasons = pol.classify_item(_media_item(), None, SOURCES,
                                     as_of=None)
    assert cls == pol.NEEDS_HUMAN_REVIEW
    assert any("source_type" in r for r in reasons)


def test_local_media_with_first_party_corroboration_publishes():
    decision = {"publication_status": "approved", "corroboration": [
        {"source": "Publix", "url": "https://corporate.publix.com/",
         "kind": "first_party"}]}
    cls, _ = pol.classify_item(_media_item(), decision, SOURCES, as_of=None)
    assert cls == pol.AUTO_PUBLISHABLE


def test_local_media_with_two_outlets_publishes():
    decision = {"publication_status": "approved", "corroboration": [
        {"source": "JDR", "url": "https://www.jaxdailyrecord.com/", "kind": "local_media"},
        {"source": "Business Journals", "url": "https://www.bizjournals.com/", "kind": "local_media"}]}
    cls, _ = pol.classify_item(_media_item(), decision, SOURCES, as_of=None)
    assert cls == pol.AUTO_PUBLISHABLE


def test_single_weak_outlet_does_not_publish():
    decision = {"publication_status": "approved", "corroboration": [
        {"source": "one outlet", "url": "https://example.com/", "kind": "local_media"}]}
    cls, reasons = pol.classify_item(_media_item(), decision, SOURCES, as_of=None)
    assert cls == pol.NEEDS_HUMAN_REVIEW
    assert any("source_type" in r for r in reasons)


# --------------------------------------------------------------------------- #
# Qualified publication
# --------------------------------------------------------------------------- #


def test_qualified_local_media_publishes_without_confirmation():
    decision = {"publication_status": "approved", "qualified": True,
                "qualified_label": "Tenant unconfirmed"}
    cls, _ = pol.classify_item(_media_item(), decision, SOURCES, as_of=None)
    assert cls == pol.AUTO_PUBLISHABLE


# --------------------------------------------------------------------------- #
# Stale-timely / durable context
# --------------------------------------------------------------------------- #

from datetime import datetime, timezone  # noqa: E402

AS_OF = datetime(2026, 8, 7, tzinfo=timezone.utc)


def _timely_item(item_id="SJC-BF-202508-0013"):
    return {
        "item_id": item_id,
        "title": "CR 2209 construction underway",
        "summary": "County building a new four-lane corridor.",
        "topics": ["transportation"],
        "source_id": "sjc_county_news",
        "source_url": "https://www.sjcfl.us/example",
        "source_published_at": "2025-08-20",
        "review_status": "verified",
        "verification_status": "source_confirmed",
        "sensitivity": "low",
        "urgency": "timely",
        "communities": ["silverleaf"],
        "primary_topic": "transportation",
        "resident_relevance": {"why_it_matters": "x" * 30,
                               "affected_audiences": ["residents"]},
    }


def test_stale_timely_without_context_role_blocked():
    cls, reasons = pol.classify_item(_timely_item(), None, SOURCES, as_of=AS_OF)
    assert cls == pol.NEEDS_HUMAN_REVIEW
    assert any("stale" in r for r in reasons)


def test_stale_timely_with_browse_role_allowed_as_context():
    decision = {"publication_status": "approved", "role": "browse"}
    cls, _ = pol.classify_item(_timely_item(), decision, SOURCES, as_of=AS_OF)
    assert cls == pol.AUTO_PUBLISHABLE


def test_stale_timely_with_timeline_role_allowed():
    decision = {"publication_status": "approved", "role": "timeline"}
    cls, _ = pol.classify_item(_timely_item(), decision, SOURCES, as_of=AS_OF)
    assert cls == pol.AUTO_PUBLISHABLE


# --------------------------------------------------------------------------- #
# Publication plan generator
# --------------------------------------------------------------------------- #


def _release(items):
    return {
        "release_id": "SJC-REL-2026-08-003",
        "items": items,
    }


def test_plan_renders_all_required_sections(tmp_path, monkeypatch):
    items = [
        {"public_item_id": "A", "title": "Latest item", "role": "latest",
         "display_topic": "roads_traffic", "source_name": "S", "source_date": "2026-08-01"},
        {"public_item_id": "B", "title": "Browse item", "role": "browse",
         "display_topic": "local_business", "source_name": "S2", "source_date": "2025-10-01",
         "qualified": True, "qualified_label": "Tenant unconfirmed"},
        {"public_item_id": "C", "title": "Timeline item", "role": "timeline",
         "display_topic": "schools_community", "source_name": "S3", "source_date": "2025-08-01",
         "related_item_ids": ["A"]},
    ]
    # Avoid reading the real editorial inputs / adaptive state.
    monkeypatch.setattr("scripts.build_publication_plan.PLAN_INPUTS",
                        str(tmp_path / "plan_inputs.yaml"))
    monkeypatch.setattr("scripts.build_publication_plan.ACCEPTED_STATE",
                        str(tmp_path / "accepted_state.yaml"))
    open(str(tmp_path / "plan_inputs.yaml"), "w").write("editorial_summary:\n  - 'test'\n")
    open(str(tmp_path / "accepted_state.yaml"), "w").write("accepted: {}\n")

    content = render(_release(items))
    for sec in REQUIRED_SECTIONS:
        assert f"## " in content
    assert "Latest item" in content
    assert "Browse item" in content
    assert "Tenant unconfirmed" in content
    assert check_doc(content) == []


def test_plan_check_rejects_missing_section():
    content = "# Current Publication Plan\n**Generated:** x\n"
    assert check_doc(content)


# --------------------------------------------------------------------------- #
# Release projection (role + qualified)
# --------------------------------------------------------------------------- #


def test_project_item_emits_role_and_qualified():
    from scripts.build_static_release import project_item
    item = {
        "item_id": "SJC-SL-20260704-0005",
        "title": "two supermarkets",
        "summary": "Two 61,000 sq ft supermarkets proposed.",
        "topics": ["development"],
        "source_id": "st_johns_citizen",
        "source_url": "https://sjcitizen.com/example",
        "source_published_at": "2025-12-02",
        "primary_topic": "development",
        "communities": ["silverleaf"],
        "resident_relevance": {"why_it_matters": "grocery competition"},
    }
    decision = {
        "role": "browse",
        "display_topic": "local_business",
        "qualified": True,
        "qualified_label": "Tenant unconfirmed",
        "relevance": "in_silverleaf",
    }
    rec = project_item(item, decision, "SJC-REL-2026-08-003")
    assert rec["role"] == "browse"
    assert rec["qualified"] is True
    assert rec["qualified_label"] == "Tenant unconfirmed"
    assert rec["display_topic"] == "local_business"
