"""Day 13 · Make one broken ticket, to test the try/except trap.

It copies tickets.json to tickets_broken.json and empties the text of
ticket 107. Then run:
  python summarizer.py tickets_broken.json
You should see 19 ready and 1 saved in failed.json.
"""

import json

BROKEN_ID = 107

with open("tickets.json", encoding="utf-8") as f:
    tickets = json.load(f)

for t in tickets:
    if t["id"] == BROKEN_ID:
        t["text"] = ""  # empty text: ask() will raise an error here

with open("tickets_broken.json", "w", encoding="utf-8") as out:
    json.dump(tickets, out, indent=2, ensure_ascii=False)

print(f"Made tickets_broken.json (ticket {BROKEN_ID} has no text).")
print("Now run: python summarizer.py tickets_broken.json")
