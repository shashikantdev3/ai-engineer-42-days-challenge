# Day 6: the railway counter
# A loop does the same work for every item in a list,
# like a clerk who serves every person in the line the same way.
# Sample data only (made-up tickets).

tickets = [
    {"id": 101, "category": "Password"},
    {"id": 102, "category": "VPN"},
    {"id": 103, "category": "Laptop"},
    {"id": 104, "category": "VPN"},
    {"id": 105, "category": "Email"},
]

print("Counter khul gaya! Line mein", len(tickets), "tickets hain.\n")

# 'for t in tickets' takes each ticket, one by one, and puts it in t.
# The indented lines run once for every ticket.
for t in tickets:
    print("Next please! Ticket", t["id"], "->", t["category"])

print("\nLine khatam. Same kaam, har ticket ke saath, ek hi loop se.")
