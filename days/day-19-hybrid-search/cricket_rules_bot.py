"""Day 19 bonus: cricket rules bot that answers only from a note, with a source.

Standard library only. Run:
    python cricket_rules_bot.py
    python cricket_rules_bot.py "follow-on kya hota hai?"
    python cricket_rules_bot.py --trap

NOTE is a short rules note written in my own words (not the MCC text).
For the exact wording, read MCC Law 14: lords.org/mcc/the-laws-of-cricket/the-follow-on
Search = Day 19 hybrid search (BM25 keyword + toy vector, joined with RRF).
New rule here: answer only when BOTH searches agree on the top para
(like on-field umpire + third umpire). Otherwise: "Pata nahi".
"""

import math
import sys
from collections import Counter

# The rules note, in my own words. One para = one chunk.
NOTE = [
    "Test match 5 din ka hota hai. Har team 2 baar batting karti hai.",
    "Follow-on: 5 din ke match mein jo team pehle batting kare aur 200 run aage ho, "
    "wo doosri team ko turant dobara batting karwa sakti hai.",
    "Chhote match mein lead kam chahiye: 3 ya 4 din = 150 run, 2 din = 100, 1 din = 75.",
    "Ye option hai, zaroori nahi. Captain decide karta hai aur umpires ko batata hai. "
    "Batane ke baad faisla final.",
    "Pehla din poora baarish mein gaya? Lead bache hue din ke hisaab se lagti hai.",
    "5 din mein result na nikle to match draw hota hai.",
]

QUESTIONS = [
    "follow-on kya hota hai?",
    "kitne run aage hone chahiye?",
    "kal match kaun jeetega?",
]

STOP = {"kya", "hai", "hota", "ho", "ke", "ki", "ka", "mein", "to", "se", "aur", "hone", "chahiye"}


def tokenize(text):
    """lower() + split + strip punctuation, small words removed."""
    words = [w.strip(".,?!:;\"'()") for w in text.lower().split()]
    return [w for w in words if w and w not in STOP]


class BM25:
    """A small BM25 (Okapi), same as Day 19."""

    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.avg_len = sum(len(d) for d in docs) / len(docs)
        self.doc_freq = Counter(w for d in docs for w in set(d))

    def get_scores(self, query_words):
        n_docs, scores = len(self.docs), []
        for doc in self.docs:
            counts, score = Counter(doc), 0.0
            for w in query_words:
                f = counts[w]
                if f:
                    idf = math.log((n_docs - self.doc_freq[w] + 0.5) / (self.doc_freq[w] + 0.5) + 1)
                    part = 1 - self.b + self.b * len(doc) / self.avg_len
                    score += idf * f * (self.k1 + 1) / (f + self.k1 * part)
            scores.append(score)
        return scores


# Toy "meaning" map. A real embedding model learns this by itself (Day 15).
MEANING = {
    "follow-on": "followon", "dobara": "followon", "turant": "followon",
    "run": "lead", "aage": "lead", "lead": "lead",
    "din": "days", "baarish": "rain",
    "captain": "decide", "decide": "decide", "faisla": "decide",
    "draw": "result", "result": "result",
}


def to_vector(text):
    return Counter(MEANING[w] for w in tokenize(text) if w in MEANING)


def cosine(a, b):
    dot = sum(a[k] * b[k] for k in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def to_rank(scores):
    ids = [i for i, s in enumerate(scores) if s > 0]
    return sorted(ids, key=lambda i: scores[i], reverse=True)


def rrf(*ranked_lists, k=60):
    total = {}
    for ranked in ranked_lists:
        for rank, i in enumerate(ranked, start=1):
            total[i] = total.get(i, 0.0) + 1 / (k + rank)
    return sorted(total, key=lambda i: total[i], reverse=True)


def ask(q, two_umpires=True):
    kw = to_rank(BM25([tokenize(p) for p in NOTE]).get_scores(tokenize(q)))
    vec = to_rank([cosine(to_vector(q), to_vector(p)) for p in NOTE])
    top = rrf(kw, vec)
    # Two umpires: both searches must have the same para in their top 2.
    if not top:
        return "Pata nahi. Ye note mein nahi hai.", None
    if two_umpires and (top[0] not in kw[:2] or top[0] not in vec[:2]):
        return "Pata nahi. Ye note mein nahi hai.", None
    return NOTE[top[0]], top[0] + 1


def main():
    if sys.argv[1:] == ["--trap"]:
        # The trap from the reel: no two-umpire rule, so "match" alone is enough.
        q = "kal match kaun jeetega?"
        answer, para = ask(q, two_umpires=False)
        print("TRAP (one umpire):", q, "->", answer, f"[Note, para {para}]")
        answer, para = ask(q)
        print("FIX  (two umpires):", q, "->", answer)
        return
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else QUESTIONS
    for q in questions:
        answer, para = ask(q)
        print("Sawaal:", q)
        print("Jawab: ", answer)
        print("Source:", f"[Note, para {para}]" if para else "(koi nahi)")
        print()


if __name__ == "__main__":
    main()
