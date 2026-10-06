# Briefing and answering

How to turn the docs set into a brief and into answers a developer can code from. Headings below are English; the brief is written in the developer's language (SKILL.md §Language).

## 1. Where each kind of answer lives

The single-source-of-truth rule (`conventions.md` §7) says where to look first. Search there before anywhere else; a match elsewhere that disagrees is a conflict to report.

| The developer asks… | Look first in | Then |
| --- | --- | --- |
| What does this word mean? | Glossary | The DR or DOC its "Related" column names |
| What exactly must I build? Is it done? | The task row in master plan §5 (task, output and acceptance, documents) | Requirements `FR-xx.y` acceptance criteria; the screen's acceptance criteria; required tests of the design documents |
| Which requirement or use case is this for? | Traceability matrix (master plan §6) | Requirements FR → UC → F → DOC matrix; use case "Related" line |
| What happens, step by step? | Detailed flow `FL-xx` (sequence diagram, step table) | Use case main/alternative/error flows; data flows for cross-container paths |
| What does the endpoint take and return? | API endpoint catalog `E-xx` | API guidelines (pagination, errors, time format, idempotency) |
| Which table, column, index? | Data documents (DDL) | The endpoint's "Data source"; the flow's step table |
| What is the default / which key? | Configuration reference | The design document's configuration section (must match) |
| What error code, status, message? | Error handling; the flow's "Errors and handling" table | The endpoint's errors; ui-states-and-copy for the message |
| What does the screen show, in which state? | The screen file (`08-ux-ui/screens/`) | ui-states-and-copy; design system for components and tokens |
| Who may do this? | Security: endpoint × role matrix | The screen's permissions section; DB roles and grants |
| What must be logged or measured? | Observability (metric catalog, required log fields) | The design document's metrics section |
| Why was it designed this way? | The DR (Problem, Options, Consequences) | The ADR (Options considered, Consequences); original SDD options analysis |
| What happens on concurrency, crash, retry? | The flow's "Transactions and concurrency"; the design document's concurrency section | Data flows (commit and ack points); quality attributes |
| How do I run, seed, test it locally? | Local dev | Test strategy (tools, naming, fixtures, which CI stage) |
| Is it in scope? When? | Feature catalog (phase, MoSCoW, flag) | Vision and scope (out of scope with reasons); master plan cut order |

When a project has no such document (no UI, no configuration reference yet), say so and fall back to the next source, marked accordingly.

## 2. Expanding each entry point

Start from the `context.py` output, then read in this order. Stop expanding when a branch leaves the scope of the item (a neighbouring feature, another phase).

| Entry | Read |
| --- | --- |
| Task `Pn-xx` | Its row (acceptance, depends on, documents) → the gate task `Pn-00` → the FRs that list the task in the traceability matrix and their acceptance criteria → the UCs of those FRs → every `FL-xx` of those UCs that the task's documents contain → the endpoints, tables, screens and configuration keys named in those flows → required tests whose IDs appear in the matrix's Verification column → the DRs on that path |
| Feature `F-<GROUP>-xx` | Its row in the feature catalog (FRs, UCs, phase, flag, dependencies) → the tasks of that phase that cover its FRs → then as for a task |
| Use case `UC-xx` | The UC (main, alternative, error flows, rules) → its `FL-xx` (each alternative and error flow should be an `alt` branch) → endpoints, screens, tables → FRs and their acceptance criteria → the tasks that implement it |
| Flow `FL-xx` | The section: participants, sequence diagram, step table, transactions, errors, required tests → each `E-xx` and table it names → its UC and screen → decided and proposed DRs it cites |
| Endpoint `E-xx` | Its section (authorization, parameters, response, errors, data source, cache, performance) → API guidelines → the flows and screens that call it → security matrix row → the task that implements it |
| Screen (file or words) | The screen file (§5 data with `E-xx`, §6 interactions, §7 states, §9 acceptance criteria) → each endpoint → the flows that start from it → ui-states-and-copy entries → the task in the "Main readers" line |
| `DOC-xx` | The header (depends on, main readers), the tasks whose Documents column names it, its open questions |
| `DR-xx` / `ADR-xxxx` | The decision in full → its Write to targets → where it is cited (flows, design sections) → whether it was revised later |

## 3. Brief skeleton

Render headings in the developer's language. Drop a section that has nothing to say for this item, except Readiness and gaps, which is always present.

```markdown
## <ID> · <title>

**Verdict:** ready | ready with risks | blocked — <one line why> · Phase n · Gate Pn-00 <state>

### What and why
2–4 sentences: the user-visible result, the FR/UC it serves, the value. (FR-…, UC-…)

### Done means
- The task's acceptance, verbatim. (master plan §5, Pn-xx)
- Acceptance criteria by ID: FR-xx.y, the screen's IDs (SM-01…), verbatim or tightly summarized.
- Required tests to make pass: H-01, H-02… with their expected results.

### Read first
Ordered, at most ~6: `DOC-xx §n` — what it gives you. Status of each.

### How it works
The main flow as numbered steps from the user's action to the data store and back (FL-xx steps), the transaction boundaries, the arbiter in races, then each error branch as one line: condition → status/code → what the user sees.

### Contracts
- Endpoints: `METHOD /path` (E-xx), key request and response fields, error codes.
- Data: tables and columns touched, constraints and indexes that matter. (DOC-xx §n)
- Configuration: `key` = default (unit). Metrics and log fields to emit.
- UI: states, exact strings.

### Rules and edge cases
Business rules, invariants, idempotency, permissions, limits, time zones — each with its source.

### In the code
Exists / to create, with paths; the existing implementation to copy the pattern from; architecture rules that apply.

### Readiness and gaps
Each blocker or gap: what, where (`path:line`), who closes it (Owner decides DR-xx · `/docs-project DOC-xx` · task Pn-xx lands · ask <role>).

### Suggested order (optional)
3–6 steps, each ending with the test that proves it.
```

Example of the right density for one "How it works" step: "3. `HoldService.hold` runs the conditional `UPDATE seat SET status='HELD' … WHERE status='FREE'`; 1 row → insert `hold` and commit T1; 0 rows → roll back and throw `SeatTakenException` → 409 `seat-taken` (FL-01 step 4, DR-01)." Not: "The service checks whether the seat is available and handles conflicts appropriately."

## 4. Answer format

```markdown
<Direct answer in 1–3 sentences.>

<Evidence: the quote or summary, each with its source. For "how", numbered steps. For "why", the DR's problem and the options rejected with their reason.>

<Caveats, only when they apply: ⚠ from a Draft document / Proposed DR — may change · ⚠ docs disagree: A (source) vs B (source); A wins because … · ⚠ code differs from docs: path:line.>
```

Kinds of statements, always distinguishable in the answer:

| Kind | Meaning | How it is written |
| --- | --- | --- |
| Specified | A document says it | Statement + `(source)` |
| Derived | Follows from specified items | "Inference:" + the chain of sources |
| Not specified | No document says it | "Not specified" + where you looked + options + marked recommendation |

Good: "The hold lasts 10 minutes (`booking.hold-ttl`), but only as a proposal: DR-02 is still Proposed, so the value may change; read it from configuration, do not hard-code it (DR-02, FL-01)."
Bad: "Holds usually last around 10–15 minutes." (no source, invented range, hides that the decision is open)

## 5. Code mapping

- Use the names the docs give (class, method, table, route, key) as search terms; fall back to the glossary term and its English code name.
- Report each as `exists path:line`, `to create`, or `exists but differs` (the docs say `holdTtl`, the code has `HOLD_MINUTES = 15` → drift).
- For "to create", point to the closest existing sibling (`OrderController` for a new controller) and the rules from `code-architecture.md` (layer, package, naming, where the transaction lives).
- Never propose code that contradicts a decided DR or ADR; if the developer wants to deviate, that is a new decision (§6).

## 6. Gaps

| Gap | Found by | Closed by |
| --- | --- | --- |
| ID referenced but undefined (`E-02`) | `context.py` `GAP undefined` | `docs-project` adds it to its source document |
| Proposed DR on the path | `GAP proposed`, `READY block DR-xx` | The Owner decides it |
| Non-empty open questions | `GAP open-questions` | The Owner decides the DR behind it; `docs-project` updates the document |
| Document Draft/Review/not written | `GAP not-approved`, `GAP not-written`, `READY block DOC-xx` | `docs-project` finishes it; the Owner approves |
| Missing behavior: an error flow without handling, a default without a value, a state without a screen state | Reading (the script cannot see these) | A proposed DR + an open question |
| Contradiction between documents | Reading | The higher-priority source wins; `docs-project` fixes the other |
| Drift between docs and code | Code mapping (§5) | Fix the code, or record a DR that changes the docs, same PR (Definition of Done) |

For each missing behavior, give the developer a way forward without deciding for the project: the options, the recommended one marked "recommendation, not decided", and what to do meanwhile (put it behind configuration, write the test with the value as a parameter, leave a `TODO(DR-xx)` comment if the code conventions allow it).
