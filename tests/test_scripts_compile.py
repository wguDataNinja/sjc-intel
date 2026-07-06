import os
import sys


SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
SCRIPTS_TO_CHECK = [
    "rebuild_dedupe_index.py",
    "build_review_queue.py",
    "extract_nbor.py",
    "extract_bcc_agenda.py",
    "update_dedupe_index.py",
    "update_review_status.py",
    "batch_review_queue.py",
    "batch_review.py",
]


def test_all_scripts_compile():
    for fname in SCRIPTS_TO_CHECK:
        fpath = os.path.join(SCRIPT_DIR, fname)
        assert os.path.exists(fpath), f"{fname} should exist"
        with open(fpath) as f:
            try:
                compile(f.read(), fpath, "exec")
            except SyntaxError as e:
                assert False, f"{fname} compilation failed: {e}"
