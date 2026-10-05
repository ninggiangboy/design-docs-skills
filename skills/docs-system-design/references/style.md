# Style and presentation patterns

Examples below are in English to show structure and depth. Write the SDD in the output language, following the Conventions section of its vocabulary file (number and date formats, punctuation, register). Never copy example sentences; write new ones about the actual system.

## 1. Writing style

- Technical terms stay in English when the local term is awkward (reservation, webhook, consumer lag); names from code, tables, columns, endpoints and configuration go in backticks.
- Short, active, assertive sentences. No hedging ("could consider", "might want to"), no marketing ("powerful", "optimal"), no filler.
- **Every claim carries its reason or consequence.** "`SKIP LOCKED` never waits for a lock, so there is no deadlock and losers return immediately."
- **Concrete numbers** instead of adjectives: 10 minutes, 3 links per email per 15 minutes, p95 under 500 ms, 20,000 seats.
- **Say what is not done** and why: "No model is used for bunching or ETA: they are plain statistics; a model would only be slower, cost more and be harder to verify."
- Every level-2 section (and important level-3 sections) opens with **one sentence stating the governing rule**, before any detail.
- Lists with bold leads: `- **Point.** Explanation.` or `- **Point** — explanation.` Pick one form for the whole document.
- Internal references use the vocabulary's `ref.section` form (`section 8.4`, `mục 8.4`, `8.4 節`…) or `§8.4`. Requirements are referenced by ID: `NFR-03`, `EXP-10`. Do not use DR/ADR/DOC IDs in a new SDD; they belong to the doc set produced later.
- External sources (engineering articles, standards) are cited with a Markdown link in the sentence that uses them.
- No emoji. No all-caps sentences, except an invariant isolated for emphasis (`NEVER OVERSELL`).

## 2. Mermaid diagrams

- Every diagram is Mermaid so it renders on GitHub and in editors. ASCII is only for a short pipeline sketch or the text version of a figure.
- **Always quote node labels**: `A["Hold seats (SKIP LOCKED)"]`. An unquoted label containing `()[]{}` breaks the diagram.
- Quote edge labels too: `A -- "webhook" --> B`, `A -. "only to shed load" .-> B`.
- Labels are in the output language, short, and state a role rather than only a name.
- Pick the type by content:

  | Content | Type |
  | --- | --- |
  | Architecture, components | `flowchart TD` with `subgraph` |
  | Business flow with decisions | `flowchart TD` with `{"…?"}` nodes and edges `-- Yes -->` / `-- No -->` |
  | Interaction over time, races, retries | `sequenceDiagram` with `par`, `alt`/`else`, `loop`, `Note over`, `autonumber`; a lost message as `--x` |
  | Entity lifecycle | `stateDiagram-v2`, transition labels are the triggering events; `note right of` for intermediate states |
  | Data model | `erDiagram` with relation labels |
  | Use cases | `flowchart LR`, actors `(["…"])`, use cases grouped by `subgraph` |
  | Plan | `flowchart LR`, a dashed edge to "Later" |

- Each diagram has at least one sentence saying what the reader should see in it. A diagram never replaces a rule table: a lifecycle always has both a `stateDiagram` and a transition table.

## 3. Reusable patterns

### Invariant table

```markdown
| Object | Invariant | Enforced by |
| --- | --- | --- |
| Reservation | Leaves `ACTIVE` exactly once | `UPDATE … WHERE status = 'ACTIVE'` |
```

### Conditional write with explanation

````markdown
```sql
UPDATE login_token SET used_at = now()
WHERE token_hash = :hash AND used_at IS NULL AND expires_at > now();
```

Exactly one request wins: a later request sees `used_at` already set and updates 0 rows.
````

SQL comments say how to read the result: `-- The updated row count must equal :qty. Fewer: ROLLBACK and return 409.`

### Race between two flows

1. A sentence naming **the arbiter** ("the `reservation` row is the only arbiter").
2. Numbered steps of each flow, including error and timeout branches.
3. A `sequenceDiagram` with `alt` per outcome.
4. A closing paragraph explaining why no gap remains, and which section holds the last safety net.

### Options analysis

```markdown
### 10.3 <Problem>: options and rationale

Option D is chosen: … Options A, B and C were considered first; this section records their pros and cons and why they were rejected.

**The problem.** <One or two sentences on what is hard, with a diagram if it helps.>

#### Option A: <name>
<How it works, with code if needed.>
- **Pros**: …
- **Cons**: …
- **Verdict**: …

#### Option D: <name> (chosen)
…

#### Comparison and rationale

| Option | <Criterion 1> | <Criterion 2> | Complexity | Verdict |
| --- | --- | --- | --- | --- |

1. **<The top requirement eliminates which options first>.**
2. **<Of the rest, only one removes the root cause>.**
3. **<The cost of the chosen option is small in this problem because…>.**
4. **The choice is verified by measurement**: EXP-xx.
```

A rejected option that is still correct becomes the **baseline** of an experiment.

### Parameter table

```markdown
**Parameters** (per event; values are proposed defaults, tuned in EXP-05)

| Parameter | Default | Meaning |
| --- | --- | --- |
| `max_active` | 500 users | Maximum number of users inside the booking area at once |
```

Add a back-of-the-envelope example showing how the parameters interact.

### Failure table

```markdown
| Failure | Detection | System behavior | Recovery |
| --- | --- | --- | --- |
| PostgreSQL unavailable | Connection errors | Every write returns 503 | Resumes when the database is back |
```

Precede it with the principle: when something fails, which side the system leans to.

### Experiments

```markdown
| ID | Experiment | Method | Metrics | Expected |
| --- | --- | --- | --- | --- |
| EXP-01 | Contention on one seat | 10,000 concurrent requests hold seat A1 | Successful holds; seats with two owners | Exactly 1 success; 0 double-sold seats |
```

Expectations are numbers. An exploratory experiment says "comparison report, no expectation set in advance".

### UI figure with a text version

````markdown
&#91;embedded content: <description of the figure>\]

<One caption sentence: what state the figure shows.>

<sdd.text_version> (`>` marks the selected item):

```
+-----------------------------+
| ASCII only, at most 90 wide |
+-----------------------------+
```
````

The ASCII box uses only ASCII characters (no diacritics, no full-width characters) so it aligns in every editor.

### Formula

Write it in a `latex` code block, then explain each case in words (N = 1, curved paths, …).

## 4. Reference lengths

| Part | Research pipeline (thesis) | Ticket booking (product) |
| --- | --- | --- |
| Whole SDD | ~790 lines, 15 sections | ~1,620 lines, 17 sections, 28 diagrams |
| Core section | ETL: ~60 lines plus tables | Inventory: ~200 lines; load handling: ~280 lines |
| "Basic" section | 5–15 lines | 5–15 lines |

Length follows the investment level of table 2.2, not an even split.
