"""Tests for the SilverLeaf Brief static release exporter (§3B-G2)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts import static_release_common as src  # noqa: E402
from scripts.build_static_release import build_demo_release, build_real_release  # noqa: E402
from scripts.static_release_common import (  # noqa: E402
    build_release_dict,
    build_search_index,
    order_items,
    validate_public_item,
    write_artifacts,
)

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
DEMO_FIXTURE = os.path.join(REPO_ROOT, "site", "fixtures", "demo", "release.yaml")


def _tmp(tmp_path, name):
    p = tmp_path / name
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def _demo_release(reviewer="Demo test"):
    release, rev, warnings = build_demo_release(
        DEMO_FIXTURE, "SJC-REL-DEMO-TEST", None, None, reviewer,
        src.GENERATOR_REVISION)
    return release, rev, warnings


class TestExportDeterminism:
    def test_byte_stable_across_runs(self, tmp_path):
        a = _tmp(tmp_path, "a")
        b = _tmp(tmp_path, "b")
        for out in (a, b):
            release, rev, _ = _demo_release()
            write_artifacts(out, release, build_search_index(
                release, release["dimensions"]), reviewer=rev)
        for name in ("release.json", "search-index.json", "release-manifest.json"):
            with open(os.path.join(a, name), "rb") as fa, \
                    open(os.path.join(b, name), "rb") as fb:
                assert fa.read() == fb.read(), name

    def test_deterministic_item_order(self):
        items = [
            {"public_item_id": "B", "source_date": "2026-05-01"},
            {"public_item_id": "A", "source_date": "2026-05-01"},
            {"public_item_id": "C", "source_date": "2026-06-01"},
            {"public_item_id": "D"},
        ]
        ordered = order_items(items)
        ids = [it["public_item_id"] for it in ordered]
        assert ids == ["C", "A", "B", "D"]  # date desc, id asc, undated last


class TestPublicProjection:
    def test_release_items_only_allowlisted_fields(self, tmp_path):
        release, _, _ = _demo_release()
        allowed = src.PUBLIC_ITEM_FIELDS
        for it in release["items"]:
            unknown = set(it.keys()) - allowed
            assert not unknown, f"{it['public_item_id']}: {unknown}"

    def test_no_internal_fields_in_items(self, tmp_path):
        release, _, _ = _demo_release()
        for it in release["items"]:
            for key in it:
                assert not key.startswith("_"), key
                assert key not in src.INTERNAL_DENYLIST, key

    def test_release_top_level_has_no_reviewer(self, tmp_path):
        release, _, _ = _demo_release()
        assert "reviewer" not in release
        assert "reviewer" not in src.RELEASE_TOP_FIELDS

    def test_release_identity_and_counts(self, tmp_path):
        release, _, _ = _demo_release()
        assert release["release_id"] == "SJC-REL-DEMO-TEST"
        assert release["environment"] == "demo"
        assert len(release["items"]) == 8
        assert release["schema_version"] == "1.0"

    def test_checksums_match_bytes(self, tmp_path):
        out = _tmp(tmp_path, "out")
        release, rev, _ = _demo_release()
        _, checksums, manifest = write_artifacts(
            out, release, build_search_index(release, release["dimensions"]),
            reviewer=rev)
        for name, want in checksums.items():
            with open(os.path.join(out, name), "rb") as f:
                assert src.sha256_bytes(f.read()) == want
        assert manifest["checksums"] == checksums
        assert manifest["item_ids"] == [it["public_item_id"] for it in release["items"]]

    def test_demo_isolation(self, tmp_path):
        release, _, _ = _demo_release()
        assert release["environment"] == "demo"
        index = build_search_index(release, release["dimensions"])
        assert index["environment"] == "demo"
        # Demo IDs must not be mistaken for real SJC item IDs.
        for it in release["items"]:
            assert it["public_item_id"].startswith("DEMO-")


class TestContentQuality:
    def _ok(self, record):
        return validate_public_item(record)

    def test_valid_record_passes(self):
        record = {
            "public_item_id": "SJC-X-20260101-0001",
            "title": "A title",
            "summary": "A summary.",
            "why_it_matters": "Why.",
            "source_name": "Source",
            "source_url": "https://example.com/",
            "source_date": "2026-01-01",
            "published_date": "2026-01-02",
            "relevance": "in_silverleaf",
            "display_topic": "utilities_water",
            "topic_ids": ["infrastructure"],
            "entity_ids": [],
            "place_ids": ["silverleaf"],
            "sensitivity_display": "none",
            "verification_display": "Confirmed from source",
        }
        res = self._ok(record)
        assert res.ok, res.errors

    def test_missing_required_copy_fails(self):
        record = {"public_item_id": "SJC-X-20260101-0002",
                  "title": "", "summary": "", "why_it_matters": "",
                  "source_name": "", "source_url": "",
                  "source_date": "", "published_date": "",
                  "relevance": "", "topic_ids": []}
        res = self._ok(record)
        assert not res.ok
        codes = " ".join(res.errors)
        for field in ("title", "summary", "why_it_matters", "source_name",
                      "source_date", "published_date", "relevance"):
            assert field in codes

    def test_missing_source_url_needs_unavailable_flag(self):
        base = {"public_item_id": "SJC-X-20260101-0003",
                "title": "t", "summary": "s", "why_it_matters": "w",
                "source_name": "src", "source_date": "2026-01-01",
                "published_date": "2026-01-02", "relevance": "countywide_impact",
                "display_topic": "utilities_water",
                "topic_ids": ["environment"]}
        res = self._ok(dict(base))
        assert not res.ok
        assert "source_url" in " ".join(res.errors)
        ok = self._ok(dict(base, source_unavailable=True))
        assert ok.ok, ok.errors

    def test_invalid_relevance_rejected(self):
        base = {"public_item_id": "SJC-X-20260101-0004",
                "title": "t", "summary": "s", "why_it_matters": "w",
                "source_name": "src",
                "source_url": "https://example.com/",
                "source_date": "2026-01-01", "published_date": "2026-01-02",
                "relevance": "maybe", "display_topic": "utilities_water", "topic_ids": ["environment"]}
        res = self._ok(base)
        assert not res.ok

    def test_unknown_field_rejected(self):
        base = {"public_item_id": "SJC-X-20260101-0005",
                "title": "t", "summary": "s", "why_it_matters": "w",
                "source_name": "src", "source_url": "https://e.com/",
                "source_date": "2026-01-01", "published_date": "2026-01-02",
                "relevance": "near_silverleaf", "display_topic": "utilities_water", "topic_ids": ["environment"]}
        res = self._ok(dict(base, secret_field="x"))
        assert not res.ok
        assert "unknown" in " ".join(res.errors)

    def test_internal_field_rejected(self):
        base = {"public_item_id": "SJC-X-20260101-0006",
                "title": "t", "summary": "s", "why_it_matters": "w",
                "source_name": "src", "source_url": "https://e.com/",
                "source_date": "2026-01-01", "published_date": "2026-01-02",
                "relevance": "near_silverleaf", "display_topic": "utilities_water", "topic_ids": ["environment"]}
        res = self._ok(dict(base, _dedupe_key="abc", reviewer_notes="secret"))
        assert not res.ok

    def test_internal_acronym_in_copy_warns(self):
        base = {"public_item_id": "SJC-X-20260101-0007",
                "title": "Item SJC-CN-20260603-0001 approved",
                "summary": "s", "why_it_matters": "w",
                "source_name": "src", "source_url": "https://e.com/",
                "source_date": "2026-01-01", "published_date": "2026-01-02",
                "relevance": "near_silverleaf", "display_topic": "utilities_water", "topic_ids": ["environment"]}
        res = self._ok(base)
        assert res.ok  # warning, not exclusion
        assert any("internal" in w for w in res.warnings)

    def test_proposal_needs_conditional_wording(self):
        base = {"public_item_id": "SJC-X-20260101-0008",
                "title": "Store will open next month", "summary": "s",
                "why_it_matters": "w", "source_name": "src",
                "source_url": "https://e.com/", "source_date": "2026-01-01",
                "published_date": "2026-01-02", "relevance": "in_silverleaf",
                "display_topic": "local_business",
                "topic_ids": ["economic_development"],
                "lifecycle": "proposed", "lifecycle_label": "Proposed"}
        res = self._ok(base)
        assert res.ok
        assert any("conditional" in w for w in res.warnings)

    def test_demo_fixture_passes_content_quality(self, tmp_path):
        release, _, warnings = _demo_release()
        assert not warnings, warnings
        for it in release["items"]:
            res = validate_public_item(it)
            assert res.ok, (it["public_item_id"], res.errors)


class TestRealMode:
    """Hermetic real-mode tests: sandbox copies of the real corpus + registry.

    build_real_release requires a full corpus (CorpusValidator scans all
    records), so we copy data/ and registry/ into a temp dir and optionally
    restrict which publication decisions are present. This keeps the tests
    deterministic regardless of live approval state.
    """

    @staticmethod
    def _sandbox(tmp_path, keep_decisions=()):
        import shutil
        sandbox = str(tmp_path / "sandbox")
        shutil.copytree(os.path.join(REPO_ROOT, "data"), os.path.join(sandbox, "data"))
        shutil.copytree(os.path.join(REPO_ROOT, "registry"), os.path.join(sandbox, "registry"))
        dec_dir = os.path.join(sandbox, "data", "publication_decisions")
        for name in os.listdir(dec_dir):
            if name == "legacy_exceptions.yaml":
                continue
            if name.rsplit(".", 1)[0] not in keep_decisions:
                os.remove(os.path.join(dec_dir, name))
        return sandbox

    @staticmethod
    def _run(tmp_path, monkeypatch, keep_decisions=(), reviewer="Buddy"):
        sandbox = TestRealMode._sandbox(tmp_path, keep_decisions)
        # publication_common computes its paths at import time, so point the
        # module constants at the sandbox rather than relying on env vars.
        import publication_common as pc
        monkeypatch.setattr(pc, "INTEL_ITEMS_DIR",
                            os.path.join(sandbox, "data", "intel_items"))
        monkeypatch.setattr(pc, "SOURCE_EVENTS_DIR",
                            os.path.join(sandbox, "data", "source_events"))
        monkeypatch.setattr(pc, "DECISIONS_DIR",
                            os.path.join(sandbox, "data", "publication_decisions"))
        monkeypatch.setattr(pc, "LEGACY_EXCEPTIONS_FILE",
                            os.path.join(sandbox, "data", "publication_decisions",
                                         "legacy_exceptions.yaml"))
        monkeypatch.setattr(pc, "SOURCES_FILE",
                            os.path.join(sandbox, "registry", "sources.yaml"))
        monkeypatch.setattr(pc, "COMMUNITIES_FILE",
                            os.path.join(sandbox, "registry", "communities.yaml"))
        monkeypatch.setattr(pc, "ENTITIES_FILE",
                            os.path.join(sandbox, "registry", "tracked_entities.yaml"))

        Args = type("Args", (), {
            "window_start": "2026-05-01T00:00:00Z",
            "window_end": "2026-08-04T00:00:00Z",
            "published_at": "2026-08-04T12:00:00Z",
            "now": "2026-08-04T12:00:00Z",
            "reviewer": reviewer,
        })
        return build_real_release("SJC-REL-TEST", src.GENERATOR_REVISION, Args())

    def test_real_mode_policy_selects_default_eligible_items_without_decisions(self, tmp_path, monkeypatch):
        release, reviewer, warnings = self._run(tmp_path, monkeypatch, keep_decisions=())
        assert release["environment"] == "real"
        assert release["items"]
        assert reviewer == "Buddy"

    def test_real_mode_selects_approved_first_release(self, tmp_path, monkeypatch):
        release, _, _ = self._run(tmp_path, monkeypatch, keep_decisions=(
            "SJC-CN-20260802-0001", "SJC-EM-20260626-0001",
            "SJC-UTIL-20260603-0001", "SJC-UTIL-20260603-0005"))
        ids = [it["public_item_id"] for it in release["items"]]
        for expected in ("SJC-CN-20260802-0001", "SJC-EM-20260626-0001",
                         "SJC-UTIL-20260603-0001", "SJC-UTIL-20260603-0005"):
            assert expected in ids
        # CR 16A carries the editorial relevance override.
        cr16a = next(it for it in release["items"]
                     if it["public_item_id"] == "SJC-CN-20260802-0001")
        assert cr16a["relevance"] == "near_silverleaf"

    def test_real_mode_requires_reviewer(self, tmp_path, monkeypatch):
        import pytest
        with pytest.raises(Exception):
            self._run(tmp_path, monkeypatch, reviewer=None)
