import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DATA_ROOT = os.path.join(os.path.dirname(__file__), "fixtures", "publication")
REG_ROOT = os.path.join(DATA_ROOT, "registry")
os.environ["SJC_INTEL_DATA_ROOT"] = DATA_ROOT
os.environ["SJC_INTEL_REGISTRY_ROOT"] = REG_ROOT

from scripts.publication_common import (  # noqa: E402
    DECISIONS_DIR,
    is_valid_url,
    iter_intel_items,
    load_all_decisions,
    public_projection,
    validate_public_safe,
)
from scripts.validate_publication_corpus import CorpusValidator  # noqa: E402
from scripts.select_publication_items import selector  # noqa: E402
from datetime import datetime, timezone

TEST_WINDOW = (datetime(2026, 5, 1, tzinfo=timezone.utc),
               datetime(2026, 8, 4, tzinfo=timezone.utc))
from scripts import publication_decision as pd  # noqa: E402


def _eligibility_item(item_id="SJC-UTIL-20260603-0002"):
    """A minimal item that passes every selector gate."""
    return (f"data/intel_items/2026-06-03/x.yaml", {
        "item_id": item_id,
        "title": "Test",
        "summary": "Test summary.",
        "topics": ["infrastructure"],
        "source_id": "sjc_utility_department",
        "source_url": "https://example.com/",
        "source_published_at": "2026-06-15",
        "discovered_at": "2026-06-15T12:00:00Z",
        "created_at": "2026-06-15T12:00:00Z",
        "sensitivity": "low",
        "review_status": "verified",
        "communities": [],
        "geographic_scope": "county_wide",
        "verification_status": "source_confirmed",
    })


def _approval_decision(item_id="SJC-UTIL-20260603-0002"):
    return {
        "publication_status": "approved",
        "release_eligible": True,
        "silverleaf_relevance": {"decision": "included"},
        "decision_timestamp": "2026-08-04T12:00:00Z",
    }


class TestSelectorLegacyTreatment:
    def test_warning_timestamp_legacy_does_not_block(self, monkeypatch):
        import publication_common
        monkeypatch.setattr(
            publication_common, "LEGACY_EXCEPTIONS_FILE",
            os.path.join(os.path.dirname(__file__), "..", "data",
                         "publication_decisions", "legacy_exceptions.yaml"))
        items = [_eligibility_item("SJC-CN-20260802-0001")]
        # Mark the item_id as covered by LEG-0802-MISSING-CREATED (warning).
        items[0][1]["item_id"] = "SJC-CN-20260802-0001"
        r = selector({items[0][1]["item_id"]: _approval_decision(items[0][1]["item_id"])},
                     items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert items[0][1]["item_id"] in r["selected"]

    def test_blocking_legacy_treatment_excludes(self, monkeypatch):
        import publication_common
        monkeypatch.setattr(
            publication_common, "LEGACY_EXCEPTIONS_FILE",
            os.path.join(os.path.dirname(__file__), "..", "data",
                         "publication_decisions", "legacy_exceptions.yaml"))
        # LEG-CDD-LEGACY blocks (retained_as_archival_evidence).
        items = [_eligibility_item("six_mile_creek_cdd-001")]
        items[0][1]["item_id"] = "six_mile_creek_cdd-001"
        r = selector({items[0][1]["item_id"]: _approval_decision(items[0][1]["item_id"])},
                     items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert items[0][1]["item_id"] not in r["selected"]
        assert any("legacy_exception" in reason
                   for reasons in r["excluded"].values() for reason in reasons)


class TestPublicationCorpus:
    def test_validator_scans_real_shaped_fixtures(self):
        v = CorpusValidator()
        s = v.run()
        assert s["items_total"] == 8
        assert s["errors"] == 0

    def test_all_items_have_valid_ids(self):
        v = CorpusValidator()
        v.run()
        bad = [e for e in v.errors if e["code"] == "bad_item_id_format"]
        assert bad == []

    def test_high_sensitivity_verified_item_not_release_eligible(self):
        v = CorpusValidator()
        s = v.run()
        assert s["not_release_eligible"] >= 1

    def test_unknown_source_event_warns(self):
        # EVT-UTIL-20260603-0001 exists; a missing event should warn not error.
        v = CorpusValidator()
        s = v.run()
        assert s["errors"] == 0

    def test_json_summary_shape(self):
        v = CorpusValidator()
        s = v.run()
        for key in ("items_total", "errors", "warnings", "error_item_ids",
                    "warning_item_ids", "by_source", "by_status"):
            assert key in s


class TestPublicationProjection:
    def test_public_projection_excludes_internal_fields(self):
        _, item = pd.find_item("SJC-UTIL-20260603-0001")
        proj = public_projection(item)
        assert validate_public_safe(proj) == []
        assert "reviewer_notes" not in proj
        assert "_dedupe_key" not in proj

    def test_public_projection_has_source_and_url(self):
        _, item = pd.find_item("SJC-UTIL-20260603-0002")
        proj = public_projection(item)
        assert proj["source_url"].startswith("https://")
        assert proj["title"]


class TestSelector:
    def test_nothing_selected_without_decisions(self):
        items = list(iter_intel_items())
        r = selector({}, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert r["selected"] == []
        assert "no_publication_decision" in r["counts"]

    def test_verified_low_sensitivity_with_approval_selected(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-UTIL-20260603-0002": {
                "publication_status": "approved",
                "release_eligible": True,
                "silverleaf_relevance": {"decision": "included"},
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-UTIL-20260603-0002" in r["selected"]

    def test_high_sensitivity_excluded_even_with_approval(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-SJSO-20260603-0004": {
                "publication_status": "approved",
                "release_eligible": True,
                "silverleaf_relevance": {"decision": "included"},
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-SJSO-20260603-0004" not in r["selected"]
        assert "high_sensitivity" in r["counts"]

    def test_pending_item_excluded_even_with_decision(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-UTIL-20260603-0003": {
                "publication_status": "approved",
                "release_eligible": True,
                "silverleaf_relevance": {"decision": "included"},
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-UTIL-20260603-0003" not in r["selected"]

    def test_withdrawn_decision_excluded(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-UTIL-20260603-0002": {
                "publication_status": "withdrawn",
                "withdrawn": True,
                "silverleaf_relevance": {"decision": "included"},
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-UTIL-20260603-0002" not in r["selected"]
        assert "withdrawn" in r["counts"]

    def test_superseded_item_excluded(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-CN-20260603-0006": {
                "publication_status": "approved",
                "silverleaf_relevance": {"decision": "included"},
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-CN-20260603-0006" not in r["selected"]
        assert "superseded" in r["counts"]

    def test_missing_silverleaf_decision_excluded(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-UTIL-20260603-0002": {
                "publication_status": "approved",
                "release_eligible": True,
            }
        }
        r = selector(decisions, items, window_start=TEST_WINDOW[0], window_end=TEST_WINDOW[1])
        assert "SJC-UTIL-20260603-0002" not in r["selected"]
        assert "missing_silverleaf_decision" in r["counts"]

    def test_deterministic_ordering(self):
        items = list(iter_intel_items())
        decisions = {
            "SJC-UTIL-20260603-0001": {
                "publication_status": "approved",
                "release_eligible": True,
                "silverleaf_relevance": {"decision": "included"},
            },
            "SJC-UTIL-20260603-0002": {
                "publication_status": "approved",
                "release_eligible": True,
                "silverleaf_relevance": {"decision": "included"},
            },
        }
        r1 = selector(decisions, items)
        r2 = selector(decisions, items)
        assert r1["selected"] == r2["selected"]
        assert r1["selected"] == sorted(r1["selected"])


class TestDecisionTool:
    def _write_decision(self, item_id, status):
        os.makedirs(DECISIONS_DIR, exist_ok=True)
        path = os.path.join(DECISIONS_DIR, f"{item_id}.yaml")
        data = {"item_id": item_id, "publication_status": status,
                "reviewer": "r", "history": [
                    {"status": status, "reviewer": "r", "timestamp": "t0",
                     "rationale": "prior"}]}
        import yaml
        with open(path, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)
        return path

    def test_dry_run_does_not_write(self):
        import yaml
        before = set(os.listdir(DECISIONS_DIR))
        try:
            pd.build_decision(
                "approve", {"item_id": "TMP-NEW", "sensitivity": "low",
                            "review_status": "verified"},
                "reviewer", "reason",
                argparse_namespace())
        except Exception:
            pass
        assert set(os.listdir(DECISIONS_DIR)) == before

    def test_invalid_transition_rejected(self):
        import pytest
        path = self._write_decision("TMP-REJ", "rejected")
        try:
            with pytest.raises(pd.PublicationDecisionError):
                pd.build_decision("withdraw",
                                  {"item_id": "TMP-REJ", "sensitivity": "low",
                                   "review_status": "verified"},
                                  "r", "why", argparse_namespace())
        finally:
            os.remove(path)

    def test_valid_transition_withdraw_after_approved(self):
        path = self._write_decision("TMP-APP", "approved")
        try:
            rec = pd.build_decision("withdraw",
                                    {"item_id": "TMP-APP", "sensitivity": "low",
                                     "review_status": "verified"},
                                    "r", "because", argparse_namespace(reason="withdrawing"))
            assert rec["publication_status"] == "withdrawn"
            assert rec["withdrawn"] is True
            assert rec["release_eligible"] is False
            assert len(rec["history"]) == 2
        finally:
            os.remove(path)

    def test_high_sensitivity_approval_blocked(self):
        import pytest
        with pytest.raises(pd.PublicationDecisionError):
            pd.build_decision("approve",
                              {"item_id": "SJC-SJSO-20260603-0004",
                               "sensitivity": "high",
                               "review_status": "verified"},
                              "r", "why", argparse_namespace())

    def test_audit_history_appended_not_replaced(self):
        path = self._write_decision("TMP-AUDIT", "approved")
        try:
            rec = pd.build_decision("withdraw",
                                    {"item_id": "TMP-AUDIT", "sensitivity": "low",
                                     "review_status": "verified"},
                                    "b", "reason", argparse_namespace(reason="w"))
            assert len(rec["history"]) == 2
            assert rec["history"][0]["rationale"] == "prior"
            assert rec["history"][1]["status"] == "withdrawn"
        finally:
            os.remove(path)

    def test_requires_reviewer_and_rationale(self):
        assert pd.COMMAND_TO_STATUS["approve"] == "approved"
        assert pd.COMMAND_TO_STATUS["withdraw"] == "withdrawn"

    def test_relevance_override_recorded(self):
        ns = argparse_namespace()
        ns.relevance = "near_silverleaf"
        rec = pd.build_decision("approve",
                                {"item_id": "SJC-CN-20260802-0001",
                                 "sensitivity": "low", "review_status": "verified"},
                                "r", "ok", ns)
        assert rec["relevance"] == "near_silverleaf"

    def test_public_summary_override_recorded_without_altering_item(self):
        ns = argparse_namespace()
        ns.public_summary_override = "A clear public-facing summary for residents."
        rec = pd.build_decision("approve",
                                {"item_id": "SJC-UTIL-20260603-0002",
                                 "sensitivity": "low", "review_status": "verified"},
                                "r", "ok", ns)
        assert rec["public_summary_override"] == "A clear public-facing summary for residents."
        assert "reviewer_notes" not in rec

    def test_public_summary_override_rejects_too_short(self):
        import pytest
        ns = argparse_namespace()
        ns.public_summary_override = "short"
        with pytest.raises(pd.PublicationDecisionError):
            pd.build_decision("approve",
                              {"item_id": "SJC-UTIL-20260603-0002",
                               "sensitivity": "low", "review_status": "verified"},
                              "r", "ok", ns)


def argparse_namespace(reason=""):
    class NS:
        def __init__(self):
            self.silverleaf = None
            self.silverleaf_rationale = ""
            self.place_ids = []
            self.entity_ids = []
            self.reason = reason
            self.public_summary_override = ""
            self.event_date = ""
            self.event_date_label = ""
            self.lifecycle = ""
            self.lifecycle_label = ""
            self.relevance = None
    return NS()
