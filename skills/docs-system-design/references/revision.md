# Revising an SDD over many turns

A good SDD takes shape over many rounds of conversation. Every revision must leave a document that is **consistent end to end**, not only correct where it was just edited. The most common failure when revising iteratively: a decision changes in a core section while the NFR table, architecture diagram, failure table, experiments, plan and risks still describe the old decision.

## 1. Every revision

1. **Re-read the current state.** The user may have edited the file by hand between turns. Always re-read the sections you will touch (and run `check_sdd.py --outline`); never rely on the version in memory.
2. **Classify the request** with the table in §2. For a vague request ("too bland", "not deep enough", "make this section better"), propose 2–3 concrete directions and ask, or pick the most sensible one and say which.
3. **List every affected place** using the propagation table in §3 plus `grep` for the old decision's keywords (table names, states, numbers, technology names, FR/NFR/EXP IDs).
4. **Edit minimally.** Change only the paragraphs that must change; do not rewrite unrelated sections or restyle parts the user already approved. Rewrite the whole file only when the user asks for a restructure.
5. **Keep section numbers and IDs stable.** Prefer appending a new subsection at the end of its parent. When inserting or deleting in the middle is unavoidable, renumber and update **every** section reference. FR/NFR/UC/EXP IDs never change number; a removed ID is deleted with all its references, a new one takes the next number.
6. **Keep the language.** The SDD's language stays; never switch language because the user wrote the request in another one.
7. **Run** `python3 <skill-dir>/scripts/check_sdd.py <file>` and fix every E error.
8. **Report briefly**: what changed in which section, what had to change with it (propagation), and what is still open or contradictory and needs the user's decision. Do not paste the written content back into the chat.

When a request contradicts an invariant or an earlier decision (for example "let Redis hold the ticket count" while the invariant is never overselling): state the contradiction and its consequence, propose a way to reach the user's goal without breaking the invariant, and wait for the user's choice.

## 2. Request types

| Type | Example | How |
| --- | --- | --- |
| Change a decision | "Use Kafka instead of RabbitMQ", "hold tickets for 15 minutes" | Edit where it is defined, then propagate via §3. For a large decision consider adding an options analysis |
| Add a module or feature | "Add refunds", "add ticket scanning" | Ask its investment level (2.2) and phase (in scope or later). If in scope, follow the "Add a module" row of §3 |
| Remove or defer | "Move the waiting room to Later" | Move it to the "Later" table with its "How this phase handles it" column; remove it everywhere else |
| Go deeper | "Analyze more options for the inventory" | Use the options-analysis pattern; add a comparison EXP when the claim needs numbers |
| Shorten | "The editor section is too long" | Keep rules, invariants, decisions and reasons; drop implementation detail that belongs to the later docs |
| Presentation | "Add a diagram", "make it a table" | No content change; check the diagram matches the text |
| Review comments | A list of remarks | Handle each remark; report per remark: fixed where / not fixed and why |
| Consistency pass | "Check everything again" | Run check_sdd.py, then read through the checklist of §4 |

## 3. Propagation table

When the left column changes, check every place in the right column.

| Change | Check |
| --- | --- |
| Scope (add, remove, defer) | Lead paragraph, 1.3 Vision, 2.2, 2.3, use cases, FRs, NFRs, 4.1, architecture diagram, affected domain sections, data model, API, screens, deployment, experiments, plan and cut order, demo, risks, repository appendix |
| Add a module | 2.2 (investment), 2.3, use cases, FRs/NFRs, 4.1, architecture diagram, 4.3 technology, the new domain section, entities and constraints, endpoints, screens, deployment containers, failure table, tests/EXPs, plan stage, risks, repository appendix |
| Technology / infrastructure | 4.3, architecture diagram, 4.1, every domain section naming the old technology (grep), deployment, failure table, testing tools, risks, repository appendix, open points |
| Core mechanism (how correctness is ensured) | Core domain section, 4.2 principles, invariant table, state machines and transition tables, data constraints, API error codes, failure table, invariant checks, EXPs and baselines, risks |
| Lifecycle / states | `stateDiagram`, transition table, every SQL statement using the state names, constraints and partial indexes, API (returned states), UI (display), background jobs, invariant checks |
| A number (timeout, threshold, load target) | Every place with that number (grep every form: `10 minutes`, `10 phút`, `600`), NFRs, parameters, worked examples, EXPs, demo, risks, open points |
| Roles / permissions | 3.1, use cases, permission table, endpoints, screens, security |
| Entity / table | erDiagram, entity table, constraints, SQL statements, endpoints returning it, repository appendix (module) |
| Endpoint | Endpoint table, request/response examples, error table, flows that call it (sequence diagrams), screens |
| Experiment | EXP table, the "which EXP proves what" paragraph, NFRs naming EXPs, domain sections naming EXPs, plan (which stage produces which EXP) |
| Plan stage | Dependency diagram, stage table, cut order, demo, "Later" table |

## 4. Consistency checklist

- The lead paragraph, 1.3, 2.1 and 2.3 describe the same scope.
- Every module of 2.2 has a domain section of the right depth; every component of 4.1 appears in the architecture diagram and the repository appendix.
- Every NFR has a numeric target and at least one EXP or verification; every EXP is produced by some plan stage.
- Every state used in SQL/API/UI exists in its state machine, and vice versa.
- Every technology mentioned in the body is in 4.3.
- The failure table covers every data store and external service in the architecture diagram.
- Every risk has a mitigation pointing to a designed section; "Open points" reflects exactly what is still undecided after this revision.
- check_sdd.py reports no E errors.

## 5. History

- The SDD has no changelog section; history lives in git.
- If the folder is a git repository and the user asks to commit: one commit per meaningful change, subject `docs(sdd): <description in English>` (e.g. `docs(sdd): expand inventory design alternatives and selection rationale`). Never commit without being asked.
- To compare with an earlier version: `git diff -- <file>`, or against a backup the user points to.
