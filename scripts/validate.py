#!/usr/bin/env python3
"""Validate the skills in this repository.

1. Every skills/<dir>/SKILL.md has frontmatter with `name` equal to <dir>
   (lowercase, digits, hyphens, at most 64 chars) and a `description` of at most
   1024 chars without angle brackets.
2. Relative links in SKILL.md and `scripts/...` mentions point to files that exist.
3. No personal absolute paths leak into skill files.
4. Every locale has the keys, English column and {placeholders} of locales/en.md,
   and a Conventions section.
5. Files shared between skills are identical to their source skill.
6. The checker scripts give the expected result on tests/fixtures.

Usage: python3 scripts/validate.py [--fix]   (--fix copies shared files from their source skill)
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FIXTURES = ROOT / "tests" / "fixtures"
EXPLAIN = ["docs-explain", "docs-explain-kid"]
SHARED = {
    # (source skill, path): skills holding a copy
    ("docs-master-plan", "references/conventions.md"): ["docs-project", *EXPLAIN],
    ("docs-master-plan", "references/templates.md"): ["docs-project"],
    ("docs-master-plan", "references/language.md"): ["docs-project", "docs-system-design", *EXPLAIN],
    ("docs-master-plan", "scripts/check_docs.py"): ["docs-project", *EXPLAIN],
    ("docs-master-plan", "locales"): ["docs-project", "docs-system-design", *EXPLAIN],
    ("docs-explain", "references/briefing.md"): ["docs-explain-kid"],
    ("docs-explain", "scripts/context.py"): ["docs-explain-kid"],
}
CHECKS = [
    # (script, target, extra args, expected exit code, codes that must appear in the output)
    ("docs-system-design/scripts/check_sdd.py", "sdd-good.md", [], 0, []),
    ("docs-system-design/scripts/check_sdd.py", "sdd-good-en.md", [], 0, []),
    ("docs-system-design/scripts/check_sdd.py", "sdd-bad.md", [], 1, ["E1", "E2", "E3", "E4", "E5", "W1"]),
    ("docs-system-design/scripts/check_sdd.py", "sdd-bad-en.md", [], 1, ["E2"]),
    ("docs-project/scripts/check_docs.py", "docs-good", [], 0, []),
    ("docs-project/scripts/check_docs.py", "docs-good-en", ["--strict"], 0, []),
    ("docs-project/scripts/check_docs.py", "docs-bad", [], 1, ["E1", "E2", "W1", "W2"]),
    ("docs-project/scripts/check_docs.py", "docs-bad-it", [], 0, ["W2"]),
    ("docs-project/scripts/check_docs.py", "docs-task-en", [], 1, ["E1"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["P2-02"], 0, ["DEF", "ROW", "OUT", "IN", "HOP2", "READY", "GAP"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["P1-01"], 0, ["READY"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["08-ux-ui/screens/seat-map.md"], 0, ["FILE", "OUT", "IN", "GAP"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["E-02"], 0, ["GAP"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["seat", "map"], 0, ["HIT"]),
    ("docs-explain/scripts/context.py", "docs-task-en", ["ZZ-99"], 1, []),
]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)\s#]+)")
SCRIPT_RE = re.compile(r"`(?:<skill-dir>/)?(scripts/[\w.-]+)")
PERSONAL_RE = re.compile(r"(/home/\w+|/Users/\w+|~/dev/)")
ROW_RE = re.compile(r"^\| ([a-z0-9_]+\.[a-z0-9_]+) \| (.*?) \|(?: (.*) \|)?$")
PLACEHOLDER_RE = re.compile(r"\{\w+\}")

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"FAIL {msg}")


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skill(skill: Path) -> None:
    md = skill / "SKILL.md"
    if not md.exists():
        fail(f"{skill.name}: SKILL.md missing")
        return
    text = md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != skill.name:
        fail(f"{skill.name}: frontmatter name '{name}' does not match the directory")
    if not NAME_RE.match(name) or len(name) > 64:
        fail(f"{skill.name}: invalid name '{name}'")
    if not desc:
        fail(f"{skill.name}: description missing")
    if len(desc) > 1024:
        fail(f"{skill.name}: description is {len(desc)} chars (max 1024)")
    if "<" in desc or ">" in desc:
        fail(f"{skill.name}: description contains angle brackets")
    lines = text.count("\n")
    if lines > 500:
        fail(f"{skill.name}: SKILL.md has {lines} lines (keep under 500)")
    for target in LINK_RE.findall(text) + SCRIPT_RE.findall(text):
        if not target.startswith(("http:", "https:")) and not (skill / target).exists():
            fail(f"{skill.name}: SKILL.md refers to missing file {target}")
    if not (skill / "locales" / "en.md").exists():
        fail(f"{skill.name}: locales/en.md missing")
    for f in skill.rglob("*"):
        if f.is_file() and PERSONAL_RE.search(f.read_text(encoding="utf-8", errors="ignore")):
            fail(f"{skill.name}: personal path in {f.relative_to(skill)}")
    print(f"ok   {skill.name} ({len(desc)} chars description, {lines} lines)")


def parse_locale(path: Path) -> dict[str, tuple[str, str]]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3) if m.group(3) is not None else m.group(2))
    return rows


def check_locales() -> None:
    folder = SKILLS / "docs-master-plan" / "locales"
    en = parse_locale(folder / "en.md")
    if len(en) < 100:
        fail(f"locales/en.md has only {len(en)} keys")
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        rows = parse_locale(path)
        problems = []
        if missing := [k for k in en if k not in rows]:
            problems.append(f"missing keys {missing[:5]}")
        if extra := [k for k in rows if k not in en]:
            problems.append(f"unknown keys {extra[:5]}")
        if wrong_en := [k for k in en if k in rows and rows[k][0] != en[k][0]]:
            problems.append(f"English column differs for {wrong_en[:5]}")
        if bad := [k for k in en if k in rows and sorted(PLACEHOLDER_RE.findall(rows[k][1])) != sorted(PLACEHOLDER_RE.findall(en[k][0]))]:
            problems.append(f"placeholders differ for {bad[:5]}")
        if "## Conventions" not in text or not re.search(r"^Language: .+ · Code: ", text, re.M):
            problems.append("missing Language line or Conventions section")
        if problems:
            fail(f"locales/{path.name}: " + "; ".join(problems))
        else:
            print(f"ok   locales/{path.name} ({len(rows)} keys)")


def same(a: Path, b: Path) -> bool:
    if a.is_dir():
        names = sorted(p.name for p in a.iterdir())
        return b.is_dir() and names == sorted(p.name for p in b.iterdir()) and all(same(a / n, b / n) for n in names)
    return b.is_file() and a.read_bytes() == b.read_bytes()


def check_shared(fix: bool) -> None:
    for (source, rel), copies in SHARED.items():
        src = SKILLS / source / rel
        for copy in copies:
            dst = SKILLS / copy / rel
            if same(src, dst):
                continue
            if fix:
                if src.is_dir():
                    shutil.rmtree(dst, ignore_errors=True)
                    shutil.copytree(src, dst)
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dst)
                print(f"fix  copied {source}/{rel} -> {copy}/{rel}")
            else:
                fail(f"{copy}/{rel} differs from {source}/{rel} (run with --fix)")
    print("ok   shared files")


def check_scripts() -> None:
    for script, target, extra, code, expected in CHECKS:
        proc = subprocess.run(
            [sys.executable, str(SKILLS / script), str(FIXTURES / target), *extra],
            capture_output=True, text=True,
        )
        missing = [c for c in expected if not re.search(rf"^{c} ", proc.stdout, re.M)]
        if proc.returncode != code or missing:
            fail(f"{script} on {target}: exit {proc.returncode} (want {code}), missing {missing}\n{proc.stdout}{proc.stderr}")
        else:
            print(f"ok   {Path(script).name} on {target}")


def main() -> int:
    fix = "--fix" in sys.argv
    check_shared(fix)
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skills:
        fail("no skills found")
    for skill in skills:
        check_skill(skill)
    check_locales()
    check_scripts()
    print(f"\n{len(skills)} skills, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
