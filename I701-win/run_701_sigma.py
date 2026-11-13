#!/usr/bin/env python3
"""#701: rt_sigma.py with 12 rough starts on the two start-b states (K = 7 and its K = 0 control at D 40.02), both at once, two BLAS threads each (4 busy threads), BelowNormal.
usage: python run_701_sigma.py          (logs/<label>_rough.log, logs/<label>_rough.exit, logs/run_701_sigma.log)
Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 12 --rough, cwd = the worktree root. The states are read from this folder's solves/ (written by run_701_solves.py)."""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i423"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
JOBS = [("K7b_D40", os.path.join(HERE, "solves", "k7b_D40_D40.0201_32x121.npz")), ("K0b_D40", os.path.join(HERE, "solves", "k0b_D40_mutnorows_D40.0201_32x121.npz"))]
NPROC = 2
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="2", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", PYTHONDONTWRITEBYTECODE="1")


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_701_sigma.log"), "a").write(line + "\n")


for _, path in JOBS:
    if not os.path.exists(path):
        say(f"missing state {path}")
        raise SystemExit(2)
running = []
while JOBS or running:
    for r in list(running):
        rc = r[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{r[1]}_rough.exit"), "w").write(f"{rc}\n")
            say(f"{r[1]} exit {rc} after {time.time() - r[2]:.0f} s")
            running.remove(r)
    while JOBS and len(running) < NPROC:
        label, path = JOBS.pop(0)
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_sigma.py"), path, "--starts", "12", "--rough"]
        p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", f"{label}_rough.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
        running.append((p, label, time.time()))
        say(f"start {label} (pid {p.pid}) {os.path.basename(path)}")
    time.sleep(5)
say("all done")
