# Day 12 · Form bharwao: structured output

**Week 2 · Project 1: Ticket Summarizer** · [← Day 11](../day-11-prompt-basics) · [Day 13 →](../day-13-p1-ticket-summarizer) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! 50 tickets ki sheet banao: category, priority, summary!"*
>
> Rahul: *"Dev sir, AI toh har baar alag tarah likhta hai, main sheet kaise bharun?"*

## The idea: give the AI a form, not a blank page

In a bank, if everyone writes on a blank paper, everyone writes differently. A form has one box (khaana) for each thing, so the name always goes in the name box.

| In the bank | In AI | What it does |
|---|---|---|
| **Khaali kaagaz** | A plain prompt reply | Free text. Different every time. Hard to put in a sheet. |
| **Form** | **Structured output** | The AI must answer in JSON, in your shape. |
| **Khaane** | **Keys** | `category`, `priority`, `summary`. Each answer goes in its own box. |
| **Form ka design** | **Schema** | The rules of the form: which keys, which type, which are required. |
| **MCQ options** | **enum** | Only allowed answers, like `High`, `Medium`, `Low`. No "thoda urgent". |

The code from the reel, line by line:

```python
r = client.interactions.create(
    model=MODEL, input=prompt,
    response_format=FORM)

data = json.loads(r.output_text)
print(data["priority"])
```

1. `create` gets the model, your prompt, and the FORM in `response_format`.
2. `r.output_text` is the JSON text the AI wrote.
3. `json.loads` turns that text into a Python dict (same as Day 7).
4. `data["priority"]` reads one khaana.

## The trap: sirf "JSON do" likhna

Writing "reply in JSON" inside the prompt is not enough. Sometimes the AI adds extra words ("Sure! Here is your JSON...") and then `json.loads` fails. Sometimes a box is missing.

**Rule:** form hamesha `response_format` se do.

And one more honest point: the docs say the reply comes as valid JSON, but the **values** should still be checked in your own code. So `form_bharo.py` checks every answer (is the priority one of High, Medium, Low?) before it goes in the sheet.

## Aaj ka kaam (about 45 to 60 minutes)

1. **Copy the FORM.** Open [form.py](form.py). It has the schema (the form design), the FORM for `response_format`, and 5 sample tickets. Read the comments.
2. **See the trap with your own eyes.** Run:
   ```
   python trap_demo.py
   ```
   You will see a "JSON do" reply fail in `json.loads`, a form reply pass, and a "thoda urgent" answer get caught by the value check. No internet needed.
3. **Fill the sheet (demo mode).** Run:
   ```
   python form_bharo.py
   ```
   Without an API key it runs in **demo mode**: it uses ready-made sample replies so you can see the full flow. It prints category, priority and summary for each of the 5 tickets and saves everything in `report.json` with `json.dump`, just like Day 7.
4. **Fill the sheet (real AI).** Use the same API key setup from your earlier LLM days:
   ```
   pip install google-genai
   ```
   Then set two things in your terminal. `GEMINI_API_KEY` is your key from Google AI Studio. `MODEL` is a model name you pick from the Gemini API docs (we don't hardcode one, because names change).
   - Windows (PowerShell): `$env:GEMINI_API_KEY="your-key"` and `$env:MODEL="model-name-from-docs"`
   - Windows (cmd): `set GEMINI_API_KEY=your-key` and `set MODEL=model-name-from-docs`
   - Mac / Linux: `export GEMINI_API_KEY="your-key"` and `export MODEL="model-name-from-docs"`

   Run `python form_bharo.py` again. The first line now says **REAL AI mode**.
5. **Open report.json.** Every ticket has the same 3 khaane. That is your sheet.
6. **Push to GitHub.** Upload `form.py`, `form_bharo.py` and `report.json` to your repo. Never upload your API key.

**Sirf sample data.** Use the sample tickets or tickets you make up. Company data kabhi nahi.

## If something breaks

| What you see | Why | Fix |
|---|---|---|
| `demo mode` even after setup | `MODEL` or `GEMINI_API_KEY` is not set in this terminal | Set both again in the same terminal window, then run |
| `ModuleNotFoundError` is not shown, but still demo mode | `google-genai` not installed for this Python | Run `pip install google-genai` (or `py -m pip install google-genai` on Windows) |
| An error about `response_format` or `interactions` | The API changed after 8 Nov 2026 | Check the structured output page in the Gemini API docs and match the field names |
| `PROBLEM: priority "..." is not allowed` | The value check caught a bad answer | That is the check doing its job. The ticket is marked in the report |

## Files in this folder

| File | What it is |
|---|---|
| [form.py](form.py) | The FORM: schema with keys and enums, plus 5 sample tickets |
| [form_bharo.py](form_bharo.py) | Homework: fills category, priority, summary for 5 tickets, checks values, saves `report.json` |
| [trap_demo.py](trap_demo.py) | Shows why "JSON do" in the prompt fails and the form works. Runs offline |

**Sheet ban gayi?** Comment **FORM** on the Day 12 reel. Tomorrow, Day 13: Project 1, Ticket Summarizer, end to end on 20 sample tickets.
