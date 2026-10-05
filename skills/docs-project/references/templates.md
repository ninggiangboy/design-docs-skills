# Templates

Canonical templates, written in English. **Render them in the output language**: look up every heading, label and table column in the English column of the vocabulary (`locales/<code>.md`, or Appendix B of the master plan for a generated language) and use the value in the output language. Keep IDs, status values (`Draft`, `Accepted`…), code, SQL, JSON and file names unchanged. Placeholders in `<…>` are filled with real content in the output language.

A.1–A.7 are copied into Appendix A of the master plan. B.x are skeletons for the remaining documents.

## A.1 ADR (short MADR)

```markdown
# ADR-XXXX: <Title that states the decision>

- Status: Proposed | Accepted | Superseded by ADR-YYYY
- Date: YYYY-MM-DD · Related: DR-xx, DOC-xx, FR-xx, NFR-xx

## Context
<The problem, constraints, why decide now. Cite SDD/DR.>

## Options considered
1. **<Name>.** <One-sentence description> — pros / cons.
2. …

## Decision
Option **N** is chosen.
- <Concrete details: mechanism, configuration, boundaries.>

## Consequences
**Positive**
- …

**Negative**
- …

**Follow-up work**
- …
```

## A.2 Use case

```markdown
## UC-XX · <Name>

- **Actor:** <main> (role), <secondary>
- **Trigger:** …
- **Preconditions:** …
- **Main flow:**
  1. …
  2. …
- **Alternative flows:**
  - 2a. …
- **Error flows:**
  - E1. … → <behavior, UI string "…">
- **Postconditions:** …
- **Business rules:** …
- **Related:** FR-…; screen `screens/<x>.md`; endpoint E-…; event …
```

## A.3 Requirement with acceptance criteria

Table form (default, compact). G/W/T stand for Given/When/Then in every language:

```markdown
### FR-02 · <Requirement group>

| ID | Requirement | Acceptance criteria | Priority | Verification |
| --- | --- | --- | --- | --- |
| FR-02.2 | A validation failure goes to the DLQ with `stage=SCHEMA` | **G** a chunk of 500 records, record #37 lacks `vehicle_id` **T** 499 rows written; 1 `SCHEMA` dead letter naming the field; offset committed to the end of the chunk | M | Unit test, EXP-03 |
```

Full form (when one requirement needs several scenarios):

```markdown
### FR-02.1 <Name>
Priority: Must · Source: SDD 3.2 · UC: UC-08
- Given …
- When …
- Then …
- And …
Verification: P2-03 unit test, EXP-03
```

NFR:

```markdown
| ID | Requirement | Target | How measured | Verification |
| --- | --- | --- | --- | --- |
| NFR-03 | Data latency | p95 < 10 s at base load | Histogram at the API | EXP-05 |
```

## A.4 API endpoint

```markdown
### E-xx `GET /stops/{stopId}/arrivals` · `listStopArrivals`

- **Purpose / UC:** …
- **Authorization:** anonymous (rate limit 60/min/IP)
- **Parameters:**

  | Name | In | Type | Required | Default | Constraints |
  | --- | --- | --- | --- | --- | --- |

- **Response 200:** schema + a complete JSON example
- **Errors:** 404 `stop-not-found`, 400 `invalid-param` (Problem Details)
- **Data source:** tables/views, main query, index used
- **Cache:** TTL, key
- **Performance:** p95 < … ms
- **Related real-time events:** …
```

## A.5 Screen specification

```markdown
# Screen: <Name>

> Status: … · DOC-xx
> Depends on: …
> Main readers: Px-xx

## 1. Persona, use cases, permissions
## 2. URL and search params
## 3. Wireframe            (ASCII, desktop and mobile when relevant)
## 4. Regions and components  (refer to the design system)
## 5. Data                 (endpoint E-xx · real-time channel · refetch interval)
## 6. Interactions         (action → result → error)
## 7. States               (loading · empty · error · stale · forbidden)
## 8. Microcopy
## 9. Acceptance criteria  (Given/When/Then, with IDs)
## 10. E2E test cases
## 11. Open questions
```

## A.6 Experiment protocol

```markdown
# EXP-XX: <Name that states the claim being tested>

> Status: … · DOC-xx / EXP-XX
> Depends on: [common protocol](README.md), …
> Main readers: Px-xx; the evaluation chapter of the report

## 1. Hypothesis       (H1 (NFR-xx): … measured by …)
## 2. Variables        (independent · dependent · controlled)
## 3. Baseline
## 4. Environment      (machine, runtime environment, git version)
## 5. Steps            (automated commands)
## 6. Metrics and formulas
## 7. Pass criteria
## 8. Analysis         (scripts, charts)
## 9. Result table template
## 10. Threats to validity
## 11. Results         (empty until run)
## 12. Open questions
```

## A.7 Runbook

```markdown
# RB-XX: <Alert or operation name>

> Status: … · DOC-xx / RB-XX
>
> Alert: `AlertName` (severity, for) · Dashboard: … · Related: DOC-xx §n

## Symptoms and impact
## Checks               (commands, metric queries, SQL — runnable verbatim)
## Remediation          (steps 1, 2, 3)
## On <other environment>  (when it differs)
## Confirm it is resolved
## Prevention and follow-up
```

---

## B.1 Design document (group 06-design)

```markdown
# <Component name>

> Status: **Draft** · Updated: YYYY-MM-DD · DOC-xx
> Depends on: …
> Main readers: <app/module>, Pn-xx…

<What the document covers; what belongs to other documents.>

## 1. Purpose and scope        (component table: main class · runs in · trigger · reads · writes · task)
## 2. Components and interfaces (real code signatures)
## 3. Algorithm                (numbered pseudo-code)
## 4. Transactions and concurrency (what commits together; locks; replicas)
## 5. Configuration            (Key · Type · Default · Description)
## 6. Metrics and logs         (Metric · Type · Label; related alerts)
## 7. Errors and handling      (Situation · Behavior)
## 8. Required tests           (ID · Scenario · Expected — the document's own prefix)
## 9. Open questions           ("None." when Approved)
```

Add content-specific sections (state machines, file formats, interaction with other flows) between §3 and §5.

## B.2 Persona

```markdown
| ID | Persona | Role | Main device | Technical level | Frequency |
| --- | --- | --- | --- | --- | --- |

### PS-1 · <Role>: "<Illustrative name>, <one-line situation>"

- **Goals:** …
- **Pain points:** …
- **Needs from <system>:** …
- **Does not need:** …
- **Screens:** …
```

Journey: table `Step · Action · Touchpoint (screen/endpoint) · Emotion · Opportunity`.

## B.3 Feature

```markdown
| ID | Feature | Description | FR | UC | Phase | MoSCoW | Flag | Depends on | Cut step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## B.4 Glossary

```markdown
## 1. <Term group>

| Term | Local name | Definition | Related |
| --- | --- | --- | --- |
| feed version | <local name> | A loaded feed, identified by … Only one version is `ACTIVE` | DR-10, DOC-21 |
```

The "Local name" column (`col.local_name`) is omitted when the output language is English.

## B.5 Data table (group 05-data)

````markdown
### 5.3 `fact_vehicle_position`

- **Grain:** one row per (vehicle, event time).
- **Business key:** `(vehicle_id, event_timestamp, service_date)`.
- **Written by:** `etl` (DOC-20). **Read by:** `api`, `analytics`.

```sql
CREATE TABLE … ;
CREATE INDEX … ;  -- reason: query X in DOC-32 E-05
```

**Sample upsert:**

```sql
INSERT … ON CONFLICT (…) DO UPDATE SET … WHERE excluded.event_timestamp > t.event_timestamp;
```
````

## B.6 `docs/README.md`

```markdown
# Project documentation: <Name>

Original design document: [`../<sdd>.md`](../<sdd>.md) (the **original SDD**). Documents are written in <language>; see master plan §0.1.

## Start here

1. [00-master-plan.md](00-master-plan.md): the master plan. …
2. [00-decision-register.md](00-decision-register.md): the decision register. …

## Documents

| DOC | Document | Status |
| --- | --- | --- |
| DOC-01 | [<Vision and scope>](01-product/vision-and-scope.md) | Not written |

## Structure

| Folder | Content |
| --- | --- |

## Conventions

- The first lines of every file give its status (`Draft | Review | Approved | Superseded`) and update date.
- Diagrams are Mermaid.
- Identifiers follow master plan §0.
- A behavior change edits the docs in the same PR. A decision change gets a new ADR that supersedes the old one.
```
