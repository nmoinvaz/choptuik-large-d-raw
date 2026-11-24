#!/usr/bin/env python3
"""#1025 winb, lambda_1 at k_c 87 on a state of dh370's k_c 87 leg (t5's order, hc of 2026-11-24 ~07:22 UTC; raw I1025-dh370/kc87_leg, tag l1kc87Ldh370; the leg's states go round
dh170, macm3 and me). Which state is in point.json (D, the raw commit, the state file and the blobs of the state and the record), pinned by blob. Before anything runs:
the pins (kc87_syscheck_1025.py 6df5d960, kc79_syscheck_1025.py 29dce7ea, d18_hybsign.py e089207a, d185_scan_read.py 7c9d400f, read_lower.py 89309d3c, the state, the record, the worktree
choptuik-i1025k79 at 48c36355), the read_lower.py selftest and its two --mutate controls (exits 0, 1, 1), and the state check: both selftests exit 0, kc87_syscheck_1025.py must ACCEPT the state (exit 0),
refuse both controls (--mutate=F and --mutate=steps exit 1) and kc79_syscheck_1025.py must refuse the state (exit 1).
Then xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) at the lambda shares LISTS (semicolon-separated, one share per process, at most 4; a value may appear twice: the repeat),
FOUR PROCESSES (one per share), ONE thread each, BelowNormal, cap 10800 s by the exact pids; d18_hybsign.py checks the record system first (exit 3 if the state does not come back) and appends one JSON
line per lambda to its own file scan_kc87_D<D>_p<i>.jsonl. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
for this driver's duration. Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder, and an hc to the coordinator t5 with every line it printed.
usage: kc87_scan_driver_1025.py LISTS [--dry]     e.g. "0.870,0.885;0.875,0.890;0.880,0.895;0.885,0.900"     (--dry: runs the pins, the reader selftests and the state checks (outputs get a .dry suffix),
prints the planned commands, starts no scan)"""
import datetime, json, os, re, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
PT = json.load(open(S + "/point.json"))
DS = PT["D"]                                  # e.g. "21.09375"
D = float(DS)
DT = DS.replace(".", "")                      # file tag, e.g. 2109375
OUT = S + "/I1025-win/kc87_leg_lambda/" + DS
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
INP = S + "/inputs"
SCANNER, READER = INP + "/d18_hybsign.py", INP + "/read_lower.py"
SYS87, SYS79 = INP + "/kc87_syscheck_1025.py", INP + "/kc79_syscheck_1025.py"
TAG = "l1kc87Ldh370"
STATE, REC = INP + "/" + PT["state_file"], INP + f"/{TAG}.jsonl"
LOG = OUT + "/kc87_scan_w.log"
CAP = 10800
DRY = "--dry" in sys.argv
sfx = ".dry" if DRY else ""
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    print("usage: kc87_scan_driver_1025.py LISTS [--dry]"); sys.exit(2)
try:
    SH = [[float(v) for v in sh.split(",")] for sh in args[0].split(";")]
except ValueError:
    print("REFUSE: the shares are not semicolon-separated comma-separated lists of numbers:", args[0]); sys.exit(2)
ALL = [v for sh in SH for v in sh]
if not 1 <= len(SH) <= 4 or any(not sh for sh in SH) or len(set(ALL)) < 2 or max(ALL.count(v) for v in ALL) > 2 or not all(0.0 < v < 10.0 for v in ALL):
    print("REFUSE: wanted 1 to 4 non-empty shares, at least two distinct values in (0, 10), none more than twice:", args[0]); sys.exit(2)
LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"
PINS = [(SYS87, "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (SYS79, "29dce7eab9677e568566a8ba05d7073109296a69"), (SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"),
        (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"), (INP + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"),
        (STATE, PT["state_blob"]), (REC, PT["record_blob"])]


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG + sfx, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(msg):
    sh([HC, "send", COORD, f"winb ({now():%H:%M} UTC), #1025 k_c 87 D {DS} lambda_1 scan ({LO}-{HI}): {msg}"])


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
say(f"kc87_scan_driver_1025.py: lambda_1 at k_c 87, D {DS}, shares {args[0]}{' (dry run)' if DRY else ''}; checking pins")
for fn, want in PINS:
    got = sh(["git", "hash-object", "--no-filters", fn]).stdout.strip()
    if got != want:
        refuse(f"{fn} is blob {got}, not {want}", f"not started: pin {fn} is blob {got[:8]}.")
head = sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip()
SCANF = [OUT + f"/scan_kc87_D{DT}_p{i}.jsonl" for i in range(len(SH))]
if head != "48c36355d1ba64de4e3112ed968fd6c034384551" or any(os.path.exists(f) for f in SCANF):
    refuse(f"worktree at {head[:8]}, not 48c36355, or a scan file exists", "not started: worktree or scan file check failed.")
say(f"pins matched ({len(PINS)} blobs, worktree 48c36355, no scan file yet)")
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
    wat = subprocess.Popen([PY, "-u", S + "/kc87_watch_alert_1025.py", str(os.getpid()), "scan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
    kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)
# the state check: both selftests 0; kc87_syscheck accepts (0); its controls refuse (1, 1); kc79_syscheck refuses the state (1)
chk = []
for name, script, a in (("selftest_kc87", SYS87, ["--selftest"]), ("selftest_kc79", SYS79, ["--selftest"]), ("state", SYS87, [REC, STATE, DS, WTM]),
                        ("mutate_F", SYS87, [REC, STATE, DS, WTM, "--mutate=F"]), ("mutate_steps", SYS87, [REC, STATE, DS, WTM, "--mutate=steps"]),
                        ("kc79_refuses", SYS79, [REC, STATE, DS, WTM])):
    t1 = time.time()
    r1 = sh([PY, "-u", script] + a, cwd=WTM, env=env)
    chk.append(r1.returncode)
    txt = "\n".join(l for l in (r1.stdout + "\n" + r1.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
    open(OUT + f"/source_syscheck_{name}.txt" + sfx, "w").write(txt + f"\nexit {r1.returncode}\n")
    say(f"{os.path.basename(script)} {name}: exit {r1.returncode} ({time.time() - t1:.0f} s): {txt.splitlines()[-1][:200] if txt else ''}")
WANT = [0, 0, 0, 1, 1, 1]
if chk != WANT:
    refuse(f"the state check gave exits {chk} (selftest 87, selftest 79, state, --mutate=F, --mutate=steps, kc79 on the state), wanted {WANT}",
           f"not started: state check exits {chk} (selftest 87, selftest 79, state, mutate F, mutate steps, kc79 on the state), wanted {WANT}; no scan.")
else:
    say("the state check passed: both selftests 0, the state accepted by kc87_syscheck (exit 0), --mutate=F and --mutate=steps exit 1, 1, kc79_syscheck refuses the state (exit 1)")
cmds = [[PY, "-u", SCANNER, REC, STATE, DS, ",".join(f"{v:g}" for v in sh_), SCANF[i]] for i, sh_ in enumerate(SH)]
if DRY:
    for c in cmds:
        say("DRY: would start " + " ".join(c) + f" (cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s)")
    say(f"DRY: reader window {LO} {HI}; nothing started"); sys.exit(0)
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
with open(OUT + f"/scan_kc87_D{DT}.log", "w") as g:
    for i in range(len(procs)):
        g.write(f"== p{i}\n")
        for ln in open(OUT + f"/rows/scan_p{i}_raw.log", errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)
if any(r != 0 for r in rc):
    say(f"the scan did not finish ({rc}; 3 = not the record system): no reading")
    hc(f"the scan did NOT finish (exits {rc}; 3 means the state is not the record system). Points so far in scan_kc87_D{DT}_p*.jsonl. No reading.")
    time.sleep(70); samp.kill(); say("kc87_scan_driver_1025.py done (no reading)"); sys.exit(1)
renv = dict(os.environ, D18_DIR=INP, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + f"/read_lower_kc87_D{DT}.log", "w").write(txt + f"\nread_lower exit {r.returncode}\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended ({len(procs)} exits {rc}, {time.time() - t0:.0f} s, shares {args[0]}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + f". Raw I1025-win/kc87_leg_lambda/{DS} after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc87_scan_driver_1025.py done")
