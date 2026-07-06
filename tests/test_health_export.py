import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")
HEALTH_EXPORT_SCRIPT = os.path.join(REPO_ROOT, "scripts", "health_export.py")


def _run_script(*args, env=None):
    cmd = [sys.executable, HEALTH_EXPORT_SCRIPT]
    cmd.extend(args)
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=merged_env,
    )
    return result


def test_health_export_dry_run_succeeds():
    result = _run_script("--dry-run")
    assert result.returncode == 0
    assert "schema_version" in result.stdout
    assert "project" in result.stdout
    assert "sjc_intel" in result.stdout


def test_health_export_dry_run_output_is_valid_json():
    result = _run_script("--dry-run")
    stdout_lines = result.stdout.strip().split("\n")
    json_str = "\n".join(line for line in stdout_lines if line and not line.startswith("#"))
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"
    assert data["schema_version"] == 1
    assert data["project"] == "sjc_intel"
    assert data["status"] == "ok"


def test_health_export_dry_run_has_sanitized_fields():
    result = _run_script("--dry-run")
    stdout_lines = result.stdout.strip().split("\n")
    json_str = "\n".join(line for line in stdout_lines if line and not line.startswith("#"))
    data = json.loads(json_str)
    required = ["schema_version", "generated_at", "project", "workflow", "status", "backup_state"]
    for field in required:
        assert field in data, f"Missing required sanitized field: {field}"


def test_health_export_dry_run_has_sjc_extensions():
    result = _run_script("--dry-run")
    stdout_lines = result.stdout.strip().split("\n")
    json_str = "\n".join(line for line in stdout_lines if line and not line.startswith("#"))
    data = json.loads(json_str)
    sjc_fields = ["source_reachability", "monthly_closeout_age", "dedupe_index_size",
                  "review_queue_pending", "source_count", "tracked_entity_count"]
    for field in sjc_fields:
        assert field in data, f"Missing SJC extension field: {field}"


def test_health_export_redact_test():
    result = _run_script("--dry-run", "--redact-test")
    assert result.returncode == 0
    assert "Redaction test:" in result.stdout


def test_health_export_no_flag_still_dry():
    result = _run_script()
    assert result.returncode == 0
    assert "disabled" in result.stdout.lower()


def test_health_export_environment_flag_no_dry():
    env = {"SJC_INTEL_HEALTH_EXPORT_ENABLED": "true"}
    result = _run_script(env=env)
    assert result.returncode == 0
    assert "schema_version" in result.stdout


def test_health_export_no_prohibited_in_output():
    result = _run_script("--dry-run")
    stdout_lines = result.stdout.strip().split("\n")
    json_str = "\n".join(line for line in stdout_lines if line and not line.startswith("#"))
    data = json.loads(json_str)
    prohibited = [
        "error_message_private", "ip_address", "filesystem_path",
        "api_key", "stack_trace", "credential", "browser_profile",
    ]
    for field in prohibited:
        assert field not in data, f"Prohibited field found in output: {field}"


def test_health_export_dry_run_stderr_no_leak():
    result = _run_script("--dry-run")
    assert "error_message_private" not in result.stderr.lower()
    assert "password" not in result.stderr.lower()
    assert "secret" not in result.stderr.lower()


def test_health_export_stale_fixture_valid():
    import json as _json
    path = os.path.join(FIXTURE_DIR, "health_export_stale.json")
    with open(path) as f:
        data = _json.load(f)
    assert data["freshness"] == 864000
    assert data["status"] == "warn"


def test_health_export_schema_version_report():
    from scripts.health_export import schema_version_report
    report = schema_version_report()
    assert report["schema_version"] == 1
    assert report["contract_version"] == "1.0.0"
    assert "generated_at" in report
    assert "migration_version" in report
