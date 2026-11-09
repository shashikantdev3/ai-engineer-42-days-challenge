"""Day 21 trap: never let the AI write the source.

Run:
    python trap_demo.py

We pretend the AI wrote its own source inside the answer ("page 7").
Then we check it against the metadata our code saved at ingest.
"""

import re

from ask_with_source import load_chunks, query

q = "WFH kitne din milte hain?"
chunks = load_chunks()
res = query(chunks, q, n_results=3)
src = res["metadatas"][0]  # the real rasid, from metadata

# Pretend this text came from the AI. It made up the page number.
model_text = "WFH 2 din milte hain. (source: hr_policy page 7)"

print("AI ne likha:     ", model_text)
print("Metadata se aaya:", ", ".join(f"{s['file']} p.{s['page']}" for s in src))
print()

match = re.search(r"(\w+) page (\d+)", model_text)
if not match:
    print("AI ne koi source nahi diya. Rasid nahi, to bharosa nahi.")
else:
    claimed_file = match.group(1)
    claimed_page = int(match.group(2))
    real = {(s["file"], s["page"]) for s in src}

    # Does that page even exist in the file?
    pages_in_file = {c["meta"]["page"] for c in chunks if c["meta"]["file"] == claimed_file}

    if (claimed_file, claimed_page) in real:
        print("OK: AI ka source metadata se match karta hai.")
    else:
        print(f"TRAP PAKDA: AI bola {claimed_file} page {claimed_page}, "
              "lekin metadata mein ye nahi hai.")
        if claimed_page not in pages_in_file:
            print(f"Aur {claimed_file} mein page {claimed_page} hai hi nahi. AI ne bana diya.")
        print("Rule: source hamesha code se print karo, metadata se.")
