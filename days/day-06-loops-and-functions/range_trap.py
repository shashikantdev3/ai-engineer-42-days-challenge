# Day 6: counting with range, and the trap every beginner falls into.

# range(start, stop) goes from start up to stop - 1. The stop number is NOT included.
for i in range(1, 101):          # 1, 2, 3 ... 100
    print("Ticket", i)

print("---- the trap ----")
last = None
for i in range(1, 100):          # stops at 99, not 100!
    last = i
print("range(1, 100) ka aakhri number:", last)   # 99

# Want 1 to 100? Write 101 as the stop.
print("range(1, 101) mein kitne number:", len(range(1, 101)))   # 100
