#!/usr/bin/env python3
"""memlog_mp.py PID: every 120 s one line (UTC time, load, free+inactive GB, resident GB and CPU seconds of this run's value_mp.py processes) until PID is gone.
A gap of more than 240 s between two lines is a sleep or a stall."""
import os
import re
import subprocess
import sys
import time

pid = int(sys.argv[1])
while True:
    try:
        os.kill(pid, 0)
    except OSError:
        break
    vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    page = int(re.search(r"page size of (\d+)", vm).group(1))
    free = sum(int(v) for _, v in re.findall(r"Pages (free|inactive|speculative):\s+(\d+)", vm)) * page / 2**30
    ps = subprocess.run(["ps", "-axo", "rss=,time=,command="], capture_output=True, text=True).stdout
    rows = [l.split(None, 2) for l in ps.splitlines() if "value_mp.py" in l and "pointv" in l]
    rss = sum(int(r[0]) for r in rows) / 2**20
    cpu = ", ".join(r[1] for r in rows)
    print(f"{time.strftime('%F %T', time.gmtime())} UTC load {os.getloadavg()[0]:.2f} free+inactive {free:.1f} GB value_mp rss {rss:.2f} GB, {len(rows)} procs, cpu {cpu}", flush=True)
    time.sleep(120)
