"""Day 19: reciprocal rank fusion (RRF), step by step.

Standard library only. Run:  python rrf_demo.py

Rule: score nahi, rank jodo. Every list gives a chunk 1 / (60 + rank).
Add them up. High in both lists = highest at the end.
"""

K = 60  # the common default

# Two sample ranked lists, best first (fictional chunk names).
keyword_list = ["E-404 guide", "Printer tip", "Issue photo tip"]
vector_list = ["Issue photo tip", "E-404 guide", "Printer tip"]


def main():
    totals = {}
    for list_name, ranked in [("keyword", keyword_list), ("vector", vector_list)]:
        print(f"{list_name} list:")
        for rank, name in enumerate(ranked, start=1):
            part = 1 / (K + rank)
            totals[name] = totals.get(name, 0.0) + part
            print(f"  rank {rank}: {name:<16} 1/({K} + {rank}) = {part:.5f}")
        print()

    print("Final (added up, best first):")
    for pos, name in enumerate(sorted(totals, key=totals.get, reverse=True), start=1):
        print(f"  #{pos} {name:<16} {totals[name]:.5f}")


if __name__ == "__main__":
    main()
