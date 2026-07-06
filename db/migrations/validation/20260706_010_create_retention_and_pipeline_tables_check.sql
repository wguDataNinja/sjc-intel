-- Validation: 20260706_010_create_retention_and_pipeline_tables

SELECT 'source_retention_policies_exists' AS check_name,
       to_regclass('app.source_retention_policies') IS NOT NULL AS passed;

SELECT 'raw_artifact_records_exists' AS check_name,
       to_regclass('app.raw_artifact_records') IS NOT NULL AS passed;

SELECT 'pipeline_runs_exists' AS check_name,
       to_regclass('app.pipeline_runs') IS NOT NULL AS passed;

SELECT 'retention_prune_index_exists' AS check_name,
       to_regclass('app.idx_raw_artifact_records_source_retain_until') IS NOT NULL AS passed;
