#!/usr/bin/env python3
"""Check a docs/ tree built with the docs-project skill.

Checks:
  E1  reference to an ID whose prefix is known but the ID itself is never defined
  E2  relative markdown link to a file that does not exist
  W1  file without a status line in its first lines
  W2  Approved/Accepted file whose "open questions" section is not empty
  I1  status counts, and DOC-xx listed in the master plan without a file

An ID is "defined" when it starts a heading (`### FR-02 · ...`, `# RB-02: ...`),
is the first cell of a table row (`| FR-02.1 | ...`), is a DOC-xx in a status
line or in a `# DOC-xx` comment inside a code block, or is ADR-NNNN from a file
name `NNNN-*.md`. Only prefixes that have at least one definition are checked,
so tokens like SHA-256 or UTF-8 are ignored.

Usage: check_docs.py [docs_dir] [--strict]   (exit 1 on errors; --strict also on warnings)
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ID = r"[A-Z][A-Z0-9]{0,5}(?:-[A-Z]{2,10})?-\d{1,4}(?:\.\d+)?"
ID_RE = re.compile(rf"(?<![\w/.-])({ID})(?![\w-])")
HEADING_DEF_RE = re.compile(rf"^#{{1,6}}\s+(?:[^\s`]+:\s*)?\**({ID})\b")
TABLE_DEF_RE = re.compile(rf"^\|\s*\**\[?({ID})\]?(?:\([^)]*\))?\**(?:\s*(?:\[[^\]]*\]|\([^)]*\)))*\s*\|")
DOC_COMMENT_RE = re.compile(r"#\s*(DOC-\d+)")
STATUS_RE = re.compile(r"(Trạng thái|Status)[^:]*:\s*\**\s*(Draft|Review|Approved|Superseded|Accepted|Proposed|Deprecated)", re.I)
STATUS_DOC_RE = re.compile(r"(?:^>\s*|·\s*)(DOC-\d+)", re.M)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
OPEN_Q_RE = re.compile(r"^(#{2,6})\s+(?:\d+(?:\.\d+)*\.?\s+)?(Câu hỏi còn mở|Open questions)", re.I)
EMPTY_PREFIXES = ("không có", "không còn", "none")
EMPTY_MARKERS = {"", "—", "-"}


def prefix_of(token: str) -> str:
    return token.rsplit("-", 1)[0]


def parent_of(token: str) -> str | None:
    return token.split(".", 1)[0] if "." in token else None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    root = Path(args[0] if args else "docs").resolve()
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2

    files = sorted(p for p in root.rglob("*.md") if "assets" not in p.parts)
    defined: set[str] = set()
    refs: list[tuple[Path, int, str]] = []
    errors: list[str] = []
    warnings: list[str] = []
    statuses: Counter = Counter()
    doc_files: dict[str, Path] = {}
    plan_docs: set[str] = set()

    for path in files:
        rel = path.relative_to(root.parent)
        if path.parent.name.endswith("adr"):
            m = re.match(r"(\d{4})-", path.name)
            if m:
                defined.add(f"ADR-{m.group(1)}")
        lines = path.read_text(encoding="utf-8").splitlines()

        head = "\n".join(lines[:8])
        sm = STATUS_RE.search(head)
        for d in STATUS_DOC_RE.findall(head):
            defined.add(d)
            doc_files.setdefault(d, path)
        if sm:
            statuses[sm.group(2).capitalize()] += 1
        elif path.name != "README.md":
            warnings.append(f"W1 {rel}: no status line in the first 8 lines")
        status = sm.group(2).capitalize() if sm else None

        in_code = False
        open_q_level = None
        open_q_body: list[str] = []
        for no, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                if path.name.startswith("00-master-plan"):
                    for d in DOC_COMMENT_RE.findall(line):
                        defined.add(d)
                        plan_docs.add(d)
                continue

            hm = re.match(r"^(#{1,6})\s", line)
            if open_q_level is not None and hm and len(hm.group(1)) <= open_q_level:
                open_q_level = None
            oq = OPEN_Q_RE.match(line)
            if oq:
                open_q_level = len(oq.group(1))
                continue
            if open_q_level is not None:
                open_q_body.append(line.strip())

            for rx in (HEADING_DEF_RE, TABLE_DEF_RE):
                m = rx.match(line)
                if m:
                    defined.add(m.group(1))
            for tok in ID_RE.findall(line):
                refs.append((rel, no, tok))
            for target in LINK_RE.findall(line):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).exists():
                    errors.append(f"E2 {rel}:{no}: broken link -> {target}")

        body = " ".join(open_q_body).strip().lower()
        if status in ("Approved", "Accepted") and body not in EMPTY_MARKERS and not body.startswith(EMPTY_PREFIXES):
            warnings.append(f"W2 {rel}: status {status} but open questions are not empty")

    known_prefixes = {prefix_of(d) for d in defined}
    undefined = defaultdict(list)
    for rel, no, tok in refs:
        if prefix_of(tok) not in known_prefixes or tok in defined:
            continue
        if parent_of(tok) in defined and parent_of(tok) == tok:
            continue
        undefined[tok].append(f"{rel}:{no}")
    for tok in sorted(undefined):
        where = undefined[tok]
        more = f" (+{len(where) - 3} more)" if len(where) > 3 else ""
        errors.append(f"E1 {tok} is referenced but never defined: {', '.join(where[:3])}{more}")

    for e in errors:
        print(e)
    for w in warnings:
        print(w)
    missing = sorted(plan_docs - set(doc_files), key=lambda d: int(d.split("-")[1]))
    print(f"I1 files: {len(files)} · status: {dict(statuses)} · defined IDs: {len(defined)} "
          f"across {len(known_prefixes)} prefixes")
    if missing:
        print(f"I1 DOC in master plan without a file yet: {', '.join(missing)}")
    print(f"result: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
