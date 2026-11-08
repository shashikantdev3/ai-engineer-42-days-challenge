# Day 10: rough token estimate (no internet, no API key needed)
# Rule of thumb from the Gemini docs: 1 token is about 4 characters.
# This is only an estimate. The real count comes from client.models.count_tokens.
# Run: python estimate_tokens.py
# Or with your own text file: python estimate_tokens.py my_ticket.txt

import math
import sys

CHARS_PER_TOKEN = 4  # about 4 characters per token (a rough rule)

# Sample ticket. Fictional data only, never a real company ticket.
SAMPLE_TICKET = (
    "Ticket 101: Printer on floor 3 not working since morning. "
    "User restarted it twice, still shows paper jam. "
    "Urgent, the team needs to print the monthly report today."
)

# The same ticket, asked in two ways.
PROMPT_DETAIL = "Detail mein samjhao is ticket ko: " + SAMPLE_TICKET
PROMPT_ONE_LINE = "Summarize this ticket in 1 line: " + SAMPLE_TICKET


def estimate_tokens(text):
    """Return a rough token count: characters divided by 4, rounded up."""
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def show(label, text):
    print(f"{label}")
    print(f"  characters: {len(text)}")
    print(f"  tokens (rough estimate): {estimate_tokens(text)}")
    print()


def main():
    # If you give a file name, estimate that file instead of the sample.
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, encoding="utf-8") as f:
            text = f.read()
        show(f"Your file: {path}", text)
        return

    print("Sabzi wale ka tarazu: jitna tola, utna paisa.\n")
    show("Sample ticket", SAMPLE_TICKET)
    show("Prompt A: 'Detail mein samjhao'", PROMPT_DETAIL)
    show("Prompt B: '1 line mein'", PROMPT_ONE_LINE)

    print("Notice: the two INPUT prompts are almost the same size.")
    print("The big difference comes in the OUTPUT (the answer).")
    print("Check it with r.usage after a real call, and use bill_calculator.py.")


if __name__ == "__main__":
    main()
