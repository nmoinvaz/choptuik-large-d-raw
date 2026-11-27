#!/usr/bin/env python3
"""#1104 winb, part 2 of the kappa 0.5 stage (part 1: make_k050d23_1104.py, the re-solve driver): derives the scan driver, the secant driver and the secant go cmd from my k_c 143 lane's drivers (kc143d23_1025, made for #1025) by
asserted text replacements; extends the publish script's file list. Refuses (assert) if a replacement does not find its text exactly the stated number of times."""
import os, re, subprocess

SRC = "C:/Users/nathan/Source/kc143d23_1025/"
DST = "C:/Users/nathan/Source/k050d23_1104/"
B_GATE = "d145145e22bf511011ca9ee2ecd8a14e2ce124e4"


def rd(n):
    return open(SRC + n, encoding="utf-8").read()


def wr(n, t, crlf=False):
    open(DST + n, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)


class Doc:
    def __init__(self, t, name):
        self.t, self.name = t, name

    def rep(self, a, b, n=1):
        assert self.t.count(a) == n, (self.name, self.t.count(a), a[:100])
        self.t = self.t.replace(a, b)

    def doc(self, new):
        i = self.t.index('"""')
        j = self.t.index('"""', i + 3)
        self.t = self.t[:i] + '"""' + new + '"""' + self.t[j + 3:]


# ---------------------------------------------------------------------------------------------- scan driver
d = Doc(rd("kc143d23_scan_driver_1025.py"), "scan")
d.doc("""#1104 winb, the scan of the kappa 0.5 state at D 23.0 with the RUST block 12 (t5's order, hc of 2026-11-27 18:23 UTC and #1104 comment 7225436553; the shares are an argument): d18_secant.py scan (branch wip/ell1-rust-b12
at d4b6b6ce, committed blob 9706e506, worktree choptuik-i1102) with --b12=rust --b12_threads=2 (ellrs from my #1102 build in i1102_1025/site, on PYTHONPATH, pinned by blob; OPENBLAS_NUM_THREADS=1), on my re-solved
k_c 143 kappa 0.5 state sol_l1kc143winbk050d23_D23.0000.npy and its record (both in this folder, checked against the blobs the re-solve driver wrote into regrid_accepted.txt), at the lambda shares LISTS (semicolon-separated,
one share per process, AT MOST TWO processes (t5); a value may appear twice: a repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, 2 Rust threads per process, BelowNormal, cap 43200 s by the exact pids.
Before the scan the tool's own selftest (exit 0 wanted) and its three mutations half, norobust, nosigncheck (exit 1 wanted each), and ell_b12rs.py's selftest with --mutate=nolam and --mutate=harm (exit 0, 1, 1) are run and
logged (selftest_d18_secant.txt, selftest_ell_b12rs.txt), and read_lower.py's selftest and its two --mutate controls (exit 0, 1, 1). d18_secant.py scan checks the pins and the record system first (exit 3 if not) and appends one
JSON line per lambda (d18_hybsign.py's fields plus dln, robust, sec_parts, b12, role scan) to its own file scan_k050_D23_p<i>.jsonl. Starts only when regrid_accepted.txt exists (and names the state and record blobs) and none
of the files it would write exists. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration. Then dh170's
read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder (it reads every scan_*_p*.jsonl), and an hc to the coordinator t5 with every line it printed. The refinement (d18_secant.py run) is NOT
chained here: I read the reader's lines first (t5: the secant on the change; widen to 0.065 and 0.140 if none; more than one change is a stop), push the scan files and start it by hand.
The widening round is this same driver run by hand: "0.065;0.140" --first=2 --window=0.065,0.14 (files scan_k050_D23_p2.jsonl and p3.jsonl, logs with the suffix _w, the reader on the window of all six points).
usage: k050d23_scan_driver_1104.py LISTS [--first=N] [--window=LO,HI] [--dry [--out=DIR]]     e.g. "0.095,0.080;0.110,0.125"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR; --first=N numbers the processes and files from N, for the widening round)""")
d.rep('OUT = S + "/I1025-win/kc143_d23"', 'OUT = S + "/I1104-win"')
d.rep('DS = "23.0"\n', 'DS = "23.0"\nFIRST = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--first=")), "0"))\n'
      'WINDOW = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--window=")), "")\nLBL, SFX = ("scan", "") if FIRST == 0 else ("scanw", "_w")\n')
d.rep("# the regridded state, record and marker (written by kc143d23_regrid_driver_1025.py)", "# the re-solved state, record and marker (written by k050d23_regrid_driver_1104.py)")
d.rep('TAG = "l1kc143winbd23"', 'TAG = "l1kc143winbk050d23"')
d.rep('LOG = OUT + "/kc143d23_scan_w.log"', 'LOG = OUT + f"/k050d23_scan{SFX}_w.log"')
d.rep('print("usage: kc143d23_scan_driver_1025.py LISTS [--dry [--out=DIR]]"); sys.exit(2)', 'print("usage: k050d23_scan_driver_1104.py LISTS [--first=N] [--window=LO,HI] [--dry [--out=DIR]]"); sys.exit(2)')
d.rep('LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"\n', 'LO, HI = f"{min(ALL):g}", f"{max(ALL):g}"\nif WINDOW:\n    LO, HI = [f"{float(v):g}" for v in WINDOW.split(",")]\n')
d.rep("#1025 k_c 143 D {DS} scan ({LO}-{HI}): {msg}", "#1104 kappa 0.5 k_c 143 D {DS} scan{' (widening)' if FIRST else ''} ({LO}-{HI}): {msg}")
d.rep('say(f"kc143d23_scan_driver_1025.py: the k_c 143 hybrid scan at D {DS}, shares {args[0]}', 'say(f"k050d23_scan_driver_1104.py: the kappa 0.5 k_c 143 hybrid scan at D {DS}, shares {args[0]}, first {FIRST}, reader window {LO} {HI}')
d.rep('"not started: the k_c 143 D 23.0 regrid is not accepted."', '"not started: the kappa 0.5 re-solve is not accepted."')
d.rep('SCANF = [OUT + f"/scan_kc143_D23_p{i}.jsonl" for i in range(len(SH))]', 'SCANF = [SRC + f"/scan_k050_D23_p{i + FIRST}.jsonl" for i in range(len(SH))]     # SRC is OUT in a real run (a dry run with --out=DIR checks DIR)')
d.rep('"/sample_driver_kc143_1025.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/scan_samples.csv"', '"/sample_driver_k050_1104.ps1", "-Drv", str(os.getpid()), "-Out", OUT + f"/rows/{LBL}_samples.csv"')
d.rep('S + "/kc143d23_watch_alert_1025.py", str(os.getpid()), "scan"]', 'S + "/k050d23_watch_alert_1104.py", str(os.getpid()), LBL]')
d.rep('S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)]', 'S + "/keepawake_1104.py", str(os.getpid()), LBL, str(CAP + 600)]')
d.rep('OUT + f"/rows/scan_p{i}_raw.log"', 'OUT + f"/rows/scan_p{i + FIRST}_raw.log"', 2)
d.rep("scan p{i}:", "scan p{i + FIRST}:", 3)
d.rep('g.write(f"== p{i}\\n")', 'g.write(f"== p{i + FIRST}\\n")')
d.rep('with open(OUT + "/scan_kc143_D23.log", "w") as g:', 'with open(OUT + f"/scan_k050_D23{SFX}.log", "w") as g:')
d.rep("Points so far in scan_kc143_D23_p*.jsonl.", "Points so far in scan_k050_D23_p*.jsonl.")
d.rep('say("kc143d23_scan_driver_1025.py done (no reading)")', 'say("k050d23_scan_driver_1104.py done (no reading)")')
d.rep('open(OUT + "/read_lower_kc143_D23.log", "w")', 'open(OUT + f"/read_lower_k050_D23{SFX}.log", "w")')
d.rep("Raw I1025-win/kc143_d23 after my next push; no reading by me, you rule.", "Raw I1104-win after my next push; no reading by me, you rule.")
d.rep('say("kc143d23_scan_driver_1025.py done")', 'say("k050d23_scan_driver_1104.py done")')
assert "kc143d23" not in d.t and "I1025" not in d.t.replace("raw I1025-dh170/lower_root", ""), [l for l in d.t.splitlines() if "kc143d23" in l or "I1025" in l]
wr("k050d23_scan_driver_1104.py", d.t)

# ---------------------------------------------------------------------------------------------- secant driver
d = Doc(rd("kc143d23_secant_driver_1025.py"), "secant")
d.doc("""#1104 winb, the secant refinement of the kappa 0.5 root at k_c 143, D 23.0 with the Rust block 12 (t5's order, hc of 2026-11-27 18:23 UTC and #1104 comment 7225436553: the secant at tol 5e-5 on the change): d18_secant.py run (branch
wip/ell1-rust-b12 at d4b6b6ce, committed blob 9706e506, worktree choptuik-i1102; Brent's method on the signed hybrid determinant) with --b12=rust --b12_threads=4 (ellrs from my #1102 build, i1102_1025/site, on PYTHONPATH, pinned
by blob; OPENBLAS_NUM_THREADS=1) on my accepted re-solved state sol_l1kc143winbk050d23_D23.0000.npy and its record l1kc143winbk050d23.jsonl (both in this folder; the blobs are the ones in regrid_accepted.txt), between LO HI
(arguments: the robust bracket the scan's reader printed), with the scan's two end records (--ends, verbatim lines of scan_k050_D23_p*.jsonl):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=5e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB --ends=scan_k050_D23_ends.jsonl --b12=rust --b12_threads=4     one process, BelowNormal
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py (blob 9706e506), ell_b12rs.py, the ellrs files of the site, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree (HEAD d4b6b6ce); the three checks and the gate (kc143 e15b0ee2,
     kc135 b353d466, kc127 898ebefa, gate_k050_1104.py d145145e); the state and the record against the blobs of regrid_accepted.txt; the ends file (blob from --ends-blob=) and its two lines verbatim in the scan files;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: the kappa 0.5 gate exits 0 (its --mutate=f and --mutate=steps exit 1) and kc143_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the
     k_c 135 and k_c 127 checks refuse them (exit 1 each);
  3b. the ends: scan_k050_D23_ends.jsonl is two lines, each verbatim a line of the scan files at lambda LO and HI;
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 43200 s (12 h; t5: stop and report on any step over 12 h), one hc to t5 at 21600 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs), 3 pin differs or not the record system. Its own records (one per evaluation
record) are appended to secant/secant.jsonl; the log is secant/secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it, as in my other drivers; nothing kills on memory.
usage: k050d23_secant_driver_1104.py LO HI --ends-blob=BLOB [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)""")
d.rep('OUT = S + "/I1025-win/kc143_d23"', 'OUT = S + "/I1104-win"')
d.rep('print("usage: kc143d23_secant_driver_1025.py LO HI --ends-blob=BLOB [--dry]")', 'print("usage: k050d23_secant_driver_1104.py LO HI --ends-blob=BLOB [--dry]")')
d.rep('STATE, STUB = OUT + "/sol_l1kc143winbd23_D23.0000.npy", OUT + "/l1kc143winbd23.jsonl"', 'STATE, STUB = OUT + "/sol_l1kc143winbk050d23_D23.0000.npy", OUT + "/l1kc143winbk050d23.jsonl"\nGATE = IN + "/gate_k050_1104.py"')
d.rep('ENDS = OUT + "/scan_kc143_D23_ends.jsonl"     # t5\'s order (hc 05:59 UTC): --ends, "Reuse the scan\'s ends": the two end records of the scan, verbatim lines of the scan files',
      'ENDS = OUT + "/scan_k050_D23_ends.jsonl"     # as in my k_c 143 lane: --ends, the two end records of the scan, verbatim lines of the scan files')
d.rep('(IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719", False), (STATE, B_STATE, False)', f'(IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719", False), (GATE, "{B_GATE}", False), (STATE, B_STATE, False)')
d.rep("#1025 k_c 143 D {D} secant refinement ({LO:g}-{HI:g}): {m}", "#1104 kappa 0.5 k_c 143 D {D} secant refinement ({LO:g}-{HI:g}): {m}")
d.rep('say(f"kc143d23_secant_driver_1025.py: the secant refinement of the k_c 143 root at D {D}', 'say(f"k050d23_secant_driver_1104.py: the secant refinement of the kappa 0.5 root at k_c 143, D {D}')
d.rep('glob.glob(OUT + "/scan_kc143_D23_p*.jsonl")', 'glob.glob(OUT + "/scan_k050_D23_p*.jsonl")')
d.rep("verbatim a line of scan_kc143_D23_p*.jsonl)", "verbatim a line of scan_k050_D23_p*.jsonl)")
d.rep("the three checks, the marker's state", "the three checks and the gate, the marker's state")
d.rep('("source_kc127_syscheck.txt", [PY, IN + "/kc127_syscheck_1025.py", STUB, STATE, D, WTM])):', '("source_kc127_syscheck.txt", [PY, IN + "/kc127_syscheck_1025.py", STUB, STATE, D, WTM]),\n'
      '                   ("source_gate.txt", [PY, GATE, STUB]), ("source_gate_mutate_f.txt", [PY, GATE, STUB, "--mutate=f"]), ("source_gate_mutate_steps.txt", [PY, GATE, STUB, "--mutate=steps"])):')
d.rep('"source_kc135_syscheck.txt": 1, "source_kc127_syscheck.txt": 1}', '"source_kc135_syscheck.txt": 1, "source_kc127_syscheck.txt": 1, "source_gate.txt": 0, "source_gate_mutate_f.txt": 1, "source_gate_mutate_steps.txt": 1}')
d.rep('f"kc135 check {src[\'source_kc135_syscheck.txt\']} and kc127 check {src[\'source_kc127_syscheck.txt\']} (1 wanted each: they refuse it); {time.time() - t0:.0f} s")',
      'f"kc135 check {src[\'source_kc135_syscheck.txt\']} and kc127 check {src[\'source_kc127_syscheck.txt\']} (1 wanted each: they refuse it), the kappa 0.5 gate {src[\'source_gate.txt\']} (0 wanted) and its --mutate=f {src[\'source_gate_mutate_f.txt\']}, --mutate=steps {src[\'source_gate_mutate_steps.txt\']} (1 wanted each); {time.time() - t0:.0f} s")')
d.rep('"/sample_driver_kc143_1025.ps1"', '"/sample_driver_k050_1104.ps1"')
d.rep('S + "/kc143d23_watch_alert_1025.py"', 'S + "/k050d23_watch_alert_1104.py"')
d.rep('S + "/keepawake_1025.py"', 'S + "/keepawake_1104.py"')
d.rep("Raw I1025-win/kc143_d23/secant after my next push", "Raw I1104-win/secant after my next push")
d.rep('say("kc143d23_secant_driver_1025.py done")', 'say("k050d23_secant_driver_1104.py done")')
assert "kc143d23" not in d.t and "I1025" not in d.t, [l for l in d.t.splitlines() if "kc143d23" in l or "I1025" in l]
wr("k050d23_secant_driver_1104.py", d.t)

GO = r"""@echo off
rem #1104 winb: the kappa 0.5 secant refinement (t5's order of 2026-11-27 18:23 UTC: the secant at tol 5e-5 on the change, the scan's ends reused): one driver, the scan's bracket LO HI and the ends blob are the arguments below (written when the scan was read).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\k050d23_1104
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_secant_driver_1104.py @@LO@@ @@HI@@ --ends-blob=@@BLOB@@ > C:\Users\nathan\Source\k050d23_1104\k050d23_secant_driver_stdout.log 2>&1
"""
open(DST + "go_secant_k050d23_1104.cmd.template", "w", encoding="utf-8", newline="\r\n").write(GO)
# publish script: the scan and secant files join the list
p = open(DST + "publish_k050d23_1104.sh", encoding="utf-8").read()
a = "k050d23_regrid_driver_stdout.log publish_k050d23_1104.sh push_1104.sh"
assert p.count(a) == 1 or "k050d23_scan_driver_1104.py" in p
if a in p:
    p = p.replace(a, "k050d23_scan_driver_1104.py k050d23_secant_driver_1104.py make_k050d23_1104_part2.py go_secant_k050d23_1104.cmd k050d23_regrid_driver_stdout.log k050d23_scan_driver_stdout.log k050d23_secant_driver_stdout.log "
                  "selftest_scan_dry_1104.txt selftest_secant_dry_1104.txt dry_tests_scan_1104.sh dry_test_secant_1104.sh publish_k050d23_1104.sh push_1104.sh")
open(DST + "publish_k050d23_1104.sh", "w", encoding="utf-8", newline="\n").write(p)
print("made part 2")
