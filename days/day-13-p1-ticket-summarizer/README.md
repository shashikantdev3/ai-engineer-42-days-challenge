# Day 13 · Project 1: Ticket Summarizer

**Week 2 · First AI project** · [← Day 12](../day-12-structured-output-json) · [Day 14 →](../day-14-p1-readme-and-recap) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Kal client demo hai: 20 tickets ki summary, ek click mein!"*
> Rahul: *"Dev sir, main toh sirf tukde jaanta hoon, poora project kaise banega?"*

## The idea: mummy ki thali

Dal, chawal, sabzi alag bante hain, par parose saath jaate hain. Project 1 is the same thali. You already cooked every dish in the last few days. Today you serve them together.

| Dish in the thali | Skill (the tukda) | In `summarizer.py` |
|---|---|---|
| **Padho** | Read a JSON file | `tickets = json.load(f)` |
| **Loop** | Do the same thing for every item | `for t in tickets:` |
| **AI** | One LLM call with a good prompt and a fixed FORM | `rows.append(ask(t))` |
| **Likho** | Write the results to a file | `json.dump(rows, out)` |

## How the code works, step by step

1. **Padho.** `json.load` reads [tickets.json](tickets.json): 20 sample tickets, made up for practice.
2. **Loop.** `for t in tickets:` picks one ticket at a time.
3. **AI.** `ask(t)` is one function. Inside it: the LLM call (Day 9), the prompt (Day 11) and the FORM (Day 12: `category`, `priority`, `summary` as JSON). It gives back one row.
4. **Ruko thoda.** `time.sleep(...)` waits a little between calls so you do not hit the API too fast.
5. **Likho.** `json.dump(rows, out)` writes everything to `report.json`.

That is Project 1. Ek click, 20 tickets ki summary.

## Aaj ka kaam (about 45 minutes)

1. **Copy this folder** to your own laptop: `summarizer.py`, `tickets.json`, `make_broken.py`.
2. **Run it in practice mode first** (no key needed, no AI call, a simple keyword rule fills the FORM so you can see the full flow):
   ```
   python summarizer.py
   ```
   Mac / Linux: use `python3` instead of `python`.
   You should see `Ticket 101: summary ✓` ... up to `Ticket 120`, then `report.json` appears. Open it.
3. **Now run it with the real AI.** Set the same values you used for your Day 9 call, as environment variables (never inside the code):
   - Windows (PowerShell):
     ```
     $env:LLM_API_KEY="your-key"
     $env:LLM_BASE_URL="the base URL from your Day 9 call"
     $env:LLM_MODEL="the model name from your Day 9 call"
     python summarizer.py
     ```
   - Mac / Linux:
     ```
     export LLM_API_KEY="your-key"
     export LLM_BASE_URL="the base URL from your Day 9 call"
     export LLM_MODEL="the model name from your Day 9 call"
     python3 summarizer.py
     ```
   `ask()` here uses the common "chat completions" style of API through Python's standard library. If your Day 9 code used a different library, you can paste your Day 9 call inside `call_llm()`; keep the rest the same.
4. **Break one ticket on purpose** and watch try/except save the day:
   ```
   python make_broken.py
   python summarizer.py tickets_broken.json
   ```
   You should see 19 tickets ready and 1 saved in `failed.json` for later.
5. **Comment P1** on the Day 13 reel when your `report.json` is ready.

## The trap: ek error, sab band

Without try/except, one bad ticket (empty text, a network hiccup, a reply that is not JSON) stops the whole program. Ticket 7 fails, and tickets 8 to 20 never run.

The fix:
- **try** = koshish karo (run `ask(t)` for this ticket).
- **except** = gadbad sambhalo (note the error, save the ticket in `failed.json`, move on to the next one).

Result: 19 ready, 1 baad mein. The client sees a report, not a crash.

## Bill kitna aaya?

Same idea as Day 10: every reply has `usage`, so add up the tokens for each ticket. `summarizer.py` prints the total tokens at the end.

If you want a money estimate, set the price you checked on Day 10 for your own model:
```
$env:PRICE_PER_1K_TOKENS="0.0"      # Windows, put your own checked number
export PRICE_PER_1K_TOKENS="0.0"    # Mac / Linux
```
In the reel's example (Day 10 rate, example only): 20 tickets x $0.0003 = $0.006, so less than one cent. Your number depends on your model and your prompt. Prices change, so always check your provider's pricing page.

## Rules (same as always)

- **Key sirf env mein.** Never paste your API key into a file, and never push it to GitHub.
- **Sample data only.** Use `tickets.json` or tickets you make up. Never company tickets, client names or real customer data.
- **Own laptop.** Not the office laptop.

## Files in this folder

| File | What it is |
|---|---|
| [summarizer.py](summarizer.py) | Project 1: reads tickets, calls `ask()` for each, writes `report.json` and `failed.json`, prints tokens |
| [tickets.json](tickets.json) | 20 sample IT support tickets (fictional, for practice) |
| [make_broken.py](make_broken.py) | Makes `tickets_broken.json` with one bad ticket, to test try/except |

**report.json ready?** Comment **P1** on the Day 13 reel. Tomorrow, Day 14: Project 1 GitHub pe, with a README and screenshots, plus the Week 2 recap.
