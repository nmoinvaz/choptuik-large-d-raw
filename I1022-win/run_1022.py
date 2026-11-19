#!/usr/bin/env python3
"""#1022 (win): rt_sigma.py --rough --starts 12 on sample c's K = 0 root moved along the two deep directions out of the samples' plane (rt_perturb --dir, rows 0 and 1 of I1018-win/Q_c24.npz) and along a random direction (seed 977) by 1e-18 and 1e-17, six runs one at a time, 2 BLAS threads, BelowNormal.
From I1018-win/run_1018.py.

usage: python run_1022.py                 (venv-t151 python, from this folder; writes logs/<label>.log, logs/<label>.exit, logs/run_1022.log, logs/run_1022.exit)
       python run_1022.py --selftest      the driver on dummy children

Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12, cwd = <worktree>/solver/rt (main 7745882e). Order: q0, q1, random at 1e-18, then at 1e-17.
Stop rules: a run over its own cap of 2 h is killed and reported with what it printed (exit file 'killed 5 (cap 2 h)') and the next run still starts; a nonzero exit that is not the cap
stops the work (driver exit 7); a file STOP_1022 in this folder stops what runs (4).
Exit codes of logs/run_1022.exit: 0 all six ran to exit 0, 5 at least one cap hit and no failure, 7 a run failed, 4 stopped."""
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i1018"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
JOBS = [(f"c_{m}_d{d}", os.path.join(HERE, "states", f"c_{m}_d{d}.npz")) for d in ("1e-18", "1e-17") for m in ("q0", "q1", "rand")]
NSTARTS = 12
CAP_S = 2.0 * 3600
THREADS = "2"
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "run_1022.log"), "a") as f:
        f.write(line + "\n")


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
            code, text = 4, "killed 4 (STOP_1022)"
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


def drive(jobs, logdir, stopfile, cap_s, poll=10.0):
    """Runs the jobs in order, returns (driver exit code, {label: code})."""
    os.makedirs(logdir, exist_ok=True)
    codes, any_cap = {}, False
    for job in jobs:
        code = run_one(job, logdir, stopfile, cap_s, poll)
        codes[job["label"]] = code
        if code == 4:
            return 4, codes
        if code == 5:
            any_cap = True
        elif code != 0:
            return 7, codes
    return (5 if any_cap else 0), codes


def dummy(label, body, env):
    return dict(label=label, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env)


def selftest():
    bad = 0
    env = dict(os.environ)
    good = "print('  start 0: max|x| 1.0e+33, bound on the smallest gain 1.0e-34, max|J x - v| 1.0e-16, 67 products', flush=True)\n"
    slow = "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")
        rc, codes = drive([dummy(f"r{i}", good, env) for i in range(6)], os.path.join(td, "l1"), stop, 30, 0.2)
        ok = rc == 0 and codes == {f"r{i}": 0 for i in range(6)}
        print(f"  six good runs: exit {rc} {codes} {'ok' if ok else 'WRONG'}")
        bad += not ok
        rc, codes = drive([dummy("r0", good, env), dummy("slow", slow, env), dummy("after", good, env)], os.path.join(td, "l2"), stop, 2.0, 0.2)
        ok = rc == 5 and codes == {"r0": 0, "slow": 5, "after": 0} and open(os.path.join(td, "l2", "slow.exit")).read().startswith("killed 5")
        print(f"  cap hit: exit {rc} {codes} (want slow 5, the run after it still done) {'ok' if ok else 'WRONG'}")
        bad += not ok
        rc, codes = drive([dummy("r0", good, env), dummy("crash", "import sys; sys.exit(3)", env), dummy("after", good, env)], os.path.join(td, "l3"), stop, 30, 0.2)
        ok = rc == 7 and "after" not in codes
        print(f"  a crash: exit {rc} {codes} (want 7, after not run) {'ok' if ok else 'WRONG'}")
        bad += not ok
        open(stop, "w").write("x")
        rc, codes = drive([dummy("r0", slow, env)], os.path.join(td, "l4"), stop, 30, 0.2)
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
    rc, codes = drive(jobs, logdir, os.path.join(HERE, "STOP_1022"), CAP_S)
    open(os.path.join(logdir, "run_1022.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
