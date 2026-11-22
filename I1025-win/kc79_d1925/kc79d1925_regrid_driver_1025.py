#!/usr/bin/env python3
"""#1025 winb, the k_c 79 regrid at D 19.25 (t5's order, hc of 2026-11-22 ~16:10 UTC): win2's accepted k_c 71 D 19.25 state (from its leap, raw I1025-win2/kc71_leap, found by prep_kc79d1925_find_1025.py) is
regridded to k_c 79 with the same command as at D 19 (raw I1025-win/kc79_d19), only D, the output tag and the lambda_0 argument changed:
  D 19:    ell_refine.py SRC 71 l1kc79W19m1025 79 1 19 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
  D 19.25: ell_refine.py SRC 71 l1kc79W1925m1025 79 1 19.25 2.1144367878 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (SRC and the pins from kc79d1925_cfg_1025.txt; lambda_0 unused with --no-gamma)
4 threads, BelowNormal, cap 21600 s by the exact pid. Accepted only by kc79_syscheck_1025.py (win2's kc71_syscheck rule with k_c 71 replaced by k_c 79) and its two controls (|F| x 1.5 and steps + 1
refused, on the same numbers and through --mutate). Before the regrid win2's own check must accept the k_c 71 source state on this machine. A refusal, a failed control or a regrid that does not
converge stops here with a report. NO SCAN IS STARTED (the window comes from the coordinator); kc79d1925_scan_driver_1025.py takes it as an argument. Memory: no guard, the alert-only watcher is a separate process.
usage: kc79d1925_regrid_driver_1025.py [--selftest]"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/kc79d1925_1025"
OUT = S + "/I1025-win/kc79_d1925"
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
RAW = S + "/raw"
ST = "--selftest" in sys.argv          # the cap selftest needs no source state
CFG = {"SRC": "none"} if ST else dict(l.strip().split("=", 1) for l in open(S + "/kc79d1925_cfg_1025.txt") if "=" in l and not l.startswith("#"))
SRC, TAG = CFG["SRC"], "l1kc79W1925m1025"
STATE_N = f"sol_{TAG}_D19.2500.npy"
PINS = {} if ST else {p: b for b, p in (ln.split() for ln in open(S + "/prep_kc79d1925_pins_1025.txt"))}
LOG = OUT + "/kc79_regrid_w.log"
CAPRG = 21600
BLK = "BELOW"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def blob(p, filters=False):
    return sh(["git", "hash-object"] + ([] if filters else ["--no-filters"]) + [p]).stdout.strip()


def run_capped(cmd, logf, cap, cwd, env, tag):
    """start BelowNormal without a window, poll every 15 s, kill by the exact pid at the cap; returns (exit code or 'killed at the cap', seconds)"""
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=open(logf, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    say(f"{tag}: started pid {p.pid}: {' '.join(cmd)[:400]} > {logf}")
    t0 = time.time()
    while True:
        rc = p.poll()
        if rc is not None:
            say(f"{tag}: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
            return rc, time.time() - t0
        if time.time() - t0 > cap:
            r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
            say(f"{tag}: CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
            p.wait()
            return "killed at the cap", time.time() - t0
        time.sleep(15)


if "--selftest" in sys.argv:
    LOG = S + "/kc79_regrid_driver_selftest.log"
    if os.path.exists(LOG):
        os.remove(LOG)
    rc, _ = run_capped([PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"], S + "/kc79_selftest_cap.log", 20, S, dict(os.environ), "cap test")
    time.sleep(2)
    left = sh(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"]).stdout.strip()
    ok = rc == "killed at the cap" and left == "0"
    say(f"selftest: {rc}; dummy processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    sys.exit(0 if ok else 1)

os.makedirs(OUT + "/rows", exist_ok=True)
open(OUT + "/rows/regrid_driver.pid", "w").write(str(os.getpid()))
say("kc79d1925_regrid_driver_1025.py: the k_c 79 regrid at D 19.25; checking pins")
bad = 0
for p, b in PINS.items():
    g = blob(f"{RAW}/{p}")
    if g != b:
        say(f"REFUSE: {p} is blob {g}, not {b}")
        bad = 1
if bad:
    sys.exit(2)
if sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip() != "48c36355d1ba64de4e3112ed968fd6c034384551":
    say("REFUSE: the worktree is not at 48c36355"); sys.exit(2)
for ref, files in (("505d839940456a3d04321d75cf66cc3b5bc831c4", ["dss_ell.py", "ell_ddm.py", "ell_dd.py", "ddnp.py"]), ("48c36355d1ba64de4e3112ed968fd6c034384551", ["ell_delta.py", "ell_refine.py"])):
    if sh(["git", "-C", WT, "diff", "--quiet", ref] + ["--"] + ["solver/matter/" + f for f in files]).returncode != 0:
        say(f"REFUSE: the worktree's {files} differ from {ref[:8]}"); sys.exit(2)
if blob(WTM + "/ell_refine.py", filters=True) != "631e58016c3912dc0871e56791c3e3f99ce04239":
    say("REFUSE: ell_refine.py is not blob 631e5801"); sys.exit(2)
if blob(WTM + f"/data/sol_{SRC}_D19.2500.npy") != PINS[CFG["SRCSTATE"]]:
    say("REFUSE: the source state in the worktree is not the pinned blob " + PINS[CFG["SRCSTATE"]][:8]); sys.exit(2)
for f in (WTM + "/data/" + STATE_N, WTM + f"/data/{TAG}.jsonl"):
    if os.path.exists(f):
        say(f"REFUSE: {f} exists"); sys.exit(2)
say(f"pins ok (blobs in prep_kc79d1925_pins_1025.txt; worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")

samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/regrid_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc79d1925_watch_alert_1025.py", str(os.getpid()), "regrid"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing; stop it by that pid only); sampler pid {samp.pid}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", PYTHONFAULTHANDLER="1")
SY = S + "/kc79_syscheck_1025.py"
SY71 = RAW + "/" + CFG["SRCCHECK"]

# controls: the check's own selftest, then win2's original check on win2's accepted k_c 71 state (must accept on this machine)
r = sh([PY, SY, "--selftest"], env=env)
open(OUT + "/selftest_syscheck79.txt", "w").write(r.stdout + r.stderr)
say(f"selftest of kc79_syscheck_1025.py: exit {r.returncode} (0 wanted)")
t0 = time.time()
r2 = sh([PY, SY71, RAW + "/" + CFG["SRCREC"], WTM + f"/data/sol_{SRC}_D19.2500.npy", "19.25", WTM], env=env)
open(OUT + "/control_kc71_syscheck.txt", "w").write(r2.stdout + r2.stderr)
say(f"control: win2's kc71_syscheck.py on win2's k_c 71 D 19.25 state: exit {r2.returncode} (0 wanted), {time.time() - t0:.0f} s")
if r.returncode != 0 or r2.returncode != 0:
    say("a control is wrong: stop, no regrid")
    time.sleep(70); samp.kill(); sys.exit(1)

# part 1: the regrid
cmd = ["-u", "ell_refine.py", SRC, "71", TAG, "79", "1", "19.25", "2.1144367878", "--kappa", "0.7", "--u0", "0.04", "--Ks", "30", "--tol", "1e-12", "--wait", "60", "--no-gamma"]
t_start = datetime.datetime.now(datetime.timezone.utc)
open(OUT + "/regrid.log", "w").write(f"# {t_start:%Y-%m-%d %H:%M:%S} UTC cmd: {PY} {' '.join(cmd)} (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s)\n")
rc, wall = run_capped([PY] + cmd, OUT + "/rows/regrid_raw.log", CAPRG, WTM, env, "regrid")
t_end = datetime.datetime.now(datetime.timezone.utc)
with open(OUT + "/regrid.log", "a") as g:
    for ln in open(OUT + "/rows/regrid_raw.log", errors="replace"):
        if not re.search(r"RuntimeWarning|^  [a-z_]+ = |^  [a-z]+ = ", ln) and not re.match(r"^\s+(px|mx|a2|cx|ax|lt|pc|return|[a-z]+ = )", ln):
            g.write(ln)
    g.write(f"exit {rc}\n")

state, rec = WTM + "/data/" + STATE_N, WTM + f"/data/{TAG}.jsonl"
verdict, why = "NOT ACCEPTED", ""
if rc != 0:
    why = f"the regrid did not finish (exit {rc})"
elif not (os.path.exists(state) and os.path.getsize(state) > 0 and os.path.exists(rec) and os.path.getsize(rec) > 0):
    why = "the regrid wrote no state or record"
else:
    t0 = time.time()
    a = sh([PY, SY, rec, state, "19.25", WTM], env=env)
    open(OUT + "/syscheck.txt", "w").write(a.stdout + a.stderr)
    m1 = sh([PY, SY, rec, state, "19.25", WTM, "--mutate=F"], env=env)
    m2 = sh([PY, SY, rec, state, "19.25", WTM, "--mutate=steps"], env=env)
    open(OUT + "/syscheck_mutate.txt", "w").write(f"--mutate=F exit {m1.returncode} (1 wanted)\n{m1.stdout}\n--mutate=steps exit {m2.returncode} (1 wanted)\n{m2.stdout}\n")
    say(f"syscheck: exit {a.returncode} (0 wanted); controls --mutate=F exit {m1.returncode}, --mutate=steps exit {m2.returncode} (1 wanted each); {time.time() - t0:.0f} s")
    if a.returncode == 0 and m1.returncode == 1 and m2.returncode == 1:
        verdict = "ACCEPTED"
        shutil.copy(state, OUT + "/" + STATE_N)
        shutil.copy(rec, OUT + f"/{TAG}.jsonl")
        open(OUT + "/regrid_accepted.txt", "w").write(f"ACCEPTED {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC\n")
    else:
        why = "syscheck: " + (a.stdout.strip().splitlines() or [''])[-1]

# peak memory from the sampler's CSV (python processes of this driver's tree, stage regrid), the sampler has a line every 60 s and the peaks are the process counters
time.sleep(65)
pk = dict(ws=0.0, priv=0.0, free=1e9, commit=0.0, cpu=0.0, n=0)
try:
    for row in csv.DictReader(open(OUT + "/rows/regrid_samples.csv")):
        if row["stage"] == "regrid":
            pk["n"] += 1
            pk["ws"] = max(pk["ws"], float(row["ws_peak_gb"])); pk["priv"] = max(pk["priv"], float(row["private_peak_gb"]))
            pk["free"] = min(pk["free"], float(row["free_phys_gb"])); pk["commit"] = max(pk["commit"], float(row["commit_gb"])); pk["cpu"] = max(pk["cpu"], float(row["cpu_s"]))
except Exception as e:
    say(f"sampler csv: {e}")
recj = json.loads(open(rec).read().strip().splitlines()[-1]) if os.path.exists(rec) and os.path.getsize(rec) > 0 else {}
try:
    srcj = [json.loads(x) for x in open(RAW + "/" + CFG["SRCREC"]) if x.strip() and json.loads(x).get("D") == 19.25][-1]
except Exception:
    srcj = {}
summ = (f"regrid {t_start:%Y-%m-%d %H:%M:%S} to {t_end:%H:%M:%S} UTC, exit {rc}, wall {wall:.0f} s (record's seconds {recj.get('seconds')}); record: |F| {recj.get('F')}, F_start {recj.get('F_start')}, "
        f"steps {recj.get('steps')}, constraint {recj.get('constraint')}, Delta {recj.get('Delta')}; the k_c 71 source record at D 19.25: |F| {srcj.get('F')}, steps {srcj.get('steps')}, constraint {srcj.get('constraint')}, Delta {srcj.get('Delta')}; {verdict}{(': ' + why) if why else ''}; "
        f"peak working set {pk['ws']:.2f} GB, peak private {pk['priv']:.2f} GB (the largest python of the tree, {pk['n']} samples), lowest free memory {pk['free']:.2f} GB, peak commit {pk['commit']:.1f} GB, cpu {pk['cpu']:.0f} s")
open(OUT + "/regrid_summary.txt", "w").write(summ + "\n")
say(summ)
sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1025 k_c 79 regrid at D 19.25 finished: {summ}. Raw I1025-win/kc79_d1925 after my next push. "
    + ("The scan is NOT started: it waits for your window." if verdict == "ACCEPTED" else "No scan.")])
samp.kill()
say("scan not started: the window is the coordinator's to give (kc79d1925_scan_driver_1025.py WINDOW)")
say("kc79d1925_regrid_driver_1025.py done")
sys.exit(0 if verdict == "ACCEPTED" else 1)
