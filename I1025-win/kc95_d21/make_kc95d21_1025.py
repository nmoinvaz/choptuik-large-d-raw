#!/usr/bin/env python3
"""make_kc95d21_1025.py: writes the k_c 95 D 21.0 stage's scripts from the k_c 95 D 19 ones (raw I1025-win/kc95_d19 at f2bcf20e, staging kc95d19_1025) and the k_c 87 leg ones (kc87leg_1025/tpl) by asserted text replacements:
kc95d21_regrid_driver_1025.py, kc95d21_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1, sample_driver4_1025.ps1, go_kc95d21_1025.cmd, publish_kc95d21_1025.sh. The scan driver
kc95d21_scan_driver_1025.py is written by hand (four processes, from the k_c 87 leg driver). Each asserted replacement must occur; the diffs against the k_c 95 D 19 files are written to diff_*_vs_kc95d19.txt."""
import difflib, os, re

S = "C:/Users/nathan/Source/kc95d21_1025"
OLD = "C:/Users/nathan/Source/kc95d19_1025"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert a in t, a[:100]
        t = t.replace(a, b)
    return t


# 1. the regrid driver
t = rd(OLD + "/kc95d19_regrid_driver_1025.py")
i = t.index('"""'); j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the k_c 95 regrid at D 21.0 (t5's order, hc of 2026-11-24 ~11:05 UTC): dh610's accepted k_c 87 D 21.0 state (raw I1025-dh610/kc87_d21 at 6e89d6279: sol_l1kc87dh610e_D21.0000.npy blob 831d5977,
l1kc87dh610e.jsonl blob 9b090ba6) is regridded to k_c 95 with
  ell_refine.py l1kc87dh610e 87 l1kc95winbg 95 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.1067409501 is t5's lambda_0, unused with --no-gamma)
4 threads, BelowNormal, cap 28800 s by the exact pid, one process outside my terminal. Order of the driver (any failure stops it with an hc to t5, no regrid, exit 2 or 1):
  1. pins: dh610's kc87_syscheck_1025.py (6df5d960) and kc95_syscheck_1025.py (d487e628, the version dh610 used at D 19.5, raw I1025-dh610/kc95_d195/in/; the k_c 87 check with the k_c test changed to 95:
     3 changed lines), d18_hybsign.py, d185_scan_read.py, read_lower.py, the k_c 87 D 21.0 state and record (inputs/ and the worktree's copies), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399,
     ell_refine.py 631e5801);
  2. the selftest of both checks (exit 0 each);
  3. the SOURCE: the k_c 87 check accepts it (exit 0) and its --mutate=F and --mutate=steps exit 1; the k_c 95 check refuses it (exit 1);
  4. the regrid;
  5. ACCEPTED only if kc95_syscheck_1025.py exits 0 on the result, its selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc87_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_kc95d21_1025.cmd). Memory: no guard, the alert-only watcher is a separate
process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: kc95d21_regrid_driver_1025.py [--dry]     (--dry: pins and the two selftests only, nothing written outside rows/*.dry and the .dry logs, nothing started)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ('S = "C:/Users/nathan/Source/kc95d19_1025"', 'S = "C:/Users/nathan/Source/kc95d21_1025"'),
    ('OUT = S + "/I1025-win/kc95_d19"', 'OUT = S + "/I1025-win/kc95_d21"'),
    ('SRCD = "C:/Users/nathan/Source/kc87d19_1025/I1025-win/kc87_d19"          # my accepted k_c 87 D 19 state, record and marker (raw I1025-win/kc87_d19)',
     'SRCD = IN          # dh610\'s accepted k_c 87 D 21.0 state and record (raw I1025-dh610/kc87_d21 at 6e89d6279; copies in inputs/)'),
    ('SRC, TAG = "l1kc87wind19", "l1kc95wind19"', 'SRC, TAG = "l1kc87dh610e", "l1kc95winbg"'),
    ('SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D19.0000.npy", SRCD + f"/{SRC}.jsonl"', 'SRCSTATE, SRCREC = SRCD + f"/sol_{SRC}_D21.0000.npy", SRCD + f"/{SRC}.jsonl"'),
    ('STATE_N = f"sol_{TAG}_D19.0000.npy"', 'STATE_N = f"sol_{TAG}_D21.0000.npy"'),
    ('LAM0 = "2.1156378446"', 'LAM0 = "2.1067409501"'),
    ('''(SRCSTATE, "100f63f7a2f9a3e3ee3ff845bfd791f3829da1b9"), (SRCREC, "4fae16215e65c687189e911af17976785f6aaf59"), (SRCD + "/regrid_accepted.txt", "3d80146944abb67be68a05bb4c7be81734b192f2"),
        (WTM + f"/data/sol_{SRC}_D19.0000.npy", "100f63f7a2f9a3e3ee3ff845bfd791f3829da1b9"), (WTM + f"/data/{SRC}.jsonl", "4fae16215e65c687189e911af17976785f6aaf59")]''',
     '''(SRCSTATE, "831d5977561cab4323ace23bc5f71c05c4de926e"), (SRCREC, "9b090ba675238bd389108da4c45738d109511b84"),
        (WTM + f"/data/sol_{SRC}_D21.0000.npy", "831d5977561cab4323ace23bc5f71c05c4de926e"), (WTM + f"/data/{SRC}.jsonl", "9b090ba675238bd389108da4c45738d109511b84")]'''),
    ('LOG = OUT + "/kc95_regrid_w.log"', 'LOG = OUT + "/kc95_regrid_w.log"'),
    ('CAPRG = 21600', 'CAPRG = 28800'),
    ('#1025 k_c 95 regrid at D 19: {m}', '#1025 k_c 95 regrid at D 21.0: {m}'),
    ('kc95d19_regrid_driver_1025.py: the k_c 95 regrid at D 19 from my k_c 87 D 19 state', 'kc95d21_regrid_driver_1025.py: the k_c 95 regrid at D 21.0 from dh610\'s k_c 87 D 21.0 state'),
    ('the k_c 87 D 19 files, worktree', 'the k_c 87 D 21.0 files, worktree'),
    ('95 1 19.0 {LAM0} --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s)', '95 1 21.0 {LAM0} --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd {WTM}, 4 threads, BelowNormal, cap {CAPRG} s)'),
    ('S + "/kc95d19_watch_alert_1025.py"', 'S + "/kc95d21_watch_alert_1025.py"'),
    ('[PY, SY87, SRCREC, SRCSTATE, "19", WTM]', '[PY, SY87, SRCREC, SRCSTATE, "21.0", WTM]'),
    ('[PY, SY87, SRCREC, SRCSTATE, "19", WTM, "--mutate=F"]', '[PY, SY87, SRCREC, SRCSTATE, "21.0", WTM, "--mutate=F"]'),
    ('[PY, SY87, SRCREC, SRCSTATE, "19", WTM, "--mutate=steps"]', '[PY, SY87, SRCREC, SRCSTATE, "21.0", WTM, "--mutate=steps"]'),
    ('[PY, SY95, SRCREC, SRCSTATE, "19", WTM]', '[PY, SY95, SRCREC, SRCSTATE, "21.0", WTM]'),
    ('SRC, "87", TAG, "95", "1", "19.0", LAM0,', 'SRC, "87", TAG, "95", "1", "21.0", LAM0,'),
    ('[PY, SY95, rec, state, "19", WTM]', '[PY, SY95, rec, state, "21.0", WTM]'),
    ('[PY, SY95, rec, state, "19", WTM, "--mutate=F"]', '[PY, SY95, rec, state, "21.0", WTM, "--mutate=F"]'),
    ('[PY, SY95, rec, state, "19", WTM, "--mutate=steps"]', '[PY, SY95, rec, state, "21.0", WTM, "--mutate=steps"]'),
    ('[PY, SY87, rec, state, "19", WTM]', '[PY, SY87, rec, state, "21.0", WTM]'),
    ('.get("D") == 19.0][-1]', '.get("D") == 21.0][-1]'),
    ('the k_c 87 source record at D 19:', 'the k_c 87 source record at D 21.0:'),
    ('Raw I1025-win/kc95_d19 after my next push. " + ("The scan 1.395-1.435 and 1.530-1.550 by 0.005 plus a repeat of 1.415 (15 evaluations) starts by itself now."',
     'Raw I1025-win/kc95_d21 after my next push. " + ("The scan 0.900-0.925 by 0.005 plus a repeat of 0.910 (7 evaluations, 4 processes) starts by itself now."'),
    ('kc95d19_regrid_driver_1025.py done', 'kc95d21_regrid_driver_1025.py done'),
])
left = [m.group(0) for m in re.finditer(r".{30}19.{30}", t)]
print("regrid driver, remaining '19':", left)
wr(S + "/kc95d21_regrid_driver_1025.py", t)

# 2. helpers
for src, dst in (("kc95d19_watch_alert_1025.py", "kc95d21_watch_alert_1025.py"), ("keepawake_1025.py", "keepawake_1025.py"), ("session_check_1025.ps1", "session_check_1025.ps1"), ("sample_driver4_1025.ps1", "sample_driver4_1025.ps1")):
    t = rd(OLD + "/" + src)
    t = t.replace("kc95d19_1025", "kc95d21_1025").replace("kc95_d19", "kc95_d21").replace("kc95d19_watch", "kc95d21_watch").replace("k_c 95 check at D 19", "k_c 95 stages at D 21.0").replace("k_c 95 D 19", "k_c 95 D 21.0")
    wr(S + "/" + dst, t)
    print(dst, "remaining '19':", [m.group(0) for m in re.finditer(r".{25}19.{25}", t)][:4])

# 3. the go cmd
wr(S + "/go_kc95d21_1025.cmd", r"""@echo off
rem #1025 winb: the k_c 95 D 21.0 chain (t5's order of 2026-11-24 ~11:05 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered shares (7 evaluations, 4 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc95d21_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d21_1025\kc95d21_regrid_driver_1025.py > C:\Users\nathan\Source\kc95d21_1025\kc95d21_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc95d21_1025\I1025-win\kc95_d21\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d21_1025\kc95d21_scan_driver_1025.py "0.900,0.910;0.905,0.920;0.910,0.925;0.915" > C:\Users\nathan\Source\kc95d21_1025\kc95d21_scan_driver_stdout.log 2>&1
""".replace("\n", "\r\n"))

# 4. the publish script
wr(S + "/publish_kc95d21_1025.sh", """#!/bin/bash
# copy the staged k_c 95 D 21.0 folder (files only) into the push worktree's I1025-win/kc95_d21, then commit and push linearly with push_1025.sh
# usage: bash publish_kc95d21_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in readme_first_time.txt),
# and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc95d21_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc95_d21
D=$W/I1025-win/kc95_d21
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\\./Pushed $T UTC./" "$D/README.md"
for f in make_kc95d21_1025.py diff_regrid_driver_vs_kc95d19.txt kc95d21_regrid_driver_1025.py kc95d21_scan_driver_1025.py kc95d21_watch_alert_1025.py sample_driver4_1025.ps1 go_kc95d21_1025.cmd keepawake_1025.py session_check_1025.ps1 \\
         selftest_scan_dry_1025.txt kc95d21_regrid_driver_stdout.log kc95d21_scan_driver_stdout.log publish_kc95d21_1025.sh prep_kc95d21_pins_1025.txt; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
""")
# diff of the regrid driver against the k_c 95 D 19 one
a = rd(OLD + "/kc95d19_regrid_driver_1025.py").splitlines()
b = rd(S + "/kc95d21_regrid_driver_1025.py").splitlines()
wr(S + "/diff_regrid_driver_vs_kc95d19.txt", "\n".join(difflib.unified_diff(a, b, "kc95d19_regrid_driver_1025.py", "kc95d21_regrid_driver_1025.py", lineterm="")) + "\n")
print("done")
