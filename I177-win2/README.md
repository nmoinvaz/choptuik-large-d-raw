# I177-win2: Python 3.14 crash test on win2 (access violations 0xc0000005)

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, ASRock Z890I Nova WiFi).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/177

Runs beside #82 (I82-win2/) on the 3.12 venv; #82 is not touched. The crash test is #146's repeat-and-compare loop of the
amplitude copy `amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12` on a Python 3.14 venv, hashed with
`I140-win2/compare.py` against fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8 (#161).

Contents are added as the task proceeds (install record, `pip freeze`, rounds, crash records).

## Final state (2026-11-08 23:00 UTC)

The loop ran in two windows, 16:50:36 to 19:40:21 UTC (rounds 1 to 17) and 21:15:12 to 22:53:34 UTC (rounds 19 to 29; the loop
was paused for #82's memory peak, and the round counter has no number 18). 28 rounds, 84 copies, all exit 0, all with
hash fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8; no ALERT file. 48141 s of copy wall time (13.37 h).
`STOP` (created 22:53:08 UTC, with #82's end) stopped the loop after round 29. No python 3.14 process crashed.

Records: `rounds.csv`, `driver.txt`, `round<k>/` (JSONs, logs, `exits.txt`, `compare.txt`), `crashes.txt` (every Application-log
crash of any process; 8 python.exe access violations since 11-07 18:37 UTC, all in 3.12 processes), `crash_temps.txt` (the reading
within a minute of each crash seen by `crash_watch.py`), `sensor_log.txt` (5-minute baseline with Core Temp from 17:39 UTC).
`crash_watch.py` and `sensor_log.py` keep running until the BIOS update.
