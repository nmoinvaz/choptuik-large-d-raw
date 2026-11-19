"""#999: the M = 9 diagnostic of #980 with level 5's polish radius set by hand, XI in 0.12, 0.13, 0.14, two side by side then the third.

    python chain999.py [--selftest [--mutate=nokill]]          (from this folder; BelowNormal, 1 h cap per run)

Each run is #980's command (INNER_NB_RTOL=1e-13, no --floor, --verbose=2) plus --polish=5:XI, from the runner's own worktree
(RUN_SRC, D:/choptuik-inner/solver/inner_stokes), logs logs/hier_nb_M9_polish5_<XI>_win2.log, exit files logs/hier_nb_M9_polish5_<XI>_win2.exit,
driver log logs/run999.driver.log. The cap kills the run's whole process tree (taskkill /T /F; hier.py's spawn workers survive a kill of
the main process). --selftest runs three stub jobs (sleeping python, cap 4 s, two at a time) and exits 0 only when each is capped,
its tree is gone and the third started after the first ended.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
CAP_S = float(os.environ.get("RUN_CAP_H", "1")) * 3600
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
XIS = ["0.12", "0.13", "0.14"]
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
os.makedirs(LOGS, exist_ok=True)
drv = open(os.path.join(LOGS, "run999.driver.log" if "--selftest" not in sys.argv else "run999.selftest.driver.log"), "a")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True); drv.write(line + "\n"); drv.flush()


def command(xi):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict",
            "--procs", "2", "--h3=1e-4", "--verbose=2", f"--polish=5:{xi}"]


def main(selftest=False):
    cap = 4.0 if selftest else CAP_S
    jobs = list(XIS)
    running, done, order = {}, {}, []
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {cap:g} s, RUN_PY {PY}, RUN_SRC {SRC}, XI {XIS}, two at a time" + (" (selftest)" if selftest else ""))
    while jobs or running:
        while jobs and len(running) < 2:
            xi = jobs.pop(0)
            tag = f"hier_nb_M9_polish5_{xi}_win2" + ("_selftest" if selftest else "")
            cmd = [PY, "-c", "import time; time.sleep(60)"] if selftest else command(xi)
            f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
            p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
            running[xi] = (p, f, time.time(), tag)
            order.append(("start", xi, time.time()))
            say(f"start XI {xi} pid {p.pid}: {' '.join(cmd[2:]) if not selftest else 'stub'} > logs/{tag}.log")
        time.sleep(2 if selftest else 10)
        for xi in list(running):
            p, f, t0, tag = running[xi]
            rc, note = p.poll(), ""
            if rc is None and time.time() - t0 > cap:
                if "--mutate=nokill" not in sys.argv:           # the mutation leaves the tree alive: the selftest must fail
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                    p.wait()
                rc, note = "capped", f" (killed the process tree at the {cap:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                f.close()
                msg = f"exit {rc}{note} after {time.time() - t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"XI {xi}: {msg}")
                done[xi] = (rc, p.pid); order.append(("end", xi, time.time())); del running[xi]
    if selftest:
        ends = [t for k, x, t in order if k == "end"]; starts = {x: t for k, x, t in order if k == "start"}
        alive = [pid for rc, pid in done.values() if subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout.count(str(pid))]
        ok = all(rc == "capped" for rc, _ in done.values()) and not alive and starts["0.14"] >= min(ends) - 0.5
        say(f"selftest: capped {[rc for rc, _ in done.values()]}, alive after the cap {alive}, third started after the first ended: {starts['0.14'] >= min(ends) - 0.5}")
        say("selftest " + ("PASS" if ok else "FAIL")); return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main("--selftest" in sys.argv))
