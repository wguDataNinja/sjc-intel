# SJC Intel — Knowledge Base Cross-Project Comparison

**Date:** 2026-07-06
**Purpose:** Compare SJC Intel architecture with BSDA Courses and Idle Hacking KB
knowledge-base patterns, then produce a practical strategy for evolving SJC into
a structured local-intelligence knowledge base supporting multiple downstream
products.

**Scope:** Read-only comparison. No code or data modified.

---

## Executive Summary

SJC Intel can become a structured local-intelligence knowledge base by adopting
pattern concepts from two existing portfolio knowledge-base projects.

### The Two Knowledge-Base Models

**BSDA Courses** (`bsda_courses/`) is a **structured domain-record knowledge
base**. It ingests unstructured Reddit text, runs a multi-stage deterministic + LLM
pipeline, and produces validated **claim registers** — structured records that are
traceable to source evidence. Claims have publication status, confidence, evidence
refs, and gate diagnostics. Core object: the **claim** (canonical, versioned,
evidence-backed). Output: Reddit posts, audit companions, static HTML UI.

**Idle Hacking KB** (`idlehacking_kb/`) is a **large unstructured-content
knowledge base**. It ingests chat from Discord and VPS, runs a deterministic
filter to reduce volume, then applies LLM Scout stages for conversation-unit
discovery. Core objects are **accepted claims** (242, human-reviewed), a game
elements ontology (125 entries), glossary (216 terms), and aliases (148 entries).
Four-layer authority model prevents auto-promotion. No public-facing UI.

### What SJC Can Learn

| Pattern | Best Source | What SJC Gains |
|---------|-------------|----------------|
| LLM provider abstraction | BSDA `scripts/llm_provider.py` | Multi-provider support with structured JSON schema output |
| Run metadata provenance | Idle Hacking `scripts/llm/run_metadata.py` | Prompt/model/schema version tracking |
| Claim register model | BSDA `scripts/build_claim_register.py` | Publication-ready structured claims with status/confidence/evidence |
| Source evidence tracking | BSDA citation index + debug | Trace every claim to specific source text |
| Stage gate with HITL | BSDA `--llm-decision` + review mode | Safe introduction of LLM stages |
| Deterministic pre-filter | Idle Hacking `guide_area_routing.py` | Reduce chat/text volume before LLM stages |
| 4-layer authority model | Idle Hacking `spec-july-1.md` | Prevent auto-promotion of LLM output to production |
| Accepted claims governance | Idle Hacking `data/kb/accepted_claims/` | Versioned truth with staleness detection |
| Anchored ontology | Idle Hacking `game_elements/registry_v1.json` | Entity registry with anchor-safety policy |
| Staged review gates | Idle Hacking `AGENTS.md` (smoke→calibration→gold→corpus) | Systematic classifier calibration |

### SJC's Current Position

SJC today is closer to BSDA's model: it ingests structured public records and
produces classified intel items. But it lacks BSDA's claim register, provenance
tracking, and LLM stages. It also lacks Idle Hacking's authority layers, accepted
claims governance, and entity ontology.

### Recommended Knowledge-Base Model

**Hybrid with intel-item center and claim-structured output.** Keep intel items
as the primary ingestion record. Add a **claim register** layer (like BSDA) for
structured, publishable claims extracted from intel items. Add an **entity
registry** (like Idle Hacking's game_elements) for tracked entities, locations,
and topics. Use a **4-layer authority model** to prevent LLM output from becoming
production truth without review.

---

## Section 1 — BSDA Courses Knowledge-Base Architecture

### 1.1 Core Knowledge Object: The Claim

The primary canonical record is the **claim** within a **claim register**.
Each claim has the following structure (from `scripts/build_claim_register.py`):

| Field | Type | Example |
|-------|------|---------|
| `claim_id` | string (per-course) | `D426-C001` |
| `source_claim_id` | string | Internal pipeline ID |
| `course_code` | string | `D426` |
| `category` | string | Section category |
| `claim_text` | string | Publication-ready prose |
| `claim_type` | string | Human-readable category |
| `publication_status` | enum | `publishable` / `publishable_with_caveat` / `hold_for_review` / `do_not_publish` |
| `confidence` | enum | `high`, `medium`, `low` |
| `support_summary` | string | Reasoning/evidence summary |
| `caveats` | list[str] | Warning flags |
| `evidence_refs` | list[str] | Evidence IDs supporting claim |
| `citation_refs` | list[dict] | `{evidence_id, source_id, source_type, url}` |
| `trace_refs` | list[dict] | Pipeline run provenance |
| `evidence_count` | int | Number of evidence items |
| `source_count` | int | Number of unique sources |
| `gate_diagnostics` | object | 5 boolean checks (supporting evidence, traceable sources, etc.) |
| `excluded_from_public_post` | bool | Publication exclusion flag |
| `review_notes` | string | Reviewer notes |

### 1.2 Pipeline Architecture

The pipeline is a **mixed deterministic + LLM** sequence with strict I/O contracts:

```
Source (Reddit DB)
  → Stage 0: Bootstrap (deterministic)
  → Stage pre1: Build Relevance Input (deterministic)
  → Stage 1: Relevance LLM → selects relevant posts
  → Stage pre2: Build Categorize Input (deterministic)
  → Stage 2: Categories LLM → sections and categories
  → Stage pre3: Build Claims Input (deterministic)
  → Stage 3: Claims LLM → candidate claims
  → Stage pre4: Build Calibration Input (deterministic)
  → Stage 4: Calibration LLM → calibrated claims
  → Stage 5: Trace (deterministic) → revision trace
  → Stage 6: Assemble LLM → pre-polish guide
  → postB: Render Citations (deterministic) → evidence→source resolution
  → postC: Assemble Final Guide (deterministic)
  → Build Claim Register (deterministic) → canonical record
  → Validation → Publication
```

**Key architectural principles:**
- Deterministic builders wrap all LLM stages (no raw LLM output enters pipeline)
- LLM stages require `--llm-decision` gate (explicit approval per model tier)
- Evidence IDs are **section-local**, not global (prevents cross-contamination)
- All stage outputs include metadata: `stage`, `owner`, `production_mode`, `upstream_inputs`
- SHA-256 tracking of all input artifacts

### 1.3 LLM Provider Abstraction

**File:** `scripts/llm_provider.py` (508 lines)

```python
@runtime_checkable
class ChatClient(Protocol):
    def chat(self, model, messages, *, temperature=0.0, max_tokens=None,
             response_format="json_object", response_schema=None) -> dict:
        ...
```

**Four providers:** OpenAI, Anthropic, Ollama, opencode-go (via `make_client()`).

**Structured JSON output** via `response_schema` parameter (OpenAI `json_schema` mode).

**Key function:** `build_claims_response_schema()` generates a narrow JSON Schema
for Stage 3 claims with `evidence_enum` constraints.

### 1.4 Review and Approval

- **HITL points:** Stage 2 taxonomy requires human approval before Stage 3.
  Stage 6 guide is the editable prose artifact.
- **Review mode:** `scripts/orchestrate.py --mode review` generates 8+ review
  artifacts: `review_packet.md`, `survival_ledger.json`, `claims_input_summary.json`,
  `unused_evidence_report.json`, `duplication_review.json`, etc.
- **Validation:** `scripts/validate_claim_register.py` checks 18 required fields per
  claim, publication status semantics, evidence consistency, and gate thresholds.

### 1.5 Search and Filtering

No general-purpose search. Course-specific citation resolution via `render_citations.py`.
Live Reddit search via `experiment_live_search.py`. Daily triage queue via
`fetch_detected_posts.py` → Obsidian dashboard.

### 1.6 Downstream Products

| Product | Implementation | Status |
|---------|---------------|--------|
| Reddit posts | `scripts/build_publishable_guides.py` | 37 guides, awaiting HITL |
| Audit companion | Same script per course | Generated with each post |
| Static HTML UI | `scripts/build_static_ui.py` | 38 pages, never reviewed by Buddy |
| Explorer package | `scripts/build_publishable_explorer.py` | Structured JSON data export |

### 1.7 Key Files

| File | Purpose |
|------|---------|
| `scripts/llm_provider.py` | Multi-provider LLM abstraction |
| `scripts/orchestrate.py` | Pipeline orchestrator (999 lines) |
| `scripts/build_claim_register.py` | Claim register builder |
| `scripts/validate_claim_register.py` | Claim register validator |
| `data/claim_register_config.json` | Gate thresholds |
| `scripts/render_citations.py` | Evidence→source citation resolution |
| `scripts/build_trace.py` | Claim revision trace |
| `scripts/build_static_ui.py` | Static HTML UI generator |
| `scripts/build_publishable_explorer.py` | Structured data export |
| `PIPELINE_SPEC.md` | 961-line publication contract |
| `docs/IMPLEMENTATION_SPEC.md` | 854-line implementation spec |
| `docs/reviewer_rfi.md` | External review invitation |

---

## Section 2 — Idle Hacking KB Architecture

### 2.1 Core Knowledge Object: The Accepted Claim

**File:** `data/kb/accepted_claims/schema_v1.json`

| Field | Description |
|-------|-------------|
| `claim_id` | Dotted path: `<topic>.<subject>.<slug>.v<version>` |
| `topic_id` | Must match `topic_manifest.json` |
| `claim` | Factual claim text (human-reviewed truth) |
| `status` | `accepted` / `rejected` / `superseded` / `needs_review` |
| `authority_layer` | `official_updates` > `official_help` > `expert_consensus` > ... |
| `evidence` | Array of resolvable evidence anchors |
| `valid_from`, `valid_until` | Temporal validity bounds |
| `superseded_by`, `last_checked_against_updates` | Staleness tracking |
| `reviewed_by`, `reviewed_at` | Human review trail |
| `confidence_label`, `confidence_score` | Confidence tracking |

**Current state:** 242 accepted claims across 7 topics. No auto-promotion.

### 2.2 Architecture: Three Pillars

| Pillar | Function | Status |
|--------|----------|--------|
| **Pillar 1 — Filter** | Deterministic semantic routing, reduces chat volume ~92% before LLM | Production (20 filter areas) |
| **Pillar 2 — Claims** | Claim lifecycle, versioning, staleness, contradiction | Draft (schema designed, store populated) |
| **Pillar 3 — Answerability** | Decides whether to answer, caveat, or refuse | Prototype (Phase 8 complete) |

### 2.3 Four-Layer Authority Model

| Layer | Contents | Rule |
|-------|----------|------|
| **Evidence / Source** | Raw chat archives, source records | Observational evidence, not canon |
| **Understanding** | Glossary, aliases, game_elements, filter routing | Structured observations, not truth |
| **Derived / Evaluation** | LLM outputs, Scout results, review packets | Candidate-only until reviewed |
| **Authority / Production** | Accepted claims, production filters, detector registry | Requires explicit approval to mutate |

**No cross-layer mutation without explicit approval.** No agent or LLM may auto-promote.

### 2.4 LLM Provider Abstraction

**File:** `scripts/llm/provider_interface.py` (clean ABC)

```python
class ProviderInterface(ABC):
    def invoke(self, prompt: str, config: LLMConfig) -> LLMResult: ...
    def validate_output(self, output: str) -> bool: ...
    def is_available(self) -> bool: ...

@dataclass
class LLMConfig:
    model: str = "deepseek-v4-flash"
    temperature: float = 0.0
    max_tokens: int = 4096
    timeout: int = 120
    retry_count: int = 2
    retry_delay: float = 2.0

@dataclass
class LLMResult:
    raw_output: str
    parsed_output: dict | None
    tokens_in: int
    tokens_out: int
    cost_cents: float
    latency_ms: int
    error: str | None
    status: str
```

**Additional modules:**
- `scripts/llm/config.py` — `ProviderConfig` dataclass, `config_from_dict()`, `DEFAULT_CONFIG`
- `scripts/llm/run_metadata.py` — `RunMetadata` dataclass with provider, model, prompt versions, schema versions, timing, cost
- `scripts/llm/fixture_provider.py` — Canned-response test provider
- `scripts/llm/prompt_registry.py` — Versioned prompt registry with SHA-256 content hashing
- `scripts/llm/privacy.py` — `classify_input()` (PUBLIC/PRIVATE/SENSITIVE) + `redact_for_export()`

### 2.5 Ingestion Pipeline

**Two source families:**

| Source | Capture | Mechanism |
|--------|---------|-----------|
| VPS game chat | Auto (Tampermonkey userscript) | WebSocket + DOM → VPS disk → rsync → `data/chat/collector/archive/` |
| Discord chat | Manual (Chrome extension export) | Extension → CSV download → `data/discord/` |

**Ingestion → Clean Posts → Two downstream paths:**
1. **Path A — Scout:** Deterministic filter → Scout LLM → conversation units → Director review
2. **Path B — Answerability:** LLM harness → question discovery → answer hypotheses

### 2.6 Deterministic Filter

**File:** `scripts/lib/guide_area_routing.py` (908 lines)

20 production filter areas. First-matching-area-wins strategy.
Context-gated matching for ambiguous terms.
Produces 16-field sidecar per post (matched_area_ids, suppression_reasons, etc.).
~92% reduction on ~6,000 post corpus.

### 2.7 Scout Pipeline

**File:** `scripts/kb_agents/scout.py` (1383 lines)

Conversation-unit discovery: takes filtered chat window → LLM identifies bounded
conversation units with participants, boundaries, summary, and outcomes.
Output schema v1 with strict validation (`validate_payload()`).

### 2.8 Accepted Claims Governance

- **Store:** `data/kb/accepted_claims/` — per-topic `claims.jsonl` + `all_claims.jsonl`
- **Versioning:** `<topic>.<subject>.<slug>.v<version>` pattern
- **Status values:** `accepted`, `rejected`, `superseded`, `needs_review`
- **Temporal tracking:** `valid_from`, `valid_until`, `last_checked_against_updates`
- **Promotion rules:** Human review required, minimum 1 evidence anchor, authority layer check

### 2.9 Ontology Model

- **Game elements registry:** `data/registry/game_elements/registry_v1.json` (125 entries)
- **Glossary:** `data/registry/glossary_terms.csv` (216 rows)
- **Aliases:** `data/registry/term_aliases.csv` (148 rows)
- **KB taxonomy:** `data/kb_taxonomy_v1.md` (13 sections)
- **Anchor-safety policy:** `docs/anchor-safety-policy.md` (8 core principles)

### 2.10 Database Schema

PostgreSQL metadata store (NOT for raw chat bodies):

| Schema | Purpose | Key Tables |
|--------|---------|------------|
| `archive` | Source/channel/file/ingest tracking | `sources`, `channels`, `files`, `ingest_runs` |
| `app` | Message metadata, claims, QA index | `message_metadata`, `provenance_records`, `accepted_claims`, `claim_topics`, `claim_evidence_links`, `qa_index_metadata` |
| `llm` | LLM stage/invocation/output/validation | `stages`, `prompt_versions`, `invocations`, `outputs`, `validation_results` |
| `health` | Private health status | `private_status` |

10 migrations (001-010), all INERT (not to be applied without DB Authority Gate approval).

### 2.11 Key Files

| File | Purpose |
|------|---------|
| `spec-july-1.md` | Current architecture/scope contract |
| `scripts/llm/provider_interface.py` | Abstract LLM provider interface |
| `scripts/llm/run_metadata.py` | Run metadata audit trail |
| `scripts/llm/config.py` | Provider config |
| `scripts/llm/fixture_provider.py` | Test fixture provider |
| `scripts/llm/privacy.py` | Privacy classification/redaction |
| `scripts/llm/prompt_registry.py` | Versioned prompt registry |
| `scripts/kb_agents/scout.py` | Conversation-unit discovery |
| `scripts/lib/guide_area_routing.py` | Deterministic filter engine |
| `scripts/search_kb_evidence.py` | KB evidence search |
| `data/kb/accepted_claims/schema_v1.json` | Claim schema |
| `data/registry/game_elements/registry_v1.json` | Game elements ontology |
| `data/kb_taxonomy_v1.md` | KB taxonomy |
| `docs/ontology-routing-authority-stack.md` | Authority layer definitions |
| `docs/anchor-safety-policy.md` | Anchor safety policy |
| `docs/data_model.md` | Complete entity/relationship model |

---

## Section 3 — Side-by-Side Comparison

| Dimension | BSDA Courses | Idle Hacking KB | SJC Intel |
|-----------|-------------|-----------------|-----------|
| **Source type** | Reddit posts (unstructured text) | Chat (Discord + VPS, unstructured) | Government web pages (structured HTML + PDF) |
| **Core object** | Claim (in claim_register) | Accepted claim | Intel item |
| **Source→record lifecycle** | Multi-stage pipeline (0→postC) | Filter → Scout → review → accept | Manual fetch → classify → queue |
| **Normalization** | Deterministic pre-processors | Deterministic filter + CSV pipeline | Python extractors (per-source) |
| **Entity modeling** | Course codes, evidence IDs, source IDs | Game_elements registry (125), glossary (216), aliases (148) | Tracked entities (11), communities (20), topics (24) |
| **Relationship modeling** | Evidence→claim→citation (per-claim resolution) | claim→evidence (anchor-based), element→alias | intel_item→tracked_entity (flat array), dedupe key |
| **Topic modeling** | Course sections (taxonomy gate) | KB taxonomy (13 sections) | Topics (24), beats (14), interest tags (10) |
| **Temporal modeling** | Pipeline run timestamps, trace refs | `valid_from`, `valid_until`, `last_checked` | `discovered_at`, `source_published_at` |
| **Provenance** | SHA-256 artifact hashes, run IDs, trace refs | Run metadata, source registry, post maps | Dedupe key (SHA-256), source_event backlink |
| **Search** | Per-course citation index, live Reddit search | `search_kb_evidence.py` (scored + filtered) | None |
| **Filtering** | Relevance stage (LLM) | Deterministic filter (20 areas, rule-based) | Interest filters (7 categories, keyword) |
| **User-interest matching** | Course-code based | Area routing (20 filter areas) | Interest filter keywords |
| **LLM stages** | 5 stages (relevance→categories→claims→calibration→assemble) | Scout (conversation-unit discovery), future classifier | None |
| **LLM provider** | Multi-provider (OpenAI, Anthropic, Ollama, opencode-go) | Multi-provider (ABC with FixtureProvider) | None |
| **Review** | Orchestrator review mode, HITL points, validation scripts | Outbox packets, Buddy approval, no auto-promotion | Flat queue (132 entries), CLI review tools |
| **Publication** | Reddit posts, audit companion, static HTML UI, explorer export | None (internal KB only) | None |
| **Snapshots** | Pipeline manifests, run logs, pre-refresh snapshots | Filter run sidecars (16-field), deep annotation sets | Metric snapshots (9 types), dedupe index |
| **Downstream consumers** | Reddit readers, static site visitors | Future Q&A, future chatbot | None (internal only) |
| **Privacy** | `data/reddit_account/` never read by public scripts; `--check` mode | `scripts/llm/privacy.py` (classify + redact), 4-layer authority | No publication boundary defined |
| **Retention** | Not explicitly modeled | DB migrations for archive tracking | Source retention policies (28 sources) |
| **Evaluation** | Claim register validation, test suite (6 files) | Routing tests, provider tests, privacy tests (10 test files) | Tests (109), portability checks, parity report |
| **Operational complexity** | High (multi-stage pipeline, LLM cost, prompt management) | Very high (VPS, Discord, Scout, filter, claims governance) | Low (manual fetch, no automation, no LLM) |

### Two Useful Models

**BSDA = structured domain-record knowledge base:**
- Narrow domain (42 courses)
- Deep structure (claims with evidence, citation, confidence, status)
- LLM used for extraction/classification with deterministic guards
- Downstream consumers have known formats (Reddit post, HTML page)

**Idle Hacking KB = large unstructured-content knowledge base:**
- Broad domain (game chat, all topics)
- Shallow structure initially (filter routing, conversation units)
- LLM used for discovery and extraction with strict gatekeeping
- Authority model prevents LLM output becoming truth
- Internal-only KB, no public output

**SJC today resembles:** Neither fully. It has BSDA's aspiration for structured
records but without BSDA's provenance/validation. It has Idle Hacking's internal-
only posture but without the authority layers. SJC's sources are more structured
than either (government HTML/PDF), making it a hybrid candidate.

**SJC should grow toward:** A hybrid. Structured source → intel item → claim register
(like BSDA) for publication-quality output. Entity registry + ontology (like Idle
Hacking) for search, alerts, and relationships. 4-layer authority (like Idle Hacking)
to gate LLM stages safely.

---

## Section 4 — SJC Comparison with BSDA and Idle Hacking

| SJC Concept | BSDA Analogue | File | Mature? | Idle Hacking Analogue | File | Mature? | What SJC Can Adopt |
|------------|--------------|------|---------|----------------------|------|---------|-------------------|
| **Source** | External Reddit DB | `$WGU_REDDIT_DB_PATH` env | Live | Source registry + channels | `data/registry/source_registry.csv` | Live | Track source health, capture method, trust role |
| **Source event** | Pipeline run id + manifest | `scripts/orchestrate.py` (run_id) | Live | Ingest runs tracking | `db/migrations/003_ingest.sql` | Draft | Enrich source_event with run_id, health |
| **Intel item** | Pipeline stage output | Per-stage output JSONL | Live | Clean_post | `data/derived/chat_pipeline/clean_posts/` | Live | Keep as primary ingestion record |
| **Claim (intel-level)** | Claim register | `scripts/build_claim_register.py` | **Live** | Accepted claim | `data/kb/accepted_claims/schema_v1.json` | **Live** | Add structured claim layer on top of intel items |
| **Entity** | Course code, source ID | Pipeline config | Draft | Game_elements registry | `data/registry/game_elements/registry_v1.json` | **Live** | Expand tracked_entities with aliases, types, evidence |
| **Topic** | Course sections (taxonomy gate) | `ops/taxonomy_gate.csv` | Live | KB taxonomy (13 sections) | `data/kb_taxonomy_v1.md` | Draft | Keep deterministic topic taxonomy, refine with LLM |
| **Location** | Not modeled | — | — | Not explicitly modeled (channel-based) | — | — | Add geographic model (parcel, lat/lng, district) |
| **Community** | Not applicable | — | — | Not applicable | — | — | Keep community registry, link to geography |
| **Development/Project** | Not modeled | — | — | Not modeled | — | — | New concept — needs entity + milestone model |
| **Event/Milestone** | Stage 5 trace | `scripts/build_trace.py` | Live | Not explicitly modeled | — | — | Extract from intel items, link to timeline |
| **Claim/Fact** | Claim register claim | `scripts/build_claim_register.py` | **Live** | Accepted claim | `data/kb/accepted_claims/` | **Live** | Most important SJC adoption target |
| **Relationship** | Claim→evidence→citation | `scripts/render_citations.py` | Live | Claim→evidence (anchor) | `data/kb/accepted_claims/schema_v1.json` | Live | Add explicit relationship linking between items |
| **Provenance** | SHA-256 hashes, run IDs | `scripts/build_claim_register.py` | Live | Run metadata, source registry | `scripts/llm/run_metadata.py`, `data/registry/source_registry.csv` | Live | Add provenance to every stage |
| **Review decision** | HITL points, validation script | `scripts/validate_claim_register.py` | **Live** | Outbox packets, Buddy approval | `docs/filter-learning/operating-process.md` | **Live** | Formalize review with typed decisions |
| **Publication state** | `publication_status` enum, `excluded_from_public_post` | `scripts/build_claim_register.py` | **Live** | Not published externally | — | — | Add publication status to queue + item |
| **User interest** | Course codes (implicit) | — | — | Filter area routing | `guide_area_filters_v1.json` | **Live** | Expand interest filters into user-interest model |
| **Alert rule** | Not modeled | — | — | Not modeled | — | — | New concept — needs subscription model |
| **Newsletter item** | Reddit post (one output) | `scripts/build_publishable_guides.py` | Live | Not modeled | — | — | Structured digest from approved items |
| **Social post** | Reddit post (target output) | `PIPELINE_SPEC.md` | Live | Not modeled | — | — | Downstream rendering from claim register |
| **Snapshot** | Pipeline manifest + run log | `scripts/orchestrate.py` (manifest) | Live | Filter run sidecars + annotation sets | `data/derived/outputs/<date>/<run_id>/` | Live | Enrich metric snapshots with stage granularity |
| **Query result** | Per-course citation index | `scripts/render_citations.py` | Live | `scripts/search_kb_evidence.py` | `scripts/search_kb_evidence.py` | Draft | Build multi-filter search from structured fields |
| **LLM run** | Pipeline run with LLM decision | `scripts/orchestrate.py` | **Live** | Scout attempt + run metadata | `scripts/kb_agents/scout.py`, `scripts/llm/run_metadata.py` | **Live** | Add LLM stage runner + metadata tracking |
| **Model output** | Structured JSON with schema | `scripts/llm_provider.py` | **Live** | Scout output with validation | `scripts/kb_agents/scout.py` (validate_payload) | **Live** | Structured output with validation, not free text |
| **Evaluation record** | Claim validation report | `scripts/validate_claim_register.py` | Live | Routing regression fixtures | `data/registry/topic_filters/regressions.jsonl` | Draft | Add evaluation fixtures for every LLM+deterministic stage |

---

## Section 5 — Knowledge-Base Design Options for SJC

### Option A — Intel-Item-Centered (Closest to Current)

**Model:** Intel items remain the primary canonical record. Entities, topics,
locations, and claims are linked fields or supporting registries.

**Architecture:**
```
source → source_event → intel_item
  ├── tracked_entity_ids[], topics[], communities[] (flat arrays)
  ├── review_queue_entry (review state)
  └── dedupe_key (identity)
```

**BSDA pattern support:** Minimal — BSDA uses claim registers, not raw items.
**Idle Hacking pattern support:** Moderate — clean_post concept is analogous.

**Strengths:**
- Simplicity — current schema works, minimal migration
- Extensible — add fields without restructuring
- Supports existing review queue and dedupe

**Weaknesses:**
- No structured claims — intel items mix detection, classification, and publishing
- Flat arrays prevent relational queries ("all items about SilverLeaf AND road projects")
- Entity/location/topic resolution requires string parsing
- Timeline support requires scanning all items

**Search capability:** Limited to field matching + keyword scan. No relational queries.

**Timeline support:** Manual — requires scanning all items by date.

**Alert matching:** Current interest filter model (keywords). Only "contains" matching.

**Newsletter/social support:** Generates from raw items — needs summary/curation layer.

**Best for:** Quick wins, simple browse-by-date website, email with keyword alerts.

### Option B — Event-Centered

**Model:** Source material produces structured local events or milestones.
Intel items become evidence or summaries attached to events.

**Architecture:**
```
source → source_event → [milestone/event]
  ├── intel_item (as evidence/context)
  ├── timeline position
  └── relationships to other events
```

**BSDA pattern support:** Strong — BSDA's citation resolution maps evidence to claims
(analogous to intel items→events).

**Idle Hacking pattern support:** None — Idle Hacking doesn't use event/timeline model.

**Strengths:**
- Natural timeline support
- Cross-source linking (BCC decision + NBOR notice + news article → one event)
- Project lifecycle tracking (proposed→approved→built→opened)
- Rich alert triggers ("this event changed status")

**Weaknesses:**
- New concept — no current schema support
- Event extraction from structured text is non-trivial (LLM likely needed)
- Migration from flat items to event-linked items
- Duplicate event detection (same project mentioned in multiple sources)

**Search capability:** Event-centric search (by project, date, status, type).

**Timeline support:** Native — events have dates, status changes, milestones.

**Alert matching:** Event status changes → natural alert trigger.

**Newsletter/social support:** Event summaries + attached intel items.

**Best for:** Project tracking, development timelines, "what happened this week" summaries.

### Option C — Fact/Claim-Centered (BSDA-Inspired)

**Model:** Source material produces structured claims/facts backed by evidence
(intel items). Entities, locations, events are linked from claims.

**Architecture:**
```
source → source_event → intel_item → claim/fact
  ├── evidence refs to intel items
  ├── status (publishable/caveat/hold/reject)
  ├── confidence (high/medium/low)
  ├── entity assertions
  ├── location assertions
  └── temporal assertions
```

**BSDA pattern support:** Direct match — this is exactly BSDA's model.
**Idle Hacking pattern support:** Strong — accepted claims governance matches.

**Strengths:**
- Precision — every claim is traceable to evidence
- Provenance — source URLs, timestamps, extraction method per claim
- Cross-source comparison ("BCC says X, NBOR says Y, St. Johns Citizen says Z")
- Question answering — claims are queryable facts
- Publication quality — status/confidence/caveats gate output

**Weaknesses:**
- Highest complexity — requires claim extraction (LLM likely needed)
- Review burden — each claim needs human verification
- Evidence ID management — BSDA's section-local IDs are fragile
- Claim extraction from structured government text may be LLM-overkill

**Search capability:** Rich — filter by entity, location, topic, status, confidence, date.

**Timeline support:** Via temporal assertions on claims.

**Alert matching:** Claim status change → natural alert.

**Newsletter/social support:** Claims + caveats → precise output.

**Best for:** Knowledge base, question answering, cross-source investigation, public accountability.

### Option D — Hybrid (Recommended)

**Model:** Intel items as primary ingestion records. Claim register (Option C) as
derived layer for structured, publishable output. Event/milestone extraction
(Option B) as intermediate layer for timelines and projects. Entity registry
(Idle Hacking style) for search, alerts, and relationships.

**Architecture:**
```
source → source_event → intel_item
  ├── entity registry (expanded tracked_entities)
  ├── location model (parcel, lat/lng, district)
  ├── topic model (hierarchical)
  │
  ├──→ milestone/event extraction [LLM optional]
  │     └── timeline, project lifecycle
  │
  ├──→ claim extraction [LLM]
  │     ├── structured claim register
  │     ├── evidence refs → intel items
  │     ├── publication status
  │     └── caveats, confidence
  │
  └──→ review queue
        └──→ approved items → downstream consumers
              ├── website (browse, search, entity pages)
              ├── alerts (user interest + entity + topic)
              ├── email reports (daily/weekly/neighborhood)
              ├── social drafts (from approved claims)
              └── API
```

**Pattern support:**
- **BSDA:** Claim register, citation resolution, pipeline stages, validation
- **Idle Hacking:** Entity registry with anchor-safety, accepted claims governance,
  4-layer authority, review gate staging

**Migration complexity:** Medium — add layers incrementally without restructuring
existing data.

### Recommendation

**Start with Option A (intel-item-centered) + claim register layer (from Option C).**
This preserves all existing data and workflow while adding structured output
capability. Add Option B's event/milestone model later for timeline features.

The claim register layer is the single most important addition because it:
1. Gives SJC publication-quality structured data
2. Provides the evidence→source traceability BSDA proves is essential
3. Creates the right abstraction boundary between "what we found" and "what we publish"
4. Enables multi-source claim comparison ("official records say X, news says Y")
5. Maps directly to downstream products (website, alerts, social, email)

---

## Section 6 — Search and Interest-Based Querying

### 6.1 Required Queries and Current Support

| Query | Current SJC Support | Structured Fields Needed | Deterministic? | DB Query Type |
|-------|--------------------|------------------------|----------------|---------------|
| "Updates about my neighborhood" | Community name in YAML | `communities[]` on item | Yes | Relational (filter by community) |
| "Road projects near me" | Beat/interest tag, no geo | Lat/lng or parcel on item | Yes | Geospatial (point-in-polygon) |
| "School-related developments" | Topic filter + beat | `topics[]` + `communities[]` | Yes | Relational (topic + community) |
| "Changes involving SilverLeaf" | Tracked entity match | `entity_ids[]` on item | Yes | Relational (entity join) |
| "County decisions about utilities" | Beat + interest filter | `topics[]` + `interest_tags[]` | Yes | Relational (multi-filter) |
| "Items mentioning a developer" | Not extracted | `extracted_entities[]` | LLM needed | Full-text + entity join |
| "Recent items about traffic + safety" | Multiple filter tags | `interest_tags[]` + `topics[]` | Yes | Relational (multi-filter) |
| "Weekly changes since my last digest" | Date filter | `discovered_at` | Yes | Date-range query |
| "Timeline for SR 207 WRF" | Tracked entity + date | Entity ID + date | Yes | Relational timeline |
| "Official records vs news on same issue" | Not linked | Claim linking, source_type | LLM needed | Multi-source join |

### 6.2 Structured Fields Needed

**Must have for basic search:**
- `communities[]` — already exists
- `topics[]` — already exists
- `interest_tags[]` — already exists
- `entity_ids[]` — exists as `tracked_entity_ids[]`
- `discovered_at` — already exists
- `source_id` — already exists
- `review_status` — already exists

**Should have for rich search:**
- `geographic_scope` — exists, but needs lat/lng or GeoJSON
- `extracted_entities[]` — LLM-extracted people, organizations, addresses
- `claim_status` — publication readiness (new field)
- `event_links[]` — related event IDs (new concept)
- `milestone_date` — specific event date (vs discovered_at)

**Nice to have for advanced:**
- `parcel_id` — county parcel number
- `lat_lng` — coordinate point
- `developer` — extracted developer/contractor name
- `contract_amount` — dollar amount from notices
- `hearing_date` — public hearing date from notice

### 6.3 Query Layers

| Layer | Technology | When | What It Handles |
|-------|-----------|------|-----------------|
| **1. Deterministic filters** | PostgreSQL WHERE clauses | Now | community, topic, source, date, entity, status |
| **2. Full-text search** | PostgreSQL `to_tsvector`/`to_tsquery` or MeiliSearch | Near future | title, summary, raw_excerpt keyword search |
| **3. Relational queries** | PostgreSQL JOINs | Now—soon | entity→item, community→item, topic→item |
| **4. Geospatial queries** | PostGIS or GeoDjango | Later | "within 5 miles of this address", "in this district" |
| **5. Semantic retrieval** | Embeddings + vector search | Future | "things like...", concept similarity |
| **6. LLM query interpretation** | Natural language → structured query | Future | "What's happening with Publix in SilverLeaf?" |

### 6.4 Necessary Now vs Later

**Now (deterministic):**
- Community filter
- Topic filter
- Source filter
- Date range filter
- Entity filter (tracked_entities)
- Status filter (review_status)

**Soon (relational + FTS):**
- Full-text search across title, summary, raw_excerpt
- Multi-topic OR/AND queries
- Combined community + topic + date queries
- Entity + date timeline queries

**Later (geospatial + semantic):**
- Proximity search ("near my address")
- Semantic similarity ("show me things like...")
- LLM natural language → query

---

## Section 7 — LLM Strategy for SJC

### 7.1 Stage-by-Stage Assessment

| Stage | Useful? | Deterministic First? | Input | Output | Validation | Review? | Cost/Volume |
|-------|---------|---------------------|-------|--------|------------|---------|-------------|
| **Relevance classification** | Yes | Current keyword rules catch exact codes but miss context | Title + summary + raw_excerpt | Topic list + confidence | Sample comparison vs current | Medium | Low (~80 items/month) |
| **Entity extraction** | **High** | Current label/alias substring misses partials | Full item text | Entity IDs with confidence | Required — false positive rate | Medium | Low |
| **Entity resolution** | Medium | Aliases in registry are manual | Extracted entities | Resolved entity IDs | Required — merging | High | Low |
| **Topic tagging** | Low | 24 topics are well-covered by source-based rules | Title + summary | Refined topic list | Sample comparison | Low | Low |
| **Location extraction** | **High** | No location extraction exists at all | Full item text + address snippets | Normalized address + lat/lng | Required — compare to known places | Low | Low |
| **Event extraction** | **High** | Not done — dates are in text but not extracted | Full item text + date fields | Event records with date + type + participants | Required — cross-reference | Medium | Low |
| **Milestone extraction** | Medium | Tracked_entity lifecycle is manual | Series of related items | Status change events | Required — timeline review | High | Very low |
| **Relationship linking** | **High** | No cross-source linking exists | Two or more intel items | Relationship type + confidence | Required — sample review | High | Low |
| **Claim/fact extraction** | **High** | Not done — BSDA model proves value | One intel item | Structured claim with evidence refs | Required — claim register validation | **High** | Medium |
| **Near-duplicate detection** | Medium | Exact dedupe only, SHA-256 | Two items | Near-duplicate score | Required — thresholds need tuning | Medium | Low |
| **Article↔official record linking** | **High** | Not done | News article + official item | Link with relationship type | Required — cross-reference | High | Very low |
| **Impact/audience classification** | Low | Rules already produce adequate audiences | Item text | Audience list | Sample comparison | Low | Very low |
| **Digest generation** | **High** | Not done — needs LLM | Approved items from period | Structured digest text | HITL before send | **High** | Low (weekly) |
| **Social post drafting** | Medium | Not done | Approved claim/item | Social post draft | HITL before send | **High** | Very low |
| **Question answering** | Future | Not designed yet | KB records + question | Answer with evidence refs | Required — answerability gate | **High** | N/A |
| **User-interest matching** | Low | Current keyword filters cover basics | User prefs + new items | Matched items | Background, no review | None | High volume |

### 7.2 Recommended First LLM Stages

**Phase 1 — Entity extraction:**
- Extract named entities (people, organizations, addresses, project names) from
  existing 132 intel items
- Verify against known tracked_entities and community names
- Provenance: record model, prompt version, extracted entities per item
- Use BSDA's `run_metadata.py` pattern for tracking

**Phase 2 — Claim/fact extraction:**
- Extract structured claims from NBOR, BCC, and county news items
- Modeled on BSDA's claim register: claim_text, evidence_refs, confidence, status
- Human review of all claims before any publication
- Provenance: evidence IDs trackable to specific intel items

**Phase 3 — Relationship linking:**
- Link items across sources about the same project/event
- BCC agenda item + NBOR notice + news article about same rezoning → linked
- Store relationships in link table (PG `intel_item_tracked_entities` plus
  new `intel_item_relationships`)

### 7.3 Deterministic Parsing: Stay Deterministic

The following should remain deterministic (no LLM):

- **NBOR table extraction** — ASP.NET generates clean HTML tables. BSDA's approach
  of structured data extraction would be LLM-overkill.
- **BCC agenda PDF extraction** — pypdf + regex works. The section structure and
  numbered items are predictable. BSDA's relevance stage would be over-engineering.
- **Deduplication** — Exact SHA-256 dedupe is correct. Near-duplicate can add LLM
  later if needed.
- **Source health checking** — Simple HTTP HEAD/GET. No LLM.
- **Classification of official source types** — Source type is known from registry.
  No LLM needed.

### 7.4 Privacy and Copyright Concerns

- **Official government records:** Public domain. No copyright concern. Can be
  reproduced freely.
- **St. Johns Citizen articles:** Copyrighted. Excerpts only, with citation.
  This is what SJC's `raw_excerpt` and `citation` fields already support.
- **LLM extracts from news:** Using an LLM to extract claims from news articles
  could raise copyright concerns if substantial portions are reproduced.
  Keep extracts to facts only (rezoning approved, road closed, meeting scheduled)
  rather than article prose.
- **Privacy:** No PII should be extracted. Idle Hacking's `privacy.py` classification
  can inform SJC's privacy boundary. Police reports and arrest records need special
  handling (already SJC `human_review_required` flag).

### 7.5 Local Model Baseline

For entity extraction and claim extraction, a local model (Ollama) is realistic:
- Volume: ~80 new intel items/month initially, ~1000/month at scale
- Cost: $0 (local) vs ~$0.50/month cloud for current volume
- Latency: Entity extraction on a short text item is fast locally
- Quality: Structured JSON extraction is one of the tasks local models handle well

BSDA's `OllamaClient` and Idle Hacking's `fixture_provider.py` provide the
abstraction to switch providers without code changes.

---

## Section 8 — Downstream Product Model

### 8.1 Minimum Structured Data Per Product

| Product | Items | Entities | Locations | Claims | Dates | Review Status | User Interests |
|---------|-------|----------|-----------|--------|-------|---------------|----------------|
| **Public website — browse** | Required | Nice | Nice | Optional | Required | Required (approved only) | N/A |
| **Public website — search** | Required | Required | Required | Optional | Required | Required | N/A |
| **Public website — map** | Required | Nice | **Required** | Optional | Required | Required | N/A |
| **Public website — entity pages** | Required | **Required** | Nice | Optional | Required | Required | N/A |
| **Public website — timelines** | Required | Required | Nice | Optional | **Required** | Required | N/A |
| **Alerts — topic** | Required | N/A | N/A | N/A | Required | Required | **Required** |
| **Alerts — entity** | Required | **Required** | N/A | N/A | Required | Required | **Required** |
| **Alerts — location** | Required | N/A | **Required** | N/A | Required | Required | **Required** |
| **Email — daily** | Required | Nice | Nice | Optional | Required (since last) | Required | **Required** |
| **Email — weekly** | Required | Nice | Nice | Optional | Required (since last) | Required | **Required** |
| **Email — neighborhood** | Required | Nice | **Required** | Optional | Required | Required | **Required** |
| **Social posts** | Optional | Nice | Nice | **Required** | Nice | **Required (approved)** | N/A |
| **Reviewer UI** | **Required** | Required | Nice | Required | Required | **Required (all statuses)** | N/A |
| **API — search** | Required | Required | Required | Optional | Required | Required | N/A |
| **API — alerts** | Required | Required | Required | Optional | Required | Required | **Required** |
| **API — metrics** | Aggregate | Aggregate | N/A | N/A | Aggregate | Aggregate | N/A |

### 8.2 Product Priorities

Based on SJC's current state (no output, 132 items), the minimum viable output is:

1. **Flat public feed** (browse by date, filter by topic/source) — needs only
   current fields + a simple web server
2. **Entity pages** (browse by tracked entity) — needs entity→item linking
   (already done in queue builder, needs web rendering)
3. **Neighborhood pages** (browse by community) — needs community filter
   (already in schema)
4. **Simple email report** (weekly digest of approved items) — needs digest
   builder + mailer

---

## Section 9 — Candidate SJC Canonical Concepts

| Concept | Represents | Why | Use Cases | Already Present? | BSDA Analogue | Idle Hacking Analogue | Priority |
|---------|-----------|-----|-----------|-----------------|--------------|----------------------|----------|
| **Source** | A monitored public information channel | Foundation entity | All | ✅ `registry/sources.yaml` | External DB reference | Source registry + channels | **First-class** |
| **Source event** | One fetch/occurrence of a source | Fetch provenance | Provenance, health | Partial `data/source_events/` | Pipeline run ID | Ingest run | **First-class** |
| **Source document** | One raw document (HTML page, PDF) | Raw evidence capture | Retention, audit | Schema only (`raw_artifact_records`) | Raw Reddit post | Raw chat JSONL | **Deferred** |
| **Intel item** | One resident-impact finding | Primary atomic record | All core operations | ✅ `data/intel_items/` | Pipeline stage output | Clean_post | **First-class** |
| **Claim** | One structured fact extracted from evidence | Publication-quality truth | KB, search, social, Q&A | ❌ | **Claim register** | **Accepted claim** | **Add now** |
| **Entity** | One durable thing (project, school, road, org) | Cross-item grouping | Entity pages, alerts, timelines | ✅ `registry/tracked_entities.yaml` | Course code, source ID | Game_elements registry | **First-class** |
| **Entity alias** | Alternative name for entity | Matching flexibility | Search, entity linking | ✅ Within entity record | — | term_aliases.csv | **First-class** |
| **Location** | One geographic point or area | Map, proximity, neighborhood filter | Website map, alerts | ❌ Flat field only | — | — | **Add now** |
| **Geographic area** | One named area (community, corridor, district) | High-level geography | Browse filters, reports | ✅ `registry/communities.yaml` | — | Channel-based scope | **First-class** |
| **Topic** | One subject category | Organization | Browse, filter, alerts | ✅ `docs/taxonomy.md` (24 topics) | Course sections | KB taxonomy (13) | **First-class** |
| **Interest tag** | One reason a resident cares | Alert/relevance matching | User interest matching | ✅ `docs/taxonomy.md` (10 tags) | — | Filter area routing | **First-class** |
| **Event** | One happens-on-a-date occurrence | Timeline, calendar | Project tracking, newsletters | ❌ | Milestone/trace | — | **Deferred** |
| **Milestone** | One lifecycle status change for an entity | Status-aware entity tracking | Project updates, alerts | ❌ | Claim revision trace | Claim versioning | **Deferred** |
| **Relationship** | One link between two records | Cross-source linking | Knowledge graph, related items | ❌ Inferred only | Claim→evidence links | Claim→evidence anchors | **Add now** |
| **Provenance record** | One capture of how/when/who produced a record | Audit trail | All | ❌ Partial (dedupe key) | SHA-256 hashes, run IDs | Run metadata, source registry | **Add now** |
| **Review decision** | One human review outcome with note | Quality gate | Publication, corrections | ✅ Flat `review_status` | Validation + HITL | Outbox packet approval | **First-class** |
| **Publication** | One release of an item to a channel | Distribution tracking | All output | ❌ Field exists, no workflow | Reddit post, HTML page | Not published externally | **Add now** |
| **User interest** | One user's preference topic/entity/location | Personalization | Alerts, reports, feed | ❌ | — | Filter area (implicit) | **Add now** |
| **Subscription** | One user's alert subscription | Delivery management | Email, alerts | ❌ | — | — | **Deferred** |
| **Delivery** | One sent notification/email | Send tracking | Email reports, alerts | ❌ | Reddit post (target) | — | **Deferred** |
| **Snapshot** | One capture of aggregate metrics at a point | Dashboard, trend | Status pages, ops | ✅ `app.metric_snapshots` | Pipeline manifest | Filter run sidecar | **First-class** |
| **LLM run** | One LLM execution with metadata | Inference provenance | Audit, cost, debugging | ❌ | Orchestrate run | Scout attempt | **Add now** |
| **Evaluation record** | One evaluation of a pipeline stage | Quality measurement | Iteration, regression | ❌ | Claim register validation | Regression fixtures | **Deferred** |

---

## Section 10 — Complexity Controls

### 10.1 Patterns Worth Adopting Now

| Pattern | Source | Complexity | Effort | Benefit |
|---------|--------|-----------|--------|---------|
| **Claim register model** | BSDA | Medium | 2 sessions | Structured output, provenance, publication gating |
| **LLM run metadata** | Idle Hacking | Low | 1 session | Audit trail for all LLM stages |
| **Provenance hashing** | BSDA | Low | 0.5 session | Trace inputs to outputs |
| **4-layer authority model** | Idle Hacking | Conceptual | 0.5 session (doc) | Prevent LLM auto-promotion |
| **Entity registry expansion** | Idle Hacking | Low | 1 session | Better entity search + alerts |
| **Structured LLM output validation** | BSDA | Medium | 1 session | Verify all LLM output against schema |
| **Stage gating** | BSDA | Low | 0.5 session | `--llm-decision` patterns |

### 10.2 Patterns Worth Designing For But Deferring

| Pattern | Source | Why Defer |
|---------|--------|-----------|
| **Accepted claims governance** (versioning, staleness) | Idle Hacking | Needs user-facing KB first |
| **Pipeline orchestrator** | BSDA | Only needed at 5+ LLM stages |
| **Multi-provider LLM abstraction** | BSDA, Idle Hacking | Start with one provider (opencode-go) |
| **Geospatial model** | — | Needs PostGIS setup and parcel data |
| **Semantic search (embeddings)** | — | Needs working FTS + relational queries first |
| **Detector registry with regression fixtures** | Idle Hacking | Only needed when filter rules become complex |
| **Scout-style conversation-unit discovery** | Idle Hacking | Not applicable (SJC sources are structured, not chat) |

### 10.3 Patterns That Would Be Premature

| Pattern | Source | Why Premature |
|---------|--------|---------------|
| **Vector database (pgvector, Pinecone)** | — | Relational + FTS is sufficient for SJC's volume |
| **Graph database (Neo4j)** | — | PG link tables handle SJC's relationship complexity |
| **Generic agent framework** | — | Single-purpose scripts are simpler and more reliable |
| **Full event sourcing** | — | Append-only logs add complexity without proportional benefit |
| **Over-generalized ontology** | — | SJC's domain is bounded; 24 topics + 20 communities is enough |
| **Provider-heavy LLM abstraction** | BSDA, Idle Hacking | Start with 1-2 providers; add abstraction when migration is needed |
| **Storing every raw artifact** | — | Not authorized; `raw_artifact_records` stores hashes only |

### 10.4 What PostgreSQL Can Support Adequately

Before adding another major system, PostgreSQL 16 can handle:

- **Full-text search** — `to_tsvector`/`to_tsquery` with `ts_rank` ranking.
  Good enough for SJC's document volume (100s-1000s, not 100Ks).
- **Relational queries** — JOINs across items, entities, topics, communities.
  The link tables already exist (migration 006), they're just empty.
- **JSON queries** — `jsonb` fields for flexible metadata.
- **Array queries** — `@>` for array containment (all items tagged `[development, transportation]`).
- **Geospatial** — PostGIS extension adds point-in-polygon and proximity queries.
  Install once, use indefinitely.
- **Time-series** — Metric snapshots with `date` + `grain` + `metric_name` indexing.

Reserve vector databases, graph databases, and specialized search engines for
when SJC exceeds what PG can handle (unlikely at projected volume).

---

## Section 11 — Recommended Discussion Sequence

Buddy and ChatGPT should discuss in this order:

### Step 1: Choose the Core Knowledge Object

**Question:** Should SJC's canonical record be the current intel item, or should
it also include a structured claim register (like BSDA)?

**Options:**
- Stay intel-item-centered (simpler, current data works)
- Add claim register layer (structured output, provenance, publication gating)
- Both: intel items as ingestion, claims as derived output

**Recommendation:** Both. Keep intel items for internal operations (fetching,
dedup, review). Add claim register for publication.

### Step 2: Define Canonical Entities and Relationships

**Question:** What entities need dedicated models beyond the current 11 tracked
entities?

**Key questions:**
- Should every development project be tracked, or only high-profile ones?
- Should people (officials, developers, speakers) be extracted and tracked?
- Should organizations (CDDs, HOAs, developers, contractors) be extracted?
- What is the threshold for creating a new entity?

### Step 3: Define Location and Geography Model

**Question:** What geographic detail does SJC need?

**Options:**
- Community name only (current — `["silverleaf", "nocatee"]`)
- Add district/county commission district
- Add parcel ID and lat/lng
- Full PostGIS geospatial model

**Key constraint:** NBOR notices include district and sometimes addresses.
BCC items are county-wide. News items may include specific locations.
The extraction effort varies.

### Step 4: Define User-Interest Model

**Question:** How should user interests be represented?

**Current:** Interest filters (keyword-based, no user model).

**Options:**
- Community-based ("show me SilverLeaf updates")
- Topic-based ("show me transportation items")
- Entity-based ("track SilverLeaf Publix")
- Keyword-based ("find items about traffic")
- Complex queries ("SilverLeaf AND transportation NOT routine")

### Step 5: Define Review and Publication Boundary

**Question:** What items can be published automatically vs require human review?

**Key decisions:**
- Is "source_confirmed" from official sources sufficient for auto-publication?
- What sensitivity levels require human review?
- Who is the reviewer? How is review tracked?
- What is the corrections process?

### Step 6: Define Downstream Products

**Question:** What is the first public-facing product?

**Options:**
- Simple public feed (browse by date, filter by topic/source)
- Entity pages (one page per tracked entity with related items)
- Neighborhood pages (one page per community)
- Weekly email digest
- Social media posts
- Map-based view

**Recommendation:** Public feed first (simplest, demonstrates value), then entity
pages, then email digest.

### Step 7: Define Required LLM Stages

**Question:** Which LLM stages should be implemented first?

**Recommendation:** Entity extraction, then claim extraction, then relationship
linking. Keep NBOR and BCC deterministic.

### Step 8: Define Search and Retrieval

**Question:** What search capability is needed at launch?

**Recommendation:** Deterministic filters (community, topic, source, date, entity,
status) first. Full-text search second. Geospatial third.

### Step 9: Define Retention

**Question:** What is the retention policy for raw data, intermediate artifacts,
snapshots, and published records?

**Current:** 28-source retention policy exists in `docs/retention.md` but no
pruning has been executed.

### Step 10: Define Phased Implementation

**Question:** What is the implementation sequence?

**Recommendation:**
1. Claim register layer (2 sessions)
2. Expand entity registry (1 session)
3. LLM entity extraction (2 sessions)
4. Simple public feed website (2 sessions)
5. Entity pages + neighborhood pages (1 session)
6. LLM claim extraction (3 sessions)
7. Weekly email digest (2 sessions)
8. Search (full-text + filters, 1 session)
9. User interests and alerts (3 sessions)
10. Near-duplicate and relationship linking (2 sessions)

---

## Section 12 — Questions for Buddy

### Product Questions
1. What is the first public-facing product you want to ship?
2. Is SJC intended to be free, subscriber-supported, or ad-supported?
3. Should entities include people (officials, developers), or stay project-focused?
4. What is your comfort level with auto-publishing official government records?
5. Do you want a newsletter before or after a website?

### Data Model Questions
6. Should SJC adopt a claim register model (like BSDA) as the publication layer?
7. What geographic model is sufficient for launch? (community names only, or lat/lng?)
8. Should locations include parcel IDs from the Property Appraiser?
9. How many entities should we support? An upper bound?

### LLM Questions
10. Which LLM stage should be implemented first?
11. What is your budget for LLM API costs?
12. Are you comfortable with a local model baseline (Ollama) for extraction?
13. Should we adopt the BSDA `--llm-decision` pattern for staged model escalation?

### Operational Questions
14. When should the PostgreSQL cutover occur?
15. Who will review and approve items for publication?
16. Should the first website be static (GitHub Pages) or dynamic (VPS-hosted)?
17. What is the retention target for raw artifacts?

---

## Section 13 — Recommended Next Planning Prompt

If Buddy wants to proceed with the first implementation phase, the recommended
Codex prompt focus is:

1. Add a claim register layer to the intel item schema
2. Expand tracked_entities with entity_type hierarchy, aliases, evidence refs
3. Build a deterministic entity extraction pass over existing 132 items
4. Build a simple public feed website from approved intel items
5. Add LLM run metadata tracking

This gives SJC:
- Publication-quality structured output (claims)
- Better entity search and linking
- A working website for the first time
- Provenance infrastructure for future LLM stages

---

## Section 14 — Chat Summary

- **Best reusable BSDA pattern:** Claim register (`scripts/build_claim_register.py`)
  — structured claims with publication status, evidence refs, confidence, and
  gate diagnostics. Directly applicable to SJC's need for publication-quality output.

- **Best reusable Idle Hacking pattern:** 4-layer authority model (`spec-july-1.md`,
  `docs/ontology-routing-authority-stack.md`) — Evidence→Understanding→Derived→Authority
  prevents LLM auto-promotion. SJC needs this before any LLM stage goes live.

- **Biggest SJC knowledge-model gap:** No structured claim/fact layer. Intel items
  are optimized for internal operations (fetching, dedup, review), not for
  publication, search, or cross-source comparison. Adding a claim register
  (like BSDA) with evidence refs, publication status, and confidence solves this.

- **Most useful first LLM stage:** Entity extraction. Current keyword-based entity
  matching misses partial names, abbreviations, and context. LLM can extract
  named entities (organizations, people, project names, addresses) from item text
  with far better recall. Cheap, fast, and non-controversial.

- **Strongest recommended SJC design option:** Hybrid (Option D) — intel items
  as primary ingestion, claim register as structured output layer, entity registry
  (expanded from current 11) for search and linking. Start by adding the claim
  register layer (2 sessions), then expand entities (1 session).

- **Largest overengineering risk:** Adding a vector database, graph database, or
  generic agent framework before SJC has basic relational queries working.
  PostgreSQL (with FTS and JSON support) can handle SJC's projected volume for
  years. Reserve vector search for when semantic retrieval is actually needed.

- **Report file created:** `docs/reviews/SJC_KNOWLEDGE_BASE_CROSS_PROJECT_COMPARISON_20260706.md`

- **Commit created:** `docs: add SJC knowledge base cross-project comparison report`

- **Repository status:** Clean. Only the new report file is untracked. No data
  files, scripts, schemas, or registries were modified in any repository.
