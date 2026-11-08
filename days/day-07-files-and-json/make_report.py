# Day 7: count tickets by category and save a report with json.dump
# Run this from inside the day-07 folder: python make_report.py
# Sample data only. Never put real company tickets here.

import json


def ginti(tickets):
    """Count tickets per category (the Day 6 idea: a loop inside a function)."""
    counts = {}
    for t in tickets:
        category = t["category"]
        # get() gives 0 the first time we see a category
        counts[category] = counts.get(category, 0) + 1
    return counts


# 1. Read the diary
with open("tickets.json") as f:
    tickets = json.load(f)

# 2. Do the hisaab
by_category = ginti(tickets)

open_count = 0
for t in tickets:
    if t["status"] == "open":
        open_count += 1

report = {
    "total_tickets": len(tickets),
    "open_tickets": open_count,
    "by_category": by_category,
}

# 3. Write the report
# "w" = write a new file. Careful: it replaces an old report.json.
# indent=2 = neat and readable
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

print("report.json ready!")
print(json.dumps(report, indent=2))
