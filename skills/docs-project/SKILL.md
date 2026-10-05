---
name: docs-project
description: Writes, reviews and tracks the project documents (DOC-xx, ADRs, runbooks, experiments, screen specs…) defined by a master plan made with the docs-master-plan skill. Each document follows its required content and gate in master plan §3.2, uses the decisions in docs/00-decision-register.md, records new decisions as DRs, and is written in the output language recorded in the plan. Use when the user wants to write a specific DOC, write all docs of a gate, write the next document, review documents against the Approved definition, check the docs tree, or see documentation status (also in Vietnamese, e.g. "viết DOC-xx", "viết docs cho gate P1", "duyệt tài liệu").
argument-hint: "<DOC-xx …> | gate <Pn> | next | review <DOC-xx|all> | status"
license: MIT
---

# Write the docs from the master plan

Precondition: `docs/00-master-plan.md` and `docs/00-decision-register.md` exist (made by `docs-master-plan`). If not, stop and suggest `/docs-master-plan <sdd.md>` first.

When sources disagree, priority is: **master plan** (required content, gates, IDs, language) → **decision register** (decided DRs) → **original SDD** → this skill's references.

`<skill-dir>` in commands below is the directory containing this SKILL.md. Scripts need Python 3.10+.

References:

- [references/language.md](references/language.md): output language and vocabulary.
- [references/conventions.md](references/conventions.md): IDs, header block, statuses, decisions, style, single source of truth. Read before the first document of a session.
- [references/doc-guide.md](references/doc-guide.md): what a good document of each kind looks like.
- [references/templates.md](references/templates.md): document skeletons (A.x as in Appendix A of the plan, B.x for the rest).
- `locales/<code>.md`: vocabulary per language.
- `scripts/check_docs.py [docs_dir] [--strict] [--vocab FILE]`: checks IDs, links, status lines, open questions.

## Modes

| Command | Does |
| --- | --- |
| `/docs-project DOC-06 DOC-03` | Write the named documents, in order |
| `/docs-project gate P1` | Write every missing document and ADR gated by P1, in dependency order |
| `/docs-project next` | Write the next document of the "Write DOC-…" tasks of Phase 0 and §9 of the plan |
| `/docs-project review <DOC-xx\|all>` | Review against the Approved definition; does not change statuses |
| `/docs-project status` | DOC × gate × status table and the documents blocking the next gate |

## Language (every session, before writing)

Read master plan §0.1. It names the output language and the vocabulary source (`locales/<code>.md` or Appendix B of the plan). Load that vocabulary and its Conventions; write every heading, label and sentence in that language.

If §0.1 is missing (a plan made before this rule), **ask the user** for the output language and the code/UI language (`language.md` §1), add the block to §0 of the plan, add Appendix B if the vocabulary has to be generated, and add a decision-log line. Then continue. Never ask again once §0.1 exists.

## Writing one document

### 1. Gather inputs

- The DOC's row in master plan §3.2: copy "Required content" into a checklist. This defines "complete".
- DRs whose "Write to" names this DOC (`grep -n "DOC-xx" docs/00-decision-register.md`) and DRs the required content names. Read each in full.
- The relevant sections of the original SDD.
- Existing documents this one depends on. Always read the glossary.
- The tasks `Pn-xx` that point to this DOC: they say what the reader will do with it.

**Definition of Ready:** if a related DR is still proposed, tell the user. With their agreement, write according to the proposal and keep the document `Draft`.

### 2. Outline

From the checklist and the skeletons in `templates.md` / `doc-guide.md`, list the sections. Each required item belongs to one specific section. For large documents (endpoint catalog, core design), write the skeleton first, then fill one section at a time with Edit.

### 3. Write

- Header block per `conventions.md` §2, status `Draft` while writing.
- Concrete, with examples and numbers, citing `(DR-xx)`, `(original SDD §x)`, `(DOC-yy §z)`.
- New IDs (FR sub-items, E-xx, DQ-xx, test prefixes…) follow `conventions.md` §1; a new test prefix must be unused (`grep -rn "| <X>-01" docs/`).

### 4. Decisions made while writing

When a choice is not answered by the SDD or the DRs:

- Owner has delegated (the decision log says so, or the user said so): add a DR with the next number, state decided, decided by `dr.delegated`, a decision-log line, and "Write to" including this DOC. An architecture-level decision also gets an ADR, plus an update to `04-adr/README.md` and the plan's ADR table.
- Not delegated: add a proposed DR and put the question under "Open questions" with the DR ID; the document stays `Draft`.
- A decision that changes an Approved document: edit that document in the same change, mark the spot `*<dr.revised> (DR-xx):* …` and update its header date.

### 5. Propagate to source documents

- New term → glossary.
- New configuration key → configuration reference; new metric/alert → observability (if those exist; otherwise list them in the report to add later).
- New test IDs → the prefix index of the test strategy (if it exists).

### 6. Finish

- Tick the checklist: which item is in which section. Anything missing gets written, not skipped.
- Status → `Review` (`Approved` only when the Owner approves or has delegated approval).
- Update the status table in `docs/README.md` and the progress note of the matching plan task (e.g. `P0-09 Write DOC-01…05 — **Review 2026-10-06**`, in the output language).
- Run `python3 <skill-dir>/scripts/check_docs.py docs`; fix every E1/E2 caused by the new document. E1 for documents not written yet is normal while working through a gate; mention it in the report.
- Short report: documents written, new DRs (ID, title, decided or proposed), open questions, propagation still owed to documents that do not exist yet.

Do not commit unless the user asks.

## Writing many documents (a gate)

- Order: glossary → product (vision → personas → requirements → use cases → feature catalog) → architecture → ADRs → data → design → API → UX/UI → operations → testing. Within a gate, documents others depend on come first.
- The glossary and requirements are always written by the main agent. After them, documents of the same gate that do **not depend on each other** may be handed to subagents in parallel (fork, at most 4–5 at a time). Each subagent:
  - writes only its own document file, in the output language with the vocabulary of §0.1;
  - does **not** edit the decision register, glossary, README, master plan, configuration reference or observability;
  - marks new decisions as `DR-NEW-<doc>-<n>` inside its document and returns: proposed DRs (full Problem/Decision/Consequences), new terms, new configuration keys, new metrics, test IDs used.
- The main agent merges: assigns real DR numbers in order and replaces every `DR-NEW-…`, updates the glossary and source documents, then cross-reads for consistent table names, keys and `E-xx` IDs (`grep` the main names). Finally runs check_docs.py.

## Review (`review`)

For each document, check the five points of the Approved definition (`conventions.md` §3):

1. Compare every item of the plan's "Required content" with the document's sections; list what is missing.
2. "Open questions" is empty, or every question has a decided DR.
3. Domain terms used are in the glossary; IDs point to real items (check_docs.py).
4. The header lists its dependencies.
5. Ambiguous places have concrete examples.

Also: contradictions with decided DRs or other documents (table names, keys, thresholds, error codes); keys or metrics missing from their source documents; text not in the output language. Report as `DOC-xx §n: problem → fix`. Do not change statuses; only when the Owner approves, move to `Approved` and update the README, the plan's `Pn-00` doc-gate task, and the decision log if approval is in bulk.

## Status (`status`)

Read §3.1–3.2 of the plan and the header of every file under `docs/`, run check_docs.py. Print a table `DOC · Document · Gate · Status`, then the next gate and the DOCs/ADRs blocking it.
