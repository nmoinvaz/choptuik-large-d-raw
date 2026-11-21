#!/usr/bin/env python3
"""#1025 winb, the lambda 1.20 dd check (the coordinator's order, hc 2026-11-21 about 16:1x UTC): after the D 18.125 scan driver (d18mid_driver_1025.py) has ended, the full dd M's
sign at lambda 1.20 on D 18's state (raw I1025-win/out/sol_l1kc63W1025_D18.000000.npy, blob 45e72c6a) and on D 18.0625's (raw I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy,
blob f2307f0e): ell_ddm.py det STATE D 63 1.2 --noise 1e-24,1e-20,1e-16 (5 exact variants; noise on the dd propagator entries, 2 seeds), two processes in parallel, 4 threads
each, BelowNormal, each with a 6 h cap (21600 s) by the exact pid of the process this driver started (taskkill /PID <pid> /T /F). Then read_ref120_1025.py.
usage: ref120_driver_1025.py [--selftest]      (--selftest: the cap and the sampler on two dummy children)"""
import datetime, os, subprocess, sys, time

OUT = "C:/Users/nathan/Source/ref120_1025/I1025-win/d18ref120"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT_D = "C:/Users/nathan/Source/choptuik-i1025d"          # 48c36355: ell_ddm.py, as for rows B and D 18.5
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
RAW = "C:/Users/nathan/Source/ref120_1025/raw"
JOBS = [("D18", "18.0", RAW + "/I1025-win/out/sol_l1kc63W1025_D18.000000.npy", "45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21"),
        ("D18.0625", "18.0625", RAW + "/I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy", "f2307f0e8ffb4621b61f74450a920c652981d973")]
LOG = OUT + "/ref120_w.log"
CAP, LAM = 21600, "1.2"
WAIT_LOG, WAIT_PID = "C:/Users/nathan/Source/d18mid_1025/I1025-win/d18mid/d18mid_w.log", 10592      # the D 18.125 scan driver


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def alive(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command", f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 'yes' }}"], capture_output=True, text=True)
    return bool(r.stdout.strip())


def run_group(cmds, logs, names, cap, cwd, env, samples, interval):
    procs, t0 = [], time.time()
    for c, lg, nm in zip(cmds, logs, names):
        p = subprocess.Popen(c, cwd=cwd, env=env, stdout=open(lg, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        procs.append((p, nm))
        say(f"started {nm} pid {p.pid}: {' '.join(c)[:300]} > {lg}")
    s = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", HERE + "/sample_driver2_1025.ps1", "-Drv", str(os.getpid()), "-Out", samples, "-Interval", str(interval)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rcs = [None] * len(procs)
    while any(r is None for r in rcs):
        for i, (p, nm) in enumerate(procs):
            if rcs[i] is None:
                rc = p.poll()
                if rc is not None:
                    rcs[i] = rc
                    say(f"{nm} pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
                elif time.time() - t0 > cap:
                    r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
                    say(f"CAP {cap} s: killed {nm} pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                    p.wait()
                    rcs[i] = "killed at the cap"
        if any(r is None for r in rcs):
            time.sleep(10)
    return rcs, s


if "--selftest" in sys.argv:
    LOG = HERE + "/ref120_driver_selftest.log"
    smp = HERE + "/ref120_driver_selftest_samples.csv"
    for fn in (LOG, smp):
        if os.path.exists(fn):
            os.remove(fn)
    quick = [PY, "-c", "import time; print('quick', flush=True); time.sleep(12)"]
    slow = [PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"]
    rcs, s = run_group([quick, slow], [HERE + "/ref120_selftest_a.log", HERE + "/ref120_selftest_b.log"], ["quick", "slow"], 30, HERE, dict(os.environ), smp, 5)
    time.sleep(6)
    rows = open(smp).read().splitlines()
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"],
                          capture_output=True, text=True).stdout.strip()
    fields = {len(r.split(",")) for r in rows[1:]}
    ok = rcs == [0, "killed at the cap"] and left == "0" and len(rows) >= 4 and fields == {12}
    say(f"selftest: {rcs}; {len(rows) - 1} sample rows, field counts {fields}; dummy processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    s.kill()
    sys.exit(0 if ok else 1)

say(f"ref120_driver_1025.py: the lambda 1.20 dd check; waiting for the D 18.125 scan driver (pid {WAIT_PID}, {WAIT_LOG})")
while alive(WAIT_PID) and "d18mid_driver_1025.py done" not in open(WAIT_LOG, errors="replace").read():
    time.sleep(30)
say("the D 18.125 scan driver has ended; checking pins")
for tag, D, st, want in JOBS:
    got = subprocess.run(["git", "hash-object", "--no-filters", st], capture_output=True, text=True).stdout.strip()
    if got != want:
        say(f"REFUSE: {st} is blob {got}, not {want}")
        sys.exit(2)
headd = subprocess.run(["git", "-C", WT_D, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if headd != "48c36355d1ba64de4e3112ed968fd6c034384551" or any(os.path.exists(OUT + f"/rows/ell_ddm_{tag}_lam1.2.jsonl") for tag, D, st, w in JOBS):
    say(f"REFUSE: worktree at {headd} or an output exists")
    sys.exit(2)
os.makedirs(OUT + "/rows", exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1")
outs = [OUT + f"/rows/ell_ddm_{tag}_lam1.2.jsonl" for tag, D, st, w in JOBS]
cmds = [[PY, "-u", "ell_ddm.py", "det", st, D, "63", LAM, "--noise", "1e-24,1e-20,1e-16", "--out", o] for (tag, D, st, w), o in zip(JOBS, outs)]
say(f"pins ok; dd: lambda {LAM} on D 18 (blob 45e72c6a) and D 18.0625 (blob f2307f0e), cap {CAP} s each")
rcs, s = run_group(cmds, [OUT + f"/rows/dd_{tag}_lam1.2.log" for tag, D, st, w in JOBS], [f"dd_{tag}" for tag, D, st, w in JOBS], CAP, WT_D + "/solver/matter", env, OUT + "/rows/ref120_samples.csv", 60)
say(f"both dd processes ended: {rcs}")
r = subprocess.run([PY, HERE + "/read_ref120_1025.py", outs[0], outs[1]], capture_output=True, text=True)
open(OUT + "/rows/ref120_reading.log", "w").write(r.stdout + r.stderr)
for ln in r.stdout.splitlines():
    say(ln)
time.sleep(70)          # the sampler's last line
s.kill()
say("ref120_driver_1025.py done")
