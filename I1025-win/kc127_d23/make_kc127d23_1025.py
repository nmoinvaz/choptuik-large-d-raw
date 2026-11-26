#!/usr/bin/env python3
"""make_kc127d23_1025.py: writes the k_c 127 D 23.0 lane's scripts from the k_c 103 D 22.875 ones (staging kc103d22875_1025, raw I1025-win/kc103_d22875 at 557ea8ee3) by asserted text replacements.
Part 1 (this file's first section): kc127d23_regrid_driver_1025.py (source macm3's accepted k_c 119 state at D 23.0, raw I1025-macm3/kc119_d23; the k_c 119 check accepts it, the k_c 111 and k_c 127 checks refuse it;
the result is accepted by the k_c 127 check and refused by the k_c 119 check), kc127d23_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1, sample_driver_kc127_1025.ps1, go_kc127d23_1025.cmd,
publish_kc127d23_1025.sh. Part 2 (scan and secant drivers) is in make_kc127d23_part2_1025.py. The diff of the regrid driver against the k_c 103 D 22.875 one is written to diff_regrid_driver_vs_kc103.txt."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc127d23_1025"
OLD = "C:/Users/nathan/Source/kc103d22875_1025"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert t.count(a) == 1, a[:140]
        t = t.replace(a, b)
    return t


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc127_d23/rows", exist_ok=True)
for f in ("kc111_syscheck_1025.py", "kc119_syscheck_1025.py", "kc127_syscheck_1025.py", "d18_hybsign.py", "d185_scan_read.py", "read_lower.py", "sol_l1kc119macm3d23_D23.0000.npy", "l1kc119macm3d23.jsonl"):
    assert os.path.exists(S + "/inputs/" + f), f

# 1. the regrid driver
t = rd(OLD + "/kc103d22875_regrid_driver_1025.py")
i = t.index('"""')
j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the k_c 127 regrid at D 23.0 (t5's order, hc of 2026-11-26 ~10:40 UTC, after the k_c 87 D 22.875 ruling): macm3's accepted k_c 119 state at D 23.0 (raw I1025-macm3/kc119_d23: in/sol_l1kc119macm3d23_D23.0000.npy
blob 2771cf87, in/l1kc119macm3d23.jsonl blob 158e3086) is regridded on this Windows machine to k_c 127 with
  ell_refine.py l1kc119macm3d23 119 l1kc127wind23 127 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.0992182200 is lambda_0(23.0), unused with --no-gamma; checked below)
exactly as my k_c 103 regrids (same worktree choptuik-i1025k79 at 48c36355, venv, 4 threads, BelowNormal; macm3's k_c 119 regrid used the same ell_refine.py 631e5801), only the source tag, the D and the target tag changed.
The cap is 43200 s (t5: "killed at 43200 s") by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running; nothing is stopped at 6 h.
Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: kc111_syscheck_1025.py (85aeb312, macm3's copy), kc119_syscheck_1025.py (fc6e0dd6) and kc127_syscheck_1025.py (898ebefa, raw I1025-mac/checks at d1baa986c: the k_c 111 check with 111 -> 127 and a header line),
     d18_hybsign.py, d185_scan_read.py, read_lower.py, macm3's k_c 119 D 23.0 state and record (inputs/ and the worktree's copies), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399, ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(23.0) = 2.0992182200;
  3. the SOURCE (step 1 of t5's order): the k_c 119 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 111 check and the k_c 127 check refuse it (exit 1 each);
  4. the regrid (step 2);
  5. ACCEPTED (step 3) only if kc127_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc119_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc127d23_1025.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc127d23_regrid_driver_1025.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ('S = "C:/Users/nathan/Source/kc103d22875_1025"\nOUT = S + "/I1025-win/kc103_d22875"', 'S = "C:/Users/nathan/Source/kc127d23_1025"\nOUT = S + "/I1025-win/kc127_d23"'),
    ("# win2's accepted k_c 95 D 22.875 state and record (raw I1025-win2/kc95_d22875, commit 55161c546; copies in inputs/)", "# macm3's accepted k_c 119 D 23.0 state and record (raw I1025-macm3/kc119_d23; copies in inputs/)"),
    ('SRC, TAG = "l1kc95win2d22875", "l1kc103win22875"', 'SRC, TAG = "l1kc119macm3d23", "l1kc127wind23"'),
    ('SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D22.8750.npy", SRCD + f"/{SRC}.jsonl"\nSTATE_N = f"sol_{TAG}_D22.8750.npy"', 'SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D23.0000.npy", SRCD + f"/{SRC}.jsonl"\nSTATE_N = f"sol_{TAG}_D23.0000.npy"'),
    ('LAM0 = "2.0996545550"', 'LAM0 = "2.0992182200"'),
    ('B_STATE, B_REC = "a14f0d50edb575e85387851a61cb2324c1983317", "5381f89d5fe4f81a113295cdde8eb6358de937e8"', 'B_STATE, B_REC = "2771cf87ee8ca5c9ac32d5289397eace6bc1924b", "158e30868886465e4226a45de8975a5693852049"'),
    ('PINS = [(IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6"), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883"),\n        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d"),',
     'PINS = [(IN + "/kc111_syscheck_1025.py", "85aeb31275aa9fd3edb786c74d91e69390a1dc75"), (IN + "/kc119_syscheck_1025.py", "fc6e0dd6fbdf6bcf8fb6a2bf9274e404e3caa7ad"),\n        (IN + "/kc127_syscheck_1025.py", "898ebefa65a99e639110e018808c85506a7f5719"),'),
    ('(WTM + f"/data/sol_{SRC}_D22.8750.npy", B_STATE)', '(WTM + f"/data/sol_{SRC}_D23.0000.npy", B_STATE)'),
    ('SY103, SY95, SY87 = IN + "/kc103_syscheck_1025.py", IN + "/kc95_syscheck_1025.py", IN + "/kc87_syscheck_1025.py"', 'SY127, SY119, SY111 = IN + "/kc127_syscheck_1025.py", IN + "/kc119_syscheck_1025.py", IN + "/kc111_syscheck_1025.py"'),
    ("#1025 k_c 103 regrid at D 22.875 (from win2's k_c 95 state): {m}", "#1025 k_c 127 regrid at D 23.0 (from macm3's k_c 119 state): {m}"),
    ("the k_c 103 regrid at D 22.875 from win2's accepted k_c 95 D 22.875 state", "the k_c 127 regrid at D 23.0 from macm3's accepted k_c 119 D 23.0 state"),
    ("pins ok (the inputs of {IN}, win2's k_c 95 D 22.875 files,", "pins ok (the inputs of {IN}, macm3's k_c 119 D 23.0 files,"),
    ('ell_delta.lam0_at(22.875) = {LAM0}, as win2\'s")', 'ell_delta.lam0_at(23.0) = {LAM0}, as macm3\'s")'),
    ("as win2's", "as macm3's") if False else ("ell_delta.lam0_at(22.875, *", "ell_delta.lam0_at(23.0, *"),
    ("ell_delta.lam0_at(22.875) is {l0.stdout.strip()!r}", "ell_delta.lam0_at(23.0) is {l0.stdout.strip()!r}"),
    ('ell_refine.py {SRC} 95 {TAG} 103 1 22.875 {LAM0}', 'ell_refine.py {SRC} 119 {TAG} 127 1 23.0 {LAM0}'),
    ('S + "/kc103d22875_watch_alert_1025.py"', 'S + "/kc127d23_watch_alert_1025.py"'),
    ('say("kc103d22875_regrid_driver_1025.py done")\n    sys.exit(code)', 'say("kc127d23_regrid_driver_1025.py done")\n    sys.exit(code)'),
    ('cmd = ["-u", "ell_refine.py", SRC, "95", TAG, "103", "1", "22.875", LAM0,', 'cmd = ["-u", "ell_refine.py", SRC, "119", TAG, "127", "1", "23.0", LAM0,'),
    ('json.loads(x).get("D") == 22.875][-1]', 'json.loads(x).get("D") == 23.0][-1]'),
    ("(win2's k_c 87 to 95 at D 22.875: 2862 to 3126 = 1.0923, at D 22.0: 2874 to 3139 = 1.0922; mine k_c 95 to 103 at D 22.0: 3139 to 3402 = 1.0838, at D 21.75: 3152 to 3417 = 1.0841, at D 21.125: 3206 to 3476 = 1.0842, at D 21.0: 3219 to 3489 = 1.0839)",
     "(macm3's references at D 23.0: k_c 95 to 103 1.0838, 103 to 111 1.0779, 111 to 119 3653 to 3914 = 1.071; mine k_c 95 to 103 at D 22.875: 3126 to 3387 = 1.0835)"),
    ('Raw I1025-win/kc103_d22875 after my next push. " + ("The scan 0.04-0.20 by 0.02 plus a repeat of 0.10 (10 evaluations, 4 processes) starts by itself now."',
     'Raw I1025-win/kc127_d23 after my next push. " + ("The scan (d18_secant.py scan, lambda 0.03 0.04 0.05 0.06 plus a repeat of 0.04, 5 evaluations, 2 processes) starts by itself now."'),
    ('say("kc103d22875_regrid_driver_1025.py done")\nsys.exit(0 if verdict == "ACCEPTED" else 1)', 'say("kc127d23_regrid_driver_1025.py done")\nsys.exit(0 if verdict == "ACCEPTED" else 1)'),
])
# role renames of the checks and their outputs (target 103->127, source 95->119, third 87->111)
for a_, b_ in (("syscheck_kc95_on_result", "syscheck_kc119_on_result"), ("kc103_syscheck", "kc127_syscheck"), ("kc95_syscheck", "kc119_syscheck"), ("kc87_syscheck", "kc111_syscheck"),
               ("st103, st95, st87", "st127, st119, st111"), ("st103.", "st127."), ("st95.", "st119."), ("st87.", "st111."), ("SY103", "SY127"), ("SY95", "SY119"), ("SY87", "SY111"),
               ("s103", "s127"), ("k95", "k119"), ("kc103 check", "kc127 check"), ("kc95 check", "kc119 check"), ("kc87 check", "kc111 check"),
               ("kc103_regrid_w.log", "kc127_regrid_w.log"), ("the k_c 95 source record at D 22.875", "the k_c 119 source record at D 23.0"), ("Delta(k_c 103) minus Delta(k_c 95)", "Delta(k_c 127) minus Delta(k_c 119)")):
    t = t.replace(a_, b_)
t = t.replace('"22.875"', '"23.0"').replace("selftest_kc103", "selftest_kc127")
# the lam0 print and the remaining D strings
t = t.replace("22.875", "23.0").replace("kc103d22875_", "kc127d23_")
for bad in ("SY103", "st103", "s103", "\"103\"", "kc95", "kc87", "win2", "22.8", "D22", "a14f0d50", "5381f89d", "2.0996545550", "kc103", "k_c 95 D", "k_c 87 to"):
    k = t.replace("1025", "").replace("2.0992182200", "")
    assert bad not in k, (bad, k[max(0, k.index(bad) - 100):k.index(bad) + 80])
wr(S + "/kc127d23_regrid_driver_1025.py", t)
d = "".join(difflib.unified_diff(rd(OLD + "/kc103d22875_regrid_driver_1025.py").splitlines(True), t.splitlines(True), "kc103d22875_regrid_driver_1025.py", "kc127d23_regrid_driver_1025.py"))
wr(S + "/diff_regrid_driver_vs_kc103.txt", d)


# 2. watcher, keep-awake, session check, sampler, go cmd, publish script
def conv(txt):
    return txt.replace("kc103d22875_1025", "kc127d23_1025").replace("kc103_d22875", "kc127_d23").replace("kc103d22875_", "kc127d23_")


w = conv(rd(OLD + "/kc103d22875_watch_alert_1025.py")).replace("the k_c 103 stages at D 22.875", "the k_c 127 D 23.0 stages").replace("The k_c 103 D 22.875 {label} stage", "The k_c 127 D 23.0 {label} stage")
assert "103" not in w and "22.875" not in w, w[w.index("103") - 60:w.index("103") + 60] if "103" in w else w[w.index("22.875") - 60:w.index("22.875") + 60]
wr(S + "/kc127d23_watch_alert_1025.py", w)
k = conv(rd(OLD + "/keepawake_1025.py"))
assert "103" not in k and "22.875" not in k
wr(S + "/keepawake_1025.py", k)
sc = conv(rd(OLD + "/session_check_1025.ps1"))
assert "103" not in sc and "22.875" not in sc
wr(S + "/session_check_1025.ps1", sc)
sm = rd(OLD + "/sample_driver_secant_1025.ps1")
a = 'elseif ($cl -match "d18_secant\\.py") { "secant" }'
assert sm.count(a) == 1
sm = sm.replace(a, 'elseif ($cl -match "d18_secant\\.py scan") { "scan" } ' + a)
wr(S + "/sample_driver_kc127_1025.ps1", sm)
go = '''@echo off
rem #1025 winb: the k_c 127 D 23.0 chain (from macm3's k_c 119 state) (t5's order of 2026-11-26 ~10:40 UTC): step 1 and 2 and 3, the regrid driver (source checks, regrid, acceptance); step 4a only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\mingw64\\bin;C:\\Program Files\\Git\\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\\Users\\nathan\\Source\\kc127d23_1025
start "" /wait /belownormal /b C:\\Users\\nathan\\Source\\venv-md510\\Scripts\\python.exe -u C:\\Users\\nathan\\Source\\kc127d23_1025\\kc127d23_regrid_driver_1025.py > C:\\Users\\nathan\\Source\\kc127d23_1025\\kc127d23_regrid_driver_stdout.log 2>&1
if not exist C:\\Users\\nathan\\Source\\kc127d23_1025\\I1025-win\\kc127_d23\\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\\Users\\nathan\\Source\\venv-md510\\Scripts\\python.exe -u C:\\Users\\nathan\\Source\\kc127d23_1025\\kc127d23_scan_driver_1025.py "0.04,0.03,0.06;0.05,0.04" > C:\\Users\\nathan\\Source\\kc127d23_1025\\kc127d23_scan_driver_stdout.log 2>&1
'''
wr(S + "/go_kc127d23_1025.cmd", go.replace("\n", "\r\n"))
pub = """#!/bin/bash
# copy the staged k_c 127 D 23.0 folder (files only, and secant/) into the push worktree's I1025-win/kc127_d23, then commit and push linearly with push_1025.sh
# usage: bash publish_kc127d23_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc127d23_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc127_d23
D=$W/I1025-win/kc127_d23
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/secant"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/secant/"* "$D/secant/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc127d23_1025.py make_kc127d23_part2_1025.py diff_regrid_driver_vs_kc103.txt diff_scan_driver_vs_kc103.txt diff_secant_driver_vs_kc87.txt kc127d23_regrid_driver_1025.py kc127d23_scan_driver_1025.py \
         kc127d23_secant_driver_1025.py kc127d23_watch_alert_1025.py sample_driver_kc127_1025.ps1 go_kc127d23_1025.cmd go_secant_kc127d23_1025.cmd keepawake_1025.py session_check_1025.ps1 prep_kc127d23_pins_1025.txt \
         prep_source_checks_by_hand.txt prep_secant_selftests_by_hand.txt selftest_scan_dry_1025.txt kc127d23_regrid_driver_stdout.log kc127d23_scan_driver_stdout.log kc127d23_secant_driver_stdout.log publish_kc127d23_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
"""
wr(S + "/publish_kc127d23_1025.sh", pub)
os.chmod(S + "/publish_kc127d23_1025.sh", 0o755)
print("part 1 written")
