"""Day 16: the trap. Full handbook vs only the right pages.

Sending the whole handbook makes the prompt (and the bill) bigger,
and the AI can get lost in the middle. This counts the words you send.

Run: python trap_demo.py
"""

from rag_offline import load_pages, search

QUESTION = "How many paid leave days do I get in a year?"


def word_count(text):
    return len(text.split())


def main():
    pages = load_pages()

    full_handbook = "\n\n".join(pages)
    right_pages = "\n\n".join(search(QUESTION, pages))

    full_words = word_count(full_handbook)
    right_words = word_count(right_pages)

    print("Sawaal:", QUESTION)
    print()
    print(f"Poori handbook: {len(pages)} pages, {full_words} words")
    print(f"Sirf sahi pages: {right_words} words")

    if right_words:
        times = full_words / right_words
        print(f"\nPoori handbook is about {times:.1f}x more text to send.")
    print("\nThis sample is tiny. A real handbook can have 200 pages.")
    print("Rule: send only the right few pieces, not the whole book.")


if __name__ == "__main__":
    main()
