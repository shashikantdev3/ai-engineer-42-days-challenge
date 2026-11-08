"""Day 14: check your P1 folder before git push.

Run it inside your P1 folder:
    python check_before_push.py
Or point it at a folder:
    python check_before_push.py path/to/your/p1

It checks 3 things:
  1. README.md has the 4 board parts (name, 1 line, screenshot, Run) plus "Kya seekha".
  2. .env is listed in .gitignore, and Git is not tracking .env.
  3. No file you will push looks like it contains an API key.

It only reads files. It never sends anything anywhere.
"""

import re
import subprocess
import sys
from pathlib import Path

# Patterns that look like a real key. A match does not always mean a leak,
# but you should open the file and look.
KEY_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"(api[_-]?key|secret|token)\s*=\s*[\"'][^\"'\s]{16,}[\"']", re.IGNORECASE),
]
SCAN_SUFFIXES = {".py", ".md", ".json", ".txt", ".ipynb"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}

problems = 0


def ok(message):
    print(f"  [OK]  {message}")


def fix(message):
    global problems
    problems += 1
    print(f"  [FIX] {message}")


def check_readme(folder):
    print("\n1. README (dukaan ka board)")
    readme = folder / "README.md"
    if not readme.exists():
        fix("README.md not found. Run: python write_readme.py")
        return

    text = readme.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines()]
    lower = text.lower()

    if any(line.startswith("# ") for line in lines):
        ok("Name on top (# Title)")
    else:
        fix("Add the project name as the first line, like: # Ticket Summarizer")

    plain = [l for l in lines if l and not l.startswith(("#", "!", "-", "`", "|", ">"))]
    if plain:
        ok("1 line that says what it does")
    else:
        fix("Add 1 plain line under the title: what does the project do?")

    if "![" in text:
        ok("Screenshot linked")
        for name in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
            if not name.startswith("http") and not (folder / name).exists():
                fix(f"README shows {name}, but that file is not in the folder")
    else:
        fix("Add a screenshot line, like: ![output](output.png)")

    if "## run" in lower and "python" in lower:
        ok("Run section with commands")
    else:
        fix("Add a '## Run' section with the 3 commands")

    if "seekha" in lower or "learned" in lower:
        ok("Kya seekha section")
    else:
        fix("Add a '## Kya seekha' section: 2 or 3 honest lines")


def check_gitignore(folder):
    print("\n2. The trap: .env and .gitignore")
    gitignore = folder / ".gitignore"
    env_file = folder / ".env"

    ignored = False
    if gitignore.exists():
        entries = [l.strip() for l in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()]
        ignored = ".env" in entries or "/.env" in entries
        if ignored:
            ok(".gitignore has .env")
        else:
            fix("Add a line with .env to .gitignore")
    else:
        fix("No .gitignore. Copy sample.gitignore here and rename it to .gitignore")

    if env_file.exists() and not ignored:
        fix(".env is in this folder and NOT ignored. git add . would push your key!")

    if not (folder / ".env.example").exists():
        print("  [TIP] No .env.example. Add one with a placeholder, so others know what to fill in.")

    # Is Git already tracking .env? (only if Git is installed and this is a repo)
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=folder, capture_output=True, text=True, timeout=10
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [TIP] Git not found, skipped the 'tracked files' check.")
        return

    if result.returncode != 0:
        print("  [TIP] Not a Git repo yet, skipped the 'tracked files' check.")
        return

    tracked = [Path(line).name for line in result.stdout.splitlines()]
    if ".env" in tracked:
        fix("Git is already tracking .env. Run: git rm --cached .env  (then commit)")
    else:
        ok("Git is not tracking .env")


def check_keys(folder):
    print("\n3. Anything that looks like a key?")
    this_file = Path(__file__).resolve()
    found = False

    for path in folder.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.resolve() == this_file:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for number, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in KEY_PATTERNS):
                found = True
                fix(f"{path.relative_to(folder)} line {number} looks like a key. Move it to .env")

    if not found:
        ok("No key-like text found in .py, .md, .json, .txt or .ipynb files")


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    folder = folder.resolve()
    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        sys.exit(1)

    print(f"Checking: {folder}")
    check_readme(folder)
    check_gitignore(folder)
    check_keys(folder)

    print("\nReminder: tickets.json must be sample data only. Never company tickets.")
    if problems:
        print(f"\n{problems} thing(s) to fix before you push. Fix them and run this again.")
        sys.exit(1)
    print("\nSab theek. Now: git add, git commit, git push. Link ready!")


if __name__ == "__main__":
    main()
