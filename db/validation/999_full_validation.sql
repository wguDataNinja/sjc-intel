-- 999_full_validation.sql
-- SJC Intel full structural, ownership, grant, and isolation validation.

\set ON_ERROR_STOP on

SELECT 'row_count_app.sources' AS check_name, COUNT(*) AS row_count FROM app.sources
UNION ALL SELECT 'row_count_app.source_events', COUNT(*) FROM app.source_events
UNION ALL SELECT 'row_count_app.intel_items', COUNT(*) FROM app.intel_items
UNION ALL SELECT 'row_count_app.tracked_entities', COUNT(*) FROM app.tracked_entities
UNION ALL SELECT 'row_count_app.review_queue_entries', COUNT(*) FROM app.review_queue_entries
UNION ALL SELECT 'row_count_health.health_runs', COUNT(*) FROM health.health_runs
UNION ALL SELECT 'row_count_health.workflow_status', COUNT(*) FROM health.workflow_status;

WITH expected(schema_name) AS (
    VALUES ('app'), ('archive'), ('health')
)
SELECT 'schemas_exist' AS check_name,
       CASE WHEN COUNT(n.nspname) = 3 THEN 'PASS' ELSE 'FAIL' END AS result,
       ARRAY_AGG(n.nspname ORDER BY n.nspname) AS found
FROM expected e
LEFT JOIN pg_namespace n ON n.nspname = e.schema_name;

WITH expected(table_schema, table_name) AS (
    VALUES
        ('app','sjc_intel_migrations'),
        ('app','sources'),
        ('app','source_events'),
        ('app','intel_items'),
        ('app','tracked_entities'),
        ('app','intel_item_tracked_entities'),
        ('app','source_event_related_events'),
        ('app','intel_item_topics'),
        ('app','intel_item_communities'),
        ('app','intel_item_interest_tags'),
        ('app','source_event_items'),
        ('app','review_queue_entries'),
        ('app','dedupe_index_entries'),
        ('app','interest_filters'),
        ('app','source_candidates'),
        ('app','beat_candidates'),
        ('app','communities'),
        ('app','search_terms'),
        ('health','health_runs'),
        ('health','workflow_status')
)
SELECT 'expected_tables_exist' AS check_name,
       CASE WHEN COUNT(c.oid) = 20 THEN 'PASS' ELSE 'FAIL' END AS result,
       COUNT(c.oid) AS found
FROM expected e
LEFT JOIN pg_namespace n ON n.nspname = e.table_schema
LEFT JOIN pg_class c ON c.relnamespace = n.oid
               AND c.relname = e.table_name
               AND c.relkind = 'r';

SELECT 'schema_ownership' AS check_name,
       CASE WHEN COUNT(*) = 3 THEN 'PASS' ELSE 'FAIL' END AS result
FROM pg_namespace n
JOIN pg_roles r ON r.oid = n.nspowner
WHERE n.nspname IN ('app','archive','health')
  AND r.rolname = 'sjc_intel_owner';

SELECT 'table_ownership' AS check_name,
       CASE WHEN COUNT(*) = 20 THEN 'PASS' ELSE 'FAIL' END AS result,
       COUNT(*) AS owned_tables
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_roles r ON r.oid = c.relowner
WHERE n.nspname IN ('app','health')
  AND c.relkind = 'r'
  AND r.rolname = 'sjc_intel_owner';

SELECT 'migration_versions' AS check_name,
       CASE WHEN COUNT(*) IN (0, 9) THEN 'PASS' ELSE 'FAIL' END AS result,
       ARRAY_AGG(version ORDER BY version) AS versions
FROM app.sjc_intel_migrations
WHERE version BETWEEN 1 AND 9;

SELECT 'primary_keys' AS check_name,
       CASE WHEN COUNT(*) >= 18 THEN 'PASS' ELSE 'FAIL' END AS result,
       COUNT(*) AS pk_count
FROM information_schema.table_constraints
WHERE table_schema IN ('app','health')
  AND constraint_type = 'PRIMARY KEY';

SELECT 'foreign_keys' AS check_name,
       CASE WHEN COUNT(*) >= 12 THEN 'PASS' ELSE 'FAIL' END AS result,
       COUNT(*) AS fk_count
FROM information_schema.table_constraints
WHERE table_schema = 'app'
  AND constraint_type = 'FOREIGN KEY';

SELECT 'writer_app_dml' AS check_name,
       CASE WHEN NOT EXISTS (
           SELECT 1
           FROM pg_class c
           JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname = 'app'
             AND c.relkind = 'r'
             AND NOT (
                 has_table_privilege('sjc_intel_writer', c.oid, 'SELECT')
                 AND has_table_privilege('sjc_intel_writer', c.oid, 'INSERT')
                 AND has_table_privilege('sjc_intel_writer', c.oid, 'UPDATE')
                 AND has_table_privilege('sjc_intel_writer', c.oid, 'DELETE')
             )
       ) THEN 'PASS' ELSE 'FAIL' END AS result;

SELECT 'reader_app_select' AS check_name,
       CASE WHEN NOT EXISTS (
           SELECT 1
           FROM pg_class c
           JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname = 'app'
             AND c.relkind = 'r'
             AND NOT has_table_privilege('sjc_intel_reader', c.oid, 'SELECT')
       ) THEN 'PASS' ELSE 'FAIL' END AS result;

SELECT 'monitor_health_only' AS check_name,
       CASE WHEN has_schema_privilege('sjc_intel_monitor', 'health', 'USAGE')
             AND NOT has_schema_privilege('sjc_intel_monitor', 'app', 'USAGE')
            THEN 'PASS' ELSE 'FAIL' END AS result;

SELECT 'backup_all_project_tables' AS check_name,
       CASE WHEN NOT EXISTS (
           SELECT 1
           FROM pg_class c
           JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname IN ('app','health')
             AND c.relkind = 'r'
             AND NOT has_table_privilege('sjc_intel_backup', c.oid, 'SELECT')
       ) THEN 'PASS' ELSE 'FAIL' END AS result;

SELECT 'public_schema_privileges_revoked' AS check_name,
       CASE WHEN NOT EXISTS (
           SELECT 1
           FROM pg_namespace n
           CROSS JOIN LATERAL aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner))) acl
           WHERE n.nspname IN ('app','archive','health')
             AND acl.grantee = 0
             AND acl.privilege_type IN ('USAGE','CREATE')
       ) THEN 'PASS' ELSE 'FAIL' END AS result;

SELECT 'cross_db_connect_isolation' AS check_name,
       CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS result,
       COUNT(*) AS unexpected_connects
FROM pg_roles r
CROSS JOIN pg_database d
WHERE r.rolname IN ('sjc_intel_writer','sjc_intel_reader','sjc_intel_monitor',
                    'sjc_intel_migrator','sjc_intel_backup')
  AND d.datname IN ('traderie','wgu_reddit_ops','wgu_catalog','bsda_courses',
                    'idlehacking_kb','ih_market_companion','reckless_ben')
  AND has_database_privilege(r.rolname, d.datname, 'CONNECT');

DO $$
DECLARE
    failures text[] := ARRAY[]::text[];
BEGIN
    IF (SELECT COUNT(*) FROM pg_namespace n JOIN pg_roles r ON r.oid = n.nspowner
        WHERE n.nspname IN ('app','archive','health') AND r.rolname = 'sjc_intel_owner') <> 3 THEN
        failures := array_append(failures, 'schema_ownership');
    END IF;

    IF (SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace JOIN pg_roles r ON r.oid = c.relowner
        WHERE n.nspname IN ('app','health') AND c.relkind = 'r' AND r.rolname = 'sjc_intel_owner') <> 20 THEN
        failures := array_append(failures, 'table_ownership');
    END IF;

    IF (SELECT COUNT(*) FROM app.sjc_intel_migrations WHERE version BETWEEN 1 AND 9) NOT IN (0, 9) THEN
        failures := array_append(failures, 'migration_versions');
    END IF;

    IF (SELECT COUNT(*) FROM information_schema.table_constraints
        WHERE table_schema IN ('app','health') AND constraint_type = 'PRIMARY KEY') < 18 THEN
        failures := array_append(failures, 'primary_keys');
    END IF;

    IF (SELECT COUNT(*) FROM information_schema.table_constraints
        WHERE table_schema = 'app' AND constraint_type = 'FOREIGN KEY') < 12 THEN
        failures := array_append(failures, 'foreign_keys');
    END IF;

    IF EXISTS (
        SELECT 1
        FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'app' AND c.relkind = 'r'
          AND NOT (
              has_table_privilege('sjc_intel_writer', c.oid, 'SELECT')
              AND has_table_privilege('sjc_intel_writer', c.oid, 'INSERT')
              AND has_table_privilege('sjc_intel_writer', c.oid, 'UPDATE')
              AND has_table_privilege('sjc_intel_writer', c.oid, 'DELETE')
          )
    ) THEN
        failures := array_append(failures, 'writer_app_dml');
    END IF;

    IF NOT (has_schema_privilege('sjc_intel_monitor', 'health', 'USAGE')
            AND NOT has_schema_privilege('sjc_intel_monitor', 'app', 'USAGE')) THEN
        failures := array_append(failures, 'monitor_health_only');
    END IF;

    IF EXISTS (
        SELECT 1
        FROM pg_roles r
        CROSS JOIN pg_database d
        WHERE r.rolname IN ('sjc_intel_writer','sjc_intel_reader','sjc_intel_monitor',
                            'sjc_intel_migrator','sjc_intel_backup')
          AND d.datname IN ('traderie','wgu_reddit_ops','wgu_catalog','bsda_courses',
                            'idlehacking_kb','ih_market_companion','reckless_ben')
          AND has_database_privilege(r.rolname, d.datname, 'CONNECT')
    ) THEN
        failures := array_append(failures, 'cross_db_connect_isolation');
    END IF;

    IF array_length(failures, 1) IS NOT NULL THEN
        RAISE EXCEPTION 'SJC Intel full validation failed: %', array_to_string(failures, ', ');
    END IF;
END $$;
