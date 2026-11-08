"""Day 9: your first LLM API call.

Needs the library from the reel:  pip install -U google-genai
Needs your key in the environment variable GEMINI_API_KEY (never in this file).
Run:  python first_llm_call.py

Model names change often. If the model below gives an error,
open the Gemini API docs and use a current model name.
Free tier data is used to improve Google's products: send sample data only.
"""

import os
import sys

try:
    from google import genai
except ImportError:
    print("google-genai is not installed. Run: pip install -U google-genai")
    sys.exit(1)

if not os.environ.get("GEMINI_API_KEY"):
    print("GEMINI_API_KEY is not set. Run python check_key.py for help.")
    sys.exit(1)

# The chef. genai.Client() reads the key from GEMINI_API_KEY by itself.
client = genai.Client()

# The order (prompt). Sample kirana item, no real company data.
order = "Basmati chawal 5 kg: write a 1 line product description in simple Hinglish."

# Give the order: which model, and what to cook.
r = client.interactions.create(
    model="gemini-3.8-flash",
    input=order,
)

# The answer.
print("Order :", order)
print("Answer:", r.output_text)
