"""Day 21: answers with a source (file + page).

Standard library only. Run:
    python ask_with_source.py
    python ask_with_source.py "laptop kho jaye to kya karna hai?"

The search is simple word matching (a stand-in for Chroma).
The answer is the best matching sentence (a stand-in for the Day 16 ask()).
The important part is real: the SOURCE comes from metadata, printed by code.
"""

import re
import sys
from pathlib import Path

DOCS = Path(__file__).parent / "sample_docs"
PAGE_MARK = re.compile(r"^--- page (\d+) ---$", re.MULTILINE)

# Small words that do not help the search
STOP = {"a", "an", "the", "is", "are", "to", "of", "in", "and", "or", "for",
        "hai", "hain", "ka", "ki", "ke", "ko", "kya", "se", "me", "mein",
        "to", "jaye", "karna", "milte", "milti", "every", "your", "can"}

# A few Hinglish words mapped to the English words in the docs
SYNONYMS = {"din": "days", "chutti": "leave", "kho": "lost", "ghar": "home"}


def words(text):
    """Lowercase words, Hinglish mapped, small words removed."""
    out = []
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        w = SYNONYMS.get(w, w)
        if w not in STOP:
            out.append(w)
    return out


def load_chunks():
    """Read every .txt file, one chunk per page, with metadata {file, page}."""
    chunks = []
    for path in sorted(DOCS.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        parts = PAGE_MARK.split(text)
        # parts looks like: [before, "1", page1_text, "2", page2_text, ...]
        for i in range(1, len(parts), 2):
            page = int(parts[i])
            body = parts[i + 1].strip()
            if body:
                chunks.append({
                    "id": f"{path.stem}-p{page}",
                    "text": body,
                    "meta": {"file": path.stem, "page": page},  # the rasid
                })
    return chunks


def query(chunks, q, n_results=3):
    """Find the top chunks. Returns the same shape as Chroma's col.query()."""
    q_words = set(words(q))
    scored = []
    for c in chunks:
        chunk_words = words(c["text"])
        score = sum(1 for w in chunk_words if w in q_words)
        if score > 0:
            scored.append((score, c))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = [c for _, c in scored[:n_results]]
    # One inner list per question, like Chroma
    return {
        "ids": [[c["id"] for c in top]],
        "documents": [[c["text"] for c in top]],
        "metadatas": [[c["meta"] for c in top]],
    }


def ask(q, res):
    """Stand-in for the Day 16 ask(): pick the best sentence from the top chunk."""
    docs = res["documents"][0]
    if not docs:
        return "Pata nahi. Docs mein ye nahi mila."
    q_words = set(words(q))
    sentences = re.split(r"(?<=[.!?])\s+", docs[0])
    best = max(sentences, key=lambda s: sum(1 for w in words(s) if w in q_words))
    return best


def main():
    q = " ".join(sys.argv[1:]) or "WFH kitne din milte hain?"
    chunks = load_chunks()

    res = query(chunks, q, n_results=3)
    src = res["metadatas"][0]          # rasid, straight from metadata
    answer = ask(q, res)               # bill, written by the "AI"

    print("Sawaal:", q)
    print("Jawab: ", answer)
    print("Source (from metadata, not from AI):")
    if not src:
        print("  (koi source nahi mila, to bharosa nahi)")
    for i, s in enumerate(src, start=1):
        print(f"  {i}. {s['file']}, page {s['page']}")
    print()
    print("Same as the reel: print(answer, src)")
    print(answer, src)


if __name__ == "__main__":
    main()
