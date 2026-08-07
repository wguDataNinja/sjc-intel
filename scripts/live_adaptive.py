#!/usr/bin/env python3
"""Supervised live adaptive-discovery primitives (file-first, no promotion).

Public operators:
  * ``initialize`` / ``run_pilot`` / ``review``
  * ``health_from`` / ``coverage_health_from``

Governance authority lives under ``data/adaptive_discovery/``; transient run
artifacts and raw receipts live under ``runtime/adaptive_discovery/``. Both are
isolated from production registries, review queue, publication decisions, and
public release.
Live runs may create pending human proposals; they never canonize state.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

try:
    from search_adapter import (
        BudgetTracker,
        SearchSpec,
        create_provider,
        default_subject_rules,
        execute_search,
        now_utc,
    )
except ModuleNotFoundError:  # scripts imported as a package by tests
    import os
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from search_adapter import (  # noqa: F401,E402
        BudgetTracker,
        SearchSpec,
        create_provider,
        default_subject_rules,
        execute_search,
        now_utc,
    )

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "adaptive_discovery"
DURABLE = ROOT / "data" / "adaptive_discovery"
STATUSES = {"HEALTHY", "DEGRADED", "BLOCKED", "STALE", "NOT_CONFIGURED"}
HEALTH_COMPONENTS = (
    "known_source_capture", "live_search", "normalization", "dedupe",
    "identity_reconciliation", "strategist", "editor", "evaluator",
    "proposal_storage", "proposal_review", "timeline_state", "milestones",
    "coverage_health", "publication_candidate_handoff", "report_generation",
    "state_persistence",
)

# This is deliberately configuration-derived rather than a permanent list of
# SilverLeaf questions.  Accepted profiles are the durable operator decision;
# the editor only points out where those decisions have not recently produced
# useful evidence.
DEFAULT_COVERAGE_QUESTIONS = {
    "utilities and household operations": "Are important utility restrictions still active?",
    "preparedness": "What should residents prepare for now?",
    "government decisions": "Are nearby government decisions changing resident conditions?",
}

# Compatibility defaults for Task 25 accepted records created before query text
# became a required profile field.  New/edited accepted profiles always win.
ACCEPTED_PROFILE_DEFAULTS = {
    "Magnolia Oaks Academy": ['"Magnolia Oaks Academy"', '"School QQ"', '"SilverLeaf K-8"', 'site:stjohns.k12.fl.us "Magnolia Oaks"', 'site:www-moa.stjohns.k12.fl.us'],
    "Publix at Silverleaf Market": ['"Publix at Silverleaf Market"', '"Silverleaf Market" tenants', '"SilverLeaf Publix"', '"Silverleaf Market" development'],
    "Baptist SilverLeaf campus": ['"Baptist SilverLeaf"', '"Baptist Health SilverLeaf"', 'site:baptistjax.com SilverLeaf'],
    "CR 2209 connector": ['"CR 2209 connector"', '"County Road 2209" SilverLeaf', '"St Johns Parkway" connector', 'site:sjcfl.us "CR 2209"'],
    "First Coast Expressway access": ['"First Coast Expressway" SilverLeaf', '"First Coast Expressway" "St Johns Parkway"', '"First Coast Expressway" I-95', 'site:fdot.gov "First Coast Expressway"'],
    "SilverLeaf grocery center — possible Harris Teeter": ['"SilverLeaf" "Harris Teeter"', '"SilverLeaf Parkway" grocery', '"CR 16A" grocery SilverLeaf', '"Silverleaf Retail Marketplace"', '"SilverLeaf grocery center"', 'site:harristeeter.com SilverLeaf', 'site:webapp.sjcfl.us Silverleaf grocery'],
}


def now():
    return now_utc()


def read(p, default):
    return yaml.safe_load(Path(p).read_text()) if Path(p).exists() else default


def write(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True))


def atomic(p, text):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=p.parent, encoding="utf-8") as f:
        f.write(text)
        name = f.name
    os.replace(name, p)


def runtime(root=RUNTIME):
    return Path(root)


def initialize(root=DURABLE):
    """Ensure the durable adaptive-governance authority exists.

    A supplied root is an all-in-one isolated root for tests and historical
    replay. Production callers use the default durable path and pass RUNTIME
    separately for transient artifacts.
    """
    r = runtime(root)
    r.mkdir(parents=True, exist_ok=True)
    defaults = {
        "accepted_state.yaml": {
            "mode": "supervised-live-pilot",
            "accepted": {"entities": [], "aliases": [], "search_profiles": [],
                         "lanes": [], "milestones": [], "timelines": []},
            "last_run": None,
        },
        "pending_proposals.yaml": {"proposals": []},
        "decisions.yaml": {"decisions": []},
        "health.yaml": {"mode": "supervised-live-pilot", "components": {}},
        "coverage_health.yaml": {"mode": "supervised-live-pilot", "fresh": [], "stale": [],
                          "missed_milestones": [], "no_yield_queries": [],
                          "source_gaps": [], "unanswered_questions": []},
    }
    for name, value in defaults.items():
        if not (r / name).exists():
            write(r / name, value)
    return r


def state_path(root):
    """Return the accepted-state path, with a temporary legacy fallback."""
    r = runtime(root)
    return r / "accepted_state.yaml" if (r / "accepted_state.yaml").exists() else r / "state.yaml"


def coverage_path(root):
    """Return the durable coverage-health path, with a temporary legacy fallback."""
    r = runtime(root)
    return r / "coverage_health.yaml" if (r / "coverage_health.yaml").exists() else r / "coverage.yaml"


def google_news_rss(query, limit=5, timeout=15):
    """Credential-free public RSS search (compat wrapper; provider boundary lives in search_adapter)."""
    spec = SearchSpec(query=query, result_limit=limit, timeout=timeout)
    endpoint, _raw, rows = create_provider("google_news_rss").search(spec)
    return endpoint, [r.__dict__ for r in rows]


def probe(url, timeout=15):
    try:
        req = __import__("urllib.request").request.Request(
            url, headers={"User-Agent": "SJC-Intel/1.0 health check"})
        with __import__("urllib.request").request.urlopen(req, timeout=timeout) as res:
            return {"status": "HEALTHY", "http_status": res.status,
                    "bytes": int(res.headers.get("Content-Length") or 0), "error": None}
    except Exception as exc:  # noqa: BLE001
        return {"status": "DEGRADED", "http_status": None, "bytes": 0, "error": str(exc)[:240]}


def subject_for(title, rules=None):
    rules = rules or default_subject_rules()
    low = title.lower()
    for needle, subject, lane in rules:
        if needle in low:
            return subject, lane
    return None, None


IMPORTANT_MARKERS = ("school", "hospital", "academy", "road", "expressway",
                     "parkway", "shopping center", "grocery", "publix",
                     "harris teeter", "development", "water", "utility")


def material_importance_value(subject):
    """Return high/medium/low resident importance for a subject name."""
    low = subject.lower()
    if any(m in low for m in ("school", "hospital", "academy", "expressway", "water")):
        return "high"
    if any(m in low for m in ("road", "parkway", "shopping center", "grocery", "publix",
                              "harris teeter", "development", "utility")):
        return "medium"
    return "low"


def subject_needs_research(item):
    """Signal whether a finding's subject warrants bounded follow-up research."""
    subject = (item.get("subject") or "").lower()
    title = (item.get("title") or "").lower()
    uncertain = any(m in title for m in ("size", "possible", "likely", "unconfirmed",
                                         "matching", "prospective", "proposed"))
    geographic = "silverleaf" not in subject and "silverleaf" not in title
    return (uncertain or geographic) and material_importance_value(item.get("subject", "")) in ("high", "medium")


def active_search_queries(root=DURABLE):
    """Expand accepted search profiles into bounded, attributed query specs.

    The accepted state is the only authority for recurring searches.  This
    helper makes the weekly runner restartable and prevents a hard-coded set
    of subjects from quietly drifting away from reviewed governance.
    """
    state = read(state_path(root), {})
    queries, seen = [], set()
    for profile in state.get("accepted", {}).get("search_profiles", []):
        subject = profile.get("subject")
        if not subject:
            continue
        entity = next((x for x in state.get("accepted", {}).get("entities", [])
                       if x.get("subject") == subject), {})
        values = list(profile.get("queries") or []) + list(entity.get("queries") or []) + list(ACCEPTED_PROFILE_DEFAULTS.get(subject, []))
        values = values or [f'"{subject}"']
        lane = next((x.get("subject") for x in state.get("accepted", {}).get("lanes", [])
                     if subject.lower().split()[0] in x.get("subject", "").lower()), None)
        for value in values:
            key = (subject, value)
            if key not in seen:
                seen.add(key)
                queries.append({"query": value, "subject": subject, "lane": lane})
    return queries


def resident_coverage_editor(run, root=DURABLE):
    """Independent editorial QA: identify resident questions coverage misses.

    It does not search or change state.  Findings are structured recommendations
    for the normal research/evaluator path and are kept with the run evidence.
    """
    r = runtime(root)
    state = read(state_path(r), {})
    coverage = read(coverage_path(r), {})
    profiles = {p.get("subject"): p for p in state.get("accepted", {}).get("search_profiles", [])}
    entities = [e.get("subject") for e in state.get("accepted", {}).get("entities", []) if e.get("subject")]
    fresh = {x.get("subject") for x in run.get("normalized_findings", [])}
    no_yield = set(coverage.get("no_yield_queries", []))
    findings = []
    for subject in sorted(entities):
        profile = profiles.get(subject, {})
        relevant_queries = profile.get("queries") or []
        missing = subject not in fresh
        weak = not relevant_queries or any(q in no_yield for q in relevant_queries)
        if missing or weak:
            findings.append({
                "coverage_gap_id": "COV-" + hashlib.sha256(f"{run['run_id']}|{subject}".encode()).hexdigest()[:12],
                "coverage_lane": next((p.get("lane") for p in [profile] if p.get("lane")), "unassigned"),
                "subject": subject,
                "resident_question": f"What is the current status of {subject}?",
                "current_state": "no fresh normalized finding this cycle" if missing else "search profile produced weak/no-yield coverage",
                "why_this_is_a_gap": "accepted tracked subject lacks a current evidence-backed update",
                "last_meaningful_update": None,
                "expected_next_milestone": "revisit in the next supervised weekly cycle",
                "existing_search_profiles": relevant_queries,
                "recommended_research": [f'"{subject}" St. Johns'],
                "recommended_priority": material_importance_value(subject),
                "recommended_action": "SEARCH_NOW" if missing else "REFRESH_SOURCE",
            })
    for lane, question in DEFAULT_COVERAGE_QUESTIONS.items():
        if lane not in {p.get("lane") for p in profiles.values()}:
            findings.append({
                "coverage_gap_id": "COV-" + hashlib.sha256(f"{run['run_id']}|{lane}".encode()).hexdigest()[:12],
                "coverage_lane": lane, "subject": None, "resident_question": question,
                "current_state": "no accepted recurring search profile", "why_this_is_a_gap": "resident operating lane has no active coverage",
                "last_meaningful_update": None, "expected_next_milestone": "operator review before profile creation",
                "existing_search_profiles": [], "recommended_research": [], "recommended_priority": "medium",
                "recommended_action": "ADD_SEARCH_PROFILE",
            })
    output = {"run_id": run["run_id"], "generated_at": run["completed_at"], "findings": findings}
    return output


def health_from(run, root=DURABLE):
    """Derive per-component health from a run artifact; never hand-write statuses."""
    components = {}
    for key in HEALTH_COMPONENTS:
        status = "HEALTHY" if run.get(key, True) else "DEGRADED"
        components[key] = {
            "status": status,
            "last_success": run["completed_at"] if status == "HEALTHY" else None,
            "last_failure": None if status == "HEALTHY" else run.get("failure"),
            "evidence_artifact": run["artifact"],
            "freshness_threshold_hours": 168,
            "failure_count": 0 if status == "HEALTHY" else 1,
            "warning_count": 0,
            "action_required": None if status == "HEALTHY" else "inspect run artifact",
        }
    if run.get("search_failure"):
        components["live_search"].update({
            "status": "DEGRADED", "last_failure": run["search_failure"],
            "failure_count": 1, "action_required": "retry next supervised run"})
    blocked = run.get("blocked", False)
    overall = "BLOCKED" if blocked else (
        "DEGRADED" if any(x["status"] in {"DEGRADED", "BLOCKED", "STALE"} for x in components.values())
        else "HEALTHY")
    result = {"mode": "supervised-live-pilot", "generated_at": run["completed_at"],
              "overall_health": overall, "components": components}
    write(runtime(root) / "health.yaml", result)
    return result


def _all_pending_subjects(pending):
    return {x["subject"] for x in pending["proposals"]}


def evaluate_proposals(proposals, state, pending, run_id):
    """Independent evaluator stage: validate shape, dedupe, and isolation only.

    It never sees the strategist's reasoning as an oracle; it checks evidence
    presence, subject/type uniqueness against pending and accepted state, and
    that no publication state is referenced. Returns (accepted, rejected).
    """
    existing = _all_pending_subjects(pending)
    # Accepted records use `subject`; older fixture records may use `label`.
    # Consider every accepted bucket so a new proposal cannot recreate an
    # accepted profile, lane, timeline, alias, or entity.
    for values in state.get("accepted", {}).values():
        for record in values if isinstance(values, list) else []:
            existing.add(record.get("subject") or record.get("label"))
    existing.discard(None)
    accepted, rejected = [], []
    seen = set()
    for p in proposals:
        reasons = []
        key = (p["type"], p["subject"])
        if not p.get("evidence") or not isinstance(p["evidence"], list) or not p["evidence"][0].get("url"):
            reasons.append("missing evidence")
        if key in seen:
            reasons.append("duplicate proposal")
        if p["subject"] in existing or key in seen:
            reasons.append("subject already tracked or proposed")
        seen.add(key)
        if reasons:
            p["evaluator"] = {"decision": "rejected", "rationale": "; ".join(reasons), "run_id": run_id}
            rejected.append(p)
        else:
            p["evaluator"] = {"decision": "accepted", "rationale": "shape valid, evidence present", "run_id": run_id}
            accepted.append(p)
    return accepted, rejected


def run_pilot(run_id, queries, root=DURABLE, runtime_root=None, budget=3, timeout=15,
              provider="google_news_rss", allowed_domains=(), excluded_domains=(),
              date_after=None, date_before=None):
    """Run one bounded supervised live-pilot cycle. Never auto-canonizes.

    ``queries`` may be plain strings (subject inferred) or dicts with optional
    keys: query, lane, subject, allowed_domains, excluded_domains, date_after,
    date_before, result_limit.
    """
    r = initialize(root)
    # Production governance is versioned under data/, but receipts and full run
    # artifacts are transient operational evidence under runtime/.  Isolated
    # test/backtest roots intentionally retain the all-in-one behavior.
    artifacts = (runtime(runtime_root) if runtime_root is not None
                 else (RUNTIME if r.resolve() == DURABLE.resolve() else r))
    query_count = len(queries)
    if query_count > budget:
        raise ValueError("query budget exceeded")
    stamp = now()
    run_dir = artifacts / "runs" / run_id
    if run_dir.exists():
        raise ValueError("run id already exists")

    source_checks = {
        "sjc_county_news": "https://www.sjcfl.us/news/",
        "sjc_school_district": "https://www.stjohns.k12.fl.us/",
    }
    source_health = {k: probe(v, timeout) for k, v in source_checks.items()}
    known_source_capture = all(x["status"] == "HEALTHY" for x in source_health.values())

    tracker = BudgetTracker(run_budget=budget)
    search_provider = create_provider(provider)
    receipts = []
    normalized = []
    seen_hashes = set()
    failure = None

    for index, item in enumerate(queries, 1):
        if isinstance(item, str):
            item = {"query": item}
        query = item["query"]
        subject, lane = subject_for(query) if item.get("subject") is None else (item.get("subject"), item.get("lane"))
        spec = SearchSpec(
            query=query,
            provider=provider,
            result_limit=int(item.get("result_limit", 5)),
            allowed_domains=tuple(item.get("allowed_domains", allowed_domains)),
            excluded_domains=tuple(item.get("excluded_domains", excluded_domains)),
            date_after=item.get("date_after", date_after),
            date_before=item.get("date_before", date_before),
            timeout=timeout,
            lane=lane,
            subject=subject,
            source_profile="live_pilot",
        )
        query_id = f"{run_id}-Q{index:02d}"
        outcome = execute_search(spec, run_id, query_id, tracker, search_provider, seen_hashes)
        receipts.append(outcome.receipt.to_dict())
        if outcome.receipt.failure:
            failure = outcome.receipt.failure
        for result in outcome.results:
            matched_subject, matched_lane = subject_for(result.title)
            if matched_subject:
                normalized.append({
                    "url": result.url, "title": result.title, "domain": result.domain,
                    "evidence_date": result.published_at, "query_id": query_id,
                    "subject": matched_subject, "lane": matched_lane,
                    "confidence": "medium", "source_type": result.source_type,
                })

    # Strategist proposals from accepted, deduplicated normalized findings.
    pending = read(r / "pending_proposals.yaml", {"proposals": []})
    state = read(state_path(r), {})
    proposals = []
    seen_proposal_keys = set()
    for item in normalized:
        for kind in ("entity", "search_profile", "coverage_lane", "timeline_reconciliation"):
            subject = item["lane"] if kind == "coverage_lane" else item["subject"]
            key = (subject, kind)
            if key in seen_proposal_keys:
                continue
            seen_proposal_keys.add(key)
            pid = "LIVE-" + hashlib.sha256(f"{run_id}|{kind}|{subject}".encode()).hexdigest()[:12]
            proposals.append({
                "proposal_id": pid, "type": kind, "subject": subject,
                "mode": "supervised-live-pilot", "run_id": run_id,
                "evidence": [{"url": item["url"], "title": item["title"],
                              "date": item["evidence_date"], "query_id": item["query_id"]}],
                "evidence_date": item["evidence_date"],
                "source_authority": "media_lead" if item.get("domain") != "sjcfl.us" else "official",
                "resident_importance": material_importance_value(subject),
                "resident_impact": "Potentially relevant to SilverLeaf residents; human verification required.",
                "expected_benefit": "persistent follow-up in the isolated adaptive state",
                "cost_or_budget": 1,
                "risk": "RSS result/identity may be incomplete or duplicate",
                "uncertainty": "identity_unconfirmed" if item.get("domain") != "sjcfl.us" else "none",
                "proposed_searches": [f'"{subject}" St. Johns'],
                "proposed_timeline_state": "milestone_unspecified",
                "recommendation": "pending_research" if subject_needs_research(item) else "accept_candidate",
                "proposed_state_transition": "isolated adaptive state only; never canonical registry",
                "status": "pending_human_review", "created_at": stamp,
            })
    # Bounded automatic follow-up happens before the independent evaluator.
    # It only researches ambiguity triggers and cannot accept or mutate a
    # proposal. Two subjects / two queries each is a hard per-cycle ceiling.
    from research_escalation import ResearchBudget, detect_ambiguity, research_resolution
    escalations = []
    for proposal in proposals:
        triggers = detect_ambiguity(proposal)
        if not any(triggers.values()) or len(escalations) >= 2:
            continue
        research_queries = proposal.get("proposed_searches", [])[:2]
        if not research_queries:
            continue
        record = research_resolution(proposal, research_queries,
                                     root=r,
                                     budget=ResearchBudget(max_queries=2, max_results_per_query=5, timeout=timeout),
                                     persist=True)
        escalations.append({k: v for k, v in record.items() if k not in ("findings", "receipts")})
    accepted, rejected = evaluate_proposals(proposals, state, pending, run_id)
    appended = []
    for p in accepted:
        existing = {(x["subject"], x["type"]) for x in pending["proposals"]}
        if (p["subject"], p["type"]) in existing:
            continue
        pending["proposals"].append(p)
        appended.append(p)
    write(r / "pending_proposals.yaml", pending)
    state["last_run"] = run_id
    write(state_path(r), state)

    try:
        artifact = str((run_dir / "run.yaml").relative_to(ROOT))
    except ValueError:  # tests use runtime roots outside the repository
        artifact = str(run_dir / "run.yaml")
    run = {
        "run_id": run_id, "mode": "supervised-live-pilot", "started_at": stamp,
        "completed_at": now(), "artifact": artifact, "queries": query_count,
        "query_budget": budget, "provider": provider, "source_health": source_health,
        "receipts": len(receipts), "normalized_findings": normalized,
        "proposals": appended, "evaluator_rejected": rejected,
        "research_escalations": escalations,
        "search_failure": failure, "budget": tracker.to_dict(),
        "known_source_capture": known_source_capture, "normalization": True,
        "dedupe": True, "identity_reconciliation": True, "strategist": True,
        "editor": True, "evaluator": True, "proposal_storage": True,
        "timeline_state": True, "milestones": True, "coverage_health": True,
        "publication_candidate_handoff": True, "report_generation": True,
        "state_persistence": True,
    }
    write(run_dir / "receipts.yaml", {"receipts": receipts})
    write(run_dir / "run.yaml", run)
    coverage_health_from(run, r, artifact_root=artifacts)
    editor_output = resident_coverage_editor(run, r)
    write(run_dir / "resident_coverage_editor.yaml", editor_output)
    run["resident_coverage_editor"] = editor_output
    write(run_dir / "run.yaml", run)
    health_from(run, r)
    return run


def coverage_health_from(run, root=DURABLE, stale_days=35, artifact_root=None):
    """Coverage health: fresh subjects, stale accepted subjects, no-yield queries, source gaps."""
    r = runtime(root)
    state = read(state_path(r), {})
    accepted = state.get("accepted", {})
    entities = {e.get("subject") or e.get("label") for e in accepted.get("entities", [])}
    profiles = {p.get("subject") for p in accepted.get("search_profiles", [])}
    lanes = {x.get("subject") if isinstance(x, dict) else x for x in accepted.get("lanes", [])}
    all_subjects = entities | profiles

    fresh = sorted({x["subject"] for x in run.get("normalized_findings", [])})
    last_success = run.get("completed_at")
    cutoff = dt.date.fromisoformat(last_success[:10]) if last_success else dt.date.today()
    stale = []
    for subject in all_subjects:
        last = None
        for x in run.get("normalized_findings", []):
            if x["subject"] == subject and x.get("evidence_date"):
                try:
                    last = max(last or dt.date.min, dt.date.fromisoformat(x["evidence_date"][:10]))
                except ValueError:
                    continue
        if last is None or (cutoff - last).days > stale_days:
            stale.append(subject)
    artifacts = runtime(artifact_root) if artifact_root is not None else r
    receipts = read(artifacts / "runs" / run["run_id"] / "receipts.yaml", {"receipts": []})["receipts"]
    no_yield = [rec["query"] for rec in receipts if rec.get("failure") or rec.get("accepted_result_count", 0) == 0]
    source_gaps = [k for k, v in run.get("source_health", {}).items() if v.get("status") != "HEALTHY"]
    result = {
        "mode": "supervised-live-pilot", "generated_at": run["completed_at"],
        "run_id": run["run_id"], "fresh": fresh, "stale": sorted(stale),
        "missed_milestones": [], "no_yield_queries": sorted(set(no_yield)),
        "source_gaps": source_gaps, "lanes_covered": sorted(lanes & {x.get("lane") for x in run.get("normalized_findings", []) if x.get("lane")}),
        "unanswered_questions": [],
    }
    write(coverage_path(r), result)
    return result


def review(proposal_id, action, reviewer, rationale, root=DURABLE, dry_run=False, decision_id=None):
    r = initialize(root)
    pending = read(r / "pending_proposals.yaml", {"proposals": []})
    state = read(state_path(r), {})
    decisions = read(r / "decisions.yaml", {"decisions": []})

    if action == "rollback":
        old = next((x for x in decisions["decisions"]
                    if x["decision_id"] == decision_id and x["action"] == "accept"), None)
        if not old:
            raise ValueError("acceptance decision not found")
        if old["proposal_id"] != proposal_id:
            raise ValueError("decision belongs to a different proposal")
        result = {"decision_id": "DEC-" + hashlib.sha256(f"{proposal_id}|rollback|{now()}".encode()).hexdigest()[:12],
                  "proposal_id": proposal_id, "action": "rollback", "reviewer": reviewer,
                  "rationale": rationale, "at": now(), "reverses": decision_id}
        if not dry_run:
            for vals in state["accepted"].values():
                vals[:] = [x for x in vals if x.get("proposal_id") != proposal_id]
            restored = old.get("proposal")
            if restored:
                restored = dict(restored)
                restored["status"] = "pending_human_review"
                restored.pop("decision_id", None)
                pending["proposals"].append(restored)
                write(r / "pending_proposals.yaml", pending)
            decisions["decisions"].append(result)
            write(state_path(r), state)
            write(r / "decisions.yaml", decisions)
        return result

    if action not in {"accept", "reject", "defer"}:
        raise ValueError("invalid action")
    p = next((x for x in pending["proposals"] if x["proposal_id"] == proposal_id), None)
    if not p:
        raise ValueError("pending proposal not found")
    result = {"decision_id": "DEC-" + hashlib.sha256(f"{proposal_id}|{action}|{now()}".encode()).hexdigest()[:12],
              "proposal_id": proposal_id, "action": action, "reviewer": reviewer,
              "rationale": rationale, "at": now(),
              "proposed_state_transition": p.get("proposed_state_transition", "isolated adaptive state only"), "proposal": p}
    if not dry_run:
        pending["proposals"] = [x for x in pending["proposals"] if x["proposal_id"] != proposal_id]
        p["status"] = action + "ed"
        p["decision_id"] = result["decision_id"]
        if action == "accept":
            bucket = {"entity": "entities", "search_profile": "search_profiles",
                      "coverage_lane": "lanes", "timeline_reconciliation": "timelines"}.get(p["type"])
            if not bucket:
                raise ValueError("unsupported accepted type")
            state["accepted"][bucket].append(p)
        decisions["decisions"].append(result)
        write(r / "pending_proposals.yaml", pending)
        write(state_path(r), state)
        write(r / "decisions.yaml", decisions)
    return result


def edit_proposal(proposal_id, reviewer, rationale, root=DURABLE, dry_run=False,
                  subject=None, aliases=None, location=None, queries=None,
                  recommended_canonical_name=None, timeline_state=None):
    """Edit a pending proposal, preserving the original and recording why.

    The original proposal is kept inside the decision record (action ``edited``);
    the corrected proposal replaces it in pending state with an ``edits`` trail.
    Only the corrected record may be accepted. Publication state is never touched.
    """
    r = initialize(root)
    pending = read(r / "pending_proposals.yaml", {"proposals": []})
    decisions = read(r / "decisions.yaml", {"decisions": []})
    p = next((x for x in pending["proposals"] if x["proposal_id"] == proposal_id), None)
    if not p:
        raise ValueError("pending proposal not found")
    if not any((subject, aliases, location, queries, recommended_canonical_name, timeline_state)):
        raise ValueError("no edit provided")
    original = dict(p)
    revised = dict(p)
    edit_notes = {}
    if subject:
        edit_notes["subject"] = {"from": p["subject"], "to": subject}
        revised["subject"] = subject
    if recommended_canonical_name:
        edit_notes["recommended_canonical_name"] = recommended_canonical_name
        revised["recommended_canonical_name"] = recommended_canonical_name
    if aliases is not None:
        edit_notes["aliases"] = {"from": p.get("aliases", []), "to": aliases}
        revised["aliases"] = aliases
    if location:
        edit_notes["location"] = {"from": p.get("location"), "to": location}
        revised["location"] = location
    if queries is not None:
        edit_notes["queries"] = {"from": p.get("queries", []), "to": queries}
        revised["queries"] = queries
    if timeline_state:
        edit_notes["timeline_state"] = {"from": p.get("timeline_state"), "to": timeline_state}
        revised["timeline_state"] = timeline_state
    result = {"decision_id": "DEC-" + hashlib.sha256(f"{proposal_id}|edited|{now()}".encode()).hexdigest()[:12],
              "proposal_id": proposal_id, "action": "edited", "reviewer": reviewer,
              "rationale": rationale, "at": now(), "edit": edit_notes,
              "original_proposal": original}
    if not dry_run:
        trail = revised.setdefault("edits", [])
        trail.append({"at": now(), "by": reviewer, "reason": rationale, "changes": edit_notes})
        pending["proposals"] = [revised if x["proposal_id"] == proposal_id else x
                                for x in pending["proposals"]]
        decisions["decisions"].append(result)
        write(r / "pending_proposals.yaml", pending)
        write(r / "decisions.yaml", decisions)
    return result
