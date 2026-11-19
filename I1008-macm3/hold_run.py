#!/usr/bin/env python3
"""macm3b #1008: take over a running process whose capped_run.py wrapper was stopped (the cap raised in place, no restart).
Holds `caffeinate -is -w PID`, logs when PID ends, and sends SIGTERM (SIGKILL 60 s later) at DEADLINE (UTC, 'YYYY-MM-DD HH:MM:SS').
Usage: hold_run.py PID DEADLINE LOGFILE. A process that is not our child has no exit code here; its log says how it ended."""
import datetime, os, signal, subprocess, sys, time
pid = int(sys.argv[1]); deadline = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc); logf = sys.argv[3]
def log(s):
    with open(logf, "a") as f: f.write(f"1008m {s} {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
def alive():
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False
cf = subprocess.Popen(["caffeinate", "-is", "-w", str(pid)])
log(f"hold_run: holding pid {pid} (caffeinate -is -w, pid {cf.pid}), deadline {sys.argv[2]} UTC")
t0 = time.time(); hit = False
while alive():
    time.sleep(10)
    if not hit and datetime.datetime.now(datetime.timezone.utc) > deadline:
        hit = True; log(f"hold_run: deadline reached, SIGTERM to {pid}"); os.kill(pid, signal.SIGTERM); tk = time.time()
    if hit and time.time() - tk > 60 and alive(): os.kill(pid, signal.SIGKILL)
log(f"hold_run: pid {pid} ended after {time.time()-t0:.0f} s of holding, deadline_hit {hit}")
