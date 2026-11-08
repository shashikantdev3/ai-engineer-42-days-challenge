"""Day 12 homework: let the AI fill the form for 5 sample tickets.

Run:  python form_bharo.py

Two modes:
- demo mode (default): uses ready-made sample replies, no internet needed.
- REAL AI mode: if google-genai is installed and both GEMINI_API_KEY and
  MODEL are set in your terminal. MODEL = a model name from the Gemini API docs.

At the end everything is saved in report.json (json.dump, like Day 7).
"""

import json
import os

from form import CATEGORIES, FORM, PRIORITIES, SAMPLE_TICKETS

PROMPT_TEMPLATE = """You are an IT support helper at Lala Infotech.
Read this ticket and fill the form: category, priority, summary.
Ticket: {ticket}"""

# Demo replies: what a form-filled answer looks like. Sample data, not real AI output.
DEMO_REPLIES = [
    '{"category": "Hardware", "priority": "High", "summary": "Printer jam, team cannot print invoices"}',
    '{"category": "Access", "priority": "Medium", "summary": "User forgot password, needs reset"}',
    '{"category": "Network", "priority": "Medium", "summary": "Meeting room Wi-Fi drops every 10 minutes"}',
    '{"category": "Software", "priority": "Medium", "summary": "Excel crashes on big sales file"}',
    '{"category": "Access", "priority": "Low", "summary": "New joiner needs shared drive access by Friday"}',
]


def make_client():
    """Return a real client, or None for demo mode."""
    if not os.environ.get("GEMINI_API_KEY") or not os.environ.get("MODEL"):
        return None
    try:
        from google import genai
    except ImportError:
        print("google-genai is not installed, so using demo mode.")
        return None
    return genai.Client()  # reads GEMINI_API_KEY from the terminal


def ask_ai(client, ticket, index):
    """Send one ticket with the FORM. Return the JSON text."""
    if client is None:
        return DEMO_REPLIES[index]
    prompt = PROMPT_TEMPLATE.format(ticket=ticket)
    r = client.interactions.create(
        model=os.environ["MODEL"],
        input=prompt,
        response_format=FORM,
    )
    return r.output_text


def check_values(data):
    """The JSON shape can be right and a value can still be wrong. Check it."""
    problems = []
    for key in ["category", "priority", "summary"]:
        if key not in data:
            problems.append(f"khaana missing: {key}")
    if data.get("priority") not in PRIORITIES:
        problems.append(f'priority "{data.get("priority")}" is not allowed')
    if data.get("category") not in CATEGORIES:
        problems.append(f'category "{data.get("category")}" is not allowed')
    if not str(data.get("summary", "")).strip():
        problems.append("summary is empty")
    return problems


def main():
    client = make_client()
    if client is None:
        print("Mode: demo mode (sample replies)\n")
    else:
        print(f"Mode: REAL AI mode (model from MODEL = {os.environ['MODEL']})\n")

    sheet = []
    for i, ticket in enumerate(SAMPLE_TICKETS):
        text = ask_ai(client, ticket, i)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"Ticket {i + 1}: json.loads failed. Reply was: {text!r}\n")
            sheet.append({"ticket": ticket, "ok": False, "problems": ["not valid JSON"]})
            continue

        problems = check_values(data)
        print(f"Ticket {i + 1}: {ticket}")
        print(f"  category: {data.get('category')}")
        print(f"  priority: {data.get('priority')}")
        print(f"  summary : {data.get('summary')}")
        for p in problems:
            print(f"  PROBLEM: {p}")
        print()

        row = {"ticket": ticket, **data, "ok": not problems}
        if problems:
            row["problems"] = problems
        sheet.append(row)

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(sheet, f, indent=2, ensure_ascii=False)

    good = sum(1 for row in sheet if row["ok"])
    print(f"Sheet ready: {good} of {len(sheet)} tickets filled correctly. Saved in report.json")


if __name__ == "__main__":
    main()
