"""Day 8+9 bonus: Bhai Dooj gift bot (behen ka gift, budget ke andar).

Same chef as Day 9 (Gemini). The order (prompt) carries the budget and
what she likes, and asks for 3 ideas.

Needs:  pip install -U google-genai   and your key in GEMINI_API_KEY.
Run:    python bhai_dooj_gift.py

The trap: the prices in the answer are the AI's guesses. A plain LLM call
does not see today's prices. Check the price on a real site before you buy.
Model names change often; if this one errors, use a current Gemini model.
"""

import os
import sys

try:
    from google import genai
except ImportError:
    print("google-genai is not installed. Run: pip install -U google-genai")
    sys.exit(1)

if not os.environ.get("GEMINI_API_KEY"):
    print("GEMINI_API_KEY is not set. See Day 9 check_key.py.")
    sys.exit(1)

BUDGET = 1000                      # rupees (example)
LIKES = "books aur plants"         # change this for your sister

# The chef; key comes from GEMINI_API_KEY. Wait at most 40 s for an answer.
client = genai.Client(http_options={"timeout": 40_000})

order = (
    f"Bhai Dooj ke liye behen ka gift. Budget {BUDGET} rupaye, isse upar nahi. "
    f"Use {LIKES} pasand hain. 3 gift idea do, har idea 1 line mein, "
    "andaaze ki price ke saath. Simple Hinglish."
)

# Chef busy (503, high demand)? Try the next chef.
r = None
for model in ("gemini-3.8-flash", "gemini-3.5-flash"):
    try:
        r = client.interactions.create(model=model, input=order)
        break
    except Exception as error:
        print(f"{model} did not answer ({error.__class__.__name__}). Trying the next one.")
if r is None:
    print("No model answered. Try again in a few minutes.")
    sys.exit(1)

print("Order :", order)
print("Answer:")
print(r.output_text)
print()
print("Yaad rakho: ye price AI ka andaaza hai. Kharidne se pehle site pe check karo.")
