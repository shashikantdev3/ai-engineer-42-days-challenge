"""Day 17: cut on paragraphs and keep the page number with every chunk.

Run with the sample handbook:
    python chunk_with_pages.py
Run with your own text:
    python chunk_with_pages.py my_pdf.txt

Put a line like '=== PAGE 1 ===' before each page in your text file.
Without these lines, everything counts as page 1.

It saves chunks.json in this folder. Standard library only. Python 3.10+.
"""

import json
import re
import sys
from pathlib import Path

# Starting point from the reel: 300 to 500 characters. Test and change it.
MAX_CHARS = 500

QUESTION = "How many days of paid chhutti does an employee get in a year?"

STOP_WORDS = {
    "a", "an", "the", "of", "in", "on", "to", "is", "are", "and", "or",
    "how", "many", "what", "does", "do", "for", "it", "this", "that",
    "be", "by", "with", "at", "from", "get", "gets",
}


def read_pages(path):
    """Return a list of (page_number, page_text)."""
    pages = []
    current_page = None
    lines = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        marker = re.match(r"=== PAGE (\d+) ===", line.strip())
        if marker:
            if current_page is not None:
                pages.append((current_page, "\n".join(lines)))
            current_page = int(marker.group(1))
            lines = []
        else:
            lines.append(line)

    if current_page is not None:
        pages.append((current_page, "\n".join(lines)))
    else:
        # No page markers in the file: treat it all as page 1.
        pages.append((1, "\n".join(lines)))
    return pages


def paragraph_chunks(page_text, max_chars):
    """Join whole paragraphs until the next one would go over max_chars.
    A single very long paragraph stays as one chunk (we never cut inside it)."""
    paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + 2 + len(paragraph) > max_chars:
            chunks.append(current)
            current = paragraph
        elif current:
            current = current + "\n\n" + paragraph
        else:
            current = paragraph
    if current:
        chunks.append(current)
    return chunks


def important_words(sentence):
    return set(re.findall(r"[a-z0-9]+", sentence.lower())) - STOP_WORDS


def score(chunk, question):
    """Simple word match. Real search by meaning comes on Day 18."""
    return len(important_words(chunk) & important_words(question))


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path(__file__).parent / "sample_handbook.txt"

    if not path.exists():
        print(f"File not found: {path}")
        return

    # Har chunk ke saath page: every chunk is a small dict.
    records = []
    for page, page_text in read_pages(path):
        for chunk in paragraph_chunks(page_text, MAX_CHARS):
            records.append({"id": len(records) + 1, "page": page, "text": chunk})

    out_file = Path(__file__).parent / "chunks.json"
    out_file.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"File: {path.name}")
    print(f"{len(records)} chunks (paragraph cut, max {MAX_CHARS} characters)")
    print(f"Saved: {out_file.name}")
    print()

    for record in records:
        first_line = record["text"].splitlines()[0]
        print(f"  chunk {record['id']:>2}  page {record['page']:>3}  {len(record['text']):>4} chars  {first_line[:40]}...")

    best = max(records, key=lambda r: score(r["text"], QUESTION))
    print()
    print(f"Question: {QUESTION}")
    print(f"Best match: chunk {best['id']}, page {best['page']}")
    print("-" * 60)
    print(best["text"])
    print("-" * 60)
    print(f"Saboot: page {best['page']}. On Day 21 your bot will show this with its answer.")


if __name__ == "__main__":
    main()
