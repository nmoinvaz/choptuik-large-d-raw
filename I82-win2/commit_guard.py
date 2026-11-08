#!/usr/bin/env python3
"""Second memory guard for #82 (coordinator's decision of 2026-11-08): kill the process trees of the PIDs when the
commit charge comes within MIN_HEADROOM_GB of the commit limit, whatever the free memory. It runs beside
util_report.py --guard 6, which fires on free memory under 6 GB; the pair is the coordinator's "6 GB free, and the
commit charge at least 10 GB below the limit". Same reading as util_report.py (GlobalMemoryStatusEx: charge =
ullTotalPageFile - ullAvailPageFile, limit = ullTotalPageFile), same kill (taskkill /T /F), same log line start.

    python commit_guard.py MIN_HEADROOM_GB LOG INTERVAL_S PID...     exit 3 when it fired, 0 when every PID ended
    python commit_guard.py --selftest                                 a threshold above the machine's headroom kills a
                                                                      sleeping child (exit 3), a threshold of 0 does not
"""
import os, subprocess, sys, tempfile, time, datetime as dt

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-t126")
import util_report as u  # kill_tree and alive, the same functions the free-memory guard uses
import ctypes

GB = 1024.0 ** 3


class MS(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def commit():
    """(charge_gb, limit_gb)"""
    m = MS(); m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return (m.ullTotalPageFile - m.ullAvailPageFile) / GB, m.ullTotalPageFile / GB


def guard(min_headroom, log, interval, pids, max_iter=None):
    n = 0
    while max_iter is None or n < max_iter:
        n += 1
        charge, limit = commit()
        if limit - charge < min_headroom:
            for p in pids:
                u.kill_tree(p)
            with open(log, "a") as f:
                f.write(f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M UTC}  stopped {' '.join(map(str, pids))}: "
                        f"commit {charge:.1f} of {limit:.1f} GB, headroom {limit - charge:.1f} GB < {min_headroom} GB\n")
            return 3
        if not any(u.alive(p) for p in pids):
            return 0
        if max_iter is None or n < max_iter:
            time.sleep(interval)
    return 0


def selftest():
    charge, limit = commit()
    with tempfile.TemporaryDirectory() as d:
        log = os.path.join(d, "g.log")
        c1 = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"]); time.sleep(0.5)
        fired = guard(limit - charge + 1.0, log, 0, [c1.pid], max_iter=1)
        for _ in range(50):
            if c1.poll() is not None: break
            time.sleep(0.1)
        dead = c1.poll() is not None
        c2 = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"]); time.sleep(0.5)
        quiet = guard(0.0, log, 0, [c2.pid], max_iter=1)
        alive2 = c2.poll() is None
        u.kill_tree(c2.pid); c2.wait()
        line = open(log).read().strip()
    print(f"selftest: commit {charge:.1f} of {limit:.1f} GB; threshold above headroom -> exit {fired} (want 3), child dead "
          f"{dead} (want True); threshold 0 -> exit {quiet} (want 0), child alive {alive2} (want True)\n  log line: {line}")
    return 0 if (fired, dead, quiet, alive2) == (3, True, 0, True) else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    a = sys.argv[1:]
    if len(a) < 4:
        print(__doc__); sys.exit(2)
    pids = [int(x) for x in a[3:]]
    print(f"commit guard: stop {pids} when commit headroom < {a[0]} GB, every {a[2]} s, log {a[1]}", flush=True)
    sys.exit(guard(float(a[0]), a[1], float(a[2]), pids))
