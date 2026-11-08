#!/usr/bin/env python3
"""LOG ONLY, kills nothing. Every 300 s appends one line of CPU clock, load and package power (sensors.py) to
sensor_log.txt: the baseline against which each crash reading (crash_temps.txt) is set. The CPU temperature is n/a on this
machine (no built-in source, issue #177). Exits when the file STOP exists beside this script.

    python sensor_log.py [INTERVAL_S]"""
import datetime as dt, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sensors


def main():
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 300
    path = os.path.join(HERE, "sensor_log.txt")
    while not os.path.exists(os.path.join(HERE, "STOP")):
        t0 = time.time()
        try:
            line = sensors.fmt(sensors.read())
        except Exception as e:  # a failed reading is logged, the logger goes on
            line = f"reading failed: {e!r}"
        with open(path, "a") as f:
            f.write(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ") + "  " + line + "\n")
        time.sleep(max(1.0, interval - (time.time() - t0)))


if __name__ == "__main__":
    sys.exit(main())
