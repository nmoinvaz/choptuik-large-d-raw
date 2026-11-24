#!/usr/bin/env python3
"""make_kc103d21125x_1025.py: writes the k_c 103 D 21.125 cross-build stage's scripts from the k_c 103 D 21.0 ones (staging kc103d21_1025, raw I1025-win/kc103_d21 at 3499f61a8) by asserted text replacements:
kc103d21125x_regrid_driver_1025.py (head written here, body from the D 21.0 one), kc103d21125x_scan_driver_1025.py, kc103d21125x_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1,
sample_driver4_1025.ps1, go_kc103d21125x_1025.cmd, publish_kc103d21125x_1025.sh. Each asserted replacement must occur; the diff of the regrid driver against the D 21.0 one is written to
diff_regrid_driver_vs_kc103d21.txt. The source (dh170's accepted k_c 95 D 21.125 state and record, raw I1025-dh170/kc95_d21125) and the pinned checks are in inputs/ already (copied by hand, blobs checked)."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc103d21125x_1025"
OLD = "C:/Users/nathan/Source/kc103d21_1025"


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
    """names, tags and D: applied to every derived file after its own asserted edits"""
    t = t.replace("l1kc103winbg", "l1kc103winx").replace("l1kc95winbg", "l1kc95dh170f")
    t = t.replace("read_lower_kc103_D21", "read_lower_kc103x_D21125").replace("scan_kc103_D21", "scan_kc103x_D21125")
    t = re.sub(r"kc103_d21(?!125)", "kc103_d21125x", t)
    t = t.replace("kc103d21_", "kc103d21125x_")
    t = t.replace("D21.0000", "D21.1250")
    t = re.sub(r"(?<![0-9.])21\.0(?![0-9])", "21.125", t)
    for bad in ("winbg", "D21.0000", "kc103_d21 ", "kc103d21_"):
        assert bad not in t, bad
    assert not re.search(r"(?<![0-9.])21\.0(?![0-9])", t)
    return t


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc103_d21125x/rows", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc95dh170f_D21.1250.npy", "l1kc95dh170f.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f

# 1. the regrid driver
t = rd(OLD + "/kc103d21_regrid_driver_1025.py")
body = t[t.index("\ndef say(m):"):]
body = rep(body, [
    ("from my accepted k_c 95 D 21.0 state", "from dh170's accepted k_c 95 D 21.0 state"),
    ("the k_c 95 D 21.0 files", "dh170's k_c 95 D 21.0 files"),
    ('st103, st95 = sh([PY, SY103, "--selftest"], env=env), sh([PY, SY95, "--selftest"], env=env)',
     'st103, st95, st87 = sh([PY, SY103, "--selftest"], env=env), sh([PY, SY95, "--selftest"], env=env), sh([PY, SY87, "--selftest"], env=env)'),
    ('open(OUT + "/selftest_kc95_syscheck.txt" + sfx, "w").write(st95.stdout + st95.stderr)\n',
     'open(OUT + "/selftest_kc95_syscheck.txt" + sfx, "w").write(st95.stdout + st95.stderr)\nopen(OUT + "/selftest_kc87_syscheck.txt" + sfx, "w").write(st87.stdout + st87.stderr)\n'),
    ('say(f"selftests: kc103_syscheck exit {st103.returncode}, kc95_syscheck exit {st95.returncode} (0 wanted each)")',
     'say(f"selftests: kc103_syscheck exit {st103.returncode}, kc95_syscheck exit {st95.returncode}, kc87_syscheck exit {st87.returncode} (0 wanted each)")'),
    ("if st103.returncode != 0 or st95.returncode != 0:\n    stop(\"a check's selftest is not 0\")\n",
     "if st103.returncode != 0 or st95.returncode != 0 or st87.returncode != 0:\n    stop(\"a check's selftest is not 0\")\n"
     "l0 = sh([PY, \"-c\", \"import ell_delta; print('%.10f' % ell_delta.lam0_at(21.0, *ell_delta.lam0_table())[0])\"], cwd=WTM, env=env)\n"
     "if l0.stdout.strip().splitlines()[-1:] != [LAM0]:\n"
     "    stop(f\"ell_delta.lam0_at(21.0) is {l0.stdout.strip()!r}, not {LAM0} (exit {l0.returncode})\")\n"
     "say(f\"ell_delta.lam0_at(21.0) = {LAM0}, as dh170's\")\n"),
    ('("source_kc103_syscheck.txt", [PY, SY103, SRCREC, SRCSTATE, "21.0", WTM])):',
     '("source_kc87_syscheck.txt", [PY, SY87, SRCREC, SRCSTATE, "21.0", WTM]), ("source_kc103_syscheck.txt", [PY, SY103, SRCREC, SRCSTATE, "21.0", WTM])):'),
    ('"source_kc95_syscheck_mutate_steps.txt": 1, "source_kc103_syscheck.txt": 1}', '"source_kc95_syscheck_mutate_steps.txt": 1, "source_kc87_syscheck.txt": 1, "source_kc103_syscheck.txt": 1}'),
    ("(1 wanted each), kc103 check {src['source_kc103_syscheck.txt']} (1 wanted: it refuses the source)",
     "(1 wanted each), kc87 check {src['source_kc87_syscheck.txt']} and kc103 check {src['source_kc103_syscheck.txt']} (1 wanted each: they refuse the source)"),
    ("(k_c 87 to 95 at D 21.0: 3219/2948 = 1.092)", "(dh170's k_c 95 to 103 at D 21.0: 3206 to 3476 = 1.0842; mine at D @@D210@@: 3219 to 3489 = 1.0839)"),
    ("The scan 0.905-0.925 by 0.005 plus a repeat of 0.915 (6 evaluations, 4 processes)", "The scan 0.875-0.895 by 0.005 plus a repeat of 0.885 (6 evaluations, 4 processes)"),
    ("#1025 k_c 103 regrid at D 21.0: {m}", "#1025 k_c 103 regrid at D 21.0 (cross-build, from dh170's k_c 95 state): {m}"),
    ('the k_c 103 regrid at D 21.0 from dh170', 'the k_c 103 regrid at D 21.0 (cross-build) from dh170'),
])
body = glob_rep(body).replace("@@D210@@", "21.0")
head = '''#!/usr/bin/env python3
"""#1025 winb, the k_c 103 regrid at D 21.125, the cross-build repeat (t5's order, hc of 2026-11-24 ~22:19 UTC, after the k_c 103 D 21.0 ruling 0.913448): dh170's accepted k_c 95 D 21.125 state
(raw I1025-dh170/kc95_d21125 at 30befd983: sol_l1kc95dh170f_D21.1250.npy blob c9d37744, l1kc95dh170f.jsonl blob 6df5a5ee) is regridded on this Windows machine to k_c 103 with
  ell_refine.py l1kc95dh170f 95 l1kc103winx 103 1 21.125 2.1062343410 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.1062343410 is lambda_0(21.125), unused with --no-gamma; checked below)
exactly as my k_c 103 D 21.0 regrid (same worktree, venv, 4 threads, BelowNormal), only the source tag, the D and the target tag changed; cap 21600 s (t5's 6 h) by the exact pid, one process outside my terminal.
Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: kc87_syscheck_1025.py (6df5d960), kc95_syscheck_1025.py (d487e628, dh610's) and kc103_syscheck_1025.py (3ab58d16, dh170's: the k_c 95 check with only the k_c constant changed, 3 lines),
     d18_hybsign.py, d185_scan_read.py, read_lower.py, dh170's k_c 95 D 21.125 state and record (inputs/ and the worktree's copies), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399,
     ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(21.125) = 2.1062343410;
  3. the SOURCE: the k_c 95 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 87 check and the k_c 103 check refuse it (exit 1 each);
  4. the regrid;
  5. ACCEPTED only if kc103_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc95_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc103d21125x_1025.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc103d21125x_regrid_driver_1025.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
import csv, datetime, json, os, re, shutil, subprocess, sys, time

S = "C:/Users/nathan/Source/kc103d21125x_1025"
OUT = S + "/I1025-win/kc103_d21125x"
IN = S + "/inputs"
SRCD = IN          # dh170's accepted k_c 95 D 21.125 state and record (raw I1025-dh170/kc95_d21125 at 30befd983; copies in inputs/)
WT = "C:/Users/nathan/Source/choptuik-i1025k79"
WTM = WT + "/solver/matter"
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
SRC, TAG = "l1kc95dh170f", "l1kc103winx"
SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D21.1250.npy", SRCD + f"/{SRC}.jsonl"
STATE_N = f"sol_{TAG}_D21.1250.npy"
LAM0 = "2.1062343410"
B_STATE, B_REC = "c9d3774447775d9457d26529d4d447c9e30afce4", "6df5a5ee09fbfb0dabdec50d6012017dcb727c6a"
PINS = [(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"),
        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, B_STATE), (SRCREC, B_REC),
        (WTM + f"/data/sol_{SRC}_D21.1250.npy", B_STATE), (WTM + f"/data/{SRC}.jsonl", B_REC)]
LOG = OUT + "/kc103_regrid_w.log" + (".dry" if DRY else "")
CAPRG = 21600
SY103, SY95, SY87 = IN + "/kc103_syscheck_1025.py", IN + "/kc95_syscheck_1025.py", IN + "/kc87_syscheck_1025.py"

'''
new = head + body
wr(S + "/kc103d21125x_regrid_driver_1025.py", new)
d = "".join(difflib.unified_diff(t.splitlines(True), new.splitlines(True), "kc103d21_regrid_driver_1025.py", "kc103d21125x_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_kc103d21.txt", d)

# 2. the scan driver
t = rd(OLD + "/kc103d21_scan_driver_1025.py")
t = rep(t, [("t5's order, hc of 2026-11-24 ~15:47 UTC", "t5's order, hc of 2026-11-24 ~22:19 UTC"), ('"0.915,0.905;0.910;0.920,0.925;0.915"', '"0.885,0.875;0.880;0.890,0.895;0.885"'),
            ("on my regridded k_c 103 D 21.0 state", "on my regridded k_c 103 D 21.0 state (the cross-build repeat from dh170's k_c 95 D 21.0 state)"),
            ("the k_c 103 D 21.0 regrid is not accepted", "the k_c 103 D 21.0 cross-build regrid is not accepted")])
t = glob_rep(t)
wr(S + "/kc103d21125x_scan_driver_1025.py", t)

# 3. watcher, keep-awake, session check, sampler
for a in ("kc103d21_watch_alert_1025.py", "keepawake_1025.py", "session_check_1025.ps1"):
    t = glob_rep(rd(OLD + "/" + a))
    wr(S + "/" + a.replace("kc103d21_", "kc103d21125x_"), t)
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc103d21_1025.cmd")
t = rep(t, [("~15:47 UTC", "~22:19 UTC"), ('"0.915,0.905;0.910;0.920,0.925;0.915"', '"0.885,0.875;0.880;0.890,0.895;0.885"'), ("the k_c 103 D 21.0 chain", "the k_c 103 D 21.0 cross-build chain (from dh170's k_c 95 state)")])
wr(S + "/go_kc103d21125x_1025.cmd", glob_rep(t))
t = rd(OLD + "/publish_kc103d21_1025.sh")
t = rep(t, [("diff_regrid_driver_vs_kc95d21.txt", "diff_regrid_driver_vs_kc103d21.txt"), ("prep_kc103d21_pins_1025.txt", "prep_kc103d21_pins_1025.txt prep_source_checks_by_hand.txt")])
wr(S + "/publish_kc103d21125x_1025.sh", glob_rep(t))
os.chmod(S + "/publish_kc103d21125x_1025.sh", 0o755)
shutil.copyfile(OLD + "/kc103_syscheck_1025_vs_kc95.diff", S + "/kc103_syscheck_1025_vs_kc95.diff")
print("written")
