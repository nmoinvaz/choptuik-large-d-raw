#!/usr/bin/env python3
"""make_kc103d2175_1025.py: writes the k_c 103 D 21.75 stage's scripts from the k_c 103 D 21.125 cross-build ones (staging kc103d21125x_1025, raw I1025-win/kc103_d21125x at c58c9430a) by asserted text replacements:
kc103d2175_regrid_driver_1025.py (head written here, body from the D 21.125 one), kc103d2175_scan_driver_1025.py, kc103d2175_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1,
sample_driver4_1025.ps1, go_kc103d2175_1025.cmd, publish_kc103d2175_1025.sh. Each asserted replacement must occur; the diff of the regrid driver against the D 21.125 one is written to
diff_regrid_driver_vs_crossbuild.txt. The source (dh610's accepted k_c 95 D 21.75 state and record, raw I1025-dh610/kc95_d2175) and the pinned checks are in inputs/ already (copied by hand, blobs checked).
The regrid's cap is 43200 s (t5's hc of 2026-11-25 ~04:35 UTC) with an hc to t5 at 21600 s if it is still running; the scan's cap stays 21600 s."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc103d2175_1025"
OLD = "C:/Users/nathan/Source/kc103d21125x_1025"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert a in t, a[:120]
        t = t.replace(a, b)
    return t


def glob_rep(t):
    """names, tags, D and lambda_0: applied to every derived file after its own asserted edits"""
    t = t.replace("l1kc103winx", "l1kc103win2175").replace("l1kc95dh170f", "l1kc95dh610d2175")
    t = t.replace("read_lower_kc103x_D21125", "read_lower_kc103_D2175").replace("scan_kc103x_D21125", "scan_kc103_D2175")
    t = t.replace("kc103_d21125x", "kc103_d2175").replace("kc103d21125x_", "kc103d2175_")
    t = t.replace("D21.1250", "D21.7500").replace("2.1062343410", "2.1037780803")
    t = re.sub(r"(?<![0-9.])21\.125(?![0-9])", "21.75", t)
    for bad in ("dh170's accepted", "dh170's k_c", "as dh170's", "cross-build", "21125", "D21.1250", "2.1062343410"):
        assert bad not in t, bad
    return t


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc103_d2175/rows", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc95dh610d2175_D21.7500.npy", "l1kc95dh610d2175.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f

# 1. the regrid driver
t = rd(OLD + "/kc103d21125x_regrid_driver_1025.py")
body = t[t.index("\ndef say(m):"):]
body = rep(body, [
    ("dh170's accepted k_c 95 D 21.125 state", "dh610's accepted k_c 95 D 21.125 state"),
    ("dh170's k_c 95 D 21.125 files", "dh610's k_c 95 D 21.125 files"),
    ("as dh170's", "as dh610's"),
    ("(cross-build, from dh170's k_c 95 state)", "(from dh610's k_c 95 state)"),
    ("the k_c 103 regrid at D 21.125 (cross-build) from", "the k_c 103 regrid at D 21.125 from"),
    ("(dh170's k_c 95 to 103 at D 21.125: 3206 to 3476 = 1.0842; mine at D 21.0: 3219 to 3489 = 1.0839)",
     "(dh610's k_c 87 to 95 at D 21.125: 2887 to 3152 = 1.0918; mine k_c 95 to 103 at D @@D1125@@: 3206 to 3476 = 1.0842, at D @@D210@@: 3219 to 3489 = 1.0839)"),
    ("The scan 0.875-0.895 by 0.005 plus a repeat of 0.885 (6 evaluations, 4 processes)", "The scan 0.635-0.655 by 0.005 plus a repeat of 0.645 (6 evaluations, 4 processes)"),
    # the regrid's cap is 43200 s with one hc to t5 at 21600 s if it is still running
    ('def run_capped(cmd, logf, cap, cwd, env, tag):', 'def run_capped(cmd, logf, cap, cwd, env, tag, notify_at=None):'),
    ("    t0 = time.time()\n    while True:\n        rc = p.poll()\n",
     "    t0 = time.time()\n    notified = False\n    while True:\n        rc = p.poll()\n"),
    ("        if time.time() - t0 > cap:\n",
     "        if notify_at and not notified and time.time() - t0 > notify_at:\n"
     "            notified = True\n"
     "            say(f\"{tag}: still running at {notify_at} s (pid {p.pid}); cap {cap} s; hc to t5 as ordered\")\n"
     "            hc(f\"the {tag} (pid {p.pid}) is still running after {notify_at} s (6 h); its cap is {cap} s as t5 ordered; nothing is stopped at 6 h.\")\n"
     "        if time.time() - t0 > cap:\n"),
    ('rc, wall = run_capped([PY] + cmd, OUT + "/rows/regrid_raw.log", CAPRG, WTM, env, "regrid")', 'rc, wall = run_capped([PY] + cmd, OUT + "/rows/regrid_raw.log", CAPRG, WTM, env, "regrid", notify_at=21600)'),
])
body = glob_rep(body).replace("@@D1125@@", "21.125").replace("@@D210@@", "21.0")
head = '''#!/usr/bin/env python3
"""#1025 winb, the k_c 103 regrid at D 21.75 (t5's order, hc of 2026-11-25 ~04:30 UTC, after the k_c 103 D 21.125 ruling 0.884384): dh610's accepted k_c 95 D 21.75 state
(raw I1025-dh610/kc95_d2175, regrid commit dc5a6edb: in/sol_l1kc95dh610d2175_D21.7500.npy blob ee18ab90, in/l1kc95dh610d2175.jsonl blob 6bde1c86) is regridded on this Windows machine to k_c 103 with
  ell_refine.py l1kc95dh610d2175 95 l1kc103win2175 103 1 21.75 2.1037780803 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.1037780803 is lambda_0(21.75), unused with --no-gamma; checked below)
exactly as my k_c 103 regrids at D 21.0 and 21.125 (same worktree, venv, 4 threads, BelowNormal), only the source tag, the D and the target tag changed. The cap is 43200 s (12 h; t5's hc of ~04:35 UTC raised it from
the 6 h of the earlier regrids because dh610's own k_c 95 regrid at this D took 9339 s on 8 threads), killed by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running; nothing is stopped at 6 h.
Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: kc87_syscheck_1025.py (6df5d960), kc95_syscheck_1025.py (d487e628, dh610's) and kc103_syscheck_1025.py (3ab58d16, dh170's: the k_c 95 check with only the k_c constant changed, 3 lines),
     d18_hybsign.py, d185_scan_read.py, read_lower.py, dh610's k_c 95 D 21.75 state and record (inputs/ and the worktree's copies), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399,
     ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(21.75) = 2.1037780803;
  3. the SOURCE: the k_c 95 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 87 check and the k_c 103 check refuse it (exit 1 each);
  4. the regrid;
  5. ACCEPTED only if kc103_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc95_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc103d2175_1025.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc103d2175_regrid_driver_1025.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/kc103d2175_1025"
OUT = S + "/I1025-win/kc103_d2175"
IN = S + "/inputs"
SRCD = IN          # dh610's accepted k_c 95 D 21.75 state and record (raw I1025-dh610/kc95_d2175, commit dc5a6edb; copies in inputs/)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SRC, TAG = "l1kc95dh610d2175", "l1kc103win2175"
SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D21.7500.npy", SRCD + f"/{SRC}.jsonl"
STATE_N = f"sol_{TAG}_D21.7500.npy"
LAM0 = "2.1037780803"
B_STATE, B_REC = "ee18ab90e3dc826d2d45c600b0e6938b20ccd48e", "6bde1c86007d67e7c3c6e36c2d9e64fc743d75a7"
PINS = [(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"),
        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, B_STATE), (SRCREC, B_REC),
        (WTM + f"/data/sol_{SRC}_D21.7500.npy", B_STATE), (WTM + f"/data/{SRC}.jsonl", B_REC)]
LOG = OUT + "/kc103_regrid_w.log" + (".dry" if DRY else "")
CAPRG = 43200
SY103, SY95, SY87 = IN + "/kc103_syscheck_1025.py", IN + "/kc95_syscheck_1025.py", IN + "/kc87_syscheck_1025.py"

'''
new = head + body
wr(S + "/kc103d2175_regrid_driver_1025.py", new)
d = "".join(difflib.unified_diff(t.splitlines(True), new.splitlines(True), "kc103d21125x_regrid_driver_1025.py", "kc103d2175_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_crossbuild.txt", d)

# 2. the scan driver (cap 21600 s, unchanged)
t = rd(OLD + "/kc103d21125x_scan_driver_1025.py")
t = rep(t, [("t5's order, hc of 2026-11-24 ~22:19 UTC", "t5's order, hc of 2026-11-25 ~04:30 UTC"), ('"0.885,0.875;0.880;0.890,0.895;0.885"', '"0.645,0.635;0.640;0.650,0.655;0.645"'),
            ("(the cross-build repeat from dh170's k_c 95 D 21.125 state)", "(from dh610's k_c 95 D 21.125 state)"),
            ("the k_c 103 D 21.125 cross-build regrid is not accepted", "the k_c 103 D 21.125 regrid is not accepted")])
wr(S + "/kc103d2175_scan_driver_1025.py", glob_rep(t))

# 3. watcher, keep-awake, session check, sampler
for a in ("kc103d21125x_watch_alert_1025.py", "keepawake_1025.py", "session_check_1025.ps1"):
    t = glob_rep(rd(OLD + "/" + a))
    wr(S + "/" + a.replace("kc103d21125x_", "kc103d2175_"), t)
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc103d21125x_1025.cmd")
t = rep(t, [("2026-11-24 ~22:19 UTC", "2026-11-25 ~04:30 UTC"), ('"0.885,0.875;0.880;0.890,0.895;0.885"', '"0.645,0.635;0.640;0.650,0.655;0.645"'),
            ("the k_c 103 D 21.125 cross-build chain (from dh170's k_c 95 state)", "the k_c 103 D 21.125 chain (from dh610's k_c 95 state)")])
wr(S + "/go_kc103d2175_1025.cmd", glob_rep(t))
t = rd(OLD + "/publish_kc103d21125x_1025.sh")
t = rep(t, [("diff_regrid_driver_vs_kc103d21.txt", "diff_regrid_driver_vs_crossbuild.txt")])
wr(S + "/publish_kc103d2175_1025.sh", glob_rep(t))
os.chmod(S + "/publish_kc103d2175_1025.sh", 0o755)
shutil.copyfile(OLD + "/kc103_syscheck_1025_vs_kc95.diff", S + "/kc103_syscheck_1025_vs_kc95.diff")
print("written")
