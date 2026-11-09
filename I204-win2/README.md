# I204-win2: 24 h full-load crash test on win2 after the BIOS update (BIOS 3.40, microcode 0x122)

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, ASRock Z890I Nova WiFi).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/204

Watchers copied from I177-win2/ unchanged (`crash_watch.py`, `sensor_log.py`, `sensors.py`, `coretemp.py`), alert-only: they
kill nothing and change no setting. Contents are added as the task proceeds (firmware record, crash records, sensor log, rounds).
