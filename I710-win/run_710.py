#!/usr/bin/env python3
"""#710: five anm_run.py runs of the full system (--kfreeze 13) with #682's flags, one at a time, A/B on --elim_switch 0.
usage: python run_710.py A0 A1 B0 B1 C          (names in the order to run; logs/<name>.log, logs/<name>.exit, logs/run_710.log, output in <name>/)
A0, A1: start I682-win/cont3/anm_pin13_D99.7500.npz, --h_max 0.125 --a0 0.125 --steps 1 (A1 adds --elim_switch 0)
B0, B1: start I682-win/cont3/anm_pin13_D99.9531.npz, --h_max 0.09765625 --a0 0.09765625 --steps 1 (B1 adds --elim_switch 0)
C: start I682-win/cont2/anm_pin13_D99.6250.npz, --h_max 1.0 --a0 0.5 --steps 6 --elim_switch 0
Gate (README): after A1, if its first attempt did not converge within 8 corrector steps the driver stops (exit 3) and the run is reported, as the issue says.
Each job: python -u anm_run.py RAW OUT --state S --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import re
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
A_ST, B_ST, C_ST = "I682-win/cont3/anm_pin13_D99.7500.npz", "I682-win/cont3/anm_pin13_D99.9531.npz", "I682-win/cont2/anm_pin13_D99.6250.npz"
JOBS = {
    "A0": (A_ST, ["--h_max", "0.125", "--a0", "0.125", "--steps", "1"]),
    "A1": (A_ST, ["--h_max", "0.125", "--a0", "0.125", "--steps", "1", "--elim_switch", "0"]),
    "B0": (B_ST, ["--h_max", "0.09765625", "--a0", "0.09765625", "--steps", "1"]),
    "B1": (B_ST, ["--h_max", "0.09765625", "--a0", "0.09765625", "--steps", "1", "--elim_switch", "0"]),
    "C": (C_ST, ["--h_max", "1.0", "--a0", "0.5", "--steps", "6", "--elim_switch", "0"]),
}
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_710.log"), "a").write(line + "\n")


def first_attempt_converged(path, it_max=8):
    """True if the first attempt (the block after the first re-seed line) says 'converged' in at most it_max steps."""
    seen = False
    for ln in open(path, encoding="utf-8", errors="replace"):
        if re.match(r"^    a [0-9.]+: re-seeded", ln):
            seen = True
        m = re.search(r"quad-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)", ln)
        if seen and m:
            return m.group(3) == "converged" and int(m.group(1)) <= it_max and float(m.group(2)) <= 1e-44
    return False


for name in sys.argv[1:]:
    state, extra = JOBS[name]
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, *extra, "--threads", "4"]
    log = os.path.join(HERE, "logs", f"{name}.log")
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}): {' '.join(extra)}")
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s")
    if rc != 0:
        say(f"{name} exited non-zero, stopping the driver")
        sys.exit(2)
    if name == "A1" and not first_attempt_converged(log):
        say("A1's first attempt did not converge to 1e-44 within 8 steps: the hypothesis is refuted, stopping the driver (README gate)")
        sys.exit(3)
say("done " + " ".join(sys.argv[1:]))
