# Day 20 · Project 2 part 1: Lala Policy Bot

**Week 3 · RAG** · [← Day 19](../day-19-hybrid-search) · [Day 21 →](../day-21-p2-citations) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! HR se roz 50 baar chhutti, WFH poochhte hain. Monday tak bot chahiye!"*

Aaj Project 2 shuru. The reel asked: **PDF se bot tak kitne steps?** The answer is below. Try your own guess first.

## The idea: naya munshi aur Lala ki rulebook

A new munshi joins Lala's office. Before he answers anyone, he reads the rulebook, cuts it into small parts, marks every part with its page, keeps it in the right drawer, and opens that exact page when someone asks. A policy bot does the same.

**Jawab: 5 steps.**

| Step | The munshi | In code | What it does |
|---|---|---|---|
| **1. Padho** | Reads the rulebook | `PdfReader(f).pages` (pypdf) | Gets the text out of each PDF page |
| **2. Kaato** | Cuts pages into small parts | `chunk(text)` (your Day 17 helper) | Small pieces are easier to search |
| **3. Address banao** | Writes the page on each part | `new_id(f, n, i)` + `{"page": n}` | A stable id and the page number for every piece |
| **4. Rakho** | Keeps parts in the drawer | `col.add(...)` (Chroma) | Stores the piece. Chroma makes the embedding for you |
| **5. Poochho** | Opens the right page | `col.query(...)` | Finds the closest pieces for a question |

## The trap: scanned PDF

Har beginner yahan phansta hai. A scanned PDF is only photos of pages. There is no text inside, so `page.extract_text()` gives back an empty string `""`. Your bot then has nothing to search, and nothing tells you.

**The rule:** check every page before you store it. If the text is empty, skip it and print a warning. Reading text from photos (OCR) is a separate job, not part of today.

## Policy badal gayi? Upsert

HR changes the WFH rule. Do not add the new text with new ids, or the bot keeps the old rule too. Use the **same ids** with `col.upsert(...)`: the old piece is replaced by the new one. That is why ids are built from file + page + chunk number: the same piece always gets the same id.

If the new page has fewer chunks than before, delete the extra old ids with `col.delete(ids=[...])`.

## Aaj ka kaam (about 45 to 60 minutes)

1. **Make the sample PDFs.** No real company files, only the fictional Lala sample:
   ```
   python make_sample_pdf.py
   ```
   You get `lala_hr_policy.pdf` (12 pages, text PDF) and `lala_scanned_notice.pdf` (a page with no text layer, it behaves like a scan, for the trap).
2. **See the 5 steps without installing anything.** This runs with plain Python:
   ```
   python mini_ingest.py
   python mini_ingest.py "Sick leave ke liye kya chahiye?"
   ```
   It reads `sample_policy.txt`, chunks it, stores pieces with ids and pages, answers a question with the page number, shows the trap check and does an upsert.
3. **Now the real way: pypdf + Chroma.** In a virtual environment:
   ```
   pip install pypdf chromadb
   ```
   Save this as `ingest.py` in this folder and run `python ingest.py`:
   ```python
   from pathlib import Path

   import chromadb
   from pypdf import PdfReader


   def chunk(text, size=500, overlap=50):
       # Same idea as Day 17: fixed size pieces with a small overlap.
       pieces = []
       start = 0
       while start < len(text):
           pieces.append(text[start:start + size])
           start += size - overlap
       return pieces


   def new_id(f, page, i):
       # Stable id: file + page + chunk number. Same piece, same id.
       return f"{Path(f).stem}-p{page}-c{i}"


   client = chromadb.Client()
   col = client.get_or_create_collection("lala_policy")

   for f in ["lala_hr_policy.pdf", "lala_scanned_notice.pdf"]:
       # 1. Padho
       for n, page in enumerate(PdfReader(f).pages, 1):
           text = page.extract_text() or ""
           # The trap check
           if not text.strip():
               print(f"{f} page {n}: no text (scanned?). Skipped. OCR is a separate step.")
               continue
           # 2. Kaato
           for i, c in enumerate(chunk(text)):
               # 3. Address banao + 4. Rakho
               col.add(ids=[new_id(f, n, i)], documents=[c], metadatas=[{"page": n}])

   # 5. Poochho
   res = col.query(query_texts=["How many WFH days do I get?"], n_results=2)
   for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
       print(f"page {meta['page']}: {doc[:120]}")
   ```
   The first run downloads a small embedding model, so you need internet once.
4. **Print the page number with the answer.** You should see the WFH page in the results. In our sample it is page 4 (example output, your text may differ).
5. **Push to GitHub:** `make_sample_pdf.py`, `mini_ingest.py`, `ingest.py`, `sample_policy.txt`. Project 2 has its first commit.

Sirf sample ya public data. Never put your office's HR PDFs in a public repo.

Aur haan: hike wali policy is sample mein bhi nahi hai. Chaddha sir ko bhi nahi mili.

## Files in this folder

| File | What it is |
|---|---|
| [sample_policy.txt](sample_policy.txt) | Fictional Lala Infotech HR policy, 12 pages (sample data) |
| [make_sample_pdf.py](make_sample_pdf.py) | Builds the two sample PDFs from the text file (standard library only) |
| [mini_ingest.py](mini_ingest.py) | The 5 steps, trap check and upsert in plain Python, no installs |

**Bot ne pehla jawab diya?** Comment **BOT** on the Day 20 reel. Tomorrow, Day 21: jawab ke saath saboot, the answer shows its source page.
