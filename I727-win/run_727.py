#!/usr/bin/env python3
"""#727: anm_run.py --steps 0 (the base polish alone) of the three D 99.875 full-system states with #682's flags, --elim_switch 0 as #725 used it, --tol_qd 1e-60 --qd_it 12.
usage: python run_727.py chk          (the check on cont3 first: quad-double, saved nothing)
       python run_727.py pilot        (the common-plan polish, step 2: cont3's own state, octo-double; logs/<name>.log, logs/<name>.exit, logs/run_727.log, output in <name>/)
       python run_727.py A1c X2c      (step 3, only if the pilot passed: the states/ copies with cont3's plan)
The octo-double jobs use --corrector od --tol_od 1e-60 in place of --corrector qd --tol_qd 1e-60, and --save_base 1 (saves <name>/base_pin13_D99.8750.npz, eight parts).
chk and pilot: I682-win/cont3/anm_pin13_D99.8750.npz. A1c and X2c: I727-win/states/A1_on_cont3plan.npz and X2_on_cont3plan.npz (make_states_727.py).
Each job: python -u anm_run.py RAW OUT --state S --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --h_max 0.0625 --a0 0.0625 --steps 0 --elim_switch 0 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i710\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
FLAGS = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "qd", "--tol_qd", "1e-60", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
         "--reseed", "2", "--reseed_q", "1", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04"]
STEP = ["--h_max", "0.0625", "--a0", "0.0625", "--steps", "0", "--elim_switch", "0"]
JOBS = {"chk": "I682-win/cont3/anm_pin13_D99.8750.npz", "pilot": "I682-win/cont3/anm_pin13_D99.8750.npz",
        "A1c": "I727-win/states/A1_on_cont3plan.npz", "X2c": "I727-win/states/X2_on_cont3plan.npz"}


def flags_for(name):
    """the qd flags, or for the octo-double jobs the corrector pair swapped and --save_base 1 added"""
    if name == "chk":
        return FLAGS + STEP
    f = list(FLAGS)
    i = f.index("--corrector")
    f[i + 1] = "od"
    j = f.index("--tol_qd")
    f[j:j + 2] = ["--tol_od", "1e-60"]
    return f + STEP + ["--save_base", "1"]
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_727.log"), "a").write(line + "\n")


for name in sys.argv[1:]:
    state = JOBS[name]
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *flags_for(name), "--threads", "4"]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}) from {state}")
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s")
    if rc != 0:
        say(f"{name} exited non-zero, stopping the driver")
        sys.exit(2)
say("done " + " ".join(sys.argv[1:]))
