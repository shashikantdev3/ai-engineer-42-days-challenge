"""Day 16 homework, part 1: 10 questions a new joinee asks.

Replace the sample questions below with your own.
Run: python questions.py
"""

# Sample questions. Change them to the ones a real new joinee would ask.
QUESTIONS = [
    "How many paid leave days do I get in a year?",
    "How many sick leave days do I get?",
    "What are the office working hours?",
    "Can I work from home?",
    "When do I get my laptop?",
    "What do I do if I lose my ID card?",
    "How long is the probation period?",
    "How do I claim travel reimbursement?",
    "What is the notice period?",
    "Does the canteen serve free biryani on Fridays?",
]


def main():
    print("New joinee ke sawaal:\n")
    for number, question in enumerate(QUESTIONS, start=1):
        print(f"{number:2}. {question}")

    count = len(QUESTIONS)
    print()
    if count < 10:
        print(f"Abhi {count} sawaal hain. 10 tak likho.")
    else:
        print(f"{count} sawaal ready. Ab inhe rag_offline.py mein try karo.")


if __name__ == "__main__":
    main()
