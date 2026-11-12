#!/usr/bin/env python3
"""#404: run the RT prototype's solves of one D, four at a time as separate processes (one thread each, BelowNormal).
usage: python run_queue_404.py D60.0020|D54.9961|D50.0075|D40.0201 [--nproc 4] [--grids 99,103,...]
Jobs in this order: for N in the ladder, start a then start b (so both roots of a grid finish together). A job whose exit file says 0 and whose jsonl has a converged record at this D is skipped (resume).
A solve past --cap seconds (default 14400) is killed and its exit file says 'timeout'. Logs: logs/<tag>_<D>.stdout and .exit; states and records in roots/ (rt_run.py's --out)."""
import argparse
import json
import os
import subprocess
import sys
import time

RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw"
REPO = r"C:\Users\nathan\Source\choptuik-i404"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
HERE = os.path.join(RAW, "I404-win")
OUT, LOG = os.path.join(HERE, "roots"), os.path.join(HERE, "logs")
NTOL = {"D60.0020": "1e-36", "D54.9961": "1e-38", "D50.0075": "1e-40", "D40.0201": "1e-40"}
DVAL = {"D60.0020": 60.001952, "D54.9961": 54.996085, "D50.0075": 50.007491, "D40.0201": 40.020065}
OPTS = "--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4".split()
BELOW_NORMAL, NO_WINDOW = 0x00004000, 0x08000000


def start_of(s, dtag):
    if s == "a":
        return os.path.join(RAW, "I145-mac", "cont", f"cont_32x101_{dtag}_32x101.npz"), "a101"
    return os.path.join(RAW, "I145-mac", "fol", f"fol_32x121_{dtag}_32x121.npz"), "b121"


def done(tag, N, dtag):
    # rt_run.py exits 1 when |Delta_RT - Delta_hp| > --tol (1e-12): that is the quantity under study, not a failure of the solve; done = a converged record at this D in the jsonl
    jl = os.path.join(OUT, f"{tag}_32x{N}.jsonl")
    if not os.path.exists(jl):
        return False
    for ln in open(jl):
        r = json.loads(ln)
        if r.get("solver") == "mp" and r.get("ok") and abs(r["D"] - DVAL[dtag]) < 1e-5:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dtag", choices=list(NTOL))
    ap.add_argument("--nproc", type=int, default=4)
    ap.add_argument("--grids", default="99,103,107,111,115,119,123")
    ap.add_argument("--cap", type=float, default=14400.0)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(LOG, exist_ok=True)
    jobs = [(s, int(N)) for N in a.grids.split(",") for s in "ab"]
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    running = []
    t_all = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC queue {a.dtag}: {len(jobs)} jobs, {a.nproc} at once", flush=True)
    while jobs or running:
        for p in list(running):
            proc, s, N, t0, ex = p
            rc = proc.poll()
            if rc is None and time.time() - t0 > a.cap:
                subprocess.call(["taskkill", "/T", "/F", "/PID", str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                rc = "timeout"
            if rc is not None:
                open(ex, "w").write(f"{rc}\n")
                print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC {s}{N} {a.dtag} exit {rc} after {time.time() - t0:.0f} s", flush=True)
                running.remove(p)
        while jobs and len(running) < a.nproc:
            s, N = jobs.pop(0)
            st, tag = start_of(s, a.dtag)
            if done(tag, N, a.dtag):
                print(f"skip {tag}_32x{N} {a.dtag} (done)", flush=True)
                continue
            out = open(os.path.join(LOG, f"{tag}_32x{N}_{a.dtag}.stdout"), "w")
            cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(REPO, "solver", "rt", "rt_run.py"), "--start", st, "--grids", f"32x{N}", *OPTS, "--newton_tol", NTOL[a.dtag], "--out", OUT, "--tag", f"{tag}_32x{N}"]
            proc = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=out, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NO_WINDOW)
            running.append((proc, s, N, time.time(), os.path.join(LOG, f"{tag}_32x{N}_{a.dtag}.exit")))
            print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC start {tag}_32x{N} {a.dtag} pid {proc.pid}", flush=True)
        time.sleep(10)
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC queue {a.dtag} done after {time.time() - t_all:.0f} s", flush=True)


if __name__ == "__main__":
    main()
