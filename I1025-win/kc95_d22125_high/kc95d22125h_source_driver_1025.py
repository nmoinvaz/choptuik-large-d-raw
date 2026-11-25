#!/usr/bin/env python3
"""#1025 winb, the source of the k_c 95 HIGH scan at D 22.125 (t5's order, hc of 2026-11-25 ~09:30 UTC): dh610's accepted k_c 95 D 22.125 state
(raw I1025-dh610/kc95_d22125, regrid commit ce4fce87f: in/sol_l1kc95dh610d22125_D22.1250.npy blob 06c5082f, in/l1kc95dh610d22125.jsonl blob 64ecb047) is NOT regridded: it is scanned as it is. This driver
only pins and checks it, in the order of my k_c 103 regrid driver without its regrid (any failure stops it with an hc to t5, no scan, exit 2 or 1):
  1. pins: kc87_syscheck_1025.py (6df5d960), kc95_syscheck_1025.py (d487e628, dh610's) and kc103_syscheck_1025.py (3ab58d16, dh170's: the k_c 95 check with only the k_c constant changed, 3 lines),
     d18_hybsign.py, d185_scan_read.py, read_lower.py, dh610's k_c 95 D 22.125 state and record (inputs/), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399, ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(22.125) = 2.1023628304 (dh610's);
  3. the SOURCE: the k_c 95 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 87 check and the k_c 103 check refuse it (exit 1 each);
  4. the marker source_accepted.txt (ACCEPTED, with the state and record blobs) is written from this python process and the state, record and reader are copied beside it; the scan driver starts only after it
     (go_kc95d22125h_1025.cmd). Memory: no guard, the alert-only watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched)
     holds for this driver's duration.
usage: kc95d22125h_source_driver_1025.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/kc95d22125h_1025"
OUT = S + "/I1025-win/kc95_d22125_high"
IN = S + "/inputs"
SRCD = IN          # dh610's accepted k_c 95 D 22.125 state and record (raw I1025-dh610/kc95_d22125, commit ce4fce87f; copies in inputs/)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SRC = "l1kc95dh610d22125"
SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D22.1250.npy", SRCD + f"/{SRC}.jsonl"
STATE_N = f"sol_{SRC}_D22.1250.npy"
LAM0 = "2.1023628304"
B_STATE, B_REC = "06c5082f523c3eb9f1a2669415ac6981e2f82ae2", "64ecb0474d17c1bcd1e4cb0d7ec8f41eafc71580"
PINS = [(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"),
        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, B_STATE), (SRCREC, B_REC)]
LOG = OUT + "/kc95d22125h_source_w.log" + (".dry" if DRY else "")
SY103, SY95, SY87 = IN + "/kc103_syscheck_1025.py", IN + "/kc95_syscheck_1025.py", IN + "/kc87_syscheck_1025.py"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def blob(p, filters=False):
    return sh(["git", "hash-object"] + ([] if filters else ["--no-filters"]) + [p]).stdout.strip()


def hc(m):
    sh([HC, "send", COORD, f"winb ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), #1025 k_c 95 HIGH scan at D 22.125 (dh610's state), source: {m}"])


def stop(m, code=2):
    say("STOP: " + m)
    if not DRY:
        hc("not started: " + m)
    sys.exit(code)


os.makedirs(OUT + "/rows", exist_ok=True)
if not DRY:
    open(OUT + "/rows/source_driver.pid", "w").write(str(os.getpid()))
say(f"kc95d22125h_source_driver_1025.py: the source of the k_c 95 HIGH scan at D 22.125, dh610's accepted k_c 95 D 22.125 state{' (dry run)' if DRY else ''}; checking pins")
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
for f in (OUT + "/source_accepted.txt", OUT + "/" + STATE_N, OUT + f"/{SRC}.jsonl"):
    if os.path.exists(f) and not DRY:
        stop(f"{f} exists")
say(f"pins ok (the inputs of {IN}, dh610's k_c 95 D 22.125 files, worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1", PYTHONFAULTHANDLER="1")
sfx = ".dry" if DRY else ""
st103, st95, st87 = sh([PY, SY103, "--selftest"], env=env), sh([PY, SY95, "--selftest"], env=env), sh([PY, SY87, "--selftest"], env=env)
open(OUT + "/selftest_kc103_syscheck.txt" + sfx, "w").write(st103.stdout + st103.stderr)
open(OUT + "/selftest_kc95_syscheck.txt" + sfx, "w").write(st95.stdout + st95.stderr)
open(OUT + "/selftest_kc87_syscheck.txt" + sfx, "w").write(st87.stdout + st87.stderr)
say(f"selftests: kc103_syscheck exit {st103.returncode}, kc95_syscheck exit {st95.returncode}, kc87_syscheck exit {st87.returncode} (0 wanted each)")
if st103.returncode != 0 or st95.returncode != 0 or st87.returncode != 0:
    stop("a check's selftest is not 0")
l0 = sh([PY, "-c", "import ell_delta; print('%.10f' % ell_delta.lam0_at(22.125, *ell_delta.lam0_table())[0])"], cwd=WTM, env=env)
if l0.stdout.strip().splitlines()[-1:] != [LAM0]:
    stop(f"ell_delta.lam0_at(22.125) is {l0.stdout.strip()!r}, not {LAM0} (exit {l0.returncode})")
say(f"ell_delta.lam0_at(22.125) = {LAM0}, as dh610's")
if DRY:
    say("DRY: would run the five source checks and write source_accepted.txt; nothing started")
    sys.exit(0)

samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver4_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/source_samples.csv", "-Interval", "60"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
wat = subprocess.Popen([PY, "-u", S + "/kc95d22125h_watch_alert_1025.py", str(os.getpid()), "source"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "source", "7200"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")


def finish(code, m):
    say(m)
    hc(m)
    time.sleep(70)          # the sampler's last line
    samp.kill()
    say("kc95d22125h_source_driver_1025.py done")
    sys.exit(code)


# step 3: the source, through both checks (the checks re-freeze the state: minutes each)
t0 = time.time()
src = {}
for name, cmd in (("source_kc95_syscheck.txt", [PY, SY95, SRCREC, SRCSTATE, "22.125", WTM]), ("source_kc95_syscheck_mutate_F.txt", [PY, SY95, SRCREC, SRCSTATE, "22.125", WTM, "--mutate=F"]),
                  ("source_kc95_syscheck_mutate_steps.txt", [PY, SY95, SRCREC, SRCSTATE, "22.125", WTM, "--mutate=steps"]), ("source_kc87_syscheck.txt", [PY, SY87, SRCREC, SRCSTATE, "22.125", WTM]), ("source_kc103_syscheck.txt", [PY, SY103, SRCREC, SRCSTATE, "22.125", WTM])):
    r = sh(cmd, env=env)
    open(OUT + "/" + name, "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    src[name] = r.returncode
want = {"source_kc95_syscheck.txt": 0, "source_kc95_syscheck_mutate_F.txt": 1, "source_kc95_syscheck_mutate_steps.txt": 1, "source_kc87_syscheck.txt": 1, "source_kc103_syscheck.txt": 1}
say(f"the source: kc95 check exit {src['source_kc95_syscheck.txt']} (0 wanted), --mutate=F {src['source_kc95_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc95_syscheck_mutate_steps.txt']} (1 wanted each), kc87 check {src['source_kc87_syscheck.txt']} and kc103 check {src['source_kc103_syscheck.txt']} (1 wanted each: they refuse the source); {time.time() - t0:.0f} s")
if src != want:
    finish(1, f"the source checks are not as wanted ({src}, wanted {want}): no scan")


# step 4: the marker, the copies the scan driver reads, the sampler's last line
for f in (OUT + "/source_accepted.txt",):
    assert not os.path.exists(f), f
shutil.copy(SRCSTATE, OUT + "/" + STATE_N)
shutil.copy(SRCREC, OUT + f"/{SRC}.jsonl")
shutil.copy(IN + "/read_lower.py", OUT + "/read_lower.py")
open(OUT + "/source_accepted.txt", "w").write(f"ACCEPTED {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC\nstate {blob(OUT + '/' + STATE_N)}\nrecord {blob(OUT + f'/{SRC}.jsonl')}\n")
recj = json.loads(open(SRCREC).read().strip().splitlines()[-1])
finish(0, f"the source is ACCEPTED (dh610's k_c 95 D 22.125 record: |F| {recj['F']}, steps {recj['steps']}, constraint {recj['constraint']}, Delta {recj['Delta']}; the checks as ordered). The scan 0.52-0.76 by 0.04 plus a repeat of 0.64 (8 evaluations, 4 processes) starts by itself now. Raw I1025-win/kc95_d22125_high after my next push.")
