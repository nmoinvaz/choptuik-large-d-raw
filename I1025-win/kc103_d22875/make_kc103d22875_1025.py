#!/usr/bin/env python3
"""make_kc103d22875_1025.py: writes the k_c 103 D 22.875 stage's scripts from the k_c 103 D 22.0 ones (staging kc103d22_1025, raw I1025-win/kc103_d22 at 78aa1bc90) by asserted text replacements:
kc103d22875_regrid_driver_1025.py, kc103d22875_scan_driver_1025.py, kc103d22875_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1, sample_driver4_1025.ps1,
go_kc103d22875_1025.cmd, publish_kc103d22875_1025.sh. Each asserted replacement must occur; the diff of the regrid driver against the D 22.0 one is written to diff_regrid_driver_vs_prev.txt.
The source (win2's accepted k_c 95 D 22.875 state and record, raw I1025-win2/kc95_d22875, commit 55161c546) and the pinned checks are in inputs/ already (copied by hand, blobs checked).
The regrid's cap is 43200 s with an hc to t5 at 21600 s if it is still running (t5's order); the scan's cap stays 21600 s."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc103d22875_1025"
OLD = "C:/Users/nathan/Source/kc103d22_1025"
OLDSHARES = "0.545,0.530;0.550,0.535;0.540,0.555;0.545,0.560"
SHARES = "0.10,0.08,0.04;0.12,0.16,0.20;0.14,0.06;0.10,0.18"


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
    """names, tags, D, lambda_0, blobs, shares: applied to every derived file after its own asserted edits"""
    t = t.replace(OLDSHARES, SHARES)
    t = t.replace("12:35 UTC", "18:55 UTC")
    t = t.replace("l1kc95win2d22", "l1kc95win2d22875").replace("l1kc103win22", "l1kc103win22875")
    t = t.replace("read_lower_kc103_D22", "read_lower_kc103_D22875").replace("scan_kc103_D22", "scan_kc103_D22875")
    t = re.sub(r"kc103_d22(?!875)", "kc103_d22875", t)
    t = re.sub(r"kc103d22_(?!875)", "kc103d22875_", t)
    t = t.replace("D22.0000", "D22.8750").replace("2.1028298859", "2.0996545550")
    t = t.replace("daae6b2e896d2c302be6ab26e25051c44da98a8e", "a14f0d50edb575e85387851a61cb2324c1983317")
    t = t.replace("85e667361c8a8892022861886eaee945b0b5bb11", "5381f89d5fe4f81a113295cdde8eb6358de937e8")
    t = t.replace("daae6b2e", "a14f0d50").replace("85e66736", "5381f89d")
    t = t.replace("commit 309ff9991", "commit 55161c546")
    t = re.sub(r"I1025-win2/kc95_d22(?![0-9])", "I1025-win2/kc95_d22875", t)
    t = re.sub(r"(?<![0-9.])22\.0(?![0-9])", "22.875", t)
    for bad in ("22.0", "D22.0000", "daae6b2e", "85e66736", "309ff9991", "2.1028298859", "12:35", "0.545", "0.530", "0.560", "0.535", "0.555", "0.550", "0.540", "kc103_d22,", "kc103_d22/", "kc103_d22 ",
                "kc103d22_", "win22 ", "2874 to 3139 = 1.0922; mine k_c 95 to 103 at D 21.75"):
        assert bad not in t, (bad, t[max(0, t.index(bad) - 80):t.index(bad) + 60])
    return t.replace("@@DPREV@@", "22.0")


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc103_d22875/rows", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc95win2d22875_D22.8750.npy", "l1kc95win2d22875.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f

# 1. the regrid driver
t = rd(OLD + "/kc103d22_regrid_driver_1025.py")
t = rep(t, [
    ("after the k_c 95 D 22.125 ruling, outcome B", "after the k_c 103 D @@DPREV@@ ruling, 0.547345"),
    ("exactly as my k_c 103 regrids at D 21.0, 21.125 and 21.75 (same worktree", "exactly as my k_c 103 regrids at D 21.0, 21.125, 21.75 and @@DPREV@@ (same worktree"),
    ("the earlier regrids had 6 h, my D 21.75 one took 8415 s)", "the earlier regrids had 6 h, my D @@DPREV@@ one took 10230 s)"),
    ("(win2's k_c 87 to 95 at D 22.0: 2874 to 3139 = 1.0922; mine k_c 95 to 103 at D 21.75: 3152 to 3417 = 1.0841,",
     "(win2's k_c 87 to 95 at D 22.875: 2862 to 3126 = 1.0923, at D @@DPREV@@: 2874 to 3139 = 1.0922; mine k_c 95 to 103 at D @@DPREV@@: 3139 to 3402 = 1.0838, at D 21.75: 3152 to 3417 = 1.0841,"),
    ("The scan 0.530-0.560 by 0.005 plus a repeat of 0.545 (8 evaluations, 4 processes) starts by itself now.", "The scan 0.04-0.20 by 0.02 plus a repeat of 0.10 (10 evaluations, 4 processes) starts by itself now."),
])
new = glob_rep(t)
wr(S + "/kc103d22875_regrid_driver_1025.py", new)
d = "".join(difflib.unified_diff(rd(OLD + "/kc103d22_regrid_driver_1025.py").splitlines(True), new.splitlines(True), "kc103d22_regrid_driver_1025.py", "kc103d22875_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_prev.txt", d)

# 2. the scan driver (cap 21600 s, unchanged)
t = rd(OLD + "/kc103d22_scan_driver_1025.py")
t = rep(t, [("(t5's order, hc of 2026-11-25 ~12:35 UTC; the shares are an argument)", "(t5's order, hc of 2026-11-25 ~12:35 UTC; the shares are an argument)")])
wr(S + "/kc103d22875_scan_driver_1025.py", glob_rep(t))

# 3. watcher, keep-awake, session check, sampler
for a in ("kc103d22_watch_alert_1025.py", "keepawake_1025.py", "session_check_1025.ps1"):
    wr(S + "/" + a.replace("kc103d22_", "kc103d22875_"), glob_rep(rd(OLD + "/" + a)))
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc103d22_1025.cmd")
t = rep(t, [("(8 evaluations, 4 processes)", "(10 evaluations, 4 processes)")])
wr(S + "/go_kc103d22875_1025.cmd", glob_rep(t))
t = rd(OLD + "/publish_kc103d22_1025.sh")
wr(S + "/publish_kc103d22875_1025.sh", glob_rep(t))
os.chmod(S + "/publish_kc103d22875_1025.sh", 0o755)
shutil.copyfile(OLD + "/kc103_syscheck_1025_vs_kc95.diff", S + "/kc103_syscheck_1025_vs_kc95.diff")
print("written")
