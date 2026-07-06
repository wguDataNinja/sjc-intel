import os
import sys

script_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from extract_nbor import parse_rows, normalize_records, classify_category


class TestParseRows:
    def test_parse_nbor_html(self, nbor_html):
        records = parse_rows(nbor_html)
        assert isinstance(records, list)

    def test_parsed_records_have_expected_fields(self, nbor_html):
        records = parse_rows(nbor_html)
        if records:
            rec = records[0]
            assert "title" in rec
            assert "description" in rec
            assert "category" in rec
            assert "date" in rec

    def test_normalized_items(self, nbor_html):
        records = parse_rows(nbor_html)
        items = normalize_records(records)
        assert isinstance(items, list)
        for item in items:
            assert "item_id" in item
            assert "title" in item
            assert "summary" in item
            assert "source_id" in item


class TestClassifyCategory:
    def test_rezoning(self):
        assert classify_category("REZ 2026000011 Test", "", "") == "rezoning_comp_plan_dri"

    def test_comp_plan(self):
        assert classify_category("CPA 2025-01 Test", "", "") == "rezoning_comp_plan_dri"

    def test_variance(self):
        assert classify_category("ZVAR 2025-01 Test", "", "") == "rezoning_comp_plan_dri"

    def test_general_construction(self):
        assert classify_category("Temp Power Installation", "bulkhead replacement", "") == "site_plans_permits_construction"
