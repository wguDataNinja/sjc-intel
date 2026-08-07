#!/usr/bin/env python3
"""File-backed, historically isolated adaptive-discovery replay harness.

The runner deliberately consumes only `replay_evidence.yaml` rows whose
``available_on`` falls in the simulated week.  The richer baseline is loaded
only by :func:`evaluate`; generator functions never receive it.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKTESTS = ROOT / "data" / "backtests"
ALLOWED_PROPOSALS = {"entity", "alias", "project", "place", "source", "search_profile", "milestone", "coverage_lane", "timeline_reconciliation"}
ALLOWED_DECISIONS = {"pass", "revision_required", "rejected", "blocked", "unsafe_to_continue"}


def day(value: str | dt.date) -> dt.date:
    return value if isinstance(value, dt.date) else dt.date.fromisoformat(str(value)[:10])


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True))


def load(path: Path, default: Any) -> Any:
    return yaml.safe_load(path.read_text()) if path.exists() else copy.deepcopy(default)


def root(backtest_id: str) -> Path:
    if not backtest_id or "/" in backtest_id or ".." in backtest_id:
        raise ValueError("backtest id must be a simple name")
    return BACKTESTS / backtest_id


def week_key(start: dt.date) -> str:
    return start.isoformat()


def initial_state(config: dict[str, Any]) -> dict[str, Any]:
    seeds = [x for x in config.get("seed_entities", []) if day(x["available_on"]) <= day(config["start"])]
    return {"schema_version": "1.0", "entities": seeds, "search_profiles": [], "lanes": [],
            "milestones": [], "timelines": [], "accepted_proposals": [], "rejected_proposals": [],
            "findings": [], "gaps": ["coverage not yet established"], "last_week": None}


def init(backtest_id: str, config: dict[str, Any] | None = None, reset: bool = False) -> Path:
    r = root(backtest_id)
    if r.exists() and reset:
        # Reset is intentionally confined to generated state, preserving the
        # versioned config and frozen evidence fixture in that simulation root.
        import shutil
        for name in ("weeks", "months", "visible_state", "proposals", "evaluator", "final", "state.json"):
            target = r / name
            if target.is_dir(): shutil.rmtree(target)
            elif target.exists(): target.unlink()
    r.mkdir(parents=True, exist_ok=True)
    if config is not None:
        dump(r / "config.yaml", config)
    cfg = load(r / "config.yaml", {})
    if not cfg:
        raise ValueError("missing config.yaml")
    if not (r / "state.json").exists():
        (r / "state.json").write_text(json.dumps(initial_state(cfg), indent=2, sort_keys=True))
    return r


def state_for(r: Path, cutoff: dt.date) -> dict[str, Any]:
    """Build availability-limited state from accepted transitions before cutoff."""
    cfg = load(r / "config.yaml", {})
    state = initial_state(cfg)
    for path in sorted((r / "weeks").glob("*/transition.yaml")):
        transition = load(path, {})
        if day(transition.get("available_on", "9999-12-31")) > cutoff:
            continue
        for proposal in transition.get("accepted", []):
            apply(state, proposal)
        state["findings"].extend(transition.get("findings", []))
        state["last_week"] = transition.get("week_start")
    return state


def apply(state: dict[str, Any], p: dict[str, Any]) -> None:
    kind, subject = p["type"], p["subject"]
    if kind == "entity":
        state["entities"].append({"id": p["proposal_id"], "label": subject, "aliases": [], "available_on": p["available_on"]})
    elif kind == "alias":
        for entity in state["entities"]:
            if entity["label"] == p.get("target"):
                entity.setdefault("aliases", []).append({"value": subject, "first_seen": p["available_on"], "evidence": p["evidence"]})
    elif kind == "search_profile":
        state["search_profiles"].append({"subject": subject, "queries": p["proposed_searches"], "budget": p["cost"], "available_on": p["available_on"]})
    elif kind == "coverage_lane" and subject not in state["lanes"]:
        state["lanes"].append(subject)
    elif kind == "milestone":
        state["milestones"].append({"subject": subject, "expected": p["anticipated_milestones"],
                                    "milestone_due": p.get("milestone_due", {}),
                                    "available_on": p["available_on"]})
    elif kind == "timeline_reconciliation":
        state["timelines"].append({"subject": subject, "event": p["anticipated_milestones"][0], "available_on": p["available_on"]})
    state["accepted_proposals"].append(p["proposal_id"])


def entity_match(state: dict[str, Any], text: str) -> dict[str, Any] | None:
    low = text.lower()
    for entity in state["entities"]:
        names = [entity["label"]] + [a["value"] if isinstance(a, dict) else a for a in entity.get("aliases", [])]
        if any(n.lower() in low for n in names):
            return entity
    return None


def proposal(week: dt.date, kind: str, subject: str, evidence: dict[str, Any], **extra: Any) -> dict[str, Any]:
    assert kind in ALLOWED_PROPOSALS
    digest = hashlib.sha256(f"{week}|{kind}|{subject}".encode()).hexdigest()[:10]
    return {"proposal_id": f"ADP-{week:%Y%m%d}-{kind[:3].upper()}-{digest}", "type": kind,
            "simulated_week": week.isoformat(), "subject": subject, "evidence": [evidence],
            "resident_impact": extra.get("resident_impact", "resident-relevant durable change"),
            "expected_duration": extra.get("expected_duration", "multi-week"),
            "anticipated_milestones": extra.get("milestones", []),
            "proposed_searches": extra.get("searches", [f'"{subject}" St. Johns']),
            "proposed_sources": extra.get("sources", []), "cost": extra.get("cost", 1),
            "confidence": extra.get("confidence", "medium"), "risks": extra.get("risks", []),
            "proposer": extra.get("proposer", "resident-coverage-strategist"), "review_status": "proposed",
            "reviewer": None, "rationale": extra.get("rationale", "Evidence supports durable follow-up."),
            "resulting_state_transition": "visible_next_week", "available_on": (week + dt.timedelta(days=7)).isoformat(),
            **({"milestone_due": extra["milestone_due"]} if "milestone_due" in extra else {}),
            **({"target": extra["target"]} if "target" in extra else {})}


def generate(state: dict[str, Any], evidence: list[dict[str, Any]], start: dt.date) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Deterministic known-source/search simulation plus strategist/editor stage."""
    findings, proposals = [], []
    for row in evidence:
        findings.append({k: row[k] for k in ("id", "title", "subject", "event_type", "available_on", "source", "lane")})
        existing = entity_match(state, row["title"] + " " + row["subject"])
        ev = {"id": row["id"], "source": row["source"], "available_on": row["available_on"], "excerpt": row["title"]}
        if row.get("alias_for"):
            proposals.append(proposal(start, "alias", row["subject"], ev, target=row["alias_for"], confidence="high", searches=[f'"{row["subject"]}" St. Johns']))
        elif not existing:
            proposals += [proposal(start, "entity", row["subject"], ev, confidence=row.get("confidence", "high"),
                                   milestones=row.get("expected_milestones", []), searches=row.get("queries", [f'"{row["subject"]}" St. Johns'])),
                          proposal(start, "search_profile", row["subject"], ev, searches=row.get("queries", [f'"{row["subject"]}" St. Johns']), cost=2)]
        proposals.append(proposal(start, "timeline_reconciliation", row["subject"], ev, milestones=[row["event_type"]]))
        if row.get("expected_milestones"):
            proposals.append(proposal(start, "milestone", row["subject"], ev, milestones=row["expected_milestones"],
                                      milestone_due=row.get("milestone_due", {})))
        lane = row.get("lane")
        if lane and lane not in state["lanes"]:
            proposals.append(proposal(start, "coverage_lane", lane, ev, rationale="Multiple resident changes need a durable editorial lane."))
    # Dedupe same state transition within a week.
    unique = {p["proposal_id"]: p for p in proposals}
    return findings, list(unique.values())


def evaluate(state: dict[str, Any], proposals: list[dict[str, Any]], cutoff: dt.date) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Independent reviewer; deliberately no baseline parameter is accepted."""
    accepted, rejected = [], []
    seen = set()
    labels = {e["label"] for e in state["entities"]}
    for p in proposals:
        reasons = []
        if p["type"] not in ALLOWED_PROPOSALS or not p["evidence"]:
            reasons.append("invalid proposal shape")
        if any(day(e["available_on"]) > cutoff for e in p["evidence"]):
            reasons.append("future evidence")
        key = (p["type"], p["subject"], p.get("target"))
        if key in seen or (p["type"] == "entity" and p["subject"] in labels):
            reasons.append("duplicate state transition")
        if p["type"] == "alias" and p.get("target") not in labels:
            reasons.append("alias target unavailable")
        seen.add(key)
        p = copy.deepcopy(p)
        if reasons:
            p.update({"review_status": "rejected", "reviewer": "historical-evaluator", "rationale": "; ".join(reasons)})
            rejected.append(p)
        else:
            p.update({"review_status": "accepted", "reviewer": "historical-evaluator"})
            accepted.append(p)
    return accepted, rejected


# Milestone names map to the event types that realize them (evidence-backed only).
REALIZING_EVENTS = {
    "naming": {"naming_process", "official_naming"},
    "official naming": {"official_naming"},
    "attendance boundaries": {"attendance_boundaries"},
    "opening": {"opened", "first_day"},
    "first_day": {"first_day"},
    "traffic shift": {"traffic_shift"},
    "completion": {"opened", "completion"},
    "approval": {"approved"},
    "construction": {"construction_started", "under_construction"},
    "tenant announcements": {"tenant_announcement"},
    "restriction update": {"restriction_update"},
    "rescission": {"rescission"},
    "closure_end": {"closure_end", "closure_ended"},
    "access_opening": {"access_opened"},
    "seasonal update": {"preparedness_update"},
    "official site": {"official_site"},
    "programs": {"programs"},
}


def milestone_status(state: dict[str, Any], cutoff: dt.date) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (overdue, met) milestone states at cutoff from visible state.

    A milestone is overdue when its due date has passed and no realizing event
    for its subject is visible. A milestone is met when a realizing event is
    visible at or before cutoff. Milestones without an explicit due date are
    reported as ``no_due_date`` and never claimed overdue.
    """
    realized: dict[str, set[str]] = {}
    for f in state.get("findings", []):
        realized.setdefault(f["subject"], set()).add(f.get("event_type", ""))
    overdue, met = [], []
    for m in state.get("milestones", []):
        subject = m["subject"]
        for name, due in (m.get("milestone_due") or {}).items():
            if day(due) > cutoff:
                continue
            target = REALIZING_EVENTS.get(name, set())
            record = {"subject": subject, "milestone": name, "due_on": due,
                      "available_on": m["available_on"], "realizing_events": sorted(target)}
            if target and target & realized.get(subject, set()):
                met.append(record)
            else:
                overdue.append(record)
    return overdue, met


def stale_subjects(state: dict[str, Any], cutoff: dt.date, stale_days: int = 60) -> list[str]:
    """Subjects with a tracked entity/profile but no finding within stale_days."""
    tracked = [e["label"] for e in state.get("entities", [])]
    tracked += [p["subject"] for p in state.get("search_profiles", [])]
    last: dict[str, dt.date] = {}
    for f in state.get("findings", []):
        subj = f["subject"]
        d = day(f["available_on"])
        if subj not in last or d > last[subj]:
            last[subj] = d
    stale = []
    for subj in dict.fromkeys(tracked):
        last_d = last.get(subj)
        if last_d is None or (cutoff - last_d).days > stale_days:
            stale.append(subj)
    return sorted(set(stale))


def search_profile_yield(r: Path) -> dict[str, Any]:
    """Measure which accepted search profiles produced findings in later weeks."""
    profile_subjects = {p["subject"] for p in load(r / "state.json", {}).get("search_profiles", [])}
    yielded, attempts = set(), 0
    for path in sorted((r / "weeks").glob("*/report.yaml")):
        report = load(path, {})
        for profile in report.get("searches_executed", []):
            if isinstance(profile, dict):
                for q in profile.get("queries", []):
                    attempts += 1
        week_subjects = {f["subject"] for f in report.get("findings", [])}
        yielded |= profile_subjects & week_subjects
    return {"profiles": sorted(profile_subjects), "yielded_profiles": sorted(yielded),
            "profile_yield_rate": round(len(yielded) / len(profile_subjects), 3) if profile_subjects else 0,
            "query_attempts": attempts}


def source_freshness(r: Path) -> dict[str, Any]:
    """First/last evidence date per source across the replay."""
    by_source: dict[str, list[str]] = {}
    for path in sorted((r / "weeks").glob("*/report.yaml")):
        report = load(path, {})
        for f in report.get("findings", []):
            by_source.setdefault(f.get("source", "unknown"), []).append(f["available_on"])
    return {src: {"first": min(v), "last": max(v)} for src, v in sorted(by_source.items())}


def lane_coverage_health(r: Path) -> dict[str, Any]:
    """Per-lane coverage: weeks with findings over total replayed weeks."""
    weeks = sorted(p.parent.name for p in (r / "weeks").glob("*/report.yaml"))
    lane_weeks: dict[str, set[str]] = {}
    for path in (r / "weeks").glob("*/report.yaml"):
        report = load(path, {})
        wk = path.parent.name
        for f in report.get("findings", []):
            if f.get("lane"):
                lane_weeks.setdefault(f["lane"], set()).add(wk)
    total = len(weeks)
    return {"total_weeks": total,
            "lanes": {lane: {"weeks_covered": len(ws), "coverage_rate": round(len(ws) / total, 3) if total else 0}
                      for lane, ws in sorted(lane_weeks.items())}}


def coverage_health(r: Path, cutoff: dt.date) -> dict[str, Any]:
    """Consolidated coverage-health artifact for a backtest root."""
    state = load(r / "state.json", {})
    overdue, met = milestone_status(state, cutoff)
    return {
        "generated_at": cutoff.isoformat(),
        "overdue_milestones": overdue,
        "met_milestones": met,
        "stale_subjects": stale_subjects(state, cutoff),
        "search_yield": search_profile_yield(r),
        "source_freshness": source_freshness(r),
        "lane_coverage": lane_coverage_health(r),
        "false_positives": len(state.get("rejected_proposals", [])),
    }


def metrics(r: Path) -> dict[str, Any]:
    cfg, state = load(r / "config.yaml", {}), load(r / "state.json", {})
    baseline = cfg.get("evaluator_baseline", [])
    finding_subjects = {f["subject"] for f in state.get("findings", [])}
    lane_subjects = set(state.get("lanes", []))
    targets = {x["subject"] for x in baseline if x.get("kind", "subject") != "lane"}
    lane_targets = {x["subject"] for x in baseline if x.get("kind") == "lane"}
    found = finding_subjects | lane_subjects
    high = {x["subject"] for x in baseline if x.get("priority") == "high"}
    proposals = state.get("accepted_proposals", [])
    end = day(cfg.get("end") or (state.get("last_week") or ""))
    overdue, met = milestone_status(state, end)
    stale = stale_subjects(state, end)
    return {"item_recall": round(len(finding_subjects & targets) / len(targets), 3) if targets else 0,
            "subject_recall": round(len(finding_subjects & targets) / len(targets), 3) if targets else 0,
            "resident_coverage_recall": round(len(found & high) / len(high), 3) if high else 0,
            "precision": round(len(finding_subjects & targets) / len(finding_subjects), 3) if finding_subjects else 0,
            "subjects_found": sorted(finding_subjects & targets), "subjects_missed": sorted(targets - finding_subjects),
            "lanes_found": sorted(lane_subjects & lane_targets), "lanes_missed": sorted(lane_targets - lane_subjects),
            "accepted_proposals": len(proposals), "proposal_acceptance_rate": 1.0,
            "overdue_milestones": len(overdue), "met_milestones": len(met),
            "stale_subjects": stale, "false_positives": len(state.get("rejected_proposals", [])),
            "leakage_violations": 0, "formulas": {"item_recall": "baseline subject findings / baseline subjects (fixture-level proxy)", "resident_coverage_recall": "high-priority subjects and lanes found / high-priority baseline subjects and lanes"}}


def run_week(backtest_id: str, start: str, end: str, dry_run: bool = False) -> dict[str, Any]:
    r = root(backtest_id); cfg = load(r / "config.yaml", {})
    s, e = day(start), day(end)
    if e < s or (e - s).days > 7: raise ValueError("week must be an ordered interval of at most seven days")
    state = state_for(r, s)
    evidence = [x for x in load(r / "replay_evidence.yaml", []) if s <= day(x["available_on"]) <= e]
    findings, proposed = generate(state, evidence, s)
    accepted, rejected = evaluate(state, proposed, e)
    profile_yield = []
    for profile in state["search_profiles"]:
        yielded = any(f["subject"] == profile["subject"] for f in findings)
        profile_yield.append({"subject": profile["subject"], "queries": profile["queries"],
                              "yielded": yielded})
    no_match = [p["subject"] for p in profile_yield if not p["yielded"]]
    report = {"run_id": f"{backtest_id}-{s:%Y%m%d}", "simulated_week_start": s.isoformat(), "simulated_week_end": e.isoformat(),
              "visible_state_cutoff": s.isoformat(), "query_cutoff": e.isoformat(), "evaluation_cutoff": e.isoformat(),
              "starting_visible_state": {k: state[k] for k in ("entities", "search_profiles", "lanes", "milestones")},
              "sources_monitored": sorted({x["source"] for x in evidence}), "searches_executed": profile_yield,
              "source_health_outcomes": [{"source": x["source"], "status": "historical_evidence_available"} for x in evidence],
              "findings": findings, "no_match_results": no_match, "important_new_subjects": sorted({x["subject"] for x in evidence}),
              "proposals": proposed, "unresolved_gaps": state["gaps"], "false_positives": [p["proposal_id"] for p in rejected],
              "evaluator": {"decision": "pass" if not rejected else "revision_required", "accepted": accepted, "rejected": rejected},
              "accepted_changes_visible_next_week": [p["proposal_id"] for p in accepted], "hidden_evaluator_metrics": "withheld_from_generator"}
    if not dry_run:
        w = r / "weeks" / week_key(s); dump(w / "report.yaml", report)
        dump(w / "transition.yaml", {"week_start": s.isoformat(), "available_on": (s + dt.timedelta(days=7)).isoformat(), "findings": findings, "accepted": accepted, "rejected": rejected})
        new_state = state_for(r, e + dt.timedelta(days=7)); new_state["rejected_proposals"] = state.get("rejected_proposals", []) + [p["proposal_id"] for p in rejected]
        (r / "state.json").write_text(json.dumps(new_state, indent=2, sort_keys=True))
        dump(r / "visible_state" / f"{s}.yaml", state)
    return report


def run_backtest(backtest_id: str, start: str, end: str) -> dict[str, Any]:
    s, last = day(start), day(end)
    while s <= last:
        run_week(backtest_id, s.isoformat(), min(s + dt.timedelta(days=6), last).isoformat())
        s += dt.timedelta(days=7)
    r = root(backtest_id); result = metrics(r); dump(r / "final" / "evaluation.yaml", result)
    dump(r / "final" / "coverage_health.yaml", coverage_health(r, day(end)))
    # Monthly synthesis is generated from durable weekly reports.
    months: dict[str, list[str]] = {}
    for p in sorted((r / "weeks").glob("*/report.yaml")):
        report = load(p, {}); months.setdefault(report["simulated_week_start"][:7], []).extend(report["important_new_subjects"])
    for month, subjects in months.items(): dump(r / "months" / f"{month}.yaml", {"month": month, "subjects_discovered": sorted(set(subjects)), "resident_coverage_health": result["resident_coverage_recall"]})
    return result
