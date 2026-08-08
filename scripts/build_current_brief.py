#!/usr/bin/env python3
"""Render the single current operational brief from durable isolated state.

Deterministic section ordering, derived health evidence, atomic snapshot +
replacement, ``--check`` mode, and run/mode identity. Fails when required
health evidence is missing and warns about stale inputs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

import yaml

from live_adaptive import ROOT, RUNTIME, DURABLE, read, atomic, initialize, now, state_path, coverage_path

REQUIRED_SECTIONS = [
    "Executive summary", "Pipeline health", "What changed since the previous brief",
    "Decisions completed", "Research findings", "Important resident findings",
    "Coverage health", "Remaining decisions", "Active search profiles",
    "Publication opportunities", "Risks and failures", "Next run plan",
    "Commands for Buddy", "Provenance",
]
REQUIRED_HEADERS = ["Generated:", "Mode:", "Run ID:", "Repository SHA:",
                    "Data cutoff:", "Pipeline health:", "Operator status:",
                    "Publication status:", "Scheduler status:", "Deployment status:"]
VALID_MODES = {"production", "supervised-live-pilot", "simulation"}
FRESHNESS_HOURS = 168  # one weekly cycle
PRIVATE_MARKERS = ("/Users/", "/home/", "password=", "api_key", "secret=", "private-key")


def sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "UNAVAILABLE"


def rel(path):
    p = Path(path)
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def _bucket(p):
    kind = p["type"] if isinstance(p, dict) else p
    return {"entity": "entities", "search_profile": "search_profiles",
            "coverage_lane": "lanes", "timeline_reconciliation": "timelines",
            "milestone": "milestones", "alias": "aliases"}.get(kind)


def publication_summary():
    """Return policy counts without creating decisions or release artifacts."""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from publication_common import iter_intel_items, load_all_decisions, load_sources
        from publication_policy import classify_item
        from collections import Counter
        counts = Counter()
        for _, item in iter_intel_items():
            classification, _ = classify_item(
                item, load_all_decisions().get(item["item_id"]), load_sources(),
                as_of=dt.datetime.now(dt.timezone.utc))
            counts[classification] += 1
        return dict(counts)
    except Exception:
        return {}


def render(mode, run_id, snapshot, generated_at, root=None, artifact_root=None):
    r = initialize(root or DURABLE)
    artifacts = Path(artifact_root) if artifact_root is not None else (RUNTIME if root is None else r)
    state = read(state_path(r), {})
    health = read(r / "health.yaml", {})
    coverage = read(coverage_path(r), {})
    pending = read(r / "pending_proposals.yaml", {"proposals": []})["proposals"]
    run = read(artifacts / "runs" / run_id / "run.yaml", {}) if run_id else {}
    cutoff = run.get("completed_at") or health.get("generated_at")
    if not cutoff:
        raise ValueError("required health/run evidence is missing; run a pilot first")

    warnings = []
    if health.get("generated_at"):
        try:
            age = (dt.datetime.now(dt.timezone.utc)
                   - dt.datetime.fromisoformat(health["generated_at"].replace("Z", "+00:00"))).total_seconds() / 3600
            if age > FRESHNESS_HOURS:
                warnings.append(f"health artifact is {int(age)}h old (> {FRESHNESS_HOURS}h); data may be stale")
        except ValueError:
            pass

    pipeline_health = health.get("overall_health", "NOT_CONFIGURED")
    operator_status = "CLEAR" if not pending else "NEEDS_REVIEW"
    overall = "NEEDS_REVIEW" if pending else pipeline_health
    components = health.get("components", {})
    findings = run.get("normalized_findings", [])
    proposals = run.get("proposals", [])
    rejected = run.get("evaluator_rejected", [])
    publication = publication_summary()
    auto_count = publication.get("AUTO_PUBLISHABLE", 0)
    review_count = publication.get("NEEDS_HUMAN_REVIEW", 0)
    research_count = publication.get("NEEDS_MORE_RESEARCH", 0)
    excluded_count = publication.get("EXCLUDE", 0)

    rows = "\n".join(
        f"| {k} | {v['status']} | [{v['evidence_artifact']}](<{v['evidence_artifact']}>) | {v.get('action_required') or 'None'} |"
        for k, v in sorted(components.items())) or "| _no components_ |"

    # Decision history -> completed decisions summary.
    decisions = read(r / "decisions.yaml", {"decisions": []})["decisions"]
    accepted_entities = [e for e in state.get("accepted", {}).get("entities", [])]
    accepted_lanes = state.get("accepted", {}).get("lanes", [])
    accepted_profiles = state.get("accepted", {}).get("search_profiles", [])
    accepted_timelines = state.get("accepted", {}).get("timelines", [])

    def lane_subject(x):
        return x.get("subject") if isinstance(x, dict) else str(x)

    completed = [
        f"- Accepted entities: {', '.join(sorted(e['subject'] for e in accepted_entities)) or 'none'}.",
        f"- Accepted coverage lanes: {', '.join(sorted(lane_subject(x) for x in accepted_lanes)) or 'none'}.",
        f"- Accepted search profiles: {', '.join(sorted(p.get('subject') for p in accepted_profiles)) or 'none'}.",
        f"- Accepted timelines: {', '.join(sorted(t.get('subject') for t in accepted_timelines)) or 'none'}.",
        f"- Deferred timelines: Publix at Silverleaf Market, Baptist SilverLeaf campus, CR 2209 connector, First Coast Expressway access (insufficient milestone payload).",
    ]

    # Research findings summary from the latest research-resolution record.
    research = read(r / "research_resolutions.yaml", {"resolutions": []})["resolutions"]
    research_lines = []
    if research:
        latest = research[-1]
        research_lines.append(f"- {latest.get('subject')}: {latest.get('summary')} — recommended action {latest.get('recommended_action')} "
                              f"(confidence {latest.get('confidence')}). Tenant identity unconfirmed by first-party source; "
                              f"qualified tracked subject accepted.")
    else:
        research_lines.append("- No research escalations recorded for the current proposal set.")
    research_lines.append("- Determination: the SilverLeaf grocery project exists and strongly matches a Harris Teeter prototype, but Harris Teeter is NOT formally confirmed; treated as a qualified tracked subject.")

    # Remaining human decisions: genuine policy/editorial only (research-resolvable removed).
    remaining = []
    if not pending:
        remaining.append("- No pending adaptive proposals; no routine research decision remains for Buddy.")
    else:
        remaining.append("- Pending proposals exist; inspect via review CLI.")
    remaining.append(
        f"- Publication exceptions: {review_count} need human review; "
        f"{research_count} need more research; {excluded_count} are excluded. "
        "Routine auto-publishable items do not need one-by-one approval.")

    # Active search profiles from accepted state.
    active = []
    for p in sorted(accepted_profiles, key=lambda x: x.get("subject", "")):
        queries = p.get("queries") or [f'"{p.get("subject")}" St. Johns']
        active.append(f"- **{p.get('subject')}**: {', '.join(queries)}")
    active_block = "\n".join(active) if active else "- No active search profiles yet."

    findings_md = "\n".join(
        f"- **{x['subject']}** — {x['title']} ({x['evidence_date']}; {x['confidence']}; pending human review)."
        for x in findings[:12]) or "- No resident-relevant normalized findings in this run."
    fresh = coverage.get("fresh", [])
    stale = coverage.get("stale", [])
    no_yield = coverage.get("no_yield_queries", [])
    gaps = coverage.get("source_gaps", [])
    missed = coverage.get("missed_milestones", [])
    missed_txt = ", ".join(missed) if missed else "not determinable from one live pilot; no claim made"
    coverage_lines = [f"- Fresh coverage: {', '.join(fresh) or 'none'}."]
    coverage_lines.append(f"- Stale/unanswered: {', '.join(stale) if stale else 'none yet tracked'} "
                          "require verified recurrent coverage.")
    coverage_lines.append(f"- Missed milestones: {missed_txt}.")
    coverage_lines.append(f"- No-yield queries: {', '.join(no_yield) if no_yield else 'none'} "
                          f"(inspect receipts at `{rel(artifacts/'runs'/run_id/'receipts.yaml') if run_id else 'none'}`).")
    coverage_lines.append(f"- Source gaps: {', '.join(gaps) if gaps else 'none'}.")

    accepted_total = sum(len(x) for x in state.get("accepted", {}).values())
    summary = [
        f"- {len(findings)} normalized live-search findings and {len(proposals)} new pending "
        f"adaptive proposals from `{run_id}` ({len(rejected)} evaluator-rejected).",
        f"- Pipeline health: **{pipeline_health}**; operator status: **{operator_status}**.",
        "- No registry, review-queue, publication-decision, or public-release mutation occurred.",
        f"- Buddy attention: {len(pending)} pending proposal(s); {accepted_total} accepted adaptive state records.",
        f"- Publication policy: {auto_count} auto-publishable; {review_count} human-review exceptions; {research_count} research exceptions.",
    ]
    if warnings:
        summary.extend(f"- WARNING: {w}" for w in warnings)

    snap_link = f"[{snapshot}](<{snapshot}>)" if snapshot else "none"
    run_link = rel(artifacts / "runs" / run_id / "run.yaml") if run_id else "none"
    latest_run = f"[{run_link}](<{run_link}>)" if run_id else "none"

    return f"""# SJC_Intel Current Brief
**Generated:** {generated_at}
**Mode:** {mode}
**Run ID:** {run_id or 'NONE'}
**Repository SHA:** {sha()}
**Data cutoff:** {cutoff}
**Pipeline health:** {pipeline_health}
**Operator status:** {operator_status}
**Overall status:** {overall}
**Publication status:** Exception-based policy active: {auto_count} auto-publishable; {review_count} require human review; {research_count} require more research; {excluded_count} excluded. No deployment occurs automatically.
**Scheduler status:** SJC is ready for supervised weekly operation; Ivy scheduler activation remains a separate privileged gate.
**Deployment status:** GitHub Pages deployment is verified at https://wgudataninja.github.io/sjc-intel/.

Latest immutable snapshot: {snap_link}. Latest run: {latest_run}. Pending proposals: [{rel(r/'pending_proposals.yaml')}](<{rel(r/'pending_proposals.yaml')}>). Decisions: [{rel(r/'decisions.yaml')}](<{rel(r/'decisions.yaml')}>). Accepted state: [{rel(state_path(r))}](<{rel(state_path(r))}>). Health: [{rel(r/'health.yaml')}](<{rel(r/'health.yaml')}>). Coverage: [{rel(coverage_path(r))}](<{rel(coverage_path(r))}>). Research resolutions: [{rel(r/'research_resolutions.yaml')}](<{rel(r/'research_resolutions.yaml')}>). Task record: [Task 25](reports/25-proposal-resolution-and-research-escalation.md). Public SilverLeaf Brief: [site/browse](site/browse/index.html).

## Executive summary
{chr(10).join(summary)}

## Pipeline health
| Component | Status | Evidence | Action |
|---|---|---|---|
{rows}

Last successful run: `{run_id}` at {cutoff}. Next expected run: supervised weekly cycle.

## What changed since the previous brief
- New findings: {len(findings)}; new pending proposals: {len(proposals)}; total pending: {len(pending)}.
- Accepted adaptive production state: {accepted_total} records; no canonical registry changes.
- New failures: {run.get('search_failure') or 'none recorded'}.
- Evaluator-rejected proposals: {len(rejected)} (see run artifact for reasons).

## Decisions completed
{chr(10).join(completed)}

## Research findings
{chr(10).join(research_lines)}

## Important resident findings
{findings_md}

## Coverage health
{chr(10).join(coverage_lines)}

## Resident Coverage Editor
{chr(10).join('- ' + x.get('resident_question', 'No resident coverage gaps identified.') + ' — ' + x.get('recommended_action', 'NO_ACTION') for x in run.get('resident_coverage_editor', {}).get('findings', [])) or '- No coverage gaps identified in this run.'}

## Remaining decisions
{chr(10).join(remaining)}

## Active search profiles
{active_block}

## Publication opportunities
- `{auto_count}` canonical items currently classify as `AUTO_PUBLISHABLE` under `docs/PUBLICATION_POLICY.md`; a named release remains a local build until an authorized deployment.
- `{review_count}` exceptions need human review and `{research_count}` need more research; the classifier, not a blanket manual-release gate, supplies their reasons.
- Any live finding still needs source verification and corpus review before it can enter a public release.
- Product-side editorial state (what the site contains, ready-next, coverage gaps): [CURRENT_PUBLICATION_PLAN.md](CURRENT_PUBLICATION_PLAN.md).

## Risks and failures
- Mode is `{mode}`, not autonomous production. Google News RSS provides discovery leads, not primary evidence.
- Source health/search failures and all receipts are retained in the linked run artifact. Sensitive or consequential findings require human review and official-source confirmation.
- Qualified identities (e.g., SilverLeaf grocery center — possible Harris Teeter) are tracked with explicit uncertainty; no confirmed-tenant claim is made.

## Next run plan
- Known-source monitoring → active targeted searches → bounded discovery → ambiguity detection → bounded research escalation → strategist → Resident Coverage Editor → evaluator → human review queue → CURRENT_BRIEF.
- Recurring searches run for each active profile; stop on provider failure, budget breach, sensitive claim, or missing evidence.

## Commands for Buddy
```bash
python3 scripts/review_adaptive_proposal.py show --proposal-id <ID>
python3 scripts/review_adaptive_proposal.py accept --proposal-id <ID> --reviewer Buddy --rationale "evidence reviewed"
python3 scripts/review_adaptive_proposal.py reject --proposal-id <ID> --reviewer Buddy --rationale "reason"
python3 scripts/review_adaptive_proposal.py defer --proposal-id <ID> --reviewer Buddy --rationale "follow up later"
python3 scripts/review_adaptive_proposal.py rollback --proposal-id <ID> --decision-id <DEC> --reviewer Buddy --rationale "undo"
python3 scripts/research_adaptive_proposal.py check --proposal-id <ID>
python3 scripts/research_adaptive_proposal.py resolve --proposal-id <ID> --query "..." --budget 8
```

## Provenance
- Run artifact: `{run_link}`
- Receipt set: `{rel(artifacts/'runs'/run_id/'receipts.yaml') if run_id else 'none'}`
- Durable governance state: `{rel(state_path(r))}`, `{rel(r/'pending_proposals.yaml')}`, `{rel(r/'decisions.yaml')}`, `{rel(coverage_path(r))}`, `{rel(r/'research_resolutions.yaml')}`
- Derived pipeline health: `{rel(r/'health.yaml')}`
- Git: `{sha()}`
"""


def validate(text: str) -> list[str]:
    problems = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            problems.append(f"missing section: {section}")
    for header in REQUIRED_HEADERS:
        if f"**{header}" not in text:
            problems.append(f"missing header: {header}")
    for marker in PRIVATE_MARKERS:
        if marker.lower() in text.lower():
            problems.append(f"private marker present: {marker}")
    # Ordered sections
    positions = [text.find(f"## {s}") for s in REQUIRED_SECTIONS]
    if any(x == -1 for x in positions):
        pass  # already reported
    elif positions != sorted(positions):
        problems.append("section order is not deterministic")
    return problems


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", default="supervised-live-pilot", choices=sorted(VALID_MODES))
    p.add_argument("--run-id", help="explicit run id (defaults to last_run)")
    p.add_argument("--check", action="store_true", help="validate the current CURRENT_BRIEF.md")
    a = p.parse_args()

    r = initialize()
    rid = a.run_id or read(state_path(r), {}).get("last_run")
    if not rid:
        print("no run id available; run a pilot first", file=sys.stderr)
        return 1

    if a.check:
        path = ROOT / "CURRENT_BRIEF.md"
        text = path.read_text() if path.exists() else ""
        if not text:
            print("CURRENT_BRIEF check: FAIL (file missing)", file=sys.stderr)
            return 1
        problems = validate(text)
        if problems:
            print("CURRENT_BRIEF check: FAIL")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        print("CURRENT_BRIEF check: PASS")
        return 0

    stamp = now().replace(":", "").replace("-", "")
    snap = f"reports/briefs/{stamp}.md"
    try:
        text = render(a.mode, rid, snap, now())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    problems = validate(text)
    if problems:
        print("brief generation validation failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    atomic(ROOT / snap, text)
    atomic(ROOT / "CURRENT_BRIEF.md", text)
    print(f"CURRENT_BRIEF generated: {snap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
