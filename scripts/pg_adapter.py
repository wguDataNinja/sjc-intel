import logging
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from urllib.parse import urlparse

from scripts.adapter_base import StorageAdapter

logger = logging.getLogger(__name__)


try:
    import psycopg2
    from psycopg2.extras import Json, RealDictCursor
except ImportError:  # pragma: no cover - exercised only on hosts without psycopg2
    psycopg2 = None
    Json = None
    RealDictCursor = None


READ_TABLES = {
    "intel_item": ("app.intel_items", "item_id"),
    "intel_items": ("app.intel_items", "item_id"),
    "source": ("app.sources", "source_id"),
    "sources": ("app.sources", "source_id"),
    "source_event": ("app.source_events", "event_id"),
    "source_events": ("app.source_events", "event_id"),
    "tracked_entity": ("app.tracked_entities", "entity_id"),
    "tracked_entities": ("app.tracked_entities", "entity_id"),
    "queue_entry": ("app.review_queue_entries", "queue_id"),
    "queue_entries": ("app.review_queue_entries", "queue_id"),
}


LIST_QUERIES = {
    "source": "SELECT * FROM app.sources",
    "sources": "SELECT * FROM app.sources",
    "source_event": "SELECT * FROM app.source_events",
    "source_events": "SELECT * FROM app.source_events",
    "tracked_entity": "SELECT * FROM app.tracked_entities",
    "tracked_entities": "SELECT * FROM app.tracked_entities",
    "queue_entry": "SELECT * FROM app.review_queue_entries",
    "queue_entries": "SELECT * FROM app.review_queue_entries",
}


INTEL_COLUMNS = [
    "item_id",
    "title",
    "summary",
    "source_id",
    "source_event_id",
    "source_url",
    "source_published_at",
    "discovered_at",
    "discovered_by",
    "topics",
    "communities",
    "geographic_scope",
    "urgency",
    "verification_status",
    "sensitivity",
    "recommended_channels",
    "raw_excerpt",
    "citation",
    "primary_topic",
    "interest_tags",
    "resident_relevance",
    "taxonomy_gap",
    "human_review_required",
    "review_status",
    "reviewer_notes",
    "tracked_entity_ids",
    "superseded_by",
    "dedupe_key",
    "beat",
    "signal",
    "category",
    "app_id",
    "pdf_urls",
    "map_url",
    "district",
    "raw_text",
    "meeting_date",
    "agenda_item_number",
    "action_type",
    "source_type",
    "internal_metadata",
    "created_at",
    "updated_at",
]


class PgAdapter(StorageAdapter):
    """PostgreSQL-backed implementation of the SJC storage adapter."""

    def __init__(self, connection_factory=None):
        self._enabled = _truthy(os.environ.get("SJC_INTEL_PG_ADAPTER_ENABLED", "false"))
        self._connection_factory = connection_factory
        self._pg_url = os.environ.get("SJC_INTEL_PG_URL", "")
        self._reader_url = os.environ.get("SJC_INTEL_PG_READER_URL", self._pg_url)
        self._writer_url = os.environ.get("SJC_INTEL_PG_WRITER_URL", self._pg_url)
        self._pg_database = os.environ.get("SJC_INTEL_PG_DATABASE", "sjc_intel")
        self._pg_host = os.environ.get("SJC_INTEL_PG_HOST", "")
        self._pg_port = os.environ.get("SJC_INTEL_PG_PORT", "")
        self._pg_writer_user = os.environ.get("SJC_INTEL_PG_WRITER_USER", "sjc_intel_writer")
        self._pg_reader_user = os.environ.get("SJC_INTEL_PG_READER_USER", "sjc_intel_reader")

    def _check_enabled(self):
        if not self._enabled:
            raise RuntimeError("PostgreSQL adapter is disabled")
        if psycopg2 is None and self._connection_factory is None:
            raise RuntimeError("PostgreSQL adapter requires psycopg2")

    def read_item(self, item_id):
        self._check_enabled()
        try:
            return self._query_item(item_id)
        except Exception as e:
            logger.warning("PG read_item failed, falling back: %s", _safe_error(e))
            return None

    def write_item(self, item_id, data):
        self._check_enabled()
        try:
            return self._upsert_item(item_id, data)
        except Exception as e:
            logger.warning("PG write_item failed: %s", _safe_error(e))
            return False

    def list_items(self, filter_dict=None):
        self._check_enabled()
        try:
            return self._query_items(filter_dict or {})
        except Exception as e:
            logger.warning("PG list_items failed, falling back: %s", _safe_error(e))
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
            logger.warning("PG health check failed: %s", _safe_error(e))
            return {
                "adapter": "postgresql",
                "status": "error",
                "enabled": True,
                "error": _safe_error(e),
            }

    @contextmanager
    def _transaction(self, readonly=True):
        conn = self._connect(readonly=readonly)
        try:
            yield conn
            if not readonly:
                conn.commit()
        except Exception:
            if not readonly:
                conn.rollback()
            raise
        finally:
            conn.close()

    def _connect(self, readonly=True):
        if self._connection_factory:
            try:
                return self._connection_factory(readonly=readonly)
            except TypeError:
                return self._connection_factory()

        url = self._reader_url if readonly else self._writer_url
        if url:
            return psycopg2.connect(url, cursor_factory=RealDictCursor)

        kwargs = {"dbname": self._pg_database, "cursor_factory": RealDictCursor}
        if self._pg_host:
            kwargs["host"] = self._pg_host
        if self._pg_port:
            kwargs["port"] = self._pg_port
        kwargs["user"] = self._pg_reader_user if readonly else self._pg_writer_user
        return psycopg2.connect(**kwargs)

    def _query_item(self, item_id):
        with self._transaction(readonly=True) as conn:
            with conn.cursor() as cur:
                for table, key_column in [
                    ("app.intel_items", "item_id"),
                    ("app.sources", "source_id"),
                    ("app.source_events", "event_id"),
                    ("app.tracked_entities", "entity_id"),
                    ("app.review_queue_entries", "queue_id"),
                ]:
                    cur.execute(f"SELECT * FROM {table} WHERE {key_column} = %s", (item_id,))
                    row = cur.fetchone()
                    if row:
                        return _row_to_dict(row)
        return None

    def _upsert_item(self, item_id, data):
        payload = self._normalize_intel_item(item_id, data)
        with self._transaction(readonly=False) as conn:
            with conn.cursor() as cur:
                self._upsert_source(cur, payload, data)
                self._upsert_intel_item(cur, payload)
                self._upsert_dedupe_entry(cur, payload)
        return True

    def _query_items(self, filter_dict):
        entity_type = filter_dict.get("entity_type", "intel_items")
        limit = _bounded_int(filter_dict.get("limit"), default=500, minimum=1, maximum=1000)
        offset = _bounded_int(filter_dict.get("offset"), default=0, minimum=0, maximum=1000000)

        with self._transaction(readonly=True) as conn:
            with conn.cursor() as cur:
                if entity_type in LIST_QUERIES:
                    query = f"{LIST_QUERIES[entity_type]} ORDER BY 1 LIMIT %s OFFSET %s"
                    cur.execute(query, (limit, offset))
                    return [_row_to_dict(row) for row in cur.fetchall()]

                conditions = []
                params = []
                if filter_dict.get("source_id"):
                    conditions.append("source_id = %s")
                    params.append(filter_dict["source_id"])
                status = filter_dict.get("review_status") or filter_dict.get("status")
                if status:
                    conditions.append("review_status = %s")
                    params.append(status)
                if filter_dict.get("category"):
                    conditions.append("category = %s")
                    params.append(filter_dict["category"])
                if filter_dict.get("since"):
                    conditions.append("discovered_at >= %s")
                    params.append(filter_dict["since"])

                where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""
                params.extend([limit, offset])
                cur.execute(
                    f"""
                    SELECT *
                    FROM app.intel_items
                    {where_sql}
                    ORDER BY discovered_at DESC, item_id
                    LIMIT %s OFFSET %s
                    """,
                    tuple(params),
                )
                return [_row_to_dict(row) for row in cur.fetchall()]

    def _check_connection(self):
        with self._transaction(readonly=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT version() AS pg_version,
                           current_database() AS database_name,
                           current_user AS database_user
                    """
                )
                row = _row_to_dict(cur.fetchone())
                cur.execute("SELECT COUNT(*) AS count FROM app.intel_items")
                intel_count = _count_value(cur.fetchone())
                cur.execute("SELECT COUNT(*) AS count FROM app.sources")
                source_count = _count_value(cur.fetchone())
        return {
            "adapter": "postgresql",
            "status": "ok",
            "enabled": True,
            "database": row.get("database_name"),
            "database_user": row.get("database_user"),
            "pg_version": row.get("pg_version"),
            "intel_items": intel_count,
            "sources": source_count,
        }

    def _normalize_intel_item(self, item_id, data):
        now = datetime.now(timezone.utc).isoformat()
        source_url = data.get("source_url") or _citation_value(data, "url") or data.get("url") or "about:blank"
        title = data.get("title") or item_id
        summary = data.get("summary") or data.get("raw_excerpt") or title
        created_at = data.get("created_at") or data.get("discovered_at") or now
        discovered_at = data.get("discovered_at") or created_at

        payload = {
            "item_id": item_id,
            "title": title,
            "summary": summary,
            "source_id": data.get("source_id") or "unknown_source",
            "source_event_id": data.get("source_event_id"),
            "source_url": source_url,
            "source_published_at": data.get("source_published_at") or data.get("published_at"),
            "discovered_at": discovered_at,
            "discovered_by": data.get("discovered_by"),
            "topics": _as_list(data.get("topics")),
            "communities": _as_list(data.get("communities")) or None,
            "geographic_scope": data.get("geographic_scope") or "county_wide",
            "urgency": data.get("urgency") or "ongoing",
            "verification_status": data.get("verification_status") or "unverified",
            "sensitivity": data.get("sensitivity") or "low",
            "recommended_channels": _as_list(data.get("recommended_channels")) or None,
            "raw_excerpt": data.get("raw_excerpt") or summary,
            "citation": _json_value(data.get("citation")),
            "primary_topic": data.get("primary_topic"),
            "interest_tags": _as_list(data.get("interest_tags")) or None,
            "resident_relevance": _json_value(data.get("resident_relevance")),
            "taxonomy_gap": data.get("taxonomy_gap"),
            "human_review_required": bool(data.get("human_review_required", False)),
            "review_status": data.get("review_status") or "pending_review",
            "reviewer_notes": data.get("reviewer_notes"),
            "tracked_entity_ids": _as_list(data.get("tracked_entity_ids")) or None,
            "superseded_by": data.get("superseded_by"),
            "dedupe_key": data.get("dedupe_key") or data.get("_dedupe_key"),
            "beat": data.get("beat") or data.get("_beat"),
            "signal": _normalize_signal(data.get("signal") or data.get("_signal")),
            "category": data.get("category") or data.get("_category"),
            "app_id": data.get("app_id") or data.get("_app_id"),
            "pdf_urls": _as_list(data.get("pdf_urls") or data.get("_pdf_urls")) or None,
            "map_url": data.get("map_url") or data.get("_map_url"),
            "district": data.get("district") or data.get("_district"),
            "raw_text": data.get("raw_text") or data.get("_raw_text"),
            "meeting_date": data.get("meeting_date") or data.get("_meeting_date"),
            "agenda_item_number": data.get("agenda_item_number") or data.get("_agenda_item_number"),
            "action_type": data.get("action_type") or data.get("_action_type"),
            "source_type": data.get("source_type") or data.get("_source_type"),
            "internal_metadata": _json_value(data.get("internal_metadata")),
            "created_at": created_at,
            "updated_at": data.get("updated_at"),
        }
        if not payload["topics"]:
            payload["topics"] = ["general"]
        return payload

    def _upsert_source(self, cur, payload, original_data):
        source_id = payload["source_id"]
        source_url = payload["source_url"]
        parsed = urlparse(source_url)
        base_domain = parsed.netloc or "unknown"
        source_name = (
            original_data.get("source_name")
            or original_data.get("name")
            or source_id.replace("_", " ").title()
        )
        source_type = payload.get("source_type") or original_data.get("source_type") or "official_public_record"
        cur.execute(
            """
            INSERT INTO app.sources (
                source_id, name, description, url, base_domain, source_type,
                relevance, monitor_frequency, automatable, status, topics,
                communities, discovered_at, updated_at
            )
            VALUES (
                %(source_id)s, %(name)s, %(description)s, %(url)s, %(base_domain)s,
                %(source_type)s, %(relevance)s, %(monitor_frequency)s, %(automatable)s,
                %(status)s, %(topics)s, %(communities)s, %(discovered_at)s, %(updated_at)s
            )
            ON CONFLICT (source_id) DO UPDATE SET
                name = COALESCE(app.sources.name, EXCLUDED.name),
                url = COALESCE(NULLIF(EXCLUDED.url, 'about:blank'), app.sources.url),
                base_domain = COALESCE(NULLIF(EXCLUDED.base_domain, 'unknown'), app.sources.base_domain),
                source_type = COALESCE(EXCLUDED.source_type, app.sources.source_type),
                topics = COALESCE(EXCLUDED.topics, app.sources.topics),
                communities = COALESCE(EXCLUDED.communities, app.sources.communities),
                updated_at = COALESCE(EXCLUDED.updated_at, app.sources.updated_at),
                updated_at_db = now()
            """,
            {
                "source_id": source_id,
                "name": source_name,
                "description": original_data.get("source_description") or f"SJC Intel source {source_id}",
                "url": source_url,
                "base_domain": base_domain,
                "source_type": source_type,
                "relevance": original_data.get("relevance") or "MEDIUM",
                "monitor_frequency": original_data.get("monitor_frequency") or "weekly",
                "automatable": original_data.get("automatable") or "LIKELY",
                "status": original_data.get("source_status") or "active",
                "topics": payload["topics"],
                "communities": payload["communities"],
                "discovered_at": payload["discovered_at"],
                "updated_at": payload["updated_at"],
            },
        )

    def _upsert_intel_item(self, cur, payload):
        placeholders = ", ".join([f"%({column})s" for column in INTEL_COLUMNS])
        columns = ", ".join(INTEL_COLUMNS)
        update_columns = [column for column in INTEL_COLUMNS if column not in ("item_id", "created_at")]
        updates = ",\n                ".join([f"{column} = EXCLUDED.{column}" for column in update_columns])
        cur.execute(
            f"""
            INSERT INTO app.intel_items ({columns})
            VALUES ({placeholders})
            ON CONFLICT (item_id) DO UPDATE SET
                {updates},
                updated_at_db = now()
            """,
            payload,
        )

    def _upsert_dedupe_entry(self, cur, payload):
        if not payload.get("dedupe_key"):
            return
        cur.execute(
            """
            INSERT INTO app.dedupe_index_entries (
                key, item_id, title, source_id, beat, discovered_at, status
            )
            VALUES (
                %(key)s, %(item_id)s, %(title)s, %(source_id)s, %(beat)s,
                %(discovered_at)s, %(status)s
            )
            ON CONFLICT (key) DO UPDATE SET
                item_id = EXCLUDED.item_id,
                title = EXCLUDED.title,
                source_id = EXCLUDED.source_id,
                beat = EXCLUDED.beat,
                discovered_at = EXCLUDED.discovered_at,
                status = EXCLUDED.status
            """,
            {
                "key": payload["dedupe_key"],
                "item_id": payload["item_id"],
                "title": payload["title"],
                "source_id": payload["source_id"],
                "beat": payload["beat"],
                "discovered_at": payload["discovered_at"],
                "status": payload["review_status"],
            },
        )


def _truthy(value):
    return str(value).lower() in ("true", "1", "yes")


def _safe_error(error):
    return error.__class__.__name__


def _row_to_dict(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return dict(row)
    if hasattr(row, "keys"):
        return {key: row[key] for key in row.keys()}
    return row


def _count_value(row):
    row = _row_to_dict(row)
    if isinstance(row, dict):
        return row.get("count", 0)
    return row[0] if row else 0


def _bounded_int(value, default, minimum, maximum):
    if value is None:
        return default
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, number))


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _json_value(value):
    if value is None:
        return None
    if Json is None:
        return value
    return Json(value)


def _citation_value(data, key):
    citation = data.get("citation") or {}
    if isinstance(citation, dict):
        return citation.get(key)
    return None


def _normalize_signal(value):
    if value in ("high", "medium", "low_signal", None):
        return value
    mapping = {
        "high_signal": "high",
        "medium_signal": "medium",
        "routine_noise": "low_signal",
        "low": "low_signal",
    }
    return mapping.get(value)
