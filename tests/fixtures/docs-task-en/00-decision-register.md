# Decision Register

> Status: **Review** · Updated: 2026-10-05

### DR-01 · Who wins when two customers click the same seat — **Decided**
- **Decision:** The conditional `UPDATE seat … WHERE status='FREE'` is the arbiter.
- **Write to:** DOC-04.

### DR-02 · How long a hold lasts
- **Problem:** The original SDD says "a few minutes".
- **Decision (proposed):** 10 minutes, key `booking.hold-ttl`.
- **Write to:** DOC-04, DOC-06.
