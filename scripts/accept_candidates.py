#!/usr/bin/env python3
"""
SJC_Intel — human-gated candidate acceptance.

Decides a staged weekly-bundle intelligence candidate:

    python3 scripts/accept_candidates.py --run-id <run_id> --candidate-id <id> \
        --decision accept|reject|defer --reviewer <name> [--notes <text>] \
        [--dry-run]

Guarantees (contract: docs/weekly_operational_contract.md §5):

  * candidates are NEVER auto-accepted; a human must choose explicitly;
  * an accepted candidate becomes a corpus intel_item with
    review_status=pending_review (never verified/published);
  * dedupe index and review queue are rebuilt with the EXISTING tooling
    (scripts/rebuild_dedupe_index.py, scripts/build_review_queue.py), which
    preserves prior review decisions;
  * rejected/deferred candidates leave a durable decision record and their
    evidence intact; nothing is deleted;
  * source proposals are never promoted here — registry/sources.yaml is
    untouched by this command.

Decision records: data/incoming/{run_id}/decisions/{item_id}.yaml
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import yaml

try:
    from scripts.bundle_common import manifest_path, read_json, valid_run_id, write_json
except ImportError:
    from bundle_common import manifest_path, read_json, valid_run_id, write_json

DEFAULT_INCOMING_ROOT = "data/incoming"
DEFAULT_INTEL_ROOT = "data/intel_items"
DEFAULT_INDEX_FILE = "data/index/prior_items.yaml"
DEFAULT_QUEUE_DIR = "data/review_queue"

VALID_DECISIONS = {"accept", "reject", "defer"}

REQUIRED_CANDIDATE_FIELDS = [
    "item_id", "title", "summary", "source_id", "source_url", "discovered_at",
    "raw_excerpt", "topics", "geographic_scope", "urgency",
    "verification_status", "sensitivity", "human_review_required",
]


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_candidates(incoming_root, run_id):
    """Return {item_id: (file, candidate)} for a staged run."""
    stage = os.path.join(incoming_root, run_id)
    if not os.path.isdir(stage):
        return {}
    out = {}
    cand_dir = os.path.join(stage, "intel_candidates")
    if not os.path.isdir(cand_dir):
        return out
    for name in sorted(os.listdir(cand_dir)):
        if not name.endswith(".json"):
            continue
        try:
            data = read_json(os.path.join(cand_dir, name))
        except Exception:
            continue
        for item in data.get("items", []):
            item_id = item.get("item_id")
            if item_id:
                out[item_id] = (os.path.join(cand_dir, name), item)
    return out


def candidate_to_corpus_record(cand, origin_run_id, origin_bundle_id,
                               reviewer, imported_at):
    """Map a candidate to an intel_item record (review_status: pending_review).

    Drops candidate-lifecycle fields (status/outcome/_* internals) so the
    accepted record reads as a corpus intel_item; provenance is carried in
    _origin_* metadata.
    """
    record = {}
    drop = {"status", "outcome", "review_status"}
    for k, v in cand.items():
        if k.startswith("_") or k in drop:
            continue
        record[k] = v
    record["review_status"] = "pending_review"
    record["created_at"] = imported_at
    record["updated_at"] = imported_at
    record["_origin_run_id"] = origin_run_id
    record["_origin_bundle_id"] = origin_bundle_id
    record["_import_decision"] = "accept"
    record["_imported_at"] = imported_at
    record["_reviewer"] = reviewer
    return record


def load_existing_items(intel_root, date_dir, source_id):
    """Load the existing corpus YAML for a source/date (or empty)."""
    path = os.path.join(intel_root, date_dir, f"{source_id}.yaml")
    if not os.path.exists(path):
        return path, []
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return path, list(data.get("items", []))


def dedupe_key_of(cand, source_id):
    key = cand.get("_dedupe_key")
    if key:
        return key
    url = cand.get("source_url", "")
    if url:
        return hashlib.sha256(f"{source_id}||{url}".encode()).hexdigest()[:16]
    title = cand.get("title", "")
    date = cand.get("source_published_at", cand.get("discovered_at", ""))
    return hashlib.sha256(f"{source_id}||{title}||{date}".encode()).hexdigest()[:16]


def load_index_keys(index_file):
    if not os.path.exists(index_file):
        return set()
    with open(index_file) as f:
        data = yaml.safe_load(f) or {}
    return {e.get("key") for e in data.get("prior_items", [])}


def next_item_id(item_id, intel_root, source_id):
    """Reuse candidate item_id if unique; else generate SJC-{prefix}-{date}-{NNNN}."""
    existing = set()
    if os.path.isdir(intel_root):
        for date_dir in os.listdir(intel_root):
            path = os.path.join(intel_root, date_dir, f"{source_id}.yaml")
            if os.path.isfile(path):
                try:
                    with open(path) as f:
                        data = yaml.safe_load(f) or {}
                    existing.update(i.get("item_id") for i in data.get("items", []))
                except Exception:
                    pass
    if item_id and item_id not in existing:
        return item_id
    parts = (item_id or "SJC-XX-00000000-0000").split("-")
    prefix = parts[1] if len(parts) > 1 else "XX"
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    n = 1
    while f"SJC-{prefix}-{today}-{n:04d}" in existing:
        n += 1
    return f"SJC-{prefix}-{today}-{n:04d}"


def write_decision_record(incoming_root, run_id, item_id, decision_dict):
    dec_dir = os.path.join(incoming_root, run_id, "decisions")
    os.makedirs(dec_dir, exist_ok=True)
    path = os.path.join(dec_dir, f"{item_id}.yaml")
    with open(path, "w") as f:
        yaml.dump(decision_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return path


def decision_record_exists(incoming_root, run_id, item_id):
    path = os.path.join(incoming_root, run_id, "decisions", f"{item_id}.yaml")
    return os.path.exists(path)


def rebuild_dedupe_and_queue(intel_root, index_file, queue_dir):
    """Reuse existing tooling to rebuild dedupe index + review queue."""
    try:
        import scripts.rebuild_dedupe_index as rdi
        import scripts.build_review_queue as brq
    except ImportError:  # standalone: python3 scripts/accept_candidates.py
        import rebuild_dedupe_index as rdi
        import build_review_queue as brq

    rdi.INTEL_ITEMS_DIR = intel_root
    rdi.INDEX_FILE = index_file
    items = rdi.collect_all_items()
    items = rdi.deduplicate(items)
    rdi.deduped_items = items
    # Write using the tool's own serializer (same header contract).
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    with open(index_file, "w") as f:
        f.write("# =============================================================================\n")
        f.write("# SJC_Intel — Prior Items Dedupe Index\n")
        f.write("# =============================================================================\n")
        f.write("# Tracks item fingerprints for deduplication across monitor cycles.\n")
        f.write("#\n")
        f.write("# Schema version: 1.1\n")
        f.write(f"# Last updated: {now[:10]}\n")
        f.write("# Updated by: rebuild_dedupe_index.py (via accept_candidates.py)\n")
        f.write("# =============================================================================\n")
        f.write("\n")
        yaml.dump({"prior_items": items}, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    brq.INTEL_ITEMS_DIR = intel_root
    brq.QUEUE_DIR = queue_dir
    brq.QUEUE_FILE = os.path.join(queue_dir, "queue.yaml")
    brq.SUMMARY_FILE = os.path.join(queue_dir, "summary.yaml")
    entries = brq.collect_items()
    entries = brq.deduplicate(entries)
    for e in entries:
        e["escalation"] = brq.compute_escalation(e)
    summary = brq.build_summary(entries)
    brq.write_queue(entries, summary)
    return len(items), len(entries)


def plan(run_id, item_id, cand, decision, reviewer, notes, incoming_root,
         intel_root, index_file, queue_dir, origin_bundle_id):
    source_id = cand["source_id"]
    key = dedupe_key_of(cand, source_id)
    existing_keys = load_index_keys(index_file)
    date_dir = (cand.get("discovered_at") or utc_now_iso())[:10]
    new_item_id = next_item_id(cand.get("item_id"), intel_root, source_id)
    return {
        "run_id": run_id,
        "item_id": new_item_id,
        "candidate_id": cand.get("item_id"),
        "source_id": source_id,
        "title": cand.get("title", ""),
        "decision": decision,
        "reviewer": reviewer,
        "dedupe_key": key,
        "dedupe_status": "already_indexed" if key in existing_keys else "new",
        "target_corpus_file": os.path.join(intel_root, date_dir, f"{source_id}.yaml"),
        "would_update_dedupe_index": key not in existing_keys,
        "would_rebuild_review_queue": True,
        "origin_bundle_id": origin_bundle_id,
        "notes": notes,
    }


def decide(run_id, item_id, cand, decision, reviewer, notes, incoming_root,
           intel_root, index_file, queue_dir, dry_run=False, origin_bundle_id=None):
    """Perform a decision. Returns (status, message, plan)."""
    if decision not in VALID_DECISIONS:
        raise ValueError(f"invalid decision: {decision!r}")
    missing = [f for f in REQUIRED_CANDIDATE_FIELDS if f not in cand]
    if missing:
        return ("failed", f"candidate missing required fields: {missing}", None)

    p = plan(run_id, item_id, cand, decision, reviewer, notes, incoming_root,
             intel_root, index_file, queue_dir, origin_bundle_id)

    if decision == "accept":
        if next_item_id(cand.get("item_id"), intel_root, cand["source_id"]) != cand.get("item_id") \
                and _item_in_corpus(intel_root, cand["source_id"], cand.get("item_id")):
            return ("already_accepted", f"candidate {cand.get('item_id')} is already in the corpus", p)
        if dry_run:
            return ("dry_run", "acceptance plan ready (no mutation)", p)

        imported_at = utc_now_iso()
        record = candidate_to_corpus_record(cand, run_id, origin_bundle_id, reviewer, imported_at)
        final_id = next_item_id(cand.get("item_id"), intel_root, cand["source_id"])
        record["item_id"] = final_id
        date_dir = (cand.get("discovered_at") or imported_at)[:10]
        path, items = load_existing_items(intel_root, date_dir, cand["source_id"])
        if any(i.get("item_id") == final_id for i in items):
            return ("already_accepted", f"item {final_id} already in {path}", p)
        items.append(record)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            yaml.dump({"source_id": cand["source_id"], "items": items}, f,
                      default_flow_style=False, sort_keys=False, allow_unicode=True)

        decision_dict = {
            "decision_id": f"DEC-{run_id}-{final_id}",
            "item_id": final_id,
            "candidate_id": cand.get("item_id"),
            "run_id": run_id,
            "bundle_id": origin_bundle_id,
            "source_id": cand["source_id"],
            "title": cand.get("title"),
            "source_url": cand.get("source_url"),
            "discovered_at": cand.get("discovered_at"),
            "dedupe_key": p["dedupe_key"],
            "decision": "accept",
            "reviewer": reviewer,
            "decided_at": imported_at,
            "notes": notes or "",
            "accepted_to": path,
        }
        write_decision_record(incoming_root, run_id, final_id, decision_dict)
        rebuild_dedupe_and_queue(intel_root, index_file, queue_dir)
        return ("accepted", f"accepted {final_id} -> {path}; dedupe + queue rebuilt", p)

    # reject / defer — auditable decision record, evidence preserved.
    if dry_run:
        return ("dry_run", f"{decision} plan ready (no mutation)", p)
    if decision_record_exists(incoming_root, run_id, item_id):
        return ("already_decided", f"{item_id} already has a decision record", p)
    decision_dict = {
        "decision_id": f"DEC-{run_id}-{item_id}",
        "item_id": item_id,
        "candidate_id": cand.get("item_id"),
        "run_id": run_id,
        "bundle_id": origin_bundle_id,
        "source_id": cand["source_id"],
        "title": cand.get("title"),
        "source_url": cand.get("source_url"),
        "discovered_at": cand.get("discovered_at"),
        "dedupe_key": p["dedupe_key"],
        "decision": decision,
        "reviewer": reviewer,
        "decided_at": utc_now_iso(),
        "notes": notes or "",
        "rejection_reason": notes or "",
    }
    path = write_decision_record(incoming_root, run_id, item_id, decision_dict)
    return (decision + "ed", f"{decision} recorded -> {path} (evidence preserved)", p)


def _item_in_corpus(intel_root, source_id, item_id):
    if not os.path.isdir(intel_root):
        return False
    for date_dir in os.listdir(intel_root):
        path = os.path.join(intel_root, date_dir, f"{source_id}.yaml")
        if os.path.isfile(path):
            try:
                with open(path) as f:
                    data = yaml.safe_load(f) or {}
                if any(i.get("item_id") == item_id for i in data.get("items", [])):
                    return True
            except Exception:
                pass
    return False


def main():
    parser = argparse.ArgumentParser(description="Human-gated candidate acceptance.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--candidate-id", required=True, help="Candidate item_id.")
    parser.add_argument("--decision", required=True, choices=sorted(VALID_DECISIONS))
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--incoming-root", default=DEFAULT_INCOMING_ROOT)
    parser.add_argument("--intel-root", default=DEFAULT_INTEL_ROOT)
    parser.add_argument("--index-file", default=DEFAULT_INDEX_FILE)
    parser.add_argument("--queue-dir", default=DEFAULT_QUEUE_DIR)
    args = parser.parse_args()

    candidates = load_candidates(args.incoming_root, args.run_id)
    if args.candidate_id not in candidates:
        print(f"ERROR: candidate {args.candidate_id} not found in "
              f"{args.incoming_root}/{args.run_id}", file=sys.stderr)
        sys.exit(1)

    origin_bundle_id = None
    manifest_path_ = manifest_path(os.path.join(args.incoming_root, args.run_id))
    if os.path.isfile(manifest_path_):
        try:
            origin_bundle_id = read_json(manifest_path_).get("replay_identity")
        except Exception:
            pass

    status, message, _p = decide(
        args.run_id, args.candidate_id,
        candidates[args.candidate_id][1],
        args.decision, args.reviewer, args.notes,
        args.incoming_root, args.intel_root, args.index_file, args.queue_dir,
        dry_run=args.dry_run, origin_bundle_id=origin_bundle_id,
    )
    print(message)
    sys.exit(0 if status in ("accepted", "rejected", "deferred", "dry_run",
                             "already_accepted", "already_decided") else 1)


if __name__ == "__main__":
    main()
