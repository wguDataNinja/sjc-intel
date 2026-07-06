"""
Test migration SQL files for basic syntax correctness.
Static analysis only — no database connection required.
"""
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIGRATIONS_DIR = os.path.join(REPO_ROOT, "db", "migrations")
ROLLBACK_DIR = os.path.join(MIGRATIONS_DIR, "rollback")
VALIDATION_DIR = os.path.join(MIGRATIONS_DIR, "validation")


def _list_sql_files(directory):
    if not os.path.isdir(directory):
        return []
    return sorted([
        f for f in os.listdir(directory)
        if f.endswith(".sql")
    ])


def _check_balanced_quotes(content):
    """Simple check that single quotes are balanced (approximate)."""
    in_string = False
    i = 0
    while i < len(content):
        if content[i] == "'" and (i == 0 or content[i - 1] != '\\'):
            in_string = not in_string
        i += 1
    return not in_string


def _check_balanced_parens(content):
    """Check parentheses are balanced (ignores strings)."""
    depth = 0
    in_string = False
    for i, c in enumerate(content):
        if c == "'" and (i == 0 or content[i - 1] != '\\'):
            in_string = not in_string
        if in_string:
            continue
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
    return depth == 0


def test_migration_directory_exists():
    assert os.path.isdir(MIGRATIONS_DIR), f"Migrations directory not found: {MIGRATIONS_DIR}"
    assert os.path.isdir(ROLLBACK_DIR), f"Rollback directory not found: {ROLLBACK_DIR}"
    assert os.path.isdir(VALIDATION_DIR), f"Validation directory not found: {VALIDATION_DIR}"


def test_migration_files_exist():
    files = _list_sql_files(MIGRATIONS_DIR)
    assert len(files) >= 9, f"Expected at least 9 migration files, found {len(files)}: {files}"


def test_rollback_files_exist():
    files = _list_sql_files(ROLLBACK_DIR)
    assert len(files) >= 9, f"Expected at least 9 rollback files, found {len(files)}: {files}"


def test_validation_files_exist():
    files = _list_sql_files(VALIDATION_DIR)
    assert len(files) >= 9, f"Expected at least 9 validation files, found {len(files)}: {files}"


def test_migration_file_pairs_complete():
    """Every forward migration should have matching rollback and validation."""
    migrations = {f.replace(".sql", "") for f in _list_sql_files(MIGRATIONS_DIR)}
    rollbacks = {f.replace("_down.sql", "") for f in _list_sql_files(ROLLBACK_DIR)}
    validations = {f.replace("_check.sql", "") for f in _list_sql_files(VALIDATION_DIR)}

    missing_rollback = migrations - rollbacks
    missing_validation = migrations - validations

    assert not missing_rollback, f"Migrations missing rollback: {missing_rollback}"
    assert not missing_validation, f"Migrations missing validation: {missing_validation}"


def test_migration_naming_convention():
    """Verify filenames match YYYYMMDD_NNN_description.sql pattern."""
    pattern = re.compile(r'^\d{8}_\d{3}_.+\.sql$')
    for f in _list_sql_files(MIGRATIONS_DIR):
        assert pattern.match(f), f"Migration filename does not match convention: {f}"


def test_migration_sql_syntax():
    """Basic static analysis of SQL files."""
    for dirname, label in [
        (MIGRATIONS_DIR, "migration"),
        (ROLLBACK_DIR, "rollback"),
        (VALIDATION_DIR, "validation"),
    ]:
        for fname in _list_sql_files(dirname):
            fpath = os.path.join(dirname, fname)
            with open(fpath) as f:
                content = f.read()

            assert len(content) > 0, f"Empty SQL file: {fpath}"
            assert _check_balanced_quotes(content), f"Unbalanced quotes in {fpath}"
            assert _check_balanced_parens(content), f"Unbalanced parentheses in {fpath}"


def test_migration_has_version_recording():
    """Forward migrations should record themselves in sjc_intel_migrations."""
    for fname in _list_sql_files(MIGRATIONS_DIR):
        fpath = os.path.join(MIGRATIONS_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        assert "sjc_intel_migrations" in content, (
            f"Migration {fname} does not record itself in sjc_intel_migrations"
        )


def test_migration_no_production_data():
    """Verify no production credentials or data in migration files."""
    sensitive_patterns = [
        r'password\s*=',
        r'PGPASSWORD',
        r'PGUSER',
        r'postgres://',
        r'CREATE\s+USER',
        r'ALTER\s+USER',
        r'scraper',
        r'ih-market-vps',
        r'46\.224\.146\.164',
    ]
    for dirname in [MIGRATIONS_DIR, ROLLBACK_DIR, VALIDATION_DIR]:
        for fname in _list_sql_files(dirname):
            fpath = os.path.join(dirname, fname)
            with open(fpath) as f:
                content = f.read().lower()
            for pattern in sensitive_patterns:
                assert not re.search(pattern, content, re.IGNORECASE), (
                    f"Sensitive content in {fpath}: matched {pattern}"
                )


def test_fixture_yaml_files_exist():
    """Verify fixture YAML files exist."""
    fixture_dir = os.path.join(REPO_ROOT, "db", "fixtures")
    assert os.path.isdir(fixture_dir), f"Fixtures directory not found: {fixture_dir}"
    fixture_files = [f for f in os.listdir(fixture_dir) if f.endswith(".yaml")]
    assert len(fixture_files) >= 4, f"Expected at least 4 fixture files, found {len(fixture_files)}"
