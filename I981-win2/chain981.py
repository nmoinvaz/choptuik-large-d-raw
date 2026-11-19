"""#981: Job A (xi1 0.14) at INNER_NB_RTOL=1e-14 with --h3=1e-4, then with --h3=1e-5, one at a time, 3 h cap each, BelowNormal,
perturbed repeats (seed 976, 1e-7, up to 3 per solve). Exits go to exits_981.txt.   python chain981.py   (from this folder)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
for h3, tag in (("1e-4", "rtol14_h3e4_xi014"), ("1e-5", "rtol14_h3e5_xi014")):
    env = dict(os.environ, INNER_NB_RTOL="1e-14", RUN_H3=h3, RUN_RNGSEED="976")
    t0 = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start h3 {h3} ({tag})", flush=True)
    rc = subprocess.run([sys.executable, "-u", "run_job981.py", "0.14", tag, "--cap_h", "3"], cwd=HERE, env=env,
                        creationflags=BELOW_NORMAL).returncode
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC h3 {h3} ({tag}) exit {rc} after {time.time() - t0:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits_981.txt"), "a") as f:
        f.write(line + "\n")
