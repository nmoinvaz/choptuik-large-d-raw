#!/usr/bin/env python3
"""#611, second round: scan_qd.py with --predictor lagrange (the default 'auto' predictor, the tangent driver.tangent_q while fewer than 3 points are converged, raised
ValueError: singular or non-finite pivot at column 0 (NaN) in every D 54.996085 run with this venv's hpkernel: failed_tangent_predictor/). Starts are the saved quad-double states of the first round.
usage: python run_611b.py JOB [JOB ...]    JOB = tag:START.npz:D_END:K     (two at a time, 3 threads each, BelowNormal; logs/<tag>.stdout, .exit)"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HP = r"C:\Users\nathan\Source\choptuik-i611\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
jobs = [j.split(":", 3) for j in sys.argv[1:]]
nproc = 2
running = []
while jobs or running:
    for p in list(running):
        rc = p[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{p[1]}.exit"), "w").write(f"{rc}\n")
            print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC {p[1]} exit {rc} after {time.time() - p[2]:.0f} s", flush=True)
            running.remove(p)
    while jobs and len(running) < nproc:
        tag, start, D, K = jobs.pop(0)
        cmd = [PY, "-u", "scan_qd.py", os.path.join(HERE, f"qd_{tag}.jsonl"), os.path.join(HERE, start), D, "--kfreeze", K, "--threads", "3", "--tag", tag, "--predictor", "lagrange"]
        proc = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{tag}.stdout"), "w"), stderr=subprocess.STDOUT,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), creationflags=0x00004000 | 0x08000000)
        running.append((proc, tag, time.time()))
        print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC start {tag} {start} -> D {D} kf {K}", flush=True)
    time.sleep(5)
print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC all done", flush=True)
