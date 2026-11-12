#!/usr/bin/env python3
"""#404: after the D 54.996085 queue (logs/queue_D54.9961.exit appears), run the D 50.007491 queue and then the D 40.020065 queue, each with run_queue_404.py (four solves at once).
usage: python chain_404.py      (started from this folder; logs/queue_D50.0075.stdout and .exit, logs/queue_D40.0201.stdout and .exit)"""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
while not os.path.exists(os.path.join(HERE, "logs", "queue_D54.9961.exit")):
    time.sleep(30)
for d in ("D50.0075", "D40.0201"):
    with open(os.path.join(HERE, "logs", f"queue_{d}.stdout"), "w") as out:
        rc = subprocess.call([PY, "-u", os.path.join(HERE, "run_queue_404.py"), d, "--nproc", "4"], cwd=HERE, stdout=out, stderr=subprocess.STDOUT, creationflags=0x00004000 | 0x08000000)
    open(os.path.join(HERE, "logs", f"queue_{d}.exit"), "w").write(f"{rc}\n")
    print(time.strftime("%H:%M:%S", time.gmtime()), "UTC", d, "queue ended", rc, flush=True)
