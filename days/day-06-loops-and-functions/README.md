# Day 6 · Kaam ek baar likho: loops aur functions

**Week 1 · Python basics** · [← Day 5](../day-05-lists-and-dicts) · [Day 7 →](../day-07-files-and-json) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Friday shaam hai. 100 tickets haath se gino, tabhi ghar jaana!"*

## The idea: mummy ki rotiyan

Mummy makes 10 rotiyan. For every roti she does the same work: **belo, seko, palto**. She does not write new instructions for roti number 7. That is a loop.

| Python word | In the kitchen | What it does |
|---|---|---|
| **loop** (`for roti in rotiyan:`) | "Har roti ke liye..." | Does the same work for every item |
| **indented block** (4 spaces) | belo, seko, palto | The work that repeats for each item |
| **`range(1, 101)`** | Counting 1 to 100 | Gives numbers from 1 up to 100 (the stop, 101, is not included) |
| **function** (`def`) | Giving the work a name | Packs the work into one named machine |
| **return** | The plate comes back | Sends the answer out of the function |

**Ek baar likho, hazaar baar chalao.** Write it once, run it a thousand times. Try [roti_loop.py](roti_loop.py).

### The trap: `range(1, 100)` stops at 99

`range` never includes its last number. `range(1, 100)` gives 1 to 99. For 1 to 100, write `range(1, 101)`. Run [range_trap.py](range_trap.py) and see it yourself.

```python
for i in range(1, 101):
    print("Ticket", i)     # Ticket 1 ... Ticket 100
```

## The code, line by line (same as the reel)

**1. The loop.** For every ticket `t` in `tickets`, do the indented work:

```python
tickets = [101, 102, 103]

for t in tickets:
    print(t)
```

- `for t in tickets:` means "for each ticket, call it `t`". Note the `:` at the end.
- `print(t)` is 4 spaces inside. Everything indented under `for` is the repeat wala kaam.

**2. The function.** Give the counting work a name, `ginti`:

```python
def ginti(tickets):
    count = 0
    for t in tickets:
        count += 1
    return count
```

| Line | In plain English |
|---|---|
| `def ginti(tickets):` | Make a machine called `ginti`. It takes a list called `tickets`. |
| `count = 0` | Start the counter at 0. |
| `for t in tickets:` | Go through the tickets one by one. |
| `count += 1` | Add 1 each time. Same as `count = count + 1`. |
| `return count` | Hand the final number back. |

**3. The call.** Just say the name:

```python
print(ginti(tickets))
```

## Aaj ka kaam (about 30 minutes)

0. **Count 1 to 10 with range.** In a new file write `for i in range(1, 11):` and, 4 spaces inside, `print(i)`. Run it: you should see 1 to 10. Then try `range(1, 10)` and notice it stops at 9 (the trap from the reel). [range_trap.py](range_trap.py) shows both.
1. **Run the loop.** Copy [loop_basics.py](loop_basics.py) and run it:
   ```
   python loop_basics.py
   ```
   You should see `101`, `102`, `103` on separate lines.
2. **Write ginti yourself.** Open [ginti.py](ginti.py). It has 5 sample tickets (a list of dicts, like Day 5). Read the function, then try typing it again from memory in a new file. Run it:
   ```
   python ginti.py
   ```
   You should see `Total tickets: 5`.
3. **Change the data.** Add a 6th sample ticket to the list and run again. The function did not change, the answer did. That is the power of a function.
4. **Bonus: count by category.** Run [ginti_by_category.py](ginti_by_category.py). Same loop, but now a dict keeps one counter per category (Login, Printer, VPN...).
5. **The reel's promise: 100 tickets.** Run [hundred_tickets.py](hundred_tickets.py). A loop makes 100 sample tickets, `ginti` counts them and the script prints how long it took. The "2 second" in the reel was a story example; check your own number on your laptop.
6. **Put it on GitHub.** Upload `ginti.py` (and the bonus files if you did them) to your repo, the same way as Day 3. Commit message: `Day 6: ginti function`.

Mac / Linux: use `python3` instead of `python`.

## Common galtiyan

| Problem | Why | Fix |
|---|---|---|
| `IndentationError` | The line under `for` or `def` is not indented | Use 4 spaces inside |
| `SyntaxError` on the `for` line | Missing `:` at the end | `for t in tickets:` |
| Function prints nothing | You never called it | Add `print(ginti(tickets))` |
| Answer is always 1 | `return count` is inside the loop | Move `return` back to 4 spaces, under `for`, not under `count += 1` |
| Answer is `None` | You forgot `return count` | Add it as the last line of the function |

Side note: Python already has `len(tickets)`, which gives the same number. We wrote `ginti` ourselves to learn how loops and functions work. Tomorrow's real projects need both.

## One rule: sample data only

Use the sample tickets in these files or make up your own. Never paste real tickets or customer data from your office.

## Files in this folder

| File | What it is |
|---|---|
| [loop_basics.py](loop_basics.py) | The first loop from the reel: prints every ticket |
| [ginti.py](ginti.py) | Today's homework: `ginti(tickets)` on 5 sample tickets |
| [ginti_by_category.py](ginti_by_category.py) | Bonus: count tickets per category with a loop and a dict |
| [hundred_tickets.py](hundred_tickets.py) | Makes 100 sample tickets, counts them, prints the time taken |

**ginti chal gaya?** Comment **LOOP** on the Day 6 reel. Tomorrow, Day 7: files and JSON, reading data from a file instead of typing it.
