#!/usr/bin/env python3
"""#745: start a's twelve rough bounds at D 40.02 at 1000 products. rt_sigma.py --starts 12 --rough --max_products 1000 on I671-win/solves/k7_D40_D40.0201_32x121.npz.
2 BLAS threads, BelowNormal. Windows port of I745-rpi5/run_745.py (itself from I720-win2/run_720.py), the same control and stop rules.

usage: python run_745.py                (logs/main_1000.log, logs/main_1000.exit, logs/run_745.log, logs/control_745.log, logs/progress_745.log, logs/resource.log)
       python run_745.py --selftest     the control comparison on #681's own log: identical must pass, a 1% change of one printed bound must miss

Control (the issue's acceptance 1): starts 0 to 2 print #720's bounds (1.257e-34, 9.921e-34, 7.797e-34). Rule, fixed before the run: the printed number (four significant digits of the
log line) equals the issue's. Each start is compared as it appears; the first miss stops the task (the process tree killed, logs/control_745_MISS.txt, exit 3).
A file STOP_745 stops the task (exit 4); a run unfinished after CAP_H hours is killed (exit 5) and reported with what it printed."""
import ctypes
import ctypes.wintypes as wt
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"D:\choptuik-i745"
PY = r"C:\Users\nathan\Source\venv-t177\Scripts\python.exe"
RAW = r"D:\choptuik-i935-raw"
LAUNCH = os.path.join(HERE, "rt_launch.py")
STATE = os.path.join(RAW, "I671-win", "solves", "k7_D40_D40.0201_32x121.npz")
REF_LOG = os.path.join(RAW, "I681-win", "logs", "K7_D40_rough.log")
ISSUE = {0: "1.257e-34", 1: "9.921e-34", 2: "7.797e-34"}
NSTARTS = 12
MAXPROD = 1000
THREADS = "2"
CAP_H = 8.0
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


class _FT(ctypes.Structure):
    _fields_ = [("lo", wt.DWORD), ("hi", wt.DWORD)]


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]


def proc_stats(pid):
    """(working set MB, peak working set MB, cpu seconds) of a process, nan when it cannot be read"""
    k32, ps = ctypes.WinDLL("kernel32"), ctypes.WinDLL("psapi")
    k32.OpenProcess.restype = wt.HANDLE
    h = k32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return float("nan"), float("nan"), float("nan")
    try:
        pmc = _PMC()
        pmc.cb = ctypes.sizeof(_PMC)
        ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]
        ok = ps.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb)
        c, e, k, u = _FT(), _FT(), _FT(), _FT()
        k32.GetProcessTimes.argtypes = [wt.HANDLE] + [ctypes.POINTER(_FT)] * 4
        t = k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(k), ctypes.byref(u))
        cpu = ((k.hi << 32 | k.lo) + (u.hi << 32 | u.lo)) / 1e7 if t else float("nan")
        return (pmc.WorkingSetSize / 2**20, pmc.PeakWorkingSetSize / 2**20, cpu) if ok else (float("nan"), float("nan"), cpu)
    finally:
        k32.CloseHandle(h)


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


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
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1")
    log = os.path.join(HERE, "logs", "main_1000.log")
    cmd = [PY, "-u", LAUNCH, os.path.join(WT, "solver", "rt", "rt_sigma.py"), STATE, "--starts", str(NSTARTS), "--rough", "--max_products", str(MAXPROD)]
    t0 = time.time()
    # BELOW_NORMAL_PRIORITY_CLASS | CREATE_NO_WINDOW
    p = subprocess.Popen(cmd, cwd=WT, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=env, creationflags=0x00004000 | 0x08000000)
    say(f"start main_1000 (pid {p.pid}) --max_products {MAXPROD} --starts {NSTARTS}, {THREADS} BLAS threads, BelowNormal")
    seen, code, last_res, nstart, peak = 0, 0, 0.0, 0, 0.0
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
        ws, pk, cpu = proc_stats(p.pid)
        peak = max(peak, pk) if pk == pk else peak
        if time.time() - last_res > 600:
            last_res = time.time()
            el = time.time() - t0
            say(f"elapsed {el / 3600:.2f} h, working set {ws:.0f} MB, peak {peak:.0f} MB, cpu {cpu / 60:.1f} min ({cpu / el:.2f} busy threads averaged), {nstart} starts printed", "resource.log")
        if os.path.exists(os.path.join(HERE, "STOP_745")):
            code = code or 4
        if time.time() - t0 > CAP_H * 3600:
            code = code or 5
        if code:
            kill_tree(p)
            open(os.path.join(HERE, "logs", "main_1000.exit"), "w").write(f"killed {code}\n")
            say(f"main_1000 killed (code {code}: 3 control miss, 4 STOP_745, 5 {CAP_H:g} h cap)")
            sys.exit(code)
        rc = p.poll()
        if rc is not None:
            open(os.path.join(HERE, "logs", "main_1000.exit"), "w").write(f"{rc}\n")
            say(f"main_1000 exit {rc} after {(time.time() - t0) / 3600:.2f} h, peak working set {peak:.0f} MB, cpu {cpu / 60:.1f} min")
            sys.exit(0 if rc == 0 else 6)


if __name__ == "__main__":
    main()
