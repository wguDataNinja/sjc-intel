#!/usr/bin/env python3
"""
SilverLeaf Brief — Static Site Generator (§3C-G2 v0).

Reads a release artifact directory (site/data/demo or
site/data/releases/{release-id}) and generates the portable static site under
site/:

  /                Latest
  /browse          Search + filters
  /about           Methodology & limitations
  /sources         Data & sources
  /item/{id}/      Item detail
  /topic/{id}/     Collection (topic)
  /place/{id}/     Collection (place)
  /entity/{id}/    Collection (entity)
  /404.html

Behavior:
- semantic HTML, one H1 per page, skip link, landmarks;
- relative URLs (relocatable under any static path);
- server-rendered cards (readable with JavaScript disabled);
- Browse enhances with site/assets/js/browse.js (progressive enhancement);
- demo releases render a visible "Demo preview" banner;
- verifies release-manifest checksums before building (rollback safety).

Usage:
  python3 scripts/build_static_site.py [--source site/data/demo]
      [--out-dir site] [--list-routes]
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import site_search  # noqa: E402
import site_templates as tpl  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RELEASES_DIR = os.path.join(REPO_ROOT, "site", "data", "releases")
DEFAULT_DEMO = os.path.join(REPO_ROOT, "site", "data", "demo")


def default_release_dir():
    """Prefer the most recent real release; fall back to the demo fixture.

    Makes `python3 scripts/build_static_site.py` produce the standalone MVP
    (the latest real release) by default while keeping the demo build
    available via --source site/data/demo.
    """
    import glob
    candidates = sorted(glob.glob(os.path.join(DEFAULT_RELEASES_DIR, "*", "release.json")))
    if candidates:
        # Highest release_id (e.g. SJC-REL-2026-08-001) is the newest.
        return os.path.dirname(candidates[-1])
    return DEFAULT_DEMO


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class BuildError(Exception):
    pass


# Generated files/dirs the generator owns (cleaned before each build so a
# release change never leaves stale routes behind). assets/, fixtures/,
# data/, and README.md are source/managed and never removed.
GENERATED_TOP_FILES = ("index.html", "404.html", "build.json")
GENERATED_DIRS = ("browse", "about", "sources", "item", "topic", "place", "entity")


class SiteBuilder:
    def __init__(self, source_dir, out_dir):
        self.source_dir = os.path.abspath(source_dir)
        self.out_dir = os.path.abspath(out_dir)
        self.release = load_json(os.path.join(self.source_dir, "release.json"))
        self.search = load_json(os.path.join(self.source_dir, "search-index.json"))
        self.manifest = load_json(os.path.join(self.source_dir, "release-manifest.json"))
        self._verify_checksums()
        self.items = self.release.get("items", [])
        self.dimensions = self.release.get("dimensions", {})
        self.ctx = {
            "environment": self.release.get("environment", "real"),
            "release": self.release,
        }
        self.routes = []

    def clean_generated(self):
        """Remove previously generated pages so stale routes never mix in."""
        for name in GENERATED_TOP_FILES:
            path = os.path.join(self.out_dir, name)
            if os.path.exists(path):
                os.remove(path)
        for name in GENERATED_DIRS:
            path = os.path.join(self.out_dir, name)
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)

    def _verify_checksums(self):
        expected = self.manifest.get("checksums") or {}
        for name, want in sorted(expected.items()):
            path = os.path.join(self.source_dir, name)
            if not os.path.exists(path):
                raise BuildError(f"checksum target missing: {name}")
            if sha256_file(path) != want:
                raise BuildError(
                    f"checksum mismatch for {name} — refusing to build (rollback "
                    "safety; see docs/static_release_data_contract.md §9)")

    # ------------------------------------------------------------------ #
    # Page writers
    # ------------------------------------------------------------------ #

    def _write(self, rel_path, content):
        path = os.path.join(self.out_dir, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.routes.append(rel_path)

    # ------------------------------------------------------------------ #
    # Latest
    # ------------------------------------------------------------------ #

    def build_latest(self):
        depth = 0
        all_count = len(self.items)
        latest_items = [it for it in self.items if it.get("role") in (None, "latest")]
        if any(it.get("role") for it in self.items):
            latest_items = [it for it in self.items if it.get("role") == "latest"]
        count = len(latest_items)
        published = tpl.format_date(self.release.get("published_at"))
        browse = "Browse" if all_count != count else None
        cover = (
            f"This release includes {count} current updates on Latest — schools, "
            "roads, healthcare, retail, utilities, and preparedness — plus a "
            "Browse corpus of durable neighborhood context and timelines."
            if browse else
            "Reviewed updates with direct links to public sources — schools, "
            "roads, healthcare, retail, utilities, and preparedness.")

        topic_ids = self._ordered_dimension_ids("topics")
        shortcuts = ""
        if topic_ids:
            chips = " ".join(
                f'<a class="topic-shortcut badge-topic" '
                f'href="topic/{html_id(tid)}/index.html">'
                f'{html(topic_label(self.dimensions, tid))}</a>'
                for tid in topic_ids)
            shortcuts = f'<nav class="topic-shortcuts" aria-label="Browse by topic">{chips}</nav>'

        if latest_items:
            cards = "\n".join(tpl.item_card(it, self.dimensions, depth) for it in latest_items)
        else:
            cards = tpl.empty_state(
                "No reviewed intelligence published yet",
                "Nothing has been approved for publication in this release. "
                "Check back after the next review.",
                depth, [("Browse by topic", "browse/index.html")])

        browse_note = ""
        if browse:
            browse_note = (
                f'<p>See <a href="browse/index.html">Browse</a> for all '
                f'{all_count} reviewed updates, including historical context '
                f'and timelines.</p>')

        body = (
            '<div class="page">'
            f'  <header class="hero">'
            f'    <h1>{tpl.html_escape(tpl.TAGLINE)}</h1>'
            f'    <p class="release-date">Updated {tpl.html_escape(published or "—")}</p>'
            f'    <p class="item-count">{count} reviewed {"updates" if count != 1 else "update"}</p>'
            f'    <p class="trust">{tpl.html_escape(tpl.TRUST_STATEMENT)}</p>'
            f'  </header>'
            f'  {shortcuts}'
            f'  <section class="release-list" aria-label="Updates in this release">'
            f'    {cards}'
            f'  </section>'
            f'  <section class="coverage" id="coverage" aria-labelledby="coverage-heading">'
            f'    <h2 id="coverage-heading">About this release</h2>'
            f'    <p>{tpl.html_escape(cover)}</p>'
            f'    {browse_note}'
            f'    <p>Links go to the original public records. See '
            f'<a href="about/index.html">About</a> for methodology and '
            f'<a href="sources/index.html">Data &amp; Sources</a> for the source '
            f'directory.</p>'
            f'  </section>'
            '</div>')
        self._write("index.html", tpl.page_shell(
            "Latest", "Reviewed neighborhood intelligence for SilverLeaf and the "
            "surrounding corridor.", depth, "latest", body, self.ctx))

    # ------------------------------------------------------------------ #
    # Browse
    # ------------------------------------------------------------------ #

    def build_browse(self):
        depth = 1
        count = len(self.items)

        # Server-rendered full card list (no-JS baseline).
        if self.items:
            cards = "\n".join(tpl.item_card(it, self.dimensions, depth) for it in self.items)
        else:
            cards = tpl.empty_state(
                "No reviewed intelligence published yet",
                "This release contains no published items.",
                depth, [("Browse by topic", "browse/index.html")])

        # Filter option groups (zero-count options hidden).
        groups_html = self._render_filter_groups(depth)

        embedded = {
            "entries": self._search_entries_for_js(),
            "dimensions": self.dimensions,
        }

        no_results_html = (
            '<div id="no-results" hidden>' +
            tpl.empty_state("No items match", "Try removing a filter or browsing "
                            "by topic.", depth, [("Browse by topic",
                                                  "browse/index.html")]) +
            "</div>")

        body = (
            '<div class="page browse-page">'
            f'  <header class="browse-header">'
            f'    <h1>Browse updates</h1>'
            f'    <p>Search and filter the {count} reviewed {"updates" if count != 1 else "update"} '
            f'in this release.</p>'
            f'  </header>'
            f'  <form class="browse-search" role="search" action="index.html" method="get">'
            f'    <label class="visually-hidden" for="search-input">Search updates</label>'
            f'    <input id="search-input" name="q" type="search" '
            f'placeholder="Search titles, topics, places, sources" autocomplete="off" '
            f'aria-describedby="search-hint">'
            f'    <button type="submit" class="search-submit">Search</button>'
            f'    <p id="search-hint" class="visually-hidden">Search begins after '
            f'two characters. Results appear as you type.</p>'
            f'  </form>'
            f'  <div class="browse-layout">'
            f'    <aside class="filters-panel" id="filters-panel" aria-label="Filters">'
            f'      {groups_html}'
            f'      <button type="button" class="filters-clear" data-action="clear">Clear all</button>'
            f'    </aside>'
            f'    <section class="results" aria-label="Results">'
            f'      <div class="results-toolbar">'
            f'        <p class="result-count" aria-live="polite">{count} '
            f'{"updates" if count != 1 else "update"}</p>'
            f'        <div class="active-chips" aria-live="polite"></div>'
            f'      </div>'
            f'      <button type="button" class="filters-open" data-action="open-filters">'
            f'        Filters <span class="filters-open-count" aria-hidden="true"></span>'
            f'      </button>'
            f'      <div class="results-list" id="results-list">{cards}</div>'
            f'      {no_results_html}'
            f'    </section>'
            f'  </div>'
            '</div>')

        # Filter bottom sheet (mobile; :target fallback without JS).
        sheet = (
            '<div class="sheet-backdrop" id="sheet"></div>'
            '<aside class="filter-sheet" id="filter-sheet" role="dialog" '
            'aria-modal="false" aria-label="Filters">'
            '<div class="sheet-header">'
            '<h2>Filters</h2>'
            '<a class="sheet-close" href="#browse-page" data-action="close-filters">Close</a>'
            '</div>'
            f'<div class="sheet-body">{groups_html}</div>'
            '<div class="sheet-footer">'
            '<button type="button" class="filters-clear" data-action="clear">Clear all</button>'
            '<button type="button" class="sheet-apply" data-action="close-filters">Show results</button>'
            '</div>'
            '</aside>')

        embedded_script = (
            f'<script type="application/json" id="release-data">{tpl.embed_json(embedded)}</script>'
            f'<script src="{tpl.rel(depth, "assets/js/browse.js")}" defer></script>'
        )
        self._write("browse/index.html", tpl.page_shell(
            "Browse", "Search and filter reviewed SilverLeaf updates.", depth,
            "browse", body + sheet, self.ctx, extra_head=embedded_script,
            body_class="has-bottom-nav"))

    def _search_entries_for_js(self):
        by_id = {e["id"]: e for e in self.search.get("items", [])}
        entries = []
        for it in self.items:
            e = dict(by_id.get(it["public_item_id"], {}))
            e["id"] = it["public_item_id"]
            e["relevance"] = it.get("relevance", "countywide_impact")
            entries.append(e)
        return entries

    def _render_filter_groups(self, depth):
        groups = []
        counts = {dim: self._dimension_counts(dim) for dim in
                  ("topics", "scope", "roles", "places", "entities")}
        config = [
            ("topics", "Topic", "topic", "topic", True),
            ("scope", "Relevance", "scope", "scope", True),
            ("roles", "Edition", "role", "role", True),
            ("places", "Place", "place", "place", False),
            ("entities", "Entity", "entity", "entity", False),
        ]
        for dim, label, param, prefix, visible in config:
            rows = []
            for key, count in counts[dim]:
                display = self._dimension_label(dim, key)
                rows.append(
                    f'<label class="filter-option"><input type="checkbox" '
                    f'name="{param}" value="{html(key)}" data-dim="{param}" '
                    f'data-key="{html(key)}"> '
                    f'<span class="filter-label">{html(display)}</span> '
                    f'<span class="filter-count">{count}</span></label>')
            if not rows:
                continue
            fieldset = (
                f'<fieldset class="filter-group" data-group="{param}">'
                f'<legend>{html(label)}</legend>{"" .join(rows)}</fieldset>')
            if visible:
                groups.append(fieldset)
            else:
                groups.append(
                    f'<details class="filter-group filter-group-collapsible" '
                    f'data-group="{param}">'
                    f'<summary>{html(label)}</summary>{fieldset}</details>')
        return "".join(groups)

    def _dimension_counts(self, dim):
        from collections import Counter
        counter = Counter()
        if dim == "topics":
            for it in self.items:
                counter[it.get("display_topic", "utilities_water")] += 1
        elif dim == "roles":
            for it in self.items:
                counter[it.get("role") or "latest"] += 1
        elif dim == "scope":
            for it in self.items:
                counter[it.get("relevance", "countywide_impact")] += 1
        elif dim == "places":
            for it in self.items:
                for p in it.get("place_ids") or []:
                    counter[p] += 1
        elif dim == "entities":
            for it in self.items:
                for e in it.get("entity_ids") or []:
                    counter[e] += 1
        return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))

    def _dimension_label(self, dim, key):
        if dim == "topics":
            return topic_label(self.dimensions, key)
        if dim == "roles":
            return tpl.ROLE_LABELS.get(key, key.title())
        if dim == "scope":
            return tpl.relevance_label(self.dimensions, key)
        if dim == "places":
            return ((self.dimensions.get("places") or {}).get(key) or {}).get("label", key)
        if dim == "entities":
            return ((self.dimensions.get("entities") or {}).get(key) or {}).get("label", key)
        return key

    def _ordered_dimension_ids(self, dim_key):
        if dim_key == "topics":
            seen = []
            for it in self.items:
                dt = it.get("display_topic")
                if dt and dt not in seen:
                    seen.append(dt)
            return seen
        dim = {"places": "place_ids", "entities": "entity_ids"}[dim_key]
        seen = []
        for it in self.items:
            for key in it.get(dim) or []:
                if key not in seen:
                    seen.append(key)
        return seen

    # ------------------------------------------------------------------ #
    # Collection routes (one template for topic/place/entity)
    # ------------------------------------------------------------------ #

    def build_collections(self):
        # The "topics" dimension is keyed on the v0 display_topic.
        kinds = [
            ("topic", "display_topic", "topics", "/topic/"),
            ("place", "place_ids", "places", "/place/"),
            ("entity", "entity_ids", "entities", "/entity/"),
        ]
        for kind, id_field, dim, prefix in kinds:
            for key in self._ordered_dimension_ids(dim):
                items = [it for it in self.items if key in (it.get(id_field) or [])]
                label = self._dimension_label(dim, key)
                description = (self.dimensions.get(dim, {}).get(key, {}) or {}).get("description")
                related = self._related_collection_links(kind, key)
                page = tpl.collection_page(
                    kind, key, label, description, items, self.dimensions,
                    2, self.ctx, related)
                self._write(f"{prefix.lstrip('/')}{html_id(key)}/index.html", page)

    def _related_collection_links(self, kind, exclude_key):
        links = []
        if kind == "topic":
            for key in self._ordered_dimension_ids("topics"):
                if key != exclude_key:
                    links.append((topic_label(self.dimensions, key),
                                  f"../topic/{html_id(key)}/index.html"))
        elif kind == "place":
            for key in self._ordered_dimension_ids("places"):
                if key != exclude_key:
                    links.append((self._dimension_label("places", key),
                                  f"../place/{html_id(key)}/index.html"))
        else:
            for key in self._ordered_dimension_ids("entities"):
                if key != exclude_key:
                    links.append((self._dimension_label("entities", key),
                                  f"../entity/{html_id(key)}/index.html"))
        return links[:6]

    # ------------------------------------------------------------------ #
    # Item detail
    # ------------------------------------------------------------------ #

    def build_item_pages(self):
        for it in self.items:
            self._build_item_page(it)

    def _build_item_page(self, it):
        depth = 2
        pid = it["public_item_id"]
        rel_id = html_id(pid)

        display_topic = it.get("display_topic") or "utilities_water"
        topic_labels = (
            f'<li><a href="../topic/{html_id(display_topic)}/index.html">'
            f'{html(topic_label(self.dimensions, display_topic))}</a></li>'
            if display_topic else "")
        places = it.get("place_ids") or []
        place_labels = "".join(
            f'<li><a href="../place/{html_id(p)}/index.html">{html(self._dimension_label("places", p))}</a></li>'
            for p in places)
        entities = it.get("entity_ids") or []
        entity_labels = "".join(
            f'<li><a href="../entity/{html_id(e)}/index.html">{html(self._dimension_label("entities", e))}</a></li>'
            for e in entities)

        src_date = tpl.format_date(it.get("source_date"))
        pub_date = tpl.format_date(it.get("published_date"))

        # Source panel (working or unavailable).
        url = it.get("source_url")
        if url:
            source_action = (
                f'<p><a class="action-source" href="{html(url)}" target="_blank" '
                f'rel="noopener noreferrer">Open original source'
                f' <span class="visually-hidden">: {html(it.get("source_name") or "the source")}'
                f' (opens in a new tab)</span>'
                f'<span class="external-icon" aria-hidden="true">&#8599;</span></a></p>')
            source_note = "The source link opens the original public record."
        else:
            source_action = (f'<p><span class="action-source is-unavailable">'
                             f'{html(tpl.SOURCE_UNAVAILABLE)}</span></p>')
            source_note = "The item remains published even though the original link is currently unavailable."

        # Event/effective date (only when explicitly present).
        event_html = ""
        if it.get("event_date"):
            ev_label = it.get("event_date_label") or "Event date"
            event_html = (
                f'<div class="detail-row event-row">'
                f'<dt>{html(ev_label)}</dt>'
                f'<dd>{html(tpl.format_date(it["event_date"]))}</dd>'
                f'</div>')

        # Related items.
        related_ids = it.get("related_item_ids") or []
        related_html = ""
        if related_ids:
            rel_items = [r for r in self.items if r["public_item_id"] in related_ids]
            if rel_items:
                lis = "".join(tpl.item_card_compact(r, self.dimensions, depth) for r in rel_items)
                related_html = (
                    f'<section class="related" aria-labelledby="related-heading">'
                    f'<h2 id="related-heading">Related updates</h2>'
                    f'<ul class="related-list">{lis}</ul></section>')
            else:
                related_html = ""

        meta_btns = " ".join([
            tpl.relevance_badge(self.dimensions, it.get("relevance", "countywide_impact")),
            (tpl.topic_badge(self.dimensions, display_topic) if display_topic else ""),
            tpl.role_badge(it),
            tpl.qualified_badge(it),
            tpl.reviewed_badge(depth),
            tpl.lifecycle_badge(it),
        ])

        body = (
            '<div class="page">'
            f'<article class="detail" data-item-id="{html(pid)}">'
            f'  <p class="breadcrumb"><a href="../browse/index.html" data-back-link>'
            f'Back to Browse</a> / <span>{html(it.get("source_name") or "Item")}</span></p>'
            f'  <header class="detail-header">'
            f'    <div class="detail-meta">{meta_btns}</div>'
            f'    <h1>{html(it.get("title") or "")}</h1>'
            f'    <dl class="detail-facts">'
            f'      <div class="detail-row"><dt>Source published</dt>'
            f'      <dd>{html(src_date) if src_date else "Not available"}</dd></div>'
            f'      {event_html}'
            f'    </dl>'
            f'  </header>'
            f'  <section class="detail-summary" aria-labelledby="summary-heading">'
            f'    <h2 id="summary-heading" class="visually-hidden">Summary</h2>'
            f'    <p>{html(it.get("summary") or "")}</p>'
            f'  </section>'
            f'  <section class="detail-why" aria-labelledby="why-heading">'
            f'    <h2 id="why-heading">Why it matters</h2>'
            f'    <p>{html(it.get("why_it_matters") or "")}</p>'
            f'  </section>'
            f'  <section class="detail-source-panel" aria-labelledby="source-heading">'
            f'    <h2 id="source-heading">Original source</h2>'
            f'    <dl class="detail-facts">'
            f'      <div class="detail-row"><dt>Source</dt><dd>{html(it.get("source_name") or "—")}</dd></div>'
            f'    </dl>'
            f'    {source_action}'
            f'    <p class="source-note">{html(source_note)}</p>'
            f'  </section>'
            f'  <section class="detail-dimensions" aria-labelledby="dim-heading">'
            f'    <h2 id="dim-heading" class="visually-hidden">Places, topics, entities</h2>'
            f'    <div class="detail-dim-grid">'
            f'      {("<div><h3>Places</h3><ul>" + place_labels + "</ul></div>") if place_labels else ""}'
            f'      {("<div><h3>Topics</h3><ul>" + topic_labels + "</ul></div>") if topic_labels else ""}'
            f'      {("<div><h3>Entities</h3><ul>" + entity_labels + "</ul></div>") if entity_labels else ""}'
            f'    </div>'
            f'  </section>'
            f'  <section class="detail-publication" aria-labelledby="pub-heading">'
            f'    <h2 id="pub-heading" class="visually-hidden">Publication</h2>'
            f'    <p class="detail-row"><strong>Published in SilverLeaf Brief:</strong> '
            f'{html(pub_date) if pub_date else "Not available"}</p>'
            f'    <p>Reviewed means: {html(tpl.REVIEWED_DETAIL)} See '
            f'<a href="../about/index.html">About</a> for methodology and '
            f'<a href="../sources/index.html">Data &amp; Sources</a> for provenance.</p>'
            f'  </section>'
            f'  {related_html}'
            '</article>'
            '</div>')

        # Minimal enhancement: restore Browse filter state on the back link.
        back_script = (
            '<script>'
            '(function(){try{var s=sessionStorage.getItem("browseState");'
            'var a=document.querySelector("[data-back-link]");'
            'if(s&&a){a.setAttribute("href","../browse/index.html"+s);}}catch(e){}})();'
            '</script>')
        self._write(f"item/{rel_id}/index.html", tpl.page_shell(
            it.get("title") or "Update", it.get("summary") or "", depth,
            "browse", body, self.ctx, extra_head=back_script))

    # ------------------------------------------------------------------ #
    # About
    # ------------------------------------------------------------------ #

    def build_about(self):
        depth = 1
        body = (
            '<div class="page prose">'
            '<h1>About SilverLeaf Brief</h1>'
            '<section aria-labelledby="about-product">'
            '<h2 id="about-product">What this is</h2>'
            '<p>SilverLeaf Brief is a reviewed neighborhood briefing for '
            'SilverLeaf and the surrounding corridor. It turns local public '
            'records and reporting into clear, source-linked updates — so '
            'residents can quickly see what changed and why it may matter to '
            'their household.</p>'
            '</section>'
            '<section aria-labelledby="about-selection">'
            '<h2 id="about-selection">How items are selected</h2>'
            '<p>Items come from public sources only: county government and '
            'utility records, school district updates, public notices, and '
            'local reporting. Candidates are discovered and organized from '
            'those public records, then each item is reviewed against its '
            'source before any publication decision. Nothing is published '
            'automatically.</p>'
            '</section>'
            '<section aria-labelledby="about-reviewed">'
            '<h2 id="about-reviewed">What \u201cReviewed\u201d means</h2>'
            '<p>Each summary is reviewed against the linked source for clarity, '
            'relevance, and attribution before publication. It does not mean '
            'independently verified, guaranteed accurate, or an official '
            'county statement. When a source link is unavailable, the item '
            'remains published and that state is shown.</p>'
            '</section>'
            '<section aria-labelledby="coverage">'
            '<h2 id="coverage">Coverage &amp; limitations</h2>'
            '<p>SilverLeaf Brief covers reviewed updates for SilverLeaf and '
            'the surrounding corridor. It is periodic, not real-time; it is '
            'not complete county coverage; and it is not an official county '
            'or emergency-alert service. Crime and public-safety items are '
            'excluded by default. Dates shown are absolute: when the source '
            'published the update, and when it was published in SilverLeaf '
            'Brief.</p>'
            '</section>'
            '<section aria-labelledby="release-approach">'
            '<h2 id="release-approach">Release approach</h2>'
            '<p>Releases are published when reviewed material is ready. There '
            'is no fixed weekly schedule promise. A release may contain as few '
            'as a handful of updates; empty is fine.</p>'
            '</section>'
            '<section aria-labelledby="report-an-issue">'
            '<h2 id="report-an-issue">Corrections &amp; reporting an issue</h2>'
            '<p>If a summary is wrong, a source link is broken, or something '
            'looks out of place, report it. Corrections flow through a new '
            'reviewed decision — published items are never silently edited. '
            'Open an issue on the project repository at '
            '<a href="https://github.com/wguDataNinja/sjc-intel/issues" '
            'target="_blank" rel="noopener noreferrer">github.com/wguDataNinja/'
            'sjc-intel</a>, or use the \u201cReport an issue\u201d link in the '
            'footer to describe the problem and which item it affects.</p>'
            '</section>'
            '<section aria-labelledby="about-sources">'
            '<h2 id="about-sources">Where the data comes from</h2>'
            '<p>See <a href="sources/index.html">Data &amp; Sources</a> for '
            'the source directory of this release, the public fields, and the '
            'internal data that is never exposed.</p>'
            '</section>'
            '</div>')
        self._write("about/index.html", tpl.page_shell(
            "About", "Product, methodology, review meaning, and limitations.",
            depth, "about", body, self.ctx))

    # ------------------------------------------------------------------ #
    # Data & Sources
    # ------------------------------------------------------------------ #

    def build_sources(self):
        depth = 1
        release = self.release
        pub_date = tpl.format_date(release.get("published_at"))
        count = len(self.items)

        src_dim = self.dimensions.get("sources") or {}
        source_rows = []
        for sid in sorted(src_dim.keys()):
            rec = src_dim[sid]
            n = sum(1 for it in self.items if it.get("source_id") == sid)
            # release items don't carry source_id; count by source_name match.
            n = sum(1 for it in self.items
                    if (it.get("source_name") or "").strip().lower()
                    == (rec.get("name") or "").strip().lower())
            url = rec.get("url")
            url_html = (f'<a href="{html(url)}" target="_blank" rel="noopener noreferrer">'
                        f'{html(rec.get("name") or sid)} <span class="external-icon" '
                        f'aria-hidden="true">&#8599;</span></a>') if url else html(rec.get("name") or sid)
            source_rows.append(
                f'<tr><td>{url_html}</td>'
                f'<td>{html(rec.get("source_kind") or rec.get("source_type") or "—")}</td>'
                f'<td>{n}</td></tr>')
        if source_rows:
            tbody_html = "".join(source_rows)
        else:
            tbody_html = "<tr><td colspan='3'>No sources in this release yet.</td></tr>"

        public_fields = ["public_item_id", "title", "summary", "why_it_matters",
                         "source_name", "source_url (or unavailable)", "source_date",
                         "event_date (optional)", "published_date", "relevance",
                         "display_topic", "lifecycle (optional)", "topic_ids", "entity_ids",
                         "place_ids", "sensitivity_display", "verification_display",
                         "related_item_ids", "release_id"]
        field_lis = "".join(f"<li><code>{html(f)}</code></li>" for f in public_fields)
        internal_lis = "".join(
            f"<li>{html(x)}</li>" for x in [
                "reviewer notes and review decisions",
                "candidate records and evidence excerpts",
                "dedupe and signal metadata",
                "internal file paths and run identifiers",
                "sensitivity rationale",
                "logs and unpublished source proposals"])

        body = (
            '<div class="page prose">'
            '<h1>Data &amp; Sources</h1>'
            '<section aria-labelledby="src-release">'
            '<h2 id="src-release">Current release</h2>'
            '<dl class="detail-facts">'
            f'<div class="detail-row"><dt>Release</dt><dd>{html(release.get("release_id", ""))}</dd></div>'
            f'<div class="detail-row"><dt>Published</dt><dd>{html(pub_date or "—")}</dd></div>'
            f'<div class="detail-row"><dt>Updates</dt><dd>{count}</dd></div>'
            f'<div class="detail-row"><dt>Environment</dt><dd>{html(release.get("environment", ""))}</dd></div>'
            '</dl>'
            '</section>'
            '<section aria-labelledby="src-directory">'
            '<h2 id="src-directory">Source directory</h2>'
            '<p>Each update links to the original public record. The table '
            'below lists the sources referenced in this release and how many '
            'updates come from each.</p>'
            '<table class="source-table">'
            '<caption class="visually-hidden">Sources referenced in this release</caption>'
            '<thead><tr><th scope="col">Source</th><th scope="col">Type</th>'
            '<th scope="col">Updates</th></tr></thead>'
            f'<tbody>{tbody_html}</tbody>'
            '</table>'
            '</section>'
            '<section aria-labelledby="src-links">'
            '<h2 id="src-links">How source links are handled</h2>'
            '<p>Source links open the original public record in a new tab. '
            'When a link is unavailable, the item shows '
            '\u201cThe original source link is currently unavailable\u201d '
            'and the item remains published.</p>'
            '</section>'
            '<section aria-labelledby="src-fields">'
            '<h2 id="src-fields">Public data fields</h2>'
            f'<p>Each update carries only these public fields:</p><ul>{field_lis}</ul>'
            '</section>'
            '<section aria-labelledby="src-excluded">'
            '<h2 id="src-excluded">Excluded internal data</h2>'
            '<p>SilverLeaf Brief never exposes:</p>'
            f'<ul>{internal_lis}</ul>'
            '</section>'
            '<section aria-labelledby="src-limits">'
            '<h2 id="src-limits">Coverage limitations</h2>'
            '<p>This release reflects reviewed updates only; it is not '
            'complete county coverage and is not real-time. See '
            '<a href="about/index.html#coverage">Coverage &amp; limitations</a> '
            'for the full scope statement.</p>'
            '</section>'
            '<section aria-labelledby="src-report">'
            '<h2 id="src-report">Report a source problem</h2>'
            '<p>If a source link is broken or a source seems misattributed, '
            '<a href="about/index.html#report-an-issue">report an issue</a>.</p>'
            '</section>'
            '</div>')
        self._write("sources/index.html", tpl.page_shell(
            "Data & Sources", "Release provenance and source directory.", depth,
            "sources", body, self.ctx))

    # ------------------------------------------------------------------ #
    # 404
    # ------------------------------------------------------------------ #

    def build_404(self):
        depth = 0
        body = tpl.empty_state(
            "Page not found",
            "The page you are looking for does not exist or has moved.",
            depth, [("Latest updates", "index.html"), ("Browse", "browse/index.html")],
            heading_tag="h1")
        self._write("404.html", tpl.page_shell(
            "Page not found", "This page does not exist.", depth, "", body, self.ctx))

    # ------------------------------------------------------------------ #
    # Build
    # ------------------------------------------------------------------ #

    def build(self):
        self.clean_generated()
        self.build_latest()
        self.build_browse()
        self.build_collections()
        self.build_item_pages()
        self.build_about()
        self.build_sources()
        self.build_404()
        return self.routes


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def html(value):
    return tpl.html_escape(value)


def html_id(value):
    """Sanitize a stable ID for use in a filesystem route."""
    out = re.sub(r"[^A-Za-z0-9._-]", "-", str(value))
    return out


def topic_label(dimensions, topic_id):
    """Resident-facing label for a v0 display topic (never a raw taxonomy id)."""
    rec = (dimensions.get("display_topics") or {}).get(topic_id) or {}
    if rec.get("label"):
        return rec["label"]
    return tpl.V0_TOPIC_FALLBACK.get(topic_id, topic_id)


def main():
    ap = argparse.ArgumentParser(description="SilverLeaf Brief static site generator.")
    ap.add_argument("--source", default=None,
                    help="release artifact dir (default: latest real release, else site/data/demo)")
    ap.add_argument("--out-dir", default=os.path.join(REPO_ROOT, "site"),
                    help="output site root (default site/)")
    ap.add_argument("--list-routes", action="store_true",
                    help="print the routes that would be generated without writing")
    args = ap.parse_args()

    source_dir = args.source or default_release_dir()
    if not os.path.exists(os.path.join(source_dir, "release.json")):
        sys.exit(f"ERROR: no release.json in {source_dir}")

    builder = SiteBuilder(source_dir, args.out_dir)
    if args.list_routes:
        # Simulate route generation deterministically without writing.
        class DryRun(SiteBuilder):
            def _write(self, rel_path, content):
                self.routes.append(rel_path)

            def clean_generated(self):
                pass  # list-routes must never mutate the output directory
        d = DryRun(source_dir, args.out_dir)
        d.build()
        for route in sorted(d.routes):
            print(route)
        print(f"\n{len(d.routes)} routes ({len(d.items)} items, "
              f"env={d.release.get('environment')})")
        return

    routes = builder.build()
    summary = {
        "release_id": builder.release.get("release_id"),
        "environment": builder.release.get("environment"),
        "item_count": len(builder.items),
        "route_count": len(routes),
        "source": builder.source_dir,
        "out_dir": builder.out_dir,
    }
    build_json = os.path.join(builder.out_dir, "build.json")
    with open(build_json, "w", encoding="utf-8") as f:
        json.dump({
            **summary,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, f, indent=2, sort_keys=True)

    print(f"Built site at {builder.out_dir}")
    print(f"  release:     {summary['release_id']} ({summary['environment']})")
    print(f"  items:       {summary['item_count']}")
    print(f"  routes:      {summary['route_count']}")
    print(f"  build.json:  {build_json}")
    if summary["environment"] == "demo":
        print("  NOTE: demo release — nonproduction fixture data.")


if __name__ == "__main__":
    main()
