# Day 6 homework: the ginti function
# Run: python ginti.py
# Sample data only. Never use real company tickets.

# 5 sample tickets: a list of dicts, like Day 5
tickets = [
    {"id": 101, "category": "Login", "title": "Password reset nahi ho raha"},
    {"id": 102, "category": "Printer", "title": "Printer paper kha gaya"},
    {"id": 103, "category": "VPN", "title": "VPN baar baar disconnect"},
    {"id": 104, "category": "Login", "title": "Account locked"},
    {"id": 105, "category": "Email", "title": "Outbox mein mail atak gaya"},
]


def ginti(tickets):
    """Count the tickets one by one and return the total."""
    count = 0               # start the counter at 0
    for t in tickets:       # go through every ticket
        count += 1          # add 1 for each ticket
    return count            # hand the answer back


# Call the function by its name
total = ginti(tickets)
print("Total tickets:", total)

# Check: Python's built-in len() should give the same number
print("len() says:", len(tickets))
