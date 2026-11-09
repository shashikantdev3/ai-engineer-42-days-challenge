"""Day 15 helpers: embed() and cosine().

cosine() uses only plain Python maths (standard library).
embed() calls the Gemini API. It needs:
    pip install google-genai
and an API key in the GEMINI_API_KEY environment variable.
"""

import math
import os

# One model name, in one place. Complaints AND questions use this.
# Two different models = two different maps = scores mean nothing (the trap).
MODEL = "gemini-embedding-2"


def cosine(a, b):
    """How close are two addresses? Higher number = closer meaning."""
    if len(a) != len(b):
        raise ValueError(
            "The two lists have different lengths. "
            "Did you use two different models? Use the same MODEL for both."
        )
    dot = sum(x * y for x, y in zip(a, b))
    size_a = math.sqrt(sum(x * x for x in a))
    size_b = math.sqrt(sum(y * y for y in b))
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (size_a * size_b)


def embed(model, texts):
    """Turn a list of sentences into a list of addresses (lists of numbers)."""
    try:
        from google import genai
    except ImportError:
        raise SystemExit(
            "google-genai is not installed. Run: pip install google-genai\n"
            "No internet or key yet? Run: python mohalla_toy.py"
        )

    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        raise SystemExit(
            "No API key found. Set GEMINI_API_KEY in your terminal first "
            "(see the README). Never write the key inside the code."
        )

    client = genai.Client()  # reads the key from the environment
    r = client.models.embed_content(model=model, contents=texts)
    return [e.values for e in r.embeddings]


if __name__ == "__main__":
    # Quick self-check of cosine(), no internet needed.
    print("Same direction:", round(cosine([1, 2, 3], [2, 4, 6]), 2))  # 1.0
    print("No overlap:   ", round(cosine([1, 0], [0, 1]), 2))        # 0.0
