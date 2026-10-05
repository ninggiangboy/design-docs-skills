---
name: docs-system-design
description: Writes and iteratively revises a system design document (SDD) titled in the form "System name — System Design". Covers context, the core problem, investment per module, scope, requirements, architecture, deep domain sections (invariants, state machines, races, options analysis), data, API, UI, fault tolerance, experiments, plan and risks, in the output language the user chooses. Use when the user wants to write an SDD, design a system from an idea, or edit, extend, cut, deepen, shorten or review an existing SDD, including every follow-up edit in the same session (also in Vietnamese, e.g. "viết SDD", "sửa SDD", "thiết kế hệ thống"). The next step is the docs-master-plan skill.
argument-hint: "[path to SDD] [idea or change request]"
license: MIT
---

# Write and revise an SDD

An SDD answers **what the system does, why it is designed this way, and how the core mechanisms work**. The core must be deep enough for a reader to trust the design (key SQL, state machines, races, rejected options). Secondary parts need only enough to show they exist and how they connect to the core. Detailed specification (complete DDL, every endpoint, every screen) belongs to the doc set produced later by `docs-master-plan` and `docs-project`.

`<skill-dir>` in commands below is the directory containing this SKILL.md. Scripts need Python 3.10+.

References:

- [references/language.md](references/language.md): asking for the output language and using the vocabulary.
- [references/structure.md](references/structure.md): the sections, what each contains, variants by project type. Read before writing a new SDD.
- [references/style.md](references/style.md): style, Mermaid rules, presentation patterns (invariant table, races, options analysis, failure table, experiments). Read before writing or editing content.
- [references/revision.md](references/revision.md): the per-revision procedure, request types, the **propagation table**, the consistency checklist. Read before the first revision.
- `locales/<code>.md`: vocabulary per language (`en`, `vi`, `ja`, `zh`, `ko`, `fr`, `es`, `de`), including the `sdd.*` section headings and the number/date conventions.
- `scripts/check_sdd.py <file> [--outline] [--vocab FILE]`: checks section numbering, section references in any shipped language, FR/NFR/UC/EXP IDs, code fences, Mermaid labels.

If the user points to an earlier SDD they like, read the relevant parts to match its depth and voice; where it and the references differ in voice, follow the user's example.

## Choose the mode

- The target SDD file does not exist → **Write**.
- The file exists, or the user asks to change / add / remove / deepen / shorten / review → **Revise**.
- After the first turn, **every further request about the SDD in this session is a revision**; do not reload the skill. Each turn still re-reads the file before editing.

Default file name: `<project-slug>-sdd.md` at the root of the current repository (or the folder the user names).

## Write

### 1. Ask the output language (always)

Before anything else, ask which language the SDD should be written in (`language.md` §1), even if the user's message makes it look obvious. Offer the language of the user's messages first, then English, then other likely languages; "Other" accepts any language. Load `locales/<code>.md` if it exists; otherwise translate the `sdd.*` keys of `locales/en.md` yourself and use them consistently (the master plan will record the full vocabulary later).

### 2. Gather

From the message, attached files, notes or documents the user points to. Nine things are needed:

1. What the system does, for whom, in which domain.
2. Project type: academic/research, or a product built in phases.
3. The core problem (or research question) and the most important invariant.
4. A target scale scenario with numbers.
5. The modules and which one is the core.
6. Scope: this phase, later, out of scope.
7. Constraints: people, time, target machine, deployment environment, mandatory external services.
8. Technology preferences, if any.
9. Author name (default: the git user name).

Whatever can reasonably be inferred is proposed and recorded as an assumption. Ask only what changes the design: put these questions in the same AskUserQuestion call as the language (at most 4 questions in total, each with a recommended option), or ask a short list in the chat when the answers need free text.

### 3. Outline for approval

Unless the user said to write straight away or the input is already detailed, send a short outline in the chat first:

- the name and a draft lead paragraph;
- the core problem (one sentence) and the top invariant;
- the investment-by-module table;
- the sections, one line each saying what it will contain (core sections name the mechanisms and options to analyze);
- the important assumptions.

Update the outline with the user's changes before writing.

### 4. Write

- Write the file skeleton first (header, every heading, in the output language), then fill one section at a time with Edit. Never dump the whole document in one write.
- Fill order: section 2 → 3 → 4 → core domain sections → other domain sections → data, API, UI → operations, testing → plan, risks, appendix → **section 1 and the lead paragraph last**, so they match what was designed.
- For each core section, answer before writing: what is the invariant and where is it enforced; which two flows can race and who arbitrates; what happens with a repeated request, a process dying midway, a slow or failing external service; where time and clocks come from; at which scale a naive mechanism breaks; which obvious option was rejected; which EXP verifies it. The answers become the section.
- Behavior of external services (payment APIs, SDKs, quotas): never guess. Check the official documentation when a tool allows it; otherwise list it under "Open points".
- Depth follows table 2.2: "Deep" gets diagrams, SQL/code, rule tables, edge cases; "Basic" gets a few paragraphs.

### 5. Check and report

- Run `python3 <skill-dir>/scripts/check_sdd.py <file>` and fix every E error.
- Walk the consistency checklist (`revision.md` §4).
- Short report: file path, number of sections and diagrams, assumptions used, the "Open points", and 2–3 suggested directions for the next round (deepen option X, add an experiment for claim Y, clarify race Z). Do not paste the document into the chat.

## Revise

Follow [references/revision.md](references/revision.md) §1 for **every** request:

1. Re-read the relevant sections of the file (it may have been edited by hand).
2. Classify the request; propose concrete directions for vague ones.
3. List affected places with the propagation table and `grep`.
4. Edit minimally, keep the language, the style and the section numbers, update every reference.
5. Run check_sdd.py.
6. Report: what changed where, what changed with it, what the user must decide.

First revision of a file not yet read in this session: read the whole file, run `check_sdd.py --outline`, then act on the request. With no specific request, summarize the current state (outline, check results, sections thinner than their investment level, inconsistencies) and propose what to change. The language of an existing SDD is kept; do not ask for it.

Do not commit unless the user asks (commit convention in `revision.md` §5).

## When the SDD is stable

Suggest the next step: `/docs-master-plan <file>` to build the decision register and master plan, then `/docs-project` to write the doc set.
