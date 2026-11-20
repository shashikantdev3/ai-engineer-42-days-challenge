# Day 19 · Vector DB hi sab kuch nahi: hybrid search

**Week 3 · Project 2 (RAG)** · [← Day 18](../day-18-vector-search) · [Day 20 →](../day-20-p2-policy-bot-ingest) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Customer ne E-404 poocha, bot printer ki kahani suna raha hai!"*

## The idea: mele mein bachcha khoya

Yesterday (Day 18) you searched chunks by **meaning** with a vector DB. That works great for normal sentences. But exact things like error codes (`E-404`), product names and IDs can get missed, because a code has no "meaning" for the model to match.

So how do you find a lost child at a mela? **Dono se.** Announcement by name, and recognising the face.

| At the mela | In search | What it catches |
|---|---|---|
| **Naam se** (announcement) | Keyword search (BM25) | Exact words: error codes, product names, IDs |
| **Shakal se** (pehchaan) | Vector search | Meaning: "printer kharab" ≈ "print nahi ho raha" |
| **Dono se** | Hybrid search | Both. Join the two ranked lists. |

## Rule 1: score nahi, rank jodo

BM25 scores and vector scores live on different scales, so you cannot just add them. Instead, join the **ranks**: whatever is high in both lists ends up highest.

This is called **reciprocal rank fusion (RRF)**. For every list a chunk appears in, it gets:

```
1 / (60 + rank)
```

Add these up and sort. `k = 60` is the common default (Cormack, Clarke and Buettcher, 2009). Example: a chunk at rank 1 in keyword and rank 2 in vector gets `1/61 + 1/62`.

## Rule 2: the trap (Chhutti vs chhutti)

For keyword search, `"Chhutti"` and `"chhutti"` are two different words. If your chunk says *Chhutti policy* and the user types *chhutti*, no match.

The fix: **`.lower()` on both sides.** Chunks bhi, sawaal bhi. Lower one side only and the trap is still there.

## Aaj ka kaam (about 45 minutes)

1. **See the trap.** Run [trap_lower.py](trap_lower.py):
   ```
   python trap_lower.py
   ```
   It shows the match failing without `lower()` and working with it on both sides.
2. **See RRF by hand.** Run [rrf_demo.py](rrf_demo.py). It joins two small ranked lists and prints every `1/(60 + rank)` step, so you can check the maths yourself.
3. **Compare all three.** Run [hybrid_search.py](hybrid_search.py):
   ```
   python hybrid_search.py
   ```
   It has 10 sample Lala Infotech chunks (one is the E-404 guide) and prints the top 3 for **keyword-only**, **vector-only** and **hybrid**. You should see the E-404 guide at #1 in keyword and hybrid, while vector-only puts a general "issue" tip first.
4. **Make it yours.** Change `QUESTION` at the top of the file, add your own sample chunk with another error code, and run again. Write in your notes: which search won, and why?
5. **Put it on GitHub.** Upload the files to your repo with a commit like `Day 19: hybrid search`.

Only sample or public data. Never office tickets or real customer data.

**Note on `hybrid_search.py`:** it uses only the standard library, so it runs anywhere. BM25 is written out in about 20 lines. The "vector" part is a **toy stand-in**: a small hand-written word-to-meaning map, not a real embedding model. It is there to show the idea (meaning matches, codes don't). In your real bot, use the Day 18 Chroma search, as below.

## Pro way (optional): the real libraries from the reel

This is the code shown in the reel. It needs your Day 18 Chroma collection (`col`) with your chunks stored, using the same ids.

```
pip install rank-bm25
```

```python
from rank_bm25 import BM25Okapi
from hybrid_search import rrf   # the small rrf() helper from this folder

# chunks: list of texts, ids: their ids in the same order (same as in Chroma)
bm25 = BM25Okapi([c.lower().split() for c in chunks])

q = "E-404 error aa raha hai"
kw = bm25.get_scores(q.lower().split())
kw_rank = [ids[i] for i in sorted(range(len(chunks)), key=lambda i: kw[i], reverse=True)]

vec = col.query(query_texts=[q], n_results=10)
vec_rank = vec["ids"][0]

final = rrf(kw_rank, vec_rank)
print(final[:3])
```

`kw_rank` and `vec_rank` are just ids sorted from best to worst. `rrf()` joins them.

## Bonus: cricket rules bot (answers only from a note)

India's Test in Wellington is on, and Chaddha sir has a cricket-mad client on Monday. The bot must answer "follow-on kya hota hai?" without guessing.

```
python cricket_rules_bot.py
python cricket_rules_bot.py "follow-on kya hota hai?"
python cricket_rules_bot.py --trap
```

How it works:
1. `NOTE` is 6 short paras of rules, written in my own words. One para = one chunk.
2. The same hybrid search as above: BM25 keyword + toy vector, joined with `rrf()`.
3. **Two-umpire rule:** answer only if the top para is in the top 2 of BOTH searches. Otherwise print `Pata nahi`.
4. The answer comes with its source: `[Note, para 2]`.

The trap (`--trap`): with only one umpire, "kal match kaun jeetega?" matches the word "match" and the bot replies "5 din mein result na nikle to match draw hota hai". That is not a prediction, and the note has no predictions at all. With two umpires, the bot says `Pata nahi`.

Notes:
- The follow-on rule is MCC Law 14 in my words: in a match of 5 days or more, the side batting first and at least 200 runs ahead may make the other side bat again (150 for 3-4 days, 100 for 2 days, 75 for 1 day). It is the captain's choice. For the exact wording read [MCC Law 14](https://www.lords.org/mcc/the-laws-of-cricket/the-follow-on).
- "Top 2 in both" is an example rule, not a standard. Tune it on your own questions.
- The toy vector search only knows a few words, so "follow on" without the hyphen gets `Pata nahi`. A real embedding model (Day 15) fixes that.

## Files in this folder

| File | What it is |
|---|---|
| [hybrid_search.py](hybrid_search.py) | 10 sample chunks, BM25 keyword search, a toy vector search, RRF, and the top 3 of each |
| [rrf_demo.py](rrf_demo.py) | Reciprocal rank fusion step by step on two small lists |
| [trap_lower.py](trap_lower.py) | The Chhutti vs chhutti trap and the `lower()` fix |
| [cricket_rules_bot.py](cricket_rules_bot.py) | Bonus: rules bot that answers only from a note, with a source, or says `Pata nahi` |

**Hybrid chal gaya?** Comment **HYBRID** on the Day 19 reel. Tomorrow, Day 20: Project 2 part 1, Lala Policy Bot.
