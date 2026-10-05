# Standard document catalog

Used to build master plan §3.1 (the tree) and §3.2 (required content and gates). This is **a menu to choose from**, not a list to copy:

1. Take every document marked **Always**.
2. Take a **Conditional** document when the SDD meets its condition.
3. The `06-design` group gets **one document per major component or mechanism** of the SDD (each level-2 SDD section about a module is usually one document), plus the cross-cutting documents.
4. Rewrite the "Required content" column **for the specific project**: table names, job names, screen names, the DRs that apply. In the plan this column must be concrete enough that the writer knows exactly which sections the document needs. "Describe the design" does not qualify.
5. Number `DOC-01…` in tree order. Documents added later take the next number.
6. Document titles are written in the output language; file and folder names stay English kebab-case.

Default gates: foundation documents (product, glossary, architecture, core data model, local dev) gate **P1**; design documents gate **the phase that implements them**; UI documents gate the UI phase; runbooks and experiments gate the phase that measures or operates. Documents that keep growing (configuration reference, CI/CD) are marked "skeleton at P1".

## 00 · Coordination (always; created by docs-master-plan)

| File | Content |
| --- | --- |
| `README.md` | Index, reading order, DOC × status table, folder table, short conventions |
| `00-master-plan.md` | Per `master-plan.md` |
| `00-decision-register.md` | Per `decision-register.md` |

## 01-product (always)

| File | Required content |
| --- | --- |
| `vision-and-scope.md` | Context, problem, vision (layers of value). Research question or business goal. **Measurable goals** tied to NFRs and to how they are verified. In and out of scope (with reasons for what is out). Assumptions. Constraints (machine, time, people, budget). Cut order |
| `personas-and-journeys.md` | Persona table `PS-x` (system role, device, technical level, frequency). Per persona: goals, pain points, what they need from the system, what they do not need, screens used. One journey `J-x` per persona (steps, emotions, touchpoints: screens and endpoints) |
| `requirements.md` | FRs keep the SDD's IDs; added requirements continue the numbering and are marked "(added)". Each FR is split into `FR-xx.y` rows: requirement, **Given/When/Then acceptance criteria with concrete numbers**, MoSCoW priority, verification (test level, EXP). NFRs: numeric target, how measured, tool, verifying EXP or task. FR → UC → F → design DOC matrix |
| `use-cases.md` | Overall use case diagram (Mermaid). Each `UC-xx` per template A.2: actor, trigger, preconditions, numbered main flow, alternative flows (2a…), error flows (E1…), postconditions, rules, screens/endpoints/events, FRs. The UC list comes from master plan §3.4 |
| `feature-catalog.md` | `F-<GROUP>-xx` by group. Each feature: description, FRs, UCs, phase completed, MoSCoW, feature flag, dependencies, deploying app, cut step in the cut order |

## 02-glossary.md (always)

Tables by topic: term (the name used in code and UI) · local name · definition in 1–3 sentences (with an example when useful) · related (DR/DOC/standard). The master plan lists the **minimum term list**: scan the SDD for every domain noun, every reliability concept, every infrastructure tool. Gate P1, and written **first**.

## 03-architecture

| File | Condition | Required content |
| --- | --- | --- |
| `system-context-and-containers.md` | Always | C4 level 1 (users, external systems). C4 level 2 (every container, protocols between them). Deployment unit table. **Data ownership table**: which table/topic/bucket is written by whom and read by whom. Trust boundaries |
| `data-flows.md` | ≥ 2 components exchange data | A sequence diagram for **every main flow** (the plan names each flow) **and the failure flows** (database down mid-chunk, process killed before ack, external service timeout…) |
| `messaging-contracts.md` | A broker, events, webhooks or file exchange | Topic/queue table, envelope, JSON Schema per version, headers, backward-compatibility rules, hash/key rules |
| `quality-attributes.md` | Always | Per NFR: tactic → concrete mechanism → where implemented → verification. Latency budget per hop. **Capacity estimate** (events/s, rows/day, GB/day at base load and ×10). Resource budget on the target machine |
| `tech-stack-and-versions.md` | Always | Libraries and tools with pinned versions, reason, license. Dev tools. Compatibility table (from spikes) |
| `code-architecture.md` | The project enforces code architecture rules (Clean/Hexagonal/layers) | Layers, dependency rules, package layout, naming, DTOs and mapping, where transactions live, automated rules (ArchUnit…), exceptions, review checklist |

## 04-adr (always)

`README.md` (table: ADR · title · status · gate · source DR) and `0001-record-architecture-decisions.md`. Other ADRs come from architecture-level DRs. The master plan lists each ADR with its source (DR or SDD §) and gate.

## 05-data (when there is storage)

| File | Condition | Required content |
| --- | --- | --- |
| `source-data.md` | External or source-system data | Sources, license, hash, statistics. Fields used and their mapping to tables. Source schemas with DDL. Time rules |
| `<core>-model.md` (warehouse model, domain model…) | A database | Mermaid ERD. **Complete runnable DDL** for every business table. Indexes with reasons. Grain, business key, audit columns. Sample upsert/query for the main tables |
| `ops-model.md` | Operational/state tables (jobs, queues, audit, flags) | DDL. **A state diagram** for every status column. Shared enums |
| `data-quality-rules.md` | Data ingestion or validation | `DQ-xx` catalog: table, layer (before/after write), expression or SQL, severity, action, threshold |
| `db-roles-and-grants.md` | ≥ 2 apps or roles use the database | Role × table × privilege matrix (down to columns when needed). Which app uses which role. Secret provisioning. Migration user separate from runtime users. Permission test matrix |
| `data-lifecycle.md` | Data grows over time | Retention per table/bucket. Maintenance and cleanup jobs. Backup schedule. Personal data policy |

## 06-design

**Common skeleton** of this group (state it in the plan): Purpose → Scope → Components and interfaces (code signatures) → Algorithm (pseudo-code) → Transactions and concurrency → Configuration → Metrics and logs → Errors and handling → Required tests (table with IDs) → Open questions (empty when Approved).

Per SDD component (examples seen): batch/chunk processing, streaming consumer, static data loading, dead letters and replay, analytics (every algorithm has an **input → expected output test table**), AI/LLM (abstract port, adapters, thresholds, kill switches, safety), simulator or synthetic source, real-time delivery (SSE/WebSocket), demo tooling.

Cross-cutting (always when there is a backend):

| File | Required content |
| --- | --- |
| `security.md` | Authn/authz, **endpoint × role matrix**, CORS, rate limits, secrets per environment, TLS, personal data, lightweight STRIDE per trust boundary, security scanning in CI |
| `observability.md` | **Metric catalog** (name, type, labels, emitting service, meaning). Required log fields. Spans and trace propagation. Dashboards (panel list). **Alert rules in the real query language** (PromQL…) linked to runbooks. Delivery channels |
| `configuration-reference.md` | Per app: key · type · default · environment variable · profile · description. Runtime flags |
| `error-handling.md` | Error classes. Exception/error code → class → action. Exception → HTTP status → problem type. Error logging rules |

## 07-api (when there is an API)

| File | Required content |
| --- | --- |
| `api-guidelines.md` | Naming, versioning, pagination, filtering, time, errors, caching, headers, idempotency |
| `api-endpoints.md` | One section `E-xx` per endpoint per template A.4: purpose/UC, authorization, parameters, sample response, errors, data source (tables, main query, index), cache, performance target, related events |
| `<events>.md` | SSE/WebSocket/webhooks: event types, sample payloads, channels, authorization |

## 08-ux-ui (when there is a UI)

| File | Required content |
| --- | --- |
| `ux-principles-and-ia.md` | Numbered UX principles. Sitemap. Navigation by role. URL map with search params. Responsive behavior. Performance budget |
| `design-system.md` | Tokens (color, type, spacing, radius, dark mode, colors for business states). Component catalog. Chart/map conventions. Accessibility criteria |
| `screens/*.md` | **One file per screen** per template A.5, plus a `README.md` index. The plan names each file |
| `ui-states-and-copy.md` | Patterns for loading/empty/error/stale/forbidden. All microcopy. Number and time formats |

## 09-operations

| File | Condition | Required content |
| --- | --- | --- |
| `local-dev.md` | Always | Machine requirements. Tool setup. `make` targets. Port table. Demo accounts. Seed/reset data. Common problems |
| `deploy-<target>.md` | Each target environment | Profiles, start order, health checks, resources, environment variables and secrets, upgrades, migrations, teardown (k8s: probes, PDB, autoscaling, NetworkPolicy…) |
| `ci-cd.md` | Always | Stages, merge-blocking conditions, caching, image tags, deployment, smoke tests |
| `runbooks/RB-xx-*.md` | There are alerts | One runbook per alert per template A.7, plus runbooks for dangerous operations (replay, restore, secret rotation) |
| `backup-restore.md` | Durable state | Schedule, step-by-step restore, RPO/RTO, how it is verified |

## 10-testing

| File | Condition | Required content |
| --- | --- | --- |
| `test-strategy.md` | Always | Test pyramid. Module × test level. Tools. Naming. Test data/fixtures. Coverage targets per module. Fault injection, contract, performance tests. Which tests run in which CI stage. **Index of every document's test-ID prefix** |
| `experiments/EXP-xx-*.md` + `README.md` | Research questions or quantitative claims to prove | README: common protocol, ground truth, baseline, shared formulas. Each EXP per template A.6 |
| `demo-script.md` | A demo or defense | Steps with narration, actions, expected results, fallback when something breaks, pre-demo checklist, reset |

## 11-report (thesis, dissertation or formal report)

`thesis-mapping.md`: chapter outline; for each section, which documents, figures and tables it draws from; claims ↔ evidence; preparation procedure.
