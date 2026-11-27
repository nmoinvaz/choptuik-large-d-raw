#!/usr/bin/env python3
"""#1102 winb: the Windows gate of the Rust block 12 (t5's order, hc of 2026-11-27 05:47 UTC). Worktree choptuik-i1102 = branch wip/ell1-rust-b12 at d4b6b6ce (detached);
SPEED_ELL1.md "Block 12 in Rust" from Git Bash. Order of the driver (any failure stops it, nothing further is started, exit 2; no toolchain is installed):
  1. pins: worktree HEAD d4b6b6ce and clean; the ellrs tree (47ce5fb8), ell_b12rs.py (a1fff74f), ell_ddm.py, ddnp.py, ell_fastm.py, dss_ell.py; the k_c 31 state (f07a8984) and stub (e5a87ec5) from raw I1102-mac/in;
     cargo, rustc and maturin found (cargo and maturin are only looked for here; if one is missing the driver stops and says so);
  2. ellrs/build.sh SITE (SITE = this stage's site/, outside the scanner's venv, which stays untouched: pip freeze before and after must be equal and ellrs must not import from the venv alone);
  3. with PYTHONPATH=SITE and OPENBLAS_NUM_THREADS=1: ell_b12rs.py selftest (exit 0 wanted), selftest --mutate=nolam (1), selftest --mutate=harm (1),
     check STUB STATE 10.5 2.87 --threads=4 --controls=1 (0 wanted, "15010 of 15010 entries bit for bit", both controls FAIL).
Everything is BelowNormal (the cmd starts this driver so). A keep-awake helper runs beside it. Logs in I1102-win/ (gate_driver_w.log, build.log, gate_*.log, gate_summary.txt).
usage: gate_i1102_driver_1025.py [--dry]     (--dry: step 1 and the toolchain versions only)"""
import datetime, os, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
OUT = S + "/I1102-win"
ROWS = OUT + "/rows"
IN = S + "/inputs"
SITE = S + "/site"
WTS = "C:/Users/nathan/Source/choptuik-i1102"
WTM = WTS + "/solver/matter"
VENV = "C:/Users/nathan/Source/venv-md510"
PY = VENV + "/Scripts/python.exe"
GITBIN = "C:/Program Files/Git/bin/bash.exe"
CARGOBIN = "C:/Users/nathan/.cargo/bin"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
os.makedirs(ROWS, exist_ok=True)
LOG = OUT + "/gate_driver_w.log"
B_HEAD = "d4b6b6cea24f518d38cac17877c9a0da813b05f4"
PINS = [("", "ellrs", "47ce5fb8b2d9ddcda01953385d9be93c64fdc2a1"), ("", "ell_b12rs.py", "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef"),
        ("", "ell_ddm.py", "86578feeab868691778019b79771aef727510a76"), ("", "ddnp.py", "9b1fb195d0fa95d5dd7abd1083ac9b36fef04869"),
        ("", "ell_fastm.py", "93f963f6102f48e35c56c9eace25e1afd03b6ea2"), ("", "dss_ell.py", "5d28c19e17efa6b0103cb81d650891706605532d")]
STATE, STUB = IN + "/sol_l1kc31r1025_D10.5000.npy", IN + "/l1kc31r1025.jsonl"
B_STATE, B_STUB = "f07a8984e9b13be834a171a44f05f8bd979735b0", "e5a87ec573c6e53c36c2ef3b2598850f44e8d68d"


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a", encoding="utf-8").write(line + "\n")


def refuse(m):
    say("REFUSE: " + m)
    sys.exit(2)


def run(cmd, log=None, env=None, cwd=None, cap=3600):
    t0 = time.time()
    f = open(log, "w", encoding="utf-8", errors="replace") if log else subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, env=env, cwd=cwd, text=True if not log else None)
    try:
        out = p.communicate(timeout=cap)[0]
        rc = p.returncode
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
        say(f"CAP {cap} s reached: killed pid {p.pid} (exact pid, tree) running {cmd[:3]}")
        out, rc = "", 124
    if log:
        f.close()
    return rc, (out or ""), time.time() - t0


def git(*a):
    return subprocess.run(["git", "-C", WTS] + list(a), capture_output=True, text=True).stdout.strip()


say(f"gate_i1102_driver_1025.py {'(dry) ' if DRY else ''}: the Windows gate of the Rust block 12 (#1102); worktree {WTS}")
# 1. pins
if git("rev-parse", "HEAD") != B_HEAD:
    refuse(f"worktree HEAD {git('rev-parse', 'HEAD')} is not {B_HEAD}")
if git("status", "--porcelain") and not os.path.exists(OUT + "/build.log"):
    refuse("worktree not clean before the build: " + git("status", "--porcelain")[:200])
for _, name, want in PINS:
    path = "solver/matter/" + name
    got = git("rev-parse", "HEAD:" + path)
    if got != want:
        refuse(f"{path}: {got} (wanted {want})")
for path, want in ((STATE, B_STATE), (STUB, B_STUB)):
    got = subprocess.run(["git", "hash-object", "--no-filters", path], capture_output=True, text=True).stdout.strip()
    if got != want:
        refuse(f"{path}: blob {got} (wanted {want})")
say("pins ok: worktree HEAD d4b6b6ce, the ellrs tree 47ce5fb8, ell_b12rs.py a1fff74f, ell_ddm.py, ddnp.py, ell_fastm.py, dss_ell.py; the k_c 31 state f07a8984 and stub e5a87ec5")
env = dict(os.environ)
env["PATH"] = ";".join([CARGOBIN, VENV + "/Scripts", "C:/Program Files/Git/usr/bin", "C:/Program Files/Git/mingw64/bin"]) + ";" + env["PATH"]
env["VIRTUAL_ENV"] = VENV
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"
env["VECLIB_MAXIMUM_THREADS"] = "1"
env.pop("PYTHONPATH", None)
tool = {}
for nm, cmd in (("cargo", [CARGOBIN + "/cargo.exe", "--version"]), ("rustc", [CARGOBIN + "/rustc.exe", "-vV"]), ("maturin", [VENV + "/Scripts/maturin.exe", "--version"]), ("python", [PY, "-c", "import sys, numpy, scipy; print(sys.version.split()[0], 'numpy', numpy.__version__, 'scipy', scipy.__version__)"])):
    try:
        rc, out, _ = run(cmd, env=env, cap=120)
    except FileNotFoundError:
        rc, out = 127, ""
    tool[nm] = (rc, out.strip())
    say(f"{nm}: exit {rc}: " + " | ".join(out.strip().splitlines()[:1] + [l for l in out.splitlines() if l.startswith("host") or l.startswith("release")]))
if tool["cargo"][0] != 0 or tool["maturin"][0] != 0:
    refuse("cargo or maturin is missing (not installing toolchains, as ordered): report to t5 and stop")
rc, freeze0, _ = run([PY, "-m", "pip", "freeze"], env=env, cap=300)
open(OUT + "/venv_freeze_before.txt", "w").write(freeze0)
say(f"scanner venv {VENV}: pip freeze before, {len(freeze0.splitlines())} lines (venv_freeze_before.txt)")
if DRY:
    say("dry run ends here: nothing built")
    sys.exit(0)

kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1025.py", str(os.getpid()), "gate", "7200"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       creationflags=0x00004000)
say(f"keep-awake helper started as its own process, pid {kaw.pid}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until this driver (pid {os.getpid()}) ends; power plan untouched; kills nothing")
res = []

# 2. build
say("build: ellrs/build.sh SITE  (maturin build --release, RUSTFLAGS=-C target-cpu=native, pip install --target SITE; cap 3600 s)")
rc, out, wall = run([GITBIN, WTM + "/ellrs/build.sh", SITE], log=OUT + "/build.log", env=env, cwd=WTM, cap=3600)
tail = [l for l in open(OUT + "/build.log", encoding="utf-8", errors="replace").read().splitlines() if l.strip()][-3:]
say(f"build: exit {rc}, {wall:.0f} s; last lines: " + " | ".join(tail))
res.append(("build.sh SITE", rc, 0, wall))
if rc != 0:
    say("build failed: nothing further started; report to t5")
    sys.exit(2)
rc, freeze1, _ = run([PY, "-m", "pip", "freeze"], env=env, cap=300)
open(OUT + "/venv_freeze_after.txt", "w").write(freeze1)
rc2, imp, _ = run([PY, "-c", "import importlib.util as u; print('ellrs in the venv alone:', u.find_spec('ellrs'))"], env=env, cap=120)
say(f"scanner venv untouched: pip freeze after equals before: {freeze0 == freeze1}; {imp.strip()}")
genv = dict(env)
genv["PYTHONPATH"] = SITE

# 3. gates
GATES = [("selftest", ["selftest"], 0, "gate_selftest.log"),
         ("selftest --mutate=nolam", ["selftest", "--mutate=nolam"], 1, "gate_selftest_nolam.log"),
         ("selftest --mutate=harm", ["selftest", "--mutate=harm"], 1, "gate_selftest_harm.log"),
         ("check k_c 31 D 10.5 lambda 2.87 --threads=4 --controls=1", ["check", STUB, STATE, "10.5", "2.87", "--threads=4", "--controls=1", "--out=" + OUT + "/check_kc31.jsonl"], 0, "gate_check_kc31.log")]
ok = True
for nm, a, want, lg in GATES:
    rc, out, wall = run([PY, "-u", WTM + "/ell_b12rs.py"] + a, log=OUT + "/" + lg, env=genv, cwd=WTM, cap=3600)
    body = [l for l in open(OUT + "/" + lg, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
    say(f"{nm}: exit {rc} (wanted {want}), {wall:.0f} s; {len(body)} lines; last: {body[-1][:200] if body else ''}")
    res.append((nm, rc, want, wall))
    ok = ok and rc == want
chk = open(OUT + "/gate_check_kc31.log", encoding="utf-8", errors="replace").read()
bit = "15010 of 15010" in chk
say(f"the check printed '15010 of 15010': {bit}")
ok = ok and bit
with open(OUT + "/gate_summary.txt", "w", encoding="utf-8") as f:
    f.write("step, exit, wanted, wall s\n")
    for nm, rc, want, wall in res:
        f.write(f"{nm}, {rc}, {want}, {wall:.0f}\n")
    f.write(f"15010 of 15010 printed: {bit}\nall as wanted: {ok}\n")
say("ALL GATES AS WANTED" if ok else "NOT AS WANTED: see gate_summary.txt")
say("gate_i1102_driver_1025.py done")
sys.exit(0 if ok else 1)
