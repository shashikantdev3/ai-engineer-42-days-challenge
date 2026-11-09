"""Day 18: a tiny vector search with only the Python standard library.

This is a TOY to feel the idea:
  1. Turn every chunk into a vector ONCE (the index card).
  2. Save the index to a file (the diary).
  3. For a question, make its vector and return the top-k closest chunks.

Our "embedding" just counts words. Real embedding models understand meaning
(so "chhutti" and "leave" can match). The steps are the same.

Run:   python mini_vector_search.py      (top 3)
       python mini_vector_search.py 5    (top 5)
"""

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
POLICY_FILE = HERE / "sample_policy.txt"
INDEX_FILE = HERE / "toy_index.json"

# Small common words that carry no meaning for search.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "be", "to", "of", "in", "on", "for", "and",
    "or", "do", "does", "i", "my", "me", "can", "how", "what", "it", "at",
    "with", "by", "from", "get", "in", "this", "that", "every", "year",
}


def words(text):
    """Lowercase words, without stop words."""
    found = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in found if w not in STOP_WORDS]


def embed(text):
    """Toy embedding: a dictionary of word -> count."""
    return dict(Counter(words(text)))


def cosine(a, b):
    """How close two vectors are: 1.0 = same direction, 0.0 = nothing shared."""
    dot = sum(count * b.get(word, 0) for word, count in a.items())
    size_a = math.sqrt(sum(c * c for c in a.values()))
    size_b = math.sqrt(sum(c * c for c in b.values()))
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (size_a * size_b)


def load_chunks():
    """One chunk per paragraph (blank line = new chunk), like Day 17."""
    text = POLICY_FILE.read_text(encoding="utf-8")
    return [c.strip() for c in text.split("\n\n") if c.strip()]


def build_index(chunks):
    """Every chunk gets a unique string id and its vector."""
    return [
        {"id": str(i), "text": chunk, "vector": embed(chunk)}
        for i, chunk in enumerate(chunks)
    ]


def get_index():
    """Load the saved index if it exists. Otherwise build it once and save it."""
    if INDEX_FILE.exists():
        print(f"Index found in {INDEX_FILE.name} (the diary). Loading it, no rebuild.")
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    print(f"No index yet. Building it once and saving to {INDEX_FILE.name}.")
    index = build_index(load_chunks())
    INDEX_FILE.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index


def query(index, question, k=3):
    """Return the top-k chunks closest to the question."""
    q_vector = embed(question)
    scored = [(cosine(q_vector, item["vector"]), item) for item in index]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:k]


def main():
    k = 3
    if len(sys.argv) > 1:
        try:
            k = max(1, int(sys.argv[1]))
        except ValueError:
            print("k must be a number, for example: python mini_vector_search.py 5")
            return

    index = get_index()
    print(f"Chunks in the index: {len(index)}  |  k = {k}")

    questions = [
        "How many casual leave days do I get?",
        "Can I work from home on Friday?",
        "How do I claim my internet bill?",
    ]

    for question in questions:
        print(f"\nQ: {question}")
        for rank, (score, item) in enumerate(query(index, question, k), start=1):
            print(f"  #{rank}  score {score:.2f}  id {item['id']}  {item['text'][:70]}...")

    print("\nTip: delete toy_index.json to rebuild the index from scratch.")


if __name__ == "__main__":
    main()
