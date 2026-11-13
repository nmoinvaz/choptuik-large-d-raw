#!/usr/bin/env python3
"""#631: sigma-model at eta = 7 and 14, D = 4: the k_c 15 continuations (7 from eta 5, 14 from eta 10), then the refines to k_c 23 and 39.
usage: python run_631.py          (BelowNormal, OPENBLAS_NUM_THREADS=1, one thread per process, at most 4 busy; logs/*.log, logs/*.exit, logs/run_631.log)
Both continuations start at once; each one's two refines start as soon as its continuation has landed. Commands, from the worktree's solver/matter:
  python -u sigdss_run.py cont i631a data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy --par eps --start 0.2 --end 0.142857142857 --targets 0.142857142857 --D 4 --kc 15 --kappa 0.5
  python -u sigdss_run.py cont i631b data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy --par eps --start 0.1 --end 0.0714285714286 --targets 0.0714285714286 --D 4 --kc 15 --kappa 0.5
  python -u sigdss_run.py refine data/sigdss_sol_i631{a,b}_D4.0000_eta{7,14}.0000.npy --D 4 --eps {0.142857142857,0.0714285714286} --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i631_kc{23,39}_eta{7,14}"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CWD = r"C:\Users\nathan\Source\choptuik-i623\solver\matter"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
# letter, eta label, seed, eps start, eps target
CASES = [("a", "7", "data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy", "0.2", "0.142857142857"),
         ("b", "14", "data/sigdss_sol_i623seed_D4.0000_eta10.0000.npy", "0.1", "0.0714285714286")]


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_631.log"), "a").write(line + "\n")


def start(name, args):
    p = subprocess.Popen([PY, "-u", "sigdss_run.py"] + args, cwd=CWD, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT,
                         env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid})")
    return [p, name, time.time()]


running = []
pending = {}
for letter, eta, seed, e0, e1 in CASES:
    running.append(start(f"cont_{letter}_eta{eta}", ["cont", f"i631{letter}", seed, "--par", "eps", "--start", e0, "--end", e1, "--targets", e1, "--D", "4", "--kc", "15", "--kappa", "0.5"]))
    pending[f"cont_{letter}_eta{eta}"] = (letter, eta, e1)
failed = False
while running:
    for r in list(running):
        rc = r[0].poll()
        if rc is None:
            continue
        running.remove(r)
        open(os.path.join(HERE, "logs", f"{r[1]}.exit"), "w").write(f"{rc}\n")
        say(f"{r[1]} exit {rc} after {time.time() - r[2]:.0f} s")
        if r[1] in pending:
            letter, eta, e1 = pending[r[1]]
            seed = os.path.join(CWD, "data", f"sigdss_sol_i631{letter}_D4.0000_eta{eta}.0000.npy")
            if rc != 0 or not os.path.exists(seed):
                say(f"continuation {r[1]} did not produce the eta = {eta} point, its refines are not started")
                failed = True
                continue
            for kc in (23, 39):
                running.append(start(f"kc{kc}_eta{eta}", ["refine", f"data/sigdss_sol_i631{letter}_D4.0000_eta{eta}.0000.npy", "--D", "4", "--eps", e1, "--kc_seed", "15", "--kc", str(kc),
                                                          "--kappa", "0.5", "--tag", f"i631_kc{kc}_eta{eta}"]))
    time.sleep(5)
say("all done" + (" (a continuation failed)" if failed else ""))
sys.exit(1 if failed else 0)
