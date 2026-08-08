#!/usr/bin/env python3
"""Validate the evidence-backed SilverLeaf mobility scope registry."""
import argparse
import json
import os
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOBILITY_FILE = os.path.join(REPO_ROOT, "registry", "silverleaf_mobility.yaml")
SOURCES_FILE = os.path.join(REPO_ROOT, "registry", "sources.yaml")
ENTITIES_FILE = os.path.join(REPO_ROOT, "registry", "tracked_entities.yaml")

RELATIONSHIPS = {
    "direct_access", "direct_connection_interface", "nearby_commute_corridor",
    "contextual_only",
}


def load_yaml(path):
    with open(path) as handle:
        return yaml.safe_load(handle)


def validate():
    errors, warnings, checks = [], [], []

    def check(name, ok, detail=""):
        checks.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")

    if not os.path.exists(MOBILITY_FILE):
        return {"status": "FAIL", "errors": ["registry/silverleaf_mobility.yaml missing"],
                "warnings": [], "checks": []}
    mobility = load_yaml(MOBILITY_FILE)
    sources = load_yaml(SOURCES_FILE)
    entities = load_yaml(ENTITIES_FILE)
    authority = {item.get("id"): item for item in mobility.get("authority_sources", []) if item.get("id")}
    source_ids = {item.get("source_id") for item in sources.get("sources", []) if item.get("source_id")}
    entity_ids = {item.get("entity_id") for item in entities.get("tracked_entities", []) if item.get("entity_id")}
    segments = mobility.get("segments", [])

    check("schema version present", bool(mobility.get("schema_version")))
    check("authority sources present", len(authority) >= 5, f"found {len(authority)}")
    bad_urls = [item_id for item_id, item in authority.items()
                if not str(item.get("source_url", "")).startswith("https://")]
    check("authority URLs use HTTPS", not bad_urls, str(bad_urls))
    required_authority = {"SJC-CR2209-OPEN-2025", "SJC-SR16-IGP-2025",
                          "FDOT-SR16-IGP-I95-2025", "SJC-CR210-COMPLETE-2026"}
    check("required project authorities present", required_authority <= set(authority),
          str(sorted(required_authority - set(authority))))
    check("segments present", len(segments) >= 5, f"found {len(segments)}")

    bad_segments = []
    for segment in segments:
        segment_id = segment.get("id", "?")
        if segment.get("relationship") not in RELATIONSHIPS:
            bad_segments.append(f"{segment_id}: invalid relationship")
        endpoints = segment.get("endpoints") or {}
        if not endpoints.get("from") or not endpoints.get("to"):
            bad_segments.append(f"{segment_id}: endpoints incomplete")
        unresolved_authority = [item_id for item_id in segment.get("source_ids", []) if item_id not in authority]
        if not segment.get("source_ids") or unresolved_authority:
            bad_segments.append(f"{segment_id}: unresolved authority {unresolved_authority}")
        unresolved_monitor_source = [item_id for item_id in segment.get("monitor_sources", []) if item_id not in source_ids]
        if not segment.get("monitor_sources") or unresolved_monitor_source:
            bad_segments.append(f"{segment_id}: unresolved monitor source {unresolved_monitor_source}")
        if not segment.get("selection_rule") or not segment.get("exclusions"):
            bad_segments.append(f"{segment_id}: missing selection rule or exclusions")
        entity_id = segment.get("linked_entity_id")
        if entity_id and entity_id not in entity_ids:
            bad_segments.append(f"{segment_id}: unresolved entity {entity_id}")
    check("segments are source-backed and bounded", not bad_segments, str(bad_segments))

    direct = [segment for segment in segments if segment.get("relationship") == "direct_access"]
    contextual = [segment for segment in segments if segment.get("relationship") == "contextual_only"]
    check("at least one direct-access segment", bool(direct), "")
    check("contextual corridors explicitly constrained", all(segment.get("exclusions") for segment in contextual),
          str([segment.get("id") for segment in contextual if not segment.get("exclusions")]))

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "segments": len(segments),
        "authority_sources": len(authority),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate SilverLeaf mobility scope registry.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SilverLeaf Mobility Scope Validation")
        print("=" * 50)
        for check in result["checks"]:
            print(f"  [{'PASS' if check['passed'] else 'FAIL'}] {check['name']}"
                  + (f" — {check['detail']}" if check.get("detail") else ""))
        print("=" * 50)
        print(f"Result: {result['status']} ({len(result['errors'])} errors)")
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
