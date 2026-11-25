#!/usr/bin/env python3
"""macm3b #1070: run a command under a wall-clock cap. SIGTERM at the cap, SIGKILL 60 s later; prints the child's pid, its exit code
and its wall time. Usage: capped_run.py CAP_SECONDS CMD ARGS..."""
import os, signal, subprocess, sys, time
cap = float(sys.argv[1]); t0 = time.time()
p = subprocess.Popen(sys.argv[2:])
print(f"capped_run: child pid {p.pid}, cap {cap:.0f} s", flush=True)
hit = False
while p.poll() is None:
    time.sleep(10)
    if not hit and time.time() - t0 > cap:
        hit = True; print(f"capped_run: cap reached after {time.time()-t0:.0f} s, SIGTERM to {p.pid}", flush=True); p.send_signal(signal.SIGTERM)
    if hit and time.time() - t0 > cap + 60:
        p.send_signal(signal.SIGKILL)
print(f"capped_run: exit {p.returncode} wall {time.time()-t0:.0f} s cap_hit {hit}", flush=True)
sys.exit(0 if p.returncode == 0 else (124 if hit else p.returncode))
