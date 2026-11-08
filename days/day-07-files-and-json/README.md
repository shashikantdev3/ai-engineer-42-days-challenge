# Day 7 · Week 1 recap: files aur JSON

**Week 1 · Python basics** · [← Day 6](../day-06-loops-and-functions) · [Day 8 →](../day-08-what-is-an-api) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"500 tickets ki file hai. Ek-ek copy karo, tabhi Diwali bonus!"*

Copy-paste nahi. Today Python reads the file by itself, and writes the report by itself.

## The idea: mummy ki doodh diary

Mummy writes the doodh ka hisaab in a diary, because the dimaag forgets. Python works the same way.

| In Python | At home | What it means |
|---|---|---|
| **Variable** | Dimaag | Lives only while the program runs. Program band, sab gayab. |
| **File** | Diary | Stays on disk. Close the program, the data is still there tomorrow. |
| **JSON** | The way you write in the diary | Naam and value pairs: `{"id": 101, "status": "open"}` |
| **json.load(f)** | Reading the diary | Opens the file and gives you Python lists and dicts. |
| **json.dump(obj, f)** | Writing in the diary | Saves your Python data into a file as JSON. |

### Read a JSON file (what the reel showed)

```python
import json

with open("tickets.json") as f:
    tickets = json.load(f)

print(len(tickets))

for t in tickets:
    print(t["id"], t["status"])
```

### Write a JSON file

```python
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)
```

- `"w"` means write a new file. **Dhyan do:** if `report.json` already exists, `"w"` wipes it and writes fresh.
- `indent=2` makes the file padhne layak (one key per line, neatly spaced).

## The trap: single quotes

Har beginner yahan phansta hai. Python dicts accept single quotes. **JSON does not.**

| You write | Result |
|---|---|
| `{'id': 101}` | `json.JSONDecodeError` |
| `{"id": 101}` | Works ✓ |

Rule: in a JSON file, keys and text values always use **double quotes**. Run [trap_demo.py](trap_demo.py) to see the error with your own eyes (it catches the error, so nothing crashes).

## Aaj ka kaam (about 40 minutes)

Open a terminal **inside this folder** first (so Python can find `tickets.json`). On Mac / Linux, type `python3` wherever you see `python`.

1. **Look at the diary.** Open [tickets.json](tickets.json) in VS Code. 5 sample tickets, each with `id`, `status`, `category` and `title`. Notice every key and every text value has double quotes.
2. **Read it with Python.** Run:
   ```
   python read_tickets.py
   ```
   You should see `Total tickets: 5` and one line per ticket.
3. **Count and save the report.** Run:
   ```
   python make_report.py
   ```
   It reads the tickets, counts them by category with `ginti()` (the same idea as Day 6: a loop inside a function), and writes `report.json`. Open `report.json`: it is pretty, thanks to `indent=2`.
4. **Make it yours.** Add 2 more tickets to `tickets.json` (copy one block, change the `id` and `category`, keep the comma between blocks). Run `make_report.py` again and see the counts change.
5. **Break it on purpose.** Change one `"` to `'` in `tickets.json` and run `read_tickets.py`. You will get the JSONDecodeError. Fix the quote. Now you know the trap.
6. **Put it on GitHub.** Upload `tickets.json`, `read_tickets.py`, `make_report.py` and your `report.json` to your repo, then **Commit changes**.

**Sirf sample data.** Make up your tickets. Never use real company tickets or customer data, not even "just to test".

## Bonus: CSV files and the top 3 categories

Many offices export tickets as CSV (a spreadsheet saved as text, one row per line). Python reads it with the built-in `csv` module.

```
python top3_csv.py
```

It reads [tickets.csv](tickets.csv) (10 sample tickets) and prints the top 3 categories. Try opening `tickets.csv` in Excel or Google Sheets too: same data, different diary format.

## Files in this folder

| File | What it is |
|---|---|
| [tickets.json](tickets.json) | 5 sample tickets in JSON (double quotes everywhere) |
| [read_tickets.py](read_tickets.py) | `json.load` + a loop that prints each ticket's id and status |
| [make_report.py](make_report.py) | Counts tickets by category with `ginti()` and saves `report.json` with `json.dump` |
| [trap_demo.py](trap_demo.py) | Shows the single quote trap and the double quote fix |
| [tickets.csv](tickets.csv) | 10 sample tickets as CSV (bonus) |
| [top3_csv.py](top3_csv.py) | Reads the CSV and prints the top 3 categories (bonus) |

All files use the standard library only. Python 3.10 or newer.

**Report ban gaya?** Comment **JSON** on the Day 7 reel. Week 1 complete. Tomorrow, Day 8: API matlab waiter.
