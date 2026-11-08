"""Day 9: check your setup before the first LLM call.

Standard library only. Run:  python check_key.py

It checks 3 things:
1. Is GEMINI_API_KEY set? (it never prints the key)
2. Is the google-genai library installed?
3. Did you type a key inside any .py file in this folder? (the beginner trap)
"""

import importlib.util
import os
from pathlib import Path


def key_is_set():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key.strip():
        print("[OK]   GEMINI_API_KEY is set (not showing it, keys are secret).")
        return True
    print("[MISS] GEMINI_API_KEY is not set.")
    print("       Windows: setx GEMINI_API_KEY \"your_key\"  then open a NEW terminal.")
    print("       Mac/Linux: export GEMINI_API_KEY=\"your_key\"")
    return False


def library_is_installed():
    try:
        found = importlib.util.find_spec("google.genai") is not None
    except ModuleNotFoundError:
        found = False
    if found:
        print("[OK]   google-genai is installed.")
        return True
    print("[MISS] google-genai is not installed.")
    print("       Run: pip install -U google-genai")
    return False


def no_key_in_code():
    # Look for api_key= typed inside the .py files next to this script.
    folder = Path(__file__).resolve().parent
    this_file = Path(__file__).resolve()
    problems = []
    for py_file in folder.glob("*.py"):
        if py_file.resolve() == this_file:
            continue
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        for number, line in enumerate(text.splitlines(), start=1):
            clean = line.replace(" ", "")
            if "api_key=" in clean and not clean.startswith("#"):
                problems.append(f"{py_file.name}, line {number}")
    if problems:
        print("[TRAP] A key may be typed inside your code:")
        for place in problems:
            print("       -", place)
        print("       Remove it. Keep the key only in GEMINI_API_KEY.")
        return False
    print("[OK]   No api_key= found inside your .py files.")
    return True


if __name__ == "__main__":
    print("Day 9 setup check\n")
    results = [key_is_set(), library_is_installed(), no_key_in_code()]
    print()
    if all(results):
        print("Sab ready! Now run: python first_llm_call.py")
    else:
        print("Fix the lines marked above, then run this check again.")
