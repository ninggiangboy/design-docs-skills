#!/usr/bin/env python3
"""Check the internal consistency of an SDD written with the docs-system-design skill.

Checks:
  E1  H2 numbering is not 1, 2, 3, ... or an H3 does not match its parent H2
  E2  a cross reference ("section 8.4", "mục 8.4", "8.4 節", "§8.4", ...) points to a missing section
  E3  an ID (FR-, NFR-, UC-, EXP-) is referenced but never defined in a table
  E4  an ID is defined twice
  E5  unbalanced code fence
  W1  mermaid flowchart node label with brackets/parentheses that is not quoted
  W2  a defined EXP that nothing else references (no claim or phase uses it)
  I1  outline and counts

Cross-reference words come from the `ref.section` and `ref.joiners` keys of every
locales/*.md next to this script, plus --vocab FILE (any markdown file with a
vocabulary table, e.g. a master plan with a generated Appendix B). `§N` always works.

Usage: check_sdd.py <sdd.md> [--outline] [--vocab FILE]   (exit 1 on errors)
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

H2_RE = re.compile(r"^##\s+(\d+)\.\s+(.*)")
H3_RE = re.compile(r"^###\s+(\d+)\.(\d+)\s+(.*)")
H4_RE = re.compile(r"^####\s+(.*)")
NUM = r"\d+(?:\.\d+)?"
ID_PREFIXES = ("FR", "NFR", "UC", "EXP")
ID_RE = re.compile(r"(?<![\w-])((?:FR|NFR|UC|EXP)-\d{1,3}(?:\.\d+)?)(?![\w-])")
TABLE_DEF_RE = re.compile(r"^\|\s*\**((?:FR|NFR|UC|EXP)-\d{1,3}(?:\.\d+)?)\**(?:\s*\([^)]*\))?\s*\|")
MERMAID_NODE_RE = re.compile(r"\b\w+\s*[\[\({]+(?!\")([^\]\)}\"]*[()\[\]][^\]\)}\"]*)[\]\)}]+")
VOCAB_ROW_RE = re.compile(r"^\|\s*`?([a-z0-9_]+\.[a-z0-9_]+)`?\s*\|(.*)\|\s*$")


def load_vocab(paths: list[Path]) -> dict[str, set[str]]:
    """Collect every value (English and local) of every key in vocabulary tables."""
    vocab: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            m = VOCAB_ROW_RE.match(line)
            if not m:
                continue
            for cell in m.group(2).split("|"):
                for value in cell.split(" / "):
                    if value.strip():
                        vocab[m.group(1)].add(value.strip())
    return vocab


def ref_patterns(vocab: dict[str, set[str]]) -> list[re.Pattern]:
    """One regex per `ref.section` template; group 1 is a list of section numbers."""
    joiners = sorted(vocab["ref.joiners"] | {",", "、", "，", "–", "-"}, key=len, reverse=True)
    joiner = "|".join(re.escape(j) for j in joiners)
    number_list = rf"(?<![\d.])({NUM}(?:\s*(?:{joiner})\s*{NUM})*)"
    patterns = []
    for template in vocab["ref.section"] | {"section {n}", "§{n}"}:
        if "{n}" not in template:
            continue
        before, after = (part.strip() for part in template.split("{n}", 1))
        boundary = r"(?<![A-Za-z])" if before[:1].isascii() and before[:1].isalpha() else ""
        before_re = r"\s*".join(re.escape(w) for w in before.split())
        if before[-1:].isascii() and before[-1:].isalpha():
            before_re += r"[a-z]{0,2}"  # plural: sections, Abschnitte, secciones
        after_re = r"\s*".join(re.escape(w) for w in after.split())
        patterns.append(re.compile(rf"{boundary}{before_re}\s*{number_list}" + (rf"\s*{after_re}" if after_re else ""), re.I))
    return patterns


def expand(numbers: str) -> list[str]:
    """'1.1, 1.3' -> ['1.1', '1.3']; '8.2 và 4' -> ['8.2', '8.4'] (a bare number after a dotted one is a sibling)."""
    found = re.findall(NUM, numbers)
    out = [found[0]]
    for extra in found[1:]:
        if "." in extra or "." not in found[0]:
            out.append(extra)
        else:
            out.append(f"{found[0].split('.')[0]}.{extra}")
    return out


def main() -> int:
    argv = sys.argv[1:]
    extra_vocab = []
    if "--vocab" in argv:
        i = argv.index("--vocab")
        extra_vocab = [Path(argv[i + 1])]
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    path = Path(args[0])
    lines = path.read_text(encoding="utf-8").splitlines()
    locales = sorted((Path(__file__).resolve().parent.parent / "locales").glob("*.md"))
    patterns = ref_patterns(load_vocab(locales + extra_vocab))
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
    is_flowchart = False

    for no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code, fence_line = True, no
                nxt = lines[no] if no < len(lines) else ""
                is_flowchart = stripped[3:].strip() == "mermaid" and bool(re.match(r"^\s*(flowchart|graph)\b", nxt))
            else:
                in_code = False
            continue
        if in_code:
            if is_flowchart:
                for m in MERMAID_NODE_RE.finditer(line):
                    if "--" not in m.group(1):
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
        for tok in ID_RE.findall(line[dm.end():] if dm else line):
            refs[tok].append(no)
        spans: list[tuple[int, int]] = []
        for pattern in patterns:
            for m in pattern.finditer(line):
                if any(a <= m.start(1) < b for a, b in spans):
                    continue
                spans.append((m.start(1), m.end(1)))
                sec_refs.extend((no, ref) for ref in expand(m.group(1)))

    if in_code:
        errors.append(f"E5 code fence opened at line {fence_line} is never closed")

    for no, ref in sec_refs:
        if ref not in sections:
            errors.append(f"E2 line {no}: section {ref} does not exist")

    for tok, where in sorted(refs.items()):
        if tok in defined or ("." in tok and tok.split(".", 1)[0] in defined):
            continue
        errors.append(f"E3 {tok} referenced at line {', '.join(map(str, where[:5]))} but never defined in a table")
    for tok, n in sorted(defined.items()):
        if n > 1:
            errors.append(f"E4 {tok} defined {n} times (first at line {def_line[tok]})")
        if tok.startswith("EXP") and not refs.get(tok):
            warnings.append(f"W2 {tok} (line {def_line[tok]}) is defined but referenced nowhere else")

    if "--outline" in argv:
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
