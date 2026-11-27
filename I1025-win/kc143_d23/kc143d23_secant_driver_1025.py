#!/usr/bin/env python3
"""#1025 winb, the secant refinement of the k_c 143 root at D 23.0 with the Rust block 12 (t5's order, hc of 2026-11-27 05:59 UTC, step 3 of the lane): d18_secant.py run (branch wip/ell1-rust-b12 at d4b6b6ce, committed
blob 9706e506, worktree choptuik-i1102; Brent's method on the signed hybrid determinant) with --b12=rust --b12_threads=4 (ellrs from my #1102 build, i1102_1025/site, on PYTHONPATH, pinned by blob; OPENBLAS_NUM_THREADS=1) on my
accepted k_c 143 state sol_l1kc143winbd23_D23.0000.npy and its record l1kc143winbd23.jsonl (both in this folder; the blobs are the ones in regrid_accepted.txt), between LO HI (arguments: the robust bracket the scan's reader
printed), with the scan's two end records (--ends, verbatim lines of scan_kc143_D23_p*.jsonl; t5: "Reuse the scan's ends"):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=5e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB --ends=scan_kc143_D23_ends.jsonl --b12=rust --b12_threads=4     one process, BelowNormal
(--tol=5e-5 is t5's, not 1e-5: #1101's dh370 test measured a root scatter of 1.75e-4 between two solves of one state). Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py (blob 9706e506), ell_b12rs.py, the ellrs files of the site, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree (HEAD d4b6b6ce); the three checks (kc127 898ebefa, kc135 b353d466, kc143 e15b0ee2); the state and
     the record against the blobs of regrid_accepted.txt; the ends file (blob from --ends-blob=) and its two lines verbatim in the scan files;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc143_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 135 and k_c 127 checks refuse them (exit 1 each);
  3b. the ends: scan_kc143_D23_ends.jsonl is two lines, each verbatim a line of the scan files at lambda LO and HI;
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 43200 s (12 h; t5: stop and report on any step over 12 h), one hc to t5 at 21600 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs), 3 pin differs or not the record system. Its own records (one per evaluation
record) are appended to secant/secant.jsonl; the log is secant/secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it, as in my other drivers; nothing kills on memory.
usage: kc143d23_secant_driver_1025.py LO HI --ends-blob=BLOB [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)"""
import datetime, glob, json, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1025-win/kc143_d23"
SEC = OUT + "/secant"
IN = S + "/inputs"
WTS = "C:/Users/nathan/Source/choptuik-i1102"
SITE = "C:/Users/nathan/Source/i1102_1025/site"          # ellrs (my #1102 build, cp314, avx512), on PYTHONPATH
WTM = WTS + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
ENDSBLOB = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--ends-blob=")), "")
if len(args) != 2 or len(ENDSBLOB) != 40:
    print("usage: kc143d23_secant_driver_1025.py LO HI --ends-blob=BLOB [--dry]"); sys.exit(2)
try:
    LO, HI = float(args[0]), float(args[1])
except ValueError:
    print("REFUSE: LO HI are not numbers:", args); sys.exit(2)
if not 0.0 < LO < HI < 10.0:
    print("REFUSE: wanted 0 < LO < HI < 10:", LO, HI); sys.exit(2)
D = "23.0"
STATE, STUB = OUT + "/sol_l1kc143winbd23_D23.0000.npy", OUT + "/l1kc143winbd23.jsonl"
_mk = open(OUT + "/regrid_accepted.txt").read().split() if os.path.exists(OUT + "/regrid_accepted.txt") else []
B_STATE, B_STUB = (_mk[5], _mk[7]) if len(_mk) > 7 and _mk[0] == "ACCEPTED" else ("0" * 40, "0" * 40)
ENDS = OUT + "/scan_kc143_D23_ends.jsonl"     # t5's order (hc 05:59 UTC): --ends, "Reuse the scan's ends": the two end records of the scan, verbatim lines of the scan files
B_ENDS = ENDSBLOB
PINS = [(WTM + "/d18_secant.py", "9706e506111357e5e6a3f1bccd60154ac3d17cbc", True), (WTM + "/ell_b12rs.py", "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef", True), (SITE + "/ellrs/ellrs.cp314-win_amd64.pyd", "ddd5a08281f4aa325bd8564f08f9f2c3cebba33d", False), (SITE + "/ellrs/__init__.py", "76c7cfbc8fdfe90adb0debb60ac2d4754974cb1d", False), (WTM + "/ell_fastm.py", "93f963f6102f48e35c56c9eace25e1afd03b6ea2", True),
        (WTM + "/ell_ddm.py", "86578feeab868691778019b79771aef727510a76", True), (WTM + "/dss_ell.py", "5d28c19e17efa6b0103cb81d650891706605532d", True),
        (WTM + "/ell_dd.py", "7e58fcbc2288eca8f8f1ebfc36f7250a328b0c4e", True), (WTM + "/ddnp.py", "9b1fb195d0fa95d5dd7abd1083ac9b36fef04869", True),
        (IN + "/kc143_syscheck_1025.py", "e15b0ee2b0b1f9e48a914b6e3e75f4fec48251f4", False), (IN + "/kc135_syscheck_1025.py", "b353d46696d2c90eb413fb071becb3e9aa8f976a", False),
        (IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719", False), (STATE, B_STATE, False), (STUB, B_STUB, False), (ENDS, B_ENDS, False)]
CAP, NOTIFY = 43200, 21600
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
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 143 D {D} secant refinement ({LO:g}-{HI:g}): {m}"])


def refuse(m):
    say("REFUSE: " + m)
    if DRY:
        say("DRY: a real run would stop here")
        return
    hc("not started: " + m)
    sys.exit(2)


os.makedirs(SEC, exist_ok=True)
os.makedirs(OUT + "/rows", exist_ok=True)
say(f"kc143d23_secant_driver_1025.py: the secant refinement of the k_c 143 root at D {D}, bracket ({LO!r}, {HI!r}){' (dry run)' if DRY else ''}; checking pins")
if sh(["git", "-C", WTS, "rev-parse", "HEAD"]).stdout.strip() != "d4b6b6cea24f518d38cac17877c9a0da813b05f4":
    refuse("the secant worktree is not at d4b6b6ce")
for p, b, filt in PINS:
    g = sh(["git", "hash-object"] + ([] if filt else ["--no-filters"]) + [p]).stdout.strip()
    if g != b:
        refuse(f"{p} is blob {g}, not {b}")
_ends = open(ENDS, "rb").read().decode("utf-8").splitlines(keepends=True) if os.path.exists(ENDS) else []
_scan = set(l for f in glob.glob(OUT + "/scan_kc143_D23_p*.jsonl") for l in open(f, "rb").read().decode("utf-8").splitlines(keepends=True))
if len(_ends) != 2 or any(l not in _scan for l in _ends) or [json.loads(l)["lam"] for l in _ends] != [LO, HI]:
    refuse("the --ends file is not the scan records at LO and HI (two lines, each verbatim a line of scan_kc143_D23_p*.jsonl)")
say(f"pins ok (worktree d4b6b6ce, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, the ellrs site files, ell_fastm.py 93f963f6, the solver files equal to my regrids', the three checks, the marker's state {B_STATE[:8]}, record {B_STUB[:8]})")
env = dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=SITE)
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
for k in (143, 135, 127):
    r = sh([PY, "-u", IN + f"/kc{k}_syscheck_1025.py", "--selftest"], cwd=WTM, env=env)
    st[k] = r.returncode
    open(SEC + "/selftest_kc%d_syscheck.txt" % k + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
if st != {143: 0, 135: 0, 127: 0}:
    refuse(f"the selftests of the k_c 143, 135 and 127 checks gave exits {st}, wanted 0 each")
else:
    say("selftests: kc143_syscheck exit 0, kc135_syscheck exit 0, kc127_syscheck exit 0 (0 wanted each)")
t0 = time.time()
src = {}
for name, cmdl in (("source_kc143_syscheck.txt", [PY, IN + "/kc143_syscheck_1025.py", STUB, STATE, D, WTM]), ("source_kc143_syscheck_mutate_F.txt", [PY, IN + "/kc143_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=F"]),
                   ("source_kc143_syscheck_mutate_steps.txt", [PY, IN + "/kc143_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=steps"]), ("source_kc135_syscheck.txt", [PY, IN + "/kc135_syscheck_1025.py", STUB, STATE, D, WTM]),
                   ("source_kc127_syscheck.txt", [PY, IN + "/kc127_syscheck_1025.py", STUB, STATE, D, WTM])):
    r = sh(cmdl, env=env)
    open(SEC + "/" + name + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    src[name] = r.returncode
want = {"source_kc143_syscheck.txt": 0, "source_kc143_syscheck_mutate_F.txt": 1, "source_kc143_syscheck_mutate_steps.txt": 1, "source_kc135_syscheck.txt": 1, "source_kc127_syscheck.txt": 1}
say(f"the state: kc143 check exit {src['source_kc143_syscheck.txt']} (0 wanted: it accepts), --mutate=F {src['source_kc143_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc143_syscheck_mutate_steps.txt']} (1 wanted each), "
    f"kc135 check {src['source_kc135_syscheck.txt']} and kc127 check {src['source_kc127_syscheck.txt']} (1 wanted each: they refuse it); {time.time() - t0:.0f} s")
if src != want:
    refuse(f"the state is not accepted as wanted ({src}, wanted {want})")
cmd = [PY, "-u", WTM + "/d18_secant.py", "run", STUB, STATE, D, f"{LO:g}", f"{HI:g}", SEC + "/secant.jsonl", "--tol=5e-5", "--maxev=10", f"--pin={B_STATE},{B_STUB}", f"--ends={ENDS}", "--b12=rust", "--b12_threads=4"]
if DRY:
    say("DRY: would start " + " ".join(cmd) + f" > {SEC}/secant.log (cwd {WTM}, ellrs 4 threads, BelowNormal, cap {CAP} s, hc at {NOTIFY} s, PYTHONPATH {SITE}); nothing started")
    sys.exit(0)
if os.path.exists(SEC + "/secant.jsonl") or os.path.exists(SEC + "/secant.log"):
    refuse("secant.jsonl or secant.log exists")
open(SEC + "/secant_driver.pid", "w").write(str(os.getpid()))
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_kc143_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/secant_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc143d23_watch_alert_1025.py", str(os.getpid()), "secant"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "secant", str(CAP + 1800)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
p = subprocess.Popen(cmd, cwd=WTM, env=env, stdout=open(SEC + "/secant.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
say(f"secant: started pid {p.pid}: d18_secant.py run {STUB} {STATE} {D} {LO:g} {HI:g} {SEC}/secant.jsonl --tol=5e-5 --maxev=10 --pin=... --ends={ENDS} --b12=rust --b12_threads=4")
t0, notified, rc = time.time(), False, None
while rc is None:
    rc = p.poll()
    if rc is not None:
        break
    if not notified and time.time() - t0 > NOTIFY:
        notified = True
        n = sum(1 for _ in open(SEC + "/secant.jsonl")) if os.path.exists(SEC + "/secant.jsonl") else 0
        say(f"secant: still running at {NOTIFY} s (pid {p.pid}), {n} record(s) in secant.jsonl; cap {CAP} s; hc to t5")
        hc(f"the refinement (pid {p.pid}) is still running after {NOTIFY} s (6 h), {n} evaluation record(s) so far; it is killed by the exact pid at {CAP} s (12 h, your stop).")
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
hc(f"the refinement ended, {summ}. Lines as printed: " + " | ".join(lines) + ". Raw I1025-win/kc143_d23/secant after my next push; no reading by me, you rule.")
time.sleep(5)
samp.kill()
say("kc143d23_secant_driver_1025.py done")
sys.exit(0 if rc == 0 else 1)
