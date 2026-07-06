import os
import yaml
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


@pytest.fixture
def fixture_dir():
    return FIXTURE_DIR


@pytest.fixture
def schema_dir():
    return SCHEMA_DIR


@pytest.fixture
def script_dir():
    return SCRIPT_DIR


@pytest.fixture
def nbor_html():
    path = os.path.join(FIXTURE_DIR, "nbor_raw.html")
    with open(path) as f:
        return f.read()


@pytest.fixture
def bcc_agenda_text_jan20():
    path = os.path.join(FIXTURE_DIR, "1202026_agenda.txt")
    with open(path) as f:
        return f.read()


@pytest.fixture
def bcc_agenda_text_may19():
    path = os.path.join(FIXTURE_DIR, "051926_agenda.txt")
    with open(path) as f:
        return f.read()


@pytest.fixture
def clerk_html():
    path = os.path.join(FIXTURE_DIR, "clerk_agendas.html")
    with open(path) as f:
        return f.read()


@pytest.fixture
def load_yaml():
    def _load(path):
        with open(path) as f:
            return yaml.safe_load(f)
    return _load
