## 🌬️ Customizing Wind Labels for Your Break

#!/usr/bin/env python3
import time
from pyworxcloud import WorxCloud

EMAIL    = "<EMAIL>"
PASSWORD = "<PASSWORD>"
SERIAL   = "<SERIAL NUMBER>"
POLL     = 30  # seconds

cloud = WorxCloud(EMAIL, PASSWORD, "worx", verify_ssl=False)
if not cloud.authenticate():
    print("❌ Login failed")
    exit(1)
cloud.connect()

print(f"▶️  Watching mower {SERIAL} – polling every {POLL}s. Ctrl-C to stop.")

wire_missing = False
prev_dist    = None  # store last total distance reading

def watch_and_restart():
    global wire_missing, prev_dist

    try:
        state = cloud.get_mower(SERIAL)
    except Exception as e:
        print(f"[{time.ctime()}] ⚠️  Fetch failed: {e}")
        return

    payload = state.get("last_status", {}).get("payload", {})
    dat     = payload.get("dat", {})
    bt      = dat.get("bt", {})
    stats   = dat.get("st", {})     # {'b':…, 'd': total_distance, 'wt':…, 'bl':…}

    batt_pct = bt.get("p", "?")
    cur_dist = stats.get("d", 0)
    err_id   = state.get("error", {}).get("id", 0)
    wire_le  = dat.get("le", None)  # wire-error code also shows up here

    # 1) Boundary-wire missing → send it home (once)
    if err_id == 3 or wire_le == 3:
        if not wire_missing:
            print(f"[{time.ctime()}] ⚠️  Wire-missing; sending it home…")
            cloud.home(SERIAL)
            wire_missing = True
        # don't change prev_dist here; mower is traveling home

    # 2) Wire restored & mower idle → restart mowing
    elif wire_missing and prev_dist is not None and cur_dist == prev_dist:
        print(f"[{time.ctime()}] 👍  Wire restored; starting mower…")
        cloud.start(SERIAL)
        wire_missing = False

    # 3) Battery-temp error → reboot baseboard
    elif err_id == 17 or wire_le == 17:
        print(f"[{time.ctime()}] ⚠️  Battery-temp error; restarting baseboard…")
        cloud.restart(SERIAL)

    else:
        # detect mowing by distance increase
        if prev_dist is not None and cur_dist > prev_dist:
            status = "mowing"
        else:
            status = "idle"
        print(f"[{time.ctime()}] ✅  Battery: {batt_pct}% | Status: {status}")

    # update for next round
    prev_dist = cur_dist

try:
    while True:
        watch_and_restart()
        time.sleep(POLL)
finally:
    cloud.disconnect()