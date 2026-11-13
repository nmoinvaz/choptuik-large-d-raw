#!/usr/bin/env python3
"""#623: the sigma-model refines at k_c 23 and 39, BelowNormal, one thread each (OPENBLAS_NUM_THREADS=1).
usage: python run_623.py NPROC KC:E [KC:E ...]       e.g.  python run_623.py 1 39:inf      or      python run_623.py 4 23:inf 23:10.0000 23:5.0000 23:2.0000
(E in inf, 10.0000, 5.0000, 2.0000; EPS = 1/E). Each job: python -u sigdss_run.py refine data/sigdss_sol_i623seed_D4.0000_eta{E}.npy --D 4 --eps EPS --kc_seed 15 --kc KC --kappa 0.5 --tag i623_kc{KC}_eta{E},
from the worktree's solver/matter; stdout and stderr -> logs/kc{KC}_eta{E}.log, exit code -> logs/kc{KC}_eta{E}.exit, start and exit times (UTC) -> logs/run_623.log."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CWD = r"C:\Users\nathan\Source\choptuik-i623\solver\matter"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
EPS = {"inf": "0", "10.0000": "0.1", "5.0000": "0.2", "2.0000": "0.5"}
NPROC = int(sys.argv[1])
JOBS = [tuple(j.split(":")) for j in sys.argv[2:]]
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_623.log"), "a").write(line + "\n")


running = []
while JOBS or running:
    for p in list(running):
        rc = p[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{p[1]}.exit"), "w").write(f"{rc}\n")
            say(f"{p[1]} exit {rc} after {time.time() - p[2]:.0f} s")
            running.remove(p)
    while JOBS and len(running) < NPROC:
        kc, e = JOBS.pop(0)
        tag = f"kc{kc}_eta{e}"
        cmd = [PY, "-u", "sigdss_run.py", "refine", f"data/sigdss_sol_i623seed_D4.0000_eta{e}.npy", "--D", "4", "--eps", EPS[e],
               "--kc_seed", "15", "--kc", kc, "--kappa", "0.5", "--tag", f"i623_{tag}"]
        proc = subprocess.Popen(cmd, cwd=CWD, stdout=open(os.path.join(HERE, "logs", f"{tag}.log"), "w"), stderr=subprocess.STDOUT, env=env,
                                creationflags=0x00004000 | 0x08000000)
        running.append((proc, tag, time.time()))
        say(f"start {tag} (pid {proc.pid})")
    time.sleep(5)
say("all done")
