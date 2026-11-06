# Day 5 homework: 5 sample tickets as a list of dicts
# Run: python tickets.py
# Sample data only. Never put real company tickets here.

# Each ticket is one dict (a labelled drawer).
# All tickets sit in one list (the rack).
tickets = [
    {"id": 101, "type": "printer", "status": "open"},
    {"id": 102, "type": "vpn", "status": "closed"},
    {"id": 103, "type": "email", "status": "open"},
    {"id": 104, "type": "laptop", "status": "pending"},
    {"id": 105, "type": "password", "status": "open"},
]

# The main task: the type of the first ticket.
# tickets[0] opens slot 0 of the rack, ["type"] reads the label.
print(tickets[0]["type"])

# Bonus: a few more reads from the same rack
print("First ticket id:", tickets[0]["id"])
print("Last ticket status:", tickets[-1]["status"])
print("Total tickets:", len(tickets))
