# Day 16 · LLM ko company ki baat nahi pata: why RAG

**Week 3 · Project 2: Lala Policy Bot (RAG)** · [← Day 15: Embeddings](../) · [Day 17: Chunking →](../) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! AI ne joinee ko 24 chhutti boli, policy mein 18!"*

## The sawaal from the reel

**To fix this, do we have to train the AI again?**

**Jawab: na!** No training. Make it an open book exam: first find the right page, then give it to the AI. That is **RAG**.

## The idea: naya joinee aur handbook

A new joinee is smart, but he has not read the company handbook. Ask him "chhutti kitni?" and he guesses. The AI is the same.

| In the office | In RAG | What it does |
|---|---|---|
| **Naya joinee** | The AI (LLM) | Smart, but does not know your company's rules |
| **Handbook ka sahi page** | Context | The few lines that hold the answer |
| **Page dhoondhna** | `search()` (your Day 15 helper) | Finds the right pages for the question |
| **"Is page se jawab do"** | The prompt | Tells the AI to answer only from that context |
| **Sahi jawab** | The output | "18 din", because it read the right page |

RAG = **R**etrieve the right pages, **A**ugment (add) them to the prompt, **G**enerate the answer.

## The trap: poori handbook mat do

The beginner mistake: paste all 200 pages into the prompt. The bill gets bigger, and the AI can get lost in the middle of a long text. Give it only the right few pieces (the reel says 3). Tomorrow, Day 17, you learn how to cut a handbook into good pieces (chunking).

## The rule: "pata nahi" bolo

What if the answer is not in the handbook? Write it in the prompt: if it is not in the context, do not guess, say "pata nahi". A "pata nahi" is better than a wrong answer that a new joinee trusts.

## The code from the reel (rag.py)

This is the shape shown in the reel. `search()` is the Day 15 helper from this repo, not a library call. `client` and `MODEL` are set up the same way as in the earlier days of this repo, so no model name is written here.

```python
context = search(q)
prompt = f"Sirf is context se jawab do:\n{context}\nSawaal: {q}"

r = client.interactions.create(
    model=MODEL, input=prompt)
print(r.output_text)
```

If your `search()` returns a list of pages, join them into one string first, for example `context = "\n\n".join(search(q))`.

Then add the "pata nahi" rule to the prompt, for example:

```python
prompt = (
    "Sirf is context se jawab do. Agar jawab context mein nahi hai, "
    "toh sirf 'pata nahi' bolo.\n"
    f"{context}\nSawaal: {q}"
)
```

## Aaj ka kaam (about 40 minutes)

The files in this folder run **offline**, with the Python standard library only. No API key, no internet. They show every RAG step except the real AI call, so you can see exactly what goes into the prompt.

1. **Write 10 questions.** Open [questions.py](questions.py) and replace the sample questions with 10 questions a new joinee really asks (chhutti, laptop, timings, ID card...). Run it:
   ```
   python questions.py
   ```
   It numbers your questions and tells you if you have fewer than 10.
2. **Read the sample handbook.** Open [sample_policy.txt](sample_policy.txt). It is a fictional Lala Infotech HR policy (sample data). Each paragraph is one "page".
3. **Run RAG offline.** Run:
   ```
   python rag_offline.py
   ```
   For each question it shows the pages that `search` found, the full prompt it would send to the AI, and a toy answer. Then pass your own question:
   ```
   python rag_offline.py "How many paid leave days do I get?"
   ```
4. **Pick 3 of your questions** whose answer is in the sample policy, and run them. Check that the right page comes first.
5. **Ask one question that is NOT in the policy** (for example about the canteen menu). The toy answer should be `pata nahi`. If you have your AI setup from earlier days, send the same prompt to the real AI and see if it also says "pata nahi".
6. **See the trap.** Run:
   ```
   python trap_demo.py
   ```
   It compares how many words you send with the full handbook vs only the top 3 pages.
7. **Put it on GitHub.** Add `questions.py` with your 10 questions to your repo and commit: `Day 16: why RAG`.

**Important:** the toy answer in `rag_offline.py` is not an AI. It just shows the best matching page, so you can test search and the "pata nahi" rule without a key.

## One rule: sirf sample data

Use the sample policy in this folder or any public document. Never paste your company's real handbook, tickets or customer data into an AI tool or into a public repo.

## Files in this folder

| File | What it is |
|---|---|
| [questions.py](questions.py) | Your list of 10 new joinee questions |
| [sample_policy.txt](sample_policy.txt) | Fictional Lala Infotech HR policy (sample data) |
| [rag_offline.py](rag_offline.py) | Search, prompt building and the "pata nahi" rule, offline |
| [trap_demo.py](trap_demo.py) | Full handbook vs top 3 pages: how much text you send |

**Got "pata nahi" for the unknown question?** Comment **RAG** on the Day 16 reel. Tomorrow, Day 17: thali parosna, chunking. How to cut the handbook into the right pieces.
