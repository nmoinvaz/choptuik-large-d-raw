#!/usr/bin/env python3
"""#721: rt_sigma.py with 48 rough starts on #701's two start-b states (K = 7 and K = 0 at D 40.02), both at once, 4 BLAS threads each (8 busy
threads), BelowNormal, with the control of the acceptance rule watched while they run.

usage: python run_721.py                (logs/<label>_rough.log, logs/<label>_rough.exit, logs/run_721.log, logs/control_721.log)
       python run_721.py --selftest     the control comparison on #701's own logs: identical must pass, and a 1% change of one start's reference must miss

Job: python rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --starts 48 --rough, cwd = the worktree root (main 989e103c). The states are #701's,
read in place from the raw repository's push checkout (I701-win/solves/, commit recorded in README.md).

Control (acceptance 1 of the issue): the first 12 bounds of each run reproduce #701's logs/<label>_rough.log to 3 digits. Rule fixed before the run: a start's
bound agrees if |a - b| / b <= 1e-3 against #701's printed value (4 significant digits, so printing alone is up to 5e-4). Each of the first 12 starts is
compared as it appears; the first miss stops that task (both jobs killed, logs/control_721_MISS.txt written, exit 3), as the coordinator ordered.
A run unfinished after CAP_H hours is killed and reported with what it printed. A file STOP_721 in this folder stops both jobs (exit 4)."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"D:\choptuik-i721"
PY = r"C:\Users\nathan\Source\venv-t177\Scripts\python.exe"
RAW_PUSH = r"D:\choptuik-large-d-raw-push"
I701 = os.path.join(RAW_PUSH, "I701-win")
JOBS = [("K7b_D40", "k7b_D40_D40.0201_32x121.npz"), ("K0b_D40", "k0b_D40_mutnorows_D40.0201_32x121.npz")]
NSTARTS = 48
NCTRL = 12
TOL = 1e-3
THREADS = "4"
CAP_H = 7.0
LINE = re.compile(r"^\s+start (\d+): max\|x\| ([0-9.e+-]+), bound on the smallest gain ([0-9.e+-]+), max\|J x - v\| ([0-9.e+-]+), (\d+) products")


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


def selftest():
    bad = 0
    for label, _ in JOBS:
        ref = bounds_of(os.path.join(I701, "logs", f"{label}_rough.log"))
        assert len(ref) == NCTRL, f"{label}: {len(ref)} reference starts"
        same = compare(dict(ref), ref)
        okc = len(same) == NCTRL and all(r[4] for r in same)
        mut = dict(ref)
        mut[3] *= 1.01
        mr = compare(mut, ref)
        missc = [r[0] for r in mr if not r[4]] == [3]
        print(f"  {label}: identical -> {'all ok' if okc else 'WRONG'}; start 3 changed by 1% -> misses {[r[0] for r in mr if not r[4]]} {'ok' if missc else 'WRONG'}")
        bad += (not okc) + (not missc)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def say(msg, name="run_721.log"):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(HERE, "logs", name), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    refs = {}
    for label, st in JOBS:
        if not os.path.exists(os.path.join(I701, "solves", st)):
            say(f"missing state {st}")
            sys.exit(2)
        refs[label] = bounds_of(os.path.join(I701, "logs", f"{label}_rough.log"))
        if len(refs[label]) != NCTRL:
            say(f"{label}: {len(refs[label])} reference starts, expected {NCTRL}")
            sys.exit(2)
    running, t0, seen = [], time.time(), {l: 0 for l, _ in JOBS}
    for label, st in JOBS:
        cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_sigma.py"), os.path.join(I701, "solves", st), "--starts", str(NSTARTS), "--rough"]
        p = subprocess.Popen(cmd, cwd=WT, stdout=open(os.path.join(HERE, "logs", f"{label}_rough.log"), "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
        running.append((p, label))
        say(f"start {label} (pid {p.pid}) {st}, {THREADS} BLAS threads")
    verdict = None
    while running:
        time.sleep(10)
        for label, _ in JOBS:
            rows = compare(bounds_of(os.path.join(HERE, "logs", f"{label}_rough.log")), refs[label])
            for i, b, r, d, ok in rows:
                if i >= seen[label]:
                    say(f"control {label} start {i}: {b:.3e} vs #701 {r:.3e}, relative difference {d:.1e}, {'ok' if ok else 'MISS'}", "control_721.log")
                    seen[label] = i + 1
                    if not ok and verdict is None:
                        verdict = 3
                        open(os.path.join(HERE, "logs", "control_721_MISS.txt"), "w").write(f"{label} start {i}: {b:.4e} vs #701 {r:.4e}, relative difference {d:.2e}\n")
        if os.path.exists(os.path.join(HERE, "STOP_721")):
            verdict = verdict or 4
        if time.time() - t0 > CAP_H * 3600:
            verdict = verdict or 5
        if verdict:
            for p, label in running:
                kill_tree(p)
                say(f"{label} killed (code {verdict}: 3 control miss, 4 STOP_721, 5 {CAP_H} h cap)")
                open(os.path.join(HERE, "logs", f"{label}_rough.exit"), "w").write(f"killed {verdict}\n")
            say(f"stopped with code {verdict}")
            sys.exit(verdict)
        for r in list(running):
            rc = r[0].poll()
            if rc is not None:
                open(os.path.join(HERE, "logs", f"{r[1]}_rough.exit"), "w").write(f"{rc}\n")
                say(f"{r[1]} exit {rc} after {time.time() - t0:.0f} s")
                running.remove(r)
    say("all done")


if __name__ == "__main__":
    main()
