"""Run a command and kill its process tree when a wall-clock cap is reached (#462's 24 h cap per chain, held by the
machine and not by a session).

    python3 run_capped.py CAP_SECONDS CMD [ARGS...]

stdout and stderr are the caller's (a .cmd redirects them to the chain's log). Exits with the command's code, or 124
when the cap killed it, after printing a `run_capped: cap ... reached` line."""
import shutil
import subprocess
import sys

cap, cmd = float(sys.argv[1]), sys.argv[2:]
# A bare "python.exe" would be searched first in the directory of the running image, which for a venv's launcher is the
# base interpreter's, so the command's first word is resolved against PATH here (the venv first, as the .cmd sets it).
cmd[0] = shutil.which(cmd[0]) or cmd[0]
p = subprocess.Popen(cmd)
try:
    rc = p.wait(timeout=cap)
except subprocess.TimeoutExpired:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"run_capped: cap of {cap:.0f} s reached, killed pid {p.pid}", flush=True)
    rc = 124
sys.exit(rc)
