import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.storage_adapter import create_adapter


def build_metric_snapshots(adapter, snapshot_time=None, grain="daily"):
    snapshot_time = snapshot_time or datetime.now(timezone.utc)
    snapshot_date = snapshot_time.date().isoformat()

    intel_items = adapter.list_items({"entity_type": "intel_items", "limit": 1000})
    sources = adapter.list_items({"entity_type": "sources", "limit": 1000})
    tracked_entities = adapter.list_items({"entity_type": "tracked_entities", "limit": 1000})
    review_queue = adapter.list_items({"entity_type": "queue_entries", "limit": 1000})

    snapshots = []
    snapshots.append(
        _snapshot(snapshot_date, grain, "intel_items_total", {}, len(intel_items), snapshot_time)
    )
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "intel_items_by_source", intel_items, "source_id", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "intel_items_by_status", intel_items, "review_status", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "intel_items_by_category", intel_items, "category", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "sources_by_type", sources, "source_type", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "sources_by_status", sources, "status", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "tracked_entities_by_type", tracked_entities, "entity_type", snapshot_time))
    snapshots.extend(_counter_snapshots(snapshot_date, grain, "review_queue_by_status", review_queue, "review_status", snapshot_time))

    for source in sources:
        source_id = source.get("source_id")
        if not source_id:
            continue
        source_items = [item for item in intel_items if item.get("source_id") == source_id]
        latest = _latest_value(source_items, "discovered_at")
        if latest:
            snapshots.append(
                _snapshot(
                    snapshot_date,
                    grain,
                    "source_latest_discovery",
                    {"source_id": source_id},
                    1,
                    snapshot_time,
                    notes=f"latest_discovered_at={latest}",
                )
            )
    return sorted(snapshots, key=lambda row: row["snapshot_id"])


def upsert_metric_snapshots(pg_adapter, snapshots):
    from scripts.pg_adapter import Json

    with pg_adapter._transaction(readonly=False) as conn:
        with conn.cursor() as cur:
            for snapshot in snapshots:
                payload = dict(snapshot)
                if Json is not None:
                    payload["dimensions"] = Json(snapshot["dimensions"])
                cur.execute(
                    """
                    INSERT INTO app.metric_snapshots (
                        snapshot_id, snapshot_date, grain, metric_name, dimensions,
                        dimensions_hash, metric_value, generated_at, retention_until,
                        visibility, notes
                    )
                    VALUES (
                        %(snapshot_id)s, %(snapshot_date)s, %(grain)s, %(metric_name)s,
                        %(dimensions)s, %(dimensions_hash)s, %(metric_value)s,
                        %(generated_at)s, %(retention_until)s, %(visibility)s, %(notes)s
                    )
                    ON CONFLICT (snapshot_date, grain, metric_name, dimensions_hash) DO UPDATE SET
                        metric_value = EXCLUDED.metric_value,
                        generated_at = EXCLUDED.generated_at,
                        retention_until = EXCLUDED.retention_until,
                        visibility = EXCLUDED.visibility,
                        notes = EXCLUDED.notes,
                        updated_at = now()
                    """,
                    payload,
                )
    return len(snapshots)


def _counter_snapshots(snapshot_date, grain, metric_name, rows, key, snapshot_time):
    counter = Counter(row.get(key) or "unknown" for row in rows)
    return [
        _snapshot(snapshot_date, grain, metric_name, {key: value}, count, snapshot_time)
        for value, count in sorted(counter.items())
    ]


def _snapshot(snapshot_date, grain, metric_name, dimensions, value, generated_at, notes=None):
    dimensions_json = json.dumps(dimensions, sort_keys=True, separators=(",", ":"))
    dimensions_hash = hashlib.sha256(dimensions_json.encode("utf-8")).hexdigest()
    identity = "|".join([snapshot_date, grain, metric_name, dimensions_hash])
    snapshot_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return {
        "snapshot_id": snapshot_id,
        "snapshot_date": snapshot_date,
        "grain": grain,
        "metric_name": metric_name,
        "dimensions": dimensions,
        "dimensions_hash": dimensions_hash,
        "metric_value": value,
        "generated_at": generated_at.isoformat(),
        "retention_until": None,
        "visibility": "public_safe",
        "notes": notes,
    }


def _latest_value(rows, key):
    values = [row.get(key) for row in rows if row.get(key)]
    return max(values) if values else None


def main():
    parser = argparse.ArgumentParser(description="Generate compact SJC metric snapshots.")
    parser.add_argument("--backend", choices=["file", "pg"], default=None)
    parser.add_argument("--grain", choices=["daily", "weekly", "monthly", "current"], default="daily")
    parser.add_argument("--write", action="store_true", help="Write snapshots to PostgreSQL.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    adapter = create_adapter(args.backend)
    snapshots = build_metric_snapshots(adapter, grain=args.grain)
    if args.write:
        from scripts.pg_adapter import PgAdapter

        if not isinstance(adapter, PgAdapter):
            raise SystemExit("--write requires --backend pg")
        if not _write_enabled():
            raise SystemExit("Snapshot writes require SJC_INTEL_SNAPSHOT_WRITE_ENABLED=true")
        count = upsert_metric_snapshots(adapter, snapshots)
    else:
        count = 0

    report = {
        "snapshot_count": len(snapshots),
        "written_count": count,
        "snapshots": snapshots,
        "destructive_actions": [],
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Generated {len(snapshots)} metric snapshots; written={count}")


def _write_enabled():
    import os

    return os.environ.get("SJC_INTEL_SNAPSHOT_WRITE_ENABLED", "false").lower() in ("true", "1", "yes")


if __name__ == "__main__":
    main()
