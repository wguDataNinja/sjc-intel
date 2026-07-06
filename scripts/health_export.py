#!/usr/bin/env python3
"""
SJC Intel — Sanitized health export producer (INERT).

Reads SHARED-003 contract rules and outputs fake/dry-run sanitized JSON.
No live data reading. Disabled by default via --dry-run flag or
SJC_INTEL_HEALTH_EXPORT_ENABLED=false environment variable.

Usage:
    python scripts/health_export.py --dry-run
    SJC_INTEL_HEALTH_EXPORT_ENABLED=true python scripts/health_export.py --dry-run
"""

import json
import os
import sys
from datetime import datetime, timezone

EXPORT_ENABLED_ENV = "SJC_INTEL_HEALTH_EXPORT_ENABLED"

# SHARED-003 prohibited field names
PROHIBITED_FIELDS = {
    "error_message_private", "error_message", "raw_payload",
    "source_url", "filesystem_path", "credential", "api_key",
    "token", "cookie", "session_id", "browser_profile",
    "private_notes", "reviewer", "approval_detail", "backlog_detail",
    "ip_address", "hostname", "local_path", "stack_trace",
    "sql_error", "chat_body", "reddit_body", "raw_html", "raw_response",
}

# SHARED-003 required sanitized fields
REQUIRED_SANITIZED_FIELDS = [
    "schema_version", "generated_at", "project", "workflow",
    "status", "last_success", "freshness", "expected_cadence",
    "volume_24h", "incident", "backup_state",
]

VALID_STATUSES = {"ok", "warn", "fail", "skip"}
VALID_BACKUP_STATES = {"ok", "stale", "fail", "not_applicable"}

SCHEMA_VERSION = 1


def redact_payload(data):
    """Return a copy of data with all prohibited fields removed."""
    return {k: v for k, v in data.items() if k not in PROHIBITED_FIELDS}


def validate_sanitized(data):
    """Validate sanitized payload against SHARED-003 rules. Returns list of errors."""
    errors = []
    for field in REQUIRED_SANITIZED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors.append(f"invalid status: {data['status']}")
    if "backup_state" in data and data["backup_state"] not in VALID_BACKUP_STATES:
        errors.append(f"invalid backup_state: {data['backup_state']}")
    if "schema_version" in data and not isinstance(data["schema_version"], int):
        errors.append(f"schema_version must be int, got {type(data['schema_version']).__name__}")
    found_prohibited = [f for f in data if f in PROHIBITED_FIELDS]
    if found_prohibited:
        errors.append(f"prohibited fields found: {found_prohibited}")
    return errors


def build_fake_health_payload():
    """Build a fake dry-run sanitized health payload for SJC Intel."""
    now = datetime.now(timezone.utc)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "project": "sjc_intel",
        "workflow": "daily_ingest",
        "status": "ok",
        "last_success": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freshness": 300,
        "expected_cadence": 86400,
        "volume_24h": 47,
        "incident": False,
        "degraded_reason_code": None,
        "backup_state": "not_applicable",
        "migration_version": None,
        "source_reachability": "ok",
        "monthly_closeout_age": 0,
        "dedupe_index_size": 142,
        "review_queue_pending": 5,
        "source_count": 28,
        "tracked_entity_count": 12,
    }


def schema_version_report():
    """Return schema and migration versions from environment or config."""
    return {
        "schema_version": SCHEMA_VERSION,
        "schema_name": "SHARED-003 Health Contract",
        "contract_version": "1.0.0",
        "migration_version": os.environ.get("SJC_INTEL_MIGRATION_VERSION", None),
        "export_enabled": os.environ.get(EXPORT_ENABLED_ENV, "false").lower() == "true",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def main():
    is_dry_run = "--dry-run" in sys.argv
    is_enabled = os.environ.get(EXPORT_ENABLED_ENV, "false").lower() == "true"

    if not is_enabled and not is_dry_run:
        print(f"Health export disabled. Set {EXPORT_ENABLED_ENV}=true or use --dry-run.")
        sys.exit(0)

    payload = build_fake_health_payload()

    if "--redact-test" in sys.argv:
        payload_with_secrets = dict(payload)
        payload_with_secrets["ip_address"] = "192.168.1.1"
        payload_with_secrets["filesystem_path"] = "/home/scraper/data/sjc_intel/raw"
        payload_with_secrets["api_key"] = "sk-abc123"
        sanitized = redact_payload(payload_with_secrets)
        print("Redaction test: ip_address" if "ip_address" not in sanitized else "FAIL")
        print("Redaction test: filesystem_path" if "filesystem_path" not in sanitized else "FAIL")
        print("Redaction test: api_key" if "api_key" not in sanitized else "FAIL")
        output = sanitized
    else:
        output = payload

    errors = validate_sanitized(output)
    if errors:
        print("Validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(output, indent=2))

    if is_dry_run:
        version = schema_version_report()
        print(f"\n# Schema version report: {json.dumps(version)}", file=sys.stderr)


if __name__ == "__main__":
    main()
