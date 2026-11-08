# Day 11 · Chaddha sir jaisa prompt mat likho

**Week 2 · P1 Ticket Summarizer** · [← Day 10](../day-10-tokens-and-cost) · [Day 12 →](../day-12-structured-output-json) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Maine AI ko report bola, isne kavita likh di!"*

He typed `Report bana do` and got "Roses are red...". The AI did nothing wrong. It got a vague prompt and made a guess. Galti AI ki nahi, prompt ki thi.

## The idea: prompt = darzi ka order

Tell a darzi only "shirt silo" and you get whatever shirt he likes. Give him the naap and you get the right shirt. A prompt works the same way. It has 4 parts:

| Part | At the darzi | What you tell the AI | Example from the reel |
|---|---|---|---|
| **Role** | Darzi | Who the AI should be | `Tum support analyst ho.` |
| **Task** | Silai | What to do | `Ticket ka summary likho.` |
| **Context** | Naap | What to work on: the actual data | `Printer jam, 2nd floor` |
| **Format** | Sleeve | What the answer should look like | `1 line, Hinglish` |

## The beginner trap: format chhoda, toh AI ki marzi

Without a format, the AI picks one for you. Kabhi para, kabhi list, kabhi 10 lines. So always write:

- **kitni line** (1 line, 3 bullets, under 20 words)
- **kis bhasha** (Hinglish, English, Hindi)

| Prompt says | What you get |
|---|---|
| `Summary likho` | kabhi para, kabhi list |
| `Summary likho. 1 line, Hinglish.` | the same shape every time |

## Still the wrong format? Ek example do

Show the AI one finished answer for a **different** ticket. It follows the pattern. Use a different ticket so the AI copies the shape, not the words.

## The full prompt (all 4 parts + one example)

```
Tum Lala Infotech mein support analyst ho.
Neeche diye ticket ka summary likho.
Ticket: 2nd floor ka printer subah se jam hai. 5 log print nahi kar pa rahe. 3 baje ki review se pehle theek chahiye.
Format: sirf 1 line, Hinglish mein, is pattern mein: problem, jagah | priority (Low, Medium ya High).
Example:
Ticket: Meeting room B ka WiFi subah se band hai. Kal tak chalega.
Jawab: WiFi band, meeting room B | Medium
```

A clear prompt makes the right answer far more likely on the first try. It is not magic: always read the answer before you send it to anyone.

## Aaj ka kaam (about 30 to 40 minutes)

Rewrite one bad prompt (`Report bana do`) 3 ways and compare the answers.

1. **Print the 3 versions.** Run [prompt_builder.py](prompt_builder.py):
   ```
   python prompt_builder.py
   ```
   It prints the bad prompt and 3 better ones:
   - **v1:** Task + Context only
   - **v2:** all 4 parts (Role, Task, Context, Format)
   - **v3:** all 4 parts + one example
2. **Send each one to an AI.** Use any chat AI you already have, or your own LLM call code from Day 9. Start a **new chat for every version**, so the earlier answer does not help the next one.
3. **Write down the answers.** Fill in [my_results.md](my_results.md): what came back, and was it the right shape on the first try?
4. **Check your own prompt.** Run [prompt_checker.py](prompt_checker.py) on any prompt you write. It tells you which of the 5 parts you forgot:
   ```
   python prompt_checker.py "Tum support analyst ho. Ticket ka summary likho."
   ```
   Run it with nothing after the file name to see it check the bad prompt and v3.
5. **Make it yours.** Open `prompt_builder.py`, change `TICKET` to your own made-up ticket, run steps 1 to 3 again.
6. **Put it on GitHub.** Upload `my_results.md` to your repo. That is today's proof.

On Windows, if `python` doesn't work, try `py prompt_builder.py`. On Mac / Linux, use `python3`.

## One rule: sirf sample data

Only made-up tickets, like the ones in this folder. Never paste real company tickets, customer names, emails or phone numbers into an AI tool.

## Files in this folder

| File | What it is |
|---|---|
| [prompt_builder.py](prompt_builder.py) | Prints the bad prompt and 3 better versions to copy into an AI |
| [prompt_checker.py](prompt_checker.py) | Simple keyword check: Role, Task, Context, Format, Example present? |
| [my_results.md](my_results.md) | Fill-in table for your 3 answers (your proof for GitHub) |

**Teeno compare kar liye?** Comment **PROMPT** on the Day 11 reel. Tomorrow, Day 12: AI se form bharwao, JSON mein.
