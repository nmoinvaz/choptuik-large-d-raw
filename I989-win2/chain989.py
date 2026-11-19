"""#989: the control, then Job A of #975 at xi1 0.145 and at 0.155, one at a time, from the runner's worktree D:/choptuik-inner
(origin/main b081fbb2), INNER_NB_RTOL=1e-14, --h3=1e-4, perturbed repeats (seed 976, 1e-7, up to 3), 3 h cap each, BelowNormal.
The control (xi1 0.15 `zero` solve, must reproduce #976's log) stops the chain when it fails. Exits go to exits_989.txt.
    python chain989.py     (from this folder)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
env = dict(os.environ, INNER_NB_RTOL="1e-14", RUN_H3="1e-4", RUN_RNGSEED="976", RUN_SRC="D:/choptuik-inner/solver/inner_stokes",
           PYTHONDONTWRITEBYTECODE="1")


def step(label, args):
    t0 = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start {label}", flush=True)
    rc = subprocess.run([sys.executable, "-u"] + args, cwd=HERE, env=env, creationflags=BELOW_NORMAL).returncode
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {label} exit {rc} after {time.time() - t0:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits_989.txt"), "a") as f:
        f.write(line + "\n")
    return rc


if step("control (xi1 0.15 zero solve against #976's log)", ["control989.py"]) != 0:
    print("the control differs: the chain stops", flush=True)
    sys.exit(1)
for xi, tag in (("0.145", "rtol14_xi0145"), ("0.155", "rtol14_xi0155")):
    step(f"Job A at xi1 {xi} ({tag})", ["run_job981.py", xi, tag, "--cap_h", "3"])
