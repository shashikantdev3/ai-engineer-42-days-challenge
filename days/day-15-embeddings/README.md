# Day 15 · Embeddings: mohalla ka address

**Week 3 · P2 Lala Policy Bot (RAG) starts** · [← Day 14](../day-14-p1-readme-and-recap) · [Day 16 →](../day-16-why-rag) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! 500 complaints mein se battery wali nikaalo, kal subah tak!"*
> Rahul: *"Log battery nahi, 'charge nahi tikta' likhte hain!"*

Ctrl F only finds the exact word. Today you learn how a computer finds the **meaning**, even when the word is missing.

## The idea: every sentence gets an address

In a desi mohalla, similar shops sit together. Mithai ki dukaanein ek gali mein, kapde ki doosri mein.

| In the mohalla | In AI | What it means |
|---|---|---|
| A shop's address | **Embedding** | A list of numbers for one sentence |
| Mithai shops in one gali | Similar meaning | Sentences with similar meaning get nearby addresses |
| How close two shops are | **Cosine score** | A number for how close two addresses are. Higher means closer |
| Walking every gali | **Loop + sorted** | Score every complaint, then keep the top 3 |

So "charge nahi tikta" lands **near** "battery jaldi khatam", even though the word battery is not in it. And "printer jam" lands far away.

The code from the reel:

```python
r = client.models.embed_content(
    model="gemini-embedding-2",
    contents=texts)
v = [e.values for e in r.embeddings]
s = cosine(v[0], v[1])
```

`embed_content` and `.values` come from the Gemini API (google-genai package). `cosine()` is not a library function: it is a small helper you get in [embed_helpers.py](embed_helpers.py), written with plain Python maths.

**About the numbers in the reel:** 0.82 and 0.21 were **examples**. Your scores will be different. What matters is the order: the battery-type sentence scores higher than the printer one.

## The trap: do alag model, do alag nakshe

If you embed the complaints with one model and the question with another model, you get two different maps. The addresses do not match, and the scores mean nothing.

**Rule:** complaints and question, always the **same model**. In the code, keep the model name in one place (`MODEL` in [embed_helpers.py](embed_helpers.py)) and use it for both.

[mohalla_toy.py](mohalla_toy.py) shows this trap with toy numbers, no internet needed.

## Aaj ka kaam (about 45 minutes)

1. **Start offline.** Download this folder and run:
   ```
   python mohalla_toy.py
   ```
   It uses hand-made 3-number addresses (real embeddings are much longer, 3072 numbers by default). You will see the closest pair, the top 3 for "battery", and the trap.
2. **Install the Gemini package** (only needed for the real embeddings):
   ```
   pip install google-genai
   ```
3. **Set your API key** in the terminal, never inside the code:
   - Windows (PowerShell): `$env:GEMINI_API_KEY="your-key"`
   - Mac / Linux: `export GEMINI_API_KEY="your-key"`
4. **Homework: embed 5 sentences, find the closest pair.**
   ```
   python closest_pair.py
   ```
   It embeds 5 sample sentences, prints the cosine score of every pair (10 pairs) and tells you the closest one. Then change the 5 sentences to your own and run it again. Did the pair you guessed win?
5. **Bonus: Rahul's battery search.**
   ```
   python find_battery.py
   ```
   It reads [sample_complaints.txt](sample_complaints.txt), embeds every complaint and the question with the same model, loops over the scores and shows the top 3. It also shows how many of them Ctrl F would have missed.
6. **Push to GitHub.** Add the files to your repo with a commit like `Day 15: embeddings and closest pair`. Write your closest pair and its score in your README.

## Rules for today

- **Sample data only.** Never paste real company complaints or customer data into any API. Lala Infotech is fictional, and so are these complaints.
- **Own laptop, own key.** Keep the key in an environment variable, never commit it to GitHub.

## Files in this folder

| File | What it is |
|---|---|
| [embed_helpers.py](embed_helpers.py) | `cosine()` (plain Python) and `embed()` (calls the Gemini API). One `MODEL` for everything |
| [mohalla_toy.py](mohalla_toy.py) | Offline demo with toy addresses: closest pair, top 3, and the 2-model trap |
| [closest_pair.py](closest_pair.py) | The homework: embed 5 sentences, score every pair, find the closest |
| [find_battery.py](find_battery.py) | Bonus: top 3 battery complaints without the word battery |
| [sample_complaints.txt](sample_complaints.txt) | 15 made-up complaints, one per line |

**Closest pair mil gaya?** Comment **EMBED** on the Day 15 reel. Tomorrow, Day 16: LLM ko company ki baat kyun nahi pata? Week 3, RAG ki shuruaat.
