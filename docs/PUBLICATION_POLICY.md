# Publication Policy

**Status:** Authoritative policy for public-release classification.  The
release mechanics remain in `docs/publication_release_contract.md`.
**Owner:** Buddy owns policy and human exceptions. Hermes and release tooling
apply this policy deterministically.
**Version:** 1.1 — 2026-08-07 (Model B refinements, Task 29).

## Default rule

SJC_Intel normally publishes a verified, public-source item by default when it
is clearly relevant to SilverLeaf households, has a public-safe projection,
and does not fall into an exception below. A human does not need to approve
each ordinary road, school, utility, development, business, service, county
decision, preparedness, or durable historical-context item one at a time.

The classifier is evidence-preserving: it derives a status from canonical item
fields and existing human decisions. It never upgrades review status, changes
source evidence, or writes a publication decision by itself.

## Classification outcomes

| Outcome | Meaning | Release treatment |
|---|---|---|
| `AUTO_PUBLISHABLE` | Verified, publicly attributable, low-sensitivity, resident-relevant item with an allowed public projection. | Included by the deterministic selector. |
| `NEEDS_HUMAN_REVIEW` | Potentially useful but sensitive, ambiguous, locally insufficient, media-only, or explicitly deferred. | Excluded until a human records an exception decision. |
| `NEEDS_MORE_RESEARCH` | Evidence, verification, canonicality, source link, or review status is incomplete. | Excluded; research/review work is required. |
| `EXCLUDE` | Not appropriate for the public corpus, withdrawn, rejected, superseded, duplicate, archival-only, or private/internal. | Never selected unless a new, auditable correction changes the underlying disposition. |

## Ordinary auto-publishable material

Provided the default rule is met, this includes official and publicly
attributable resident information about roads and construction; schools;
development and zoning with a concrete local scope; utilities; businesses and
openings; health-care facilities; parks and services; county decisions with
household impact; preparedness; project timelines; and official historical
context.

“Verified” is necessary but not sufficient. The product is SilverLeaf Brief,
not an unfiltered county notice feed. A record must carry a concrete
SilverLeaf, corridor, tracked-entity, or structured countywide-household
relevance signal. High-volume NBOR notices and BCC agenda motions need that
concrete signal; generic boilerplate is not inferred to be resident-relevant.

## Human-review exceptions

Human review is required for public-safety or crime incidents; minors;
arrests; allegations; personally sensitive information; unclear identities;
conflicting, weak, or stale evidence; material speculation; content that could
unfairly characterize a person or entity; non-official media context; and any
item marked `human_review_required`, medium, or high sensitivity.

An approved `data/publication_decisions/<item_id>.yaml` record is the durable
human exception or override. A rejected, withdrawn, or deferred record wins
over default classification. Existing decisions remain audit history; the
policy does not replace them.

### Corroborated local-media handling (v1.1)

A local-media or other non-official-source item may publish by default (without
a per-item approval) only when the approved decision records corroboration of
its central fact:

- at least one official or first-party source; or
- two or more credible independent outlets supporting the same central fact.

The corroboration is recorded on the decision (`corroboration[].kind` =
`official` | `first_party` | `local_media`). Allegations, anonymous claims,
sensitive personal reporting, and weak single-source speculation are never
auto-published. An item may also publish as a qualified subject with explicit
attribution even without formal corroboration (see below).

### Qualified publication (v1.1)

A confirmed subject with unresolved details may publish with a qualified
posture rather than being classified unpublishable. Example:

> A grocery-anchored center is under review at CR 16A and SilverLeaf Parkway.
> Plans have repeatedly been reported as matching Harris Teeter, but the tenant
> has not been formally confirmed.

The decision records `qualified: true` (and a public-safe `qualified_label`).
Qualified items never state an unconfirmed detail as fact.

### Editorial product roles (v1.1)

Each release item carries an editorial role set by a human decision:
`latest` (current/recent/active), `browse` (durable resident knowledge),
`context` (background for another item or timeline), or `timeline` (merged
history of one durable subject). Roles are never inferred from recency alone.
Home shows `latest`; Browse shows the full corpus. Completed projects and
historical milestones may appear as `browse`/`context`/`timeline` without
being presented as fresh news.

### Expired events vs durable context (v1.1)

The 30-day stale protection still applies to genuine time-bound notices
(closures, chlorine burnouts, application deadlines). A record marked with a
durable role (`browse`/`context`/`timeline`) or an approved decision is durable
context, not an expired notice, and does not require repeated human exceptions
solely because it is older than 30 or 60 days. Historical milestones always
display with their explicit source dates.

### Backfill visibility (v1.1)

Monthly backfill intelligence records (`data/monthly/*/discovered_items.yaml`,
the `SJC-BF-*` family) are part of the canonical publication candidate universe
via the shared read path in `scripts/publication_common.py`. They are
deduplicated against `data/intel_items/`, preserve their original IDs and
source attribution, and are classified under the same rules as ordinary items.
Monthly wraps, topic clusters, and source-gap notes are not items.

## Never-public material

Do not publish private or login-gated information, unsupported rumors, raw
agent reasoning, internal review notes, candidate/source-proposal metadata,
credentials, secrets, private operational data, duplicate captures, or
superseded/withdrawn public claims.

## Evidence and relevance requirements

An automatic classification needs all of the following:

1. `review_status: verified` and `verification_status` of `source_confirmed`,
   `cross_referenced`, or `fact_checked`.
2. A registered, public source and direct public source URL.
3. An official-source type for default publication. Local media may establish
   a lead or context but is a human-review exception until corroborated.
4. A low-sensitivity record with no `human_review_required` flag and no
   sensitive incident/person-harm indicators.
5. A concrete resident signal: registered SilverLeaf/nearby corridor/place,
   tracked entity, or a structured countywide household impact with a
   resident-facing topic and explanation.
6. A projection that passes the public allowlist/denylist checks.

Time-bound notices older than 30 days are a human-review exception unless a
recorded decision preserves them as durable context. This prevents expired
closures, temporary water-treatment notices, and event invitations from being
silently republished as current information.

The policy intentionally treats an absent relevance signal as an exception,
not as permission to guess from a title or keyword.

## Operations and corrections

`scripts/select_publication_items.py` is the policy implementation and emits
classification reasons. `CURRENT_BRIEF.md` summarizes counts and exceptions;
it does not expose internal notes or raw reasoning. The release builder may
include all `AUTO_PUBLISHABLE` items plus approved human exceptions, while the
deploy step remains an explicit authorized action.

When a public item is wrong, stale, or harmful: record a withdrawal or
correction decision, generate a superseding release, preserve the old manifest
for audit/rollback, and do not silently rewrite historic public artifacts.
