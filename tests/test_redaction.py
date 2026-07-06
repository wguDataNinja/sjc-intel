import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from health_export import PROHIBITED_FIELDS, redact_payload, validate_sanitized

FIXTURE_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")


def _load_fixture(name):
    path = os.path.join(FIXTURE_DIR, name)
    with open(path) as f:
        return json.load(f)


def test_redaction_strips_ip_address():
    data = {"ip_address": "192.168.1.1"}
    result = redact_payload(data)
    assert "ip_address" not in result


def test_redaction_strips_filesystem_path():
    data = {"filesystem_path": "/home/scraper/data/sjc_intel/raw"}
    result = redact_payload(data)
    assert "filesystem_path" not in result


def test_redaction_strips_credentials():
    data = {"api_key": "sk-abc123def456"}
    result = redact_payload(data)
    assert "api_key" not in result


def test_redaction_strips_all_prohibited_fields():
    data = {field: "test" for field in PROHIBITED_FIELDS}
    result = redact_payload(data)
    for field in PROHIBITED_FIELDS:
        assert field not in result, f"{field} was not redacted"


def test_redaction_preserves_allowed_fields():
    data = {
        "schema_version": 1,
        "project": "sjc_intel",
        "workflow": "daily_ingest",
        "status": "ok",
        "source_reachability": "ok",
    }
    result = redact_payload(data)
    for field in data:
        assert field in result, f"{field} was incorrectly removed"


def test_redaction_from_fixture_prohibited():
    data = _load_fixture("health_export_prohibited.json")
    result = redact_payload(data)
    assert "error_message_private" not in result
    assert "ip_address" not in result
    assert "filesystem_path" not in result
    assert "api_key" not in result
    assert "stack_trace" not in result
    assert result["project"] == "sjc_intel"
    assert result["status"] == "ok"
    assert result["schema_version"] == 1


def test_redaction_from_fixture_valid():
    data = _load_fixture("health_export_valid.json")
    result = redact_payload(data)
    assert result == data


def test_validate_sanitized_rejects_prohibited_fields():
    data = _load_fixture("health_export_prohibited.json")
    errors = validate_sanitized(data)
    prohibited_errors = [e for e in errors if "prohibited" in e]
    assert len(prohibited_errors) >= 1


def test_validate_sanitized_accepts_clean_payload():
    data = _load_fixture("health_export_valid.json")
    errors = validate_sanitized(data)
    assert len(errors) == 0


def test_validate_sanitized_rejects_invalid_status():
    data = _load_fixture("health_export_valid.json")
    data["status"] = "critical"
    errors = validate_sanitized(data)
    status_errors = [e for e in errors if "status" in e]
    assert len(status_errors) >= 1


def test_failure_state_stale_payload():
    data = _load_fixture("health_export_stale.json")
    errors = validate_sanitized(data)
    assert len(errors) == 0
    assert data["status"] == "warn"
    assert data["degraded_reason_code"] == "freshness_exceeded"


def test_failure_state_missing_file():
    path = os.path.join(FIXTURE_DIR, "health_export_nonexistent.json")
    assert not os.path.exists(path)


def test_redaction_handles_empty_input():
    data = {}
    result = redact_payload(data)
    assert result == {}
