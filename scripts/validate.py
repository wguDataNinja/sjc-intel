#!/usr/bin/env python3
"""
SJC_Intel — Deterministic validation script.
Verifies YAML schemas parse, Python scripts compile, and fixture files exist.
No network, production data, or credentials required.
"""
import os
import sys
import yaml

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

    # 4. Requirements file
    print("\n4. Requirements.txt")
    req_path = os.path.join(REPO_ROOT, "requirements.txt")
    check("requirements.txt exists", os.path.exists(req_path))

    print(f"\n{'=' * 50}")
    print(f"Result: {'ALL PASSED' if exit_code == 0 else f'{exit_code} FAILURES'}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
