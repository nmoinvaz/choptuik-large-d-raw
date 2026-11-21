#!/usr/bin/env python3
"""#1025 winb, the D 18.125 scan (the coordinator's order of 2026-11-21 13:2x UTC and his "split" of about 13:34 UTC): xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob
e089207a, unchanged) on the leap state sol_l1kc63Wm1025_D18.125000.npy at lambda 1.70 to 1.95 at 0.01, with its noise test and the float64 sign, in TWO processes, 4 threads
each, BelowNormal, each with an 8 h cap (28800 s) by the exact pid of the process this driver started (taskkill /PID <pid> /T /F). The per-point seeds are unchanged (the
scanner's). Process A: lambda 1.82, then 1.70 to 1.81 (13 points); process B: lambda 1.82 again, then 1.83 to 1.95 (14 points). The repeated point 1.82 is first in both, so the
check "same sign and ln|det| to 1e-6" is available after the first point of each. After both: merge_d18mid_1025.py (the repeat check and the merged 26-point scan), then
read_d18mid_1025.py. Starts after the D 18.5 driver (d185_driver_1025.py) has ended (it has, at 13:32:24).
usage: d18mid_driver_1025.py [--selftest]      (--selftest: the cap and the sampler on two dummy children)"""
import datetime, os, re, subprocess, sys, time

OUT = "C:/Users/nathan/Source/d18mid_1025/I1025-win/d18mid"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT = "C:/Users/nathan/Source/choptuik-i1025-lowd"        # 505d8399: the P4 rows' solver code
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
RAW = "C:/Users/nathan/Source/d18mid_1025/raw"
SCANNER = RAW + "/I1025-mac/d18/d18_hybsign.py"
STATE = RAW + "/I1025-mac/d18/sol_l1kc63Wm1025_D18.125000.npy"
REC = RAW + "/I1025-mac/d18/l1kc63Wm1025.jsonl"
SCANA, SCANB, SCAN = OUT + "/d18mid_scanA_1025.jsonl", OUT + "/d18mid_scanB_1025.jsonl", OUT + "/d18mid_scan_1025.jsonl"
LOG = OUT + "/d18mid_w.log"
D, CAP = "18.125", 28800
WAIT_LOG, WAIT_PID = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/d185_w.log", 12848     # the D 18.5 driver
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (STATE, "5bf7b711a2dbbabb664201e182f90b79d88bb037"), (REC, "08f4dbf367edba55814e5cf989ccd32a9a5dbe67")]


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def alive(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command", f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 'yes' }}"], capture_output=True, text=True)
    return bool(r.stdout.strip())


def run_group(cmds, logs, names, cap, cwd, env, samples, interval):
    """start every command, poll, kill any still running at the cap by exact pid; returns (exit codes, the sampler process)"""
    procs, t0 = [], time.time()
    for c, lg, nm in zip(cmds, logs, names):
        p = subprocess.Popen(c, cwd=cwd, env=env, stdout=open(lg, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        procs.append((p, nm))
        say(f"started {nm} pid {p.pid}: {' '.join(c)[:300]} > {lg}")
    s = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", HERE + "/sample_driver_1025.ps1", "-Drv", str(os.getpid()), "-Out", samples, "-Interval", str(interval)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rcs = [None] * len(procs)
    while any(r is None for r in rcs):
        for i, (p, nm) in enumerate(procs):
            if rcs[i] is None:
                rc = p.poll()
                if rc is not None:
                    rcs[i] = rc
                    say(f"{nm} pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
                elif time.time() - t0 > cap:
                    r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
                    say(f"CAP {cap} s: killed {nm} pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                    p.wait()
                    rcs[i] = "killed at the cap"
        if any(r is None for r in rcs):
            time.sleep(10)
    return rcs, s


if "--selftest" in sys.argv:
    LOG = HERE + "/d18mid_driver_selftest.log"
    smp = HERE + "/d18mid_driver_selftest_samples.csv"
    for fn in (LOG, smp):
        if os.path.exists(fn):
            os.remove(fn)
    quick = [PY, "-c", "import time; print('quick', flush=True); time.sleep(12)"]
    slow = [PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"]
    rcs, s = run_group([quick, slow], [HERE + "/d18mid_selftest_a.log", HERE + "/d18mid_selftest_b.log"], ["quick", "slow"], 30, HERE, dict(os.environ), smp, 5)
    time.sleep(6)
    rows = open(smp).read().splitlines()
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"],
                          capture_output=True, text=True).stdout.strip()
    fields = {len(r.split(",")) for r in rows[1:]}
    ok = rcs == [0, "killed at the cap"] and left == "0" and len(rows) >= 4 and fields == {12}
    say(f"selftest: {rcs}; {len(rows) - 1} sample rows, field counts {fields}; dummy processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    s.kill()
    sys.exit(0 if ok else 1)

say(f"d18mid_driver_1025.py: the D 18.125 scan in two processes; waiting for the D 18.5 driver (pid {WAIT_PID}, {WAIT_LOG})")
while alive(WAIT_PID) and "d185_driver_1025.py done" not in open(WAIT_LOG, errors="replace").read():
    time.sleep(30)
say("the D 18.5 driver has ended; checking pins")
for fn, want in PINS:
    got = subprocess.run(["git", "hash-object", "--no-filters", fn], capture_output=True, text=True).stdout.strip()
    if got != want:
        say(f"REFUSE: {fn} is blob {got}, not {want}")
        sys.exit(2)
head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if head != "505d839940456a3d04321d75cf66cc3b5bc831c4" or any(os.path.exists(f) for f in (SCANA, SCANB, SCAN)):
    say(f"REFUSE: worktree at {head} or a scan file exists")
    sys.exit(2)
os.makedirs(OUT + "/rows", exist_ok=True)
LA = ",".join(["1.82"] + [f"{1.70 + 0.01 * i:.2f}" for i in range(12)])         # 1.82, then 1.70 to 1.81
LB = ",".join(["1.82"] + [f"{1.83 + 0.01 * i:.2f}" for i in range(13)])         # 1.82 again, then 1.83 to 1.95
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1",
           P4_WT_MATTER=WT + "/solver/matter")
say(f"pins ok; scans: A d18_hybsign.py {REC} {STATE} {D} {LA} {SCANA}; B ... {LB} {SCANB}; 4 threads each, BelowNormal, cap {CAP} s each")
rcs, s = run_group([[PY, "-u", SCANNER, REC, STATE, D, LA, SCANA], [PY, "-u", SCANNER, REC, STATE, D, LB, SCANB]],
                   [OUT + "/rows/d18mid_scanA_raw.log", OUT + "/rows/d18mid_scanB_raw.log"], ["scanA", "scanB"], CAP, WT + "/solver/matter", env, OUT + "/rows/d18mid_samples.csv", 60)
for nm in ("A", "B"):
    with open(OUT + f"/d18mid_scan{nm}.log", "w") as g:
        for ln in open(OUT + f"/rows/d18mid_scan{nm}_raw.log", errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)
say(f"both scans ended: {rcs}")
r = subprocess.run([PY, HERE + "/merge_d18mid_1025.py", SCANA, SCANB, SCAN], capture_output=True, text=True)
open(OUT + "/rows/d18mid_merge.log", "w").write(r.stdout + r.stderr)
for ln in r.stdout.splitlines():
    say(ln)
if os.path.exists(SCAN):
    r = subprocess.run([PY, HERE + "/read_d18mid_1025.py", SCAN], capture_output=True, text=True)
    open(OUT + "/rows/d18mid_reading.log", "w").write(r.stdout + r.stderr)
    for ln in r.stdout.splitlines():
        if not ln.startswith("ln|det|:"):
            say(ln)
else:
    say("no merged scan: no reading (the points so far are in the two scan jsonl files)")
time.sleep(70)          # the sampler's last line
s.kill()
say("d18mid_driver_1025.py done")
