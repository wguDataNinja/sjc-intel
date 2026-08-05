# Weekly Operational Contract

**Status:** Authoritative supporting contract for the bounded weekly VPS/Hermes
operational workflow.
**Authority:** `ROADMAP.md` §§3E–3F, `VPS_ROADMAP.md`, `docs/VPS_CONTINUITY.md`.
**Owner:** Buddy for activation/policy decisions; implementation follows
approved task packets.
**Last reconciled:** 2026-08-03 (Tasks 12–13).
**Operator reference:** `docs/weekly_operator_guide.md` (commands).
**Candidate/proposal schemas:** `schemas/intel_candidate.schema.yaml`,
`schemas/source_proposal.schema.yaml`.

## 1. Purpose and boundary

This contract defines the bounded **weekly operational run** that a future
authorized VPS Hermes execution may perform:

```
weekly scheduled run on VPS
→ monitor approved canonical sources
→ run bounded discovery for potential new sources
→ produce intelligence candidates and source proposals
→ create a manifested transfer bundle
→ Mac pulls and verifies the bundle
→ Mac imports it without damaging review state
→ receipt and acknowledgement are recorded
→ VPS payload becomes eligible for delayed pruning
```

The weekly workflow **never**:

- publishes intelligence (no public output, no newsletter, no web release);
- promotes sources automatically (candidates stay in `source_proposals` only);
- removes canonical sources;
- changes taxonomy, search profiles, or permanent scope;
- treats social media as sole consequential evidence (corroboration only);
- bypasses human review (all candidates start `candidate`, and sensitive items
  are flagged `needs_review` for the Mac human pipeline).

The Mac file corpus remains the durable authority for corpus, review,
archive/restore, and static-release preparation. The VPS produces candidates
and operational evidence only.

## 2. Inputs

Each weekly run is bound by the following explicit inputs. The Hermes weekly
task (`prompts/sjc_weekly_ops_task.md`) supplies all of them at dispatch time;
the bundle manifest records the resolved values.

| Input | Source | Required? |
|-------|--------|-----------|
| Approved canonical source list | `registry/sources.yaml` (status `active` or `verified`, `monitor_frequency: weekly` or a Stage-A override) | Yes |
| Source registry revision | Git SHA of `registry/sources.yaml` at run start (see §5 registry pin) | Yes |
| Tracked entities | `registry/tracked_entities.yaml` | Yes |
| Search profiles | `registry/search_profiles.yaml` — discovery profile selection (default: `sl_core` + one bounded discovery pass) | Yes |
| Taxonomy / configuration revision | Git SHA of `docs/taxonomy.md` + `registry/interest_filters.yaml` at run start | Yes |
| Run time window | `window_start` / `window_end` (UTC). Sources fetched only inside this window. | Yes |
| Prior dedupe state | `data/index/prior_items.yaml` fingerprint set shipped to VPS in the deployment payload | Yes |
| Runtime budget | Explicit token/cost and wall-clock budget (see §8 runtime controls) | Yes |

### 2.1 Source registry pin

The run executes against the exact committed revision pinned in the deployment
payload (exact Git SHA). The `source_registry_revision` recorded in the bundle
manifest is the SHA of the pinned checkout, not the repository's latest HEAD.

## 3. Stage A — canonical-source monitoring

Stage A processes each approved canonical source in the run source list.

For each source the run produces:

| Output | Contents |
|--------|----------|
| Source-health result | HTTP status, fetch latency, accessible/unreachable, retry count, last error |
| Source event | Normalized `source_event` record (container for the fetch) |
| Normalized intelligence candidates | Structured candidate records following `schemas/intel_item.schema.yaml` (subset), marked `candidate` |
| Source URLs | Each candidate carries its original source URL |
| Evidence excerpts | Bounded `raw_excerpt` (first paragraph / key sentence only — never full article text) |
| Outcome classification | Each candidate is labeled `duplicate`, `no_match`, `partial`, or `failed` |
| Bounded raw captures | Only where a source type requires them (e.g. HTML fixtures); size-capped and listed in the manifest |

### 3.1 Candidate outcome labels

| Label | Meaning |
|-------|---------|
| `duplicate` | Matched prior dedupe state — not re-emitted as new |
| `no_match` | Not seen before — emitted as a candidate |
| `partial` | Partially extracted (e.g. missing date) — emitted with the missing field nulled and `partial` flag |
| `failed` | Extraction failed for a bounded reason — recorded in the failure summary, no candidate emitted |

### 3.2 Candidate contract

Candidates are **never** `verified`. Every candidate record carries:

- `item_id` candidate form `SJC-{prefix}-{YYYYMMDD}-{NNNN}`;
- `status: candidate`;
- `review_status: candidate` (distinct from the Mac corpus `pending_review`);
- all classification fields using `docs/taxonomy.md` controlled vocabulary;
- `source_url`, `source_published_at`, `discovered_at`, `raw_excerpt`;
- resident-interest layer (`primary_topic`, `interest_tags`,
  `resident_relevance`, `human_review_required`).

Sensitive items (public safety, legal, crime, schools, minors, controversy)
must set `human_review_required: true`. The VPS does not resolve sensitivity;
it flags.

## 4. Stage B — bounded source discovery

Stage B runs a single bounded discovery pass and may **propose only**. It
searches for:

- newly relevant public sources;
- missing source coverage (beats with no canonical source);
- moved or replaced sources (dead URLs, redirects, renamed pages);
- SilverLeaf-specific sources (community, development, retail, school, road,
  utility, government proximity);
- gaps involving schools, roads, utilities, development, government,
  communities, and tracked entities.

Discovery uses the search profile selected in the run inputs (default
`sl_core`) and the discovery constraints in `docs/discovery_loops.md`.

### 4.1 Source proposal contract

Each proposal includes:

| Field | Meaning |
|-------|---------|
| `proposal_id` | `PROP-{source_family}-{NNNN}` stable within the run |
| `source_name` | Human name |
| `url` | Proposed public URL |
| `source_family` | From `docs/taxonomy.md` source families |
| `authority_level` | `official` / `local_media` / `community` / `other` |
| `discovered_through` | Search profile, query, and fetch evidence |
| `evidence` | Excerpts / links that support relevance |
| `relevance_rationale` | Why residents care, tied to homeowner beats |
| `geographic_relevance` | Communities/geography affected |
| `coverage_gap_addressed` | Which beat/geography gap this fills |
| `recommended_disposition` | `propose` / `defer` / `reject` |
| `confidence` | `high` / `medium` / `low` |
| `review_status` | `candidate` (never `promoted`) |

### 4.2 Stage B prohibitions

The run must not:

- promote candidates into `registry/sources.yaml`;
- remove canonical sources;
- change taxonomy or permanent scope;
- publish intelligence;
- treat social media as sole consequential evidence.

## 5. Review boundary

The following separation is explicit and non-negotiable:

```
candidate intelligence ≠ verified intelligence
verified intelligence   ≠ published intelligence
source proposal         ≠ canonical source
```

- `candidate` (bundle) → only the Mac human review pipeline may turn a
  candidate into a corpus `intel_item` with `review_status: pending_review`.
- `verified` is a corpus review state and is never a publication authorization
  (`docs/publication_release_contract.md` §1).
- `source proposal` (bundle) → only Buddy-approved promotion may add a source
  to `registry/sources.yaml`.

## 6. Outputs

The run's sole durable artifact is the **transfer bundle** (§7). Inside the
bundle the artifact classes and proposed paths are:

| Class | Bundle path |
|-------|-------------|
| Run record | `run.json` |
| Source-health results | `source_health/{source_id}.json` |
| Source events | `source_events/{source_id}.json` |
| Intelligence candidates | `intel_candidates/{source_id}.json` |
| Source proposals | `source_proposals/proposals.json` |
| Bounded logs | `logs/run.log` |
| Manifest | `manifest.json` |
| Checksums | `checksums.sha256` |
| Failure summary | `run.json` → `failure_summary` block (also mirrored in `logs/run.log`) |

No files are written outside the bundle during a run. The VPS never touches
the Mac corpus paths (`data/intel_items/`, `data/review_queue/`,
`data/source_events/`, `data/index/`).

## 7. Transfer-bundle contract

### 7.1 Format and schema version

Bundle schema version: **`1.0`**. Layout is deterministic:

```
bundle/
  manifest.json          # authoritative index + metadata (§7.3)
  checksums.sha256       # sha256 per included file (including manifest.json)
  run.json               # run record (§7.4)
  source_health/         # {source_id}.json
  source_events/         # {source_id}.json
  intel_candidates/      # {source_id}.json
  source_proposals/      # proposals.json
  logs/                  # run.log
```

Only required artifacts are included. A run with zero candidates and zero
proposals still emits an empty `intel_candidates/` and `source_proposals/`
file so the bundle shape is stable.

### 7.2 Checksums

- Algorithm: SHA-256, hex lowercase.
- `checksums.sha256` format matches `sha256sum`: `<64-hex-hash>  <relative-path>`
  (two spaces), one line per included file, sorted by relative path.
- Every file listed in `manifest.included_files` must have an entry.
- `manifest.json` itself is included in `checksums.sha256` (so a modified
  manifest is detected). `checksums.sha256` is not itself checksummed.

### 7.3 manifest.json

| Field | Meaning |
|-------|---------|
| `bundle_schema_version` | `"1.0"` |
| `run_id` | `SJC-WK-{YYYYMMDD}-{NNNN}` |
| `producing_git_sha` | Pinned repository SHA executed |
| `producing_task_or_profile` | Hermes weekly task ID / run profile |
| `source_registry_revision` | §2.1 registry pin |
| `window_start` / `window_end` | Run time window (UTC) |
| `retention_deadline` | Earliest UTC time the bundle may be considered for pruning (default `window_end` + 14 days; prune still requires a verified receipt, §7.7) |
| `run_status` | `completed` / `completed_partial` / `failed` / `aborted` |
| `included_files` | `[{path, size_bytes, sha256}]`, sorted by path |
| `bundle_total_bytes` | Sum of `included_files.size_bytes` — byte-bounds evidence for Ivy admission |
| `candidate_counts` | `{per_source: new/duplicate/partial/failed}` |
| `failure_counts` | `{total, by_source, by_reason}` |
| `replay_identity` | `"1.0::{run_id}::{producing_git_sha}::" + source_registry_revision` |

`run_status` `failed` / `aborted` bundles carry a failure summary and are
still transferable for operator diagnosis; they are never eligible for import
into review state.

### 7.4 run.json

Carries the run record: `run_id`, `run_status`, `started_at`, `ended_at`,
`window_start`, `window_end`, `retention_deadline`, `profile_id`, source list
processed, counts, `failure_summary`, `replay_identity`, and
`next_check_after` (UTC).

### 7.5 Transfer semantics

| Concern | Behavior |
|---------|----------|
| Duplicate bundle | Import is keyed by `run_id`. A second transfer of the same `run_id` is idempotent: no re-import, no new review state, existing receipt returned. |
| Partial transfer | Any missing file, size mismatch, or checksum mismatch fails verification; import refuses. |
| Safe replay | Replay identity is stored in the receipt; replaying the same run restores the same staging copy with no corpus mutation. |
| Import failure | Bundle left in staging, no receipt emitted, no `LAST_RUN` advance, no prune. Failure is reported to the operator. |
| Mac-offline retention | VPS retains the bundle until it observes a valid receipt (see §7.7). No retention-based deletion until then. |
| Duplicate run_id, different content | Rejected as a conflict; operator investigates. |
| Unknown bundle schema version | Rejected; does not advance import. |

### 7.6 Import behavior (Mac)

Import is **staging-only** by default:

1. `bundle_verify` runs (checksums + manifest + run.json shape).
2. Bundle is copied to `data/incoming/{run_id}/` (idempotent).
3. A receipt is written to `data/receipts/{run_id}.receipt.json` only after
   full verification and a successful stage.
4. No authoritative corpus path is written. Converting candidates to
   `data/intel_items/` + review queue remains a separate, human-gated import
   step (a later medium-agent task, never automatic).

### 7.7 Acknowledgement and delayed pruning

Receipt format (`receipt_schema_version: "1.0"`):

| Field | Meaning |
|-------|---------|
| `receipt_id` | `RCP-{run_id}` |
| `run_id` | Source run |
| `bundle_sha256` | SHA-256 of the verified bundle (checksums file content) |
| `verified_files` | Count of files verified |
| `verified_checksums` | `true` |
| `imported_at` | UTC timestamp |
| `importing_git_sha` | Mac repository SHA at import time |
| `status` | `acknowledged` |

Pruning rules:

- A bundle is eligible for delayed prune **only** when the producer has
  observed a valid receipt whose `bundle_sha256` matches the produced bundle
  **and** the retention delay (default 14 days, configurable) has elapsed.
- Transfer initiation alone never authorizes pruning.
- Prune is executed by a separate authorized privileged action (§ privileged
  packet), never by the weekly run itself.

## 8. Runtime controls

| Control | Value / behavior |
|---------|------------------|
| Run ID | One run ID per window, `SJC-WK-{YYYYMMDD}-{NNNN}` |
| Writer | Exactly one scheduler/writer; lock before run (§ lock method in privileged packet) |
| Duplicate-run prevention | Run ID uniqueness + lock file + `run.json` presence check |
| Maximum runtime | Wall-clock budget (default 120 min, configurable) |
| Retry ceiling | Per-source fetch retries capped (default 2); never retries past the window end |
| Query/fetch ceiling | Max HTTP fetches per run (default 120); max candidates per source (default 50) |
| Token/cost ceiling | Agentic discovery is bounded by the run profile's `max_queries`/`max_results` and an explicit token budget; exhausted budget stops discovery, does not fail the run |
| Partial-run behavior | `completed_partial` when Stage A completes but Stage B is bounded off; partial per-source failures recorded in failure summary |
| Failure behavior | Non-200/parse/health failures are recorded, never fabricated; run continues other sources; run ends `completed_partial` or `failed` |
| No-match behavior | Empty results are a valid, recorded outcome (`completed` with zero candidates) |
| Restart/replay behavior | Same pinned SHA, same run inputs → deterministic replay; duplicate run_id prevented by lock/run.json |
| Stop conditions | Time budget, token budget, lock contention, >90% disk, unexpected network egress, protected-path write attempt, or any evidence of automatic promotion/publish |

## 9. What is never done by this workflow

No cron/launchd created by this document; no service/timer installation;
no PostgreSQL mutation; no secrets configuration; no deployment; no publishing;
no source promotion; no taxonomy change; no corpus rewrite; no pruning before a
verified receipt plus retention delay.
