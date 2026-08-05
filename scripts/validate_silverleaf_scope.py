#!/usr/bin/env python3
"""
SJC_Intel — SilverLeaf Scope Registry Validator (ROADMAP.md §3B-G1).

Validates registry/silverleaf_scope.yaml: provenance vocabulary, stable-ID
cross-references to registry/communities.yaml and registry/tracked_entities.yaml,
relevance-rule id integrity, and structural requirements defined in
schemas/silverleaf_scope.schema.yaml.

Output: deterministic human summary (+ --json), exit 0 when no blocking
errors, exit 1 otherwise.
"""
import argparse
import json
import os
import sys
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPE_FILE = os.path.join(REPO_ROOT, "registry", "silverleaf_scope.yaml")
COMMUNITIES_FILE = os.path.join(REPO_ROOT, "registry", "communities.yaml")
ENTITIES_FILE = os.path.join(REPO_ROOT, "registry", "tracked_entities.yaml")

PROVENANCE = {"verified", "inferred", "editorial-policy", "needs-review"}
RELEVANCE_IDS = {"in_silverleaf", "near_silverleaf", "countywide_impact"}


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def validate():
    errors = []
    warnings = []

    if not os.path.exists(SCOPE_FILE):
        return {"status": "FAIL", "errors": ["registry/silverleaf_scope.yaml missing"],
                "warnings": [], "checks": []}
    scope = load_yaml(SCOPE_FILE)
    comm = load_yaml(COMMUNITIES_FILE)
    ents = load_yaml(ENTITIES_FILE)

    community_ids = {c["id"] for c in comm.get("communities", []) if c.get("id")}
    entity_ids = {e["entity_id"] for e in ents.get("tracked_entities", []) if e.get("entity_id")}
    checks = []

    def _check(name, ok, detail=""):
        checks.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")

    def _warn(name, detail):
        warnings.append(f"{name}: {detail}")

    # Structural
    _check("schema_version present", bool(scope.get("schema_version")))
    _check("community.canonical_name present",
           bool((scope.get("community") or {}).get("canonical_name")))

    # Provenance vocabulary everywhere it appears.
    provenance_fields = []
    for nb in scope.get("neighborhoods", []):
        provenance_fields.append((f"neighborhood.{nb.get('id')}", nb.get("verification")))
    for road in scope.get("roads", {}).get("direct_serving", []):
        provenance_fields.append((f"road.{road.get('id')}", road.get("verification")))
    for road in scope.get("roads", {}).get("adjacent_corridors", []):
        provenance_fields.append((f"road.{road.get('id')}", road.get("verification")))
    for s in scope.get("schools", []):
        provenance_fields.append((f"school.{s.get('id')}", s.get("verification")))
    for u in scope.get("utilities", []):
        provenance_fields.append((f"utility.{u.get('id')}", u.get("verification")))
    for d in scope.get("developments", []):
        provenance_fields.append((f"development.{d.get('id')}", d.get("verification")))
    for b in scope.get("businesses_services", []):
        provenance_fields.append((f"business.{b.get('id')}", b.get("verification")))
    for section in ("direct", "nearby", "countywide_material"):
        for r in scope.get("relevance", {}).get(section, []):
            provenance_fields.append((f"relevance.{section}.{r.get('id')}", r.get("verification")))
    for rule in list(scope.get("inclusion_rules", [])) + list(scope.get("exclusion_rules", [])):
        provenance_fields.append((f"rule.{rule.get('id')}", rule.get("verification")))

    bad_prov = [(name, p) for name, p in provenance_fields if p not in PROVENANCE]
    _check("all provenance values valid", not bad_prov, str(bad_prov))

    # Neighborhoods cross-reference communities.yaml.
    missing_nb = [nb["id"] for nb in scope.get("neighborhoods", [])
                  if nb.get("id") not in community_ids]
    _check("all neighborhoods exist in communities.yaml", not missing_nb, str(missing_nb))

    # Developments ENT-* cross-reference tracked_entities.yaml.
    missing_dev = [d["id"] for d in scope.get("developments", [])
                   if d.get("id", "").startswith("ENT-") and d["id"] not in entity_ids]
    _check("all ENT-* developments exist in tracked_entities.yaml", not missing_dev,
           str(missing_dev))

    # entity_id links (roads/schools) cross-reference tracked_entities.yaml.
    missing_link = []
    for road in scope.get("roads", {}).get("direct_serving", []):
        eid = road.get("entity_id")
        if eid and eid not in entity_ids:
            missing_link.append(f"road.{road.get('id')} -> {eid}")
    for s in scope.get("schools", []):
        eid = s.get("entity_id")
        if eid and eid not in entity_ids:
            missing_link.append(f"school.{s.get('id')} -> {eid}")
    _check("entity_id links resolve to tracked_entities.yaml", not missing_link,
           str(missing_link))

    # Adjacent corridors where id is a community should exist (corridor type).
    corridor_ids = {c["id"] for c in comm.get("communities", [])
                    if c.get("type") == "corridor" and c.get("id")}
    for road in scope.get("roads", {}).get("adjacent_corridors", []):
        rid = road.get("id")
        if rid in community_ids and rid not in corridor_ids:
            _warn(f"adjacent corridor {rid} is a community but not typed 'corridor'")

    # Relevance id integrity.
    rel_ids = []
    for section, expected in (("direct", "in_silverleaf"),
                              ("nearby", "near_silverleaf"),
                              ("countywide_material", "countywide_impact")):
        for r in scope.get("relevance", {}).get(section, []):
            rel_ids.append(r.get("id"))
            if r.get("id") != expected:
                _check(f"relevance.{section} id is {expected}", r.get("id") == expected,
                       f"got {r.get('id')}")
    _check("relevance ids are the stable set", set(rel_ids) == RELEVANCE_IDS,
           str(set(rel_ids)))

    # Needs-review ids: item-like ids should exist in the corpus.
    # (Soft: only warn if a referenced item id is unknown to the corpus.)
    corpus_ids = set()
    import glob
    for f in sorted(glob.glob(os.path.join(REPO_ROOT, "data", "intel_items", "*", "*.yaml"))):
        try:
            data = load_yaml(f)
        except Exception:
            continue
        for it in data.get("items", []) or []:
            if it.get("item_id"):
                corpus_ids.add(it["item_id"])
    unknown_nr = [nr["id"] for nr in scope.get("needs_review", [])
                  if str(nr.get("id", "")).startswith("SJC-") and nr["id"] not in corpus_ids]
    if unknown_nr:
        _warn("needs_review references unknown corpus item ids", str(unknown_nr))

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "neighborhoods": len(scope.get("neighborhoods", [])),
        "developments": len(scope.get("developments", [])),
        "direct_roads": len(scope.get("roads", {}).get("direct_serving", [])),
        "adjacent_corridors": len(scope.get("roads", {}).get("adjacent_corridors", [])),
        "needs_review": len(scope.get("needs_review", [])),
    }


def main():
    ap = argparse.ArgumentParser(description="Validate SilverLeaf scope registry.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = validate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SilverLeaf Scope Registry Validation")
        print("=" * 50)
        for c in result["checks"]:
            print(f"  [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}"
                  + (f" — {c['detail']}" if c.get("detail") else ""))
        if result["warnings"]:
            print("\nWARNINGS:")
            for w in result["warnings"]:
                print(f"  - {w}")
        print("\n" + "=" * 50)
        print(f"Result: {result['status']} "
              f"({len(result['errors'])} errors, {len(result['warnings'])} warnings)")
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
