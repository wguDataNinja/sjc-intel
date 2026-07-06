import os
import sys

script_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from extract_bcc_agenda import parse_agenda_items, classify_action_type, classify_resident_impact


class TestParseAgendaItems:
    def test_jan20_regular_items_count(self, bcc_agenda_text_jan20):
        items = parse_agenda_items(bcc_agenda_text_jan20, "1/20/2026")
        assert len(items) > 0

    def test_jan20_contains_comp_plan(self, bcc_agenda_text_jan20):
        items = parse_agenda_items(bcc_agenda_text_jan20, "1/20/2026")
        titles = [item["title"].lower() for item in items]
        has_comp_plan = any("comprehensive plan" in t or "2050" in t for t in titles)
        assert has_comp_plan

    def test_may19_regular_items_count(self, bcc_agenda_text_may19):
        items = parse_agenda_items(bcc_agenda_text_may19, "5/19/2026")
        assert len(items) > 0

    def test_may19_contains_public_hearing(self, bcc_agenda_text_may19):
        items = parse_agenda_items(bcc_agenda_text_may19, "5/19/2026")
        has_public_hearing = any(
            "public hearing" in item["text"].lower() for item in items
        )
        assert has_public_hearing


class TestClassifyActionType:
    def test_public_hearing(self):
        assert classify_action_type("Public Hearing * REZ 2025-01") == "public_hearing"

    def test_ordinance(self):
        assert classify_action_type("Ordinance 2026-01") == "ordinance"

    def test_resolution(self):
        assert classify_action_type("Resolution 2026-01") == "resolution"

    def test_contract(self):
        assert classify_action_type("Contract award") == "contract"

    def test_budget(self):
        assert classify_action_type("Budget amendment") == "budget"

    def test_land_use(self):
        assert classify_action_type("Rezoning request") == "land_use"

    def test_procurement(self):
        result = classify_action_type("Bid award")
        assert result in ("procurement", "contract")

    def test_consent(self):
        assert classify_action_type("Consent agenda") == "consent"
