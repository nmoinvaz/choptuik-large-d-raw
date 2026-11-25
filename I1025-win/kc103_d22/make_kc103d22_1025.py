#!/usr/bin/env python3
"""make_kc103d22_1025.py: writes the k_c 103 D 22.0 stage's scripts from the k_c 103 D 21.75 ones (staging kc103d2175_1025, raw I1025-win/kc103_d2175 at df17428bc) by asserted text replacements:
kc103d22_regrid_driver_1025.py, kc103d22_scan_driver_1025.py, kc103d22_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1, sample_driver4_1025.ps1, go_kc103d22_1025.cmd,
publish_kc103d22_1025.sh. Each asserted replacement must occur; the diff of the regrid driver against the D 21.75 one is written to diff_regrid_driver_vs_prev.txt. The source (win2's accepted
k_c 95 D 22.0 state and record, raw I1025-win2/kc95_d22) and the pinned checks are in inputs/ already (copied by hand, blobs checked). The regrid's cap is 43200 s with an hc to t5 at 21600 s if it
is still running (t5's order); the scan's cap stays 21600 s."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc103d22_1025"
OLD = "C:/Users/nathan/Source/kc103d2175_1025"
SHARES = "0.545,0.530;0.550,0.535;0.540,0.555;0.545,0.560"


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
    """names, tags, D, lambda_0 and blobs: applied to every derived file after its own asserted edits"""
    t = t.replace("l1kc103win2175", "l1kc103win22").replace("l1kc95dh610d2175", "l1kc95win2d22")
    t = t.replace("read_lower_kc103_D2175", "read_lower_kc103_D22").replace("scan_kc103_D2175", "scan_kc103_D22")
    t = t.replace("kc103_d2175", "kc103_d22").replace("kc103d2175_", "kc103d22_")
    t = t.replace("D21.7500", "D22.0000").replace("2.1037780803", "2.1028298859")
    t = t.replace("ee18ab90e3dc826d2d45c600b0e6938b20ccd48e", "daae6b2e896d2c302be6ab26e25051c44da98a8e")
    t = t.replace("6bde1c86007d67e7c3c6e36c2d9e64fc743d75a7", "85e667361c8a8892022861886eaee945b0b5bb11")
    t = re.sub(r"(?<![0-9.])21\.75(?![0-9])", "22.0", t)
    for bad in ("dh610's accepted", "dh610's k_c 95 D", "dh610's k_c 87", "as dh610's", "I1025-dh610", "2175", "21.75", "D21.7500", "2.1037780803", "ee18ab90", "6bde1c86", "dc5a6edb", "0.635", "0.645"):
        assert bad not in t, (bad, t[max(0, t.index(bad) - 80):t.index(bad) + 60])
    return t.replace("@@DPREV@@", "21.75")


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc103_d22/rows", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc95win2d22_D22.0000.npy", "l1kc95win2d22.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f

# 1. the regrid driver
t = rd(OLD + "/kc103d2175_regrid_driver_1025.py")
t = rep(t, [
    ("(t5's order, hc of 2026-11-25 ~04:30 UTC, after the k_c 103 D 21.125 ruling 0.884384): dh610's accepted k_c 95 D 21.75 state",
     "(t5's order, hc of 2026-11-25 ~12:35 UTC, after the k_c 95 D 22.125 ruling, outcome B): win2's accepted k_c 95 D 22.0 state"),
    ("(raw I1025-dh610/kc95_d2175, regrid commit dc5a6edb: in/sol_l1kc95dh610d2175_D21.7500.npy blob ee18ab90, in/l1kc95dh610d2175.jsonl blob 6bde1c86)",
     "(raw I1025-win2/kc95_d22, commit 309ff9991: sol_l1kc95win2d22_D22.0000.npy blob daae6b2e, l1kc95win2d22.jsonl blob 85e66736)"),
    ("exactly as my k_c 103 regrids at D 21.0 and 21.125 (same worktree", "exactly as my k_c 103 regrids at D 21.0, 21.125 and @@DPREV@@ (same worktree"),
    ("The cap is 43200 s (12 h; t5's hc of ~04:35 UTC raised it from\nthe 6 h of the earlier regrids because dh610's own k_c 95 regrid at this D took 9339 s on 8 threads), killed by the exact pid,",
     "The cap is 43200 s (12 h; t5's order of ~12:35 UTC: \"cap 43200 s\"; the earlier regrids had 6 h, my D @@DPREV@@ one took 8415 s), killed by the exact pid,"),
    ("dh610's k_c 95 D 21.75 state and record (inputs/ and the worktree's copies)", "win2's k_c 95 D 22.0 state and record (inputs/ and the worktree's copies)"),
    ("# dh610's accepted k_c 95 D 21.75 state and record (raw I1025-dh610/kc95_d2175, commit dc5a6edb; copies in inputs/)",
     "# win2's accepted k_c 95 D 22.0 state and record (raw I1025-win2/kc95_d22, commit 309ff9991; copies in inputs/)"),
    ("#1025 k_c 103 regrid at D 21.75 (from dh610's k_c 95 state): ", "#1025 k_c 103 regrid at D 21.75 (from win2's k_c 95 state): "),
    ("the k_c 103 regrid at D 21.75 from dh610's accepted k_c 95 D 21.75 state", "the k_c 103 regrid at D 21.75 from win2's accepted k_c 95 D 21.75 state"),
    ("pins ok (the inputs of {IN}, dh610's k_c 95 D 21.75 files,", "pins ok (the inputs of {IN}, win2's k_c 95 D 21.75 files,"),
    ("= {LAM0}, as dh610's\")", "= {LAM0}, as win2's\")"),
    ("(dh610's k_c 87 to 95 at D 21.75: 2887 to 3152 = 1.0918; mine k_c 95 to 103 at D 21.125: 3206 to 3476 = 1.0842, at D 21.0: 3219 to 3489 = 1.0839)",
     "(win2's k_c 87 to 95 at D 21.75: 2874 to 3139 = 1.0922; mine k_c 95 to 103 at D @@DPREV@@: 3152 to 3417 = 1.0841, at D 21.125: 3206 to 3476 = 1.0842, at D 21.0: 3219 to 3489 = 1.0839)"),
    ("The scan 0.635-0.655 by 0.005 plus a repeat of 0.645 (6 evaluations, 4 processes)", "The scan 0.530-0.560 by 0.005 plus a repeat of 0.545 (8 evaluations, 4 processes)"),
])
new = glob_rep(t)
wr(S + "/kc103d22_regrid_driver_1025.py", new)
d = "".join(difflib.unified_diff(rd(OLD + "/kc103d2175_regrid_driver_1025.py").splitlines(True), new.splitlines(True), "kc103d2175_regrid_driver_1025.py", "kc103d22_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_prev.txt", d)

# 2. the scan driver (cap 21600 s, unchanged)
t = rd(OLD + "/kc103d2175_scan_driver_1025.py")
t = rep(t, [("(from dh610's k_c 95 D 21.75 state) (t5's order, hc of 2026-11-25 ~04:30 UTC;", "(from win2's k_c 95 D 21.75 state) (t5's order, hc of 2026-11-25 ~12:35 UTC;"),
            ('"0.645,0.635;0.640;0.650,0.655;0.645"', '"' + SHARES + '"'),
            ("the k_c 103 D 21.75 regrid is not accepted", "the k_c 103 D 21.75 regrid is not accepted")])
wr(S + "/kc103d22_scan_driver_1025.py", glob_rep(t))

# 3. watcher, keep-awake, session check, sampler
for a in ("kc103d2175_watch_alert_1025.py", "keepawake_1025.py", "session_check_1025.ps1"):
    wr(S + "/" + a.replace("kc103d2175_", "kc103d22_"), glob_rep(rd(OLD + "/" + a)))
shutil.copyfile(OLD + "/sample_driver4_1025.ps1", S + "/sample_driver4_1025.ps1")

# 4. the go cmd and the publish script
t = rd(OLD + "/go_kc103d2175_1025.cmd")
t = rep(t, [("(from dh610's k_c 95 state) (t5's order of 2026-11-25 ~04:30 UTC)", "(from win2's k_c 95 state) (t5's order of 2026-11-25 ~12:35 UTC)"),
            ('"0.645,0.635;0.640;0.650,0.655;0.645"', '"' + SHARES + '"'), ("(6 evaluations, 4 processes)", "(8 evaluations, 4 processes)")])
wr(S + "/go_kc103d22_1025.cmd", glob_rep(t))
t = rd(OLD + "/publish_kc103d2175_1025.sh")
t = rep(t, [("diff_regrid_driver_vs_crossbuild.txt", "diff_regrid_driver_vs_prev.txt")])
wr(S + "/publish_kc103d22_1025.sh", glob_rep(t))
os.chmod(S + "/publish_kc103d22_1025.sh", 0o755)
shutil.copyfile(OLD + "/kc103_syscheck_1025_vs_kc95.diff", S + "/kc103_syscheck_1025_vs_kc95.diff")
print("written")
