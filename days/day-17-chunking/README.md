# Day 17 · Thali parosna: chunking

**Week 3 · P2 Lala Policy Bot (RAG)** · [← Day 16](../day-16-why-rag) · [Day 18 →](../day-18-vector-search) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! 200 page ki HR handbook bot mein daalo, aaj shaam tak!"*

Yesterday (Day 16) we learned that you should not paste a whole book into the prompt. So how do 200 pages go into a bot? You cut them into small pieces first. That cutting is called **chunking**.

## The idea: shaadi ki thali

At a wedding nobody puts the whole bhagona on one thali. Food is served in portions.

| Word | At the shaadi | What it means in code |
|---|---|---|
| **Document** | Bhagona | The full text, for example a 200-page handbook |
| **Chunk** | Portion on the thali | One small piece of that text |
| **Overlap** | A little dal on the chawal too | The end of one chunk repeats at the start of the next, so nothing breaks at the edge |

Why cut at all? Small pieces let a search find the *right* piece (that is Day 18), and the prompt stays short.

## The code from the reel

```python
size, step = 500, 450          # step 450 means 50 characters of overlap
chunks = []
for i in range(0, len(text), step):
    chunks.append(text[i:i + size])
print(len(chunks))
```

Line by line:
- `size = 500`: each piece is 500 characters long.
- `step = 450`: the next piece starts 450 characters later, so the last 50 characters repeat. That is the overlap.
- `text[i:i + size]`: Python slicing, "give me characters from i up to i + size".
- `range(0, len(text), step)`: i goes 0, 450, 900, ... until the text ends.
- `len(chunks)`: how many pieces you got.

In the reel the demo text is one sample chapter of 18000 characters. 18000 / 450 = 40, so you get exactly 40 chunks. That is just arithmetic on that sample, your own count depends on your text.

## The trap: sentence beech mein kat gaya

A fixed cut does not care about sentences. In the sample policy, "chhutti" can land in one chunk and "18 din" in the next. Now neither chunk has the full answer. Matlab toot gaya.

Two fixes:
1. **Keep an overlap**, so the edge of each chunk repeats in the next one.
2. **Cut on paragraphs** (or sentences) instead of a fixed number of characters.

Run [trap_demo.py](trap_demo.py) to see the break happen and both fixes working.

## One more rule: har chunk ke saath page number

Save the page with every chunk, like this:

```python
{"text": chunk, "page": 12}
```

(Page 12 is just an example.) Later, on Day 21, your bot will show the page as saboot for its answer. No page saved now means no saboot later.

## Jawab: kitna bada, kahan se kaato?

A good **starting point**: 300 to 500 characters, a little overlap, and cut on paragraphs when you can. This is not a law. Test it on your own text and change it.

## Aaj ka kaam (about 40 minutes)

1. **Get the files.** Copy this folder, open it in VS Code and run:
   ```
   python chunk_3_ways.py
   ```
   It cuts [sample_handbook.txt](sample_handbook.txt) 3 ways (200, 500 and 1000 characters, 10% overlap), counts the chunks and shows which chunk best matches a question.
2. **See the trap.**
   ```
   python trap_demo.py
   ```
3. **Chunk with page numbers.**
   ```
   python chunk_with_pages.py
   ```
   It cuts on paragraphs, keeps the page with every chunk and saves `chunks.json`. Open that file and look at it.
4. **Now your own public PDF.** Pick any public PDF (a public policy, a public report, a public manual). Open it, select all the text, copy it and paste it into a new file `my_pdf.txt` in this folder. Python's standard library cannot read PDFs, so copy and paste is the simple way today.
   - Want page numbers? Put a line like `=== PAGE 1 ===` before each page's text. Without these lines everything counts as page 1.
5. **Run it 3 ways on your text.**
   ```
   python chunk_3_ways.py my_pdf.txt
   python chunk_with_pages.py my_pdf.txt
   ```
   Change `QUESTION` at the top of the file to a question your PDF answers. Note down: how many chunks for 200, 500 and 1000? Which size gave the best chunk? How many chunks were cut mid-sentence?
6. **Put it on GitHub.** Upload the scripts and a short note with your 3 counts and which size won. Your bahi khata gets one more entry.

**Note:** the "best chunk" here is found by counting matching words. It is a simple stand-in so you can compare the 3 sizes. Real search by meaning comes tomorrow.

## One rule: sirf sample ya public data

Never paste office or company documents into these scripts or any AI tool. Use the sample handbook here or a public PDF. Lala Infotech and its handbook are fictional.

## Files in this folder

| File | What it is |
|---|---|
| [sample_handbook.txt](sample_handbook.txt) | A few pages of a fictional Lala Infotech HR handbook, with page markers |
| [chunk_3_ways.py](chunk_3_ways.py) | Cuts a text into 200, 500 and 1000 character chunks, counts them, finds the best match for a question |
| [trap_demo.py](trap_demo.py) | Shows a sentence breaking at a chunk edge, then the overlap fix and the sentence fix |
| [chunk_with_pages.py](chunk_with_pages.py) | Cuts on paragraphs, keeps the page number with every chunk, saves `chunks.json` |

**Chunks ready?** Comment **CHUNK** on the Day 17 reel. Tomorrow, Day 18: library ka index, vector search. Sahi tukda pal mein kaise milta hai.
