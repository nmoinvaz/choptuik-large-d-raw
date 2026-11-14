#!/usr/bin/env python3
"""#751: the octo-double polish (anm_run.py --steps 0, the base polish alone) of cont3's D 99.875 state with one plan node shifted by +1e-3.
usage: python run_751.py NA NB NC ND NE NF      (in order; logs/<name>.log, logs/<name>.exit, logs/run_751.log, output in <name>/base_pin13_D99.8750.npz)
       python run_751.py R_<X>                  (the repeat of node X from A1's arrays, after make_repro_751.py <X>)
Starts: states/N<X>_seg<i>_<j>_shift1e-3.npz (make_shifts_751.py); the repeat's: states/R_<X>.npz.
Threads: the number in threads.txt (default 2), read before each job, so it can be raised to 4 when #742 ends.
Each job: python -u anm_run.py RAW OUT --state S --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --reseed_o 3 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --h_max 0.0625 --a0 0.0625 --steps 0 --elim_switch 0 --save_base 1 --threads T, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal. Each job is capped at 2400 s."""
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i710\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
FLAGS = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "od", "--tol_od", "1e-60", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
         "--reseed", "2", "--reseed_q", "1", "--reseed_o", "3", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04",
         "--h_max", "0.0625", "--a0", "0.0625", "--steps", "0", "--elim_switch", "0", "--save_base", "1"]
CAP = 2400
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def threads():
    try:
        t = open(os.path.join(HERE, "threads.txt")).read().strip()
        return t if t.isdigit() and 1 <= int(t) <= 6 else "2"
    except OSError:
        return "2"


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_751.log"), "a").write(line + "\n")


for name in sys.argv[1:]:
    pat = f"N{name[1:]}_seg*_shift1e-3.npz" if name.startswith("N") else f"{name}.npz"
    found = glob.glob(os.path.join(HERE, "states", pat))
    if len(found) != 1:
        raise SystemExit(f"{name}: expected one state matching {pat}, found {found}")
    state = "I751-win/states/" + os.path.basename(found[0])
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    th = threads()
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, "--threads", th]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}) from {state}, {th} threads")
    reason = None
    while p.poll() is None:
        time.sleep(5)
        if time.time() - t0 > CAP:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            reason = f"the {CAP} s cap"
            say(f"{name}: killed the tree, {reason}")
            break
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s" + (f" ({reason})" if reason else ""))
    if rc != 0 or reason:
        say(f"{name} did not finish by itself, stopping the driver")
        sys.exit(2)
say("done " + " ".join(sys.argv[1:]))
