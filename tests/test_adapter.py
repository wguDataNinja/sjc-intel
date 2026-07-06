import os
import sys
import yaml
import tempfile
import shutil

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
sys.path.insert(0, REPO_ROOT)

from scripts.file_adapter import FileAdapter
from scripts.pg_adapter import PgAdapter
from scripts.storage_adapter import StorageFacade, create_adapter


def setup_module():
    os.environ.setdefault("SJC_INTEL_PG_ADAPTER_ENABLED", "false")


class TestFileAdapter:

    def setup_method(self):
        self.adapter = FileAdapter()

    def test_read_item_found(self):
        item = self.adapter.read_item("SJC-SL-20260704-0001")
        assert item is not None
        assert item.get("item_id") == "SJC-SL-20260704-0001"
        assert item.get("title") is not None

    def test_read_item_not_found(self):
        item = self.adapter.read_item("SJC-NONEXISTENT-99999999-9999")
        assert item is None

    def test_list_items_default(self):
        items = self.adapter.list_items()
        assert isinstance(items, list)
        assert len(items) > 0
        for item in items:
            assert "item_id" in item

    def test_list_items_filter_by_source(self):
        items = self.adapter.list_items({"source_id": "st_johns_citizen"})
        assert isinstance(items, list)
        if items:
            for item in items:
                assert item.get("source_id") == "st_johns_citizen"

    def test_list_items_filter_by_status(self):
        items = self.adapter.list_items({"review_status": "verified"})
        assert isinstance(items, list)
        if items:
            for item in items:
                assert item.get("review_status") == "verified"

    def test_list_items_filter_by_entity_type_source(self):
        items = self.adapter.list_items({"entity_type": "source"})
        assert isinstance(items, list)
        assert len(items) > 0
        for item in items:
            assert "source_id" in item

    def test_list_items_filter_by_entity_type_tracked_entity(self):
        items = self.adapter.list_items({"entity_type": "tracked_entities"})
        assert isinstance(items, list)
        assert len(items) > 0
        for item in items:
            assert "entity_id" in item

    def test_write_and_read_item_idempotent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = FileAdapter(root_dir=tmpdir)
            intel_dir = os.path.join(tmpdir, "data", "intel_items", "2026-07-05")
            os.makedirs(intel_dir)
            item = {
                "item_id": "SJC-TEMP-20260705-9999",
                "title": "Temp Test Item",
                "source_id": "temp_test",
                "review_status": "pending_review",
                "created_at": "2026-07-05T12:00:00Z",
                "updated_at": "2026-07-05T12:00:00Z",
            }
            result = adapter.write_item(item["item_id"], item)
            assert result is True

            read_back = adapter.read_item("SJC-TEMP-20260705-9999")
            assert read_back is not None
            assert read_back["item_id"] == "SJC-TEMP-20260705-9999"
            assert read_back["title"] == "Temp Test Item"

            updated = dict(item)
            updated["title"] = "Updated Temp Item"
            adapter.write_item(item["item_id"], updated)
            read_again = adapter.read_item("SJC-TEMP-20260705-9999")
            assert read_again["title"] == "Updated Temp Item"

    def test_get_health(self):
        health = self.adapter.get_health()
        assert health["adapter"] == "file"
        assert health["status"] == "ok"
        assert isinstance(health["total_items"], int)
        assert health["total_items"] > 0
        assert isinstance(health["intel_item_files"], int)
        assert health["intel_item_files"] > 0

    def test_list_sources_entity_type(self):
        items = self.adapter.list_items({"entity_type": "sources"})
        assert isinstance(items, list)
        for item in items:
            assert "source_id" in item

    def test_list_tracked_entities_entity_type(self):
        items = self.adapter.list_items({"entity_type": "tracked_entities"})
        assert isinstance(items, list)
        for item in items:
            assert "entity_id" in item


class TestPgAdapter:

    def setup_method(self):
        self.adapter = PgAdapter()

    def test_read_item_raises_when_disabled(self):
        try:
            self.adapter.read_item("any-id")
            assert False, "Expected RuntimeError"
        except RuntimeError as e:
            assert "disabled" in str(e).lower()

    def test_write_item_raises_when_disabled(self):
        try:
            self.adapter.write_item("any-id", {})
            assert False, "Expected RuntimeError"
        except RuntimeError as e:
            assert "disabled" in str(e).lower()

    def test_list_items_raises_when_disabled(self):
        try:
            self.adapter.list_items()
            assert False, "Expected RuntimeError"
        except RuntimeError as e:
            assert "disabled" in str(e).lower()

    def test_get_health_returns_disabled(self):
        health = self.adapter.get_health()
        assert health["adapter"] == "postgresql"
        assert health["status"] == "disabled"
        assert health["enabled"] is False


class TestPgAdapterEnabled:

    def setup_method(self):
        os.environ["SJC_INTEL_PG_ADAPTER_ENABLED"] = "true"
        self.conn = FakeConnection()
        self.adapter = PgAdapter(connection_factory=lambda readonly=True: self.conn)

    def teardown_method(self):
        os.environ["SJC_INTEL_PG_ADAPTER_ENABLED"] = "false"

    def test_read_item_queries_known_tables(self):
        self.conn.cursor_obj.rows = [{"item_id": "SJC-TEST-1", "title": "Test"}]
        result = self.adapter.read_item("SJC-TEST-1")
        assert result["item_id"] == "SJC-TEST-1"
        assert "SELECT * FROM app.intel_items" in self.conn.cursor_obj.executed[0][0]

    def test_list_items_reads_intel_items(self):
        self.conn.cursor_obj.rows = [{"item_id": "SJC-TEST-1", "source_id": "test"}]
        result = self.adapter.list_items()
        assert result == [{"item_id": "SJC-TEST-1", "source_id": "test"}]
        assert "FROM app.intel_items" in self.conn.cursor_obj.executed[0][0]

    def test_write_item_uses_transaction_and_upserts_dedupe(self):
        result = self.adapter.write_item(
            "SJC-TEST-1",
            {
                "title": "Test",
                "summary": "Summary",
                "source_id": "test_source",
                "source_url": "https://example.com/test",
                "_dedupe_key": "test-source::test",
                "_signal": "high_signal",
                "created_at": "2026-07-06T00:00:00Z",
            },
        )
        assert result is True
        assert self.conn.committed is True
        sql_text = "\n".join(sql for sql, _params in self.conn.cursor_obj.executed)
        assert "INSERT INTO app.sources" in sql_text
        assert "INSERT INTO app.intel_items" in sql_text
        assert "INSERT INTO app.dedupe_index_entries" in sql_text

    def test_get_health_returns_ok(self):
        self.conn.cursor_obj.rows_by_execute = [
            [{"pg_version": "PostgreSQL 16", "database_name": "sjc_intel", "database_user": "sjc_intel_reader"}],
            [{"count": 3}],
            [{"count": 2}],
        ]
        health = self.adapter.get_health()
        assert health["status"] == "ok"
        assert health["database"] == "sjc_intel"
        assert health["intel_items"] == 3


class TestStorageFacade:

    def test_create_adapter_default_is_file(self):
        adapter = create_adapter()
        assert isinstance(adapter, FileAdapter)

    def test_create_adapter_file_explicit(self):
        adapter = create_adapter("file")
        assert isinstance(adapter, FileAdapter)

    def test_create_adapter_pg(self):
        adapter = create_adapter("pg")
        assert isinstance(adapter, PgAdapter)

    def test_facade_file_primary(self):
        facade = StorageFacade(primary_backend="file")
        items = facade.list_items()
        assert len(items) > 0
        health = facade.get_health()
        assert health["adapter"] == "file"

    def test_facade_pg_primary_with_file_fallback(self):
        os.environ["SJC_INTEL_PG_ADAPTER_ENABLED"] = "false"
        facade = StorageFacade(primary_backend="pg", fallback_backend=FileAdapter())
        items = facade.list_items()
        assert len(items) > 0
        health = facade.get_health()
        assert health["status"] in ("disabled", "error")


class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class FakeCursor:
    def __init__(self):
        self.executed = []
        self.rows = []
        self.rows_by_execute = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        if self.rows_by_execute:
            self.rows = self.rows_by_execute.pop(0)

    def fetchone(self):
        if not self.rows:
            return None
        return self.rows.pop(0)

    def fetchall(self):
        rows = self.rows
        self.rows = []
        return rows
