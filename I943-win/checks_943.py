#!/usr/bin/env python3
"""#943 (win): the two planted checks of rt_sigma.py before the runs (command 1 of the plan), at BelowNormal with 2 BLAS threads, from solver/rt of the worktree.
`rt_sigma.py --planted` must exit 0 (best bound 1.4103e-21 in #701's and #721's runs) and `rt_sigma.py --planted --mutate=shift` must exit 1 (1.4244e-19, FAIL).
usage: python checks_943.py      (logs/planted.log, logs/planted_mutate_shift.log, logs/planted.exit, logs/planted_mutate_shift.exit)
The exit code is 0 if the first exited 0 and the second exited 1, and 1 otherwise."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i943"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
ENV = dict(os.environ, OPENBLAS_NUM_THREADS="2", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", PYTHONDONTWRITEBYTECODE="1")


def run(tag, extra):
    cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(RT, "rt_sigma.py"), "--planted"] + extra
    with open(os.path.join(HERE, "logs", f"{tag}.log"), "w") as f:
        rc = subprocess.run(cmd, cwd=RT, stdout=f, stderr=subprocess.STDOUT, env=ENV, creationflags=0x00004000 | 0x08000000).returncode
    open(os.path.join(HERE, "logs", f"{tag}.exit"), "w").write(f"{rc}\n")
    return rc


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    a = run("planted", [])
    b = run("planted_mutate_shift", ["--mutate=shift"])
    print(f"--planted exit {a} (want 0), --planted --mutate=shift exit {b} (want 1)")
    sys.exit(0 if (a == 0 and b == 1) else 1)
