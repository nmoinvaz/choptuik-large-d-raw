#!/usr/bin/env python3
"""#951 (win): rt_sigma.py with 48 rough starts on start c's K = 7 and K = 0 states at D 40.02, both at once, 2 BLAS threads each, BelowNormal. From I943-win/run_943.py
without its #681 control (a new pair has no earlier log) and without the adoption: a nonzero exit, a cap or a stop ends that run only.

usage: python run_951.py --t0 "YYYY-MM-DD HH:MM:SS"     (t0 = the start of the solves, UTC; logs/K7c_D40_rough.log, logs/K0c_D40_rough.log, their .exit files, logs/run_951.log, logs/run_951.exit)
       python run_951.py --selftest                       the driver on dummy children: a good one runs to exit 0, one over its own cap and one over the deadline get code 5, STOP_951 gives 4

Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 48 --rough, cwd = <worktree>/solver/rt (main a80697d7, solver/rt unchanged since 5135cdeb).
The states are the solves of run_951_solves.py (solves/). Stop rules (the issue's 30 h): a run unfinished at t0 + 30 h is killed and reported with what it printed (code 5); the K 0 run
also after 10 h of its own time (code 5). A file STOP_951 in this folder stops what still runs (code 4).
Exit codes: <run>_rough.exit holds 'exit N' or 'killed N (...)'; logs/run_951.exit holds 0 if both runs exited 0, else the first code that was not 0 in the order K 7, K 0."""
import calendar
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i951"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
# label, state, own cap in hours (None: only the deadline)
JOBS = [("K7c_D40", os.path.join(HERE, "solves", "k7c_D40_D40.0201_32x121.npz"), None),
        ("K0c_D40", os.path.join(HERE, "solves", "k0c_D40_mutnorows_D40.0201_32x121.npz"), 10.0)]
NSTARTS = 48
THREADS = "2"
DEADLINE_H = 30.0
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "run_951.log"), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def drive(jobs, logdir, stopfile, deadline, poll=10.0):
    """jobs: dicts label, cmd, cwd, env, own_cap_s (or None). deadline: epoch seconds. Returns {label: code} (0 normal, 4 STOP, 5 cap or deadline, else the exit code)."""
    os.makedirs(logdir, exist_ok=True)
    run, codes = {}, {}
    for j in jobs:
        lab = j["label"]
        p = subprocess.Popen(j["cmd"], cwd=j["cwd"], stdout=open(os.path.join(logdir, f"{lab}_rough.log"), "w"), stderr=subprocess.STDOUT, env=j["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
        run[lab] = (p, j, time.time())
        say(logdir, f"start {lab} (pid {p.pid}), deadline {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(deadline))} UTC, own cap {j['own_cap_s'] / 3600 if j['own_cap_s'] else 'none'} h")

    def finish(lab, code, text):
        open(os.path.join(logdir, f"{lab}_rough.exit"), "w").write(text + "\n")
        say(logdir, f"{lab} {text} after {time.time() - run[lab][2]:.0f} s")
        codes[lab] = code
        del run[lab]

    while run:
        time.sleep(poll)
        for lab in list(run):
            p, j, t_start = run[lab]
            if os.path.exists(stopfile):
                kill_tree(p)
                finish(lab, 4, "killed 4 (STOP_951)")
            elif time.time() > deadline:
                kill_tree(p)
                finish(lab, 5, "killed 5 (30 h deadline)")
            elif j["own_cap_s"] and time.time() - t_start > j["own_cap_s"]:
                kill_tree(p)
                finish(lab, 5, f"killed 5 (own cap {j['own_cap_s'] / 3600:.2f} h)")
            else:
                rc = p.poll()
                if rc is not None:
                    finish(lab, rc, f"exit {rc}")
    return codes


def dummy_jobs(env, n_good=6, dt=0.3):
    good = ("import time\nfor i in range(%d):\n    print('  start %%d: max|x| 1.0e+33, bound on the smallest gain 1.0e-34, max|J x - v| 1.0e-15, 67 products' %% i, flush=True)\n"
            "    time.sleep(%r)\n" % (n_good, dt))
    slow = "import time\ntime.sleep(60)\n"
    base = dict(cwd=tempfile.gettempdir(), env=env)
    return [dict(label="good", cmd=[sys.executable, "-c", good], own_cap_s=None, **base),
            dict(label="owncap", cmd=[sys.executable, "-c", slow], own_cap_s=2.0, **base),
            dict(label="late", cmd=[sys.executable, "-c", slow], own_cap_s=None, **base)]


def selftest():
    bad = 0
    env = dict(os.environ)
    with tempfile.TemporaryDirectory() as td:
        codes = drive(dummy_jobs(env), os.path.join(td, "logs"), os.path.join(td, "STOP"), time.time() + 4.0, poll=0.3)
        want = {"good": 0, "owncap": 5, "late": 5}
        ok = codes == want
        n = sum(1 for ln in open(os.path.join(td, "logs", "good_rough.log")) if "start " in ln)
        why = open(os.path.join(td, "logs", "late_rough.exit")).read().strip(), open(os.path.join(td, "logs", "owncap_rough.exit")).read().strip()
        okt = "deadline" in why[0] and "own cap" in why[1]
        print(f"  deadline and own cap: codes {codes} (want {want}) {'ok' if ok else 'WRONG'}; good printed {n} of 6 starts {'ok' if n == 6 else 'WRONG'}; kill reasons {why} {'ok' if okt else 'WRONG'}")
        bad += (not ok) + (n != 6) + (not okt)
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")
        open(stop, "w").write("x")
        codes = drive(dummy_jobs(env)[1:], os.path.join(td, "logs"), stop, time.time() + 60, poll=0.3)
        ok = codes == {"owncap": 4, "late": 4}
        print(f"  STOP file: codes {codes} (want 4 for both) {'ok' if ok else 'WRONG'}")
        bad += not ok
    with tempfile.TemporaryDirectory() as td:
        j = dummy_jobs(env)[0]
        j["cmd"] = [sys.executable, "-c", "import sys; sys.exit(3)"]
        codes = drive([j], os.path.join(td, "logs"), os.path.join(td, "STOP"), time.time() + 60, poll=0.3)
        ok = codes == {"good": 3}
        print(f"  a run's own nonzero exit: codes {codes} (want 3) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    t0 = calendar.timegm(time.strptime(sys.argv[sys.argv.index("--t0") + 1], "%Y-%m-%d %H:%M:%S"))
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    jobs = []
    for lab, state, cap_h in JOBS:
        if not os.path.exists(state):
            say(logdir, f"missing state {state}")
            sys.exit(2)
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(RT, "rt_sigma.py"), state, "--starts", str(NSTARTS), "--rough"]
        jobs.append({"label": lab, "cmd": cmd, "cwd": RT, "env": env, "own_cap_s": cap_h * 3600 if cap_h else None})
    codes = drive(jobs, logdir, os.path.join(HERE, "STOP_951"), t0 + DEADLINE_H * 3600)
    rc = next((codes[l] for l, _, _ in JOBS if codes[l] != 0), 0)
    open(os.path.join(logdir, "run_951.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
