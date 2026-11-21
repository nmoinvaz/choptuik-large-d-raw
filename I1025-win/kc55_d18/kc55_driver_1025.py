#!/usr/bin/env python3
"""#1025 winb, the k_c 55 test at D 18 (the coordinator's order, hc 2026-11-21 about 22:0x UTC): ONE process. xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged)
on the Mac's k_c 55 state sol_l1kc55F1025_D18.000000.npy (blob b2c3c302) and the D 18.0 line of l1kc55F1025.jsonl (blob 0fb77df8; its system check passed before, signtest.py
syscheck), lambda 1.70 to 1.85 at 0.01 (16 points), the noise test (1e-15 on blocks 0-11, 2 seeds) and the float64 sign, 4 threads, BelowNormal, 8 h cap (28800 s) by the exact pid of
the process this driver started (taskkill /PID <pid> /T /F). A memory watchdog polls the laptop's free physical memory every 15 s: below 1 GB the scan is stopped by that exact pid
and the coordinator is told by hc (the order). Then d18f_read.py window and read_kc55_1025.py (the coordinator's reading). usage: kc55_driver_1025.py [--selftest]"""
import datetime, os, re, subprocess, sys, time

OUT = "C:/Users/nathan/Source/kc55_1025/I1025-win/kc55_d18"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT_H = "C:/Users/nathan/Source/choptuik-i1025-lowd"       # 505d8399: d18_hybsign's solver code
WT_D = "C:/Users/nathan/Source/choptuik-i1025d"          # 48c36355: ell_delta.py for the readers
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
RAW = "C:/Users/nathan/Source/kc55_1025/raw/I1025-mac"
SCANNER, READER = RAW + "/d18/d18_hybsign.py", RAW + "/d18/d18f_read.py"
STATE, REC = RAW + "/out/sol_l1kc55F1025_D18.000000.npy", RAW + "/out/l1kc55F1025.jsonl"
SCAN, LOG = OUT + "/scan_kc55_D18_1025.jsonl", OUT + "/kc55_w.log"
CAP, MEM_STOP_GB = 28800, 1.0
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "5fb96dceb427e965b830b42db5b8f30255f20532"), (STATE, "b2c3c30278f92d8c4ce0ae4f235add7ea437eb16"),
        (REC, "0fb77df8281d634e6ecf2d3b2038e3706df3c960"), (RAW + "/d18/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"),
        (RAW + "/d18/d18c_read.py", "1383470feaa976e4185e423626a0d5fec328de86"), (RAW + "/d18/d18d_read.py", "6b6089034738a45c8dc9e6831a1654c1bac4ed18")]


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def free_gb():
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB, 3)"], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def run_guarded(cmd, logf, cap, cwd, env, mem_stop, tag):
    """start, poll every 15 s; kill by exact pid at the cap or when free memory is below mem_stop GB; returns (exit code or reason, minimum free memory seen)"""
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=open(logf, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    say(f"{tag}: started pid {p.pid}: {' '.join(cmd)[:300]} > {logf}")
    t0, lo, last = time.time(), 1e9, 0
    while True:
        rc = p.poll()
        if rc is not None:
            say(f"{tag}: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s; minimum free memory seen {lo:.2f} GB")
            return rc, lo
        f = free_gb()
        if f is not None:
            lo = min(lo, f)
            if time.time() - last > 600:
                say(f"{tag}: free memory {f:.2f} GB (minimum so far {lo:.2f})")
                last = time.time()
            if f < mem_stop:
                r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
                say(f"{tag}: MEMORY STOP: free memory {f:.2f} GB is below {mem_stop} GB: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                p.wait()
                return f"memory stop at {f:.2f} GB", lo
        if time.time() - t0 > cap:
            r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
            say(f"{tag}: CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
            p.wait()
            return "killed at the cap", lo
        time.sleep(15)


if "--selftest" in sys.argv:
    LOG = HERE + "/kc55_driver_selftest.log"
    if os.path.exists(LOG):
        os.remove(LOG)
    slow = [PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"]
    a = run_guarded(slow, HERE + "/kc55_selftest_a.log", 20, HERE, dict(os.environ), 0.0, "cap test")
    b = run_guarded(slow, HERE + "/kc55_selftest_b.log", 600, HERE, dict(os.environ), 1000.0, "memory test (threshold 1000 GB: always below)")
    time.sleep(2)
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"],
                          capture_output=True, text=True).stdout.strip()
    ok = a[0] == "killed at the cap" and str(b[0]).startswith("memory stop") and left == "0"
    say(f"selftest: {a[0]}; {b[0]}; dummy processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    sys.exit(0 if ok else 1)

say("kc55_driver_1025.py: the k_c 55 test at D 18; checking pins")
for fn, want in PINS:
    got = subprocess.run(["git", "hash-object", "--no-filters", fn], capture_output=True, text=True).stdout.strip()
    if got != want:
        say(f"REFUSE: {fn} is blob {got}, not {want}")
        sys.exit(2)
h = subprocess.run(["git", "-C", WT_H, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if h != "505d839940456a3d04321d75cf66cc3b5bc831c4" or os.path.exists(SCAN):
    say(f"REFUSE: worktree at {h} or {SCAN} exists")
    sys.exit(2)
os.makedirs(OUT + "/rows", exist_ok=True)
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", HERE + "/sample_driver3_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/kc55_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
L = ",".join(f"{1.70 + 0.01 * i:.2f}" for i in range(16))
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1",
           P4_WT_MATTER=WT_H + "/solver/matter")
say(f"pins ok; free memory now {free_gb()} GB; scan: d18_hybsign.py {REC} {STATE} 18.0 {L} {SCAN}")
rc, lo = run_guarded([PY, "-u", SCANNER, REC, STATE, "18.0", L, SCAN], OUT + "/rows/scan_kc55_D18_raw.log", CAP, WT_H + "/solver/matter", env, MEM_STOP_GB, "scan")
with open(OUT + "/scan_kc55_D18.log", "w") as g:
    for ln in open(OUT + "/rows/scan_kc55_D18_raw.log", errors="replace"):
        if not re.search(r"Warning|^  [a-z]+ = ", ln):
            g.write(ln)
if isinstance(rc, str) and rc.startswith("memory stop"):
    say(f"STOPPED for memory ({rc}); the points so far are in {SCAN}; no reading. Telling the coordinator.")
    subprocess.run([HC, "send", "nathans-macbook-air-m5-3/t5", f"winb: the k_c 55 D 18 scan was STOPPED by exact pid at {datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC because free memory fell below 1 GB ({rc}); points so far in raw I1025-win/kc55_d18 (after my next push); I do not restart it unless you say so."], capture_output=True)
    time.sleep(70); samp.kill(); say("kc55_driver_1025.py done (memory stop)")
    sys.exit(1)
if rc != 0:
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    time.sleep(70); samp.kill(); say("kc55_driver_1025.py done (no reading)")
    sys.exit(1)
renv = dict(os.environ, PYTHONPATH=WT_D + "/solver/matter", PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = subprocess.run([PY, READER, "window", "18.0", "1.70", "1.85", SCAN], cwd=WT_D + "/solver/matter", env=renv, capture_output=True, text=True)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return "))
open(OUT + "/read_kc55_D18.log", "w").write(txt + "\n")
r2 = subprocess.run([PY, HERE + "/read_kc55_1025.py", OUT + "/read_kc55_D18.log"], capture_output=True, text=True)
open(OUT + "/read_kc55_1025.log", "w").write(r2.stdout + r2.stderr)
for ln in (txt + "\n" + r2.stdout).splitlines():
    say(ln)
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc55_driver_1025.py done")
