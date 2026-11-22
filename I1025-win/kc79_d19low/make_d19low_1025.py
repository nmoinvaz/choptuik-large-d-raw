#!/usr/bin/env python3
"""#1025 winb, k_c 79 lower-root scan at D 19 (t5's order, hc of 2026-11-22 ~17:35 UTC; start ordered by the hc of ~21:03 UTC after the D 19.25 regrid was stopped): derives the scan driver, watcher, launcher and publish script from the
D 19 ones (C:/Users/nathan/Source/kc79d19_1025, raw I1025-win/kc79_d19 at 010273bc) by exact replacements, each asserted, and writes a diff against the D 19 file for each (diff_*_vs_d19.txt).
Changed: the folder and file names (kc79d19 -> kc79d19low), the scan file (scan_kc79_D19low_p0.jsonl: read_lower.py globs scan_*_p*.jsonl), the source (the accepted D 19 state, record and
regrid_accepted.txt stay in kc79_d19 and are pinned by blob), a window that may repeat a value (twice at most), the reader (dh170's read_lower.py, blob 89309d3c, run with its selftest and the two
controls first, instead of d18f_read.py), the hc text, a keep-awake helper (keepawake_1025.py) started with the other helpers, the launcher without a new console (start /b, for the headless
conhost launch). Nothing else."""
import difflib, os, re

A = "C:/Users/nathan/Source/kc79d19_1025"
B = "C:/Users/nathan/Source/kc79d19low_1025"
os.makedirs(B + "/I1025-win/kc79_d19low/rows", exist_ok=True)


def sub(s, old, new, n=1, what=""):
    assert s.count(old) == n, f"{what or old[:60]!r}: found {s.count(old)}, wanted {n}"
    return s.replace(old, new)


def common(s):
    s = s.replace("kc79d19", "kc79d19low").replace("kc79_d19", "kc79_d19low")
    s = s.replace("scan_kc79_D19", "scan_kc79_D19low").replace("read_kc79_D19", "read_lower_kc79_D19low")
    s = re.sub(r"diff_(\w+)_vs_d185\.txt", r"diff_\1_vs_d19.txt", s)
    return s


made = {}
ORDER = "t5's order, hc of 2026-11-22 ~17:35 UTC"

# ---- the scan driver
s = open(A + "/kc79d19_scan_driver_1025.py").read()
i = s.index('"""', s.index('"""') + 3) + 3                 # end of the docstring
doc = f'''#!/usr/bin/env python3
"""#1025 winb, the k_c 79 LOWER-root hybrid scan at D 19 ({ORDER}; the window is an argument, so the driver needs no edit):
xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) on the accepted D 19 k_c 79 state sol_l1kc79W19m1025_D19.0000.npy (raw I1025-win/kc79_d19, pinned by blob; the same state
as the first D 19 scan) and its record, at the lambda list WINDOW (comma-separated, in the given order; a value may appear twice: the repeat), the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64
sign, ONE process, 4 threads, BelowNormal, cap 28800 s (8 h) by the exact pid. d18_hybsign.py checks the record system first (exit 3 if the state does not come back). Starts only when the D 19 regrid_accepted.txt
exists and the scan file does not. Memory: no guard, the alert-only watcher is its own process. Then dh170's read_lower.py (raw I1025-dh170/lower_root, blob 89309d3c, three-decimal keys; its selftest
and the two --mutate controls must give exit 0, 1, 1 before the scan starts) on the scan file, and an hc to the coordinator t5 with every line it printed.
usage: kc79d19low_scan_driver_1025.py LAMBDA_LIST [--dry]     e.g. 0.92,0.96,1.00,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.12     (--dry: runs the checks, prints the planned command, starts nothing)"""'''
s = doc + common(s[i:])                                     # the new docstring names the D 19 files and is not renamed
assert s.count("scan_kc79_D19low_1025.jsonl") == 2
s = s.replace("scan_kc79_D19low_1025.jsonl", "scan_kc79_D19low_p0.jsonl")
s = sub(s, 'RAWM = S + "/raw/I1025-mac/d18"', 'SRC = "C:/Users/nathan/Source/kc79d19_1025/I1025-win/kc79_d19"          # the accepted D 19 state, record and marker (raw I1025-win/kc79_d19)\nRAWM = S + "/raw/I1025-mac/d18"', 1, "SRC")
s = sub(s, 'SCANNER, READER = RAWM + "/d18_hybsign.py", RAWM + "/d18f_read.py"', 'SCANNER, READER = RAWM + "/d18_hybsign.py", OUT + "/read_lower.py"', 1, "scanner/reader")
s = sub(s, 'STATE, REC = OUT + f"/sol_{TAG}_D19.0000.npy", OUT + f"/{TAG}.jsonl"', 'STATE, REC = SRC + f"/sol_{TAG}_D19.0000.npy", SRC + f"/{TAG}.jsonl"', 1, "state/rec")
assert 'SCAN, LOG = OUT + "/scan_kc79_D19low_p0.jsonl"' in s
s = sub(s, "if len(LV) < 2 or len(set(LV)) != len(LV) or not all(0.0 < v < 10.0 for v in LV):\n    print(\"REFUSE: the window needs at least two distinct values in (0, 10):\", LAMS); sys.exit(2)",
        "if len(set(LV)) < 2 or max(LV.count(v) for v in LV) > 2 or not all(0.0 < v < 10.0 for v in LV):\n    print(\"REFUSE: the window needs at least two distinct values in (0, 10), none more than twice:\", LAMS); sys.exit(2)", 1, "window rule")
# pins: scanner, d185_scan_read (imported by the reader), read_lower, the D 19 state, record and marker
i, j = s.index("PINS = ["), s.index("\n\n\ndef say")
pins = '''PINS = [(SCANNER, "e089207a61fbd98614716abd309571cbc4888db2"), (READER, "89309d3c8e4f758bb5f936f7d24796b594e4cbdb"), (RAWM + "/d185_scan_read.py", "7c9d400fd0966a35ac306b5495febb4ec4efe7da"),
        (STATE, "3a3b1999e1754c9c2e138ebf4d80f33a366abf3b"), (REC, "9e197e492e1d77f0305cf767141dca2c9cc96ce7"), (SRC + "/regrid_accepted.txt", "06aff278c98e1850d9fd1b2a47d7b962f79bfa26")]'''
s = s[:i] + pins + s[j:]
s = sub(s, 'if not os.path.exists(OUT + "/regrid_accepted.txt"):\n    refuse("regrid_accepted.txt does not exist", "not started: the regrid is not accepted.")',
        'if not os.path.exists(SRC + "/regrid_accepted.txt"):\n    refuse("the D 19 regrid_accepted.txt does not exist", "not started: the D 19 regrid is not accepted.")', 1, "accepted")
# the reader's selftest and its two controls before the scan
s = sub(s, "if DRY:\n    say(f\"DRY: would start", '''renv0 = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
st = []
for mut in ("", "--mutate=shift", "--mutate=round2"):
    r0 = sh([PY, "-I", READER, "selftest"] + ([mut] if mut else []), cwd=OUT, env=renv0)
    st.append(r0.returncode)
    open(OUT + "/selftest_read_lower_1025.txt" + (".dry" if DRY else ""), "a").write(f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC read_lower.py selftest {mut}\\n" + r0.stdout + f"selftest {mut} exit {r0.returncode} ({0 if not mut else 1} wanted)\\n")
if st != [0, 1, 1]:
    refuse(f"read_lower.py selftest and its two controls gave exits {st}, wanted [0, 1, 1]", f"not started: read_lower.py selftest/controls exits {st}, wanted [0, 1, 1].")
else:
    say("read_lower.py selftest exit 0 and its two --mutate controls exit 1, 1 as wanted")
if DRY:
    say(f"DRY: would start''', 1, "selftest block")
# the reader call and the hc
i = s.index("renv = dict(os.environ, PYTHONPATH=WTM")
tail = '''renv = dict(os.environ, D18_DIR=RAWM, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
r = sh([PY, "-I", READER, OUT, LO, HI], cwd=OUT, env=renv)
txt = "\\n".join(l for l in (r.stdout + "\\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return ")).strip()
open(OUT + "/read_lower_kc79_D19low.log", "w").write(txt + f"\\nread_lower exit {r.returncode}\\n")
for ln in txt.splitlines():
    say(ln)
hc(f"the scan ended (exit 0, {time.time() - t0:.0f} s, window {LAMS}). read_lower.py {LO} {HI} (exit {r.returncode}), lines as printed: " + " | ".join(l.strip() for l in txt.splitlines())
   + ". Raw I1025-win/kc79_d19low after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc79d19low_scan_driver_1025.py done")
'''
s = s[:i] + tail
s = sub(s, "#1025 k_c 79 scan: {msg}", "#1025 k_c 79 D 19 lower-root scan: {msg}", 1, "hc prefix")
s = sub(s, 'say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")',
        '''say(f"alert-only memory watcher started as its own process, pid {wat.pid} (kills nothing); sampler pid {samp.pid}")
kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "scan", str(CAP + 600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000 | 0x08000000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")''', 1, "keepawake start")
made["kc79d19low_scan_driver_1025.py"] = s

# ---- the watcher
s = common(open(A + "/kc79d19_watch_alert_1025.py").read())
s = sub(s, "The k_c 79 D 19 {label} stage", "The k_c 79 D 19 lower-root {label} stage", 1, "alert text")
made["kc79d19low_watch_alert_1025.py"] = s

# ---- launcher
s = common(open(A + "/start_kc79d19_scan_1025.cmd").read())
s = sub(s, "the k_c 79 check at D 19, the scan driver", "the k_c 79 lower-root scan at D 19, the scan driver", 1, "cmd rem")
s = sub(s, "only when the coordinator has given the window.", "only when the coordinator has ordered it (the window is in the hc of 2026-11-22 ~17:35 UTC).", 1, "cmd rem 2")
s = sub(s, 'start "kc79d19lowscan" /belownormal /wait /min ', 'start "" /wait /belownormal /b ', 1, "cmd start")
s = sub(s, "rem usage: start_kc79d19low_scan_1025.cmd", "rem started as: conhost.exe --headless cmd.exe /c <this file> \"<window>\" (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff); the driver runs in this console (start /b)\nrem usage: start_kc79d19low_scan_1025.cmd", 1, "cmd rem 3")
s = sub(s, '"1.55,1.56,1.57,1.58"', '"0.92,0.96,1.00,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.12"', 1, "cmd example")
made["start_kc79d19low_scan_1025.cmd"] = s

# ---- publish script
s = common(open(A + "/publish_kc79d19_1025.sh").read())
s = sub(s, "copy the staged k_c 79 D 19 folder", "copy the staged k_c 79 D 19 low-scan folder", 1, "pub head")
i, j = s.index("for f in make_d19_1025.py"), s.index("  [ -f \"$S/$f\" ] && cp")
files = ("for f in make_d19low_1025.py diff_scan_driver_vs_d19.txt diff_watcher_vs_d19.txt prep_kc79d19low_pins_1025.txt kc79d19low_scan_driver_1025.py kc79d19low_watch_alert_1025.py sample_driver4_1025.ps1 \\\n"
         "         start_kc79d19low_scan_1025.cmd go_kc79d19low_scan_1025.cmd kc79d19low_scan_first_try_stdout.log keepawake_1025.py session_check_1025.ps1 selftest_scan_dry_1025.txt kc79d19low_scan_driver_stdout.log publish_kc79d19low_1025.sh; do\n")
s = s[:i] + files + s[j:]
made["publish_kc79d19low_1025.sh"] = s

for name, text in made.items():
    open(f"{B}/{name}", "w", newline="\n").write(text)
for key, (name, srcname) in {"scan_driver": ("kc79d19low_scan_driver_1025.py", "kc79d19_scan_driver_1025.py"), "watcher": ("kc79d19low_watch_alert_1025.py", "kc79d19_watch_alert_1025.py")}.items():
    d = "".join(difflib.unified_diff(open(f"{A}/{srcname}").read().splitlines(1), open(f"{B}/{name}").read().splitlines(1), srcname, name, n=0))
    open(f"{B}/diff_{key}_vs_d19.txt", "w", newline="\n").write(d)
print("derived:", ", ".join(made))
