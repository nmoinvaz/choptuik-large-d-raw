#!/usr/bin/env python3
"""#404: rt_roots.py (planted check and pair test) on each pair of roots at one D, and the controls at D 60.
usage: python run_fit_404.py D60.0020 [--controls N] [--nproc 4]       (run from this folder)
Logs: fit/roots_32xN_<D>.log (exit code on its last line); controls: fit/control_roots_mid_32xN_<D>.log (rt_roots.py --mutate=mid, must exit 1), fit/control_grids_shift_32xN_<D>.log
(rt_grids.py --mutate=shift on the grid's two roots, must exit 1, at --tol 1e-11 so that the unmutated check, control_grids_plain_*, passes: at 1e-14 or 1e-12 the best grid itself fails and the mutation could not be told from it)."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
REPO = r"C:\Users\nathan\Source\choptuik-i404"
DVAL = {"D60.0020": "60.001952", "D54.9961": "54.996085", "D50.0075": "50.007491", "D40.0201": "40.020065"}
LADDER = (99, 103, 107, 111, 115, 119, 123)
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")


def job(name, args, log):
    return dict(name=name, cmd=[PY, os.path.join(HERE, "rt_launch.py"), *args], log=os.path.join(HERE, "fit", log))


def main():
    dtag = sys.argv[1]
    nproc = int(sys.argv[sys.argv.index("--nproc") + 1]) if "--nproc" in sys.argv else 4
    ctl = int(sys.argv[sys.argv.index("--controls") + 1]) if "--controls" in sys.argv else None
    os.makedirs(os.path.join(HERE, "fit"), exist_ok=True)
    npz = lambda t, N: os.path.join("roots", f"{t}_32x{N}_{dtag}_32x{N}.npz")
    jobs = []
    if ctl is None:
        for N in LADDER:
            jobs.append(job(f"roots {N}", [os.path.join(REPO, "solver", "rt", "rt_roots.py"), npz("a101", N), npz("b121", N)], f"roots_32x{N}_{dtag}.log"))
    else:
        jobs.append(job(f"control mid {ctl}", [os.path.join(REPO, "solver", "rt", "rt_roots.py"), npz("a101", ctl), npz("b121", ctl), "--mutate=mid"], f"control_roots_mid_32x{ctl}_{dtag}.log"))
        jobs.append(job(f"control same {ctl}", [os.path.join(REPO, "solver", "rt", "rt_roots.py"), npz("a101", ctl), npz("b121", ctl), "--mutate=same"], f"control_roots_same_32x{ctl}_{dtag}.log"))
        jobs.append(job(f"control shift {ctl}", [os.path.join(REPO, "solver", "rt", "rt_grids.py"), os.path.join("roots", f"a101_32x{ctl}.jsonl"), os.path.join("roots", f"b121_32x{ctl}.jsonl"),
                                                 "--D", DVAL[dtag], "--tol", "1e-11", "--mutate=shift"], f"control_grids_shift_32x{ctl}_{dtag}.log"))
        jobs.append(job(f"grids unmutated {ctl}", [os.path.join(REPO, "solver", "rt", "rt_grids.py"), os.path.join("roots", f"a101_32x{ctl}.jsonl"), os.path.join("roots", f"b121_32x{ctl}.jsonl"),
                                                   "--D", DVAL[dtag], "--tol", "1e-11"], f"control_grids_plain_32x{ctl}_{dtag}.log"))
    running = []
    while jobs or running:
        for p in list(running):
            rc = p["proc"].poll()
            if rc is not None:
                with open(p["log"], "a", encoding="utf-8") as f:
                    f.write(f"\nexit {rc}\n")
                print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC {p['name']} exit {rc} after {time.time() - p['t0']:.0f} s", flush=True)
                running.remove(p)
        while jobs and len(running) < nproc:
            j = jobs.pop(0)
            j["proc"] = subprocess.Popen(j["cmd"], cwd=HERE, env=ENV, stdout=open(j["log"], "w", encoding="utf-8"), stderr=subprocess.STDOUT)
            j["t0"] = time.time()
            running.append(j)
        time.sleep(3)


if __name__ == "__main__":
    main()
