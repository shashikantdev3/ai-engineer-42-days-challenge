"""Day 20: the 5 steps of a policy bot, in plain Python (no installs).

    python mini_ingest.py
    python mini_ingest.py "Sick leave ke liye kya chahiye?"

Padho -> Kaato -> Address banao -> Rakho -> Poochho.
The real version uses pypdf and Chroma (see README). This mini version
reads sample_policy.txt and counts shared words to find pieces (like the
Day 19 keyword search). Real Chroma searches by meaning with embeddings.
All data is fictional sample data.
"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
FILE = "sample_policy.txt"


# 1. Padho: read the pages
def read_pages(path):
    """Return a list of (page_number, text)."""
    pages = []
    current = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("=== PAGE"):
            if current:
                pages.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        pages.append("\n".join(current).strip())
    return list(enumerate(pages, 1))


# 2. Kaato: cut text into small pieces (same idea as Day 17)
def chunk(text, size=200, overlap=40):
    pieces = []
    start = 0
    while start < len(text):
        pieces.append(text[start:start + size])
        start += size - overlap
    return pieces


# 3. Address banao: a stable id from file + page + chunk number
def new_id(file, page, i):
    return f"{Path(file).stem}-p{page}-c{i}"


# 4. Rakho: a tiny drawer that works a bit like a Chroma collection
class MiniCollection:
    def __init__(self):
        self.items = {}  # id -> (document, metadata)

    def add(self, ids, documents, metadatas):
        for i, doc, meta in zip(ids, documents, metadatas):
            if i in self.items:
                # Our mini add refuses to overwrite, so you notice. Use upsert.
                print(f"  id {i} already stored. Use upsert to replace it.")
                continue
            self.items[i] = (doc, meta)

    def upsert(self, ids, documents, metadatas):
        # Same id = the old piece is replaced by the new one.
        for i, doc, meta in zip(ids, documents, metadatas):
            self.items[i] = (doc, meta)

    def delete(self, ids):
        for i in ids:
            self.items.pop(i, None)

    def query(self, question, n_results=2):
        # 5. Poochho: score = how many question words appear in the piece.
        words = [w.strip("?.,!()").lower() for w in question.split()]
        words = [w for w in words if len(w) > 2]
        scored = []
        for i, (doc, meta) in self.items.items():
            doc_words = {w.strip("?.,!():").lower() for w in doc.split()}
            score = sum(1 for w in words if w in doc_words)
            if score > 0:
                scored.append((score, i, doc, meta))
        scored.sort(key=lambda row: row[0], reverse=True)
        return scored[:n_results]


def ingest(col, file, pages):
    """Store every page. Skip empty pages (the scanned PDF trap)."""
    stored = 0
    for n, text in pages:
        # The trap check: a scanned page has no text at all.
        if not text.strip():
            print(f"  {file} page {n}: no text (scanned?). Skipped. OCR is a separate step.")
            continue
        for i, c in enumerate(chunk(text)):
            col.add(ids=[new_id(file, n, i)], documents=[c], metadatas=[{"page": n}])
            stored += 1
    return stored


def ask(col, question):
    print(f"\nSawaal: {question}")
    results = col.query(question)
    if not results:
        print("  Koi jawab nahi mila. Try other words.")
        return
    for score, i, doc, meta in results:
        short = " ".join(doc.split())[:110]
        print(f"  page {meta['page']} (score {score}): {short}")


def main():
    question = " ".join(sys.argv[1:]) or "WFH kitne din milta hai? WFH per week"
    col = MiniCollection()

    print("Steps 1 to 4: padho, kaato, address banao, rakho")
    pages = read_pages(HERE / FILE)
    stored = ingest(col, FILE, pages)
    print(f"  {len(pages)} pages read, {stored} pieces stored")

    print("\nStep 5: poochho")
    ask(col, question)

    print("\nTrap demo: a page that came from a scanned PDF")
    ingest(col, "scanned_notice.pdf", [(1, "")])

    print("\nPolicy badli: WFH is now 3 days. Upsert with the same ids.")
    new_text = (
        "Work from home (WFH)\n"
        "Employees can take up to 3 WFH days per week.\n"
        "WFH must be marked in the HR portal one day before."
    )
    new_pieces = chunk(new_text)
    new_ids = [new_id(FILE, 4, i) for i in range(len(new_pieces))]
    col.upsert(ids=new_ids, documents=new_pieces, metadatas=[{"page": 4}] * len(new_pieces))
    # The new page is shorter, so remove old pieces that are no longer used.
    old_ids = [k for k in col.items if k.startswith(f"{Path(FILE).stem}-p4-")]
    col.delete([k for k in old_ids if k not in new_ids])
    ask(col, "WFH kitne din per week?")


if __name__ == "__main__":
    main()
