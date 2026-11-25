#!/usr/bin/env python3
"""#1025 winb, the secant refinement of the k_c 103 root at D 22.875 (t5's order, hc of 2026-11-25 ~22:50 UTC, queued after the D 22.875 scan): xfkappa's d18_secant.py (branch wip/ell1-speed at 6010e37b,
committed blob a3d90cd5; Brent's method on the hybrid sign) on my accepted k_c 103 state sol_l1kc103win22875_D22.8750.npy and its record l1kc103win22875.jsonl (blobs 28051531, f623d3e6, the scan's), between the scan's
robust bracket LO HI (arguments, taken by me from the reader's lines):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 22.875 LO HI secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB     one process, BelowNormal, 1 thread (OMP/OPENBLAS/MKL 1 too)
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree choptuik-i1025secant (HEAD 6010e37b); the state and the record against the blobs in regrid_accepted.txt and the constants here;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each (t5's order);
  3. the bracket: the scan's files scan_kc103_D22875_p*.jsonl hold LO and HI for this state, both noise-robust, with opposite hybrid signs (the tool re-evaluates both ends and refuses otherwise: exit 2);
  4. the run, capped at 54000 s by the exact pid (killed by taskkill /PID /T /F), one hc to t5 at 21600 s if it is still running; nothing is stopped at 6 h.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends), 3 pin differs or not the record system. Its own records (one per evaluation, then a root record)
are appended to secant/secant.jsonl; the log is secant/secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it, as in my other drivers; nothing kills on memory.
usage: kc103d22875_secant_driver_1025.py LO HI [--dry [--scandir=DIR]]     (--dry: pins, selftests, bracket check, prints the command, starts nothing; --scandir=DIR (dry only) takes the scan files from DIR)"""
import datetime, glob, json, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1025-win/kc103_d22875"
SEC = OUT + "/secant"
WTS = "C:/Users/nathan/Source/choptuik-i1025secant"
WTM = WTS + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SCANDIR = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--scandir=")), None)
if SCANDIR and not DRY:
    print("REFUSE: --scandir=DIR is for --dry only"); sys.exit(2)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 2:
    print("usage: kc103d22875_secant_driver_1025.py LO HI [--dry [--scandir=DIR]]"); sys.exit(2)
try:
    LO, HI = float(args[0]), float(args[1])
except ValueError:
    print("REFUSE: LO HI are not numbers:", args); sys.exit(2)
if not 0.0 < LO < HI < 10.0:
    print("REFUSE: wanted 0 < LO < HI < 10:", LO, HI); sys.exit(2)
D = "22.875"
STATE, STUB = OUT + "/sol_l1kc103win22875_D22.8750.npy", OUT + "/l1kc103win22875.jsonl"
B_STATE, B_STUB = "280515313e580cccbf14a6e0828e4eaa9b22086d", "f623d3e67b94a5ac4e38e2c55d05d3bf247e4c71"
PINS = [(WTM + "/d18_secant.py", "a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49", True), (WTM + "/ell_fastm.py", "93f963f6102f48e35c56c9eace25e1afd03b6ea2", True),
        (WTM + "/ell_ddm.py", "86578feeab868691778019b79771aef727510a76", True), (WTM + "/dss_ell.py", "5d28c19e17efa6b0103cb81d650891706605532d", True),
        (WTM + "/ell_dd.py", "7e58fcbc2288eca8f8f1ebfc36f7250a328b0c4e", True), (WTM + "/ddnp.py", "9b1fb195d0fa95d5dd7abd1083ac9b36fef04869", True),
        (STATE, B_STATE, False), (STUB, B_STUB, False)]
CAP, NOTIFY = 54000, 21600
LOG = SEC + "/secant_driver_w.log" + (".dry" if DRY else "")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(m):
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 103 D {D} secant refinement ({LO:g}-{HI:g}): {m}"])


def refuse(m):
    say("REFUSE: " + m)
    if DRY:
        say("DRY: a real run would stop here")
        return
    hc("not started: " + m)
    sys.exit(2)


os.makedirs(SEC, exist_ok=True)
os.makedirs(OUT + "/rows", exist_ok=True)
say(f"kc103d22875_secant_driver_1025.py: the secant refinement of the k_c 103 root at D {D}, bracket ({LO!r}, {HI!r}){' (dry run)' if DRY else ''}; checking pins")
if sh(["git", "-C", WTS, "rev-parse", "HEAD"]).stdout.strip() != "6010e37b30f92688dd5c659e383c6d0c8d14b6da":
    refuse("the secant worktree is not at 6010e37b")
for p, b, filt in PINS:
    g = sh(["git", "hash-object"] + ([] if filt else ["--no-filters"]) + [p]).stdout.strip()
    if g != b:
        refuse(f"{p} is blob {g}, not {b}")
if not DRY or SCANDIR is None:
    mk = open(OUT + "/regrid_accepted.txt").read().split() if os.path.exists(OUT + "/regrid_accepted.txt") else []
    if len(mk) < 8 or mk[0] != "ACCEPTED" or mk[5] != B_STATE or mk[7] != B_STUB:
        refuse(f"regrid_accepted.txt does not carry the state {B_STATE[:8]} and record {B_STUB[:8]} blobs: {mk}")
say(f"pins ok (worktree 6010e37b, d18_secant.py a3d90cd5, ell_fastm.py 93f963f6, the solver files equal to my regrids', state {B_STATE[:8]}, record {B_STUB[:8]})")
env = dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
ex = []
for mut in ("", "--mutate=half", "--mutate=norobust", "--mutate=nosigncheck"):
    r = sh([PY, "-u", WTM + "/d18_secant.py", "selftest"] + ([mut] if mut else []), cwd=WTM, env=env)
    ex.append(r.returncode)
    open(SEC + "/selftest_d18_secant.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC d18_secant.py selftest {mut}\n" + r.stdout + r.stderr + f"exit {r.returncode} ({0 if not mut else 1} wanted)\n")
if ex != [0, 1, 1, 1]:
    refuse(f"d18_secant.py selftest and its three controls (half, norobust, nosigncheck) gave exits {ex}, wanted [0, 1, 1, 1]")
else:
    say("d18_secant.py selftest exit 0 and its three controls (half, norobust, nosigncheck) exit 1, 1, 1 as wanted")
rows = []
for f in sorted(glob.glob((SCANDIR or OUT) + "/scan_kc103_D22875_p*.jsonl")):
    rows += [json.loads(l) for l in open(f) if l.strip()]
rows = [w for w in rows if w.get("D") == float(D) and w.get("kc") == 103 and w.get("state") == os.path.basename(STATE)]
ends = []
for lam in (LO, HI):
    m = [w for w in rows if abs(w["lam"] - lam) < 1e-9]
    if not m:
        refuse(f"the scan has no record at lambda {lam!r} of this state"); ends = None; break
    ends.append(m[-1])
if ends:
    if not all(e.get("noise_robust") for e in ends):
        refuse(f"an end of the bracket is not noise-robust in the scan: {[(e['lam'], e['sign'], e.get('noise_robust')) for e in ends]}")
    elif ends[0]["sign"] == ends[1]["sign"]:
        refuse(f"the scan's hybrid signs at {LO!r} and {HI!r} are equal ({ends[0]['sign']:+.0f})")
    else:
        say(f"bracket ok: the scan's hybrid sign is {ends[0]['sign']:+.0f} at {LO!r} and {ends[1]['sign']:+.0f} at {HI!r}, both noise-robust")
cmd = [PY, "-u", WTM + "/d18_secant.py", "run", STUB, STATE, D, f"{LO:g}", f"{HI:g}", SEC + "/secant.jsonl", "--tol=1e-5", "--maxev=10", f"--pin={B_STATE},{B_STUB}"]
if DRY:
    say("DRY: would start " + " ".join(cmd) + f" > {SEC}/secant.log (cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s, hc at {NOTIFY} s); nothing started")
    sys.exit(0)
if os.path.exists(SEC + "/secant.jsonl") or os.path.exists(SEC + "/secant.log"):
    refuse("secant.jsonl or secant.log exists")
open(SEC + "/secant_driver.pid", "w").write(str(os.getpid()))
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_secant_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/secant_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc103d22875_watch_alert_1025.py", str(os.getpid()), "secant"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "secant", str(CAP + 1800)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
p = subprocess.Popen(cmd, cwd=WTM, env=env, stdout=open(SEC + "/secant.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
say(f"secant: started pid {p.pid}: d18_secant.py run {STUB} {STATE} {D} {LO:g} {HI:g} {SEC}/secant.jsonl --tol=1e-5 --maxev=10 --pin=...")
t0, notified, rc = time.time(), False, None
while rc is None:
    rc = p.poll()
    if rc is not None:
        break
    if not notified and time.time() - t0 > NOTIFY:
        notified = True
        n = sum(1 for _ in open(SEC + "/secant.jsonl")) if os.path.exists(SEC + "/secant.jsonl") else 0
        say(f"secant: still running at {NOTIFY} s (pid {p.pid}), {n} record(s) in secant.jsonl; cap {CAP} s; hc to t5")
        hc(f"the refinement (pid {p.pid}) is still running after {NOTIFY} s (6 h), {n} evaluation record(s) so far; its cap is {CAP} s (15 h); nothing is stopped at 6 h.")
    if time.time() - t0 > CAP:
        r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
        say(f"secant: CAP {CAP} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
        p.wait()
        rc = "killed at the cap"
        break
    time.sleep(15)
wall = time.time() - t0
say(f"secant: pid {p.pid} ended with exit {rc} after {wall:.0f} s")
recs = [json.loads(l) for l in open(SEC + "/secant.jsonl") if l.strip()] if os.path.exists(SEC + "/secant.jsonl") else []
ev = [r for r in recs if r.get("kind") == "eval"]
root = next((r for r in reversed(recs) if r.get("kind") == "root"), None)
lines = [f"eval {r['it']} ({r['role']}) lam {r['lam']!r}: hybrid {r['sign']:+.0f} ln|det| {r['ln']:.10f} dln {r['dln'] if r['dln'] is None else format(r['dln'], '.2e')} robust {r['robust']}, float64 {r['f64_sign']:+.0f}, {r.get('sec')} s {r.get('sec_parts', '')}" for r in ev]
if root:
    lines.append(f"root: status {root['status']} ({root['why'] or '-'}), bracket [{root['bracket'][0]!r}, {root['bracket'][1]!r}] width {root['width']:.3e}, signs {root['signs']}, "
                 f"det-linear {root['lam_lin']!r}, Brent {root['lam_brent']!r}, {root['n_eval']} evaluations, {root['sec']} s")
else:
    lines.append("no root record")
for ln in lines:
    say(ln)
time.sleep(70)          # the sampler's last line
pk = dict(priv=0.0, ws=0.0, free=1e9, commit=0.0, cpu=0.0, n=0)
try:
    import csv
    for row in csv.DictReader(open(OUT + "/rows/secant_samples.csv")):
        if row["stage"] == "secant":
            pk["n"] += 1
            pk["priv"] = max(pk["priv"], float(row["private_peak_gb"])); pk["ws"] = max(pk["ws"], float(row["ws_peak_gb"]))
            pk["cpu"] = max(pk["cpu"], float(row["cpu_s"]))
        pk["free"] = min(pk["free"], float(row["free_phys_gb"])); pk["commit"] = max(pk["commit"], float(row["commit_gb"]))
except Exception as e:
    say(f"sampler csv: {e}")
summ = f"exit {rc}, wall {wall:.0f} s; peak private {pk['priv']:.2f} GB, peak working set {pk['ws']:.2f} GB, lowest free memory {pk['free']:.2f} GB, peak commit {pk['commit']:.1f} GB, cpu {pk['cpu']:.0f} s ({pk['n']} samples)"
say(summ)
open(SEC + "/secant_summary.txt", "w").write("\n".join(lines) + "\n" + summ + "\n")
hc(f"the refinement ended, {summ}. Lines as printed: " + " | ".join(lines) + ". Raw I1025-win/kc103_d22875/secant after my next push; no reading by me, you rule.")
time.sleep(5)
samp.kill()
say("kc103d22875_secant_driver_1025.py done")
sys.exit(0 if rc == 0 else 1)
