# Writing each kind of document

The source of truth for **required content** is the document's row in master plan §3.2. This file adds what a good document looks like, the depth expected and common mistakes. Skeletons are in `templates.md`; render every heading in the output language.

## General rules

- **Follow the plan's checklist.** Before writing, copy the "Required content" items into a list; each item becomes a section or a table. When done, map every item to the section that covers it.
- **Write so someone else can implement without asking.** The reader is whoever codes the task `Pn-xx` that points to this document. Missing table names, keys, defaults or error codes mean the document is incomplete.
- **Real examples.** JSON with every field, runnable SQL, test tables with concrete numbers. Take numbers from real data when available (write a small script, record its path and the date).
- **Boundaries.** Every document says which parts live in which other document. Never copy another document's content; link to it with `DOC-xx §n`.
- **New decisions.** When a choice is not answered by the SDD or the DRs, create a DR (see SKILL.md). A document that produces many decisions adds a sentence "Every new decision in this document is recorded as … and summarized in §N" and a summary section at the end.
- **Open questions** is the last section of every document except ADRs. Write the vocabulary's `phrase.none` when Approved; when decisions were made while writing, it may say so: "None. Decisions made while writing are DR-67 and DR-68."
- **Length** follows content, not page count. Reference points from a real project: vision 90 lines, requirements 200, use cases 250, glossary 250, design documents 300–700, endpoint catalog 1,600, runbook 50, experiment 140.

## Glossary (written first)

- Group by topic (domain → data → processing → infrastructure → experiments).
- Contains the plan's **minimum term list** plus every word the foundation documents will use.
- Definitions say how the project uses the term, not only the dictionary meaning ("This system uses a JSON envelope instead of Protobuf (DR-03)").
- The Term column is the name used in code and UI; the local-name column holds the output-language name (omitted for English). A term with two meanings in the project (e.g. "replay" of the DLQ and of the raw zone) gets the meanings separated explicitly.

## Product

- **vision-and-scope**: a "Measurable goals" table with target, NFR and verification (EXP/test). Out-of-scope items have reasons. The cut order matches master plan §4.3.
- **personas-and-journeys**: the persona overview table first, details after. Say that persona names are illustrative. Journeys name concrete touchpoints (screens, endpoints) so screen specs can point back ("Journey J-1 steps 1–3").
- **requirements**: §0 conventions (MoSCoW, the G/W/T notation, the verification column). Each FR is a section `### FR-xx · <name>` with its FR-xx.y table. Acceptance criteria have **concrete numbers** (127 rows, p95 10 s, 499 of 500). A requirement revised later carries `*<dr.revised> (DR-xx): …*`. End with the NFR table and the FR → UC → F → DOC matrix.
- **use-cases**: §0 overall use case diagram (Mermaid flowchart actor → UC). State once the abbreviation conventions (endpoint prefix, quoted UI strings). Error flows name the exact UI behavior and message.
- **feature-catalog**: §0 column conventions, §1 overview (features per group × phase), one table per group, a final section mapping the cut order to features.

## Architecture

- **system-context-and-containers**: Mermaid for C4 levels 1 and 2; container table (technology, responsibility, port, protocol); deployment unit table; **data ownership per store** (table/schema/topic/bucket × written by × read by); trust boundaries (who authenticates where, which secret crosses which boundary); a final traceability section to other documents.
- **data-flows**: one `sequenceDiagram` per flow with a few lines on the commit and ack points. Failure flows matter as much as the main ones.
- **messaging-contracts**: JSON Schemas live in the code (path stated); the document has full examples and a field table. Backward-compatibility rules are written as checkable rules.
- **quality-attributes**: table NFR → tactic → mechanism → where implemented → verification. Latency budget per hop with a total. Capacity estimate computed from real data by a script (named). Planned and measured numbers clearly separated.
- **tech-stack-and-versions**: pinned versions (never "latest"), reason, license; compatibility table from spikes.

## ADR

- One ADR, one decision, sourced from a DR. The title is the decision ("Effectively-once via at-least-once plus upsert by business key"), not a topic.
- "Options considered" includes the obvious options that were rejected and why.
- "Consequences" has a real **negative** part.
- Update `04-adr/README.md` (table: ADR · title · status · gate · source).

## Data

- **DDL must run.** If Docker is available, start a throwaway database (`docker run --rm` with the version from the tech stack) and run all DDL in order before moving the document to Review; write "DDL tested on <database version> on <date>". Without Docker, say it has not been run.
- Every table: grain, business key, writers and readers, DDL, indexes with reasons (pointing to the query that uses them), sample upsert/query.
- Every status column has a `stateDiagram-v2` and a transition table (from → to · by whom · when).
- The DB permission matrix comes with a list of permission test cases (role × operation × expected).

## Design (06-design)

- Skeleton B.1. Interfaces are real code signatures in the project's language. Algorithms are numbered pseudo-code.
- The concurrency section answers: what commits together, when offsets/acks happen, what happens with several replicas, what happens if the process dies at each point.
- **Required tests**: table `ID · Scenario · Expected`, with the document's own prefix (registered in the test strategy). Scenarios and expectations have numbers. Business algorithms get input → expected output tables.
- Configuration and metrics of the document must also appear in the configuration reference and observability documents (add them there if those documents exist).
- Cross-cutting documents: security has a complete endpoint × role matrix; observability has alerts in PromQL (or the real query language) with `for`, severity and runbook link; error handling maps error code/exception → class → action → HTTP status → problem type.

## API

- One section per endpoint `### E-xx \`METHOD /path\` · \`operationId\``; `E-xx` is reused in screens, tests and OpenAPI.
- Response examples have every field, in the time and pagination formats of the API guidelines.
- The data source names the main SQL and index; the performance target is a number.
- §2 overview is a table of every endpoint (ID, method, path, authorization, UC, screen).

## UX/UI

- One file per screen per A.5, ASCII wireframes (desktop and mobile when relevant), data referenced by `E-xx` and real-time channel.
- Acceptance criteria have the screen's own IDs, written Given/When/Then; E2E cases are named so they can become tests.
- Microcopy is the exact string that will appear (in the UI language), collected in ui-states-and-copy.

## Operations

- Commands in local-dev, deploy and runbooks **run verbatim** (copy-paste) and state the expected output.
- Runbooks: Checks include metric queries, SQL and container/k8s commands; Remediation is numbered; "Confirm it is resolved" is a measurable condition.
- Every alert in observability has exactly one runbook; the runbooks README maps alert → RB.

## Testing

- **test-strategy** has the index of every test-ID prefix and the document holding it, coverage targets per module, and the CI stage of each test type.
- **experiments/README** defines the common protocol: ground truth, baseline, shared metric formulas, number of runs, machine, how results are stored. Each EXP covers only its own specifics.
- **demo-script**: each step has narration, action, expected result, fallback; a pre-demo checklist; how to reset.
