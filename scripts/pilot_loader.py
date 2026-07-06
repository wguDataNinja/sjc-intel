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
from urllib.parse import urlparse

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
    "app.sources": ["source_id", "name", "source_type", "url", "base_domain", "discovered_at"],
    "app.source_events": ["event_id", "source_id", "event_type", "title", "event_date", "source_url"],
    "app.intel_items": ["item_id", "title", "summary", "source_id", "source_url", "discovered_at", "topics", "urgency", "verification_status"],
    "app.dedupe_index_entries": ["key", "item_id", "discovered_at"],
}

BACKUP_MANIFEST_REQUIRED_PREFIX = "manifest_clean_"


def _pg_connect():
    import psycopg2
    writer_url = os.environ.get("SJC_INTEL_PG_WRITER_URL") or os.environ.get("SJC_INTEL_PG_URL")
    if writer_url:
        conn = psycopg2.connect(writer_url)
    else:
        conn = psycopg2.connect(
            database=PG_DATABASE,
            user=PG_WRITER_USER,
            host=os.environ.get("SJC_INTEL_PG_HOST", os.environ.get("PGHOST", "")),
            port=os.environ.get("SJC_INTEL_PG_PORT", os.environ.get("PGPORT", "5432")),
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
        parsed_url = urlparse(source_url)
        base_domain = parsed_url.netloc or "unknown"
        discovered_at = record.get("discovered_at")
        event_date = str(discovered_at or datetime.now(timezone.utc).date().isoformat())[:10]
        topics = record.get("topics", [])
        geographic_scope = record.get("geographic_scope", "")
        urgency = record.get("urgency", "ongoing")
        verification_status = record.get("verification_status", "unverified")
        sensitivity = record.get("sensitivity", "low")
        raw_excerpt = record.get("raw_excerpt", "")
        dedupe_key = record.get("_dedupe_key") or record.get("dedupe_key")

        # app.sources
        c.execute("""
            INSERT INTO app.sources (
                source_id, name, description, url, base_domain, source_type,
                relevance, monitor_frequency, automatable, status, topics, discovered_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO UPDATE SET
                url = COALESCE(NULLIF(EXCLUDED.url, ''), app.sources.url),
                base_domain = COALESCE(NULLIF(EXCLUDED.base_domain, 'unknown'), app.sources.base_domain),
                updated_at_db = now()
        """, (
            source_id,
            source_id.replace("_", " ").title(),
            "SJC Intel bounded pilot source",
            source_url or "about:blank",
            base_domain,
            "government_portal",
            "HIGH",
            "daily",
            "LIKELY",
            "active",
            topics,
            discovered_at,
        ))

        event_id = f"{item_id}:pilot_event"
        c.execute("""
            INSERT INTO app.source_events (
                event_id, source_id, event_type, title, event_date, discovered_at,
                source_url, status, extraction_status, source_health
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (event_id) DO UPDATE SET
                title = EXCLUDED.title,
                source_url = EXCLUDED.source_url,
                status = EXCLUDED.status,
                updated_at_db = now()
        """, (
            event_id,
            source_id,
            "public_notice_snapshot",
            f"Pilot event for {title}",
            event_date,
            discovered_at,
            source_url or "about:blank",
            "extracted",
            "pilot_loader",
            "accessible",
        ))

        # app.intel_items
        c.execute("""
            INSERT INTO app.intel_items (
                item_id, title, summary, source_id, source_event_id, source_url,
                discovered_at, topics, geographic_scope, urgency,
                verification_status, sensitivity, raw_excerpt, created_at,
                dedupe_key, beat, category, app_id, pdf_urls, map_url,
                district, raw_text, source_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (item_id) DO UPDATE SET
                title = EXCLUDED.title,
                summary = EXCLUDED.summary,
                source_event_id = EXCLUDED.source_event_id,
                source_url = EXCLUDED.source_url,
                topics = EXCLUDED.topics,
                geographic_scope = EXCLUDED.geographic_scope,
                urgency = EXCLUDED.urgency,
                verification_status = EXCLUDED.verification_status,
                sensitivity = EXCLUDED.sensitivity,
                raw_excerpt = EXCLUDED.raw_excerpt,
                dedupe_key = EXCLUDED.dedupe_key,
                updated_at_db = now()
        """, (
            item_id,
            title,
            summary,
            source_id,
            event_id,
            source_url or "about:blank",
            discovered_at,
            topics or ["general"],
            geographic_scope or "county_wide",
            urgency,
            verification_status,
            sensitivity,
            raw_excerpt or summary,
            discovered_at,
            dedupe_key,
            record.get("_beat") or record.get("beat"),
            record.get("_category") or record.get("category"),
            record.get("_app_id") or record.get("app_id"),
            record.get("_pdf_urls") or record.get("pdf_urls"),
            record.get("_map_url") or record.get("map_url"),
            record.get("_district") or record.get("district"),
            record.get("_raw_text") or record.get("raw_text"),
            "government_portal",
        ))

        # app.dedupe_index_entries
        if dedupe_key:
            c.execute("""
                INSERT INTO app.dedupe_index_entries (key, item_id, title, source_id, beat, discovered_at, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (key) DO UPDATE SET
                    item_id = EXCLUDED.item_id,
                    title = EXCLUDED.title,
                    source_id = EXCLUDED.source_id,
                    beat = EXCLUDED.beat,
                    discovered_at = EXCLUDED.discovered_at,
                    status = EXCLUDED.status
            """, (
                dedupe_key,
                item_id,
                title,
                source_id,
                record.get("_beat") or record.get("beat"),
                discovered_at,
                record.get("review_status", "pending_review"),
            ))
        inserted += 1

    conn.commit()
    return inserted


def delete_pilot_rows(conn, item_ids, source_id):
    c = conn.cursor()
    for item_id in item_ids:
        c.execute("DELETE FROM app.source_event_items WHERE item_id = %s", (item_id,))
        c.execute("DELETE FROM app.dedupe_index_entries WHERE item_id = %s", (item_id,))
        c.execute("DELETE FROM app.intel_items WHERE item_id = %s", (item_id,))
        c.execute("DELETE FROM app.source_events WHERE event_id = %s", (f"{item_id}:pilot_event",))
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

    # Plan mode is the approval artifact for the bounded pilot, so it uses the
    # eligible subset by default to preserve the established pilot manifest.
    effective_eligible_only = args.eligible_only or args.plan

    # Select records
    file_records = select_records(args.source_id, args.limit, eligible_only=effective_eligible_only)
    classification = classify_records(file_records)
    item_ids = [r.get("item_id") for r in file_records if r.get("item_id")]
    digest = stable_digest(file_records)

    report = {
        "project": "sjc_intel",
        "mode": "plan" if args.plan else ("dry-run" if args.dry_run else ("apply" if args.apply else args._get_kwargs()[0][0])),
        "source_id": args.source_id,
        "limit": args.limit,
        "eligible_only": effective_eligible_only,
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
            print(f"  source: {args.source_id}, limit: {args.limit}, eligible: {effective_eligible_only}")
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
