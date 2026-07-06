import os
import logging

from scripts.file_adapter import FileAdapter
from scripts.pg_adapter import PgAdapter

logger = logging.getLogger(__name__)


def create_adapter(backend=None):
    backend = backend or os.environ.get("SJC_INTEL_ADAPTER_BACKEND", "file")
    if backend == "pg":
        return PgAdapter()
    return FileAdapter()


class StorageFacade:

    def __init__(self, primary_backend=None, fallback_backend=None):
        self._primary = create_adapter(primary_backend)
        self._fallback = fallback_backend if fallback_backend else self._resolve_fallback()
        logger.info("StorageFacade primary=%s fallback=%s",
                     type(self._primary).__name__,
                     type(self._fallback).__name__ if self._fallback else "none")

    def _resolve_fallback(self):
        if isinstance(self._primary, PgAdapter):
            fallback_enabled = os.environ.get("SJC_INTEL_FILE_FALLBACK_ENABLED", "true").lower() in (
                "true",
                "1",
                "yes",
            )
            if fallback_enabled:
                return FileAdapter()
        return None

    def read_item(self, item_id):
        if isinstance(self._primary, PgAdapter):
            try:
                result = self._primary.read_item(item_id)
                if result is not None:
                    return result
            except RuntimeError:
                pass
            except Exception as e:
                logger.warning("Primary read failed, falling back: %s", e)
            if self._fallback:
                return self._fallback.read_item(item_id)
            return None
        return self._primary.read_item(item_id)

    def write_item(self, item_id, data):
        return self._primary.write_item(item_id, data)

    def list_items(self, filter_dict=None):
        if isinstance(self._primary, PgAdapter):
            try:
                return self._primary.list_items(filter_dict)
            except RuntimeError:
                pass
            except Exception as e:
                logger.warning("Primary list failed, falling back: %s", e)
            if self._fallback:
                return self._fallback.list_items(filter_dict)
            return []
        return self._primary.list_items(filter_dict)

    def get_health(self):
        primary_health = self._primary.get_health()
        fallback_available = self._fallback is not None
        primary_health["fallback_available"] = fallback_available
        return primary_health
