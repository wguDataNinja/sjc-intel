/* =============================================================================
   SilverLeaf Brief — Browse enhancement (progressive).
   Mirrors scripts/site_search.py (the reference implementation).
   No-JavaScript baseline: the full release list is already server-rendered;
   this file filters, ranks, and updates the URL. All core content is readable
   without it.
   ============================================================================= */
(function () {
  "use strict";

  var dataEl = document.getElementById("release-data");
  if (!dataEl) return;

  var data;
  try {
    data = JSON.parse(dataEl.textContent);
  } catch (e) {
    return; // degrade gracefully: full list stays visible
  }

  var entries = data.entries || [];          // search entries (with relevance)
  var dimensions = data.dimensions || {};    // id -> {label, ...}
  var listEl = document.getElementById("results-list");
  var countEl = document.querySelector(".result-count");
  var chipsEl = document.querySelector(".active-chips");
  var noResultsEl = document.getElementById("no-results");
  var searchInput = document.getElementById("search-input");
  var filtersOpenBtn = document.querySelector("[data-action=open-filters]");
  var filterSheet = document.getElementById("filter-sheet");
  var sheetBackdrop = document.getElementById("sheet");

  var DIMS = ["topic", "place", "entity", "scope"];
  var sheetTrigger = null;

  function normalize(text) {
    return String(text || "").toLowerCase().replace(/[^0-9a-z ]/g, " ");
  }
  function qTokens(q) {
    return normalize(q).split(/\s+/).filter(function (t) { return t.length >= 2; });
  }
  function hasTokens(entry, q) {
    var tokens = qTokens(q);
    if (!tokens.length) return true;
    var hay = entry.tokens || "";
    for (var i = 0; i < tokens.length; i++) {
      if (hay.indexOf(tokens[i]) === -1) return false;
    }
    return true;
  }
  function dimOverlap(entryIds, selected) {
    if (!selected.length) return true;
    for (var i = 0; i < selected.length; i++) {
      if ((entryIds || []).indexOf(selected[i]) !== -1) return true;
    }
    return false;
  }
  function matches(entry, state) {
    if (!hasTokens(entry, state.q)) return false;
    if (!dimOverlap(entry.topics, state.topic)) return false;
    if (!dimOverlap(entry.places, state.place)) return false;
    if (!dimOverlap(entry.entities, state.entity)) return false;
    if (state.scope.length && state.scope.indexOf(entry.relevance) === -1) return false;
    return true;
  }
  function score(entry, q) {
    if (!q) return 0;
    var ql = String(q).toLowerCase();
    var title = entry.title || "";
    var summary = entry.summary || "";
    var why = entry.why_it_matters || "";
    var labels = (entry.topics || []).concat(entry.places || [], entry.entities || [])
      .join(" ") + " " + (entry.source || "");
    var s = 0;
    if (ql && title.indexOf(ql) !== -1) s += 8;
    var tokens = qTokens(q);
    for (var i = 0; i < tokens.length; i++) {
      if (title.indexOf(tokens[i]) !== -1) s += 3;
      else if (summary.indexOf(tokens[i]) !== -1) s += 2;
      else if (why.indexOf(tokens[i]) !== -1) s += 1;
      else if (labels.indexOf(tokens[i]) !== -1) s += 1;
    }
    return s;
  }

  function parseState() {
    var state = { q: "", topic: [], place: [], entity: [], scope: [] };
    var params = new URLSearchParams(window.location.search);
    state.q = (params.get("q") || "").trim();
    DIMS.forEach(function (dim) {
      var all = params.getAll(dim);
      all.forEach(function (val) {
        val.split(",").forEach(function (part) {
          part = part.trim();
          if (part && state[dim].indexOf(part) === -1) state[dim].push(part);
        });
      });
    });
    return state;
  }

  function pushState(state) {
    var params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    DIMS.forEach(function (dim) {
      if (state[dim].length) params.set(dim, state[dim].join(","));
    });
    var qs = params.toString();
    var url = window.location.pathname + (qs ? "?" + qs : "");
    try {
      window.history.replaceState({}, "", url);
      sessionStorage.setItem("browseState", qs ? "?" + qs : "");
    } catch (e) { /* storage may be unavailable; ignore */ }
  }

  function labelFor(dim, key) {
    var map = dim === "topic" ? dimensions.display_topics
            : dim === "place" ? dimensions.places
            : dim === "entity" ? dimensions.entities
            : dimensions.relevance;
    var rec = (map || {})[key];
    return rec ? rec.label : key;
  }

  function render(state) {
    // Rank + filter, preserving release order for ties (stable sort).
    var matched = entries.filter(function (e) { return matches(e, state); });
    var scored = matched.map(function (e) { return { e: e, s: score(e, state.q) }; });
    scored.sort(function (a, b) { return b.s - a.s; });

    var cards = listEl.querySelectorAll(".card");
    var visible = {};
    var ordered = [];
    scored.forEach(function (pair) { ordered.push(pair.e.id); });
    scored.forEach(function (pair) { visible[pair.e.id] = true; });

    var fragment = document.createDocumentFragment();
    var byId = {};
    cards.forEach(function (card) {
      byId[card.getAttribute("data-item-id")] = card;
      card.hidden = !visible[card.getAttribute("data-item-id")];
    });
    ordered.forEach(function (id) { if (byId[id]) fragment.appendChild(byId[id]); });
    listEl.appendChild(fragment);

    // Result count + zero-results.
    var n = ordered.length;
    if (countEl) countEl.textContent = n + (n === 1 ? " update" : " updates");
    if (noResultsEl) noResultsEl.hidden = n !== 0;

    // Chips.
    var chips = [];
    function chipFor(dim, key) {
      return {
        dim: dim, key: key,
        label: labelFor(dim, key) + (dim === "scope" ? " (relevance)" : "")
      };
    }
    DIMS.forEach(function (dim) {
      state[dim].forEach(function (key) { chips.push(chipFor(dim, key)); });
    });
    renderChips(chips, state);
    renderCheckboxes(state);
    renderSheetCount(chips.length);
  }

  function renderChips(chips, state) {
    if (!chipsEl) return;
    chipsEl.textContent = "";
    chips.forEach(function (chip) {
      var span = document.createElement("span");
      span.className = "chip";
      span.textContent = chip.label + " ";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("aria-label", "Remove " + chip.label + " filter");
      btn.textContent = "\u00d7";
      btn.addEventListener("click", function () {
        state[chip.dim] = state[chip.dim].filter(function (k) { return k !== chip.key; });
        syncCheckboxes(state);
        pushState(state);
        render(state);
      });
      span.appendChild(btn);
      chipsEl.appendChild(span);
    });
  }

  function renderCheckboxes(state) {
    document.querySelectorAll(".filter-option input").forEach(function (input) {
      var key = input.getAttribute("data-key");
      var dim = input.getAttribute("data-dim");
      input.checked = state[dim].indexOf(key) !== -1;
    });
  }
  function syncCheckboxes(state) {
    renderCheckboxes(state);
    updateSheetCount();
  }

  function renderSheetCount(n) {
    document.querySelectorAll(".filters-open-count").forEach(function (el) {
      el.textContent = n || "";
    });
    var btn = document.querySelector(".filters-open");
    if (btn) btn.setAttribute("aria-expanded", String(filterSheet.classList.contains("is-open")));
  }
  function updateSheetCount() {
    var state = currentStateFromDom();
    var n = state.topic.length + state.place.length + state.entity.length + state.scope.length;
    renderSheetCount(n);
  }

  function currentStateFromDom() {
    var state = parseState();
    document.querySelectorAll(".filter-option input").forEach(function (input) {
      var key = input.getAttribute("data-key");
      var dim = input.getAttribute("data-dim");
      if (input.checked && state[dim].indexOf(key) === -1) state[dim].push(key);
      if (!input.checked) state[dim] = state[dim].filter(function (k) { return k !== key; });
    });
    return state;
  }

  function clearAll(state) {
    state.q = "";
    DIMS.forEach(function (dim) { state[dim] = []; });
    if (searchInput) searchInput.value = "";
    pushState(state);
    render(state);
  }

  // ---- Events ----
  function onSearchInput() {
    var state = parseState();
    state.q = searchInput.value.trim();
    if (state.q.length === 1) return; // begin after two characters
    pushState(state);
    render(state);
  }

  function onCheckboxChange() {
    var state = currentStateFromDom();
    state.q = searchInput ? searchInput.value.trim() : "";
    pushState(state);
    render(state);
  }

  // Sheet focus management.
  function firstFocusable(sheet) {
    var els = sheet.querySelectorAll("input, button, a");
    for (var i = 0; i < els.length; i++) {
      if (els[i].offsetParent !== null || els[i].getClientRects().length) return els[i];
    }
    return sheet;
  }
  function openSheet() {
    if (!filterSheet) return;
    sheetTrigger = document.activeElement;
    filterSheet.classList.add("is-open");
    if (sheetBackdrop) sheetBackdrop.classList.add("is-open");
    filterSheet.setAttribute("aria-modal", "true");
    var first = firstFocusable(filterSheet);
    if (first) first.focus();
    renderSheetCount();
  }
  function closeSheet() {
    if (!filterSheet) return;
    filterSheet.classList.remove("is-open");
    if (sheetBackdrop) sheetBackdrop.classList.remove("is-open");
    filterSheet.setAttribute("aria-modal", "false");
    if (sheetTrigger && sheetTrigger.focus) sheetTrigger.focus();
    updateSheetCount();
  }

  function trapFocus(e) {
    if (!filterSheet || !filterSheet.classList.contains("is-open")) return;
    if (e.key !== "Tab") return;
    var focusables = Array.prototype.slice.call(
      filterSheet.querySelectorAll("input, button, a"));
    if (!focusables.length) return;
    var first = focusables[0], last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus();
    }
  }

  function initEvents() {
    if (searchInput) {
      searchInput.addEventListener("input", onSearchInput);
      // Live region polite announcement via count change (handled in render).
    }
    document.querySelectorAll(".filter-option input").forEach(function (input) {
      input.addEventListener("change", onCheckboxChange);
    });
    document.querySelectorAll("[data-action=clear]").forEach(function (btn) {
      btn.addEventListener("click", function () { clearAll(parseState()); });
    });
    if (filtersOpenBtn) filtersOpenBtn.addEventListener("click", openSheet);
    document.querySelectorAll("[data-action=close-filters]").forEach(function (btn) {
      btn.addEventListener("click", closeSheet);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSheet();
    });
    document.addEventListener("keydown", trapFocus);
    window.addEventListener("popstate", function () {
      var state = parseState();
      if (searchInput) searchInput.value = state.q;
      render(state);
    });
    if (filterSheet && sheetBackdrop) {
      sheetBackdrop.addEventListener("click", closeSheet);
    }
  }

  // ---- Init ----
  function init() {
    var state = parseState();
    if (searchInput) searchInput.value = state.q;
    initEvents();
    render(state);
  }
  init();
})();
