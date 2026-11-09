"""Day 18 trap: memory forgets, a file remembers.

memory list   = like chromadb.Client()            (dimaag: program band, sab gayab)
diary.json    = like chromadb.PersistentClient()  (diary: saved in a folder)

Run it 2 or 3 times and compare the counts.
Start fresh:  python memory_vs_diary.py --reset
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DIARY_FILE = Path(__file__).parent / "diary.json"


def main():
    if "--reset" in sys.argv:
        if DIARY_FILE.exists():
            DIARY_FILE.unlink()
        print("Diary deleted. Fresh start.")
        return

    note = f"chunk saved at {datetime.now():%H:%M:%S}"

    # Memory: a new empty list every time the program starts.
    memory = []
    memory.append(note)

    # Diary: read what was saved before, add the new note, save again.
    if DIARY_FILE.exists():
        diary = json.loads(DIARY_FILE.read_text(encoding="utf-8"))
    else:
        diary = []
    diary.append(note)
    DIARY_FILE.write_text(json.dumps(diary, indent=2), encoding="utf-8")

    print(f"Memory (like Client()):           {len(memory)} item")
    print(f"Diary  (like PersistentClient()): {len(diary)} items")
    print("\nRun me again. Memory goes back to 1. The diary keeps growing.")


if __name__ == "__main__":
    main()
