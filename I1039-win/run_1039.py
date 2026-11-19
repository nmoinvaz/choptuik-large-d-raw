#!/usr/bin/env python3
"""#1039 (win): the eight commands of notes/P6_route3.md 10.6 (#990's route3_bound.py and route3_tuned.py) from solver/proof, one process at a time at
BelowNormal, as I1030-rpi5's run1030.sh ran them (same log names, each log ending with a line `exit N`).
From I1022-win/run_1022.py.

usage: python run_1039.py                 (venv-choptuik-314 python, from this folder; writes logs/<name>.log, logs/<name>.exit, logs/driver.log, logs/times.txt, logs/versions.txt, logs/run_1039.exit)
       python run_1039.py --selftest      the driver on dummy children

Stop rules: a run over its cap of 2 h is killed (taskkill /T /F on that pid) and logged 'killed 5 (cap 2 h)', the next run still starts; a run whose exit code is not the expected one
(0 for a verdict run, 1 for a control) stops the work (driver exit 7); a file STOP_1039 in this folder stops what runs (4).
Exit codes of logs/run_1039.exit: 0 all eight ended as expected, 5 at least one cap hit and no unexpected exit, 7 an unexpected exit, 4 stopped."""
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i1039"
PROOF = os.path.join(WT, "solver", "proof")
PY = r"C:\Users\nathan\Source\venv-choptuik-314\Scripts\python.exe"
# name, script arguments, expected exit
JOBS = [("route3_bound_lemmas", ["route3_bound.py", "--lemmas"], 0),
        ("route3_bound_constants", ["route3_bound.py", "--constants"], 0),
        ("route3_bound_constants_J0100", ["route3_bound.py", "--constants", "--J0=100"], 0),
        ("route3_bound_check", ["route3_bound.py", "--check"], 0),
        ("route3_bound_check_plant", ["route3_bound.py", "--check", "--mutate=plant"], 1),
        ("route3_bound_check_psi", ["route3_bound.py", "--check", "--mutate=psi"], 1),
        ("route3_tuned_7_800", ["route3_tuned.py", "7", "800"], 0),
        ("route3_tuned_7_800_demix", ["route3_tuned.py", "7", "800", "--mutate=demix"], 1)]
CAP_S = 2.0 * 3600
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "driver.log"), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def run_one(job, logdir, stopfile, cap_s, poll=5.0):
    """job: dict name, cmd, cwd, env, want. Returns (code, text): 4 STOP, 5 cap, else the child's exit code. The log ends with 'exit N' for a child that ended."""
    nm = job["name"]
    t = time.time()
    lp = os.path.join(logdir, f"{nm}.log")
    with open(lp, "w", encoding="utf-8", newline="") as lf:
        p = subprocess.Popen(job["cmd"], cwd=job["cwd"], stdout=lf, stderr=subprocess.STDOUT, env=job["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
        say(logdir, f"start {nm} (pid {p.pid}), expect exit {job['want']}, cap {cap_s / 3600:.2f} h")
        while True:
            time.sleep(poll)
            if os.path.exists(stopfile):
                kill_tree(p)
                p.wait()
                code, text = 4, "killed 4 (STOP_1039)"
            elif time.time() - t > cap_s:
                kill_tree(p)
                p.wait()
                code, text = 5, f"killed 5 (cap {cap_s / 3600:.2f} h)"
            else:
                rc = p.poll()
                if rc is None:
                    continue
                code, text = rc, f"exit {rc}"
            break
    secs = time.time() - t
    with open(lp, "a", encoding="utf-8", newline="") as lf:
        lf.write(("exit %d\n" % code) if code not in (4, 5) else (text + "\n"))
    open(os.path.join(logdir, f"{nm}.exit"), "w").write(text + "\n")
    with open(os.path.join(logdir, "times.txt"), "a") as f:
        f.write(f"{nm} {secs:.0f} s {text}\n")
    say(logdir, f"{nm} {text} after {secs:.0f} s")
    return code, text


def drive(jobs, logdir, stopfile, cap_s, poll=5.0):
    """Runs the jobs in order, returns (driver exit code, {name: code})."""
    os.makedirs(logdir, exist_ok=True)
    codes, any_cap = {}, False
    for job in jobs:
        code, _ = run_one(job, logdir, stopfile, cap_s, poll)
        codes[job["name"]] = code
        if code == 4:
            return 4, codes
        if code == 5:
            any_cap = True
        elif code != job["want"]:
            return 7, codes
    return (5 if any_cap else 0), codes


def dummy(name, body, env, want):
    return dict(name=name, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env, want=want)


def selftest():
    bad = 0
    env = dict(os.environ)
    ok_run = "print('PASS')\n"
    ctrl = "import sys\nprint('FAIL')\nsys.exit(1)\n"
    slow = "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")
        rc, codes = drive([dummy("v0", ok_run, env, 0), dummy("c0", ctrl, env, 1), dummy("v1", ok_run, env, 0)], os.path.join(td, "l1"), stop, 30, 0.2)
        t0 = open(os.path.join(td, "l1", "c0.log")).read().splitlines()
        ok = rc == 0 and codes == {"v0": 0, "c0": 1, "v1": 0} and t0[-2:] == ["FAIL", "exit 1"]
        print(f"  verdict runs and a control that exits 1: driver exit {rc} {codes}, control log ends {t0[-2:]} {'ok' if ok else 'WRONG'}")
        bad += not ok
        rc, codes = drive([dummy("v0", ok_run, env, 0), dummy("c0", ok_run, env, 1), dummy("after", ok_run, env, 0)], os.path.join(td, "l2"), stop, 30, 0.2)
        ok = rc == 7 and "after" not in codes
        print(f"  a control that exits 0 (unexpected): driver exit {rc} {codes} (want 7, after not run) {'ok' if ok else 'WRONG'}")
        bad += not ok
        rc, codes = drive([dummy("v0", ok_run, env, 0), dummy("slow", slow, env, 0), dummy("after", ok_run, env, 0)], os.path.join(td, "l3"), stop, 2.0, 0.2)
        ok = rc == 5 and codes == {"v0": 0, "slow": 5, "after": 0} and open(os.path.join(td, "l3", "slow.log")).read().strip().endswith("killed 5 (cap 0.00 h)")
        print(f"  cap hit: driver exit {rc} {codes} (want slow 5, after still run) {'ok' if ok else 'WRONG'}")
        bad += not ok
        open(stop, "w").write("x")
        rc, codes = drive([dummy("v0", slow, env, 0)], os.path.join(td, "l4"), stop, 30, 0.2)
        ok = rc == 4
        print(f"  STOP file: driver exit {rc} (want 4) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    vers = subprocess.run([PY, "-I", "-c",
                           "import sys, flint, mpmath, sympy, numpy, platform\n"
                           "print('Python', sys.version.split()[0], platform.python_implementation(), platform.machine(), platform.platform())\n"
                           "print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_RELEASE__, 'mpmath', mpmath.__version__, 'sympy', sympy.__version__, 'numpy', numpy.__version__)\n"],
                          capture_output=True, text=True).stdout
    head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    open(os.path.join(logdir, "versions.txt"), "w").write(vers + f"code worktree {WT} at {head}\n")
    say(logdir, f"driver start, main {head[:8]}; " + " ".join(vers.split()))
    jobs = [dict(name=nm, cmd=[PY, "-u"] + a, cwd=PROOF, env=env, want=w) for nm, a, w in JOBS]
    rc, codes = drive(jobs, logdir, os.path.join(HERE, "STOP_1039"), CAP_S)
    open(os.path.join(logdir, "run_1039.exit"), "w").write(f"{rc}\n")
    say(logdir, f"driver done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
