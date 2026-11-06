# Day 6 bonus: count tickets by category
# Run: python ginti_by_category.py
# Sample data only. Never use real company tickets.

tickets = [
    {"id": 101, "category": "Login", "title": "Password reset nahi ho raha"},
    {"id": 102, "category": "Printer", "title": "Printer paper kha gaya"},
    {"id": 103, "category": "VPN", "title": "VPN baar baar disconnect"},
    {"id": 104, "category": "Login", "title": "Account locked"},
    {"id": 105, "category": "Email", "title": "Outbox mein mail atak gaya"},
]


def ginti_by_category(tickets):
    """Return a dict like {"Login": 2, "VPN": 1} with one count per category."""
    counts = {}                     # empty dict: no categories counted yet
    for t in tickets:               # same loop as ginti()
        category = t["category"]    # read the category of this ticket
        if category in counts:
            counts[category] += 1   # seen before: add 1
        else:
            counts[category] = 1    # first time: start at 1
    return counts


result = ginti_by_category(tickets)

# Print one line per category
for category in result:
    print(category, ":", result[category])
