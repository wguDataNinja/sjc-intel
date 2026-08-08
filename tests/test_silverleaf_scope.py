"""Tests for the SilverLeaf scope registry (ROADMAP.md §3B-G1)."""
import os
import sys
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.validate_silverleaf_scope import validate, PROVENANCE  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return yaml.safe_load(f)


class TestScopeRegistry:
    def test_registry_exists_and_parses(self):
        scope = _load("registry/silverleaf_scope.yaml")
        assert scope["schema_version"] == "1.0"
        assert scope["status"] == "active"
        assert scope["community"]["id"] == "silverleaf"
        assert scope["community"]["canonical_name"] == "SilverLeaf"

    def test_validator_passes(self):
        result = validate()
        assert result["status"] == "PASS", result["errors"]
        assert result["errors"] == []

    def test_authoritative_geography_is_evidence_only_and_resolves(self):
        scope = _load("registry/silverleaf_scope.yaml")
        geo = scope["geographic_authority"]
        assert geo["status"] == "evidence_only"
        sources = {source["id"]: source for source in geo["sources"]}
        assert {"SJC-DRIMOD-2024-01", "SJC-MAJMOD-2024-04",
                "SJC-COMP-PLAN-2050-LAND-USE"} <= set(sources)
        assert all(source["source_url"].startswith("https://www.sjcfl.us/")
                   for source in sources.values())
        assert all(record["source_id"] in sources
                   for record in geo["canonical_geography"])
        assert all(record["geometry_status"] == "no_geometry_loaded"
                   for record in geo["canonical_geography"])

    def test_school_service_is_year_bound_partial_and_source_backed(self):
        scope = _load("registry/silverleaf_scope.yaml")
        sources = {source["id"]: source for source in scope["school_authority"]["sources"]}
        assert {"SJCSD-ZONING-2026-27", "SJCSD-QQ-PLAN-C-2026-27",
                "SJCSD-MAGNOLIA-OPENING-2026"} <= set(sources)
        magnolia = next(school for school in scope["schools"]
                       if school["id"] == "ENT-EDU-SILVERLEAF-K8")
        service = magnolia["attendance_service"]
        assert service["school_year"] == "2026-2027"
        assert service["scope"] == "partial_silverleaf"
        assert set(service["source_ids"]) <= set(sources)
        assert "individual address" in service["limitations"].lower()
        tocoi = next(school for school in scope["schools"]
                     if school["id"] == "tocoi_creek_high")
        assert tocoi["verification"] == "needs-review"
        assert "unverified" in tocoi["status"]

    def test_provenance_vocabulary(self):
        scope = _load("registry/silverleaf_scope.yaml")
        fields = []
        for nb in scope.get("neighborhoods", []):
            fields.append(nb.get("verification"))
        for road in scope.get("roads", {}).get("direct_serving", []):
            fields.append(road.get("verification"))
        for s in scope.get("schools", []):
            fields.append(s.get("verification"))
        for u in scope.get("utilities", []):
            fields.append(u.get("verification"))
        for d in scope.get("developments", []):
            fields.append(d.get("verification"))
        for b in scope.get("businesses_services", []):
            fields.append(b.get("verification"))
        assert set(fields) <= PROVENANCE

    def test_neighborhoods_match_communities_registry(self):
        scope = _load("registry/silverleaf_scope.yaml")
        comm = _load("registry/communities.yaml")
        comm_ids = {c["id"] for c in comm["communities"]}
        nb_ids = {nb["id"] for nb in scope["neighborhoods"]}
        assert nb_ids <= comm_ids
        # Every registered SilverLeaf neighborhood is present in the scope.
        sl_neighborhoods = {c["id"] for c in comm["communities"]
                            if c.get("parent_area") == "silverleaf"}
        assert sl_neighborhoods <= nb_ids

    def test_developments_reference_tracked_entities(self):
        scope = _load("registry/silverleaf_scope.yaml")
        ents = _load("registry/tracked_entities.yaml")
        ent_ids = {e["entity_id"] for e in ents["tracked_entities"]}
        for d in scope["developments"]:
            if d["id"].startswith("ENT-"):
                assert d["id"] in ent_ids, d["id"]

    def test_relevance_ids_are_stable(self):
        scope = _load("registry/silverleaf_scope.yaml")
        ids = []
        for section in ("direct", "nearby", "countywide_material"):
            for r in scope["relevance"].get(section, []):
                ids.append(r["id"])
        assert set(ids) == {"in_silverleaf", "near_silverleaf", "countywide_impact"}

    def test_inclusion_and_exclusion_rules_present(self):
        scope = _load("registry/silverleaf_scope.yaml")
        assert len(scope["inclusion_rules"]) >= 5
        assert len(scope["exclusion_rules"]) >= 5
        for rule in scope["inclusion_rules"] + scope["exclusion_rules"]:
            assert rule.get("id") and rule.get("rule")

    def test_no_gis_or_boundary_claims(self):
        scope = _load("registry/silverleaf_scope.yaml")
        # The registry may describe why a future polygon/coordinate is not
        # available, but an evidence-only registry must not carry geometry.
        forbidden_geometry_keys = {
            "polygon", "latitude", "longitude", "coordinates", "coordinate",
            "geometry", "geojson", "wkt",
        }

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    assert (key.lower() not in forbidden_geometry_keys
                            or key == "geometry_status"), key
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(scope)
        geo = scope["geographic_authority"]
        assert geo["status"] == "evidence_only"
        assert all(record["geometry_status"] == "no_geometry_loaded"
                   for record in geo["canonical_geography"])
        assert "no official boundary" in str(scope.get("roads", {}).get("boundary_notes", "")).lower()
