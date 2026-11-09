"""Day 19: the trap. "Chhutti" and "chhutti" are different words for
keyword search. Fix: lower() on BOTH sides, chunks and question.

Standard library only. Run:  python trap_lower.py
"""

chunk = "Chhutti policy: saal mein 18 chhutti, manager approval zaroori."
question = "Chhutti kitni milti?"


def words(text):
    # Split into words and strip punctuation like : , ?
    return {w.strip(".,?!:;") for w in text.split()}


def check(title, chunk_words, question_words):
    common = chunk_words & question_words
    print(title)
    print(f"  matching words: {sorted(common) if common else 'none'}")
    print()


def main():
    # 1. No lower() at all: works only by luck (same capital letter).
    check("1. No lower():", words(chunk), words(question))

    # 2. The user types in small letters. Now the capital "Chhutti" is missed
    #    and only the second, small "chhutti" in the chunk matches.
    q_small = "chhutti policy kya?"
    check("2. User types small, no lower():", words(chunk), words(q_small))

    # 3. lower() on one side only: the trap is still there.
    q_caps = "CHHUTTI POLICY kya?"
    check("3. lower() on chunk only:", words(chunk.lower()), words(q_caps))

    # 4. The rule: lower() on both sides.
    check("4. lower() on both sides:", words(chunk.lower()), words(q_caps.lower()))


if __name__ == "__main__":
    main()
