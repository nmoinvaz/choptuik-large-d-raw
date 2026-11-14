#!/usr/bin/env python3
"""#739: the full system past D 112.75 with the octo-double corrector, from I726-win/L/anm_pin13_D112.7500.npz (M = 32).
usage: python run_739.py --selftest   (the stop rule on planted logs)
       python run_739.py ctl A          (names in order; logs/<name>.log, logs/<name>.exit, logs/run_739.log, output in <name>/)
       python run_739.py B              (only if A converged)
ctl: the octo-double polish of the D 112.75 state alone (--steps 0 --save_base 1), the control (a) and the cost of a step at this D.
A:   one attempt a = 1/8 to D 112.875 (--h_max 0.125 --a0 0.125 --steps 1).   B: one attempt a = 1/4 to D 113 from the D 112.75 state (--h_max 0.25 --a0 0.25 --steps 1).
An attempt that ends not converged is stopped by this driver at once (the process tree is killed after the attempt's summary line), so its halvings do not run; the log keeps each Newton step's max|F|.
Each job is capped (CAP seconds); the cap kills the tree and is logged.
Flags (#682's, as the issue gives them): --kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --reseed_o 3 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
          --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --elim_switch 0 --threads 4, cwd = the worktree's hp/, OPENBLAS_NUM_THREADS=1, BelowNormal."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = r"C:\Users\nathan\Source\choptuik-i710\hp"
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
STATE = "I726-win/L/anm_pin13_D112.7500.npz"
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
FLAGS = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--corrector", "od", "--tol_od", "1e-60", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
         "--reseed", "2", "--reseed_q", "1", "--reseed_o", "3", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04", "--elim_switch", "0"]
JOBS = {"ctl": (["--steps", "0", "--save_base", "1", "--h_max", "0.125", "--a0", "0.125"], 2400),
        "A": (["--steps", "1", "--h_max", "0.125", "--a0", "0.125"], 5400),
        "B": (["--steps", "1", "--h_max", "0.25", "--a0", "0.25"], 5400)}
OD_LINE = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    open(os.path.join(HERE, "logs", "run_739.log"), "a").write(line + "\n")


def kill_tree(pid):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)


def scan(lines, name, pending):
    """the stop rule on new log lines: returns (pending, stop_reason, messages). An attempt that ends not converged sets pending, and the
    attempt's summary line (it starts with 4 spaces and 'a ') then stops the run. The control `ctl` never stops this way."""
    msgs, reason = [], None
    for ln in lines:
        m = OD_LINE.search(ln)
        if m and name != "ctl" and m.group(3) == "not converged":
            pending = True
            msgs.append(f"{name}: attempt ended not converged, {m.group(1)} octo-double steps, max|F| {m.group(2)}")
        if pending and ln.startswith("    a "):
            reason = "the first attempt was refused, stopped before its halvings"
    return pending, reason, msgs


def selftest():
    bad = 0
    nc = ["      octo-double Newton: 9 steps, max|F| 2.7e-49, not converged; double-double |F| of its first two parts 9.3e-17"]
    ok_ = ["      octo-double Newton: 3 steps, max|F| 2.4e-62, converged; double-double |F| of its first two parts 9.3e-17"]
    summ = ["    a 0.125 -> D 112.875: predicted |F| 1.2e-14, od 9 steps -> 2.7e-49 (tol 1.0e-20), Delta 1.7"]
    cases = [("not converged, then its summary line", nc + summ, "A", True, True),
             ("not converged, summary line not yet printed", nc, "A", True, False),
             ("converged, then its summary line", ok_ + summ, "A", False, False),
             ("not converged in the control", nc + summ, "ctl", False, False)]
    for label, lines, name, want_pending, want_stop in cases:
        pending, reason, _ = scan(lines, name, False)
        good = (pending == want_pending) and ((reason is not None) == want_stop)
        print(f"  {label}: pending {pending}, stop {reason is not None} (expected {want_pending}, {want_stop}) {'ok' if good else 'WRONG'}")
        bad += not good
    # split across two reads: pending must carry over
    p1, r1, _ = scan(nc, "A", False)
    p2, r2, _ = scan(summ, "A", p1)
    good = p1 and r1 is None and r2 is not None
    print(f"  not converged line and its summary in two reads: stop {r2 is not None} {'ok' if good else 'WRONG'}")
    bad += not good
    print("selftest", "FAILED" if bad else "passed")
    return bad


def tail_state(path, seen):
    """new log lines since `seen` (bytes offset); returns (lines, new offset)"""
    with open(path, "rb") as f:
        f.seek(seen)
        data = f.read()
    return data.decode("utf-8", "replace").splitlines(), seen + len(data)


if "--selftest" in sys.argv:
    sys.exit(selftest())
for name in sys.argv[1:]:
    extra, cap = JOBS[name]
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    logp = os.path.join(HERE, "logs", f"{name}.log")
    cmd = [PY, "-u", "anm_run.py", RAW, out, "--state", STATE, *FLAGS, *extra, "--threads", "4"]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=HP, stdout=open(logp, "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {name} (pid {p.pid}) from {STATE}: {' '.join(extra)}")
    seen, stop_reason, pending = 0, None, False
    while p.poll() is None:
        time.sleep(3)
        lines, seen = tail_state(logp, seen)
        pending, reason, msgs = scan(lines, name, pending)
        for mm in msgs:
            say(mm)
        stop_reason = stop_reason or reason
        if stop_reason is None and time.time() - t0 > cap:
            stop_reason = f"the {cap} s cap"
        if stop_reason:
            kill_tree(p.pid)
            say(f"{name}: killed the tree, {stop_reason}")
            break
    rc = p.wait()
    open(os.path.join(HERE, "logs", f"{name}.exit"), "w").write(f"{rc}\n")
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s" + (f" ({stop_reason})" if stop_reason else ""))
    if stop_reason or rc != 0:
        say(f"{name} did not finish by itself, stopping the driver")
        sys.exit(2)
say("done " + " ".join(sys.argv[1:]))
