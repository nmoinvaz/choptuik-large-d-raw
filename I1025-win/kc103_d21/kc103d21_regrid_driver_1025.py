#!/usr/bin/env python3
"""#1025 winb, the k_c 103 regrid at D 21.0 (t5's order, hc of 2026-11-24 ~15:47 UTC, after the k_c 95 D 21.0 ruling): my accepted k_c 95 D 21.0 state (raw I1025-win/kc95_d21 at 7b7f37628:
sol_l1kc95winbg_D21.0000.npy blob d7a4844a, l1kc95winbg.jsonl blob 2e8fe124, the marker's blobs) is regridded to k_c 103 with
  ell_refine.py l1kc95winbg 95 l1kc103winbg 103 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.1067409501 is t5's lambda_0, unused with --no-gamma)
exactly as the k_c 95 regrid (same worktree, venv, 4 threads, BelowNormal), only the source tag and k_c and the target k_c changed; cap 21600 s (t5's 6 h) by the exact pid, one process outside my terminal.
Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: kc95_syscheck_1025.py (d487e628, dh610's) and kc103_syscheck_1025.py (3ab58d16, dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, raw I1025-dh170/kc103_d21125/in/),
     d18_hybsign.py, d185_scan_read.py, read_lower.py, the k_c 95 D 21.0 state and record (inputs/ and the worktree's copies), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399,
     ell_refine.py 631e5801);
  2. the selftest of both checks (exit 0 each);
  3. the SOURCE: the k_c 95 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 103 check refuses it (exit 1);
  4. the regrid;
  5. ACCEPTED only if kc103_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc95_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc103d21_1025.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc103d21_regrid_driver_1025.py [--dry]     (--dry: pins and the two selftests only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/kc103d21_1025"
OUT = S + "/I1025-win/kc103_d21"
IN = S + "/inputs"
SRCD = IN          # my accepted k_c 95 D 21.0 state and record (raw I1025-win/kc95_d21 at 7b7f37628; copies in inputs/)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SRC, TAG = "l1kc95winbg", "l1kc103winbg"
SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D21.0000.npy", SRCD + f"/{SRC}.jsonl"
STATE_N = f"sol_{TAG}_D21.0000.npy"
LAM0 = "2.1067409501"
B_STATE, B_REC = "d7a4844a76e47c015591ac9ad839dddc14a5b2ce", "2e8fe124f24534089f6cb29dff227db5789f8e96"
PINS = [(IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"), (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, B_STATE), (SRCREC, B_REC),
        (WTM + f"/data/sol_{SRC}_D21.0000.npy", B_STATE), (WTM + f"/data/{SRC}.jsonl", B_REC)]
LOG = OUT + "/kc103_regrid_w.log" + (".dry" if DRY else "")
CAPRG = 21600
SY103, SY95 = IN + "/kc103_syscheck_1025.py", IN + "/kc95_syscheck_1025.py"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def blob(p, filters=False):
    return sh(["git", "hash-object"] + ([] if filters else ["--no-filters"]) + [p]).stdout.strip()


def hc(m):
    sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1025 k_c 103 regrid at D 21.0: {m}"])


def stop(m, code=2):
    say("STOP: " + m)
    if not DRY:
        hc("not started or stopped: " + m)
    sys.exit(code)


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


os.makedirs(OUT + "/rows", exist_ok=True)
if not DRY:
    open(OUT + "/rows/regrid_driver.pid", "w").write(str(os.getpid()))
say(f"kc103d21_regrid_driver_1025.py: the k_c 103 regrid at D 21.0 from my accepted k_c 95 D 21.0 state{' (dry run)' if DRY else ''}; checking pins")
for p, b in PINS:
    g = blob(p)
    if g != b:
        stop(f"{p} is blob {g}, not {b}")
if sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip() != "48c36355d1ba64de4e3112ed968fd6c034384551":
    stop("the worktree is not at 48c36355")
for ref, files in (("505d839940456a3d04321d75cf66cc3b5bc831c4", ["dss_ell.py", "ell_ddm.py", "ell_dd.py", "ddnp.py"]), ("48c36355d1ba64de4e3112ed968fd6c034384551", ["ell_delta.py", "ell_refine.py"])):
    if sh(["git", "-C", WT, "diff", "--quiet", ref] + ["--"] + ["solver/matter/" + f for f in files]).returncode != 0:
        stop(f"the worktree's {files} differ from {ref[:8]}")
if blob(WTM + "/ell_refine.py", filters=True) != "631e58016c3912dc0871e56791c3e3f99ce04239":
    stop("ell_refine.py is not blob 631e5801")
for f in (WTM + "/data/" + STATE_N, WTM + f"/data/{TAG}.jsonl", OUT + "/regrid_accepted.txt", OUT + "/" + STATE_N):
    if os.path.exists(f) and not DRY:
        stop(f"{f} exists")
say(f"pins ok (the inputs of {IN}, the k_c 95 D 21.0 files, worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", PYTHONFAULTHANDLER="1")
sfx = ".dry" if DRY else ""
st103, st95 = sh([PY, SY103, "--selftest"], env=env), sh([PY, SY95, "--selftest"], env=env)
open(OUT + "/selftest_kc103_syscheck.txt" + sfx, "w").write(st103.stdout + st103.stderr)
open(OUT + "/selftest_kc95_syscheck.txt" + sfx, "w").write(st95.stdout + st95.stderr)
say(f"selftests: kc103_syscheck exit {st103.returncode}, kc95_syscheck exit {st95.returncode} (0 wanted each)")
if st103.returncode != 0 or st95.returncode != 0:
    stop("a check's selftest is not 0")
if DRY:
    say(f"DRY: would start ell_refine.py {SRC} 95 {TAG} 103 1 21.0 {LAM0} --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s); nothing started")
    sys.exit(0)

samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/regrid_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc103d21_watch_alert_1025.py", str(os.getpid()), "regrid"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "regrid", str(CAPRG + 1800)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")


def finish(code, m):
    say(m)
    hc(m)
    time.sleep(70)          # the sampler's last line
    samp.kill()
    say("kc103d21_regrid_driver_1025.py done")
    sys.exit(code)


# step 3: the source, through both checks (the checks re-freeze the state: minutes each)
t0 = time.time()
src = {}
for name, cmd in (("source_kc95_syscheck.txt", [PY, SY95, SRCREC, SRCSTATE, "21.0", WTM]), ("source_kc95_syscheck_mutate_F.txt", [PY, SY95, SRCREC, SRCSTATE, "21.0", WTM, "--mutate=F"]),
                  ("source_kc95_syscheck_mutate_steps.txt", [PY, SY95, SRCREC, SRCSTATE, "21.0", WTM, "--mutate=steps"]), ("source_kc103_syscheck.txt", [PY, SY103, SRCREC, SRCSTATE, "21.0", WTM])):
    r = sh(cmd, env=env)
    open(OUT + "/" + name, "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    src[name] = r.returncode
want = {"source_kc95_syscheck.txt": 0, "source_kc95_syscheck_mutate_F.txt": 1, "source_kc95_syscheck_mutate_steps.txt": 1, "source_kc103_syscheck.txt": 1}
say(f"the source: kc95 check exit {src['source_kc95_syscheck.txt']} (0 wanted), --mutate=F {src['source_kc95_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc95_syscheck_mutate_steps.txt']} (1 wanted each), kc103 check {src['source_kc103_syscheck.txt']} (1 wanted: it refuses the source); {time.time() - t0:.0f} s")
if src != want:
    finish(1, f"the source checks are not as wanted ({src}, wanted {want}): no regrid")

# step 4: the regrid
cmd = ["-u", "ell_refine.py", SRC, "95", TAG, "103", "1", "21.0", LAM0, "--kappa", "0.7", "--u0", "0.04", "--Ks", "30", "--tol", "1e-12", "--wait", "60", "--no-gamma"]
t_start = datetime.datetime.now(datetime.timezone.utc)
open(OUT + "/regrid.log", "w").write(f"# {t_start:%Y-%m-%d %H:%M:%S} UTC cmd: {PY} {' '.join(cmd)} (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s)\n")
rc, wall = run_capped([PY] + cmd, OUT + "/rows/regrid_raw.log", CAPRG, WTM, env, "regrid")
t_end = datetime.datetime.now(datetime.timezone.utc)
with open(OUT + "/regrid.log", "a") as g:
    for ln in open(OUT + "/rows/regrid_raw.log", errors="replace"):
        if not re.search(r"RuntimeWarning|^  [a-z_]+ = |^  [a-z]+ = ", ln) and not re.match(r"^\s+(px|mx|a2|cx|ax|lt|pc|return|[a-z]+ = )", ln):
            g.write(ln)
    g.write(f"exit {rc}\n")

# step 5: acceptance
state, rec = WTM + "/data/" + STATE_N, WTM + f"/data/{TAG}.jsonl"
verdict, why = "NOT ACCEPTED", ""
if rc != 0:
    why = f"the regrid did not finish (exit {rc})"
elif not (os.path.exists(state) and os.path.getsize(state) > 0 and os.path.exists(rec) and os.path.getsize(rec) > 0):
    why = "the regrid wrote no state or record"
else:
    t0 = time.time()
    a = sh([PY, SY103, rec, state, "21.0", WTM], env=env)
    open(OUT + "/syscheck.txt", "w").write(a.stdout + a.stderr + f"exit {a.returncode}\n")
    s103 = sh([PY, SY103, "--selftest"], env=env)
    open(OUT + "/selftest_kc103_syscheck_after.txt", "w").write(s103.stdout + s103.stderr + f"exit {s103.returncode}\n")
    m1 = sh([PY, SY103, rec, state, "21.0", WTM, "--mutate=F"], env=env)
    m2 = sh([PY, SY103, rec, state, "21.0", WTM, "--mutate=steps"], env=env)
    open(OUT + "/syscheck_mutate.txt", "w").write(f"--mutate=F exit {m1.returncode} (1 wanted)\n{m1.stdout}\n--mutate=steps exit {m2.returncode} (1 wanted)\n{m2.stdout}\n")
    k95 = sh([PY, SY95, rec, state, "21.0", WTM], env=env)
    open(OUT + "/syscheck_kc95_on_result.txt", "w").write(k95.stdout + k95.stderr + f"exit {k95.returncode}\n")
    say(f"result: kc103 check exit {a.returncode} (0 wanted), its selftest {s103.returncode} (0 wanted), --mutate=F {m1.returncode}, --mutate=steps {m2.returncode} (1 wanted each), kc95 check on the result {k95.returncode} (1 wanted: it refuses); {time.time() - t0:.0f} s")
    if (a.returncode, s103.returncode, m1.returncode, m2.returncode, k95.returncode) == (0, 0, 1, 1, 1):
        verdict = "ACCEPTED"
        shutil.copy(state, OUT + "/" + STATE_N)
        shutil.copy(rec, OUT + f"/{TAG}.jsonl")
        shutil.copy(IN + "/read_lower.py", OUT + "/read_lower.py")
        open(OUT + "/regrid_accepted.txt", "w").write(f"ACCEPTED {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC\nstate {blob(OUT + '/' + STATE_N)}\nrecord {blob(OUT + f'/{TAG}.jsonl')}\n")
    else:
        why = "syscheck: " + (a.stdout.strip().splitlines() or [''])[-1]

# the sampler's CSV: peak memory of the regrid stage
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
srcj = [json.loads(x) for x in open(SRCREC) if x.strip() and json.loads(x).get("D") == 21.0][-1]
dd = (recj["Delta"] - srcj["Delta"]) if recj.get("Delta") is not None else None
sratio = (recj["steps"] / srcj["steps"]) if recj.get("steps") and srcj.get("steps") else None
summ = (f"regrid {t_start:%Y-%m-%d %H:%M:%S} to {t_end:%H:%M:%S} UTC, exit {rc}, wall {wall:.0f} s (record's seconds {recj.get('seconds')}); record: |F| {recj.get('F')}, F_start {recj.get('F_start')}, "
        f"steps {recj.get('steps')}, constraint {recj.get('constraint')}, Delta {recj.get('Delta')}; the k_c 95 source record at D 21.0: |F| {srcj.get('F')}, steps {srcj.get('steps')}, constraint {srcj.get('constraint')}, Delta {srcj.get('Delta')}; "
        f"Delta(k_c 103) minus Delta(k_c 95) = {dd}; steps ratio {sratio} (k_c 87 to 95 at D 21.0: 3219/2948 = 1.092); {verdict}{(': ' + why) if why else ''}; "
        f"peak working set {pk['ws']:.2f} GB, peak private {pk['priv']:.2f} GB (the largest python of the tree, {pk['n']} samples), lowest free memory {pk['free']:.2f} GB, peak commit {pk['commit']:.1f} GB, cpu {pk['cpu']:.0f} s")
open(OUT + "/regrid_summary.txt", "w").write(summ + "\n")
say(summ)
hc(f"finished: {summ}. Raw I1025-win/kc103_d21 after my next push. " + ("The scan 0.905-0.925 by 0.005 plus a repeat of 0.915 (6 evaluations, 4 processes) starts by itself now." if verdict == "ACCEPTED" else "No scan."))
time.sleep(5)
samp.kill()
say("kc103d21_regrid_driver_1025.py done")
sys.exit(0 if verdict == "ACCEPTED" else 1)
