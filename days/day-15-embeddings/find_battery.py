"""Day 15 bonus: Rahul's battery search, by meaning, not by word.

Needs: pip install google-genai, and GEMINI_API_KEY set in your terminal.
Run:   python find_battery.py
Uses sample_complaints.txt (made-up complaints, not company data).
"""

from pathlib import Path

from embed_helpers import MODEL, cosine, embed

# 1. Read the sample complaints, one per line.
file = Path(__file__).with_name("sample_complaints.txt")
complaints = [line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]
print(f"{len(complaints)} sample complaints loaded.")

# 2. Embed the complaints AND the question with the SAME model (avoid the trap).
question = "battery ki problem"
vecs = embed(MODEL, complaints)
q = embed(MODEL, [question])[0]

# 3. The Day 6 loop: one score for every complaint.
scores = []
for c in vecs:
    scores.append(cosine(q, c))

# 4. Keep the score together with its complaint, then take the top 3.
#    (The reel showed sorted(scores)[-3:]. Pairing with the text tells you WHICH ones.)
ranked = sorted(zip(scores, complaints), reverse=True)
top = ranked[:3]

print(f"\nQuestion: '{question}'")
print("Top 3 by meaning:")
missed = 0
for score, text in top:
    has_word = "battery" in text.lower()
    if not has_word:
        missed += 1
    note = "" if has_word else "   <- no 'battery' word, Ctrl F would miss this"
    print(f"{score:.2f}  {text}{note}")

print(f"\nCtrl F for 'battery' would have missed {missed} of these 3.")
