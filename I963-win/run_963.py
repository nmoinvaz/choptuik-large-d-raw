#!/usr/bin/env python3
"""#963 (win): rt_sigma.py --rough --starts 12 on sample c's K = 0 root (the control, delta 0) and on its three moved states, one run at a time, 2 BLAS threads, BelowNormal.
From I951-win/run_951.py. Order: c_d0, c_d1e-20, c_d1e-19, c_d1e-18.

usage: python run_963.py                 (venv-t151 python, from this folder; writes logs/<label>.log, logs/<label>.exit, logs/run_963.log, logs/run_963.exit)
       python run_963.py --selftest      the driver on dummy children and the control compare on planted logs

Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12, cwd = <worktree>/solver/rt (main f88adb20).
Stop rules (the issue): a run over its own cap of 2 h is killed and reported with what it printed (exit file 'killed 5 (cap 2 h)'); the next run then still starts. A run's nonzero exit
that is not the cap stops the work (driver exit 7). After c_d0 the control must hold, its 12 'start' lines equal to the first 12 of #951's K0c_D40_rough.log in every printed
character (the max|F| line is not compared, its state path differs); if not, the work stops (driver exit 6, logs/control.exit FAILED). A file STOP_963 in this folder stops what runs (4).
Exit codes of logs/run_963.exit: 0 all four ran to exit 0, 5 at least one cap hit and no failure, 6 control failed, 7 a run failed, 4 stopped."""
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i963"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
S = r"C:\Users\nathan\Source\choptuik-large-d-raw\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"
REF = r"C:\Users\nathan\Source\choptuik-large-d-raw\I951-win\logs\K0c_D40_rough.log"
JOBS = [("c_d0", S), ("c_d1e-20", os.path.join(HERE, "states", "c_d1e-20.npz")),
        ("c_d1e-19", os.path.join(HERE, "states", "c_d1e-19.npz")), ("c_d1e-18", os.path.join(HERE, "states", "c_d1e-18.npz"))]
NSTARTS = 12
CAP_S = 2.0 * 3600
THREADS = "2"
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000
START = re.compile(r"^\s+start \d+: max\|x\|")


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "run_963.log"), "a") as f:
        f.write(line + "\n")


def start_lines(path, n):
    with open(path, encoding="utf-8", errors="replace") as f:
        return [ln.rstrip("\r\n") for ln in f if START.match(ln)][:n]


def control_ok(log, ref, n=NSTARTS):
    a, b = start_lines(log, n), start_lines(ref, n)
    if len(b) < n:
        return False, f"reference has {len(b)} start lines"
    if len(a) < n:
        return False, f"control printed {len(a)} of {n} start lines"
    bad = [i for i in range(n) if a[i] != b[i]]
    return (not bad), (f"{n} of {n} start lines equal" if not bad else f"start lines differ at {bad}: {a[bad[0]]!r} against {b[bad[0]]!r}")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def run_one(job, logdir, stopfile, cap_s, poll=10.0):
    """job: dict label, cmd, cwd, env. Returns the code: 0 normal, 4 STOP, 5 cap, else the exit code."""
    lab = job["label"]
    t = time.time()
    p = subprocess.Popen(job["cmd"], cwd=job["cwd"], stdout=open(os.path.join(logdir, f"{lab}.log"), "w"), stderr=subprocess.STDOUT, env=job["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
    say(logdir, f"start {lab} (pid {p.pid}), cap {cap_s / 3600:.2f} h")
    while True:
        time.sleep(poll)
        if os.path.exists(stopfile):
            kill_tree(p)
            code, text = 4, "killed 4 (STOP_963)"
        elif time.time() - t > cap_s:
            kill_tree(p)
            code, text = 5, f"killed 5 (cap {cap_s / 3600:.2f} h)"
        else:
            rc = p.poll()
            if rc is None:
                continue
            code, text = rc, f"exit {rc}"
        break
    open(os.path.join(logdir, f"{lab}.exit"), "w").write(text + "\n")
    say(logdir, f"{lab} {text} after {time.time() - t:.0f} s")
    return code


def drive(jobs, logdir, stopfile, ref, cap_s, poll=10.0):
    """Runs the jobs in order, returns (driver exit code, {label: code}). jobs[0] is the control."""
    os.makedirs(logdir, exist_ok=True)
    codes, any_cap = {}, False
    for i, job in enumerate(jobs):
        code = run_one(job, logdir, stopfile, cap_s, poll)
        codes[job["label"]] = code
        if code == 4:
            return 4, codes
        if i == 0:
            ok, why = control_ok(os.path.join(logdir, f"{job['label']}.log"), ref) if code == 0 else (False, f"control exit {code}")
            open(os.path.join(logdir, "control.exit"), "w").write(("ok " if ok else "FAILED ") + why + "\n")
            say(logdir, f"control {'ok' if ok else 'FAILED'}: {why}")
            if not ok:
                return 6, codes
        elif code == 5:
            any_cap = True
        elif code != 0:
            return 7, codes
    return (5 if any_cap else 0), codes


def dummy(label, body, env):
    return dict(label=label, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env)


def selftest():
    bad = 0
    env = dict(os.environ)
    lines = lambda k: "".join(f"print('  start {i}: max|x| 1.{i}e+33, bound on the smallest gain 9.{i}e-36, max|J x - v| 1.0e-16, 67 products', flush=True)\n" for i in range(k))
    slow = "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        ref = os.path.join(td, "ref.log")
        open(ref, "w").write("hdr different\n" + "".join(f"  start {i}: max|x| 1.{i}e+33, bound on the smallest gain 9.{i}e-36, max|J x - v| 1.0e-16, 67 products\n" for i in range(12)) + "tail\n")
        # a good control and three good runs: driver exit 0
        jobs = [dummy("c_d0", "print('other header')\n" + lines(12), env)] + [dummy(f"r{i}", lines(12), env) for i in range(3)]
        rc, codes = drive(jobs, os.path.join(td, "l1"), os.path.join(td, "STOP"), ref, 30, 0.2)
        ok = rc == 0 and open(os.path.join(td, "l1", "control.exit")).read().startswith("ok")
        print(f"  good control and runs: exit {rc} {codes} {'ok' if ok else 'WRONG'}")
        bad += not ok
        # the control with one digit changed must fail and stop the work (the control of the control)
        mut = lines(12).replace("9.5e-36", "9.6e-36")
        jobs = [dummy("c_d0", mut, env), dummy("r0", lines(12), env)]
        rc, codes = drive(jobs, os.path.join(td, "l2"), os.path.join(td, "STOP"), ref, 30, 0.2)
        ok = rc == 6 and "r0" not in codes and open(os.path.join(td, "l2", "control.exit")).read().startswith("FAILED")
        print(f"  control with one digit changed: exit {rc} {codes} (want 6, r0 not run) {'ok' if ok else 'WRONG'}")
        bad += not ok
        # a control with 11 start lines fails
        jobs = [dummy("c_d0", lines(11), env)]
        rc, _ = drive(jobs, os.path.join(td, "l3"), os.path.join(td, "STOP"), ref, 30, 0.2)
        ok = rc == 6
        print(f"  control with 11 of 12 starts: exit {rc} (want 6) {'ok' if ok else 'WRONG'}")
        bad += not ok
        # a cap hit on a moved run is reported and the next run still starts; a crash stops
        jobs = [dummy("c_d0", lines(12), env), dummy("slow", slow, env), dummy("after", lines(12), env)]
        rc, codes = drive(jobs, os.path.join(td, "l4"), os.path.join(td, "STOP"), ref, 2.0, 0.2)
        ok = rc == 5 and codes == {"c_d0": 0, "slow": 5, "after": 0}
        print(f"  cap hit: exit {rc} {codes} (want slow 5 and the run after it still done) {'ok' if ok else 'WRONG'}")
        bad += not ok
        jobs = [dummy("c_d0", lines(12), env), dummy("crash", "import sys; sys.exit(3)", env), dummy("after", lines(12), env)]
        rc, codes = drive(jobs, os.path.join(td, "l5"), os.path.join(td, "STOP"), ref, 30, 0.2)
        ok = rc == 7 and "after" not in codes
        print(f"  a crash: exit {rc} {codes} (want 7, after not run) {'ok' if ok else 'WRONG'}")
        bad += not ok
        stop = os.path.join(td, "STOP")
        open(stop, "w").write("x")
        rc, codes = drive([dummy("c_d0", slow, env)], os.path.join(td, "l6"), stop, ref, 30, 0.2)
        ok = rc == 4
        print(f"  STOP file: exit {rc} (want 4) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    jobs = []
    for lab, state in JOBS:
        if not os.path.exists(state):
            say(logdir, f"missing state {state}")
            sys.exit(2)
        jobs.append(dict(label=lab, cmd=[PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(RT, "rt_sigma.py"), state, "--rough", "--starts", str(NSTARTS)], cwd=RT, env=env))
    rc, codes = drive(jobs, logdir, os.path.join(HERE, "STOP_963"), REF, CAP_S)
    open(os.path.join(logdir, "run_963.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
