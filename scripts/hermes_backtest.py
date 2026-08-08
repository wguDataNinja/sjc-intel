#!/usr/bin/env python3
"""SJC_Intel — Hermes-operated historical production backtest infrastructure.

This is the isolated workspace and orchestration layer for Task 30: Hermes
itself performs the weekly reasoning/discovery against historical-visible
state, rather than the deterministic Task 22 `generate()`.

Layers:
- `feed` — per-week dated historical source feed derived from the production
  corpus (the best available dated record of what public sources published),
  placed in each simulated week. Two views: `monitored.yaml` (items from the
  sources Hermes currently monitors) and `all.yaml` (the week's full dated
  feed, used as the stand-in search universe for approved search profiles).
- `assemble_week` — writes the weekly packet (starting state, feed, task,
  budgets) for a simulated week.
- `ingest_week` — validates Hermes's outputs, applies the simulated acceptance
  policy, and produces next-week state.
- `evaluate` — the hidden evaluator (runs only after Hermes finishes a week):
  subject/lane discovery vs the hidden subject set, Resident Coverage Recall,
  discovery lag, promotion lag, search/alias/timeline/source evolution, and
  false positives. Never written into a Hermes packet.
- `publication_snapshot` — backtest-only release inventory showing what Hermes
  would have published at a historical date (never touches the real site).

Isolation: everything under `data/hermes_backtests/<id>/`. No production path
is ever written by this module.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HERMES_BACKTESTS = ROOT / "data" / "hermes_backtests"
PROMPT_TEMPLATE = ROOT / "prompts" / "hermes_historical_weekly_task.md"

PROPOSAL_TYPES = {"entity", "alias", "project", "place", "source",
                  "search_profile", "milestone", "timeline_reconciliation",
                  "coverage_lane"}
EDITOR_ACTIONS = {"SEARCH_NOW", "ADD_SEARCH_PROFILE", "REFRESH_SOURCE",
                  "EXPECT_MILESTONE", "CREATE_TIMELINE_PROPOSAL",
                  "CREATE_ENTITY_PROPOSAL", "NO_ACTION", "ESCALATE_TO_HUMAN"}
SENSITIVE_TOPIC_HINTS = ("crime", "arrest", "shooting", "murder", "minor",
                         "charg", "detainer")


def day(value):
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value)[:10])


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True))


def load(path: Path, default=None):
    return yaml.safe_load(path.read_text()) if path.exists() else copy.deepcopy(default)


def root(backtest_id: str) -> Path:
    if not backtest_id or "/" in backtest_id or ".." in backtest_id:
        raise ValueError("backtest id must be a simple name")
    return HERMES_BACKTESTS / backtest_id


def weeks_between(start: dt.date, end: dt.date, step_days: int = 7):
    s = start
    while s <= end:
        yield s
        s += dt.timedelta(days=step_days)


# --------------------------------------------------------------------------- #
# Feed construction (historically reproducible evidence from dated corpus)
# --------------------------------------------------------------------------- #

def _item_date(item):
    for key in ("source_published_at", "discovered_at"):
        val = item.get(key)
        if val:
            try:
                return day(val)
            except Exception:
                continue
    return None


def iter_corpus_records():
    """Yield dated corpus records (intel_items + monthly backfill)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from publication_common import iter_intel_items
    for rel, item in iter_intel_items():
        d = _item_date(item)
        if not d:
            continue
        yield {
            "item_id": item["item_id"],
            "week_date": d,
            "source_id": item.get("source_id"),
            "source_name": (item.get("citation") or {}).get("source_name") or item.get("source_id"),
            "title": item.get("title"),
            "summary": item.get("summary"),
            "source_published_at": item.get("source_published_at"),
            "topics": item.get("topics") or [],
            "sensitivity": item.get("sensitivity", "low"),
            "review_status": item.get("review_status"),
        }


def build_feed(backtest_id: str, rebuild: bool = False) -> Path:
    """Write per-week feed files under feed/weeks/<YYYY-MM-DD>.yaml."""
    r = root(backtest_id)
    cfg = load(r / "config.yaml", {})
    start, end = day(cfg["start"]), day(cfg["end"])
    out_root = r / "feed" / "weeks"
    if rebuild and out_root.exists():
        import shutil
        shutil.rmtree(out_root)
    records = list(iter_corpus_records())
    # Documented overrides: dated public records that are historically real but
    # were captured outside the corpus as items (e.g., a live-search lead with a
    # known publication date). Feed/overrides.yaml is part of the versioned
    # backtest fixture, not the production corpus. Task 30 §6.
    for ov in load(r / "feed" / "overrides.yaml", []):
        if ov.get("item_id") in {x["item_id"] for x in records}:
            continue
        d = day(ov["week_date"])
        records.append({
            "item_id": ov["item_id"], "week_date": d,
            "source_id": ov.get("source_id", "web_discovery"),
            "source_name": ov.get("source_name", ov.get("source_id", "web_discovery")),
            "title": ov.get("title"), "summary": ov.get("summary", ""),
            "source_published_at": ov.get("week_date"),
            "topics": ov.get("topics", []),
            "sensitivity": ov.get("sensitivity", "low"),
            "review_status": "historical_override",
        })
    # Bucket each record into its simulated week (the week_start whose 7-day
    # interval contains the record's publication/availability date).
    week_starts = list(weeks_between(start, end))
    buckets = defaultdict(list)
    seen_ids = set()
    for rec in records:
        if rec["item_id"] in seen_ids:
            continue
        seen_ids.add(rec["item_id"])
        if not (start <= rec["week_date"] <= end):
            continue
        idx = (rec["week_date"] - start).days // 7
        wk = week_starts[min(idx, len(week_starts) - 1)]
        buckets[wk.isoformat()].append(rec)
    total = 0
    for wk in week_starts:
        wk_key = wk.isoformat()
        entries = sorted(buckets.get(wk_key, []),
                         key=lambda x: (x["source_id"], x["item_id"]))
        dump(out_root / f"{wk_key}.yaml", {
            "week_start": wk_key, "week_end": (wk + dt.timedelta(days=6)).isoformat(),
            "entries": entries,
        })
        total += len(entries)
    dump(r / "feed" / "summary.yaml", {
        "weeks": sum(1 for _ in weeks_between(start, end)),
        "total_entries": total,
        "note": ("Derived from the dated production corpus (intel_items + monthly "
                 "backfill) placed in each simulated publication week. This is the "
                 "historically reproducible evidence layer; it is not a claim to "
                 "reproduce historical search rankings (Task 30 §6/§9)."),
    })
    return out_root


def monitored_source_ids(state: dict) -> list[str]:
    """Visible seed sources + accepted source proposals, by subject label."""
    ids = []
    for s in state.get("sources", []):
        ids.append(s.get("source_id") or s.get("subject"))
    return sorted(set(x for x in ids if x))


def visible_state(backtest_id: str, week_start: dt.date) -> dict:
    """Rebuild availability-limited state from accepted transitions before week_start."""
    r = root(backtest_id)
    seed = load(r / "seed.yaml", {})
    state = {
        "available_on": seed.get("available_on"),
        "sources": list(seed.get("sources", [])),
        "entities": list(seed.get("entities", [])),
        "search_profiles": list(seed.get("search_profiles", [])),
        "lanes": list(seed.get("lanes", [])),
        "milestones": list(seed.get("milestones", [])),
        "timelines": list(seed.get("timelines", [])),
        "accepted_proposals": [],
        "rejected_proposals": [],
        "last_week": None,
    }
    for path in sorted((r / "weeks").glob("*/accepted_state.yaml")):
        acc = load(path, {})
        if day(acc.get("available_on", "9999-12-31")) > week_start:
            continue
        for p in acc.get("accepted", []):
            apply_proposal(state, p)
        state["last_week"] = acc.get("week_start")
        state["accepted_proposals"].extend(acc.get("accepted_ids", []))
        state["rejected_proposals"].extend(acc.get("rejected_ids", []))
    return state


def apply_proposal(state: dict, p: dict) -> None:
    kind, subject = p["type"], p["subject"]
    avail = p.get("available_on", p.get("simulated_week"))
    if kind == "entity":
        state["entities"].append({"id": p["proposal_id"], "label": subject,
                                  "aliases": [], "available_on": avail,
                                  "evidence": p.get("evidence", [])})
    elif kind == "alias":
        for e in state["entities"]:
            if e["label"] == p.get("target"):
                e.setdefault("aliases", []).append({"value": subject, "first_seen": avail})
    elif kind == "search_profile":
        state["search_profiles"].append({"subject": subject,
                                         "queries": p.get("proposed_searches", []),
                                         "budget": p.get("cost", 1),
                                         "available_on": avail})
    elif kind == "source":
        if not any(s.get("source_id") == subject for s in state["sources"]):
            state["sources"].append({"source_id": subject, "name": subject,
                                     "kind": "proposed", "available_on": avail})
    elif kind == "coverage_lane" and subject not in state["lanes"]:
        state["lanes"].append(subject)
    elif kind == "milestone":
        state["milestones"].append({"subject": subject,
                                    "expected": p.get("anticipated_milestones", []),
                                    "milestone_due": p.get("milestone_due", {}),
                                    "available_on": avail})
    elif kind == "timeline_reconciliation":
        state["timelines"].append({"subject": subject,
                                   "event": (p.get("anticipated_milestones") or [None])[0],
                                   "available_on": avail})


def entity_matches(state: dict, text: str) -> bool:
    low = text.lower()
    for e in state["entities"]:
        names = [e["label"]] + [a["value"] if isinstance(a, dict) else a
                                for a in e.get("aliases", [])]
        if any(n.lower() in low for n in names):
            return True
    return False


# --------------------------------------------------------------------------- #
# Week assembly
# --------------------------------------------------------------------------- #

def render_task(template: str, cfg: dict, week_start: dt.date, week_end: dt.date,
                state: dict) -> str:
    monitored = ", ".join(monitored_source_ids(state)) or "none"
    b = cfg.get("budgets", {})
    budgets = (f"model_calls_per_week: {b.get('max_model_calls_per_week')}, "
               f"search_profiles_executed: {b.get('max_search_profiles_executed_per_week')}, "
               f"research_escalations: {b.get('max_research_escalations_per_week')}, "
               f"research_queries_per_escalation: {b.get('max_research_queries_per_escalation')}")
    return (template
            .replace("{backtest_id}", cfg.get("backtest_id", "hermes-sjc-v1"))
            .replace("{week_start}", week_start.isoformat())
            .replace("{week_end}", week_end.isoformat())
            .replace("{monitored_sources}", monitored)
            .replace("{budgets}", budgets))


def assemble_week(backtest_id: str, week_start: str, overwrite: bool = False) -> Path:
    r = root(backtest_id)
    cfg = load(r / "config.yaml", {})
    s = day(week_start)
    e = s + dt.timedelta(days=6)
    w = r / "weeks" / s.isoformat()
    if w.exists() and not overwrite:
        raise SystemExit(f"week directory already exists: {w} (use --overwrite for a versioned redo)")
    state = visible_state(backtest_id, s)
    dump(w / "starting_state.yaml", state)
    # Feed views for this week.
    feed_week = load(r / "feed" / "weeks" / f"{s.isoformat()}.yaml", {"entries": []})
    entries = feed_week.get("entries", [])
    monitored_ids = set(monitored_source_ids(state))
    monitored = [x for x in entries if x["source_id"] in monitored_ids]
    all_ = entries
    dump(w / "feed" / "monitored.yaml", {"week_start": s.isoformat(), "entries": monitored})
    dump(w / "feed" / "all.yaml", {"week_start": s.isoformat(), "entries": all_})
    dump(w / "budgets.yaml", {"week_start": s.isoformat(), **cfg.get("budgets", {})})
    task = render_task(PROMPT_TEMPLATE.read_text(encoding="utf-8"), cfg, s, e, state)
    (w / "hermes_task.md").write_text(task)
    dump(w / "meta.yaml", {"backtest_id": backtest_id, "week_start": s.isoformat(),
                           "week_end": e.isoformat(), "status": "pending",
                           "visible_state_cutoff": s.isoformat()})
    return w


# --------------------------------------------------------------------------- #
# Ingest + simulated acceptance
# --------------------------------------------------------------------------- #

def _is_sensitive(entry_text: str, sensitivity: str) -> bool:
    low = (entry_text or "").lower()
    if sensitivity in ("medium", "high"):
        return True
    return any(h in low for h in SENSITIVE_TOPIC_HINTS)


def ingest_week(backtest_id: str, week_start: str) -> dict:
    r = root(backtest_id)
    cfg = load(r / "config.yaml", {})
    policy = cfg.get("simulated_acceptance", {})
    s = day(week_start)
    e = s + dt.timedelta(days=6)
    w = r / "weeks" / s.isoformat()
    if not w.exists():
        raise SystemExit(f"week not assembled: {w}")
    meta = load(w / "meta.yaml", {})
    if meta.get("status") == "completed":
        raise SystemExit(f"week already ingested: {s}")

    # Validate required Hermes outputs exist.
    for name in ("findings.yaml", "proposals.yaml", "coverage_editor.yaml", "weekly_report.md"):
        if not (w / name).exists():
            raise SystemExit(f"missing Hermes output: {w / name}")

    findings = load(w / "findings.yaml", [])
    proposals = load(w / "proposals.yaml", [])
    editor = load(w / "coverage_editor.yaml", [])
    research = load(w / "research.yaml", [])
    state = visible_state(backtest_id, s)
    labels = {en["label"] for en in state["entities"]}

    # Validate feed references are within the week and feed ids exist.
    feed_all = {x["item_id"] for x in load(w / "feed" / "all.yaml", {"entries": []}).get("entries", [])}
    for p in proposals:
        for ev in p.get("evidence", []):
            ref = ev.get("feed_id") if isinstance(ev, dict) else None
            if ref and ref not in feed_all:
                p["evidence_error"] = f"feed_id {ref} not in this week's feed"
        if p["type"] not in PROPOSAL_TYPES:
            p["evidence_error"] = "invalid proposal type"
        if not p.get("evidence"):
            p["evidence_error"] = "missing evidence"

    accepted, rejected = [], []
    seen = set()
    for p in proposals:
        reasons = []
        if p.get("evidence_error"):
            reasons.append(p["evidence_error"])
        # Duplicate-subject rejection applies to durable tracking proposals only.
        # Milestone and timeline updates for an already-tracked subject are
        # legitimate advances of that subject's history.
        if p["type"] in ("entity", "search_profile") and p["subject"] in labels:
            reasons.append("duplicate subject already tracked")
        if p["type"] == "alias" and p.get("target") not in labels:
            reasons.append("alias target not visible")
        if _is_sensitive(" ".join([str(p.get("subject", "")), str(p.get("rationale", ""))]),
                         p.get("sensitivity", "low")):
            reasons.append("sensitive subject excluded from simulated acceptance")
        key = (p["type"], p["subject"], p.get("target"))
        if key in seen:
            reasons.append("duplicate proposal")
        seen.add(key)
        if reasons:
            p = copy.deepcopy(p)
            p.update({"review_status": "rejected",
                      "reviewer": policy.get("reviewer", "hermes-simulated-evaluator"),
                      "rationale": p.get("rationale", "") + " | " + "; ".join(reasons)})
            rejected.append(p)
        else:
            p = copy.deepcopy(p)
            p.update({"review_status": "accepted",
                      "reviewer": policy.get("reviewer", "hermes-simulated-evaluator")})
            accepted.append(p)

    # Cap accepted per week.
    cap = policy.get("max_accepted_per_week", 12)
    if len(accepted) > cap:
        accepted, extra = accepted[:cap], accepted[cap:]
        rejected.extend(extra)

    next_state = visible_state(backtest_id, s + dt.timedelta(days=7))
    for p in accepted:
        apply_proposal(next_state, p)
    next_state["rejected_proposals"].extend(state.get("rejected_proposals", []))

    dump(w / "accepted_state.yaml", {
        "week_start": s.isoformat(),
        "available_on": (s + dt.timedelta(days=7)).isoformat(),
        "accepted": accepted, "rejected": rejected,
        "accepted_ids": [p["proposal_id"] for p in accepted],
        "rejected_ids": [p["proposal_id"] for p in rejected],
        "findings": findings,
    })
    dump(w / "next_state.yaml", next_state)
    meta["status"] = "completed"
    dump(w / "meta.yaml", meta)

    return {"week_start": s.isoformat(), "findings": len(findings),
            "proposals": len(proposals), "accepted": len(accepted),
            "rejected": len(rejected), "editor_gaps": len(editor),
            "research": len(research)}


# --------------------------------------------------------------------------- #
# Hidden evaluation
# --------------------------------------------------------------------------- #

def _subject_keywords(subject: str) -> list[str]:
    stop = {"the", "and", "or", "of", "for", "to", "a", "an", "silverleaf",
            "possible", "center", "academy", "school", "connector", "access",
            "facility", "campus", "widening", "improvements", "shortage",
            "restrictions", "zoning", "attendance", "boundaries",
            "cr", "sr", "igp", "us", "rd", "ct", "st"}
    return [k for k in re.findall(r"[A-Za-z0-9\-]{2,}", subject.lower()) if k not in stop]


def evaluate_week(backtest_id: str, week_start: str) -> dict:
    r = root(backtest_id)
    cfg = load(r / "config.yaml", {})
    hidden = cfg.get("hidden_evaluator", {})
    s = day(week_start)
    e = s + dt.timedelta(days=6)
    w = r / "weeks" / s.isoformat()
    meta = load(w / "meta.yaml", {})
    if meta.get("status") != "completed":
        return {"week_start": s.isoformat(), "status": "not_completed"}
    findings = load(w / "findings.yaml", [])
    accepted = load(w / "accepted_state.yaml", {}).get("accepted", [])
    editor = load(w / "coverage_editor.yaml", [])
    state_after = visible_state(backtest_id, e)

    known_subjects = {f.get("subject") for f in findings}
    promoted = {p.get("subject") for p in accepted}
    profiles = {p.get("subject") for p in state_after.get("search_profiles", [])}
    lanes = set(state_after.get("lanes", []))

    subject_targets = [x["subject"] for x in hidden.get("subjects", []) if x.get("priority") == "high"]
    lane_targets = [x["subject"] for x in hidden.get("lanes", []) if x.get("priority") == "high"]

    def hit(subject):
        kws = _subject_keywords(subject)
        if not kws:
            return False
        hay = " ".join(list(known_subjects) + list(promoted) + list(profiles)).lower()
        return any(k in hay for k in kws)

    found_subjects = [t for t in subject_targets if hit(t)]
    missed = [t for t in subject_targets if not hit(t)]
    found_lanes = [t for t in lane_targets if t in lanes]
    missed_lanes = [t for t in lane_targets if t not in lanes]
    found_set = set(found_subjects) | set(found_lanes)
    high_set = set(subject_targets) | set(lane_targets)
    rcr = round(len(found_set & high_set) / len(high_set), 3) if high_set else 0

    # Discovery lag: first feed evidence date for the subject vs first Hermes finding.
    feed_all = load(w / "feed" / "all.yaml", {"entries": []}).get("entries", [])
    lag = {}
    for t in found_subjects:
        kws = _subject_keywords(t)
        hay = " ".join([f.get("subject", "") for f in findings]).lower()
        if any(k in hay for k in kws):
            lag[t] = 0
    return {
        "findings": len(findings), "proposals": len(accepted),
        "editor_gaps": len(editor),
        "subjects_found": sorted(found_subjects),
        "subjects_missed": sorted(missed),
        "lanes_found": sorted(found_lanes),
        "lanes_missed": sorted(missed_lanes),
        "resident_coverage_recall": rcr,
        "high_priority_targets": len(high_set),
        "note": "Cumulative comparison is produced by evaluate_all (runs after Hermes completes).",
    }


def evaluate_all(backtest_id: str, as_of: str | None = None) -> dict:
    r = root(backtest_id)
    cfg = load(r / "config.yaml", {})
    hidden = cfg.get("hidden_evaluator", {})
    cutoff = day(as_of) if as_of else day(cfg["end"])

    known_subjects: set[str] = set()
    promoted: set[str] = set()
    profiles: set[str] = set()
    lanes: set[str] = set()
    aliases: list[dict] = []
    findings_total = proposals_total = editor_gaps = 0
    first_found: dict[str, dt.date] = {}

    subject_targets = [x["subject"] for x in hidden.get("subjects", [])]
    lane_targets = [x["subject"] for x in hidden.get("lanes", [])]

    completed = []
    for path in sorted((r / "weeks").glob("*/meta.yaml")):
        meta = load(path, {})
        if meta.get("status") != "completed":
            continue
        ws = day(meta["week_start"])
        if ws > cutoff:
            continue
        completed.append(path.parent)
    for w in completed:
        meta = load(w / "meta.yaml", {})
        ws = day(meta["week_start"])
        findings = load(w / "findings.yaml", [])
        accepted = load(w / "accepted_state.yaml", {}).get("accepted", [])
        editor = load(w / "coverage_editor.yaml", [])
        findings_total += len(findings)
        proposals_total += len(accepted)
        editor_gaps += len(editor)
        for f in findings:
            subj = f.get("subject")
            if subj:
                known_subjects.add(subj)
                first_found.setdefault(subj, ws)
        for p in accepted:
            promoted.add(p.get("subject"))
            if p["type"] == "search_profile":
                profiles.add(p["subject"])
            if p["type"] == "coverage_lane":
                lanes.add(p["subject"])
            if p["type"] == "alias":
                aliases.append({"value": p["subject"], "target": p.get("target"),
                                "week": meta["week_start"]})

    haystack = " ".join(list(known_subjects) + list(promoted) + list(profiles)).lower()

    def hit(subject):
        kws = _subject_keywords(subject)
        return bool(kws) and any(k in haystack for k in kws)

    found_subjects = [t for t in subject_targets if hit(t)]
    missed_subjects = [t for t in subject_targets if not hit(t)]
    found_lanes = [t for t in lane_targets if t in lanes]
    missed_lanes = [t for t in lane_targets if t not in lanes]
    # Resident Coverage Recall is computed over HIGH-priority targets only
    # (Task 22 §25); the found/missed lists above include all targets for
    # inspection.
    high_subject_targets = [x["subject"] for x in hidden.get("subjects", [])
                            if x.get("priority") == "high"]
    high_lane_targets = [x["subject"] for x in hidden.get("lanes", [])
                         if x.get("priority") == "high"]
    high_found = ([t for t in high_subject_targets if hit(t)]
                  + [t for t in high_lane_targets if t in lanes])
    high_set = set(high_subject_targets) | set(high_lane_targets)
    rcr = round(len(set(high_found) & high_set) / len(high_set), 3) if high_set else 0

    discovery_week = {}
    for t in found_subjects:
        kws = _subject_keywords(t)
        best = None
        for w in completed:
            meta = load(w / "meta.yaml", {})
            ws = day(meta["week_start"])
            findings = load(w / "findings.yaml", [])
            text = " ".join([f.get("subject", "") for f in findings]).lower()
            if any(k in text for k in kws):
                best = ws
                break
        if best:
            discovery_week[t] = best.isoformat()

    return {
        "as_of": cutoff.isoformat(),
        "weeks_completed": len(completed),
        "findings_total": findings_total,
        "accepted_proposals_total": proposals_total,
        "editor_gaps_total": editor_gaps,
        "subjects_found": sorted(found_subjects),
        "subjects_missed": sorted(missed_subjects),
        "lanes_found": sorted(found_lanes),
        "lanes_missed": sorted(missed_lanes),
        "resident_coverage_recall": rcr,
        "discovery_week_by_subject": discovery_week,
        "search_profiles_created": sorted(profiles),
        "lanes_created": sorted(lanes),
        "aliases_learned": aliases,
        "note": "Hidden evaluator; never exposed to a Hermes week packet.",
    }


# --------------------------------------------------------------------------- #
# Publication snapshot (backtest-only)
# --------------------------------------------------------------------------- #

def publication_snapshot(backtest_id: str, as_of: str) -> Path:
    """Markdown release inventory showing what Hermes would publish at a date."""
    r = root(backtest_id)
    cutoff = day(as_of)
    state = visible_state(backtest_id, cutoff)
    latest = []
    for path in sorted((r / "weeks").glob("*/accepted_state.yaml")):
        acc = load(path, {})
        if day(acc.get("available_on", "9999-12-31")) <= cutoff:
            for p in acc.get("accepted", []):
                if p["type"] in ("entity", "search_profile", "timeline_reconciliation"):
                    latest.append(p)
    lines = [
        f"# Hermes backtest publication snapshot — {cutoff.isoformat()}",
        "",
        f"Backtest: {backtest_id}",
        f"Tracked entities: {len(state['entities'])}",
        f"Search profiles: {len(state['search_profiles'])}",
        f"Lanes: {len(state['lanes'])}",
        f"Milestones: {len(state['milestones'])}",
        f"Timeline events: {len(state['timelines'])}",
        "",
        "## Would publish (resident-facing inventory)",
        "",
    ]
    for p in latest:
        rationale = " ".join((p.get("rationale") or "").split())[:100].rstrip()
        lines.append(f"- [{p['type']}] {p.get('subject')} — {rationale}")
    if not latest:
        lines.append("- _No publishable inventory yet at this date._")
    out = r / "publication" / cutoff.isoformat() / "inventory.md"
    dump_md(out, "\n".join(lines) + "\n")
    return out


def dump_md(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def monthly_summaries(backtest_id: str) -> list[Path]:
    """Aggregate weekly outputs into monthly syntheses (months/YYYY-MM.yaml).

    Runs after Hermes completes the weeks in a month. Each synthesis reports
    new subjects, search profiles, aliases, lanes, timeline events, editor
    gaps, and false positives for the month.
    """
    r = root(backtest_id)
    months: dict[str, dict] = {}
    for path in sorted((r / "weeks").glob("*/meta.yaml")):
        meta = load(path, {})
        if meta.get("status") != "completed":
            continue
        w = path.parent
        key = meta["week_start"][:7]
        m = months.setdefault(key, {
            "month": key, "weeks": 0, "new_subjects": [], "search_profiles": [],
            "aliases": [], "lanes": [], "timeline_events": 0,
            "editor_gaps": 0, "false_positives": 0, "findings": 0,
        })
        m["weeks"] += 1
        findings = load(w / "findings.yaml", [])
        acc = load(w / "accepted_state.yaml", {"accepted": [], "rejected": []})
        m["findings"] += len(findings)
        m["editor_gaps"] += len(load(w / "coverage_editor.yaml", []))
        m["false_positives"] += len(acc.get("rejected", []))
        for f in findings:
            subj = f.get("subject")
            if subj and subj not in m["new_subjects"]:
                m["new_subjects"].append(subj)
        for p in acc.get("accepted", []):
            if p["type"] == "search_profile" and p["subject"] not in m["search_profiles"]:
                m["search_profiles"].append(p["subject"])
            if p["type"] == "alias":
                m["aliases"].append({"value": p["subject"], "target": p.get("target")})
            if p["type"] == "coverage_lane" and p["subject"] not in m["lanes"]:
                m["lanes"].append(p["subject"])
            if p["type"] == "timeline_reconciliation":
                m["timeline_events"] += 1
    out = []
    for key in sorted(months):
        p = r / "months" / f"{key}.yaml"
        dump(p, months[key])
        out.append(p)
    return out


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="Hermes-operated historical backtest infrastructure.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("build-feed"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--rebuild", action="store_true")

    p = sub.add_parser("assemble-week"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--week-start", required=True); p.add_argument("--overwrite", action="store_true")

    p = sub.add_parser("ingest-week"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--week-start", required=True)

    p = sub.add_parser("evaluate-week"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--week-start", required=True)

    p = sub.add_parser("evaluate-all"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--as-of", default=None)

    p = sub.add_parser("snapshot"); p.add_argument("--backtest-id", required=True)
    p.add_argument("--as-of", required=True)

    p = sub.add_parser("monthly"); p.add_argument("--backtest-id", required=True)

    args = ap.parse_args()
    if args.cmd == "build-feed":
        out = build_feed(args.backtest_id, args.rebuild)
        print(f"feed built: {out}")
    elif args.cmd == "assemble-week":
        print(assemble_week(args.backtest_id, args.week_start, args.overwrite))
    elif args.cmd == "ingest-week":
        print(ingest_week(args.backtest_id, args.week_start))
    elif args.cmd == "evaluate-week":
        import json
        print(json.dumps(evaluate_week(args.backtest_id, args.week_start), indent=2, sort_keys=True))
    elif args.cmd == "evaluate-all":
        import json
        print(json.dumps(evaluate_all(args.backtest_id, args.as_of), indent=2, sort_keys=True))
    elif args.cmd == "snapshot":
        print(publication_snapshot(args.backtest_id, args.as_of))
    elif args.cmd == "monthly":
        for p in monthly_summaries(args.backtest_id):
            print(p)


if __name__ == "__main__":
    main()
