"""#965 stage 2: run one command at nice 10 with a wall-time cap; the whole process group is killed at the cap (hier.py's spawn workers
survive a kill of the main process). Usage: python3 run_cap.py CAP_H LOG EXITFILE -- CMD ... (env passes through). stdout and stderr go to LOG."""
import os, signal, subprocess, sys, time
cap, log, exitfile = float(sys.argv[1]), sys.argv[2], sys.argv[3]
cmd = sys.argv[sys.argv.index("--") + 1:]
t0 = time.time()
with open(log, "w") as f:
    p = subprocess.Popen(["nice", "-n", "10"] + cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    try:
        rc = p.wait(timeout=cap * 3600)
        note = ""
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); p.wait(); rc = "capped"; note = f" (killed the process group at the {cap:g} h cap)"
open(exitfile, "w").write(f"exit {rc}{note} after {time.time()-t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC\n")
