---
name: docs-master-plan
description: Turns a system design document (SDD) into a decision register (docs/00-decision-register.md), a gated master plan (docs/00-master-plan.md) and a docs index (docs/README.md). The master plan lists every document to write with its required content and gate, every task by phase with acceptance criteria, and a traceability matrix; the register turns every gap in the SDD into a decision with a proposed option. Asks for the output language on first use and records it in the plan. Use when the user wants a master plan or decision register from an SDD, to analyze an SDD for gaps, to prepare the doc set of a new project, or to apply the Owner's decisions afterwards (also in Vietnamese, e.g. "lập master plan từ SDD", "phân tích SDD", "tạo sổ quyết định"). The next step is the docs-project skill.
argument-hint: "<path to SDD> | apply-decisions"
license: MIT
---

# SDD → decision register + master plan

Input: one SDD at the repository root (the **original SDD**). Outputs, in order:

1. `docs/00-decision-register.md`: every place where the SDD does not say "exactly how", each as a DR with one proposed option.
2. `docs/00-master-plan.md`: documents to write (required content, gate), roadmap, tasks per phase, traceability, conventions, templates.
3. `docs/README.md`: index and status table.

This skill does **not** write the DOC-xx documents; that is the `docs-project` skill.

`<skill-dir>` in commands below is the directory containing this SKILL.md. Scripts need Python 3.10+.

References (read before writing the matching part):

- [references/language.md](references/language.md): asking for the output language, vocabulary, the plan's Language block. Read first.
- [references/conventions.md](references/conventions.md): identifiers, header block, statuses, decisions, style.
- [references/decision-register.md](references/decision-register.md): register skeleton and the **gap-hunting checklist**.
- [references/doc-catalog.md](references/doc-catalog.md): standard documents, when to include each, required content, default gates.
- [references/master-plan.md](references/master-plan.md): master plan skeleton, section by section.
- [references/templates.md](references/templates.md): templates A.1–A.8 for Appendix A and B.6 for the README.
- `locales/<code>.md`: vocabulary per language (`en`, `vi`, `ja`, `zh`, `ko`, `fr`, `es`, `de`).
- `scripts/check_docs.py [docs_dir] [--vocab FILE]`: checks IDs, links, status lines.

## Modes

- `/docs-master-plan <sdd.md>`: create (steps 1–7).
- `/docs-master-plan apply-decisions`: the Owner has answered the DRs → step 8.

## Procedure

### 1. Pre-checks

- No SDD path given: look for a large `.md` at the repository root whose title is "… — System Design" or its translation; ask if unsure.
- `docs/00-master-plan.md` or `docs/00-decision-register.md` already exists: **do not overwrite**. Ask whether to revise the existing files or stop.
- Every header date is today.

### 2. Read the whole SDD

Read it all, not skimming; read long files in chunks to the end. Keep a scratch **project profile** (in the session scratchpad, not in the repo):

- Goal, research question or main value; which part is the core that must not be cut.
- Users and roles; FRs and NFRs (keep the SDD's IDs if it has them).
- Components, data stores, channels (API, broker, files), external systems.
- UI? AI? experiments? academic report? target environments?
- Plan, cut order and risks the SDD already states.
- Every domain noun (input to the glossary's minimum term list).
- The SDD's language.

### 3. Ask (one AskUserQuestion, at most 4 questions)

Always ask, even if the answers look obvious:

1. **Output language of the documents** (`language.md` §1): the SDD's language first, then English, then other likely languages; "Other" accepts any language.
2. **Language of code, UI strings, logs, commits**: default English.

Ask only when not inferable:

3. Scope: build everything, or known cuts.
4. While writing docs later, may Claude decide small questions itself (recorded as `dr.delegated`)?

Every other technical choice is **not** asked: it goes into the register as a proposal.

Then load the vocabulary: `locales/<code>.md` when shipped; otherwise build it by translating `locales/en.md` (`language.md` §2) for Appendix B of the plan.

### 4. Write the decision register

Follow `references/decision-register.md`. Walk the SDD section by section with the gap-hunting checklist, reading closely enough to catch contradictions inside the SDD. Each DR has a proposed decision **concrete enough to code from** (DDL, JSON, tables, defaults with units). Mark ⚠ when it deviates from the SDD, 🔬 when it needs a spike. Each DR has a "Write to" line pointing to DOCs/ADRs that will exist in the plan. End with "Summary by impact". Document status `Review`; every DR `Proposed`. The first decision-log line records the language choice.

Long file: write the skeleton first, then add one group at a time with Edit; never dump the whole file in one write.

### 5. Write the master plan

Follow `references/master-plan.md`, using `references/doc-catalog.md` to choose documents. Order: §0 with 0.1 Language → §1 (from the register) → §3 (tree and project-specific required content) → §4 → §5 → §6 → §2, §7, §8, §9 → Appendix A (templates rendered in the output language) → Appendix B when the vocabulary was generated.

Cross-checks that must hold:

- Every DR "Write to" points to a DOC in the §3.1 tree or an ADR in the ADR table.
- Every architecture-level DR has an ADR; every ADR has a source (DR or SDD §).
- Every 🔬 DR has a spike `S-xx` in Phase 0.
- Every phase has a `Pn-00` doc gate listing exactly the DOCs/ADRs gated by Pn, and checkable exit criteria `Mn`.
- Every task points to the DOC holding its design; every design DOC is used by at least one task.
- §6 has every FR and NFR; every FR has tasks and a verification.
- Phase 0 has "Write DOC-…" tasks in this order: glossary → product → architecture + P1 ADRs → data → foundation ops docs.

### 6. Write `docs/README.md`

Template B.6, in the output language. Every DOC is "Not written" (`readme.not_written`).

### 7. Check and report

- Run `python3 <skill-dir>/scripts/check_docs.py docs`. Fix every E2 (broken link) and every E1 for IDs the plan or register defines (`DR-`, `DOC-`, `Pn-`, `S-`, `UC-`). E1 for IDs that unwritten documents will define (`FR-xx.y`, `EXP-`, `E-`, `RB-`…) is expected at this stage. The I1 line "DOC … without a file yet" is informational.
- Re-check the cross-checks of step 5.
- Short report: number of DRs (how many ⚠, how many 🔬), the 5–8 heaviest gaps, counts of DOCs/ADRs/phases/tasks, the P1-blocking DRs the Owner should read first, the recorded language. Next step: the Owner reviews the DRs (accept all, or name the ones to change), then `/docs-master-plan apply-decisions`; after that `/docs-project`.

Do not commit unless the user asks.

### 8. `apply-decisions`

When the Owner answers:

- Each decided DR: append `— **<dr.decided>**` (or `**<dr.decided>: <choice>**`) to its title; a changed DR: write the new option in the Decision field and keep the old one as "*<dr.changed> YYYY-MM-DD:* …".
- Add decision-log lines (date, decided by, content, affected items). A bulk acceptance is one line: "Accept all remaining proposals".
- Propagate decisions into the master plan (§1.2, §1.3, required content, tasks, risks) when they change them.
- When every P1-blocking DR is decided and the Owner approves the plan: the plan becomes `Approved v1.0` and task P0-01 is marked done.

All of this is written in the output language recorded in §0.1.
