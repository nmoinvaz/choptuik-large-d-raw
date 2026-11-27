#!/usr/bin/env python3
"""#1025 winb, the k_c 143 lane at D 23.0 (t5's order, hc of 2026-11-27 05:59 UTC): derives this stage's files from the k_c 127 stage (kc127d23_1025) by one simultaneous renaming (k_c 127 -> 143,
119 -> 135, 111 -> 127 in the check names; the blobs of the three checks and of the source files; l1kc127wind23 -> l1kc143winbd23, l1kc119macm3d23 -> l1kc135win2d23) and asserted text replacements.
Run once from anywhere; refuses (assert) if a replacement does not find its text exactly the stated number of times. Output: the drivers, the watcher, the sampler, the keep-awake helper and the session check,
the two go cmds and the publish script, in this folder, and diff_*_driver_vs_kc127.txt."""
import os, re, subprocess

SRC = "C:/Users/nathan/Source/kc127d23_1025/"
DST = "C:/Users/nathan/Source/kc143d23_1025/"
BLOBS = {
    "85aeb31275aa9fd3edb786c74d91e69390a1dc75": "898ebefa65a99e639110e018808c85506a7f5719",     # kc111 check -> kc127 check
    "fc6e0dd6fbdf6bcf8fb6a2bf9274e404e3caa7ad": "b353d46696d2c90eb413fb071becb3e9aa8f976a",     # kc119 -> kc135
    "898ebefa65a99e639110e018808c85506a7f5719": "e15b0ee2b0b1f9e48a914b6e3e75f4fec48251f4",     # kc127 -> kc143
    "2771cf87ee8ca5c9ac32d5289397eace6bc1924b": "cd134e2cc283fd5beb2e5beb6ad2e1f1353efe1d",     # macm3's k_c 119 state -> win2's k_c 135 state
    "158e30868886465e4226a45de8975a5693852049": "bc295fbcc4a90adaf224128d0160ce02ce68a0f7",     # its record
    "85aeb312": "898ebefa", "fc6e0dd6": "b353d466", "898ebefa": "e15b0ee2", "2771cf87": "cd134e2c", "158e3086": "bc295fbc",
}
NUM = {"127": "143", "119": "135", "111": "127"}
B_SCANNER = "9706e506111357e5e6a3f1bccd60154ac3d17cbc"       # d18_secant.py at wip/ell1-rust-b12 d4b6b6ce
B_B12RS = "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef"         # ell_b12rs.py
B_PYD = "ddd5a08281f4aa325bd8564f08f9f2c3cebba33d"           # site/ellrs/ellrs.cp314-win_amd64.pyd (built 2026-11-27 05:54 UTC, my #1102 gate)
B_INIT = "76c7cfbc8fdfe90adb0debb60ac2d4754974cb1d"          # site/ellrs/__init__.py
HEAD_RS = "d4b6b6cea24f518d38cac17877c9a0da813b05f4"
SITE = "C:/Users/nathan/Source/i1102_1025/site"


def ren(t):
    t = t.replace("l1kc127wind23", "@@TAG@@").replace("l1kc119macm3d23", "@@SRC@@")
    t = re.sub("|".join(sorted(map(re.escape, BLOBS), key=len, reverse=True)), lambda m: BLOBS[m.group(0)], t)
    t = re.sub(r"(kc|k_c )(127|119|111)", lambda m: m.group(1) + NUM[m.group(2)], t)
    t = re.sub(r"\b(SY|st|s|k)(127|119|111)\b", lambda m: m.group(1) + NUM[m.group(2)], t)
    return t.replace("@@TAG@@", "l1kc143winbd23").replace("@@SRC@@", "l1kc135win2d23")


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

    def rx(self, pat, b, n=1, flags=re.S):
        m = re.findall(pat, self.t, flags)
        assert len(m) == n, (self.name, len(m), pat)
        self.t = re.sub(pat, lambda _m: b, self.t, flags=flags)

    def doc(self, new):
        i = self.t.index('"""')
        j = self.t.index('"""', i + 3)
        self.t = self.t[:i] + '"""' + new + '"""' + self.t[j + 3:]


# ---------------------------------------------------------------------------------------------- regrid driver
d = Doc(ren(rd("kc127d23_regrid_driver_1025.py")), "regrid")
d.doc("""#1025 winb, the k_c 143 regrid at D 23.0 (t5's order, hc of 2026-11-27 05:59 UTC): win2's accepted k_c 135 state at D 23.0 (raw I1025-win2/kc135_d23: sol_l1kc135win2d23_D23.0000.npy blob cd134e2c,
l1kc135win2d23.jsonl blob bc295fbc) is regridded on this Windows machine to k_c 143 with
  ell_refine.py l1kc135win2d23 135 l1kc143winbd23 143 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.0992182200 is lambda_0(23.0), unused with --no-gamma; checked below)
with the code of my k_c 127 regrid (same worktree choptuik-i1025k79 at 48c36355, ell_refine.py 631e5801, venv, 4 threads, BelowNormal), only the source tag, the target tag and the k_c numbers changed.
The cap is 43200 s (t5) by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running; nothing is stopped at 6 h.
Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: kc127_syscheck_1025.py (898ebefa), kc135_syscheck_1025.py (b353d466) and kc143_syscheck_1025.py (e15b0ee2, raw 5370db0e3 I1025-mac/checks), d18_hybsign.py, d185_scan_read.py, read_lower.py,
     win2's k_c 135 D 23.0 state and record (inputs/ and the worktree's copies in solver/matter/data/), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399, ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(23.0) = 2.0992182200;
  3. the SOURCE (step 1 of t5's order): the k_c 135 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 127 and k_c 143 checks refuse it (exit 1 each);
  4. the regrid (step 1 of the lane);
  5. ACCEPTED only if kc143_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc135_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc143d23_1025.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc143d23_regrid_driver_1025.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)""")
d.rep("# macm3's accepted k_c 135 D 23.0 state and record (raw I1025-macm3/kc135_d23; copies in inputs/)", "# win2's accepted k_c 135 D 23.0 state and record (raw I1025-win2/kc135_d23; copies in inputs/)")
d.rep("(from macm3's k_c 135 state)", "(from win2's k_c 135 state)")
d.rep("from macm3's accepted k_c 135 D 23.0 state", "from win2's accepted k_c 135 D 23.0 state")
d.rep("macm3's k_c 135 D 23.0 files", "win2's k_c 135 D 23.0 files")
d.rep("= {LAM0}, as macm3's\")", "= {LAM0}, as t5's order\")")
d.rep("{SRC} 119 {TAG} 127 1 23.0", "{SRC} 135 {TAG} 143 1 23.0")
d.rep('SRC, "119", TAG, "127", "1", "23.0"', 'SRC, "135", TAG, "143", "1", "23.0"')
d.rep("sample_driver4_1025.ps1", "sample_driver_kc143_1025.ps1")
d.rx(r"\(macm3's references at D 23\.0:.*?= 1\.0835\)", "(references at D 23.0: k_c 119 to 127 3914 to 4179 = 1.0677 (mine), k_c 127 to 135 4179 to 4441 = 1.0627 (win2's))")
d.rx(r"\"The scan \(d18_secant\.py scan, lambda 0\.03 0\.04 0\.05 0\.06 plus a repeat of 0\.04, 5 evaluations, 2 processes\) starts by itself now\.\"",
     "\"The scan (d18_secant.py scan with the Rust block, --b12=rust --b12_threads=2, lambda 0.050 0.055 0.060 plus a repeat of 0.055, 4 evaluations, 2 processes) starts by itself now.\"")
assert "macm3" not in d.t, [l for l in d.t.splitlines() if "macm3" in l]
wr("kc143d23_regrid_driver_1025.py", d.t)

# ---------------------------------------------------------------------------------------------- scan driver
d = Doc(ren(rd("kc127d23_scan_driver_1025.py")), "scan")
d.doc("""#1025 winb, the k_c 143 scan at D 23.0 with the RUST block 12 (t5's order, hc of 2026-11-27 05:59 UTC; the shares are an argument): d18_secant.py scan (branch wip/ell1-rust-b12 at d4b6b6ce, committed blob 9706e506,
worktree choptuik-i1102) with --b12=rust --b12_threads=2 (ellrs from my #1102 build in i1102_1025/site, on PYTHONPATH, pinned by blob; OPENBLAS_NUM_THREADS=1), on my regridded k_c 143 state
sol_l1kc143winbd23_D23.0000.npy and its record (both in this folder, checked against the blobs the regrid driver wrote into regrid_accepted.txt), at the lambda shares LISTS (semicolon-separated, one share per process,
AT MOST TWO processes (t5); a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, 2 Rust threads per process, BelowNormal, cap 43200 s by the exact pids.
Before the scan the tool's own selftest (exit 0 wanted) and its three mutations half, norobust, nosigncheck (exit 1 wanted each), and ell_b12rs.py's selftest with --mutate=nolam and --mutate=harm (exit 0, 1, 1) are run and
logged (selftest_d18_secant.txt, selftest_ell_b12rs.txt), and read_lower.py's selftest and its two --mutate controls (exit 0, 1, 1). d18_secant.py scan checks the pins and the record system first (exit 3 if not) and appends one
JSON line per lambda (d18_hybsign.py's fields plus dln, robust, sec_parts, b12, role scan) to its own file scan_kc143_D23_p<i>.jsonl. Starts only when regrid_accepted.txt exists (and names the state and record blobs) and no scan
file exists. Memory: no guard, the alert-only watcher is its own process. A keep-awake helper holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) for this driver's duration. Then dh170's read_lower.py (raw
I1025-dh170/lower_root, blob 89309d3c, three-decimal keys) on the folder, and an hc to the coordinator t5 with every line it printed. The refinement (d18_secant.py run) is NOT chained here: I read the reader's lines first
(t5's stop: no robust change or more than one), push the scan files and start it by hand.
usage: kc143d23_scan_driver_1025.py LISTS [--dry [--out=DIR]]     e.g. "0.055,0.050;0.060,0.055"     (--dry: runs the checks, prints the planned commands, starts nothing; --out=DIR (dry only) takes the
state, record and marker from DIR)""")
d.rep('WT = "C:/Users/nathan/Source/choptuik-i1025secant92"', 'WT = "C:/Users/nathan/Source/choptuik-i1102"\nSITE = "' + SITE + '"          # ellrs (my #1102 build, cp314, avx512), on PYTHONPATH')
d.rep('PINS = [(SCANNER, "eb1396ad39d9236ae983064da5702164947e0948"),',
      f'PINS = [(SCANNER, "{B_SCANNER}"), (WTM + "/ell_b12rs.py", "{B_B12RS}"), (SITE + "/ellrs/ellrs.cp314-win_amd64.pyd", "{B_PYD}"), (SITE + "/ellrs/__init__.py", "{B_INIT}"),')
d.rep('["git", "hash-object"] + ([] if fn == SCANNER else ["--no-filters"]) + [fn]', '["git", "hash-object"] + ([] if fn in (SCANNER, WTM + "/ell_b12rs.py") else ["--no-filters"]) + [fn]')
d.rep('"92b9bf533ff371247be642c47e067a9042cabed1"', '"' + HEAD_RS + '"')
d.rep("not 92b9bf53, or a scan file exists", "not d4b6b6ce, or a scan file exists")
d.rep("d18_secant.py (92b9bf53, blob eb1396ad) selftest {mut}", "d18_secant.py (d4b6b6ce, blob 9706e506) selftest {mut}")
d.rep('say("d18_secant.py (92b9bf53, blob eb1396ad) selftest exit 0', 'say("d18_secant.py (d4b6b6ce, blob 9706e506) selftest exit 0')
# the Rust block's selftest and its two controls, after the tool's own
d.rep('st = []\nfor mut in ("", "--mutate=shift", "--mutate=round2"):',
      'senv = dict(os.environ, PYTHONPATH=SITE, OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")\n'
      'exr = []\n'
      'for mut in ("", "--mutate=nolam", "--mutate=harm"):\n'
      '    rr = sh([PY, "-u", WTM + "/ell_b12rs.py", "selftest"] + ([mut] if mut else []), cwd=WTM, env=senv)\n'
      '    exr.append(rr.returncode)\n'
      '    open(OUT + "/selftest_ell_b12rs.txt" + (".dry" if DRY else ""), "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC ell_b12rs.py (blob {B12RS_BLOB[:8]}) selftest {mut}\\n" + rr.stdout + rr.stderr + f"exit {rr.returncode} ({0 if not mut else 1} wanted)\\n")\n'
      'if exr != [0, 1, 1]:\n'
      '    refuse(f"ell_b12rs.py selftest and its controls nolam, harm gave exits {exr}, wanted [0, 1, 1]", f"not started: ell_b12rs.py selftest/controls exits {exr}, wanted [0, 1, 1].")\n'
      'else:\n'
      '    say("ell_b12rs.py selftest exit 0 and its controls --mutate=nolam, --mutate=harm exit 1, 1 as wanted (ellrs from " + SITE + ")")\n'
      'st = []\nfor mut in ("", "--mutate=shift", "--mutate=round2"):')
d.rep('CAP = 43200\n', 'CAP = 43200\nB12RS_BLOB = "' + B_B12RS + '"\n')
d.rep('",".join(f"{v:g}" for v in sh_), SCANF[i], PINARG] for i, sh_', '",".join(f"{v:g}" for v in sh_), SCANF[i], PINARG, "--b12=rust", "--b12_threads=2"] for i, sh_')
d.rep('(cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s)', '(cwd {WTM}, ellrs 2 threads, BelowNormal, cap {CAP} s, PYTHONPATH {SITE})')
d.rep('RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM)', 'RAYON_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", P4_WT_MATTER=WTM, PYTHONPATH=SITE)')
d.rep("d18_secant.py scan {REC} {STATE} {DS} {c[7]} {SCANF[i]} {PINARG}\")", "d18_secant.py scan {REC} {STATE} {DS} {c[7]} {SCANF[i]} {PINARG} --b12=rust --b12_threads=2\")")
assert "macm3" not in d.t
wr("kc143d23_scan_driver_1025.py", d.t)

# ---------------------------------------------------------------------------------------------- secant driver
d = Doc(ren(rd("kc127d23_secant_driver_1025.py")), "secant")
d.doc("""#1025 winb, the secant refinement of the k_c 143 root at D 23.0 with the Rust block 12 (t5's order, hc of 2026-11-27 05:59 UTC, step 3 of the lane): d18_secant.py run (branch wip/ell1-rust-b12 at d4b6b6ce, committed
blob 9706e506, worktree choptuik-i1102; Brent's method on the signed hybrid determinant) with --b12=rust --b12_threads=4 (ellrs from my #1102 build, i1102_1025/site, on PYTHONPATH, pinned by blob; OPENBLAS_NUM_THREADS=1) on my
accepted k_c 143 state sol_l1kc143winbd23_D23.0000.npy and its record l1kc143winbd23.jsonl (both in this folder; the blobs are the ones in regrid_accepted.txt), between LO HI (arguments: the robust bracket the scan's reader
printed), with the scan's two end records (--ends, verbatim lines of scan_kc143_D23_p*.jsonl; t5: "Reuse the scan's ends"):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=5e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB --ends=scan_kc143_D23_ends.jsonl --b12=rust --b12_threads=4     one process, BelowNormal
(--tol=5e-5 is t5's, not 1e-5: #1101's dh370 test measured a root scatter of 1.75e-4 between two solves of one state). Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py (blob 9706e506), ell_b12rs.py, the ellrs files of the site, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree (HEAD d4b6b6ce); the three checks (kc127 898ebefa, kc135 b353d466, kc143 e15b0ee2); the state and
     the record against the blobs of regrid_accepted.txt; the ends file (blob from --ends-blob=) and its two lines verbatim in the scan files;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc143_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 135 and k_c 127 checks refuse them (exit 1 each);
  3b. the ends: scan_kc143_D23_ends.jsonl is two lines, each verbatim a line of the scan files at lambda LO and HI;
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 43200 s (12 h; t5: stop and report on any step over 12 h), one hc to t5 at 21600 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs), 3 pin differs or not the record system. Its own records (one per evaluation
record) are appended to secant/secant.jsonl; the log is secant/secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it, as in my other drivers; nothing kills on memory.
usage: kc143d23_secant_driver_1025.py LO HI --ends-blob=BLOB [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)""")
d.rep('WTS = "C:/Users/nathan/Source/choptuik-i1025secant92"', 'WTS = "C:/Users/nathan/Source/choptuik-i1102"\nSITE = "' + SITE + '"          # ellrs (my #1102 build, cp314, avx512), on PYTHONPATH')
d.rep('if len(args) != 2:\n    print("usage: kc143d23_secant_driver_1025.py LO HI [--dry]"); sys.exit(2)',
      'ENDSBLOB = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--ends-blob=")), "")\nif len(args) != 2 or len(ENDSBLOB) != 40:\n    print("usage: kc143d23_secant_driver_1025.py LO HI --ends-blob=BLOB [--dry]"); sys.exit(2)')
d.rep('# t5\'s order (hc 19:46 UTC): --ends, the two end records of the scan, verbatim (p0 line 1 lambda 0.04, p1 line 1 lambda 0.05)', '# t5\'s order (hc 05:59 UTC): --ends, "Reuse the scan\'s ends": the two end records of the scan, verbatim lines of the scan files')
d.rep('B_ENDS = "62584ab6a5153a1a9267454bb9f570fc474a7d0a"', 'B_ENDS = ENDSBLOB')
d.rep('(WTM + "/d18_secant.py", "eb1396ad39d9236ae983064da5702164947e0948", True),',
      f'(WTM + "/d18_secant.py", "{B_SCANNER}", True), (WTM + "/ell_b12rs.py", "{B_B12RS}", True), (SITE + "/ellrs/ellrs.cp314-win_amd64.pyd", "{B_PYD}", False), (SITE + "/ellrs/__init__.py", "{B_INIT}", False),')
d.rep('"92b9bf533ff371247be642c47e067a9042cabed1"', '"' + HEAD_RS + '"')
d.rep('refuse("the secant worktree is not at 92b9bf53")', 'refuse("the secant worktree is not at d4b6b6ce")')
d.rep("pins ok (worktree 92b9bf53, d18_secant.py eb1396ad, ell_fastm.py 93f963f6,", "pins ok (worktree d4b6b6ce, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, the ellrs site files, ell_fastm.py 93f963f6,")
d.rep('env = dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")',
      'env = dict(os.environ, RAYON_NUM_THREADS="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=SITE)')
d.rep("for k in (127, 119, 111):", "for k in (143, 135, 127):")
d.rep("if st != {127: 0, 119: 0, 111: 0}:", "if st != {143: 0, 135: 0, 127: 0}:")
d.rep("the selftests of the k_c 143, 119 and 111 checks gave exits", "the selftests of the k_c 143, 135 and 127 checks gave exits")
d.rep('"--tol=1e-5", "--maxev=10", f"--pin={B_STATE},{B_STUB}", f"--ends={ENDS}"]', '"--tol=5e-5", "--maxev=10", f"--pin={B_STATE},{B_STUB}", f"--ends={ENDS}", "--b12=rust", "--b12_threads=4"]')
d.rep("--tol=1e-5 --maxev=10 --pin=...\")", "--tol=5e-5 --maxev=10 --pin=... --ends={ENDS} --b12=rust --b12_threads=4\")")
d.rep("(cwd {WTM}, 1 thread, BelowNormal, cap {CAP} s, hc at {NOTIFY} s)", "(cwd {WTM}, ellrs 4 threads, BelowNormal, cap {CAP} s, hc at {NOTIFY} s, PYTHONPATH {SITE})")
assert "macm3" not in d.t
wr("kc143d23_secant_driver_1025.py", d.t)

# ---------------------------------------------------------------------------------------------- the small files
wr("kc143d23_watch_alert_1025.py", ren(rd("kc127d23_watch_alert_1025.py")))
t = ren(rd("sample_driver_kc127_1025.ps1"))
wr("sample_driver_kc143_1025.ps1", t)
wr("keepawake_1025.py", ren(rd("keepawake_1025.py")))
wr("session_check_1025.ps1", ren(rd("session_check_1025.ps1")))
GO = r"""@echo off
rem #1025 winb: the k_c 143 D 23.0 chain (from win2's k_c 135 state) (t5's order of 2026-11-27 05:59 UTC): the regrid driver (source checks, regrid, acceptance); only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan with the Rust block, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc143d23_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc143d23_1025\kc143d23_regrid_driver_1025.py > C:\Users\nathan\Source\kc143d23_1025\kc143d23_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc143d23_1025\I1025-win\kc143_d23\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc143d23_1025\kc143d23_scan_driver_1025.py "0.055,0.050;0.060,0.055" > C:\Users\nathan\Source\kc143d23_1025\kc143d23_scan_driver_stdout.log 2>&1
"""
wr("go_kc143d23_1025.cmd", GO, crlf=True)
# publish script: the k_c 127 one, renamed, with this stage's file list
p = ren(rd("publish_kc127d23_1025.sh"))
i = p.index("for f in make_kc143d23_1025.py")
j = p.index("; do\n", i)
p = p[:i] + ("for f in make_kc143d23_1025.py diff_regrid_driver_vs_kc127.txt diff_scan_driver_vs_kc127.txt diff_secant_driver_vs_kc127.txt kc143d23_regrid_driver_1025.py kc143d23_scan_driver_1025.py kc143d23_secant_driver_1025.py "
             "kc143d23_watch_alert_1025.py sample_driver_kc143_1025.ps1 go_kc143d23_1025.cmd go_secant_kc143d23_1025.cmd keepawake_1025.py session_check_1025.ps1 prep_kc143d23_pins_1025.txt selftest_scan_dry_1025.txt "
             "kc143d23_regrid_driver_stdout.log kc143d23_scan_driver_stdout.log kc143d23_secant_driver_stdout.log publish_kc143d23_1025.sh") + p[j:]
wr("publish_kc143d23_1025.sh", p)
for k, n in (("regrid", "kc143d23_regrid_driver_1025.py"), ("scan", "kc143d23_scan_driver_1025.py"), ("secant", "kc143d23_secant_driver_1025.py")):
    o = subprocess.run(["diff", SRC + n.replace("kc143", "kc127"), DST + n], capture_output=True, text=True).stdout
    open(DST + f"diff_{k}_driver_vs_kc127.txt", "w", encoding="utf-8", newline="\n").write(o)
print("made")
