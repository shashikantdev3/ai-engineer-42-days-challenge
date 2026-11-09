"""Day 15 homework: embed 5 sentences and find the closest pair.

Needs: pip install google-genai, and GEMINI_API_KEY set in your terminal.
Run:   python closest_pair.py
Sample sentences only. Never use real company data.
"""

from itertools import combinations

from embed_helpers import MODEL, cosine, embed

# Change these 5 to your own sentences after the first run.
sentences = [
    "Mera phone ka charge nahi tikta",
    "Battery bahut jaldi khatam ho jaati hai",
    "Printer mein paper phas gaya hai",
    "Office ka WiFi baar baar band ho jaata hai",
    "Laptop bahut garam ho raha hai",
]

print(f"Embedding {len(sentences)} sentences with {MODEL} ...")
vectors = embed(MODEL, sentences)
print(f"Each address has {len(vectors[0])} numbers.\n")

# Score every pair: 5 sentences make 10 pairs.
pairs = []
for i, j in combinations(range(len(sentences)), 2):
    score = cosine(vectors[i], vectors[j])
    pairs.append((score, i, j))

print("All pairs, closest first:")
for score, i, j in sorted(pairs, reverse=True):
    print(f"{score:.2f}  '{sentences[i]}'  <->  '{sentences[j]}'")

best_score, i, j = max(pairs)
print("\nClosest pair:")
print(f"  '{sentences[i]}'")
print(f"  '{sentences[j]}'")
print(f"  score: {best_score:.2f}")
print("\nYour numbers will not match the reel. Look at the ORDER, not the exact score.")
