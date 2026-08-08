#!/usr/bin/env python3
"""
SilverLeaf Brief — HTML template helpers for the static site generator.

Shared rendering for the site shell, item cards, badges, and the single
collection-page template used by topic/place/entity routes. The generator
(scripts/build_static_site.py) calls these to emit semantic, accessible,
no-JavaScript-readable HTML.
"""
import json
import re
from datetime import datetime

SITE_TITLE = "SilverLeaf Brief"
TAGLINE = "What changed around SilverLeaf—and why it matters."

REVIEWED_DETAIL = (
    "Each summary is reviewed against the linked source for clarity, "
    "relevance, and attribution before publication."
)
TRUST_STATEMENT = (
    "Reviewed summaries with direct links to public sources."
)
SOURCE_UNAVAILABLE = "The original source link is currently unavailable."

# v0 resident topic label fallback (dimensions.display_topics carry the real
# labels; this guard prevents any raw id from ever rendering).
V0_TOPIC_FALLBACK = {
    "roads_traffic": "Roads & Traffic",
    "utilities_water": "Utilities & Water",
    "emergency_preparedness": "Emergency Preparedness",
    "schools_community": "Schools & Community",
    "local_business": "Local Business",
}

# Relevance id -> human label (dimensions carry the label; fallback here).
RELEVANCE_FALLBACK = {
    "in_silverleaf": "In SilverLeaf",
    "near_silverleaf": "Near SilverLeaf",
    "countywide_impact": "Countywide impact",
}

_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


def html_escape(value):
    return (
        str(value)
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("'", "&#39;")
    )


def embed_json(data):
    """Inline JSON safe for a <script type=application/json> block."""
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026"))


def rel(depth, target):
    """Build a site-root-relative URL from a page at the given depth."""
    return "../" * depth + target


def format_date(value, default=None):
    """Absolute, human-readable date from an ISO date string."""
    if not value:
        return default
    s = str(value)[:10]
    try:
        dt = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return str(value)
    return f"{_MONTHS[dt.month - 1]} {dt.day}, {dt.year}"


# --------------------------------------------------------------------------- #
# Badges and card pieces
# --------------------------------------------------------------------------- #

def relevance_label(dimensions, relevance_id):
    d = (dimensions.get("relevance") or {}).get(relevance_id)
    if d and d.get("label"):
        return d["label"]
    return RELEVANCE_FALLBACK.get(relevance_id, relevance_id)


def relevance_badge(dimensions, relevance_id):
    label = relevance_label(dimensions, relevance_id)
    return (f'<span class="badge badge-relevance badge-relevance--{html_escape(relevance_id)}">'
            f'{html_escape(label)}</span>')


def topic_badge(dimensions, topic_id):
    """Resident-facing topic chip (v0 display topic; never a raw taxonomy id)."""
    label = ((dimensions.get("display_topics") or {}).get(topic_id) or {}) \
        .get("label") or V0_TOPIC_FALLBACK.get(topic_id, topic_id)
    return (f'<span class="badge badge-topic" data-topic="{html_escape(topic_id)}">'
            f'{html_escape(label)}</span>')


def reviewed_badge(depth=0):
    """'Reviewed' trust label; links to the About definition."""
    return (f'<a class="badge badge-reviewed" href="{rel(depth, "about/index.html")}#reviewed" '
            f'title="{html_escape(REVIEWED_DETAIL)}">'
            f'<span aria-hidden="true" class="badge-dot"></span>Reviewed</a>')


def lifecycle_badge(record):
    label = record.get("lifecycle_label") or record.get("lifecycle")
    if not label:
        return ""
    return (f'<span class="badge badge-lifecycle" data-lifecycle="{html_escape(record.get("lifecycle", ""))}">'
            f'{html_escape(label)}</span>')


# Public labels for the editorial product role (latest/browse/context/timeline).
ROLE_LABELS = {
    "latest": "Latest",
    "browse": "Browse",
    "context": "Context",
    "timeline": "Timeline",
}


def role_badge(record):
    role = record.get("role") or "browse"
    label = ROLE_LABELS.get(role, role.title())
    return (f'<span class="badge badge-role" data-role="{html_escape(role)}">'
            f'{html_escape(label)}</span>')


def qualified_badge(record):
    if not record.get("qualified"):
        return ""
    label = record.get("qualified_label") or "Details unconfirmed"
    return (f'<span class="badge badge-qualified" title="{html_escape(label)}">'
            f'<span aria-hidden="true">&#9888;</span> {html_escape(label)}</span>')


def source_link(record, depth):
    """Original source action; handles the unavailable state."""
    url = record.get("source_url")
    name = record.get("source_name") or "Source"
    if url:
        return (f'<a class="action-source" href="{html_escape(url)}" '
                f'target="_blank" rel="noopener noreferrer">'
                f'Original source <span class="visually-hidden">: {html_escape(name)} (opens in a new tab)</span>'
                f'<span class="external-icon" aria-hidden="true">&#8599;</span></a>')
    return (f'<span class="action-source is-unavailable" '
            f'title="{html_escape(SOURCE_UNAVAILABLE)}">'
            f'Original source <span class="visually-hidden">: currently unavailable</span></span>')


def item_card(record, dimensions, depth):
    """The shared item card (Latest, Browse, collection routes)."""
    pid = record["public_item_id"]
    href = rel(depth, f"item/{pid}/index.html")
    display_topic = record.get("display_topic") or "utilities_water"

    meta = " ".join([
        relevance_badge(dimensions, record.get("relevance", "countywide_impact")),
        topic_badge(dimensions, display_topic),
        role_badge(record),
        qualified_badge(record),
        reviewed_badge(depth),
        lifecycle_badge(record),
    ])

    src_date = format_date(record.get("source_date"))
    event_date = format_date(record.get("event_date"))
    source_dl_rows = []
    if event_date and record.get("event_date_label"):
        source_dl_rows.append(
            f'<div class="card-source-row"><dt>{html_escape(record["event_date_label"])}</dt>'
            f'<dd>{html_escape(event_date)}</dd></div>')
    source_dl_rows.append(
        f'<div class="card-source-row"><dt>Source</dt>'
        f'<dd class="card-source-name">{html_escape(record.get("source_name") or "—")}</dd></div>')
    source_dl_rows.append(
        f'<div class="card-source-row"><dt>Source published</dt>'
        f'<dd>{html_escape(src_date) if src_date else "Not available"}</dd></div>')
    source_dl = f'<dl class="card-source">{"".join(source_dl_rows)}</dl>'

    return (
        f'<article class="card" data-item-id="{html_escape(pid)}">\n'
        f'  <div class="card-meta">{meta}</div>\n'
        f'  <h3 class="card-title"><a href="{href}">{html_escape(record.get("title") or "")}</a></h3>\n'
        f'  <p class="card-summary">{html_escape(record.get("summary") or "")}</p>\n'
        f'  <div class="card-why">\n'
        f'    <h4 class="card-why-title">Why it matters</h4>\n'
        f'    <p>{html_escape(record.get("why_it_matters") or "")}</p>\n'
        f'  </div>\n'
        f'  {source_dl}\n'
        f'  <div class="card-actions">\n'
        f'    <a class="action-read" href="{href}">Read update</a>\n'
        f'    {source_link(record, depth)}\n'
        f'  </div>\n'
        f'</article>'
    )


def item_card_compact(record, dimensions, depth):
    """Compact card for related-items lists on the detail page."""
    pid = record["public_item_id"]
    href = rel(depth, f"../{pid}/index.html")
    return (
        f'<li class="related-item"><a href="{href}">{html_escape(record.get("title") or "")}</a> '
        f'<span class="related-item-date">— {html_escape(format_date(record.get("source_date")) or "date unavailable")}</span></li>'
    )


# --------------------------------------------------------------------------- #
# Shell
# --------------------------------------------------------------------------- #

def page_shell(title, description, depth, active_nav, body, ctx,
               extra_head="", body_class=""):
    """Full HTML document: skip link, header, main, footer, mobile nav."""
    css = rel(depth, "assets/css/silverleaf.css")
    demo_banner = ""
    if ctx.get("environment") == "demo":
        demo_banner = (
            '<div class="demo-banner" role="note">'
            '<strong>Demo preview.</strong> This site shows example data to '
            'demonstrate SilverLeaf Brief. It is not a real public release.'
            '</div>')

    nav_items = [
        ("index.html", "Latest", "latest"),
        ("browse/index.html", "Browse", "browse"),
        ("about/index.html", "About", "about"),
    ]
    nav_links = []
    for target, label, key in nav_items:
        cls = ' class="nav-link is-active" aria-current="page"' if key == active_nav else ' class="nav-link"'
        nav_links.append(f'<a href="{rel(depth, target)}"{cls}>{label}</a>')

    release = ctx.get("release") or {}
    release_line = f'{html_escape(release.get("release_id", ""))} · {html_escape(format_date(release.get("published_at")) or "no date")}'
    env_note = ' · <span class="footer-demo">demo data</span>' if ctx.get("environment") == "demo" else ""

    footer = (
        f'<footer class="site-footer" id="footer">'
        f'  <nav class="footer-nav" aria-label="Secondary">'
        f'    <a href="{rel(depth, "sources/index.html")}">Data &amp; Sources</a>'
        f'    <a href="{rel(depth, "about/index.html")}#coverage">Coverage &amp; limitations</a>'
        f'    <a href="{rel(depth, "about/index.html")}#report-an-issue">Report an issue</a>'
        f'  </nav>'
        f'  <p class="footer-release">Current release: {release_line}{env_note}</p>'
        f'  <p class="footer-note">Not an official government or emergency-alert service.</p>'
        f'</footer>'
    )

    bottom_nav = (
        '<nav class="bottom-nav" aria-label="Primary">'
        f'<a class="bottom-nav-item{" is-active" if active_nav == "latest" else ""}" href="{rel(depth, "index.html")}">Latest</a>'
        f'<a class="bottom-nav-item{" is-active" if active_nav == "browse" else ""}" href="{rel(depth, "browse/index.html")}">Browse</a>'
        f'<a class="bottom-nav-item{" is-active" if active_nav == "about" else ""}" href="{rel(depth, "about/index.html")}">About</a>'
        '</nav>'
    )

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <meta name="description" content="{html_escape(description)}">\n'
        f'  <meta name="theme-color" content="#235B43">\n'
        f'  <title>{html_escape(title)} · SilverLeaf Brief</title>\n'
        f'  <link rel="stylesheet" href="{css}">\n'
        f'  {extra_head}'
        '</head>\n'
        f'<body class="{body_class}">\n'
        '  <a class="skip-link" href="#main">Skip to main content</a>\n'
        f'  {demo_banner}'
        '  <header class="site-header">\n'
        f'    <p class="brand"><a href="{rel(depth, "index.html")}">SilverLeaf <span>Brief</span></a></p>\n'
        f'    <nav class="primary-nav" aria-label="Primary">{"" .join(nav_links)}</nav>\n'
        '  </header>\n'
        f'  <main id="main">{body}</main>\n'
        f'  {footer}'
        f'  {bottom_nav}'
        '</body>\n'
        '</html>\n'
    )


def empty_state(title, message, depth, links=(), heading_tag="h2"):
    parts = [f'<div class="empty-state">'
             f'<{heading_tag}>{html_escape(title)}</{heading_tag}>'
             f'<p>{html_escape(message)}</p>']
    if links:
        parts.append('<ul class="empty-links">')
        for label, target in links:
            parts.append(f'<li><a href="{rel(depth, target)}">{html_escape(label)}</a></li>')
        parts.append('</ul>')
    parts.append('</div>')
    return "".join(parts)


# --------------------------------------------------------------------------- #
# Collection page (one reusable template for topic/place/entity)
# --------------------------------------------------------------------------- #

def collection_page(collection_kind, collection_id, label, description,
                    items, dimensions, depth, ctx, related_filters):
    """Single collection-page template used by topic/place/entity routes.

    collection_kind: 'topic' | 'place' | 'entity'
    related_filters: list of (label, rel_href) navigation to sibling collections.
    """
    count = len(items)
    if items:
        cards = "\n".join(item_card(it, dimensions, depth) for it in items)
        body_items = cards
    else:
        body_items = empty_state(
            "No items in this collection yet",
            "This collection is valid but currently has no published items.",
            depth,
            [("Browse all updates", "browse/index.html")],
        )

    filters_html = ""
    if related_filters:
        links = " ".join(
            f'<a class="related-filter" href="{rel(depth, target)}">{html_escape(lbl)}</a>'
            for lbl, target in related_filters)
        filters_html = f'<div class="collection-filters" aria-label="Related collections">{links}</div>'

    kind_label = {"topic": "Topic", "place": "Place", "entity": "Entity"}[collection_kind]

    body = (
        f'<div class="page collection-page">\n'
        f'  <p class="breadcrumb"><a href="{rel(depth, "browse/index.html")}">Browse</a> / '
        f'<span>{html_escape(kind_label)}</span></p>\n'
        f'  <header class="collection-header">\n'
        f'    <h1>{html_escape(label)}</h1>\n'
        f'    <p class="collection-count" aria-live="polite">{count} update{"s" if count != 1 else ""}</p>\n'
        f'    {filters_html}'
        f'    {("<p class=collection-description>" + html_escape(description) + "</p>") if description else ""}'
        f'  </header>\n'
        f'  <div class="collection-items">{body_items}</div>\n'
        '</div>'
    )
    page_title = f"{label} — {kind_label}"
    return page_shell(page_title, f"{kind_label} collection: {label}", depth, "browse", body, ctx)
