#!/usr/bin/env python3
"""#943 (win): rt_sigma.py with 48 rough starts on start a's K = 7 and K = 0 states at D 40.02, both at once, 2 BLAS threads each, BelowNormal, with the control
of the acceptance rule watched while they run. From I721-win/run_721.py with two jobs: a miss, a cap or a nonzero exit stops that run only.

usage: python run_943.py                (logs/K7_D40_rough.log, logs/K0_D40_rough.log, their .exit files, logs/run_943.log, logs/control_943.log, logs/run_943.exit)
       python run_943.py --selftest     the control comparison on #681's own logs (identical must pass, a 1% change of one start must miss), and the driver on dummy
                                        children (one good, one with a 1% change at start 3, one over its cap): the bad one is killed with code 3, the capped one with 5,
                                        and the good one runs on to exit 0

Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 48 --rough, cwd = <worktree>/solver/rt (main 09ffaa1e, solver/rt unchanged since 5135cdeb).
The states are #671's, read in place from this raw clone (I671-win/solves/). The reference bounds are #681's logs, read in place from the push worktree.

Control (acceptance 1 of the issue): the first 12 bounds of each run reproduce #681's logs (I681-win/logs/K7_D40_rough.log, K0_D40_rough.log) to 3 digits. Rule fixed
before the runs: a start's bound agrees if |a - b| / b <= 1e-3 against #681's printed value (4 significant digits, so printing alone is up to 5e-4). Each of the first 12
starts is compared as it appears; the first miss of a run kills that run (logs/control_943_MISS_<run>.txt, code 3) and leaves the other running. A run unfinished after its cap
(K 7 18 h, K 0 10 h, the coordinator's) is killed and reported with what it printed (code 5). A file STOP_943 in this folder stops what still runs (code 4).
Exit codes: <run>_rough.exit holds the run's code (0 normal, rt_sigma's own nonzero code, or 'killed N'); logs/run_943.exit holds 0 if both runs exited 0, else the first code
that was not 0 in the order K 7, K 0."""
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i943"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
R = r"C:\Users\nathan\Source\choptuik-large-d-raw"
RAW_PUSH = r"C:\Users\nathan\Source\choptuik-large-d-raw-754"
I681 = os.path.join(RAW_PUSH, "I681-win")
# label, state (read in place from R), cap in hours
JOBS = [("K7_D40", os.path.join(R, "I671-win", "solves", "k7_D40_D40.0201_32x121.npz"), 18.0),
        ("K0_D40", os.path.join(R, "I671-win", "solves", "k0_D40_mutnorows_D40.0201_32x121.npz"), 10.0)]
NSTARTS = 48
NCTRL = 12
TOL = 1e-3
THREADS = "2"
LINE = re.compile(r"^\s+start (\d+): max\|x\| ([0-9.e+-]+), bound on the smallest gain ([0-9.e+-]+), max\|J x - v\| ([0-9.e+-]+), (\d+) products")
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def bounds_of(path):
    out = {}
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8", errors="replace"):
            m = LINE.match(ln)
            if m:
                out[int(m.group(1))] = float(m.group(3))
    return out


def compare(run, ref, tol=TOL, n=NCTRL):
    """[(i, run bound, ref bound, relative difference, ok)] for the starts < n the run has printed."""
    rows = []
    for i in sorted(run):
        if i < n and i in ref:
            d = abs(run[i] - ref[i]) / ref[i]
            rows.append((i, run[i], ref[i], d, d <= tol))
    return rows


def say(logdir, msg, name="run_943.log"):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, name), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def drive(jobs, logdir, stopfile, poll=10.0):
    """jobs: dicts label, cmd, cwd, env, ref (start -> bound), cap_s. Runs them all at once. Returns {label: code} (0 normal, 3 control miss, 4 STOP, 5 cap, else the exit code)."""
    os.makedirs(logdir, exist_ok=True)
    t0 = time.time()
    run = {}
    for j in jobs:
        lab = j["label"]
        log = os.path.join(logdir, f"{lab}_rough.log")
        p = subprocess.Popen(j["cmd"], cwd=j["cwd"], stdout=open(log, "w"), stderr=subprocess.STDOUT, env=j["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
        run[lab] = {"p": p, "seen": 0, "job": j, "log": log}
        say(logdir, f"start {lab} (pid {p.pid}), cap {j['cap_s'] / 3600:.2f} h")
    codes = {}

    def finish(lab, code, text):
        open(os.path.join(logdir, f"{lab}_rough.exit"), "w").write(text + "\n")
        say(logdir, f"{lab} {text} after {time.time() - t0:.0f} s")
        codes[lab] = code
        del run[lab]

    while run:
        time.sleep(poll)
        for lab in list(run):
            r = run[lab]
            j, p = r["job"], r["p"]
            miss = None
            for i, b, ref, d, ok in compare(bounds_of(r["log"]), j["ref"]):
                if i >= r["seen"]:
                    say(logdir, f"control {lab} start {i}: {b:.3e} vs #681 {ref:.3e}, relative difference {d:.1e}, {'ok' if ok else 'MISS'}", "control_943.log")
                    r["seen"] = i + 1
                    if not ok and miss is None:
                        miss = (i, b, ref, d)
            if miss:
                kill_tree(p)
                open(os.path.join(logdir, f"control_943_MISS_{lab}.txt"), "w").write(f"{lab} start {miss[0]}: {miss[1]:.4e} vs #681 {miss[2]:.4e}, relative difference {miss[3]:.2e}\n")
                finish(lab, 3, "killed 3 (control miss)")
            elif os.path.exists(stopfile):
                kill_tree(p)
                finish(lab, 4, "killed 4 (STOP_943)")
            elif time.time() - t0 > j["cap_s"]:
                kill_tree(p)
                finish(lab, 5, f"killed 5 (cap {j['cap_s'] / 3600:.2f} h)")
            else:
                rc = p.poll()
                if rc is not None:
                    finish(lab, rc, f"exit {rc}")
    return codes


def selftest():
    bad = 0
    for lab, _, _ in JOBS:
        ref = bounds_of(os.path.join(I681, "logs", f"{lab}_rough.log"))
        assert len(ref) == NCTRL, f"{lab}: {len(ref)} reference starts"
        same = compare(dict(ref), ref)
        okc = len(same) == NCTRL and all(r[4] for r in same)
        mut = dict(ref)
        mut[3] *= 1.01
        misses = [r[0] for r in compare(mut, ref) if not r[4]]
        print(f"  {lab}: identical -> {'all ok' if okc else 'WRONG'}; start 3 changed by 1% -> misses {misses} {'ok' if misses == [3] else 'WRONG'}")
        bad += (not okc) + (misses != [3])
    # the driver on dummy children: good (matches the reference), bad (start 3 changed by 1%), slow (over a 3 s cap)
    ref = {i: 1e-34 * (1 + 0.1 * i) for i in range(NCTRL)}
    child = ("import sys,time\nref=%r\nbad=int(sys.argv[1])\n"
             "for i in range(14):\n    b=ref.get(i,1e-34)*(1.01 if (bad and i==3) else 1.0)\n"
             "    print('  start %%d: max|x| 1.000e+33, bound on the smallest gain %%.3e, max|J x - v| 1.0e-15, 250 products'%%(i,b),flush=True)\n"
             "    time.sleep(0.6 if i<12 else 0.1)\n" % ref)
    slow = "import time\ntime.sleep(60)\n"
    env = dict(os.environ)
    with tempfile.TemporaryDirectory() as td:
        jobs = [{"label": "good", "cmd": [sys.executable, "-c", child, "0"], "cwd": td, "env": env, "ref": ref, "cap_s": 120},
                {"label": "bad", "cmd": [sys.executable, "-c", child, "1"], "cwd": td, "env": env, "ref": ref, "cap_s": 120},
                {"label": "slow", "cmd": [sys.executable, "-c", slow], "cwd": td, "env": env, "ref": ref, "cap_s": 3}]
        sys.stdout.flush()
        codes = drive(jobs, os.path.join(td, "logs"), os.path.join(td, "STOP"), poll=0.4)
        want = {"good": 0, "bad": 3, "slow": 5}
        okd = codes == want
        good_starts = len(bounds_of(os.path.join(td, "logs", "good_rough.log")))
        okg = good_starts == 14
        okm = os.path.exists(os.path.join(td, "logs", "control_943_MISS_bad.txt")) and not os.path.exists(os.path.join(td, "logs", "control_943_MISS_good.txt"))
        print(f"  driver on dummy children: codes {codes} (want {want}) {'ok' if okd else 'WRONG'}; the good one printed {good_starts} of 14 starts {'ok' if okg else 'WRONG'}; "
              f"MISS file for bad only {'ok' if okm else 'WRONG'}")
        bad += (not okd) + (not okg) + (not okm)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    jobs = []
    for lab, state, cap_h in JOBS:
        if not os.path.exists(state):
            say(logdir, f"missing state {state}")
            sys.exit(2)
        ref = bounds_of(os.path.join(I681, "logs", f"{lab}_rough.log"))
        if len(ref) != NCTRL:
            say(logdir, f"{lab}: {len(ref)} reference starts, expected {NCTRL}")
            sys.exit(2)
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(RT, "rt_sigma.py"), state, "--starts", str(NSTARTS), "--rough"]
        jobs.append({"label": lab, "cmd": cmd, "cwd": RT, "env": env, "ref": ref, "cap_s": cap_h * 3600})
    codes = drive(jobs, logdir, os.path.join(HERE, "STOP_943"))
    rc = next((codes[l] for l, _, _ in JOBS if codes[l] != 0), 0)
    open(os.path.join(logdir, "run_943.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
