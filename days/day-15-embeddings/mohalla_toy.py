"""Day 15 offline demo: the mohalla with toy addresses.

No internet, no key, standard library only.
These addresses are HAND-MADE with 3 numbers each, just to show the idea:
    [battery / power, printer / paper, network / wifi]
Real embeddings come from a model and are much longer (3072 numbers by default).
"""

from itertools import combinations

from embed_helpers import cosine

# Toy "model A": each sentence gets a hand-made address.
model_a = {
    "Battery jaldi khatam ho jaati hai": [0.90, 0.10, 0.10],
    "Charge nahi tikta": [0.85, 0.05, 0.20],
    "Printer mein paper jam hai": [0.10, 0.95, 0.05],
    "Printer print nahi kar raha": [0.05, 0.90, 0.10],
    "WiFi baar baar disconnect hota hai": [0.10, 0.05, 0.95],
}

print("=== 1. Every pair, with its score ===")
pairs = []
for s1, s2 in combinations(model_a, 2):
    score = cosine(model_a[s1], model_a[s2])
    pairs.append((score, s1, s2))

for score, s1, s2 in sorted(pairs, reverse=True):
    print(f"{score:.2f}  '{s1}'  <->  '{s2}'")

best = max(pairs)
print(f"\nClosest pair: '{best[1]}' and '{best[2]}' ({best[0]:.2f})")

print("\n=== 2. Top 3 for the question 'battery problem' ===")
question = [0.95, 0.05, 0.10]  # toy address of the question, same toy model
scores = []
for sentence, address in model_a.items():  # the Day 6 loop
    scores.append((cosine(question, address), sentence))

top = sorted(scores, reverse=True)[:3]
for score, sentence in top:
    has_word = "battery" in sentence.lower()
    note = "" if has_word else "   <- Ctrl F would miss this!"
    print(f"{score:.2f}  {sentence}{note}")

print("\n=== 3. The trap: two models, two maps ===")
# Toy "model B" draws its map differently: the same meaning sits on
# different numbers. Here the columns are in another order.
model_b_battery = [0.10, 0.10, 0.90]  # 'Battery jaldi khatam' in model B

charge_in_a = model_a["Charge nahi tikta"]
battery_in_a = model_a["Battery jaldi khatam ho jaati hai"]

print(f"Same model (A and A): {cosine(charge_in_a, battery_in_a):.2f}  ✓ close, as it should be")
print(f"Mixed models (A and B): {cosine(charge_in_a, model_b_battery):.2f}  ✗ looks far, but the meaning is the same")
print("\nRule: complaints and question, always the same model.")
