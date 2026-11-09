# Day 21 · P2 part 2: jawab ke saath source

**Week 3 · Project 2: Lala Policy Bot (RAG)** · [← Day 20](../day-20-p2-policy-bot-ingest) · [Day 22 →](../day-22-hallucination) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Bot bola WFH 3 din, HR bola 2! Saboot do!"*

Yesterday your Policy Bot read the docs and answered one question. Today every answer comes with its **rasid**: the file and the page it came from. If the bot is making things up, you catch it in 2 seconds.

## The idea: kirana ka bill aur rasid

The kirana wala says "500 rupaye" (example). You don't just trust him. You ask for the rasid.

| At the kirana | In the Policy Bot | Where it comes from |
|---|---|---|
| **Bill** (500 rupaye, ex.) | The bot's answer | The AI writes it |
| **Rasid** | Source: file + page | Your code prints it from **metadata** |

The one rule of today: **the source is printed by your code from metadata, never written by the AI.**

## The code, step by step

This is the Chroma version from the reel. It builds on your Day 20 ingest and the Day 16 `ask(q, res)` helper.

**Step 1. At ingest, store the file AND the page.** Day 20 stored only `{"page": n}`. Now add the file name too:

```python
col.add(
    documents=chunks,
    metadatas=[{"file": f, "page": n} for f, n in chunk_sources],
    ids=chunk_ids,
)
```

Metadata changed, so run your ingest again (use a fresh collection, or delete the old one first).

**Step 2. Take the top 3 chunks and their metadata.**

```python
res = col.query(query_texts=[q], n_results=3)
src = res["metadatas"][0]
```

`res["metadatas"]` has one list per question. You asked one question, so `[0]` is the list of metadata dicts of the top 3 chunks.

**Step 3. Get the answer and print it with the rasid.**

```python
answer = ask(q, res)
print(answer, src)
```

Example output (story example, sample data):

```
WFH 2 din, hr_policy page 4
```

## The trap: source bhi AI se likhwaya

Many beginners write in the prompt: *"answer and also tell the page number"*. The AI can invent a page number. It may say "page 7" when the real chunk was page 4, or when page 7 doesn't even exist.

| Who writes it | Can you trust it? |
|---|---|
| AI: "page 7" | No. The AI can make it up. |
| Metadata: page 4 | Yes. Your code saved it at ingest. |

So: the AI writes the **bill**. Your code prints the **rasid**.

## Jawab: bot ka gappa 2 second mein kaise pakdoge?

**Rasid dekho.** Open that file at that page and check. Rasid nahi, to bharosa nahi.

## Aaj ka kaam (about 45 minutes)

No Chroma or API key needed for the practice files below. They use only the Python standard library and a tiny word-match search, so you can see the idea first.

1. **Run the bot with sources.** In this folder:
   ```
   python ask_with_source.py
   ```
   Ask your own question too:
   ```
   python ask_with_source.py "laptop kho jaye to kya karna hai?"
   ```
   You see the answer, then the source list (file + page) printed from metadata.
2. **See the trap.** Run:
   ```
   python trap_demo.py
   ```
   A pretend AI answer says "page 7". The script compares it with the metadata and catches the gappa.
3. **Check 3 answers yourself.** For each answer, open the page it points to:
   ```
   python check_sources.py hr_policy 4
   ```
   Read the page. Does it really say what the bot said? Write down any answer that didn't match. You will need that list tomorrow.
4. **Upgrade your real Policy Bot.** In your Day 20 project: store `{"file": f, "page": n}` at ingest, re-ingest, and print `src` under every answer, as in the steps above.
5. **Push to GitHub.** Commit with a message like `Day 21: answers show source file + page`.

Sirf sample ya public data. Never put real company documents in a public repo.

## Week 3 recap

| Term | Plain meaning |
|---|---|
| **Embedding** | Address: text turned into numbers, so similar meaning sits close together |
| **RAG** | Open book exam: find the right pages first, then answer |
| **Chunk** | Thali: the big document served in small pieces |
| **Vector DB** | Index: finds the closest chunks fast |
| **Source (today)** | Rasid: file + page, printed from metadata |

## Files in this folder

| File | What it is |
|---|---|
| [ask_with_source.py](ask_with_source.py) | Loads the sample docs page by page, stores `{"file", "page"}` metadata, finds the top 3 chunks, prints the answer and the source from metadata |
| [trap_demo.py](trap_demo.py) | Shows the trap: a pretend AI source ("page 7") checked against the real metadata |
| [check_sources.py](check_sources.py) | Opens a file at a page so you can check an answer with your own eyes |
| [sample_docs/hr_policy.txt](sample_docs/hr_policy.txt) | Fictional Lala Infotech HR policy (sample data) |
| [sample_docs/travel_policy.txt](sample_docs/travel_policy.txt) | Fictional Lala Infotech travel policy (sample data) |

The search here is simple word matching, a stand-in for Chroma, and the answer is the best matching sentence, a stand-in for the Day 16 `ask(q, res)` that calls the LLM. The source rule is exactly the same.

**Rasid aa gayi?** Comment **SOURCE** on the Day 21 reel. Tomorrow, Day 22: hallucination, Chaddha ki fake news. Why does a bot make things up, and how do you reduce it?

*(Fictional story, real plan. Lala Infotech and its policies are made up for practice.)*
