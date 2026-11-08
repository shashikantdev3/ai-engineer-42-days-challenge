"""Day 8: ask an API for the weather (mausam).

The API is the waiter. The URL is the order slip (parchi).
The server is the kitchen. The JSON is the food (khaana).

Run:  python mausam.py
Works with the requests library if you installed it,
and with Python's built-in urllib if you did not.
"""

import json
import urllib.request
from pathlib import Path

# Your city. Lucknow by default. Change these two numbers for your city.
LATITUDE = 26.85
LONGITUDE = 80.95

# The order slip: which city, and which values we want.
URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=temperature_2m,rain"
)

# A saved example answer, used only when there is no internet.
SAMPLE_FILE = Path(__file__).with_name("sample_response.json")


def order_mausam(url):
    """Give the order to the waiter and return the JSON as a Python dict."""
    try:
        import requests  # the waiter from the reel
    except ImportError:
        requests = None

    if requests is not None:
        r = requests.get(url, timeout=10)
        # The trap: this prints only the receipt, not the weather.
        print("print(r) shows:", r)
        r.raise_for_status()  # stop here if the status is not OK
        return r.json()  # the real food

    # No requests installed: use the built-in urllib instead.
    with urllib.request.urlopen(url, timeout=10) as response:
        print("Status code:", response.status, "(200 = order mil gaya)")
        return json.loads(response.read().decode("utf-8"))


def get_mausam(url):
    """Try the live API. If the internet fails, use the saved sample."""
    try:
        return order_mausam(url)
    except OSError as error:
        print("Could not reach the API:", error)
        print("Using the saved example from sample_response.json instead.")
        return json.loads(SAMPLE_FILE.read_text(encoding="utf-8"))


def main():
    data = get_mausam(URL)
    c = data["current"]  # open the plate
    temperature = c["temperature_2m"]
    rain = c["rain"]

    print("Temperature:", temperature, "°C")
    print("Rain:", rain, "mm")

    if rain > 0:
        print("Barish ho rahi hai! Truck roko.")
    else:
        print("Barish nahi. Truck chalne do.")


if __name__ == "__main__":
    main()
