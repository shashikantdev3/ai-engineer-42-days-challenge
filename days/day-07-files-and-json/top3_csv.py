# Day 7 bonus: read a CSV file and print the top 3 categories
# Run this from inside the day-07 folder: python top3_csv.py
# Sample data only. Never put real company tickets here.

import csv
from collections import Counter

# newline="" is what the csv docs recommend when opening CSV files
with open("tickets.csv", newline="") as f:
    reader = csv.DictReader(f)   # each row becomes a dict, using the header line as keys
    tickets = list(reader)

print("Total tickets:", len(tickets))

# Counter does the counting for us (you did it by hand in ginti())
counts = Counter(t["category"] for t in tickets)

print("Top 3 categories:")
for category, count in counts.most_common(3):
    print(" ", category, "=", count)
