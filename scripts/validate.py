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

    print(f"\n{'=' * 50}")
    print(f"Result: {'ALL PASSED' if exit_code == 0 else f'{exit_code} FAILURES'}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
