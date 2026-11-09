"""Day 19: hybrid search = keyword (BM25) + vector, joined with RRF.

Standard library only. Run:  python hybrid_search.py

The "vector" search here is a TOY stand-in (a small word-to-meaning map),
so the file runs anywhere. In your real bot, use the Day 18 Chroma search.
All chunks are fictional sample data for Lala Infotech.
"""

import math
from collections import Counter

# Change this and run again.
QUESTION = "E-404 error aa raha hai"

# 10 sample chunks. Chunk 2 is the E-404 guide.
CHUNKS = [
    "Printer mein error aaye toh printer restart karo.",
    "Wifi slow ho toh router ke paas baitho.",
    "E-404 guide: E-404 error aaye toh browser cache clear karo.",
    "Koi bhi issue ho toh pehle error ka photo lo.",
    "Chhutti policy: saal mein 18 chhutti, manager approval zaroori.",
    "Password reset ke liye IT portal kholo.",
    "Salary slip har mahine 5 tareekh ko milti.",
    "Naya laptop chahiye toh form bharo aur manager ko batao.",
    "Office canteen subah 9 baje khulti.",
    "Meeting room book karne ke liye calendar use karo.",
]


def tokenize(text):
    """lower() + split into words. Also strips punctuation like , . : ?"""
    return [w.strip(".,?!:;\"'()") for w in text.lower().split()]


# ---------- Keyword search: BM25 (the "naam se" search) ----------

class BM25:
    """A small BM25 (Okapi). Same idea as rank_bm25.BM25Okapi."""

    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs = docs                      # list of token lists
        self.k1 = k1
        self.b = b
        self.n_docs = len(docs)
        self.avg_len = sum(len(d) for d in docs) / len(docs)
        # In how many docs does each word appear?
        self.doc_freq = Counter(word for d in docs for word in set(d))

    def idf(self, word):
        # Rare words (like an error code) get a high weight.
        n = self.doc_freq[word]
        return math.log((self.n_docs - n + 0.5) / (n + 0.5) + 1)

    def get_scores(self, query_words):
        scores = []
        for doc in self.docs:
            counts = Counter(doc)
            score = 0.0
            for word in query_words:
                f = counts[word]
                if f == 0:
                    continue
                length_part = 1 - self.b + self.b * len(doc) / self.avg_len
                score += self.idf(word) * f * (self.k1 + 1) / (f + self.k1 * length_part)
            scores.append(score)
        return scores


# ---------- Toy vector search (the "shakal se" search) ----------
# A real embedding model learns meaning by itself. Here we fake it with a
# tiny map: different words with the same meaning point to one idea.
# Notice: "e-404" is not in the map. Codes have no meaning to match.
MEANING = {
    "error": "problem", "issue": "problem", "kharab": "problem",
    "printer": "printing", "print": "printing",
    "wifi": "device", "router": "device", "laptop": "device", "browser": "device",
    "chhutti": "leave", "leave": "leave",
    "password": "login", "login": "login",
    "salary": "money",
}


def to_vector(text):
    """Count the meanings in a text, e.g. {'problem': 1, 'device': 1}."""
    return Counter(MEANING[w] for w in tokenize(text) if w in MEANING)


def cosine(a, b):
    dot = sum(a[k] * b[k] for k in a)
    size_a = math.sqrt(sum(v * v for v in a.values()))
    size_b = math.sqrt(sum(v * v for v in b.values()))
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (size_a * size_b)


# ---------- Helpers ----------

def to_rank(scores):
    """Turn scores into a list of chunk ids, best first (only score > 0)."""
    ids = [i for i in range(len(scores)) if scores[i] > 0]
    return sorted(ids, key=lambda i: scores[i], reverse=True)


def rrf(*ranked_lists, k=60):
    """Reciprocal rank fusion: add 1 / (k + rank) from every list.
    Returns ids, best first. Rank starts at 1."""
    total = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, start=1):
            total[doc_id] = total.get(doc_id, 0.0) + 1 / (k + rank)
    return sorted(total, key=lambda d: total[d], reverse=True)


def show(title, ranked_ids):
    print(title)
    if not ranked_ids:
        print("  (nothing found)")
    for pos, i in enumerate(ranked_ids[:3], start=1):
        print(f"  #{pos} [chunk {i}] {CHUNKS[i]}")
    print()


def main():
    print(f"Sawaal: {QUESTION}\n")

    # Keyword: lower() on chunks AND on the question (the trap rule).
    bm25 = BM25([tokenize(c) for c in CHUNKS])
    kw_rank = to_rank(bm25.get_scores(tokenize(QUESTION)))

    # Vector (toy): compare meanings.
    q_vec = to_vector(QUESTION)
    vec_rank = to_rank([cosine(q_vec, to_vector(c)) for c in CHUNKS])

    # Hybrid: join the two ranked lists.
    hybrid_rank = rrf(kw_rank, vec_rank)

    show("KEYWORD only (naam se):", kw_rank)
    show("VECTOR only (shakal se, toy):", vec_rank)
    show("HYBRID (dono, RRF k=60):", hybrid_rank)


if __name__ == "__main__":
    main()
