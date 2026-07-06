import os
import yaml


def test_intel_item_schema_parses(schema_dir, load_yaml):
    path = os.path.join(schema_dir, "intel_item.schema.yaml")
    data = load_yaml(path)
    assert data is not None
    assert isinstance(data, dict)


def test_source_event_schema_parses(schema_dir, load_yaml):
    path = os.path.join(schema_dir, "source_event.schema.yaml")
    data = load_yaml(path)
    assert data is not None


def test_source_schema_parses(schema_dir, load_yaml):
    path = os.path.join(schema_dir, "source.schema.yaml")
    data = load_yaml(path)
    assert data is not None


def test_tracked_entity_schema_parses(schema_dir, load_yaml):
    path = os.path.join(schema_dir, "tracked_entity.schema.yaml")
    data = load_yaml(path)
    assert data is not None


def test_all_schemas_valid_yaml(schema_dir):
    for fname in sorted(os.listdir(schema_dir)):
        if not fname.endswith(".yaml"):
            continue
        path = os.path.join(schema_dir, fname)
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{fname} should parse as valid YAML"
