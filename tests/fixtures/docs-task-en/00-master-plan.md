# Master Plan: building Seat Hold end to end

> Status: **Approved v1.0** · Updated: 2026-10-05 · Accompanies: [00-decision-register.md](00-decision-register.md)

## 0. How to use this document

### 0.1 Language

| | |
| --- | --- |
| Documents | English (`en`) · vocabulary: shipped `locales/en.md` |
| Code, UI strings, logs, commits | English |

## 3. Documents to write

```
docs/
  01-product/
    requirements.md       # DOC-01
    use-cases.md          # DOC-02
  02-glossary.md          # DOC-03
  06-design/
    flows/
      booking.md          # DOC-04
  07-api/
    api-endpoints.md      # DOC-05
  08-ux-ui/
    screens/
      seat-map.md         # DOC-06
```

## 5. Tasks per phase

### Phase 1: Foundation

| ID | Task | Output and acceptance | Depends on | Documents |
| --- | --- | --- | --- | --- |
| P1-00 | Doc gate: DOC-01…03 | Approved | M0 | — |
| P1-01 | Initialize the repo and the `seat` table — **Done 2026-10-01** (`a1b2c3d`) | `make up` → database healthy; migration V1 applied | P1-00 | DOC-01 |

**M1 reached on 2026-10-02.**

### Phase 2: Booking core

| ID | Task | Output and acceptance | Depends on | Documents |
| --- | --- | --- | --- | --- |
| P2-00 | Doc gate: DOC-04, DOC-05 | Approved | M1 | — |
| P2-01 | `HoldService.hold` with the conditional `UPDATE` | Test: 2 concurrent holds on one seat → 1 succeeds, 1 gets `seat-taken` | P2-00 | DOC-04 |
| P2-02 | Endpoint E-01 and the seat map screen | Test: click a free seat → seat shown as held, countdown 10:00 | P2-01 | DOC-04, DOC-05, DOC-06 |

## 6. Traceability matrix

| Requirement | Design documents | Tasks | Verification |
| --- | --- | --- | --- |
| FR-01 | DOC-04, DOC-05 | P2-01, P2-02 | H-01, H-02 |
