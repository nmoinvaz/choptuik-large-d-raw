#!/usr/bin/env python3
"""I243-mac: run jobs in turn: reeval:NAME=CACHE_SRC (reeval.py) or offset:NAME (offset_check.py, log NAME/offset.log).

    python3 run_jobs.py HP_DIR JOB ..."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
for job in sys.argv[2:]:
    kind, rest = job.split(":", 1)
    t = time.time()
    if kind == "reeval":
        name, src = rest.split("=", 1)
        cmd, log = [sys.executable, os.path.join(HERE, "reeval.py"), name, hp, src], "count.log"
    else:
        name = rest
        cmd, log = [sys.executable, os.path.join(HERE, "offset_check.py"), name, hp], "offset.log"
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    with open(os.path.join(HERE, name, log), "w") as fo:
        r = subprocess.run(cmd, stdout=fo, stderr=subprocess.STDOUT, env=env)
    line = f"{kind} {name} exit {r.returncode} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, {time.time() - t:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits.txt"), "a") as fo:
        fo.write(line + "\n")
