#!/usr/bin/env python3
"""#741: the octo-double polish (anm_run.py --steps 0, the base polish alone) of cont3's D 99.875 state with one plan node shifted.
usage: python run_741.py S0 S1 S2 S3 S4          (in order; logs/<name>.log, logs/<name>.exit, logs/run_741.log, output in <name>/base_pin13_D99.8750.npz)
       python run_741.py S5                      (only after fit_741.py --fit has written fit_741_out.txt)
Starts: states/<name>_shift<tag>.npz from make_shifts_741.py (cont3's arrays, one node of segs[3][1] shifted: S0 0, S1 1e-4, S2 3e-4, S3 1e-3, S4 3e-3, S5 1e-2).
Each job: python -u anm_run.py RAW OUT --state S --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --reseed_o 3 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --h_max 0.0625 --a0 0.0625 --steps 0 --elim_switch 0 --save_base 1 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal.
(#727's A1c flags: #682's with the corrector pair swapped, --reseed_o 3 and --save_base 1.) Each job is capped at 2400 s; the cap kills the tree and is logged."""
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
TAGS = {"S0": "0", "S1": "1e-4", "S2": "3e-4", "S3": "1e-3", "S4": "3e-3", "S5": "1e-2"}
CAP = 2400
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_741.log"), "a").write(line + "\n")


for name in sys.argv[1:]:
    if name == "S5" and not os.path.exists(os.path.join(HERE, "fit_741_out.txt")):
        raise SystemExit("S5 runs only after fit_741.py --fit has written fit_741_out.txt")
    state = f"I741-win/states/{name}_shift{TAGS[name]}.npz"
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, "--threads", "4"]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}) from {state}")
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
