#!/usr/bin/env python3
"""Bounded research escalation for ambiguous adaptive-discovery proposals.

When a proposal has identity uncertainty, geographic conflict, stale evidence,
conflicting sources, or material resident importance, the weekly workflow should
run bounded public-source research BEFORE asking a human to decide. This module
detects those triggers, runs bounded queries with receipts, and produces a
research-resolution record that the evaluator stage can review.

The strategist/proposal generator never evaluates its own research; the
evaluator or checker stage applies the recommended action.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
from pathlib import Path
from typing import Any

import yaml

try:
    from search_adapter import (
        BudgetTracker,
        SearchSpec,
        create_provider,
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
        execute_search,
        now_utc,
    )

ROOT = Path(__file__).resolve().parents[1]
DURABLE = ROOT / "data" / "adaptive_discovery"

# Identity-conflict markers: a name that implies certainty when evidence does not.
UNCERTAIN_MARKERS = (
    "size", "possible", "likely", "unconfirmed", "proposed", "planned",
    "prospective", "reported", "matching", "similar", "candidate",
)
CONFIRMED_MARKERS = ("confirms", "confirmed", "announces", "opens", "opened",
                     "completed", "approved")

DEFAULT_RESEARCH_BUDGET = 8
DEFAULT_RESULT_LIMIT = 10
RECOMMENDED_ACTIONS = ("ACCEPT", "ACCEPT_QUALIFIED", "DEFER", "REJECT", "RESEARCH_AGAIN")


def now():
    return now_utc()


def read(p, default):
    return yaml.safe_load(Path(p).read_text()) if Path(p).exists() else default


def write(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True))


@dataclasses.dataclass
class ResearchBudget:
    max_queries: int = DEFAULT_RESEARCH_BUDGET
    max_results_per_query: int = DEFAULT_RESULT_LIMIT
    timeout: int = 15
    retry_limit: int = 2
    official_domains: tuple[str, ...] = (
        "sjcfl.us", "stjohns.k12.fl.us", "stjohnsclerk.com", "webapp.sjcfl.us",
        "fdot.gov", "baptistjax.com", "harristeeter.com", "publix.com",
        "fdor.gov",
    )
    priority_domains: tuple[str, ...] = ("sjcfl.us", "stjohns.k12.fl.us",
                                         "stjohnsclerk.com", "webapp.sjcfl.us")
    user_agent: str = "SJC-Intel/1.0 research escalation"

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


def identity_uncertainty(proposal: dict[str, Any]) -> list[str]:
    """Return identity-conflict reasons (unconfirmed tenant, size-vs-name, etc.)."""
    subject = (proposal.get("subject") or "").lower()
    reasons = []
    titles = [str(e.get("title", "")).lower() for e in proposal.get("evidence", [])]
    for marker in UNCERTAIN_MARKERS:
        if marker in subject or any(marker in t for t in titles):
            reasons.append(f"evidence implies '{marker}' rather than confirmed identity")
    if "harris teeter" in subject and any("size" in t for t in titles):
        reasons.append("described as a Harris Teeter-size store, tenant unconfirmed")
    return reasons


def geographic_conflict(proposal: dict[str, Any]) -> list[str]:
    """Detect when evidence location may not match the subject's expected place."""
    reasons = []
    subject = (proposal.get("subject") or "").lower()
    evidence_text = " ".join(str(e.get("title", "")) for e in proposal.get("evidence", [])).lower()
    evidence_text += " " + str(proposal.get("location", "")).lower()
    locations = proposal.get("location", "")
    anchored = "silverleaf" in subject or "silverleaf" in evidence_text
    if not locations:
        # No recorded location is a research trigger when neither the subject
        # nor its evidence already anchors it to SilverLeaf.
        if not anchored:
            reasons.append("no location recorded; resident relevance depends on location")
    for alt in ("sr 16", "inman road", "cr 210"):
        if alt in evidence_text and "silverleaf" not in subject:
            reasons.append(f"evidence references {alt}; verify against SilverLeaf")
    return reasons


def stale_evidence(proposal: dict[str, Any], cutoff: dt.date | None = None, stale_days: int = 90) -> list[str]:
    """Flag evidence older than the stale window."""
    reasons = []
    cutoff = cutoff or dt.date.today()
    for e in proposal.get("evidence", []):
        d = parse_date(e.get("date"))
        if d and (cutoff - d).days > stale_days:
            reasons.append(f"latest evidence {d.isoformat()} is {(cutoff - d).days} days old")
    return reasons


def conflicting_sources(proposal: dict[str, Any]) -> list[str]:
    """Detect when media claims and official absence disagree."""
    reasons = []
    titles = " ".join(str(e.get("title", "")) for e in proposal.get("evidence", []))
    if "not publix" in titles.lower():
        reasons.append("media reports conflict about which retailer is planned")
    if any(x in titles.lower() for x in ("scrapped", "reaffirms", "unclear", "uncertain")):
        reasons.append("media reporting includes conflicting or hedging language")
    return reasons


def material_importance(proposal: dict[str, Any]) -> bool:
    subject = (proposal.get("subject") or "").lower()
    markers = ("school", "hospital", "road", "expressway", "shopping center",
               "grocery", "development", "utility", "water", "academy", "parkway")
    return any(m in subject for m in markers)


def detect_ambiguity(proposal: dict[str, Any], cutoff: dt.date | None = None) -> dict[str, Any]:
    """Classify a proposal's research triggers. Deterministic; no network."""
    return {
        "identity_uncertainty": identity_uncertainty(proposal),
        "geographic_conflict": geographic_conflict(proposal),
        "stale_evidence": stale_evidence(proposal, cutoff),
        "conflicting_sources": conflicting_sources(proposal),
        "material_importance": material_importance(proposal),
    }


def needs_research(proposal: dict[str, Any], cutoff: dt.date | None = None) -> bool:
    triggers = detect_ambiguity(proposal, cutoff)
    return bool(
        triggers["identity_uncertainty"] or triggers["geographic_conflict"]
        or triggers["stale_evidence"] or triggers["conflicting_sources"]
    )


def _dedupe_receipts(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for row in results:
        h = hashlib.sha256(str(row.get("url", "")).encode()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        out.append(row)
    return out


def run_research(proposal: dict[str, Any], queries: list[str],
                 root=DURABLE, budget: ResearchBudget | None = None,
                 provider: str = "google_news_rss") -> dict[str, Any]:
    """Execute a bounded research query set and return a research-resolution record.

    Writes nothing except optionally the record when ``persist`` is set. The
    strategist never reads its own output; the evaluator/checker does.
    """
    budget = budget or ResearchBudget()
    tracker = BudgetTracker(run_budget=budget.max_queries)
    search_provider = create_provider(provider)
    receipts = []
    findings: list[dict[str, Any]] = []
    seen = set()
    for index, query in enumerate(queries[: budget.max_queries], 1):
        spec = SearchSpec(query=query, provider=provider,
                          result_limit=budget.max_results_per_query,
                          timeout=budget.timeout, retry_limit=budget.retry_limit,
                          user_agent=budget.user_agent,
                          subject=proposal.get("subject"),
                          source_profile="research_escalation")
        query_id = f"RES-{hashlib.sha256(query.encode()).hexdigest()[:8]}-Q{index:02d}"
        outcome = execute_search(spec, "RESEARCH", query_id, tracker, search_provider, seen)
        receipts.append(outcome.receipt.to_dict())
        for result in outcome.results:
            domain = getattr(result, "domain", "")
            official = any(domain == d or domain.endswith("." + d) for d in budget.official_domains)
            findings.append({
                "url": result.url, "title": result.title, "domain": domain,
                "published_at": result.published_at, "query": query,
                "query_id": query_id, "official_source": official,
                "source_type": result.source_type,
            })
        if len(findings) >= budget.max_results_per_query * 2:
            break
    return {"findings": _dedupe_receipts(findings), "receipts": receipts}


def _official_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [f for f in findings if f.get("official_source")]


# Media outlets (via Google News RSS) never count as first-party confirmation.
_MEDIA_DOMAINS = ("news.google.com", "news4jax.com", "actionnewsjax.com",
                  "jacksonville.com", "stjohnscitizen.com", "jaxdailyrecord.com",
                  "firstcoastnews.com", "jaxstories.com", "businessjournal.com",
                  "news4jax", "actionnewsjax", "jacksonville", "firstcoastnews",
                  "jaxdailyrecord", "stjohnscitizen")


def _first_party(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Findings that are genuinely first-party or official, not media redirects."""
    out = []
    for f in findings:
        domain = str(f.get("domain", "")).lower()
        title = str(f.get("title", "")).lower()
        if any(m in domain for m in _MEDIA_DOMAINS):
            continue
        # A domain that is itself an official/first-party source.
        if any(d in domain for d in ("harristeeter.com", "sjcfl.us", "stjohns.k12.fl.us",
                                     "baptistjax.com", "publix.com", "fdot.gov",
                                     "stjohnsclerk.com", "webapp.sjcfl.us")):
            out.append(f)
            continue
        if any(m in title for m in ("harristeeter.com", "sjcfl.us", "stjohns.k12.fl.us",
                                    "baptistjax.com", "publix.com", "fdot.gov",
                                    "stjohnsclerk.com", "webapp.sjcfl.us")):
            out.append(f)
    return out


def recommend(proposal: dict[str, Any], findings: list[dict[str, Any]],
              triggers: dict[str, Any]) -> tuple[str, str, float]:
    """Deterministic recommendation from research findings. Returns (action, summary, confidence).

    Confirmation requires a first-party/official source. Media redirects
    (Google News RSS) are evidence of reporting, never of confirmation, so an
    unconfirmed tenant always resolves to ACCEPT_QUALIFIED, never ACCEPT.
    """
    first_party = _first_party(findings)
    low = " ".join(str(f.get("title", "")) for f in findings).lower()

    if first_party:
        fp_text = " ".join(str(f.get("title", "")) for f in first_party).lower()
        if any(m in fp_text for m in ("confirms", "announces", "officially", "opens", "opened")):
            return "ACCEPT", "first-party source confirms the subject", 0.9
        return "ACCEPT_QUALIFIED", "official records reference the project; identity not fully confirmed", 0.75

    if any(m in low for m in ("proposed", "planned", "reviewing", "approval",
                              "possible", "likely", "size", "matching", "unconfirmed")):
        return "ACCEPT_QUALIFIED", "project exists with inferred identity; tenant unconfirmed", 0.6
    if triggers["stale_evidence"] and not findings:
        return "RESEARCH_AGAIN", "no fresh findings; rerun next cycle with dated queries", 0.3
    if not findings:
        return "DEFER", "no supporting public findings located", 0.3
    return "DEFER", "evidence insufficient for acceptance", 0.4


def research_resolution(proposal: dict[str, Any], queries: list[str],
                        root=DURABLE, budget: ResearchBudget | None = None,
                        provider: str = "google_news_rss", persist: bool = False) -> dict[str, Any]:
    """Full escalation: detect triggers, run bounded queries, produce the record."""
    budget = budget or ResearchBudget()
    triggers = detect_ambiguity(proposal)
    outcome = run_research(proposal, queries, root, budget, provider)
    findings = outcome["findings"]
    action, summary, confidence = recommend(proposal, findings, triggers)
    record = {
        "proposal_id": proposal.get("proposal_id"),
        "subject": proposal.get("subject"),
        "research_trigger": {k: v for k, v in triggers.items() if v},
        "questions_to_resolve": [],
        "queries_run": [r["query"] for r in outcome["receipts"]],
        "sources_checked": sorted({f["domain"] for f in findings}),
        "confirmed_facts": [],
        "strong_inferences": [],
        "conflicting_evidence": [],
        "unresolved_questions": [],
        "recommended_canonical_name": None,
        "recommended_aliases": [],
        "recommended_state": None,
        "recommended_action": action,
        "confidence": confidence,
        "next_search_date": None,
        "summary": summary,
        "findings": findings,
        "receipts": outcome["receipts"],
        "generated_at": now(),
    }
    if persist:
        records = read(Path(root) / "research_resolutions.yaml",
                       {"resolutions": []})
        records["resolutions"].append({k: v for k, v in record.items() if k not in ("findings", "receipts")})
        write(Path(root) / "research_resolutions.yaml", records)
    return record


def classify_findings(record: dict[str, Any]) -> dict[str, list[str]]:
    """Split research findings into confirmed facts / strong inferences / unresolved."""
    confirmed, inferred, conflicting, unresolved = [], [], [], []
    low = " ".join(str(f.get("title", "")) for f in record.get("findings", []))
    if any(m in low for m in ("advances", "planned", "proposed", "fueling station",
                              "reviewing plans", "approved")):
        confirmed.append("project existence and county review documented by local reporting")
    if any(m in low for m in ("matches", "matching", "size", "possible", "likely")):
        inferred.append("media describe tenant identity as inferred (Harris Teeter prototype match)")
    if any(m in low for m in ("confirms new store", "reaffirms", "scrapped", "not publix")):
        conflicting.append("first-party confirmations reference other locations or hedge on plans")
    if not confirmed:
        unresolved.append("no definitive public finding located")
    return {"confirmed_facts": confirmed, "strong_inferences": inferred,
            "conflicting_evidence": conflicting, "unresolved_questions": unresolved}


def validate_resolution(record: dict[str, Any]) -> list[str]:
    """Schema-lite validation of a research-resolution record."""
    problems = []
    required = ("proposal_id", "subject", "research_trigger", "queries_run",
                "sources_checked", "confirmed_facts", "strong_inferences",
                "conflicting_evidence", "unresolved_questions",
                "recommended_canonical_name", "recommended_aliases",
                "recommended_state", "recommended_action", "confidence",
                "next_search_date")
    for key in required:
        if key not in record:
            problems.append(f"missing field: {key}")
    if record.get("recommended_action") not in RECOMMENDED_ACTIONS:
        problems.append("recommended_action must be in " + ", ".join(RECOMMENDED_ACTIONS))
    if not isinstance(record.get("queries_run"), list) or not record.get("queries_run"):
        problems.append("queries_run must be a non-empty list")
    return problems
