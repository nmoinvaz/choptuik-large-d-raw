#!/usr/bin/env python3
"""#682: anm_run.py on the full system (--kfreeze 13, no --held_fit) from I642-win/released_kf13_D77.0000.npz, quad-double jet and corrector (README.md).
usage: python run_682.py chain          the 3-step chain, 4 threads (logs/chain.log, chain/)
       python run_682.py ladder         single steps at fixed a = 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, one after the other, 2 threads (logs/ladder_a<k>.log, ladder/a<k>/)
       python run_682.py probe          the double-double probe (no --jet_q), 4 threads (logs/probe_dd.log, probe_dd/)
       python run_682.py cont           the continuation from chain/anm_pin13_D80.0000.npz, --steps 20, 4 threads (logs/cont.log, cont/)
       python run_682.py cont2          one step of 0.5 from cont/anm_pin13_D99.5000.npz to D 100, 4 threads (logs/cont2.log, cont2/)
       python run_682.py cont3          up to 8 steps of at most 1/8 from cont2/anm_pin13_D99.6250.npz, 4 threads, anm_run's stop at three refusals in a row (logs/cont3.log, cont3/)
       python run_682.py cont4          one step of 3/64 from cont3/anm_pin13_D99.9531.npz (D 99.953125) to D 100 exactly, 4 threads (logs/cont4.log, cont4/)
Each job: python -u anm_run.py RAWDIR OUTDIR --state I642-win/released_kf13_D77.0000.npz --kfreeze 13 --N 24 --eps 1e-14 --h_max H --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12
          --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads T --steps S, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i682\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
BASE = ["--state", "I642-win/released_kf13_D77.0000.npz", "--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "qd", "--tol_qd", "1e-44", "--qd_it", "12",
        "--reseed", "2", "--reseed_q", "1", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04"]
JETQ = ["--jet_q", "1", "--pred_q", "1"]


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_682.log"), "a").write(line + "\n")


def run(name, out, extra, threads):
    os.makedirs(out, exist_ok=True)
    cmd = [PY, "-u", "anm_run.py", RAW, out, *BASE, *extra, "--threads", str(threads)]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}): {' '.join(extra)} threads {threads}")
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s")
    return rc


os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
mode = sys.argv[1]
if mode == "chain":
    run("chain", os.path.join(HERE, "chain"), [*JETQ, "--h_max", "1.0", "--steps", "3"], 4)
elif mode == "ladder":
    for den in (64, 32, 16, 8, 4, 2):
        a = Fraction(1, den)
        run(f"ladder_a1_{den}", os.path.join(HERE, "ladder", f"a1_{den}"), [*JETQ, "--h_max", repr(float(a)), "--a0", repr(float(a)), "--steps", "1"], 2)
elif mode == "cont":
    BASE[BASE.index("I642-win/released_kf13_D77.0000.npz")] = "I682-win/chain/anm_pin13_D80.0000.npz"
    run("cont", os.path.join(HERE, "cont"), [*JETQ, "--h_max", "1.0", "--steps", "20"], 4)
elif mode == "cont2":
    BASE[BASE.index("I642-win/released_kf13_D77.0000.npz")] = "I682-win/cont/anm_pin13_D99.5000.npz"
    run("cont2", os.path.join(HERE, "cont2"), [*JETQ, "--h_max", "0.5", "--steps", "1"], 4)
elif mode == "cont3":
    BASE[BASE.index("I642-win/released_kf13_D77.0000.npz")] = "I682-win/cont2/anm_pin13_D99.6250.npz"
    run("cont3", os.path.join(HERE, "cont3"), [*JETQ, "--h_max", "0.125", "--a0", "0.125", "--steps", "8"], 4)
elif mode == "cont4":
    BASE[BASE.index("I642-win/released_kf13_D77.0000.npz")] = "I682-win/cont3/anm_pin13_D99.9531.npz"
    run("cont4", os.path.join(HERE, "cont4"), [*JETQ, "--h_max", "0.046875", "--a0", "0.046875", "--steps", "1"], 4)
elif mode == "probe":
    run("probe_dd", os.path.join(HERE, "probe_dd"), ["--h_max", "1.0", "--steps", "1", "--probe", "1"], 4)
say(f"{mode} done")
