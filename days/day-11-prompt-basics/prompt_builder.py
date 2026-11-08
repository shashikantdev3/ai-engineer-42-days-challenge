"""Day 11: one bad prompt, rewritten 3 ways.

Run:  python prompt_builder.py
Copy each version into an AI chat (a new chat for each one) and compare the answers.
Sample data only. Change TICKET to your own made-up ticket.
"""

# The bad prompt Chaddha sir wrote
BAD_PROMPT = "Report bana do"

# Sample ticket (made up, not real company data)
TICKET = (
    "2nd floor ka printer subah se jam hai. 5 log print nahi kar pa rahe. "
    "3 baje ki review se pehle theek chahiye."
)

# The 4 parts of a good prompt (darzi = role, silai = task, naap = context, sleeve = format)
ROLE = "Tum Lala Infotech mein support analyst ho."
TASK = "Neeche diye ticket ka summary likho."
CONTEXT = "Ticket: " + TICKET
FORMAT = (
    "Format: sirf 1 line, Hinglish mein, is pattern mein: "
    "problem, jagah | priority (Low, Medium ya High)."
)

# One example answer for a DIFFERENT ticket, so the AI copies the shape, not the words
EXAMPLE = (
    "Example:\n"
    "Ticket: Meeting room B ka WiFi subah se band hai. Kal tak chalega.\n"
    "Jawab: WiFi band, meeting room B | Medium"
)


def build_versions():
    """Return the 3 better prompts as a list of (name, prompt) pairs."""
    v1 = "\n".join([TASK, CONTEXT])
    v2 = "\n".join([ROLE, TASK, CONTEXT, FORMAT])
    v3 = "\n".join([ROLE, TASK, CONTEXT, FORMAT, EXAMPLE])
    return [
        ("v1 · Task + Context", v1),
        ("v2 · 4 hisse (Role, Task, Context, Format)", v2),
        ("v3 · 4 hisse + ek example", v3),
    ]


def show(name, prompt):
    """Print one prompt with a header and its word count."""
    print("=" * 50)
    print(name)
    print("-" * 50)
    print(prompt)
    print(f"({len(prompt.split())} words)")
    print()


def main():
    show("BAD · Chaddha sir ka prompt", BAD_PROMPT)
    for name, prompt in build_versions():
        show(name, prompt)
    print("Tip: more words = more tokens (Day 10). Clear beats long.")
    print("Now paste each version into a NEW chat and fill in my_results.md.")


if __name__ == "__main__":
    main()
