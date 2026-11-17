"""GTA 6 countdown with timezones (Python bonus).

Run:  python gta6_countdown.py
Windows: if you see "No time zone found", run  pip install tzdata  once.

Release time: Rockstar says midnight local time on 19 Nov 2026 in every region.
India: 12:00 AM IST (PlayStation and Xbox India listings).
"""
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
NZ = ZoneInfo("Pacific/Auckland")

# 1. New Zealand's midnight, seen on an Indian clock
nz = datetime(2026, 11, 19, tzinfo=NZ)
print("New Zealand unlock in IST:", nz.astimezone(IST))      # 2026-11-18 16:30:00+05:30

# 2. India's midnight and the countdown
launch = datetime(2026, 11, 19, tzinfo=IST)
print("NZ, India se kitna pehle:", launch - nz)         # 7:30:00

baaki = launch - datetime.now(IST)
if baaki.total_seconds() > 0:
    ghante, rest = divmod(int(baaki.total_seconds()), 3600)
    print(f"GTA 6 mein baaki: {ghante} ghante {rest // 60} minute")
else:
    print("GTA 6 India mein khul chuka hai.")

# Trap: datetime(2026, 11, 19) without tzinfo uses whatever clock the machine has.
# A cloud server usually runs on UTC, so that countdown would be 5.5 hours off.
