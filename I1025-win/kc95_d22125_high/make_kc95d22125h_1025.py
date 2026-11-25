#!/usr/bin/env python3
"""make_kc95d22125h_1025.py: writes the k_c 95 HIGH scan stage's scripts (t5's order of 2026-11-25 ~09:30 UTC: dh610's accepted k_c 95 state at D 22.125, lambda 0.52 to 0.76 by 0.04 plus a repeat of 0.64)
from the k_c 103 D 21.75 stage's (staging kc103d2175_1025, raw I1025-win/kc103_d2175) by asserted text replacements: kc95d22125h_source_driver_1025.py (the regrid driver without its regrid: pins,
selftests, lambda_0, the source through the five checks, then the marker source_accepted.txt), kc95d22125h_scan_driver_1025.py, kc95d22125h_watch_alert_1025.py, keepawake_1025.py,
session_check_1025.ps1, sample_driver4_1025.ps1, go_kc95d22125h_1025.cmd, publish_kc95d22125h_1025.sh. Each asserted replacement must occur; the diff of the source driver against the regrid driver is written to
diff_source_driver_vs_regrid_driver.txt. The source (dh610's accepted k_c 95 D 22.125 state and record, raw I1025-dh610/kc95_d22125, commit ce4fce87f) and the pinned checks are in inputs/ already (copied from
git, blobs checked). There is no regrid here: the state is dh610's, scanned as it is."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc95d22125h_1025"
OLD = "C:/Users/nathan/Source/kc103d2175_1025"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert a in t, a[:120]
        t = t.replace(a, b)
    return t


def cut(t, a, b=None):
    """text from the first a to the first b after it (b not included; to the end if b is None)"""
    i = t.index(a)
    j = t.index(b, i) if b else len(t)
    return t[i:j]


def names(t):
    """the stage-wide renames, applied to every derived file after its own asserted edits"""
    t = t.replace("kc103d2175_scan_driver_1025", "kc95d22125h_scan_driver_1025").replace("kc103d2175_watch_alert_1025", "kc95d22125h_watch_alert_1025")
    t = t.replace("kc103d2175_source_driver_1025", "kc95d22125h_source_driver_1025").replace("kc103d2175_scan_w", "kc95d22125h_scan_w")
    t = t.replace("read_lower_kc103_D2175", "read_lower_kc95_D22125_high").replace("scan_kc103_D2175", "scan_kc95_D22125_high")
    t = t.replace("kc103_d2175", "kc95_d22125_high").replace("kc103d2175_1025", "kc95d22125h_1025").replace("go_kc103d2175_1025", "go_kc95d22125h_1025")
    t = t.replace("kc103d2175_scan_driver_stdout", "kc95d22125h_scan_driver_stdout")
    t = t.replace("regrid_accepted.txt", "source_accepted.txt")
    return t


for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc95dh610d22125_D22.1250.npy", "l1kc95dh610d22125.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f
os.makedirs(S + "/I1025-win/kc95_d22125_high/rows", exist_ok=True)

# 1. the source driver: the old regrid driver without the regrid
old = rd(OLD + "/kc103d2175_regrid_driver_1025.py")
head = '''#!/usr/bin/env python3
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


'''
# say, sh, blob, hc, stop (up to run_capped), then main from os.makedirs through the end of step 3
b1 = cut(old, "def say(m):", "def run_capped")
b1 = rep(b1, [("#1025 k_c 103 regrid at D 21.75 (from dh610's k_c 95 state): {m}", "#1025 k_c 95 HIGH scan at D 22.125 (dh610's state), source: {m}"),
              ('hc("not started or stopped: " + m)', 'hc("not started: " + m)')])
b2 = cut(old, 'os.makedirs(OUT + "/rows", exist_ok=True)', "# step 4: the regrid")
b2 = rep(b2, [
    ('"/rows/regrid_driver.pid"', '"/rows/source_driver.pid"'),
    ('say(f"kc103d2175_regrid_driver_1025.py: the k_c 103 regrid at D 21.75 from dh610\'s accepted k_c 95 D 21.75 state{\' (dry run)\' if DRY else \'\'}; checking pins")',
     'say(f"kc95d22125h_source_driver_1025.py: the source of the k_c 95 HIGH scan at D 22.125, dh610\'s accepted k_c 95 D 22.125 state{\' (dry run)\' if DRY else \'\'}; checking pins")'),
    ('for f in (WTM + "/data/" + STATE_N, WTM + f"/data/{TAG}.jsonl", OUT + "/regrid_accepted.txt", OUT + "/" + STATE_N):',
     'for f in (OUT + "/regrid_accepted.txt", OUT + "/" + STATE_N, OUT + f"/{SRC}.jsonl"):'),
    ('say(f"pins ok (the inputs of {IN}, dh610\'s k_c 95 D 21.75 files, worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")',
     'say(f"pins ok (the inputs of {IN}, dh610\'s k_c 95 D 22.125 files, worktree 48c36355 with solver code = 505d8399 and ell_delta/ell_refine = 48c36355); python {PY}")'),
    ('lam0_at(21.75, *', 'lam0_at(22.125, *'), ("ell_delta.lam0_at(21.75) is", "ell_delta.lam0_at(22.125) is"), ("ell_delta.lam0_at(21.75) = {LAM0}", "ell_delta.lam0_at(22.125) = {LAM0}"),
    ('say(f"DRY: would start ell_refine.py {SRC} 95 {TAG} 103 1 21.75 {LAM0} --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s); nothing started")',
     'say("DRY: would run the five source checks and write source_accepted.txt; nothing started")'),
    ('"/rows/regrid_samples.csv"', '"/rows/source_samples.csv"'), ('"regrid"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL', '"source"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL'),
    ('"regrid", str(CAPRG + 1800)]', '"source", "7200"]'),
    ('kc103d2175_watch_alert_1025.py', 'kc95d22125h_watch_alert_1025.py'),
    ('"21.75", WTM', '"22.125", WTM'),
    ('kc103d2175_regrid_driver_1025.py done', 'kc95d22125h_source_driver_1025.py done'),
    ('the source checks are not as wanted ({src}, wanted {want}): no regrid', 'the source checks are not as wanted ({src}, wanted {want}): no scan'),
    ('say(f"the source: kc95 check', 'say(f"the source: kc95 check'),
])
tail = '''
# step 4: the marker, the copies the scan driver reads, the sampler's last line
for f in (OUT + "/source_accepted.txt",):
    assert not os.path.exists(f), f
shutil.copy(SRCSTATE, OUT + "/" + STATE_N)
shutil.copy(SRCREC, OUT + f"/{SRC}.jsonl")
shutil.copy(IN + "/read_lower.py", OUT + "/read_lower.py")
open(OUT + "/source_accepted.txt", "w").write(f"ACCEPTED {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC\\nstate {blob(OUT + '/' + STATE_N)}\\nrecord {blob(OUT + f'/{SRC}.jsonl')}\\n")
recj = json.loads(open(SRCREC).read().strip().splitlines()[-1])
finish(0, f"the source is ACCEPTED (dh610's k_c 95 D 22.125 record: |F| {recj['F']}, steps {recj['steps']}, constraint {recj['constraint']}, Delta {recj['Delta']}; the checks as ordered). The scan 0.52-0.76 by 0.04 plus a repeat of 0.64 (8 evaluations, 4 processes) starts by itself now. Raw I1025-win/kc95_d22125_high after my next push.")
'''
new = head + b1 + b2.replace('"/regrid_accepted.txt"', '"/source_accepted.txt"') + tail
new = new.replace('OUT + "/regrid_accepted.txt"', 'OUT + "/source_accepted.txt"')
assert "regrid_accepted" not in new.replace("source_accepted", "")
# finish() sleeps for the sampler's last line and kills it; in the old code it is defined after the samplers start (inside b2 through 'def finish')
assert "def finish(code, m):" in new and "TAG" not in new and "CAPRG" not in new and "21.75" not in new and "21.7500" not in new, [w for w in ("TAG", "CAPRG", "21.75", "21.7500") if w in new]
wr(S + "/kc95d22125h_source_driver_1025.py", new)
wr(S + "/diff_source_driver_vs_regrid_driver.txt", "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "kc103d2175_regrid_driver_1025.py", "kc95d22125h_source_driver_1025.py")))

# 2. the scan driver
t = rd(OLD + "/kc103d2175_scan_driver_1025.py")
doc_new = '''#!/usr/bin/env python3
"""#1025 winb, the k_c 95 HIGH hybrid scan at D 22.125 on dh610's accepted k_c 95 D 22.125 state (t5's order, hc of 2026-11-25 ~09:30 UTC; the shares are an argument): xfkappa's d18_hybsign.py (raw I1025-mac/d18,
blob e089207a, unchanged) on the state sol_l1kc95dh610d22125_D22.1250.npy and its record (dh610's, raw I1025-dh610/kc95_d22125; copies in this folder, checked against the blobs the source driver wrote into
source_accepted.txt), at the lambda shares LISTS (semicolon-separated, one share per process, at most 4; a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign,
FOUR PROCESSES (one per share), ONE thread each, BelowNormal, cap 21600 s by the exact pids. d18_hybsign.py checks the record system first (exit 3 if the state does not come back) and appends one JSON line per lambda
to its own file scan_kc95_D22125_high_p<i>.jsonl. Starts only when source_accepted.txt exists (and names the state and record blobs) and no scan file exists. Memory: no guard, the alert-only watcher is its own
process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration.
Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys; its selftest and the two --mutate controls must give exit 0, 1, 1 before the scan starts) on the folder, and an hc to the
coordinator t5 with every line it printed.
usage: kc95d22125h_scan_driver_1025.py LISTS [--dry [--out=DIR]]     e.g. "0.60,0.52;0.64,0.56;0.68,0.72;0.64,0.76"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR)"""
'''
i = t.index("import datetime, os, re, subprocess, sys, time")
t = doc_new + t[i:]
t = rep(t, [
    ('DS = "21.75"', 'DS = "22.125"'),
    ('# the regridded state, record and marker (written by kc103d2175_regrid_driver_1025.py)', "# dh610's accepted state and record and the marker (copied and written by kc95d22125h_source_driver_1025.py)"),
    ('TAG = "l1kc103win2175"', 'TAG = "l1kc95dh610d22125"'), ('_D21.7500.npy', '_D22.1250.npy'),
    ('the k_c 103 D 21.75 regrid is not accepted', 'the source of the k_c 95 D 22.125 high scan is not accepted'),
    ('#1025 k_c 103 D {DS} scan ({LO}-{HI}): {msg}', '#1025 k_c 95 HIGH scan at D {DS} ({LO}-{HI}), dh610\'s state: {msg}'),
    ('the k_c 103 hybrid scan at D {DS}, shares', 'the k_c 95 high hybrid scan at D {DS}, shares'),
    ("the scan did not finish ({rc}; 3 = not the record system): no reading", "the scan did not finish ({rc}; 3 = not the record system): no reading"),
])
t = names(t)
for bad in ("103", "21.75", "2175", "D21.7500", "regrid", "Regrid"):
    assert bad not in t, (bad, [l for l in t.splitlines() if bad in l][:3])
wr(S + "/kc95d22125h_scan_driver_1025.py", t)

# 3. watcher, keep-awake, session check, sampler
t = rd(OLD + "/kc103d2175_watch_alert_1025.py")
t = rep(t, [("the k_c 103 stages at D 21.75", "the k_c 95 high-scan stages at D 22.125"), ("The k_c 103 D 21.75 {label} stage", "The k_c 95 high-scan D 22.125 {label} stage")])
t = names(t)
for bad in ("103", "21.75", "2175"):
    assert bad not in t, bad
wr(S + "/kc95d22125h_watch_alert_1025.py", t)
for a in ("keepawake_1025.py", "session_check_1025.ps1"):
    t = names(rd(OLD + "/" + a))
    assert "2175" not in t and "kc103" not in t, a
    wr(S + "/" + a, t)
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")
shutil.copyfile(OLD + "/kc103_syscheck_1025_vs_kc95.diff", S + "/kc103_syscheck_1025_vs_kc95.diff")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc103d2175_1025.cmd")
t = rep(t, [("the k_c 103 D 21.75 chain (from dh610's k_c 95 state) (t5's order of 2026-11-25 ~04:30 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered shares (6 evaluations, 4 processes).",
             "the k_c 95 HIGH scan at D 22.125 chain (dh610's accepted k_c 95 state, not regridded) (t5's order of 2026-11-25 ~09:30 UTC): step 1, the source driver (pins, selftests, the source checks); step 2 only if source_accepted.txt exists, the scan driver with the ordered shares (8 evaluations, 4 processes)."),
            ("kc103d2175_regrid_driver_1025.py", "kc95d22125h_source_driver_1025.py"), ("kc103d2175_regrid_driver_stdout.log", "kc95d22125h_source_driver_stdout.log"),
            ('"0.645,0.635;0.640;0.650,0.655;0.645"', '"0.60,0.52;0.64,0.56;0.68,0.72;0.64,0.76"')])
t = names(t)
assert "2175" not in t and "103" not in t and "regrid_" not in t, [l for l in t.splitlines() if "103" in l or "regrid_" in l]
wr(S + "/go_kc95d22125h_1025.cmd", t)
t = rd(OLD + "/publish_kc103d2175_1025.sh")
t = rep(t, [("copy the staged k_c 103 D 21.75 folder", "copy the staged k_c 95 high-scan D 22.125 folder"),
            ("make_kc103d2175_1025.py kc103_syscheck_1025_vs_kc95.diff diff_regrid_driver_vs_crossbuild.txt kc103d2175_regrid_driver_1025.py kc103d2175_scan_driver_1025.py",
             "make_kc95d22125h_1025.py kc103_syscheck_1025_vs_kc95.diff diff_source_driver_vs_regrid_driver.txt kc95d22125h_source_driver_1025.py kc95d22125h_scan_driver_1025.py"),
            ("kc103d2175_regrid_driver_stdout.log", "kc95d22125h_source_driver_stdout.log"), ("prep_kc103d2175_pins_1025.txt", "prep_kc95d22125h_pins_1025.txt"),
            ("publish_kc103d2175_1025.sh", "publish_kc95d22125h_1025.sh"), ("kc103d2175_scan_driver_stdout.log", "kc95d22125h_scan_driver_stdout.log")])
t = names(t.replace("kc103d2175_watch_alert_1025.py", "kc95d22125h_watch_alert_1025.py"))
assert "2175" not in t and "103d" not in t, [l for l in t.splitlines() if "2175" in l or "103d" in l]
wr(S + "/publish_kc95d22125h_1025.sh", t)
os.chmod(S + "/publish_kc95d22125h_1025.sh", 0o755)
print("written")
