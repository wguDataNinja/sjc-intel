import json
import logging
from datetime import datetime, timezone

from scripts.file_adapter import FileAdapter
from scripts.pg_adapter import PgAdapter

logger = logging.getLogger(__name__)


class ParityReport:

    def __init__(self, file_adapter=None, pg_adapter=None):
        self._file = file_adapter or FileAdapter()
        self._pg = pg_adapter or PgAdapter()
        health = self._pg.get_health()
        self._pg_enabled = health.get("enabled", False) and health.get("status") == "ok"

    def compare_item_counts(self):
        file_items = self._file.list_items()
        file_count = len(file_items)
        pg_count = 0
        pg_items = []
        if self._pg_enabled:
            try:
                pg_items = self._pg.list_items()
                pg_count = len(pg_items)
            except Exception as e:
                logger.warning("PG list_items failed during parity: %s", e)
        return {
            "file_count": file_count,
            "pg_count": pg_count,
            "match": file_count == pg_count,
            "difference": file_count - pg_count,
        }

    def compare_by_field(self, field_name):
        file_items = self._file.list_items()
        file_counts = {}
        for item in file_items:
            val = item.get(field_name, "__missing__")
            file_counts[val] = file_counts.get(val, 0) + 1
        pg_counts = {}
        if self._pg_enabled:
            try:
                pg_items = self._pg.list_items()
                for item in pg_items:
                    val = item.get(field_name, "__missing__")
                    pg_counts[val] = pg_counts.get(val, 0) + 1
            except Exception as e:
                logger.warning("PG field compare failed: %s", e)
        return {
            "field": field_name,
            "file_distribution": file_counts,
            "pg_distribution": pg_counts,
            "match": file_counts == pg_counts,
        }

    def compare_dedupe_keys(self):
        file_items = self._file.list_items()
        file_keys = set()
        for item in file_items:
            key = item.get("_dedupe_key") or item.get("dedupe_key")
            if key:
                file_keys.add(key)
        pg_keys = set()
        if self._pg_enabled:
            try:
                pg_items = self._pg.list_items()
                for item in pg_items:
                    key = item.get("_dedupe_key") or item.get("dedupe_key")
                    if key:
                        pg_keys.add(key)
            except Exception as e:
                logger.warning("PG dedupe compare failed: %s", e)
        only_in_file = file_keys - pg_keys
        only_in_pg = pg_keys - file_keys
        return {
            "file_dedupe_count": len(file_keys),
            "pg_dedupe_count": len(pg_keys),
            "common_count": len(file_keys & pg_keys),
            "only_in_file": list(only_in_file)[:20],
            "only_in_pg": list(only_in_pg)[:20],
            "match": file_keys == pg_keys,
        }

    def generate(self):
        report = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pg_enabled": self._pg_enabled,
            "item_count": self.compare_item_counts(),
            "by_source": self.compare_by_field("source_id"),
            "by_review_status": self.compare_by_field("review_status"),
            "dedupe_keys": self.compare_dedupe_keys(),
        }
        if self._pg_enabled:
            report["pg_status"] = "connected"
        else:
            report["pg_status"] = "disabled"
        return report

    def generate_json(self, indent=2):
        return json.dumps(self.generate(), indent=indent, default=str)

    def print_report(self):
        report = self.generate()
        print("=" * 60)
        print("SJC Intel — Storage Parity Report")
        print(f"Generated: {report['generated_at']}")
        print("=" * 60)
        print(f"PG Adapter: {report['pg_status']}")
        print()
        print("Item Counts:")
        ic = report["item_count"]
        print(f"  File: {ic['file_count']}  PG: {ic['pg_count']}  "
              f"{'MATCH' if ic['match'] else 'MISMATCH (diff: ' + str(ic['difference']) + ')'}")
        print()
        print("By Source:")
        bs = report["by_source"]
        print(f"  {'MATCH' if bs['match'] else 'MISMATCH'}")
        if not bs["match"]:
            for src in sorted(set(list(bs["file_distribution"].keys()) + list(bs["pg_distribution"].keys()))):
                fc = bs["file_distribution"].get(src, 0)
                pc = bs["pg_distribution"].get(src, 0)
                if fc != pc:
                    print(f"    {src}: file={fc} pg={pc}")
        print()
        print("By Review Status:")
        br = report["by_review_status"]
        print(f"  {'MATCH' if br['match'] else 'MISMATCH'}")
        print()
        print("Dedupe Keys:")
        dk = report["dedupe_keys"]
        print(f"  {'MATCH' if dk['match'] else 'MISMATCH'}")
        if not dk["match"]:
            print(f"  Only in file: {len(dk['only_in_file'])}")
            print(f"  Only in PG:   {len(dk['only_in_pg'])}")
        print("=" * 60)
        return report


def main():
    import sys
    report = ParityReport()
    if "--json" in sys.argv:
        print(report.generate_json())
    else:
        report.print_report()


if __name__ == "__main__":
    main()
