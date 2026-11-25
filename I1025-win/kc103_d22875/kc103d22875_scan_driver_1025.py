#!/usr/bin/env python3
"""#1025 winb, the k_c 103 hybrid scan at D 22.875 on my regridded k_c 103 D 22.875 state (from win2's k_c 95 D 22.875 state) (t5's order, hc of 2026-11-25 ~18:55 UTC; the shares are an argument): xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged)
on the accepted state sol_l1kc103win22875_D22.8750.npy and its record (both in this folder, checked against the blobs the regrid driver wrote into regrid_accepted.txt), at the lambda shares LISTS (semicolon-separated, one share
per process, at most 4; a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, FOUR PROCESSES (one per share), ONE thread each, BelowNormal, cap 21600 s by the exact pids.
d18_hybsign.py checks the record system first (exit 3 if the state does not come back) and appends one JSON line per lambda to its own file scan_kc103_D22875_p<i>.jsonl. Starts only when regrid_accepted.txt exists (and names the
state and record blobs) and no scan file exists. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration.
Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys; its selftest and the two --mutate controls must give exit 0, 1, 1 before the scan starts) on the folder, and an hc to the coordinator t5
with every line it printed.
usage: kc103d22875_scan_driver_1025.py LISTS [--dry [--out=DIR]]     e.g. "0.10,0.08,0.04;0.12,0.16,0.20;0.14,0.06;0.10,0.18"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR)"""
import datetime, os, re, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1025-win/kc103_d22875"
DRYOUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
if DRYOUT and "--dry" not in sys.argv:
    print("REFUSE: --out=DIR is for --dry only"); sys.exit(2)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DS = "22.875"
SRC = DRYOUT or OUT          # the regridded state, record and marker (written by kc103d22875_regrid_driver_1025.py)
RAWM = S + "/inputs"
SCANNER, READER = RAWM + "/d18_hybsign.py", RAWM + "/read_lower.py"
TAG = "l1kc103win22875"
STATE, REC = SRC + f"/sol_{TAG}_D22.8750.npy", SRC + f"/{TAG}.jsonl"
LOG = OUT + "/kc103d22875_scan_w.log"
CAP = 21600
DRY = "--dry" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    print("usage: kc103d22875_scan_driver_1025.py LISTS [--dry [--out=DIR]]"); sys.exit(2)
try:
    SH = [[float(v) for v in sh.split(",")] for sh in args[0].split(";")]
except ValueError:
    print("REFUSE: the shares are not semicolon-separated comma-separated lists of numbers:", args[0]); sys.exit(2)
ALL = [v for sh in SH for v in sh]
if not 1 <= len(SH) <= 4 or any(not sh for sh in SH) or len(set(ALL)) < 2 or max(ALL.count(v) for v in ALL) > 2 or not all(0.0 < v < 10.0 for v in ALL):
    print("REFUSE: wanted 1 to 4 non-empty shares, at least two distinct values in (0, 10), none more than twice:", args[0]); sys.exit(2)
LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"
if DRY:
    LOG = LOG + ".dry"
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"), (RAWM + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da")]


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 103 D {DS} scan ({LO}-{HI}): {msg}"])


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
say(f"kc103d22875_scan_driver_1025.py: the k_c 103 hybrid scan at D {DS}, shares {args[0]}{' (dry run)' if DRY else ''}; checking pins")
if not os.path.exists(SRC + "/regrid_accepted.txt"):
    refuse("regrid_accepted.txt does not exist", "not started: the k_c 103 D 22.875 regrid is not accepted.")
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
head = sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip()
SCANF = [OUT + f"/scan_kc103_D22875_p{i}.jsonl" for i in range(len(SH))]
if head != "48c36355d1ba64de4e3112ed968fd6c034384551" or any(os.path.exists(f) for f in SCANF):
    refuse(f"worktree at {head[:8]}, not 48c36355, or a scan file exists", "not started: worktree or scan file check failed.")
renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
st = []
for mut in ("", "--mutate=shift", "--mutate=round2"):
    r0 = sh([PY, "-I", READER, "selftest"] + ([mut] if mut else []), cwd=OUT, env=renv0)
    st.append(r0.returncode)
    open(OUT + "/selftest_read_lower_1025.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC read_lower.py selftest {mut}\n" + r0.stdout + f"selftest {mut} exit {r0.returncode} ({0 if not mut else 1} wanted)\n")
if st != [0, 1, 1]:
    refuse(f"read_lower.py selftest and its two controls gave exits {st}, wanted [0, 1, 1]", f"not started: read_lower.py selftest/controls exits {st}, wanted [0, 1, 1].")
else:
    say("read_lower.py selftest exit 0 and its two --mutate controls exit 1, 1 as wanted")
cmds = [[PY, "-u", SCANNER, REC, STATE, DS, ",".join(f"{v:g}" for v in sh_), SCANF[i]] for i, sh_ in enumerate(SH)]
if DRY:
    for c in cmds:
        say("DRY: would start " + " ".join(c) + f" (cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s)")
    say(f"DRY: reader window {LO} {HI}; nothing started"); sys.exit(0)
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scan_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc103d22875_watch_alert_1025.py", str(os.getpid()), "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)
procs = []
for i, c in enumerate(cmds):
    p = subprocess.Popen(c, cwd=WTM, env=env, stdout=open(OUT + f"/rows/scan_p{i}_raw.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    procs.append(p)
    say(f"scan p{i}: started pid {p.pid}: d18_hybsign.py {REC} {STATE} {DS} {c[6]} {SCANF[i]}")
t0, rc = time.time(), [None] * len(procs)
while any(r is None for r in rc):
    for i, p in enumerate(procs):
        if rc[i] is None:
            rc[i] = p.poll()
            if rc[i] is not None:
                say(f"scan p{i}: pid {p.pid} ended with exit {rc[i]} after {time.time() - t0:.0f} s")
    if any(r is None for r in rc) and time.time() - t0 > CAP:
        for i, p in enumerate(procs):
            if rc[i] is None:
                r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
                say(f"scan p{i}: CAP {CAP} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                p.wait(); rc[i] = "killed at the cap"
    elif any(r is None for r in rc):
        time.sleep(15)
say(f"all scan processes ended after {time.time() - t0:.0f} s, exits {rc}")
with open(OUT + "/scan_kc103_D22875.log", "w") as g:
    for i in range(len(procs)):
        g.write(f"== p{i}\n")
        for ln in open(OUT + f"/rows/scan_p{i}_raw.log", errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)
if any(r != 0 for r in rc):
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exits {rc}; 3 means the state is not the record system). Points so far in scan_kc103_D22875_p*.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("kc103d22875_scan_driver_1025.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + "/read_lower_kc103_D22875.log", "w").write(txt + f"\nread_lower exit {r.returncode}\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended ({len(procs)} exits {rc}, {time.time() - t0:.0f} s, shares {args[0]}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + ". Raw I1025-win/kc103_d22875 after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc103d22875_scan_driver_1025.py done")
