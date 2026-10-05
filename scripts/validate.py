#!/usr/bin/env python3
"""Validate the skills in this repository.

1. Every skills/<dir>/SKILL.md has frontmatter with `name` equal to <dir>
   (lowercase, digits, hyphens, at most 64 chars) and a `description` of at most
   1024 chars without angle brackets.
2. Relative links in SKILL.md and `scripts/...` mentions point to files that exist.
3. No personal absolute paths leak into skill files.
4. Files shared between skills are identical (docs-master-plan is the source).
5. The checker scripts give the expected result on tests/fixtures.

Usage: python3 scripts/validate.py [--fix]   (--fix copies shared files from the source skill)
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FIXTURES = ROOT / "tests" / "fixtures"
SHARED = {
    "references/conventions.md": ("docs-master-plan", ["docs-project"]),
    "references/templates.md": ("docs-master-plan", ["docs-project"]),
    "scripts/check_docs.py": ("docs-master-plan", ["docs-project"]),
}
CHECKS = [
    # (script, target, expected exit code, codes that must appear in the output)
    ("docs-system-design/scripts/check_sdd.py", "sdd-good.md", 0, []),
    ("docs-system-design/scripts/check_sdd.py", "sdd-bad.md", 1, ["E1", "E2", "E3", "E4", "E5", "W1"]),
    ("docs-project/scripts/check_docs.py", "docs-good", 0, []),
    ("docs-project/scripts/check_docs.py", "docs-bad", 1, ["E1", "E2", "W1", "W2"]),
]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)\s#]+)")
SCRIPT_RE = re.compile(r"`(?:<skill-dir>/)?(scripts/[\w.-]+)")
PERSONAL_RE = re.compile(r"(/home/\w+|/Users/\w+|~/dev/)")

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
    body_lines = text.count("\n")
    if body_lines > 500:
        fail(f"{skill.name}: SKILL.md has {body_lines} lines (keep under 500)")
    for target in LINK_RE.findall(text) + SCRIPT_RE.findall(text):
        if target.startswith(("http:", "https:")):
            continue
        if not (skill / target).exists():
            fail(f"{skill.name}: SKILL.md refers to missing file {target}")
    for f in skill.rglob("*"):
        if f.is_file() and PERSONAL_RE.search(f.read_text(encoding="utf-8", errors="ignore")):
            fail(f"{skill.name}: personal path in {f.relative_to(skill)}")
    print(f"ok   {skill.name} ({len(desc)} chars description, {body_lines} lines)")


def check_shared(fix: bool) -> None:
    for rel, (source, copies) in SHARED.items():
        src = SKILLS / source / rel
        for copy in copies:
            dst = SKILLS / copy / rel
            if dst.exists() and dst.read_bytes() == src.read_bytes():
                continue
            if fix:
                shutil.copyfile(src, dst)
                print(f"fix  copied {source}/{rel} -> {copy}/{rel}")
            else:
                fail(f"{copy}/{rel} differs from {source}/{rel} (run with --fix)")
    print("ok   shared files" if not fix else "ok   shared files synced")


def check_scripts() -> None:
    for script, target, code, expected in CHECKS:
        proc = subprocess.run(
            [sys.executable, str(SKILLS / script), str(FIXTURES / target)],
            capture_output=True, text=True,
        )
        missing = [c for c in expected if not re.search(rf"^{c} ", proc.stdout, re.M)]
        if proc.returncode != code or missing:
            fail(f"{script} on {target}: exit {proc.returncode} (want {code}), missing {missing}\n{proc.stdout}{proc.stderr}")
        else:
            print(f"ok   {Path(script).name} on {target}")


def main() -> int:
    fix = "--fix" in sys.argv
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skills:
        fail("no skills found")
    for skill in skills:
        check_skill(skill)
    check_shared(fix)
    check_scripts()
    print(f"\n{len(skills)} skills, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
