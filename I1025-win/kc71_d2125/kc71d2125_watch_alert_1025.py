#!/usr/bin/env python3
"""#1025 winb (successor session), the k_c 71 lambda_1 scan at D 21.25: an ALERT-ONLY memory watcher (Nathan's standing rule: no guard that kills processes for memory). Polls the laptop's free physical
memory (FreePhysicalMemory, the figure the samplers log) every 15 s; below 1 GB it sends the coordinator t5 ONE hc alert, repeated at most every 30 min while the memory stays below
1 GB. It kills nothing and touches nothing. It ends when the watched driver pid is gone.
usage: kc71d2125_watch_alert_1025.py DRIVER_PID LABEL [--dry] [--threshold GB] [--max-polls N]     (--dry prints the alert instead of sending it; used for the test)"""
import datetime, subprocess, sys, time

HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
pid, label = int(sys.argv[1]), sys.argv[2]
dry = "--dry" in sys.argv
thr = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 1.0
maxp = int(sys.argv[sys.argv.index("--max-polls") + 1]) if "--max-polls" in sys.argv else None
LOG = f"C:/Users/nathan/Source/kc71d2125_1025/I1025-win/kc71_d2125/rows/{label}_memwatch{'_dry' if dry else ''}.log"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def ps(cmd):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True).stdout.strip()


say(f"alert-only memory watcher ({label}) started for driver pid {pid}: free physical memory every 15 s, one hc alert below {thr} GB, repeated at most every 30 min; it kills nothing")
last_alert, lo, n, polls = 0.0, 1e9, 0, 0
while True:
    if not ps(f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 'yes' }}"):
        say(f"driver pid {pid} is gone; watcher ends; minimum free memory seen {lo:.2f} GB; {n} alert(s) sent")
        break
    try:
        f = float(ps("[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB, 3)"))
    except ValueError:
        f = None
    if f is not None:
        lo = min(lo, f)
        if f < thr and time.time() - last_alert > 1800:
            msg = (f"winb ALERT {datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC: free physical memory {f:.2f} GB, below {thr:g} GB. The k_c 71 D 21.25 {label} stage (driver pid {pid}) is "
                   f"still running, untouched; this watcher is alert-only and kills nothing. Next alert in 30 min at the earliest.")
            if dry:
                say(f"DRY: would send hc: {msg}")
            else:
                r = subprocess.run([HC, "send", COORD, msg], capture_output=True, text=True)
                say(f"ALERT sent (free {f:.2f} GB): {r.stdout.strip()[:120]}")
            last_alert, n = time.time(), n + 1
    polls += 1
    if maxp is not None and polls >= maxp:
        say(f"stopping after {polls} polls (test); minimum free memory seen {lo:.2f} GB; {n} alert(s)")
        break
    time.sleep(15)
