import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "registry" / "sources.yaml"


RAW_RETENTION_BY_TYPE = {
    "wordpress_blog": 14,
    "wordpress_portal": 14,
    "government_portal": 30,
    "official_special_district": 30,
    "gis_map": 7,
    "cms": 14,
    "local_media": 7,
    "social_media": 3,
    "alias": 0,
}


NORMALIZED_RETENTION_BY_TYPE = {
    "social_media": 90,
    "local_media": 180,
}


EXPECTED_RECORDS_BY_FREQUENCY = {
    "realtime": 20,
    "daily": 10,
    "weekly": 25,
    "monthly": 30,
    "per_event": 40,
}


@dataclass(frozen=True)
class RetentionPolicy:
    source_id: str
    source_type: str
    fetch_frequency: str
    expected_records_per_run: int
    raw_payload_format: str
    raw_artifact_retention_days: int
    normalized_retention_days: int | None
    retry_window_days: int
    snapshot_required: bool
    archive_before_prune: bool
    prune_key: str
    ui_dependency: str
    notes: str


def load_source_registry(path=REGISTRY_PATH):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("sources", [])


def build_policy(source):
    source_type = source.get("source_type", "government_portal")
    frequency = source.get("monitor_frequency", "weekly")
    raw_days = RAW_RETENTION_BY_TYPE.get(source_type, 14)
    normalized_days = NORMALIZED_RETENTION_BY_TYPE.get(source_type)
    archive_before_prune = source_type in ("local_media", "social_media")
    raw_format = "none" if source_type == "alias" else "external_file_hash_only"
    notes = (
        "Raw artifacts remain outside PostgreSQL; PostgreSQL stores hashes, provenance, "
        "and current normalized state."
    )
    return RetentionPolicy(
        source_id=source["source_id"],
        source_type=source_type,
        fetch_frequency=frequency,
        expected_records_per_run=EXPECTED_RECORDS_BY_FREQUENCY.get(frequency, 10),
        raw_payload_format=raw_format,
        raw_artifact_retention_days=raw_days,
        normalized_retention_days=normalized_days,
        retry_window_days=max(7, min(raw_days or 7, 30)),
        snapshot_required=True,
        archive_before_prune=archive_before_prune,
        prune_key="retain_until",
        ui_dependency="current_normalized_state_and_compact_snapshots",
        notes=notes,
    )


def build_policies(sources=None):
    sources = sources if sources is not None else load_source_registry()
    return [build_policy(source) for source in sources if source.get("source_id")]


def select_prunable_artifacts(records, as_of=None):
    as_of = as_of or datetime.now(timezone.utc)
    selected = []
    for record in records:
        if record.get("prune_status") == "protected":
            continue
        if record.get("archive_required") and not record.get("archived_at"):
            continue
        retain_until = _parse_datetime(record.get("retain_until"))
        if retain_until and retain_until <= as_of:
            selected.append(record)
    return selected


def dry_run_report(sources=None, as_of=None):
    policies = build_policies(sources)
    total_expected_daily_records = 0.0
    for policy in policies:
        total_expected_daily_records += _daily_rate(policy)
    return {
        "generated_at": (as_of or datetime.now(timezone.utc)).isoformat(),
        "source_count": len(policies),
        "estimated_records_per_day": round(total_expected_daily_records, 2),
        "policies": [asdict(policy) for policy in policies],
        "destructive_actions": [],
    }


def _daily_rate(policy):
    if policy.fetch_frequency == "realtime":
        return policy.expected_records_per_run
    if policy.fetch_frequency == "daily":
        return policy.expected_records_per_run
    if policy.fetch_frequency == "weekly":
        return policy.expected_records_per_run / 7.0
    if policy.fetch_frequency == "monthly":
        return policy.expected_records_per_run / 30.0
    return policy.expected_records_per_run / 7.0


def _parse_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def main():
    parser = argparse.ArgumentParser(description="Build SJC retention policy and pruning dry-run reports.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()
    report = dry_run_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"SJC retention dry run: {report['source_count']} sources")
        print(f"Estimated records/day: {report['estimated_records_per_day']}")
        print("Destructive actions: none")


if __name__ == "__main__":
    main()
