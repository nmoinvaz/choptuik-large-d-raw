"""#989 Jobs only (the control ran apart, see the README): Job A of #975 at xi1 0.145 and then at 0.155, one at a time, from the runner's
worktree D:/choptuik-inner (origin/main b081fbb2), INNER_NB_RTOL=1e-14, --h3=1e-4, perturbed repeats (seed 976, 1e-7, up to 3), 3 h cap
each, BelowNormal. Exits go to exits_989.txt.     python chain989b.py     (from this folder)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
env = dict(os.environ, INNER_NB_RTOL="1e-14", RUN_H3="1e-4", RUN_RNGSEED="976", RUN_SRC="D:/choptuik-inner/solver/inner_stokes",
           PYTHONDONTWRITEBYTECODE="1")
for xi, tag in (("0.145", "rtol14_xi0145"), ("0.155", "rtol14_xi0155")):
    t0 = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start Job A at xi1 {xi} ({tag})", flush=True)
    rc = subprocess.run([sys.executable, "-u", "run_job981.py", xi, tag, "--cap_h", "3"], cwd=HERE, env=env,
                        creationflags=BELOW_NORMAL).returncode
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC Job A at xi1 {xi} ({tag}) exit {rc} after {time.time() - t0:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits_989.txt"), "a") as f:
        f.write(line + "\n")
