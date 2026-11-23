#!/usr/bin/env python3
"""#1025 winb, k_c 95 at D 19 from my accepted k_c 87 D 19 state (t5's order, #1025 comment of 2026-11-23 12:45 UTC): derives the regrid driver, scan driver, watcher, keep-awake helper, session check, go file
and publish script from the k_c 87 D 19 ones (C:/Users/nathan/Source/kc87d19_1025, raw I1025-win/kc87_d19 at 3b833805) and writes a diff against each (diff_*_vs_kc87d19.txt).
The roles move one k_c up: the old SOURCE k_c 79 becomes k_c 87 (my accepted state, tag l1kc87wind19), the old TARGET k_c 87 becomes k_c 95 (tag l1kc95wind19). The mapping is done in this order, so nothing is mapped twice:
  1. explicit replacements of the command lines and the pin block (asserted),  2. kc87 -> kc95 (and k_c 87, SY87, st87, s87),  3. the source tag l1kc79W19m1025 -> l1kc87wind19,  4. kc79 -> kc87 (and k_c 79, SY79, st79, k79).
Then the asserted specifics: the pins (dh610's kc95_syscheck_1025.py d487e628, my k_c 87 state/record/marker blobs), the docstrings, the hc prefixes, the window, the caps (scan cap 64800 s for 15 points), the dry-run text.
Afterwards it prints every line of each derived file that still names 79, 87 or 95 for reading (the diffs are published too)."""
import difflib, os, re

A = "C:/Users/nathan/Source/kc87d19_1025"
B = "C:/Users/nathan/Source/kc95d19_1025"
os.makedirs(B + "/I1025-win/kc95_d19/rows", exist_ok=True)
WIN = "1.395,1.400,1.405,1.410,1.415,1.420,1.425,1.430,1.435,1.530,1.535,1.540,1.545,1.550,1.415"
OLDWIN = "1.380,1.405,1.430,1.455,1.480,1.505,1.530,1.555,1.580,1.480"


def sub(s, old, new, n=1, what=""):
    assert s.count(old) == n, f"{what or old[:70]!r}: found {s.count(old)}, wanted {n}"
    return s.replace(old, new)


def mapk(s, regrid=False):
    """kc87 -> kc95, then the source tag, then kc79 -> kc87 (the same order everywhere)"""
    for o, n in (("kc87", "kc95"), ("k_c 87", "k_c 95"), ("SY87", "SY95"), ("st87", "st95"), ("s87", "s95")):
        s = s.replace(o, n)
    s = s.replace("l1kc79W19m1025", "l1kc87wind19")
    for o, n in (("kc79", "kc87"), ("k_c 79", "k_c 87"), ("SY79", "SY87"), ("st79", "st87"), ("k79", "k87")):
        s = s.replace(o, n)
    return s


made = {}
# ---- the regrid driver: docstring and pin block are written out, the code is mapped
s = open(A + "/kc87d19_regrid_driver_1025.py").read()
i, j = s.index('"""'), s.index("import csv,")
doc = '''"""#1025 winb, the k_c 95 regrid at D 19 (t5's order, #1025 comment of 2026-11-23 12:45 UTC): my accepted k_c 87 D 19 state (raw I1025-win/kc87_d19 at 3b833805, tag l1kc87wind19) is regridded to k_c 95 with
  ell_refine.py l1kc87wind19 87 l1kc95wind19 95 1 19.0 LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (LAM0 = ell_delta.lam0_at(19.0, *lam0_table())[0] = 2.1156378446, unused with --no-gamma)
4 threads, BelowNormal, cap 21600 s by the exact pid, one process outside my terminal. Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: dh610's kc87_syscheck_1025.py (6df5d960) and kc95_syscheck_1025.py (d487e628, the version dh610 used at D 19.5, raw I1025-dh610/kc95_d195/in/; the k_c 87 check with the k_c test changed to 95:
     3 changed lines, its kc95_syscheck_1025.diff), d18_hybsign.py, d185_scan_read.py, read_lower.py, the k_c 87 D 19 state, record and marker, the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399,
     ell_refine.py 631e5801) and its copies of the source state and record;
  2. the selftest of both checks (exit 0 each);
  3. the SOURCE: the k_c 87 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 95 check refuses it (exit 1);
  4. the regrid;
  5. ACCEPTED only if kc95_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc87_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc95d19_1025.cmd). Memory: no guard, the alert-only watcher is a separate
process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc95d19_regrid_driver_1025.py [--dry]     (--dry: pins and the two selftests only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""
'''
head, body = s[:i], s[j:]
# the pin block of the old driver is replaced as a whole (it names source blobs and the old check)
a = body.index("PINS = [")
b = body.index("LOG = OUT")
body = body[:a] + "@@PINS@@\n" + body[b:]
# explicit command lines (before the generic mapping)
body = sub(body, 'cmd = ["-u", "ell_refine.py", SRC, "79", TAG, "87", "1", "19.0", LAM0,', 'cmd = ["-u", "ell_refine.py", SRC, "87", TAG, "95", "1", "19.0", LAM0,', 1, "cmd list")
body = sub(body, "ell_refine.py {SRC} 79 {TAG} 87 1 19.0 {LAM0}", "ell_refine.py {SRC} 87 {TAG} 95 1 19.0 {LAM0}", 1, "dry text")
body = sub(body, "The scan 1.380-1.580 by 0.025 plus a repeat of 1.480 starts by itself now.", "The scan 1.395-1.435 and 1.530-1.550 by 0.005 plus a repeat of 1.415 (15 evaluations) starts by itself now.", 1, "final hc")
# generic mapping
body = mapk(body)
assert body.count("choptuik-i1025k87") == 1, body.count("choptuik-i1025k87")
body = body.replace("choptuik-i1025k87", "choptuik-i1025k79")      # the worktree keeps its name (k79 -> k87 is for the variable only)
assert "k_c 79" not in body and "kc79" not in body
pins_text = '''PINS = [(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"),
        (IN + "/d18_hybsign.py", "e089207a61fbd98614716abd309571cbc4888db2"), (IN + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"), (IN + "/read_lower.py", "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"),
        (SRCSTATE, "100f63f7a2f9a3e3ee3ff845bfd791f3829da1b9"), (SRCREC, "4fae16215e65c687189e911af17976785f6aaf59"), (SRCD + "/regrid_accepted.txt", "3d80146944abb67be68a05bb4c7be81734b192f2"),
        (WTM + f"/data/sol_{SRC}_D19.0000.npy", "100f63f7a2f9a3e3ee3ff845bfd791f3829da1b9"), (WTM + f"/data/{SRC}.jsonl", "4fae16215e65c687189e911af17976785f6aaf59")]
'''

assert body.count("@@PINS@@") == 1
body = body.replace("@@PINS@@\n", pins_text)
s2 = head + doc + body
made["kc95d19_regrid_driver_1025.py"] = s2

# ---- the scan driver
s = open(A + "/kc87d19_scan_driver_1025.py").read()
s = sub(s, "the k_c 87 hybrid scan at D 19 on my regridded k_c 87 D 19 state (t5's order, #1025 comment of 2026-11-23 05:10 UTC, step 2 after ACCEPTED; the window is an argument)",
        "the k_c 95 hybrid scan at D 19 on my regridded k_c 95 D 19 state (t5's order, #1025 comment of 2026-11-23 12:45 UTC, after ACCEPTED; the window is an argument)", 1, "doc 1")
s = sub(s, "BelowNormal, cap 36000 s (10 h) by the exact pid.", "BelowNormal, cap 64800 s (18 h) by the exact pid (15 evaluations).", 1, "doc cap")
s = sub(s, "e.g. " + OLDWIN, "e.g. " + WIN, 1, "usage")
s = sub(s, "CAP = 36000", "CAP = 64800", 1, "cap")
s = sub(s, "#1025 k_c 87 D 19 scan (1.38-1.58): {msg}", "#1025 k_c 95 D 19 scan (1.395-1.435 and 1.530-1.550): {msg}", 1, "hc prefix")
s = sub(s, "the regrid driver wrote", "the regrid driver wrote", 1, "unchanged text")
for o, n in (("kc87", "kc95"), ("k_c 87", "k_c 95")):
    s = s.replace(o, n)
assert "kc79" not in s and "k_c 79" not in s
made["kc95d19_scan_driver_1025.py"] = s

# ---- watcher, keep-awake, session check, publish script, launcher
for src, dst in (("kc87d19_watch_alert_1025.py", "kc95d19_watch_alert_1025.py"), ("keepawake_1025.py", "keepawake_1025.py"), ("session_check_1025.ps1", "session_check_1025.ps1")):
    t = open(A + "/" + src).read()
    for o, n in (("kc87", "kc95"), ("k_c 87", "k_c 95")):
        t = t.replace(o, n)
    made[dst] = t
t = open(A + "/publish_kc87d19_1025.sh").read()
for o, n in (("kc87", "kc95"), ("k_c 87", "k_c 95")):
    t = t.replace(o, n)
t = sub(t, "diff_scan_driver_vs_gap.txt diff_watcher_vs_gap.txt diff_regrid_driver_vs_d19.txt", "diff_scan_driver_vs_kc87d19.txt diff_watcher_vs_kc87d19.txt diff_regrid_driver_vs_kc87d19.txt kc95_syscheck_1025_dh610.diff", 1, "pub diffs")
assert "make_kc95d19_1025.py" in t
made["publish_kc95d19_1025.sh"] = t
t = open(A + "/go_kc87d19_1025.cmd").read()
t = sub(t, "the k_c 87 D 19 chain (t5's order of 2026-11-23 05:10 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered window.",
        "the k_c 95 D 19 chain (t5's order of 2026-11-23 12:45 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered window (15 evaluations).", 1, "go rem")
t = sub(t, OLDWIN, WIN, 1, "go window")
for o, n in (("kc87", "kc95"), ("k_c 87", "k_c 95")):
    t = t.replace(o, n)
made["go_kc95d19_1025.cmd"] = t

for name, text in made.items():
    open(f"{B}/{name}", "w", newline="\n").write(text)
for key, (name, srcname) in {"regrid_driver": ("kc95d19_regrid_driver_1025.py", "kc87d19_regrid_driver_1025.py"), "scan_driver": ("kc95d19_scan_driver_1025.py", "kc87d19_scan_driver_1025.py"),
                             "watcher": ("kc95d19_watch_alert_1025.py", "kc87d19_watch_alert_1025.py")}.items():
    d = "".join(difflib.unified_diff(open(f"{A}/{srcname}").read().splitlines(1), open(f"{B}/{name}").read().splitlines(1), srcname, name, n=0))
    open(f"{B}/diff_{key}_vs_kc87d19.txt", "w", newline="\n").write(d)
print("derived:", ", ".join(made))
for name in made:
    for n, ln in enumerate(open(f"{B}/{name}").read().splitlines(), 1):
        if re.search(r"\b79\b|\bkc79|k_c 79|\b87\b|kc87|k_c 87|SY87|SY79", ln):
            print(f"  {name}:{n}: {ln[:200]}")
