#!/usr/bin/env python3
"""#633: sigma-model at eta = 6 and 8.5, D = 4: the k_c 15 continuations (6 from #631's eta = 5 seed, 8.5 from #631's eta = 7 solution), then the refines to k_c 23 and 39.
usage: python run_633.py          (BelowNormal, OPENBLAS_NUM_THREADS=1, one thread per process, at most 4 busy; logs/*.log, logs/*.exit, logs/run_633.log)
Both continuations start at once; each one's two refines start as soon as its continuation has landed. Commands, from the worktree's solver/matter:
  python -u sigdss_run.py cont i633a data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy --par eps --start 0.2 --end 0.166666666667 --targets 0.166666666667 --D 4 --kc 15 --kappa 0.5
  python -u sigdss_run.py cont i633b data/sigdss_sol_i631a_D4.0000_eta7.0000.npy --par eps --start 0.142857142857 --end 0.117647058824 --targets 0.117647058824 --D 4 --kc 15 --kappa 0.5
  python -u sigdss_run.py refine data/sigdss_sol_i633{a,b}_D4.0000_eta{6.0000,8.5000}.npy --D 4 --eps {0.166666666667,0.117647058824} --kc_seed 15 --kc {23,39} --kappa 0.5 --tag i633_kc{23,39}_eta{6,8.5}"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CWD = r"C:\Users\nathan\Source\choptuik-i623\solver\matter"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
# letter, eta label, eta in file names, seed, eps start, eps target
CASES = [("a", "6", "6.0000", "data/sigdss_sol_i623seed_D4.0000_eta5.0000.npy", "0.2", "0.166666666667"),
         ("b", "8.5", "8.5000", "data/sigdss_sol_i631a_D4.0000_eta7.0000.npy", "0.142857142857", "0.117647058824")]


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_633.log"), "a").write(line + "\n")


def start(name, args):
    p = subprocess.Popen([PY, "-u", "sigdss_run.py"] + args, cwd=CWD, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT,
                         env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid})")
    return [p, name, time.time()]


running = []
pending = {}
for letter, eta, efile, seed, e0, e1 in CASES:
    name = f"cont_{letter}_eta{eta}"
    running.append(start(name, ["cont", f"i633{letter}", seed, "--par", "eps", "--start", e0, "--end", e1, "--targets", e1, "--D", "4", "--kc", "15", "--kappa", "0.5"]))
    pending[name] = (letter, eta, efile, e1)
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
            letter, eta, efile, e1 = pending[r[1]]
            rel = f"data/sigdss_sol_i633{letter}_D4.0000_eta{efile}.npy"
            if rc != 0 or not os.path.exists(os.path.join(CWD, rel)):
                say(f"continuation {r[1]} did not produce the eta = {eta} point ({rel}), its refines are not started")
                failed = True
                continue
            for kc in (23, 39):
                running.append(start(f"kc{kc}_eta{eta}", ["refine", rel, "--D", "4", "--eps", e1, "--kc_seed", "15", "--kc", str(kc), "--kappa", "0.5", "--tag", f"i633_kc{kc}_eta{eta}"]))
    time.sleep(5)
say("all done" + (" (a continuation failed)" if failed else ""))
sys.exit(1 if failed else 0)
