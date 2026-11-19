"""#1012 last stage (the coordinator's hc, 2026-11-19 ~12:25 UTC): the slope of the corrected r_1 in (A, omega) at M = 9, from the M = 7 protocol's solves (proof/B_tail_M7.md 3.1, run_job.py) at
XI 0.11 / AP 0.105 / --h5=1e-4 (the stage-1 command, --predict, --floor_max=1e-4, --verbose=2, rtol 1e-13), from D:/choptuik-h9b (main 299c4eb9), BelowNormal, 3 h cap each, side by side:
  dA           A + 2e-4  (2.719419, 1.000022), seeded with Z's harmonics (--x=...)
  dw           w/w_inf + 1e-4  (2.719219, 1.000122), seeded
  zero_repeat  (2.719219, 1.000022), UNSEEDED (no --x, the default seed), a second centre solve
The zero solve is stage 1's XI 0.11 run itself (same command, deterministic: its first 1082 lines were reproduced line for line by stage 5(b) from this extract), I1012-win2's
hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_win2.log; it is not run again.

    python chain1012g.py [--selftest [--mutate=nokill|swap]]            (from this folder)

Logs logs/hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_outer_<name>_win2.log, .exit files, driver log logs/run1012g.driver.log. As the other drivers: every level-5 solve's end, a solve
below 1e-6 (the success of #1012), the K-line check (10 residuals with --predict).
--selftest builds each run's command and checks the (A, w, seed) of each (dA has A 2.719419 and w 1.000022, dw A 2.719219 and w 1.000122, both with --x=, zero_repeat 2.719219 1.000022 without --x=)
and runs three stubs (cap 3 s) that must leave no process; --mutate=swap exchanges dA's and dw's values and must fail, --mutate=nokill leaves the stubs and must fail."""
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
drv = open(os.path.join(LOGS, "run1012g.selftest.driver.log" if SELF else "run1012g.driver.log"), "a")
RUNS = [dict(name="dA", A="2.719419", w="1.000022", seeded=True), dict(name="dw", A="2.719219", w="1.000122", seeded=True),
        dict(name="zero_repeat", A="2.719219", w="1.000022", seeded=False)]
if "--mutate=swap" in sys.argv:
    RUNS[0]["A"], RUNS[1]["A"] = RUNS[1]["A"], RUNS[0]["A"]
    RUNS[0]["w"], RUNS[1]["w"] = RUNS[1]["w"], RUNS[0]["w"]


def say(s):
    line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
    print(line, flush=True)
    drv.write(line + "\n")
    drv.flush()


def command(r):
    c = [PY, "-u", "hier_nb.py", "9", r["A"], r["w"]] + ([f"--x={Z_X}"] if r["seeded"] else [])
    return c + ["--xi1=0.15", "--pretune", "--fixA", "--schur", "--predict", "--procs", "2", "--h3=1e-4", "--h5=1e-4", "--floor_max=1e-4", "--verbose=2",
                "--approach=5:0.105", "--polish=5:0.11"]


def check_commands():
    cm = {r["name"]: command(r) for r in RUNS}
    ok = (cm["dA"][4:6] == ["2.719419", "1.000022"] and cm["dw"][4:6] == ["2.719219", "1.000122"] and cm["zero_repeat"][4:6] == ["2.719219", "1.000022"]
          and any(a.startswith("--x=") for a in cm["dA"]) and any(a.startswith("--x=") for a in cm["dw"]) and not any(a.startswith("--x=") for a in cm["zero_repeat"])
          and all("--h5=1e-4" in c and "--predict" in c and "--floor_max=1e-4" in c for c in cm.values()))
    return ok


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
        tag = f"hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_outer_{r['name']}_win2" + ("_selftest" if SELF else "")
        if SELF:
            cmd = [PY, "-c", "import time\nprint('   Jacobian K computed (10 residuals) [5 s]', flush=True)\ntime.sleep(60)"]
        else:
            cmd = command(r)
        f = open(os.path.join(LOGS, tag + ".log"), "w", encoding="utf-8", newline="\n")
        p = subprocess.Popen(cmd, cwd=SRC, env=ENV, stdout=f, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NEW_GROUP)
        runs[tag] = dict(p=p, f=f, t0=time.time(), r=r, seen=0, k=False)
        say(f"start ({r['name']}) A {r['A']} w {r['w']} {'seeded' if r['seeded'] else 'unseeded'} pid {p.pid}: {' '.join(cmd[2:]) if not SELF else 'stub'} > logs/{tag}.log")
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
                say(f"({r['name']}) level-5 solve {x['seen']} ended " + (f"below 1e-6 ({v:.2e}): the success case of #1012 (the run goes on within the cap)" if v < 1e-6 else f"at {v:.2e}"))
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
        os.remove(os.path.join(LOGS, "run1012g.selftest.driver.log"))
    except OSError:
        pass
    cmd_ok = check_commands()
    subprocess.run([sys.executable, os.path.abspath(__file__), "--selftest-inner"] + [a for a in sys.argv if a.startswith("--mutate=")], capture_output=True, text=True)
    log = open(os.path.join(LOGS, "run1012g.selftest.driver.log"), encoding="utf-8").read()
    pids = [int(x) for x in re.findall(r"pid (\d+):", log)]
    alive = [pid for pid in pids if subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout.split().count(str(pid))]
    ok = cmd_ok and not alive and len(pids) == 3
    print(f"commands carry the right (A, w, seed) per run: {cmd_ok}; stubs started {len(pids)} (want 3); alive after the cap {alive} -> selftest {'PASS' if ok else 'FAIL'}", flush=True)
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
