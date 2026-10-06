# Documentation conventions

Shared by the master plan, the decision register and every document under `docs/`. The master plan copies the core of this file into its §0, §7 and Appendix A, so once a plan exists **the plan is the source of truth**; when they disagree, follow the plan.

Headings and labels below are given in English. Render them in the project's output language through the vocabulary (`references/language.md`). IDs, status values, code and file names never change with the language.

## 1. Identifiers

Each prefix has one meaning in the whole project. Before introducing a new prefix (test IDs of a document, tasks of a special phase), check it is unused. Example of a clash avoided in a real project: the refactoring phase used `RF-xx` because `R-xx` was already the prefix of replay tests.

| Prefix | Meaning | Defined in |
| --- | --- | --- |
| `FR-xx` / `FR-xx.y` | Functional requirement / sub-requirement | requirements |
| `NFR-xx` | Non-functional requirement | requirements |
| `UC-xx` | Use case | use cases |
| `PS-x`, `J-x` | Persona, journey | personas and journeys |
| `F-<GROUP>-xx` | Feature | feature catalog |
| `BR-xx` | Business rule (when rules need numbers) | use cases |
| `DOC-xx` | Document | master plan §3.1 |
| `ADR-xxxx` | Architecture decision | `04-adr/NNNN-*.md` |
| `DR-xx` | Decision register entry | `00-decision-register.md` |
| `Pn-xx` | Task of phase n; `Pn-00` is always the doc gate | master plan §5 |
| `Mn` | Milestone that closes phase n | master plan §4 |
| `S-xx` | Spike (an experiment of at most 1–2 days) | master plan, Phase 0 |
| `E-xx` | API endpoint | API endpoint catalog |
| `FL-xx` / `FL-xx.y` | Detailed flow / sub-flow | `06-design/flows/` |
| `DQ-xx` | Data quality rule | data quality rules |
| `EXP-xx` | Experiment | `experiments/` |
| `RB-xx` | Runbook | `runbooks/` |
| `<X>-xx` | Required test case of one document (one prefix per document, e.g. `B-`, `R-`, `G-`) | the document's "Required tests" section; the test strategy indexes all prefixes |

Rules:

- A number once assigned never changes and is never reused. A dropped item is struck through (`~~…~~`) with the reason; its number is not deleted.
- New items take the next number in the sequence (`DR-105`, `DOC-49`), even if their topic belongs to an earlier group.
- Ranges are written compactly: `FR-01…12`, `DOC-07…11`, `DR-21–24`, `P5-06…13`.
- A reference to a subsection is `DOC-19 §4.3`. A reference to the original SDD uses `meta.original_sdd` in the output language plus `§`: "original SDD §6.2", "SDD gốc §6.2".

## 2. Header block

Ordinary document:

```markdown
# <Document title>

> Status: **Draft** · Updated: YYYY-MM-DD · DOC-xx
> Depends on: original SDD §x, [DR](../00-decision-register.md) (DR-05, 20), [DOC-yy](../03-architecture/x.md) §2
> Main readers: <who or which tasks read it: app, Pn-xx, other documents>

<1–3 sentences: what this document covers, what it does not and where that lives.>
```

When updating because of a decision, add the reason after the date: `Updated: 2026-09-30 (DR-104: Clean Architecture layout)`.

ADR:

```markdown
# ADR-0003: <Title that states the decision>

- Status: Accepted
- Date: YYYY-MM-DD · Related: DR-13, FR-03, NFR-01, EXP-01
```

Runbook: the second header line is `Alert: \`AlertName\` (severity, for) · Dashboard: … · Related: …`. Experiment: `DOC-45 / EXP-01`.

The labels (Status, Updated, Depends on, Main readers, Related, Date) come from the `meta.*` keys of the vocabulary; the status values stay in English.

## 3. Statuses

| Kind | Lifecycle |
| --- | --- |
| Document | `Draft` → `Review` → `Approved` → `Superseded` |
| ADR | `Proposed` → `Accepted` → `Superseded by ADR-yyyy` |
| DR | `dr.proposed` → `dr.decided` or `dr.changed` (record the alternative chosen), written in the output language |
| Plan task | empty → `**<plan.done>** (\`sha\`)`; postponed or cut tasks state the reason |

A document is **Approved** when all five hold:

1. It has every item of its required content in master plan §3.2.
2. "Open questions" is empty ("None."), or each question has a DR in the decided state.
3. Every term is in the glossary; every ID (FR, UC, DR, E…) points to an existing item.
4. The documents it depends on are listed in its header.
5. Every place that could be read two ways has a concrete example (payload, SQL, test table).

Only the Owner moves a document to Approved, unless the Owner has delegated it.

## 4. Decisions

- Every choice the original SDD does not make is a **DR**. No silent decisions inside a document.
- New DR: next number, placed in the matching topic group, plus one line in the decision log (date, decided by, content, affected items). "Decided by" is the Owner, or `dr.delegated` ("Claude (delegated by Owner)") when the Owner has delegated.
- Each DR has a **Write to** line listing its target documents. Architecture-level DRs (hard to reverse, many modules affected) become ADRs.
- Changing a decided item: never overwrite. Add `*<dr.revised> (DR-yy):* …` inside the old item and update its target documents in the same change. ADRs are never edited in substance: write a new ADR and mark the old one `Superseded by`.
- A proposal that differs from the original SDD is marked **⚠ <dr.deviates>** with the reason. Never edit the original SDD file.
- A choice that needs an experiment first is marked **🔬 <dr.spike>** and gets a task `S-xx` in Phase 0.

## 5. Language

The output language, and the language of code, UI strings, logs and commits, are chosen once per project and recorded in master plan §0 (`references/language.md`). Defaults offered: documents in the SDD's language; everything else in English.

- Technical terms stay in English when the local term is awkward; code names go in backticks.
- UI strings shown in documents are quoted exactly as they appear on screen, in the UI language.

## 6. Writing style

- Short, active sentences, one idea per sentence. No marketing, no hedging ("could consider", "might want to").
- Write enough to **implement without asking**: table names, columns, configuration keys, defaults, units, thresholds, error codes.
- Every design statement cites its source in parentheses: `(DR-21)`, `(original SDD 6.3)`, `(DOC-14 §5)`.
- Tables for catalogs and comparisons; numbered lists for sequences; prose for reasons.
- Diagrams in Mermaid (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`) so they render on GitHub. Quote every node label: `A["Hold (SKIP LOCKED)"]`.
- Real examples instead of abstract descriptions: JSON with every field, runnable SQL, test tables with inputs and expected results.
- Never re-explain a framework or a standard; say how the project uses and configures it.
- Each document states its boundary: what belongs to which other document.
- Numbers say whether they are **planned** or **measured** (with date, machine and measuring script).
- Number and date formats follow the Conventions section of the output language's vocabulary.

## 7. Single source of truth

| Item | Defined only in | Elsewhere |
| --- | --- | --- |
| Term | glossary | use the exact word; never redefine |
| Configuration key, environment variable | configuration reference | sub-tables in design documents are allowed but must match |
| Metric, alert | observability | link to it |
| Table, column, DDL | data documents | link with `DOC-xx §n` |
| Endpoint | API endpoint catalog (`E-xx`) | refer by `E-xx` |
| Topic, message, schema | messaging contracts | link to it |
| Decision | DR / ADR | link to it; do not re-argue at length |

Adding a configuration key, metric or term anywhere means updating its source document in the same change.

## 8. Folder layout

- `docs/README.md`: index, reading order, DOC × status table, short conventions.
- `docs/00-master-plan.md`, `docs/00-decision-register.md`.
- Numbered groups: `01-product/`, `02-glossary.md`, `03-architecture/`, `04-adr/`, `05-data/`, `06-design/`, `07-api/`, `08-ux-ui/`, `09-operations/`, `10-testing/`, `11-report/`. Unused groups are omitted without renumbering the others.
- File and folder names are English kebab-case in every output language. ADR: `NNNN-kebab-title.md`. Runbook: `RB-xx-kebab.md`. Experiment: `EXP-xx-kebab.md`.
- The SDD file stays at the repository root and is called the **original SDD** (`meta.original_sdd`).
