#!/usr/bin/env python3
"""#1025 winb, the secant refinement of the k_c 95 root at D 22.875 (t5's order, hc of 2026-11-26 ~06:35 UTC, after the k_c 103 D 22.875 ruling): xfkappa's d18_secant.py (branch wip/ell1-speed at 6010e37b,
committed blob a3d90cd5; Brent's method on the hybrid sign) on win2's accepted k_c 95 state sol_l1kc95win2d22875_D22.8750.npy (raw I1025-win2/kc95_d22875, blob a14f0d50) and its record l1kc95win2d22875.jsonl
(blob 5381f89d; copies in in/), between LO HI (arguments: win2's robust bracket (0.10, 0.12)):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 22.875 LO HI secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB     one process, BelowNormal, 1 thread (OMP/OPENBLAS/MKL 1 too)
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree choptuik-i1025secant (HEAD 6010e37b); the three checks (kc87 6df5d960, kc95 d487e628, kc103 3ab58d16); the state and the record;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc95_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 87 and k_c 103 checks refuse them (exit 1 each);
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 28800 s (8 h; t5: stop and report on any step over 8 h), one hc to t5 at 14400 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs: t5's "signs at 0.10 and 0.12 that do not differ"), 3 pin differs or
not the record system. Its own records (one per evaluation, then a root record) are appended to secant.jsonl; the log is secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run
beside it, as in my other drivers; nothing kills on memory.
usage: kc95d22875s_secant_driver_1025.py LO HI [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)"""
import datetime, json, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1025-win/kc95_d22875_secant"
SEC = OUT
IN = S + "/inputs"
WTS = "C:/Users/nathan/Source/choptuik-i1025secant"
WTM = WTS + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 2:
    print("usage: kc95d22875s_secant_driver_1025.py LO HI [--dry]"); sys.exit(2)
try:
    LO, HI = float(args[0]), float(args[1])
except ValueError:
    print("REFUSE: LO HI are not numbers:", args); sys.exit(2)
if not 0.0 < LO < HI < 10.0:
    print("REFUSE: wanted 0 < LO < HI < 10:", LO, HI); sys.exit(2)
D = "22.875"
STATE, STUB = OUT + "/in/sol_l1kc95win2d22875_D22.8750.npy", OUT + "/in/l1kc95win2d22875.jsonl"
B_STATE, B_STUB = "a14f0d50edb575e85387851a61cb2324c1983317", "5381f89d5fe4f81a113295cdde8eb6358de937e8"
PINS = [(WTM + "/d18_secant.py", "a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49", True), (WTM + "/ell_fastm.py", "93f963f6102f48e35c56c9eace25e1afd03b6ea2", True),
        (WTM + "/ell_ddm.py", "86578feeab868691778019b79771aef727510a76", True), (WTM + "/dss_ell.py", "5d28c19e17efa6b0103cb81d650891706605532d", True),
        (WTM + "/ell_dd.py", "7e58fcbc2288eca8f8f1ebfc36f7250a328b0c4e", True), (WTM + "/ddnp.py", "9b1fb195d0fa95d5dd7abd1083ac9b36fef04869", True),
        (IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6", False), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883", False),
        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d", False), (STATE, B_STATE, False), (STUB, B_STUB, False)]
CAP, NOTIFY = 28800, 14400
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
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 95 D {D} secant refinement ({LO:g}-{HI:g}): {m}"])


def refuse(m):
    say("REFUSE: " + m)
    if DRY:
        say("DRY: a real run would stop here")
        return
    hc("not started: " + m)
    sys.exit(2)


os.makedirs(SEC, exist_ok=True)
os.makedirs(OUT + "/rows", exist_ok=True)
say(f"kc95d22875s_secant_driver_1025.py: the secant refinement of the k_c 95 root at D {D}, bracket ({LO!r}, {HI!r}){' (dry run)' if DRY else ''}; checking pins")
if sh(["git", "-C", WTS, "rev-parse", "HEAD"]).stdout.strip() != "6010e37b30f92688dd5c659e383c6d0c8d14b6da":
    refuse("the secant worktree is not at 6010e37b")
for p, b, filt in PINS:
    g = sh(["git", "hash-object"] + ([] if filt else ["--no-filters"]) + [p]).stdout.strip()
    if g != b:
        refuse(f"{p} is blob {g}, not {b}")
say(f"pins ok (worktree 6010e37b, d18_secant.py a3d90cd5, ell_fastm.py 93f963f6, the solver files equal to my regrids', the three checks, state {B_STATE[:8]}, record {B_STUB[:8]})")
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
st = {}
for k in (95, 87, 103):
    r = sh([PY, "-u", IN + f"/kc{k}_syscheck_1025.py", "--selftest"], cwd=WTM, env=env)
    st[k] = r.returncode
    open(SEC + "/selftest_kc%d_syscheck.txt" % k + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
if st != {95: 0, 87: 0, 103: 0}:
    refuse(f"the selftests of the k_c 95, 87 and 103 checks gave exits {st}, wanted 0 each")
else:
    say("selftests: kc95_syscheck exit 0, kc87_syscheck exit 0, kc103_syscheck exit 0 (0 wanted each)")
t0 = time.time()
src = {}
for name, cmdl in (("source_kc95_syscheck.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM]), ("source_kc95_syscheck_mutate_F.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=F"]),
                   ("source_kc95_syscheck_mutate_steps.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=steps"]), ("source_kc87_syscheck.txt", [PY, IN + "/kc87_syscheck_1025.py", STUB, STATE, D, WTM]),
                   ("source_kc103_syscheck.txt", [PY, IN + "/kc103_syscheck_1025.py", STUB, STATE, D, WTM])):
    r = sh(cmdl, env=env)
    open(SEC + "/" + name + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    src[name] = r.returncode
want = {"source_kc95_syscheck.txt": 0, "source_kc95_syscheck_mutate_F.txt": 1, "source_kc95_syscheck_mutate_steps.txt": 1, "source_kc87_syscheck.txt": 1, "source_kc103_syscheck.txt": 1}
say(f"the state: kc95 check exit {src['source_kc95_syscheck.txt']} (0 wanted: it accepts), --mutate=F {src['source_kc95_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc95_syscheck_mutate_steps.txt']} (1 wanted each), "
    f"kc87 check {src['source_kc87_syscheck.txt']} and kc103 check {src['source_kc103_syscheck.txt']} (1 wanted each: they refuse it); {time.time() - t0:.0f} s")
if src != want:
    refuse(f"the state is not accepted as wanted ({src}, wanted {want})")
cmd = [PY, "-u", WTM + "/d18_secant.py", "run", STUB, STATE, D, f"{LO:g}", f"{HI:g}", SEC + "/secant.jsonl", "--tol=1e-5", "--maxev=10", f"--pin={B_STATE},{B_STUB}"]
if DRY:
    say("DRY: would start " + " ".join(cmd) + f" > {SEC}/secant.log (cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s, hc at {NOTIFY} s); nothing started")
    sys.exit(0)
if os.path.exists(SEC + "/secant.jsonl") or os.path.exists(SEC + "/secant.log"):
    refuse("secant.jsonl or secant.log exists")
open(SEC + "/secant_driver.pid", "w").write(str(os.getpid()))
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_secant_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/secant_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc95d22875s_watch_alert_1025.py", str(os.getpid()), "secant"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
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
        hc(f"the refinement (pid {p.pid}) is still running after {NOTIFY} s (4 h), {n} evaluation record(s) so far; it is killed by the exact pid at {CAP} s (8 h, your stop).")
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
say("kc95d22875s_secant_driver_1025.py done")
sys.exit(0 if rc == 0 else 1)
