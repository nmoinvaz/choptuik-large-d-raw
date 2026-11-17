#!/usr/bin/env python3
"""#745: start a's twelve rough bounds at D 40.02 at 1000 products. rt_sigma.py --starts 12 --rough --max_products 1000 on I671-win/solves/k7_D40_D40.0201_32x121.npz.
2 BLAS threads, nice 10, own session. Adapted from I720-win2/run_720.py (Windows) for Linux.

usage: python run_745.py                (logs/main_1000.log, logs/main_1000.exit, logs/run_745.log, logs/control_745.log, logs/resource.log)
       python run_745.py --selftest     the control comparison on #681's own log: identical must pass, a 1% change of one printed bound must miss

Control (the issue's acceptance 1): starts 0 to 2 print #720's bounds (1.257e-34, 9.921e-34, 7.797e-34). Rule, fixed before the run: the printed number (four significant digits of the
log line) equals the issue's. Each start is compared as it appears; the first miss stops the task (the process group killed, logs/control_745_MISS.txt, exit 3).
A file STOP_745 stops the task (exit 4); a run unfinished after CAP_H hours is killed (exit 5) and reported with what it printed."""
import os
import re
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
WT = os.path.join(HOME, "Source", "choptuik-large-d-745")
PY = os.path.join(HOME, "Source", "venv-choptuik", "bin", "python")
MDSITE = os.path.join(HOME, "Source", "md-site-745")
RAW = os.path.join(HOME, "Source", "choptuik-large-d-raw")
LAUNCH = os.path.join(RAW, "I720-win2", "rt_launch.py")
STATE = os.path.join(RAW, "I671-win", "solves", "k7_D40_D40.0201_32x121.npz")
REF_LOG = os.path.join(RAW, "I681-win", "logs", "K7_D40_rough.log")
ISSUE = {0: "1.257e-34", 1: "9.921e-34", 2: "7.797e-34"}
NSTARTS = 12
MAXPROD = 1000
THREADS = "2"
CAP_H = 12.0
LINE = re.compile(r"^\s+start (\d+): max\|x\| ([0-9.e+-]+), bound on the smallest gain ([0-9.e+-]+), max\|J x - v\| ([0-9.e+-]+), (\d+) products")


def parse(path):
    """start -> (printed bound string, products)"""
    out = {}
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8", errors="replace"):
            m = LINE.match(ln)
            if m:
                out[int(m.group(1))] = (m.group(3), int(m.group(5)))
    return out


def compare(run, ref):
    """rows (start, printed, issue, relative difference, equal as printed) for the starts of run that have a reference"""
    rows = []
    for i in sorted(run):
        if i in ref:
            d = abs(float(run[i][0]) - float(ref[i])) / float(ref[i])
            rows.append((i, run[i][0], ref[i], d, run[i][0] == ref[i]))
    return rows


def selftest():
    ref = {i: v[0] for i, v in parse(REF_LOG).items() if i < 3}
    same_as_issue = ref == ISSUE
    run = {i: (ref[i], 250) for i in ref}
    ok = compare(run, ref)
    okc = len(ok) == 3 and all(r[4] for r in ok)
    run[1] = ("%.3e" % (float(ref[1]) * 1.01), 250)
    mr = compare(run, ref)
    missc = [r[0] for r in mr if not r[4]] == [1]
    run[1] = ("%.3e" % (float(ref[1]) * 1.0009), 250)
    near = [r[0] for r in compare(run, ref) if not r[4]] == [1]
    print(f"  reference parsed from #681's log equals the issue's three printed numbers: {same_as_issue}")
    print(f"  identical -> {'all ok' if okc else 'WRONG'}; start 1 changed by 1% -> misses {[r[0] for r in mr if not r[4]]} {'ok' if missc else 'WRONG'}; by 0.09% (the 4th digit) -> still a miss {'ok' if near else 'WRONG'}")
    bad = (not same_as_issue) + (not okc) + (not missc) + (not near)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def say(msg, name="run_745.log"):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(HERE, "logs", name), "a") as f:
        f.write(line + "\n")


def rss_mb(pid):
    try:
        for ln in open(f"/proc/{pid}/status"):
            if ln.startswith("VmRSS"):
                return int(ln.split()[1]) / 1024
    except OSError:
        pass
    return float("nan")


def kill_group(p):
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except OSError:
        pass


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for path in (STATE, LAUNCH, PY):
        if not os.path.exists(path):
            say(f"missing {path}")
            sys.exit(2)
    ref = {i: v[0] for i, v in parse(REF_LOG).items() if i < 3}
    if ref != ISSUE:
        say("reference from #681's log does not equal the issue's numbers")
        sys.exit(2)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=MDSITE)
    log = os.path.join(HERE, "logs", "main_1000.log")
    cmd = [PY, "-u", LAUNCH, os.path.join(WT, "solver", "rt", "rt_sigma.py"), STATE, "--starts", str(NSTARTS), "--rough", "--max_products", str(MAXPROD)]
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=WT, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env, start_new_session=True, preexec_fn=lambda: os.nice(10))
    say(f"start main_1000 (pid {p.pid}) --max_products {MAXPROD} --starts {NSTARTS}, {THREADS} BLAS threads, nice 10")
    seen, code, last_res, nstart = 0, 0, 0.0, 0
    while True:
        time.sleep(10)
        for i, b, r, d, ok in compare(parse(log), ref):
            if i >= seen:
                say(f"control start {i}: {b} vs #720 {r}, relative difference {d:.1e}, {'equal' if ok else 'MISS'}", "control_745.log")
                seen = i + 1
                if not ok and not code:
                    code = 3
                    open(os.path.join(HERE, "logs", "control_745_MISS.txt"), "w").write(f"start {i}: {b} vs #720 {r}, relative difference {d:.2e}\n")
        n = len(parse(log))
        if n != nstart:
            nstart = n
            say(f"{n} starts printed", "progress_745.log")
        if time.time() - last_res > 600:
            last_res = time.time()
            say(f"elapsed {(time.time() - t0) / 3600:.2f} h, rss {rss_mb(p.pid):.0f} MB, load {os.getloadavg()[0]:.2f}, {nstart} starts printed", "resource.log")
        if os.path.exists(os.path.join(HERE, "STOP_745")):
            code = code or 4
        if time.time() - t0 > CAP_H * 3600:
            code = code or 5
        if code:
            kill_group(p)
            open(os.path.join(HERE, "logs", "main_1000.exit"), "w").write(f"killed {code}\n")
            say(f"main_1000 killed (code {code}: 3 control miss, 4 STOP_745, 5 {CAP_H:g} h cap)")
            sys.exit(code)
        rc = p.poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", "main_1000.exit"), "w").write(f"{rc}\n")
            say(f"main_1000 exit {rc} after {(time.time() - t0) / 3600:.2f} h")
            sys.exit(0 if rc == 0 else 6)


if __name__ == "__main__":
    main()
