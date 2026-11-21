#!/usr/bin/env python3
"""development worker (not a result): builds ls1064's context once (the octo-double LU), then executes job_*.py files from the jobs/ directory in that process with `ctx` and `ls` (ls1064, reloaded per job) in scope,
writing each job's stdout to jobs/<job>.log; the job is renamed to <job>.done. A file jobs/STOP ends it. Usage: worker1064.py RAWDIR STATE KS KEEP_PLAN"""
import contextlib
import glob
import importlib
import os
import sys
import time
import traceback

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import ls1064  # noqa: E402

raw, st, ks, kp = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
os.makedirs(os.path.join(D, "jobs"), exist_ok=True)
ctx = ls1064.setup(raw, st, ks, kp, 4, 32)
print("worker ready", flush=True)
while True:
    if os.path.exists(os.path.join(D, "jobs", "STOP")):
        break
    for jf in sorted(glob.glob(os.path.join(D, "jobs", "job_*.py"))):
        lf = jf + ".log"
        with open(lf, "w") as fh, contextlib.redirect_stdout(fh):
            try:
                ls = importlib.reload(ls1064)
                exec(compile(open(jf).read(), jf, "exec"), {"ctx": ctx, "ls": ls, "mp": ls.mp, "np": ls.np, "time": time, "__name__": "job"})
            except BaseException:
                traceback.print_exc(file=fh)
            print("JOB DONE", flush=True)
        os.rename(jf, jf[:-3] + ".done.py")
    time.sleep(2)
print("worker stopped", flush=True)
