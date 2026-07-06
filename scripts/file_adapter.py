import os
import re
import yaml

from scripts.adapter_base import StorageAdapter

INTEL_ITEMS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "intel_items")
REGISTRY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "registry")
SOURCE_EVENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "source_events")
QUEUE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "review_queue")

SKIP_FILES = {"daily_cycle_summary.yaml", "bcc_weekly_summary.yaml", "bcc_calibration_notes.md"}
SKIP_PREFIXES = {".deprecated"}


class FileAdapter(StorageAdapter):

    def __init__(self, root_dir=None):
        self._root_dir = root_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._intel_items_dir = os.path.join(self._root_dir, "data", "intel_items")
        self._registry_dir = os.path.join(self._root_dir, "registry")
        self._source_events_dir = os.path.join(self._root_dir, "data", "source_events")
        self._queue_dir = os.path.join(self._root_dir, "data", "review_queue")

    def _item_id_to_date(self, item_id):
        m = re.match(r"SJC-[A-Z]+-(\d{4})(\d{2})(\d{2})", item_id)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        return None

    def _walk_yaml_files(self, directory):
        files = []
        if not os.path.isdir(directory):
            return files
        for root, dirs, fnames in os.walk(directory):
            dirs[:] = [d for d in dirs if not any(skip in d for skip in SKIP_PREFIXES)]
            for fname in sorted(fnames):
                if not fname.endswith(".yaml") or fname in SKIP_FILES:
                    continue
                if any(fname.endswith(skip) for skip in SKIP_PREFIXES):
                    continue
                files.append(os.path.join(root, fname))
        return files

    def _load_yaml(self, path):
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def read_item(self, item_id):
        date_prefix = self._item_id_to_date(item_id)
        candidates = []
        if date_prefix:
            date_dir = os.path.join(self._intel_items_dir, date_prefix)
            if os.path.isdir(date_dir):
                candidates.extend(self._walk_yaml_files(date_dir))
            date_events_dir = os.path.join(self._source_events_dir, date_prefix)
            if os.path.isdir(date_events_dir):
                candidates.extend(self._walk_yaml_files(date_events_dir))
        if not candidates:
            candidates = self._walk_yaml_files(self._intel_items_dir)
            candidates.extend(self._walk_yaml_files(self._source_events_dir))
        for fpath in candidates:
            data = self._load_yaml(fpath)
            if data is None:
                continue
            items = data.get("items", [])
            for item in items:
                if item.get("item_id") == item_id:
                    return item
            if isinstance(data, dict) and data.get("item_id") == item_id:
                return data
            if isinstance(data, dict) and data.get("event_id") == item_id:
                return data
            if isinstance(data, dict) and data.get("source_id") == item_id:
                return data
            if isinstance(data, dict) and data.get("entity_id") == item_id:
                return data
            if isinstance(data, dict) and data.get("queue_id") == item_id:
                return data
        return None

    def write_item(self, item_id, data):
        date_prefix = self._item_id_to_date(item_id)
        if not date_prefix:
            return False
        date_dir = os.path.join(self._intel_items_dir, date_prefix)
        os.makedirs(date_dir, exist_ok=True)
        target_file = os.path.join(date_dir, f"{data.get('source_id', 'unknown')}.yaml")
        existing = self._load_yaml(target_file) if os.path.exists(target_file) else None
        if existing and "items" in existing:
            items = existing["items"]
            for i, item in enumerate(items):
                if item.get("item_id") == item_id:
                    items[i] = data
                    break
            else:
                items.append(data)
            existing["total_items"] = len(items)
        elif existing and existing.get("item_id") == item_id:
            existing.update(data)
        else:
            record = {
                "source_id": data.get("source_id", "unknown"),
                "items": [data],
                "total_items": 1,
            }
            existing = record
        with open(target_file, "w") as f:
            yaml.dump(existing, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True

    def list_items(self, filter_dict=None):
        results = []
        filter_dict = filter_dict or {}
        source_id_filter = filter_dict.get("source_id")
        status_filter = filter_dict.get("status") or filter_dict.get("review_status")
        entity_type_filter = filter_dict.get("entity_type")

        if entity_type_filter == "source" or entity_type_filter == "sources":
            sources_file = os.path.join(self._registry_dir, "sources.yaml")
            data = self._load_yaml(sources_file)
            if data:
                items = data.get("sources", [])
                for item in items:
                    if source_id_filter and item.get("source_id") != source_id_filter:
                        continue
                    results.append(item)
            return results

        if entity_type_filter == "tracked_entity" or entity_type_filter == "tracked_entities":
            entities_file = os.path.join(self._registry_dir, "tracked_entities.yaml")
            data = self._load_yaml(entities_file)
            if data:
                items = data.get("tracked_entities", [])
                for item in items:
                    results.append(item)
            return results

        if entity_type_filter == "queue_entry" or entity_type_filter == "queue_entries":
            queue_file = os.path.join(self._queue_dir, "queue.yaml")
            data = self._load_yaml(queue_file)
            if data:
                items = data.get("queue", [])
                for item in items:
                    if source_id_filter and item.get("source_id") != source_id_filter:
                        continue
                    if status_filter and item.get("review_status") != status_filter:
                        continue
                    results.append(item)
            return results

        if entity_type_filter == "source_event" or entity_type_filter == "source_events":
            candidates = self._walk_yaml_files(self._source_events_dir)
            for fpath in candidates:
                data = self._load_yaml(fpath)
                if data is None:
                    continue
                items = data.get("items", [])
                for item in items:
                    if source_id_filter and item.get("source_id") != source_id_filter:
                        continue
                    results.append(item)
            return results

        candidates = self._walk_yaml_files(self._intel_items_dir)
        for fpath in candidates:
            data = self._load_yaml(fpath)
            if data is None:
                continue
            items = data.get("items", [])
            for item in items:
                if source_id_filter and item.get("source_id") != source_id_filter:
                    continue
                if status_filter and item.get("review_status") != status_filter:
                    continue
                results.append(item)
        return results

    def get_health(self):
        item_files = self._walk_yaml_files(self._intel_items_dir)
        event_files = self._walk_yaml_files(self._source_events_dir)
        total_items = 0
        for fpath in item_files:
            data = self._load_yaml(fpath)
            if data:
                total_items += len(data.get("items", []))
        return {
            "adapter": "file",
            "status": "ok",
            "intel_item_files": len(item_files),
            "source_event_files": len(event_files),
            "total_items": total_items,
            "registry_dir_exists": os.path.isdir(self._registry_dir),
        }
