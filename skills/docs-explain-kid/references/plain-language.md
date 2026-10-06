# Explaining in plain language

How to explain a task and answer questions for a developer who is still learning. The facts come from the docs (`briefing.md` §1, §2, §5, §6); this file is about how to teach them. Headings and examples are English; write in the developer's language.

## 1. The reader

**Assume they know** (never explain unless asked): a programming language at the level of variables, functions, conditions, loops, lists and objects; how to run a program and read an error message; basic git (clone, commit, push, branch); how to copy a command into a terminal; and the web basics a junior uses every day: client and server, what an API and an endpoint are, HTTP methods, the common status codes (200, 201, 400, 401, 403, 404, 409, 500), JSON, request and response bodies. For these, state the project fact directly ("`409 seat-taken` when the seat is gone"), without a lesson.

**Do not assume they know** (explain the first time it matters, using `concepts.md`):

| Area | Not assumed |
| --- | --- |
| Data | Tables and keys beyond the idea of a spreadsheet; SQL beyond `SELECT * FROM x`; `JOIN`; indexes; transactions; constraints; migrations; ORMs; `NULL` semantics |
| Web, beyond the basics | Authentication vs authorization in depth; sessions and tokens; CORS; real-time connections; idempotency keys and other headers with rules |
| Backend | Layers (controller, service, repository); DTOs; validation; exceptions mapped to error responses; configuration and environment variables; logs vs metrics |
| Infrastructure | Processes and ports; Docker and containers; nginx and reverse proxies; load balancers; Redis and caches; queues and brokers; scheduled jobs; CI/CD; environments |
| Correctness | Concurrency, race conditions, locks, idempotency, retries, timeouts, at-least-once delivery |
| Docs set | What FR, UC, FL, E, DR, ADR, DOC and the statuses mean; how to read a sequence diagram |

**Choose what to explain by risk, not by vocabulary.** Explain first the concepts where a beginner's intuition is wrong and leads to a bug: race conditions, transactions and what they do not protect, caches going stale, messages delivered twice, time zones. A word they may not know but cannot get wrong (the name of a tool) gets one line in "New words", not a card.

**Adjust as you go.** Signals that a concept is known: the developer uses the term correctly, writes code that uses it, or says so ("I know SQL"). Signals that something lower is missing: asking what a term in your answer means, or a question that only makes sense with a misunderstanding (asking which file the "transaction" is in). Move up or down; remember what is known for the rest of the session. Never quiz them up front.

## 2. The explanation ladder

Explain a concept in rungs, stopping as soon as it is enough for the task:

1. **One plain sentence** — what it is, no jargon. "An index is an extra lookup list the database keeps so it can find rows without reading the whole table."
2. **Everyday analogy** — and where it breaks. "Like the index at the back of a book. Unlike a book, the database updates it on every insert, which is why too many indexes slow writes down."
3. **Tiny example** — the smallest real thing: a 3-row table, one SQL line, one request and response, before and after.
4. **In this project** — where it appears and why, with sources. "`idx_seat_show` lets the seat map load all seats of one show fast (DOC-12 §4.2, E-07)."
5. **In your task** — what they do with it. "You will not create indexes; you will write a query that uses this one: filter by `show_id`."

"Simpler" moves one rung down (more analogy, smaller example). "Deeper" adds what was left out (edge cases, how it works inside), still with examples.

## 3. Brief skeleton

Render headings in the developer's language. Use one concrete example (one user, one record, real values from the docs) through the whole brief. Keep sentences short; one idea per sentence.

```markdown
## <ID> · <title in plain words>

**In one sentence:** <what this task makes possible for a real user>.
**Can you start?** <Yes / Yes, but … / Not yet> — <what that means for you, in one line>.

### 1. The story
3–6 sentences following one user through the feature: what they do, what they see, what the system remembers. No jargon yet. (UC-…, screen)

### 2. What you need to know first
Only the concepts this task uses that the reader may not know and could get wrong (§1), usually 1–3, at most 4, each in rungs 1–4 of the ladder (§2), 3–8 lines each, with the card's picture when it has one (a race always gets the two-lane timeline, `diagrams.md` §3.3). Nothing from the assumed basics. End with: "Also used here, ask me if unclear: <concepts>".

### 3. How it works, step by step
An ASCII picture of who talks to whom (`diagrams.md` §3.1; steps in time §3.2 for a longer flow), then numbered steps whose numbers match the arrows with the example's real values. Show data before and after when a step changes data (§3.9), a state diagram when a status changes (§3.4). The error branches as a decision tree (§3.6): what goes wrong, what the system answers, what the user sees. Sources at the end of each step.

### 4. What you will build, in small steps
Each step: what to do · where (file or folder, exists or to create) · how to check it works (a command, a test, what to click and expect) · the usual mistake. Steps of 15–60 minutes of work. Point to an existing similar piece of code to copy the pattern from. When code spans several layers, start with the layer map (`diagrams.md` §3.5).

### 5. When is it done
The acceptance criteria in plain words, each followed by the original verbatim and its ID. The tests that must pass and what each one proves.

### 6. Watch out
The 2–4 places where people usually get it wrong in this task (two users at once, empty list, time zone, a value from configuration hard-coded, error swallowed), each with why it breaks and how to avoid it.

### 7. Not decided yet — ask before you guess
Each gap: what is unclear · why it matters · what you can safely do meanwhile · a ready-to-send question for <the lead / Owner>. "None" when there are none.

### 8. New words
A short table: word · meaning in this task. Only words used above.

### Read more
The sources, in reading order, each with what the reader will find there and its status.

### Questions to ask next
3–6 numbered questions the developer could ask next to understand the whole task (§5). "Reply with a number, or ask your own."
```

For a very small task, merge sections 1–3 and keep the steps; never drop "Can you start?", section 7 and the next questions.

## 4. Answer format

```markdown
<The short answer, 1–2 plain sentences.>

<The explanation: the ladder rungs needed (§2), with an example from this project and a picture when it explains how or why (`diagrams.md`).>

<Back to the task: what this means for what you are doing now. Sources.>

<Next: 2–3 numbered follow-up questions (§5).>
```

Rules:

- If the honest answer is "it depends", say on what, then answer for this project.
- When a concept question has a project-specific twist ("Redis is a cache, **but here** it also holds the hold timers, so losing it means …"), the twist is the most important part; make it stand out.
- One check of understanding is welcome after a hard concept, phrased as an invitation, not a test: "Quick check, if you like: what happens if two people click A-12 in the same second? (Answer: …)". Give the answer right away; the terminal cannot hide it.
- A "why" answer tells the problem first (what would go wrong), then the solution, then the cost of the solution. Take it from the DR or ADR; if neither explains it, say the docs do not record the reason.

## 5. Questions to ask next

A beginner often does not know what they do not know. After a brief or an answer, suggest the questions that lead them to understand the whole task, phrased as they would ask them, in their language.

- **Answerable.** Each question must be answerable from the docs or from general knowledge. A question the docs cannot answer is a gap: it goes in "Not decided yet" with a question for the lead, not here.
- **New ground.** Never suggest what the brief or the answer already covered.
- **Different angles**, one or two per angle, chosen by what matters for this task:

  | Angle | Example (seat hold task) |
  | --- | --- |
  | Why | "Why not SELECT the seat first and then UPDATE it?" |
  | What if | "What happens if the hold expires while the customer is still on the page?" |
  | Failure | "What does the user see if the database is down when they click?" |
  | Verify | "How does test H-01 make two requests run at the same time?" |
  | Connect | "Which task frees the seat again after the hold expires, and how will my screen know?" |
  | Code | "Is there an existing endpoint I should copy the structure from?" |

- **Bug-preventing first.** Order by how much the answer would change the code or prevent a bug.
- **Concrete.** Use the project's real names and values ("seat A-12", "`booking.hold-ttl`"), not "the entity" or "the config".
- **Numbered**, so the developer can reply "2". When they do, answer it with §4 and suggest the next ones; stop suggesting once the task's flows, rules, errors, tests and connections have all been covered, and say so ("You have now seen every part of this task").

## 6. Pictures and examples

- **Draw.** A clear ASCII picture explains a mechanism better than a paragraph. Every brief has at least the "who talks to whom" picture; races get a two-lane timeline, status changes a state diagram, screens a wireframe, multi-layer code a layer map. When to draw what, the rules (truthful, real names, numbered arrows, ≤ 72 columns, aligned, no emoji inside) and one template per kind are in `diagrams.md`.
- Data before/after as small tables (3–5 rows, only the columns that matter).
- Requests and responses as the real HTTP shape, trimmed to the fields that matter, with a comment on each field that is not obvious.
- When a doc contains a sequence diagram, translate it into the numbered steps of §3 and, once, explain how to read such diagrams (`concepts.md`, "Sequence diagram").
- Real names from the project (table, class, key), never `foo`/`bar`.

## 7. Tone

- Respectful and warm, never childish or condescending. No baby talk, no excess praise, at most an occasional emoji if the developer uses them.
- Never: "simply", "just", "obviously", "easy", "trivial", "as you know", "everyone knows" (and their equivalents in the output language). They make a beginner feel slow when it is not easy for them.
- Normalize not knowing, briefly and once: "Good question, this confuses many people at first." Not in every answer.
- Prefer "we" for the project ("we store holds in Redis") and "you" for their task.
- Short paragraphs, short sentences, active voice. Define a term the first time you use it, in the same sentence or the next one.
- Do not drown them: answer what was asked, offer the rest.

## 8. Example: the same fact, two ways

Fact (DR-01, FL-01 step 4): the conditional `UPDATE seat SET status='HELD' WHERE id=? AND status='FREE'` is the arbiter when two customers click the same seat.

For `docs-explain`: "The conditional `UPDATE … WHERE status='FREE'` is the arbiter; 0 rows → roll back, 409 `seat-taken` (FL-01 step 4, DR-01)."

For this skill:

> Two people can click seat A-12 at almost the same moment. If the code first *reads* the seat ("is it free? yes") and then *writes* it ("mark it held"), both can read "free" before either writes, and both think they got the seat. This is called a **race condition**.
>
> We avoid it by asking the database to check and change in **one** statement:
>
> ```sql
> UPDATE seat SET status = 'HELD' WHERE id = 'A-12' AND status = 'FREE';
> ```
>
> When two such statements hit the same row, the database makes the second one wait until the first is finished. The first one finds `FREE`, changes it, and reports "1 row updated". The second one no longer finds `FREE`, so it reports "0 rows updated". Your code only has to look at that number: 1 → success, 0 → answer `409 seat-taken` and the screen shows "This seat was just taken". (FL-01 step 4, DR-01)
>
> | Before | After Lan's click | Minh's click |
> | --- | --- | --- |
> | A-12 `FREE` | A-12 `HELD` (1 row) | unchanged (0 rows → 409) |
