-- Validation: 20260706_011_create_metric_snapshots

SELECT 'metric_snapshots_exists' AS check_name,
       to_regclass('app.metric_snapshots') IS NOT NULL AS passed;

SELECT 'metric_snapshots_unique_key_exists' AS check_name,
       EXISTS (
           SELECT 1
           FROM pg_indexes
           WHERE schemaname = 'app'
             AND tablename = 'metric_snapshots'
             AND indexdef LIKE '%snapshot_date%'
             AND indexdef LIKE '%metric_name%'
             AND indexdef LIKE '%dimensions_hash%'
       ) AS passed;
