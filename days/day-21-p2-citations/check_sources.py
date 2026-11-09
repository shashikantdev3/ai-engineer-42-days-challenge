"""Open a file at a page and read it yourself. Rasid dekho, khol ke check karo.

Run:
    python check_sources.py hr_policy 4
    python check_sources.py travel_policy 2
"""

import sys

from ask_with_source import load_chunks


def main():
    file_name = sys.argv[1] if len(sys.argv) > 1 else "hr_policy"
    file_name = file_name.removesuffix(".txt")
    try:
        page = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    except ValueError:
        print("Page ek number hona chahiye, jaise: python check_sources.py hr_policy 4")
        return

    for c in load_chunks():
        if c["meta"]["file"] == file_name and c["meta"]["page"] == page:
            print(f"--- {file_name}, page {page} ---")
            print(c["text"])
            print()
            print("Ab bot ka jawab is page se milao. Match nahi? To bharosa nahi.")
            return

    print(f"{file_name} page {page} nahi mila.")
    print("Check the file name (hr_policy, travel_policy) and the page number.")


if __name__ == "__main__":
    main()
