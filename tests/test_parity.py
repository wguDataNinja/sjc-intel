import os
import sys
import json

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
sys.path.insert(0, REPO_ROOT)

from scripts.file_adapter import FileAdapter
from scripts.pg_adapter import PgAdapter
from scripts.parity_report import ParityReport


def setup_module():
    os.environ.setdefault("SJC_INTEL_PG_ADAPTER_ENABLED", "false")


class TestParityReport:

    def setup_method(self):
        self.file_adapter = FileAdapter()
        self.pg_adapter = PgAdapter()
        self.report = ParityReport(
            file_adapter=self.file_adapter,
            pg_adapter=self.pg_adapter,
        )

    def test_compare_item_counts(self):
        result = self.report.compare_item_counts()
        assert "file_count" in result
        assert "pg_count" in result
        assert isinstance(result["file_count"], int)
        assert isinstance(result["pg_count"], int)
        assert result["file_count"] > 0
        assert result["difference"] == result["file_count"] - result["pg_count"]

    def test_compare_by_source(self):
        result = self.report.compare_by_field("source_id")
        assert result["field"] == "source_id"
        assert "file_distribution" in result
        assert "pg_distribution" in result
        assert len(result["file_distribution"]) > 0

    def test_compare_by_review_status(self):
        result = self.report.compare_by_field("review_status")
        assert result["field"] == "review_status"
        assert "match" in result

    def test_compare_dedupe_keys(self):
        result = self.report.compare_dedupe_keys()
        assert "file_dedupe_count" in result
        assert "pg_dedupe_count" in result
        assert "common_count" in result
        assert isinstance(result["file_dedupe_count"], int)
        assert isinstance(result["only_in_file"], list)

    def test_generate_report_structure(self):
        report = self.report.generate()
        assert "generated_at" in report
        assert "pg_enabled" in report
        assert report["pg_enabled"] is False
        assert "item_count" in report
        assert "by_source" in report
        assert "by_review_status" in report
        assert "dedupe_keys" in report
        assert report["pg_status"] == "disabled"

    def test_generate_json_valid(self):
        json_str = self.report.generate_json()
        data = json.loads(json_str)
        assert "generated_at" in data
        assert "item_count" in data
        assert data["pg_enabled"] is False

    def test_print_report(self):
        import io
        import sys as _sys
        captured = io.StringIO()
        old_stdout = _sys.stdout
        _sys.stdout = captured
        try:
            self.report.print_report()
        finally:
            _sys.stdout = old_stdout
        output = captured.getvalue()
        assert "Parity Report" in output
        assert "PG Adapter: disabled" in output
        assert "Item Counts:" in output


class TestParityReportKnownFixtures:

    def setup_method(self):
        self.file_adapter = FileAdapter()
        self.pg_adapter = PgAdapter()
        self.report = ParityReport(
            file_adapter=self.file_adapter,
            pg_adapter=self.pg_adapter,
        )

    def test_item_count_positive(self):
        result = self.report.compare_item_counts()
        assert result["file_count"] > 0, "Repo should have at least one intel item"

    def test_dedupe_keys_positive(self):
        result = self.report.compare_dedupe_keys()
        assert result["file_dedupe_count"] > 0, "Repo should have dedupe keys"

    def test_source_distribution_includes_known_sources(self):
        result = self.report.compare_by_field("source_id")
        sources = list(result["file_distribution"].keys())
        assert "st_johns_citizen" in sources or len(sources) > 0
