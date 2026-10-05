# Mini Shop — System Design

Oct 5, 2026 · @tester

A small shop selling limited stock; it never sells more than it has.

## 1. Introduction

### 1.1 Context

Limited goods, many concurrent buyers (section 2.1, §2.2).

## 2. Goals, scope and focus

### 2.1 Core problem

> How do we never oversell when many requests compete for one item?

### 2.2 Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| FR-01 | Atomic hold | — |
| NFR-01 | Never oversell | 0 orders above stock (EXP-01) |

See sections 1.1 and 2.1 for the context.

## 3. Testing and evaluation

### 3.1 Experiments

| ID | Experiment | Method | Metrics | Expected |
| --- | --- | --- | --- | --- |
| EXP-01 | Contention on one item | 1,000 concurrent requests | Successful orders | Exactly 1, per FR-01 |
