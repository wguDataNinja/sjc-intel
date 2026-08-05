#!/usr/bin/env python3
"""
SJC_Intel — Deterministic validation script.
Verifies YAML schemas parse, Python scripts compile, and fixture files exist.
No network, production data, or credentials required.
"""
import os
import sys
import yaml

VALID_TIERS = {"core", "active", "stable", "temporary", "dormant"}
VALID_CADENCES = {"weekly", "biweekly", "monthly", "one_time"}
VALID_MODES = {"scheduled", "event_triggered", "manual"}
VALID_MATCH_CLASSES = {"exact", "probable", "related", "unverified", "irrelevant", "no_match"}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exit_code = 0


def check(description, ok, detail=""):
    global exit_code
    status = "PASS" if ok else "FAIL"
    if not ok:
        exit_code = 1
    print(f"  [{status}] {description}" + (f" — {detail}" if detail else ""))


def validate_yaml(path):
    try:
        with open(path) as f:
            yaml.safe_load(f)
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False


def main():
    print("SJC_Intel Validation")
    print("=" * 50)

    # 1. YAML schemas parse
    print("\n1. YAML Schema Validation")
    schema_dir = os.path.join(REPO_ROOT, "schemas")
    schema_files = sorted(os.listdir(schema_dir))
    for fname in schema_files:
        if fname.endswith(".yaml"):
            check(f"Schema: {fname}", validate_yaml(os.path.join(schema_dir, fname)))

    # 2. Python scripts compile
    print("\n2. Python Script Compilation")
    script_dir = os.path.join(REPO_ROOT, "scripts")
    for fname in sorted(os.listdir(script_dir)):
        if fname.endswith(".py") and fname != "validate.py":
            fpath = os.path.join(script_dir, fname)
            try:
                with open(fpath) as f:
                    compile(f.read(), fpath, "exec")
                check(f"Script: {fname}", True)
            except SyntaxError as e:
                check(f"Script: {fname}", False, str(e))

    # 3. Fixture files exist
    print("\n3. Fixture File Presence")
    fixture_dir = os.path.join(REPO_ROOT, "tests", "fixtures")
    expected_fixtures = [
        "051926_agenda.pdf", "051926_agenda.txt",
        "1202026_agenda.pdf", "1202026_agenda.txt",
        "clerk_agendas.html", "nbor_raw.html", "utility_department.html",
    ]
    for fname in expected_fixtures:
        fpath = os.path.join(fixture_dir, fname)
        check(f"Fixture: {fname}", os.path.exists(fpath),
              f"{'found' if os.path.exists(fpath) else 'MISSING'}")

    # 4. Registry validation — search_profiles.yaml
    print("\n4. Search Profiles Registry")
    sp_path = os.path.join(REPO_ROOT, "registry", "search_profiles.yaml")
    if os.path.exists(sp_path):
        check("search_profiles.yaml exists", True)
        try:
            with open(sp_path) as f:
                sp_data = yaml.safe_load(f)
            check("search_profiles.yaml parses", True)
            profiles = sp_data.get("profiles", [])
            check(f"Profiles defined: {len(profiles)}", True)
            profile_ids = set()
            all_ok = True
            for p in profiles:
                pid = p.get("profile_id", "?")
                # Unique IDs
                if pid in profile_ids:
                    check(f"  Profile {pid}: duplicate ID", False)
                    all_ok = False
                profile_ids.add(pid)
                # Enablement
                check(f"  Profile {pid}: enabled={p.get('enabled', False)}", True)
                # Tier
                tier = p.get("tier")
                if tier and tier not in VALID_TIERS:
                    check(f"  Profile {pid}: invalid tier '{tier}'", False)
                    all_ok = False
                # Cadence
                cadence = p.get("cadence")
                if cadence and cadence not in VALID_CADENCES:
                    check(f"  Profile {pid}: invalid cadence '{cadence}'", False)
                    all_ok = False
                # At least one entity_id or community_id for enabled profiles
                if p.get("enabled"):
                    has_eid = bool(p.get("entity_ids"))
                    has_cid = bool(p.get("community_ids"))
                    has_template = bool(p.get("query_templates"))
                    if not (has_eid or has_cid) and not has_template:
                        check(f"  Profile {pid}: enabled but no entity_ids, community_ids, or query_templates", False)
                        all_ok = False
                # Provisional terms must be clearly marked
                prov = p.get("provisional_terms", [])
                if prov and not any("unconfirm" in (p.get("notes", "") + " ").lower() for p in [p]):
                    check(f"  Profile {pid}: has provisional_terms but notes may not clarify unconfirmed status", True)  # soft check
            if all_ok:
                check("  All profile checks passed", True)
        except Exception as e:
            check(f"search_profiles.yaml validation failed: {e}", False)
    else:
        check("search_profiles.yaml not found (optional)", True)

    # 5. Registry validation — tracked_entities ID consistency
    print("\n5. Cross-Registry ID Consistency")
    te_path = os.path.join(REPO_ROOT, "registry", "tracked_entities.yaml")
    comm_path = os.path.join(REPO_ROOT, "registry", "communities.yaml")
    if os.path.exists(sp_path) and os.path.exists(te_path) and os.path.exists(comm_path):
        try:
            with open(te_path) as f:
                te_data = yaml.safe_load(f)
            with open(comm_path) as f:
                comm_data = yaml.safe_load(f)
            with open(sp_path) as f:
                sp_data = yaml.safe_load(f)
            te_ids = {e["entity_id"] for e in te_data["tracked_entities"]}
            comm_ids = {c["id"] for c in comm_data["communities"]}
            all_ok = True
            for p in sp_data.get("profiles", []):
                for eid in p.get("entity_ids", []):
                    if eid not in te_ids:
                        check(f"  Profile {p['profile_id']}: entity_id '{eid}' not found in tracked_entities.yaml", False)
                        all_ok = False
                for cid in p.get("community_ids", []):
                    if cid not in comm_ids:
                        check(f"  Profile {p['profile_id']}: community_id '{cid}' not found in communities.yaml", False)
                        all_ok = False
            if all_ok:
                check("  All cross-registry references valid", True)
        except Exception as e:
            check(f"Cross-registry validation error: {e}", False)
    else:
        check("Cross-registry check skipped (search_profiles.yaml not present)", True)

    # 6. Requirements file
    print("\n6. Requirements.txt")
    req_path = os.path.join(REPO_ROOT, "requirements.txt")
    check("requirements.txt exists", os.path.exists(req_path))

    # 7. Weekly task declaration manifest
    print("\n7. Weekly Task Declaration")
    task_path = os.path.join(REPO_ROOT, "deploy", "sjc-weekly-task.yaml")
    task_required = [
        "schema_version", "task_id", "enabled", "prompt_path", "runner",
        "profile_id", "bundle_contract_version", "approved_sources",
        "runtime_limits", "outputs", "secrets", "activation",
    ]
    if os.path.exists(task_path):
        check("deploy/sjc-weekly-task.yaml exists", True)
        try:
            with open(task_path) as f:
                task_data = yaml.safe_load(f)
            check("deploy/sjc-weekly-task.yaml parses", True)
            missing = [k for k in task_required if k not in task_data]
            check("  required fields present", not missing, f"missing: {missing}")
            sources = task_data.get("approved_sources", [])
            check(f"  approved_sources ({len(sources)})", isinstance(sources, list) and bool(sources))
            limits = task_data.get("runtime_limits", {})
            check("  runtime limits present", "max_wallclock_minutes" in limits and "max_fetches" in limits)
        except Exception as e:
            check(f"deploy/sjc-weekly-task.yaml validation failed: {e}", False)
    else:
        check("deploy/sjc-weekly-task.yaml missing (optional)", True)

    # 8. Publication-decision foundation
    print("\n8. Publication Decision Foundation")
    pd_schema = os.path.join(REPO_ROOT, "schemas", "publication_decision.schema.yaml")
    check("schemas/publication_decision.schema.yaml exists", os.path.exists(pd_schema))
    legacy_ex = os.path.join(REPO_ROOT, "data", "publication_decisions", "legacy_exceptions.yaml")
    if os.path.exists(legacy_ex):
        check("data/publication_decisions/legacy_exceptions.yaml exists", True)
        try:
            with open(legacy_ex) as f:
                lex = yaml.safe_load(f)
            check("legacy_exceptions.yaml parses", True)
            exs = lex.get("legacy_exceptions", [])
            check(f"  exceptions defined ({len(exs)})", bool(exs))
            for e in exs:
                if not e.get("id") or not isinstance(e.get("item_ids"), list):
                    check(f"  exception {e.get('id', '?')} malformed", False)
        except Exception as e:
            check(f"legacy_exceptions.yaml validation failed: {e}", False)
    else:
        check("data/publication_decisions/legacy_exceptions.yaml missing (optional)", True)

    # 9. SilverLeaf Brief static site + export artifacts
    print("\n9. SilverLeaf Brief Static Site")
    demo_fixture = os.path.join(REPO_ROOT, "site", "fixtures", "demo", "release.yaml")
    if os.path.exists(demo_fixture):
        try:
            with open(demo_fixture) as f:
                demo = yaml.safe_load(f)
            check("site/fixtures/demo/release.yaml parses", True)
            items = demo.get("items", [])
            check(f"  demo fixture items: {len(items)}", bool(items))
            if demo.get("release_metadata", {}).get("release_id", "").startswith("SJC-REL-DEMO"):
                check("  demo release clearly labeled SJC-REL-DEMO-*", True)
            else:
                check("  demo release clearly labeled SJC-REL-DEMO-*", False)
        except Exception as e:
            check(f"demo fixture validation failed: {e}", False)
    else:
        check("site/fixtures/demo/release.yaml missing (optional)", True)

    demo_manifest = os.path.join(REPO_ROOT, "site", "data", "demo", "release-manifest.json")
    if os.path.exists(demo_manifest):
        try:
            import json, hashlib
            with open(demo_manifest) as f:
                m = json.load(f)
            check("site/data/demo/release-manifest.json parses", True)
            check(f"  demo environment tag", m.get("environment") == "demo")
            checks_ok = all(
                hashlib.sha256(open(os.path.join(
                    os.path.dirname(demo_manifest), name), "rb").read()).hexdigest() == want
                for name, want in m.get("checksums", {}).items())
            check("  demo artifact checksums verify", checks_ok)
        except Exception as e:
            check(f"demo manifest validation failed: {e}", False)
    else:
        check("site/data/demo/release-manifest.json missing (optional)", True)

    # Site pages present + no private path leakage.
    site_root = os.path.join(REPO_ROOT, "site")
    expected_pages = ["index.html", "browse/index.html", "about/index.html",
                      "sources/index.html", "404.html"]
    present = sum(1 for p in expected_pages if os.path.exists(os.path.join(site_root, p)))
    if present:
        check(f"  site pages present ({present}/{len(expected_pages)})",
              present == len(expected_pages))
        leaks = []
        for root, _dirs, files in os.walk(site_root):
            for name in files:
                if not name.endswith(".html"):
                    continue
                text = open(os.path.join(root, name), encoding="utf-8").read()
                if "/Users/" in text or "/home/" in text:
                    leaks.append(os.path.relpath(os.path.join(root, name), REPO_ROOT))
        check("  no private paths in generated pages", not leaks, str(leaks) if leaks else "")
    else:
        check("  site pages present", True)  # not built yet — optional

    # 10. SilverLeaf scope registry
    print("\n10. SilverLeaf Scope Registry")
    scope_path = os.path.join(REPO_ROOT, "registry", "silverleaf_scope.yaml")
    scope_schema = os.path.join(REPO_ROOT, "schemas", "silverleaf_scope.schema.yaml")
    check("registry/silverleaf_scope.yaml exists", os.path.exists(scope_path))
    check("schemas/silverleaf_scope.schema.yaml exists", os.path.exists(scope_schema))
    if os.path.exists(scope_path):
        try:
            with open(scope_path) as f:
                scope = yaml.safe_load(f)
            check("silverleaf_scope.yaml parses", True)
            comm_path = os.path.join(REPO_ROOT, "registry", "communities.yaml")
            ent_path = os.path.join(REPO_ROOT, "registry", "tracked_entities.yaml")
            with open(comm_path) as f:
                comm = yaml.safe_load(f)
            with open(ent_path) as f:
                ents = yaml.safe_load(f)
            comm_ids = {c["id"] for c in comm.get("communities", []) if c.get("id")}
            ent_ids = {e["entity_id"] for e in ents.get("tracked_entities", []) if e.get("entity_id")}
            nbs = scope.get("neighborhoods", [])
            check(f"  neighborhoods registered ({len(nbs)})", bool(nbs))
            missing_nb = [nb["id"] for nb in nbs if nb.get("id") not in comm_ids]
            check("  all neighborhoods exist in communities.yaml", not missing_nb, str(missing_nb))
            devs = scope.get("developments", [])
            missing_dev = [d["id"] for d in devs if d.get("id", "").startswith("ENT-") and d["id"] not in ent_ids]
            check(f"  developments registered ({len(devs)})", bool(devs))
            check("  all ENT-* developments exist in tracked_entities.yaml", not missing_dev, str(missing_dev))
            # Run the standalone validator for the full check surface.
            import subprocess
            sub = subprocess.run(
                [sys.executable, os.path.join(REPO_ROOT, "scripts", "validate_silverleaf_scope.py")],
                capture_output=True, text=True)
            check("  validate_silverleaf_scope.py passes", sub.returncode == 0,
                  sub.stdout.strip().splitlines()[-1] if sub.stdout else sub.stderr[:120])
        except Exception as e:
            check(f"silverleaf scope validation failed: {e}", False)
    else:
        check("silverleaf_scope.yaml missing (optional)", True)

    print(f"\n{'=' * 50}")
    print(f"Result: {'ALL PASSED' if exit_code == 0 else f'{exit_code} FAILURES'}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
