# API endpoints

> Status: **Approved** · Updated: 2026-10-05 · DOC-05

### E-01 `POST /holds` · `createHold`

- **Purpose:** UC-01
- **Request:** `{ "seatId": "A-12", "showId": 42 }`
- **Response 201:** `{ "holdId": "h_9f2", "seatId": "A-12", "expiresAt": "2026-10-05T10:10:00Z" }`
- **Errors:** 409 `seat-taken`

## Open questions

None.
