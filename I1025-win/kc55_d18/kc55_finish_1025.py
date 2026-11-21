#!/usr/bin/env python3
"""#1025 winb, the k_c 55 test at D 18: the finisher that replaces the stopped driver's remaining parts (see the README, "Change: alert-only memory watcher"). It does NOT touch the
scan except by the 8 h time cap of the order. It waits for the scan's launcher pid (17520) to end; at 22:02:36 UTC + 28800 s it kills that exact pid (taskkill /PID <pid> /T /F) if the scan
is still running. It starts the read-only sampler for that pid, then, when the scan has ended with all 16 points, filters the log, runs d18f_read.py window and read_kc55_1025.py, as the
driver would have. usage: kc55_finish_1025.py SCAN_PID"""
import datetime, os, re, subprocess, sys, time

OUT = "C:/Users/nathan/Source/kc55_1025/I1025-win/kc55_d18"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT_D = "C:/Users/nathan/Source/choptuik-i1025d"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
READER = "C:/Users/nathan/Source/kc55_1025/raw/I1025-mac/d18/d18f_read.py"
SCAN, LOG = OUT + "/scan_kc55_D18_1025.jsonl", OUT + "/kc55_w.log"
pid = int(sys.argv[1])
CAP_END = datetime.datetime(2026, 11, 22, 6, 2, 36, tzinfo=datetime.timezone.utc)      # the scan started 2026-11-21 22:02:36 UTC; 8 h cap


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def alive(p):
    r = subprocess.run(["powershell", "-NoProfile", "-Command", f"if (Get-Process -Id {p} -ErrorAction SilentlyContinue) {{ 'yes' }}"], capture_output=True, text=True)
    return bool(r.stdout.strip())


say(f"kc55_finish_1025.py: waiting for scan pid {pid}; the 8 h time cap ends {CAP_END:%Y-%m-%d %H:%M:%S} UTC (kill by exact pid then)")
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", HERE + "/sample_driver3_1025.ps1", "-Drv", str(pid), "-Out", OUT + "/rows/kc55_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
capped = False
while alive(pid):
    if datetime.datetime.now(datetime.timezone.utc) > CAP_END:
        r = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True)
        say(f"CAP 28800 s: killed pid {pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
        capped = True
        break
    time.sleep(15)
time.sleep(5)
n = sum(1 for l in open(SCAN) if l.strip()) if os.path.exists(SCAN) else 0
say(f"the scan has ended ({'killed at the cap' if capped else 'by itself'}); {n} of 16 points in {SCAN}")
with open(OUT + "/scan_kc55_D18.log", "w") as g:
    for ln in open(OUT + "/rows/scan_kc55_D18_raw.log", errors="replace"):
        if not re.search(r"Warning|^  [a-z]+ = ", ln):
            g.write(ln)
if n == 16 and not capped:
    renv = dict(os.environ, PYTHONPATH=WT_D + "/solver/matter", PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
    r = subprocess.run([PY, READER, "window", "18.0", "1.70", "1.85", SCAN], cwd=WT_D + "/solver/matter", env=renv, capture_output=True, text=True)
    txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return "))
    open(OUT + "/read_kc55_D18.log", "w").write(txt + "\n")
    r2 = subprocess.run([PY, HERE + "/read_kc55_1025.py", OUT + "/read_kc55_D18.log"], capture_output=True, text=True)
    open(OUT + "/read_kc55_1025.log", "w").write(r2.stdout + r2.stderr)
    for ln in (txt + "\n" + r2.stdout).splitlines():
        say(ln)
else:
    say("the scan did not deliver all 16 points: no reading; the points so far are in the scan file")
time.sleep(70)          # the sampler's last line (it ends by itself when the scan pid is gone)
samp.kill()
say("kc55_finish_1025.py done")
