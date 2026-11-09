# Day 18 · Library ka index: vector search

**Week 3 · RAG: Lala Policy Bot (P2)** · [← Day 17](../day-17-chunking) · [Day 19 →](../day-19-hybrid-search) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Bot 10 second leta hai, customer bhaag rahe! Kal tak fast karo!"*

## Sawaal (answered at the end)

10,000 kitaabon mein se sirf 3 chahiye. **Har kitaab khologe?**

Rahul's bot was doing exactly that: reading every chunk for every question. Today we fix it.

## The idea: a library with an index

| In the library | In your bot | What it does |
|---|---|---|
| **Kitaabein** | Chunks (from Day 17) | The small pieces of your document |
| **Index card** | Embeddings, stored in a **vector DB** | Made **once**, before any question comes |
| **Sawaal** | **Query** | Your question also becomes an embedding |
| **Paas ki k kitaabein** | **Top-k** results | The k chunks closest to the question |

You don't open every book in a library. You check the index, then walk straight to the right shelf. A vector DB keeps the index ready, so a question only has to find its nearest neighbours.

## Aaj ka kaam (about 45 minutes)

1. **Feel the idea first (no install).** Run the toy version. It uses only the Python standard library:
   ```
   python mini_vector_search.py
   ```
   It builds a tiny index from [sample_policy.txt](sample_policy.txt), saves it to `toy_index.json` and prints the top 3 chunks for 3 questions. Run it again: this time it loads the saved index instead of building it. Try `python mini_vector_search.py 5` to see the top 5.

2. **Install Chroma** (a real vector DB). Open a terminal:
   ```
   pip install chromadb
   ```
   Windows and `pip` doesn't work? Try `py -m pip install chromadb`.

3. **Make `search.py`.** Create a new file `search.py` in this folder and paste this:
   ```python
   import chromadb

   # Load chunks: blank line = new chunk. Or use your Day 17 chunks here.
   with open("sample_policy.txt", encoding="utf-8") as f:
       chunks = [c.strip() for c in f.read().split("\n\n") if c.strip()]

   # PersistentClient saves to the "db" folder (the diary).
   db = chromadb.PersistentClient(path="db")
   col = db.get_or_create_collection("policy")

   # Add only once. Every chunk needs a unique string id.
   if col.count() == 0:
       ids = [str(i) for i in range(len(chunks))]
       col.add(ids=ids, documents=chunks)
       print("Saved", col.count(), "chunks")
   else:
       print("Already saved in the diary:", col.count(), "chunks")

   questions = [
       "How many casual leave days do I get?",
       "Can I work from home on Friday?",
       "How do I claim my internet bill?",
   ]

   for q in questions:
       res = col.query(query_texts=[q], n_results=3)
       print("\nQ:", q)
       for rank, doc in enumerate(res["documents"][0], start=1):
           print(f"  #{rank}", doc[:80])
   ```
   Run it:
   ```
   python search.py
   ```
   Chroma embeds the chunks and the questions **itself**, with the same model for both (the Day 15 rule). The first run can be slower while Chroma sets things up.

4. **The diary test.** Close the program and run `python search.py` again. You should see `Already saved in the diary`. Your data survived.

5. **Put it on GitHub.** Upload `search.py` and a screenshot of your top 3 results. Don't upload the `db` folder; it can be rebuilt any time.

Sirf sample ya public data. No office documents, no customer data.

## Trap: Client() se sab gayab

Har beginner yahan phansta hai.

| Code | Like | What happens |
|---|---|---|
| `chromadb.Client()` | Dimaag (Day 7) | Lives in memory. Program band, sab gayab. |
| `chromadb.PersistentClient(path="db")` | Diary | Saved in a folder. Still there tomorrow. |

See it with plain Python:
```
python memory_vs_diary.py
python memory_vs_diary.py
```
The memory list is always back to 1 item. The diary file keeps growing. Start fresh with `python memory_vs_diary.py --reset`.

## k kitna? Top 3 hi kyun?

- **Too many chunks:** more tokens, and more noise for the LLM to get confused by.
- **Too few chunks:** the right answer can be missed.
- **Start with 3 to 5**, then test with your own questions. This is a starting point, not a rule.

## Jawab

**Nahi, har kitaab nahi kholte.** The vector DB already holds the index (the embeddings were made once, when you added the chunks). A question comes in, gets its own embedding, and the DB hands back the closest 3 straight away.

The toy version in this folder still compares the question with every chunk, because it is tiny. Real vector DBs use smarter index structures so they don't have to check everything, which is why they stay fast with many chunks.

## Files in this folder

| File | What it is |
|---|---|
| [sample_policy.txt](sample_policy.txt) | Fictional Lala Infotech HR policy (sample data), one chunk per paragraph |
| [mini_vector_search.py](mini_vector_search.py) | Toy vector search, standard library only: build index once, save it, query top-k |
| [memory_vs_diary.py](memory_vs_diary.py) | The trap in plain Python: memory forgets, a file remembers |
| `search.py` | You make this in step 3 (needs `pip install chromadb`) |

**Top 3 mil gaye?** Comment **VECTOR** on the Day 18 reel. Tomorrow, Day 19: vector DB hi sab kuch nahi, hybrid search (keyword + vector).

*Fictional story, real plan. Lala Infotech and its policy are made up.*
