# Concept cards

Starting points for explaining a concept from zero (`plain-language.md` §2). Each card: **Plain** (rung 1), **Analogy** and where it **breaks** (rung 2), **Looks like** (rung 3), **Mistakes** beginners make, and **In the docs** (where to find rung 4, how this project uses it).

Use the cards as material, not text to paste: write new sentences in the developer's language, swap in the project's real names and values, and choose analogies that fit the developer's world. For a concept that has no card, follow the same five parts. General knowledge here needs no citation; anything about the project does.

## Contents

- Web and API: client and server · HTTP request and response · status codes · JSON · API and endpoint · authentication and authorization · session, cookie, token · CORS · real-time (WebSocket, SSE)
- Data: database · table, row, column · primary key · foreign key · SQL · NULL · index · transaction · constraint · migration · ORM
- Backend: layers · DTO · validation · exceptions and error responses · configuration and environment variables · logs · metrics and alerts
- Infrastructure: process and port · environment · Docker image and container · Docker Compose · nginx and reverse proxy · load balancer · cache and Redis · TTL · queue and message broker · background job and scheduler · CI/CD
- Correctness: concurrency and race condition · lock · idempotency · retry and timeout · at-least-once delivery
- Frontend: component and state · loading, empty, error states · routing and URL parameters · client vs server validation
- The docs set: requirement and acceptance criteria · use case · sequence diagram · endpoint spec · DR and ADR · document status and gates

---

## Web and API

### Client and server
- **Plain:** The client (browser, mobile app) asks; the server answers. They are separate programs, usually on separate machines, talking over the network.
- **Analogy:** A customer and a kitchen. **Breaks:** one server answers thousands of clients at the same time.
- **Looks like:** the React app in `web/` is the client; the service in `api/` is the server.
- **Mistakes:** trusting data from the client (it can be changed by the user); putting secrets in client code.
- **In the docs:** system context and containers (who talks to whom).

### HTTP request and response
- **Plain:** A request is a message from client to server: a **method** (what to do), a **path** (on what), **headers** (extra info such as who you are) and sometimes a **body** (the data). The response has a **status code**, headers and a body.
- **Analogy:** A form handed in at a counter, and the stamped answer you get back.
- **Looks like:**
  ```http
  POST /holds HTTP/1.1
  Authorization: Bearer eyJ…
  Content-Type: application/json

  { "seatId": "A-12", "showId": 42 }
  ```
  Methods: `GET` read · `POST` create or act · `PUT`/`PATCH` change · `DELETE` remove.
- **Mistakes:** changing data in a `GET`; forgetting `Content-Type`; sending the body as a string instead of JSON.
- **In the docs:** API guidelines; each endpoint `E-xx`.

### Status codes
- **Plain:** A three-digit number saying how the request went. 2xx worked, 4xx the client asked for something wrong, 5xx the server failed.
- **Common ones:** `200 OK` · `201 Created` · `204 No Content` · `400` bad input · `401` not logged in · `403` logged in but not allowed · `404` not found · `409` conflict with the current state (seat already taken) · `422` input well-formed but breaks a rule · `429` too many requests · `500` server bug · `503` server temporarily unavailable.
- **Mistakes:** returning 200 with `{ "error": … }`; 500 for bad user input; mixing up 401 and 403.
- **In the docs:** error handling (exception → status → problem type); each endpoint's errors.

### JSON
- **Plain:** A text format for data: objects `{ }` with named fields, lists `[ ]`, strings, numbers, `true`/`false`, `null`.
- **Looks like:** `{ "holdId": "h_9f2", "expiresAt": "2026-10-05T10:10:00Z", "seats": ["A-12"] }`
- **Mistakes:** numbers as strings (`"42"`); dates in a local format instead of the agreed ISO format with time zone; renaming a field the client already uses.
- **In the docs:** API guidelines (naming, time format); the endpoint's sample response.

### API and endpoint
- **Plain:** An API is the list of requests a server accepts. An endpoint is one of them: a method plus a path, like `POST /holds`.
- **Analogy:** A restaurant menu: you can only order what is on it, in the way it is written.
- **Mistakes:** inventing an endpoint the docs do not list; changing a response shape without updating the spec.
- **In the docs:** API endpoint catalog, one `E-xx` per endpoint (purpose, who may call it, input, output, errors, which table it reads).

### Authentication and authorization
- **Plain:** Authentication: *who are you?* (login). Authorization: *are you allowed to do this?* (permissions, roles).
- **Analogy:** Showing your ID at the building entrance vs. having the key card for a specific floor.
- **Mistakes:** checking permissions only in the UI (hiding a button) and not on the server; checking the role but not ownership ("this order belongs to this user").
- **In the docs:** security (endpoint × role matrix); the screen's permissions section.

### Session, cookie, token
- **Plain:** After login, the server must recognise you on every request. Either it keeps a **session** and gives the browser a **cookie** holding the session ID, or it gives a signed **token** (often a JWT) the client sends in the `Authorization` header.
- **Analogy:** A coat-check ticket (session ID: the counter keeps your coat) vs. a festival wristband (token: everything needed is on the wristband, checked by its seal).
- **Mistakes:** storing tokens where any script can read them; trusting the content of a token without verifying its signature; logging tokens.
- **In the docs:** security (authentication method, token lifetime).

### CORS
- **Plain:** A browser rule: a page from one address may call an API on another address only if the API says that address is allowed.
- **Analogy:** A guest list at the door, checked by the browser, not by the server.
- **Mistakes:** "fixing" a CORS error by allowing every origin (`*`) with credentials; thinking CORS protects the API from scripts or other servers (it does not; only browsers enforce it).
- **In the docs:** security (CORS); nginx or API configuration.

### Real-time: WebSocket and SSE
- **Plain:** Normal HTTP: the client asks, the server answers, done. For live updates the connection stays open: **SSE** lets the server push messages one way; **WebSocket** lets both sides send at any time.
- **Analogy:** Phoning to ask "anything new?" every minute vs. staying on the line.
- **Mistakes:** not handling reconnects; assuming no message is ever missed; forgetting to close the connection when the screen closes.
- **In the docs:** the events document (event types, payloads, channels); the screen's Data section.

## Data

### Database
- **Plain:** A program whose job is to store data safely and find it fast, even when many users read and write at the same time and even if the machine crashes. PostgreSQL and MySQL are relational databases (data in tables).
- **Analogy:** A filing room with a very strict clerk who never loses a page. **Breaks:** the clerk also enforces rules and handles thousands of requests at once.
- **Mistakes:** keeping important data only in memory or in files; connecting to a shared or production database to "try something".
- **In the docs:** the data model document (tables, DDL); local dev (how to start a local database).

### Table, row, column
- **Plain:** A table is like one spreadsheet sheet with a fixed list of columns, each with a type. Each row is one record.
- **Looks like:**

  | id | show_id | status |
  | --- | --- | --- |
  | A-12 | 42 | FREE |
  | A-13 | 42 | HELD |
- **Mistakes:** storing several values in one column ("A-12,A-13"); storing the same fact in two tables that can disagree.
- **In the docs:** data model (each table: what one row means, columns, who writes and who reads it).

### Primary key
- **Plain:** The column (or columns) that identifies one row; it is unique and never empty.
- **Analogy:** A citizen ID number: two people may share a name, never an ID.
- **Mistakes:** using something that can change (an email) as the key; letting the client choose IDs without checking.
- **In the docs:** the DDL (`PRIMARY KEY`); "business key" in the table description.

### Foreign key
- **Plain:** A column that points to the primary key of another table, and the database checks the target exists.
- **Analogy:** An order slip that must name an existing customer number.
- **Looks like:** `hold.seat_id REFERENCES seat(id)`.
- **Mistakes:** deleting a parent row and being surprised the database refuses (or deletes the children, if `ON DELETE CASCADE`).
- **In the docs:** DDL; the ERD diagram.

### SQL
- **Plain:** The language for talking to a relational database. Four verbs do most of the work: `SELECT` read, `INSERT` add, `UPDATE` change, `DELETE` remove. `WHERE` chooses which rows; `JOIN` combines tables.
- **Looks like:**
  ```sql
  SELECT s.id, s.status FROM seat s WHERE s.show_id = 42 ORDER BY s.id;
  ```
- **Mistakes:** `UPDATE`/`DELETE` without `WHERE` (changes every row); building SQL by gluing user input into a string (SQL injection; use parameters); loading a whole table to filter in code.
- **In the docs:** the endpoint's data source (main query); the data model's sample queries.

### NULL
- **Plain:** "No value / unknown". Not zero, not an empty string.
- **Mistakes:** `WHERE x = NULL` never matches (use `IS NULL`); forgetting that a nullable column can be null in code too.
- **In the docs:** DDL (`NOT NULL` or not); the field table of the endpoint.

### Index
- **Plain:** An extra structure the database keeps so it can find rows by some columns without reading the whole table.
- **Analogy:** The index at the back of a book. **Breaks:** the database must update every index on every write, so each index makes inserts and updates a bit slower.
- **Looks like:** `CREATE INDEX idx_seat_show ON seat (show_id);` makes `WHERE show_id = 42` fast.
- **Mistakes:** filtering by a column with no index on a big table; wrapping the column in a function (`WHERE lower(email) = …`) so the index is not used.
- **In the docs:** data model (indexes with the query each one serves).

### Transaction
- **Plain:** A group of database changes that succeed together or fail together. Until it **commits**, nobody else sees the changes; on **rollback**, it is as if nothing happened.
- **Analogy:** A bank transfer: taking money from A and adding it to B must both happen, or neither.
- **Looks like:**
  ```sql
  BEGIN;
  UPDATE seat SET status = 'HELD' WHERE id = 'A-12' AND status = 'FREE';
  INSERT INTO hold (seat_id, expires_at) VALUES ('A-12', now() + interval '10 minutes');
  COMMIT;
  ```
  In code, frameworks often open and commit it for you around a method (for example `@Transactional`).
- **Mistakes:** calling an external service (email, payment) inside a transaction; catching an error and continuing as if the transaction were still fine; assuming a transaction alone stops two users from both "reading free then writing held" (see race condition).
- **In the docs:** the flow's "Transactions and concurrency" (`T1 begins` / `T1 commits` notes); the design document's concurrency section.

### Constraint
- **Plain:** A rule the database enforces itself: `NOT NULL`, `UNIQUE`, `CHECK (qty >= 0)`, foreign keys. If a write breaks it, the database refuses.
- **Analogy:** A form that will not submit until required boxes are filled.
- **Mistakes:** checking only in code and not in the database (two requests at once can both pass the code check); not turning the constraint error into a clear error for the user.
- **In the docs:** DDL; error handling (which constraint violation maps to which error code).

### Migration
- **Plain:** A versioned script that changes the database structure (add a table, a column, an index). They run in order, once each, on every environment.
- **Analogy:** Numbered renovation work orders for a building; every copy of the building gets the same orders in the same order.
- **Mistakes:** editing a migration that already ran elsewhere (write a new one); changing the database by hand.
- **In the docs:** master plan §7.3 (migration naming); local dev (how to run them).

### ORM
- **Plain:** A library that maps tables to classes so you write code instead of SQL (JPA/Hibernate, Prisma, Entity Framework, SQLAlchemy…).
- **Mistakes:** the "N+1" problem (one query for a list, then one more query per item); not knowing which SQL the ORM really runs (turn on SQL logging locally).
- **In the docs:** code architecture; tech stack.

## Backend

### Layers: controller, service, repository
- **Plain:** Code is split by job. The **controller** speaks HTTP (reads the request, returns the response). The **service** holds the business rules. The **repository** talks to the database.
- **Analogy:** Waiter, cook, storeroom.
- **Mistakes:** business rules in the controller; SQL in the service; the controller calling the repository directly.
- **In the docs:** code architecture (layers, dependency rules, where transactions live); the flow's participants table (which class does what).

### DTO
- **Plain:** A small class that only carries data in or out (the request body, the response body), separate from the database entity.
- **Mistakes:** returning database entities directly (leaks fields, breaks when the table changes).
- **In the docs:** the endpoint's request and response; code architecture (DTOs and mapping).

### Validation
- **Plain:** Checking input before using it: required fields, formats, ranges, and business rules ("a seat can only be held if the show has not started").
- **Mistakes:** validating only on the client; returning a vague error instead of saying which field is wrong.
- **In the docs:** the endpoint's parameters and errors; the use case's rules.

### Exceptions and error responses
- **Plain:** When something goes wrong, code throws an exception; one central place turns each kind of exception into the right status code and error body for the client.
- **Mistakes:** catching an exception and doing nothing; showing the internal error message or stack trace to the user; a new error type with no mapping (becomes a 500).
- **In the docs:** error handling (exception → status → problem type); the flow's "Errors and handling" table.

### Configuration and environment variables
- **Plain:** Values that may differ per environment or change without changing code (timeouts, limits, URLs, passwords) live in configuration, often set by environment variables.
- **Analogy:** The settings menu of an app.
- **Looks like:** `booking.hold-ttl=10m`, set in production by `BOOKING_HOLD_TTL=10m`.
- **Mistakes:** hard-coding a value the docs list as configuration; committing passwords; a new key not added to the configuration reference.
- **In the docs:** configuration reference (key, type, default, environment variable).

### Logs
- **Plain:** Text lines a program writes about what it is doing, read later to understand what happened. Levels: `DEBUG`, `INFO`, `WARN`, `ERROR`.
- **Mistakes:** logging passwords, tokens or personal data; `ERROR` for normal situations (a user typed a wrong password); logs without the ID that lets you follow one request.
- **In the docs:** observability (required log fields).

### Metrics and alerts
- **Plain:** Metrics are numbers measured over time (requests per second, errors, latency). An alert fires when a metric crosses a threshold, and a runbook says what to do.
- **Analogy:** The dashboard and warning lights of a car.
- **In the docs:** observability (metric catalog, alerts); runbooks.

## Infrastructure

### Process and port
- **Plain:** A running program is a process. A server process listens on a **port** (a numbered door on the machine) for connections: e.g. API on 8080, PostgreSQL on 5432, Redis on 6379.
- **Mistakes:** "port already in use" because an old copy is still running; mixing up the port inside a container and the one on your machine.
- **In the docs:** local dev (port table).

### Environment
- **Plain:** A complete copy of the system for a purpose: **local** (your machine), **staging/test** (shared, for checking), **production** (real users, real data).
- **Mistakes:** testing against production; assuming staging data is disposable when others use it.
- **In the docs:** deployment documents; configuration reference (profiles).

### Docker image and container
- **Plain:** An **image** is a packaged program with everything it needs to run. A **container** is a running copy of an image, isolated from the rest of the machine.
- **Analogy:** A recipe card and a dish cooked from it; or an app installer and the running app.
- **Looks like:** `docker ps` lists running containers; `docker logs api` shows one's output.
- **Mistakes:** expecting files written inside a container to survive when it is recreated (use volumes); editing code inside a container.
- **In the docs:** local dev; deployment.

### Docker Compose
- **Plain:** A file (`compose.yaml`) that starts several containers together (API, database, Redis…) with one command.
- **Looks like:** `docker compose up -d` start · `docker compose ps` status · `docker compose logs -f api` follow logs · `docker compose down` stop.
- **Mistakes:** `docker compose down -v` deletes the volumes (the local data); never run it without knowing that.
- **In the docs:** local dev (`make` targets, start order, demo accounts, reset).

### nginx and reverse proxy
- **Plain:** nginx is a web server that often sits **in front of** the application. It receives every request from the internet and forwards it to the right program: `/api/…` to the API, everything else to the web app. This forwarding role is called a **reverse proxy**. It also commonly handles HTTPS, compression, static files and size or rate limits.
- **Analogy:** A building receptionist who takes every visitor and sends them to the right office.
- **Looks like:**
  ```nginx
  location /api/ { proxy_pass http://api:8080/; }
  location /     { root /usr/share/nginx/html; try_files $uri /index.html; }
  ```
- **Mistakes:** the API sees nginx's address instead of the user's (read `X-Forwarded-For` as configured); a request body bigger than nginx's limit fails before reaching the API (`413`); timeouts in nginx shorter than a slow endpoint.
- **In the docs:** deployment; system context (containers); security (TLS, rate limits).

### Load balancer
- **Plain:** Spreads requests across several copies of the same service, so more users can be served and one copy can fail without an outage. nginx can do this too.
- **Mistakes:** keeping user state in the memory of one copy (the next request may go to another copy); scheduled jobs running on every copy at once.
- **In the docs:** deployment; quality attributes (scaling).

### Cache and Redis
- **Plain:** A cache keeps a copy of data somewhere faster so you do not recompute or reload it every time. **Redis** is a very fast key–value store kept in memory, often used as a cache, and also for counters, short-lived data (sessions, holds), locks and simple queues.
- **Analogy:** Sticky notes on your desk next to the filing room: fast to read, limited space, and they can be thrown away.
- **Breaks:** depending on configuration Redis may be wiped on restart or may evict keys when full; never treat it as the only copy of important data unless the docs say it is set up for that.
- **Looks like:** `SET hold:A-12 "lan" EX 600` (expires in 600 s) · `GET hold:A-12` · `TTL hold:A-12`.
- **Mistakes:** the cache shows old data after the database changes (no invalidation); a key with no expiry grows forever; `KEYS *` on a big Redis (blocks it; use `SCAN`); `FLUSHALL` (deletes everything).
- **In the docs:** the design document that uses it (key names, TTL, what happens if Redis is down); configuration reference.

### TTL (time to live)
- **Plain:** How long a piece of data is kept before it expires automatically.
- **Mistakes:** different units in different places (seconds vs minutes); expecting expiry to the exact millisecond.
- **In the docs:** configuration reference; the DR that chose the duration.

### Queue and message broker
- **Plain:** A broker (RabbitMQ, Kafka…) holds messages between programs. A **producer** puts a message in; a **consumer** takes it out later and does the work. The producer does not wait for the work to finish.
- **Analogy:** The ticket line at a bank: you take a number, and a free counter calls you when it can.
- **Mistakes:** assuming each message is processed exactly once (see at-least-once); assuming messages arrive in order across partitions or queues; doing work and crashing before acknowledging, then being surprised it runs again.
- **In the docs:** messaging contracts (topics, message schemas); data flows (commit and ack points).

### Background job and scheduler
- **Plain:** Work that runs without a user waiting: on a schedule (every night, every minute) or triggered by a message. A **cron** expression says when.
- **Looks like:** `0 */5 * * * *` = every 5 minutes (format depends on the library; check the docs).
- **Mistakes:** the job runs on every copy of the service at once; a job that cannot be safely rerun after a crash halfway.
- **In the docs:** the design document of the job; ops model (job status tables).

### CI/CD
- **Plain:** **CI** automatically builds and tests every push or pull request. **CD** automatically deploys what passed.
- **Mistakes:** merging with red CI; tests that pass locally only because of local data.
- **In the docs:** CI/CD (stages, what blocks a merge); master plan §7.2 Definition of Done.

## Correctness

### Concurrency and race condition
- **Plain:** Many requests run at the same time. A **race condition** is a bug that appears only when two of them interleave badly, typically "read, decide, write": both read the same old value, both decide, both write.
- **Analogy:** Two people booking the last seat on two different phones at the same second.
- **Looks like:** read `FREE` → (other user also reads `FREE`) → both write `HELD` → seat sold twice.
- **Mistakes:** "it works on my machine" (you alone never trigger it); fixing it with a `sleep`.
- **In the docs:** the flow's "Transactions and concurrency" (which step is the **arbiter**: the one place that decides who wins); the DR behind it; required tests with two concurrent requests.

### Lock
- **Plain:** A way to make others wait while you work on something. **Pessimistic:** lock first, then work (`SELECT … FOR UPDATE`). **Optimistic:** work, then write only if nobody changed it meanwhile (a `version` column or a conditional `UPDATE … WHERE`).
- **Analogy:** Locking the bathroom door vs. checking nobody moved your things before you sit back down.
- **Mistakes:** holding a lock while calling a slow external service; two pieces of code locking things in different orders (deadlock).
- **In the docs:** design document concurrency section; the DR that chose the approach.

### Idempotency
- **Plain:** Doing the same request twice has the same effect as doing it once. Needed because networks retry: the client may not know whether the first try worked.
- **Analogy:** Pressing the elevator button five times still calls the elevator once.
- **Looks like:** the client sends `Idempotency-Key: 7f3c…`; the server remembers the key and returns the first result for repeats. Or an upsert by business key instead of a plain insert.
- **Mistakes:** charging or creating twice when the user double-clicks or the request is retried.
- **In the docs:** API guidelines (idempotency); the endpoint's headers; the flow's step table.

### Retry and timeout
- **Plain:** A **timeout** is how long to wait before giving up. A **retry** tries again after a failure, usually after a growing pause (backoff).
- **Mistakes:** no timeout (one slow service freezes everything); retrying something that is not idempotent; retrying instantly in a loop.
- **In the docs:** configuration reference (timeouts, retry counts); the flow's error table.

### At-least-once delivery
- **Plain:** Many brokers guarantee a message is delivered **at least** once, so sometimes twice. The consumer must handle duplicates (idempotency).
- **Mistakes:** assuming "exactly once" and double-counting.
- **In the docs:** data flows; the DR or ADR on delivery semantics.

## Frontend

### Component and state
- **Plain:** A screen is built from components (button, seat map, countdown). **State** is the data a component remembers that changes what it shows (selected seat, loading or not).
- **Mistakes:** two components keeping their own copy of the same state that drifts apart; state from the server kept forever without refreshing.
- **In the docs:** the screen file (regions and components); design system.

### Loading, empty, error states
- **Plain:** Every screen that loads data has more than the happy case: still loading, nothing to show, failed, data is old, not allowed.
- **Mistakes:** a blank screen while loading; an error shown as an empty list; no way to retry.
- **In the docs:** the screen's States section; ui-states-and-copy (patterns and exact messages).

### Routing and URL parameters
- **Plain:** The URL decides which screen shows (`/shows/42/seats`), and search parameters keep filters (`?section=A`), so a page can be shared or reloaded.
- **Mistakes:** keeping filters only in memory (lost on reload).
- **In the docs:** UX principles and IA (URL map); the screen's URL section.

### Client vs server validation
- **Plain:** The client checks input to help the user quickly; the server checks again because the client can be bypassed.
- **Mistakes:** only one of the two; different rules in the two places.
- **In the docs:** the screen's interactions and microcopy; the endpoint's errors.

## The docs set

### Requirement and acceptance criteria
- **Plain:** `FR-xx` says what the system must do. Each `FR-xx.y` has acceptance criteria written **Given** (the situation) **When** (the action) **Then** (the result), with real numbers. They become tests.
- **In the docs:** requirements; master plan §6 (which tasks and tests cover which FR).

### Use case
- **Plain:** `UC-xx` tells one goal of one user as steps: the main path, the alternative paths (2a…), and what happens when things go wrong (E1…).
- **In the docs:** use cases; each one points to its flows `FL-xx`.

### Sequence diagram
- **Plain:** A picture of who talks to whom, in time order, top to bottom. Each vertical line is a participant (screen, API, service, database). Each arrow is one call; a dashed arrow is the answer. `alt` / `else` boxes are the different outcomes. `Note over … T1 begins / commits` marks a transaction.
- **Looks like:** step numbers on the arrows match the rows of the step table below the diagram.
- **In the docs:** detailed flows `FL-xx`; data flows.

### Endpoint spec
- **Plain:** `E-xx` describes one endpoint: what it is for, who may call it, inputs, a full example response, errors, which table and query it uses, how fast it must be.
- **In the docs:** API endpoint catalog.

### DR and ADR
- **Plain:** A **DR** (decision register entry) is a question the design had to answer, with the options and the choice. **Proposed** means not decided yet; **Decided** means you follow it. An **ADR** records a big architecture decision with its reasons and its costs. Together they answer "why do we do it this way?".
- **Mistakes:** coding against a Proposed DR as if it were final; changing a decided behavior without a new decision.
- **In the docs:** `00-decision-register.md`; `04-adr/`.

### Document status and gates
- **Plain:** Each document is `Draft` (being written) → `Review` (written, being checked) → `Approved` (you can rely on it). A phase starts only when the documents it needs are Approved (its task `Pn-00`, the doc gate).
- **Mistakes:** building from a Draft without telling anyone; treating "Open questions" as optional reading.
- **In the docs:** master plan §0 and §3.3; the status line at the top of each document.
