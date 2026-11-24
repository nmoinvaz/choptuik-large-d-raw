#!/usr/bin/env python3
"""make_kc103d21_1025.py: writes the k_c 103 D 21.0 stage's scripts from the k_c 95 D 21.0 ones (staging kc95d21_1025, raw I1025-win/kc95_d21 at 7b7f37628) by asserted text replacements:
kc103d21_regrid_driver_1025.py (head written here, body from the k_c 95 one), kc103d21_scan_driver_1025.py, kc103d21_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1,
sample_driver4_1025.ps1, go_kc103d21_1025.cmd, publish_kc103d21_1025.sh. Each asserted replacement must occur; the diff of the regrid driver against the k_c 95 one is written to
diff_regrid_driver_vs_kc95d21.txt. Source (my accepted k_c 95 D 21.0 state) and the two checks go to inputs/ by copy."""
import difflib, os, shutil

S = "C:/Users/nathan/Source/kc103d21_1025"
OLD = "C:/Users/nathan/Source/kc95d21_1025"
OLDOUT = OLD + "/I1025-win/kc95_d21"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert a in t, a[:100]
        t = t.replace(a, b)
    return t


GEN = [("kc95", "kc103"), ("kc87", "kc95"), ("k_c 95", "k_c 103"), ("k_c 87", "k_c 95")]
os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc103_d21/rows", exist_ok=True)

# 0. inputs: the source (my accepted k_c 95 D 21.0 state and record) and the pinned scripts
for src, dst in ((OLDOUT + "/sol_l1kc95winbg_D21.0000.npy", S + "/inputs/sol_l1kc95winbg_D21.0000.npy"), (OLDOUT + "/l1kc95winbg.jsonl", S + "/inputs/l1kc95winbg.jsonl"),
                 (OLD + "/inputs/kc95_syscheck_1025.py", S + "/inputs/kc95_syscheck_1025.py"), (OLD + "/inputs/d18_hybsign.py", S + "/inputs/d18_hybsign.py"),
                 (OLD + "/inputs/d185_scan_read.py", S + "/inputs/d185_scan_read.py"), (OLD + "/inputs/read_lower.py", S + "/inputs/read_lower.py")):
    shutil.copyfile(src, dst)
assert os.path.exists(S + "/inputs/kc103_syscheck_1025.py")

# 1. the regrid driver
t = rd(OLD + "/kc95d21_regrid_driver_1025.py")
body = t[t.index("\ndef say(m):"):]
body = rep(body, [('SRC, "87", TAG, "95"', 'SRC, "95", TAG, "103"'), ("{SRC} 87 {TAG} 95 1 21.0", "{SRC} 95 {TAG} 103 1 21.0"),
                  ("from dh610's k_c 87 D 21.0 state", "from @@MYSRC@@ D 21.0 state"),
                  ("SY95", "SY103"), ("SY87", "SY95"), ("st95", "st103"), ("st87", "st95"), ("s95", "s103"), ("k87", "k95"),
                  ("The scan 0.900-0.925 by 0.005 plus a repeat of 0.910 (7 evaluations, 4 processes)", "The scan 0.905-0.925 by 0.005 plus a repeat of 0.915 (6 evaluations, 4 processes)"),
                  ('dd = (recj["Delta"] - srcj["Delta"]) if recj.get("Delta") is not None else None',
                   'dd = (recj["Delta"] - srcj["Delta"]) if recj.get("Delta") is not None else None\nsratio = (recj["steps"] / srcj["steps"]) if recj.get("steps") and srcj.get("steps") else None'),
                  ("= {dd}; {verdict}", "= {dd}; steps ratio {sratio} (@@K87@@ to 95 at D 21.0: 3219/2948 = 1.092); {verdict}")] + GEN)
body = body.replace("@@MYSRC@@", "my accepted k_c 95")
BAD = ("k_c 87", "kc87", "SY87", "st87", "k87", "dh610", " 87 ", '"87"')
assert not any(b in body for b in BAD), [l for l in body.splitlines() if any(b in l for b in BAD)]
body = body.replace("@@K87@@", "k_c 87")
head = '''#!/usr/bin/env python3
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

'''
new = head + body
wr(S + "/kc103d21_regrid_driver_1025.py", new)
d = "".join(difflib.unified_diff(t.splitlines(True), new.splitlines(True), "kc95d21_regrid_driver_1025.py", "kc103d21_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_kc95d21.txt", d)

# 2. the scan driver
t = rd(OLD + "/kc95d21_scan_driver_1025.py")
t = rep(t, [("t5's order, hc of 2026-11-24 ~11:05 UTC", "t5's order, hc of 2026-11-24 ~15:47 UTC"), ('"0.900,0.910;0.905,0.920;0.910,0.925;0.915"', '"0.915,0.905;0.910;0.920,0.925;0.915"')])
for a, b in GEN:
    t = t.replace(a, b)
assert not any(b in t for b in ("k_c 87", "kc87", "dh610", " 87 ")), "scan driver"
wr(S + "/kc103d21_scan_driver_1025.py", t)

# 3. watcher, keep-awake, session check, sampler
for a, b in (("kc95d21_watch_alert_1025.py", "kc103d21_watch_alert_1025.py"), ("keepawake_1025.py", "keepawake_1025.py"), ("session_check_1025.ps1", "session_check_1025.ps1")):
    t = rd(OLD + "/" + a)
    t = t.replace("kc95", "kc103").replace("k_c 95", "k_c 103")
    assert "kc95" not in t and "kc87" not in t and "k_c 87" not in t
    wr(S + "/" + b, t)
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc95d21_1025.cmd")
t = rep(t, [("~11:05 UTC", "~15:47 UTC"), ("(7 evaluations, 4 processes)", "(6 evaluations, 4 processes)"), ('"0.900,0.910;0.905,0.920;0.910,0.925;0.915"', '"0.915,0.905;0.910;0.920,0.925;0.915"')])
for a, b in GEN:
    t = t.replace(a, b)
wr(S + "/go_kc103d21_1025.cmd", t)
t = rd(OLD + "/publish_kc95d21_1025.sh")
t = rep(t, [("kc95_syscheck_1025_dh610.diff", "kc103_syscheck_1025_vs_@@KC95@@.diff"), ("diff_regrid_driver_vs_kc95d19.txt", "diff_regrid_driver_vs_@@K@@.txt"), ("selftest_scan_dry_1025.txt", "selftest_scan_dry_1025.txt")])
for a, b in GEN:
    t = t.replace(a, b)
t = t.replace("@@K@@", "kc95d21").replace("@@KC95@@", "kc95")
assert "kc87" not in t and "k_c 87" not in t
wr(S + "/publish_kc103d21_1025.sh", t)
os.chmod(S + "/publish_kc103d21_1025.sh", 0o755)
print("written")
