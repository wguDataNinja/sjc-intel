#!/usr/bin/env python3
"""
SilverLeaf Brief — client search/filter logic (pure, testable).

Mirrors the behavior implemented in site/assets/js/browse.js. The Python here
is the reference implementation used by the site generator and the test
suite; the JS is a faithful port.

Semantics (docs/public_ui_v0_spec.md §7):
- OR within a filter dimension; AND across filter dimensions;
- search begins after two characters; lexical only; deterministic;
- release order breaks ties; no semantic search; no sort menu.
"""
import re

# Filters that map to a stable-id dimension.
DIMENSION_PARAMS = ("topic", "place", "entity", "scope")


def parse_query(query_string):
    """Parse a raw query string into a filter state.

    Returns dict with keys q (str) and topic/place/entity/scope (sets).
    Comma-separated values and repeated parameters are both supported, e.g.
    ?topic=infrastructure,transportation&entity=ENT-X or ?topic=a&topic=b.
    """
    state = {"q": "", "topic": set(), "place": set(), "entity": set(),
             "scope": set()}
    if not query_string:
        return state
    if query_string.startswith("?"):
        query_string = query_string[1:]
    pairs = query_string.split("&")
    for pair in pairs:
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        key = _unquote(key)
        value = _unquote(value)
        if key == "q":
            state["q"] = value.strip()
        elif key in DIMENSION_PARAMS:
            for part in value.split(","):
                part = part.strip()
                if part:
                    state[key].add(part)
    return state


def _unquote(value):
    from urllib.parse import unquote_plus
    return unquote_plus(value)


def normalize_tokens(text):
    """Tokenize search/copy text (matches JS normalize)."""
    text = text.lower()
    text = re.sub(r"[^0-9a-z ]", " ", text)
    tokens = [t for t in re.split(r"\s+", text) if t]
    return tokens


def _has_tokens(entry, q):
    """All q tokens (length>=2) must appear somewhere in the entry tokens."""
    tokens = [t for t in normalize_tokens(q) if len(t) >= 2]
    if not tokens:
        return True
    hay = entry.get("tokens") or ""
    return all(t in hay for t in tokens)


def _matches_dimension(entry_ids, selected):
    """OR within a dimension: any overlap => match (empty selection = all)."""
    if not selected:
        return True
    return bool(set(entry_ids) & selected)


def matches(entry, state, release_items_by_id=None):
    """Boolean filter for one search-index entry against a filter state."""
    if not _has_tokens(entry, state.get("q", "")):
        return False
    if not _matches_dimension(entry.get("topics") or [], state.get("topic")):
        return False
    if not _matches_dimension(entry.get("places") or [], state.get("place")):
        return False
    if not _matches_dimension(entry.get("entities") or [], state.get("entity")):
        return False
    if state.get("scope"):
        # scope filters on the item's relevance id (from release.json).
        item = (release_items_by_id or {}).get(entry.get("id")) or {}
        if item.get("relevance") not in state["scope"]:
            return False
    return True


def score(entry, q):
    """Deterministic relevance score (higher = better). Release order ties.

    Exact phrase in title > title word match > summary word match >
    why-it-matters / label match.
    """
    if not q:
        return 0
    q_lower = q.lower()
    title = entry.get("title") or ""
    summary = entry.get("summary") or ""
    why = entry.get("why_it_matters") or ""
    labels = " ".join(
        list(entry.get("topics") or []) +
        list(entry.get("places") or []) +
        list(entry.get("entities") or []))
    tokens = [t for t in normalize_tokens(q) if len(t) >= 2]

    score_val = 0
    if q_lower and q_lower in title:
        score_val += 8
    for t in tokens:
        if t in title:
            score_val += 3
        elif t in summary:
            score_val += 2
        elif t in why:
            score_val += 1
        elif t in labels or t in (entry.get("source") or ""):
            score_val += 1
    return score_val


def search_and_filter(release_items, search_entries, state):
    """Apply filters + optional ranking, preserving release order on ties.

    Returns a list of release item dicts (the same objects, ordered).
    """
    by_id = {e["id"]: e for e in search_entries}
    item_by_id = {it["public_item_id"]: it for it in release_items}

    matched = [it for it in release_items
               if matches(by_id[it["public_item_id"]], state, item_by_id)]

    q = state.get("q", "")
    # Search "begins after two characters": a query with no 2+ char tokens is
    # a no-op (no filtering and no reordering).
    if not q or not [t for t in normalize_tokens(q) if len(t) >= 2]:
        return matched

    scored = [(score(by_id[it["public_item_id"]], q), it) for it in matched]
    # stable sort by score desc preserves release order within equal scores
    scored.sort(key=lambda pair: -pair[0])
    return [it for _, it in scored]
