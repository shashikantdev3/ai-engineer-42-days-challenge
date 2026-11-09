"""Day 16: RAG steps, offline (standard library only).

What it does:
1. Loads the sample handbook. Each paragraph is one "page".
2. search(): finds the pages that share the most words with the question.
   (A simple stand-in for your Day 15 embeddings search.)
3. Builds the RAG prompt with the "pata nahi" rule.
4. Gives a TOY answer: the best page, or "pata nahi" if nothing matches.
   This is not an AI. It only lets you test search and the rule.

Run: python rag_offline.py
Or:  python rag_offline.py "How many paid leave days do I get?"
"""

import re
import sys
from pathlib import Path

POLICY_FILE = Path(__file__).with_name("sample_policy.txt")
TOP_K = 3       # how many pages to send (the reel says: sahi 3 tukde)
MIN_SCORE = 2   # a page needs at least this many shared words to count

# Small common words that do not help the search.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "do", "does", "i", "my", "me", "we",
    "you", "your", "to", "of", "in", "on", "at", "for", "and", "or",
    "how", "many", "much", "what", "when", "where", "can", "get", "it",
    "if", "be", "with", "this", "that", "from", "per", "kya", "hai",
}

# Demo questions: 3 that the policy answers, 1 that it does not.
DEMO_QUESTIONS = [
    "How many paid leave days do I get in a year?",
    "What is the notice period after probation?",
    "What do I do if I lose my ID card?",
    "Does the canteen serve free biryani on Fridays?",
]


def load_pages():
    """Read the handbook and split it into pages (paragraphs)."""
    text = POLICY_FILE.read_text(encoding="utf-8")
    pages = [p.strip() for p in text.split("\n\n") if p.strip()]
    return pages[1:]  # skip the title line


def words(text):
    """Lowercase words of a text, without the stop words."""
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


def search(question, pages, k=TOP_K):
    """Return up to k pages that share the most words with the question."""
    q_words = words(question)
    scored = []
    for page in pages:
        score = len(q_words & words(page))
        if score >= MIN_SCORE:
            scored.append((score, page))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [page for score, page in scored[:k]]


def build_prompt(question, context):
    """The RAG prompt: only this context, and 'pata nahi' if it is missing."""
    return (
        "Sirf is context se jawab do. Agar jawab context mein nahi hai, "
        "toh sirf 'pata nahi' bolo.\n"
        f"{context}\nSawaal: {question}"
    )


def toy_answer(hits):
    """NOT an AI. Shows the best page, or 'pata nahi' if nothing matched."""
    if not hits:
        return "pata nahi"
    return f"(toy) Best page: {hits[0]}"


def run(question, pages):
    print("=" * 60)
    print("Sawaal:", question)

    hits = search(question, pages)
    print(f"\nsearch() found {len(hits)} page(s):")
    for number, page in enumerate(hits, start=1):
        print(f"  {number}. {page[:70]}...")

    context = "\n\n".join(hits) if hits else "(koi page nahi mila)"
    prompt = build_prompt(question, context)
    print("\nPrompt that would go to the AI:")
    print("-" * 60)
    print(prompt)
    print("-" * 60)

    print("\nJawab:", toy_answer(hits))
    print()


def main():
    pages = load_pages()
    questions = sys.argv[1:] if len(sys.argv) > 1 else DEMO_QUESTIONS
    for question in questions:
        run(question, pages)


if __name__ == "__main__":
    main()
