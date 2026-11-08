"""Day 9 bonus: many descriptions with the Day 6 loop.

Run:  python loop_items.py

PRACTICE = True  -> a fake chef answers. Standard library only, no key, no internet.
PRACTICE = False -> Gemini answers for real. Needs: pip install -U google-genai
                    and your key in GEMINI_API_KEY.

time.sleep(6) is an example pause to stay inside free tier limits.
It is not an official number. If you see "too many requests", make it longer.
"""

import time

PRACTICE = True   # change to False for real Gemini calls

# Sample kirana items. For 100 items the loop is exactly the same.
items = [
    "Basmati chawal 5 kg",
    "Toor dal 1 kg",
    "Sarson tel 1 litre",
    "Chai patti 500 g",
    "Haldi powder 200 g",
]


def likho(item):
    """Return a 1 line description for one item."""
    if PRACTICE:
        # Fake chef: same style answer, so you can test the loop first.
        return f"{item}: fresh, saaf aur ghar ke liye perfect. (practice answer)"

    # Real chef. Imported here so practice mode needs no extra library.
    from google import genai

    client = genai.Client()   # key comes from GEMINI_API_KEY
    r = client.interactions.create(
        model="gemini-3.8-flash",   # model names change: check the docs
        input=f"{item}: write a 1 line product description in simple Hinglish.",
    )
    return r.output_text


if __name__ == "__main__":
    pause = 0.5 if PRACTICE else 6   # example pauses
    for number, item in enumerate(items, start=1):
        print(f"Item {number}: {likho(item)}")
        if number < len(items):
            time.sleep(pause)
    print(f"\n{len(items)}/{len(items)} descriptions ready.")
