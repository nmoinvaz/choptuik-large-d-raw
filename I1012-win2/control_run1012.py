"""#1012 plumbing control runs: #1011 run 1's command (XI 0.11, AP 0.105, --floor_max=1e-4, --verbose=2) with --h5=1e-6 and with --h5=1e-4, both at once, each stopped (its own
process tree, by pid) when its first `level 5 (low): stop at` line appears or after 600 s. Logs logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5<H5>_ctrl_win2.log
(truncated on purpose). Then control1012.py compares each with #1011 run 1's log (REF).     python control_run1012.py REF"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
env = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
jobs = {}
for h5 in ("1e-6", "1e-4"):
    log = os.path.join(HERE, "logs", f"hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5{h5}_ctrl_win2.log")
    cmd = ["C:/Users/nathan/Source/venv-i962/Scripts/python.exe", "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur",
           "--predict", "--procs", "2", "--h3=1e-4", f"--h5={h5}", "--floor_max=1e-4", "--verbose=2", "--approach=5:0.105", "--polish=5:0.11"]
    f = open(log, "w", encoding="utf-8", newline="\n")
    p = subprocess.Popen(cmd, cwd=SRC, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x4000 | 0x200)
    jobs[h5] = (p, f, log); print(time.strftime("%H:%M:%S UTC", time.gmtime()), "started --h5", h5, "pid", p.pid, flush=True)
t0 = time.time(); done = {}
while len(done) < 2 and time.time() - t0 < 600:
    time.sleep(2)
    for h5, (p, f, log) in jobs.items():
        if h5 not in done and ("level 5 (low): stop at" in open(log, encoding="utf-8", errors="replace").read() or p.poll() is not None):
            done[h5] = "stop line" if p.poll() is None else f"exited {p.returncode}"
time.sleep(1)
for h5, (p, f, log) in jobs.items():
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
    print(time.strftime("%H:%M:%S UTC", time.gmtime()), f"--h5 {h5}: stopped ({done.get(h5, 'cap')}) after {time.time() - t0:.0f} s, taskkill /T /F /PID {p.pid}", flush=True)
