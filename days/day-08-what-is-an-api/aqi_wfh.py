"""Day 8 bonus: Delhi AQI se WFH ka faisla (AQI ka WFH bot).

Same waiter as Day 8, new order: "hawa ki report".
The API answers with the current US AQI for Delhi, and one if decides:
aaj WFH ya office.

Run:  python aqi_wfh.py

Data: Open-Meteo Air Quality API (free for non-commercial use, no key),
built on CAMS (Copernicus) model data. Credit: "Air quality data by
Open-Meteo.com, CAMS".

Read this before you trust the number:
- This is a model estimate on a grid (about 45 km for India), not a
  ground station. CPCB (the official India AQI) measures at stations.
- It is the US AQI scale, not the India AQI scale. Same air, different
  number. On 9 Nov 2026 at 7 AM, the model said US AQI 177 while CPCB
  showed India AQI 368 for Delhi.
- So for a real decision, also check the official number (CPCB / SAMEER app).
- The 150 rule below is an example company rule (ex.), not a government
  rule and not health advice.
"""

import json
import urllib.parse
import urllib.request

# Delhi. Change these two numbers for your city.
LATITUDE = 28.61
LONGITUDE = 77.21

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "us_aqi,pm2_5",
    "timezone": "Asia/Kolkata",
}

# Example company rule (ex.): US AQI above 150 is "Unhealthy" on the US scale.
WFH_ABOVE = 150


def order_aqi():
    """Give the order to the waiter and return the 'current' part of the JSON."""
    try:
        import requests  # the waiter from Day 8
    except ImportError:
        requests = None

    if requests is not None:
        r = requests.get(URL, params=PARAMS, timeout=10)
        r.raise_for_status()  # 200 = order mil gaya; the data is in r.json()
        return r.json()["current"]

    # No requests installed: Python's built-in urllib does the same job.
    full_url = URL + "?" + urllib.parse.urlencode(PARAMS)
    with urllib.request.urlopen(full_url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))["current"]


def decide(aqi):
    """The whole 'bot': one if."""
    if aqi > WFH_ABOVE:
        return "Aaj WFH"
    return "Office aao"


def main():
    cur = order_aqi()
    aqi = cur["us_aqi"]
    print("Time:", cur["time"])
    print("US AQI (model):", aqi)
    print("PM2.5:", cur["pm2_5"], "µg/m³")
    print("Faisla:", decide(aqi), f"(rule: US AQI > {WFH_ABOVE}, ex.)")
    print("Official India AQI ke liye CPCB / SAMEER app bhi dekho.")


if __name__ == "__main__":
    main()
