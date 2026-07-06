#!/usr/bin/env bash
# SJC Intel — Migration readiness check (INERT TEMPLATE).
# Dry-run by default. No psql calls. Checks file-based readiness only.
#
# Usage:
#   bash scripts/migration_readiness_check.sh
#   DRY_RUN=false bash scripts/migration_readiness_check.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
: "${DRY_RUN:=true}"

MIGRATIONS_DIR="${REPO_ROOT}/db/migrations"
ROLLBACK_DIR="${MIGRATIONS_DIR}/rollback"
VALIDATION_DIR="${MIGRATIONS_DIR}/validation"
UNAPPLIED_MARKER="${REPO_ROOT}/db/.unapplied_migrations"

PASS=0
FAIL=0

check() {
    local desc="$1" result="$2"
    if [ "$result" = "true" ] || [ "$result" = "0" ]; then
        echo "  [PASS] ${desc}"
        PASS=$((PASS + 1))
    else
        echo "  [FAIL] ${desc}"
        FAIL=$((FAIL + 1))
    fi
}

echo "SJC Intel — Migration Readiness Check"
echo "======================================"
echo "Dry-run: ${DRY_RUN}"
echo ""

# 1. Migration directory exists
check "Migration directory exists" "$([ -d "${MIGRATIONS_DIR}" ] && echo true || echo false)"

# 2. Rollback directory exists
check "Rollback directory exists" "$([ -d "${ROLLBACK_DIR}" ] && echo true || echo false)"

# 3. Validation directory exists
check "Validation directory exists" "$([ -d "${VALIDATION_DIR}" ] && echo true || echo false)"

# 4. Migration files present
migration_count=$(ls -1 "${MIGRATIONS_DIR}"/*.sql 2>/dev/null | wc -l | tr -d ' ')
check "Migration files found (${migration_count})" "$([ "${migration_count}" -ge 1 ] && echo true || echo false)"

# 5. Rollback files present
rollback_count=$(ls -1 "${ROLLBACK_DIR}"/*.sql 2>/dev/null | wc -l | tr -d ' ')
check "Rollback files found (${rollback_count})" "$([ "${rollback_count}" -ge 1 ] && echo true || echo false)"

# 6. Validation files present
validation_count=$(ls -1 "${VALIDATION_DIR}"/*.sql 2>/dev/null | wc -l | tr -d ' ')
check "Validation files found (${validation_count})" "$([ "${validation_count}" -ge 1 ] && echo true || echo false)"

# 7. No unapplied migrations marker
check "No unapplied migrations marker" "$([ ! -f "${UNAPPLIED_MARKER}" ] && echo true || echo false)"

# 8. README exists
check "db/README.md exists" "$([ -f "${REPO_ROOT}/db/README.md" ] && echo true || echo false)"

echo ""
echo "--------------------"
echo "Results: ${PASS} passed, ${FAIL} failed"

if [ "${FAIL}" -gt 0 ]; then
    exit 1
fi
exit 0
