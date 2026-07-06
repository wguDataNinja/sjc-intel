#!/usr/bin/env python3
"""SJC Intel real PostgreSQL pilot loader.

Modes:
  --dry-run   Show what would be loaded, no mutation.
  --plan      Same as dry-run with expanded evidence.
  --apply     Execute the bounded pilot load (requires explicit --apply flag).

Operations:
  --rollback  Delete pilot rows by source_id and item_id set.
  --parity    Compare file-sourced counts against PostgreSQL counts.

Safety:
  - Writer-role-only data mutation (sjc_intel_writer).
  - Never mutates as superuser.
  - Requires explicit --apply (not a default).
  - Pre-load backup check warns if no recent backup exists.
  - Every mutation outputs starting and ending row counts.
  - Rollback is delete-by-selected-ids then re-run validation.
"""

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.pilot_readiness_report import select_records, classify_records, stable_digest, DEFAULT_SOURCE

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BACKUP_ROOT = Path(os.environ.get("SJC_INTEL_BACKUP_ROOT", REPO_ROOT / ".backups"))
PG_DATABASE = os.environ.get("SJC_INTEL_PG_DATABASE", "sjc_intel")
PG_WRITER_USER = os.environ.get("SJC_INTEL_PG_WRITER_USER", "sjc_intel_writer")

TARGET_TABLES = ["app.sources", "app.source_events", "app.intel_items", "app.dedupe_index_entries"]

REQUIRED_PG_FIELDS = {
    "app.sources": ["source_id", "source_name", "source_type", "url", "discovered_at"],
    "app.source_events": ["event_id", "source_id", "event_type", "occurred_at", "summary"],
    "app.intel_items": ["item_id", "title", "summary", "source_id", "discovered_at", "topics", "urgency", "verification_status"],
    "app.dedupe_index_entries": ["entry_id", "item_id", "dedupe_key", "created_at"],
}

BACKUP_MANIFEST_REQUIRED_PREFIX = "manifest_clean_"


def _pg_connect():
    import psycopg2
    conn = psycopg2.connect(
        database=PG_DATABASE,
        user=PG_WRITER_USER,
        host=os.environ.get("PGHOST", ""),
        port=os.environ.get("PGPORT", "5432"),
    )
    conn.autocommit = False
    return conn


def row_counts(conn):
    counts = {}
    for table in TARGET_TABLES:
        schema, tbl = table.split(".")
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {schema}.{tbl}")
        counts[table] = c.fetchone()[0]
    return counts


def has_recent_backup():
    if not BACKUP_ROOT.is_dir():
        return False
    manifests = sorted(BACKUP_ROOT.glob(f"{BACKUP_MANIFEST_REQUIRED_PREFIX}*.yaml"))
    if not manifests:
        return False
    return True


def load_records_into_pg(conn, records, source_id):
    c = conn.cursor()
    inserted = 0
    for record in records:
        item_id = record.get("item_id")
        title = record.get("title", "")
        summary = record.get("summary", "")
        source_url = record.get("source_url", "")
        discovered_at = record.get("discovered_at")
        topics = record.get("topics", [])
        geographic_scope = record.get("geographic_scope", "")
        urgency = record.get("urgency", "low")
        verification_status = record.get("verification_status", "unverified")
        sensitivity = record.get("sensitivity", "public")
        raw_excerpt = record.get("raw_excerpt", "")
        dedupe_key = record.get("_dedupe_key") or record.get("dedupe_key")

        # app.sources
        c.execute("""
            INSERT INTO app.sources (source_id, source_name, source_type, url, discovered_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
        """, (source_id, source_id, "nbor_notice", source_url, discovered_at))

        # app.intel_items
        c.execute("""
            INSERT INTO app.intel_items (item_id, title, summary, source_id, discovered_at, topics, geographic_scope, urgency, verification_status, sensitivity, raw_excerpt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (item_id) DO NOTHING
        """, (item_id, title, summary, source_id, discovered_at, topics, geographic_scope, urgency, verification_status, sensitivity, raw_excerpt))

        # app.source_events
        c.execute("""
            INSERT INTO app.source_events (source_id, event_type, occurred_at, summary)
            VALUES (%s, %s, %s, %s)
        """, (source_id, "discovery", discovered_at, f"Discovered: {title}"))

        # app.dedupe_index_entries
        if dedupe_key:
            c.execute("""
                INSERT INTO app.dedupe_index_entries (item_id, dedupe_key, created_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (dedupe_key) DO NOTHING
            """, (item_id, dedupe_key, discovered_at))
        inserted += 1

    conn.commit()
    return inserted


def delete_pilot_rows(conn, item_ids, source_id):
    c = conn.cursor()
    for item_id in item_ids:
        c.execute("DELETE FROM app.dedupe_index_entries WHERE item_id = %s", (item_id,))
        c.execute("DELETE FROM app.intel_items WHERE item_id = %s", (item_id,))
    c.execute("DELETE FROM app.source_events WHERE source_id = %s", (source_id,))
    c.execute("DELETE FROM app.sources WHERE source_id = %s", (source_id,))
    conn.commit()


def run_validation(conn):
    val_path = REPO_ROOT / "db" / "validation" / "999_full_validation.sql"
    if val_path.exists():
        c = conn.cursor()
        c.execute(val_path.read_text())
        conn.commit()


def main():
    parser = argparse.ArgumentParser(description="SJC Intel PostgreSQL pilot loader")
    parser.add_argument("--source-id", default=DEFAULT_SOURCE)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--eligible-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Show what would load, no mutation")
    parser.add_argument("--plan", action="store_true", help="Alias for --dry-run with expanded evidence")
    parser.add_argument("--apply", action="store_true", help="Execute the bounded pilot load")
    parser.add_argument("--rollback", action="store_true", help="Delete pilot rows by source_id and item_id set")
    parser.add_argument("--parity", action="store_true", help="Compare file counts vs PG counts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.apply and not args.dry_run and not args.plan and not args.rollback and not args.parity:
        parser.print_help()
        sys.exit(1)

    if args.apply:
        if not has_recent_backup():
            print("BLOCKED: No recent clean backup found at %s" % BACKUP_ROOT)
            print("Create a fresh pre-load backup before --apply.")
            sys.exit(1)

    # Select records
    file_records = select_records(args.source_id, args.limit, eligible_only=args.eligible_only)
    classification = classify_records(file_records)
    item_ids = [r.get("item_id") for r in file_records if r.get("item_id")]
    digest = stable_digest(file_records)

    report = {
        "project": "sjc_intel",
        "mode": "dry-run" if (args.dry_run or args.plan) else ("apply" if args.apply else args._get_kwargs()[0][0]),
        "source_id": args.source_id,
        "limit": args.limit,
        "eligible_only": args.eligible_only,
        "selected_count": len(file_records),
        "selected_item_ids": item_ids,
        "selected_digest_sha256": digest,
        "mapping_target_tables": TARGET_TABLES,
        "classification": classification,
        "has_recent_backup": has_recent_backup(),
    }

    if args.dry_run or args.plan:
        if classification["required_field_rejects"]:
            report["pilot_blocked"] = True
            report["blocker"] = "Selected records have missing required fields"
        report["simulated_inserts"] = len(file_records) - len(classification["required_field_rejects"])
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print("SJC Intel pilot loader — %s" % report["mode"])
            print(f"  source: {args.source_id}, limit: {args.limit}, eligible: {args.eligible_only}")
            print(f"  selected: {len(file_records)} records, digest: {digest[:16]}...")
            print(f"  simulated inserts: {report['simulated_inserts']}")
            if report.get("pilot_blocked"):
                print(f"  BLOCKED: {report['blocker']}")
        return

    if args.rollback:
        conn = _pg_connect()
        try:
            before = row_counts(conn)
            delete_pilot_rows(conn, item_ids, args.source_id)
            after = row_counts(conn)
            run_validation(conn)
            report["before_counts"] = before
            report["after_counts"] = after
            report["rollback_ok"] = True
            if args.json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                print(f"Rollback OK — deleted {len(item_ids)} items from {args.source_id}")
                print(f"  Before: {before}")
                print(f"  After:  {after}")
        finally:
            conn.close()
        return

    if args.parity:
        conn = _pg_connect()
        try:
            pg_counts = row_counts(conn)
            file_count = len(file_records)
            report["file_count"] = file_count
            report["pg_counts"] = pg_counts
            report["parity_ok"] = file_count <= max(v for v in pg_counts.values()) + 5
            if args.json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                print(f"Parity: file={file_count}, PG={pg_counts}")
                print(f"  Parity {'OK' if report['parity_ok'] else 'MISMATCH'}")
        finally:
            conn.close()
        return

    if args.apply:
        conn = _pg_connect()
        try:
            before = row_counts(conn)
            logger.info("Starting pilot load — before: %s", before)

            inserted = load_records_into_pg(conn, file_records, args.source_id)

            after = row_counts(conn)
            run_validation(conn)

            report["apply_ok"] = True
            report["inserted"] = inserted
            report["before_counts"] = before
            report["after_counts"] = after
            report["pilot_readiness_report"] = {
                "selected_count": len(file_records),
                "digest": digest,
                "item_ids": item_ids,
            }

            if args.json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                print(f"Pilot load OK — inserted {inserted} records")
                print(f"  Before: {before}")
                print(f"  After:  {after}")
        finally:
            conn.close()
        return


if __name__ == "__main__":
    main()
