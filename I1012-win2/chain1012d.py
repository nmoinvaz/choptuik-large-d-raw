"""#1012 stage 4 (the coordinator's hc, 2026-11-19 ~09:00 UTC): XI 0.11, AP 0.105 at INNER_NB_RTOL=1e-13 with --h5=1e-4 --h7=1e-4 --h9=1e-4 (levels 5, 7 and 9 all at 100 x hier's
default finite-difference step), from the extract D:/choptuik-h9b of main 299c4eb9 (the worktree D:/choptuik-inner stays under the live runs). One run, BelowNormal, 3 h cap (its whole
process tree killed at the cap).

    python chain1012d.py [--selftest [--mutate=nokill|anysolve]]         (from this folder)

Command: hier_nb.py 9 2.719219 1.000022 --x=... --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=1e-4 --h7=1e-4 --h9=1e-4 --floor_max=1e-4 --verbose=2
--approach=5:0.105 --polish=5:0.11.   Log logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5h7h91e-4_win2.log, .exit file, driver log logs/run1012d.driver.log.
The driver logs every level-5 solve's end and a level-5 solve below 1e-6 (any solve counts as the success of #1012). The selftest and its mutations are as chain1012c.py's: a stub prints a
first solve of 6.0 and a later one of 5e-7, one success notice must appear, no process may be left; --mutate=anysolve and --mutate=nokill must fail.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-h9b/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF = "--selftest-inner" in sys.argv
CAP = 3.0 if SELF else 10800.0
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run1012d.selftest.driver.log" if SELF else "run1012d.driver.log"), "a")
TAG = "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5h7h91e-4_win2" + ("_selftest" if SELF else "")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def level5_solves(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [float(x) for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]


def main():
    if SELF:
        cmd = [PY, "-c", "import time\nprint('   level 5 solved: |r_5| 6.0e+00', flush=True)\ntime.sleep(1)\nprint('   level 5 solved: |r_5| 5.0e-07', flush=True)\ntime.sleep(60)"]
    else:
        cmd = [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict", "--procs", "2", "--h3=1e-4",
               "--h5=1e-4", "--h7=1e-4", "--h9=1e-4", "--floor_max=1e-4", "--verbose=2", "--approach=5:0.105", "--polish=5:0.11"]
    f = open(os.path.join(LOGS, TAG + ".log"), "w", encoding="utf-8", newline="\n")
    p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
    t0, seen = time.time(), 0
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s, RUN_SRC {SRC}; start pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{TAG}.log")
    while True:
        time.sleep(0.5 if SELF else 10)
        sol = level5_solves(os.path.join(LOGS, TAG + ".log"))
        while seen < len(sol):
            v = sol[seen]
            seen += 1
            if v < 1e-6 and not ("--mutate=anysolve" in sys.argv and seen > 1):
                say(f"level-5 solve {seen} ended below 1e-6 ({v:.2e}): the success case of #1012 (the run goes on within the cap)")
            else:
                say(f"level-5 solve {seen} ended at {v:.2e}")
        rc, note = p.poll(), ""
        if rc is None and time.time() - t0 > CAP:
            if "--mutate=nokill" not in sys.argv:
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                p.wait()
            rc, note = "capped", f" (killed the process tree at the {CAP:g} s cap, taskkill /T /F /PID {p.pid})"
        if rc is not None:
            f.close()
            msg = f"exit {rc}{note} after {time.time() - t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
            open(os.path.join(LOGS, TAG + ".exit"), "w").write(msg + "\n")
            say(msg)
            return p.pid


def selftest():
    try:
        os.remove(os.path.join(LOGS, "run1012d.selftest.driver.log"))
    except OSError:
        pass
    subprocess.run([sys.executable, os.path.abspath(__file__), "--selftest-inner"] + [a for a in sys.argv if a.startswith("--mutate=")], capture_output=True, text=True)
    log = open(os.path.join(LOGS, "run1012d.selftest.driver.log"), encoding="utf-8").read()
    pids = [int(x) for x in re.findall(r"start pid (\d+):", log)]
    alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
    n_notice = log.count("ended below 1e-6")
    ok = not alive and n_notice == 1 and "solve 1 ended at 6.00e+00" in log
    print(f"success notices {n_notice} (want 1), first solve logged {'solve 1 ended at 6.00e+00' in log}, alive after the cap {alive} -> selftest {'PASS' if ok else 'FAIL'}", flush=True)
    for fn in os.listdir(LOGS):
        if fn.endswith("_selftest.log") or fn.endswith("_selftest.exit"):
            try:
                os.remove(os.path.join(LOGS, fn))
            except OSError:
                pass
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
    sys.exit(0)
