from datetime import datetime, timezone

from scripts.retention import build_policy, dry_run_report, select_prunable_artifacts


def test_build_policy_keeps_raw_artifacts_bounded():
    policy = build_policy(
        {
            "source_id": "sjc_nbor_public_notices",
            "source_type": "government_portal",
            "monitor_frequency": "daily",
        }
    )
    assert policy.raw_artifact_retention_days == 30
    assert policy.raw_payload_format == "external_file_hash_only"
    assert policy.snapshot_required is True


def test_select_prunable_artifacts_protects_unarchived_required_records():
    as_of = datetime(2026, 7, 6, tzinfo=timezone.utc)
    records = [
        {
            "artifact_id": "old-ok",
            "retain_until": "2026-07-01T00:00:00Z",
            "archive_required": False,
            "prune_status": "retained",
        },
        {
            "artifact_id": "needs-archive",
            "retain_until": "2026-07-01T00:00:00Z",
            "archive_required": True,
            "prune_status": "retained",
        },
        {
            "artifact_id": "protected",
            "retain_until": "2026-07-01T00:00:00Z",
            "archive_required": False,
            "prune_status": "protected",
        },
    ]
    selected = select_prunable_artifacts(records, as_of=as_of)
    assert [row["artifact_id"] for row in selected] == ["old-ok"]


def test_dry_run_report_has_no_destructive_actions():
    report = dry_run_report(
        sources=[
            {
                "source_id": "sjc_bcc_calendar",
                "source_type": "government_portal",
                "monitor_frequency": "weekly",
            }
        ]
    )
    assert report["source_count"] == 1
    assert report["destructive_actions"] == []
