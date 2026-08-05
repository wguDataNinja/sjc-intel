"""Tests for the SilverLeaf Brief static site generator + client search logic."""
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts import site_search  # noqa: E402
from scripts.build_static_release import build_demo_release  # noqa: E402
from scripts.static_release_common import (  # noqa: E402
    GENERATOR_REVISION,
    build_search_index,
    write_artifacts,
)
from scripts.build_static_site import SiteBuilder  # noqa: E402
from scripts.site_templates import SOURCE_UNAVAILABLE  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
DEMO_FIXTURE = os.path.join(REPO_ROOT, "site", "fixtures", "demo", "release.yaml")


def _build_demo_site(tmp_path):
    """Build the demo release + site into tmp and return the site dir + builder."""
    release, rev, _ = build_demo_release(
        DEMO_FIXTURE, "SJC-REL-DEMO-TEST", None, None, "Test reviewer",
        GENERATOR_REVISION)
    data_dir = str(tmp_path / "data")
    out_dir = str(tmp_path / "site")
    os.makedirs(data_dir, exist_ok=True)
    write_artifacts(data_dir, release,
                    build_search_index(release, release["dimensions"]),
                    reviewer=rev)
    builder = SiteBuilder(data_dir, out_dir)
    builder.build()
    return out_dir, builder, release


def _read(out_dir, rel):
    with open(os.path.join(out_dir, rel), encoding="utf-8") as f:
        return f.read()


class TestRouteGeneration:
    def test_all_required_routes_generated(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        required = [
            "index.html", "browse/index.html", "about/index.html",
            "sources/index.html", "404.html",
        ]
        for pid in release["items"]:
            required.append(f"item/{pid['public_item_id']}/index.html")
        for it in release["items"]:
            for t in it.get("topic_ids") or []:
                required.append(f"topic/{t}/index.html")
            for p in it.get("place_ids") or []:
                required.append(f"place/{p}/index.html")
            for e in it.get("entity_ids") or []:
                required.append(f"entity/{e}/index.html")
        for rel in required:
            assert os.path.exists(os.path.join(out, rel)), rel

    def test_no_private_paths_in_output(self, tmp_path):
        out, builder, _ = _build_demo_site(tmp_path)
        for root, _dirs, files in os.walk(out):
            for name in files:
                if not name.endswith(".html"):
                    continue
                text = open(os.path.join(root, name), encoding="utf-8").read()
                assert "/Users/" not in text, name
                assert "scripts/" not in text, name
                assert "data/intel_items" not in text, name


class TestNoJsReadability:
    def test_latest_renders_all_item_titles(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "index.html")
        for it in release["items"]:
            assert it["title"] in html, it["public_item_id"]

    def test_browse_server_renders_all_cards(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "browse/index.html")
        for it in release["items"]:
            assert it["title"] in html
            assert it["why_it_matters"][:40] in html

    def test_card_anatomy_present(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "index.html")
        n = len(release["items"])
        for token in ("badge-relevance", "badge-reviewed", "card-why",
                      "card-source-row", "action-read", "action-source"):
            assert html.count(token) >= n, token


class TestSearchLogic:
    def _entries(self):
        release, rev, _ = build_demo_release(
            DEMO_FIXTURE, "SJC-REL-DEMO-TEST", None, None, "t", GENERATOR_REVISION)
        index = build_search_index(release, release["dimensions"])
        entries = index["items"]
        # relevance needed for scope filter
        by_id = {it["public_item_id"]: it for it in release["items"]}
        for e in entries:
            e["relevance"] = by_id[e["id"]].get("relevance", "countywide_impact")
        return release, entries

    def test_parse_query(self):
        st = site_search.parse_query(
            "?q=water&topic=environment,water_restrictions&entity=ENT-EDU-SILVERLEAF-K8&scope=in_silverleaf")
        assert st["q"] == "water"
        assert st["topic"] == {"environment", "water_restrictions"}
        assert st["entity"] == {"ENT-EDU-SILVERLEAF-K8"}
        assert st["scope"] == {"in_silverleaf"}

    def test_parse_query_repeated_params(self):
        st = site_search.parse_query("?topic=a&topic=b")
        assert st["topic"] == {"a", "b"}

    def test_or_within_dimension_and_across_dimensions(self):
        release, entries = self._entries()
        # topic OR (within topic dimension)
        st = site_search.parse_query("?topic=environment,water_restrictions")
        results = site_search.search_and_filter(release["items"], entries, st)
        ids = [it["public_item_id"] for it in results]
        assert "DEMO-SL-20260804-0001" in ids  # water + environment
        # entity filter AND with topic
        st2 = site_search.parse_query(
            "?topic=education&entity=ENT-EDU-SILVERLEAF-K8")
        r2 = site_search.search_and_filter(release["items"], entries, st2)
        assert [it["public_item_id"] for it in r2] == ["DEMO-SL-20260804-0002"]

    def test_search_starts_after_two_characters(self):
        release, entries = self._entries()
        one = site_search.parse_query("?q=w")
        assert site_search.search_and_filter(release["items"], entries, one) == \
            release["items"]  # no filtering or reordering at 1 char

    def test_search_token_match(self):
        release, entries = self._entries()
        st = site_search.parse_query("?q=publix")
        results = site_search.search_and_filter(release["items"], entries, st)
        ids = [it["public_item_id"] for it in results]
        assert "DEMO-SL-20260804-0005" in ids

    def test_release_order_breaks_search_ties(self):
        # Two items with identical scores keep release order (stable sort).
        release_items = [
            {"public_item_id": "A1", "source_date": "2026-02-01"},
            {"public_item_id": "B1", "source_date": "2026-02-01"},
            {"public_item_id": "C1", "source_date": "2026-01-01"},
        ]
        # Same token, same score for A1 and B1 (present once in each summary).
        entries = [
            {"id": "A1", "tokens": "t a one mention here", "title": "t a",
             "summary": "one mention here", "why_it_matters": "w",
             "topics": [], "places": [], "entities": [], "source": "",
             "source_date": "2026-02-01", "relevance": "in_silverleaf"},
            {"id": "B1", "tokens": "t b another mention here", "title": "t b",
             "summary": "another mention here", "why_it_matters": "w",
             "topics": [], "places": [], "entities": [], "source": "",
             "source_date": "2026-02-01", "relevance": "in_silverleaf"},
            {"id": "C1", "tokens": "t c no match", "title": "t c",
             "summary": "no match", "why_it_matters": "w",
             "topics": [], "places": [], "entities": [], "source": "",
             "source_date": "2026-01-01", "relevance": "in_silverleaf"},
        ]
        st = site_search.parse_query("?q=mention")
        results = site_search.search_and_filter(release_items, entries, st)
        ids = [it["public_item_id"] for it in results]
        assert ids == ["A1", "B1"]  # release order preserved on equal score

    def test_zero_results(self):
        release, entries = self._entries()
        st = site_search.parse_query("?q=zzzznotaword&topic=education")
        assert site_search.search_and_filter(release["items"], entries, st) == []

    def test_no_query_keeps_release_order(self):
        release, entries = self._entries()
        st = site_search.parse_query("")
        results = site_search.search_and_filter(release["items"], entries, st)
        assert [it["public_item_id"] for it in results] == \
            [it["public_item_id"] for it in release["items"]]


class TestCollectionRoutes:
    def test_topic_page_contains_only_matching_items(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "topic/education/index.html")
        assert "DEMO-SL-20260804-0002" in html  # school item
        assert "SilverLeaf K-8 School On Track" in html

    def test_place_page_counts(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "place/silverleaf/index.html")
        n = sum(1 for it in release["items"] if "silverleaf" in (it.get("place_ids") or []))
        assert html.count('class="card"') == n

    def test_entity_page(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "entity/ENT-EDU-SILVERLEAF-K8/index.html")
        assert "DEMO-SL-20260804-0002" in html


class TestFailureStates:
    def test_unavailable_source_message_rendered(self):
        from scripts.site_templates import source_link
        html = source_link({"source_name": "X"}, 0)
        assert "currently unavailable" in html
        assert SOURCE_UNAVAILABLE in html

    def test_empty_release_renders_empty_states(self, tmp_path):
        import json
        release, rev, _ = build_demo_release(
            DEMO_FIXTURE, "SJC-REL-DEMO-TEST", None, None, "t", GENERATOR_REVISION)
        release["items"] = []  # simulate empty release
        data_dir = str(tmp_path / "data")
        out_dir = str(tmp_path / "site")
        os.makedirs(data_dir, exist_ok=True)
        write_artifacts(data_dir, release,
                        build_search_index(release, release["dimensions"]),
                        reviewer=rev)
        SiteBuilder(data_dir, out_dir).build()
        html = _read(out_dir, "index.html")
        assert "No reviewed intelligence published yet" in html

    def test_404_page(self, tmp_path):
        out, builder, _ = _build_demo_site(tmp_path)
        html = _read(out, "404.html")
        assert "Page not found" in html


class _AccessibilityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.skip_links = 0
        self.mains = 0
        self.navs = 0
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and "skip-link" in (d.get("class") or ""):
            self.skip_links += 1
        if tag == "main":
            self.mains += 1
        if tag == "nav":
            self.navs += 1
        if tag == "a":
            self.links.append(d)


class TestAccessibilityStructure:
    def test_pages_have_single_h1_skip_link_and_landmarks(self, tmp_path):
        out, builder, _ = _build_demo_site(tmp_path)
        for rel in ("index.html", "browse/index.html", "about/index.html",
                    "sources/index.html", "404.html",
                    "item/DEMO-SL-20260804-0001/index.html",
                    "topic/education/index.html"):
            parser = _AccessibilityParser()
            parser.feed(_read(out, rel))
            assert parser.h1_count == 1, f"{rel}: {parser.h1_count} h1"
            assert parser.skip_links == 1, rel
            assert parser.mains >= 1, rel
            assert parser.navs >= 2, rel  # primary + bottom

    def test_external_links_are_labeled(self, tmp_path):
        out, builder, _ = _build_demo_site(tmp_path)
        html = _read(out, "item/DEMO-SL-20260804-0001/index.html")
        assert "opens in a new tab" in html
        assert 'target="_blank"' in html
        assert 'rel="noopener noreferrer"' in html

    def test_search_input_labeled(self, tmp_path):
        out, builder, _ = _build_demo_site(tmp_path)
        html = _read(out, "browse/index.html")
        assert 'for="search-input"' in html
        assert 'id="search-input"' in html


class TestBrowseEmbed:
    def test_embedded_release_data_present(self, tmp_path):
        out, builder, release = _build_demo_site(tmp_path)
        html = _read(out, "browse/index.html")
        assert 'id="release-data"' in html
        assert "browse.js" in html
        # embedded JSON must be script-safe (no raw </script>)
        m = re.search(r'<script type="application/json" id="release-data">(.*?)</script>',
                      html, re.S)
        assert m
        payload = m.group(1)
        assert "</script>" not in payload
