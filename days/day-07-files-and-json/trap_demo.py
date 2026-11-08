# Day 7: the single quote trap
# Run: python trap_demo.py
# json.loads() reads JSON from a string (json.load reads from a file).

import json

wrong = "{'id': 101, 'status': 'open'}"   # single quotes: not valid JSON
right = '{"id": 101, "status": "open"}'   # double quotes: valid JSON

print("Trying the wrong one:", wrong)
try:
    json.loads(wrong)
except json.JSONDecodeError as e:
    print("  JSONDecodeError:", e)

print()
print("Trying the right one:", right)
ticket = json.loads(right)
print("  Works! id =", ticket["id"], "and status =", ticket["status"])

print()
print("Rule: in JSON, always use double quotes.")
