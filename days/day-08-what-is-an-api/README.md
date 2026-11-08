# Day 8 · API matlab waiter

**Week 2 · Project 1: Ticket Summarizer** · [← Day 7](../day-07-files-and-json) · [Day 9 →](../day-09-first-llm-api-call) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Aaj raat har ghante Lucknow ka mausam dekho. Barish hui toh truck roko!"*

Poori raat F5 dabaoge? Nahi. Python khud mausam poochhega, aur tum so jaoge.

## The idea: the restaurant waiter

In a restaurant you never walk into the kitchen. You give your order to the waiter, and the waiter brings the food. An API works the same way.

| In the restaurant | In code | What it means |
|---|---|---|
| **Waiter** | API | The middle person. Takes your order, brings back the answer. |
| **You (the customer)** | Your program | Your Python file places the order. |
| **Kitchen** | Server | The computer that has the data. You never go inside. |
| **Order ki parchi** | URL | Exactly what you want: which city, which values. |
| **Khaana** | JSON | The answer comes back as JSON (the same JSON from Day 7). |

## The code from the reel

This is the code Dev sir shows, line by line:

```python
import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=26.85&longitude=80.95&current=temperature_2m,rain"
r = requests.get(url)
c = r.json()["current"]
print(c["temperature_2m"])
```

1. `import requests`: bring in the waiter.
2. `requests.get(url)`: give the order (the parchi).
3. `r.json()["current"]`: open the plate and take the current weather.
4. `print(...)`: eat. You see the temperature.

## The trap: 200 is not the khaana

Every beginner does this once:

```python
print(r)
```

You get `<Response [200]>`, not the weather. **200 only means "order mil gaya"**: the server got your order and answered fine. The actual data is inside. To get it, use `r.json()`.

| You write | You see |
|---|---|
| `print(r)` | `<Response [200]>` (just the receipt) |
| `print(r.json())` | the full JSON with the weather |

## Aaj ka kaam (about 30 minutes)

1. **Install requests.** Open a terminal and run:
   ```
   python -m pip install requests
   ```
   (Mac / Linux: use `python3`.) No luck? Don't worry: `mausam.py` also works without it, using Python's built-in `urllib`.
2. **Open the URL in your browser** first. Paste this and look at the JSON:
   ```
   https://api.open-meteo.com/v1/forecast?latitude=26.85&longitude=80.95&current=temperature_2m,rain
   ```
   Find `"current"`, then `"temperature_2m"` and `"rain"` inside it. That is the khaana.
3. **Run [mausam.py](mausam.py):**
   ```
   python mausam.py
   ```
   It prints the status code, the temperature and the rain for Lucknow, and tells you if the truck should stop.
4. **Your city.** Search "your city latitude longitude", then change `LATITUDE` and `LONGITUDE` at the top of `mausam.py`. Run it again.
5. **Bonus:** print `rain` too, not only the temperature (it is already in the URL).
6. **Upload to GitHub.** Put `mausam.py` (with your city) in your repo. Bahi khata mein ek aur entry.

**No internet right now?** `mausam.py` falls back to [sample_response.json](sample_response.json), a saved example answer, so you can still practise reading the JSON. The numbers in it are an example (28.2 °C, rain 0.0, one morning in Lucknow), not live weather.

## Har ghante check: loop + time.sleep

Rahul's next question: *"Dev sir, aur har ghante check karna ho toh?"*

Use the Day 6 loop, and inside it `time.sleep(3600)`. 3600 seconds = 1 hour of aaram.

```python
for ghanta in range(1, 13):
    r = requests.get(url)
    time.sleep(3600)
```

[har_ghante.py](har_ghante.py) does this for real. For practice it waits only 5 seconds and checks 3 times, so you see it work quickly. When you are ready, change `WAIT_SECONDS = 3600` and `CHECKS = 12`. Stop it any time with **Ctrl + C**.

Please keep the short wait for practice. Asking a free public API every second is not polite: the waiter serves other customers too.

## Rules for today

- **Public API only.** Open-Meteo needs no API key for non-commercial use (checked on 8 Nov 2026). For commercial use, read their terms first.
- **No keys in code, ever.** Tomorrow's API needs a key, and keys never go into a file you upload to GitHub.
- **No company data.** Your own laptop, your own accounts, public data only.

## Files in this folder

| File | What it is |
|---|---|
| [mausam.py](mausam.py) | Asks Open-Meteo for one city's weather, shows the 200 trap, says "truck roko" if it rains |
| [har_ghante.py](har_ghante.py) | The loop + `time.sleep` version: checks the weather again and again |
| [sample_response.json](sample_response.json) | A saved example answer, for practice without internet |

**Mausam print ho gaya?** Comment **API** on the Day 8 reel. Tomorrow, Day 9: yahi waiter AI se baat karega. Your first LLM API call.
