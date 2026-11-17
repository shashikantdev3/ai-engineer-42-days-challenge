"""Day 10 bonus: kal subah fog? (Fog alert bot)

Day 10 said: every AI call has a bill. So first ask: does this job even need AI?
An LLM does not know tomorrow's weather. A weather API does, for free: 0 tokens.
Same waiter as Day 8, new order: "kal subah ki visibility".

Run:  python fog_alert.py

Data: Open-Meteo Forecast API, hourly "visibility" in metres (free for
non-commercial use, no key). Credit: "Weather data by Open-Meteo.com" (CC BY 4.0).

Read this before you trust the number:
- It is a model forecast, not a reading from a station. Shallow fog can slip
  past it. On 11 Nov 2026 at 3:30 PM the model said 5,660 m for Delhi at 7 AM
  on 12 Nov, while IMD's Delhi forecast (issued 10 Nov, 8:40 PM) said
  "mist/shallow fog at most places in the morning hours".
- IMD is the official source. Fog means visibility under 1,000 m; IMD calls
  500 to 999 m shallow fog.
- "15 min pehle niklo" is an example personal rule (ex.), not advice.
"""

import datetime
import json
import urllib.parse
import urllib.request

# Delhi. Change these two numbers for your city.
LATITUDE = 28.61
LONGITUDE = 77.21

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "visibility",
    "timezone": "Asia/Kolkata",
    "forecast_days": 2,
}

FOG_BELOW = 1000                              # metres: under 1 km counts as fog
TRAVEL_HOURS = ("06", "07", "08", "09")       # your morning travel window (ex.)


def order_visibility():
    """Give the order to the waiter and return the 'hourly' part of the JSON."""
    try:
        import requests  # the waiter from Day 8
    except ImportError:
        requests = None

    if requests is not None:
        r = requests.get(URL, params=PARAMS, timeout=10)
        r.raise_for_status()  # 200 = order mil gaya; the data is in r.json()
        return r.json()["hourly"]

    # No requests installed: Python's built-in urllib does the same job.
    full_url = URL + "?" + urllib.parse.urlencode(PARAMS)
    with urllib.request.urlopen(full_url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))["hourly"]


def decide(vis):
    """The whole 'bot': one if."""
    if vis < FOG_BELOW:
        return "Fog ho sakta hai: 15 min pehle niklo (ex.)"
    return "Visibility theek: normal time pe niklo"


def main():
    hourly = order_visibility()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()

    lowest = None
    for t, vis in zip(hourly["time"], hourly["visibility"]):
        if t.startswith(tomorrow) and t[11:13] in TRAVEL_HOURS and vis is not None:
            print(t.replace("T", " "), "->", int(vis), "m")
            if lowest is None or vis < lowest:
                lowest = vis

    if lowest is None:
        print("Kal subah ka data nahi mila. Thodi der baad chalao.")
        return

    print("Kal subah sabse kam visibility (model):", int(lowest), "m")
    print("Faisla:", decide(lowest))
    print("Checked at:", datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"))
    print("Official forecast ke liye IMD (mausam.imd.gov.in) bhi dekho.")


if __name__ == "__main__":
    main()
