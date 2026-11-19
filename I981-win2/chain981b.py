"""#981 run 2 only, from the runner's own worktree D:/choptuik-inner (main 5e603e30), after the coordinator's rule not to run from
D:\choptuik-i962 (win2b's ks_chain2 uses it). INNER_NB_RTOL=1e-14, --h3=1e-5, perturbed repeats (seed 976, 1e-7, up to 3), 3 h cap,
BelowNormal. Exit goes to exits_981.txt.   python chain981b.py   (from this folder)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
h3, tag = "1e-5", "rtol14_h3e5_xi014"
env = dict(os.environ, INNER_NB_RTOL="1e-14", RUN_H3=h3, RUN_RNGSEED="976", RUN_SRC="D:/choptuik-inner/solver/inner_stokes")
t0 = time.time()
print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start h3 {h3} ({tag}) from D:/choptuik-inner", flush=True)
rc = subprocess.run([sys.executable, "-u", "run_job981.py", "0.14", tag, "--cap_h", "3"], cwd=HERE, env=env,
                    creationflags=BELOW_NORMAL).returncode
line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC h3 {h3} ({tag}) from D:/choptuik-inner exit {rc} after {time.time() - t0:.0f} s"
print(line, flush=True)
with open(os.path.join(HERE, "exits_981.txt"), "a") as f:
    f.write(line + "\n")
