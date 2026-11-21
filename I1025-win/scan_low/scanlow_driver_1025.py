#!/usr/bin/env python3
"""#1025 winb, the low-lambda scans (the coordinator's order, hc 2026-11-21 about 18:15 UTC, and his correction of 18:16 and 18:2x): where the root that crossed lambda 1.20
went. Exactly xfkappa's (ii) (lane_d18f.sh, blob below): per state, d18_hybsign.py REC STATE D LAMS OUT (blob e089207a) at the 12 points 1.00 to 1.55 at 0.05; then
d18f_read.py refine (blob 5fb96dce) gives the 0.01 points inside each bracket with a sign change, and d18_hybsign.py runs them; then d18f_read.py window reads the
merged points (a change counts only if both of its grid points are noise-robust; its position is the four-estimator range; ln|det| minima without a change are listed).
No bisection and no further 0.01 points (the correction). Two states, one process each, in parallel: D 18.0625 (leap state, blob f2307f0e) and D 18 (winb's state, blob
45e72c6a), 4 threads each, BelowNormal, every child capped at 6 h (21600 s) and killed at the cap by its exact pid (taskkill /PID <pid> /T /F). More than 4 brackets
(or none) at the refine step: the refine exits 4; none goes straight to the reading, more than 4 stops that state and is reported (as in (ii)).
After both states: read_scanlow_1025.py applies the coordinator's readings. usage: scanlow_driver_1025.py [--selftest]"""
import datetime, os, re, subprocess, sys, threading, time

OUT = "C:/Users/nathan/Source/scanlow_1025/I1025-win/scan_low"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT_H = "C:/Users/nathan/Source/choptuik-i1025-lowd"       # 505d8399: d18_hybsign's solver code (the P4 rows', the D 18.125 scan's)
WT_D = "C:/Users/nathan/Source/choptuik-i1025d"          # 48c36355: ell_delta.py for the readers (xfkappa's lane pins it)
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
RAW = "C:/Users/nathan/Source/scanlow_1025/raw/I1025-mac/d18"
RAW_W = "C:/Users/nathan/Source/scanlow_1025/raw/I1025-win/out"
SCANNER, READER, REF = RAW + "/d18_hybsign.py", RAW + "/d18f_read.py", RAW + "/d18_refsign_1025.jsonl"
STATES = [("D18.0625", "18.0625", RAW + "/sol_l1kc63Wm1025_D18.062500.npy", RAW + "/l1kc63Wm1025.jsonl", "f2307f0e8ffb4621b61f74450a920c652981d973"),
          ("D18", "18.0", RAW_W + "/sol_l1kc63W1025_D18.000000.npy", RAW_W + "/l1kc63W1025.jsonl", "45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21")]
PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "5fb96dceb427e965b830b42db5b8f30255f20532"), (REF, "3e2d8b4e8f72943983fab091730629464b04e854"),
        (RAW + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (RAW + "/d18c_read.py", "1383470feaa976e4185e423626a0d5fec328de86"),
        (RAW + "/d18d_read.py", "6b6089034738a45c8dc9e6831a1654c1bac4ed18"), (STATES[0][3], "08f4dbf367edba55814e5cf989ccd32a9a5dbe67"),
        (STATES[1][3], "c33039dfa38b495486fb3ef7da77077d43db775a")] + [(s[2], s[4]) for s in STATES]
LOG, CAP, LO, HI = OUT + "/scanlow_w.log", 21600, "1.00", "1.55"
lock = threading.Lock()


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    with lock:
        print(line, flush=True)
        open(LOG, "a").write(line + "\n")


def run_capped(cmd, logf, cap, cwd, env, tag):
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=open(logf, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    say(f"{tag}: started pid {p.pid}: {' '.join(cmd)[:360]} > {logf}")
    t0 = time.time()
    while True:
        rc = p.poll()
        if rc is not None:
            say(f"{tag}: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
            return rc
        if time.time() - t0 > cap:
            r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
            say(f"{tag}: CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
            p.wait()
            return "killed at the cap"
        time.sleep(10)


def filtered(raw, dst):
    with open(dst, "w") as g:
        for ln in open(raw, errors="replace"):
            if not re.search(r"Warning|^  [a-z]+ = ", ln):
                g.write(ln)


def reader(args, tag, logf):
    env = dict(os.environ, PYTHONPATH=WT_D + "/solver/matter", PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
    r = subprocess.run([PY, READER] + args, cwd=WT_D + "/solver/matter", env=env, capture_output=True, text=True)
    txt = "\n".join(l for l in (r.stdout + "\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return "))
    open(logf, "w").write(txt + "\n")
    return r.returncode, r.stdout.strip(), txt


def worker(st, result):
    tag, D, state, rec, blob = st
    low, fine = OUT + f"/scan_{tag}_coarse_1025.jsonl", OUT + f"/scan_{tag}_fine_1025.jsonl"
    env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1",
               P4_WT_MATTER=WT_H + "/solver/matter")
    L = ",".join(f"{1.00 + 0.05 * i:.2f}" for i in range(12))
    say(f"{tag}: coarse: d18_hybsign.py {rec} {state} {D} {L} {low}")
    rc = run_capped([PY, "-u", SCANNER, rec, state, D, L, low], OUT + f"/rows/scan_{tag}_coarse_raw.log", CAP, WT_H + "/solver/matter", env, tag)
    filtered(OUT + f"/rows/scan_{tag}_coarse_raw.log", OUT + f"/scan_{tag}_coarse.log")
    if rc != 0:
        say(f"{tag}: STOP: the coarse scan did not finish (exit {rc}; 3 = not the record system); the points so far are in {low}")
        result[tag] = "stopped at the coarse scan"
        return
    rrc, out, txt = reader(["refine", D, LO, HI, f"{REF},{low}"], tag, OUT + f"/rows/refine_{tag}.log")
    if rrc == 0:
        P = out.splitlines()[-1]
        say(f"{tag}: refine: the 0.01 points inside the brackets with a sign change: {P}")
        rc = run_capped([PY, "-u", SCANNER, rec, state, D, P, fine], OUT + f"/rows/scan_{tag}_fine_raw.log", CAP, WT_H + "/solver/matter", env, tag)
        filtered(OUT + f"/rows/scan_{tag}_fine_raw.log", OUT + f"/scan_{tag}_fine.log")
        if rc != 0:
            say(f"{tag}: STOP: the fine scan did not finish (exit {rc}); the points so far are in {fine}")
            result[tag] = "stopped at the fine scan"
            return
        files = [low, fine]
    else:
        m = re.search(r"refine: (\d+) brackets", txt)
        n = int(m.group(1)) if m else -1
        say(f"{tag}: refine exit {rrc}: {n} brackets with a sign change at 0.05 ({txt.strip()[:200]})")
        if n != 0:
            say(f"{tag}: STOP: more than 4 brackets (or the refine failed): the coordinator rules; no fine scan, no reading")
            result[tag] = "stopped at the refine"
            return
        say(f"{tag}: no bracket with a sign change over 1.00-1.55 at 0.05: no fine scan, straight to the reading")
        files = [low]
    for suffix, fl in (("", [REF] + files), ("_noref", files)):
        rrc, out, txt = reader(["window", D, LO, HI, ",".join(fl)], tag, OUT + f"/read_{tag}{suffix}.log")
        say(f"{tag}: window reading{' (without the check file)' if suffix else ' (as in (ii), with the check file)'}: exit {rrc}")
        for ln in txt.splitlines():
            say(f"{tag}: {ln}")
    result[tag] = "done"


if "--selftest" in sys.argv:
    LOG = HERE + "/scanlow_driver_selftest.log"
    if os.path.exists(LOG):
        os.remove(LOG)
    quick = [PY, "-c", "import time; print('quick', flush=True); time.sleep(8)"]
    slow = [PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"]
    res = {}
    ths = [threading.Thread(target=lambda c=c, n=n: res.__setitem__(n, run_capped(c, HERE + f"/scanlow_selftest_{n}.log", 25, HERE, dict(os.environ), n))) for c, n in ((quick, "quick"), (slow, "slow"))]
    [t.start() for t in ths]; [t.join() for t in ths]
    time.sleep(3)
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"],
                          capture_output=True, text=True).stdout.strip()
    ok = res == {"quick": 0, "slow": "killed at the cap"} and left == "0"
    say(f"selftest: {res}; dummy processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    sys.exit(0 if ok else 1)

say("scanlow_driver_1025.py: the low-lambda scans on D 18.0625 and D 18; checking pins")
for fn, want in PINS:
    got = subprocess.run(["git", "hash-object", "--no-filters", fn], capture_output=True, text=True).stdout.strip()
    if got != want:
        say(f"REFUSE: {fn} is blob {got}, not {want}")
        sys.exit(2)
for wt, c in ((WT_H, "505d839940456a3d04321d75cf66cc3b5bc831c4"), (WT_D, "48c36355d1ba64de4e3112ed968fd6c034384551")):
    h = subprocess.run(["git", "-C", wt, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if h != c:
        say(f"REFUSE: {wt} is at {h}, not {c}")
        sys.exit(2)
if any(os.path.exists(OUT + f"/scan_{s[0]}_{k}_1025.jsonl") for s in STATES for k in ("coarse", "fine")):
    say("REFUSE: a scan file exists")
    sys.exit(2)
os.makedirs(OUT + "/rows", exist_ok=True)
say("pins ok; two workers, one per state; sampler every 60 s into rows/scanlow_samples.csv")
samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", HERE + "/sample_driver3_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scanlow_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
res = {}
ths = [threading.Thread(target=worker, args=(s, res)) for s in STATES]
[t.start() for t in ths]; [t.join() for t in ths]
say(f"both workers ended: {res}")
r = subprocess.run([PY, HERE + "/read_scanlow_1025.py", OUT + "/read_D18.0625.log", OUT + "/read_D18.log"], capture_output=True, text=True)
open(OUT + "/read_scanlow_1025.log", "w").write(r.stdout + r.stderr)
for ln in r.stdout.splitlines():
    say(ln)
time.sleep(70)          # the sampler's last line
samp.kill()
say("scanlow_driver_1025.py done")
