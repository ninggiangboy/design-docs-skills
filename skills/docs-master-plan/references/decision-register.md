# Blueprint: `docs/00-decision-register.md`

The decision register is the most important output of planning. An SDD usually explains *what* and *why* well but leaves *exactly how* open. Each gap becomes a DR with **one concrete proposed option** so the Owner can review quickly. Guessing wrong at the data and semantics layer is expensive to undo, so those DRs are decided before any code.

Headings and labels below are English; render them through the vocabulary (`dr.*`, `col.*` keys).

## 1. File skeleton

```markdown
# Decision Register

> Status: **Review** · Updated: YYYY-MM-DD · Source: analysis of `<sdd>.md` (the **original SDD**)

<One paragraph: where the SDD is strong, where it lacks "exactly how", why these must be decided first.>

**How to use**

- Each entry has a state: `Proposed` → (Owner reviews) → `Decided` or `Changed` (record the alternative).
- A decided entry is carried into its target documents (the *Write to* line). Architecture-level entries become ADRs in `docs/04-adr/`.
- **⚠ deviates from the original SDD**: the proposal differs from the SDD; the reason is given.
- **🔬 spike**: needs a short experiment (≤ 1 day) before deciding.

## Decision log

| Date | Decided by | Content | Affected items |
| --- | --- | --- | --- |

---

## A. <Topic group 1>

### DR-01 · <Question to decide> — ⚠ deviates from the original SDD
- **Problem:** …
- **Options:** (1) … ; (2) … ; (3) … — only when there is a real choice
- **Decision (proposed):** …
- **Consequences:** …
- **Write to:** DOC-xx, ADR-xxxx.

…

---

## Summary by impact

| Level | Items | Why decide early |
| --- | --- | --- |
| Blocks P1 | DR-… | Fixes schemas, contracts and repo layout |
| Blocks P2 | DR-… | … |
```

When the Owner decides, the DR title gets the result — `### DR-01 · Which feed to use — **Decided: Metro Transit**` — and the decision log gets a line. The Owner may accept in bulk ("Accept all remaining proposals"); record it exactly so.

## 2. What a good DR looks like

- The title is **a specific question**, not a topic ("Mapping a poll to a chunk, and when to ack", not "Kafka").
- **Problem** quotes where the SDD says it (SDD §x) and states the consequence of leaving it open.
- **Decision** is detailed enough to code from: DDL, a JSON example with every field, a topic/key/partition table, defaults with units, numbered algorithm steps, formulas. Example:

  ```markdown
  ### DR-05 · Topics, keys and partitions
  - **Decision:**

    | Topic | Key | Partitions | Retention | Notes |
    | --- | --- | --- | --- | --- |
    | `gtfs.vehicle_positions` | `route_id` | 12 | 7 days | delete |

    Dev: RF = 1. k8s: RF = 3, `min.insync.replicas = 2`. Topics are created by script; auto-create is off.
  - **Write to:** DOC-09, ADR-0008.
  ```
- When there is a real choice, list the options with one line of pros and cons each, then pick one.
- **Consequences** name the cost and the follow-up work (new tables, cleanup jobs, required tests).
- One DR, one decision. A large decision with several parts uses a sub-list inside one DR rather than five scattered DRs.

## 3. Gap-hunting checklist

Walk through the SDD section by section and ask the questions below. Every question the SDD does not answer precisely becomes a DR. Not every project has every group.

**Data and sources**
- Which exact source (file, dataset, API, database), license, size, statistics? Does it need a spike to measure?
- The schema of every source and of every table the SDD only names. The business key / natural key of each entity.
- Time zones, clocks, business dates, times past midnight, daylight-saving transitions.
- Is reference data versioned; how does a new version replace the old one (staging, swap)?
- Partitioning, retention, estimated volume, indexes.
- Personal data: which fields, where they are removed, where they must never go.

**Contracts**
- Message format, envelope, field names, `schema_version`, backward-compatibility rules.
- Topics or queues, keys, partition counts, which ordering must hold.
- API conventions: versioning, pagination, errors (Problem Details), time format, idempotency of POST.
- Contracts with external systems (SDK, quota, error codes, timeouts).

**Correctness semantics**
- Delivery guarantee (at-most / at-least / effectively-once) and the exact mechanism.
- Idempotency: which key, which ordering guard; are computed results idempotent on re-run (keyed by event time or by wall clock?).
- Transaction boundaries: what commits together; when offsets or acks commit.
- Several replicas at once: locks, fencing, duplicate job runs, recovery when a process dies midway.
- A state machine for every entity that has a status.
- Replay and backfill: from which source; does the dedup mechanism block it?

**Errors**
- Error classes (data / transient infrastructure / fatal) and the behavior of each.
- Retry, backoff, limits, dead letter queue, skip limits, circuit breakers.

**Contradictions and ordering inside the SDD**
- Permissions that contradict features (a read-only service that exposes write endpoints).
- A feature promised in an early phase whose infrastructure arrives in a later phase.
- Quantitative claims (NFRs) with no measuring method, no ground truth, no baseline.
- Two mechanisms that cannot be used together.

**Algorithms and business rules**
- Exact definitions, parameters and defaults, edge cases, triggers, schedules.
- Which configuration holds each threshold; who owns the decision (code or an AI model).

**Platform**
- Versions of language, framework, libraries (default: the latest stable; 🔬 spike for compatibility).
- Deployment units: how many apps or images, which app runs which profile, which module is a library.
- Repository layout (monorepo?), build tool, code architecture (layers, dependency rules).
- Identity provider, secret management, TLS.
- Observability backend: where metrics, logs and traces live; alert channels.
- Resource budget on the target machine (RAM per container); is each image still published; licenses.

**Frontend and UX** (when there is a UI)
- Stack, routing, state, data fetching, real-time; maps and charts; authentication in a SPA; UI language; runtime configuration.

**Operations, testing, experiments**
- Environments (local compose, k8s, cloud), how to deploy, whether CI runners have enough resources.
- Backup, RPO/RTO. Runbooks for which alerts.
- Ground truth and baseline for each experiment; number of runs; the machine they run on.
- Demo: script, pre-seeded data, fallback plan.

**Process**
- Languages of documents and code (already recorded in master plan §0); branching; commit convention; public or private repository; scope (full or with planned cuts).

## 4. Groups and order

- Group by topic with letters A, B, C…, following the system's flow (sources → data model → core processing → business logic → AI → API → frontend → operations → deployment, demo).
- Number DRs consecutively from DR-01 in order of appearance. Later DRs take the next number whatever their group.
- A 50–80 KB SDD usually yields 40–70 DRs. Fewer than 20 usually means the review was too shallow.

## 5. "Summary by impact"

Assign each DR to the first phase it blocks. DRs that block P1 (schemas, contracts, repo layout, versions) and P2 (core semantics) must be decided before coding. This table is the input to task P0-01 of the master plan.
