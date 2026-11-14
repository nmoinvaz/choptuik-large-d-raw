#!/usr/bin/env python3
"""#720: is start a's R(40.02) = 0.98 a product-cap artefact? rt_sigma.py --starts 3 --rough on I671-win/solves/k7_D40_D40.0201_32x121.npz,
first the control at --max_products 250, then the run at --max_products 1000. 2 BLAS threads, BelowNormal.

usage: python run_720.py                (logs/control_250.log, logs/main_1000.log, their .exit files, logs/run_720.log, logs/control_720.log)
       python run_720.py --selftest     the control comparison on #681's own log: identical must pass, and a 1% change of one bound must miss

Control (the issue's acceptance 1): the 250-product run reproduces #681's first three bounds (1.257e-34, 9.921e-34, 7.797e-34) to 3 digits. Rule fixed
before the run: a start's bound agrees if |a - b| / b <= 1e-3 against #681's printed value (4 significant digits). The reference is parsed from
I671/I681's log (I681-win/logs/K7_D40_rough.log, starts 0 to 2) and must equal the three numbers of the issue. Each start is compared as it appears;
the first miss stops the task (the control's process killed, logs/control_720_MISS.txt, exit 3, the 1000-product run is not started).
A file STOP_720 stops the task (exit 4); a run unfinished after CAP_H hours is killed (exit 5) and reported with what it printed."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"D:\choptuik-i721"
PY = r"C:\Users\nathan\Source\venv-t177\Scripts\python.exe"
RAW_PUSH = r"D:\choptuik-large-d-raw-push"
STATE = os.path.join(RAW_PUSH, "I671-win", "solves", "k7_D40_D40.0201_32x121.npz")
REF_LOG = os.path.join(RAW_PUSH, "I681-win", "logs", "K7_D40_rough.log")
ISSUE = {0: 1.257e-34, 1: 9.921e-34, 2: 7.797e-34}
NSTARTS = 3
TOL = 1e-3
THREADS = "2"
CAP_H = 7.0
LINE = re.compile(r"^\s+start (\d+): max\|x\| ([0-9.e+-]+), bound on the smallest gain ([0-9.e+-]+), max\|J x - v\| ([0-9.e+-]+), (\d+) products")


def parse(path):
    out = {}
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8", errors="replace"):
            m = LINE.match(ln)
            if m:
                out[int(m.group(1))] = (float(m.group(3)), int(m.group(5)))
    return out


def compare(run, ref, tol=TOL):
    rows = []
    for i in sorted(run):
        if i in ref:
            d = abs(run[i][0] - ref[i]) / ref[i]
            rows.append((i, run[i][0], ref[i], d, d <= tol))
    return rows


def selftest():
    ref = {i: v[0] for i, v in parse(REF_LOG).items() if i < NSTARTS}
    same_as_issue = all(abs(ref[i] - ISSUE[i]) / ISSUE[i] < 1e-9 for i in ISSUE)
    run = {i: (ref[i], 250) for i in ref}
    ok = compare(run, ref)
    okc = len(ok) == NSTARTS and all(r[4] for r in ok)
    run[1] = (ref[1] * 1.01, 250)
    mr = compare(run, ref)
    missc = [r[0] for r in mr if not r[4]] == [1]
    print(f"  reference parsed from #681's log equals the issue's three numbers: {same_as_issue}")
    print(f"  identical -> {'all ok' if okc else 'WRONG'}; start 1 changed by 1% -> misses {[r[0] for r in mr if not r[4]]} {'ok' if missc else 'WRONG'}")
    bad = (not same_as_issue) + (not okc) + (not missc)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def say(msg, name="run_720.log"):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(HERE, "logs", name), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def run_one(tag, max_products, ref, t_start):
    """Runs rt_sigma; for the control compares each start to ref as it appears. Returns 0 or the stop code."""
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    log = os.path.join(HERE, "logs", f"{tag}.log")
    cmd = [PY, "-u", os.path.join(HERE, "rt_launch.py"), os.path.join(WT, "solver", "rt", "rt_sigma.py"), STATE, "--starts", str(NSTARTS), "--rough", "--max_products", str(max_products)]
    p = subprocess.Popen(cmd, cwd=WT, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start {tag} (pid {p.pid}) --max_products {max_products}, {THREADS} BLAS threads")
    seen, code = 0, 0
    while True:
        time.sleep(10)
        if ref is not None:
            for i, b, r, d, ok in compare(parse(log), ref):
                if i >= seen:
                    say(f"control start {i}: {b:.3e} vs #681 {r:.3e}, relative difference {d:.1e}, {'ok' if ok else 'MISS'}", "control_720.log")
                    seen = i + 1
                    if not ok and not code:
                        code = 3
                        open(os.path.join(HERE, "logs", "control_720_MISS.txt"), "w").write(f"start {i}: {b:.4e} vs #681 {r:.4e}, relative difference {d:.2e}\n")
        if os.path.exists(os.path.join(HERE, "STOP_720")):
            code = code or 4
        if time.time() - t_start > CAP_H * 3600:
            code = code or 5
        if code:
            kill_tree(p)
            open(os.path.join(HERE, "logs", f"{tag}.exit"), "w").write(f"killed {code}\n")
            say(f"{tag} killed (code {code}: 3 control miss, 4 STOP_720, 5 {CAP_H} h cap)")
            return code
        rc = p.poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", f"{tag}.exit"), "w").write(f"{rc}\n")
            say(f"{tag} exit {rc}")
            return 0 if rc == 0 else 6


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    if not os.path.exists(STATE):
        say(f"missing state {STATE}")
        sys.exit(2)
    ref = {i: v[0] for i, v in parse(REF_LOG).items() if i < NSTARTS}
    if len(ref) != NSTARTS or not all(abs(ref[i] - ISSUE[i]) / ISSUE[i] < 1e-9 for i in ISSUE):
        say("reference from #681's log does not equal the issue's numbers")
        sys.exit(2)
    t0 = time.time()
    rc = run_one("control_250", 250, ref, t0)
    if rc:
        say(f"task stopped after the control, code {rc}; the 1000-product run was not started")
        sys.exit(rc)
    rc = run_one("main_1000", 1000, None, t0)
    say(f"task done, code {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
