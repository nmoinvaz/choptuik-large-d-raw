#!/usr/bin/env python3
"""#1025 winb, k_c 79 gap scan at D 19 (t5's order, hc of 2026-11-23 ~03:05 UTC, after the lower-root scan of kc79_d19low): derives the scan driver, watcher, launcher, keep-awake helper, session check and
publish script from the d19low ones (C:/Users/nathan/Source/kc79d19low_1025, raw I1025-win/kc79_d19low at 40f1a01a) by exact replacements, each asserted, and writes a diff against the d19low file for each
(diff_*_vs_d19low.txt). Changed: the folder and file names (d19low -> d19gap, D19low -> D19gap), the order text, the docstring and usage example, the hc prefix, the window (go_kc79d19gap_scan_1025.cmd).
Same state, pins, scanner (d18_hybsign.py e089207a) and reader (read_lower.py 89309d3c, with its selftest and the two controls first), same launcher, sampler, alert-only watcher and keep-awake helper. Nothing else."""
import difflib, os

A = "C:/Users/nathan/Source/kc79d19low_1025"
B = "C:/Users/nathan/Source/kc79d19gap_1025"
os.makedirs(B + "/I1025-win/kc79_d19gap/rows", exist_ok=True)
WIN = "1.345,1.37,1.395,1.42,1.445,1.395"
OLDWIN = "0.92,0.96,1.00,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.12"


def sub(s, old, new, n=1, what=""):
    assert s.count(old) == n, f"{what or old[:60]!r}: found {s.count(old)}, wanted {n}"
    return s.replace(old, new)


def common(s):
    return s.replace("d19low", "d19gap").replace("D19low", "D19gap")


made = {}
# ---- the scan driver
s = open(A + "/kc79d19low_scan_driver_1025.py").read()
s = sub(s, "the k_c 79 LOWER-root hybrid scan at D 19 (t5's order, hc of 2026-11-22 ~17:35 UTC;", "the k_c 79 GAP hybrid scan at D 19, the gap (1.32, 1.475) between the two earlier D 19 scans (t5's order, hc of 2026-11-23 ~03:05 UTC;", 1, "doc 1")
s = sub(s, "as the first D 19 scan) and its record", "as the first D 19 scan and the lower-root scan) and its record", 1, "doc 2")
s = sub(s, "e.g. " + OLDWIN, "e.g. " + WIN, 1, "usage")
s = sub(s, "#1025 k_c 79 D 19 lower-root scan: {msg}", "#1025 k_c 79 D 19 gap scan (1.32-1.475): {msg}", 1, "hc prefix")
s = common(s)
made["kc79d19gap_scan_driver_1025.py"] = s

# ---- the watcher
s = open(A + "/kc79d19low_watch_alert_1025.py").read()
s = sub(s, "The k_c 79 D 19 lower-root {label} stage", "The k_c 79 D 19 gap {label} stage", 1, "alert text")
made["kc79d19gap_watch_alert_1025.py"] = common(s)

# ---- launcher and go file
s = open(A + "/start_kc79d19low_scan_1025.cmd").read()
s = sub(s, "the k_c 79 lower-root scan at D 19, the scan driver", "the k_c 79 gap scan (1.32, 1.475) at D 19, the scan driver", 1, "cmd rem")
s = sub(s, "(the window is in the hc of 2026-11-22 ~17:35 UTC)", "(the window is in the hc of 2026-11-23 ~03:05 UTC)", 1, "cmd rem 2")
s = sub(s, OLDWIN, WIN, 1, "cmd example")
made["start_kc79d19gap_scan_1025.cmd"] = common(s)
s = open(A + "/go_kc79d19low_scan_1025.cmd").read()
s = sub(s, "starts the k_c 79 D 19 lower-root scan with the ordered window", "starts the k_c 79 D 19 gap scan with the ordered window", 1, "go rem")
s = sub(s, OLDWIN, WIN, 1, "go window")
made["go_kc79d19gap_scan_1025.cmd"] = common(s)

# ---- keep-awake helper, session check (folder paths)
made["keepawake_1025.py"] = common(open(A + "/keepawake_1025.py").read())
made["session_check_1025.ps1"] = common(open(A + "/session_check_1025.ps1").read())

# ---- publish script
s = open(A + "/publish_kc79d19low_1025.sh").read()
s = sub(s, "copy the staged k_c 79 D 19 low-scan folder", "copy the staged k_c 79 D 19 gap-scan folder", 1, "pub head")
s = sub(s, "diff_scan_driver_vs_d19.txt diff_watcher_vs_d19.txt", "diff_scan_driver_vs_d19low.txt diff_watcher_vs_d19low.txt", 1, "pub diffs")
s = sub(s, " kc79d19low_scan_first_try_stdout.log", "", 1, "pub first try")
made["publish_kc79d19gap_1025.sh"] = common(s)

for name, text in made.items():
    open(f"{B}/{name}", "w", newline="\n").write(text)
for key, (name, srcname) in {"scan_driver": ("kc79d19gap_scan_driver_1025.py", "kc79d19low_scan_driver_1025.py"), "watcher": ("kc79d19gap_watch_alert_1025.py", "kc79d19low_watch_alert_1025.py")}.items():
    d = "".join(difflib.unified_diff(open(f"{A}/{srcname}").read().splitlines(1), open(f"{B}/{name}").read().splitlines(1), srcname, name, n=0))
    open(f"{B}/diff_{key}_vs_d19low.txt", "w", newline="\n").write(d)
print("derived:", ", ".join(made))
