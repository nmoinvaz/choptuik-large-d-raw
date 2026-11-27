#!/usr/bin/env python3
"""#1104 winb, the kappa 0.5 re-solve of my k_c 143 D 23.0 state (t5's order, #1104 comment 7225436553 of 2026-11-27 18:23 UTC): my accepted k_c 143 kappa 0.7 state at D 23.0 (raw I1025-win/kc143_d23:
sol_l1kc143winbd23_D23.0000.npy blob 866c434b, l1kc143winbd23.jsonl blob 88f0be8b) is re-solved on this Windows machine at kappa 0.5 with
  ell_refine.py l1kc143winbd23 143 l1kc143winbk050d23 143 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.0992182200 is lambda_0(23.0), unused with --no-gamma; checked below)
with the worktree, settings and threads of my k_c 143 regrid (worktree choptuik-i1025k79 at 48c36355, ell_refine.py 631e5801, venv, 4 threads, BelowNormal), only --kappa 0.5, the source (my k_c 143 record and state) and the
new tag (k050) changed. The cap is 64800 s (t5's hc of 2026-11-27 18:27 UTC; the order said the same cap as my regrid, 43200 s, and t5 raised it after my estimate of about 44000 s) by the exact pid, with one hc to t5 at
21600 s (6 h) if it is still running; nothing is stopped at 6 h. If a file cap_seconds.txt (one integer) exists in the output folder, the cap is read from it at every poll (only on t5's word; each change is logged).
Order of the driver (any failure stops it with an hc to t5, no re-solve, exit 2 or 1):
  1. pins: kc127_syscheck_1025.py (898ebefa), kc135_syscheck_1025.py (b353d466), kc143_syscheck_1025.py (e15b0ee2), gate_k050_1104.py (d145145e), d18_hybsign.py, d185_scan_read.py, read_lower.py, my k_c 143 kappa 0.7
     state and record (inputs/ and the worktree's copies in solver/matter/data/), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399, ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(23.0) = 2.0992182200;
  3. the SOURCE: the k_c 143 check accepts it (exit 0), its --mutate=F and --mutate=steps exit 1; the k_c 135 and k_c 127 checks refuse it (exit 1 each); the kappa 0.5 gate refuses it (exit 1: kappa 0.7, 4705 steps);
  4. the re-solve;
  5. ACCEPTED only if (t5's bars) gate_k050_1104.py exits 0 on the result (D 23.0, k_c 143, kappa 0.5, |F| <= 5e-10, steps 6455 to 6719 = 6587 +- 132), its selftest exits 0 and its --mutate=f and --mutate=steps exit 1; and
     (my addition, the state against its record) kc143_syscheck_1025.py exits 0 on the result (it takes kappa from the record: the state's |F| within 1% of the record's and freeze_from gives the record's step count), its
     selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc135_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_k050d23_1104.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: k050d23_regrid_driver_1104.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/k050d23_1104"
OUT = S + "/I1104-win"
IN = S + "/inputs"
SRCD = IN          # my accepted k_c 143 D 23.0 kappa 0.7 state and record (raw I1025-win/kc143_d23; copies in inputs/)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SRC, TAG = "l1kc143winbd23", "l1kc143winbk050d23"
GATE = IN + "/gate_k050_1104.py"
SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D23.0000.npy", SRCD + f"/{SRC}.jsonl"
STATE_N = f"sol_{TAG}_D23.0000.npy"
LAM0 = "2.0992182200"
B_STATE, B_REC = "866c434bc1ae8854e12de9024b0ff859a7764800", "88f0be8bd3a329cadd3a4209614f1295bed61c6e"
PINS = [(IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719"), (IN + "/kc135_syscheck_1025.py", "b353d46696d2c90eb413fb071becb3e9aa8f976a"),
        (IN + "/kc143_syscheck_1025.py", "e15b0ee2b0b1f9e48a914b6e3e75f4fec48251f4"), (IN + "/gate_k050_1104.py", "d145145e22bf511011ca9ee2ecd8a14e2ce124e4"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, B_STATE), (SRCREC, B_REC),
        (WTM + f"/data/sol_{SRC}_D23.0000.npy", B_STATE), (WTM + f"/data/{SRC}.jsonl", B_REC)]
LOG = OUT + "/k050_regrid_w.log" + (".dry" if DRY else "")
CAPRG = 64800          # t5, hc 2026-11-27 18:27 UTC: cap 64800 s (18 h); OUT/cap_seconds.txt, if present, overrides it while the re-solve runs
SY143, SY135, SY127 = IN + "/kc143_syscheck_1025.py", IN + "/kc135_syscheck_1025.py", IN + "/kc127_syscheck_1025.py"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def blob(p, filters=False):
    return sh(["git", "hash-object"] + ([] if filters else ["--no-filters"]) + [p]).stdout.strip()


def hc(m):
    sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1104 kappa 0.5 re-solve at k_c 143, D 23.0 (from my kappa 0.7 state): {m}"])


def stop(m, code=2):
    say("STOP: " + m)
    if not DRY:
        hc("not started or stopped: " + m)
    sys.exit(code)


def run_capped(cmd, logf, cap, cwd, env, tag, notify_at=None):
    """start BelowNormal without a window, poll every 15 s, kill by the exact pid at the cap; returns (exit code or 'killed at the cap', seconds)"""
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=open(logf, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    say(f"{tag}: started pid {p.pid}: {' '.join(cmd)[:400]} > {logf}")
    t0 = time.time()
    notified = False
    while True:
        rc = p.poll()
        if rc is not None:
            say(f"{tag}: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
            return rc, time.time() - t0
        if notify_at and not notified and time.time() - t0 > notify_at:
            notified = True
            say(f"{tag}: still running at {notify_at} s (pid {p.pid}); cap {cap} s; hc to t5 as ordered")
            hc(f"the {tag} (pid {p.pid}) is still running after {notify_at} s (6 h); its cap is {cap} s (t5: 64800 s); nothing is stopped at 6 h.")
        try:
            c2 = int(open(OUT + "/cap_seconds.txt").read().split()[0])
            if c2 != cap:
                say(f"{tag}: cap changed from {cap} s to {c2} s (cap_seconds.txt)"); cap = c2
        except (OSError, ValueError, IndexError):
            pass
        if time.time() - t0 > cap:
            r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
            say(f"{tag}: CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
            p.wait()
            return "killed at the cap", time.time() - t0
        time.sleep(15)


os.makedirs(OUT + "/rows", exist_ok=True)
if not DRY:
    open(OUT + "/rows/regrid_driver.pid", "w").write(str(os.getpid()))
say(f"k050d23_regrid_driver_1104.py: the kappa 0.5 re-solve of my k_c 143 D 23.0 state{' (dry run)' if DRY else ''}; checking pins")
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
say(f"pins ok (the inputs of {IN}, my k_c 143 D 23.0 kappa 0.7 files, the gate, worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", PYTHONFAULTHANDLER="1")
sfx = ".dry" if DRY else ""
st143, st135, st127 = sh([PY, SY143, "--selftest"], env=env), sh([PY, SY135, "--selftest"], env=env), sh([PY, SY127, "--selftest"], env=env)
open(OUT + "/selftest_kc143_syscheck.txt" + sfx, "w").write(st143.stdout + st143.stderr)
open(OUT + "/selftest_kc135_syscheck.txt" + sfx, "w").write(st135.stdout + st135.stderr)
open(OUT + "/selftest_kc127_syscheck.txt" + sfx, "w").write(st127.stdout + st127.stderr)
say(f"selftests: kc143_syscheck exit {st143.returncode}, kc135_syscheck exit {st135.returncode}, kc127_syscheck exit {st127.returncode} (0 wanted each)")
if st143.returncode != 0 or st135.returncode != 0 or st127.returncode != 0:
    stop("a check's selftest is not 0")
l0 = sh([PY, "-c", "import ell_delta; print('%.10f' % ell_delta.lam0_at(23.0, *ell_delta.lam0_table())[0])"], cwd=WTM, env=env)
if l0.stdout.strip().splitlines()[-1:] != [LAM0]:
    stop(f"ell_delta.lam0_at(23.0) is {l0.stdout.strip()!r}, not {LAM0} (exit {l0.returncode})")
say(f"ell_delta.lam0_at(23.0) = {LAM0}, as t5's order")
if DRY:
    say(f"DRY: would start ell_refine.py {SRC} 143 {TAG} 143 1 23.0 {LAM0} --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s); nothing started")
    sys.exit(0)

samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_k050_1104.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/regrid_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/k050d23_watch_alert_1104.py", str(os.getpid()), "regrid"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1104.py", str(os.getpid()), "regrid", str(CAPRG + 43200)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")


def finish(code, m):
    say(m)
    hc(m)
    time.sleep(70)          # the sampler's last line
    samp.kill()
    say("k050d23_regrid_driver_1104.py done")
    sys.exit(code)


# step 3: the source (my k_c 143 kappa 0.7 state), through the checks (they re-freeze the state: minutes each)
t0 = time.time()
src = {}
for name, cmd in (("source_kc143_syscheck.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM]), ("source_kc143_syscheck_mutate_F.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM, "--mutate=F"]),
                  ("source_kc143_syscheck_mutate_steps.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM, "--mutate=steps"]), ("source_kc135_syscheck.txt", [PY, SY135, SRCREC, SRCSTATE, "23.0", WTM]),
                  ("source_kc127_syscheck.txt", [PY, SY127, SRCREC, SRCSTATE, "23.0", WTM]), ("source_gate.txt", [PY, GATE, SRCREC])):
    r = sh(cmd, env=env)
    open(OUT + "/" + name, "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    src[name] = r.returncode
want = {"source_kc143_syscheck.txt": 0, "source_kc143_syscheck_mutate_F.txt": 1, "source_kc143_syscheck_mutate_steps.txt": 1, "source_kc135_syscheck.txt": 1, "source_kc127_syscheck.txt": 1, "source_gate.txt": 1}
say(f"the source: kc143 check exit {src['source_kc143_syscheck.txt']} (0 wanted), --mutate=F {src['source_kc143_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc143_syscheck_mutate_steps.txt']} (1 wanted each), kc135 check {src['source_kc135_syscheck.txt']}, kc127 check {src['source_kc127_syscheck.txt']} and the kappa 0.5 gate {src['source_gate.txt']} (1 wanted each: they refuse the source); {time.time() - t0:.0f} s")
if src != want:
    finish(1, f"the source checks are not as wanted ({src}, wanted {want}): no re-solve")

# step 4: the re-solve
cmd = ["-u", "ell_refine.py", SRC, "143", TAG, "143", "1", "23.0", LAM0, "--kappa", "0.5", "--u0", "0.04", "--Ks", "30", "--tol", "1e-12", "--wait", "60", "--no-gamma"]
t_start = datetime.datetime.now(datetime.timezone.utc)
open(OUT + "/regrid.log", "w").write(f"# {t_start:%Y-%m-%d %H:%M:%S} UTC cmd: {PY} {' '.join(cmd)} (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s)\n")
rc, wall = run_capped([PY] + cmd, OUT + "/rows/regrid_raw.log", CAPRG, WTM, env, "re-solve", notify_at=21600)
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
    a = sh([PY, SY143, rec, state, "23.0", WTM], env=env)
    open(OUT + "/syscheck.txt", "w").write(a.stdout + a.stderr + f"exit {a.returncode}\n")
    s143 = sh([PY, SY143, "--selftest"], env=env)
    open(OUT + "/selftest_kc143_syscheck_after.txt", "w").write(s143.stdout + s143.stderr + f"exit {s143.returncode}\n")
    m1 = sh([PY, SY143, rec, state, "23.0", WTM, "--mutate=F"], env=env)
    m2 = sh([PY, SY143, rec, state, "23.0", WTM, "--mutate=steps"], env=env)
    open(OUT + "/syscheck_mutate.txt", "w").write(f"--mutate=F exit {m1.returncode} (1 wanted)\n{m1.stdout}\n--mutate=steps exit {m2.returncode} (1 wanted)\n{m2.stdout}\n")
    k135 = sh([PY, SY135, rec, state, "23.0", WTM], env=env)
    open(OUT + "/syscheck_kc135_on_result.txt", "w").write(k135.stdout + k135.stderr + f"exit {k135.returncode}\n")
    say(f"result: kc143 check exit {a.returncode} (0 wanted), its selftest {s143.returncode} (0 wanted), --mutate=F {m1.returncode}, --mutate=steps {m2.returncode} (1 wanted each), kc135 check on the result {k135.returncode} (1 wanted: it refuses); {time.time() - t0:.0f} s")
    g0, g1, g2, gs = sh([PY, GATE, rec], env=env), sh([PY, GATE, rec, "--mutate=f"], env=env), sh([PY, GATE, rec, "--mutate=steps"], env=env), sh([PY, GATE, "--selftest"], env=env)
    open(OUT + "/gate.txt", "w").write(f"gate on the result: exit {g0.returncode} (0 wanted)\n{g0.stdout}{g0.stderr}\n--mutate=f exit {g1.returncode} (1 wanted)\n{g1.stdout}\n--mutate=steps exit {g2.returncode} (1 wanted)\n{g2.stdout}\nselftest exit {gs.returncode} (0 wanted)\n{gs.stdout}")
    say(f"gate (t5's bars |F| <= 5e-10, steps 6455-6719): exit {g0.returncode} (0 wanted): {g0.stdout.strip()}; --mutate=f {g1.returncode}, --mutate=steps {g2.returncode} (1 wanted each); its selftest {gs.returncode} (0 wanted)")
    if (a.returncode, s143.returncode, m1.returncode, m2.returncode, k135.returncode, g0.returncode, g1.returncode, g2.returncode, gs.returncode) == (0, 0, 1, 1, 1, 0, 1, 1, 0):
        verdict = "ACCEPTED"
        shutil.copy(state, OUT + "/" + STATE_N)
        shutil.copy(rec, OUT + f"/{TAG}.jsonl")
        shutil.copy(IN + "/read_lower.py", OUT + "/read_lower.py")
        open(OUT + "/regrid_accepted.txt", "w").write(f"ACCEPTED {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC\nstate {blob(OUT + '/' + STATE_N)}\nrecord {blob(OUT + f'/{TAG}.jsonl')}\n")
    else:
        why = "syscheck: " + (a.stdout.strip().splitlines() or [''])[-1] + "; gate: " + g0.stdout.strip()

# the sampler's CSV: peak memory of the regrid stage
time.sleep(65)
pk = dict(ws=0.0, priv=0.0, free=1e9, commit=0.0, cpu=0.0, n=0)
try:
    for row in csv.DictReader(open(OUT + "/rows/regrid_samples.csv")):
        if row["stage"] in ("regrid", "re-solve"):
            pk["n"] += 1
            pk["ws"] = max(pk["ws"], float(row["ws_peak_gb"])); pk["priv"] = max(pk["priv"], float(row["private_peak_gb"]))
            pk["free"] = min(pk["free"], float(row["free_phys_gb"])); pk["commit"] = max(pk["commit"], float(row["commit_gb"])); pk["cpu"] = max(pk["cpu"], float(row["cpu_s"]))
except Exception as e:
    say(f"sampler csv: {e}")
recj = json.loads(open(rec).read().strip().splitlines()[-1]) if os.path.exists(rec) and os.path.getsize(rec) > 0 else {}
srcj = [json.loads(x) for x in open(SRCREC) if x.strip() and json.loads(x).get("D") == 23.0][-1]     # my kappa 0.7 record
dd = (recj["Delta"] - srcj["Delta"]) if recj.get("Delta") is not None else None
sratio = (recj["steps"] / srcj["steps"]) if recj.get("steps") and srcj.get("steps") else None
summ = (f"re-solve {t_start:%Y-%m-%d %H:%M:%S} to {t_end:%H:%M:%S} UTC, exit {rc}, wall {wall:.0f} s (record's seconds {recj.get('seconds')}); record (kappa {recj.get('kappa')}): |F| {recj.get('F')}, F_start {recj.get('F_start')}, "
        f"steps {recj.get('steps')}, constraint {recj.get('constraint')}, Delta {recj.get('Delta')}; the kappa 0.7 source record at D 23.0: |F| {srcj.get('F')}, steps {srcj.get('steps')}, constraint {srcj.get('constraint')}, Delta {srcj.get('Delta')}; "
        f"Delta(kappa 0.5) minus Delta(kappa 0.7) = {dd}; steps ratio {sratio} (t5's bars: |F| <= 5e-10, steps 6587 +- 132 = 6455 to 6719, i.e. 1.4 times 4705; freeze_from on the source state at kappa 0.5 gives 6582); {verdict}{(': ' + why) if why else ''}; "
        f"peak working set {pk['ws']:.2f} GB, peak private {pk['priv']:.2f} GB (the largest python of the tree, {pk['n']} samples), lowest free memory {pk['free']:.2f} GB, peak commit {pk['commit']:.1f} GB, cpu {pk['cpu']:.0f} s")
open(OUT + "/regrid_summary.txt", "w").write(summ + "\n")
say(summ)
hc(f"finished: {summ}. Raw I1104-win after my next push. " + ("The scan (d18_secant.py scan with the Rust block, --b12=rust --b12_threads=2, lambda 0.080 0.095 0.110 0.125, 4 evaluations, 2 processes) starts by itself now." if verdict == "ACCEPTED" else "No scan."))
time.sleep(5)
samp.kill()
say("k050d23_regrid_driver_1104.py done")
sys.exit(0 if verdict == "ACCEPTED" else 1)
