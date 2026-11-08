"""Day 14: write the README for Project 1 (Ticket Summarizer).

Run it inside your P1 folder:
    python write_readme.py

It asks a few questions and writes README.md.
If README.md already exists, it writes README_new.md instead (nothing is overwritten).
"""

from pathlib import Path

TEMPLATE = """# {title}

{one_line}

![output]({screenshot})

## Run

```
pip install google-genai
cp .env.example .env
python {script}
```

After the second command, open `.env` and paste your own API key. Windows Command Prompt: use `copy .env.example .env`.

## Kya seekha

{learned}

## Data

Sample tickets only. No company data.

---
Built by {name} as Project 1 of the 42-day AI Engineer challenge.
"""


def ask(question, default):
    """Ask a question. Pressing Enter keeps the default answer."""
    answer = input(f"{question} [{default}]: ").strip()
    return answer or default


def main():
    print("README banate hain. Press Enter to keep the answer in [brackets].\n")

    title = ask("Project name", "Ticket Summarizer")
    one_line = ask(
        "One line: what does it do?",
        "Reads 20 sample support tickets from tickets.json and writes a short summary for each into report.json.",
    )
    screenshot = ask("Screenshot file name", "output.png")
    script = ask("Your main Python file", "summarizer.py")
    name = ask("Your name (shown at the bottom)", "Your Name")

    print("\nKya seekha? Write up to 3 short lines. Press Enter on an empty line to finish.")
    learned_lines = []
    while len(learned_lines) < 3:
        line = input(f"  {len(learned_lines) + 1}. ").strip()
        if not line:
            break
        learned_lines.append(f"- {line}")
    if not learned_lines:
        learned_lines = [
            "- How to call an LLM from Python and keep the key in .env, not in the code.",
            "- How to ask for the answer in a fixed format and save it as JSON.",
        ]

    text = TEMPLATE.format(
        title=title,
        one_line=one_line,
        screenshot=screenshot,
        script=script,
        name=name,
        learned="\n".join(learned_lines),
    )

    target = Path("README.md")
    if target.exists():
        target = Path("README_new.md")
        print("\nREADME.md already exists, so I am writing README_new.md.")

    target.write_text(text, encoding="utf-8")
    print(f"\nDone: {target} is ready.")

    if not Path(screenshot).exists():
        print(f"Reminder: {screenshot} is not in this folder yet. Take the screenshot and save it here.")
    print("Next: python check_before_push.py")


if __name__ == "__main__":
    main()
