"""#977: two runs of #976's driver, one at a time, 3 h cap each, BelowNormal, Job 0 (xi1 0.15) at --procs 2 (the driver's S):
   1. INNER_NB_RTOL=1e-14, perturbation seed 977  (tag rtol14_s977_xi015)
   2. INNER_NB_RTOL=1e-13, perturbation seed 976  (tag rtol13_s976_xi015)
The driver is #976's run_job976.py unchanged (its driver log is named run976_<tag>.driver.log). Exits go to exits_977.txt.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
for rtol, seed, tag in (("1e-14", "977", "rtol14_s977_xi015"), ("1e-13", "976", "rtol13_s976_xi015")):
    env = dict(os.environ, INNER_NB_RTOL=rtol, RUN_RNGSEED=seed)
    t0 = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start rtol {rtol} seed {seed} ({tag})", flush=True)
    rc = subprocess.run([sys.executable, "-u", "run_job976.py", "0.15", tag, "--cap_h", "3"], cwd=HERE, env=env,
                        creationflags=BELOW_NORMAL).returncode
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC rtol {rtol} seed {seed} ({tag}) exit {rc} after {time.time() - t0:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits_977.txt"), "a") as f:
        f.write(line + "\n")
