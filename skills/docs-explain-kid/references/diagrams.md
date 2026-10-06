# ASCII diagrams

A beginner understands a mechanism from a picture much faster than from a paragraph. The terminal does not render Mermaid, so every picture is plain text in a ```` ```text ```` fence. This file says when to draw, how to keep a drawing readable, and gives one template per kind. Templates use the seat-hold example; replace every name and value with the project's.

## 1. When to draw

| Situation | Picture | Where |
| --- | --- | --- |
| Every brief | Who talks to whom (§3.1) | Brief section 3, first thing |
| A flow with more than 3 calls | Steps in time (§3.2) | Brief section 3, translating the `FL-xx` sequence diagram |
| A race, a lock, a retry, anything "at the same time" | Timeline in two lanes (§3.3), the bug first, then the fix | Section 2 or the answer |
| The item changes a status column | State diagram (§3.4) | Section 3 |
| Code in more than one layer or file | Layer map (§3.5) | Section 4 |
| An outcome with branches (success, error cases) | Decision tree (§3.6) | Section 3, after the steps |
| A screen task | Wireframe with numbered regions (§3.7) | Section 1 or 3 |
| Several tables involved | Table relationships (§3.8) | Section 2 or 3 |
| A step that changes data | Before/after table (§3.9) | Under that step |
| A concept card in section 2 | The card's **Picture** in `concepts.md` | Under rung 2 or 3 |

In answers: draw when explaining **how** or **why** something works; a one-fact answer needs no picture. Two or three pictures in a brief are usually enough; a picture that repeats another is noise.

## 2. Rules

- **Truthful.** Draw only what the docs say: participants from the flow's participants table (`flows/README.md` naming), states from the data document's state diagram, regions from the screen file's wireframe. A box or arrow the docs do not have is invented; leave it out. Say "simplified: nginx left out" when you drop something.
- **Real names on boxes and arrows.** `SeatMap`, `api`, `HoldService`, `seat`; arrows carry the real call (`POST /holds (E-01)`, `UPDATE seat … WHERE status='FREE'`, `hold(A-12)`), shortened with `…` if needed.
- **Numbered arrows** `(1) (2) …` that match the numbered steps under the picture, so the reader can go back and forth.
- **Small.** At most 72 columns wide and about 15 lines high. Bigger → split into two pictures (main path, then the error branch).
- **One character set per picture.** Box drawing `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼` with arrows `▶ ◀ ▲ ▼`. If the developer says boxes look broken, switch to plain ASCII `+ - | > < ^ v` for the rest of the session.
- **Alignment is the whole point.** Every character takes one column. Keep labels inside boxes short (up to ~14 characters). Never put emoji or CJK characters inside a drawing: they take two columns and break the lines; put such text in the legend. Latin letters with diacritics (Vietnamese, French…) are fine. Before sending, check that every vertical line stays in the same column from top to bottom.
- **Legend and takeaway.** Under the picture: what the symbols mean if not obvious, and 1–2 sentences on **what to notice** ("Notice that check and change happen in one arrow, (3)").

## 3. Templates

### 3.1 Who talks to whom

```text
┌──────────┐ (1) POST /holds  ┌─────┐ (2) UPDATE seat ┌──────────┐
│ SeatMap  │ ───────────────▶ │ api │ ──────────────▶ │    db    │
│ (screen) │ ◀─────────────── │     │ ◀────────────── │ Postgres │
└──────────┘ (4) 201 / 409    └─────┘ (3) 1 or 0 rows └──────────┘
```

Notice: the screen never talks to the database; everything goes through `api`.

### 3.2 Steps in time

The translation of a Mermaid `sequenceDiagram`: one column per participant, time goes down, arrow numbers match the steps.

```text
SeatMap            api           HoldService             db
  │ (1) POST /holds │                 │                   │
  │────────────────▶│                 │                   │
  │                 │ (2) hold(A-12)  │                   │
  │                 │────────────────▶│                   │
  │                 │                 │ (3) UPDATE…FREE   │
  │                 │                 │──────────────────▶│
  │                 │                 │ (4) 1 row         │
  │                 │                 │◀──────────────────│
  │                 │ (5) Hold        │                   │
  │                 │◀────────────────│                   │
  │ (6) 201 + hold  │                 │                   │
  │◀────────────────│                 │                   │
```

Draw the main path; put each `alt` branch of the flow in a decision tree (§3.6) instead of cramming it in.

### 3.3 Timeline in two lanes (races, locks, retries)

Show the bug first, then the fix, with the same two people and the same values.

```text
         Lan                          Minh
time  │  SELECT A-12 → FREE
      │                               SELECT A-12 → FREE
      │  UPDATE A-12 → HELD
      ▼                               UPDATE A-12 → HELD  ✗ sold twice
```

```text
         Lan                          Minh
time  │  UPDATE … WHERE status='FREE'
      │    → 1 row: HELD ✓            UPDATE … WHERE status='FREE'
      │                                 (waits until Lan's is done)
      ▼                                 → 0 rows: 409 seat-taken
```

Notice: in the first picture both read "FREE" before either writes; in the second there is no gap between check and change.

### 3.4 State diagram

```text
            (1) click, E-01              (2) pay
  ┌──────┐ ────────────────▶ ┌──────┐ ────────────▶ ┌──────┐
  │ FREE │                   │ HELD │               │ SOLD │
  └──────┘ ◀──────────────── └──────┘               └──────┘
            (3) hold expires
```

Every arrow is a transition from the data document's transition table: what triggers it and who does it. A state with no way out (`SOLD`) is worth pointing out.

### 3.5 Layer map

```text
HTTP request
    │
    ▼
HoldController.create      api/…/HoldController.java   to create
    │  reads the body, turns SeatTaken into 409
    ▼
HoldService.hold           api/…/HoldService.java      exists (P2-01)
    │  the rule: only FREE → HELD
    ▼
SeatRepository.holdIfFree  api/…/SeatRepository.java   to create
    │  UPDATE seat … WHERE status='FREE'
    ▼
PostgreSQL: seat
```

Paths and "exists / to create" come from the code mapping (`briefing.md` §5).

### 3.6 Decision tree

```text
rows updated by (3)?
  ├── 1 → commit → 201 + hold     → seat turns blue, countdown starts
  └── 0 → 409 seat-taken          → toast "This seat was just taken"
```

One branch per `alt` of the flow, ending in what the user sees.

### 3.7 Wireframe with numbered regions

Start from the screen file's own wireframe when it has one.

```text
┌─────────────────────────────────────────────┐
│ Show 42 · Hamlet           Time left 09:58  │ (3)
├─────────────────────────────────────────────┤
│  A  [ ][ ][#][ ][ ]                         │ (1)
│  B  [ ][ ][ ][x][ ]                         │
├─────────────────────────────────────────────┤
│ Selected: A-12                     [ Pay ]  │ (2)
└─────────────────────────────────────────────┘
[ ] free   [#] held by you   [x] taken
```

Then: "(1) the seat map, data from E-02 · (2) the selection bar · (3) the countdown, from `expiresAt`".

### 3.8 Table relationships

```text
┌──────┐ 1      n ┌──────┐ 1    0..1 ┌──────┐
│ show │──────────│ seat │───────────│ hold │
└──────┘          └──────┘           └──────┘
 id                id                 seat_id
                   show_id            expires_at
                   status
```

Only the tables and columns this task touches. `1 … n`: one show has many seats.

### 3.9 Before and after

```text
seat                    after (3) for Lan          after (3) for Minh
id    show  status      id    show  status         (0 rows, unchanged)
A-12  42    FREE   ──▶  A-12  42    HELD     ──▶   A-12  42    HELD
A-13  42    FREE        A-13  42    FREE           A-13  42    FREE
```

A markdown table works too when the terminal renders it; the text form keeps the arrow between states.
