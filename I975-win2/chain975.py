"""#975: Job 0 (xi1 0.15) then Job A (xi1 0.14), one at a time, INNER_NB_RTOL=1e-13, 3 h cap each, BelowNormal.

    python chain975.py          (run from this folder; exits are appended to exits_975.txt)
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BELOW_NORMAL = 0x00004000
env = dict(os.environ, INNER_NB_RTOL="1e-13")
for xi, tag in (("0.15", "rtol13_xi015"), ("0.14", "rtol13_xi014")):
    t0 = time.time()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC start job xi1 {xi} ({tag})", flush=True)
    rc = subprocess.run([sys.executable, "-u", "run_job.py", xi, tag, "--cap_h", "3"], cwd=HERE, env=env,
                        creationflags=BELOW_NORMAL).returncode
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC job xi1 {xi} ({tag}) exit {rc} after {time.time() - t0:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits_975.txt"), "a") as f:
        f.write(line + "\n")
