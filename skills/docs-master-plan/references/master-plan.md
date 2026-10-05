# Blueprint: `docs/00-master-plan.md`

The goal of the master plan: **when a task starts, everything needed to do it is already in the docs; nobody has to ask.** The plan says which documents must exist, what each must contain, which task happens when, and what "done" means for each. The plan holds no detailed design; design lives in DRs and DOCs.

The first version has status `Review`. When the Owner approves it, it becomes `Approved v1.0`. Headings below are English; render them with the `plan.*`, `col.*` and `meta.*` keys of the vocabulary.

## Header

```markdown
# Master Plan: building <Project> end to end

> Status: **Review** · Updated: YYYY-MM-DD · Accompanies: [00-decision-register.md](00-decision-register.md) · Source: `<sdd>.md` (**original SDD**)

<Intro listing the four things the plan contains: the gaps found in the SDD; every document to write (content and gate); every task by phase with acceptance criteria; traceability from requirements to tasks and verification.>

Goal: when a task starts, everything needed for it is already in the docs. Nobody has to ask.
```

## §0. How to use this document

- **0.1 Language** — the block defined in `language.md` §3: output language and vocabulary source, language of code/UI/logs/commits, who decided and when. Always first.
- Reading order for newcomers: §1 → §4 → the current phase in §5 → the documents that phase references.
- **Doc gate rule:** every phase has a task `Pn-00` that reviews documents; a phase starts only when the documents it needs are `Approved` (§3.3).
- The identifier table (from `conventions.md` §1, keeping only prefixes this project uses, plus any project-specific prefix).
- Document status lifecycle.

## §1. Analysis of the original SDD

### 1.1 What is already good and stays
5–8 specific bullets (no generic praise). This is what the plan commits not to change.

### 1.2 Main gaps
Table `# · Gap · Consequence if left open · DR`, the 8–15 heaviest items from the register. The consequence column states the real damage ("a replay creates new rows and breaks idempotency"), not "unclear".

### 1.3 Adjustments to the plan in the original SDD
Table `Adjustment · Reason`. Always includes **adding Phase 0: specification and spikes**. Common adjustments: moving work whose dependency arrives in a later phase; minimal CI from P1; tables or components that must be added for the SDD's flows to work; replacing a heavy tool by a lighter one; using an existing framework instead of building one.

## §2. Working principles

5–8 numbered principles drawn from the SDD's focus. Always:
1. The core (the research question or the main value) right first, complete later; core phases are never cut.
2. Every phase ends with something that runs and can be demonstrated (milestone).
3. Docs travel with code: a behavior change edits the doc in the same PR; a decision change gets a new ADR.
4. Every threshold is configuration; every configuration key is in the configuration reference.

Add project-specific principles ("transaction boundaries are proven by fault-injection tests before writing real jobs", "every computed result is idempotent and has a run-twice test").

## §3. Documents to write

### 3.1 The docs/ tree
One code block with the tree; every file has a `# DOC-xx` comment (the checker reads DOC IDs from it). Built from `doc-catalog.md`.

### 3.2 Required content of each document
"The Gate column is the phase that needs the document Approved before it starts." One table per group: `DOC · Document · Required content · Gate`. The design group states the **common skeleton**. ADRs get their own table: `ADR · Subject · Source · Gate`.

Required content must be **specific to the project**: names of the tables that need DDL, names of the flows that need sequence diagrams, job names, screen names, the minimum glossary term list, the DRs that apply, coverage targets. Bold the items most likely to be forgotten.

### 3.3 Definition of "Approved"
The five-point checklist (`conventions.md` §3).

### 3.4 Use cases to write
Table `UC · Name · Main actor · FR`. Includes user use cases and system use cases (schedulers, automation) and operator/researcher use cases.

## §4. Roadmap

### 4.1 Phase overview
Table `Phase · Name · Estimate (1 person, full time) · Milestone`. A milestone `Mn` is a checkable sentence ("`make up` works; events reach Kafka; the raw zone has files"). A total row, and a factor for part-time work. State that the numbers are for planning and are recalibrated after every milestone.

Default phase skeleton (merge, split or rename to fit the SDD; keep the SDD's own phases when it has a plan):

| Phase | Typical content |
| --- | --- |
| P0 | Specification, deciding DRs, spikes, writing the P1-gated documents |
| P1 | Foundation: repo, build, minimal CI, local infrastructure, migrations, data sources or simulator |
| P2 | The core of the system (what answers the research question / delivers the main value) |
| P3 | Reliability, observability, experiments for the core |
| P4 | Business logic or analytics, and the API |
| P5 | User interface |
| P6 | Advanced features (AI…) |
| P7 | Scale, k8s, fault tolerance |
| P8 | Hardening: security, docs, demo, release |

### 4.2 Phase dependencies
Mermaid `flowchart LR`, plus a sentence on which phases can run in parallel with two people.

### 4.3 Cut order when time runs short
One line from first cut to last, each item with its task IDs. State what **must not be cut**. State the trigger (for example a milestone more than 50% late).

## §5. Tasks per phase

"Each table has the columns **ID · Task · Output and acceptance · Depends on · Documents**."

Each phase:

```markdown
### Phase n: <Name>

Goal: <one sentence>.   (optional)

| ID | Task | Output and acceptance | Depends on | Documents |
| --- | --- | --- | --- | --- |
| Pn-00 | Doc gate: DOC-…; ADR … | Approved | M(n-1) | — |
| Pn-01 | <a concrete task naming the class/job/table/command> | <a checkable output: which command produces what, which test passes, which number> | Pn-xx | DOC-xx |

**Exit criteria (Mn):** <manual and automated checks, with numbers>.
```

Task rules:
- One task ≈ 0.5–3 days of work and ends in one complete commit or PR.
- The acceptance column is **a test**, not a description: "Test: 1 bad record in a chunk of 500 → 499 rows written, 1 dead letter", "`docker compose up` → every container healthy in ≤ 3 min", "coverage ≥ 90%".
- The Documents column points to the DOC that holds the task's design. A task with no design DOC signals a missing document.
- Phase 0 contains: P0-01 review the decision register; one task per spike `S-xx` (output: spike note and evidence, which DR/ADR/DOC it updates); the "Write DOC-…" tasks in the order of §9. Exit M0: every P1-gated document Approved, every P1-blocking spike concluded.
- The last phase has a release-tag task.

## §6. Traceability matrix

Table `Requirement · Design documents · Tasks · Verification`, one row for **every** FR and NFR (and major architecture decisions if any). No FR without tasks; no NFR without a verification.

## §7. Working conventions

- 7.1 Definition of Ready: referenced documents Approved; no related DR still Proposed; measurable acceptance criteria; dependencies done.
- 7.2 Definition of Done: merged and CI green; tests for new behavior, a reproducing test for every bug fix; new metrics/logs/configuration recorded in their source documents; docs updated in the same PR; runs with the standard start command (when there is a runtime). Add project-specific conditions (architecture rules…).
- 7.3 Git and code: branches, Conventional Commits, languages (from 0.1), PR template, formatter, migration naming.

## §8. Additional risks (beyond the original SDD)

Table `Risk · Early sign · Mitigation`. Every spike and every external dependency (SDK, service, image, new major version) usually brings one risk. The mitigation names a concrete fallback.

## §9. Start now: the first 10 tasks

A numbered list: decide the P1/P2-blocking DRs → run spikes in parallel → write the glossary → requirements and use cases → architecture and the P1-gated ADRs → data model with DDL tried on a real database → foundation ops documents → review M0 → start P1 → write P2's documents in parallel with P1.

## Appendix A: Shared templates

Copy templates A.1–A.7 from `templates.md`, rendered in the output language. Drop templates of groups that do not apply; replace examples with examples from this project.

## Appendix B: Vocabulary (only for a generated vocabulary)

When the output language has no shipped `locales/<code>.md`, the full translated vocabulary table goes here (`language.md` §2): `| Key | English | <language> |`, every key of `locales/en.md`, plus a short Conventions list. With a shipped locale, omit this appendix; 0.1 names the locale file.

---

## Updating the plan during implementation (for reference; not part of creating the plan)

- Task done: append `— **Done YYYY-MM-DD** (\`sha\`)` (in the output language) to the Task column; when the result deviates from the docs add `(deviates slightly from the docs, DR-xx)`.
- Milestone reached: add a paragraph `**Mn reached on YYYY-MM-DD.**` with the measuring environment and a `Criterion · Result` table of real numbers.
- Spike done: strike the old title, record the result and the new DR/ADR.
- A risk that happened: strike it, note "happened, handled YYYY-MM-DD" and how.
