"""#1012 stage 6 (the coordinator's hc, 2026-11-19 ~10:20 UTC): after both stage-5 runs have reached their caps (12:59:21 UTC) or ended, close the level-5 step bracket with two runs side by
side, from D:/choptuik-h9b (extract of main 299c4eb9), XI 0.11 / AP 0.105, INNER_NB_RTOL=1e-13, --predict on as stage 1, BelowNormal, 3 h cap each (whole process tree killed at the cap):
  (c) --h5=3e-5      (d) --h5=1e-5
Command: hier_nb.py 9 2.719219 1.000022 --x=... --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=H5 --floor_max=1e-4 --verbose=2 --approach=5:0.105 --polish=5:0.11

    python chain1012f.py [--selftest [--mutate=nokill|anysolve|nowait]]         (from this folder)

The driver WAITS for the exit files of stage 5's two runs (logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-4_win2.exit and ..._h51e-4_nopredict_win2.exit) and starts only
when both exist; stop rule: if they are not both there by 13:15 UTC (UTC clock, the day the driver starts) it logs that and exits without starting anything. Logs
logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-5_win2.log and ..._h51e-5_win2.log (named h5<value>), .exit files, driver log logs/run1012f.driver.log. As chain1012e.py it logs every
level-5 solve's end, any solve below 1e-6 (the success of #1012) and checks the K line (10 residuals with --predict).
--selftest: the wait files are created 2.5 s after the inner driver starts; the driver must log waiting >= 1 s before its start lines, one success notice (a stub prints solves 6.0 then 5e-7),
and leave no process. --mutate=nowait starts at once, --mutate=anysolve hides the later success notice, --mutate=nokill leaves the trees: each must fail.
"""
import os, re, subprocess, sys, threading, time

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
drv = open(os.path.join(LOGS, "run1012f.selftest.driver.log" if SELF else "run1012f.driver.log"), "a")
SELF_WAIT = [os.path.join(LOGS, "_wait_selftest_a.exit"), os.path.join(LOGS, "_wait_selftest_b.exit")]     # the only files the selftest may create or remove
WAIT_FILES = (SELF_WAIT if SELF else
              [os.path.join(LOGS, "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-4_win2.exit"),
               os.path.join(LOGS, "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_nopredict_win2.exit")])
RUNS = [dict(name="c", h5="3e-5"), dict(name="d", h5="1e-5")]
T00 = time.time()


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def command(r):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict", "--procs", "2", "--h3=1e-4",
            f"--h5={r['h5']}", "--floor_max=1e-4", "--verbose=2", "--approach=5:0.105", "--polish=5:0.11"]


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
    say(f"waiting for the stage-5 exit files: {[os.path.basename(f) for f in WAIT_FILES]}" + (" (selftest)" if SELF else ""))
    if "--mutate=nowait" not in sys.argv:
        while not all(os.path.exists(f) for f in WAIT_FILES):
            if not SELF and int(time.strftime("%H%M", time.gmtime())) >= 1315:
                say("13:15 UTC reached with a stage-5 run still not ended: nothing is started (the stop rule)")
                return
            time.sleep(0.2 if SELF else 15)
    say(f"waited {time.time() - T00:.1f} s; INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s, RUN_SRC {SRC}")
    runs = {}
    for r in RUNS:
        tag = f"hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5{r['h5']}_win2" + ("_selftest" if SELF else "")
        if SELF:
            body = ["print('   level 5 solved: |r_5| 6.0e+00', flush=True)\nprint('   Jacobian K computed (10 residuals) [5 s]', flush=True)\ntime.sleep(1)\nprint('   level 5 solved: |r_5| 5.0e-07', flush=True)",
                    "print('   Jacobian K computed (10 residuals) [5 s]', flush=True)"][len(runs)]
            cmd = [PY, "-c", "import time\n" + body + "\ntime.sleep(60)"]
        else:
            cmd = command(r)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        runs[tag] = dict(p=p, f=f, t0=time.time(), r=r, seen=0, k=False)
        say(f"start ({r['name']}) --h5={r['h5']} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
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
                say(f"({r['name']}) K line: {nk} residuals (want 10 with --predict): " + ("ok" if nk == 10 else "PLUMBING MISMATCH"))
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
        os.remove(os.path.join(LOGS, "run1012f.selftest.driver.log"))
    except OSError:
        pass
    assert all("_wait_selftest" in os.path.basename(f) for f in SELF_WAIT), "the selftest must touch only its own wait files"
    real = [os.path.join(LOGS, n) for n in ("hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-4_win2.exit", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_nopredict_win2.exit")]
    real_before = [os.path.exists(f) for f in real]
    for f in SELF_WAIT:
        try:
            os.remove(f)
        except OSError:
            pass
    proc = subprocess.Popen([sys.executable, os.path.abspath(__file__), "--selftest-inner"] + [a for a in sys.argv if a.startswith("--mutate=")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.5)
    for f in SELF_WAIT:
        open(f, "w").write("exit 0\n")
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)    # the inner driver (own pid) never started its runs
        print("the inner driver did not finish within 60 s: killed", flush=True)
    log = open(os.path.join(LOGS, "run1012f.selftest.driver.log"), encoding="utf-8").read()
    m = re.search(r"waited ([0-9.]+) s", log)
    waited = float(m.group(1)) if m else -1.0
    pids = [int(x) for x in re.findall(r"pid (\d+):", log)]
    alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
    n_succ, n_mis = log.count("ended below 1e-6"), log.count("PLUMBING MISMATCH")
    untouched = [os.path.exists(f) for f in real] == real_before
    ok = waited >= 1.0 and not alive and n_succ == 1 and n_mis == 0 and untouched
    print(f"waited {waited} s (want >= 1; the wait files appear 2.5 s after the launch), success notices {n_succ} (want 1), K mismatches {n_mis} (want 0), alive after the cap {alive}, the real stage-5 exit files untouched {untouched} -> selftest {'PASS' if ok else 'FAIL'}", flush=True)
    for fn in os.listdir(LOGS):
        if fn.endswith("_selftest.log") or fn.endswith("_selftest.exit") or fn.startswith("_wait_selftest"):
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
