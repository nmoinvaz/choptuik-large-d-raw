#!/usr/bin/env python3
"""memlog1080.py PID: every 60 s one line (UTC time, load, free+inactive memory in GB, resident memory of this run's hier_nb.py processes in GB) until PID is gone.
A gap of more than 120 s between two lines is a sleep or a stall; the awake time of the run is its wall time minus those gaps."""
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
    pg = {k: int(v) for k, v in re.findall(r"Pages (free|inactive|speculative):\s+(\d+)", vm)}
    free = sum(pg.values()) * page / 2**30
    ps = subprocess.run(["ps", "-axo", "rss=,command="], capture_output=True, text=True).stdout
    rss = sum(int(l.split(None, 1)[0]) for l in ps.splitlines() if "hier_nb.py" in l) / 2**20
    print(f"{time.strftime('%F %T', time.gmtime())} UTC load {os.getloadavg()[0]:.2f} free+inactive {free:.1f} GB hier_nb rss {rss:.2f} GB", flush=True)
    time.sleep(60)
