#!/usr/bin/env python3
"""Dry-run readiness report for a bounded SJC Intel PostgreSQL pilot.

This script is intentionally non-mutating. It reads the file-backed source of
truth, selects a deterministic pilot subset, and reports mapping/dedup facts
needed before a real PostgreSQL loader is authorized.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.file_adapter import FileAdapter
from scripts.pg_adapter import PgAdapter


DEFAULT_SOURCE = "sjc_nbor_public_notices"


def stable_digest(records):
    payload = json.dumps(records, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def select_records(source_id, limit, eligible_only=False):
    adapter = FileAdapter()
    records = adapter.list_items({"source_id": source_id})
    records = sorted(records, key=lambda r: (r.get("discovered_at") or "", r.get("item_id") or ""))
    if not eligible_only:
        return records[:limit]
    selected = []
    seen_dedupe = set()
    for record in records:
        classification = classify_records([record])
        dedupe_key = record.get("_dedupe_key") or record.get("dedupe_key")
        if classification["required_field_rejects"]:
            continue
        if dedupe_key and dedupe_key in seen_dedupe:
            continue
        if dedupe_key:
            seen_dedupe.add(dedupe_key)
        selected.append(record)
        if len(selected) >= limit:
            break
    return selected


def classify_records(records):
    required = {
        "item_id",
        "title",
        "summary",
        "source_id",
        "source_url",
        "discovered_at",
        "topics",
        "geographic_scope",
        "urgency",
        "verification_status",
        "sensitivity",
        "raw_excerpt",
        "created_at",
    }
    rejects = []
    dedupe_keys = []
    item_ids = []
    for record in records:
        missing = sorted(k for k in required if record.get(k) in (None, "", []))
        item_id = record.get("item_id")
        dedupe_key = record.get("_dedupe_key") or record.get("dedupe_key")
        if item_id:
            item_ids.append(item_id)
        if dedupe_key:
            dedupe_keys.append(dedupe_key)
        if missing:
            rejects.append({
                "item_id": item_id,
                "reason": "missing_required_fields",
                "fields": missing,
            })
    duplicate_item_ids = sorted(k for k in set(item_ids) if item_ids.count(k) > 1)
    duplicate_dedupe_keys = sorted(k for k in set(dedupe_keys) if dedupe_keys.count(k) > 1)
    return {
        "required_field_rejects": rejects,
        "duplicate_item_ids": duplicate_item_ids,
        "duplicate_dedupe_keys": duplicate_dedupe_keys,
    }


def main():
    parser = argparse.ArgumentParser(description="SJC Intel pilot readiness dry-run")
    parser.add_argument("--source-id", default=DEFAULT_SOURCE)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--eligible-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    records = select_records(args.source_id, args.limit, eligible_only=args.eligible_only)
    classification = classify_records(records)
    pg_health = PgAdapter().get_health()
    gate_blockers = []
    if pg_health.get("status") != "ok":
        gate_blockers.append("PostgreSQL adapter is not implemented/enabled for live reads or writes")
    if classification["required_field_rejects"]:
        gate_blockers.append("Selected subset has records missing required target fields")
    if classification["duplicate_item_ids"]:
        gate_blockers.append("Selected subset has duplicate item_id values")
    if classification["duplicate_dedupe_keys"]:
        gate_blockers.append("Selected subset has duplicate dedupe keys")

    report = {
        "project": "sjc_intel",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dry_run_only": True,
        "source_id": args.source_id,
        "limit": args.limit,
        "eligible_only": args.eligible_only,
        "selected_count": len(records),
        "selected_item_ids": [r.get("item_id") for r in records],
        "selected_digest_sha256": stable_digest(records),
        "mapping_target_tables": [
            "app.sources",
            "app.source_events",
            "app.intel_items",
            "app.dedupe_index_entries",
        ],
        "deduplication_keys": {
            "primary": "app.intel_items.item_id",
            "secondary": "app.intel_items.dedupe_key unique where not null",
        },
        "rollback_model": "delete pilot rows by deterministic item_id set, then rerun 999 validation",
        "delete_and_reimport_model": "same selected source_id and sorted item_id list must recreate the same digest",
        "pg_adapter_health": pg_health,
        "classification": classification,
        "gate_status": "BLOCKED" if gate_blockers else "READY_FOR_OPERATOR_GATE",
        "gate_blockers": gate_blockers,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    print("SJC Intel pilot readiness dry-run")
    print(f"source_id: {report['source_id']}")
    print(f"selected_count: {report['selected_count']}")
    print(f"digest: {report['selected_digest_sha256']}")
    print(f"gate_status: {report['gate_status']}")
    for blocker in gate_blockers:
        print(f"blocker: {blocker}")


if __name__ == "__main__":
    main()
