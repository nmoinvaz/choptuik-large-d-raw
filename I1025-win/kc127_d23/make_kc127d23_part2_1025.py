#!/usr/bin/env python3
"""make_kc127d23_part2_1025.py: writes the k_c 127 D 23.0 lane's scan and secant drivers by asserted text replacements:
kc127d23_scan_driver_1025.py from my k_c 103 D 22.875 scan driver (staging kc103d22875_1025: the new scanner d18_secant.py scan at 92b9bf53 in place of d18_hybsign.py, at most 2 processes, cap 43200 s, the
selftest of the tool and its three mutations logged first), diff_scan_driver_vs_kc103.txt; kc127d23_secant_driver_1025.py from my k_c 87 D 22.875 secant driver (staging kc87d22875s_1025: the tool at 92b9bf53,
my regridded k_c 127 state and record pinned by the marker's blobs, the k_c 127 check as the acceptance, cap 43200 s), diff_secant_driver_vs_kc87.txt."""
import difflib, os

S = "C:/Users/nathan/Source/kc127d23_1025"
OLD_SCAN = "C:/Users/nathan/Source/kc103d22875_1025/kc103d22875_scan_driver_1025.py"
OLD_SEC = "C:/Users/nathan/Source/kc87d22875s_1025/kc87d22875s_secant_driver_1025.py"
TOOL92, HEAD92 = "eb1396ad39d9236ae983064da5702164947e0948", "92b9bf533ff371247be642c47e067a9042cabed1"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert t.count(a) == 1, a[:150]
        t = t.replace(a, b)
    return t


# ------------------------------------------------------------------ the scan driver
t = rd(OLD_SCAN)
i = t.index('"""')
j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the k_c 127 scan at D 23.0 (t5's order, hc of 2026-11-26 ~10:40 UTC, step 4a; the shares are an argument): the NEW scanner, d18_secant.py scan (branch wip/ell1-speed at 92b9bf53, committed blob eb1396ad,
worktree choptuik-i1025secant92), on my regridded k_c 127 state sol_l1kc127wind23_D23.0000.npy and its record (both in this folder, checked against the blobs the regrid driver wrote into regrid_accepted.txt), at the lambda shares
LISTS (semicolon-separated, one share per process, AT MOST TWO (t5: a k_c 127 process may need 8 GB); a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, ONE thread each,
BelowNormal, cap 43200 s by the exact pids. Before the scan the tool's own selftest (exit 0 wanted) and its three mutations half, norobust, nosigncheck (exit 1 wanted each) are run and logged (selftest_d18_secant.txt), and read_lower.py's
selftest and its two --mutate controls (exit 0, 1, 1). d18_secant.py scan checks the pins and the record system first (exit 3 if not) and appends one JSON line per lambda (d18_hybsign.py's fields plus dln, robust, sec_parts, role scan) to its
own file scan_kc127_D23_p<i>.jsonl. Starts only when regrid_accepted.txt exists (and names the state and record blobs) and no scan file exists. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds
SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration. Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder, and an hc to the coordinator t5 with every line it
printed. The refinement (d18_secant.py run) is NOT chained here: I read the reader's lines first (t5's stop: no robust change or more than one) and start it by hand.
usage: kc127d23_scan_driver_1025.py LISTS [--dry [--out=DIR]]     e.g. "0.04,0.03,0.06;0.05,0.04"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ('OUT = S + "/I1025-win/kc103_d22875"', 'OUT = S + "/I1025-win/kc127_d23"'),
    ('WT = "C:/Users/nathan/Source/choptuik-i1025k79"', 'WT = "C:/Users/nathan/Source/choptuik-i1025secant92"'),
    ('DS = "22.875"', 'DS = "23.0"'),
    ('SCANNER, READER = RAWM + "/d18_hybsign.py", RAWM + "/read_lower.py"', 'SCANNER, READER = WTM + "/d18_secant.py", RAWM + "/read_lower.py"'),
    ('TAG = "l1kc103win22875"', 'TAG = "l1kc127wind23"'),
    ('STATE, REC = SRC + f"/sol_{TAG}_D22.8750.npy", SRC + f"/{TAG}.jsonl"', 'STATE, REC = SRC + f"/sol_{TAG}_D23.0000.npy", SRC + f"/{TAG}.jsonl"'),
    ('CAP = 21600', 'CAP = 43200'),
    ("if not 1 <= len(SH) <= 4 or", "if not 1 <= len(SH) <= 2 or"),
    ('print("REFUSE: wanted 1 to 4 non-empty shares,', 'print("REFUSE: wanted 1 to 2 non-empty shares,'),
    ('PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER,', 'PINS = [(SCANNER, "' + TOOL92 + '"), (READER,'),
    ('for fn, want in PINS:\n    got = sh(["git", "hash-object", "--no-filters", fn]).stdout.strip()', 'for fn, want in PINS:\n    got = sh(["git", "hash-object"] + ([] if fn == SCANNER else ["--no-filters"]) + [fn]).stdout.strip()'),
    ('if head != "48c36355d1ba64de4e3112ed968fd6c034384551" or', 'if head != "' + HEAD92 + '" or'),
    ('"not started: worktree or scan file check failed."', '"not started: worktree or scan file check failed."'),
    ('refuse(f"worktree at {head[:8]}, not 48c36355, or a scan file exists",', 'refuse(f"worktree at {head[:8]}, not 92b9bf53, or a scan file exists",'),
    ('"-File", S + "/sample_driver4_1025.ps1"', '"-File", S + "/sample_driver_kc127_1025.ps1"'),
    ('cmds = [[PY, "-u", SCANNER, REC, STATE, DS, ",".join(f"{v:g}" for v in sh_), SCANF[i]] for i, sh_ in enumerate(SH)]',
     'PINARG = f"--pin={mk[5]},{mk[7]}" if len(mk) > 7 else "--pin=0,0"\ncmds = [[PY, "-u", SCANNER, "scan", REC, STATE, DS, ",".join(f"{v:g}" for v in sh_), SCANF[i], PINARG] for i, sh_ in enumerate(SH)]'),
    ('say(f"scan p{i}: started pid {p.pid}: d18_hybsign.py {REC} {STATE} {DS} {c[6]} {SCANF[i]}")', 'say(f"scan p{i}: started pid {p.pid}: d18_secant.py scan {REC} {STATE} {DS} {c[7]} {SCANF[i]} {PINARG}")'),
    ('if not os.path.exists(SRC + "/regrid_accepted.txt"):', 'mk = []\nif not os.path.exists(SRC + "/regrid_accepted.txt"):'),
    ('renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")\n',
     'renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")\n'
     'ex0 = []\nfor mut in ("", "--mutate=half", "--mutate=norobust", "--mutate=nosigncheck"):\n'
     '    r1 = sh([PY, "-u", SCANNER, "selftest"] + ([mut] if mut else []), cwd=WTM, env=dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1"))\n'
     '    ex0.append(r1.returncode)\n'
     '    open(OUT + "/selftest_d18_secant.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC d18_secant.py (92b9bf53, blob eb1396ad) selftest {mut}\\n" + r1.stdout + r1.stderr + f"exit {r1.returncode} ({0 if not mut else 1} wanted)\\n")\n'
     'if ex0 != [0, 1, 1, 1]:\n    refuse(f"d18_secant.py selftest and its three mutations (half, norobust, nosigncheck) gave exits {ex0}, wanted [0, 1, 1, 1]", f"not started: d18_secant.py selftest/mutations exits {ex0}, wanted [0, 1, 1, 1].")\n'
     'else:\n    say("d18_secant.py (92b9bf53, blob eb1396ad) selftest exit 0 and its three mutations half, norobust, nosigncheck exit 1, 1, 1 as wanted")\n'),
])
t = t.replace("scan_kc103_D22875", "scan_kc127_D23").replace("read_lower_kc103_D22875", "read_lower_kc127_D23").replace("kc103d22875_", "kc127d23_").replace("kc103_d22875", "kc127_d23")
t = t.replace("k_c 103", "k_c 127").replace("22.875", "23.0")
for bad in ("kc103", "103", "22.8", "D22", "hybsign.py {REC}", "21600", "e089207a", "48c36355"):
    assert bad not in t.replace("1025", ""), (bad, t[max(0, t.index(bad) - 100):t.index(bad) + 80])
wr(S + "/kc127d23_scan_driver_1025.py", t)
wr(S + "/diff_scan_driver_vs_kc103.txt", "".join(difflib.unified_diff(rd(OLD_SCAN).splitlines(True), t.splitlines(True), "kc103d22875_scan_driver_1025.py", "kc127d23_scan_driver_1025.py")))

# ------------------------------------------------------------------ the secant driver
t = rd(OLD_SEC)
i = t.index('"""')
j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the secant refinement of the k_c 127 root at D 23.0 (t5's order, hc of 2026-11-26 ~10:40 UTC, step 4b): xfkappa's d18_secant.py run (branch wip/ell1-speed at 92b9bf53, committed blob eb1396ad; Brent's method on the hybrid sign;
worktree choptuik-i1025secant92) on my accepted k_c 127 state sol_l1kc127wind23_D23.0000.npy and its record l1kc127wind23.jsonl (both in this folder; the blobs are the ones in regrid_accepted.txt), between LO HI (arguments: the robust bracket
the scan's reader printed):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB     one process, BelowNormal, 1 thread (OMP/OPENBLAS/MKL 1 too)
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree (HEAD 92b9bf53); the three checks (kc111 85aeb312, kc119 fc6e0dd6, kc127 898ebefa); the state and the record against the marker's blobs;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc127_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 119 and k_c 111 checks refuse them (exit 1 each);
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 43200 s (12 h; t5: stop and report on any step over 12 h), one hc to t5 at 21600 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs), 3 pin differs or not the record system. Its own records (one per evaluation, then a root
record) are appended to secant/secant.jsonl; the log is secant/secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it, as in my other drivers; nothing kills on memory.
usage: kc127d23_secant_driver_1025.py LO HI [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ('OUT = S + "/I1025-win/kc87_d22875_secant"\nSEC = OUT', 'OUT = S + "/I1025-win/kc127_d23"\nSEC = OUT + "/secant"'),
    ('WTS = "C:/Users/nathan/Source/choptuik-i1025secant"', 'WTS = "C:/Users/nathan/Source/choptuik-i1025secant92"'),
    ('D = "22.875"', 'D = "23.0"'),
    ('STATE, STUB = OUT + "/in/sol_l1kc87Lmacm3c_D22.875000.npy", OUT + "/in/l1kc87Lmacm3c.jsonl"\nB_STATE, B_STUB = "b1e4f8cad92d4384f3c2e2dffe15cd2b801251dd", "338bd7f1afa55d6afd80f03051402b855e198a3f"',
     'STATE, STUB = OUT + "/sol_l1kc127wind23_D23.0000.npy", OUT + "/l1kc127wind23.jsonl"\n_mk = open(OUT + "/regrid_accepted.txt").read().split() if os.path.exists(OUT + "/regrid_accepted.txt") else []\n'
     'B_STATE, B_STUB = (_mk[5], _mk[7]) if len(_mk) > 7 and _mk[0] == "ACCEPTED" else ("0" * 40, "0" * 40)'),
    ('(WTM + "/d18_secant.py", "a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49", True)', '(WTM + "/d18_secant.py", "' + TOOL92 + '", True)'),
    ('(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6", False), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883", False),\n        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d", False),',
     '(IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719", False), (IN + "/kc119_syscheck_1025.py", "fc6e0dd6fbdf6bcf8fb6a2bf9274e404e3caa7ad", False),\n        (IN + "/kc111_syscheck_1025.py", "85aeb31275aa9fd3edb786c74d91e69390a1dc75", False),'),
    ("CAP, NOTIFY = 28800, 14400", "CAP, NOTIFY = 43200, 21600"),
    ('!= "6010e37b30f92688dd5c659e383c6d0c8d14b6da":\n    refuse("the secant worktree is not at 6010e37b")', '!= "' + HEAD92 + '":\n    refuse("the secant worktree is not at 92b9bf53")'),
    ("pins ok (worktree 6010e37b, d18_secant.py a3d90cd5, ell_fastm.py 93f963f6, the solver files equal to my regrids', the three checks, state", "pins ok (worktree 92b9bf53, d18_secant.py eb1396ad, ell_fastm.py 93f963f6, the solver files equal to my regrids', the three checks, the marker's state"),
    ('"/sample_driver_secant_1025.ps1"', '"/sample_driver_kc127_1025.ps1"'),
    ('S + "/kc87d22875s_watch_alert_1025.py"', 'S + "/kc127d23_watch_alert_1025.py"'),
    ("(4 h), {n} evaluation record(s) so far; it is killed by the exact pid at {CAP} s (8 h, your stop).", "(6 h), {n} evaluation record(s) so far; it is killed by the exact pid at {CAP} s (12 h, your stop)."),
    ("Raw I1025-win/kc103_d22875/secant after my next push", "Raw I1025-win/kc127_d23/secant after my next push"),
    ('st = {}\nfor k in (95, 87, 103):', 'st = {}\nfor k in (127, 119, 111):'),
    ('refuse(f"the selftests of the k_c 95, 87 and 103 checks gave exits {st}, wanted 0 each")', 'refuse(f"the selftests of the k_c 127, 119 and 111 checks gave exits {st}, wanted 0 each")'),
    ("if st != {95: 0, 87: 0, 103: 0}:", "if st != {127: 0, 119: 0, 111: 0}:"),
])
# the role renames of the checks (target kc87 -> kc127, refuse kc95 -> kc119, kc103 -> kc111)
t = t.replace("kc87d22875s_", "kc127d23_").replace("kc87d22875s", "kc127d23")
for a_, b_ in (("kc87", "@@A@@"), ("kc95", "@@B@@"), ("kc103", "@@C@@")):
    t = t.replace(a_, b_)
t = t.replace("@@A@@", "kc127").replace("@@B@@", "kc119").replace("@@C@@", "kc111")
t = t.replace("k_c 87", "k_c 127").replace("kc87d22875s_", "kc127d23_").replace("kc87d22875s", "kc127d23").replace("22.875", "23.0")
for bad in ("22875", "kc87", "kc95", "kc103", "k_c 87", "k_c 95", "k_c 103", "6010e37b", "a3d90cd5", "28800", "22.8", "D22", "kc87_d22875", "b1e4f8ca", "338bd7f1"):
    assert bad not in t, (bad, t[max(0, t.index(bad) - 100):t.index(bad) + 80])
wr(S + "/kc127d23_secant_driver_1025.py", t)
wr(S + "/diff_secant_driver_vs_kc87.txt", "".join(difflib.unified_diff(rd(OLD_SEC).splitlines(True), t.splitlines(True), "kc87d22875s_secant_driver_1025.py", "kc127d23_secant_driver_1025.py")))
print("part 2 written")
