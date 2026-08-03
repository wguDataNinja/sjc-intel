# SJC_Intel VPS Continuity

**Status:** Current supporting continuity reference.
**Authority:** `ROADMAP.md` §§3E–3F is execution authority; Ivy Control VPS owns privileged infrastructure procedures.
**Last reconciled:** 2026-08-03.

## Current state

- **VERIFIED locally:** file-backed SJC data remains authoritative; storage and PostgreSQL adapters/migrations are present; retention and metrics tools have offline coverage; deployment units are inert templates.
- **VERIFIED locally:** no SJC VPS checkout, active service/timer, real health producer, or SJC Hermes runtime was found during Task 08.
- **DOCUMENTED BUT NOT VERIFIED in this repo:** current VPS capacity, deployed SJC revision, live database state, and service configuration. Obtain fresh authorized Ivy evidence; do not rely on historical capacity reports alone.

## Durable operating model

The VPS may perform approved bounded deterministic fetching and prepare short-lived run bundles. The Mac receives acknowledged bundles and remains durable authority for corpus, review, archives, restore, and static release preparation. The VPS never publishes.

If separately approved after admission, PostgreSQL Option B may hold locks, run state, source health, transfer manifests/acknowledgements, and small operational queues. It is not a corpus, search, or launch requirement.

## Required evidence before activation

1. Clean approved revision and Ivy admission.
2. Read-only capacity evidence and approved two-source selection.
3. Explicit service/config/secrets/transfer/retention/rollback packet.
4. One runner with lock/timeout behavior, real health, bounded manifest/checksum bundle, Mac receipt acknowledgement, and prune gate.
5. Four reconciled shadow runs, then separately authorized scheduling with a seven-day healthy window.

## Routing

Use Ivy's current project control record and deployment/admission standards for privileged operation. Read `AGENTS.md`, `ROADMAP.md`, and this file before VPS work. No document here authorizes service/timer installation, deployment, secrets, migrations, database writes, transfer, retention pruning, or publication.
