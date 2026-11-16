"""Outage-proof API call: timeout + retry + Plan B (Day 8 bonus).

Run:          python outage_retry.py
Fake outage:  python outage_retry.py 0.001   (a tiny timeout makes every try fail)

Open-Meteo needs no API key. Weather data by Open-Meteo.com
"""
import sys
import time

import requests

URL = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=28.61&longitude=77.21"
       "&current=temperature_2m")
TIMEOUT = float(sys.argv[1]) if len(sys.argv) > 1 else 5   # seconds; never wait forever
KOSHISH = 3   # example value, not a standard
WAIT = 2      # seconds between tries, example value


def call():
    r = requests.get(URL, timeout=TIMEOUT)
    r.raise_for_status()          # 500 / 503 also count as a fail
    return r.json()


for k in range(KOSHISH):
    try:
        print("Delhi abhi:", call()["current"]["temperature_2m"], "°C")
        break
    except requests.RequestException as e:
        print(f"Koshish {k + 1}: fail ({type(e).__name__})")
        time.sleep(WAIT)
else:   # runs only if the loop never hit break, i.e. all tries failed
    print("Plan B: client ko call karo.")
