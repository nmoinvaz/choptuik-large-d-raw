#!/usr/bin/env python3
"""#1025 winb (successor session), the k_c 79 convergence check at D 18.5, PART 2, the hybrid scan (t5's order via t1w, confirmed by the coordinator t2j by hc after my 06:30 UTC report on 22 Nov):
xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) on the accepted k_c 79 state sol_l1kc79Wm1025_D18.5000.npy and its record, lambda 1.66, 1.67, 1.68, 1.69 (4 points),
the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, ONE process, 4 threads, BelowNormal, cap 28800 s (8 h) by the exact pid. d18_hybsign.py checks the record system first
(exit 3 if the state does not come back). Starts only when regrid_accepted.txt exists. Memory: no guard, the alert-only watcher is its own process. Then d18f_read.py window and
read_kc79_1025.py (the robust minus-to-plus change's det-linear estimate beside 1.677016 and 1.675995), and an hc to the coordinator t2j.
usage: kc79_scan_driver_1025.py"""
import datetime, os, re, subprocess, sys, time

S = "C:/Users/nathan/Source/kc79_1025"
OUT = S + "/I1025-win/kc79_d185"
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t2j"
RAWM = S + "/raw/I1025-mac/d18"
SCANNER, READER = RAWM + "/d18_hybsign.py", RAWM + "/d18f_read.py"
TAG = "l1kc79Wm1025"
STATE, REC = OUT + f"/sol_{TAG}_D18.5000.npy", OUT + f"/{TAG}.jsonl"
SCAN, LOG = OUT + "/scan_kc79_D185_1025.jsonl", OUT + "/kc79_scan_w.log"
CAP = 28800
LAMS = "1.66,1.67,1.68,1.69"
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "5fb96dceb427e965b830b42db5b8f30255f20532"), (RAWM + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"),
        (RAWM + "/d18c_read.py", "1383470feaa976e4185e423626a0d5fec328de86"), (RAWM + "/d18d_read.py", "6b6089034738a45c8dc9e6831a1654c1bac4ed18")]


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1025 k_c 79 scan: {msg}"])


os.makedirs(OUT + "/rows", exist_ok=True)
open(OUT + "/rows/scan_driver.pid", "w").write(str(os.getpid()))
say("kc79_scan_driver_1025.py: the k_c 79 hybrid scan at D 18.5; checking pins")
if not os.path.exists(OUT + "/regrid_accepted.txt"):
    say("REFUSE: regrid_accepted.txt does not exist"); hc("not started: the regrid is not accepted."); sys.exit(2)
for fn, want in PINS:
    got = sh(["git", "hash-object", "--no-filters", fn]).stdout.strip()
    if got != want:
        say(f"REFUSE: {fn} is blob {got}, not {want}"); hc(f"not started: pin {fn} is blob {got[:8]}."); sys.exit(2)
if sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip() != "48c36355d1ba64de4e3112ed968fd6c034384551" or os.path.exists(SCAN):
    say(f"REFUSE: worktree not at 48c36355 or {SCAN} exists"); hc("not started: worktree or scan file check failed."); sys.exit(2)
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scan_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc79_watch_alert_1025.py", str(os.getpid()), "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)
cmd = [PY, "-u", SCANNER, REC, STATE, "18.5", LAMS, SCAN]
p = subprocess.Popen(cmd, cwd=WTM, env=env, stdout=open(OUT + "/rows/scan_kc79_raw.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
say(f"scan: started pid {p.pid}: d18_hybsign.py {REC} {STATE} 18.5 {LAMS} {SCAN}")
t0, rc = time.time(), None
while rc is None:
    rc = p.poll()
    if rc is None and time.time() - t0 > CAP:
        r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
        say(f"scan: CAP {CAP} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
        p.wait(); rc = "killed at the cap"
    elif rc is None:
        time.sleep(15)
say(f"scan: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
with open(OUT + "/scan_kc79_D185.log", "w") as g:
    for ln in open(OUT + "/rows/scan_kc79_raw.log", errors="replace"):
        if not re.search(r"Warning|^  [a-z]+ = ", ln):
            g.write(ln)
if rc != 0:
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exit {rc}; 3 means the state is not the record system). Points so far in scan_kc79_D185_1025.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("kc79_scan_driver_1025.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, PYTHONPATH=WTM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, READER, "window", "18.5", "1.66", "1.69", SCAN], cwd=WTM, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return "))
open(OUT + "/read_kc79_D185.log", "w").write(txt + "\n")
r2 = sh([PY, S + "/read_kc79_1025.py", OUT + "/read_kc79_D185.log"])
open(OUT + "/read_kc79_1025.log", "w").write(r2.stdout + r2.stderr)
for ln in (txt + "\n" + r2.stdout).splitlines():
    say(ln)
last = [l for l in r2.stdout.splitlines() if l.startswith("READING")]
hc(f"the scan ended (exit 0, {time.time() - t0:.0f} s, 4 points). {last[0] if last else 'see read_kc79_1025.log'} Raw I1025-win/kc79_d185 after my next push; I post on #1025 next.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc79_scan_driver_1025.py done")
