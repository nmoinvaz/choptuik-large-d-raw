#!/usr/bin/env python3
"""#725: two anm_run.py runs of the full system (--kfreeze 13) with #682's flags and --elim_switch 0 at a = 1/16, one after the other.
usage: python run_725.py X1 X2          (logs/<name>.log, logs/<name>.exit, logs/run_725.log, output in <name>/)
X1: start I682-win/cont3/anm_pin13_D99.7500.npz, to D 99.8125. X2: start I725-win/X1/anm_pin13_D99.8125.npz, to D 99.875. Both --h_max 0.0625 --a0 0.0625 --steps 1 --elim_switch 0.
Each job: python -u anm_run.py RAW OUT --state S --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i710\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
FLAGS = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "qd", "--tol_qd", "1e-44", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
         "--reseed", "2", "--reseed_q", "1", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04"]
STEP = ["--h_max", "0.0625", "--a0", "0.0625", "--steps", "1", "--elim_switch", "0"]
JOBS = {"X1": "I682-win/cont3/anm_pin13_D99.7500.npz", "X2": "I725-win/X1/anm_pin13_D99.8125.npz"}
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_725.log"), "a").write(line + "\n")


for name in sys.argv[1:]:
    state = JOBS[name]
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, *STEP, "--threads", "4"]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}) from {state}")
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s")
    if rc != 0:
        say(f"{name} exited non-zero, stopping the driver")
        sys.exit(2)
say("done " + " ".join(sys.argv[1:]))
