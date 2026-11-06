# Day 5 · Godown ke racks: lists aur dicts

**Week 1 · Python basics** · [← Day 4](../day-04-python-variables) · [Day 6 →](../day-06-loops-and-functions) · [Roadmap](../day-01-roadmap)

> Rahul: *"0 se?! Ye toh save karna padega!"*

Chaddha sir's way: 100 tickets, 100 variables, copy-paste. Our way: 100 tickets, 1 list.

## The idea: the godown

| Python | In the godown | What it does | Example |
|---|---|---|---|
| **list** | Rack with numbered khaane | Keeps many things in order. Counting starts at **0**. | `tickets = [101, 102, 103]` then `tickets[0]` gives `101` |
| **dict** | Drawer with a label on each part | Keeps things by name (a **key**). Say the label, get the thing. | `ticket = {"id": 101, "type": "printer"}` then `ticket["type"]` gives `"printer"` |
| **list of dicts** | A rack full of labelled drawers | Each ticket is one dict. All the tickets go in one list. | `tickets[0]["type"]` |

**Why 0?** The index means "how many steps from the start". The first slot is 0 steps away, so it is `tickets[0]`. The second is `tickets[1]`. Ginti 0 se, yaad rakho.

## The real shape: list of dicts

```python
tickets = [
    {"id": 101, "type": "printer", "status": "open"},
    {"id": 102, "type": "vpn", "status": "closed"},
]

print(tickets[0]["type"])   # printer
```

Read `tickets[0]["type"]` from left to right: go to the rack `tickets`, open slot `0`, read the label `"type"`.

## Aaj ka kaam (about 20 minutes)

1. **Run the demo.** Copy [rack_and_drawer.py](rack_and_drawer.py) into your folder and run it:
   ```
   python rack_and_drawer.py
   ```
   (Mac / Linux: `python3 rack_and_drawer.py`.) Read each output line next to the code that printed it.
2. **Make your own tickets.py.** Write 5 sample tickets as a list of dicts. Each dict has 3 keys: `id`, `type`, `status`. Make up the values (for example `printer`, `vpn`, `email`, `laptop`, `password`).
3. **Print the type of the first ticket:**
   ```python
   print(tickets[0]["type"])
   ```
4. **Check your work** against [tickets.py](tickets.py). Yours does not have to match. Different types and ids are fine.
5. **Put it on GitHub.** On your repo page: **Add file → Upload files**, drop `tickets.py`, then **Commit changes**. One more entry in your bahi khata.

**Bonus (2 minutes):** print the status of the last ticket with `tickets[-1]["status"]`, and the number of tickets with `len(tickets)`.

## When it breaks

| Error | What it means | Fix |
|---|---|---|
| `IndexError: list index out of range` | You asked for a slot that does not exist. 5 tickets means slots 0 to 4. | Use a smaller number. `tickets[5]` does not exist. |
| `KeyError: 'Type'` | No drawer has that label. Keys are case-sensitive. | Use the exact key: `"type"`, not `"Type"`. |
| `SyntaxError` | Usually a missing comma, quote or bracket. | Every dict inside the list needs a comma after its `}` (except the last is optional). |
| `NameError: name 'printer' is not defined` | Text without quotes looks like a variable to Python. | Put text in quotes: `"printer"`. |

## One rule: sample data only

Make up your tickets. Never copy real tickets, names, emails or anything from your company into this repo. Public repo, public data only.

## Files in this folder

| File | What it is |
|---|---|
| [rack_and_drawer.py](rack_and_drawer.py) | Demo: a list (rack, index from 0) and a dict (drawer, read by key) |
| [tickets.py](tickets.py) | Today's homework solution: 5 sample tickets as a list of dicts, prints the first ticket's type |

**Done?** Comment **LIST** on the Day 5 reel. Tomorrow, Day 6: loops and functions. Haath se ginna band.
