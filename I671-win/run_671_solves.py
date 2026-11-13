#!/usr/bin/env python3
"""#671: the four RT solves, K = 7 and its same-start K = 0 control at D 40.020065 and D 54.996085, on 32x121 from #145's 32x101 continuation states.
usage: python run_671_solves.py          (BelowNormal, one BLAS thread each, the four at once = 4 busy threads; logs/<tag>.log, logs/<tag>.exit, logs/run_671.log)
Job: python rt_launch.py <worktree>/solver/rt/rt_run.py --start STATE --grids 32x121 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4
     --newton_tol NTOL --horizon 7 --out solves --tag TAG --resample_mp [--mutate=norows]     (#163's run_one.sh: NTOL 1e-40 at D 40.02, 1e-38 at D 54.996)
rt_run.py exits 1 when |Delta_RT - Delta_hp| > 1e-12, the quantity under study, so a solve is judged by its jsonl record (`ok`, newton max|F|), not by the exit code."""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i423"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
os.makedirs(os.path.join(HERE, "solves"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
OPTS = "--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4".split()
CASES = [("D40", "cont_32x101_D40.0201_32x101.npz", "1e-40"), ("D55", "cont_32x101_D54.9961_32x101.npz", "1e-38")]
JOBS = []
for d, f, ntol in CASES:
    JOBS.append((f"k7_{d}", os.path.join(STAGE, "I145-mac", "cont", f), ntol, []))
    JOBS.append((f"k0_{d}", os.path.join(STAGE, "I145-mac", "cont", f), ntol, ["--mutate=norows"]))


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_671.log"), "a").write(line + "\n")


running = []
for tag, start, ntol, extra in JOBS:
    cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_run.py"), "--start", start, "--grids", "32x121", *OPTS, "--newton_tol", ntol,
           "--horizon", "7", "--out", os.path.join(HERE, "solves"), "--tag", tag, "--resample_mp", *extra]
    p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", f"{tag}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    running.append((p, tag, time.time()))
    say(f"start {tag} (pid {p.pid}) from {os.path.basename(start)} NTOL {ntol} {' '.join(extra)}")
while running:
    for r in list(running):
        rc = r[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{r[1]}.exit"), "w").write(f"{rc}\n")
            say(f"{r[1]} exit {rc} after {time.time() - r[2]:.0f} s")
            running.remove(r)
    time.sleep(5)
say("solves done")
