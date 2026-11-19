#!/usr/bin/env python3
"""#1029 (win): the four amp_flint_par.py runs of the issue (K 25, J 750 and 1000, at wf 0.100532 and 0.065740), at most two at once, 3 processes each,
BelowNormal (the class the spawned workers inherit; nice 10 on Linux), a 4 h cap per run.

usage: python run_1029.py                 (venv-t151 python, from this folder; writes logs/<label>.log, logs/<label>.exit, logs/run_1029.log, logs/run_1029.exit, logs/status_1029.log)
       python run_1029.py --selftest      the scheduler on dummy children

Job (cwd <worktree>/solver/inner_amp, main 4a056a28):
    python -u amp_flint_par.py WF 25 J 640 --procs 3 --fit phys --mf 6:12 --out <this folder>/sigF_wWF_K25_J<J>.json
Queue (two slots, the next job starts when a slot frees): wf 0.100532 J 750, wf 0.100532 J 1000, wf 0.065740 J 750, wf 0.065740 J 1000.
Stop rules: a run over 4 h is killed by its exact pid (taskkill /T /F /PID: that pid and its spawned workers, nothing else) and reported with the order
its OUT.partial.json reached (exit file 'killed 5 (cap 4 h), order k_done ...'); the other run goes on and the queue goes on. A run that exits nonzero other than by the cap
(exit file 'exit N') stops new starts (driver exit 7), the run still going is left to finish; a file STOP_1029 in this folder kills what runs (driver exit 4).
logs/status_1029.log: every 10 min free memory, each running job's pid, age and order reached.
Exit codes of logs/run_1029.exit: 0 all four ran to exit 0, 5 at least one cap hit and no failure, 7 a run failed, 4 stopped."""
import ctypes
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i1029"
INNER = os.path.join(WT, "solver", "inner_amp")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
ORDER = [("0.100532", 750), ("0.100532", 1000), ("0.065740", 750), ("0.065740", 1000)]
CAP_S = 4.0 * 3600
SLOTS = 2
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg, name="run_1029.log"):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, name), "a") as f:
        f.write(line + "\n")


def free_gb():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("load", ctypes.c_ulong), ("tot", ctypes.c_ulonglong), ("avail", ctypes.c_ulonglong),
                    ("t1", ctypes.c_ulonglong), ("t2", ctypes.c_ulonglong), ("t3", ctypes.c_ulonglong), ("t4", ctypes.c_ulonglong), ("t5", ctypes.c_ulonglong)]
    m = M()
    m.l = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.avail / 2**30, m.tot / 2**30


def kill_tree(pid):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)


def reached(partial):
    try:
        return json.load(open(partial))["k_done"]
    except Exception:
        return None


def drive(jobs, logdir, stopfile, cap_s, slots=SLOTS, poll=10.0, status_s=600.0):
    """jobs: dicts label, cmd, cwd, env, partial. Returns (driver exit code, {label: code})."""
    os.makedirs(logdir, exist_ok=True)
    queue, running, codes = list(jobs), {}, {}
    any_cap = failed = stopped = False
    last_status = 0.0
    while queue or running:
        if os.path.exists(stopfile) and not stopped:
            stopped = True
            for lab, r in list(running.items()):
                kill_tree(r["p"].pid)
                r["forced"] = (4, f"killed 4 (STOP_1029), order reached {reached(r['job']['partial'])}")
        while queue and len(running) < slots and not failed and not stopped:
            job = queue.pop(0)
            p = subprocess.Popen(job["cmd"], cwd=job["cwd"], stdout=open(os.path.join(logdir, f"{job['label']}.log"), "w"), stderr=subprocess.STDOUT,
                                 env=job["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
            running[job["label"]] = dict(p=p, t=time.time(), job=job, forced=None)
            say(logdir, f"start {job['label']} (pid {p.pid}), cap {cap_s / 3600:.2f} h, {len(running)} running")
        if stopped or failed:
            queue = []
        time.sleep(poll)
        for lab, r in list(running.items()):
            p, age = r["p"], time.time() - r["t"]
            if r["forced"]:
                code, text = r["forced"]
                p.wait()
            elif age > cap_s:
                kill_tree(p.pid)
                p.wait()
                code, text = 5, f"killed 5 (cap {cap_s / 3600:.2f} h), order reached {reached(r['job']['partial'])}"
                any_cap = True
            else:
                rc = p.poll()
                if rc is None:
                    continue
                code, text = rc, f"exit {rc}"
                if rc != 0:
                    failed = True
            open(os.path.join(logdir, f"{lab}.exit"), "w").write(text + "\n")
            say(logdir, f"{lab} {text} after {age:.0f} s (pid {p.pid})")
            codes[lab] = code
            del running[lab]
        if time.time() - last_status >= status_s and running:
            last_status = time.time()
            fr, tot = free_gb()
            say(logdir, f"free {fr:.1f} of {tot:.1f} GiB; " + "; ".join(f"{lab} pid {r['p'].pid} age {time.time() - r['t']:.0f} s order {reached(r['job']['partial'])}" for lab, r in running.items()), "status_1029.log")
    rc = 4 if stopped else (7 if failed else (5 if any_cap else 0))
    return rc, codes


def dummy(label, body, env, partial=None):
    return dict(label=label, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env, partial=partial or os.path.join(tempfile.gettempdir(), "no_such_partial.json"))


def selftest():
    bad = 0
    env = dict(os.environ)
    good = "import time\ntime.sleep(1.5)\nprint('done', flush=True)\n"
    slow = "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")
        t = time.time()
        rc, codes = drive([dummy(f"r{i}", good, env) for i in range(4)], os.path.join(td, "l1"), stop, 30, 2, 0.2, 1.0)
        dur = time.time() - t
        starts = [l.split()[4] for l in open(os.path.join(td, "l1", "run_1029.log")) if " start " in l]
        # four 1.5 s jobs, two slots: two rounds (about 3 s), never one round (1.5 s) nor four in a row (6 s)
        ok = rc == 0 and codes == {f"r{i}": 0 for i in range(4)} and 2.6 < dur < 5.0 and starts == ["r0", "r1", "r2", "r3"]
        print(f"  four good runs, two slots: exit {rc}, {dur:.1f} s (two rounds: 2.6 to 5 s) {'ok' if ok else 'WRONG'}")
        bad += not ok
        part = os.path.join(td, "slow.partial.json")
        json.dump({"k_done": 9}, open(part, "w"))
        rc, codes = drive([dummy("r0", good, env), dummy("slow", slow, env, part), dummy("after", good, env)], os.path.join(td, "l2"), stop, 3.0, 2, 0.2, 1.0)
        ex = open(os.path.join(td, "l2", "slow.exit")).read()
        ok = rc == 5 and codes == {"r0": 0, "slow": 5, "after": 0} and "killed 5" in ex and "order reached 9" in ex
        print(f"  cap hit: exit {rc} {codes}, exit file '{ex.strip()}' (want slow killed 5 with order 9, the others done) {'ok' if ok else 'WRONG'}")
        bad += not ok
        rc, codes = drive([dummy("crash", "import sys; sys.exit(3)", env), dummy("r1", good, env), dummy("after", good, env)], os.path.join(td, "l3"), stop, 30, 2, 0.2, 1.0)
        ok = rc == 7 and "after" not in codes and codes.get("crash") == 3 and codes.get("r1") == 0
        print(f"  a crash with a run beside it: exit {rc} {codes} (want 7, r1 finished, after not started) {'ok' if ok else 'WRONG'}")
        bad += not ok
        import threading
        threading.Timer(1.5, lambda: open(stop, "w").write("x")).start()      # the file appears after both runs started
        rc, codes = drive([dummy("r0", slow, env), dummy("r1", slow, env)], os.path.join(td, "l4"), stop, 30, 2, 0.2, 1.0)
        ok = rc == 4 and codes == {"r0": 4, "r1": 4}
        print(f"  STOP file: exit {rc} {codes} (want 4, both killed) {'ok' if ok else 'WRONG'}")
        bad += not ok
    fr, tot = free_gb()
    ok = 0 < fr < tot
    print(f"  free memory read: {fr:.1f} of {tot:.1f} GiB {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    ver = subprocess.run([PY, "-I", "-c", "import flint, mpmath, sys; print('python-flint', flint.__version__, 'mpmath', mpmath.__version__, 'python', sys.version.split()[0])"],
                         capture_output=True, text=True).stdout.strip()
    say(logdir, f"{ver}; code worktree {WT} at {subprocess.run(['git', '-C', WT, 'rev-parse', '--short=8', 'HEAD'], capture_output=True, text=True).stdout.strip()}")
    jobs = []
    for wf, J in ORDER:
        out = os.path.join(HERE, f"sigF_w{wf}_K25_J{J}.json")
        jobs.append(dict(label=f"w{wf}_J{J}", cmd=[PY, "-u", "amp_flint_par.py", wf, "25", str(J), "640", "--procs", "3", "--fit", "phys", "--mf", "6:12", "--out", out],
                         cwd=INNER, env=env, partial=out + ".partial.json"))
    rc, codes = drive(jobs, logdir, os.path.join(HERE, "STOP_1029"), CAP_S)
    open(os.path.join(logdir, "run_1029.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
