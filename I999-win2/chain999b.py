"""#999 after the coordinator changed the scan (2026-11-19 ~02:06 UTC): drop XI 0.14; after the runs for 0.12 and 0.13 have ended, run
--polish=5:0.11 with --approach=5:0.105 and --polish=5:0.10 with --approach=5:0.095, side by side, 1 h cap each, BelowNormal.

    python chain999b.py [--selftest]       (from this folder)

Waits for logs/hier_nb_M9_polish5_0.12_win2.exit and ..._0.13_win2.exit (written by adopt999.py). Same command as chain999.py plus
--approach. Cap rule of the issue ("if one works, go on to the M = 9 zero solve with it, 3 h cap"): a run whose log shows a level-5
solve ending below 1e-6 gets its cap extended to 3 h from its start, which is the same computation continued. Logs
logs/hier_nb_M9_polish5_<XI>_approach5_<AP>_win2.log, .exit files, driver log logs/run999b.driver.log. --selftest runs two stubs (cap 3 s,
extended 9 s): the one whose log shows 'level 5 solved: |r_5| 5.0e-07' must live past 3 s and die near 9 s, the other must die at 3 s.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-inner/solver/inner_stokes")
Z_X = "0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168"
RUNS = [("0.11", "0.105"), ("0.10", "0.095")]            # polish XI, approach AP of level 5
BELOW_NORMAL, NEW_GROUP = 0x00004000, 0x00000200
ENV = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOGS = os.path.join(HERE, "logs")
SELF = "--selftest" in sys.argv
CAP, CAP_EXT = (3.0, 9.0) if SELF else (3600.0, 10800.0)
drv = open(os.path.join(LOGS, "run999b.selftest.driver.log" if SELF else "run999b.driver.log"), "a")


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True); drv.write(line + "\n"); drv.flush()


def command(xi, ap):
    return [PY, "-u", "hier_nb.py", "9", "2.719219", "1.000022", f"--x={Z_X}", "--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict",
            "--procs", "2", "--h3=1e-4", "--verbose=2", f"--polish=5:{xi}", f"--approach=5:{ap}"]


def below_bar(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return False
    return any(float(x) < 1e-6 for x in re.findall(r"level 5 solved: \|r_5\| (\S+)", t))


def main():
    if not SELF:
        say("waiting for the 0.12 and 0.13 runs to end")
        while not all(os.path.exists(os.path.join(LOGS, f"hier_nb_M9_polish5_{x}_win2.exit")) for x in ("0.12", "0.13")):
            time.sleep(15)
    running, ext, fate = {}, {}, {}
    say(f"INNER_NB_RTOL={ENV['INNER_NB_RTOL']} cap {CAP:g} s (extended to {CAP_EXT:g} s once a level-5 solve ends below 1e-6), RUN_SRC {SRC}, runs {RUNS}" + (" (selftest)" if SELF else ""))
    for k, (xi, ap) in enumerate(RUNS):
        tag = f"hier_nb_M9_polish5_{xi}_approach5_{ap}_win2" + ("_selftest" if SELF else "")
        if SELF:
            body = "import time,sys\nprint('   level 5 solved: |r_5| 5.0e-07', flush=True)\n" if k == 0 else "import time\nprint('   level 5 solved: |r_5| 6.0e+00', flush=True)\n"
            cmd = [PY, "-c", body + "time.sleep(60)"]
        else:
            cmd = command(xi, ap)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        running[tag] = (p, f, time.time()); say(f"start polish {xi} approach {ap} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
    while running:
        time.sleep(1 if SELF else 10)
        for tag in list(running):
            p, f, t0 = running[tag]
            logp = os.path.join(LOGS, tag + ".log")
            if tag not in ext and below_bar(logp):
                ext[tag] = time.time() - t0; say(f"{tag}: a level-5 solve ended below 1e-6, cap extended to {CAP_EXT:g} s from the start")
            cap = CAP_EXT if tag in ext else CAP
            rc, note = p.poll(), ""
            if rc is None and time.time() - t0 > cap:
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                p.wait(); rc, note = "capped", f" (killed the process tree at the {cap:g} s cap, taskkill /T /F /PID {p.pid})"
            if rc is not None:
                f.close()
                msg = f"exit {rc}{note} after {time.time() - t0:.0f} s, ended {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC"
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
                say(f"{tag}: {msg}"); fate[tag] = time.time() - t0; del running[tag]
    if SELF:
        ts = sorted(fate.items())
        ok = len(ts) == 2 and 8.5 <= fate[[t for t in fate if "0.11" in t][0]] <= 12 and 2.5 <= fate[[t for t in fate if "0.10_" in t][0]] <= 6
        say(f"selftest: fates {[(t[-30:], round(v, 1)) for t, v in ts]}; extended run lived to ~9 s, the other died at ~3 s: {ok}")
        say("selftest " + ("PASS" if ok else "FAIL")); return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
