"""Tests for SJC Intel pilot loader — no real PG or external services."""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.pilot_loader import TARGET_TABLES, REQUIRED_PG_FIELDS, select_records, classify_records, stable_digest


def test_target_tables_defined():
    assert len(TARGET_TABLES) == 4
    assert "app.sources" in TARGET_TABLES
    assert "app.intel_items" in TARGET_TABLES


def test_required_pg_fields_defined():
    assert "app.sources" in REQUIRED_PG_FIELDS
    assert "app.intel_items" in REQUIRED_PG_FIELDS


def test_select_records_defaults():
    records = select_records("sjc_nbor_public_notices", 5, eligible_only=True)
    assert len(records) <= 5
    if records:
        assert "item_id" in records[0]


def test_classify_records_empty():
    result = classify_records([])
    assert result["required_field_rejects"] == []
    assert result["duplicate_item_ids"] == []
    assert result["duplicate_dedupe_keys"] == []


def test_classify_records_valid():
    records = [{"item_id": "SJC-NB-20260101-001", "title": "T", "summary": "S", "source_id": "src1",
                "source_url": "http://x", "discovered_at": "2026-01-01", "topics": ["t"],
                "geographic_scope": "local", "urgency": "low", "verification_status": "unverified",
                "sensitivity": "public", "raw_excerpt": "...", "created_at": "2026-01-01"}]
    result = classify_records(records)
    assert result["required_field_rejects"] == []


def test_classify_records_missing_fields():
    records = [{"item_id": "SJC-NB-20260101-001"}]  # missing most required fields
    result = classify_records(records)
    assert len(result["required_field_rejects"]) == 1


def test_select_records_empty_source():
    records = select_records("nonexistent_source", 5)
    assert records == []


def test_stable_digest_deterministic():
    r1 = [{"a": 1, "b": 2}]
    r2 = [{"b": 2, "a": 1}]
    assert stable_digest(r1) == stable_digest(r2)


def test_stable_digest_differs():
    assert stable_digest([{"a": 1}]) != stable_digest([{"a": 2}])


def test_dry_run_no_mutation():
    """Verify --dry-run runs without connecting to PG."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/pilot_loader.py", "--dry-run", "--limit", "3", "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["mode"] == "dry-run"
    assert report["project"] == "sjc_intel"
    assert report["selected_count"] >= 0


def test_plan_mode():
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/pilot_loader.py", "--plan", "--limit", "3", "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["mode"] == "plan"
    assert "simulated_inserts" in report
