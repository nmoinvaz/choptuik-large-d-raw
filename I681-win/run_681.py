#!/usr/bin/env python3
"""#681: rt_sigma.py with 12 rough starts on the six states (K = 7 and its K = 0 control at D 40.02, 50.007, 54.996), three at a time, two BLAS threads each, BelowNormal.
usage: python run_681.py          (logs/<label>_rough.log, logs/<label>_rough.exit, logs/run_681.log)
Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 12 --rough, cwd = the worktree root. The states are read in place from the raw repository's stage checkout (origin/main).
The K = 7 runs go first (they are the long ones: up to 250 products per start)."""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i423"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
JOBS = [("K7_D40", r"I671-win\solves\k7_D40_D40.0201_32x121.npz"), ("K7_D50", r"I163-mac\acc\a_32x121_D50.0075_32x121.npz"), ("K7_D55", r"I671-win\solves\k7_D55_D54.9961_32x121.npz"),
        ("K0_D40", r"I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz"), ("K0_D50", r"I163-mac\acc\a_32x121_mutnorows_D50.0075_32x121.npz"),
        ("K0_D55", r"I671-win\solves\k0_D55_mutnorows_D54.9961_32x121.npz")]
NPROC = 3
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="2", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", PYTHONDONTWRITEBYTECODE="1")


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_681.log"), "a").write(line + "\n")


running = []
while JOBS or running:
    for r in list(running):
        rc = r[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{r[1]}_rough.exit"), "w").write(f"{rc}\n")
            say(f"{r[1]} exit {rc} after {time.time() - r[2]:.0f} s")
            running.remove(r)
    while JOBS and len(running) < NPROC:
        label, rel = JOBS.pop(0)
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_sigma.py"), os.path.join(STAGE, rel), "--starts", "12", "--rough"]
        p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", f"{label}_rough.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
        running.append((p, label, time.time()))
        say(f"start {label} (pid {p.pid}) {os.path.basename(rel)}")
    time.sleep(5)
say("all done")
