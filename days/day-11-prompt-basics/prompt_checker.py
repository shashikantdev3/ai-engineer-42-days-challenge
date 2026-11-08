"""Day 11: check a prompt for the 4 parts + an example.

Run:  python prompt_checker.py                 (checks the bad prompt and v3)
      python prompt_checker.py "your prompt"   (checks your own prompt)

This is a simple keyword check, not an AI. It only tells you
which part you may have forgotten. You still read the AI's answer yourself.
"""

import re
import sys

from prompt_builder import BAD_PROMPT, build_versions

# (tag, question to ask yourself, keyword patterns that usually mean the part is there)
CHECKS = [
    ("ROLE", "Who should the AI be? e.g. 'Tum support analyst ho.'",
     [r"\byou are\b", r"\bact as\b", r"\brole\b", r"\btum\b.*\bho\b"]),
    ("TASK", "What should it do? e.g. 'Summary likho.'",
     [r"\bwrite\b", r"\bsummar", r"\blikho\b", r"\bbana", r"\bexplain\b", r"\btask\b"]),
    ("CTX", "What data should it work on? e.g. 'Ticket: printer jam...'",
     [r"\bcontext\b", r"\bticket\b", r"\bissue\b", r"\bproblem\b", r"\bdata\b"]),
    ("FMT", "What shape should the answer have? e.g. '1 line, Hinglish'",
     [r"\bformat\b", r"\blines?\b", r"\bwords\b", r"\bbullets?\b", r"\bjson\b",
      r"\btable\b", r"\bhinglish\b", r"\benglish\b", r"\bhindi\b"]),
    ("EXMPL", "Did you show one finished answer? e.g. 'Example: ...'",
     [r"\bexample\b", r"\bjaise\b", r"\be\.g\.", r"\bsample answer\b"]),
]


def check(prompt):
    """Return a list of (tag, found, hint) for one prompt."""
    text = prompt.lower()
    results = []
    for tag, hint, patterns in CHECKS:
        found = any(re.search(p, text) for p in patterns)
        results.append((tag, found, hint))
    return results


def report(title, prompt):
    """Print the check result for one prompt."""
    results = check(prompt)
    score = sum(1 for _, found, _ in results if found)
    print("=" * 50)
    print(title)
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    for tag, found, hint in results:
        mark = "OK " if found else "MISSING"
        line = f"{mark:8} {tag}"
        if not found:
            line += f"  ->  {hint}"
        print(line)
    print(f"Score: {score}/5")
    if score < 4:
        print("Darzi ko naap nahi diya. Add the missing parts.")
    print()


def main():
    if len(sys.argv) > 1:
        report("YOUR PROMPT", " ".join(sys.argv[1:]))
        return
    report("BAD · Chaddha sir ka prompt", BAD_PROMPT)
    name, v3 = build_versions()[-1]
    report(name, v3)
    print('Check your own: python prompt_checker.py "your prompt here"')


if __name__ == "__main__":
    main()
