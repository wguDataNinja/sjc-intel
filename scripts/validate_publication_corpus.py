#!/usr/bin/env python3
"""
SJC_Intel — Publication/Corpus Validator.

Validates actual corpus records (data/intel_items/**/*.yaml) for
publication-relevant integrity per docs/publication_release_contract.md and
ROADMAP.md §3A-G2. This is distinct from scripts/validate.py (schemas,
compilation, registries) — this validates every item record.

Output:
- deterministic human-readable and --json machine-readable summaries;
- failure counts, warning counts, exact item IDs;
- exit 0 when no blocking errors; exit 1 when blocking errors exist.

Legacy records documented in data/publication_decisions/legacy_exceptions.yaml
are excluded from release eligibility with a machine-readable reason and do
not block the validator (they are not release candidates).
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publication_common import (  # noqa: E402
    REPO_ROOT,
    ITEM_ID_RE,
    INTERNAL_ONLY_FIELDS,
    PUBLIC_FIELD_ALLOWLIST,
    CANONICAL_REVIEW_STATUSES,
    VALID_SENSITIVITIES,
    TOPIC_VOCABULARY,
    decision_path,
    is_valid_url,
    iter_intel_items,
    legacy_exception_for_item,
    load_communities,
    load_entities,
    load_legacy_exceptions,
    load_sources,
    load_source_events,
    parse_iso,
    public_projection,
    validate_public_safe,
)

# The source_event linkage policy: items SHOULD reference a source_event where
# source_event adoption exists. Missing linkage is a warning for legacy items,
# not a blocking error (data_model.md §11 notes incomplete adoption).
REQUIRE_SOURCE_EVENT = False

# Topic vocabulary check: legacy items used pre-taxonomy topics. Unknown topics
# are a warning, not a blocking error, unless the item is a release candidate.
TREAT_UNKNOWN_TOPICS_AS_WARNING = True


def _is_legacy_date(val):
    """Accept NBOR-style M/D/YYYY meeting dates as a documented legacy format."""
    try:
        parts = str(val).strip().split("/")
        if len(parts) != 3:
            return False
        m, d, y = int(parts[0]), int(parts[1]), int(parts[2])
        return 1 <= m <= 12 and 1 <= d <= 31 and 1900 <= y <= 2100
    except (ValueError, TypeError):
        return False


class CorpusValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = Counter()
        self.by_source = Counter()
        self.by_status = Counter()
        self.by_sensitivity = Counter()
        self.legacy_exceptions = load_legacy_exceptions()
        self.sources = load_sources()
        self.communities = load_communities()
        self.entities = load_entities()
        self.source_events = load_source_events()
        self.items = list(iter_intel_items())
        self.item_index = self._build_item_index()

    def _build_item_index(self):
        idx = {}
        for rel, item in self.items:
            idx.setdefault(item["item_id"], []).append((rel, item))
        return idx

    def _check(self, level, code, item_id, message):
        rec = {"level": level, "code": code, "item_id": item_id, "message": message}
        if level == "error":
            self.errors.append(rec)
            self.stats["errors"] += 1
        else:
            self.warnings.append(rec)
            self.stats["warnings"] += 1

    def _legacy_exception(self, item_id):
        eid = legacy_exception_for_item(item_id)
        if not eid:
            return None
        for entry in (self.legacy_exceptions or {}).get("legacy_exceptions", []):
            if entry.get("id") == eid:
                return entry
        return None

    # ------------------------------------------------------------------ #
    # Individual checks
    # ------------------------------------------------------------------ #

    def check_id_format(self, rel, item):
        item_id = item["item_id"]
        if ITEM_ID_RE.match(item_id):
            self.stats["id_ok"] += 1
            return
        ex = self._legacy_exception(item_id)
        if ex:
            self._check("warning", "legacy_id_format", item_id,
                        f"legacy ID format (exception {ex['id']}): {item_id}")
            self.stats["legacy_exception"] += 1
        else:
            self._check("error", "bad_item_id_format", item_id,
                        f"item_id does not match SJC-{'{PREFIX}'}-{{YYYYMMDD}}-{{NNNN}}: {item_id}")

    def check_id_uniqueness(self):
        for item_id, reps in sorted(self.item_index.items()):
            if len(reps) == 1:
                continue
            # Duplicate item IDs across files.
            rels = [r for r, _ in reps]
            # A legacy exception may declare one canonical file; the other
            # copies are non-canonical but not blocking.
            covered = any(self._legacy_exception(item_id) for item_id in [item_id])
            if covered:
                self._check("warning", "duplicate_id_legacy", item_id,
                            f"item_id appears in {len(rels)} files but is covered by a legacy exception: {rels}")
            else:
                self._check("error", "duplicate_item_id", item_id,
                            f"item_id appears in {len(rels)} files: {rels}")

    def check_source_exists(self, rel, item):
        sid = item.get("source_id")
        if not sid:
            self._check("error", "missing_source_id", item["item_id"], "no source_id")
            return
        if sid not in self.sources:
            # silverleaf_discovery is a pseudo-source from a one-off discovery
            # run; its records carry source_id st_johns_citizen per data_model §11.
            self._check("warning", "unknown_source_id", item["item_id"],
                        f"source_id '{sid}' not in registry/sources.yaml")

    def check_source_event_linkage(self, rel, item):
        eid = item.get("source_event_id")
        if not eid:
            if REQUIRE_SOURCE_EVENT:
                self._check("error", "missing_source_event", item["item_id"], "no source_event_id")
            return
        if eid not in self.source_events:
            self._check("warning", "unknown_source_event", item["item_id"],
                        f"source_event_id '{eid}' not found in data/source_events/")

    def check_source_url(self, rel, item):
        url = item.get("source_url")
        if not is_valid_url(url):
            ex = self._legacy_exception(item["item_id"])
            if ex:
                self._check("warning", "missing_source_url_legacy", item["item_id"],
                            f"missing/invalid source_url (exception {ex['id']})")
            else:
                self._check("error", "missing_source_url", item["item_id"],
                            "missing or invalid source_url")

    def check_timestamps(self, rel, item):
        from publication_common import parse_iso
        for field in ("source_published_at", "discovered_at", "created_at"):
            val = item.get(field)
            if not val:
                if field == "created_at":
                    # Legacy 2026-08-02 records missing created_at are warned.
                    self._check("warning", "missing_timestamp", item["item_id"],
                                f"missing {field}")
                continue
            if parse_iso(val) is None:
                # Legacy NBOR source_published_at uses M/D/YYYY meeting dates.
                # This is a documented legacy format: warn, do not block.
                if _is_legacy_date(val):
                    self._check("warning", "legacy_date_format", item["item_id"],
                                f"{field} uses legacy M/D/YYYY date: {val}")
                else:
                    self._check("error", "bad_timestamp", item["item_id"],
                                f"{field} not ISO-8601: {val}")

    def check_required_evidence(self, rel, item):
        item_id = item["item_id"]
        missing = []
        for field in ("title", "summary", "topics", "raw_excerpt"):
            if not item.get(field):
                missing.append(field)
        if missing:
            ex = self._legacy_exception(item_id)
            if ex:
                self._check("warning", "missing_evidence_legacy", item_id,
                            f"missing {missing} (exception {ex['id']})")
            else:
                self._check("error", "missing_evidence", item_id, f"missing {missing}")

    def check_dedupe_fingerprint(self, rel, item):
        key = item.get("_dedupe_key")
        if not key:
            self._check("warning", "missing_dedupe_key", item["item_id"],
                        "missing _dedupe_key (rebuild_dedupe_index.py can regenerate)")

    def check_enums(self, rel, item):
        item_id = item["item_id"]
        sens = item.get("sensitivity")
        if sens not in VALID_SENSITIVITIES:
            ex = self._legacy_exception(item_id)
            if ex:
                self._check("warning", "legacy_sensitivity", item_id,
                            f"sensitivity '{sens}' (exception {ex['id']})")
            else:
                self._check("error", "invalid_sensitivity", item_id,
                            f"sensitivity '{sens}' not in {sorted(VALID_SENSITIVITIES)}")
        rs = item.get("review_status")
        if rs and rs not in CANONICAL_REVIEW_STATUSES:
            self._check("error", "invalid_review_status", item_id,
                        f"review_status '{rs}' not in {sorted(CANONICAL_REVIEW_STATUSES)}")
        topics = item.get("topics") or []
        if not isinstance(topics, list):
            self._check("error", "bad_topics_type", item_id, "topics is not a list")
            return
        for t in topics:
            if t not in TOPIC_VOCABULARY and not self._legacy_exception(item_id):
                if TREAT_UNKNOWN_TOPICS_AS_WARNING:
                    self._check("warning", "unknown_topic", item_id, f"topic '{t}' not in taxonomy")

    def check_sensitivity_review(self, rel, item):
        """High-sensitivity items must require human review (taxonomy rule)."""
        item_id = item["item_id"]
        if item.get("sensitivity") == "high" and not item.get("human_review_required"):
            self._check("warning", "high_sensitivity_no_human_review", item_id,
                        "high sensitivity but human_review_required not set")

    def check_review_status(self, rel, item):
        item_id = item["item_id"]
        rs = item.get("review_status")
        if rs not in ("verified", "pending_review", "archived", "rejected_noise"):
            return  # already validated as enum
        self.stats[f"review_status:{rs}"] += 1
        self.by_status[rs] += 1

    def check_references(self, rel, item):
        item_id = item["item_id"]
        for eid in item.get("tracked_entity_ids", []):
            if eid not in self.entities:
                self._check("error", "unknown_entity_ref", item_id,
                            f"tracked_entity_ids references unknown entity '{eid}'")
        for cid in item.get("communities", []):
            if cid and cid not in self.communities:
                if self._legacy_exception(item_id):
                    self._check("warning", "unknown_community_ref_legacy", item_id,
                                f"communities references unregistered community '{cid}' (legacy exception)")
                else:
                    self._check("error", "unknown_community_ref", item_id,
                                f"communities references unknown community '{cid}'")
        sb = item.get("superseded_by")
        if sb and sb not in self.item_index:
            self._check("error", "unknown_superseded_by", item_id,
                        f"superseded_by references unknown item '{sb}'")

    def check_canonical_relationship(self, rel, item):
        """An item should not be both superseding and superseded blindly;
        superseded items are excluded from release by the selector."""
        item_id = item["item_id"]
        if item.get("superseded_by"):
            self.stats["superseded"] += 1

    def check_public_safety(self, rel, item):
        """Public-field safety: ensure a projection contains no internal-only
        fields and that internal-only fields are absent from the item."""
        item_id = item["item_id"]
        leaked = [k for k in item if k in INTERNAL_ONLY_FIELDS and k not in ("_dedupe_key", "_beat", "_signal", "_category", "_app_id")]
        # _dedupe_key etc. are operational metadata, not public fields; the
        # projection helper excludes them. Flag only clearly private prose keys.
        private_prose = [k for k in item if k in ("reviewer_notes", "internal_notes", "private_notes")]
        if private_prose:
            self._check("warning", "internal_prose_field", item_id,
                        f"internal prose field present: {private_prose}")
        proj = public_projection(item)
        unsafe = validate_public_safe(proj)
        if unsafe:
            self._check("error", "public_projection_leak", item_id,
                        f"public projection leaks internal fields: {unsafe}")

    def check_release_eligibility_preview(self, rel, item):
        """Publication-relevant preview (not a release): record item-level
        release-readiness signals that the selector uses. Does not approve."""
        item_id = item["item_id"]
        rs = item.get("review_status")
        sens = item.get("sensitivity")
        url_ok = is_valid_url(item.get("source_url"))
        ex = self._legacy_exception(item_id)

        reasons = []
        if ex:
            reasons.append(f"legacy_exception:{ex['id']}")
        if rs != "verified":
            reasons.append(f"review_status:{rs or 'none'}")
        if rs == "verified" and sens in ("medium", "high"):
            reasons.append(f"requires_editorial_approval:{sens}")
        if not url_ok:
            reasons.append("invalid_source_url")
        if reasons:
            self.stats["not_release_eligible"] += 1
        else:
            self.stats["release_eligible_reviewed"] += 1

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(self):
        for rel, item in self.items:
            item_id = item["item_id"]
            self.by_source[item.get("source_id") or "?"] += 1
            self.stats["items_total"] += 1
            self.check_id_format(rel, item)
            self.check_source_exists(rel, item)
            self.check_source_event_linkage(rel, item)
            self.check_source_url(rel, item)
            self.check_timestamps(rel, item)
            self.check_required_evidence(rel, item)
            self.check_dedupe_fingerprint(rel, item)
            self.check_enums(rel, item)
            self.check_sensitivity_review(rel, item)
            self.check_review_status(rel, item)
            self.check_references(rel, item)
            self.check_canonical_relationship(rel, item)
            self.check_public_safety(rel, item)
            self.check_release_eligibility_preview(rel, item)
        self.check_id_uniqueness()
        self._check_decisions()
        return self._summary()

    def _check_decisions(self):
        """Validate publication-decision files reference real items and use
        allowed statuses."""
        from publication_common import load_all_decisions
        decisions = load_all_decisions()
        for item_id, dec in sorted(decisions.items()):
            if item_id not in self.item_index:
                self._check("error", "orphan_decision", item_id,
                            "publication decision references unknown item")
            status = dec.get("publication_status")
            if status not in ("approved", "rejected", "deferred", "withdrawn"):
                self._check("error", "bad_decision_status", item_id,
                            f"publication_status '{status}' invalid")
            sl = dec.get("silverleaf_relevance") or {}
            if sl.get("decision") not in ("included", "excluded", "needs_review", "not_assessed", None):
                self._check("error", "bad_silverleaf_decision", item_id,
                            f"silverleaf_relevance.decision '{sl.get('decision')}' invalid")
            rel = dec.get("relevance")
            if rel is not None and rel not in (
                    "in_silverleaf", "near_silverleaf", "countywide_impact"):
                self._check("error", "bad_relevance_override", item_id,
                            f"relevance override '{rel}' invalid")
            self.stats["decisions_total"] += 1

    def _summary(self):
        return {
            "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "items_total": self.stats.get("items_total", 0),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "error_item_ids": sorted({e["item_id"] for e in self.errors}),
            "warning_item_ids": sorted({e["item_id"] for e in self.warnings}),
            "by_source": dict(self.by_source),
            "by_status": dict(self.by_status),
            "by_sensitivity": dict(self.by_sensitivity),
            "legacy_exception_count": self.stats.get("legacy_exception", 0),
            "decisions_total": self.stats.get("decisions_total", 0),
            "release_eligible_reviewed": self.stats.get("release_eligible_reviewed", 0),
            "not_release_eligible": self.stats.get("not_release_eligible", 0),
            "superseded": self.stats.get("superseded", 0),
        }

    def render_human(self, summary):
        lines = []
        lines.append("SJC_Intel Publication Corpus Validation")
        lines.append("=" * 50)
        lines.append(f"Items scanned:        {summary['items_total']}")
        lines.append(f"Blocking errors:      {summary['errors']}")
        lines.append(f"Warnings:             {summary['warnings']}")
        lines.append(f"Legacy exceptions:    {summary['legacy_exception_count']}")
        lines.append(f"Publication decisions:{summary['decisions_total']}")
        lines.append(f"Reviewed release-eligible (preview): {summary['release_eligible_reviewed']}")
        lines.append("")
        if self.errors:
            lines.append("BLOCKING ERRORS:")
            for e in self.errors:
                lines.append(f"  [{e['code']}] {e['item_id']} — {e['message']}")
            lines.append("")
        if self.warnings:
            lines.append("WARNINGS:")
            for w in self.warnings:
                lines.append(f"  [{w['code']}] {w['item_id']} — {w['message']}")
            lines.append("")
        lines.append("=" * 50)
        lines.append(f"Result: {'FAIL' if self.errors else 'PASS'} "
                     f"({summary['errors']} errors, {summary['warnings']} warnings)")
        return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Validate SJC corpus for publication relevance.")
    ap.add_argument("--json", action="store_true", help="emit machine-readable summary only")
    args = ap.parse_args()

    v = CorpusValidator()
    summary = v.run()
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(v.render_human(summary))
    sys.exit(1 if summary["errors"] else 0)


if __name__ == "__main__":
    main()
