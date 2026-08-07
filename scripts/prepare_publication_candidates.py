#!/usr/bin/env python3
"""Prepare publication-readiness candidates from live findings — no mutation.

Reads the latest supervised-live-pilot run, identifies high-value subjects
against the current public release, and writes suggested titles/summaries/
why-it-matters copy to ``runtime/adaptive_discovery/publication_candidates.md``.
It never verifies, approves, publishes, or changes any review/release state.

Usage:
  python3 scripts/prepare_publication_candidates.py [--run-id <ID>]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from live_adaptive import initialize, read, now, ROOT, RUNTIME, state_path

CURRENT_RELEASE = ROOT / "site" / "fixtures" / "demo" / "release.yaml"


def current_release_subjects() -> set[str]:
    if not CURRENT_RELEASE.exists():
        return set()
    data = yaml.safe_load(CURRENT_RELEASE.read_text())
    return {item.get("title", "") for item in data.get("items", [])}


def render_candidates(run, run_id: str) -> str:
    findings = run.get("normalized_findings", [])
    release_subjects = current_release_subjects()
    groups: dict[str, list[dict]] = {}
    for f in findings:
        groups.setdefault(f["subject"], []).append(f)
    lines = [
        "# Publication-readiness candidates (prepared, NOT approved)",
        "",
        f"**Generated:** {now()}",
        f"**Run ID:** {run_id}",
        f"**Mode:** {run.get('mode', 'supervised-live-pilot')}",
        "",
        "Nothing below is verified, approved, or published. Each candidate "
        "requires source verification and explicit human approval through the "
        "existing review/release process before any public use.",
        "",
        "## Subjects surfaced by this run",
        "",
    ]
    for subject in sorted(groups):
        entries = groups[subject]
        top = entries[0]
        represented = "already represented in current release" if any(
            subject.lower() in t.lower() for t in release_subjects
        ) else "NOT represented in the current public release"
        lines.append(f"### {subject}")
        lines.append(f"- **Current release status:** {represented}")
        lines.append(f"- **Suggested title:** {subject} — recent update")
        summary = top["title"].split(" - ")[0].strip()
        lines.append(f"- **Suggested summary:** {summary} (source leads; verify before use).")
        lines.append("- **Why it matters:** Resident-relevant subject surfaced by supervised live discovery; human verification required.")
        lines.append(f"- **Relevance label:** {top.get('lane', 'unassigned')}")
        lines.append(f"- **Evidence:** {top['url']} ({top.get('evidence_date')}, {top.get('confidence')})")
        lines.append(f"- **Candidate for:** publication review, source verification, copy editing, Browse/archive or a future Latest update.")
        lines.append("- **Status:** NOT_APPROVED — preparation only.")
        lines.append("")
    lines.append("## Open items")
    lines.append("")
    lines.append("- No review status, publication decision, or release file was modified by this script.")
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-id", default=None)
    a = p.parse_args()
    r = initialize()
    rid = a.run_id or read(state_path(r), {}).get("last_run")
    if not rid:
        print("no run available; run a pilot first", file=sys.stderr)
        return 1
    run = read(RUNTIME / "runs" / rid / "run.yaml", {})
    if not run:
        print(f"run {rid} not found", file=sys.stderr)
        return 1
    text = render_candidates(run, rid)
    out = RUNTIME / "publication_candidates.md"
    out.write_text(text)
    print(f"publication candidates written: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
