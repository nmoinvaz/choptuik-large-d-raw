#!/usr/bin/env python3
"""#423: rt_sigma.py runs on stored RT states (smooth and rough starts), a few at a time, BelowNormal, 2 BLAS threads each.
usage: python run_423.py NPROC LABEL=STATEPATH [LABEL=STATEPATH ...]      each state runs twice, smooth then rough, as separate jobs
Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 3 [--rough]  (cwd = the worktree root), stdout and stderr -> logs/<LABEL>_<smooth|rough>.log,
exit code -> logs/<LABEL>_<kind>.exit, start and exit times (UTC) and wall seconds -> logs/run_423.log.
The states are read in place from the raw repository's stage checkout (origin/main); nothing is copied or changed."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i423"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
NPROC = int(sys.argv[1])
jobs = []
for arg in sys.argv[2:]:
    label, path = arg.split("=", 1)
    jobs += [(label, "smooth", os.path.join(STAGE, path)), (label, "rough", os.path.join(STAGE, path))]
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
BT = os.environ.get("I423_BLAS_THREADS", "2")      # 2 for every run except the 48x141 retry, which needs 1 (multithreaded OpenBLAS crashes above 4 GiB, lu_size_test.py)
env = dict(os.environ, OPENBLAS_NUM_THREADS=BT, OMP_NUM_THREADS=BT, MKL_NUM_THREADS=BT, PYTHONDONTWRITEBYTECODE="1")


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_423.log"), "a").write(line + "\n")


running = []
while jobs or running:
    for r in list(running):
        rc = r[0].poll()
        if rc is not None:
            wall = time.time() - r[2]
            open(os.path.join(HERE, "logs", f"{r[1]}.exit"), "w").write(f"{rc}\n")
            say(f"{r[1]} exit {rc} after {wall:.0f} s")
            running.remove(r)
    while jobs and len(running) < NPROC:
        label, kind, path = jobs.pop(0)
        name = f"{label}_{kind}"
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_sigma.py"), path, "--starts", "3"] + (["--rough"] if kind == "rough" else [])
        p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
        running.append((p, name, time.time()))
        say(f"start {name} (pid {p.pid}) {os.path.basename(path)}")
    time.sleep(5)
say("all done")
