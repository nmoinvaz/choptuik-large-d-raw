"""#1012: #1011's two runs with --h5=1e-4, then --h5=1e-3 if neither first level-5 solve gets below 1e-6. BelowNormal, 3 h cap each.

    python chain1012.py [--selftest [--mutate=nokill|anyone]]          (from this folder; INNER_NB_RTOL=1e-13, RUN_SRC the runner's worktree)

Stage 1: (XI 0.11, AP 0.105) and (XI 0.105, AP 0.105) at --h5=1e-4, started at once. Stage 2: run 1 only, (XI 0.11, AP 0.105), at --h5=1e-3 (the issue's "run 1 again"),
started as soon as both stage-1 runs have ended their FIRST level-5 solve, and only when NEITHER first solve is below 1e-6; stage 1 goes on to its cap beside it (a run whose first solve is below 1e-6 goes on to the zero
within its 3 h; the driver only logs it). A stage-1 run that exits before any level-5 solve counts as no solve below 1e-6. Each cap kills the run's whole process tree
(taskkill /T /F).
Command (as #1011, plus --h5): hier_nb.py 9 2.719219 1.000022 --x=... --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=H5 --floor_max=1e-4
--verbose=2 --approach=5:AP --polish=5:XI.
Logs logs/hier_nb_M9_polish5_<XI>_approach5_<AP>_fm1e-4_h5<H5>_win2.log, .exit files, driver log logs/run1012.driver.log.
--selftest runs the driver twice on stubs (cap 3 s): scenario A, first solves 6.0 and 8.0 (stage 2 must start), scenario B, first solves 5e-7 and 8.0 (stage 2 must not
start); each needs no process left. --mutate=anyone starts stage 2 when ANY first solve is above 1e-6 (scenario B must then fail); --mutate=nokill leaves the trees alive
(must fail).
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
PAIR = [("0.11", "0.105"), ("0.105", "0.105")]
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF_INNER = next((a.split("=")[1] for a in sys.argv if a.startswith("--inner=")), None)
SELF = SELF_INNER is not None
CAP = 3.0 if SELF else 10800.0
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run1012.selftest.driver.log" if SELF else "run1012.driver.log"), "a")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def command(xi, ap, h5):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict", "--procs", "2",
            "--h3=1e-4", f"--h5={h5}", "--floor_max=1e-4", "--verbose=2", f"--approach=5:{ap}", f"--polish=5:{xi}"]


def level5_solves(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [float(x) for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]


def start(runs, xi, ap, h5, k=0):
    tag = f"hier_nb_M9_polish5_{xi}_approach5_{ap}_fm1e-4_h5{h5}_win2" + ("_selftest" if SELF else "")
    if SELF:
        first = {"A": ("6.0e+00", "8.0e+00"), "B": ("5.0e-07", "8.0e+00")}[SELF_INNER][k] if h5 == "1e-4" else "7.0e+00"
        cmd = [PY, "-c", "import time\nprint('   level 5 solved: |r_5| " + first + "', flush=True)\ntime.sleep(60)"]
    else:
        cmd = command(xi, ap, h5)
    f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
    p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
    runs[tag] = dict(p=p, f=f, t0=time.time(), xi=xi, ap=ap, h5=h5, notes=set(), stage=1 if h5 == "1e-4" else 2)
    say(f"start stage {runs[tag]['stage']} XI {xi} AP {ap} --h5={h5} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")


def main():
    runs, fate, decided = {}, {}, False
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s, RUN_SRC {SRC}, stage 1 --h5=1e-4, stage 2 --h5=1e-3 only if neither first level-5 solve is below 1e-6"
        + (f" (selftest {SELF_INNER})" if SELF else ""))
    for k, (xi, ap) in enumerate(PAIR):
        start(runs, xi, ap, "1e-4", k)
    while runs:
        time.sleep(0.5 if SELF else 10)
        if not decided:
            s1 = [t for t, r in runs.items() if r["stage"] == 1] + [t for t in fate if fate[t]["stage"] == 1]
            firsts = {}
            for t in s1:
                sol = level5_solves(os.path.join(LOGS, t + ".log"))
                firsts[t] = sol[0] if sol else (float("inf") if t in fate else None)
            if all(v is not None for v in firsts.values()):
                decided = True
                bad = [v >= 1e-6 for v in firsts.values()]
                go = any(bad) if "--mutate=anyone" in sys.argv else all(bad)
                say(f"decision: first level-5 solves {[f'{v:.2e}' for v in firsts.values()]}, stage 2 (--h5=1e-3) {'starts' if go else 'does not start'}")
                if go:
                    for k, (xi, ap) in enumerate(PAIR[:1]):               # the issue: "run 1 again with --h5=1e-3" (XI 0.11, AP 0.105 only)
                        start(runs, xi, ap, "1e-3", k)
        for tag in list(runs):
            r = runs[tag]
            p = r["p"]
            sol = level5_solves(os.path.join(LOGS, tag + ".log"))
            if sol and "first" not in r["notes"] and sol[0] < 1e-6:
                r["notes"].add("first")
                say(f"{tag}: the first level-5 solve ended at {sol[0]:.2e}, below 1e-6 (the success case; the run goes on within the cap)")
            if len(sol) > 1 and "later" not in r["notes"] and min(sol[1:]) < 1e-6:
                r["notes"].add("later")
                say(f"{tag}: a later level-5 solve ended below 1e-6 ({min(sol[1:]):.2e}); the first was {sol[0]:.2e}")
            rc, note = p.poll(), ""
            if rc is None and time.time() - r["t0"] > CAP:
                if "--mutate=nokill" not in sys.argv:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {CAP:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                r["f"].close()
                msg = f"exit {rc}{note} after {time.time() - r['t0']:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"{tag}: {msg}")
                fate[tag] = dict(rc=rc, pid=p.pid, stage=r["stage"])
                del runs[tag]
    return 0


def selftest():
    ok = True
    for scen, want_stage2 in (("A", True), ("B", False)):
        try:
            os.remove(os.path.join(LOGS, "run1012.selftest.driver.log"))
        except OSError:
            pass
        subprocess.run([sys.executable, os.path.abspath(__file__), f"--inner={scen}"] + [a for a in sys.argv if a.startswith("--mutate=")], capture_output=True, text=True)
        log = open(os.path.join(LOGS, "run1012.selftest.driver.log"), encoding="utf-8").read()
        pids = [int(x) for x in re.findall(r"pid (\d+): stub", log)]
        alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
        stage2 = "stage 2 (--h5=1e-3) starts" in log
        n2 = log.count("start stage 2")
        good = stage2 == want_stage2 and not alive and n2 == (1 if want_stage2 else 0)
        print(f"scenario {scen}: stage 2 started {stage2} (want {want_stage2}), stage-2 runs {n2}, alive after the cap {alive} -> {'ok' if good else 'FAIL'}", flush=True)
        ok = ok and good
        for fn in os.listdir(LOGS):
            if fn.endswith("_selftest.log") or fn.endswith("_selftest.exit"):
                try:
                    os.remove(os.path.join(LOGS, fn))
                except OSError:
                    pass
    print("selftest " + ("PASS" if ok else "FAIL"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
