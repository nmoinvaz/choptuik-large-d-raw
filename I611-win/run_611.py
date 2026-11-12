#!/usr/bin/env python3
"""#611: hp's quad-double polishes (hp/scan_qd.py) with and without the kf 13 cut, two at a time, 3 threads each, BelowNormal.
usage: python run_611.py          (from this folder; logs/<tag>.stdout and .exit, records qd_<tag>.jsonl and the saved states <tag>_D<D>.npz here)
Each job: python -u scan_qd.py RAW/I611-win/qd_<tag>.jsonl STATE.npz D_END --kfreeze K --threads 3 --tag <tag>, from the worktree's hp/."""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HP = r"C:\Users\nathan\Source\choptuik-i611\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
JOBS = []
for tagd, state, D in (("D50", "up8_D50.0075", "50.007491"), ("D60", "up13_D60.0020", "60.001952"), ("D54a", "up10_D55.0351", "54.996085"), ("D54b", "up10_D54.0414", "54.996085")):
    for kname, K in (("kf13", "13"), ("kfm1", "-1")):
        JOBS.append((f"{kname}_{tagd}", state, D, K))
NPROC = 2
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
running = []
t_all = time.time()
while JOBS or running:
    for p in list(running):
        rc = p[0].poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{p[1]}.exit"), "w").write(f"{rc}\n")
            print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC {p[1]} exit {rc} after {time.time() - p[2]:.0f} s", flush=True)
            running.remove(p)
    while JOBS and len(running) < NPROC:
        tag, state, D, K = JOBS.pop(0)
        cmd = [PY, "-u", "scan_qd.py", os.path.join(HERE, f"qd_{tag}.jsonl"), os.path.join("data", "states", state + ".npz"), D, "--kfreeze", K, "--threads", "3", "--tag", tag]
        proc = subprocess.Popen(cmd, cwd=HP, stdout=open(os.path.join(HERE, "logs", f"{tag}.stdout"), "w"), stderr=subprocess.STDOUT,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), creationflags=0x00004000 | 0x08000000)
        running.append((proc, tag, time.time()))
        print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC start {tag} {state} -> D {D} kf {K}", flush=True)
    time.sleep(5)
print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC all done after {time.time() - t_all:.0f} s", flush=True)
