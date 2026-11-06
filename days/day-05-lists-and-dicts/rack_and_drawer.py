# Day 5: the godown rack (list) and the labelled drawer (dict)
# Run: python rack_and_drawer.py
# Sample data only. These ticket ids and types are made up.

# ---------- LIST = RACK ----------
# A list is a rack with numbered slots. Counting starts at 0.
tickets = [101, 102, 103]

print("Whole rack:", tickets)
print("Slot 0 (first ticket):", tickets[0])
print("Slot 1 (second ticket):", tickets[1])
print("Slot -1 (last ticket):", tickets[-1])
print("Number of slots:", len(tickets))

# Add one more ticket at the end of the rack
tickets.append(104)
print("After append(104):", tickets)

print()

# ---------- DICT = DRAWER ----------
# A dict is a drawer with labels (keys). Say the label, get the thing.
ticket = {"id": 101, "type": "printer", "status": "open"}

print("Whole drawer:", ticket)
print('Label "type":', ticket["type"])
print('Label "status":', ticket["status"])

# Change what is inside one label
ticket["status"] = "closed"
print("After closing it:", ticket)

# .get() does not crash when a label is missing. It gives a default instead.
print('Label "priority":', ticket.get("priority", "no such label"))
