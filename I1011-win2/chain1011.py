"""#1011: M = 9, levels 5 and 3 without the slow-progress stop above 1e-4. #1007's command with --floor_max=1e-4 --verbose=2 at
(1) --polish=5:0.11 --approach=5:0.105 and (2) --polish=5:0.105 --approach=5:0.105, side by side, BelowNormal, 3 h cap each.

    python chain1011.py [--selftest [--mutate=nokill|anysolve]]       (from this folder)

The cap is already 3 h, so a run whose first level-5 solve ends below 1e-6 simply goes on to the zero within it; the driver only logs that event (first solve
only; a later solve below 1e-6 is logged apart). The cap kills the run's whole tree (taskkill /T /F; hier.py's spawn workers survive a kill of the main process).
Logs logs/hier_nb_M9_polish5_<XI>_approach5_<AP>_fm1e-4_win2.log, .exit files, driver log logs/run1011.driver.log.
--selftest: two stubs (cap 3 s): stub 1's first level-5 solve is 5e-7 (the notice must appear for it), stub 2's first is 6 and a later one 5e-7 (no 'first solve' notice,
a 'later solve' notice); both must be killed with no process left. --mutate=nokill leaves the trees alive, --mutate=anysolve gives the first-solve notice for stub 2: both must fail.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
RUNS = [("0.11", "0.105"), ("0.105", "0.105")]                      # (polish XI, approach AP) of level 5
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF = "--selftest" in sys.argv
CAP = 3.0 if SELF else 10800.0
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run1011.selftest.driver.log" if SELF else "run1011.driver.log"), "a")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True); drv.write(line + "\n"); drv.flush()


def command(xi, ap):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict",
            "--procs", "2", "--h3=1e-4", "--floor_max=1e-4", "--verbose=2", f"--approach=5:{ap}", f"--polish=5:{xi}"]


def level5_solves(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [float(x) for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]


def main():
    running, noted, fate = {}, {}, {}
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s, RUN_SRC {SRC}, runs (XI, AP) {RUNS}, --floor_max=1e-4 --verbose=2, side by side" + (" (selftest)" if SELF else ""))
    for k, (xi, ap) in enumerate(RUNS):
        tag = f"hier_nb_M9_polish5_{xi}_approach5_{ap}_fm1e-4_win2" + ("_selftest" if SELF else "")
        if SELF:
            body = ["print('   level 5 solved: |r_5| 5.0e-07', flush=True)",
                    "print('   level 5 solved: |r_5| 6.0e+00', flush=True)\ntime.sleep(1)\nprint('   level 5 solved: |r_5| 5.0e-07', flush=True)"][k]
            cmd = [PY, "-c", "import time\n" + body + "\ntime.sleep(60)"]
        else:
            cmd = command(xi, ap)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        running[tag] = (p, f, time.time(), xi); noted[tag] = set()
        say(f"start XI {xi} AP {ap} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
    while running:
        time.sleep(0.5 if SELF else 10)
        for tag in list(running):
            p, f, t0, xi = running[tag]
            sol = level5_solves(os.path.join(LOGS, tag + ".log"))
            if sol and "first" not in noted[tag] and (sol[0] < 1e-6 or ("--mutate=anysolve" in sys.argv and min(sol) < 1e-6)):
                noted[tag].add("first"); say(f"XI {xi}: the first level-5 solve ended at {sol[0]:.2e}, below 1e-6 (the success case; the run goes on within the cap)")
            if len(sol) > 1 and "later" not in noted[tag] and min(sol[1:]) < 1e-6:
                noted[tag].add("later"); say(f"XI {xi}: a later level-5 solve ended below 1e-6 ({min(sol[1:]):.2e}); the first was {sol[0]:.2e}")
            rc, note = p.poll(), ""
            if rc is None and time.time() - t0 > CAP:
                if "--mutate=nokill" not in sys.argv:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {CAP:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                f.close()
                msg = f"exit {rc}{note} after {time.time() - t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"XI {xi}: {msg}"); fate[tag] = (rc, p.pid); del running[tag]
    if SELF:
        alive = [pid for rc, pid in fate.values() if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
        log = open(os.path.join(LOGS, "run1011.selftest.driver.log"), encoding="utf-8").read()
        first_for_1 = "XI 0.11: the first level-5 solve ended" in log
        first_for_2 = "XI 0.105: the first level-5 solve ended" in log
        later_for_2 = "XI 0.105: a later level-5 solve ended" in log
        ok = not alive and first_for_1 and not first_for_2 and later_for_2 and all(rc == "capped" for rc, _ in fate.values())
        say(f"selftest: alive after the cap {alive}; first-solve notice for stub 1 {first_for_1}, for stub 2 {first_for_2} (want False); later-solve notice for stub 2 {later_for_2}")
        say("selftest " + ("PASS" if ok else "FAIL")); return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
