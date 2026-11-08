"""Day 8: check the weather again and again with a loop.

Day 6 loop + time.sleep = Python checks, you sleep.

Run:  python har_ghante.py
Stop any time with Ctrl + C.
"""

import time

from mausam import URL, get_mausam

# Practice values: 3 checks, 5 seconds apart, so you see it work fast.
# For the real night shift: WAIT_SECONDS = 3600 (1 hour) and CHECKS = 12.
WAIT_SECONDS = 5
CHECKS = 3


def main():
    for ghanta in range(1, CHECKS + 1):
        data = get_mausam(URL)
        c = data["current"]
        print(f"Check {ghanta}: {c['temperature_2m']} °C, rain {c['rain']} mm")

        if c["rain"] > 0:
            print("Barish! Truck roko.")

        if ghanta < CHECKS:  # no need to wait after the last check
            print(f"Waiting {WAIT_SECONDS} seconds... aaram karo.")
            time.sleep(WAIT_SECONDS)

    print("All checks done. Good night, Rahul.")


if __name__ == "__main__":
    main()
