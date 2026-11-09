#!/usr/bin/env python3
"""I243-mac: run reeval.py on several counts in turn.  python3 run_batch.py HP_DIR NAME=CACHE_SRC ..."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
for arg in sys.argv[2:]:
    name, src = arg.split("=", 1)
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    t = time.time()
    with open(os.path.join(HERE, name, "count.log"), "w") as fo:
        r = subprocess.run([sys.executable, os.path.join(HERE, "reeval.py"), name, hp, src], stdout=fo,
                           stderr=subprocess.STDOUT)
    line = f"{name} exit {r.returncode} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, {time.time() - t:.0f} s"
    print(line, flush=True)
    with open(os.path.join(HERE, "exits.txt"), "a") as fo:
        fo.write(line + "\n")
