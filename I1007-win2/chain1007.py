"""#1007: M = 9, level 5's polish radius XI at the fixed approach radius 0.105. #999's command with --approach=5:0.105 --verbose=3
and --polish=5:XI for XI in 0.105, 0.115, 0.12, two at a time (the third starts when a slot frees), BelowNormal, 1 h cap each.

    python chain1007.py [--selftest [--mutate=nokill|anysolve]]       (from this folder)

Cap rule of the issue: a run whose FIRST level-5 solve ends below 1e-6 gets a 3 h cap from its start (the same computation continued, the
M = 9 zero). A later level-5 solve below 1e-6 does not extend the cap but is written to the driver log. The cap kills the run's whole tree
(taskkill /T /F; hier.py's spawn workers survive a kill of the main process). Logs logs/hier_nb_M9_polish5_<XI>_approach5_0.105_v3_win2.log,
.exit files, driver log logs/run1007.driver.log. The selftest runs three stubs (cap 3 s, extended 9 s, two at a time): stub 1's first
level-5 solve is 5e-7 (must live to ~9 s), stub 2's first is 6 and a later one 5e-7 (must die at ~3 s), stub 3 starts after a slot frees.
--mutate=nokill leaves the tree alive after the cap, --mutate=anysolve extends on any solve below the bar: the selftest must fail on both.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
AP = "0.105"
XIS = ["0.105", "0.115", "0.12"]
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF = "--selftest" in sys.argv
CAP, CAP_EXT = (3.0, 9.0) if SELF else (3600.0, 10800.0)
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run1007.selftest.driver.log" if SELF else "run1007.driver.log"), "a")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True); drv.write(line + "\n"); drv.flush()


def command(xi):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict",
            "--procs", "2", "--h3=1e-4", "--verbose=3", f"--approach=5:{AP}", f"--polish=5:{xi}"]


def level5_solves(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [float(x) for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t)]


def main():
    jobs = list(XIS)
    running, ext, noted, fate, started = {}, {}, set(), {}, {}
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s (extended to {CAP_EXT:g} s when the first level-5 solve ends below 1e-6), RUN_SRC {SRC}, "
        f"approach 5:{AP}, XI {XIS}, two at a time" + (" (selftest)" if SELF else ""))
    while jobs or running:
        while jobs and len(running) < 2:
            xi = jobs.pop(0)
            tag = f"hier_nb_M9_polish5_{xi}_approach5_{AP}_v3_win2" + ("_selftest" if SELF else "")
            if SELF:
                i = len(started)
                body = ["print('   level 5 solved: |r_5| 5.0e-07', flush=True)", "print('   level 5 solved: |r_5| 6.0e+00', flush=True); "
                        "import time; time.sleep(1.5); print('   level 5 solved: |r_5| 5.0e-07', flush=True)", "pass"][i]
                cmd = [PY, "-c", "import time\n" + body + "\ntime.sleep(60)"]
            else:
                cmd = command(xi)
            f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
            p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
            running[tag] = (p, f, time.time(), xi); started[xi] = time.time()
            say(f"start XI {xi} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
        time.sleep(0.5 if SELF else 10)
        for tag in list(running):
            p, f, t0, xi = running[tag]
            sol = level5_solves(os.path.join(LOGS, tag + ".log"))
            if tag not in ext and sol and (sol[0] < 1e-6 or ("--mutate=anysolve" in sys.argv and min(sol) < 1e-6)):
                ext[tag] = True; say(f"XI {xi}: the first level-5 solve ended at {sol[0]:.2e} (below 1e-6 or the mutation), cap extended to {CAP_EXT:g} s from the start")
            elif tag not in ext and tag not in noted and len(sol) > 1 and min(sol[1:]) < 1e-6:
                noted.add(tag); say(f"XI {xi}: a later level-5 solve ended below 1e-6 ({min(sol[1:]):.2e}), first solve {sol[0]:.2e}, cap not extended (the issue's rule is the first solve)")
            cap = CAP_EXT if tag in ext else CAP
            rc, note = p.poll(), ""
            if rc is None and time.time() - t0 > cap:
                if "--mutate=nokill" not in sys.argv:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {cap:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                f.close()
                msg = f"exit {rc}{note} after {time.time() - t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"XI {xi}: {msg}"); fate[xi] = (rc, p.pid, time.time() - t0); del running[tag]
    if SELF:
        alive = [pid for rc, pid, _ in fate.values() if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
        l1, l2 = fate["0.105"][2], fate["0.115"][2]
        third_after = started["0.12"] >= min(started["0.105"], started["0.115"]) + 2.5
        ok = (8.5 <= l1 <= 12) and (2.5 <= l2 <= 6) and not alive and third_after
        say(f"selftest: lived {l1:.1f} s (extended, want ~9) and {l2:.1f} s (not extended, want ~3), alive after the cap {alive}, third started after a slot freed: {third_after}")
        say("selftest " + ("PASS" if ok else "FAIL")); return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
