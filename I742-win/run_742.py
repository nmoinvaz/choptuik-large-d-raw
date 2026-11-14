#!/usr/bin/env python3
"""#742: the full system from D 113 to 120 with the octo-double corrector, from I739-win/B/anm_pin13_D113.0000.npz (eight parts, M = 32).
usage: python run_742.py P                      (the pilot: one step a = 1 from D 113 to D 114, --save_base 1, so its base polish is the control (a))
       python run_742.py L [STATE [STEPS]]      (the chain: default STATE I742-win/P/anm_pin13_D114.0000.npz, default 6 steps; --h_max 1.0 --a0 1.0)
Each run: logs/<name>.log, logs/<name>.exit, logs/run_742.log, output in <name>/. The stop rule is anm_run's own (four refused attempts at one D, the first plus three halvings, then
"stopped: no convergence after three halvings"). Each run is capped (CAP seconds), the cap kills the tree and is logged.
Flags, #739's (#682's plus --elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3): --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
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
         "--reseed", "2", "--reseed_q", "1", "--reseed_o", "3", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04", "--elim_switch", "0"]
START = "I739-win/B/anm_pin13_D113.0000.npz"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_742.log"), "a").write(line + "\n")


name = sys.argv[1]
if name == "P":
    state, extra, cap = START, ["--steps", "1", "--h_max", "1.0", "--a0", "1.0", "--save_base", "1"], 7200
elif name == "L":
    state = sys.argv[2] if len(sys.argv) > 2 else "I742-win/P/anm_pin13_D114.0000.npz"
    steps = sys.argv[3] if len(sys.argv) > 3 else "6"
    extra, cap = ["--steps", steps, "--h_max", "1.0", "--a0", "1.0"], 18000
else:
    raise SystemExit("name is P or L")
out = os.path.join(HERE, name)
os.makedirs(out, exist_ok=True)
cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", state, *FLAGS, *extra, "--threads", "4"]
t0 = time.time()
p = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{name}.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
say(f"start {name} (pid {p.pid}) from {state}: {' '.join(extra)}")
reason = None
while p.poll() is None:
    time.sleep(5)
    if time.time() - t0 > cap:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        reason = f"the {cap} s cap"
        say(f"{name}: killed the tree, {reason}")
        break
rc = p.wait()
open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
say(f"{name} exit {rc} after {time.time() - t0:.0f} s" + (f" ({reason})" if reason else ""))
sys.exit(0 if rc == 0 and not reason else 2)
