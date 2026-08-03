# SJC_Intel VPS Supporting Plan

**Status:** Supporting deployment reference; not an execution roadmap.
**Authority:** `ROADMAP.md` §§3E–3F controls SJC VPS sequencing and gates.
**Last reconciled:** 2026-08-03.

## Purpose

The low-cost Ivy VPS may become an always-on operational node for bounded deterministic collection. It is not required for the first static SilverLeaf release and is not the durable SJC corpus authority. The Mac file corpus remains authoritative for source events, intelligence items, review, archive/restore, and public-release preparation.

## Intended operating boundary

~~~
VPS: approved fetches, one scheduler/writer, bounded temporary run bundles,
     health and (only if separately approved) narrow PostgreSQL metadata
              ↓ checksum/manifest + receipt acknowledgement
Mac: durable file corpus, review, archive/restore, publication export
~~~

PostgreSQL is optional until VPS activation. If approved, use Option B only for locks, run/source-health state, transfer manifests/acknowledgements, and small operational queues. Do not make it corpus authority, a search API, or a launch dependency. Bounded staging or corpus authority needs new measured evidence and a separate roadmap decision.

## Admission and activation sequence

1. A clean, approved deployable revision and separate Ivy admission packet.
2. Current read-only capacity evidence, exact source-selection rationale, service/configuration/secrets route, and rollback/transfer plan.
3. An explicitly authorized two-source manual/disabled shadow runner with a lock, timeouts/retries, run bundle, checksum, Mac acknowledgement, retention limit, real health producer, and prune gate.
4. Four healthy shadow runs with reconciliation and rollback evidence.
5. Only then, separately authorized limited scheduling and a seven-day healthy window. Agentic discovery remains manually triggered and candidate-only.

Ivy Control VPS owns privileged operations, deployment controls, health registration, capacity evidence, service/timer changes, secrets, and database operations. Follow its current `repos/sjc-intel/CONTROL.md` and applicable admission/deployment contracts after reconciling their state with this roadmap.

## Non-goals

No SJC VPS action is authorized here. Do not install/enable services/timers, provision PostgreSQL, run migrations, transfer real data, prune, deploy, or publish from this plan. The historical detailed plan was superseded because it assumed a PostgreSQL operational corpus before the file-authority and static-launch decision.
