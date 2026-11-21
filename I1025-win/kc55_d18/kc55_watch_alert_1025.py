#!/usr/bin/env python3
"""#1025 winb, the k_c 55 test at D 18: an ALERT-ONLY memory watcher (the coordinator's correction, 2026-11-21 about 22:04 UTC: Nathan's standing rule is no guard that kills processes
for memory; alert-only watchers are fine). Polls the laptop's free physical memory (FreePhysicalMemory, the figure my samplers log) every 15 s; below 1 GB it sends the coordinator
ONE hc alert, and repeats it at most every 30 min while the memory stays below 1 GB. It kills nothing and touches nothing. It ends when the scan's launcher pid is gone.
usage: kc55_watch_alert_1025.py SCAN_PID [--dry] [--threshold GB] [--max-polls N]     (--dry prints the alert instead of sending it; used for the test)"""
import datetime, subprocess, sys, time

HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
LOG = "C:/Users/nathan/Source/kc55_1025/I1025-win/kc55_d18/rows/kc55_memwatch.log"
pid = int(sys.argv[1])
dry = "--dry" in sys.argv
thr = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 1.0
maxp = int(sys.argv[sys.argv.index("--max-polls") + 1]) if "--max-polls" in sys.argv else None
if dry:
    LOG = LOG.replace("kc55_memwatch.log", "kc55_memwatch_dry.log")


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def ps(cmd):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True).stdout.strip()


say(f"alert-only memory watcher started for scan pid {pid}: free physical memory every 15 s, one hc alert below {thr} GB, repeated at most every 30 min; it kills nothing")
last_alert, lo, n, polls = 0.0, 1e9, 0, 0
while True:
    if not ps(f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 'yes' }}"):
        say(f"scan pid {pid} is gone; watcher ends; minimum free memory seen {lo:.2f} GB; {n} alert(s) sent")
        break
    try:
        f = float(ps("[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB, 3)"))
    except ValueError:
        f = None
    if f is not None:
        lo = min(lo, f)
        if f < thr and time.time() - last_alert > 1800:
            msg = (f"winb ALERT {datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC: free physical memory {f:.2f} GB, below {thr:g} GB. The k_c 55 D 18 scan (pid {pid}) is still running, "
                   f"untouched; this watcher is alert-only and kills nothing. Next alert in 30 min at the earliest.")
            if dry:
                say(f"DRY: would send hc: {msg}")
            else:
                r = subprocess.run([HC, "send", "nathans-macbook-air-m5-3/t5", msg], capture_output=True, text=True)
                say(f"ALERT sent (free {f:.2f} GB): {r.stdout.strip()[:120]}")
            last_alert, n = time.time(), n + 1
    polls += 1
    if maxp is not None and polls >= maxp:
        say(f"stopping after {polls} polls (test); minimum free memory seen {lo:.2f} GB; {n} alert(s)")
        break
    time.sleep(15)
