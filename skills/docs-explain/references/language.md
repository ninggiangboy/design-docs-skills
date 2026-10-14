# Output language

Shared by `docs-system-design`, `docs-master-plan` and `docs-project`. Everything the skills write for the user (SDD, decision register, master plan, docs) uses one **output language** per project. The instructions in the skills are English; the output is not necessarily English.

## 1. Choosing the language

The output language is chosen **once per project, on first use**:

| Skill | Choose when | Record in |
| --- | --- | --- |
| `docs-system-design` | Creating a new SDD | The SDD itself is written in that language; no other record |
| `docs-master-plan` | Creating the plan | Master plan §0 "Language" (§3 below) |
| `docs-project` | Only when the master plan has no "Language" block (older plan) | Add the block to master plan §0, then continue |

Never choose again once the master plan records a language. Revising an existing SDD keeps its language without asking.

Look at the language of the user's messages and, for the master plan, the language of the SDD:

- **All English** (the user writes in English and the SDD, if any, is in English): write in English and do not ask.
- **Anything else** (the user writes in another language, or the SDD is in another language even if the user writes in English): ask with one AskUserQuestion (other questions of the same skill may go in the same call):
  - Question: "Which language should the documents be written in?"
  - Options: the non-English language first (the SDD's language, then the user's if different), then English. "Other" still lets the user type any language.

**Code, logs, API error codes, commits and PR titles are always English.** Never ask; record it in the Language block.

**UI language** (master plan only, when there is a UI) is a product choice, not the documents' language. Infer it from the SDD: who the end users are, which country or market, whether several languages are needed. When the SDD makes it clear, record it without asking. When it does not, ask in the same AskUserQuestion call ("Which language will the UI show to end users?"): the most likely language from the SDD first, then English, then "Several (i18n)"; when everything is English and the SDD gives no hint, assume English and note it as an assumption instead of asking. With several UI languages, record the list and the default one; how i18n is done is a DR in the register.

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
| Code, logs, API error codes, commits, PR titles | English |
| UI (strings shown to end users) | Tiếng Việt · from SDD §3.1 (users in Vietnam) |
| Decided | 2026-10-05, Owner |
```

For a generated vocabulary write `vocabulary: Appendix B`. Labels in the left column are written in the output language. Also add a line to the decision log ("Documents in <language>; UI in <language>; code in English"). Changing the language later is a decision: new decision-log line, update the block, and do not translate approved documents unless the Owner asks.

## 4. Writing in the output language

- All prose in the output language, following the Conventions of the vocabulary file.
- Keep widely used English technical terms when the local term is awkward or rare; be consistent and add them to the glossary.
- UI strings shown in documents are quoted in the UI language; log messages and error codes in English.
- Examples in the references are illustrations of depth and structure, not text to copy; write new sentences in the output language.
