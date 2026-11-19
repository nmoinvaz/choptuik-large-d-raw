"""#1012 stage 5 (the coordinator's hc, 2026-11-19 ~09:55 UTC): two runs side by side, from D:/choptuik-h9b (extract of main 299c4eb9), XI 0.11 / AP 0.105, INNER_NB_RTOL=1e-13,
BelowNormal, 3 h cap each (whole process tree killed at the cap):
  (a) --h5=3e-4 (h7, h9 default), to bracket the level-5 step (1e-3 gave 4.5e-2, 1e-4 gave 1.7e-2 at the first solve);
  (b) --h5=1e-4 WITHOUT --predict (--schur kept): tests whether the leakage Jacobian K that --predict uses for every nested re-solve keeps level 5's later solves at 1e-4..1e-3.

    python chain1012e.py [--selftest [--mutate=nokill|anysolve]]         (from this folder)

Command (a): hier_nb.py 9 2.719219 1.000022 --x=... --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=3e-4 --floor_max=1e-4 --verbose=2 --approach=5:0.105 --polish=5:0.11
Command (b): the same with --h5=1e-4 and without --predict.
Logs logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-4_win2.log and ..._h51e-4_nopredict_win2.log, .exit files, driver log logs/run1012e.driver.log. The driver logs every
level-5 solve's end and any solve below 1e-6 (any solve counts as the success of #1012), and checks each log's 'Jacobian K computed (N residuals)' line: N = 10 with --predict (M + 1),
N = 8 without it (M - 1); a log that disagrees is flagged as a plumbing failure.
--selftest runs two stubs (cap 3 s): stub 1 prints a first solve of 6.0 and a later one of 5e-7 and a K line with 10 residuals (a), stub 2 a K line with 10 residuals where (b) expects 8:
the driver must log exactly one success notice, exactly one K-line mismatch, and leave no process; --mutate=anysolve and --mutate=nokill must fail.
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
drv = open(os.path.join(LOGS, "run1012e.selftest.driver.log" if SELF else "run1012e.driver.log"), "a")
RUNS = [dict(name="a", suffix="h53e-4", h5="3e-4", predict=True), dict(name="b", suffix="h51e-4_nopredict", h5="1e-4", predict=False)]


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def command(r):
    c = [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur"] + (["--predict"] if r["predict"] else [])
    return c + ["--procs", "2", "--h3=1e-4", f"--h5={r['h5']}", "--floor_max=1e-4", "--verbose=2", "--approach=5:0.105", "--polish=5:0.11"]


def level5_solves(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [float(x) for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]


def k_residuals(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    m = re.search(r"Jacobian K computed \((\d+) residuals\)", t)
    return int(m.group(1)) if m else None


def main():
    runs = {}
    for r in RUNS:
        tag = f"hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_{r['suffix']}_win2" + ("_selftest" if SELF else "")
        if SELF:
            body = ["print('   level 5 solved: |r_5| 6.0e+00', flush=True)\nprint('   Jacobian K computed (10 residuals) [5 s]', flush=True)\ntime.sleep(1)\nprint('   level 5 solved: |r_5| 5.0e-07', flush=True)",
                    "print('   Jacobian K computed (10 residuals) [5 s]', flush=True)"][len(runs)]
            cmd = [PY, "-c", "import time\n" + body + "\ntime.sleep(60)"]
        else:
            cmd = command(r)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        runs[tag] = dict(p=p, f=f, t0=time.time(), r=r, seen=0, k=False)
        say(f"start ({r['name']}) --h5={r['h5']}{'' if r['predict'] else ' without --predict'} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
    while runs:
        time.sleep(0.5 if SELF else 10)
        for tag in list(runs):
            x = runs[tag]
            p, r = x["p"], x["r"]
            path = os.path.join(LOGS, tag + ".log")
            sol = level5_solves(path)
            while x["seen"] < len(sol):
                v = sol[x["seen"]]
                x["seen"] += 1
                if v < 1e-6 and not ("--mutate=anysolve" in sys.argv and x["seen"] > 1):
                    say(f"({r['name']}) level-5 solve {x['seen']} ended below 1e-6 ({v:.2e}): the success case of #1012 (the run goes on within the cap)")
                else:
                    say(f"({r['name']}) level-5 solve {x['seen']} ended at {v:.2e}")
            nk = k_residuals(path)
            if nk is not None and not x["k"]:
                x["k"] = True
                want = 10 if r["predict"] else 8
                say(f"({r['name']}) K line: {nk} residuals (want {want} {'with' if r['predict'] else 'without'} --predict): " + ("ok" if nk == want else "PLUMBING MISMATCH"))
            rc, note = p.poll(), ""
            if rc is None and time.time() - x["t0"] > CAP:
                if "--mutate=nokill" not in sys.argv:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {CAP:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                x["f"].close()
                msg = f"exit {rc}{note} after {time.time() - x['t0']:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"({r['name']}) {msg}")
                del runs[tag]


def selftest():
    try:
        os.remove(os.path.join(LOGS, "run1012e.selftest.driver.log"))
    except OSError:
        pass
    subprocess.run([sys.executable, os.path.abspath(__file__), "--selftest-inner"] + [a for a in sys.argv if a.startswith("--mutate=")], capture_output=True, text=True)
    log = open(os.path.join(LOGS, "run1012e.selftest.driver.log"), encoding="utf-8").read()
    pids = [int(x) for x in re.findall(r"pid (\d+):", log)]
    alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
    n_succ, n_mis, n_ok = log.count("ended below 1e-6"), log.count("PLUMBING MISMATCH"), log.count(": ok")
    ok = not alive and n_succ == 1 and n_mis == 1 and n_ok == 1
    print(f"success notices {n_succ} (want 1), K mismatches {n_mis} (want 1), K ok {n_ok} (want 1), alive after the cap {alive} -> selftest {'PASS' if ok else 'FAIL'}", flush=True)
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
