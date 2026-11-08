"""Day 13 · Project 1: Ticket Summarizer

The thali:
  Padho  -> json.load reads the tickets
  Loop   -> for t in tickets
  AI     -> ask(t) fills the FORM: category, priority, summary
  Likho  -> json.dump writes report.json

Run:
  python summarizer.py                      (uses tickets.json)
  python summarizer.py tickets_broken.json  (test the try/except trap)

No API key set? It runs in PRACTICE MODE: no AI call, a simple keyword
rule fills the FORM so you can see the whole flow. Standard library only.
Sample data only. Never use company tickets.
"""

import json
import os
import sys
import time
import urllib.request

# Print the ✓ safely even on old Windows consoles.
try:
    sys.stdout.reconfigure(errors="replace")
except AttributeError:
    pass

# Settings come from environment variables (same values as your Day 9 call).
API_KEY = os.environ.get("LLM_API_KEY", "")
BASE_URL = os.environ.get("LLM_BASE_URL", "").rstrip("/")
MODEL = os.environ.get("LLM_MODEL", "")
PRICE_PER_1K = os.environ.get("PRICE_PER_1K_TOKENS", "")  # your Day 10 number

REAL_AI = bool(API_KEY and BASE_URL and MODEL)
SLEEP_S = 6 if REAL_AI else 0  # wait between real calls, like the reel

# The FORM from Day 12: these keys must be in every answer.
FORM = ["category", "priority", "summary"]
CATEGORIES = ["Access", "Hardware", "Network", "Email", "Software", "Other"]
PRIORITIES = ["High", "Medium", "Low"]

# The prompt from Day 11: role, task, rules, output format.
PROMPT = (
    "You are an IT support lead at Lala Infotech.\n"
    "Read the ticket and fill this FORM as JSON only, no extra text:\n"
    '{"category": one of ' + json.dumps(CATEGORIES) + ', '
    '"priority": one of ' + json.dumps(PRIORITIES) + ', '
    '"summary": "one short sentence, max 15 words"}\n'
    "Ticket:\n"
)


def call_llm(text):
    """One chat completions style call (the Day 9 idea).
    Returns (reply_text, tokens_used)."""
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT + text}],
        "temperature": 0,
    }
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        r = json.loads(resp.read().decode("utf-8"))
    reply = r["choices"][0]["message"]["content"]
    tokens = r.get("usage", {}).get("total_tokens", 0)  # Day 10: r.usage
    return reply, tokens


def practice_answer(text):
    """No key? A simple keyword rule fills the FORM. Not AI, just practice."""
    low = text.lower()
    if "password" in low or "login" in low or "access" in low:
        category = "Access"
    elif "printer" in low or "laptop" in low or "mouse" in low or "screen" in low:
        category = "Hardware"
    elif "vpn" in low or "wifi" in low or "internet" in low or "network" in low:
        category = "Network"
    elif "mail" in low or "outlook" in low:
        category = "Email"
    elif "install" in low or "excel" in low or "software" in low or "update" in low:
        category = "Software"
    else:
        category = "Other"

    if "urgent" in low or "down" in low or "client" in low or "all" in low:
        priority = "High"
    elif "today" in low or "slow" in low:
        priority = "Medium"
    else:
        priority = "Low"

    first = text.split(".")[0].strip()
    summary = " ".join(first.split()[:15])
    reply = json.dumps({"category": category, "priority": priority, "summary": summary})
    return reply, 0


def clean_json(reply):
    """Some models wrap JSON in ``` fences. Remove them, then parse."""
    reply = reply.strip()
    if reply.startswith("```"):
        reply = reply.strip("`")
        if reply.lower().startswith("json"):
            reply = reply[4:]
    return json.loads(reply)


def ask(t):
    """One ticket in, one filled FORM out (prompt + FORM + call)."""
    text = t.get("text", "").strip()
    if not text:
        raise ValueError("ticket has no text")

    if REAL_AI:
        reply, tokens = call_llm(text)
    else:
        reply, tokens = practice_answer(text)

    form = clean_json(reply)
    for key in FORM:
        if key not in form:
            raise ValueError("answer is missing " + key)

    return {
        "id": t["id"],
        "category": form["category"],
        "priority": form["priority"],
        "summary": form["summary"],
        "tokens": tokens,
    }


def main():
    in_file = sys.argv[1] if len(sys.argv) > 1 else "tickets.json"
    mode = "REAL AI" if REAL_AI else "PRACTICE MODE (no key, no AI call)"
    print("Mode:", mode)
    print("Reading:", in_file)

    # 1. Padho
    with open(in_file, encoding="utf-8") as f:
        tickets = json.load(f)

    rows = []
    failed = []

    # 2. Loop
    for t in tickets:
        tid = t.get("id", "?")
        # 3. AI, inside try/except so one error does not stop everything
        try:
            rows.append(ask(t))
            print(f"Ticket {tid}: summary ✓")
        except Exception as e:
            failed.append({"id": tid, "error": str(e)})
            print(f"Ticket {tid}: error, baad mein dekhenge ({e})")
        time.sleep(SLEEP_S)

    # 4. Likho
    with open("report.json", "w", encoding="utf-8") as out:
        json.dump(rows, out, indent=2, ensure_ascii=False)
    if failed:
        with open("failed.json", "w", encoding="utf-8") as out:
            json.dump(failed, out, indent=2, ensure_ascii=False)

    print()
    print(f"{len(rows)} ready, {len(failed)} baad mein.")
    print("Saved: report.json" + (" and failed.json" if failed else ""))

    # Bill: add up the tokens (Day 10 idea)
    total_tokens = sum(r["tokens"] for r in rows)
    print("Total tokens:", total_tokens)
    if PRICE_PER_1K:
        try:
            cost = total_tokens / 1000 * float(PRICE_PER_1K)
            print(f"Estimated bill: ${cost:.4f} (your rate, estimate only)")
        except ValueError:
            print("PRICE_PER_1K_TOKENS is not a number, skipping the bill.")
    elif not REAL_AI:
        print("Practice mode makes no AI calls, so the bill is 0.")


if __name__ == "__main__":
    main()
