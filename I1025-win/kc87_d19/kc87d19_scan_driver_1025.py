#!/usr/bin/env python3
"""#1025 winb, the k_c 87 hybrid scan at D 19 on my regridded k_c 87 D 19 state (t5's order, #1025 comment of 2026-11-23 05:10 UTC, step 2 after ACCEPTED; the window is an argument):
xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) on the accepted state sol_l1kc87wind19_D19.0000.npy and its record (both in this folder, checked against the blobs the regrid driver wrote into
regrid_accepted.txt), at the lambda list WINDOW (comma-separated, in the given order; a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, ONE process, 4 threads,
BelowNormal, cap 36000 s (10 h) by the exact pid. d18_hybsign.py checks the record system first (exit 3 if the state does not come back). Starts only when regrid_accepted.txt exists (and names the state and record blobs)
and the scan file does not. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration. Then dh170's
read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys; its selftest and the two --mutate controls must give exit 0, 1, 1 before the scan starts) on the scan file, and an hc to the coordinator t5 with every line it printed.
usage: kc87d19_scan_driver_1025.py LAMBDA_LIST [--dry [--out=DIR]]     e.g. 1.380,1.405,1.430,1.455,1.480,1.505,1.530,1.555,1.580,1.480     (--dry: runs the checks, prints the planned command, starts nothing; --out=DIR (dry only) takes the state, record and marker from DIR)"""
import datetime, os, re, subprocess, sys, time

S = "C:/Users/nathan/Source/kc87d19_1025"
OUT = S + "/I1025-win/kc87_d19"
DRYOUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
if DRYOUT and "--dry" not in sys.argv:
    print("REFUSE: --out=DIR is for --dry only"); sys.exit(2)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
SRC = DRYOUT or OUT          # the regridded state, record and marker (written by kc87d19_regrid_driver_1025.py)
RAWM = S + "/inputs"
SCANNER, READER = RAWM + "/d18_hybsign.py", RAWM + "/read_lower.py"
TAG = "l1kc87wind19"
STATE, REC = SRC + f"/sol_{TAG}_D19.0000.npy", SRC + f"/{TAG}.jsonl"
SCAN, LOG = OUT + "/scan_kc87_D19_p0.jsonl", OUT + "/kc87d19_scan_w.log"
CAP = 36000
DRY = "--dry" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    print("usage: kc87d19_scan_driver_1025.py LAMBDA_LIST [--dry]"); sys.exit(2)
LAMS = args[0]
try:
    LV = [float(v) for v in LAMS.split(",")]
except ValueError:
    print("REFUSE: the window is not a comma-separated list of numbers:", LAMS); sys.exit(2)
if len(set(LV)) < 2 or max(LV.count(v) for v in LV) > 2 or not all(0.0 < v < 10.0 for v in LV):
    print("REFUSE: the window needs at least two distinct values in (0, 10), none more than twice:", LAMS); sys.exit(2)
LO, HI = f"{min(LV):g}", f"{max(LV):g}"
if DRY:
    LOG = LOG + ".dry"
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"), (RAWM + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da")]


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1025 k_c 87 D 19 scan (1.38-1.58): {msg}"])


def refuse(m, h):
    say("REFUSE: " + m)
    if DRY:
        say("DRY: a real run would stop here")
        return
    hc(h)
    sys.exit(2)


os.makedirs(OUT + "/rows", exist_ok=True)
if not DRY:
    open(OUT + "/rows/scan_driver.pid", "w").write(str(os.getpid()))
say(f"kc87d19_scan_driver_1025.py: the k_c 87 hybrid scan at D 19, window {LAMS}{' (dry run)' if DRY else ''}; checking pins")
if not os.path.exists(SRC + "/regrid_accepted.txt"):
    refuse("regrid_accepted.txt does not exist", "not started: the k_c 87 D 19 regrid is not accepted.")
else:
    mk = open(SRC + "/regrid_accepted.txt").read().split()
    if len(mk) < 8 or mk[0] != "ACCEPTED" or mk[4] != "state" or mk[6] != "record":
        refuse(f"regrid_accepted.txt is not an ACCEPTED marker with state and record blobs: {mk}", "not started: regrid_accepted.txt has no state and record blobs.")
    else:
        PINS += [(STATE, mk[5]), (REC, mk[7])]
for fn, want in PINS:
    got = sh(["git", "hash-object", "--no-filters", fn]).stdout.strip()
    if got != want:
        refuse(f"{fn} is blob {got}, not {want}", f"not started: pin {fn} is blob {got[:8]}.")
if sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip() != "48c36355d1ba64de4e3112ed968fd6c034384551" or os.path.exists(SCAN):
    refuse(f"worktree not at 48c36355 or {SCAN} exists", "not started: worktree or scan file check failed.")
renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
st = []
for mut in ("", "--mutate=shift", "--mutate=round2"):
    r0 = sh([PY, "-I", READER, "selftest"] + ([mut] if mut else []), cwd=OUT, env=renv0)
    st.append(r0.returncode)
    open(OUT + "/selftest_read_lower_1025.txt" + (".dry" if DRY else ""), "a").write(f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC read_lower.py selftest {mut}\n" + r0.stdout + f"selftest {mut} exit {r0.returncode} ({0 if not mut else 1} wanted)\n")
if st != [0, 1, 1]:
    refuse(f"read_lower.py selftest and its two controls gave exits {st}, wanted [0, 1, 1]", f"not started: read_lower.py selftest/controls exits {st}, wanted [0, 1, 1].")
else:
    say("read_lower.py selftest exit 0 and its two --mutate controls exit 1, 1 as wanted")
if DRY:
    say(f"DRY: would start d18_hybsign.py {REC} {STATE} 19 {LAMS} {SCAN} (cwd {WTM}, 4 threads, BelowNormal, cap {CAP} s); reader window {LO} {HI}; nothing started"); sys.exit(0)
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scan_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc87d19_watch_alert_1025.py", str(os.getpid()), "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)
cmd = [PY, "-u", SCANNER, REC, STATE, "19", LAMS, SCAN]
p = subprocess.Popen(cmd, cwd=WTM, env=env, stdout=open(OUT + "/rows/scan_kc87d19_raw.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
say(f"scan: started pid {p.pid}: d18_hybsign.py {REC} {STATE} 19 {LAMS} {SCAN}")
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
with open(OUT + "/scan_kc87_D19.log", "w") as g:
    for ln in open(OUT + "/rows/scan_kc87d19_raw.log", errors="replace"):
        if not re.search(r"Warning|^  [a-z]+ = ", ln):
            g.write(ln)
if rc != 0:
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exit {rc}; 3 means the state is not the record system). Points so far in scan_kc87_D19_p0.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("kc87d19_scan_driver_1025.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + "/read_lower_kc87_D19.log", "w").write(txt + f"\nread_lower exit {r.returncode}\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended (exit 0, {time.time() - t0:.0f} s, window {LAMS}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + ". Raw I1025-win/kc87_d19 after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc87d19_scan_driver_1025.py done")
