#!/usr/bin/env python3
"""
SJC_Intel — bounded local weekly runner (workspace-safe).

Runs explicitly approved monitors into an isolated run workspace and, when
requested, assembles a versioned transfer bundle. NEVER writes to the
authoritative corpus paths by default: data/intel_items/, data/source_events/,
data/review_queue/, data/index/, registry/sources.yaml.

Contract authority: docs/weekly_operational_contract.md
Workspace layout (established by Task 13):

    runtime/weekly/{run_id}/
      run.json              # run record (contract §7.4)
      source_health/        # {source_id}.json
      source_events/        # {source_id}.json
      intel_candidates/     # {source_id}.json  (status: candidate)
      source_proposals/     # proposals.json    (proposals only, never promoted)
      raw/                  # bounded raw captures
      logs/                 # run.log

Usage (repo root):

    python3 scripts/run_weekly.py \
        --run-id SJC-WK-20260803-0001 \
        --monitor sjc_nbor_public_notices \
        [--offline-html tests/fixtures/nbor_raw.html] \
        --git-sha <sha> --registry-revision <sha> \
        --window-start 2026-08-03T10:00:00Z --window-end 2026-08-03T11:00:00Z \
        [--workspace-root runtime/weekly] \
        [--bundle-out data/incoming/pre-bundles] \
        [--status completed]

Approved monitors (Stage A): only `sjc_nbor_public_notices` is implemented in
this foundation. Additional monitors must be added to the MONITORS registry and
approved explicitly.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET

try:
    from scripts.bundle_build import (
        assemble_bundle,
        build_run_json,
        count_candidates,
        write_manifest_and_checksums,
    )
    from scripts.bundle_common import (
        RETENTION_DAYS_DEFAULT,
        RUN_JSON_REQUIRED_FIELDS,
        replay_identity,
        valid_run_id,
        write_json,
    )
    from scripts.extract_nbor import (
        NBOR_URL,
        candidate_items,
        fetch_page,
        normalize_records,
        parse_rows,
    )
except ImportError:  # standalone: python3 scripts/run_weekly.py
    from bundle_build import (
        assemble_bundle,
        build_run_json,
        count_candidates,
        write_manifest_and_checksums,
    )
    from bundle_common import (
        RETENTION_DAYS_DEFAULT,
        RUN_JSON_REQUIRED_FIELDS,
        replay_identity,
        valid_run_id,
        write_json,
    )
    from extract_nbor import (
        NBOR_URL,
        candidate_items,
        fetch_page,
        normalize_records,
        parse_rows,
    )

DEFAULT_WORKSPACE_ROOT = "runtime/weekly"
DEFAULT_PROFILE = "sjc-weekly-001"

SOURCE_EVENT_PREFIX = {"sjc_nbor_public_notices": "EVT-NBOR"}


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_run_id(workspace_root):
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    seq = 1
    if os.path.isdir(workspace_root):
        for name in os.listdir(workspace_root):
            if name.startswith(f"SJC-WK-{today}-"):
                try:
                    seq = max(seq, int(name.rsplit("-", 1)[-1]) + 1)
                except ValueError:
                    pass
    return f"SJC-WK-{today}-{seq:04d}"


def make_workspace(workspace_root, run_id, force=False):
    ws = os.path.join(workspace_root, run_id)
    if os.path.exists(ws):
        if force:
            shutil.rmtree(ws)
        else:
            raise SystemExit(
                f"run workspace already exists: {ws} (duplicate/concurrent run "
                f"prevention). Use --force only to replace a failed run."
            )
    for sub in ("source_health", "source_events", "intel_candidates",
                "source_proposals", "raw", "logs"):
        os.makedirs(os.path.join(ws, sub), exist_ok=True)
    return ws


def run_nbor_monitor(ws, offline_html):
    """Stage A monitor for sjc_nbor_public_notices (deterministic path)."""
    source_id = "sjc_nbor_public_notices"
    now = utc_now_iso()
    errors = []

    try:
        if offline_html:
            with open(offline_html) as f:
                html = f.read()
            http_status = 200
            health = "accessible"
        else:
            html = fetch_page()
            http_status = 200
            health = "accessible"
    except Exception as e:
        errors.append(f"fetch failed: {e}")
        http_status = None
        health = "unreachable"
        html = None

    records = []
    items = []
    if html is not None:
        try:
            records = parse_rows(html)
            items = normalize_records(records, source_event_id=None)
        except Exception as e:
            errors.append(f"parse failed: {e}")

    cands = candidate_items(items)
    today_num = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    event_id = f"{SOURCE_EVENT_PREFIX[source_id]}-{today_num}-0001"

    write_json(
        os.path.join(ws, "intel_candidates", f"{source_id}.json"),
        {"source_id": source_id, "fetched_at": now, "source_url": NBOR_URL,
         "total_items": len(cands), "items": cands},
    )
    write_json(
        os.path.join(ws, "source_events", f"{source_id}.json"),
        {"source_id": source_id, "event_id": event_id, "event_type": "public_notice_snapshot",
         "source_url": NBOR_URL, "status": "extracted" if not errors else "blocked",
         "extraction_status": f"{len(cands)} candidates",
         "source_health": health, "generated_at": now, "errors": errors},
    )
    write_json(
        os.path.join(ws, "source_health", f"{source_id}.json"),
        {"source_id": source_id, "checked_at": now, "http_status": http_status,
         "bytes": len(html) if html else 0, "health": health, "retries": 0,
         "last_error": errors[-1] if errors else None},
    )
    if html is not None:
        with open(os.path.join(ws, "raw", f"{source_id}.html"), "w") as f:
            f.write(html)

    return {
        "source_id": source_id,
        "health": health,
        "http_status": http_status,
        "candidates": len(cands),
        "errors": errors,
    }


MONITORS = {
    "sjc_nbor_public_notices": run_nbor_monitor,
}


# ── SJSO RSS monitor ────────────────────────────────────────────────────

SJSO_FEED_URL = "https://www.sjso.org/feed/"
SJSO_USER_AGENT = "Mozilla/5.0 (SJC_Intel SJSO RSS Extractor/1.0)"

CRIME_REVIEW_KEYWORDS = [
    "arrest", "charged", "jail", "prison", "suspect", "victim", "shooting",
    "homicide", "investigat", "burglar", "robbery", "stolen", "warrant",
    "drug", "dui", "driving under the influence",
]


def fetch_rss(offline_rss):
    import urllib.request
    if offline_rss:
        with open(offline_rss) as f:
            return f.read(), 200
    req = urllib.request.Request(SJSO_FEED_URL, headers={"User-Agent": SJSO_USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace"), resp.getcode()


def parse_rss_entries(xml_text):
    """Parse RSS 2.0 items into raw entry dicts (title, link, pub_date, description)."""
    entries = []
    root = ET.fromstring(xml_text)
    for item in root.iter("item"):
        def _t(tag):
            el = item.find(tag)
            return el.text.strip() if el is not None and el.text else ""
        entries.append({
            "title": _t("title"),
            "link": _t("link"),
            "pub_date": _t("pubDate"),
            "description": _t("description"),
        })
    return [e for e in entries if e["title"] and e["link"]]


def normalize_sjso_candidates(entries, source_id="sjso_news_stories"):
    """Convert RSS entries into bundle candidates (status: candidate)."""
    now = utc_now_iso()
    today_num = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    cands = []
    for i, e in enumerate(entries):
        dedupe_raw = f"{source_id}||{e['link']}"
        key = hashlib.sha256(dedupe_raw.encode()).hexdigest()[:16]
        text = (e["title"] + " " + e["description"]).lower()
        human_review = any(kw in text for kw in CRIME_REVIEW_KEYWORDS)
        cands.append({
            "item_id": f"SJC-SJSO-{today_num}-{i + 1:04d}",
            "title": e["title"],
            "summary": e["description"][:300] or e["title"],
            "source_id": source_id,
            "source_url": e["link"],
            "source_published_at": e["pub_date"] or None,
            "discovered_at": now,
            "discovered_by": "sjc-weekly-runner",
            "topics": ["public_safety", "crime"] if human_review else ["public_safety"],
            "communities": [],
            "geographic_scope": "county_wide",
            "urgency": "timely",
            "verification_status": "source_confirmed",
            "sensitivity": "medium" if human_review else "low",
            "recommended_channels": ["website_review_queue", "weekly_brief_candidate"],
            "raw_excerpt": e["description"][:300] or e["title"],
            "human_review_required": human_review,
            "status": "candidate",
            "review_status": "candidate",
            "outcome": "no_match",
            "_dedupe_key": key,
        })
    return cands


def run_sjso_monitor(ws, offline_rss):
    """Stage A monitor for sjso_news_stories via its verified RSS 2.0 feed."""
    source_id = "sjso_news_stories"
    now = utc_now_iso()
    errors = []
    try:
        xml_text, http_status = fetch_rss(offline_rss)
        health = "accessible"
    except Exception as e:
        errors.append(f"fetch failed: {e}")
        xml_text, http_status, health = None, None, "unreachable"

    cands = []
    if xml_text is not None:
        try:
            entries = parse_rss_entries(xml_text)
            cands = normalize_sjso_candidates(entries)
        except Exception as e:
            errors.append(f"parse failed: {e}")

    today_num = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    event_id = f"EVT-SJSO-{today_num}-0001"

    write_json(
        os.path.join(ws, "intel_candidates", f"{source_id}.json"),
        {"source_id": source_id, "fetched_at": now, "source_url": SJSO_FEED_URL,
         "total_items": len(cands), "items": cands},
    )
    write_json(
        os.path.join(ws, "source_events", f"{source_id}.json"),
        {"source_id": source_id, "event_id": event_id, "event_type": "rss_snapshot",
         "source_url": SJSO_FEED_URL, "status": "extracted" if not errors else "blocked",
         "extraction_status": f"{len(cands)} candidates",
         "source_health": health, "generated_at": now, "errors": errors},
    )
    write_json(
        os.path.join(ws, "source_health", f"{source_id}.json"),
        {"source_id": source_id, "checked_at": now, "http_status": http_status,
         "bytes": len(xml_text) if xml_text else 0, "health": health, "retries": 0,
         "last_error": errors[-1] if errors else None},
    )
    if xml_text is not None:
        with open(os.path.join(ws, "raw", f"{source_id}.xml"), "w") as f:
            f.write(xml_text)

    return {
        "source_id": source_id,
        "health": health,
        "http_status": http_status,
        "candidates": len(cands),
        "errors": errors,
    }


MONITORS = {
    "sjc_nbor_public_notices": run_nbor_monitor,
    "sjso_news_stories": run_sjso_monitor,
}


def build_run_log(ws, run_id, monitor_results, status):
    lines = [f"run_id={run_id} status={status}"]
    for res in monitor_results:
        lines.append(
            f"monitor={res['source_id']} health={res['health']} "
            f"http={res['http_status']} candidates={res['candidates']} "
            f"errors={len(res['errors'])}"
        )
    with open(os.path.join(ws, "logs", "run.log"), "w") as f:
        f.write("\n".join(lines) + "\n")


def write_run_json(ws, args, monitor_results, run_id, started_at, ended_at, status):
    counts = count_candidates(ws)
    failure_summary = {"total": 0, "by_source": {}, "by_reason": {}}
    for res in monitor_results:
        if res["errors"]:
            failure_summary["total"] += len(res["errors"])
            failure_summary["by_source"][res["source_id"]] = len(res["errors"])
            failure_summary["by_reason"]["fetch_or_parse"] = failure_summary["by_reason"].get(
                "fetch_or_parse", 0) + len(res["errors"])

    run = {
        "run_id": run_id,
        "run_status": status,
        "started_at": started_at,
        "ended_at": ended_at,
        "window_start": args.window_start,
        "window_end": args.window_end,
        "retention_deadline": args.retention_deadline,
        "profile_id": args.profile,
        "replay_identity": replay_identity(run_id, args.git_sha, args.registry_revision),
        "producing_git_sha": args.git_sha,
        "source_registry_revision": args.registry_revision,
        "candidate_counts": counts,
        "failure_summary": failure_summary,
        "monitors": [r["source_id"] for r in monitor_results],
        "next_check_after": (datetime.datetime.now(datetime.timezone.utc)
                             + datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write_json(os.path.join(ws, "run.json"), run)
    return run


def main():
    parser = argparse.ArgumentParser(description="Bounded local weekly runner (workspace-safe).")
    parser.add_argument("--run-id", default=None, help="e.g. SJC-WK-20260803-0001; generated if omitted.")
    parser.add_argument("--workspace-root", default=DEFAULT_WORKSPACE_ROOT)
    parser.add_argument("--monitor", action="append", default=[], dest="monitors",
                        help="Approved monitor id. Repeatable.")
    parser.add_argument("--offline-html", default=None,
                        help="NBOR HTML fixture for offline/test runs (no network).")
    parser.add_argument("--offline-rss", default=None,
                        help="SJSO RSS XML fixture for offline/test runs (no network).")
    parser.add_argument("--git-sha", required=True)
    parser.add_argument("--registry-revision", required=True)
    parser.add_argument("--window-start", required=True)
    parser.add_argument("--window-end", required=True)
    parser.add_argument("--retention-deadline", default=None)
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--bundle-out", default=None, help="Also assemble a bundle here.")
    parser.add_argument("--status", default="completed",
                        choices=["completed", "completed_partial", "failed", "aborted"])
    parser.add_argument("--force", action="store_true",
                        help="Replace an existing (failed) run workspace.")
    args = parser.parse_args()

    for m in args.monitors:
        if m not in MONITORS:
            print(f"ERROR: monitor '{m}' is not an approved monitor. "
                  f"Approved: {sorted(MONITORS)}", file=sys.stderr)
            sys.exit(2)

    run_id = args.run_id or generate_run_id(args.workspace_root)
    if not valid_run_id(run_id):
        print(f"ERROR: invalid run_id '{run_id}'", file=sys.stderr)
        sys.exit(2)

    if args.retention_deadline is None:
        end = datetime.datetime.strptime(args.window_end, "%Y-%m-%dT%H:%M:%SZ")
        end = end.replace(tzinfo=datetime.timezone.utc)
        args.retention_deadline = (end + datetime.timedelta(days=RETENTION_DAYS_DEFAULT)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")

    started_at = utc_now_iso()
    ws = make_workspace(args.workspace_root, run_id, force=args.force)
    print(f"run_id={run_id}")
    print(f"workspace={ws}")

    results = []
    for m in args.monitors:
        print(f"  running monitor: {m}")
        if m == "sjc_nbor_public_notices":
            results.append(MONITORS[m](ws, args.offline_html))
        elif m == "sjso_news_stories":
            results.append(MONITORS[m](ws, args.offline_rss))
        else:
            results.append(MONITORS[m](ws, None))

    status = args.status
    failed_monitors = [r for r in results if r["errors"]]
    if failed_monitors and status == "completed":
        status = "completed_partial"

    write_run_json(ws, args, results, run_id, started_at, utc_now_iso(), status)
    build_run_log(ws, run_id, results, status)

    print(f"run_status={status}")
    for r in results:
        print(f"  {r['source_id']}: health={r['health']} candidates={r['candidates']} "
              f"errors={len(r['errors'])}")
    print(f"run.json written to {os.path.join(ws, 'run.json')}")

    if args.bundle_out:
        bundle_dir = os.path.join(args.bundle_out, run_id)
        counts = count_candidates(ws)
        run = build_run_json(ws, args, counts)
        run["candidate_counts"] = counts
        run["producing_git_sha"] = args.git_sha
        run["producing_task_or_profile"] = args.profile
        run["source_registry_revision"] = args.registry_revision
        assemble_bundle(ws, bundle_dir, args, counts)
        write_manifest_and_checksums(bundle_dir, run, args.git_sha, args.profile,
                                     args.registry_revision)
        print(f"bundle written to {bundle_dir}")

    sys.exit(0)


if __name__ == "__main__":
    main()
