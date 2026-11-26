#!/usr/bin/env python3
"""make_kc95d22875s_1025.py: writes the k_c 95 D 22.875 secant lane's scripts from the k_c 103 D 22.875 secant ones (staging kc103d22875_1025, raw I1025-win/kc103_d22875/secant at a83c9a635) by asserted
text replacements: kc95d22875s_secant_driver_1025.py (the state, record, bracket and acceptance check changed: the state is win2's accepted k_c 95 D 22.875 state, accepted by kc95_syscheck_1025.py with its
--mutate=F and --mutate=steps exit 1, and refused by the k_c 87 and k_c 103 checks, in place of the k_c 103 regrid marker and the scan-record check), kc95d22875s_watch_alert_1025.py, keepawake_1025.py,
session_check_1025.ps1, sample_driver_secant_1025.ps1, go_kc95d22875s_1025.cmd, publish_kc95d22875s_1025.sh. The diff of the driver against the k_c 103 one is written to diff_secant_driver_vs_kc103.txt."""
import difflib, os, re, shutil

S = "C:/Users/nathan/Source/kc95d22875s_1025"
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
os.makedirs(S + "/I1025-win/kc95_d22875_secant/rows", exist_ok=True)
os.makedirs(S + "/I1025-win/kc95_d22875_secant/in", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py"):
    assert os.path.exists(S + "/inputs/" + f), f
for f in ("sol_l1kc95win2d22875_D22.8750.npy", "l1kc95win2d22875.jsonl"):
    assert os.path.exists(S + "/I1025-win/kc95_d22875_secant/in/" + f), f

# 1. the driver
t = rd(OLD + "/kc103d22875_secant_driver_1025.py")
i = t.index('"""')
j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the secant refinement of the k_c 95 root at D 22.875 (t5's order, hc of 2026-11-26 ~06:35 UTC, after the k_c 103 D 22.875 ruling): xfkappa's d18_secant.py (branch wip/ell1-speed at 6010e37b,
committed blob a3d90cd5; Brent's method on the hybrid sign) on win2's accepted k_c 95 state sol_l1kc95win2d22875_D22.8750.npy (raw I1025-win2/kc95_d22875, blob a14f0d50) and its record l1kc95win2d22875.jsonl
(blob 5381f89d; copies in in/), between LO HI (arguments: win2's robust bracket (0.10, 0.12)):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 22.875 LO HI secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB     one process, BelowNormal, 1 thread (OMP/OPENBLAS/MKL 1 too)
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree choptuik-i1025secant (HEAD 6010e37b); the three checks (kc87 6df5d960, kc95 d487e628, kc103 3ab58d16); the state and the record;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc95_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 87 and k_c 103 checks refuse them (exit 1 each);
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 28800 s (8 h; t5: stop and report on any step over 8 h), one hc to t5 at 14400 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs: t5's "signs at 0.10 and 0.12 that do not differ"), 3 pin differs or
not the record system. Its own records (one per evaluation, then a root record) are appended to secant.jsonl; the log is secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run
beside it, as in my other drivers; nothing kills on memory.
usage: kc95d22875s_secant_driver_1025.py LO HI [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ("import datetime, glob, json, os, subprocess, sys, time\n", "import datetime, json, os, subprocess, sys, time\n"),
    ('OUT = S + "/I1025-win/kc103_d22875"\nSEC = OUT + "/secant"\n', 'OUT = S + "/I1025-win/kc95_d22875_secant"\nSEC = OUT\nIN = S + "/inputs"\n'),
    ('SCANDIR = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--scandir=")), None)\nif SCANDIR and not DRY:\n    print("REFUSE: --scandir=DIR is for --dry only"); sys.exit(2)\n', ""),
    ('"usage: kc103d22875_secant_driver_1025.py LO HI [--dry [--scandir=DIR]]"', '"usage: kc95d22875s_secant_driver_1025.py LO HI [--dry]"'),
    ('STATE, STUB = OUT + "/sol_l1kc103win22875_D22.8750.npy", OUT + "/l1kc103win22875.jsonl"\n', 'STATE, STUB = OUT + "/in/sol_l1kc95win2d22875_D22.8750.npy", OUT + "/in/l1kc95win2d22875.jsonl"\n'),
    ('B_STATE, B_STUB = "280515313e580cccbf14a6e0828e4eaa9b22086d", "f623d3e67b94a5ac4e38e2c55d05d3bf247e4c71"\n',
     'B_STATE, B_STUB = "a14f0d50edb575e85387851a61cb2324c1983317", "5381f89d5fe4f81a113295cdde8eb6358de937e8"\n'),
    ('        (STATE, B_STATE, False), (STUB, B_STUB, False)]\nCAP, NOTIFY = 54000, 21600\n',
     '        (IN + "/kc87_syscheck_1025.py", "6df5d9600edebeae8cc4e602025e42e79925b7d6", False), (IN + "/kc95_syscheck_1025.py", "d487e628f61d1accae8e09f7d1ad438c1d787883", False),\n'
     '        (IN + "/kc103_syscheck_1025.py", "3ab58d16106435af602445940f55900b60c5a61d", False), (STATE, B_STATE, False), (STUB, B_STUB, False)]\nCAP, NOTIFY = 28800, 14400\n'),
    ('hc(f"the refinement (pid {p.pid}) is still running after {NOTIFY} s (6 h), {n} evaluation record(s) so far; its cap is {CAP} s (15 h); nothing is stopped at 6 h.")',
     'hc(f"the refinement (pid {p.pid}) is still running after {NOTIFY} s (4 h), {n} evaluation record(s) so far; it is killed by the exact pid at {CAP} s (8 h, your stop).")'),
    ('#1025 k_c 103 D {D} secant refinement', '#1025 k_c 95 D {D} secant refinement'),
    ('the secant refinement of the k_c 103 root at D {D}, bracket', 'the secant refinement of the k_c 95 root at D {D}, bracket'),
    ('S + "/kc103d22875_watch_alert_1025.py"', 'S + "/kc95d22875s_watch_alert_1025.py"'),
])
# the acceptance block replaces the regrid-marker check and the scan-record bracket check
a = t.index("if not DRY or SCANDIR is None:")
b = t.index("env = dict(os.environ")
t = t[:a] + 'say(f"pins ok (worktree 6010e37b, d18_secant.py a3d90cd5, ell_fastm.py 93f963f6, the solver files equal to my regrids\', the three checks, state {B_STATE[:8]}, record {B_STUB[:8]})")\n' + t[b:]
a = t.index("rows = []\nfor f in sorted(glob.glob")
b = t.index("cmd = [PY, \"-u\", WTM + \"/d18_secant.py\", \"run\"")
accept = '''st = {}
for k in (95, 87, 103):
    r = sh([PY, "-u", IN + f"/kc{k}_syscheck_1025.py", "--selftest"], cwd=WTM, env=env)
    st[k] = r.returncode
    open(SEC + "/selftest_kc%d_syscheck.txt" % k + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\\n")
if st != {95: 0, 87: 0, 103: 0}:
    refuse(f"the selftests of the k_c 95, 87 and 103 checks gave exits {st}, wanted 0 each")
else:
    say("selftests: kc95_syscheck exit 0, kc87_syscheck exit 0, kc103_syscheck exit 0 (0 wanted each)")
t0 = time.time()
src = {}
for name, cmdl in (("source_kc95_syscheck.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM]), ("source_kc95_syscheck_mutate_F.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=F"]),
                   ("source_kc95_syscheck_mutate_steps.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=steps"]), ("source_kc87_syscheck.txt", [PY, IN + "/kc87_syscheck_1025.py", STUB, STATE, D, WTM]),
                   ("source_kc103_syscheck.txt", [PY, IN + "/kc103_syscheck_1025.py", STUB, STATE, D, WTM])):
    r = sh(cmdl, env=env)
    open(SEC + "/" + name + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\\n")
    src[name] = r.returncode
want = {"source_kc95_syscheck.txt": 0, "source_kc95_syscheck_mutate_F.txt": 1, "source_kc95_syscheck_mutate_steps.txt": 1, "source_kc87_syscheck.txt": 1, "source_kc103_syscheck.txt": 1}
say(f"the state: kc95 check exit {src['source_kc95_syscheck.txt']} (0 wanted: it accepts), --mutate=F {src['source_kc95_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc95_syscheck_mutate_steps.txt']} (1 wanted each), "
    f"kc87 check {src['source_kc87_syscheck.txt']} and kc103 check {src['source_kc103_syscheck.txt']} (1 wanted each: they refuse it); {time.time() - t0:.0f} s")
if src != want:
    refuse(f"the state is not accepted as wanted ({src}, wanted {want})")
'''
t = t[:a] + accept + t[b:]
t = t.replace('"--pin={B_STATE},{B_STUB}"', '"--pin={B_STATE},{B_STUB}"')
t = t.replace("kc103d22875_secant_driver_1025.py", "kc95d22875s_secant_driver_1025.py")
for bad in ("kc103win", "k_c 103", "scandir", "SCANDIR", "regrid_accepted", "28051531", "f623d3e6", "54000", "21600", "kc103d22875"):
    assert bad not in t.replace("kc103_syscheck", "").replace("kc103 check", "").replace("k_c 103 check", "").replace("k_c 103 checks", "").replace("kc103d22875_1025", "").replace("k_c 103 D 22.875 ruling", ""), (bad, t[max(0, t.index(bad) - 100):t.index(bad) + 80])
wr(S + "/kc95d22875s_secant_driver_1025.py", t)
d = "".join(difflib.unified_diff(rd(OLD + "/kc103d22875_secant_driver_1025.py").splitlines(True), t.splitlines(True), "kc103d22875_secant_driver_1025.py", "kc95d22875s_secant_driver_1025.py"))
wr(S + "/diff_secant_driver_vs_kc103.txt", d)

# 2. watcher, keep-awake, session check, sampler
w = rd(OLD + "/kc103d22875_watch_alert_1025.py")
w = w.replace("kc103d22875_1025/I1025-win/kc103_d22875", "kc95d22875s_1025/I1025-win/kc95_d22875_secant").replace("kc103d22875_watch_alert_1025.py", "kc95d22875s_watch_alert_1025.py")
w = w.replace("the k_c 103 stages at D 22.875", "the k_c 95 D 22.875 secant lane").replace("The k_c 103 D 22.875 {label} stage", "The k_c 95 D 22.875 {label} stage")
assert "103" not in w, w[w.index("103") - 60:w.index("103") + 60]
wr(S + "/kc95d22875s_watch_alert_1025.py", w)
k = rd(OLD + "/keepawake_1025.py").replace("kc103d22875_1025/I1025-win/kc103_d22875", "kc95d22875s_1025/I1025-win/kc95_d22875_secant")
assert "103" not in k
wr(S + "/keepawake_1025.py", k)
sc = rd(OLD + "/session_check_1025.ps1").replace("kc103d22875_1025\\I1025-win\\kc103_d22875", "kc95d22875s_1025\\I1025-win\\kc95_d22875_secant")
assert "103" not in sc
wr(S + "/session_check_1025.ps1", sc)
shutil.copyfile(OLD + "/sample_driver_secant_1025.ps1", S + "/sample_driver_secant_1025.ps1")

# 3. the go cmd and the publish script
go = '''@echo off
rem #1025 winb: the k_c 95 D 22.875 secant lane (t5's order of 2026-11-26 ~06:35 UTC): one driver, win2's bracket (0.10, 0.12).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\mingw64\\bin;C:\\Program Files\\Git\\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\\Users\\nathan\\Source\\kc95d22875s_1025
start "" /wait /belownormal /b C:\\Users\\nathan\\Source\\venv-md510\\Scripts\\python.exe -u C:\\Users\\nathan\\Source\\kc95d22875s_1025\\kc95d22875s_secant_driver_1025.py 0.10 0.12 > C:\\Users\\nathan\\Source\\kc95d22875s_1025\\kc95d22875s_secant_driver_stdout.log 2>&1
'''
wr(S + "/go_kc95d22875s_1025.cmd", go.replace("\n", "\r\n"))
pub = '''#!/bin/bash
# copy the staged k_c 95 D 22.875 secant folder (files only) into the push worktree's I1025-win/kc95_d22875_secant, then commit and push linearly with push_1025.sh
# usage: bash publish_kc95d22875s_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc95d22875s_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc95_d22875_secant
D=$W/I1025-win/kc95_d22875_secant
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/in"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/in/"* "$D/in/"
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\\./Pushed $T UTC./" "$D/README.md"
for f in make_kc95d22875s_1025.py diff_secant_driver_vs_kc103.txt kc95d22875s_secant_driver_1025.py kc95d22875s_watch_alert_1025.py sample_driver_secant_1025.ps1 go_kc95d22875s_1025.cmd keepawake_1025.py session_check_1025.ps1 \\
         selftest_secant_dry_1025.txt kc95d22875s_secant_driver_stdout.log publish_kc95d22875s_1025.sh prep_kc95d22875s_pins_1025.txt prep_source_checks_by_hand.txt prep_secant_selftests_by_hand.txt; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
'''
wr(S + "/publish_kc95d22875s_1025.sh", pub)
os.chmod(S + "/publish_kc95d22875s_1025.sh", 0o755)
print("written")
