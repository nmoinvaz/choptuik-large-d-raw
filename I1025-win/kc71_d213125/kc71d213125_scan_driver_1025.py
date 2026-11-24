#!/usr/bin/env python3
"""#1025 winb, lambda_1 at k_c 71 on leg 6's D 21.3125 state (t5's order, hc of 2026-11-24 ~03:47 UTC; win2's raw I1025-win2/kc71_leap, commit 5fefca16, tag l1kc71Lw1025e):
the state states/sol_l1kc71Lw1025e_D21.312500.npy (blob 8456f980) and its record states/l1kc71Lw1025e.jsonl (blob 05a5eaa2), both copied to inputs/ and pinned by blob. Before anything runs:
the pins (kc71_syscheck.py 4cd86cd4, d18_hybsign.py e089207a, d185_scan_read.py 7c9d400f, read_lower.py 89309d3c, state, record, the worktree choptuik-i1025k79 at 48c36355), the read_lower.py
selftest and its two --mutate controls (exits 0, 1, 1), and the state check: kc71_syscheck.py must ACCEPT the state (exit 0; its selftest 0) and refuse both controls (--mutate=F and --mutate=steps exit 1).
Then xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) at the lambda shares LISTS (semicolon-separated, one share per process, at most 4; a value may appear twice: the repeat),
FOUR PROCESSES (one per share), ONE thread each, BelowNormal, cap 10800 s by the exact pids; d18_hybsign.py checks the record system first (exit 3 if the state does not come back) and appends one JSON
line per lambda to its own file scan_kc71_D213125_p<i>.jsonl. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
for this driver's duration. Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder, and an hc to the coordinator t5 with every line it printed.
usage: kc71d213125_scan_driver_1025.py LISTS [--dry]     e.g. "0.785,0.800;0.790,0.805;0.795,0.810;0.800,0.815"     (--dry: runs the pins, the reader selftests and the state checks (outputs get a .dry suffix), prints the planned commands, starts no scan)"""
import datetime, os, re, subprocess, sys, time

S = "C:/Users/nathan/Source/kc71d213125_1025"
OUT = S + "/I1025-win/kc71_d213125"
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
INP = S + "/inputs"
SCANNER, READER, SYSCHK = INP + "/d18_hybsign.py", INP + "/read_lower.py", INP + "/kc71_syscheck.py"
TAG, D = "l1kc71Lw1025e", 21.3125
STATE, REC = INP + f"/sol_{TAG}_D21.312500.npy", INP + f"/{TAG}.jsonl"
LOG = OUT + "/kc71d213125_scan_w.log"
CAP = 10800
DRY = "--dry" in sys.argv
sfx = ".dry" if DRY else ""
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    print("usage: kc71d213125_scan_driver_1025.py LISTS [--dry]"); sys.exit(2)
try:
    SH = [[float(v) for v in sh.split(",")] for sh in args[0].split(";")]
except ValueError:
    print("REFUSE: the shares are not semicolon-separated comma-separated lists of numbers:", args[0]); sys.exit(2)
ALL = [v for sh in SH for v in sh]
if not 1 <= len(SH) <= 4 or any(not sh for sh in SH) or len(set(ALL)) < 2 or max(ALL.count(v) for v in ALL) > 2 or not all(0.0 < v < 10.0 for v in ALL):
    print("REFUSE: wanted 1 to 4 non-empty shares, at least two distinct values in (0, 10), none more than twice:", args[0]); sys.exit(2)
LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"
PINS = [(SYSCHK, "4cd86cd4c9001d7472fc5df625b0635e1884bf81"), (SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (INP + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (STATE, "8456f9800ed92f3d747cccde0eee1f676cc93f39"), (REC, "05a5eaa26f653d7bcf24cb2936464afb2f617809")]


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG + sfx, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 71 D 21.3125 lambda_1 scan (0.785-0.815): {msg}"])


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
say(f"kc71d213125_scan_driver_1025.py: lambda_1 at k_c 71, D 21.3125, shares {args[0]}{' (dry run)' if DRY else ''}; checking pins")
for fn, want in PINS:
    got = sh(["git", "hash-object", "--no-filters", fn]).stdout.strip()
    if got != want:
        refuse(f"{fn} is blob {got}, not {want}", f"not started: pin {fn} is blob {got[:8]}.")
head = sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip()
SCANF = [OUT + f"/scan_kc71_D213125_p{i}.jsonl" for i in range(len(SH))]
if head != "48c36355d1ba64de4e3112ed968fd6c034384551" or any(os.path.exists(f) for f in SCANF):
    refuse(f"worktree at {head[:8]}, not 48c36355, or a scan file exists", "not started: worktree or scan file check failed.")
say("pins matched (6 blobs, worktree 48c36355, no scan file yet)")
renv0 = dict(os.environ, D18_DIR=INP, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
st = []
for mut in ("", "--mutate=shift", "--mutate=round2"):
    r0 = sh([PY, "-I", READER, "selftest"] + ([mut] if mut else []), cwd=OUT, env=renv0)
    st.append(r0.returncode)
    open(OUT + "/selftest_read_lower_1025.txt" + sfx, "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC read_lower.py selftest {mut}\n" + r0.stdout + f"selftest {mut} exit {r0.returncode} ({0 if not mut else 1} wanted)\n")
if st != [0, 1, 1]:
    refuse(f"read_lower.py selftest and its two controls gave exits {st}, wanted [0, 1, 1]", f"not started: read_lower.py selftest/controls exits {st}, wanted [0, 1, 1].")
else:
    say("read_lower.py selftest exit 0 and its two --mutate controls exit 1, 1 as wanted")
if not DRY:
    samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scan_samples.csv", "-Interval", "60"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    wat = subprocess.Popen([PY, "-u", S + "/kc71d213125_watch_alert_1025.py", str(os.getpid()), "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
    kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)
# the state check: kc71_syscheck.py accepts (exit 0, selftest 0) and refuses both controls (exit 1, 1)
chk = []
for name, a in (("selftest", ["--selftest"]), ("state", [REC, STATE, "21.3125", WTM]), ("mutate_F", [REC, STATE, "21.3125", WTM, "--mutate=F"]), ("mutate_steps", [REC, STATE, "21.3125", WTM, "--mutate=steps"])):
    t1 = time.time()
    r1 = sh([PY, "-u", SYSCHK] + a, cwd=WTM, env=env)
    chk.append(r1.returncode)
    txt = "\n".join(l for l in (r1.stdout + "\n" + r1.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
    open(OUT + f"/source_syscheck_{name}.txt" + sfx, "w").write(txt + f"\nexit {r1.returncode}\n")
    say(f"kc71_syscheck.py {name}: exit {r1.returncode} ({time.time() - t1:.0f} s): {txt.splitlines()[-1][:200] if txt else ''}")
if chk != [0, 0, 1, 1]:
    refuse(f"the state check gave exits {chk} (selftest, state, --mutate=F, --mutate=steps), wanted [0, 0, 1, 1]", f"not started: kc71_syscheck.py exits {chk} (selftest, state, mutate F, mutate steps), wanted [0, 0, 1, 1]; no scan.")
else:
    say("the state check passed: the state is accepted (exit 0), selftest 0, --mutate=F and --mutate=steps exit 1, 1")
cmds = [[PY, "-u", SCANNER, REC, STATE, "21.3125", ",".join(f"{v:g}" for v in sh_), SCANF[i]] for i, sh_ in enumerate(SH)]
if DRY:
    for c in cmds:
        say("DRY: would start " + " ".join(c) + f" (cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s)")
    say(f"DRY: reader window {LO} {HI}; nothing started"); sys.exit(0)
procs = []
for i, c in enumerate(cmds):
    p = subprocess.Popen(c, cwd=WTM, env=env, stdout=open(OUT + f"/rows/scan_p{i}_raw.log", "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    procs.append(p)
    say(f"scan p{i}: started pid {p.pid}: d18_hybsign.py {REC} {STATE} 21.3125 {c[6]} {SCANF[i]}")
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
with open(OUT + "/scan_kc71_D213125.log", "w") as g:
    for i in range(len(procs)):
        g.write(f"== p{i}\n")
        for ln in open(OUT + f"/rows/scan_p{i}_raw.log", errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)
if any(r != 0 for r in rc):
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exits {rc}; 3 means the state is not the record system). Points so far in scan_kc71_D213125_p*.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("kc71d213125_scan_driver_1025.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, D18_DIR=INP, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + "/read_lower_kc71_D213125.log", "w").write(txt + f"\nread_lower exit {r.returncode}\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended (4 exits {rc}, {time.time() - t0:.0f} s, shares {args[0]}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + ". Raw I1025-win/kc71_d213125 after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc71d213125_scan_driver_1025.py done")
