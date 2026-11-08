# Day 10 · Tokens = paisa

**Week 2 · Project 1: Ticket Summarizer** · [← Day 9](../day-09-first-llm-api-call) · [Day 11 →](../day-11-prompt-basics) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! AI ka bill 5,000 rupaye! Kal tak hisaab do, warna salary se katega!"*
>
> (Fictional story. The 5,000 rupaye bill is Chaddha sir's joke, not a real price.)

Reel ka waada: **har sawaal ka bill pehle se jaan lo.** This page shows you how.

## The idea: sabzi wale ka tarazu

The sabzi wala weighs everything on his tarazu. Jitna tola, utna paisa. An AI model works the same way, but it weighs **tokens**.

| In the sabzi mandi | In AI | What it means |
|---|---|---|
| **Tarazu** | Tokens | A token is a piece of a word. For Gemini models, 1 token is about 4 characters. |
| **What you hand over** | Input tokens | Your question (the prompt) is weighed. |
| **What you take home** | Output tokens | The AI's answer is weighed too. |
| **Final hisaab** | The bill | You pay for **both**: input + output. |
| **Thaila** | Context window | The bag has a fixed size. Only that many tokens fit in one go. Zyada daalo, toh bahar. |

## Aaj ke rate (checked 8 Nov 2026)

From the [Google AI Studio pricing page](https://aistudio.google.com/docs/pricing), **Gemini 3.8 Flash, paid tier, through 31 Dec 2026**:

| Token type | Price |
|---|---|
| Input | $0.75 per 1 million tokens |
| Output (includes thinking tokens) | $3.75 per 1 million tokens |

The free tier is free of charge, with limits. Rates change, so **always check the pricing page yourself** before you trust any number, including these.

### Example math (example numbers, not a real bill)

| | Tokens (ex.) | Cost (ex.) |
|---|---|---|
| Input: 1 ticket + "1 line mein" prompt | 200 | 200 × $0.75 / 1M = $0.00015 |
| Output: a 1-line summary | 40 | 40 × $3.75 / 1M = $0.00015 |
| **1 ticket** | | **$0.0003** |
| **1,000 tickets** | | **$0.30** (30 cent) |

## The trap: output 5 guna mehenga

Look at the rates again: $3.75 vs $0.75. **Output tokens cost 5 times more than input tokens.**

So "detail mein samjhao" is the expensive part of the bill, not your question.

| You ask for | Output tokens (ex.) | Output cost per ticket (ex.) |
|---|---|---|
| "Detail mein samjhao" | 800 | $0.003 |
| "1 line mein" | 40 | $0.00015 |

Rule: **jitna chahiye, utna maango.** If you only need one line, say "1 line mein".

Also note: on this model, output includes thinking tokens. So the output count can be bigger than the answer you see on screen. That is why you check `r.usage` after the call instead of guessing.

## Context window = thaila

Every model has a bag of fixed size: the context window. Your prompt and the answer both have to fit in it. Put too much in and the extra does not fit.

We are not putting a number here on purpose. Each model has its own limit, so look it up on that model's docs page when you need it. For one ticket, you are nowhere near the limit.

## Aaj ka kaam (about 30 minutes)

1. **Rough estimate, no API needed.** Run [estimate_tokens.py](estimate_tokens.py). It uses the "about 4 characters per token" rule on a sample ticket:
   ```
   python estimate_tokens.py
   ```
   This is only a guess. The real count comes from the model in the next step.

2. **Real count, before sending.** Open your Day 9 file (it already has `client` and `MODEL`). Add these lines **before** your call:
   ```python
   prompt = "Summarize this ticket in 1 line: Printer on floor 3 not working since morning. Restarted twice, still shows paper jam."
   n = client.models.count_tokens(
       model=MODEL, contents=prompt)
   print(n.total_tokens)
   ```
   Pehle tolo, phir bhejo.

3. **Real bill, after the call.** After your Day 9 call, print the usage. `r` is the result of that call:
   ```python
   print(r.usage)
   ```
   You will see the input tokens, the output tokens and the total. If your Day 9 code uses `generate_content` and `r.usage` gives an error, the counts are in `r.usage_metadata` instead. The exact names are on the [Gemini token docs page](https://ai.google.dev/gemini-api/docs/interactions/tokens).

4. **Catch the trap yourself.** Ask the same ticket twice: once with "detail mein samjhao", once with "1 line mein". Print `r.usage` for both and compare the **output** tokens. Write both numbers down.

5. **Make your own bill.** Put your real numbers into [bill_calculator.py](bill_calculator.py):
   ```
   python bill_calculator.py --input 200 --output 40
   ```
   It prints the cost for 1 ticket and for 1,000 tickets, plus the "detail vs 1 line" comparison.

6. **Put it on GitHub.** Upload today's files and your updated Day 9 file. Commit message idea: `Day 10: token count + bill`. Your bahi khata gets one more entry.

## One rule: sirf sample data

Use made-up tickets like the ones in these files. Never paste real company tickets, customer names or office data into an AI API. Your own laptop, your own key, sample data only.

And never type your API key into the code. Keep it the way you set it up on Day 9.

## Files in this folder

| File | What it is |
|---|---|
| [estimate_tokens.py](estimate_tokens.py) | Rough token estimate (about 4 characters per token) for a sample ticket and two prompts. No internet, no key. |
| [bill_calculator.py](bill_calculator.py) | Turns input and output tokens into a bill for 1 ticket and 1,000 tickets. Shows the 5 guna trap. |

**Tokens gine?** Comment **TOKEN** on the Day 10 reel. Tomorrow, Day 11: Chaddha sir jaisa prompt mat likho. Role, task, context, format.
