"""Regression coverage for the SilverLeaf mobility scope registry."""
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.validate_silverleaf_mobility import validate  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def load_mobility():
    with open(os.path.join(REPO_ROOT, "registry", "silverleaf_mobility.yaml")) as handle:
        return yaml.safe_load(handle)


def test_mobility_validator_passes():
    result = validate()
    assert result["status"] == "PASS", result["errors"]


def test_direct_access_and_contextual_scope_are_distinct():
    segments = {segment["id"]: segment for segment in load_mobility()["segments"]}
    assert segments["sl_cr2209_igp_to_silverleaf_parkway"]["relationship"] == "direct_access"
    assert segments["sl_sr16_igp_to_i95"]["relationship"] == "nearby_commute_corridor"
    assert segments["sl_cr210_i95_to_us1_context"]["relationship"] == "contextual_only"
    assert segments["sl_i95_interface_context"]["relationship"] == "contextual_only"
    assert "generic i-95 incident" in " ".join(segments["sl_i95_interface_context"]["exclusions"]).lower()


def test_internal_streets_and_fce_are_not_inferred():
    unknown = {item["id"]: item for item in load_mobility()["unknown_or_unverified"]}
    assert unknown["sl_internal_streets_and_entrances"]["status"] == "not_registered"
    assert unknown["sl_fce_alignment_and_access"]["status"] == "not_registered"
