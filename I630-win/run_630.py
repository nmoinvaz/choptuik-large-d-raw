#!/usr/bin/env python3
"""#630: sigma-model at eta = 20, D = 4: the k_c 15 continuation from eta = 10 (eps 0.1) to eta = 20 (eps 0.05), then the refines to k_c 23 and 39 at once.
usage: python run_630.py          (BelowNormal, OPENBLAS_NUM_THREADS=1, one thread per process; logs/*.log, logs/*.exit, logs/run_630.log)
Commands (from the worktree's solver/matter):
  python -u sigdss_run.py cont i630 data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy --par eps --start 0.1 --end 0.05 --targets 0.05 --D 4 --kc 15 --kappa 0.5
  python -u sigdss_run.py refine data/sigdss_sol_i630_D4.0000_eta20.0000.npy --D 4 --eps 0.05 --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i630_kc{23,39}_eta20"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CWD = r"C:\Users\nathan\Source\choptuik-i623\solver\matter"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_630.log"), "a").write(line + "\n")


def start(name, args):
    p = subprocess.Popen([PY, "-u", "sigdss_run.py"] + args, cwd=CWD, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT,
                         env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid})")
    return p, name, time.time()


def finish(p):
    rc = p[0].wait()
    open(os.path.join(HERE, "logs", f"{p[1]}.exit"), "w").write(f"{rc}\n")
    say(f"{p[1]} exit {rc} after {time.time() - p[2]:.0f} s")
    return rc


cont = start("cont_i630", ["cont", "i630", "data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy", "--par", "eps", "--start", "0.1", "--end", "0.05", "--targets", "0.05",
                           "--D", "4", "--kc", "15", "--kappa", "0.5"])
rc = finish(cont)
seed = os.path.join(CWD, "data", "sigdss_sol_i630_D4.0000_eta20.0000.npy")
if rc != 0 or not os.path.exists(seed):
    say("continuation did not produce the eta = 20 point, stopping")
    sys.exit(1)
procs = [start(f"kc{kc}_eta20", ["refine", "data/sigdss_sol_i630_D4.0000_eta20.0000.npy", "--D", "4", "--eps", "0.05", "--kc_seed", "15", "--kc", str(kc), "--kappa", "0.5",
                                 "--tag", f"i630_kc{kc}_eta20"]) for kc in (23, 39)]
for p in procs:
    finish(p)
say("all done")
