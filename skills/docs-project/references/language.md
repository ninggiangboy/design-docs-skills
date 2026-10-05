# Output language

Shared by `docs-system-design`, `docs-master-plan` and `docs-project`. Everything the skills write for the user (SDD, decision register, master plan, docs) uses one **output language** per project. The instructions in the skills are English; the output is not necessarily English.

## 1. When to ask

Ask **once per project, on first use, even if the language looks obvious** (the user writing in one language does not mean they want the documents in it):

| Skill | Ask when | Record in |
| --- | --- | --- |
| `docs-system-design` | Creating a new SDD | The SDD itself is written in that language; no other record |
| `docs-master-plan` | Always when creating the plan (the SDD language is the first option, not an assumption) | Master plan §0 "Language" (§3 below) |
| `docs-project` | Only when the master plan has no "Language" block (older plan) | Add the block to master plan §0, then continue |

Never ask again once the master plan records a language. Revising an existing SDD keeps its language without asking.

Ask with one AskUserQuestion (other questions of the same skill may go in the same call):

- Question: "Which language should the documents be written in?"
- Options, most likely first: the language of the existing SDD or of the user's messages, then English, then one or two other likely languages. "Other" lets the user type any language.
- For the master plan, ask a second question in the same call: "Which language for code, UI strings, logs and commits?" Default English.

## 2. Vocabulary

Templates and fixed labels (headings, table columns, status labels, "Open questions", "None.") come from a vocabulary file so every document in the project uses the same words.

1. Look for `locales/<code>.md` in the skill directory. Shipped: `en`, `vi`, `ja`, `zh` (Simplified Chinese), `ko`, `fr`, `es`, `de`.
2. **Shipped locale:** read it; use its Conventions section (number and date format, punctuation, register) for all prose.
3. **No shipped locale** (any other language, e.g. `it`, `id`, `th`, `pt-BR`): build the vocabulary yourself by translating every row of `locales/en.md`, keeping keys, the English column and `{placeholders}` unchanged, and writing a short Conventions list for that language. Write it as **Appendix B** of the master plan (`plan.vocabulary`), in the same table format: `| Key | English | <language> |`. When the SDD skill runs before any master plan exists, keep the translated terms consistent within the SDD; the master plan skill writes Appendix B later.
4. The checker scripts read `locales/*.md` and also any vocabulary table in `docs/00-master-plan.md`, so generated languages are checked too.

Rendering rule: a template heading or label written in English (`## Context`, `| Depends on |`) is looked up in the English column and replaced by the value in the output language. IDs (`FR-01`, `DOC-14`), code, SQL, JSON, file names, folder names (`01-product/`) and status values (`Draft`, `Review`, `Approved`, `Superseded`, `Proposed`, `Accepted`) stay as they are in every language.

## 3. The "Language" block of the master plan

Put it in §0 of the master plan, under the `plan.language` heading:

```markdown
### 0.1 <plan.language>

| | |
| --- | --- |
| Documents (`docs/`, decision register, master plan) | Tiếng Việt (`vi`) · vocabulary: shipped `locales/vi.md` |
| Code, UI strings, logs, API errors, commits, PR titles | English |
| Decided | 2026-10-05, Owner |
```

For a generated vocabulary write `vocabulary: Appendix B`. Labels in the left column are written in the output language. Also add a line to the decision log ("Documents in <language>; code and UI in <language>"). Changing the language later is a decision: new decision-log line, update the block, and do not translate approved documents unless the Owner asks.

## 4. Writing in the output language

- All prose in the output language, following the Conventions of the vocabulary file.
- Keep widely used English technical terms when the local term is awkward or rare; be consistent and add them to the glossary.
- UI strings, log messages and error codes shown in documents are quoted in the language chosen for code and UI.
- Examples in the references are illustrations of depth and structure, not text to copy; write new sentences in the output language.
