# Day 6: the reel's promise, 100 tickets counted by a function
# Run: python hundred_tickets.py
# All tickets here are made up by the code (sample data only).

import time

categories = ["Login", "Printer", "VPN", "Email"]


def make_sample_tickets(how_many):
    """Make a list of fake tickets using a loop."""
    tickets = []
    for i in range(how_many):                       # i goes 0, 1, 2, ... how_many - 1
        ticket = {
            "id": 1000 + i,
            "category": categories[i % len(categories)],  # cycle through the categories
            "title": "Sample ticket " + str(i + 1),
        }
        tickets.append(ticket)
    return tickets


def ginti(tickets):
    """Count the tickets one by one and return the total."""
    count = 0
    for t in tickets:
        count += 1
    return count


tickets = make_sample_tickets(100)

start = time.perf_counter()     # note the time before counting
total = ginti(tickets)
seconds = time.perf_counter() - start

print("Total tickets:", total)
print("Time taken:", round(seconds, 6), "seconds")
print("Haath se gino? Nahi. Loop lagao.")
