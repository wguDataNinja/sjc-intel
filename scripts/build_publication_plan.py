#!/usr/bin/env python3
"""SJC_Intel — Current Publication Plan generator (Task 29).

Renders the canonical product-side editorial state document
CURRENT_PUBLICATION_PLAN.md, distinct from CURRENT_BRIEF.md (operational
health). It answers: what is on the public site, what is in Latest/Browse,
which timelines exist, which categories are strong or weak, what is ready
next, what needs source checks, what is qualified/uncertain, what is
intentionally excluded, and where coverage is sparse.

Sources:
- the latest real release artifact (site/data/releases/<latest>/release.json)
  for the published corpus (roles, categories, qualified flags);
- data/editorial/plan_inputs.yaml for human-maintained editorial inputs
  (needs source check, ready next, coverage gaps, exclusions, next-release);
- data/adaptive_discovery/accepted_state.yaml for accepted adaptive subjects
  with no corpus item (the adaptive-state-to-corpus coverage check).

Usage:
  python3 scripts/build_publication_plan.py [--check] [--out CURRENT_PUBLICATION_PLAN.md]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASES_DIR = os.path.join(REPO_ROOT, "site", "data", "releases")
PLAN_INPUTS = os.path.join(REPO_ROOT, "data", "editorial", "plan_inputs.yaml")
ACCEPTED_STATE = os.path.join(REPO_ROOT, "data", "adaptive_discovery", "accepted_state.yaml")
DEFAULT_OUT = os.path.join(REPO_ROOT, "CURRENT_PUBLICATION_PLAN.md")

CATEGORY_ORDER = ["schools_community", "roads_traffic", "local_business",
                  "utilities_water", "emergency_preparedness"]
CATEGORY_LABELS = {
    "schools_community": "Schools & Community",
    "roads_traffic": "Roads & Traffic",
    "local_business": "Local Business",
    "utilities_water": "Utilities & Water",
    "emergency_preparedness": "Emergency Preparedness",
}
ROLE_LABELS = {"latest": "Latest", "browse": "Browse", "context": "Context", "timeline": "Timeline"}
ROLE_ORDER = ["latest", "browse", "context", "timeline"]
REQUIRED_SECTIONS = [
    "Editorial summary", "Current category health", "Latest", "Browse/context",
    "Timelines", "Ready next", "Needs source check",
    "Qualified/uncertain subjects", "Intentional exclusions", "Coverage gaps",
    "Next release recommendation",
]
REQUIRED_HEADERS = ["Generated:", "Current release:", "Latest:", "Browse/context:",
                    "Timelines:", "Total unique public items:"]
PRIVATE_MARKERS = ("/Users/", "/home/", "password=", "api_key", "secret=", "private-key")


def latest_release_path():
    candidates = sorted(glob.glob(os.path.join(RELEASES_DIR, "*", "release.json")))
    if not candidates:
        return None
    return os.path.dirname(candidates[-1])


def _status(count):
    if count >= 8:
        return "STRONG"
    if count >= 4:
        return "GOOD"
    if count >= 1:
        return "THIN"
    return "MISSING"


def load_inputs():
    if not os.path.exists(PLAN_INPUTS):
        return {}
    return yaml.safe_load(open(PLAN_INPUTS)) or {}


def accepted_subjects_without_items(items, entities_map):
    """Return accepted adaptive entity subjects lacking a corpus item.

    Matches accepted subjects against corpus item titles AND the labels of the
    tracked entities those items reference (so 'CR 2209 connector' matches the
    CR 2209 item whose tracked entity label is 'CR 2209 Connector (IGP to
    SilverLeaf Parkway)').
    """
    if not os.path.exists(ACCEPTED_STATE):
        return []
    state = yaml.safe_load(open(ACCEPTED_STATE)) or {}
    entities = state.get("accepted", {}).get("entities", [])
    haystack_parts = [it.get("title", "") for it in items]
    for it in items:
        for eid in it.get("entity_ids") or []:
            haystack_parts.append(entities_map.get(eid, ""))
    haystack = " ".join(haystack_parts).lower()

    out = []
    for ent in entities:
        subject = ent.get("subject") or ""
        if not subject:
            continue
        keywords = [k for k in subject.lower().split()
                    if len(k) > 4 and k not in {"silverleaf", "center", "possible"}]
        if not keywords or any(k in haystack for k in keywords):
            continue
        out.append(subject)
    return out


def render(release):
    inputs = load_inputs()
    items = release.get("items", [])
    total = len(items)
    by_role = Counter(it.get("role", "latest") for it in items)
    latest_n = by_role.get("latest", 0)
    browse_n = by_role.get("browse", 0) + by_role.get("context", 0)
    timeline_n = by_role.get("timeline", 0)

    entities_map = {}
    try:
        ent_file = os.path.join(REPO_ROOT, "registry", "tracked_entities.yaml")
        for e in (yaml.safe_load(open(ent_file)) or {}).get("tracked_entities", []):
            if e.get("entity_id"):
                entities_map[e["entity_id"]] = e.get("label", "")
    except Exception:
        pass

    by_category = defaultdict(list)
    for it in items:
        by_category[it.get("display_topic")].append(it)

    def cat_rows():
        rows = []
        for cat in CATEGORY_ORDER:
            cat_items = by_category.get(cat, [])
            n = len(cat_items)
            subjects = ", ".join(sorted({str(it["title"])[:38] + "…"
                                         if len(str(it["title"])) > 38 else str(it["title"])
                                         for it in cat_items}))[:160]
            rows.append((cat, n, _status(n), subjects))
        return rows

    lines = []
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append("# Current Publication Plan")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Current release:** {release.get('release_id')}")
    lines.append(f"**Latest:** {latest_n}")
    lines.append(f"**Browse/context:** {browse_n}")
    lines.append(f"**Timelines:** {timeline_n}")
    lines.append(f"**Total unique public items:** {total}")
    lines.append("")
    lines.append("## 1. Editorial summary")
    for bullet in (inputs.get("editorial_summary") or
                   ["SilverLeaf Brief now publishes a full resident corpus rather than "
                    "a narrow official-news subset."]):
        lines.append(f"- {bullet}")
    lines.append("")

    lines.append("## 2. Current category health")
    lines.append("| Category | Public items | Status | Main subjects | Gap |")
    lines.append("|---|---|---|---|---|")
    for cat, n, status, subjects in cat_rows():
        gap = (inputs.get("category_gaps") or {}).get(cat, "")
        lines.append(f"| {CATEGORY_LABELS.get(cat, cat)} | {n} | {status} | {subjects} | {gap} |")
    lines.append("")

    lines.append("## 3. Latest")
    for it in items:
        if it.get("role", "latest") == "latest":
            lines.append(f"- **{it.get('title')}** — {CATEGORY_LABELS.get(it.get('display_topic'), '')} "
                         f"({it.get('source_name')}, {it.get('source_date')})")
    lines.append("")

    lines.append("## 4. Browse/context")
    lines.append("Grouped by category:")
    lines.append("")
    for cat in CATEGORY_ORDER:
        cat_items = [it for it in items
                     if it.get("display_topic") == cat and it.get("role", "latest") in ("browse", "context")]
        if not cat_items:
            continue
        lines.append(f"**{CATEGORY_LABELS.get(cat, cat)}**")
        for it in cat_items:
            role = ROLE_LABELS.get(it.get("role", "browse"), "Browse")
            q = " *(qualified)*" if it.get("qualified") else ""
            lines.append(f"- {role}: {it.get('title')}{q}")
        lines.append("")
    lines.append("")

    lines.append("## 5. Timelines")
    for it in items:
        if it.get("role") == "timeline":
            related = len(it.get("related_item_ids") or [])
            lines.append(f"- **{it.get('title')}** — {related} related milestone item(s)")
    if not any(it.get("role") == "timeline" for it in items):
        lines.append("- _No timeline items in the current release._")
    lines.append("")

    lines.append("## 6. Ready next")
    for note in (inputs.get("ready_next") or ["No further work flagged."]):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## 7. Needs source check")
    for note in (inputs.get("needs_source_check") or ["No open source checks."]):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## 8. Qualified/uncertain subjects")
    qualified = [it for it in items if it.get("qualified")]
    if qualified:
        for it in qualified:
            label = it.get("qualified_label") or "Details unconfirmed"
            lines.append(f"- **{it.get('title')}** — {label}")
    else:
        lines.append("- _No qualified subjects in the current release._")
    for note in (inputs.get("qualified_notes") or []):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## 9. Intentional exclusions")
    for note in (inputs.get("exclusions") or
                 ["Crime/arrest, minors, allegations, and private information remain "
                  "excluded or human-gated."]):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## 10. Coverage gaps")
    for note in (inputs.get("coverage_gaps") or []):
        lines.append(f"- {note}")
    subjects = accepted_subjects_without_items(items, entities_map)
    for s in subjects:
        lines.append(f"- Accepted adaptive subject with no corpus item: **{s}**.")
    lines.append("")

    lines.append("## 11. Next release recommendation")
    for note in (inputs.get("next_release") or
                 ["Review Ready-next items, resolve Needs-source-check items, then "
                  "build the next release."]):
        lines.append(f"- {note}")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def check_doc(content):
    problems = []
    for hdr in REQUIRED_HEADERS:
        if hdr not in content:
            problems.append(f"missing header: {hdr}")
    for sec in REQUIRED_SECTIONS:
        if not re.search(rf"^## \d+\. {re.escape(sec)}$", content, flags=re.M):
            problems.append(f"missing section: {sec}")
    for marker in PRIVATE_MARKERS:
        if marker in content:
            problems.append(f"private marker present: {marker}")
    return problems


def main():
    ap = argparse.ArgumentParser(description="Generate CURRENT_PUBLICATION_PLAN.md.")
    ap.add_argument("--check", action="store_true", help="validate the existing doc")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output path")
    ap.add_argument("--release-dir", default=None,
                    help="release artifact dir (default: latest real release)")
    args = ap.parse_args()

    if args.check:
        if not os.path.exists(args.out):
            print(f"CHECK FAIL: {args.out} does not exist", file=sys.stderr)
            sys.exit(1)
        content = open(args.out, encoding="utf-8").read()
        problems = check_doc(content)
        if problems:
            print("CHECK FAIL:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            sys.exit(1)
        print(f"CHECK PASS: {args.out}")
        sys.exit(0)

    release_dir = args.release_dir or latest_release_path()
    if not release_dir:
        print("ERROR: no real release found to derive the plan from", file=sys.stderr)
        sys.exit(1)
    release = yaml.safe_load(open(os.path.join(release_dir, "release.json")))
    content = render(release)
    problems = check_doc(content)
    if problems:
        print("ERROR: generated plan fails checks:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {args.out} (release {release.get('release_id')}, "
          f"{len(release.get('items', []))} items)")


if __name__ == "__main__":
    main()
