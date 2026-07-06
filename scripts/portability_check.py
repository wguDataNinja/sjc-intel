import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MIGRATION_DIR = REPO_ROOT / "db" / "migrations"
ROLLBACK_DIR = MIGRATION_DIR / "rollback"
VALIDATION_PATH = REPO_ROOT / "db" / "validation" / "999_full_validation.sql"


def run_checks():
    migrations = sorted(MIGRATION_DIR.glob("20*.sql"))
    versions = [_migration_version(path) for path in migrations]
    expected_versions = list(range(1, len(versions) + 1))
    rollback_missing = [
        path.name for path in migrations if not (ROLLBACK_DIR / path.name.replace(".sql", "_down.sql")).exists()
    ]
    checks = [
        _check("migration_versions_contiguous", versions == expected_versions, {"versions": versions}),
        _check("rollback_files_present", not rollback_missing, {"missing": rollback_missing}),
        _check("validation_mentions_latest_version", _validation_mentions_latest(versions[-1] if versions else 0), {}),
        _check("migrations_use_owner_role", _all_contain(migrations, "SET ROLE sjc_intel_owner;"), {}),
        _check("no_mac_paths_in_application_code", not _mac_paths_in_application_code(), {}),
        _check("pg_env_documented", _pg_env_documented(), {}),
    ]
    return {
        "status": "PASS" if all(check["passed"] for check in checks) else "FAIL",
        "checks": checks,
        "migration_count": len(migrations),
        "latest_migration_version": versions[-1] if versions else None,
    }


def _migration_version(path):
    match = re.match(r"^20\d{6}_(\d{3})_", path.name)
    if not match:
        raise ValueError(f"Migration file does not contain a 3-digit version: {path.name}")
    return int(match.group(1))


def _validation_mentions_latest(version):
    if version == 0:
        return False
    text = VALIDATION_PATH.read_text(encoding="utf-8")
    return f"BETWEEN 1 AND {version}" in text and f"(0, {version})" in text


def _all_contain(paths, expected):
    return all(expected in path.read_text(encoding="utf-8") for path in paths)


def _mac_paths_in_application_code():
    mac_user_path = "/Users/" + "buddy"
    homebrew_word = "Home" + "brew"
    application_paths = [
        REPO_ROOT / "scripts",
        REPO_ROOT / "db",
        REPO_ROOT / "deploy",
    ]
    hits = []
    for root in application_paths:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix in (".pyc",):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if mac_user_path in text or homebrew_word in text:
                hits.append(str(path.relative_to(REPO_ROOT)))
    return hits


def _pg_env_documented():
    env_docs = [
        REPO_ROOT / "deploy" / "env.example",
        REPO_ROOT / "docs" / "VPS_CONTINUITY.md",
    ]
    required = [
        "SJC_INTEL_PG_ADAPTER_ENABLED",
        "SJC_INTEL_PG_DATABASE",
        "SJC_INTEL_PG_READER_USER",
        "SJC_INTEL_PG_WRITER_USER",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in env_docs if path.exists())
    return all(item in text for item in required)


def _check(name, passed, evidence):
    return {"name": name, "passed": bool(passed), "evidence": evidence}


def main():
    parser = argparse.ArgumentParser(description="Run non-mutating SJC Mac-to-VPS portability checks.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()
    report = run_checks()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"SJC portability check: {report['status']}")
        for check in report["checks"]:
            status = "PASS" if check["passed"] else "FAIL"
            print(f"{status} {check['name']}")
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
