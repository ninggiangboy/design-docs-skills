---
name: docs-explain
description: Explains a task, feature, use case, flow, endpoint or screen to the developer who is about to implement it, and answers their questions, from the docs set made by docs-master-plan and docs-project (master plan, decision register, DOC-xx, ADRs) and the code. Builds a task brief: what and why, what done means, what to read first, the flow step by step, contracts (endpoints, tables, configuration, errors), rules and edge cases, where it goes in the code, readiness and gaps. Every answer cites its source; anything the docs do not say is reported as a gap, never guessed, and can be recorded as a proposed DR. Use when a developer starts a task Pn-xx, a feature, a screen or a flow, asks what to do, how something works, why it was decided, where something is specified, or whether a task is ready (also in Vietnamese, e.g. "giải thích task P2-03", "bắt đầu code màn hình…", "tại sao chọn…", "API này trả gì"). Read-only unless the user agrees to record a gap.
argument-hint: "<Pn-xx | F-… | UC-xx | FL-xx | E-xx | screen | words> [question] | ready <Pn-xx | Pn>"
license: MIT
---

# Explain a task to the developer who implements it

The master plan promises that **when a task starts, everything needed is already in the docs**. This skill is where that promise is kept or found broken: it reads the docs for the developer, explains the piece they are about to code, answers their questions with citations, and turns every unanswered question into a visible gap instead of a silent guess.

Precondition: a `docs/` tree with `00-master-plan.md` (made by `docs-master-plan`, filled by `docs-project`). Without it, work from whatever design documents or SDD exist, say that the answers have no plan behind them, and suggest `/docs-master-plan`.

`<skill-dir>` in commands below is the directory containing this SKILL.md. Scripts need Python 3.10+.

References:

- [references/briefing.md](references/briefing.md): where each kind of answer lives, how to expand each entry point, the brief skeleton, the answer format, gap handling. Read before the first brief or answer of a session.
- [references/conventions.md](references/conventions.md): identifiers, statuses, decisions, single source of truth (shared with the other skills).
- [references/language.md](references/language.md): how the docs' language and vocabulary work, needed to read docs written in any language.
- `locales/<code>.md`: vocabularies, used by the scripts to read status lines, DR states and "Open questions" in any shipped language.
- `scripts/context.py [docs_dir] <ID | file | words> [--depth 1|2] [--max N]`: the item's definition, what it references, what references it, second-hop neighbours, task readiness, and gaps (undefined IDs, proposed DRs, open questions, documents not Approved).
- `scripts/check_docs.py [docs_dir]`: the docs checker shared with `docs-project`.

## Modes

| Command | Does |
| --- | --- |
| `/docs-explain P2-03` | Brief for a task: what, why, done means, read first, how it works, contracts, rules, code, readiness, gaps |
| `/docs-explain F-ORD-02`, `UC-04`, `FL-07`, `E-12` | Brief centred on that feature, use case, flow or endpoint |
| `/docs-explain seat-map.md` or `/docs-explain seat map screen` | Brief for a screen (file name or words; ambiguous words → pick from the matches) |
| `/docs-explain P2-03 what happens if the hold expires during payment?` | Answer one question in the context of the item |
| `/docs-explain why do we use SKIP LOCKED?` | Answer a question without an item; find the item first |
| `/docs-explain ready P2-03` / `ready P2` | Readiness only: one task, or every task of a phase |

After the first call, **every further question in the session is answered in this mode**, reusing the context already read; run the script again only for items not yet explored.

## Ground rules

1. **The docs are the source of truth for intended behavior; the code is the source of truth for current behavior.** Priority when docs disagree: master plan → decided DRs → Approved documents → ADRs → Review/Draft documents → original SDD. When docs and code disagree, report both; that is drift, not something to resolve silently.
2. **Cite everything.** Each statement ends with its source: `(DOC-14 §5.2)`, `(DR-21)`, `(FL-07 step 4)`, `(E-12)`, or `path:line` for code. A statement without a source is labelled **inference** and shows the chain it comes from, or it is a **gap**.
3. **Never fill a gap with a plausible guess.** When the docs do not say, write "not specified" and what was searched; then give options with a recommendation clearly marked as *not decided* (`briefing.md` §6).
4. **Flag unstable sources.** Anything from a `Draft`/`Review` document or a `Proposed` DR is marked "may change"; a revised item (`*Revised … (DR-xx):*`) is quoted in its revised form.
5. **Map, don't copy.** Summarize and cite. Quote verbatim only what must be exact: payloads, error codes, configuration keys and defaults, UI strings, acceptance criteria.
6. **Do not re-explain frameworks or standards.** Explain how this project uses them, as the docs do.
7. **Read-only by default.** Edit docs only when the user agrees, and only to record gaps (§Gaps below). Writing or reviewing documents is `docs-project`'s job.

## Language

The brief and answers are a conversation, not a document: write them in **the language the developer writes in**. Quote document text, UI strings and error codes exactly as they appear; IDs, code names and file paths never change. If the developer asks to save the brief, write it where they say, outside `docs/` (which holds only the documents of the plan), in the language they asked in.

## Brief

### 1. Locate

- Find `docs/00-master-plan.md` (also `doc/`, `documentation/`, or ask). Read §0 (language, ID table) and §7 (Definition of Ready and Done) once per session.
- Run `python3 <skill-dir>/scripts/context.py docs <query>`. With free words, the output is `HIT` lines: take the clear winner, or ask with the top 3–4 candidates (one AskUserQuestion).

### 2. Expand

From the script output, follow the expansion for the entry kind (`briefing.md` §2). Read the `SECT` ranges and `ROW`s, not whole files, except short ones. Always read in full: the decided DRs that touch the item, the acceptance criteria, and every `FL-xx` step table involved. Look up glossary terms the developer may not know.

### 3. Look at the code

When the repository has code (skip for a docs-only repository):

- For each participant in the flows (`Code` column), each endpoint path, table, configuration key and screen route: Grep/Glob whether it exists → **exists** (with `path:line`) or **to create**.
- Find the closest existing implementation of the same kind (another endpoint, job, screen) as the pattern to follow, and the code architecture rules (`code-architecture.md` when the plan has it).
- Check the task's dependencies marked Done really exist in the code; a dependency marked Done with nothing in the code is a gap.

### 4. Readiness

Use the script's `READY` lines and master plan §7.1: referenced documents Approved, related DRs decided, dependencies done, acceptance measurable. Report **ready**, **ready with risks** (only Review documents or answers needing confirmation) or **blocked** (with each blocker and who unblocks it: the Owner decides DR-xx, `docs-project` finishes DOC-xx, task Pn-xx lands first).

### 5. Write the brief

Use the skeleton in `briefing.md` §3. Lead with the one-line verdict (ready / ready with risks / blocked). Keep it to what the developer needs to start: about one screen for a small task, more only when the flow is long. Close with the gaps and the questions worth asking, and invite follow-up questions.

## Answering a question

1. Identify the items the question touches (IDs mentioned, the item of the session, or words → `context.py`) and the kind of answer (`briefing.md` §1 says where each kind lives).
2. Read the source. For "why" questions, read the DR (Problem, Options, Consequences) or the ADR (Options considered, Consequences); never invent a rationale.
3. Answer per `briefing.md` §4: the direct answer first (1–3 sentences), then the evidence with citations, then caveats (unstable source, conflict, drift).
4. If the answer is not in the docs: say so, list where you looked, give options with a marked recommendation, and offer to record the gap.

## Gaps

A gap is anything a developer would otherwise have to decide alone: an undefined ID, a proposed DR on the path, a non-empty open question, a missing error flow, an unspecified default, a contradiction between documents, drift between docs and code. List each with its location and the person or skill that closes it (`briefing.md` §6).

When the user agrees to record gaps (only then):

- Add a DR with the next number to `docs/00-decision-register.md` in its topic group, in the output language of master plan §0.1, state proposed, with Problem (where it was found), Options, Decision (proposed), Consequences and Write to. Follow `conventions.md` §4.
- Add the question with its DR ID under "Open questions" of each affected document; its status stays as it is or goes back to `Draft` if it was Approved.
- If the Owner has delegated decisions (decision log) and the user asks to decide it now, record it decided by `dr.delegated` with a decision-log line, and propagate it into the target documents as `docs-project` does; otherwise suggest `/docs-project` for the propagation.
- Run `python3 <skill-dir>/scripts/check_docs.py docs` and fix the errors the change caused.

Do not commit unless the user asks.

## Ready (`ready`)

For one task: the readiness part of the brief only. For a phase `Pn`: run `context.py` on every task of the phase, then print a table `Task · State · Ready · Blockers`, followed by the blockers grouped by who unblocks them (Owner decisions, documents to finish, tasks to land).
