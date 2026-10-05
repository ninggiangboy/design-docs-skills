#!/usr/bin/env python3
"""Check the internal consistency of an SDD written with the docs-system-design skill.

Checks:
  E1  H2 numbering is not 1, 2, 3, ... or an H3 does not match its parent H2
  E2  a cross reference "mục X" / "mục X.Y" points to a section that does not exist
  E3  an ID (FR-, NFR-, UC-, EXP-) is referenced but never defined in a table
  E4  an ID is defined twice
  E5  unbalanced code fence
  W1  mermaid flowchart node label with brackets/parentheses that is not quoted
  W2  a defined EXP that nothing else references (no claim or phase uses it)
  I1  outline and counts

Usage: check_sdd.py <sdd.md> [--outline]   (exit 1 on errors)
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

H2_RE = re.compile(r"^##\s+(\d+)\.\s+(.*)")
H3_RE = re.compile(r"^###\s+(\d+)\.(\d+)\s+(.*)")
H4_RE = re.compile(r"^####\s+(.*)")
REF_RE = re.compile(r"\b[Mm]ục\s+(\d+(?:\.\d+)?)((?:\s*(?:,|và|hoặc|đến|tới|–|-)\s*\d+(?:\.\d+)?)*)")
ID_PREFIXES = ("FR", "NFR", "UC", "EXP")
ID_RE = re.compile(r"(?<![\w-])((?:FR|NFR|UC|EXP)-\d{1,3}(?:\.\d+)?)(?![\w-])")
TABLE_DEF_RE = re.compile(r"^\|\s*\**((?:FR|NFR|UC|EXP)-\d{1,3}(?:\.\d+)?)\**(?:\s*\([^)]*\))?\s*\|")
MERMAID_NODE_RE = re.compile(r"\b\w+\s*[\[\({]+(?!\")([^\]\)}\"]*[()\[\]][^\]\)}\"]*)[\]\)}]+")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    path = Path(args[0])
    lines = path.read_text(encoding="utf-8").splitlines()
    errors, warnings = [], []

    sections: set[str] = set()
    outline: list[str] = []
    defined: Counter = Counter()
    def_line: dict[str, int] = {}
    refs: dict[str, list[int]] = defaultdict(list)
    sec_refs: list[tuple[int, str]] = []

    expected_h2 = 1
    current_h2 = None
    expected_h3 = 1
    in_code = False
    fence_line = 0
    code_lang = ""

    for no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code, fence_line, code_lang = True, no, stripped[3:].strip()
            else:
                in_code = False
            continue
        if in_code:
            if code_lang == "mermaid" and re.match(r"^\s*(flowchart|graph)\b", lines[fence_line] if fence_line < len(lines) else ""):
                for m in MERMAID_NODE_RE.finditer(line):
                    if "-->" in m.group(0) or "--" in m.group(1):
                        continue
                    warnings.append(f"W1 line {no}: unquoted mermaid label with brackets: {m.group(0).strip()[:60]}")
            for tok in ID_RE.findall(line):
                refs[tok].append(no)
            continue

        m2 = H2_RE.match(line)
        if m2:
            n = int(m2.group(1))
            if n != expected_h2:
                errors.append(f"E1 line {no}: H2 numbered {n}, expected {expected_h2}")
            expected_h2 = n + 1
            current_h2, expected_h3 = n, 1
            sections.add(str(n))
            outline.append(f"{n}. {m2.group(2)}")
            continue
        if line.startswith("## "):
            current_h2 = None
            outline.append(line[3:])
            continue
        m3 = H3_RE.match(line)
        if m3:
            p, c = int(m3.group(1)), int(m3.group(2))
            if p != current_h2:
                errors.append(f"E1 line {no}: H3 {p}.{c} under H2 {current_h2}")
            elif c != expected_h3:
                errors.append(f"E1 line {no}: H3 numbered {p}.{c}, expected {p}.{expected_h3}")
            expected_h3 = c + 1
            sections.add(f"{p}.{c}")
            outline.append(f"  {p}.{c} {m3.group(3)}")
            continue
        m4 = H4_RE.match(line)
        if m4:
            outline.append(f"    - {m4.group(1)}")

        dm = TABLE_DEF_RE.match(line)
        if dm:
            defined[dm.group(1)] += 1
            def_line.setdefault(dm.group(1), no)
            rest = line[dm.end():]
            for tok in ID_RE.findall(rest):
                refs[tok].append(no)
        else:
            for tok in ID_RE.findall(line):
                refs[tok].append(no)
        for m in REF_RE.finditer(line):
            sec_refs.append((no, m.group(1)))
            for extra in re.findall(r"\d+(?:\.\d+)?", m.group(2)):
                if "." in extra or "." not in m.group(1):
                    sec_refs.append((no, extra))
                else:
                    sec_refs.append((no, f"{m.group(1).split('.')[0]}.{extra}"))

    if in_code:
        errors.append(f"E5 code fence opened at line {fence_line} is never closed")

    for no, ref in sec_refs:
        if ref not in sections:
            errors.append(f"E2 line {no}: 'mục {ref}' does not exist")

    for tok, where in sorted(refs.items()):
        if tok in defined:
            continue
        parent = tok.split(".", 1)[0]
        if parent in defined and "." in tok:
            continue
        errors.append(f"E3 {tok} referenced at line {', '.join(map(str, where[:5]))} but never defined in a table")
    for tok, n in sorted(defined.items()):
        if n > 1:
            errors.append(f"E4 {tok} defined {n} times (first at line {def_line[tok]})")
        if tok.startswith("EXP") and not refs.get(tok):
            warnings.append(f"W2 {tok} (line {def_line[tok]}) is defined but referenced nowhere else")

    if "--outline" in sys.argv:
        print("\n".join(outline))
    for e in errors:
        print(e)
    for w in warnings:
        print(w)
    counts = Counter(t.split("-")[0] for t in defined)
    mermaid = sum(1 for l in lines if l.strip() == "```mermaid")
    print(f"I1 {path.name}: {len(lines)} lines · {sum(1 for s in sections if '.' not in s)} H2 · "
          f"{sum(1 for s in sections if '.' in s)} H3 · mermaid {mermaid} · "
          + " · ".join(f"{p} {counts.get(p, 0)}" for p in ID_PREFIXES))
    print(f"result: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
