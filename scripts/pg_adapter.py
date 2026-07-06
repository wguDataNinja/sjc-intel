import os
import logging

from scripts.adapter_base import StorageAdapter

logger = logging.getLogger(__name__)


class PgAdapter(StorageAdapter):

    def __init__(self):
        self._enabled = os.environ.get("SJC_INTEL_PG_ADAPTER_ENABLED", "false").lower() in ("true", "1", "yes")
        self._pg_url = os.environ.get("SJC_INTEL_PG_URL", "")
        self._pg_database = os.environ.get("SJC_INTEL_PG_DATABASE", "sjc_intel")
        self._pg_writer_user = os.environ.get("SJC_INTEL_PG_WRITER_USER", "sjc_intel_writer")
        self._pg_reader_user = os.environ.get("SJC_INTEL_PG_READER_USER", "sjc_intel_reader")

    def _check_enabled(self):
        if not self._enabled:
            raise RuntimeError("PostgreSQL adapter is disabled")

    def read_item(self, item_id):
        self._check_enabled()
        try:
            return self._query_item(item_id)
        except Exception as e:
            logger.warning("PG read_item failed, falling back: %s", e)
            return None

    def write_item(self, item_id, data):
        self._check_enabled()
        try:
            return self._upsert_item(item_id, data)
        except Exception as e:
            logger.warning("PG write_item failed, falling back: %s", e)
            return False

    def list_items(self, filter_dict=None):
        self._check_enabled()
        try:
            return self._query_items(filter_dict or {})
        except Exception as e:
            logger.warning("PG list_items failed, falling back: %s", e)
            return []

    def get_health(self):
        if not self._enabled:
            return {
                "adapter": "postgresql",
                "status": "disabled",
                "enabled": False,
            }
        try:
            return self._check_connection()
        except Exception as e:
            logger.warning("PG health check failed: %s", e)
            return {
                "adapter": "postgresql",
                "status": "error",
                "enabled": True,
                "error": str(e),
            }

    def _query_item(self, item_id):
        raise NotImplementedError("PG adapter requires psycopg2 and live database")

    def _upsert_item(self, item_id, data):
        raise NotImplementedError("PG adapter requires psycopg2 and live database")

    def _query_items(self, filter_dict):
        raise NotImplementedError("PG adapter requires psycopg2 and live database")

    def _check_connection(self):
        raise NotImplementedError("PG adapter requires psycopg2 and live database")
