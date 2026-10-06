# Screen: Seat map

> Status: **Draft** · Updated: 2026-10-05 · DOC-06
> Depends on: [DOC-05](../../07-api/api-endpoints.md), [DOC-04](../../06-design/flows/booking.md)
> Main readers: P2-02

## 1. Persona, use cases, permissions

Customer · UC-01

## 5. Data

| Data | Endpoint |
| --- | --- |
| Seats of a show | E-02 |

## 6. Interactions

| Action | Endpoint | Result | Error |
| --- | --- | --- | --- |
| Click a free seat | E-01 | Seat shown as held, countdown 10:00 | 409 → toast "This seat was just taken" |

## 9. Acceptance criteria

| ID | Criterion |
| --- | --- |
| SM-01 | Given seat A-12 is free, when the customer clicks it, then it turns blue and a 10:00 countdown starts |

## 11. Open questions

- The endpoint that lists the seats of a show (E-02) is not in the endpoint catalog yet.
