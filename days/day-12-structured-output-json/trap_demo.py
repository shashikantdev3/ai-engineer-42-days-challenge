"""Day 12: the trap. Why "JSON do" in the prompt is not enough.

Run:  python trap_demo.py   (no internet needed)

All replies below are sample text written for this demo.
"""

import json

from form_bharo import check_values

# 1. Only the prompt said "reply in JSON". The AI added extra words.
TRAP_REPLY = """Sure! Here is the JSON you asked for:
{"category": "Hardware", "priority": "High", "summary": "Printer jam"}
Hope this helps!"""

# 2. FORM given in response_format. Only JSON comes back.
FORM_REPLY = '{"category": "Hardware", "priority": "High", "summary": "Printer jam"}'

# 3. Valid JSON, but a bad value. Without an enum, this can happen.
URGENT_REPLY = '{"category": "Hardware", "priority": "thoda urgent", "summary": "Printer jam"}'


def try_reply(name, text):
    print(f"--- {name} ---")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"json.loads FAILED: {e}\n")
        return
    problems = check_values(data)
    if problems:
        print("JSON is fine, but the value check caught:")
        for p in problems:
            print(f"  PROBLEM: {p}")
    else:
        print(f"OK. priority = {data['priority']}")
    print()


if __name__ == "__main__":
    try_reply('Sirf prompt mein "JSON do"', TRAP_REPLY)
    try_reply("response_format=FORM", FORM_REPLY)
    try_reply('"thoda urgent" (why we use enum)', URGENT_REPLY)
    print("Rule: form hamesha response_format se do, aur values apne code mein check karo.")
