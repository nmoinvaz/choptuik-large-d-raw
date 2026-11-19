"""#1007 control run: #999's 0.11/0.105 command (the old log's own XI) from the new commit ec7cfea7 at --verbose=3, stopped (its own process tree, by pid)
when the first `level 5 (low): stop at` line appears, so that control1007.py can compare the lines before it with #999's log (efad7afd).
    python control_run1007.py            writes logs/hier_nb_M9_polish5_0.11_approach5_0.105_v3_ctrl_win2.log (truncated on purpose; a 3 min cap)"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
log = os.path.join(HERE, "logs", "hier_nb_M9_polish5_0.11_approach5_0.105_v3_ctrl_win2.log")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
cmd = ["C:/Users/nathan/Source/venv-i962/Scripts/python.exe", "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur",
       "--predict", "--procs", "2", "--h3=1e-4", "--verbose=3", "--approach=5:0.105", "--polish=5:0.11"]
env = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
f = open(log, "w", encoding="utf-8", newline="\n")
p = subprocess.Popen(cmd, cwd=SRC, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x4000 | 0x200)
print(time.strftime("%H:%M:%S UTC", time.gmtime()), "started pid", p.pid, flush=True)
t0 = time.time(); why = "cap"
while time.time() - t0 < 600:
    time.sleep(2)
    if "level 5 (low): stop at" in open(log, encoding="utf-8", errors="replace").read():
        why = "first level 5 (low) stop line"; break
    if p.poll() is not None:
        why = f"exited {p.returncode}"; break
time.sleep(1)                                                   # let the line be flushed, then stop the run's tree
subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
print(time.strftime("%H:%M:%S UTC", time.gmtime()), f"stopped ({why}) after {time.time() - t0:.0f} s, taskkill /T /F /PID {p.pid}", flush=True)
