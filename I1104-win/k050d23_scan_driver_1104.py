#!/usr/bin/env python3
"""#1104 winb, the scan of the kappa 0.5 state at D 23.0 with the RUST block 12 (t5's order, hc of 2026-11-27 18:23 UTC and #1104 comment 7225436553; the shares are an argument): d18_secant.py scan (branch wip/ell1-rust-b12
at d4b6b6ce, committed blob 9706e506, worktree choptuik-i1102) with --b12=rust --b12_threads=2 (ellrs from my #1102 build in i1102_1025/site, on PYTHONPATH, pinned by blob; OPENBLAS_NUM_THREADS=1), on my re-solved
k_c 143 kappa 0.5 state sol_l1kc143winbk050d23_D23.0000.npy and its record (both in this folder, checked against the blobs the re-solve driver wrote into regrid_accepted.txt), at the lambda shares LISTS (semicolon-separated,
one share per process, AT MOST TWO processes (t5); a value may appear twice: a repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, 2 Rust threads per process, BelowNormal, cap 43200 s by the exact pids.
Before the scan the tool's own selftest (exit 0 wanted) and its three mutations half, norobust, nosigncheck (exit 1 wanted each), and ell_b12rs.py's selftest with --mutate=nolam and --mutate=harm (exit 0, 1, 1) are run and
logged (selftest_d18_secant.txt, selftest_ell_b12rs.txt), and read_lower.py's selftest and its two --mutate controls (exit 0, 1, 1). d18_secant.py scan checks the pins and the record system first (exit 3 if not) and appends one
JSON line per lambda (d18_hybsign.py's fields plus dln, robust, sec_parts, b12, role scan) to its own file scan_k050_D23_p<i>.jsonl. Starts only when regrid_accepted.txt exists (and names the state and record blobs) and none
of the files it would write exists. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration. Then dh170's
read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder (it reads every scan_*_p*.jsonl), and an hc to the coordinator t5 with every line it printed. The refinement (d18_secant.py run) is NOT
chained here: I read the reader's lines first (t5: the secant on the change; widen to 0.065 and 0.140 if none; more than one change is a stop), push the scan files and start it by hand.
The widening round is this same driver run by hand: "0.065;0.140" --first=2 --window=0.065,0.14 (files scan_k050_D23_p2.jsonl and p3.jsonl, logs with the suffix _w, the reader on the window of all six points).
usage: k050d23_scan_driver_1104.py LISTS [--first=N] [--window=LO,HI] [--dry [--out=DIR]]     e.g. "0.095,0.080;0.110,0.125"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR; --first=N numbers the processes and files from N, for the widening round)"""
import datetime, os, re, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1104-win"
DRYOUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
if DRYOUT and "--dry" not in sys.argv:
    print("REFUSE: --out=DIR is for --dry only"); sys.exit(2)
WT = "C:/Users/nathan/Source/choptuik-i1102"
SITE = "C:/Users/nathan/Source/i1102_1025/site"          # ellrs (my #1102 build, cp314, avx512), on PYTHONPATH
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DS = "23.0"
FIRST = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--first=")), "0"))
WINDOW = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--window=")), "")
LBL, SFX = ("scan", "") if FIRST == 0 else ("scanw", "_w")
SRC = DRYOUT or OUT          # the re-solved state, record and marker (written by k050d23_regrid_driver_1104.py)
RAWM = S + "/inputs"
SCANNER, READER = WTM + "/d18_secant.py", RAWM + "/read_lower.py"
TAG = "l1kc143winbk050d23"
STATE, REC = SRC + f"/sol_{TAG}_D23.0000.npy", SRC + f"/{TAG}.jsonl"
LOG = OUT + f"/k050d23_scan{SFX}_w.log"
CAP = 43200
B12RS_BLOB = "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef"
DRY = "--dry" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    print("usage: k050d23_scan_driver_1104.py LISTS [--first=N] [--window=LO,HI] [--dry [--out=DIR]]"); sys.exit(2)
try:
    SH = [[float(v) for v in sh.split(",")] for sh in args[0].split(";")]
except ValueError:
    print("REFUSE: the shares are not semicolon-separated comma-separated lists of numbers:", args[0]); sys.exit(2)
ALL = [v for sh in SH for v in sh]
if not 1 <= len(SH) <= 2 or any(not sh for sh in SH) or len(set(ALL)) < 2 or max(ALL.count(v) for v in ALL) > 2 or not all(0.0 < v < 10.0 for v in ALL):
    print("REFUSE: wanted 1 to 2 non-empty shares, at least two distinct values in (0, 10), none more than twice:", args[0]); sys.exit(2)
LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"
if WINDOW:
    LO, HI = [f"{float(v):g}" for v in WINDOW.split(",")]
if DRY:
    LOG = LOG + ".dry"
PINS = [(SCANNER, "9706e506111357e5e6a3f1bccd60154ac3d17cbc"), (WTM + "/ell_b12rs.py", "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef"), (SITE + "/ellrs/ellrs.cp314-win_amd64.pyd", "ddd5a08281f4aa325bd8564f08f9f2c3cebba33d"), (SITE + "/ellrs/__init__.py", "76c7cfbc8fdfe90adb0debb60ac2d4754974cb1d"), (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"), (RAWM + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da")]


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1104 kappa 0.5 k_c 143 D {DS} scan{' (widening)' if FIRST else ''} ({LO}-{HI}): {msg}"])


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
say(f"k050d23_scan_driver_1104.py: the kappa 0.5 k_c 143 hybrid scan at D {DS}, shares {args[0]}, first {FIRST}, reader window {LO} {HI}{' (dry run)' if DRY else ''}; checking pins")
mk = []
if not os.path.exists(SRC + "/regrid_accepted.txt"):
    refuse("regrid_accepted.txt does not exist", "not started: the kappa 0.5 re-solve is not accepted.")
else:
    mk = open(SRC + "/regrid_accepted.txt").read().split()
    if len(mk) < 8 or mk[0] != "ACCEPTED" or mk[4] != "state" or mk[6] != "record":
        refuse(f"regrid_accepted.txt is not an ACCEPTED marker with state and record blobs: {mk}", "not started: regrid_accepted.txt has no state and record blobs.")
    else:
        PINS += [(STATE, mk[5]), (REC, mk[7])]
for fn, want in PINS:
    got = sh(["git", "hash-object"] + ([] if fn in (SCANNER, WTM + "/ell_b12rs.py") else ["--no-filters"]) + [fn]).stdout.strip()
    if got != want:
        refuse(f"{fn} is blob {got}, not {want}", f"not started: pin {fn} is blob {got[:8]}.")
head = sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip()
SCANF = [SRC + f"/scan_k050_D23_p{i + FIRST}.jsonl" for i in range(len(SH))]     # SRC is OUT in a real run (a dry run with --out=DIR checks DIR)
if head != "d4b6b6cea24f518d38cac17877c9a0da813b05f4" or any(os.path.exists(f) for f in SCANF):
    refuse(f"worktree at {head[:8]}, not d4b6b6ce, or a scan file exists", "not started: worktree or scan file check failed.")
renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
ex0 = []
for mut in ("", "--mutate=half", "--mutate=norobust", "--mutate=nosigncheck"):
    r1 = sh([PY, "-u", SCANNER, "selftest"] + ([mut] if mut else []), cwd=WTM, env=dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1"))
    ex0.append(r1.returncode)
    open(OUT + "/selftest_d18_secant.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC d18_secant.py (d4b6b6ce, blob 9706e506) selftest {mut}\n" + r1.stdout + r1.stderr + f"exit {r1.returncode} ({0 if not mut else 1} wanted)\n")
if ex0 != [0, 1, 1, 1]:
    refuse(f"d18_secant.py selftest and its three mutations (half, norobust, nosigncheck) gave exits {ex0}, wanted [0, 1, 1, 1]", f"not started: d18_secant.py selftest/mutations exits {ex0}, wanted [0, 1, 1, 1].")
else:
    say("d18_secant.py (d4b6b6ce, blob 9706e506) selftest exit 0 and its three mutations half, norobust, nosigncheck exit 1, 1, 1 as wanted")
senv = dict(os.environ, PYTHONPATH=SITE, OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
exr = []
for mut in ("", "--mutate=nolam", "--mutate=harm"):
    rr = sh([PY, "-u", WTM + "/ell_b12rs.py", "selftest"] + ([mut] if mut else []), cwd=WTM, env=senv)
    exr.append(rr.returncode)
    open(OUT + "/selftest_ell_b12rs.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC ell_b12rs.py (blob {B12RS_BLOB[:8]}) selftest {mut}\n" + rr.stdout + rr.stderr + f"exit {rr.returncode} ({0 if not mut else 1} wanted)\n")
if exr != [0, 1, 1]:
    refuse(f"ell_b12rs.py selftest and its controls nolam, harm gave exits {exr}, wanted [0, 1, 1]", f"not started: ell_b12rs.py selftest/controls exits {exr}, wanted [0, 1, 1].")
else:
    say("ell_b12rs.py selftest exit 0 and its controls --mutate=nolam, --mutate=harm exit 1, 1 as wanted (ellrs from " + SITE + ")")
st = []
for mut in ("", "--mutate=shift", "--mutate=round2"):
    r0 = sh([PY, "-I", READER, "selftest"] + ([mut] if mut else []), cwd=OUT, env=renv0)
    st.append(r0.returncode)
    open(OUT + "/selftest_read_lower_1025.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC read_lower.py selftest {mut}\n" + r0.stdout + f"selftest {mut} exit {r0.returncode} ({0 if not mut else 1} wanted)\n")
if st != [0, 1, 1]:
    refuse(f"read_lower.py selftest and its two controls gave exits {st}, wanted [0, 1, 1]", f"not started: read_lower.py selftest/controls exits {st}, wanted [0, 1, 1].")
else:
    say("read_lower.py selftest exit 0 and its two --mutate controls exit 1, 1 as wanted")
PINARG = f"--pin={mk[5]},{mk[7]}" if len(mk) > 7 else "--pin=0,0"
cmds = [[PY, "-u", SCANNER, "scan", REC, STATE, DS, ",".join(f"{v:g}" for v in sh_), SCANF[i], PINARG, "--b12=rust", "--b12_threads=2"] for i, sh_ in enumerate(SH)]
if DRY:
    for c in cmds:
        say("DRY: would start " + " ".join(c) + f" (cwd {WTM}, ellrs 2 threads, BelowNormal, cap {CAP} s, PYTHONPATH {SITE})")
    say(f"DRY: reader window {LO} {HI}; nothing started"); sys.exit(0)
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_k050_1104.ps1", "-Drv", str(os.getpid()), "-Out", OUT + f"/rows/{LBL}_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/k050d23_watch_alert_1104.py", str(os.getpid()), LBL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1104.py", str(os.getpid()), LBL, str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM, PYTHONPATH=SITE)
procs = []
for i, c in enumerate(cmds):
    p = subprocess.Popen(c, cwd=WTM, env=env, stdout=open(OUT + f"/rows/scan_p{i + FIRST}_raw.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    procs.append(p)
    say(f"scan p{i + FIRST}: started pid {p.pid}: d18_secant.py scan {REC} {STATE} {DS} {c[7]} {SCANF[i]} {PINARG} --b12=rust --b12_threads=2")
t0, rc = time.time(), [None] * len(procs)
while any(r is None for r in rc):
    for i, p in enumerate(procs):
        if rc[i] is None:
            rc[i] = p.poll()
            if rc[i] is not None:
                say(f"scan p{i + FIRST}: pid {p.pid} ended with exit {rc[i]} after {time.time() - t0:.0f} s")
    if any(r is None for r in rc) and time.time() - t0 > CAP:
        for i, p in enumerate(procs):
            if rc[i] is None:
                r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
                say(f"scan p{i + FIRST}: CAP {CAP} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                p.wait(); rc[i] = "killed at the cap"
    elif any(r is None for r in rc):
        time.sleep(15)
say(f"all scan processes ended after {time.time() - t0:.0f} s, exits {rc}")
with open(OUT + f"/scan_k050_D23{SFX}.log", "w") as g:
    for i in range(len(procs)):
        g.write(f"== p{i + FIRST}\n")
        for ln in open(OUT + f"/rows/scan_p{i + FIRST}_raw.log", errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)
if any(r != 0 for r in rc):
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exits {rc}; 3 means the state is not the record system). Points so far in scan_k050_D23_p*.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("k050d23_scan_driver_1104.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + f"/read_lower_k050_D23{SFX}.log", "w").write(txt + f"\nread_lower exit {r.returncode}\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended ({len(procs)} exits {rc}, {time.time() - t0:.0f} s, shares {args[0]}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + ". Raw I1104-win after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("k050d23_scan_driver_1104.py done")
