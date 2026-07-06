from datetime import datetime, timezone

from scripts.metrics_snapshot import build_metric_snapshots


class FakeAdapter:
    def list_items(self, filter_dict=None):
        entity_type = (filter_dict or {}).get("entity_type", "intel_items")
        if entity_type == "sources":
            return [
                {"source_id": "sjc_nbor_public_notices", "source_type": "government_portal", "status": "active"},
                {"source_id": "st_johns_citizen", "source_type": "local_media", "status": "observed"},
            ]
        if entity_type == "tracked_entities":
            return [{"entity_id": "e1", "entity_type": "development"}]
        if entity_type == "queue_entries":
            return [{"queue_id": "q1", "review_status": "pending_review"}]
        return [
            {
                "item_id": "SJC-1",
                "source_id": "sjc_nbor_public_notices",
                "review_status": "pending_review",
                "category": "development",
                "discovered_at": "2026-07-06T00:00:00Z",
            },
            {
                "item_id": "SJC-2",
                "source_id": "st_johns_citizen",
                "review_status": "approved",
                "category": "schools",
                "discovered_at": "2026-07-05T00:00:00Z",
            },
        ]


def test_metric_snapshots_are_deterministic_and_compact():
    generated_at = datetime(2026, 7, 6, 12, tzinfo=timezone.utc)
    first = build_metric_snapshots(FakeAdapter(), snapshot_time=generated_at)
    second = build_metric_snapshots(FakeAdapter(), snapshot_time=generated_at)
    assert first == second
    assert any(row["metric_name"] == "intel_items_total" and row["metric_value"] == 2 for row in first)
    assert all(row["visibility"] == "public_safe" for row in first)


def test_snapshot_rerun_updates_same_identity_for_same_day():
    morning = datetime(2026, 7, 6, 8, tzinfo=timezone.utc)
    evening = datetime(2026, 7, 6, 18, tzinfo=timezone.utc)
    first = build_metric_snapshots(FakeAdapter(), snapshot_time=morning)
    second = build_metric_snapshots(FakeAdapter(), snapshot_time=evening)
    first_ids = sorted(row["snapshot_id"] for row in first)
    second_ids = sorted(row["snapshot_id"] for row in second)
    assert first_ids == second_ids
