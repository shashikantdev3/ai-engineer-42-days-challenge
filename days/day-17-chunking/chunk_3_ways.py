"""Day 17: cut one text 3 ways and compare.

Run with the sample handbook:
    python chunk_3_ways.py
Run with your own text (copied from a public PDF):
    python chunk_3_ways.py my_pdf.txt

Standard library only. Python 3.10+.
"""

import re
import sys
from pathlib import Path

# The 3 chunk sizes from today's homework (in characters).
SIZES = [200, 500, 1000]

# Overlap as a percent of the size. 10% of 500 is 50, same as the reel.
OVERLAP_PERCENT = 10

# Change this to a question your own text can answer.
QUESTION = "How many days of paid chhutti does an employee get in a year?"

# Very common words that do not help us find the right chunk.
STOP_WORDS = {
    "a", "an", "the", "of", "in", "on", "to", "is", "are", "and", "or",
    "how", "many", "what", "does", "do", "an", "for", "it", "this", "that",
    "be", "by", "with", "at", "from", "get", "gets",
}


def load_text(path):
    """Read the file and drop the '=== PAGE N ===' marker lines."""
    raw = Path(path).read_text(encoding="utf-8")
    lines = [line for line in raw.splitlines() if not line.startswith("=== PAGE")]
    return "\n".join(lines).strip()


def chunk_text(text, size, overlap):
    """Same idea as the reel: slice the text, move forward by step."""
    step = size - overlap
    chunks = []
    for i in range(0, len(text), step):
        chunks.append(text[i:i + size])
    return chunks


def important_words(sentence):
    """Lowercase words, without the common stop words."""
    return set(re.findall(r"[a-z0-9]+", sentence.lower())) - STOP_WORDS


def score(chunk, question):
    """How many important question words appear in this chunk.
    A simple stand-in for search. Real search by meaning comes on Day 18."""
    return len(important_words(chunk) & important_words(question))


def cut_mid_sentence(chunk):
    """True if the chunk does not end at the end of a sentence."""
    return not chunk.rstrip().endswith((".", "!", "?"))


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path(__file__).parent / "sample_handbook.txt"

    if not path.exists():
        print(f"File not found: {path}")
        return

    text = load_text(path)
    print(f"File: {path.name}  ({len(text)} characters)")
    print(f"Question: {QUESTION}")

    for size in SIZES:
        overlap = size * OVERLAP_PERCENT // 100
        chunks = chunk_text(text, size, overlap)

        broken = sum(1 for chunk in chunks if cut_mid_sentence(chunk))
        best_index = max(range(len(chunks)), key=lambda n: score(chunks[n], QUESTION))
        best_chunk = chunks[best_index]

        print()
        print("=" * 60)
        print(f"Size {size}, overlap {overlap}: {len(chunks)} chunks")
        print(f"Chunks cut mid-sentence: {broken} of {len(chunks)}")
        print(f"Best match: chunk {best_index + 1} (score {score(best_chunk, QUESTION)})")
        print("-" * 60)
        print(best_chunk.strip())

    print()
    print("Now decide: which size gave the cleanest answer for your question?")


if __name__ == "__main__":
    main()
