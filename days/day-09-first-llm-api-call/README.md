# Day 9 · Pehli LLM API call

**Week 2 · Project 1: Ticket Summarizer** · [← Day 8](../day-08-what-is-an-api) · [Day 10 →](../day-10-tokens-and-cost) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! 100 items ki description, kal subah tak! Warna Sunday office!"*

Haath se 100 descriptions? Nahi. Today Python asks an AI to write them.

## The idea: kal waiter, aaj AI chef

On Day 8 you met the waiter (an API): you give an order, the waiter brings food from the kitchen. Today the kitchen has an **AI chef**.

| In the kitchen | In code | What it means |
|---|---|---|
| **Order** | prompt | The text you send, for example "Basmati 5 kg: 1 line description" |
| **Chef** | Gemini model | The LLM that reads your order and writes the answer |
| **Member card** | API key | Proves the order is yours. Without it, the kitchen does not cook |

The member card (API key) comes from **Google AI Studio**. It has a **free tier, with limits**.

## The code, line by line

```python
from google import genai          # 1. bring the Gemini library

client = genai.Client()           # 2. call the chef; the key comes from GEMINI_API_KEY

r = client.interactions.create(   # 3. give the order
    model="gemini-3.8-flash",     #    which chef
    input="Basmati 5 kg: 1 line", #    the order (your prompt)
)
print(r.output_text)              # 4. print the answer
```

That is the whole first call. 4 lines of real work.

Checked on 8 Nov 2026 against the Gemini API quickstart. **Model names change often.** If `gemini-3.8-flash` gives an error, open the docs and pick a current model name.

## The trap: key GitHub pe daal di

Every beginner does this once:

```python
client = genai.Client(api_key="tumhari_key")   # ✗ never do this
```

You push the file, the key is now public, and anyone can run calls in your name. The rule:

**Key hamesha environment variable `GEMINI_API_KEY` mein.** Never inside a `.py` file.

Key leak ho gayi? Delete that key in AI Studio and make a new one. Then remove it from your code.

## Aaj ka kaam (about 40 minutes)

1. **Make the key.** Open [Google AI Studio](https://aistudio.google.com/), sign in with your own Google account and create an API key on the free tier.
2. **Put the key in env, not in code.**
   - Windows (Command Prompt or PowerShell):
     ```
     setx GEMINI_API_KEY "paste_your_key_here"
     ```
     Then **close the terminal and open a new one** (old terminals do not see it).
   - Mac / Linux:
     ```
     export GEMINI_API_KEY="paste_your_key_here"
     ```
     This works for the current terminal only. To keep it, add the same line to `~/.zshrc` or `~/.bashrc`.
3. **Install the library.**
   ```
   pip install -U google-genai
   ```
   (Mac / Linux: `pip3` if `pip` does not work.)
4. **Check everything.** Run [check_key.py](check_key.py). It tells you if the key is set and the library is installed. It never prints your key.
   ```
   python check_key.py
   ```
5. **Your first LLM call.** Run [first_llm_call.py](first_llm_call.py). It sends one prompt for one item and prints the answer.
   ```
   python first_llm_call.py
   ```
   The answer will be different every time. That is normal for an LLM.
6. **Put it on GitHub.** Upload `first_llm_call.py` to your repo. Check once more: no key inside the file.

**Bonus: 5 items with a loop.** Run [loop_items.py](loop_items.py). It uses the Day 6 loop, a `likho()` function, and `time.sleep()` between calls.
```
python loop_items.py
```
It starts in **practice mode** (a fake chef, no internet, no key needed), so you can see the loop work first. Then open the file, set `PRACTICE = False`, and it calls Gemini for real.

## Why `time.sleep`?

The free tier has limits on how many calls you can make in a short time. A small pause between calls keeps you inside them. `time.sleep(6)` in our code is an **example** pause, not an official number. If you get a "too many requests" error, make the pause longer. Check the current limits in the AI Studio docs.

## One rule: sirf sample data

Free tier content is used to improve Google's products. So send only sample data like our kirana items. **Office ka data, customer ka data, tickets from work: kabhi nahi.** Use your own laptop and your own account.

## Files in this folder

| File | What it is |
|---|---|
| [check_key.py](check_key.py) | Standard library only. Checks `GEMINI_API_KEY`, the `google-genai` install, and warns if a key is typed inside your `.py` files |
| [first_llm_call.py](first_llm_call.py) | The reel's code: one prompt, one answer. Needs `pip install -U google-genai` |
| [loop_items.py](loop_items.py) | Bonus: 5 sample items in a loop with `likho()` and `time.sleep()`. Practice mode runs with the standard library only |

**Pehli call ho gayi?** Comment **AI** on the Day 9 reel. Tomorrow, Day 10: tokens matlab paisa. AI ka har word paisa hai?

*(Fictional story, real plan.)*
