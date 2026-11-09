"""Day 17: the trap. A fixed cut can break a sentence in two.

Run:
    python trap_demo.py

Standard library only. Python 3.10+.
"""

import re

# A tiny sample text (fictional policy, like the reel).
TEXT = "Leave rules for all staff. Paid chhutti: 18 din per year. Sick leave is separate."

OVERLAP = 20


def chunk_text(text, size, overlap):
    """Slice the text into pieces, moving forward by size minus overlap."""
    step = size - overlap
    chunks = []
    for i in range(0, len(text), step):
        chunks.append(text[i:i + size])
    return chunks


def sentence_chunks(text):
    """Cut only at the end of a sentence (after . ! or ?)."""
    return [part for part in re.split(r"(?<=[.!?])\s+", text) if part]


def has_full_answer(chunks):
    """Does any single chunk contain both 'chhutti' and '18 din'?"""
    return any("chhutti" in chunk and "18 din" in chunk for chunk in chunks)


def show(title, chunks):
    print(title)
    for number, chunk in enumerate(chunks, start=1):
        print(f"  chunk {number}: [{chunk}]")
    if has_full_answer(chunks):
        print("  Result: one chunk has the full answer. ✓")
    else:
        print("  Result: 'chhutti' and '18 din' are in different chunks. Matlab toot gaya. ✗")
    print()


def main():
    # Pick the chunk size so the cut lands right before "18 din".
    size = TEXT.index("18 din")

    show(f"1) Fixed size {size}, no overlap:", chunk_text(TEXT, size, 0))
    show(f"2) Fixed size {size}, overlap {OVERLAP}:", chunk_text(TEXT, size, OVERLAP))
    show("3) Cut on sentences:", sentence_chunks(TEXT))


if __name__ == "__main__":
    main()
