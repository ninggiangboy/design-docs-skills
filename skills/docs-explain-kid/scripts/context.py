#!/usr/bin/env python3
"""Gather the documentation context of one task, feature, use case, flow, endpoint or screen.

Reads a docs/ tree built with the docs-master-plan and docs-project skills and
builds a reference graph: an item (FR-01, P2-03, FL-07, E-12…) is defined where
check_docs.py says it is (a heading, the first cell of a table row, a status
line), and it references every ID written inside its section or row. Prints,
one fact per line:

  DEF   where the item is defined: path:line [status] title (ALSO: other definitions)
  ROW   the cells of a defining table row (a task's acceptance, dependencies, documents)
  SECT  the line range to read for a heading definition
  FILE  the queried file: path [status] DOC-xx
  OUT   items the query references, with their definition and status
  IN    items and files that reference the query
  HOP2  second-hop neighbours (via an OUT or IN item), skipped for DOC/ADR
  READY for a task: ok, or wait/block with the reason (dependencies not done,
        documents not Approved or not written, related DRs still proposed)
  GAP   undefined IDs, proposed DRs, non-empty open questions, documents not Approved
  HIT   for a free-text query: headings, rows and files that match the words

Status is the file's status, a DR's state (Proposed / Decided / Changed) or a
task's state (Done / Open). Labels are read from the vocabularies, like check_docs.py.

Usage: context.py [docs_dir] <ID | path to a .md file | words…> [--depth 1|2] [--max N]
       exit 0 when something was found, 1 when nothing matches, 2 on a bad docs dir
"""

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True  # keep the installed skill directory clean
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_docs import (  # noqa: E402  (shared checker, same directory)
    HEADING_DEF_RE, ID, ID_RE, STATUS_DOC_RE, STATUS_VALUES, TABLE_DEF_RE, alternation, load_vocab, prefix_of,
)

FULL_ID_RE = re.compile(rf"^{ID}$")
TASK_RE = re.compile(r"^P\d+-\d+$")
NO_EXPAND = ("DOC", "ADR")
EMPTY_MARKERS = {"", "—", "-"}


@dataclass
class Def:
    id: str
    rel: str
    line: int
    kind: str  # heading | row | doc
    end: int = 0
    level: int = 0
    title: str = ""
    cells: dict[str, str] = field(default_factory=dict)


@dataclass
class File:
    rel: str
    lines: list[str]
    status: str | None
    doc_id: str | None
    headings: list[tuple[int, int, str]] = field(default_factory=list)  # (line, level, text)
    code_lines: set[int] = field(default_factory=set)
    open_q: tuple[int, list[str]] | None = None


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def short(text: str, n: int = 90) -> str:
    text = re.sub(r"\s+", " ", text.replace("**", "")).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


class Index:
    def __init__(self, root: Path, vocab: dict[str, set[str]]):
        self.root = root
        self.vocab = vocab
        self.files: dict[str, File] = {}
        self.defs: dict[str, list[Def]] = defaultdict(list)
        self.mentions: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self.doc_files: dict[str, str] = {}
        status_re = re.compile(
            rf"({alternation(vocab['meta.status'], 'Status')})[^:：]*[:：]\s*\**\s*({STATUS_VALUES})", re.I)
        open_q_re = re.compile(
            rf"^(#{{2,6}})\s+(?:\d+(?:\.\d+)*\.?\s+)?({alternation(vocab['heading.open_questions'], 'Open questions')})",
            re.I)
        for path in sorted(p for p in root.rglob("*.md") if "assets" not in p.parts):
            self._read(path, status_re, open_q_re)
        self.defined = set(self.defs)
        self.known_prefixes = {prefix_of(d) for d in self.defined}

    def _read(self, path: Path, status_re: re.Pattern, open_q_re: re.Pattern) -> None:
        rel = str(path.relative_to(self.root.parent))
        lines = path.read_text(encoding="utf-8").splitlines()
        head = "\n".join(lines[:8])
        sm = status_re.search(head)
        docs = STATUS_DOC_RE.findall(head)
        f = File(rel, lines, sm.group(2).capitalize() if sm else None, docs[0] if docs else None)
        self.files[rel] = f
        for d in docs:
            self.doc_files.setdefault(d, rel)
            self.defs[d].append(Def(d, rel, 1, "doc", len(lines), 0, short(lines[0].lstrip("# "))))
        if path.parent.name.endswith("adr") and (m := re.match(r"(\d{4})-", path.name)):
            self.defs[f"ADR-{m.group(1)}"].append(Def(f"ADR-{m.group(1)}", rel, 1, "doc", len(lines), 0,
                                                      short(lines[0].lstrip("# ") if lines else path.name)))
        plan = path.name.startswith("00-master-plan")
        in_code = False
        header: list[str] = []
        prev_table = False
        open_q_level, open_q_start, open_q_body = None, 0, []
        heading_defs: list[Def] = []
        for no, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                f.code_lines.add(no)
                continue
            if in_code:
                f.code_lines.add(no)
                if not plan:
                    for tok in ID_RE.findall(line):
                        self.mentions[tok].append((rel, no))
                continue
            hm = re.match(r"^(#{1,6})\s+(.*)", line)
            if hm:
                level = len(hm.group(1))
                f.headings.append((no, level, hm.group(2).strip()))
                if open_q_level is not None and level <= open_q_level:
                    f.open_q = (open_q_start, open_q_body)
                    open_q_level = None
                if oq := open_q_re.match(line):
                    open_q_level, open_q_start, open_q_body = len(oq.group(1)), no, []
                if m := HEADING_DEF_RE.match(line):
                    d = Def(m.group(1), rel, no, "heading", 0, level, short(hm.group(2)))
                    self.defs[d.id].append(d)
                    heading_defs.append(d)
            elif open_q_level is not None and line.strip():
                open_q_body.append(line.strip())
            is_table = line.startswith("|")
            if is_table and not prev_table:
                header = cells_of(line)
            elif is_table and not re.match(r"^\|[\s:|-]+\|?$", line) and (m := TABLE_DEF_RE.match(line)):
                cells = cells_of(line)
                named = {header[i] if i < len(header) and header[i] else str(i): c for i, c in enumerate(cells)}
                self.defs[m.group(1)].append(
                    Def(m.group(1), rel, no, "row", no, 0, short(" · ".join(cells[:2])), named))
            prev_table = is_table
            for tok in ID_RE.findall(line):
                self.mentions[tok].append((rel, no))
        if open_q_level is not None:
            f.open_q = (open_q_start, open_q_body)
        for d in heading_defs:
            d.end = next((n - 1 for n, lv, _ in f.headings if n > d.line and lv <= d.level), len(lines))

    # --- lookup helpers -------------------------------------------------

    def primary(self, item: str) -> Def | None:
        def score(d: Def) -> int:
            base = {"doc": -1, "heading": 0, "row": 1}[d.kind]
            in_index = Path(d.rel).name in ("README.md",) or Path(d.rel).name.startswith("00-master-plan")
            return base + (3 if in_index and not TASK_RE.match(item) else 0)
        defs = self.defs.get(item)
        return min(defs, key=lambda d: (score(d), d.rel, d.line)) if defs else None

    def owner(self, rel: str, no: int) -> str:
        """The innermost item whose definition contains this line, or the file itself."""
        best = None
        for item, defs in self.defs.items():
            for d in defs:
                if d.rel != rel or d.kind == "doc":
                    continue
                if d.kind == "row" and d.line == no:
                    return item
                if d.kind == "heading" and d.line <= no <= d.end and (best is None or d.line > best[1]):
                    best = (item, d.line)
        if best:
            return best[0]
        f = self.files[rel]
        return f.doc_id or f"file:{rel}"

    def known(self, item: str) -> bool:
        return prefix_of(item) in self.known_prefixes

    def ranges(self, item: str) -> list[tuple[str, int, int]]:
        return [(d.rel, d.line, d.end) for d in self.defs.get(item, []) if d.kind != "doc"]

    def state(self, item: str) -> str:
        d = self.primary(item)
        if item.startswith("file:"):
            return self.files[item[5:]].status or "no status"
        if d is None:
            return "not written" if item.startswith("DOC-") else "undefined"
        if prefix_of(item) == "DR" and d.kind == "heading":
            title = self.files[d.rel].lines[d.line - 1]
            for key, label in (("dr.changed", "Changed"), ("dr.decided", "Decided")):
                if any(re.search(rf"\b{re.escape(v)}\b", title, re.I) for v in self.vocab[key] or {label}):
                    return label
            return "Proposed"
        if TASK_RE.match(item) and d.kind == "row":
            row = self.files[d.rel].lines[d.line - 1]
            done = {v.split("{")[0].strip() for v in self.vocab["plan.done"] or {"Done {date}"}}
            done |= {v.split("}")[-1].strip() for v in self.vocab["plan.done"] if v.startswith("{")}
            return "Done" if any(v and re.search(rf"\*\*\s*{re.escape(v)}", row) for v in done) else "Open"
        return self.files[d.rel].status or "no status"

    def node(self, item: str) -> str:
        if item.startswith("file:"):
            return f"{item[5:]} [{self.state(item)}]"
        d = self.primary(item)
        if d is None:
            return f"{item} [{self.state(item)}]"
        loc = d.rel if d.kind == "doc" else f"{d.rel}:{d.line}"
        return f"{item} {loc} [{self.state(item)}] {d.title}"

    def out_of(self, item: str) -> list[str]:
        seen: dict[str, None] = {}
        for rel, start, end in self.ranges(item):
            for no in range(start, end + 1):
                for tok in ID_RE.findall(self.files[rel].lines[no - 1]):
                    if tok != item and self.known(tok):
                        seen.setdefault(tok)
        return list(seen)

    def in_of(self, item: str) -> dict[str, tuple[str, int]]:
        own = self.ranges(item)
        found: dict[str, tuple[str, int]] = {}
        for rel, no in self.mentions.get(item, []):
            if any(rel == r and s <= no <= e for r, s, e in own):
                continue
            o = self.owner(rel, no)
            if o != item:
                found.setdefault(o, (rel, no))
        return found


def find_file(index: Index, query: str) -> str | None:
    q = query.strip()
    for cand in (Path(q), index.root / q, index.root.parent / q):
        if cand.is_file():
            try:
                rel = str(cand.resolve().relative_to(index.root.parent))
            except ValueError:
                return None
            return rel if rel in index.files else None
    matches = [rel for rel in index.files if rel.endswith("/" + q) or Path(rel).name == q]
    return matches[0] if len(matches) == 1 else None


def gaps(index: Index, items: list[str], files: set[str]) -> list[str]:
    out = []
    for item in items:
        if prefix_of(item) in index.known_prefixes and item not in index.defined and not item.startswith("DOC-"):
            where = index.mentions.get(item, [("?", 0)])[0]
            out.append(f"GAP undefined {item} (referenced at {where[0]}:{where[1]})")
        if prefix_of(item) == "DR" and item in index.defined and index.state(item) == "Proposed":
            out.append(f"GAP proposed {index.node(item)}")
        if item.startswith("DOC-") and item not in index.doc_files:
            out.append(f"GAP not-written {item}")
    none_prefixes = tuple(v.lower().rstrip(".。") for v in index.vocab["phrase.none"] or {"None."})
    for rel in sorted(files):
        f = index.files[rel]
        if f.status and f.status not in ("Approved", "Accepted") and not Path(rel).name.startswith("00-"):
            out.append(f"GAP not-approved {rel} [{f.status}]")
        if f.open_q:
            start, body = f.open_q
            text = " ".join(body).strip()
            if text.lower() not in EMPTY_MARKERS and not text.lower().startswith(none_prefixes):
                out.append(f"GAP open-questions {rel}:{start}: {short(text, 110)}")
    return list(dict.fromkeys(out))


def readiness(index: Index, task: str) -> list[str]:
    d = index.primary(task)
    if d is None or d.kind != "row":
        return []
    def column(key: str, fallback: str) -> str:
        names = index.vocab[key] or {fallback}
        return next((v for k, v in d.cells.items() if k in names), "")
    out = []
    for dep in ID_RE.findall(column("col.depends", "Depends on")):
        if TASK_RE.match(dep) and not dep.endswith("-00") and index.state(dep) != "Done":
            out.append(f"READY wait {dep} is {index.state(dep)}: {index.primary(dep).title if index.primary(dep) else ''}")
    plan = index.files[d.rel]
    for ms in re.findall(r"\bM\d+\b", column("col.depends", "Depends on")):
        templates = index.vocab["plan.reached"] or {"{milestone} reached on {date}."}
        pats = [re.escape(t).replace(re.escape("{milestone}"), re.escape(ms)).replace(re.escape("{date}"), r".+?")
                for t in templates]
        if not any(re.search(p.rstrip(r"\."), line) for p in pats for line in plan.lines):
            out.append(f"READY wait {ms} not recorded as reached in {d.rel}")
    docs = ID_RE.findall(column("col.documents", "Documents"))
    gate = re.sub(r"-\d+$", "-00", task)
    if gate != task and (g := index.primary(gate)) and g.kind == "row":
        docs += ID_RE.findall(" ".join(g.cells.values()))
    for doc in dict.fromkeys(x for x in docs if x.startswith(("DOC-", "ADR-"))):
        st = index.state(doc)
        if st not in ("Approved", "Accepted"):
            out.append(f"READY block {doc} is {st}" + (f" ({index.doc_files[doc]})" if doc in index.doc_files else ""))
    drs = [x for x in index.out_of(task) if x.startswith("DR-")]
    for doc in docs:
        drs += [o for o in index.in_of(doc) if o.startswith("DR-")]
    for dr in dict.fromkeys(drs):
        if index.state(dr) == "Proposed":
            out.append(f"READY block {dr} is Proposed: {index.primary(dr).title if index.primary(dr) else ''}")
    return out or ["READY ok"]


def print_neighbours(index: Index, query: str, outs: list[str], ins: dict[str, tuple[str, int]],
                     depth: int, limit: int) -> set[str]:
    files = set()
    for item in outs:
        print(f"OUT  {index.node(item)}")
        if (d := index.primary(item)):
            files.add(d.rel)
    for item, (rel, no) in ins.items():
        print(f"IN   {index.node(item)}  (at {rel}:{no})")
        files.add(rel)
    if depth >= 2:
        shown = {query, *outs, *ins}
        count = 0
        for via in [*outs, *ins]:
            if via.startswith("file:") or prefix_of(via) in NO_EXPAND or via not in index.defined:
                continue
            for item in [*index.out_of(via), *index.in_of(via)]:
                if item in shown or item.startswith("file:"):
                    continue
                shown.add(item)
                count += 1
                if count > limit:
                    print(f"HOP2 … more than {limit}; rerun with --max")
                    return files
                print(f"HOP2 via {via} -> {index.node(item)}")
    return files


def query_id(index: Index, item: str, depth: int, limit: int) -> int:
    if item.startswith("DOC-") and item in index.doc_files:
        return query_file(index, index.doc_files[item], depth, limit)
    d = index.primary(item)
    if d is None:
        where = index.mentions.get(item)
        if not where:
            print(f"result: {item} is neither defined nor referenced")
            return 1
        print(f"GAP undefined {item}: referenced but never defined")
        owners: dict[str, tuple[str, int]] = {}
        for rel, no in where:
            owners.setdefault(index.owner(rel, no), (rel, no))
        for owner, (rel, no) in owners.items():
            print(f"IN   {index.node(owner)}  (at {rel}:{no})")
        return 0
    print(f"DEF  {index.node(item)}")
    for other in index.defs[item]:
        if other is not d:
            print(f"ALSO {other.rel}:{other.line} {other.title}")
    if d.kind == "row":
        for k, v in d.cells.items():
            print(f"ROW  {k}: {v}")
    else:
        print(f"SECT {d.rel}:{d.line}-{d.end}")
    outs, ins = index.out_of(item), index.in_of(item)
    files = {d.rel} | print_neighbours(index, item, outs, ins, depth, limit)
    if TASK_RE.match(item):
        for line in readiness(index, item):
            print(line)
    for line in gaps(index, [item, *outs, *ins], files):
        print(line)
    return 0


def query_file(index: Index, rel: str, depth: int, limit: int) -> int:
    f = index.files[rel]
    print(f"FILE {rel} [{f.status or 'no status'}] {f.doc_id or ''}".rstrip())
    own = [i for i, defs in index.defs.items() if any(d.rel == rel and d.kind != "doc" for d in defs)]
    for item in own[:limit]:
        print(f"DEF  {index.node(item)}")
    outs: dict[str, None] = {}
    for no, line in enumerate(f.lines, 1):
        for tok in ID_RE.findall(line):
            if tok not in own and tok != f.doc_id and index.known(tok):
                outs.setdefault(tok)
    ins = index.in_of(f.doc_id) if f.doc_id else {}
    name = Path(rel).name
    for other, of in index.files.items():
        if other == rel:
            continue
        for no, line in enumerate(of.lines, 1):
            if re.search(rf"\]\([^)]*{re.escape(name)}", line):
                ins.setdefault(index.owner(other, no), (other, no))
    ins = {k: v for k, v in ins.items() if k not in own}
    files = {rel} | print_neighbours(index, f.doc_id or "", list(outs), ins, depth, limit)
    for line in gaps(index, list(outs), files):
        print(line)
    return 0


def query_words(index: Index, words: str, limit: int) -> int:
    norm = lambda s: re.sub(r"[-_/·`*]", " ", s.lower())
    tokens = [t for t in norm(words).split() if len(t) > 1]
    hits = []
    for rel, f in index.files.items():
        name_score = sum(t in norm(rel) for t in tokens)
        if name_score:
            hits.append((name_score + 0.5, f"HIT  {rel} [{f.status or 'no status'}] {f.doc_id or ''}".rstrip()))
        for no, level, text in f.headings:
            score = sum(t in norm(text) for t in tokens)
            if score:
                hits.append((score, f"HIT  {rel}:{no} {short(text)}"))
    for item, defs in index.defs.items():
        for d in defs:
            if d.kind == "row":
                score = sum(t in norm(" ".join(d.cells.values())) for t in tokens)
                if score:
                    hits.append((score - 0.25, f"HIT  {item} {d.rel}:{d.line} {d.title}"))
    if not hits:
        print(f"result: nothing matches '{words}'")
        return 1
    for _, line in sorted(hits, key=lambda h: -h[0])[:limit]:
        print(line)
    return 0


def main() -> int:
    argv = sys.argv[1:]
    depth, limit = 2, 40
    for flag in ("--depth", "--max"):
        if flag in argv:
            i = argv.index(flag)
            value = int(argv[i + 1])
            depth, limit = (value, limit) if flag == "--depth" else (depth, value)
            del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    root = Path("docs")
    if len(args) >= 2 and Path(args[0]).is_dir():
        root = Path(args.pop(0))
    if not args:
        print(__doc__)
        return 2
    root = root.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2
    locales = sorted((Path(__file__).resolve().parent.parent / "locales").glob("*.md"))
    index = Index(root, load_vocab(locales + [root / "00-master-plan.md"]))
    query = " ".join(args)
    if FULL_ID_RE.match(query):
        return query_id(index, query, depth, limit)
    if rel := find_file(index, query):
        return query_file(index, rel, depth, limit)
    return query_words(index, query, limit)


if __name__ == "__main__":
    sys.exit(main())
