#!/usr/bin/env python3
"""#642: hp/release_held.py (full release, --kfreeze=13) on the planted control and the chain states D 74 to 79, one run at a time (--threads=4, OPENBLAS_NUM_THREADS=1, BelowNormal).
usage: python run_642.py control      the three planted-control runs on T81/conv_pin5_D73.0000_D73.000000.npz, each in its own subfolder (control_p0, control_p1e-10, control_p1e-10_it0)
       python run_642.py states       the six chain states T138-win2/chain/anm_pin3_D7X.0000.npz, X = 4 to 9, all into release.jsonl
Each job: python -u release_held.py OUT.jsonl STATE.npz --kfreeze=13 --threads=4 [--perturb=... --it_max=0], cwd = the worktree's hp/; stdout -> logs/<name>.log, exit code -> logs/<name>.exit,
start and exit times and wall seconds -> logs/run_642.log. The states are read in place from the raw repository's stage checkout (origin/main)."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HP = r"C:\Users\nathan\Source\choptuik-i642\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
CONTROL = os.path.join(STAGE, "T81", "conv_pin5_D73.0000_D73.000000.npz")
if sys.argv[1] == "control":
    jobs = [("control_p0", os.path.join(HERE, "control_p0", "release.jsonl"), CONTROL, ["--perturb=0"]),
            ("control_p1e-10", os.path.join(HERE, "control_p1e-10", "release.jsonl"), CONTROL, ["--perturb=1e-10"]),
            ("control_p1e-10_it0", os.path.join(HERE, "control_p1e-10_it0", "release.jsonl"), CONTROL, ["--perturb=1e-10", "--it_max=0"])]
else:
    jobs = [(f"D7{x}", os.path.join(HERE, "release.jsonl"), os.path.join(STAGE, "T138-win2", "chain", f"anm_pin3_D7{x}.0000.npz"), []) for x in range(4, 10)]


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_642.log"), "a").write(line + "\n")


for name, out, state, extra in jobs:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = [PY, "-u", "release_held.py", out, state, "--kfreeze=13", "--threads=4"] + extra
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}): {' '.join(cmd[3:])}")
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s")
say(f"{sys.argv[1]} done")
