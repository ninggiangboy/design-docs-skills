# SDD structure

Drawn from two real SDDs: a research data pipeline (public transport intelligence, an academic thesis) and an event ticket booking product (correctness under high load). The ticket booking one is newer and went through more revision rounds; where the two differ, follow it.

Headings are given in English; render them with the `sdd.*` keys of the vocabulary (`references/language.md`).

An SDD answers **what, why, and how the key mechanisms work**. It is not yet a detailed specification: complete DDL, every endpoint and every screen belong to the doc set produced later (`docs-master-plan`, `docs-project`). The core, though, must be deep enough for a reader to trust the design: the key SQL statements, state machines, how races are resolved, the options that were rejected. Secondary parts only need enough to show they exist, what they do and how they connect to the core.

## Header

```markdown
# <System name> — System Design

<Mon D, YYYY> · @<author>

<Lead paragraph, 2–4 sentences: what the system does for whom; the most important requirement or invariant; what this phase includes and what comes later (section 2.3).>
```

The byline date uses the English format (`Oct 5, 2026`) in every language. The author is whoever the user names; default to the git user name.

## Sections

Section numbers are a suggestion. Drop sections that do not apply and split the core into several sections, but keep the **logical order**: problem → goals → users → architecture → domain sections (core first) → data → API → UI → operations → testing → plan → risks → appendix.

### 1. Introduction

| Section | Content | Form |
| --- | --- | --- |
| 1.1 Context | The domain and why the problem is hard (nature of the data, scale, nature of the goods) | 1–2 paragraphs |
| 1.2 Real-world problems | 3–5 problems, each a **bold one-sentence summary** followed by its concrete consequence | List |
| 1.3 Vision | 2–3 numbered "layers of value", **layer name in bold** — explanation; say which layer comes in a later phase | Numbered list |

### 2. Goals, scope and focus

| Section | Content |
| --- | --- |
| 2.1 Research question *(academic)* / Core problem *(product)* | One question in a `>` blockquote stating every hard constraint ("even when requests are retried, processes die abruptly…"). Plus a **target scenario with numbers** (100,000 users competing for 5,000 tickets; 500 vehicles, 100 events per second). An invariant above every other requirement is stated on its own (a code block makes it stand out: `NEVER OVERSELL`) |
| 2.2 Investment by module | Table `Module · Role · Investment level`. Levels: "Deep, with measured experiments" / "Deep" / "Solid implementation" / "Basic" / "After the core is right". This table decides how deep every later section goes |
| 2.3 Scope | **In scope** (list, with numbers and concrete constraints). **Later** (table `Item · Content · How this phase handles it` — the last column shows the current design does not block the future). **Out of scope** (list, with reasons when not obvious) |

### 3. Users, use cases and requirements

| Section | Content |
| --- | --- |
| 3.1 User groups | Each group: **name** — what they need, what they do. State how roles relate (one account can hold two roles…) |
| 3.2 Use cases *(recommended)* | Mermaid `flowchart LR` actors → UCs grouped with `subgraph`; table `ID · Role · Use case`. Include "System" use cases (automatic jobs) |
| 3.3 Functional requirements | Table `ID · Requirement`, `FR-01…`, one testable sentence per row |
| 3.4 Non-functional requirements | Table `ID · Requirement · Target`. **Targets are numbers** with measuring conditions; important NFRs name their verifying EXP. Close with: load numbers are design targets, recalibrated to the experiment machine |

### 4. Overall architecture and technology

- Opening paragraph: the architecture style (modular monolith, pipeline, microservices…) **and why**, tied to the problem ("correctness relies on local database transactions; splitting into services would force distributed transactions").
- A Mermaid diagram of the whole system (users → edge → app → data stores → external services), edge labels saying the role ("every write is conditional", "only to shed load"). One sentence under the diagram summarizing the main flow.
- 4.1 Components: numbered list, **name** — responsibility, technology, boundaries ("modules call each other only through public interfaces").
- 4.2 Cross-cutting principles (or Data flow for a pipeline): 3–6 bold principles, each a design decision with a consequence ("**Redis only sheds load, it never decides.** Losing Redis makes the system slower but never oversells").
- 4.3 Technology: table `Layer · Technology`, naming actual libraries, not just frameworks.

### 5…N. Domain sections

One section per module of table 2.2, **core modules first and deepest**. Each opens with **one sentence stating the governing rule** of the module ("An order becomes paid only when the server receives a webhook with a verified signature; no signal from the browser is trusted."). Blocks to choose from (see style.md):

- A numbered flow with a `sequenceDiagram`.
- An invariant table `Object · Invariant · Enforced by`.
- Lifecycle: a `stateDiagram-v2` **and** a transition table `From · To · Triggered by · Effect`.
- The key SQL or code with an explanation of why it is correct under concurrency.
- A race between two flows: the arbiter rule, the steps, a `sequenceDiagram` with `alt`.
- A rule or parameter table `Item · Rule` or `Parameter · Default · Meaning`.
- An algorithm: formula (`latex` code block), cases, edge cases.
- Options analysis: options A/B/C/D, each with pros/cons/verdict, a comparison table, numbered reasons for the choice.
- A mechanism table `Mechanism · Implementation` (reliability, load…).
- A UI figure with an **ASCII text version** for Markdown export.

A "Basic" module needs only 1–3 paragraphs or one table.

### Data model

- An opening sentence stating the level of detail ("this phase fixes the conceptual model and the mandatory constraints; detailed DDL is written per module during implementation") **or** DDL of the core tables.
- `erDiagram` or a table `Table · Kind · Main content`.
- A **required constraints** table `Constraint · What it protects` — constraints are part of the design: the database rejects wrong states even when the code has a bug.
- Shared conventions (money as integer minor units, times in UTC, migration tool).

### Backend API

- Opening sentence: API style, groups, who may call what.
- Table `Group · Endpoint · Description` (the group only on its first row).
- Request/response examples for the core endpoints (full JSON, error responses too).
- Conventions: error table `HTTP · code · When`, money, time, pagination, contract (OpenAPI → client), tracing, real-time.

### User interface

- Opening sentence: one or several apps, areas, lazy-loading of heavy parts.
- Screen flow per role (`flowchart LR`).
- Table `Area · Screen · Content` (or `Screen · Content · Serves`).
- Technical notes: bundle splitting, state management, real-time, server-based clocks, optimistic UI, accessibility, devices, empty/loading/error states.

### Deployment, operations and fault tolerance

- Deployment: diagram, container/workload table `Component · Deployment · Replicas · Notes`, configuration and secrets.
- Observability and alerting when in scope: logs, metrics, traces; table `Alert · Condition · Level`.
- **Behavior under failure**: table `Failure · (Detection) · System behavior · Recovery`, covering internal failures and external services. A principle sentence: which safe side the system leans to.
- Invariant checks / reconciliation when the problem has invariants.
- Security: the minimal, concrete points.
- Scaling (if relevant): unit of parallelism, the real limits (partitions, connection pool, quotas), no blind scaling.

### Testing and evaluation

- Opening sentence: how correctness is proven.
- Strategy table `Type · Scope · Tool`.
- Experiment table `ID · Experiment · Method · Metrics · Expected`, `EXP-01…`. Every quantitative NFR claim has at least one EXP. There is a **baseline** (a naive version without the mechanism) to compare against.
- Closing paragraph: which EXPs prove which claim.

### Implementation plan

- Opening sentence: ordering principle (core correctness first; each stage ends with something that runs).
- `flowchart LR` of stage dependencies, with a branch to "Later".
- Table `Stage · Content · Results` (results name the EXPs they produce).
- **Cut order** in one sentence, with what must not be cut and why.
- Demo script: 5–7 numbered steps, each an action and what the audience sees.

### Risks and limitations

- Table `Risk or limitation · Impact · Mitigation` (8–12 rows); mitigations point back to designed sections.
- **Open points**: what is not decided yet (defaults to confirm, proposed choices). Write the vocabulary's `phrase.none` when empty.

### Appendix: Repository layout

A directory tree in a code block, a `#` comment per important directory, matching the modules of 4.1. One sentence after the tree when a shared part deserves mention.

## Variants

| Project type | Differences |
| --- | --- |
| Academic / research | 2.1 is a research question; 2.2 says "Role in the thesis"; a full experiments section with baselines; a dashboard may be a "demonstration tool"; the cut order protects the part answering the research question |
| Phased product | The lead paragraph names the phase; 2.3 has the "Later" table; each section notes what is deferred and why the current design does not block it |
| Data pipeline | 4.2 is the data flow (diagram); a sources / simulator section; a reliability mechanism table; an analytics section |
| Transactional system | Invariant tables, conditional writes, idempotency, races, invariant checks |
| With AI/ML | A dedicated section: where AI is used and **where it is not**, the pattern "code prepares the state → model judges → code decides", thresholds, safety principles, kill switches |
