#!/usr/bin/env python3
"""#643: the N_t = 48 state at D 50.007491, made the way #145 made its D 40 one: re-solve the stored K = 0 root of the 32x121 grid on 48x121 (192-bit rt_run.py --solver mp, #163's options), at its own D.
usage: python run_nt48.py          (BelowNormal, 2 BLAS threads; the matrix is 3.1 GiB, under the 4 GiB at which multithreaded OpenBLAS crashes here)
Job: python rt_launch.py <worktree>/solver/rt/rt_run.py --start I145-mac/fol/fol_32x121_D50.0075_32x121.npz --grids 48x121 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20
     --full_below 1e-4 --newton_tol 1e-40 --out nt48 --tag nt48_121; stdout -> logs/nt48_121.log, exit code -> logs/nt48_121.exit. rt_run.py exits 1 when |Delta_RT - Delta_hp| > 1e-12, the quantity
under study, so the verdict is the record's `ok` and max|F| in nt48/*.jsonl, not the exit code."""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i423"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
START = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage\I145-mac\fol\fol_32x121_D50.0075_32x121.npz"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
os.makedirs(os.path.join(HERE, "nt48"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="2", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", PYTHONDONTWRITEBYTECODE="1")
opts = "--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4".split()
cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_run.py"), "--start", START, "--grids", "48x121", *opts, "--newton_tol", "1e-40",
       "--out", os.path.join(HERE, "nt48"), "--tag", "nt48_121"]
t0 = time.time()
p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", "nt48_121.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start nt48_121 (pid {p.pid})"
print(line, flush=True)
open(os.path.join(HERE, "logs", "run_643.log"), "a").write(line + "\n")
rc = p.wait()
open(os.path.join(HERE, "logs", "nt48_121.exit"), "w").write(f"{rc}\n")
line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC nt48_121 exit {rc} after {time.time() - t0:.0f} s"
print(line, flush=True)
open(os.path.join(HERE, "logs", "run_643.log"), "a").write(line + "\n")
