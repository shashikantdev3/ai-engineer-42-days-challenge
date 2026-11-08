# Day 7: read a JSON file with Python
# Run this from inside the day-07 folder: python read_tickets.py
# Sample data only. Never put real company tickets here.

import json

try:
    # open() finds the file, json.load() turns the JSON text into Python data
    with open("tickets.json") as f:
        tickets = json.load(f)
except FileNotFoundError:
    print("tickets.json not found. Open the terminal inside this folder and try again.")
    raise SystemExit(1)
except json.JSONDecodeError as e:
    print("tickets.json has a JSON mistake. Check your quotes and commas.")
    print("Python says:", e)
    raise SystemExit(1)

# tickets is now a normal Python list of dicts
print("Total tickets:", len(tickets))

# Same for loop as Day 6: one ticket at a time
for t in tickets:
    print(t["id"], t["status"])
